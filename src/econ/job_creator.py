from src._road.road import PersonID, PersonID
from src._road.worlddir import (
    get_econ_roles_dir,
    get_econ_jobs_dir,
    get_file_name,
)
from src.agenda.agenda import get_from_json as agendaunit_get_from_json, AgendaUnit
from src.agenda.listen import (
    get_ordered_partys_roll,
    listen_to_speaker_intent,
    create_empty_agenda,
    create_listen_basis,
)
from src._instrument.file import save_file, open_file
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
    role_dir = get_econ_roles_dir(x_econ_dir)
    try:
        role_file_text = open_file(role_dir, role_file_name)
    except:
        raise RoleAgendaFileException(
            f"Role agenda file '{role_file_name}' does not exist."
        )
    return agendaunit_get_from_json(role_file_text)


def get_job_file(
    x_econ_dir: str, owner_id: PersonID, return_None_if_missing: bool = True
) -> AgendaUnit:
    jobs_dir = get_econ_jobs_dir(x_econ_dir)
    return get_speaker_agenda(jobs_dir, owner_id, return_None_if_missing)


def get_speaker_agenda(
    x_dir: str, owner_id: PersonID, return_None_if_missing: bool = True
) -> AgendaUnit:
    job_file_name = get_file_name(owner_id)
    job_file_path = f"{x_dir}/{job_file_name}"
    if os_path_exists(job_file_path) or not return_None_if_missing:
        return agendaunit_get_from_json(open_file(x_dir, job_file_name))
    else:
        None


def listen_to_debtors_roll(listener: AgendaUnit, speakers_dir: str) -> AgendaUnit:
    new_agenda = create_listen_basis(listener)
    if new_agenda._party_debtor_pool is None:
        return new_agenda

    for x_partyunit in get_ordered_partys_roll(new_agenda):
        if x_partyunit.party_id == new_agenda._owner_id:
            listen_to_speaker_intent(new_agenda, listener)
        else:
            speaker_job = get_speaker_agenda(speakers_dir, x_partyunit.party_id)
            if speaker_job is None:
                speaker_job = create_empty_agenda(new_agenda, x_partyunit.party_id)
            listen_to_speaker_intent(new_agenda, speaker_job)
    return new_agenda


def create_job_file_from_role_file(econ_dir, person_id: PersonID):
    x_role = get_role_file(econ_dir, person_id)
    jobs_dir = get_econ_jobs_dir(econ_dir)
    x_job = listen_to_debtors_roll(x_role, jobs_dir)
    save_job_file(econ_dir, x_job)
    return x_job
