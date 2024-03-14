from src._road.finance import default_planck_if_none
from src._road.road import default_road_delimiter_if_none, PersonID, RoadUnit, WorldID
from src.agenda.agenda import agendaunit_shop, AgendaUnit
from src.econ.econ import EconUnit, EconID
from src.world.gift import GiftUnit
from src.world.person import PersonUnit, personunit_shop
from src.world.journal_sqlstr import get_create_table_if_not_exist_sqlstrs
from src.instrument.python import get_empty_dict_if_none
from src.instrument.file import set_dir, open_file, delete_dir, dir_files
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from copy import deepcopy as copy_deepcopy


class PersonExistsException(Exception):
    pass


@dataclass
class WorldUnit:
    world_id: WorldID
    worlds_dir: str
    _world_dir: str = None
    _persons_dir: str = None
    _journal_db: str = None
    _personunits: dict[PersonID:PersonUnit] = None
    _gifts_dir: str = None
    _giftunits: dict[PersonID:PersonUnit] = None
    _max_gift_uid: int = None
    _road_delimiter: str = None
    _planck: float = None

    def del_giftunit(self, giftunit_uid: int):
        self._giftunits.pop(giftunit_uid)

    def giftunit_exists(self, giftunit_uid: int) -> bool:
        return self.get_giftunit(giftunit_uid) != None

    def get_giftunit(self, giftunit_uid: int) -> GiftUnit:
        return self._giftunits.get(giftunit_uid)

    def set_giftunit(self, x_giftunit: GiftUnit):
        new_uid = self._max_gift_uid + 1
        self._giftunits[new_uid] = x_giftunit
        self.set_max_gift_uid(new_uid)
        return new_uid

    def set_max_gift_uid(self, new_uid: int = None):
        self._max_gift_uid = 0 if self._max_gift_uid is None else new_uid

    def _get_person_dir(self, person_id):
        return f"{self._persons_dir}/{person_id}"

    def _set_world_dirs(self, in_memory_journal: bool = None):
        self._world_dir = f"{self.worlds_dir}/{self.world_id}"
        self._persons_dir = f"{self._world_dir}/persons"
        self._gifts_dir = f"{self._world_dir}/gifts"
        set_dir(x_path=self._world_dir)
        set_dir(x_path=self._persons_dir)
        set_dir(x_path=self._gifts_dir)
        self._create_journal_db(in_memory=in_memory_journal)

    def get_journal_db_path(self) -> str:
        return f"{self.worlds_dir}/{self.world_id}/journal.db"

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

    def personunit_exists(self, person_id: PersonID):
        return self._personunits.get(person_id) != None

    def _set_person_in_memory(self, personunit: PersonUnit):
        self._personunits[personunit.person_id] = personunit

    def add_personunit(
        self,
        person_id: PersonID,
        replace_personunit: bool = False,
        replace_alert: bool = True,
    ) -> PersonUnit:
        x_personunit = personunit_shop(
            person_id=person_id,
            world_id=self.world_id,
            worlds_dir=self.worlds_dir,
            _road_delimiter=self._road_delimiter,
        )
        x_personunit.create_core_dir_and_files()
        if (
            self.personunit_exists(x_personunit.person_id) == False
            and not replace_personunit
        ):
            self._set_person_in_memory(x_personunit)
        elif replace_alert:
            raise PersonExistsException(
                f"add_personunit fail: {x_personunit.person_id} already exists"
            )
        return self.get_personunit(person_id)

    def _get_person_ids(self) -> set:
        persons = dir_files(self._persons_dir, include_dirs=True, include_files=False)
        return set(persons.keys())

    def get_person_paths(self):
        x_person_ids = self._get_person_ids()
        return {f"{self._persons_dir}/{x_person_id}" for x_person_id in x_person_ids}

    def get_personunit(self, person_id: PersonID) -> PersonUnit:
        return self._personunits.get(person_id)

    def get_person_gut(self, person_id: PersonID) -> AgendaUnit:
        x_person = self.get_personunit(person_id)
        return x_person.get_gut_file_agenda()

    def set_all_econunits_contract(self, person_id: PersonID):
        x_gut = self.get_person_gut(person_id)
        x_gut.set_agenda_metrics()
        for healer_id, healer_dict in x_gut._healers_dict.items():
            healer_person = self.get_personunit(healer_id)
            for econ_idea in healer_dict.values():
                self._set_person_econunits_agent_contract(
                    healer_person=healer_person,
                    econ_road=econ_idea.get_road(),
                    gut_agenda=x_gut,
                )

    def _set_person_econunits_agent_contract(
        self,
        healer_person: PersonID,
        econ_road: RoadUnit,
        gut_agenda: AgendaUnit,
    ):
        x_econ = healer_person.get_econ(econ_road)
        x_econ.create_new_clerkunit(gut_agenda._owner_id)
        x_clerk = x_econ.get_clerkunit(gut_agenda._owner_id)
        x_clerk.save_role_agenda(gut_agenda)

    def add_econ_connection(
        self,
        treasurer_person_id: PersonID,
        econ_id: EconID,
        clerk_person_id: PersonID,
    ):
        if self.personunit_exists(treasurer_person_id) == False:
            self.add_personunit(treasurer_person_id)
        x_personunit = self.get_personunit(treasurer_person_id)

        if x_personunit.econunit_exists(econ_id) == False:
            x_personunit.set_econunit(econ_id)
        x_econ = x_personunit.get_econunit(econ_id)

        if self.personunit_exists(clerk_person_id) == False:
            self.add_personunit(clerk_person_id)

        if x_econ.clerkunit_exists(treasurer_person_id) == False:
            x_econ.add_clerkunit(treasurer_person_id)
        if x_econ.clerkunit_exists(clerk_person_id) == False:
            x_econ.add_clerkunit(clerk_person_id)

    def generate_outcome_agenda(self, person_id: PersonID) -> AgendaUnit:
        x_personunit = self.get_personunit(person_id)
        x_gut = x_personunit.get_gut_file_agenda()
        x_gut.set_agenda_metrics()

        x_outcome = agendaunit_shop(person_id, self.world_id)
        x_outcome_deepcopy = copy_deepcopy(x_outcome)
        for healer_id, healer_dict in x_gut._healers_dict.items():
            healer_person = self.get_personunit(healer_id)
            healer_person.create_person_econunits()
            for econ_idea in healer_dict.values():
                x_econ = healer_person.get_econ(econ_idea.get_road())
                x_econ.create_new_clerkunit(person_id)
                x_clerk = x_econ.get_clerkunit(person_id)
                x_clerk.save_refreshed_job_to_forum()
                x_job = x_econ.get_job_agenda_file(person_id)
                x_outcome.meld(x_job)

        # if outcome_agenda has not changed st outcome agenda to gut
        if x_outcome == x_outcome_deepcopy:
            x_outcome = x_gut
        x_personunit._save_outcome_file(x_outcome)
        return self.get_outcome_file_agenda(person_id)

    def generate_all_outcome_agendas(self):
        for x_person_id in self._get_person_ids():
            self.generate_outcome_agenda(x_person_id)

    def get_outcome_file_agenda(self, person_id: PersonID) -> AgendaUnit:
        x_personunit = self.get_personunit(person_id)
        return x_personunit.get_outcome_file_agenda()

    def _set_partyunit(
        self, x_econunit: EconUnit, person_id: PersonID, party_id: PersonID
    ):
        x_econunit.full_setup_clerkunit(person_id)
        person_clerkunit = x_econunit.get_clerkunit(person_id)
        person_role = person_clerkunit.get_role()
        person_role.add_partyunit(party_id)
        person_clerkunit.save_role_agenda(person_role)
        person_clerkunit.save_refreshed_job_to_forum()

    # def _display_gut_party_graph(self, x_person_id: PersonID):
    #     x_personunit = self.get_personunit(x_person_id)
    #     x_gut_agenda = x_personunit.get_gut_file_agenda()

    # def display_person_kpi_graph(self, x_person_id: PersonID):
    #     pass


def worldunit_shop(
    world_id: WorldID,
    worlds_dir: str,
    in_memory_journal: bool = None,
    _road_delimiter: str = None,
    _planck: float = None,
) -> WorldUnit:
    world_x = WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        _personunits=get_empty_dict_if_none(None),
        _giftunits=get_empty_dict_if_none(None),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _planck=default_planck_if_none(_planck),
    )
    world_x.set_max_gift_uid()
    world_x._set_world_dirs(in_memory_journal=in_memory_journal)
    return world_x
