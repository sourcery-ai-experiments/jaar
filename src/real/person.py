from src._road.finance import default_planck_if_none
from src._road.road import (
    default_road_delimiter_if_none,
    PersonID,
    RealID,
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
    get_from_json as agendaunit_get_from_json,
)
from src.agenda.pledge import create_pledge
from src.econ.econ import (
    EconUnit,
    econunit_shop,
    treasury_db_filename,
    get_rootpart_of_econ_dir,
)
from src.world.gift import (
    GiftUnit,
    giftunit_shop,
    get_json_filename as giftunit_get_json_filename,
    create_giftunit_from_files,
    init_gift_id,
    get_init_gift_id_if_None,
    get_gifts_folder,
)
from src.real.examples.real_env_kit import get_test_reals_dir, get_test_real_id
from src._instrument.python import get_empty_dict_if_none
from src._instrument.file import (
    save_file,
    open_file,
    set_dir,
    get_directory_path,
    get_all_dirs_with_file,
    get_parts_dir,
    delete_dir,
    dir_files,
    get_integer_filenames,
)
from dataclasses import dataclass
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy


class InvalidEconException(Exception):
    pass


class PersonCreateEconUnitsException(Exception):
    pass


class Invalid_duty_Exception(Exception):
    pass


class Invalid_work_Exception(Exception):
    pass


class SaveGiftFileException(Exception):
    pass


class GiftFileMissingException(Exception):
    pass


def get_duty_file_name() -> str:
    return "duty"


def get_work_file_name() -> str:
    return "work"


@dataclass
class ChapUnit:
    person_id: PersonID = None
    real_dir: str = None
    reals_dir: str = None
    real_id: str = None
    persons_dir: str = None
    person_dir: str = None
    _econs_dir: str = None
    _atoms_dir: str = None
    _gifts_dir: str = None
    _duty_obj: AgendaUnit = None
    _duty_file_name: str = None
    _duty_path: str = None
    _work_obj: AgendaUnit = None
    _work_file_name: str = None
    _work_path: str = None
    _econ_objs: dict[RoadUnit:EconUnit] = None
    _road_delimiter: str = None
    _planck: float = None


def chapunit_shop(
    x_reals_dir: str,
    x_real_id: RealID,
    x_person_id: PersonID,
    x_road_delimiter: str = None,
    x_planck: float = None,
) -> ChapUnit:
    x_planck = default_planck_if_none(x_planck)
    if x_reals_dir is None:
        x_reals_dir = get_test_reals_dir()
    if x_real_id is None:
        x_real_id = get_test_real_id()
    x_road_delimiter = default_road_delimiter_if_none(x_road_delimiter)
    x_real_dir = f"{x_reals_dir}/{x_real_id}"
    x_persons_dir = f"{x_real_dir}/persons"
    x_person_id = validate_roadnode(x_person_id, x_road_delimiter)
    x_person_dir = f"{x_persons_dir}/{x_person_id}"
    x_econs_dir = f"{x_person_dir}/econs"
    x_atoms_dir = f"{x_person_dir}/atoms"
    x_gifts_dir = f"{x_person_dir}/{get_gifts_folder()}"
    x_duty_file_name = f"{get_duty_file_name()}.json"
    x_duty_path = f"{x_person_dir}/{x_duty_file_name}"
    x_work_file_name = f"{get_work_file_name()}.json"
    x_work_path = f"{x_person_dir}/{x_work_file_name}"

    return ChapUnit(
        person_id=x_person_id,
        real_id=x_real_id,
        real_dir=x_real_dir,
        reals_dir=x_reals_dir,
        persons_dir=x_persons_dir,
        person_dir=x_person_dir,
        _econs_dir=x_econs_dir,
        _atoms_dir=x_atoms_dir,
        _gifts_dir=x_gifts_dir,
        _duty_file_name=x_duty_file_name,
        _duty_path=x_duty_path,
        _work_file_name=x_work_file_name,
        _work_path=x_work_path,
        _road_delimiter=x_road_delimiter,
        _planck=x_planck,
    )


def duty_file_exists(chapunit: ChapUnit) -> bool:
    return os_path_exists(chapunit._duty_path)


def work_file_exists(chapunit: ChapUnit) -> bool:
    return os_path_exists(chapunit._work_path)


def giftunit_file_exists(x_chapunit: ChapUnit, gift_id: int) -> bool:
    gift_filename = giftunit_get_json_filename(gift_id)
    return os_path_exists(f"{x_chapunit._gifts_dir}/{gift_filename}")


def initialize_work_file(x_chapunit):
    if work_file_exists(x_chapunit) == False:
        default_work_agenda = agendaunit_shop(
            x_chapunit.person_id,
            x_chapunit.real_id,
            x_chapunit._road_delimiter,
            x_chapunit._planck,
        )
        _save_work_file(x_chapunit, default_work_agenda)


def _save_work_file(x_chapunit: ChapUnit, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_chapunit.person_id:
        raise Invalid_work_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_chapunit.person_id}''s work agenda."
        )
    if replace in {True, False}:
        save_file(
            dest_dir=x_chapunit.person_dir,
            file_name=x_chapunit._work_file_name,
            file_text=x_agenda.get_json(),
            replace=replace,
        )


def _get_empty_agenda(x_chapunit: ChapUnit) -> AgendaUnit:
    empty_agenda = agendaunit_shop(x_chapunit.person_id, x_chapunit.real_id)
    empty_agenda._last_gift_id = init_gift_id()
    return empty_agenda


def save_duty_file(x_chapunit: ChapUnit, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_chapunit.person_id:
        raise Invalid_duty_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_chapunit.person_id}''s duty agenda."
        )
    if replace in {True, False}:
        save_file(
            dest_dir=x_chapunit.person_dir,
            file_name=x_chapunit._duty_file_name,
            file_text=x_agenda.get_json(),
            replace=replace,
        )


def get_duty_file_agenda(x_chapunit: ChapUnit) -> AgendaUnit:
    duty_json = open_file(
        dest_dir=x_chapunit.person_dir, file_name=x_chapunit._duty_file_name
    )
    return agendaunit_get_from_json(duty_json)


def giftunit_file_exists(x_chapunit: ChapUnit, gift_id: int) -> bool:
    gift_filename = giftunit_get_json_filename(gift_id)
    return os_path_exists(f"{x_chapunit._gifts_dir}/{gift_filename}")


def get_max_gift_file_number(x_chapunit: ChapUnit) -> int:
    if not os_path_exists(x_chapunit._gifts_dir):
        return None
    gift_filenames = dir_files(x_chapunit._gifts_dir, True, include_files=True).keys()
    gift_file_numbers = {int(gift_filename) for gift_filename in gift_filenames}
    return max(gift_file_numbers, default=None)


def _get_next_gift_file_number(x_chapunit: ChapUnit) -> int:
    max_file_number = get_max_gift_file_number(x_chapunit)
    init_gift_id = get_init_gift_id_if_None()
    return init_gift_id if max_file_number is None else max_file_number + 1


def _create_initial_gift_from_duty(x_chapunit: ChapUnit):
    x_giftunit = giftunit_shop(
        _giver=x_chapunit.person_id,
        _gift_id=get_init_gift_id_if_None(),
        _gifts_dir=x_chapunit._gifts_dir,
        _atoms_dir=x_chapunit._atoms_dir,
    )
    x_giftunit._bookunit.add_all_different_agendaatoms(
        before_agenda=_get_empty_agenda(x_chapunit),
        after_agenda=get_duty_file_agenda(x_chapunit),
    )
    x_giftunit.save_files()


def get_giftunit(x_chapunit: ChapUnit, file_number: int) -> GiftUnit:
    if giftunit_file_exists(x_chapunit, file_number) == False:
        raise GiftFileMissingException(
            f"GiftUnit file_number {file_number} does not exist."
        )
    x_gifts_dir = x_chapunit._gifts_dir
    x_atoms_dir = x_chapunit._atoms_dir
    return create_giftunit_from_files(x_gifts_dir, file_number, x_atoms_dir)


def _merge_gifts_into_agenda(x_chapunit: ChapUnit, x_agenda: AgendaUnit) -> AgendaUnit:
    gift_ints = get_integer_filenames(x_chapunit._gifts_dir, x_agenda._last_gift_id)
    for gift_int in gift_ints:
        x_gift = get_giftunit(x_chapunit, gift_int)
        new_agenda = x_gift._bookunit.get_edited_agenda(x_agenda)

        update_text = "UPDATE"
        x_gift._bookunit.agendaatoms.get(update_text)
    return new_agenda


def _create_duty_from_gifts(x_chapunit):
    save_duty_file(
        x_chapunit,
        _merge_gifts_into_agenda(x_chapunit, _get_empty_agenda(x_chapunit)),
    )


def _create_initial_gift_and_duty_files(x_chapunit: ChapUnit):
    default_duty_agenda = agendaunit_shop(
        x_chapunit.person_id,
        x_chapunit.real_id,
        x_chapunit._road_delimiter,
        x_chapunit._planck,
    )
    x_giftunit = giftunit_shop(
        _giver=x_chapunit.person_id,
        _gift_id=get_init_gift_id_if_None(),
        _gifts_dir=x_chapunit._gifts_dir,
        _atoms_dir=x_chapunit._atoms_dir,
    )
    x_giftunit._bookunit.add_all_different_agendaatoms(
        before_agenda=_get_empty_agenda(x_chapunit),
        after_agenda=default_duty_agenda,
    )
    x_giftunit.save_files()
    _create_duty_from_gifts(x_chapunit)


def initialize_gift_and_duty_files(x_chapunit):
    x_duty_file_exists = duty_file_exists(x_chapunit)
    gift_file_exists = giftunit_file_exists(x_chapunit, init_gift_id())
    if x_duty_file_exists == False and gift_file_exists == False:
        _create_initial_gift_and_duty_files(x_chapunit)
    elif x_duty_file_exists == False and gift_file_exists:
        _create_duty_from_gifts(x_chapunit)
    elif x_duty_file_exists and gift_file_exists == False:
        _create_initial_gift_from_duty(x_chapunit)


def chap_create_core_dir_and_files(x_chapunit: ChapUnit):
    set_dir(x_chapunit.real_dir)
    set_dir(x_chapunit.persons_dir)
    set_dir(x_chapunit.person_dir)
    set_dir(x_chapunit._econs_dir)
    set_dir(x_chapunit._atoms_dir)
    set_dir(x_chapunit._gifts_dir)
    initialize_gift_and_duty_files(x_chapunit)
    initialize_work_file(x_chapunit)


def get_work_file_agenda(x_chapunit: ChapUnit) -> AgendaUnit:
    work_json = open_file(
        dest_dir=x_chapunit.person_dir, file_name=x_chapunit._work_file_name
    )
    return agendaunit_get_from_json(work_json)


def append_gifts_to_duty_file(x_chapunit: ChapUnit) -> AgendaUnit:
    duty_agenda = get_duty_file_agenda(x_chapunit)
    duty_agenda = _merge_gifts_into_agenda(x_chapunit, duty_agenda)
    save_duty_file(x_chapunit, duty_agenda)
    return get_duty_file_agenda(x_chapunit)


def _get_next_atom_file_number(x_chapunit: ChapUnit) -> str:
    max_file_number = _get_max_atom_file_number(x_chapunit)
    return 0 if max_file_number is None else max_file_number + 1


def _get_max_atom_file_number(x_chapunit: ChapUnit) -> int:
    if not os_path_exists(x_chapunit._atoms_dir):
        return None
    atom_files_dict = dir_files(x_chapunit._atoms_dir, True, include_files=True)
    atom_filenames = atom_files_dict.keys()
    atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
    return max(atom_file_numbers, default=None)


def validate_giftunit(x_chapunit: ChapUnit, x_giftunit: GiftUnit) -> GiftUnit:
    if x_giftunit._atoms_dir != x_chapunit._atoms_dir:
        x_giftunit._atoms_dir = x_chapunit._atoms_dir
    if x_giftunit._gifts_dir != x_chapunit._gifts_dir:
        x_giftunit._gifts_dir = x_chapunit._gifts_dir
    if x_giftunit._gift_id != _get_next_gift_file_number(x_chapunit):
        x_giftunit._gift_id = _get_next_gift_file_number(x_chapunit)
    if x_giftunit._giver != x_chapunit.person_id:
        x_giftunit._giver = x_chapunit.person_id
    if x_giftunit._book_start != _get_next_atom_file_number(x_chapunit):
        x_giftunit._book_start = _get_next_atom_file_number(x_chapunit)
    return x_giftunit


def save_giftunit_file(
    x_chapunit: ChapUnit,
    x_gift: GiftUnit,
    replace: bool = True,
    change_invalid_attrs: bool = True,
) -> GiftUnit:
    if change_invalid_attrs:
        x_gift = validate_giftunit(x_chapunit, x_gift)

    if x_gift._atoms_dir != x_chapunit._atoms_dir:
        raise SaveGiftFileException(
            f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {x_gift._atoms_dir}. It must be {x_chapunit._atoms_dir}."
        )
    if x_gift._gifts_dir != x_chapunit._gifts_dir:
        raise SaveGiftFileException(
            f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {x_gift._gifts_dir}. It must be {x_chapunit._gifts_dir}."
        )
    if x_gift._giver != x_chapunit.person_id:
        raise SaveGiftFileException(
            f"GiftUnit file cannot be saved because giftunit._giver is incorrect: {x_gift._giver}. It must be {x_chapunit.person_id}."
        )
    gift_filename = giftunit_get_json_filename(x_gift._gift_id)
    if not replace and giftunit_file_exists(x_chapunit, x_gift._gift_id):
        raise SaveGiftFileException(
            f"GiftUnit file {gift_filename} already exists and cannot be saved over."
        )
    x_gift.save_files()
    return x_gift


def _create_new_giftunit(x_chapunit: ChapUnit) -> GiftUnit:
    return giftunit_shop(
        _giver=x_chapunit.person_id,
        _gift_id=_get_next_gift_file_number(x_chapunit),
        _atoms_dir=x_chapunit._atoms_dir,
        _gifts_dir=x_chapunit._gifts_dir,
    )


def create_save_giftunit(
    x_chapunit: ChapUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    new_giftunit = _create_new_giftunit(x_chapunit)
    new_giftunit._bookunit.add_all_different_agendaatoms(before_agenda, after_agenda)
    save_giftunit_file(x_chapunit, new_giftunit)


def add_pledge_gift(x_chapunit, pledge_road: RoadUnit, x_suffgroup: GroupID = None):
    duty_agenda = get_duty_file_agenda(x_chapunit)
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_giftunit = _create_new_giftunit(x_chapunit)
    next_giftunit._bookunit.add_all_different_agendaatoms(old_duty_agenda, duty_agenda)
    next_giftunit.save_files()
    append_gifts_to_duty_file(x_chapunit)


def del_giftunit_file(x_chapunit: ChapUnit, file_number: int):
    delete_dir(f"{x_chapunit._gifts_dir}/{giftunit_get_json_filename(file_number)}")


@dataclass
class PersonUnit:
    person_id: PersonID = None
    reals_dir: str = None
    real_id: str = None
    persons_dir: str = None
    person_dir: str = None
    _econs_dir: str = None
    _duty_obj: AgendaUnit = None
    _duty_file_name: str = None
    _duty_path: str = None
    _work_obj: AgendaUnit = None
    _econ_objs: dict[RoadUnit:EconUnit] = None
    _road_delimiter: str = None
    _planck: float = None

    def set_person_id(self, chapunit: ChapUnit):
        self.person_id = chapunit.person_id
        self.reals_dir = chapunit.reals_dir
        self.real_id = chapunit.real_id
        self._econs_dir = chapunit._econs_dir
        self._work_file_name = chapunit._work_file_name
        self._work_path = chapunit._work_path

    def _get_person_econ_dir(self, x_chapunit: ChapUnit, x_list: list[RoadNode]) -> str:
        return f"{x_chapunit._econs_dir}{get_directory_path(x_list=[*x_list])}"

    def _create_econ_dir(self, x_chapunit: ChapUnit, x_roadunit: RoadUnit) -> str:
        econ_root = get_rootpart_of_econ_dir()
        x_roadunit = change_road(x_roadunit, x_chapunit.real_id, econ_root)
        road_nodes = get_all_road_nodes(x_roadunit, x_chapunit._road_delimiter)
        x_econ_path = self._get_person_econ_dir(x_chapunit, road_nodes)
        set_dir(x_econ_path)
        return x_econ_path

    def _create_econunit(self, x_chapunit: ChapUnit, econ_roadunit: RoadUnit):
        x_econ_path = self._create_econ_dir(x_chapunit, econ_roadunit)
        x_econunit = econunit_shop(
            real_id=self.real_id,
            econ_dir=x_econ_path,
            _manager_person_id=self.person_id,
            _road_delimiter=self._road_delimiter,
        )
        x_econunit.set_econ_dirs()
        self._econ_objs[econ_roadunit] = x_econunit

    def create_person_econunits(
        self, x_chapunit: ChapUnit, econ_exceptions: bool = True
    ):
        x_duty_agenda = get_duty_file_agenda(x_chapunit)
        x_duty_agenda.calc_intent(econ_exceptions)
        if x_duty_agenda._econs_justified == False:
            raise PersonCreateEconUnitsException(
                f"Cannot set '{self.person_id}' duty agenda econunits because 'AgendaUnit._econs_justified' is False."
            )
        if x_duty_agenda._econs_buildable == False:
            raise PersonCreateEconUnitsException(
                f"Cannot set '{self.person_id}' duty agenda econunits because 'AgendaUnit._econs_buildable' is False."
            )

        x_person_econs = x_duty_agenda._healers_dict.get(self.person_id)
        x_person_econs = get_empty_dict_if_none(x_person_econs)
        self._econ_objs = {}
        for econ_idea in x_person_econs.values():
            self._create_econunit(x_chapunit, econ_roadunit=econ_idea.get_road())

        # delete any
        x_treasury_dirs = get_all_dirs_with_file(
            treasury_db_filename(), self._econs_dir
        )
        for treasury_dir in x_treasury_dirs:
            treasury_road = create_road_from_nodes(get_parts_dir(treasury_dir))
            treasury_road = change_road(
                treasury_road, get_rootpart_of_econ_dir(), self.real_id
            )
            if x_person_econs.get(treasury_road) is None:
                dir_to_delete = f"{self._econs_dir}/{treasury_dir}"
                delete_dir(dir_to_delete)

    def get_econ(self, econ_road: RoadUnit) -> EconUnit:
        return self._econ_objs.get(econ_road)

    def set_econunit_role(self, econ_road: RoadUnit, role: AgendaUnit):
        x_econ = self.get_econ(econ_road)
        x_econ.save_role_file(role)

    def set_econunits_role(self, role: AgendaUnit):
        for x_econ_road in self._econ_objs.keys():
            self.set_econunit_role(x_econ_road, role)

    def set_person_econunits_role(self):
        self.set_econunits_role(self._duty_obj)


def personunit_shop(
    person_id: PersonID,
    real_id: str = None,
    reals_dir: str = None,
    _econ_objs: dict[RoadUnit:EconUnit] = None,
    _road_delimiter: str = None,
    _planck: float = None,
    create_files: bool = True,
) -> PersonUnit:
    x_personunit = PersonUnit(
        real_id=real_id,
        reals_dir=reals_dir,
        _econ_objs=get_empty_dict_if_none(_econ_objs),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _planck=default_planck_if_none(_planck),
    )
    x_chapunit = chapunit_shop(reals_dir, real_id, person_id, _road_delimiter, _planck)
    x_personunit.set_person_id(x_chapunit)
    if create_files:
        chap_create_core_dir_and_files(x_chapunit)
        x_personunit._duty_obj = get_duty_file_agenda(x_chapunit)
    return x_personunit
