from src._instrument.file import (
    get_directory_path,
    save_file,
    open_file,
    delete_dir,
    dir_files,
    set_dir,
    get_integer_filenames,
)
from src._instrument.python import get_empty_set_if_none
from src._instrument.sqlite import sqlite_connection
from src._road.jaar_config import (
    roles_str,
    jobs_str,
    grades_folder,
    get_rootpart_of_econ_dir,
    treasury_file_name,
    get_atoms_folder,
    get_test_real_id,
    get_test_reals_dir,
    get_init_atom_id_if_None,
    get_json_filename,
    init_atom_id,
)
from src._road.finance import (
    default_pixel_if_none,
    default_penny_if_none,
    default_money_magnitude_if_none,
)
from src._road.road import (
    PersonID,
    RealID,
    RoadNode,
    RoadUnit,
    rebuild_road,
    get_all_road_nodes,
    validate_roadnode,
    default_road_delimiter_if_none,
)
from src._truth.truth import (
    TruthUnit,
    get_from_json as truthunit_get_from_json,
    truthunit_shop,
)
from src.atom.quark import (
    QuarkUnit,
    get_from_json as quarkunit_get_from_json,
    modify_truth_with_quarkunit,
)
from src.listen.basis_truths import get_default_live_truth
from src.atom.atom import AtomUnit, atomunit_shop, create_atomunit_from_files
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


class Invalid_same_Exception(Exception):
    pass


class Invalid_live_Exception(Exception):
    pass


class SaveAtomFileException(Exception):
    pass


class AtomFileMissingException(Exception):
    pass


class get_econ_roadsException(Exception):
    pass


class _econ_roadMissingException(Exception):
    pass


def get_econ_roles_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{roles_str()}"


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{jobs_str()}"


def get_gift_grades_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{grades_folder()}"


@dataclass
class UserHub:
    person_id: PersonID = None
    reals_dir: str = None
    real_id: str = None
    econ_road: RoadUnit = None
    road_delimiter: str = None
    pixel: float = None
    penny: float = None
    econ_money_magnitude: float = None

    def real_dir(self):
        return f"{self.reals_dir}/{self.real_id}"

    def persons_dir(self):
        return f"{self.real_dir()}/persons"

    def person_dir(self):
        return f"{self.persons_dir()}/{self.person_id}"

    def econs_dir(self):
        return f"{self.person_dir()}/econs"

    def quarks_dir(self):
        return f"{self.person_dir()}/quarks"

    def atoms_dir(self):
        return f"{self.person_dir()}/{get_atoms_folder()}"

    def same_dir(self) -> str:
        return f"{self.person_dir()}/same"

    def live_dir(self) -> str:
        return f"{self.person_dir()}/live"

    def same_file_name(self):
        return get_json_filename(self.person_id)

    def same_file_path(self):
        return f"{self.same_dir()}/{self.same_file_name()}"

    def live_file_name(self):
        return get_json_filename(self.person_id)

    def live_path(self):
        return f"{self.live_dir()}/{self.live_file_name()}"

    def save_file_same(self, file_text: str, replace: bool):
        save_file(
            dest_dir=self.same_dir(),
            file_name=self.same_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def save_file_live(self, file_text: str, replace: bool):
        save_file(
            dest_dir=self.live_dir(),
            file_name=self.live_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def same_file_exists(self) -> bool:
        return os_path_exists(self.same_file_path())

    def live_file_exists(self) -> bool:
        return os_path_exists(self.live_path())

    def open_file_same(self):
        return open_file(self.same_dir(), self.same_file_name())

    def save_same_truth(self, x_truth: TruthUnit):
        if x_truth._owner_id != self.person_id:
            raise Invalid_same_Exception(
                f"TruthUnit with owner_id '{x_truth._owner_id}' cannot be saved as person_id '{self.person_id}''s same truth."
            )
        self.save_file_same(x_truth.get_json(), True)

    def get_same_truth(self) -> TruthUnit:
        if self.same_file_exists() is False:
            return None
        file_content = self.open_file_same()
        return truthunit_get_from_json(file_content)

    def default_same_truth(self) -> TruthUnit:
        x_truthunit = truthunit_shop(
            _owner_id=self.person_id,
            _real_id=self.real_id,
            _road_delimiter=self.road_delimiter,
            _pixel=self.pixel,
            _penny=self.penny,
        )
        x_truthunit._last_atom_id = init_atom_id()
        return x_truthunit

    def delete_same_file(self):
        delete_dir(self.same_file_path())

    def open_file_live(self):
        return open_file(self.live_dir(), self.live_file_name())

    def get_max_quark_file_number(self) -> int:
        if not os_path_exists(self.quarks_dir()):
            return None
        quark_files_dict = dir_files(self.quarks_dir(), True, include_files=True)
        quark_filenames = quark_files_dict.keys()
        quark_file_numbers = {int(quark_filename) for quark_filename in quark_filenames}
        return max(quark_file_numbers, default=None)

    def _get_next_quark_file_number(self) -> int:
        max_file_number = self.get_max_quark_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def quark_file_name(self, quark_number: int) -> str:
        return f"{quark_number}.json"

    def quark_file_path(self, quark_number: int) -> str:
        return f"{self.quarks_dir()}/{self.quark_file_name(quark_number)}"

    def _save_valid_quark_file(self, x_quark: QuarkUnit, file_number: int):
        save_file(
            self.quarks_dir(),
            self.quark_file_name(file_number),
            x_quark.get_json(),
            replace=False,
        )
        return file_number

    def save_quark_file(self, x_quark: QuarkUnit):
        x_quark_filename = self._get_next_quark_file_number()
        return self._save_valid_quark_file(x_quark, x_quark_filename)

    def quark_file_exists(self, quark_number: int) -> bool:
        return os_path_exists(self.quark_file_path(quark_number))

    def delete_quark_file(self, quark_number: int):
        delete_dir(self.quark_file_path(quark_number))

    def _get_truth_from_quark_files(self) -> TruthUnit:
        x_truth = truthunit_shop(self.person_id, self.real_id)
        if self.quark_file_exists(self.get_max_quark_file_number()):
            x_quark_files = dir_files(self.quarks_dir(), delete_extensions=True)
            sorted_quark_filenames = sorted(list(x_quark_files.keys()))

            for x_quark_filename in sorted_quark_filenames:
                x_file_text = x_quark_files.get(x_quark_filename)
                x_quark = quarkunit_get_from_json(x_file_text)
                modify_truth_with_quarkunit(x_truth, x_quark)
        return x_truth

    def get_max_atom_file_number(self) -> int:
        if not os_path_exists(self.atoms_dir()):
            return None
        atoms_dir = self.atoms_dir()
        atom_filenames = dir_files(atoms_dir, True, include_files=True).keys()
        atom_file_numbers = {int(filename) for filename in atom_filenames}
        return max(atom_file_numbers, default=None)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        init_atom_id = get_init_atom_id_if_None()
        return init_atom_id if max_file_number is None else max_file_number + 1

    def atom_file_name(self, atom_id: int) -> str:
        return get_json_filename(atom_id)

    def atom_file_path(self, atom_id: int) -> bool:
        atom_filename = self.atom_file_name(atom_id)
        return f"{self.atoms_dir()}/{atom_filename}"

    def atom_file_exists(self, atom_id: int) -> bool:
        return os_path_exists(self.atom_file_path(atom_id))

    def validate_atomunit(self, x_atomunit: AtomUnit) -> AtomUnit:
        if x_atomunit._quarks_dir != self.quarks_dir():
            x_atomunit._quarks_dir = self.quarks_dir()
        if x_atomunit._atoms_dir != self.atoms_dir():
            x_atomunit._atoms_dir = self.atoms_dir()
        if x_atomunit._atom_id != self._get_next_atom_file_number():
            x_atomunit._atom_id = self._get_next_atom_file_number()
        if x_atomunit.person_id != self.person_id:
            x_atomunit.person_id = self.person_id
        if x_atomunit._nuc_start != self._get_next_quark_file_number():
            x_atomunit._nuc_start = self._get_next_quark_file_number()
        return x_atomunit

    def save_atom_file(
        self,
        x_atom: AtomUnit,
        replace: bool = True,
        correct_invalid_attrs: bool = True,
    ) -> AtomUnit:
        if correct_invalid_attrs:
            x_atom = self.validate_atomunit(x_atom)

        if x_atom._quarks_dir != self.quarks_dir():
            raise SaveAtomFileException(
                f"AtomUnit file cannot be saved because atomunit._quarks_dir is incorrect: {x_atom._quarks_dir}. It must be {self.quarks_dir()}."
            )
        if x_atom._atoms_dir != self.atoms_dir():
            raise SaveAtomFileException(
                f"AtomUnit file cannot be saved because atomunit._atoms_dir is incorrect: {x_atom._atoms_dir}. It must be {self.atoms_dir()}."
            )
        if x_atom.person_id != self.person_id:
            raise SaveAtomFileException(
                f"AtomUnit file cannot be saved because atomunit.person_id is incorrect: {x_atom.person_id}. It must be {self.person_id}."
            )
        atom_filename = self.atom_file_name(x_atom._atom_id)
        if not replace and self.atom_file_exists(x_atom._atom_id):
            raise SaveAtomFileException(
                f"AtomUnit file {atom_filename} already exists and cannot be saved over."
            )
        x_atom.save_files()
        return x_atom

    def _del_atom_file(self, atom_id: int):
        delete_dir(self.atom_file_path(atom_id))

    def _default_atomunit(self) -> AtomUnit:
        return atomunit_shop(
            person_id=self.person_id,
            _atom_id=self._get_next_atom_file_number(),
            _quarks_dir=self.quarks_dir(),
            _atoms_dir=self.atoms_dir(),
        )

    def create_save_atom_file(self, before_truth: TruthUnit, after_truth: TruthUnit):
        new_atomunit = self._default_atomunit()
        new_nucunit = new_atomunit._nucunit
        new_nucunit.add_all_different_quarkunits(before_truth, after_truth)
        self.save_atom_file(new_atomunit)

    def get_atomunit(self, atom_id: int) -> AtomUnit:
        if self.atom_file_exists(atom_id) is False:
            raise AtomFileMissingException(
                f"AtomUnit file_number {atom_id} does not exist."
            )
        x_atoms_dir = self.atoms_dir()
        x_quarks_dir = self.quarks_dir()
        return create_atomunit_from_files(x_atoms_dir, atom_id, x_quarks_dir)

    def _merge_any_atoms(self, x_truth: TruthUnit) -> TruthUnit:
        atoms_dir = self.atoms_dir()
        atom_ints = get_integer_filenames(atoms_dir, x_truth._last_atom_id)
        if len(atom_ints) == 0:
            return copy_deepcopy(x_truth)

        for atom_int in atom_ints:
            x_atom = self.get_atomunit(atom_int)
            new_truth = x_atom._nucunit.get_edited_truth(x_truth)
        return new_truth

    def _create_initial_atom_files_from_default(self):
        x_atomunit = atomunit_shop(
            person_id=self.person_id,
            _atom_id=get_init_atom_id_if_None(),
            _atoms_dir=self.atoms_dir(),
            _quarks_dir=self.quarks_dir(),
        )
        x_atomunit._nucunit.add_all_different_quarkunits(
            before_truth=self.default_same_truth(),
            after_truth=self.default_same_truth(),
        )
        x_atomunit.save_files()

    def _create_same_from_atoms(self):
        x_truth = self._merge_any_atoms(self.default_same_truth())
        self.save_same_truth(x_truth)

    def _create_initial_atom_and_same_files(self):
        self._create_initial_atom_files_from_default()
        self._create_same_from_atoms()

    def _create_initial_atom_files_from_same(self):
        x_atomunit = self._default_atomunit()
        x_atomunit._nucunit.add_all_different_quarkunits(
            before_truth=self.default_same_truth(),
            after_truth=self.get_same_truth(),
        )
        x_atomunit.save_files()

    def initialize_atom_same_files(self):
        x_same_file_exists = self.same_file_exists()
        atom_file_exists = self.atom_file_exists(init_atom_id())
        if x_same_file_exists is False and atom_file_exists is False:
            self._create_initial_atom_and_same_files()
        elif x_same_file_exists is False and atom_file_exists:
            self._create_same_from_atoms()
        elif x_same_file_exists and atom_file_exists is False:
            self._create_initial_atom_files_from_same()

    def append_atoms_to_same_file(self):
        same_truth = self.get_same_truth()
        same_truth = self._merge_any_atoms(same_truth)
        self.save_same_truth(same_truth)
        return self.get_same_truth()

    def econ_dir(self) -> str:
        if self.econ_road is None:
            raise _econ_roadMissingException(
                f"UserHub '{self.person_id}' cannot save to econ_dir because it does not have econ_road."
            )
        return get_econ_path(self, self.econ_road)

    def create_econ_dir_if_missing(self):
        set_dir(self.econ_dir())

    def owner_file_name(self, owner_id: PersonID) -> str:
        return get_json_filename(owner_id)

    def treasury_file_name(self) -> str:
        return treasury_file_name()

    def treasury_db_path(self) -> str:
        return f"{self.econ_dir()}/{treasury_file_name()}"

    def role_path(self, owner_id: PersonID) -> str:
        return f"{self.roles_dir()}/{self.owner_file_name(owner_id)}"

    def job_path(self, owner_id: PersonID) -> str:
        return f"{self.jobs_dir()}/{self.owner_file_name(owner_id)}"

    def grade_path(self, owner_id: PersonID) -> str:
        return f"{self.grades_dir()}/{self.owner_file_name(owner_id)}"

    def roles_dir(self) -> str:
        return get_econ_roles_dir(self.econ_dir())

    def jobs_dir(self) -> str:
        return get_econ_jobs_dir(self.econ_dir())

    def grades_dir(self) -> str:
        return get_gift_grades_dir(self.econ_dir())

    def get_jobs_dir_file_names_list(self):
        try:
            return list(dir_files(self.jobs_dir(), True).keys())
        except Exception:
            return []

    def save_role_truth(self, x_truth: TruthUnit):
        x_file_name = self.owner_file_name(x_truth._owner_id)
        save_file(self.roles_dir(), x_file_name, x_truth.get_json())

    def save_job_truth(self, x_truth: TruthUnit):
        x_file_name = self.owner_file_name(x_truth._owner_id)
        save_file(self.jobs_dir(), x_file_name, x_truth.get_json())

    def save_live_truth(self, x_truth: TruthUnit):
        if x_truth._owner_id != self.person_id:
            raise Invalid_live_Exception(
                f"TruthUnit with owner_id '{x_truth._owner_id}' cannot be saved as person_id '{self.person_id}''s live truth."
            )
        self.save_file_live(x_truth.get_json(), True)

    def initialize_live_file(self, same: TruthUnit):
        if self.live_file_exists() is False:
            self.save_live_truth(get_default_live_truth(same))

    def role_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.role_path(owner_id))

    def job_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.job_path(owner_id))

    def get_role_truth(self, owner_id: PersonID) -> TruthUnit:
        if self.role_file_exists(owner_id) is False:
            return None
        file_content = open_file(self.roles_dir(), self.owner_file_name(owner_id))
        return truthunit_get_from_json(file_content)

    def get_job_truth(self, owner_id: PersonID) -> TruthUnit:
        if self.job_file_exists(owner_id) is False:
            return None
        file_content = open_file(self.jobs_dir(), self.owner_file_name(owner_id))
        return truthunit_get_from_json(file_content)

    def get_live_truth(self) -> TruthUnit:
        if self.live_file_exists() is False:
            return None
        file_content = self.open_file_live()
        return truthunit_get_from_json(file_content)

    def delete_role_file(self, owner_id: PersonID):
        delete_dir(self.role_path(owner_id))

    def delete_job_file(self, owner_id: PersonID):
        delete_dir(self.job_path(owner_id))

    def delete_treasury_db_file(self):
        delete_dir(self.treasury_db_path())

    def dw_speaker_truth(self, speaker_id: PersonID) -> TruthUnit:
        speaker_userhub = userhub_shop(
            reals_dir=self.reals_dir,
            real_id=self.real_id,
            person_id=speaker_id,
            road_delimiter=self.road_delimiter,
            pixel=self.pixel,
        )
        return speaker_userhub.get_live_truth()

    def get_perspective_truth(self, speaker: TruthUnit) -> TruthUnit:
        # get copy of truth without any metrics
        perspective_truth = truthunit_get_from_json(speaker.get_json())
        perspective_truth.set_owner_id(self.person_id)
        return perspective_truth

    def get_dw_perspective_truth(self, speaker_id: PersonID) -> TruthUnit:
        return self.get_perspective_truth(self.dw_speaker_truth(speaker_id))

    def rj_speaker_truth(self, healer_id: PersonID, speaker_id: PersonID) -> TruthUnit:
        speaker_userhub = userhub_shop(
            reals_dir=self.reals_dir,
            real_id=self.real_id,
            person_id=healer_id,
            econ_road=self.econ_road,
            road_delimiter=self.road_delimiter,
            pixel=self.pixel,
        )
        return speaker_userhub.get_job_truth(speaker_id)

    def rj_perspective_truth(
        self, healer_id: PersonID, speaker_id: PersonID
    ) -> TruthUnit:
        speaker_job = self.rj_speaker_truth(healer_id, speaker_id)
        return self.get_perspective_truth(speaker_job)

    def get_econ_roads(self):
        x_same_truth = self.get_same_truth()
        x_same_truth.calc_truth_metrics()
        if x_same_truth._econs_justified is False:
            x_str = f"Cannot get_econ_roads from '{self.person_id}' same truth because 'TruthUnit._econs_justified' is False."
            raise get_econ_roadsException(x_str)
        if x_same_truth._econs_buildable is False:
            x_str = f"Cannot get_econ_roads from '{self.person_id}' same truth because 'TruthUnit._econs_buildable' is False."
            raise get_econ_roadsException(x_str)
        person_healer_dict = x_same_truth._healers_dict.get(self.person_id)
        if person_healer_dict is None:
            return get_empty_set_if_none(None)
        econ_roads = x_same_truth._healers_dict.get(self.person_id).keys()
        return get_empty_set_if_none(econ_roads)

    def save_all_same_roles(self):
        same = self.get_same_truth()
        for x_econ_road in self.get_econ_roads():
            self.econ_road = x_econ_road
            self.save_role_truth(same)
        self.econ_road = None

    def create_treasury_db_file(self):
        self.create_econ_dir_if_missing()
        with sqlite3_connect(self.treasury_db_path()) as conn:
            pass

    def treasury_db_file_exists(self) -> bool:
        return os_path_exists(self.treasury_db_path())

    def treasury_db_file_conn(self) -> Connection:
        if self.econ_road is None:
            raise _econ_roadMissingException(
                f"userhub cannot connect to treasury_db_file because econ_road is {self.econ_road}"
            )
        if self.treasury_db_file_exists() is False:
            self.create_treasury_db_file()
        return sqlite_connection(self.treasury_db_path())

    def create_same_treasury_db_files(self):
        for x_econ_road in self.get_econ_roads():
            self.econ_road = x_econ_road
            self.create_treasury_db_file()
        self.econ_road = None


def userhub_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID = None,
    econ_road: RoadUnit = None,
    road_delimiter: str = None,
    pixel: float = None,
    penny: float = None,
    econ_money_magnitude: float = None,
) -> UserHub:
    if reals_dir is None:
        reals_dir = get_test_reals_dir()
    if real_id is None:
        real_id = get_test_real_id()

    return UserHub(
        reals_dir=reals_dir,
        real_id=real_id,
        person_id=validate_roadnode(person_id, road_delimiter),
        econ_road=econ_road,
        road_delimiter=default_road_delimiter_if_none(road_delimiter),
        pixel=default_pixel_if_none(pixel),
        penny=default_penny_if_none(penny),
        econ_money_magnitude=default_money_magnitude_if_none(econ_money_magnitude),
    )


def get_econ_path(x_userhub: UserHub, x_road: RoadNode) -> str:
    econ_root = get_rootpart_of_econ_dir()
    x_road = rebuild_road(x_road, x_userhub.real_id, econ_root)
    x_list = get_all_road_nodes(x_road, x_userhub.road_delimiter)
    return f"{x_userhub.econs_dir()}{get_directory_path(x_list=[*x_list])}"
