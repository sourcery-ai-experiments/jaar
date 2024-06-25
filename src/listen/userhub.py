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
    get_gifts_folder,
    get_test_real_id,
    get_test_reals_dir,
    get_init_gift_id_if_None,
    get_json_filename,
    init_gift_id,
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
from src._world.world import (
    WorldUnit,
    get_from_json as worldunit_get_from_json,
    worldunit_shop,
)
from src.gift.atom import (
    AtomUnit,
    get_from_json as atomunit_get_from_json,
    modify_world_with_atomunit,
)
from src.listen.basis_worlds import get_default_live_world
from src.gift.gift import GiftUnit, giftunit_shop, create_giftunit_from_files
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


class Invalid_same_Exception(Exception):
    pass


class Invalid_live_Exception(Exception):
    pass


class SaveGiftFileException(Exception):
    pass


class GiftFileMissingException(Exception):
    pass


class get_econ_roadsException(Exception):
    pass


class _econ_roadMissingException(Exception):
    pass


def get_econ_roles_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{roles_str()}"


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{jobs_str()}"


def get_econ_grades_dir(x_econ_dir: str) -> str:
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

    def atoms_dir(self):
        return f"{self.person_dir()}/atoms"

    def gifts_dir(self):
        return f"{self.person_dir()}/{get_gifts_folder()}"

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

    def save_same_world(self, x_world: WorldUnit):
        if x_world._owner_id != self.person_id:
            raise Invalid_same_Exception(
                f"WorldUnit with owner_id '{x_world._owner_id}' cannot be saved as person_id '{self.person_id}''s same world."
            )
        self.save_file_same(x_world.get_json(), True)

    def get_same_world(self) -> WorldUnit:
        if self.same_file_exists() is False:
            return None
        file_content = self.open_file_same()
        return worldunit_get_from_json(file_content)

    def default_same_world(self) -> WorldUnit:
        x_worldunit = worldunit_shop(
            _owner_id=self.person_id,
            _real_id=self.real_id,
            _road_delimiter=self.road_delimiter,
            _pixel=self.pixel,
            _penny=self.penny,
        )
        x_worldunit._last_gift_id = init_gift_id()
        return x_worldunit

    def delete_same_file(self):
        delete_dir(self.same_file_path())

    def open_file_live(self):
        return open_file(self.live_dir(), self.live_file_name())

    def get_max_atom_file_number(self) -> int:
        if not os_path_exists(self.atoms_dir()):
            return None
        atom_files_dict = dir_files(self.atoms_dir(), True, include_files=True)
        atom_filenames = atom_files_dict.keys()
        atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
        return max(atom_file_numbers, default=None)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def atom_file_name(self, atom_number: int) -> str:
        return f"{atom_number}.json"

    def atom_file_path(self, atom_number: int) -> str:
        return f"{self.atoms_dir()}/{self.atom_file_name(atom_number)}"

    def _save_valid_atom_file(self, x_atom: AtomUnit, file_number: int):
        save_file(
            self.atoms_dir(),
            self.atom_file_name(file_number),
            x_atom.get_json(),
            replace=False,
        )
        return file_number

    def save_atom_file(self, x_atom: AtomUnit):
        x_atom_filename = self._get_next_atom_file_number()
        return self._save_valid_atom_file(x_atom, x_atom_filename)

    def atom_file_exists(self, atom_number: int) -> bool:
        return os_path_exists(self.atom_file_path(atom_number))

    def delete_atom_file(self, atom_number: int):
        delete_dir(self.atom_file_path(atom_number))

    def _get_world_from_atom_files(self) -> WorldUnit:
        x_world = worldunit_shop(self.person_id, self.real_id)
        if self.atom_file_exists(self.get_max_atom_file_number()):
            x_atom_files = dir_files(self.atoms_dir(), delete_extensions=True)
            sorted_atom_filenames = sorted(list(x_atom_files.keys()))

            for x_atom_filename in sorted_atom_filenames:
                x_file_text = x_atom_files.get(x_atom_filename)
                x_atom = atomunit_get_from_json(x_file_text)
                modify_world_with_atomunit(x_world, x_atom)
        return x_world

    def get_max_gift_file_number(self) -> int:
        if not os_path_exists(self.gifts_dir()):
            return None
        gifts_dir = self.gifts_dir()
        gift_filenames = dir_files(gifts_dir, True, include_files=True).keys()
        gift_file_numbers = {int(filename) for filename in gift_filenames}
        return max(gift_file_numbers, default=None)

    def _get_next_gift_file_number(self) -> int:
        max_file_number = self.get_max_gift_file_number()
        init_gift_id = get_init_gift_id_if_None()
        return init_gift_id if max_file_number is None else max_file_number + 1

    def gift_file_name(self, gift_id: int) -> str:
        return get_json_filename(gift_id)

    def gift_file_path(self, gift_id: int) -> bool:
        gift_filename = self.gift_file_name(gift_id)
        return f"{self.gifts_dir()}/{gift_filename}"

    def gift_file_exists(self, gift_id: int) -> bool:
        return os_path_exists(self.gift_file_path(gift_id))

    def validate_giftunit(self, x_giftunit: GiftUnit) -> GiftUnit:
        if x_giftunit._atoms_dir != self.atoms_dir():
            x_giftunit._atoms_dir = self.atoms_dir()
        if x_giftunit._gifts_dir != self.gifts_dir():
            x_giftunit._gifts_dir = self.gifts_dir()
        if x_giftunit._gift_id != self._get_next_gift_file_number():
            x_giftunit._gift_id = self._get_next_gift_file_number()
        if x_giftunit.person_id != self.person_id:
            x_giftunit.person_id = self.person_id
        if x_giftunit._change_start != self._get_next_atom_file_number():
            x_giftunit._change_start = self._get_next_atom_file_number()
        return x_giftunit

    def save_gift_file(
        self,
        x_gift: GiftUnit,
        replace: bool = True,
        correct_invalid_attrs: bool = True,
    ) -> GiftUnit:
        if correct_invalid_attrs:
            x_gift = self.validate_giftunit(x_gift)

        if x_gift._atoms_dir != self.atoms_dir():
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {x_gift._atoms_dir}. It must be {self.atoms_dir()}."
            )
        if x_gift._gifts_dir != self.gifts_dir():
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {x_gift._gifts_dir}. It must be {self.gifts_dir()}."
            )
        if x_gift.person_id != self.person_id:
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit.person_id is incorrect: {x_gift.person_id}. It must be {self.person_id}."
            )
        gift_filename = self.gift_file_name(x_gift._gift_id)
        if not replace and self.gift_file_exists(x_gift._gift_id):
            raise SaveGiftFileException(
                f"GiftUnit file {gift_filename} already exists and cannot be saved over."
            )
        x_gift.save_files()
        return x_gift

    def _del_gift_file(self, gift_id: int):
        delete_dir(self.gift_file_path(gift_id))

    def _default_giftunit(self) -> GiftUnit:
        return giftunit_shop(
            person_id=self.person_id,
            _gift_id=self._get_next_gift_file_number(),
            _atoms_dir=self.atoms_dir(),
            _gifts_dir=self.gifts_dir(),
        )

    def create_save_gift_file(self, before_world: WorldUnit, after_world: WorldUnit):
        new_giftunit = self._default_giftunit()
        new_changeunit = new_giftunit._changeunit
        new_changeunit.add_all_different_atomunits(before_world, after_world)
        self.save_gift_file(new_giftunit)

    def get_giftunit(self, gift_id: int) -> GiftUnit:
        if self.gift_file_exists(gift_id) is False:
            raise GiftFileMissingException(
                f"GiftUnit file_number {gift_id} does not exist."
            )
        x_gifts_dir = self.gifts_dir()
        x_atoms_dir = self.atoms_dir()
        return create_giftunit_from_files(x_gifts_dir, gift_id, x_atoms_dir)

    def _merge_any_gifts(self, x_world: WorldUnit) -> WorldUnit:
        gifts_dir = self.gifts_dir()
        gift_ints = get_integer_filenames(gifts_dir, x_world._last_gift_id)
        if len(gift_ints) == 0:
            return copy_deepcopy(x_world)

        for gift_int in gift_ints:
            x_gift = self.get_giftunit(gift_int)
            new_world = x_gift._changeunit.get_edited_world(x_world)
        return new_world

    def _create_initial_gift_files_from_default(self):
        x_giftunit = giftunit_shop(
            person_id=self.person_id,
            _gift_id=get_init_gift_id_if_None(),
            _gifts_dir=self.gifts_dir(),
            _atoms_dir=self.atoms_dir(),
        )
        x_giftunit._changeunit.add_all_different_atomunits(
            before_world=self.default_same_world(),
            after_world=self.default_same_world(),
        )
        x_giftunit.save_files()

    def _create_same_from_gifts(self):
        x_world = self._merge_any_gifts(self.default_same_world())
        self.save_same_world(x_world)

    def _create_initial_gift_and_same_files(self):
        self._create_initial_gift_files_from_default()
        self._create_same_from_gifts()

    def _create_initial_gift_files_from_same(self):
        x_giftunit = self._default_giftunit()
        x_giftunit._changeunit.add_all_different_atomunits(
            before_world=self.default_same_world(),
            after_world=self.get_same_world(),
        )
        x_giftunit.save_files()

    def initialize_gift_same_files(self):
        x_same_file_exists = self.same_file_exists()
        gift_file_exists = self.gift_file_exists(init_gift_id())
        if x_same_file_exists is False and gift_file_exists is False:
            self._create_initial_gift_and_same_files()
        elif x_same_file_exists is False and gift_file_exists:
            self._create_same_from_gifts()
        elif x_same_file_exists and gift_file_exists is False:
            self._create_initial_gift_files_from_same()

    def append_gifts_to_same_file(self):
        same_world = self.get_same_world()
        same_world = self._merge_any_gifts(same_world)
        self.save_same_world(same_world)
        return self.get_same_world()

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
        return get_econ_grades_dir(self.econ_dir())

    def get_jobs_dir_file_names_list(self):
        try:
            return list(dir_files(self.jobs_dir(), True).keys())
        except Exception:
            return []

    def save_role_world(self, x_world: WorldUnit):
        x_file_name = self.owner_file_name(x_world._owner_id)
        save_file(self.roles_dir(), x_file_name, x_world.get_json())

    def save_job_world(self, x_world: WorldUnit):
        x_file_name = self.owner_file_name(x_world._owner_id)
        save_file(self.jobs_dir(), x_file_name, x_world.get_json())

    def save_live_world(self, x_world: WorldUnit):
        if x_world._owner_id != self.person_id:
            raise Invalid_live_Exception(
                f"WorldUnit with owner_id '{x_world._owner_id}' cannot be saved as person_id '{self.person_id}''s live world."
            )
        self.save_file_live(x_world.get_json(), True)

    def initialize_live_file(self, same: WorldUnit):
        if self.live_file_exists() is False:
            self.save_live_world(get_default_live_world(same))

    def role_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.role_path(owner_id))

    def job_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.job_path(owner_id))

    def get_role_world(self, owner_id: PersonID) -> WorldUnit:
        if self.role_file_exists(owner_id) is False:
            return None
        file_content = open_file(self.roles_dir(), self.owner_file_name(owner_id))
        return worldunit_get_from_json(file_content)

    def get_job_world(self, owner_id: PersonID) -> WorldUnit:
        if self.job_file_exists(owner_id) is False:
            return None
        file_content = open_file(self.jobs_dir(), self.owner_file_name(owner_id))
        return worldunit_get_from_json(file_content)

    def get_live_world(self) -> WorldUnit:
        if self.live_file_exists() is False:
            return None
        file_content = self.open_file_live()
        return worldunit_get_from_json(file_content)

    def delete_role_file(self, owner_id: PersonID):
        delete_dir(self.role_path(owner_id))

    def delete_job_file(self, owner_id: PersonID):
        delete_dir(self.job_path(owner_id))

    def delete_treasury_db_file(self):
        delete_dir(self.treasury_db_path())

    def dw_speaker_world(self, speaker_id: PersonID) -> WorldUnit:
        speaker_userhub = userhub_shop(
            reals_dir=self.reals_dir,
            real_id=self.real_id,
            person_id=speaker_id,
            road_delimiter=self.road_delimiter,
            pixel=self.pixel,
        )
        return speaker_userhub.get_live_world()

    def get_perspective_world(self, speaker: WorldUnit) -> WorldUnit:
        # get copy of world without any metrics
        perspective_world = worldunit_get_from_json(speaker.get_json())
        perspective_world.set_owner_id(self.person_id)
        return perspective_world

    def get_dw_perspective_world(self, speaker_id: PersonID) -> WorldUnit:
        return self.get_perspective_world(self.dw_speaker_world(speaker_id))

    def rj_speaker_world(self, healer_id: PersonID, speaker_id: PersonID) -> WorldUnit:
        speaker_userhub = userhub_shop(
            reals_dir=self.reals_dir,
            real_id=self.real_id,
            person_id=healer_id,
            econ_road=self.econ_road,
            road_delimiter=self.road_delimiter,
            pixel=self.pixel,
        )
        return speaker_userhub.get_job_world(speaker_id)

    def rj_perspective_world(
        self, healer_id: PersonID, speaker_id: PersonID
    ) -> WorldUnit:
        speaker_job = self.rj_speaker_world(healer_id, speaker_id)
        return self.get_perspective_world(speaker_job)

    def get_econ_roads(self):
        x_same_world = self.get_same_world()
        x_same_world.calc_world_metrics()
        if x_same_world._econs_justified is False:
            x_str = f"Cannot get_econ_roads from '{self.person_id}' same world because 'WorldUnit._econs_justified' is False."
            raise get_econ_roadsException(x_str)
        if x_same_world._econs_buildable is False:
            x_str = f"Cannot get_econ_roads from '{self.person_id}' same world because 'WorldUnit._econs_buildable' is False."
            raise get_econ_roadsException(x_str)
        person_healer_dict = x_same_world._healers_dict.get(self.person_id)
        if person_healer_dict is None:
            return get_empty_set_if_none(None)
        econ_roads = x_same_world._healers_dict.get(self.person_id).keys()
        return get_empty_set_if_none(econ_roads)

    def save_all_same_roles(self):
        same = self.get_same_world()
        for x_econ_road in self.get_econ_roads():
            self.econ_road = x_econ_road
            self.save_role_world(same)
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
