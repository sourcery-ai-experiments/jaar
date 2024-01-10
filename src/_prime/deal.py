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
    PersonID,
    EconomyID,
)
from src._prime.topic import TopicUnit, create_topicunit
from src.agenda.group import GroupBrand
from src.agenda.idea import ideaunit_shop, IdeaUnit, ideaattrfilter_shop
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


class WantSubRoadUnitException(Exception):
    pass


@dataclass
class DealUnit:
    _author: PersonID = None
    _reader: PersonID = None
    _topicunits: dict[PersonRoad:TopicUnit] = None

    def is_meaningful(self) -> bool:
        return next(
            (
                False
                for x_topicunit in self._topicunits.values()
                if x_topicunit.is_meaningful() == False
            ),
            self._topicunits != {},
        )

    def set_topicunit(self, x_topicunit: TopicUnit, actor: PersonID = None):
        self._topicunits[x_topicunit.base] = x_topicunit
        if actor != None:
            self.set_actor(actor, x_topicunit.base)

    def topicunit_exists(self, topicbase: PersonRoad) -> bool:
        return self._topicunits.get(topicbase) != None

    def get_topicunit(self, personroad: PersonRoad) -> TopicUnit:
        return self._topicunits.get(personroad)

    def del_topicunit(self, personroad: PersonRoad):
        self._topicunits.pop(personroad)

    def set_actor(self, actor: PersonID, topicbase: PersonRoad):
        if self.topicunit_exists(topicbase):
            x_topicunit = self.get_topicunit(topicbase)
            x_topicunit.set_actor(actor)

    def del_actor(self, actor: PersonID, topicbase: PersonRoad):
        if self.topicunit_exists(topicbase):
            x_topicunit = self.get_topicunit(topicbase)
            x_topicunit.del_actor(actor)

    def get_actor_topicunits(
        self, actor: PersonID, action_filter: bool = None
    ) -> dict[RoadUnit:TopicUnit]:
        return {
            x_base: x_topic
            for x_base, x_topic in self._topicunits.items()
            if x_topic.actor_exists(actor)
            and (x_topic.action == action_filter or action_filter is None)
        }

    def actor_has_topic(self, actor: PersonID, action_filter: bool = None) -> bool:
        return self.get_actor_topicunits(actor, action_filter=action_filter) != {}

    def actors_has_topics(self, actor_dict: dict[PersonID]):
        x_bool = True
        for x_actor in actor_dict:
            if self.actor_has_topic(x_actor) == False:
                x_bool = False
        return x_bool


def dealunit_shop(_author: PersonID, _reader: PersonID):
    return DealUnit(
        _author=_author, _reader=_reader, _topicunits=get_empty_dict_if_none(None)
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
