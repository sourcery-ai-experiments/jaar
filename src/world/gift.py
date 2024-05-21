from src._road.road import PersonID
from src.agenda.atom import AgendaAtom, get_from_json as agendaatom_get_from_json
from src.agenda.book import BookUnit, bookunit_shop
from src.instrument.python import (
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


def init_gift_id() -> int:
    return 0


def get_init_gift_id_if_None(x_gift_id: int = None) -> int:
    return init_gift_id() if x_gift_id is None else x_gift_id


@dataclass
class GiftUnit:
    _giver: PersonID = None
    _gift_id: int = None
    _takers: set[PersonID] = None
    _bookunit: BookUnit = None
    _book_start: int = None
    _person_dir: str = None
    _gifts_dir: str = None
    _atoms_dir: str = None

    def set_taker(self, x_taker: PersonID):
        self._takers.add(x_taker)

    def taker_exists(self, x_taker: PersonID) -> bool:
        return x_taker in self._takers

    def del_taker(self, x_taker: PersonID):
        self._takers.remove(x_taker)

    def set_bookunit(self, x_bookunit: BookUnit):
        self._bookunit = x_bookunit

    def del_bookunit(self):
        self._bookunit = bookunit_shop()

    def set_book_start(self, x_book_start: int):
        self._book_start = get_init_gift_id_if_None(x_book_start)

    def agendaatom_exists(self, x_agendaatom: AgendaAtom):
        return self._bookunit.agendaatom_exists(x_agendaatom)

    def get_step_dict(self) -> dict[str:]:
        takers_dict = {x_taker: 1 for x_taker in self._takers}
        return {
            "gifter": self._giver,
            "takers": takers_dict,
            "book": self._bookunit.get_ordered_agendaatoms(self._book_start),
        }

    def get_book_atom_numbers(self, giftunit_dict: dict[str:]) -> int:
        book_dict = giftunit_dict.get("book")
        return list(book_dict.keys())

    def get_bookmetric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "gifter": x_dict.get("gifter"),
            "takers": x_dict.get("takers"),
            "book_atom_numbers": self.get_book_atom_numbers(x_dict),
        }

    def get_bookmetric_json(self) -> str:
        return get_json_from_dict(self.get_bookmetric_dict())

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
    _giver: PersonID,
    _gift_id: int = None,
    _takers: set[PersonID] = None,
    _bookunit: BookUnit = None,
    _book_start: int = None,
    _person_dir: str = None,
    _gifts_dir: str = None,
    _atoms_dir: str = None,
):
    # _book_start = get_0_if_None(_book_start)
    _gift_id = get_init_gift_id_if_None(_gift_id)
    _takers = get_empty_set_if_none(_takers)
    if _bookunit is None:
        _bookunit = bookunit_shop()

    x_giftunit = GiftUnit(
        _giver=_giver,
        _gift_id=_gift_id,
        _takers=_takers,
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
    x_giver = gift_dict.get("gifter")
    x_takers = set(gift_dict.get("takers").keys())
    x_giftunit = giftunit_shop(x_giver, gift_id, x_takers, _atoms_dir=atoms_dir)
    book_atom_numbers_list = gift_dict.get("book_atom_numbers")
    x_giftunit._create_bookunit_from_atom_files(book_atom_numbers_list)
    return x_giftunit
