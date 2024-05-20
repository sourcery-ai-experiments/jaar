from src._road.finance import default_planck_if_none
from src._road.road import (
    default_road_delimiter_if_none,
    PersonID,
    validate_roadnode,
    RoadUnit,
    RoadNode,
    get_all_road_nodes,
    change_road,
    create_road_from_nodes,
)
from src.agenda.group import GroupID
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agenda_get_from_json,
)
from src.agenda.atom import (
    AgendaAtom,
    get_from_json as agendaatom_get_from_json,
    change_agenda_with_agendaatom,
)
from src.agenda.promise import create_promise
from src.econ.econ import EconUnit, econunit_shop, treasury_db_filename
from src.world.gift import (
    GiftUnit,
    giftunit_shop,
    get_json_filename as giftunit_get_json_filename,
    create_giftunit_from_files,
)
from src.world.examples.world_env_kit import get_test_worlds_dir, get_test_world_id
from src.instrument.python import get_empty_dict_if_none
from src.instrument.file import (
    save_file,
    open_file,
    set_dir,
    get_directory_path,
    get_all_dirs_with_file,
    get_parts_dir,
    delete_dir,
    dir_files,
)
from dataclasses import dataclass
from os.path import exists as os_path_exists


class InvalidEconException(Exception):
    pass


class PersonCreateEconUnitsException(Exception):
    pass


class Invalid_gut_Exception(Exception):
    pass


class Invalid_live_Exception(Exception):
    pass


class SaveGiftFileException(Exception):
    pass


class GiftFileMissingException(Exception):
    pass


def get_gut_file_name() -> str:
    return "gut"


def get_live_file_name() -> str:
    return "live"


@dataclass
class PersonUnit:
    person_id: PersonID = None
    worlds_dir: str = None
    world_id: str = None
    persons_dir: str = None
    person_dir: str = None
    _econs_dir: str = None
    _atoms_dir: str = None
    _gifts_dir: str = None
    _gut_obj: AgendaUnit = None
    _gut_file_name: str = None
    _gut_path: str = None
    _live_obj: AgendaUnit = None
    _live_file_name: str = None
    _live_path: str = None
    _econ_objs: dict[RoadUnit:EconUnit] = None
    _road_delimiter: str = None
    _planck: float = None

    def set_person_id(self, x_person_id: PersonID):
        self.person_id = validate_roadnode(x_person_id, self._road_delimiter)
        if self.world_id is None:
            self.world_id = get_test_world_id()
        if self.worlds_dir is None:
            self.worlds_dir = get_test_worlds_dir()
        self.world_dir = f"{self.worlds_dir}/{self.world_id}"
        self.persons_dir = f"{self.world_dir}/persons"
        self.person_dir = f"{self.persons_dir}/{self.person_id}"
        self._econs_dir = f"{self.person_dir}/econs"
        self._atoms_dir = f"{self.person_dir}/atoms"
        self._gifts_dir = f"{self.person_dir}/gifts"
        if self._gut_file_name is None:
            self._gut_file_name = f"{get_gut_file_name()}.json"
        if self._gut_path is None:
            self._gut_path = f"{self.person_dir}/{self._gut_file_name}"
        if self._live_file_name is None:
            self._live_file_name = f"{get_live_file_name()}.json"
        if self._live_path is None:
            self._live_path = f"{self.person_dir}/{self._live_file_name}"

    def create_core_dir_and_files(self):
        set_dir(self.world_dir)
        set_dir(self.persons_dir)
        set_dir(self.person_dir)
        set_dir(self._econs_dir)
        set_dir(self._atoms_dir)
        set_dir(self._gifts_dir)
        self.create_gut_file_if_does_not_exist()
        self.create_live_file_if_does_not_exist()

    def create_gut_file_if_does_not_exist(self):
        if self.gut_file_exists() == False:
            default_gut_agenda = agendaunit_shop(
                self.person_id, self.world_id, self._road_delimiter, self._planck
            )
            self.save_gut_file(default_gut_agenda)

    def create_live_file_if_does_not_exist(self):
        if self.live_file_exists() == False:
            default_live_agenda = agendaunit_shop(
                self.person_id, self.world_id, self._road_delimiter, self._planck
            )
            self._save_live_file(default_live_agenda)

    def gut_file_exists(self) -> bool:
        return os_path_exists(self._gut_path)

    def live_file_exists(self) -> bool:
        return os_path_exists(self._live_path)

    def save_gut_file(self, x_agenda: AgendaUnit, replace: bool = True):
        if x_agenda._owner_id != self.person_id:
            raise Invalid_gut_Exception(
                f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{self.person_id}''s gut agenda."
            )
        if replace in {True, False}:
            save_file(
                dest_dir=self.person_dir,
                file_name=self._gut_file_name,
                file_text=x_agenda.get_json(),
                replace=replace,
            )

    def _save_live_file(self, x_agenda: AgendaUnit, replace: bool = True):
        if x_agenda._owner_id != self.person_id:
            raise Invalid_live_Exception(
                f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{self.person_id}''s live agenda."
            )
        if replace in {True, False}:
            save_file(
                dest_dir=self.person_dir,
                file_name=self._live_file_name,
                file_text=x_agenda.get_json(),
                replace=replace,
            )

    def get_gut_file_agenda(self) -> AgendaUnit:
        gut_json = open_file(dest_dir=self.person_dir, file_name=self._gut_file_name)
        return agenda_get_from_json(gut_json)

    def get_live_file_agenda(self) -> AgendaUnit:
        live_json = open_file(dest_dir=self.person_dir, file_name=self._live_file_name)
        return agenda_get_from_json(live_json)

    def load_gut_file(self):
        self._gut_obj = self.get_gut_file_agenda()

    def load_live_file(self):
        self._live_obj = self.get_live_file_agenda()

    def giftunit_file_exists(self, gift_id: int) -> bool:
        gift_filename = giftunit_get_json_filename(gift_id)
        return os_path_exists(f"{self._gifts_dir}/{gift_filename}")

    def get_max_gift_file_number(self) -> int:
        if not os_path_exists(self._gifts_dir):
            return None
        gift_filenames = dir_files(
            dir_path=self._gifts_dir, delete_extensions=True, include_files=True
        ).keys()
        gift_file_numbers = {int(gift_filename) for gift_filename in gift_filenames}
        return max(gift_file_numbers, default=None)

    def get_next_gift_file_number(self) -> int:
        max_file_number = self.get_max_gift_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def save_giftunit_file(
        self, x_gift: GiftUnit, replace: bool = True, change_invalid_attrs: bool = True
    ) -> GiftUnit:
        if change_invalid_attrs:
            x_gift = self.get_valid_giftunit(x_gift)

        if x_gift._atoms_dir != self._atoms_dir:
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {x_gift._atoms_dir}. It must be {self._atoms_dir}."
            )
        if x_gift._gifts_dir != self._gifts_dir:
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {x_gift._gifts_dir}. It must be {self._gifts_dir}."
            )
        if x_gift._giver != self.person_id:
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit._giver is incorrect: {x_gift._giver}. It must be {self.person_id}."
            )
        gift_filename = giftunit_get_json_filename(x_gift._gift_id)
        if not replace and self.giftunit_file_exists(x_gift._gift_id):
            raise SaveGiftFileException(
                f"GiftUnit file {gift_filename} already exists and cannot be saved over."
            )
        x_gift.save_files()
        return x_gift

    def get_new_giftunit(self) -> GiftUnit:
        return giftunit_shop(
            _giver=self.person_id,
            _gift_id=self.get_next_gift_file_number(),
            _atoms_dir=self._atoms_dir,
            _gifts_dir=self._gifts_dir,
        )

    def get_valid_giftunit(self, x_giftunit: GiftUnit) -> GiftUnit:
        if x_giftunit._atoms_dir != self._atoms_dir:
            x_giftunit._atoms_dir = self._atoms_dir
        if x_giftunit._gifts_dir != self._gifts_dir:
            x_giftunit._gifts_dir = self._gifts_dir
        if x_giftunit._gift_id != self.get_next_gift_file_number():
            x_giftunit._gift_id = self.get_next_gift_file_number()
        if x_giftunit._giver != self.person_id:
            x_giftunit._giver = self.person_id
        if x_giftunit._book_start != self._get_next_atom_file_number():
            x_giftunit._book_start = self._get_next_atom_file_number()
        return x_giftunit

    def get_giftunit(self, file_number: int) -> GiftUnit:
        if self.giftunit_file_exists(file_number) == False:
            raise GiftFileMissingException(
                f"GiftUnit file_number {file_number} does not exist."
            )
        return create_giftunit_from_files(
            gifts_dir=self._gifts_dir, gift_id=file_number, atoms_dir=self._atoms_dir
        )

    def del_giftunit_file(self, file_number: int):
        delete_dir(f"{self._gifts_dir}/{giftunit_get_json_filename(file_number)}")

    def _get_agenda_from_gift_files(self, x_agenda: AgendaUnit) -> AgendaUnit:
        # get list of all gift files
        gift_ints = dir_files(self._gifts_dir, delete_extensions=True).keys()
        for gift_int in gift_ints:
            x_gift = self.get_giftunit(gift_int)
            x_agenda = x_gift._bookunit.get_edited_agenda(x_agenda)
        return x_agenda

    def _save_valid_atom_file(self, x_atom: AgendaAtom, file_number: int):
        save_file(self._atoms_dir, f"{file_number}.json", x_atom.get_json())
        return file_number

    def atom_file_exists(self, filename: int) -> bool:
        return os_path_exists(f"{self._atoms_dir}/{filename}.json")

    def _delete_atom_file(self, filename: int):
        delete_dir(f"{self._atoms_dir}/{filename}.json")

    def _get_max_atom_file_number(self) -> int:
        if not os_path_exists(self._atoms_dir):
            return None
        atom_filenames = dir_files(
            dir_path=self._atoms_dir, delete_extensions=True, include_files=True
        ).keys()
        atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
        return max(atom_file_numbers, default=None)

    def _get_next_atom_file_number(self) -> str:
        max_file_number = self._get_max_atom_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def save_atom_file(self, x_atom: AgendaAtom):
        x_filename = self._get_next_atom_file_number()
        return self._save_valid_atom_file(x_atom, x_filename)

    def _get_agenda_from_atom_files(self) -> AgendaUnit:
        x_agenda = agendaunit_shop(_owner_id=self.person_id, _world_id=self.world_id)
        x_atom_files = dir_files(self._atoms_dir, delete_extensions=True)
        sorted_atom_filenames = sorted(list(x_atom_files.keys()))

        for x_atom_filename in sorted_atom_filenames:
            x_file_text = x_atom_files.get(x_atom_filename)
            x_atom = agendaatom_get_from_json(x_file_text)
            change_agenda_with_agendaatom(x_agenda, x_atom)
        return x_agenda

    def get_rootpart_of_econ_dir(self):
        return "idearoot"

    def _get_person_econ_dir(self, x_list: list[RoadNode]) -> str:
        return f"{self._econs_dir}{get_directory_path(x_list=[*x_list])}"

    def _create_econ_dir(self, x_roadunit: RoadUnit) -> str:
        x_roadunit = change_road(
            x_roadunit, self.world_id, self.get_rootpart_of_econ_dir()
        )
        road_nodes = get_all_road_nodes(x_roadunit, delimiter=self._road_delimiter)
        x_econ_path = self._get_person_econ_dir(road_nodes)
        set_dir(x_econ_path)
        return x_econ_path

    def _create_econunit(self, econ_roadunit: RoadUnit):
        x_econ_path = self._create_econ_dir(econ_roadunit)
        x_econunit = econunit_shop(
            world_id=self.world_id,
            econ_dir=x_econ_path,
            _manager_person_id=self.person_id,
            _road_delimiter=self._road_delimiter,
        )
        x_econunit.set_econ_dirs()
        self._econ_objs[econ_roadunit] = x_econunit

    def create_person_econunits(self, econ_exceptions: bool = True):
        x_gut_agenda = self.get_gut_file_agenda()
        x_gut_agenda.set_agenda_metrics(econ_exceptions)
        if x_gut_agenda._econs_justified == False:
            raise PersonCreateEconUnitsException(
                f"Cannot set '{self.person_id}' gut agenda econunits because 'AgendaUnit._econs_justified' is False."
            )
        if x_gut_agenda._econs_buildable == False:
            raise PersonCreateEconUnitsException(
                f"Cannot set '{self.person_id}' gut agenda econunits because 'AgendaUnit._econs_buildable' is False."
            )

        x_person_econs = x_gut_agenda._healers_dict.get(self.person_id)
        x_person_econs = get_empty_dict_if_none(x_person_econs)
        self._econ_objs = {}
        for econ_idea in x_person_econs.values():
            self._create_econunit(econ_roadunit=econ_idea.get_road())

        # delete any
        curr_treasury_dirs = get_all_dirs_with_file(
            treasury_db_filename(), self._econs_dir
        )
        for treasury_dir in curr_treasury_dirs:
            treasury_road = create_road_from_nodes(get_parts_dir(treasury_dir))
            treasury_road = change_road(
                treasury_road, self.get_rootpart_of_econ_dir(), self.world_id
            )
            if x_person_econs.get(treasury_road) is None:
                dir_to_delete = f"{self._econs_dir}/{treasury_dir}"
                delete_dir(dir_to_delete)

    def get_econ(self, econ_road: RoadUnit) -> EconUnit:
        return self._econ_objs.get(econ_road)

    def set_econunit_role(self, econ_road: RoadUnit, role: AgendaUnit):
        x_econ = self.get_econ(econ_road)
        x_econ.save_file_to_roles(role)

    def set_econunits_role(self, role: AgendaUnit):
        for x_econ_road in self._econ_objs.keys():
            self.set_econunit_role(x_econ_road, role)

    def set_person_econunits_role(self):
        self.set_econunits_role(self.get_gut_file_agenda())

    def add_promise(self, promise_road: RoadUnit, x_suffgroup: GroupID = None):
        gut_agenda = self.get_gut_file_agenda()
        create_promise(gut_agenda, promise_road, x_suffgroup)
        self.save_gut_file(gut_agenda)


def personunit_shop(
    person_id: PersonID,
    world_id: str = None,
    worlds_dir: str = None,
    _econ_objs: dict[RoadUnit:EconUnit] = None,
    _road_delimiter: str = None,
    _planck: float = None,
) -> PersonUnit:
    x_personunit = PersonUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        _econ_objs=get_empty_dict_if_none(_econ_objs),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _planck=default_planck_if_none(_planck),
    )
    x_personunit.set_person_id(person_id)
    x_personunit.create_core_dir_and_files()
    return x_personunit


def get_from_json(x_person_json: str) -> PersonUnit:
    return None


def get_from_dict(person_dict: dict) -> PersonUnit:
    return None
