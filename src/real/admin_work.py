from src._road.userdir import UserDir
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
)
from src.agenda.listen import create_listen_basis


class Invalid_work_Exception(Exception):
    pass


def save_work_file(x_userdir: UserDir, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_userdir.person_id:
        raise Invalid_work_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_userdir.person_id}''s work agenda."
        )
    if replace in {True, False}:
        x_userdir.save_file_work(x_agenda.get_json(), replace)


def initialize_work_file(x_userdir: UserDir, duty: AgendaUnit):
    if x_userdir.work_file_exists() == False:
        save_work_file(x_userdir, get_default_work_agenda(duty))


def get_work_file_agenda(x_userdir: UserDir) -> AgendaUnit:
    work_json = x_userdir.open_file_work()
    return agendaunit_get_from_json(work_json)


def get_default_work_agenda(duty: AgendaUnit) -> AgendaUnit:
    default_work_agenda = create_listen_basis(duty)
    default_work_agenda._last_change_id = duty._last_change_id
    default_work_agenda._party_creditor_pool = None
    default_work_agenda._party_debtor_pool = None
    return default_work_agenda
