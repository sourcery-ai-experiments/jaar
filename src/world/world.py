from src._road.road import (
    default_road_delimiter_if_none,
    HealerID,
    ProblemID,
    PersonID,
    RoadUnit,
)
from src.agenda.agenda import agendaunit_shop, AgendaUnit
from src.econ.econ import EconUnit, EconID
from src.world.deal import DealUnit
from src.world.person import PersonUnit, personunit_shop
from src.instrument.python import get_empty_dict_if_none
from src.instrument.file import set_dir
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


class PersonExistsException(Exception):
    pass


class WorldID(str):  # Created to help track the concept
    pass


@dataclass
class WorldUnit:
    world_id: WorldID
    worlds_dir: str
    _world_dir: str = None
    _persons_dir: str = None
    _history_db: str = None
    _personunits: dict[PersonID:PersonUnit] = None
    _deals_dir: str = None
    _dealunits: dict[PersonID:PersonUnit] = None
    _max_deal_uid: int = None
    _road_delimiter: str = None

    def del_dealunit(self, dealunit_uid: int):
        self._dealunits.pop(dealunit_uid)

    def dealunit_exists(self, dealunit_uid: int) -> bool:
        return self.get_dealunit(dealunit_uid) != None

    def get_dealunit(self, dealunit_uid: int) -> DealUnit:
        return self._dealunits.get(dealunit_uid)

    def set_dealunit(self, x_dealunit: DealUnit):
        new_uid = self._max_deal_uid + 1
        self._dealunits[new_uid] = x_dealunit
        self.set_max_deal_uid(new_uid)
        return new_uid

    def set_max_deal_uid(self, new_uid: int = None):
        self._max_deal_uid = 0 if self._max_deal_uid is None else new_uid

    def _get_person_dir(self, person_id):
        return f"{self._persons_dir}/{person_id}"

    def _set_world_dirs(self, in_memory_history_db: bool = None):
        self._world_dir = f"{self.worlds_dir}/{self.world_id}"
        self._persons_dir = f"{self._world_dir}/persons"
        self._deals_dir = f"{self._world_dir}/deals"
        set_dir(x_path=self._world_dir)
        set_dir(x_path=self._persons_dir)
        set_dir(x_path=self._deals_dir)
        self._create_history_db(in_memory=in_memory_history_db)

    def get_history_db_path(self) -> str:
        return f"{self.worlds_dir}/{self.world_id}/history.db"

    def _create_history_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> Connection:
        # if overwrite:
        #     self._delete_treasury()

        history_file_new = True
        if in_memory:
            self._history_db = sqlite3_connect(":memory:")
        else:
            sqlite3_connect(self.get_history_db_path())

        # if treasury_file_new:
        #     with self.get_treasury_conn() as treasury_conn:
        #         for sqlstr in get_create_table_if_not_exist_sqlstrs():
        #             treasury_conn.execute(sqlstr)

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
        return self.get_personunit_from_memory(person_id)

    def get_personunit_from_memory(self, person_id: PersonID) -> PersonUnit:
        return self._personunits.get(person_id)

    def get_person_gut(self, person_id: PersonID) -> AgendaUnit:
        x_person = self.get_personunit_from_memory(person_id)
        return x_person.get_gut_file_agenda()

    def set_all_econunits_contract(self, person_id: PersonID):
        x_gut = self.get_person_gut(person_id)
        x_gut.set_agenda_metrics()
        for healer_id, healer_dict in x_gut._healers_dict.items():
            healer_person = self.get_personunit_from_memory(healer_id)
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
        x_econ.create_new_clerkunit(gut_agenda._worker_id)
        x_clerk = x_econ.get_clerkunit(gut_agenda._worker_id)
        x_clerk.save_plan_agenda(gut_agenda)

    def add_econ_connection(
        self,
        treasurer_person_id: PersonID,
        econ_id: EconID,
        clerk_person_id: PersonID,
    ):
        if self.personunit_exists(treasurer_person_id) == False:
            self.add_personunit(treasurer_person_id)
        x_personunit = self.get_personunit_from_memory(treasurer_person_id)

        if x_personunit.econunit_exists(econ_id) == False:
            x_personunit.set_econunit(econ_id)
        x_econ = x_personunit.get_econunit(econ_id)

        if self.personunit_exists(clerk_person_id) == False:
            self.add_personunit(clerk_person_id)

        if x_econ.clerkunit_exists(treasurer_person_id) == False:
            x_econ.add_clerkunit(treasurer_person_id)
        if x_econ.clerkunit_exists(clerk_person_id) == False:
            x_econ.add_clerkunit(clerk_person_id)

    def get_work_agenda(self, person_id: PersonID):
        x_personunit = self.get_personunit_from_memory(person_id)
        work_agenda = agendaunit_shop(person_id)
        # for econ_idea in x_personunit._gut_obj._econ_dict.values():
        #     pass

        # for person_problemunit in x_personunit._problems.values():
        #             role_agenda = x_econunit.get_role_agenda(person_id)
        #             role_agenda.set_world_id(work_agenda._world_id)
        #             work_agenda.meld(role_agenda)
        return work_agenda

    def create_person_econ(
        self,
        person_id: PersonID,
        x_problem_id: ProblemID,
        healer_id: HealerID,
        econ_id: EconID,
    ):

        self.add_personunit(person_id, replace_personunit=False, replace_alert=False)
        x_personunit = self.get_personunit_from_memory(person_id)

        self.add_personunit(healer_id, replace_personunit=False, replace_alert=False)
        # healer_personunit = self.get_personunit_from_memory(healer_id)
        # healer_personunit.set_econunit(econ_id, False, x_problem_id)
        # x_econunit = healer_personunit.get_econunit(econ_id)
        # x_econunit.full_setup_clerkunit(healer_id)
        # if healer_id != x_personunit.person_id:
        #     self._set_partyunit(x_econunit, x_personunit.person_id, healer_id)

    def _set_partyunit(
        self, x_econunit: EconUnit, person_id: PersonID, party_id: PersonID
    ):
        x_econunit.full_setup_clerkunit(person_id)
        person_clerkunit = x_econunit.get_clerkunit(person_id)
        person_plan = person_clerkunit.get_plan()
        person_plan.add_partyunit(party_id)
        person_clerkunit.save_plan_agenda(person_plan)
        person_clerkunit.save_refreshed_output_to_forum()


def worldunit_shop(
    world_id: WorldID,
    worlds_dir: str,
    in_memory_history_db: bool = None,
    _road_delimiter: str = None,
) -> WorldUnit:
    world_x = WorldUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        _personunits=get_empty_dict_if_none(None),
        _dealunits=get_empty_dict_if_none(None),
    )
    world_x.set_max_deal_uid()
    world_x._set_world_dirs(in_memory_history_db=in_memory_history_db)
    world_x._road_delimiter = default_road_delimiter_if_none(_road_delimiter)
    return world_x
