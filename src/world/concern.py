from src.agenda.road import (
    RoadPath,
    is_sub_road,
    RoadNode,
    get_road,
    get_diff_road,
    get_node_delimiter,
    ForkRoad,
    create_forkroad,
)
from src.agenda.group import GroupBrand
from src.culture.culture import CultureQID
from src.world.person import PersonID
from dataclasses import dataclass


@dataclass
class CultureAddress:
    culture_qid: CultureQID
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
    culture_qid: CultureQID,
    person_ids: dict[PersonID:int] = None,
    _road_node_delimiter: str = None,
) -> CultureAddress:
    x_cultureaddress = CultureAddress(
        person_ids=person_ids,
        culture_qid=culture_qid,
        _road_node_delimiter=get_node_delimiter(_road_node_delimiter),
    )
    x_cultureaddress.set_person_ids_empty_if_none()
    return x_cultureaddress


def create_cultureaddress(person_id: PersonID, culture_qid: CultureQID):
    x_cultureaddress = cultureaddress_shop(culture_qid=culture_qid)
    x_cultureaddress.add_person_id(person_id)
    return x_cultureaddress


class ConcernSubRoadPathException(Exception):
    pass


@dataclass
class ConcernUnit:
    cultureaddress: CultureAddress  # Culture and healers
    why: ForkRoad = None
    action: ForkRoad = None

    def get_road_node_delimiter(self):
        return self.cultureaddress._road_node_delimiter

    def set_why(self, x_forkroad: ForkRoad):
        self._check_subject_road(x_forkroad.base)
        self.why = x_forkroad

    def set_action(self, x_forkroad: ForkRoad):
        self._check_subject_road(x_forkroad.base)
        self.action = x_forkroad

    def _check_subject_road(self, road: RoadPath) -> bool:
        if road == get_road(self.cultureaddress.culture_qid, ""):
            raise ConcernSubRoadPathException(
                f"ConcernUnit subject level 1 cannot be empty. ({road})"
            )
        double_culture_qid_road = get_road(
            self.cultureaddress.culture_qid, self.cultureaddress.culture_qid
        )
        if is_sub_road(road, double_culture_qid_road):
            raise ConcernSubRoadPathException(
                f"ConcernUnit setting concern_subject '{road}' failed because first child node cannot be culture_qid as bug asumption check."
            )
        if is_sub_road(road, self.cultureaddress.culture_qid) == False:
            raise ConcernSubRoadPathException(
                f"ConcernUnit setting concern_subject '{road}' failed because culture_qid is not first node."
            )

    def get_str_summary(self):
        _concern_subject = self.why.base
        _concern_good = self.why.get_1_good()
        _concern_bad = self.why.get_1_bad()
        _action_subject = self.action.base
        _action_positive = self.action.get_1_good()
        _action_negative = self.action.get_1_bad()

        concern_road = get_diff_road(_concern_subject, self.cultureaddress.culture_qid)
        bad_road = get_diff_road(_concern_bad, _concern_subject)
        good_road = get_diff_road(_concern_good, _concern_subject)
        action_road = get_diff_road(_action_subject, self.cultureaddress.culture_qid)
        negative_road = get_diff_road(_action_negative, _action_subject)
        positive_road = get_diff_road(_action_positive, _action_subject)

        return f"""Within {list(self.cultureaddress.person_ids.keys())}'s {self.cultureaddress.culture_qid} culture subject: {concern_road}
 {bad_road} is bad. 
 {good_road} is good.
 Within the action domain of '{action_road}'
 It is good to {positive_road}
 It is bad to {negative_road}"""

    def get_any_pid(self):
        return self.cultureaddress.get_any_pid()


def concernunit_shop(
    cultureaddress: CultureAddress, why: ForkRoad, action: ForkRoad
) -> ConcernUnit:
    x_concernunit = ConcernUnit(cultureaddress=cultureaddress)
    x_concernunit.set_why(why)
    x_concernunit.set_action(action)
    return x_concernunit


def create_concernunit(
    cultureaddress: CultureAddress,
    why: RoadPath,
    good: RoadNode,
    bad: RoadNode,
    action: RoadPath,
    positive: RoadNode,
    negative: RoadNode,
):
    x_concernunit = ConcernUnit(cultureaddress=cultureaddress)
    x_concernunit.set_why(
        create_forkroad(
            base=get_road(cultureaddress.culture_qid, why),
            good=good,
            bad=bad,
        )
    )
    x_concernunit.set_action(
        create_forkroad(
            base=get_road(cultureaddress.culture_qid, action),
            good=positive,
            bad=negative,
        )
    )
    return x_concernunit


@dataclass
class UrgeUnit:
    _concernunit: ConcernUnit = None
    _actor_pids: dict[PersonID] = None
    _actor_groups: dict[GroupBrand:GroupBrand] = None
    _urger_pid: PersonID = None

    def add_actor_pid(self, pid: PersonID):
        self._actor_pids[pid] = None

    def add_actor_groupbrand(self, groupbrand: GroupBrand):
        self._actor_groups[groupbrand] = groupbrand

    def set_actor_groups_empty_if_none(self):
        if self._actor_groups is None:
            self._actor_groups = {}

    def get_str_summary(self):
        return f"""UrgeUnit: {self._concernunit.get_str_summary()}
 {list(self._actor_pids.keys())} are in groups {list(self._actor_groups.keys())} and are asked to be good."""


def urgeunit_shop(
    _concernunit: ConcernUnit,
    _actor_pids: dict[PersonID],
    _actor_groups: dict[GroupBrand:GroupBrand] = None,
    _urger_pid: PersonID = None,
):
    x_urgeunit = UrgeUnit(
        _concernunit=_concernunit,
        _actor_pids=_actor_pids,
        _actor_groups=_actor_groups,
        _urger_pid=_urger_pid,
    )
    x_urgeunit.set_actor_groups_empty_if_none()
    return x_urgeunit


def create_urgeunit(
    concernunit: ConcernUnit,
    actor_pid: PersonID,
    actor_group: GroupBrand = None,
    urger_pid: PersonID = None,
):
    if urger_pid is None:
        urger_pid = concernunit.get_any_pid()
    if actor_group is None:
        actor_group = actor_pid
    x_urgeunit = urgeunit_shop(concernunit, _actor_pids={}, _urger_pid=urger_pid)
    x_urgeunit.add_actor_pid(actor_pid)
    x_urgeunit.add_actor_groupbrand(actor_group)
    return x_urgeunit
