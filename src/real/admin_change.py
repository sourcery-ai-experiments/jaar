from src._instrument.file import save_file, delete_dir, dir_files, get_integer_filenames
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.agenda.atom import (
    AgendaAtom,
    get_from_json as agendaatom_get_from_json,
    modify_agenda_with_agendaatom,
)
from src.agenda.change import (
    ChangeUnit,
    changeunit_shop,
    get_json_filename as changeunit_get_json_filename,
    create_changeunit_from_files,
    init_change_id,
    get_init_change_id_if_None,
)
from src._road.worlddir import UserDir
from os.path import exists as os_path_exists


class SaveChangeFileException(Exception):
    pass


class ChangeFileMissingException(Exception):
    pass


# AgendaAtom
def userdir_save_atom_file(x_userdir: UserDir, x_atom: AgendaAtom):
    x_filename = _get_next_atom_file_number(x_userdir)
    return _save_valid_atom_file(x_userdir, x_atom, x_filename)


def _save_valid_atom_file(x_userdir: UserDir, x_atom: AgendaAtom, file_number: int):
    save_file(x_userdir.atoms_dir(), f"{file_number}.json", x_atom.get_json())
    return file_number


def userdir_atom_file_exists(x_userdir, filename: int) -> bool:
    return os_path_exists(f"{x_userdir.atoms_dir()}/{filename}.json")


def _delete_atom_file(x_userdir: UserDir, filename: int):
    delete_dir(f"{x_userdir.atoms_dir()}/{filename}.json")


def _get_agenda_from_atom_files(x_userdir: UserDir) -> AgendaUnit:
    x_agenda = agendaunit_shop(x_userdir.person_id, x_userdir.real_id)
    x_atom_files = dir_files(x_userdir.atoms_dir(), delete_extensions=True)
    sorted_atom_filenames = sorted(list(x_atom_files.keys()))

    for x_atom_filename in sorted_atom_filenames:
        x_file_text = x_atom_files.get(x_atom_filename)
        x_atom = agendaatom_get_from_json(x_file_text)
        modify_agenda_with_agendaatom(x_agenda, x_atom)
    return x_agenda


def _get_max_atom_file_number(x_userdir: UserDir) -> int:
    if not os_path_exists(x_userdir.atoms_dir()):
        return None
    atom_files_dict = dir_files(x_userdir.atoms_dir(), True, include_files=True)
    atom_filenames = atom_files_dict.keys()
    atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
    return max(atom_file_numbers, default=None)


def _get_next_atom_file_number(x_userdir: UserDir) -> str:
    max_file_number = _get_max_atom_file_number(x_userdir)
    return 0 if max_file_number is None else max_file_number + 1


# ChangeUnit
def changeunit_file_exists(x_userdir: UserDir, change_id: int) -> bool:
    change_filename = changeunit_get_json_filename(change_id)
    return os_path_exists(f"{x_userdir.changes_dir()}/{change_filename}")


def validate_changeunit(x_userdir: UserDir, x_changeunit: ChangeUnit) -> ChangeUnit:
    if x_changeunit._atoms_dir != x_userdir.atoms_dir():
        x_changeunit._atoms_dir = x_userdir.atoms_dir()
    if x_changeunit._changes_dir != x_userdir.changes_dir():
        x_changeunit._changes_dir = x_userdir.changes_dir()
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

    if x_change._atoms_dir != x_userdir.atoms_dir():
        raise SaveChangeFileException(
            f"ChangeUnit file cannot be saved because changeunit._atoms_dir is incorrect: {x_change._atoms_dir}. It must be {x_userdir.atoms_dir()}."
        )
    if x_change._changes_dir != x_userdir.changes_dir():
        raise SaveChangeFileException(
            f"ChangeUnit file cannot be saved because changeunit._changes_dir is incorrect: {x_change._changes_dir}. It must be {x_userdir.changes_dir()}."
        )
    if x_change._giver != x_userdir.person_id:
        raise SaveChangeFileException(
            f"ChangeUnit file cannot be saved because changeunit._giver is incorrect: {x_change._giver}. It must be {x_userdir.person_id}."
        )
    change_filename = changeunit_get_json_filename(x_change._change_id)
    if not replace and changeunit_file_exists(x_userdir, x_change._change_id):
        raise SaveChangeFileException(
            f"ChangeUnit file {change_filename} already exists and cannot be saved over."
        )
    x_change.save_files()
    return x_change


def _create_new_changeunit(x_userdir: UserDir) -> ChangeUnit:
    return changeunit_shop(
        _giver=x_userdir.person_id,
        _change_id=_get_next_change_file_number(x_userdir),
        _atoms_dir=x_userdir.atoms_dir(),
        _changes_dir=x_userdir.changes_dir(),
    )


def create_save_changeunit(
    x_userdir: UserDir, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    new_changeunit = _create_new_changeunit(x_userdir)
    new_changeunit._bookunit.add_all_different_agendaatoms(before_agenda, after_agenda)
    save_changeunit_file(x_userdir, new_changeunit)


def get_max_change_file_number(x_userdir: UserDir) -> int:
    if not os_path_exists(x_userdir.changes_dir()):
        return None
    x_changes_dir = x_userdir.changes_dir()
    change_filenames = dir_files(x_changes_dir, True, include_files=True).keys()
    change_file_numbers = {int(change_filename) for change_filename in change_filenames}
    return max(change_file_numbers, default=None)


def _get_next_change_file_number(x_userdir: UserDir) -> int:
    max_file_number = get_max_change_file_number(x_userdir)
    init_change_id = get_init_change_id_if_None()
    return init_change_id if max_file_number is None else max_file_number + 1


def get_changeunit(x_userdir: UserDir, file_number: int) -> ChangeUnit:
    if changeunit_file_exists(x_userdir, file_number) == False:
        raise ChangeFileMissingException(
            f"ChangeUnit file_number {file_number} does not exist."
        )
    x_changes_dir = x_userdir.changes_dir()
    x_atoms_dir = x_userdir.atoms_dir()
    return create_changeunit_from_files(x_changes_dir, file_number, x_atoms_dir)


def _merge_changes_into_agenda(x_userdir: UserDir, x_agenda: AgendaUnit) -> AgendaUnit:
    changes_dir = x_userdir.changes_dir()
    change_ints = get_integer_filenames(changes_dir, x_agenda._last_change_id)
    for change_int in change_ints:
        x_change = get_changeunit(x_userdir, change_int)
        new_agenda = x_change._bookunit.get_edited_agenda(x_agenda)

        update_text = "UPDATE"
        x_change._bookunit.agendaatoms.get(update_text)
    return new_agenda


def del_changeunit_file(x_userdir: UserDir, file_number: int):
    delete_dir(f"{x_userdir.changes_dir()}/{changeunit_get_json_filename(file_number)}")
