from src._prime.road import (
    RoadUnit,
    PersonRoad,
    PersonID,
)
from src.world.topic import TopicLink
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


class VowID(int):
    pass


@dataclass
class VowUnit:
    author_weight: float = None
    reader_weight: float = None
    uid: VowID = None
    actor: PersonID = None
    _topiclinks: dict[PersonRoad, TopicLink] = None
    _relative_author_weight: float = None
    _relative_reader_weight: float = None

    def set_topiclink(self, x_topiclink: TopicLink):
        self._topiclinks[x_topiclink.base] = x_topiclink

    def get_topiclink(self, topiclink_base: PersonRoad) -> TopicLink:
        return self._topiclinks.get(topiclink_base)

    def topiclink_exists(self, topiclink_base: PersonRoad) -> bool:
        return self.get_topiclink(topiclink_base) != None

    def del_topiclink(self, topiclink_base: PersonRoad):
        self._topiclinks.pop(topiclink_base)

    def get_vow_id(self) -> VowID:
        return f"Vow {self.uid:04d}"

    def edit_attr(
        self,
        author_weight: float = None,
        reader_weight: float = None,
        _relative_author_weight: float = None,
        _relative_reader_weight: float = None,
    ):
        if author_weight != None:
            self.author_weight = author_weight
        if reader_weight != None:
            self.reader_weight = reader_weight
        if _relative_author_weight != None:
            self._relative_author_weight = _relative_author_weight
        if _relative_reader_weight != None:
            self._relative_reader_weight = _relative_reader_weight

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


def vowunit_shop(
    uid: VowID,
    author_weight: int = None,
    reader_weight: int = None,
    actor: PersonID = None,
    _topiclinks: dict[PersonRoad, TopicLink] = None,
):
    if author_weight is None:
        author_weight = 1
    if reader_weight is None:
        reader_weight = 1
    _relative_author_weight = 0
    _relative_reader_weight = 0
    return VowUnit(
        uid=uid,
        author_weight=author_weight,
        reader_weight=reader_weight,
        _topiclinks=get_empty_dict_if_none(_topiclinks),
        actor=actor,
        _relative_author_weight=_relative_author_weight,
        _relative_reader_weight=_relative_reader_weight,
    )
