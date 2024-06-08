from src._instrument.file import set_dir, delete_dir, dir_files
from src._road.jaar_config import get_changes_folder
from src._road.finance import default_planck_if_none
from src._road.road import default_road_delimiter_if_none, PersonID, RoadUnit, RealID
from src.agenda.agenda import AgendaUnit
from src.change.filehub import filehub_shop, FileHub, pipeline_duty_work_text
from src.change.listen import listen_to_speaker_intent, listen_to_debtors_roll
from src.econ.econ import create_job_file_from_role_file
from src.real.econ_creator import create_person_econunits, get_econunit
from src.real.admin_duty import initialize_change_duty_files
from src.real.admin_work import initialize_work_file, get_default_work_agenda
from src.real.journal_sqlstr import get_create_table_if_not_exist_sqlstrs
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from copy import deepcopy as copy_deepcopy


@dataclass
class RealUnit:
    """Data pipelines:
    pipeline1: changes->duty
    pipeline2: duty->roles
    pipeline3: role->job
    pipeline4: job->work
    pipeline5: duty->work (direct)
    pipeline6: duty->job->work (through jobs)
    pipeline7: changes->work (could be 5 of 6)
    """

    real_id: RealID
    reals_dir: str
    _real_dir: str = None
    _persons_dir: str = None
    _journal_db: str = None
    _changes_dir: str = None
    _road_delimiter: str = None
    _planck: float = None

    # directory setup
    def _set_real_dirs(self, in_memory_journal: bool = None):
        self._real_dir = f"{self.reals_dir}/{self.real_id}"
        self._persons_dir = f"{self._real_dir}/persons"
        self._changes_dir = f"{self._real_dir}/{get_changes_folder()}"
        set_dir(x_path=self._real_dir)
        set_dir(x_path=self._persons_dir)
        set_dir(x_path=self._changes_dir)
        self._create_journal_db(in_memory=in_memory_journal)

    def _get_person_dir(self, person_id):
        return f"{self._persons_dir}/{person_id}"

    def _get_person_folder_names(self) -> set:
        persons = dir_files(self._persons_dir, include_dirs=True, include_files=False)
        return set(persons.keys())

    def get_person_filehubs(self) -> dict[PersonID:FileHub]:
        x_person_ids = self._get_person_folder_names()
        return {
            x_person_id: filehub_shop(
                reals_dir=self.reals_dir,
                real_id=self.real_id,
                person_id=x_person_id,
                econ_road=None,
                nox_type=None,
                road_delimiter=self._road_delimiter,
                planck=self._planck,
            )
            for x_person_id in x_person_ids
        }

    # database
    def get_journal_db_path(self) -> str:
        return f"{self.reals_dir}/{self.real_id}/journal.db"

    def _create_journal_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> Connection:
        journal_file_new = False
        if overwrite:
            journal_file_new = True
            self._delete_journal()

        if in_memory:
            if self._journal_db is None:
                journal_file_new = True
            self._journal_db = sqlite3_connect(":memory:")
        else:
            sqlite3_connect(self.get_journal_db_path())

        if journal_file_new:
            with self.get_journal_conn() as journal_conn:
                for sqlstr in get_create_table_if_not_exist_sqlstrs():
                    journal_conn.execute(sqlstr)

    def _delete_journal(self):
        self._journal_db = None
        delete_dir(dir=self.get_journal_db_path())

    def get_journal_conn(self) -> Connection:
        if self._journal_db is None:
            return sqlite3_connect(self.get_journal_db_path())
        else:
            return self._journal_db

    # person management
    def _get_filehub(self, person_id: PersonID) -> FileHub:
        return filehub_shop(
            person_id=person_id,
            real_id=self.real_id,
            reals_dir=self.reals_dir,
            econ_road=None,
            road_delimiter=self._road_delimiter,
            planck=self._planck,
        )

    def init_person_econs(self, person_id: PersonID):
        x_filehub = self._get_filehub(person_id)
        initialize_change_duty_files(x_filehub)
        initialize_work_file(x_filehub, self.get_person_duty_from_file(person_id))

    def get_person_duty_from_file(self, person_id: PersonID) -> AgendaUnit:
        return self._get_filehub(person_id).get_duty_agenda()

    def set_person_econunits_dirs(self, person_id: PersonID):
        x_duty = self.get_person_duty_from_file(person_id)
        x_duty.calc_agenda_metrics()
        for healer_id, healer_dict in x_duty._healers_dict.items():
            healer_filehub = filehub_shop(
                self.reals_dir,
                self.real_id,
                healer_id,
                econ_road=None,
                nox_type="role_job",
                road_delimiter=self._road_delimiter,
                planck=self._planck,
            )
            for econ_idea in healer_dict.values():
                self._set_person_econunits_agent_contract(
                    healer_filehub=healer_filehub,
                    econ_road=econ_idea.get_road(),
                    duty_agenda=x_duty,
                )

    def _set_person_econunits_agent_contract(
        self,
        healer_filehub: FileHub,
        econ_road: RoadUnit,
        duty_agenda: AgendaUnit,
    ):
        x_econ = get_econunit(healer_filehub, econ_road)
        x_econ.filehub.save_role_agenda(duty_agenda)

    # work agenda management
    def generate_work_agenda(self, person_id: PersonID) -> AgendaUnit:
        listener_filehub = self._get_filehub(person_id)
        x_duty = listener_filehub.get_duty_agenda()
        x_duty.calc_agenda_metrics()
        x_work = get_default_work_agenda(x_duty)
        for healer_id, healer_dict in x_duty._healers_dict.items():
            healer_filehub = filehub_shop(
                reals_dir=self.reals_dir,
                real_id=self.real_id,
                person_id=healer_id,
                econ_road=None,
                nox_type="role_job",
                road_delimiter=self._road_delimiter,
                planck=self._planck,
            )
            create_person_econunits(healer_filehub)
            for econ_road in healer_dict.keys():
                econ_filehub = filehub_shop(
                    reals_dir=self.reals_dir,
                    real_id=self.real_id,
                    person_id=healer_id,
                    econ_road=econ_road,
                    nox_type="role_job",
                    road_delimiter=self._road_delimiter,
                    planck=self._planck,
                )
                econ_filehub.save_role_agenda(x_duty)
                x_job = create_job_file_from_role_file(econ_filehub, person_id)
                listen_to_speaker_intent(x_work, x_job)

        # if nothing has come from duty->role->job->work pipeline use duty->work pipeline
        x_work.calc_agenda_metrics()
        if len(x_work._idea_dict) == 1:
            listener_filehub.set_nox_type(pipeline_duty_work_text())
            x_work = listen_to_debtors_roll(x_work, listener_filehub)
            x_work.calc_agenda_metrics()
        if len(x_work._idea_dict) == 1:
            x_work = x_duty
        listener_filehub.save_work_agenda(x_work)

        return self.get_work_file_agenda(person_id)

    def generate_all_work_agendas(self):
        for x_person_id in self._get_person_folder_names():
            self.generate_work_agenda(x_person_id)

    def get_work_file_agenda(self, person_id: PersonID) -> AgendaUnit:
        return self._get_filehub(person_id).get_work_agenda()

    # def _set_partyunit(
    #     self, x_econunit: EconUnit, person_id: PersonID, party_id: PersonID
    # ):
    #     person_role.add_partyunit(party_id)
    #     .save_refreshed_job_to_jobs()

    # def _display_duty_party_graph(self, x_person_id: PersonID):
    #     x_duty_agenda = x_filehub.get_duty_agenda()

    # def display_person_kpi_graph(self, x_person_id: PersonID):
    #     pass


def realunit_shop(
    real_id: RealID,
    reals_dir: str,
    in_memory_journal: bool = None,
    _road_delimiter: str = None,
    _planck: float = None,
) -> RealUnit:
    real_x = RealUnit(
        real_id=real_id,
        reals_dir=reals_dir,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _planck=default_planck_if_none(_planck),
    )
    real_x._set_real_dirs(in_memory_journal=in_memory_journal)
    return real_x
