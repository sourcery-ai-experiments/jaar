from src._prime.road import (
    RoadUnit,
    is_sub_road,
    RoadNode,
    create_road,
    get_diff_road,
    default_road_delimiter_if_none,
    get_terminus_node,
    get_parent_road_from_road,
    PersonRoad,
)
from src._prime.issue import IssueUnit, create_issueunit
from src.agenda.group import GroupBrand
from src.agenda.idea import ideaunit_shop, IdeaUnit, ideaattrfilter_shop
from src.tools.python import get_empty_dict_if_none
from src.economy.economy import EconomyID
from src.world.pain import PainGenus
from src.world.person import PersonID
from dataclasses import dataclass


class WantSubRoadUnitException(Exception):
    pass


@dataclass
class DealUnit:
    _author: PersonID = None
    _reader: PersonID = None
    _issueunits: dict[PersonRoad:IssueUnit] = None

    def is_meaningful(self) -> bool:
        return next(
            (
                False
                for x_issueunit in self._issueunits.values()
                if x_issueunit.is_meaningful() == False
            ),
            self._issueunits != {},
        )

    def set_issueunit(self, x_issueunit: IssueUnit, actor: PersonID = None):
        self._issueunits[x_issueunit.base] = x_issueunit
        if actor != None:
            self.set_actor(actor, x_issueunit.base)

    def issueunit_exists(self, issuebase: PersonRoad) -> bool:
        return self._issueunits.get(issuebase) != None

    def get_issueunit(self, personroad: PersonRoad) -> IssueUnit:
        return self._issueunits.get(personroad)

    def del_issueunit(self, personroad: PersonRoad):
        self._issueunits.pop(personroad)

    def set_actor(self, actor: PersonID, issuebase: PersonRoad):
        if self.issueunit_exists(issuebase):
            x_issueunit = self.get_issueunit(issuebase)
            x_issueunit.set_actor(actor)

    def del_actor(self, actor: PersonID, issuebase: PersonRoad):
        if self.issueunit_exists(issuebase):
            x_issueunit = self.get_issueunit(issuebase)
            x_issueunit.del_actor(actor)

    def get_actor_issueunits(
        self, actor: PersonID, action_filter: bool = None
    ) -> dict[RoadUnit:IssueUnit]:
        return {
            x_base: x_issue
            for x_base, x_issue in self._issueunits.items()
            if x_issue.actor_exists(actor)
            and (x_issue.action == action_filter or action_filter is None)
        }

    def actor_has_issue(self, actor: PersonID, action_filter: bool = None) -> bool:
        return self.get_actor_issueunits(actor, action_filter=action_filter) != {}

    def actors_has_issues(self, actor_dict: dict[PersonID]):
        x_bool = True
        for x_actor in actor_dict:
            if self.actor_has_issue(x_actor) == False:
                x_bool = False
        return x_bool


def dealunit_shop(_author: PersonID, _reader: PersonID):
    return DealUnit(
        _author=_author, _reader=_reader, _issueunits=get_empty_dict_if_none(None)
    )


# def create_dealunit(
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
#     x_dealunit

#     return
