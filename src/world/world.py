from src._prime.road import (
    default_road_delimiter_if_none,
    HealerID,
    ProblemID,
    PersonID,
)
from src.agenda.agenda import agendaunit_shop
from src.market.market import MarketUnit, MarketID
from src.world.deal import DealUnit
from src.world.person import PersonUnit, personunit_shop
from src.instrument.python import get_empty_dict_if_none
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
        self._personunits[personunit.person_id] = personunit

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
        if (
            self.personunit_exists(x_personunit.person_id) == False
            and not replace_personunit
        ):
            self._set_person_in_memory(x_personunit)
        elif replace_alert:
            raise PersonExistsException(
                f"set_personunit fail: {x_personunit.person_id} already exists"
            )

    def get_personunit_from_memory(self, person_id: PersonID) -> PersonUnit:
        return self._personunits.get(person_id)

    def add_market_connection(
        self,
        treasurer_person_id: PersonID,
        market_id: MarketID,
        clerk_person_id: PersonID,
    ):
        if self.personunit_exists(treasurer_person_id) == False:
            self.set_personunit(treasurer_person_id)
        x_personunit = self.get_personunit_from_memory(treasurer_person_id)

        if x_personunit.marketunit_exists(market_id) == False:
            x_personunit.set_marketunit(market_id)
        x_market = x_personunit.get_marketunit(market_id)

        if self.personunit_exists(clerk_person_id) == False:
            self.set_personunit(clerk_person_id)

        if x_market.clerkunit_exists(treasurer_person_id) == False:
            x_market.add_clerkunit(treasurer_person_id)
        if x_market.clerkunit_exists(clerk_person_id) == False:
            x_market.add_clerkunit(clerk_person_id)

    def get_world_agenda(self, person_id: PersonID):
        x_personunit = self.get_personunit_from_memory(person_id)
        world_agenda = agendaunit_shop(person_id)
        for person_problemunit in x_personunit._problems.values():
            for person_healerlink in person_problemunit._healerlinks.values():
                healer_personunit = self.get_personunit_from_memory(
                    person_healerlink.healer_id
                )
                for x_marketlink in person_healerlink._marketlinks.values():
                    x_marketunit = healer_personunit.get_marketunit(
                        x_marketlink.market_id
                    )
                    forum_agenda = x_marketunit.get_forum_agenda(person_id)
                    forum_agenda.set_market_id(world_agenda._market_id)
                    world_agenda.meld(forum_agenda)
        return world_agenda

    def create_person_market(
        self,
        person_id: PersonID,
        x_problem_id: ProblemID,
        healer_id: HealerID,
        market_id: MarketID,
    ):

        self.set_personunit(person_id, replace_personunit=False, replace_alert=False)
        x_personunit = self.get_personunit_from_memory(person_id)

        self.set_personunit(healer_id, replace_personunit=False, replace_alert=False)
        # healer_personunit = self.get_personunit_from_memory(healer_id)
        # healer_personunit.set_marketunit(market_id, False, x_problem_id)
        # x_marketunit = healer_personunit.get_marketunit(market_id)
        # x_marketunit.full_setup_clerkunit(healer_id)
        # if healer_id != x_personunit.person_id:
        #     self._set_partyunit(x_marketunit, x_personunit.person_id, healer_id)

    def _set_partyunit(
        self, x_marketunit: MarketUnit, person_id: PersonID, party_id: PersonID
    ):
        x_marketunit.full_setup_clerkunit(person_id)
        person_clerkunit = x_marketunit.get_clerkunit(person_id)
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
