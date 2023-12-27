from src.agenda.road import (
    RoadUnit,
    is_sub_road,
    RoadNode,
    create_road,
    get_diff_road,
    default_road_delimiter_if_none,
    get_terminus_node_from_road,
    get_pad_from_road,
)
from src.agenda.fork import ForkUnit, create_forkunit
from src.agenda.group import GroupBrand
from src.agenda.idea import ideacore_shop, IdeaCore, ideaattrfilter_shop
from src.agenda.y_func import get_empty_dict_if_none
from src.economy.economy import EconomyID
from src.world.person import PersonID
from dataclasses import dataclass


@dataclass
class EconomyAddress:
    economy_id: EconomyID
    treasurer_pids: dict[PersonID:int]
    _road_delimiter: str

    def add_treasurer_pid(self, treasurer_pid: PersonID):
        self.treasurer_pids[treasurer_pid] = 0

    def get_any_pid(self):
        x_pid = None
        for y_pid in self.treasurer_pids:
            x_pid = y_pid
        return x_pid


def economyaddress_shop(
    economy_id: EconomyID,
    treasurer_pids: dict[PersonID:int] = None,
    _road_delimiter: str = None,
) -> EconomyAddress:
    return EconomyAddress(
        treasurer_pids=get_empty_dict_if_none(treasurer_pids),
        economy_id=economy_id,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )


def create_economyaddress(treasurer_pid: PersonID, economy_id: EconomyID):
    x_economyaddress = economyaddress_shop(economy_id=economy_id)
    x_economyaddress.add_treasurer_pid(treasurer_pid)
    return x_economyaddress


class ConcernSubRoadUnitException(Exception):
    pass


@dataclass
class ConcernUnit:
    economyaddress: EconomyAddress  # Economy and healers
    action: ForkUnit = None
    reason: ForkUnit = None

    def get_economyaddress_road_delimiter(self):
        return self.economyaddress._road_delimiter

    def set_reason(self, x_forkunit: ForkUnit):
        self._check_subject_road(x_forkunit.base)
        self.reason = x_forkunit

    def set_action(self, x_forkunit: ForkUnit):
        self._check_subject_road(x_forkunit.base)
        self.action = x_forkunit

    def _check_subject_road(self, road: RoadUnit) -> bool:
        if road == create_road(self.economyaddress.economy_id, ""):
            raise ConcernSubRoadUnitException(
                f"ConcernUnit subject level 1 cannot be empty. ({road})"
            )
        double_economy_id_road = create_road(
            self.economyaddress.economy_id, self.economyaddress.economy_id
        )
        if is_sub_road(road, double_economy_id_road):
            raise ConcernSubRoadUnitException(
                f"ConcernUnit setting concern_subject '{road}' failed because first child node cannot be economy_id as bug asumption check."
            )
        if is_sub_road(road, self.economyaddress.economy_id) == False:
            raise ConcernSubRoadUnitException(
                f"ConcernUnit setting concern_subject '{road}' failed because economy_id is not first node."
            )

    def get_forkunit_ideas(self, action_weight: int = None) -> dict[RoadUnit:IdeaCore]:
        action_and_reason_roads = list(self.action.get_all_roads())
        action_and_reason_roads.extend(self.reason.get_all_roads())
        action_and_reason_roads = sorted(action_and_reason_roads)

        x_idea_dict = {
            x_key: ideacore_shop(
                get_terminus_node_from_road(x_key), _pad=get_pad_from_road(x_key)
            )
            for x_key in action_and_reason_roads
        }
        if action_weight is None:
            action_weight = 1
        for action_road in self.action.get_prongs(good=True).keys():
            action_idea = x_idea_dict.get(action_road)
            action_idea._set_idea_attr(
                ideaattrfilter_shop(weight=action_weight, promise=True)
            )

        return x_idea_dict

    def get_str_summary(self):
        _concern_subject = self.reason.base
        _concern_good = self.reason.get_1_prong(good=True)
        _concern_bad = self.reason.get_1_prong(bad=True)
        _action_subject = self.action.base
        _action_positive = self.action.get_1_prong(good=True)
        _action_negative = self.action.get_1_prong(bad=True)

        concern_road = get_diff_road(_concern_subject, self.economyaddress.economy_id)
        bad_road = get_diff_road(_concern_bad, _concern_subject)
        good_road = get_diff_road(_concern_good, _concern_subject)
        action_road = get_diff_road(_action_subject, self.economyaddress.economy_id)
        negative_road = get_diff_road(_action_negative, _action_subject)
        positive_road = get_diff_road(_action_positive, _action_subject)

        return f"""Within {list(self.economyaddress.treasurer_pids.keys())}'s {self.economyaddress.economy_id} economy subject: {concern_road}
 {bad_road} is bad. 
 {good_road} is good.
 Within the action domain of '{action_road}'
 It is good to {positive_road}
 It is bad to {negative_road}"""

    def get_any_pid(self):
        return self.economyaddress.get_any_pid()


def concernunit_shop(
    economyaddress: EconomyAddress, reason: ForkUnit, action: ForkUnit
) -> ConcernUnit:
    x_concernunit = ConcernUnit(economyaddress=economyaddress)
    x_concernunit.set_reason(reason)
    x_concernunit.set_action(action)
    return x_concernunit


def create_concernunit(
    economyaddress: EconomyAddress,
    reason: RoadUnit,  # road with economy root node
    good: RoadNode,
    bad: RoadNode,
    action: RoadUnit,  # road with economy root node
    positive: RoadNode,
    negative: RoadNode,
):
    """creates concernunit object without RoadUnit root nodes being explictely defined in the reason and action RoadUnits."""
    x_concernunit = ConcernUnit(economyaddress=economyaddress)
    x_concernunit.set_reason(
        create_forkunit(
            base=create_road(economyaddress.economy_id, reason),
            good=good,
            bad=bad,
        )
    )
    x_concernunit.set_action(
        create_forkunit(
            base=create_road(economyaddress.economy_id, action),
            good=positive,
            bad=negative,
        )
    )
    return x_concernunit


@dataclass
class RequestUnit:
    _concernunit: ConcernUnit = None
    _requestee_pids: dict[PersonID] = None
    _requestee_groups: dict[GroupBrand:GroupBrand] = None
    _requester_pid: PersonID = None
    _action_weight: float = None

    def add_requestee_pid(self, pid: PersonID):
        self._requestee_pids[pid] = None

    def add_requestee_groupbrand(self, groupbrand: GroupBrand):
        self._requestee_groups[groupbrand] = groupbrand

    def get_str_summary(self):
        return f"""RequestUnit: {self._concernunit.get_str_summary()}
 {list(self._requestee_pids.keys())} are in groups {list(self._requestee_groups.keys())} and are asked to be good."""


def requestunit_shop(
    _concernunit: ConcernUnit,
    _requestee_pids: dict[PersonID],
    _requestee_groups: dict[GroupBrand:GroupBrand] = None,
    _requester_pid: PersonID = None,
    _action_weight: float = None,
):
    if _action_weight is None:
        _action_weight = 1
    return RequestUnit(
        _concernunit=_concernunit,
        _requestee_pids=get_empty_dict_if_none(_requestee_pids),
        _requestee_groups=get_empty_dict_if_none(_requestee_groups),
        _requester_pid=_requester_pid,
        _action_weight=_action_weight,
    )


def create_requestunit(
    concernunit: ConcernUnit,
    requestee_pid: PersonID,
    requestee_group: GroupBrand = None,
    requester_pid: PersonID = None,
    action_weight: int = None,
):
    if requester_pid is None:
        requester_pid = concernunit.get_any_pid()
    if requestee_group is None:
        requestee_group = requestee_pid
    x_requestunit = requestunit_shop(
        concernunit,
        _requestee_pids={},
        _requester_pid=requester_pid,
        _action_weight=action_weight,
    )
    x_requestunit.add_requestee_pid(requestee_pid)
    x_requestunit.add_requestee_groupbrand(requestee_group)
    return x_requestunit
