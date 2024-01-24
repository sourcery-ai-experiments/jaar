from src._prime.road import default_road_delimiter_if_none, RoadUnit, HealerID

# from src.agenda.party import partylink_shop
# from src.agenda.group import groupunit_shop
# from src.agenda.idea import assigned_unit_shop
from src.agenda.agenda import agendaunit_shop, balancelink_shop
from src.economy.economy import EconomyUnit, EconomyID
from src.world.deal import DealUnit
from src.world.problem import (
    ProblemID,
    problemunit_shop,
    healerlink_shop,
    economylink_shop,
)
from src.world.person import PersonID, PersonUnit, personunit_shop
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


class PersonExistsException(Exception):
    pass


class WorldMark(str):  # Created to help track the concept
    pass


@dataclass
class WorldUnit:
    mark: WorldMark
    worlds_dir: str
    _world_dir: str = None
    _persons_dir: str = None
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

    def _set_world_dirs(self):
        self._world_dir = f"{self.worlds_dir}/{self.mark}"
        self._persons_dir = f"{self._world_dir}/persons"
        self._deals_dir = f"{self._world_dir}/deals"

    def personunit_exists(self, person_id: PersonID):
        return self._personunits.get(person_id) != None

    def _set_person_in_memory(self, personunit: PersonUnit):
        self._personunits[personunit.pid] = personunit

    def set_personunit(
        self,
        person_id: PersonID,
        replace_personunit: bool = False,
        replace_alert: bool = True,
    ):
        x_personunit = personunit_shop(
            person_id,
            self._get_person_dir(person_id),
            _road_delimiter=self._road_delimiter,
        )
        if self.personunit_exists(x_personunit.pid) == False and not replace_personunit:
            self._set_person_in_memory(x_personunit)
        elif replace_alert:
            raise PersonExistsException(
                f"set_personunit fail: {x_personunit.pid} already exists"
            )

    def get_personunit_from_memory(self, person_id: PersonID) -> PersonUnit:
        return self._personunits.get(person_id)

    def add_economy_connection(
        self,
        treasurer_pid: PersonID,
        economy_id: EconomyID,
        clerk_person_id: PersonID,
    ):
        if self.personunit_exists(treasurer_pid) == False:
            self.set_personunit(treasurer_pid)
        x_personunit = self.get_personunit_from_memory(treasurer_pid)

        if x_personunit.economyunit_exists(economy_id) == False:
            x_personunit.set_economyunit(economy_id)
        x_economy = x_personunit.get_economyunit(economy_id)

        if self.personunit_exists(clerk_person_id) == False:
            self.set_personunit(clerk_person_id)

        if x_economy.clerkunit_exists(treasurer_pid) == False:
            x_economy.add_clerkunit(treasurer_pid)
        if x_economy.clerkunit_exists(clerk_person_id) == False:
            x_economy.add_clerkunit(clerk_person_id)

    def get_priority_agenda(self, person_id: PersonID):
        x_personunit = self.get_personunit_from_memory(person_id)
        x_agenda = agendaunit_shop(person_id)
        for x_problemunit in x_personunit._problems.values():
            for x_healerlink in x_problemunit._healerlinks.values():
                healer_personunit = self.get_personunit_from_memory(
                    x_healerlink.healer_id
                )
                for x_economylink in x_healerlink._economylinks.values():
                    x_economyunit = healer_personunit.get_economyunit(
                        x_economylink.economy_id
                    )
                    forum_agenda = x_economyunit.get_forum_agenda(person_id)
                    forum_agenda.set_economy_id(x_agenda._economy_id)
                    x_agenda.meld(forum_agenda)
        return x_agenda

    def create_person_economy(
        self,
        person_id: PersonID,
        x_problem_id: ProblemID,
        healer_id: HealerID,
        economy_id: EconomyID,
    ):
        x_healerlink = healerlink_shop(healer_id)
        x_healerlink.set_economylink(economylink_shop(economy_id))
        x_problemunit = problemunit_shop(x_problem_id)
        x_problemunit.set_healerlink(x_healerlink)

        self.set_personunit(person_id, replace_personunit=False, replace_alert=False)
        x_personunit = self.get_personunit_from_memory(person_id)
        x_personunit.set_problemunit(x_problemunit)

        self.set_personunit(healer_id, replace_personunit=False, replace_alert=False)
        healer_personunit = self.get_personunit_from_memory(healer_id)
        healer_personunit.set_economyunit(economy_id, False, x_problem_id)
        x_economyunit = healer_personunit.get_economyunit(economy_id)
        x_economyunit.full_setup_clerkunit(healer_id)
        if healer_id != x_personunit.pid:
            self._set_partyunit(x_economyunit, x_personunit.pid, healer_id)

    def _set_partyunit(
        self, x_economyunit: EconomyUnit, person_id: PersonID, party_id: PersonID
    ):
        x_economyunit.full_setup_clerkunit(person_id)
        person_clerkunit = x_economyunit.get_clerkunit(person_id)
        person_contract = person_clerkunit.get_contract()
        person_contract.add_partyunit(party_id)
        person_clerkunit.save_contract_agenda(person_contract)
        person_clerkunit.save_refreshed_output_to_forum()


def worldunit_shop(
    mark: WorldMark, worlds_dir: str, _road_delimiter: str = None
) -> WorldUnit:
    world_x = WorldUnit(
        mark=mark,
        worlds_dir=worlds_dir,
        _personunits=get_empty_dict_if_none(None),
        _dealunits=get_empty_dict_if_none(None),
    )
    world_x.set_max_deal_uid()
    world_x._set_world_dirs()
    world_x._road_delimiter = default_road_delimiter_if_none(_road_delimiter)
    return world_x
