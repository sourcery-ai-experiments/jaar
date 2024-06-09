from src._instrument.file import save_file, open_file
from src._instrument.python import (
    get_empty_set_if_none,
    get_json_from_dict,
    get_dict_from_json,
)
from src._road.jaar_config import get_init_atom_id_if_None, get_json_filename
from src._road.road import PersonID
from src.atom.quark import QuarkUnit, get_from_json as quarkunit_get_from_json
from src.atom.nuc import NucUnit, nucunit_shop
from dataclasses import dataclass
from os.path import exists as os_path_exists


@dataclass
class AtomUnit:
    _giver: PersonID = None
    _atom_id: int = None
    _faces: set[PersonID] = None
    _nucunit: NucUnit = None
    _nuc_start: int = None
    _atoms_dir: str = None
    _quarks_dir: str = None

    def set_face(self, x_face: PersonID):
        self._faces.add(x_face)

    def face_exists(self, x_face: PersonID) -> bool:
        return x_face in self._faces

    def del_face(self, x_face: PersonID):
        self._faces.remove(x_face)

    def set_nucunit(self, x_nucunit: NucUnit):
        self._nucunit = x_nucunit

    def del_nucunit(self):
        self._nucunit = nucunit_shop()

    def set_nuc_start(self, x_nuc_start: int):
        self._nuc_start = get_init_atom_id_if_None(x_nuc_start)

    def quarkunit_exists(self, x_quarkunit: QuarkUnit):
        return self._nucunit.quarkunit_exists(x_quarkunit)

    def get_step_dict(self) -> dict[str:]:
        return {
            "giver": self._giver,
            "faces": {x_face: 1 for x_face in self._faces},
            "nuc": self._nucunit.get_ordered_quarkunits(self._nuc_start),
        }

    def get_nuc_quark_numbers(self, atomunit_dict: dict[str:]) -> int:
        nuc_dict = atomunit_dict.get("nuc")
        return list(nuc_dict.keys())

    def get_nucmetric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "giver": x_dict.get("giver"),
            "faces": x_dict.get("faces"),
            "nuc_quark_numbers": self.get_nuc_quark_numbers(x_dict),
        }

    def get_nucmetric_json(self) -> str:
        return get_json_from_dict(self.get_nucmetric_dict())

    def _get_num_filename(self, x_number: int) -> str:
        return get_json_filename(x_number)

    def _save_quark_file(self, quark_number: int, x_quark: QuarkUnit):
        x_filename = self._get_num_filename(quark_number)
        save_file(self._quarks_dir, x_filename, x_quark.get_json())

    def quark_file_exists(self, quark_number: int) -> bool:
        x_filename = self._get_num_filename(quark_number)
        return os_path_exists(f"{self._quarks_dir}/{x_filename}")

    def _open_quark_file(self, quark_number: int) -> QuarkUnit:
        x_json = open_file(self._quarks_dir, self._get_num_filename(quark_number))
        return quarkunit_get_from_json(x_json)

    def _save_atom_file(self):
        x_filename = self._get_num_filename(self._atom_id)
        save_file(self._atoms_dir, x_filename, self.get_nucmetric_json())

    def atom_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self._atom_id)
        return os_path_exists(f"{self._atoms_dir}/{x_filename}")

    def _save_quark_files(self):
        step_dict = self.get_step_dict()
        ordered_quarkunits = step_dict.get("nuc")
        for order_int, quarkunit in ordered_quarkunits.items():
            self._save_quark_file(order_int, quarkunit)

    def save_files(self):
        self._save_atom_file()
        self._save_quark_files()

    def _create_nucunit_from_quark_files(self, quark_number_list: list) -> NucUnit:
        x_nucunit = nucunit_shop()
        for quark_number in quark_number_list:
            x_quarkunit = self._open_quark_file(quark_number)
            x_nucunit.set_quarkunit(x_quarkunit)
        self._nucunit = x_nucunit


def atomunit_shop(
    _giver: PersonID,
    _atom_id: int = None,
    _faces: set[PersonID] = None,
    _nucunit: NucUnit = None,
    _nuc_start: int = None,
    _atoms_dir: str = None,
    _quarks_dir: str = None,
):
    if _nucunit is None:
        _nucunit = nucunit_shop()
    x_atomunit = AtomUnit(
        _giver=_giver,
        _atom_id=get_init_atom_id_if_None(_atom_id),
        _faces=get_empty_set_if_none(_faces),
        _nucunit=_nucunit,
        _atoms_dir=_atoms_dir,
        _quarks_dir=_quarks_dir,
    )
    x_atomunit.set_nuc_start(_nuc_start)
    return x_atomunit


def create_atomunit_from_files(
    atoms_dir: str,
    atom_id: str,
    quarks_dir: str,
) -> AtomUnit:
    atom_filename = get_json_filename(atom_id)
    atom_dict = get_dict_from_json(open_file(atoms_dir, atom_filename))
    x_giver = atom_dict.get("giver")
    x_faces = set(atom_dict.get("faces").keys())
    nuc_quark_numbers_list = atom_dict.get("nuc_quark_numbers")
    x_atomunit = atomunit_shop(x_giver, atom_id, x_faces, _quarks_dir=quarks_dir)
    x_atomunit._create_nucunit_from_quark_files(nuc_quark_numbers_list)
    return x_atomunit
