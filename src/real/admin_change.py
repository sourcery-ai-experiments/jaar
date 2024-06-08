from src._instrument.file import delete_dir, dir_files, get_integer_filenames
from src.change.filehub import FileHub
from src.agenda.agenda import AgendaUnit
from src.change.change import (
    ChangeUnit,
    changeunit_shop,
    get_json_filename as changeunit_get_json_filename,
    create_changeunit_from_files,
    get_init_change_id_if_None,
)
from os.path import exists as os_path_exists


class SaveChangeFileException(Exception):
    pass


class ChangeFileMissingException(Exception):
    pass


# ChangeUnit
def changeunit_file_exists(x_filehub: FileHub, change_id: int) -> bool:
    change_filename = changeunit_get_json_filename(change_id)
    return os_path_exists(f"{x_filehub.changes_dir()}/{change_filename}")


def validate_changeunit(x_filehub: FileHub, x_changeunit: ChangeUnit) -> ChangeUnit:
    if x_changeunit._atoms_dir != x_filehub.atoms_dir():
        x_changeunit._atoms_dir = x_filehub.atoms_dir()
    if x_changeunit._changes_dir != x_filehub.changes_dir():
        x_changeunit._changes_dir = x_filehub.changes_dir()
    if x_changeunit._change_id != _get_next_change_file_number(x_filehub):
        x_changeunit._change_id = _get_next_change_file_number(x_filehub)
    if x_changeunit._giver != x_filehub.person_id:
        x_changeunit._giver = x_filehub.person_id
    if x_changeunit._book_start != x_filehub._get_next_atom_file_number():
        x_changeunit._book_start = x_filehub._get_next_atom_file_number()
    return x_changeunit


def save_changeunit_file(
    x_filehub: FileHub,
    x_change: ChangeUnit,
    replace: bool = True,
    correct_invalid_attrs: bool = True,
) -> ChangeUnit:
    if correct_invalid_attrs:
        x_change = validate_changeunit(x_filehub, x_change)

    if x_change._atoms_dir != x_filehub.atoms_dir():
        raise SaveChangeFileException(
            f"ChangeUnit file cannot be saved because changeunit._atoms_dir is incorrect: {x_change._atoms_dir}. It must be {x_filehub.atoms_dir()}."
        )
    if x_change._changes_dir != x_filehub.changes_dir():
        raise SaveChangeFileException(
            f"ChangeUnit file cannot be saved because changeunit._changes_dir is incorrect: {x_change._changes_dir}. It must be {x_filehub.changes_dir()}."
        )
    if x_change._giver != x_filehub.person_id:
        raise SaveChangeFileException(
            f"ChangeUnit file cannot be saved because changeunit._giver is incorrect: {x_change._giver}. It must be {x_filehub.person_id}."
        )
    change_filename = changeunit_get_json_filename(x_change._change_id)
    if not replace and changeunit_file_exists(x_filehub, x_change._change_id):
        raise SaveChangeFileException(
            f"ChangeUnit file {change_filename} already exists and cannot be saved over."
        )
    x_change.save_files()
    return x_change


def _create_new_changeunit(x_filehub: FileHub) -> ChangeUnit:
    return changeunit_shop(
        _giver=x_filehub.person_id,
        _change_id=_get_next_change_file_number(x_filehub),
        _atoms_dir=x_filehub.atoms_dir(),
        _changes_dir=x_filehub.changes_dir(),
    )


def create_save_changeunit(
    x_filehub: FileHub, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    new_changeunit = _create_new_changeunit(x_filehub)
    new_changeunit._bookunit.add_all_different_agendaatoms(before_agenda, after_agenda)
    save_changeunit_file(x_filehub, new_changeunit)


def get_max_change_file_number(x_filehub: FileHub) -> int:
    if not os_path_exists(x_filehub.changes_dir()):
        return None
    x_changes_dir = x_filehub.changes_dir()
    change_filenames = dir_files(x_changes_dir, True, include_files=True).keys()
    change_file_numbers = {int(change_filename) for change_filename in change_filenames}
    return max(change_file_numbers, default=None)


def _get_next_change_file_number(x_filehub: FileHub) -> int:
    max_file_number = get_max_change_file_number(x_filehub)
    init_change_id = get_init_change_id_if_None()
    return init_change_id if max_file_number is None else max_file_number + 1


def get_changeunit(x_filehub: FileHub, file_number: int) -> ChangeUnit:
    if changeunit_file_exists(x_filehub, file_number) == False:
        raise ChangeFileMissingException(
            f"ChangeUnit file_number {file_number} does not exist."
        )
    x_changes_dir = x_filehub.changes_dir()
    x_atoms_dir = x_filehub.atoms_dir()
    return create_changeunit_from_files(x_changes_dir, file_number, x_atoms_dir)


def _merge_changes_into_agenda(x_filehub: FileHub, x_agenda: AgendaUnit) -> AgendaUnit:
    changes_dir = x_filehub.changes_dir()
    change_ints = get_integer_filenames(changes_dir, x_agenda._last_change_id)
    for change_int in change_ints:
        x_change = get_changeunit(x_filehub, change_int)
        new_agenda = x_change._bookunit.get_edited_agenda(x_agenda)

        update_text = "UPDATE"
        x_change._bookunit.agendaatoms.get(update_text)
    return new_agenda


def del_changeunit_file(x_filehub: FileHub, file_number: int):
    delete_dir(f"{x_filehub.changes_dir()}/{changeunit_get_json_filename(file_number)}")
