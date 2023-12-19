from src.agenda.road import (
    RoadPath,
    is_sub_road,
    RoadNode,
    get_road,
    get_diff_road,
    get_node_delimiter,
    ForkUnit,
    create_forkunit,
)
from src.agenda.group import GroupBrand
from src.culture.culture import CultureQID
from src.world.person import PersonID
from dataclasses import dataclass


@dataclass
class CultureAddress:
    culture_id: CultureQID
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


def cultureaddress_shop(
    culture_id: CultureQID,
    person_ids: dict[PersonID:int] = None,
    _road_node_delimiter: str = None,
) -> CultureAddress:
    x_cultureaddress = CultureAddress(
        person_ids=person_ids,
        culture_id=culture_id,
        _road_node_delimiter=get_node_delimiter(_road_node_delimiter),
    )
    x_cultureaddress.set_person_ids_empty_if_none()
    return x_cultureaddress


def create_cultureaddress(person_id: PersonID, culture_id: CultureQID):
    x_cultureaddress = cultureaddress_shop(culture_id=culture_id)
    x_cultureaddress.add_person_id(person_id)
    return x_cultureaddress


class ConcernSubRoadPathException(Exception):
    pass


@dataclass
class ConcernUnit:
    cultureaddress: CultureAddress  # Culture and healers
    action: ForkUnit = None
    when: ForkUnit = None

    def get_road_node_delimiter(self):
        return self.cultureaddress._road_node_delimiter

    def set_when(self, x_forkunit: ForkUnit):
        self._check_subject_road(x_forkunit.base)
        self.when = x_forkunit

    def set_action(self, x_forkunit: ForkUnit):
        self._check_subject_road(x_forkunit.base)
        self.action = x_forkunit

    def _check_subject_road(self, road: RoadPath) -> bool:
        if road == get_road(self.cultureaddress.culture_id, ""):
            raise ConcernSubRoadPathException(
                f"ConcernUnit subject level 1 cannot be empty. ({road})"
            )
        double_culture_id_road = get_road(
            self.cultureaddress.culture_id, self.cultureaddress.culture_id
        )
        if is_sub_road(road, double_culture_id_road):
            raise ConcernSubRoadPathException(
                f"ConcernUnit setting concern_subject '{road}' failed because first child node cannot be culture_id as bug asumption check."
            )
        if is_sub_road(road, self.cultureaddress.culture_id) == False:
            raise ConcernSubRoadPathException(
                f"ConcernUnit setting concern_subject '{road}' failed because culture_id is not first node."
            )

    def get_str_summary(self):
        _concern_subject = self.when.base
        _concern_good = self.when.get_1_good()
        _concern_bad = self.when.get_1_bad()
        _action_subject = self.action.base
        _action_positive = self.action.get_1_good()
        _action_negative = self.action.get_1_bad()

        concern_road = get_diff_road(_concern_subject, self.cultureaddress.culture_id)
        bad_road = get_diff_road(_concern_bad, _concern_subject)
        good_road = get_diff_road(_concern_good, _concern_subject)
        action_road = get_diff_road(_action_subject, self.cultureaddress.culture_id)
        negative_road = get_diff_road(_action_negative, _action_subject)
        positive_road = get_diff_road(_action_positive, _action_subject)

        return f"""Within {list(self.cultureaddress.person_ids.keys())}'s {self.cultureaddress.culture_id} culture subject: {concern_road}
 {bad_road} is bad. 
 {good_road} is good.
 Within the action domain of '{action_road}'
 It is good to {positive_road}
 It is bad to {negative_road}"""

    def get_any_pid(self):
        return self.cultureaddress.get_any_pid()


def concernunit_shop(
    cultureaddress: CultureAddress, when: ForkUnit, action: ForkUnit
) -> ConcernUnit:
    x_concernunit = ConcernUnit(cultureaddress=cultureaddress)
    x_concernunit.set_when(when)
    x_concernunit.set_action(action)
    return x_concernunit


def create_concernunit(
    cultureaddress: CultureAddress,
    when: RoadPath,  # road with culture root node
    good: RoadNode,
    bad: RoadNode,
    action: RoadPath,  # road with culture root node
    positive: RoadNode,
    negative: RoadNode,
):
    """creates concernunit object without roadpath root nodes being explictely defined in the when and action RoadPaths."""
    x_concernunit = ConcernUnit(cultureaddress=cultureaddress)
    x_concernunit.set_when(
        create_forkunit(
            base=get_road(cultureaddress.culture_id, when),
            good=good,
            bad=bad,
        )
    )
    x_concernunit.set_action(
        create_forkunit(
            base=get_road(cultureaddress.culture_id, action),
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
):
    x_lobbyunit = LobbyUnit(
        _concernunit=_concernunit,
        _lobbyee_pids=_lobbyee_pids,
        _lobbyee_groups=_lobbyee_groups,
        _lobbyer_pid=_lobbyer_pid,
    )
    x_lobbyunit.set_lobbyee_groups_empty_if_none()
    return x_lobbyunit


def create_lobbyunit(
    concernunit: ConcernUnit,
    lobbyee_pid: PersonID,
    lobbyee_group: GroupBrand = None,
    lobbyer_pid: PersonID = None,
):
    if lobbyer_pid is None:
        lobbyer_pid = concernunit.get_any_pid()
    if lobbyee_group is None:
        lobbyee_group = lobbyee_pid
    x_lobbyunit = lobbyunit_shop(
        concernunit, _lobbyee_pids={}, _lobbyer_pid=lobbyer_pid
    )
    x_lobbyunit.add_lobbyee_pid(lobbyee_pid)
    x_lobbyunit.add_lobbyee_groupbrand(lobbyee_group)
    return x_lobbyunit
