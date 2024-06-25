from src._instrument.file import save_file, open_file
from src._instrument.python import (
    get_empty_set_if_none,
    get_json_from_dict,
    get_dict_from_json,
)
from src._road.jaar_config import get_init_gift_id_if_None, get_json_filename
from src._road.road import PersonID, RealID, get_default_real_id_roadnode
from src.gift.atom import AtomUnit, get_from_json as atomunit_get_from_json
from src.gift.change import ChangeUnit, changeunit_shop
from dataclasses import dataclass
from os.path import exists as os_path_exists


@dataclass
class GiftUnit:
    real_id: RealID = None
    person_id: PersonID = None
    _gift_id: int = None
    _faces: set[PersonID] = None
    _changeunit: ChangeUnit = None
    _change_start: int = None
    _gifts_dir: str = None
    _atoms_dir: str = None

    def set_face(self, x_face: PersonID):
        self._faces.add(x_face)

    def face_exists(self, x_face: PersonID) -> bool:
        return x_face in self._faces

    def del_face(self, x_face: PersonID):
        self._faces.remove(x_face)

    def set_changeunit(self, x_changeunit: ChangeUnit):
        self._changeunit = x_changeunit

    def del_changeunit(self):
        self._changeunit = changeunit_shop()

    def set_change_start(self, x_change_start: int):
        self._change_start = get_init_gift_id_if_None(x_change_start)

    def atomunit_exists(self, x_atomunit: AtomUnit):
        return self._changeunit.atomunit_exists(x_atomunit)

    def get_step_dict(self) -> dict[str:]:
        return {
            "real_id": self.real_id,
            "person_id": self.person_id,
            "faces": {x_face: 1 for x_face in self._faces},
            "change": self._changeunit.get_ordered_atomunits(self._change_start),
        }

    def get_change_atom_numbers(self, giftunit_dict: dict[str:]) -> int:
        change_dict = giftunit_dict.get("change")
        return list(change_dict.keys())

    def get_changemetric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "person_id": x_dict.get("person_id"),
            "faces": x_dict.get("faces"),
            "change_atom_numbers": self.get_change_atom_numbers(x_dict),
        }

    def get_changemetric_json(self) -> str:
        return get_json_from_dict(self.get_changemetric_dict())

    def _get_num_filename(self, x_number: int) -> str:
        return get_json_filename(x_number)

    def _save_atom_file(self, atom_number: int, x_atom: AtomUnit):
        x_filename = self._get_num_filename(atom_number)
        save_file(self._atoms_dir, x_filename, x_atom.get_json())

    def atom_file_exists(self, atom_number: int) -> bool:
        x_filename = self._get_num_filename(atom_number)
        return os_path_exists(f"{self._atoms_dir}/{x_filename}")

    def _open_atom_file(self, atom_number: int) -> AtomUnit:
        x_json = open_file(self._atoms_dir, self._get_num_filename(atom_number))
        return atomunit_get_from_json(x_json)

    def _save_gift_file(self):
        x_filename = self._get_num_filename(self._gift_id)
        save_file(self._gifts_dir, x_filename, self.get_changemetric_json())

    def gift_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self._gift_id)
        return os_path_exists(f"{self._gifts_dir}/{x_filename}")

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_atomunits = step_dict.get("change")
        for order_int, atomunit in ordered_atomunits.items():
            self._save_atom_file(order_int, atomunit)

    def save_files(self):
        self._save_gift_file()
        self._save_atom_files()

    def _create_changeunit_from_atom_files(self, atom_number_list: list) -> ChangeUnit:
        x_changeunit = changeunit_shop()
        for atom_number in atom_number_list:
            x_atomunit = self._open_atom_file(atom_number)
            x_changeunit.set_atomunit(x_atomunit)
        self._changeunit = x_changeunit


def giftunit_shop(
    person_id: PersonID,
    real_id: RealID = None,
    _gift_id: int = None,
    _faces: set[PersonID] = None,
    _changeunit: ChangeUnit = None,
    _change_start: int = None,
    _gifts_dir: str = None,
    _atoms_dir: str = None,
):
    if _changeunit is None:
        _changeunit = changeunit_shop()
    if real_id is None:
        real_id = get_default_real_id_roadnode()
    x_giftunit = GiftUnit(
        real_id=real_id,
        person_id=person_id,
        _gift_id=get_init_gift_id_if_None(_gift_id),
        _faces=get_empty_set_if_none(_faces),
        _changeunit=_changeunit,
        _gifts_dir=_gifts_dir,
        _atoms_dir=_atoms_dir,
    )
    x_giftunit.set_change_start(_change_start)
    return x_giftunit


def create_giftunit_from_files(
    gifts_dir: str,
    gift_id: str,
    atoms_dir: str,
) -> GiftUnit:
    gift_filename = get_json_filename(gift_id)
    gift_dict = get_dict_from_json(open_file(gifts_dir, gift_filename))
    x_person_id = gift_dict.get("person_id")
    x_real_id = gift_dict.get("real_id")
    x_faces = set(gift_dict.get("faces").keys())
    change_atom_numbers_list = gift_dict.get("change_atom_numbers")
    x_giftunit = giftunit_shop(
        person_id=x_person_id,
        real_id=x_real_id,
        _gift_id=gift_id,
        _faces=x_faces,
        _atoms_dir=atoms_dir,
    )
    x_giftunit._create_changeunit_from_atom_files(change_atom_numbers_list)
    return x_giftunit
