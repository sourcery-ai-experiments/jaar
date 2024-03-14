from src._road.road import RoadUnit, PersonRoad, PersonID
from src.agenda.atom import AgendaAtom, get_from_json as agendaatom_get_from_json
from src.agenda.book import BookUnit, bookunit_shop
from src.instrument.python import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_empty_set_if_none,
    get_json_from_dict,
)
from src.instrument.file import save_file, open_file
from dataclasses import dataclass
from os.path import exists as os_path_exists


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
    _person_dir: str = None
    _gifts_dir: str = None
    _atoms_dir: str = None

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

    def get_book_atom_numbers(self, giftunit_dict: dict[str:]) -> int:
        book_dict = giftunit_dict.get("book")
        return list(book_dict.keys())

    def get_bookmetric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "gifter": x_dict.get("gifter"),
            "giftees": x_dict.get("giftees"),
            "book_atom_numbers": self.get_book_atom_numbers(x_dict),
        }

    def get_bookmetric_json(self) -> str:
        return get_json_from_dict(self.get_bookmetric_dict())

    def _get_atom_filename(self, atom_number: int) -> str:
        return f"{atom_number}.json"

    def _save_atom_file(self, atom_number: int, x_atom: AgendaAtom):
        save_file(
            self._atoms_dir, self._get_atom_filename(atom_number), x_atom.get_json()
        )

    def atom_file_exists(self, atom_number: int) -> bool:
        return os_path_exists(
            f"{self._atoms_dir}/{self._get_atom_filename(atom_number)}"
        )

    def _open_atom_file(self, atom_number: int) -> AgendaAtom:
        x_json = open_file(self._atoms_dir, self._get_atom_filename(atom_number))
        return agendaatom_get_from_json(x_json)


def giftunit_shop(
    _gifter: PersonID,
    _giftees: set[PersonID] = None,
    _bookunit: BookUnit = None,
    _book_start: int = None,
    _person_dir: str = None,
    _gifts_dir: str = None,
    _atoms_dir: str = None,
):
    # _book_start = get_0_if_None(_book_start)
    _giftees = get_empty_set_if_none(_giftees)
    if _bookunit is None:
        _bookunit = bookunit_shop()

    x_giftunit = GiftUnit(
        _gifter=_gifter,
        _giftees=_giftees,
        _bookunit=_bookunit,
        _person_dir=_person_dir,
        _gifts_dir=_gifts_dir,
        _atoms_dir=_atoms_dir,
    )
    x_giftunit.set_book_start(_book_start)
    return x_giftunit


def giftunit_get_from_dict(x_dict: dict[str:str]) -> GiftUnit:
    x_gifter = x_dict.get("gifter")
    x_giftees = set(x_dict.get("giftees").keys())
    x_book_atom_numbers = set(x_dict.get("book_atom_numbers"))
    x_giftunit = giftunit_shop(x_gifter, x_giftees)
    print(f"{x_book_atom_numbers=}")
    for x_atom_number in x_book_atom_numbers:
        print(f"{x_atom_number=}")

    return x_giftunit
