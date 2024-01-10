from src._prime.road import (
    RoadUnit,
    PersonRoad,
    PersonID,
)
from src._prime.topic import TopicUnit, create_topicunit, TopicLink
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


class SectionID(int):
    pass


@dataclass
class SectionUnit:
    uid: SectionID = None
    _topiclinks: dict[PersonRoad, TopicLink] = None

    def set_topiclink(self, x_topiclink: TopicLink):
        self._topiclinks[x_topiclink.base] = x_topiclink

    def get_topiclink(self, topiclink_base: PersonRoad) -> TopicLink:
        return self._topiclinks.get(topiclink_base)

    def topiclink_exists(self, topiclink_base: PersonRoad) -> bool:
        return self.get_topiclink(topiclink_base) != None

    def del_topiclink(self, topiclink_base: PersonRoad):
        self._topiclinks.pop(topiclink_base)

    def get_section_id(self) -> SectionID:
        return f"Section {self.uid:04d}"


def sectionunit_shop(
    uid: SectionID,
    _topiclinks: dict[PersonRoad, TopicLink] = None,
):
    return SectionUnit(uid=uid, _topiclinks=get_empty_dict_if_none(_topiclinks))


class WantSubRoadUnitException(Exception):
    pass


@dataclass
class DealUnit:
    _author: PersonID = None
    _reader: PersonID = None
    _topicunits: dict[PersonRoad:TopicUnit] = None
    _sectionunits: dict[SectionID:SectionUnit] = None

    def set_sectionunit(self, x_sectionunit: SectionUnit):
        self._sectionunits[x_sectionunit.uid] = x_sectionunit

    def get_sectionunit(self, x_section_id: SectionID) -> SectionUnit:
        return self._sectionunits.get(x_section_id)

    def sectionunit_exists(self, x_section_id: SectionID) -> bool:
        return self.get_sectionunit(x_section_id) != None

    def del_sectionunit(self, x_section_id: SectionID):
        self._sectionunits.pop(x_section_id)

    def add_sectionunit(self) -> SectionUnit:
        next_section_int = self._get_max_sectionunit_uid() + 1
        self.set_sectionunit(sectionunit_shop(uid=next_section_int))
        return self.get_sectionunit(next_section_int)

    def _get_max_sectionunit_uid(self) -> SectionID:
        max_sectionunit_uid = 0
        for x_sectionunit in self._sectionunits.values():
            max_sectionunit_uid = max(x_sectionunit.uid, max_sectionunit_uid)
        return max_sectionunit_uid

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
        _author=_author,
        _reader=_reader,
        _topicunits=get_empty_dict_if_none(None),
        _sectionunits=get_empty_dict_if_none(None),
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
