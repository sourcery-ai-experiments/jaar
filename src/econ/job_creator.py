from src._road.road import PersonID, PartyID, PersonID
from src.agenda.party import PartyUnit
from src.agenda.agenda import get_from_json as agendaunit_get_from_json, AgendaUnit
from src.agenda.listen import listen_to_speaker_intent, create_empty_agenda
from src._instrument.file import save_file, open_file
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy


class RoleAgendaFileException(Exception):
    pass


def get_owner_file_name(x_owner_id: str) -> str:
    return f"{x_owner_id}.json"


def get_econ_roles_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/roles"


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/jobs"


def save_role_file(x_econ_dir: str, x_agenda: AgendaUnit):
    x_dest_dir = get_econ_roles_dir(x_econ_dir)
    x_file_name = get_owner_file_name(x_agenda._owner_id)
    save_file(x_dest_dir, x_file_name, x_agenda.get_json())


def save_job_file(x_econ_dir: str, x_agenda: AgendaUnit):
    x_dest_dir = get_econ_jobs_dir(x_econ_dir)
    x_file_name = get_owner_file_name(x_agenda._owner_id)
    save_file(x_dest_dir, x_file_name, x_agenda.get_json())


def get_role_file(x_econ_dir: str, owner_id: PersonID) -> AgendaUnit:
    role_file_name = get_owner_file_name(owner_id)
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
    job_file_name = get_owner_file_name(owner_id)
    job_dir = get_econ_jobs_dir(x_econ_dir)
    job_file_path = f"{job_dir}/{job_file_name}"
    if os_path_exists(job_file_path) or not return_None_if_missing:
        return agendaunit_get_from_json(open_file(job_dir, job_file_name))
    else:
        None


def create_job_basis(x_role: AgendaUnit) -> AgendaUnit:
    x_job = create_empty_agenda(x_role, x_owner_id=x_role._owner_id)
    x_job._partys = x_role._partys
    x_job._groups = x_role._groups
    x_job.set_money_desc(x_role._money_desc)
    if x_role._party_creditor_pool != None:
        x_job.set_party_creditor_pool(x_role._party_creditor_pool)
    if x_role._party_debtor_pool != None:
        x_job.set_party_debtor_pool(x_role._party_debtor_pool)
    x_job = copy_deepcopy(x_job)
    for x_partyunit in x_job._partys.values():
        x_partyunit.reset_job_basis_attrs()
    return x_job


def get_debtors_roll(x_role: AgendaUnit) -> dict[PartyID:PartyUnit]:
    return [
        x_partyunit
        for x_partyunit in x_role._partys.values()
        if x_partyunit.debtor_weight != 0
    ]


def _listen_to_debtors_roll(econ_dir: str, listener_role: AgendaUnit) -> AgendaUnit:
    x_job = create_job_basis(listener_role)
    if x_job._party_debtor_pool is None:
        return x_job

    for x_partyunit in get_debtors_roll(x_job):
        if x_partyunit.party_id == x_job._owner_id:
            listen_to_speaker_intent(x_job, listener_role)
        else:
            speaker_job = get_job_file(econ_dir, x_partyunit.party_id)
            if speaker_job is None:
                speaker_job = create_empty_agenda(x_job, x_partyunit.party_id)
            listen_to_speaker_intent(x_job, speaker_job)
    return x_job


def create_job_file_from_role_file(econ_dir, person_id: PersonID):
    x_role = get_role_file(econ_dir, person_id)
    x_job = _listen_to_debtors_roll(econ_dir, x_role)
    save_job_file(econ_dir, x_job)
    return x_job
