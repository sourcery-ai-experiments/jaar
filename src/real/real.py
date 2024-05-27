from src._instrument.python import get_empty_dict_if_none
from src._instrument.file import set_dir, delete_dir, dir_files
from src._road.finance import default_planck_if_none
from src._road.road import default_road_delimiter_if_none, PersonID, RoadUnit, RealID
from src.agenda.agenda import agendaunit_shop, AgendaUnit
from src.econ.econ import EconUnit
from src.real.gift import get_gifts_folder
from src.real.engine import EngineUnit, engineunit_shop
from src.real.nook import (
    nookunit_shop,
    _save_work_file as person_save_work_file,
    get_duty_file_agenda,
    nookunit_create_core_dir_and_files,
    get_work_file_agenda,
)
from src.real.journal_sqlstr import get_create_table_if_not_exist_sqlstrs
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from copy import deepcopy as copy_deepcopy


class PersonExistsException(Exception):
    pass


@dataclass
class RealUnit:
    real_id: RealID
    reals_dir: str
    _real_dir: str = None
    _persons_dir: str = None
    _journal_db: str = None
    _engineunits: dict[PersonID:EngineUnit] = None
    _gifts_dir: str = None
    _road_delimiter: str = None
    _planck: float = None

    # directory setup
    def _set_real_dirs(self, in_memory_journal: bool = None):
        self._real_dir = f"{self.reals_dir}/{self.real_id}"
        self._persons_dir = f"{self._real_dir}/persons"
        self._gifts_dir = f"{self._real_dir}/{get_gifts_folder()}"
        set_dir(x_path=self._real_dir)
        set_dir(x_path=self._persons_dir)
        set_dir(x_path=self._gifts_dir)
        self._create_journal_db(in_memory=in_memory_journal)

    def _get_person_dir(self, person_id):
        return f"{self._persons_dir}/{person_id}"

    def _get_person_folder_names(self) -> set:
        persons = dir_files(self._persons_dir, include_dirs=True, include_files=False)
        return set(persons.keys())

    def get_person_paths(self):
        x_person_ids = self._get_person_folder_names()
        return {f"{self._persons_dir}/{x_person_id}" for x_person_id in x_person_ids}

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
    def _set_engineunit_in_memory(self, engineunit: EngineUnit):
        self._engineunits[engineunit.nook.person_id] = engineunit

    def engineunit_exists_in_memory(self, person_id: PersonID):
        return self._engineunits.get(person_id) != None

    def add_engineunit(
        self,
        person_id: PersonID,
        replace_engineunit: bool = False,
        replace_alert: bool = True,
    ) -> EngineUnit:
        x_engineunit = engineunit_shop(
            person_id=person_id,
            real_id=self.real_id,
            reals_dir=self.reals_dir,
            _road_delimiter=self._road_delimiter,
        )
        x_nookunit = nookunit_shop(
            self.reals_dir, self.real_id, person_id, self._road_delimiter
        )
        nookunit_create_core_dir_and_files(x_nookunit)
        if (
            self.engineunit_exists_in_memory(x_engineunit.nook.person_id) == False
            and not replace_engineunit
        ):
            self._set_engineunit_in_memory(x_engineunit)
        elif replace_alert:
            raise PersonExistsException(
                f"add_engineunit fail: {x_engineunit.nook.person_id} already exists"
            )
        return self.get_engineunit_from_memory(person_id)

    def get_engineunit_from_memory(self, person_id: PersonID) -> EngineUnit:
        return self._engineunits.get(person_id)

    def get_person_duty_from_file(self, person_id: PersonID) -> AgendaUnit:
        x_nookunit = nookunit_shop(
            self.reals_dir, self.real_id, person_id, self._road_delimiter
        )
        return get_duty_file_agenda(x_nookunit)

    def set_person_econunits_dirs(self, person_id: PersonID):
        x_duty = self.get_person_duty_from_file(person_id)
        x_duty.calc_agenda_metrics()
        for healer_id, healer_dict in x_duty._healers_dict.items():
            healer_person = self.get_engineunit_from_memory(healer_id)
            for econ_idea in healer_dict.values():
                self._set_person_econunits_agent_contract(
                    healer_person=healer_person,
                    econ_road=econ_idea.get_road(),
                    duty_agenda=x_duty,
                )

    def _set_person_econunits_agent_contract(
        self,
        healer_person: EngineUnit,
        econ_road: RoadUnit,
        duty_agenda: AgendaUnit,
    ):
        x_econ = healer_person.get_econ(econ_road)
        x_econ.save_role_file(duty_agenda)

    # work agenda management
    def generate_work_agenda(self, person_id: PersonID) -> AgendaUnit:
        x_engineunit = self.get_engineunit_from_memory(person_id)
        x_nookunit = nookunit_shop(
            self.reals_dir, self.real_id, person_id, self._road_delimiter, self._planck
        )
        x_duty = get_duty_file_agenda(x_nookunit)
        x_duty.calc_agenda_metrics()

        x_work = agendaunit_shop(person_id, self.real_id)
        x_work_deepcopy = copy_deepcopy(x_work)
        for healer_id, healer_dict in x_duty._healers_dict.items():
            healer_person = self.get_engineunit_from_memory(healer_id)
            healer_person.create_person_econunits(x_nookunit)
            for econ_idea in healer_dict.values():
                x_econ = healer_person.get_econ(econ_idea.get_road())
                x_econ.save_role_file(x_duty)
                x_job = x_econ.create_job_file_from_role_file(person_id)
                x_job.calc_agenda_metrics()
                x_work.meld(x_job)
                x_work.calc_agenda_metrics

        # if work_agenda has not changed st work agenda to duty
        if x_work == x_work_deepcopy:
            x_work = x_duty
        person_save_work_file(x_nookunit, x_work)
        return self.get_work_file_agenda(person_id)

    def generate_all_work_agendas(self):
        for x_person_id in self._get_person_folder_names():
            self.generate_work_agenda(x_person_id)

    def get_work_file_agenda(self, person_id: PersonID) -> AgendaUnit:
        x_engineunit = self.get_engineunit_from_memory(person_id)
        x_nookunit = nookunit_shop(
            self.reals_dir, self.real_id, person_id, self._road_delimiter, self._planck
        )
        return get_work_file_agenda(x_nookunit)

    # def _set_partyunit(
    #     self, x_econunit: EconUnit, person_id: PersonID, party_id: PersonID
    # ):
    #     person_role.add_partyunit(party_id)
    #     .save_refreshed_job_to_jobs()

    # def _display_duty_party_graph(self, x_person_id: PersonID):
    #     x_engineunit = self.get_engineunit_from_memory(x_person_id)
    #     x_duty_agenda = get_duty_file_agenda(x_engineunit.nook)

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
        _engineunits=get_empty_dict_if_none(None),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _planck=default_planck_if_none(_planck),
    )
    real_x._set_real_dirs(in_memory_journal=in_memory_journal)
    return real_x
