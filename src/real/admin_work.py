from src._instrument.file import save_file, open_file
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
)
from src.real.userdir import UserDir
from os.path import exists as os_path_exists


class Invalid_work_Exception(Exception):
    pass


def work_file_exists(userdir: UserDir) -> bool:
    return os_path_exists(userdir._work_path)


def save_work_file(x_userdir: UserDir, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_userdir.person_id:
        raise Invalid_work_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_userdir.person_id}''s work agenda."
        )
    if replace in {True, False}:
        save_file(
            dest_dir=x_userdir.person_dir,
            file_name=x_userdir._work_file_name,
            file_text=x_agenda.get_json(),
            replace=replace,
        )


def initialize_work_file(x_userdir):
    if work_file_exists(x_userdir) == False:
        default_work_agenda = agendaunit_shop(
            x_userdir.person_id,
            x_userdir.real_id,
            x_userdir._road_delimiter,
            x_userdir._planck,
        )
        save_work_file(x_userdir, default_work_agenda)


def get_work_file_agenda(x_userdir: UserDir) -> AgendaUnit:
    work_json = open_file(
        dest_dir=x_userdir.person_dir, file_name=x_userdir._work_file_name
    )
    return agendaunit_get_from_json(work_json)
