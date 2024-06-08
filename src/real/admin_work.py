from src._road.worldnox import UserNox
from src.agenda.agenda import AgendaUnit, get_from_json as agendaunit_get_from_json
from src.change.filehub import filehub_shop
from src.change.listen import create_listen_basis


class Invalid_work_Exception(Exception):
    pass


def initialize_work_file(x_usernox: UserNox, duty: AgendaUnit):
    x_filehub = filehub_shop(
        reals_dir=x_usernox.reals_dir,
        real_id=x_usernox.real_id,
        person_id=x_usernox.person_id,
        econ_road=None,
        road_delimiter=x_usernox._road_delimiter,
        planck=x_usernox._planck,
    )
    if x_filehub.work_file_exists() == False:
        x_filehub.save_work_agenda(get_default_work_agenda(duty))


def get_default_work_agenda(duty: AgendaUnit) -> AgendaUnit:
    default_work_agenda = create_listen_basis(duty)
    default_work_agenda._last_change_id = duty._last_change_id
    default_work_agenda._party_creditor_pool = None
    default_work_agenda._party_debtor_pool = None
    return default_work_agenda
