from src._instrument.file import get_integer_filenames
from src.change.filehub import FileHub
from src.agenda.agenda import AgendaUnit


def _merge_changes_into_agenda(x_filehub: FileHub, x_agenda: AgendaUnit) -> AgendaUnit:
    changes_dir = x_filehub.changes_dir()
    change_ints = get_integer_filenames(changes_dir, x_agenda._last_change_id)
    for change_int in change_ints:
        x_change = x_filehub.get_changeunit(change_int)
        new_agenda = x_change._bookunit.get_edited_agenda(x_agenda)

        update_text = "UPDATE"
        x_change._bookunit.agendaatoms.get(update_text)
    return new_agenda
