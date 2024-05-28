from src._instrument.file import (
    save_file,
    open_file,
    set_dir,
    delete_dir,
    dir_files,
    get_integer_filenames,
)
from src._road.road import RoadUnit
from src.agenda.group import GroupID
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
)
from src.agenda.atom import (
    AgendaAtom,
    get_from_json as agendaatom_get_from_json,
    modify_agenda_with_agendaatom,
)
from src.agenda.pledge import create_pledge
from src.real.change import (
    ChangeUnit,
    changeunit_shop,
    get_json_filename as changeunit_get_json_filename,
    create_changeunit_from_files,
    init_change_id,
    get_init_change_id_if_None,
)
from src.real.userdir import UserDir
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy


class Invalid_duty_Exception(Exception):
    pass


class SavechangeFileException(Exception):
    pass


class changeFileMissingException(Exception):
    pass


# AgendaAtom
def userdir_save_atom_file(x_userdir: UserDir, x_atom: AgendaAtom):
    x_filename = _get_next_atom_file_number(x_userdir)
    return _save_valid_atom_file(x_userdir, x_atom, x_filename)


def _save_valid_atom_file(x_userdir: UserDir, x_atom: AgendaAtom, file_number: int):
    save_file(x_userdir._atoms_dir, f"{file_number}.json", x_atom.get_json())
    return file_number


def userdir_atom_file_exists(x_userdir, filename: int) -> bool:
    return os_path_exists(f"{x_userdir._atoms_dir}/{filename}.json")


def _delete_atom_file(x_userdir: UserDir, filename: int):
    delete_dir(f"{x_userdir._atoms_dir}/{filename}.json")


def _get_agenda_from_atom_files(x_userdir: UserDir) -> AgendaUnit:
    x_agenda = agendaunit_shop(x_userdir.person_id, x_userdir.real_id)
    x_atom_files = dir_files(x_userdir._atoms_dir, delete_extensions=True)
    sorted_atom_filenames = sorted(list(x_atom_files.keys()))

    for x_atom_filename in sorted_atom_filenames:
        x_file_text = x_atom_files.get(x_atom_filename)
        x_atom = agendaatom_get_from_json(x_file_text)
        modify_agenda_with_agendaatom(x_agenda, x_atom)
    return x_agenda


def _get_max_atom_file_number(x_userdir: UserDir) -> int:
    if not os_path_exists(x_userdir._atoms_dir):
        return None
    atom_files_dict = dir_files(x_userdir._atoms_dir, True, include_files=True)
    atom_filenames = atom_files_dict.keys()
    atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
    return max(atom_file_numbers, default=None)


def _get_next_atom_file_number(x_userdir: UserDir) -> str:
    max_file_number = _get_max_atom_file_number(x_userdir)
    return 0 if max_file_number is None else max_file_number + 1


# ChangeUnit
def changeunit_file_exists(x_userdir: UserDir, change_id: int) -> bool:
    change_filename = changeunit_get_json_filename(change_id)
    return os_path_exists(f"{x_userdir._changes_dir}/{change_filename}")


def validate_changeunit(x_userdir: UserDir, x_changeunit: ChangeUnit) -> ChangeUnit:
    if x_changeunit._atoms_dir != x_userdir._atoms_dir:
        x_changeunit._atoms_dir = x_userdir._atoms_dir
    if x_changeunit._changes_dir != x_userdir._changes_dir:
        x_changeunit._changes_dir = x_userdir._changes_dir
    if x_changeunit._change_id != _get_next_change_file_number(x_userdir):
        x_changeunit._change_id = _get_next_change_file_number(x_userdir)
    if x_changeunit._giver != x_userdir.person_id:
        x_changeunit._giver = x_userdir.person_id
    if x_changeunit._book_start != _get_next_atom_file_number(x_userdir):
        x_changeunit._book_start = _get_next_atom_file_number(x_userdir)
    return x_changeunit


def save_changeunit_file(
    x_userdir: UserDir,
    x_change: ChangeUnit,
    replace: bool = True,
    correct_invalid_attrs: bool = True,
) -> ChangeUnit:
    if correct_invalid_attrs:
        x_change = validate_changeunit(x_userdir, x_change)

    if x_change._atoms_dir != x_userdir._atoms_dir:
        raise SavechangeFileException(
            f"ChangeUnit file cannot be saved because changeunit._atoms_dir is incorrect: {x_change._atoms_dir}. It must be {x_userdir._atoms_dir}."
        )
    if x_change._changes_dir != x_userdir._changes_dir:
        raise SavechangeFileException(
            f"ChangeUnit file cannot be saved because changeunit._changes_dir is incorrect: {x_change._changes_dir}. It must be {x_userdir._changes_dir}."
        )
    if x_change._giver != x_userdir.person_id:
        raise SavechangeFileException(
            f"ChangeUnit file cannot be saved because changeunit._giver is incorrect: {x_change._giver}. It must be {x_userdir.person_id}."
        )
    change_filename = changeunit_get_json_filename(x_change._change_id)
    if not replace and changeunit_file_exists(x_userdir, x_change._change_id):
        raise SavechangeFileException(
            f"ChangeUnit file {change_filename} already exists and cannot be saved over."
        )
    x_change.save_files()
    return x_change


def _create_new_changeunit(x_userdir: UserDir) -> ChangeUnit:
    return changeunit_shop(
        _giver=x_userdir.person_id,
        _change_id=_get_next_change_file_number(x_userdir),
        _atoms_dir=x_userdir._atoms_dir,
        _changes_dir=x_userdir._changes_dir,
    )


def create_save_changeunit(
    x_userdir: UserDir, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    new_changeunit = _create_new_changeunit(x_userdir)
    new_changeunit._bookunit.add_all_different_agendaatoms(before_agenda, after_agenda)
    save_changeunit_file(x_userdir, new_changeunit)


def get_max_change_file_number(x_userdir: UserDir) -> int:
    if not os_path_exists(x_userdir._changes_dir):
        return None
    x_changes_dir = x_userdir._changes_dir
    change_filenames = dir_files(x_changes_dir, True, include_files=True).keys()
    change_file_numbers = {int(change_filename) for change_filename in change_filenames}
    return max(change_file_numbers, default=None)


def _get_next_change_file_number(x_userdir: UserDir) -> int:
    max_file_number = get_max_change_file_number(x_userdir)
    init_change_id = get_init_change_id_if_None()
    return init_change_id if max_file_number is None else max_file_number + 1


def get_changeunit(x_userdir: UserDir, file_number: int) -> ChangeUnit:
    if changeunit_file_exists(x_userdir, file_number) == False:
        raise changeFileMissingException(
            f"ChangeUnit file_number {file_number} does not exist."
        )
    x_changes_dir = x_userdir._changes_dir
    x_atoms_dir = x_userdir._atoms_dir
    return create_changeunit_from_files(x_changes_dir, file_number, x_atoms_dir)


def _merge_changes_into_agenda(x_userdir: UserDir, x_agenda: AgendaUnit) -> AgendaUnit:
    changes_dir = x_userdir._changes_dir
    change_ints = get_integer_filenames(changes_dir, x_agenda._last_change_id)
    for change_int in change_ints:
        x_change = get_changeunit(x_userdir, change_int)
        new_agenda = x_change._bookunit.get_edited_agenda(x_agenda)

        update_text = "UPDATE"
        x_change._bookunit.agendaatoms.get(update_text)
    return new_agenda


def _create_initial_change_from_duty(x_userdir: UserDir):
    x_changeunit = changeunit_shop(
        _giver=x_userdir.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_userdir._changes_dir,
        _atoms_dir=x_userdir._atoms_dir,
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_userdir),
        after_agenda=get_duty_file_agenda(x_userdir),
    )
    x_changeunit.save_files()


def del_changeunit_file(x_userdir: UserDir, file_number: int):
    delete_dir(f"{x_userdir._changes_dir}/{changeunit_get_json_filename(file_number)}")


# duty
def save_duty_file(x_userdir: UserDir, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_userdir.person_id:
        raise Invalid_duty_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_userdir.person_id}''s duty agenda."
        )
    if replace in {True, False}:
        save_file(
            dest_dir=x_userdir.person_dir,
            file_name=x_userdir._duty_file_name,
            file_text=x_agenda.get_json(),
            replace=replace,
        )


def duty_file_exists(userdir: UserDir) -> bool:
    return os_path_exists(userdir._duty_path)


def get_duty_file_agenda(x_userdir: UserDir) -> AgendaUnit:
    if duty_file_exists(x_userdir) == False:
        save_duty_file(x_userdir, get_default_duty_agenda(x_userdir))
    duty_json = open_file(x_userdir.person_dir, x_userdir._duty_file_name)
    return agendaunit_get_from_json(duty_json)


def _create_duty_from_changes(x_userdir):
    x_agenda = _merge_changes_into_agenda(x_userdir, get_default_duty_agenda(x_userdir))
    save_duty_file(x_userdir, x_agenda)


def get_default_duty_agenda(x_userdir: UserDir) -> AgendaUnit:
    x_agendaunit = agendaunit_shop(
        x_userdir.person_id,
        x_userdir.real_id,
        x_userdir._road_delimiter,
        x_userdir._planck,
    )
    x_agendaunit._last_change_id = init_change_id()
    return x_agendaunit


def initialize_change_duty_files(x_userdir):
    set_dir(x_userdir.real_dir)
    set_dir(x_userdir.persons_dir)
    set_dir(x_userdir.person_dir)
    set_dir(x_userdir._atoms_dir)
    set_dir(x_userdir._changes_dir)
    x_duty_file_exists = duty_file_exists(x_userdir)
    change_file_exists = changeunit_file_exists(x_userdir, init_change_id())
    if x_duty_file_exists == False and change_file_exists == False:
        _create_initial_change_and_duty_files(x_userdir)
    elif x_duty_file_exists == False and change_file_exists:
        _create_duty_from_changes(x_userdir)
    elif x_duty_file_exists and change_file_exists == False:
        _create_initial_change_from_duty(x_userdir)


def append_changes_to_duty_file(x_userdir: UserDir) -> AgendaUnit:
    duty_agenda = get_duty_file_agenda(x_userdir)
    duty_agenda = _merge_changes_into_agenda(x_userdir, duty_agenda)
    save_duty_file(x_userdir, duty_agenda)
    return get_duty_file_agenda(x_userdir)


def _create_initial_change_and_duty_files(x_userdir: UserDir):
    x_changeunit = changeunit_shop(
        _giver=x_userdir.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_userdir._changes_dir,
        _atoms_dir=x_userdir._atoms_dir,
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_userdir),
        after_agenda=get_default_duty_agenda(x_userdir),
    )
    x_changeunit.save_files()
    _create_duty_from_changes(x_userdir)


def add_pledge_change(x_userdir, pledge_road: RoadUnit, x_suffgroup: GroupID = None):
    duty_agenda = get_duty_file_agenda(x_userdir)
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_changeunit = _create_new_changeunit(x_userdir)
    next_changeunit._bookunit.add_all_different_agendaatoms(
        old_duty_agenda, duty_agenda
    )
    next_changeunit.save_files()
    append_changes_to_duty_file(x_userdir)
