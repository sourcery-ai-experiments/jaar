from src._road.road import PersonID, PersonID
from src._road.worlddir import (
    get_econ_roles_dir,
    get_econ_jobs_dir,
    get_file_name,
)
from src.agenda.agenda import AgendaUnit
from src.agenda.listen import get_speaker_agenda, listen_to_debtors_roll
from src._instrument.file import save_file
from os.path import exists as os_path_exists


class RoleAgendaFileException(Exception):
    pass


def save_role_file(x_econ_dir: str, x_agenda: AgendaUnit):
    x_dest_dir = get_econ_roles_dir(x_econ_dir)
    x_file_name = get_file_name(x_agenda._owner_id)
    save_file(x_dest_dir, x_file_name, x_agenda.get_json())


def save_job_file(x_econ_dir: str, x_agenda: AgendaUnit):
    x_dest_dir = get_econ_jobs_dir(x_econ_dir)
    x_file_name = get_file_name(x_agenda._owner_id)
    save_file(x_dest_dir, x_file_name, x_agenda.get_json())


def get_role_file(x_econ_dir: str, owner_id: PersonID) -> AgendaUnit:
    role_file_name = get_file_name(owner_id)
    roles_dir = get_econ_roles_dir(x_econ_dir)
    if os_path_exists(f"{roles_dir}/{role_file_name}") == False:
        raise RoleAgendaFileException(
            f"Role agenda file '{role_file_name}' does not exist."
        )
    return get_speaker_agenda(roles_dir, owner_id)


def get_job_file(
    x_econ_dir: str, owner_id: PersonID, return_None_if_missing: bool = True
) -> AgendaUnit:
    jobs_dir = get_econ_jobs_dir(x_econ_dir)
    return get_speaker_agenda(jobs_dir, owner_id, return_None_if_missing)


def create_job_file_from_role_file(econ_dir, person_id: PersonID):
    x_role = get_role_file(econ_dir, person_id)
    jobs_dir = get_econ_jobs_dir(econ_dir)
    x_job = listen_to_debtors_roll(x_role, jobs_dir)
    save_job_file(econ_dir, x_job)
    return x_job
