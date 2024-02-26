from src._road.road import RoadUnit, PersonRoad, PersonID
from src.agenda.atom import BookUnit, bookunit_shop
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


def dealunit_shop(
    _author: PersonID,
    _signers: set[PersonID] = None,
    _like: BookUnit = None,
):
    if _signers is None:
        _signers = set()
    if _like is None:
        _like = bookunit_shop()

    return DealUnit(
        _author=_author,
        _signers=_signers,
        _like=_like,
    )
