from src._prime.road import (
    RoadUnit,
    PersonRoad,
    PersonID,
)
from src.accord.topic import TopicUnit, TopicLink
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


class SectionID(int):
    pass


@dataclass
class SectionUnit:
    weight: float = None
    uid: SectionID = None
    actor: PersonID = None
    _topiclinks: dict[PersonRoad, TopicLink] = None
    _relative_accord_weight: float = None

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

    def edit_attr(self, weight: float = None, _relative_accord_weight: float = None):
        if weight != None:
            self.weight = weight
        if _relative_accord_weight != None:
            self._relative_accord_weight = _relative_accord_weight

    def set_actor(self, x_actor: PersonID):
        self.actor = x_actor

    def del_actor(self, actor: PersonRoad):
        if self.actor == actor:
            self.actor = None

    def get_actor(self, x_actor: PersonID) -> PersonID:
        return self.actor

    def actor_exists(self, x_actor: PersonID) -> bool:
        return self.actor == x_actor

    def has_action(self):
        return any(x_topiclink.action for x_topiclink in self._topiclinks.values())


def sectionunit_shop(
    uid: SectionID,
    weight: int = None,
    actor: PersonID = None,
    _topiclinks: dict[PersonRoad, TopicLink] = None,
):
    if weight is None:
        weight = 1
    _relative_accord_weight = 0
    return SectionUnit(
        uid=uid,
        weight=weight,
        _topiclinks=get_empty_dict_if_none(_topiclinks),
        actor=actor,
        _relative_accord_weight=0,
    )
