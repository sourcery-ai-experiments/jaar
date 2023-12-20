from src.agenda.road import (
    RoadPath,
    is_sub_road,
    RoadNode,
    get_road,
    get_diff_road,
    get_node_delimiter,
    ForkUnit,
    create_forkunit,
    get_terminus_node_from_road,
    get_pad_from_road,
)
from src.agenda.group import GroupBrand
from src.agenda.idea import ideacore_shop, IdeaCore, IdeaAttrHolder
from src.economy.economy import EconomyID
from src.world.person import PersonID
from dataclasses import dataclass


@dataclass
class EconomyAddress:
    economy_id: EconomyID
    person_ids: dict[PersonID:int]
    _road_node_delimiter: str

    def set_person_ids_empty_if_none(self):
        if self.person_ids is None:
            self.person_ids = {}

    def add_person_id(self, person_id: PersonID):
        self.person_ids[person_id] = 0

    def get_any_pid(self):
        x_pid = None
        for y_pid in self.person_ids:
            x_pid = y_pid
        return x_pid


def economyaddress_shop(
    economy_id: EconomyID,
    person_ids: dict[PersonID:int] = None,
    _road_node_delimiter: str = None,
) -> EconomyAddress:
    x_economyaddress = EconomyAddress(
        person_ids=person_ids,
        economy_id=economy_id,
        _road_node_delimiter=get_node_delimiter(_road_node_delimiter),
    )
    x_economyaddress.set_person_ids_empty_if_none()
    return x_economyaddress


def create_economyaddress(person_id: PersonID, economy_id: EconomyID):
    x_economyaddress = economyaddress_shop(economy_id=economy_id)
    x_economyaddress.add_person_id(person_id)
    return x_economyaddress


class ConcernSubRoadPathException(Exception):
    pass


@dataclass
class ConcernUnit:
    economyaddress: EconomyAddress  # Economy and healers
    action: ForkUnit = None
    when: ForkUnit = None

    def get_road_node_delimiter(self):
        return self.economyaddress._road_node_delimiter

    def set_when(self, x_forkunit: ForkUnit):
        self._check_subject_road(x_forkunit.base)
        self.when = x_forkunit

    def set_action(self, x_forkunit: ForkUnit):
        self._check_subject_road(x_forkunit.base)
        self.action = x_forkunit

    def _check_subject_road(self, road: RoadPath) -> bool:
        if road == get_road(self.economyaddress.economy_id, ""):
            raise ConcernSubRoadPathException(
                f"ConcernUnit subject level 1 cannot be empty. ({road})"
            )
        double_economy_id_road = get_road(
            self.economyaddress.economy_id, self.economyaddress.economy_id
        )
        if is_sub_road(road, double_economy_id_road):
            raise ConcernSubRoadPathException(
                f"ConcernUnit setting concern_subject '{road}' failed because first child node cannot be economy_id as bug asumption check."
            )
        if is_sub_road(road, self.economyaddress.economy_id) == False:
            raise ConcernSubRoadPathException(
                f"ConcernUnit setting concern_subject '{road}' failed because economy_id is not first node."
            )

    def get_forkunit_ideas(self, action_weight: int = None) -> dict[RoadPath:IdeaCore]:
        action_and_when_roads = list(self.action.get_all_roads())
        action_and_when_roads.extend(self.when.get_all_roads())
        action_and_when_roads = sorted(action_and_when_roads)

        x_idea_dict = {
            x_key: ideacore_shop(
                get_terminus_node_from_road(x_key), _pad=get_pad_from_road(x_key)
            )
            for x_key in action_and_when_roads
        }
        if action_weight is None:
            action_weight = 1
        for action_road in self.action.get_good_descendents().keys():
            action_idea = x_idea_dict.get(action_road)
            action_idea._set_idea_attr(
                IdeaAttrHolder(weight=action_weight, promise=True)
            )

        return x_idea_dict

    def get_str_summary(self):
        _concern_subject = self.when.base
        _concern_good = self.when.get_1_good()
        _concern_bad = self.when.get_1_bad()
        _action_subject = self.action.base
        _action_positive = self.action.get_1_good()
        _action_negative = self.action.get_1_bad()

        concern_road = get_diff_road(_concern_subject, self.economyaddress.economy_id)
        bad_road = get_diff_road(_concern_bad, _concern_subject)
        good_road = get_diff_road(_concern_good, _concern_subject)
        action_road = get_diff_road(_action_subject, self.economyaddress.economy_id)
        negative_road = get_diff_road(_action_negative, _action_subject)
        positive_road = get_diff_road(_action_positive, _action_subject)

        return f"""Within {list(self.economyaddress.person_ids.keys())}'s {self.economyaddress.economy_id} economy subject: {concern_road}
 {bad_road} is bad. 
 {good_road} is good.
 Within the action domain of '{action_road}'
 It is good to {positive_road}
 It is bad to {negative_road}"""

    def get_any_pid(self):
        return self.economyaddress.get_any_pid()


def concernunit_shop(
    economyaddress: EconomyAddress, when: ForkUnit, action: ForkUnit
) -> ConcernUnit:
    x_concernunit = ConcernUnit(economyaddress=economyaddress)
    x_concernunit.set_when(when)
    x_concernunit.set_action(action)
    return x_concernunit


def create_concernunit(
    economyaddress: EconomyAddress,
    when: RoadPath,  # road with economy root node
    good: RoadNode,
    bad: RoadNode,
    action: RoadPath,  # road with economy root node
    positive: RoadNode,
    negative: RoadNode,
):
    """creates concernunit object without roadpath root nodes being explictely defined in the when and action RoadPaths."""
    x_concernunit = ConcernUnit(economyaddress=economyaddress)
    x_concernunit.set_when(
        create_forkunit(
            base=get_road(economyaddress.economy_id, when),
            good=good,
            bad=bad,
        )
    )
    x_concernunit.set_action(
        create_forkunit(
            base=get_road(economyaddress.economy_id, action),
            good=positive,
            bad=negative,
        )
    )
    return x_concernunit


@dataclass
class LobbyUnit:
    _concernunit: ConcernUnit = None
    _lobbyee_pids: dict[PersonID] = None
    _lobbyee_groups: dict[GroupBrand:GroupBrand] = None
    _lobbyer_pid: PersonID = None
    _action_weight: float = None

    def add_lobbyee_pid(self, pid: PersonID):
        self._lobbyee_pids[pid] = None

    def add_lobbyee_groupbrand(self, groupbrand: GroupBrand):
        self._lobbyee_groups[groupbrand] = groupbrand

    def set_lobbyee_groups_empty_if_none(self):
        if self._lobbyee_groups is None:
            self._lobbyee_groups = {}

    def get_str_summary(self):
        return f"""LobbyUnit: {self._concernunit.get_str_summary()}
 {list(self._lobbyee_pids.keys())} are in groups {list(self._lobbyee_groups.keys())} and are asked to be good."""


def lobbyunit_shop(
    _concernunit: ConcernUnit,
    _lobbyee_pids: dict[PersonID],
    _lobbyee_groups: dict[GroupBrand:GroupBrand] = None,
    _lobbyer_pid: PersonID = None,
    _action_weight: float = None,
):
    if _action_weight is None:
        _action_weight = 1
    x_lobbyunit = LobbyUnit(
        _concernunit=_concernunit,
        _lobbyee_pids=_lobbyee_pids,
        _lobbyee_groups=_lobbyee_groups,
        _lobbyer_pid=_lobbyer_pid,
        _action_weight=_action_weight,
    )
    x_lobbyunit.set_lobbyee_groups_empty_if_none()
    return x_lobbyunit


def create_lobbyunit(
    concernunit: ConcernUnit,
    lobbyee_pid: PersonID,
    lobbyee_group: GroupBrand = None,
    lobbyer_pid: PersonID = None,
    action_weight: int = None,
):
    if lobbyer_pid is None:
        lobbyer_pid = concernunit.get_any_pid()
    if lobbyee_group is None:
        lobbyee_group = lobbyee_pid
    x_lobbyunit = lobbyunit_shop(
        concernunit,
        _lobbyee_pids={},
        _lobbyer_pid=lobbyer_pid,
        _action_weight=action_weight,
    )
    x_lobbyunit.add_lobbyee_pid(lobbyee_pid)
    x_lobbyunit.add_lobbyee_groupbrand(lobbyee_group)
    return x_lobbyunit
