from src._road.road import RoadUnit, PersonID
from src.agenda.atom import AgendaAtom, get_from_json as agendaatom_get_from_json
from src.agenda.book import BookUnit, bookunit_shop
from src.instrument.python import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_empty_set_if_none,
    get_json_from_dict,
    get_dict_from_json,
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
    _gift_id: int = None
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

    def get_giftmetric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "gifter": x_dict.get("gifter"),
            "giftees": x_dict.get("giftees"),
            "book_atom_numbers": self.get_book_atom_numbers(x_dict),
        }

    def get_bookmetric_json(self) -> str:
        return get_json_from_dict(self.get_giftmetric_dict())

    def _get_num_filename(self, x_number: int) -> str:
        return get_json_filename(x_number)

    def _save_atom_file(self, atom_number: int, x_atom: AgendaAtom):
        save_file(
            self._atoms_dir, self._get_num_filename(atom_number), x_atom.get_json()
        )

    def atom_file_exists(self, atom_number: int) -> bool:
        return os_path_exists(
            f"{self._atoms_dir}/{self._get_num_filename(atom_number)}"
        )

    def _open_atom_file(self, atom_number: int) -> AgendaAtom:
        x_json = open_file(self._atoms_dir, self._get_num_filename(atom_number))
        return agendaatom_get_from_json(x_json)

    def _save_gift_file(self):
        save_file(
            self._gifts_dir,
            self._get_num_filename(self._gift_id),
            file_text=self.get_bookmetric_json(),
        )

    def gift_file_exists(self) -> bool:
        return os_path_exists(
            f"{self._gifts_dir}/{self._get_num_filename(self._gift_id)}"
        )

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_agendaatoms = step_dict.get("book")
        for order_int, agendaatom in ordered_agendaatoms.items():
            self._save_atom_file(order_int, agendaatom)

    def save_files(self):
        self._save_gift_file()
        self._save_atom_files()

    def _create_bookunit_from_atom_files(self, atom_number_list: list) -> BookUnit:
        x_bookunit = bookunit_shop()
        for atom_number in atom_number_list:
            x_agendaatom = self._open_atom_file(atom_number)
            x_bookunit.set_agendaatom(x_agendaatom)
        self._bookunit = x_bookunit


def giftunit_shop(
    _gifter: PersonID,
    _gift_id: int = None,
    _giftees: set[PersonID] = None,
    _bookunit: BookUnit = None,
    _book_start: int = None,
    _person_dir: str = None,
    _gifts_dir: str = None,
    _atoms_dir: str = None,
):
    # _book_start = get_0_if_None(_book_start)
    _gift_id = get_0_if_None(_gift_id)
    _giftees = get_empty_set_if_none(_giftees)
    if _bookunit is None:
        _bookunit = bookunit_shop()

    x_giftunit = GiftUnit(
        _gifter=_gifter,
        _gift_id=_gift_id,
        _giftees=_giftees,
        _bookunit=_bookunit,
        _person_dir=_person_dir,
        _gifts_dir=_gifts_dir,
        _atoms_dir=_atoms_dir,
    )
    x_giftunit.set_book_start(_book_start)
    return x_giftunit


def get_json_filename(filename_without_extention) -> str:
    return f"{filename_without_extention}.json"


def create_giftunit_from_files(
    gifts_dir: str,
    gift_id: str,
    atoms_dir: str,
) -> GiftUnit:
    gift_filename = get_json_filename(gift_id)
    gift_dict = get_dict_from_json(open_file(gifts_dir, gift_filename))
    x_gifter = gift_dict.get("gifter")
    x_giftees = set(gift_dict.get("giftees").keys())
    x_giftunit = giftunit_shop(x_gifter, gift_id, x_giftees, _atoms_dir=atoms_dir)
    book_atom_numbers_list = gift_dict.get("book_atom_numbers")
    x_giftunit._create_bookunit_from_atom_files(book_atom_numbers_list)
    return x_giftunit
