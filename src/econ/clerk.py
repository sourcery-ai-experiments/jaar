from src._road.road import PersonID, PartyID, ClerkID
from src.agenda.party import PartyUnit
from src.agenda.agenda import (
    get_from_json as agendaunit_get_from_json,
    AgendaUnit,
    agendaunit_shop,
    partyunit_shop,
    get_from_json as agendaunit_get_from_json,
)
from src.instrument.file import (
    set_dir,
    save_file,
    open_file,
    delete_dir,
    rename_dir as x_func_rename_dir,
)
from src._road.road import default_road_delimiter_if_none
from dataclasses import dataclass
from os import path as os_path


class InvalidclerkException(Exception):
    pass


class RoleAgendaFileException(Exception):
    pass


def get_owner_file_name(x_owner_id: str) -> str:
    return f"{x_owner_id}.json"


def get_econ_guts_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/guts"


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/jobs"


def save_file_to_guts(x_econ_dir: str, x_agenda: AgendaUnit):
    save_file(
        dest_dir=get_econ_guts_dir(x_econ_dir),
        file_name=get_owner_file_name(x_agenda._owner_id),
        file_text=x_agenda.get_json(),
    )


def save_file_to_jobs(x_econ_dir: str, x_agenda: AgendaUnit):
    save_file(
        dest_dir=get_econ_jobs_dir(x_econ_dir),
        file_name=get_owner_file_name(x_agenda._owner_id),
        file_text=x_agenda.get_json(),
    )


def get_file_in_guts(x_econ_dir: str, owner_id: PersonID) -> AgendaUnit:
    gut_file_name = get_owner_file_name(owner_id)
    gut_dir = get_econ_guts_dir(x_econ_dir)
    try:
        gut_file_text = open_file(gut_dir, gut_file_name)
    except:
        raise RoleAgendaFileException(
            f"Role agenda file '{gut_file_name}' does not exist."
        )
    return agendaunit_get_from_json(gut_file_text)


def get_file_in_jobs(x_econ_dir: str, owner_id: PersonID) -> AgendaUnit:
    job_file_name = get_owner_file_name(owner_id)
    job_dir = get_econ_jobs_dir(x_econ_dir)
    return agendaunit_get_from_json(open_file(job_dir, job_file_name))


@dataclass
class ClerkUnit:
    _clerk_id: ClerkID = None
    _econ_dir: str = None
    _guts_dir: str = None
    _jobs_dir: str = None
    _role_file_path: str = None
    # _road_delimiter: str = None
    _role: AgendaUnit = None
    _job: AgendaUnit = None
    _roll: list[(PartyID, PartyUnit)] = None

    def set_clerk_id(self, x_clerk_id: PersonID):
        self._clerk_id = x_clerk_id

    def set_econ_dir(self, x_econ_dir: str):
        self._econ_dir = x_econ_dir

    def _set_role(self):
        self._role = get_file_in_guts(self._econ_dir, self._clerk_id)

    def _set_roll(self):
        for x_partyunit in self._role._partys.values():
            self._roll.append((x_partyunit.party_id, x_partyunit.debtor_weight))

    def _set_empty_job(self):
        self._job = agendaunit_shop(
            self._role._owner_id,
            self._role._world_id,
            _road_delimiter=self._role._road_delimiter,
        )
        self._job._partys = self._role._partys
        self._job._groups = self._role._groups
        self._job._planck = self._role._planck
        self._job.set_money_desc(self._role._money_desc)
        if self._role._party_creditor_pool != None:
            self._job.set_party_creditor_pool(self._role._party_creditor_pool)
        if self._role._party_debtor_pool != None:
            self._job.set_party_debtor_pool(self._role._party_debtor_pool)


def clerkunit_shop(
    clerk_id: PersonID, env_dir: str, create_job: bool = True
) -> ClerkUnit:
    x_clerk = ClerkUnit()
    x_clerk._roll = []
    x_clerk.set_econ_dir(x_econ_dir=env_dir)
    x_clerk.set_clerk_id(x_clerk_id=clerk_id)
    x_clerk._set_clerkunit_dirs()
    if create_job:
        x_clerk._set_role()
        x_clerk._set_roll()
        x_clerk._set_empty_job()
    return x_clerk
