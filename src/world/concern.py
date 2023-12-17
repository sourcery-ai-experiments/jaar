from src.agenda.road import (
    Road,
    is_sub_road,
    RaodNode,
    get_road,
    get_diff_road,
    get_node_delimiter,
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


class ConcernSubRoadException(Exception):
    pass


@dataclass
class ConcernUnit:
    cultureaddress: CultureAddress  # Culture and healers
    _concern_subject: Road = None
    _concern_good: Road = None  # cause that is wanted
    _concern_bad: Road = None  # pain and cause is not wanted
    _action_subject: Road = None
    _action_positive: Road = None  # task that is wanted
    _action_negative: Road = None  # task that is not wanted

    def get_road_node_delimiter(self):
        return self.cultureaddress._road_node_delimiter

    def set_good(self, subject_road: Road, good_road: Road, bad_road: Road):
        self._check_subject_road(subject_road)
        if is_sub_road(bad_road, subject_road) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting concern_bad '{bad_road}' failed because subject road '{subject_road}' is not subroad"
            )
        if is_sub_road(good_road, subject_road) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting concern_good '{good_road}' failed because subject road '{subject_road}' is not subroad"
            )
        self._concern_subject = subject_road
        self._concern_good = good_road
        self._concern_bad = bad_road

    def set_action(self, subject_road: Road, positive_road: Road, negative_road: Road):
        self._check_subject_road(subject_road)
        if is_sub_road(negative_road, subject_road) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting action_negative '{negative_road}' failed because subject road '{subject_road}' is not subroad"
            )
        if is_sub_road(positive_road, subject_road) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting action_positive '{positive_road}' failed because subject road '{subject_road}' is not subroad"
            )
        self._action_subject = subject_road
        self._action_positive = positive_road
        self._action_negative = negative_road

    def _check_subject_road(self, road: Road) -> bool:
        double_culture_qid_road = get_road(
            self.cultureaddress.culture_qid, self.cultureaddress.culture_qid
        )
        if road == get_road(self.cultureaddress.culture_qid, ""):
            raise ConcernSubRoadException(
                f"ConcernUnit subject level 1 cannot be empty. ({road})"
            )
        if is_sub_road(road, double_culture_qid_road):
            raise ConcernSubRoadException(
                f"ConcernUnit setting concern_subject '{road}' failed because first child node cannot be culture_qid as bug asumption check."
            )

        if is_sub_road(road, self.cultureaddress.culture_qid) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting concern_subject '{road}' failed because culture_qid is not first node."
            )

    def get_str_summary(self):
        concern_road = get_diff_road(
            self._concern_subject, self.cultureaddress.culture_qid
        )
        bad_road = get_diff_road(self._concern_bad, self._concern_subject)
        good_road = get_diff_road(self._concern_good, self._concern_subject)
        action_road = get_diff_road(
            self._action_subject, self.cultureaddress.culture_qid
        )
        negative_road = get_diff_road(self._action_negative, self._action_subject)
        positive_road = get_diff_road(self._action_positive, self._action_subject)

        return f"""Within {list(self.cultureaddress.person_ids.keys())}'s {self.cultureaddress.culture_qid} culture subject: {concern_road}
 {bad_road} is bad. 
 {good_road} is good.
 Within the action domain of '{action_road}'
 It is good to {positive_road}
 It is bad to {negative_road}"""

    def get_any_pid(self):
        return self.cultureaddress.get_any_pid()


def concernunit_shop(
    cultureaddress: CultureAddress,
    concern_subject: Road = None,
    concern_good: Road = None,
    concern_bad: Road = None,
    action_subject: Road = None,
    action_positive: Road = None,
    action_negative: Road = None,
) -> ConcernUnit:
    x_concernunit = ConcernUnit(cultureaddress=cultureaddress)
    x_concernunit.set_good(concern_subject, concern_good, concern_bad)
    x_concernunit.set_action(action_subject, action_positive, action_negative)
    return x_concernunit


def create_concernunit(
    cultureaddress: CultureAddress,
    concern: Road,
    good: RaodNode,
    bad: RaodNode,
    action: Road,
    positive: RaodNode,
    negative: RaodNode,
):
    x_concernunit = ConcernUnit(cultureaddress=cultureaddress)
    concern = get_road(cultureaddress.culture_qid, concern)
    action = get_road(cultureaddress.culture_qid, action)

    concern_good = get_road(concern, good)
    concern_bad = get_road(concern, bad)
    x_concernunit.set_good(concern, concern_good, concern_bad)
    action_positive = get_road(action, positive)
    action_negative = get_road(action, negative)
    x_concernunit.set_action(action, action_positive, action_negative)
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
