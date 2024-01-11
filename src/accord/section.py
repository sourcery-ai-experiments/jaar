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
    uid: SectionID = None
    actors: dict[PersonID:PersonID] = None
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

    def set_actor(self, x_actor: PersonID):
        self.actors[x_actor] = x_actor

    def del_actor(self, actor: PersonRoad):
        self.actors.pop(actor)

    def get_actor(self, x_actor: PersonID) -> PersonID:
        return self.actors.get(x_actor)

    def actor_exists(self, x_actor: PersonID) -> bool:
        return self.actors.get(x_actor) != None

    def has_action(self):
        return any(x_topiclink.action for x_topiclink in self._topiclinks.values())


def sectionunit_shop(
    uid: SectionID,
    actors: dict[PersonID:PersonID] = None,
    _topiclinks: dict[PersonRoad, TopicLink] = None,
):
    return SectionUnit(
        uid=uid,
        _topiclinks=get_empty_dict_if_none(_topiclinks),
        actors=get_empty_dict_if_none(actors),
    )


class WantSubRoadUnitException(Exception):
    pass


@dataclass
class AccordUnit:
    _author: PersonID = None
    _reader: PersonID = None
    _topicunits: dict[PersonRoad:TopicUnit] = None
    _sectionunits: dict[SectionID:SectionUnit] = None

    def set_sectionunit(self, x_sectionunit: SectionUnit, actor: PersonID = None):
        self._sectionunits[x_sectionunit.uid] = x_sectionunit
        if actor != None:
            self.set_actor(actor, x_sectionunit.uid)

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

    def set_topicunit(self, x_topicunit: TopicUnit):
        self._topicunits[x_topicunit.base] = x_topicunit

    def topicunit_exists(self, topicbase: PersonRoad) -> bool:
        return self._topicunits.get(topicbase) != None

    def get_topicunit(self, personroad: PersonRoad) -> TopicUnit:
        return self._topicunits.get(personroad)

    def del_topicunit(self, personroad: PersonRoad):
        self._topicunits.pop(personroad)

    def set_actor(self, actor: PersonID, section_uid: SectionID):
        if self.sectionunit_exists(section_uid):
            x_sectionunit = self.get_sectionunit(section_uid)
            x_sectionunit.set_actor(actor)

    def del_actor(self, actor: PersonID, section_uid: PersonRoad):
        if self.sectionunit_exists(section_uid):
            x_sectionunit = self.get_sectionunit(section_uid)
            x_sectionunit.del_actor(actor)

    def get_actor_sectionunits(
        self, actor: PersonID, action_filter: bool = None
    ) -> dict[RoadUnit:SectionUnit]:
        return {
            x_base: x_sectionunit
            for x_base, x_sectionunit in self._sectionunits.items()
            if x_sectionunit.actor_exists(actor)
            and (x_sectionunit.has_action() == action_filter or action_filter is None)
        }

    def actor_has_sectionunit(
        self, actor: PersonID, action_filter: bool = None
    ) -> bool:
        return self.get_actor_sectionunits(actor, action_filter=action_filter) != {}


def accordunit_shop(_author: PersonID, _reader: PersonID):
    return AccordUnit(
        _author=_author,
        _reader=_reader,
        _topicunits=get_empty_dict_if_none(None),
        _sectionunits=get_empty_dict_if_none(None),
    )
