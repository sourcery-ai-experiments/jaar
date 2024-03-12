from src._road.road import RoadUnit, PersonRoad, PersonID
from src.agenda.atom import BookUnit, bookunit_shop, AgendaAtom
from src.instrument.python import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_empty_set_if_none,
)
from dataclasses import dataclass


class GiftMetricsException(Exception):
    pass


class WantSubRoadUnitException(Exception):
    pass


class get_member_attr_Exception(Exception):
    pass


@dataclass
class GiftUnit:
    _gifter: PersonID = None
    _giftees: set[PersonID] = None
    _bookunit: BookUnit = None
    _book_start: int = None

    def set_giftee(self, x_giftee: PersonID):
        self._giftees.add(x_giftee)

    def giftee_exists(self, x_giftee: PersonID) -> bool:
        return x_giftee in self._giftees

    def del_giftee(self, x_giftee: PersonID):
        self._giftees.remove(x_giftee)

    def set_bookunit(self, x_bookunit: BookUnit):
        self._bookunit = x_bookunit

    def del_bookunit(self):
        self._bookunit = bookunit_shop()

    def agendaatom_exists(self, x_agendaatom: AgendaAtom):
        return self._bookunit.agendaatom_exists(x_agendaatom)

    def get_dict(self):
        giftees_dict = {x_giftee: 1 for x_giftee in self._giftees}
        return {
            "gifter": self._gifter,
            "giftees": giftees_dict,
            "book": self._bookunit.get_dict(self._book_start),
        }


def giftunit_shop(
    _gifter: PersonID,
    _giftees: set[PersonID] = None,
    _bookunit: BookUnit = None,
    _book_start: int = None,
):
    # _book_start = get_0_if_None(_book_start)
    _giftees = get_empty_set_if_none(_giftees)
    if _bookunit is None:
        _bookunit = bookunit_shop()

    return GiftUnit(
        _gifter=_gifter, _giftees=_giftees, _bookunit=_bookunit, _book_start=_book_start
    )
