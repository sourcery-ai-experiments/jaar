from src._road.road import RoadUnit, PersonRoad, PersonID
from src.agenda.atom import BookUnit, bookunit_shop
from src.world.topic import TopicUnit
from src.instrument.python import get_empty_dict_if_none
from dataclasses import dataclass


class DealMetricsException(Exception):
    pass


class WantSubRoadUnitException(Exception):
    pass


class get_member_attr_Exception(Exception):
    pass


@dataclass
class DealUnit:
    _author: PersonID = None
    _signers: set[PersonID] = None
    _like: BookUnit = None
    _topicunits: dict[RoadUnit:TopicUnit] = None

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


def dealunit_shop(
    _author: PersonID,
    _signers: set[PersonID] = None,
    _like: BookUnit = None,
    _topicunits: dict[RoadUnit:TopicUnit] = None,
):
    if _signers is None:
        _signers = set()
    if _like is None:
        _like = bookunit_shop()

    return DealUnit(
        _author=_author,
        _signers=_signers,
        _like=_like,
        _topicunits=get_empty_dict_if_none(_topicunits),
    )
