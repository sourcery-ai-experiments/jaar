from src._instrument.file import delete_dir, get_integer_filenames
from src.change.filehub import FileHub
from src.agenda.agenda import AgendaUnit
from src.change.change import (
    ChangeUnit,
    changeunit_shop,
    create_changeunit_from_files,
)


class ChangeFileMissingException(Exception):
    pass


def _create_new_changeunit(x_filehub: FileHub) -> ChangeUnit:
    return changeunit_shop(
        _giver=x_filehub.person_id,
        _change_id=x_filehub._get_next_change_file_number(),
        _atoms_dir=x_filehub.atoms_dir(),
        _changes_dir=x_filehub.changes_dir(),
    )


def create_save_changeunit(
    x_filehub: FileHub, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    new_changeunit = _create_new_changeunit(x_filehub)
    new_changeunit._bookunit.add_all_different_agendaatoms(before_agenda, after_agenda)
    x_filehub.save_change_file(new_changeunit)


def get_changeunit(x_filehub: FileHub, file_number: int) -> ChangeUnit:
    if x_filehub.change_file_exists(file_number) == False:
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
    delete_dir(f"{x_filehub.changes_dir()}/{x_filehub.change_file_name(file_number)}")
