from src.agenda.road import (
    RoadUnit,
    is_sub_road,
    RoadNode,
    create_road,
    get_diff_road,
    default_road_delimiter_if_none,
    get_terminus_node_from_road,
    get_parent_road_from_road,
)
from src.agenda.belief import BeliefUnit, create_beliefunit
from src.agenda.group import GroupBrand
from src.agenda.idea import idea_kid_shop, IdeaUnit, ideaattrfilter_shop
from src.agenda.y_func import get_empty_dict_if_none
from src.economy.economy import EconomyID
from src.world.pain import PainGenus
from src.world.person import PersonID
from dataclasses import dataclass


@dataclass
class EconomyAddress:
    pain: PainGenus
    treasurer_pid: PersonID
    economy_id: EconomyID
    _road_delimiter: str

    def set_treasurer_pid(self, treasurer_pid: PersonID):
        self.treasurer_pid = treasurer_pid


def economyaddress_shop(
    pain: PainGenus,
    treasurer_pid: PersonID,
    economy_id: EconomyID,
    _road_delimiter: str = None,
) -> EconomyAddress:
    return EconomyAddress(
        pain=pain,
        treasurer_pid=treasurer_pid,
        economy_id=economy_id,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )


class WantSubRoadUnitException(Exception):
    pass


@dataclass
class WantUnit:
    economyaddress: EconomyAddress  # Economy and healers
    fix: BeliefUnit = None
    issue: BeliefUnit = None

    def get_economyaddress_road_delimiter(self):
        return self.economyaddress._road_delimiter

    def set_issue(self, x_beliefunit: BeliefUnit):
        self._check_subject_road(x_beliefunit.base)
        self.issue = x_beliefunit

    def set_fix(self, x_beliefunit: BeliefUnit):
        self._check_subject_road(x_beliefunit.base)
        self.fix = x_beliefunit

    def _check_subject_road(self, road: RoadUnit) -> bool:
        if road == create_road(self.economyaddress.economy_id, ""):
            raise WantSubRoadUnitException(
                f"WantUnit subject level 1 cannot be empty. ({road})"
            )
        double_economy_id_road = create_road(
            self.economyaddress.economy_id, self.economyaddress.economy_id
        )
        if is_sub_road(road, double_economy_id_road):
            raise WantSubRoadUnitException(
                f"WantUnit setting want_subject '{road}' failed because first child node cannot be economy_id as bug asumption check."
            )
        if is_sub_road(road, self.economyaddress.economy_id) == False:
            raise WantSubRoadUnitException(
                f"WantUnit setting want_subject '{road}' failed because economy_id is not first node."
            )

    def get_beliefunit_ideas(self, fix_weight: int = None) -> dict[RoadUnit:IdeaUnit]:
        fix_and_issue_roads = list(self.fix.get_all_roads())
        fix_and_issue_roads.extend(self.issue.get_all_roads())
        fix_and_issue_roads = sorted(fix_and_issue_roads)

        x_idea_dict = {
            x_key: idea_kid_shop(
                get_terminus_node_from_road(x_key),
                _parent_road=get_parent_road_from_road(x_key),
            )
            for x_key in fix_and_issue_roads
        }
        if fix_weight is None:
            fix_weight = 1
        for fix_road in self.fix.get_idealinks(good=True).keys():
            fix_idea = x_idea_dict.get(fix_road)
            fix_idea._set_idea_attr(
                ideaattrfilter_shop(weight=fix_weight, promise=True)
            )

        return x_idea_dict

    def get_str_summary(self):
        _want_subject = self.issue.base
        _want_good = self.issue.get_1_idealink(good=True)
        _want_bad = self.issue.get_1_idealink(bad=True)
        _fix_subject = self.fix.base
        _fix_positive = self.fix.get_1_idealink(good=True)
        _fix_negative = self.fix.get_1_idealink(bad=True)

        want_road = get_diff_road(_want_subject, self.economyaddress.economy_id)
        bad_road = get_diff_road(_want_bad, _want_subject)
        good_road = get_diff_road(_want_good, _want_subject)
        fix_road = get_diff_road(_fix_subject, self.economyaddress.economy_id)
        negative_road = get_diff_road(_fix_negative, _fix_subject)
        positive_road = get_diff_road(_fix_positive, _fix_subject)

        return f"""Within {self.economyaddress.treasurer_pid}'s {self.economyaddress.economy_id} economy subject: {want_road}
 {bad_road} is bad. 
 {good_road} is good.
 Within the fix domain of '{fix_road}'
 It is good to {positive_road}
 It is bad to {negative_road}"""

    def get_any_pid(self):
        return self.economyaddress.treasurer_pid


def wantunit_shop(
    economyaddress: EconomyAddress, issue: BeliefUnit, fix: BeliefUnit
) -> WantUnit:
    x_wantunit = WantUnit(economyaddress=economyaddress)
    x_wantunit.set_issue(issue)
    x_wantunit.set_fix(fix)
    return x_wantunit


def create_wantunit(
    economyaddress: EconomyAddress,
    issue: RoadUnit,  # road with economy root node
    good: RoadNode,
    bad: RoadNode,
    fix: RoadUnit,  # road with economy root node
    positive: RoadNode,
    negative: RoadNode,
):
    """creates wantunit object without RoadUnit root nodes being explictely defined in the issue and fix RoadUnits."""
    x_wantunit = WantUnit(economyaddress=economyaddress)
    x_wantunit.set_issue(
        create_beliefunit(
            base=create_road(economyaddress.economy_id, issue),
            good=good,
            bad=bad,
        )
    )
    x_wantunit.set_fix(
        create_beliefunit(
            base=create_road(economyaddress.economy_id, fix),
            good=positive,
            bad=negative,
        )
    )
    return x_wantunit


@dataclass
class RequestUnit:
    _wantunit: WantUnit = None
    _requestee_pids: dict[PersonID] = None
    _requestee_groups: dict[GroupBrand:GroupBrand] = None
    _requester_pid: PersonID = None
    _fix_weight: float = None

    def add_requestee_pid(self, pid: PersonID):
        self._requestee_pids[pid] = None

    def add_requestee_groupbrand(self, groupbrand: GroupBrand):
        self._requestee_groups[groupbrand] = groupbrand

    def get_str_summary(self):
        return f"""RequestUnit: {self._wantunit.get_str_summary()}
 {list(self._requestee_pids.keys())} are in groups {list(self._requestee_groups.keys())} and are asked to be good."""


def requestunit_shop(
    _wantunit: WantUnit,
    _requestee_pids: dict[PersonID],
    _requestee_groups: dict[GroupBrand:GroupBrand] = None,
    _requester_pid: PersonID = None,
    _fix_weight: float = None,
):
    if _fix_weight is None:
        _fix_weight = 1
    return RequestUnit(
        _wantunit=_wantunit,
        _requestee_pids=get_empty_dict_if_none(_requestee_pids),
        _requestee_groups=get_empty_dict_if_none(_requestee_groups),
        _requester_pid=_requester_pid,
        _fix_weight=_fix_weight,
    )


def create_requestunit(
    wantunit: WantUnit,
    requestee_pid: PersonID,
    requestee_group: GroupBrand = None,
    requester_pid: PersonID = None,
    fix_weight: int = None,
):
    if requester_pid is None:
        requester_pid = wantunit.get_any_pid()
    if requestee_group is None:
        requestee_group = requestee_pid
    x_requestunit = requestunit_shop(
        wantunit,
        _requestee_pids={},
        _requester_pid=requester_pid,
        _fix_weight=fix_weight,
    )
    x_requestunit.add_requestee_pid(requestee_pid)
    x_requestunit.add_requestee_groupbrand(requestee_group)
    return x_requestunit


@dataclass
class LobbyUnit:
    _src_requestunit: RequestUnit = None
    _dst_requestunit: RequestUnit = None


def lobbyunit_shop(
    _src_requestunit: RequestUnit = None,
    _dst_requestunit: RequestUnit = None,
):
    return LobbyUnit(
        _src_requestunit=_src_requestunit,
        _dst_requestunit=_dst_requestunit,
    )


# def create_lobbyunit(
#     src_requestee_pid: PersonID, # also dst_requestee_pid
#     dst_requestee_pid: PersonID, # also src_requester_pid
#     src_wantunit: WantUnit,
#     dst_wantunit: WantUnit = None,
#     src_requestee_group: GroupBrand = None,
#     src_fix_weight: int = None, # also same as dst_fix_weight
#     dst_requestee_group: GroupBrand = None,
# ):
#     src_requestunit = create_requestunit(
#         wantunit=src_wantunit,
#         requestee_pid=src_requestee_pid,
#         requestee_group=src_requestee_group,
#         requester_pid=src_requester_pid,
#         fix_weight=src_fix_weight,
#     )
#     dst_requestunit = create_requestunit(
#         wantunit=dst_wantunit,
#         requestee_pid=dst_requestee_pid,
#         requestee_group=dst_requestee_group,
#         requester_pid=dst_requester_pid,
#         fix_weight=dst_fix_weight,
#     )
#     x_lobbyunit

#     return
