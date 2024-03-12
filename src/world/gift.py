from src._road.road import RoadUnit, PersonRoad, PersonID
from src.agenda.book import BookUnit, bookunit_shop, AgendaAtom
from src.instrument.python import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_empty_set_if_none,
    get_json_from_dict,
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

    def set_book_start(self, x_book_start: int):
        self._book_start = get_0_if_None(x_book_start)

    def agendaatom_exists(self, x_agendaatom: AgendaAtom):
        return self._bookunit.agendaatom_exists(x_agendaatom)

    def get_step_dict(self) -> dict[str:]:
        giftees_dict = {x_giftee: 1 for x_giftee in self._giftees}
        return {
            "gifter": self._gifter,
            "giftees": giftees_dict,
            "book": self._bookunit.get_ordered_agendaatoms(self._book_start),
        }

    def get_book_min(self, giftunit_dict: dict[str:]) -> int:
        book_dict = giftunit_dict.get("book")
        book_keys = set(book_dict.keys())
        return min(book_keys)

    def get_book_max(self, giftunit_dict: dict[str:]) -> int:
        book_dict = giftunit_dict.get("book")
        book_keys = set(book_dict.keys())
        return max(book_keys)

    def get_bookmetric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "gifter": x_dict.get("gifter"),
            "giftees": x_dict.get("giftees"),
            "book_min": self.get_book_min(x_dict),
            "book_max": self.get_book_max(x_dict),
        }

    def get_bookmetric_json(self) -> str:
        return get_json_from_dict(self.get_bookmetric_dict())


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

    x_giftunit = GiftUnit(_gifter=_gifter, _giftees=_giftees, _bookunit=_bookunit)
    x_giftunit.set_book_start(_book_start)
    return x_giftunit
