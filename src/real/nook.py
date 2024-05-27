from src._instrument.file import (
    save_file,
    open_file,
    set_dir,
    delete_dir,
    dir_files,
    get_integer_filenames,
)
from src._road.finance import default_planck_if_none
from src._road.road import (
    default_road_delimiter_if_none,
    PersonID,
    RealID,
    validate_roadnode,
    RoadUnit,
)
from src.agenda.group import GroupID
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
    duty_str,
    work_str,
)
from src.agenda.atom import (
    AgendaAtom,
    get_from_json as agendaatom_get_from_json,
    modify_agenda_with_agendaatom,
)
from src.agenda.pledge import create_pledge
from src.econ.econ import EconUnit
from src.real.change import (
    changeUnit,
    changeunit_shop,
    get_json_filename as changeunit_get_json_filename,
    create_changeunit_from_files,
    init_change_id,
    get_init_change_id_if_None,
    get_changes_folder,
)
from src.real.examples.real_env_kit import get_test_reals_dir, get_test_real_id
from dataclasses import dataclass
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy


class Invalid_duty_Exception(Exception):
    pass


class Invalid_work_Exception(Exception):
    pass


class SavechangeFileException(Exception):
    pass


class changeFileMissingException(Exception):
    pass


@dataclass
class NookUnit:
    person_id: PersonID = None
    real_dir: str = None
    reals_dir: str = None
    real_id: str = None
    persons_dir: str = None
    person_dir: str = None
    _econs_dir: str = None
    _atoms_dir: str = None
    _changes_dir: str = None
    _duty_file_name: str = None
    _duty_path: str = None
    _work_file_name: str = None
    _work_path: str = None
    _road_delimiter: str = None
    _planck: float = None


def nookunit_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID,
    road_delimiter: str = None,
    planck: float = None,
) -> NookUnit:
    planck = default_planck_if_none(planck)
    if reals_dir is None:
        reals_dir = get_test_reals_dir()
    if real_id is None:
        real_id = get_test_real_id()
    road_delimiter = default_road_delimiter_if_none(road_delimiter)
    real_dir = f"{reals_dir}/{real_id}"
    persons_dir = f"{real_dir}/persons"
    person_id = validate_roadnode(person_id, road_delimiter)
    person_dir = f"{persons_dir}/{person_id}"
    econs_dir = f"{person_dir}/econs"
    atoms_dir = f"{person_dir}/atoms"
    changes_dir = f"{person_dir}/{get_changes_folder()}"
    duty_file_name = f"{duty_str()}.json"
    duty_path = f"{person_dir}/{duty_file_name}"
    work_file_name = f"{work_str()}.json"
    work_path = f"{person_dir}/{work_file_name}"

    return NookUnit(
        person_id=person_id,
        real_id=real_id,
        real_dir=real_dir,
        reals_dir=reals_dir,
        persons_dir=persons_dir,
        person_dir=person_dir,
        _econs_dir=econs_dir,
        _atoms_dir=atoms_dir,
        _changes_dir=changes_dir,
        _duty_file_name=duty_file_name,
        _duty_path=duty_path,
        _work_file_name=work_file_name,
        _work_path=work_path,
        _road_delimiter=road_delimiter,
        _planck=planck,
    )


def duty_file_exists(nookunit: NookUnit) -> bool:
    return os_path_exists(nookunit._duty_path)


def work_file_exists(nookunit: NookUnit) -> bool:
    return os_path_exists(nookunit._work_path)


def nookunit_save_atom_file(x_nookunit: NookUnit, x_atom: AgendaAtom):
    x_filename = _get_next_atom_file_number(x_nookunit)
    return _save_valid_atom_file(x_nookunit, x_atom, x_filename)


def _save_valid_atom_file(x_nookunit: NookUnit, x_atom: AgendaAtom, file_number: int):
    save_file(x_nookunit._atoms_dir, f"{file_number}.json", x_atom.get_json())
    return file_number


def nookunit_atom_file_exists(x_nookunit, filename: int) -> bool:
    return os_path_exists(f"{x_nookunit._atoms_dir}/{filename}.json")


def _delete_atom_file(x_nookunit: NookUnit, filename: int):
    delete_dir(f"{x_nookunit._atoms_dir}/{filename}.json")


def _get_agenda_from_atom_files(x_nookunit: NookUnit) -> AgendaUnit:
    x_agenda = agendaunit_shop(x_nookunit.person_id, x_nookunit.real_id)
    x_atom_files = dir_files(x_nookunit._atoms_dir, delete_extensions=True)
    sorted_atom_filenames = sorted(list(x_atom_files.keys()))

    for x_atom_filename in sorted_atom_filenames:
        x_file_text = x_atom_files.get(x_atom_filename)
        x_atom = agendaatom_get_from_json(x_file_text)
        modify_agenda_with_agendaatom(x_agenda, x_atom)
    return x_agenda


def _get_max_atom_file_number(x_nookunit: NookUnit) -> int:
    if not os_path_exists(x_nookunit._atoms_dir):
        return None
    atom_files_dict = dir_files(x_nookunit._atoms_dir, True, include_files=True)
    atom_filenames = atom_files_dict.keys()
    atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
    return max(atom_file_numbers, default=None)


def _get_next_atom_file_number(x_nookunit: NookUnit) -> str:
    max_file_number = _get_max_atom_file_number(x_nookunit)
    return 0 if max_file_number is None else max_file_number + 1


def changeunit_file_exists(x_nookunit: NookUnit, change_id: int) -> bool:
    change_filename = changeunit_get_json_filename(change_id)
    return os_path_exists(f"{x_nookunit._changes_dir}/{change_filename}")


def initialize_work_file(x_nookunit):
    if work_file_exists(x_nookunit) == False:
        default_work_agenda = agendaunit_shop(
            x_nookunit.person_id,
            x_nookunit.real_id,
            x_nookunit._road_delimiter,
            x_nookunit._planck,
        )
        _save_work_file(x_nookunit, default_work_agenda)


def _save_work_file(x_nookunit: NookUnit, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_nookunit.person_id:
        raise Invalid_work_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_nookunit.person_id}''s work agenda."
        )
    if replace in {True, False}:
        save_file(
            dest_dir=x_nookunit.person_dir,
            file_name=x_nookunit._work_file_name,
            file_text=x_agenda.get_json(),
            replace=replace,
        )


def save_duty_file(x_nookunit: NookUnit, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_nookunit.person_id:
        raise Invalid_duty_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_nookunit.person_id}''s duty agenda."
        )
    if replace in {True, False}:
        save_file(
            dest_dir=x_nookunit.person_dir,
            file_name=x_nookunit._duty_file_name,
            file_text=x_agenda.get_json(),
            replace=replace,
        )


def get_duty_file_agenda(x_nookunit: NookUnit) -> AgendaUnit:
    if duty_file_exists(x_nookunit) == False:
        save_duty_file(x_nookunit, get_default_duty_agenda(x_nookunit))
    duty_json = open_file(x_nookunit.person_dir, x_nookunit._duty_file_name)
    return agendaunit_get_from_json(duty_json)


def changeunit_file_exists(x_nookunit: NookUnit, change_id: int) -> bool:
    change_filename = changeunit_get_json_filename(change_id)
    return os_path_exists(f"{x_nookunit._changes_dir}/{change_filename}")


def get_max_change_file_number(x_nookunit: NookUnit) -> int:
    if not os_path_exists(x_nookunit._changes_dir):
        return None
    change_filenames = dir_files(
        x_nookunit._changes_dir, True, include_files=True
    ).keys()
    change_file_numbers = {int(change_filename) for change_filename in change_filenames}
    return max(change_file_numbers, default=None)


def _get_next_change_file_number(x_nookunit: NookUnit) -> int:
    max_file_number = get_max_change_file_number(x_nookunit)
    init_change_id = get_init_change_id_if_None()
    return init_change_id if max_file_number is None else max_file_number + 1


def _create_initial_change_from_duty(x_nookunit: NookUnit):
    x_changeunit = changeunit_shop(
        _giver=x_nookunit.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_nookunit._changes_dir,
        _atoms_dir=x_nookunit._atoms_dir,
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_nookunit),
        after_agenda=get_duty_file_agenda(x_nookunit),
    )
    x_changeunit.save_files()


def get_changeunit(x_nookunit: NookUnit, file_number: int) -> changeUnit:
    if changeunit_file_exists(x_nookunit, file_number) == False:
        raise changeFileMissingException(
            f"changeUnit file_number {file_number} does not exist."
        )
    x_changes_dir = x_nookunit._changes_dir
    x_atoms_dir = x_nookunit._atoms_dir
    return create_changeunit_from_files(x_changes_dir, file_number, x_atoms_dir)


def _merge_changes_into_agenda(
    x_nookunit: NookUnit, x_agenda: AgendaUnit
) -> AgendaUnit:
    change_ints = get_integer_filenames(
        x_nookunit._changes_dir, x_agenda._last_change_id
    )
    for change_int in change_ints:
        x_change = get_changeunit(x_nookunit, change_int)
        new_agenda = x_change._bookunit.get_edited_agenda(x_agenda)

        update_text = "UPDATE"
        x_change._bookunit.agendaatoms.get(update_text)
    return new_agenda


def _create_duty_from_changes(x_nookunit):
    save_duty_file(
        x_nookunit,
        _merge_changes_into_agenda(x_nookunit, get_default_duty_agenda(x_nookunit)),
    )


def get_default_duty_agenda(x_nookunit: NookUnit) -> AgendaUnit:
    x_agendaunit = agendaunit_shop(
        x_nookunit.person_id,
        x_nookunit.real_id,
        x_nookunit._road_delimiter,
        x_nookunit._planck,
    )
    x_agendaunit._last_change_id = init_change_id()
    return x_agendaunit


def _create_initial_change_and_duty_files(x_nookunit: NookUnit):
    x_changeunit = changeunit_shop(
        _giver=x_nookunit.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_nookunit._changes_dir,
        _atoms_dir=x_nookunit._atoms_dir,
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_nookunit),
        after_agenda=get_default_duty_agenda(x_nookunit),
    )
    x_changeunit.save_files()
    _create_duty_from_changes(x_nookunit)


def initialize_change_and_duty_files(x_nookunit):
    x_duty_file_exists = duty_file_exists(x_nookunit)
    change_file_exists = changeunit_file_exists(x_nookunit, init_change_id())
    if x_duty_file_exists == False and change_file_exists == False:
        _create_initial_change_and_duty_files(x_nookunit)
    elif x_duty_file_exists == False and change_file_exists:
        _create_duty_from_changes(x_nookunit)
    elif x_duty_file_exists and change_file_exists == False:
        _create_initial_change_from_duty(x_nookunit)


def nookunit_create_core_dir_and_files(x_nookunit: NookUnit):
    set_dir(x_nookunit.real_dir)
    set_dir(x_nookunit.persons_dir)
    set_dir(x_nookunit.person_dir)
    set_dir(x_nookunit._econs_dir)
    set_dir(x_nookunit._atoms_dir)
    set_dir(x_nookunit._changes_dir)
    initialize_change_and_duty_files(x_nookunit)
    initialize_work_file(x_nookunit)


def get_work_file_agenda(x_nookunit: NookUnit) -> AgendaUnit:
    work_json = open_file(
        dest_dir=x_nookunit.person_dir, file_name=x_nookunit._work_file_name
    )
    return agendaunit_get_from_json(work_json)


def append_changes_to_duty_file(x_nookunit: NookUnit) -> AgendaUnit:
    duty_agenda = get_duty_file_agenda(x_nookunit)
    duty_agenda = _merge_changes_into_agenda(x_nookunit, duty_agenda)
    save_duty_file(x_nookunit, duty_agenda)
    return get_duty_file_agenda(x_nookunit)


def _get_next_atom_file_number(x_nookunit: NookUnit) -> str:
    max_file_number = _get_max_atom_file_number(x_nookunit)
    return 0 if max_file_number is None else max_file_number + 1


def _get_max_atom_file_number(x_nookunit: NookUnit) -> int:
    if not os_path_exists(x_nookunit._atoms_dir):
        return None
    atom_files_dict = dir_files(x_nookunit._atoms_dir, True, include_files=True)
    atom_filenames = atom_files_dict.keys()
    atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
    return max(atom_file_numbers, default=None)


def validate_changeunit(x_nookunit: NookUnit, x_changeunit: changeUnit) -> changeUnit:
    if x_changeunit._atoms_dir != x_nookunit._atoms_dir:
        x_changeunit._atoms_dir = x_nookunit._atoms_dir
    if x_changeunit._changes_dir != x_nookunit._changes_dir:
        x_changeunit._changes_dir = x_nookunit._changes_dir
    if x_changeunit._change_id != _get_next_change_file_number(x_nookunit):
        x_changeunit._change_id = _get_next_change_file_number(x_nookunit)
    if x_changeunit._giver != x_nookunit.person_id:
        x_changeunit._giver = x_nookunit.person_id
    if x_changeunit._book_start != _get_next_atom_file_number(x_nookunit):
        x_changeunit._book_start = _get_next_atom_file_number(x_nookunit)
    return x_changeunit


def save_changeunit_file(
    x_nookunit: NookUnit,
    x_change: changeUnit,
    replace: bool = True,
    correct_invalid_attrs: bool = True,
) -> changeUnit:
    if correct_invalid_attrs:
        x_change = validate_changeunit(x_nookunit, x_change)

    if x_change._atoms_dir != x_nookunit._atoms_dir:
        raise SavechangeFileException(
            f"changeUnit file cannot be saved because changeunit._atoms_dir is incorrect: {x_change._atoms_dir}. It must be {x_nookunit._atoms_dir}."
        )
    if x_change._changes_dir != x_nookunit._changes_dir:
        raise SavechangeFileException(
            f"changeUnit file cannot be saved because changeunit._changes_dir is incorrect: {x_change._changes_dir}. It must be {x_nookunit._changes_dir}."
        )
    if x_change._giver != x_nookunit.person_id:
        raise SavechangeFileException(
            f"changeUnit file cannot be saved because changeunit._giver is incorrect: {x_change._giver}. It must be {x_nookunit.person_id}."
        )
    change_filename = changeunit_get_json_filename(x_change._change_id)
    if not replace and changeunit_file_exists(x_nookunit, x_change._change_id):
        raise SavechangeFileException(
            f"changeUnit file {change_filename} already exists and cannot be saved over."
        )
    x_change.save_files()
    return x_change


def _create_new_changeunit(x_nookunit: NookUnit) -> changeUnit:
    return changeunit_shop(
        _giver=x_nookunit.person_id,
        _change_id=_get_next_change_file_number(x_nookunit),
        _atoms_dir=x_nookunit._atoms_dir,
        _changes_dir=x_nookunit._changes_dir,
    )


def create_save_changeunit(
    x_nookunit: NookUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    new_changeunit = _create_new_changeunit(x_nookunit)
    new_changeunit._bookunit.add_all_different_agendaatoms(before_agenda, after_agenda)
    save_changeunit_file(x_nookunit, new_changeunit)


def add_pledge_change(x_nookunit, pledge_road: RoadUnit, x_suffgroup: GroupID = None):
    duty_agenda = get_duty_file_agenda(x_nookunit)
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_changeunit = _create_new_changeunit(x_nookunit)
    next_changeunit._bookunit.add_all_different_agendaatoms(
        old_duty_agenda, duty_agenda
    )
    next_changeunit.save_files()
    append_changes_to_duty_file(x_nookunit)


def del_changeunit_file(x_nookunit: NookUnit, file_number: int):
    delete_dir(f"{x_nookunit._changes_dir}/{changeunit_get_json_filename(file_number)}")
