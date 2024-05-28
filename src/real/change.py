from src._road.road import PersonID
from src.agenda.atom import AgendaAtom, get_from_json as agendaatom_get_from_json
from src.agenda.book import BookUnit, bookunit_shop
from src._instrument.python import (
    get_empty_set_if_none,
    get_json_from_dict,
    get_dict_from_json,
)
from src._instrument.file import save_file, open_file
from dataclasses import dataclass
from os.path import exists as os_path_exists


def get_changes_folder() -> str:
    return "changes"


def init_change_id() -> int:
    return 0


def get_init_change_id_if_None(x_change_id: int = None) -> int:
    return init_change_id() if x_change_id is None else x_change_id


def get_json_filename(filename_without_extention) -> str:
    return f"{filename_without_extention}.json"


@dataclass
class changeUnit:
    _giver: PersonID = None
    _change_id: int = None
    _faces: set[PersonID] = None
    _bookunit: BookUnit = None
    _book_start: int = None
    _person_dir: str = None
    _changes_dir: str = None
    _atoms_dir: str = None

    def set_face(self, x_face: PersonID):
        self._faces.add(x_face)

    def face_exists(self, x_face: PersonID) -> bool:
        return x_face in self._faces

    def del_face(self, x_face: PersonID):
        self._faces.remove(x_face)

    def set_bookunit(self, x_bookunit: BookUnit):
        self._bookunit = x_bookunit

    def del_bookunit(self):
        self._bookunit = bookunit_shop()

    def set_book_start(self, x_book_start: int):
        self._book_start = get_init_change_id_if_None(x_book_start)

    def agendaatom_exists(self, x_agendaatom: AgendaAtom):
        return self._bookunit.agendaatom_exists(x_agendaatom)

    def get_step_dict(self) -> dict[str:]:
        return {
            "changeer": self._giver,
            "faces": {x_face: 1 for x_face in self._faces},
            "book": self._bookunit.get_ordered_agendaatoms(self._book_start),
        }

    def get_book_atom_numbers(self, changeunit_dict: dict[str:]) -> int:
        book_dict = changeunit_dict.get("book")
        return list(book_dict.keys())

    def get_bookmetric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "changeer": x_dict.get("changeer"),
            "faces": x_dict.get("faces"),
            "book_atom_numbers": self.get_book_atom_numbers(x_dict),
        }

    def get_bookmetric_json(self) -> str:
        return get_json_from_dict(self.get_bookmetric_dict())

    def _get_num_filename(self, x_number: int) -> str:
        return get_json_filename(x_number)

    def _save_atom_file(self, atom_number: int, x_atom: AgendaAtom):
        x_filename = self._get_num_filename(atom_number)
        save_file(self._atoms_dir, x_filename, x_atom.get_json())

    def atom_file_exists(self, atom_number: int) -> bool:
        x_filename = self._get_num_filename(atom_number)
        return os_path_exists(f"{self._atoms_dir}/{x_filename}")

    def _open_atom_file(self, atom_number: int) -> AgendaAtom:
        x_json = open_file(self._atoms_dir, self._get_num_filename(atom_number))
        return agendaatom_get_from_json(x_json)

    def _save_change_file(self):
        x_filename = self._get_num_filename(self._change_id)
        save_file(self._changes_dir, x_filename, self.get_bookmetric_json())

    def change_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self._change_id)
        return os_path_exists(f"{self._changes_dir}/{x_filename}")

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_agendaatoms = step_dict.get("book")
        for order_int, agendaatom in ordered_agendaatoms.items():
            self._save_atom_file(order_int, agendaatom)

    def save_files(self):
        self._save_change_file()
        self._save_atom_files()

    def _create_bookunit_from_atom_files(self, atom_number_list: list) -> BookUnit:
        x_bookunit = bookunit_shop()
        for atom_number in atom_number_list:
            x_agendaatom = self._open_atom_file(atom_number)
            x_bookunit.set_agendaatom(x_agendaatom)
        self._bookunit = x_bookunit


def changeunit_shop(
    _giver: PersonID,
    _change_id: int = None,
    _faces: set[PersonID] = None,
    _bookunit: BookUnit = None,
    _book_start: int = None,
    _person_dir: str = None,
    _changes_dir: str = None,
    _atoms_dir: str = None,
):
    if _bookunit is None:
        _bookunit = bookunit_shop()
    x_changeunit = changeUnit(
        _giver=_giver,
        _change_id=get_init_change_id_if_None(_change_id),
        _faces=get_empty_set_if_none(_faces),
        _bookunit=_bookunit,
        _person_dir=_person_dir,
        _changes_dir=_changes_dir,
        _atoms_dir=_atoms_dir,
    )
    x_changeunit.set_book_start(_book_start)
    return x_changeunit


def create_changeunit_from_files(
    changes_dir: str,
    change_id: str,
    atoms_dir: str,
) -> changeUnit:
    change_filename = get_json_filename(change_id)
    change_dict = get_dict_from_json(open_file(changes_dir, change_filename))
    x_giver = change_dict.get("changeer")
    x_faces = set(change_dict.get("faces").keys())
    x_changeunit = changeunit_shop(x_giver, change_id, x_faces, _atoms_dir=atoms_dir)
    book_atom_numbers_list = change_dict.get("book_atom_numbers")
    x_changeunit._create_bookunit_from_atom_files(book_atom_numbers_list)
    return x_changeunit
