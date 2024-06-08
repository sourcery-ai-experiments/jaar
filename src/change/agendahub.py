from src._instrument.file import (
    get_directory_path,
    save_file,
    open_file,
    delete_dir,
    dir_files,
    set_dir,
)
from src._road.road import (
    PersonID,
    RealID,
    RoadNode,
    RoadUnit,
    rebuild_road,
    get_all_road_nodes,
)
from src._road.jaar_config import (
    roles_str,
    jobs_str,
    get_rootpart_of_econ_dir,
    treasury_str,
    treasury_file_name,
)
from src._road.worldnox import UserNox, usernox_shop, get_file_name
from src.agenda.agenda import AgendaUnit, get_from_json as agendaunit_get_from_json
from os.path import exists as os_path_exists
from dataclasses import dataclass


class Invalid_nox_type_Exception(Exception):
    pass


class Invalid_duty_Exception(Exception):
    pass


class Invalid_work_Exception(Exception):
    pass


def get_econ_path(x_usernox: UserNox, x_road: RoadNode) -> str:
    econ_root = get_rootpart_of_econ_dir()
    x_road = rebuild_road(x_road, x_usernox.real_id, econ_root)
    x_list = get_all_road_nodes(x_road, x_usernox._road_delimiter)
    return f"{x_usernox.econs_dir()}{get_directory_path(x_list=[*x_list])}"


def get_econ_roles_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{roles_str()}"


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{jobs_str()}"


def get_nox_type_set() -> set[str]:
    return {
        pipeline_duty_work_text(),
        pipeline_role_job_text(),
        pipeline_job_work_text(),
    }


def pipeline_duty_work_text() -> str:
    return "duty_work"


def pipeline_role_job_text() -> str:
    return "role_job"


def pipeline_job_work_text() -> str:
    return "job_work"


@dataclass
class AgendaHub(UserNox):
    econ_road: RoadUnit = None
    _nox_type: str = None  # can be "duty_work", "role_job", "job_work"

    def econ_dir(self) -> str:
        return get_econ_path(self, self.econ_road)

    def create_econ_dir_if_missing(self):
        set_dir(self.econ_dir())

    def owner_file_name(self, owner_id: PersonID) -> str:
        return get_file_name(owner_id)

    def treasury_file_name(self) -> str:
        return treasury_file_name()

    def treasury_db_path(self) -> str:
        return f"{self.econ_dir()}/{treasury_file_name()}"

    def role_path(self, owner_id: PersonID) -> str:
        return f"{self.roles_dir()}/{self.owner_file_name(owner_id)}"

    def job_path(self, owner_id: PersonID) -> str:
        return f"{self.jobs_dir()}/{self.owner_file_name(owner_id)}"

    def roles_dir(self) -> str:
        return get_econ_roles_dir(self.econ_dir())

    def jobs_dir(self) -> str:
        return get_econ_jobs_dir(self.econ_dir())

    def get_jobs_dir_file_names_list(self):
        try:
            return list(dir_files(self.jobs_dir(), True).keys())
        except Exception:
            return []

    def save_role_agenda(self, x_agenda: AgendaUnit):
        x_file_name = self.owner_file_name(x_agenda._owner_id)
        save_file(self.roles_dir(), x_file_name, x_agenda.get_json())

    def save_job_agenda(self, x_agenda: AgendaUnit):
        x_file_name = self.owner_file_name(x_agenda._owner_id)
        save_file(self.jobs_dir(), x_file_name, x_agenda.get_json())

    def save_duty_agenda(self, x_agenda: AgendaUnit):
        if x_agenda._owner_id != self.person_id:
            raise Invalid_duty_Exception(
                f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{self.person_id}''s duty agenda."
            )
        self.save_file_duty(x_agenda.get_json(), True)

    def save_work_agenda(self, x_agenda: AgendaUnit):
        if x_agenda._owner_id != self.person_id:
            raise Invalid_work_Exception(
                f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{self.person_id}''s work agenda."
            )
        self.save_file_work(x_agenda.get_json(), True)

    def role_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.role_path(owner_id))

    def job_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.job_path(owner_id))

    def get_role_agenda(self, owner_id: PersonID) -> AgendaUnit:
        if self.role_file_exists(owner_id) == False:
            return None
        file_content = open_file(self.roles_dir(), self.owner_file_name(owner_id))
        return agendaunit_get_from_json(file_content)

    def get_job_agenda(self, owner_id: PersonID) -> AgendaUnit:
        file_content = open_file(self.jobs_dir(), self.owner_file_name(owner_id))
        return agendaunit_get_from_json(file_content)

    def get_duty_agenda(self) -> AgendaUnit:
        file_content = self.open_file_duty()
        return agendaunit_get_from_json(file_content)

    def get_work_agenda(self) -> AgendaUnit:
        file_content = self.open_file_work()
        return agendaunit_get_from_json(file_content)

    def delete_role_file(self, owner_id: PersonID):
        delete_dir(self.role_path(owner_id))

    def delete_job_file(self, owner_id: PersonID):
        delete_dir(self.job_path(owner_id))

    def set_nox_type(self, nox_type: str):
        if nox_type is None or nox_type in get_nox_type_set():
            self._nox_type = nox_type
        else:
            raise Invalid_nox_type_Exception(f"'{nox_type}' is an invalid nox_type")

    def speaker_dir(self, x_person_id: PersonID = None, x_econ_path: RoadUnit = None):
        if self._nox_type == pipeline_role_job_text():
            return self.jobs_dir()
        if self._nox_type == pipeline_duty_work_text():
            speaker_usernox = usernox_shop(
                reals_dir=self.reals_dir,
                real_id=self.real_id,
                person_id=x_person_id,
                road_delimiter=self._road_delimiter,
                planck=self._planck,
            )
            return speaker_usernox.work_dir()
        if self._nox_type == pipeline_job_work_text():
            speaker_agendahub = agendahub_shop(
                reals_dir=self.reals_dir,
                real_id=self.real_id,
                person_id=x_person_id,
                econ_road=x_econ_path,
                road_delimiter=self._road_delimiter,
                planck=self._planck,
            )
            return speaker_agendahub.jobs_dir()

    def speaker_file_name(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return get_file_name(x_arg)
        if self._nox_type == pipeline_duty_work_text():
            return get_file_name(self.person_id)
        if self._nox_type == pipeline_job_work_text():
            return get_file_name(self.person_id)

    def listener_dir(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return self.roles_dir()
        if self._nox_type == pipeline_duty_work_text():
            return self.duty_dir()
        if self._nox_type == pipeline_job_work_text():
            return self.duty_dir()

    def listener_file_name(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return get_file_name(x_arg)
        if self._nox_type == pipeline_duty_work_text():
            return get_file_name(self.person_id)
        if self._nox_type == pipeline_job_work_text():
            return get_file_name(self.person_id)

    def destination_dir(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return self.jobs_dir()
        if self._nox_type == pipeline_duty_work_text():
            return self.work_dir()
        if self._nox_type == pipeline_job_work_text():
            return self.work_dir()

    def destination_file_name(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return get_file_name(x_arg)
        if self._nox_type == pipeline_duty_work_text():
            return get_file_name(self.person_id)
        if self._nox_type == pipeline_job_work_text():
            return get_file_name(self.person_id)

    def get_speaker_agenda(
        self, person_id: PersonID, return_None_if_missing: bool = True
    ) -> AgendaUnit:
        speaker_dir = self.speaker_dir(person_id)
        speaker_file_name = self.speaker_file_name(person_id)
        x_file_path = f"{speaker_dir}/{speaker_file_name}"
        if os_path_exists(x_file_path) or not return_None_if_missing:
            file_contents = open_file(speaker_dir, speaker_file_name)
            return agendaunit_get_from_json(file_contents)
        else:
            None

    def get_listener_agenda(self, person_id: PersonID) -> AgendaUnit:
        listener_dir = self.listener_dir(person_id)
        listener_file_name = self.listener_file_name(person_id)
        x_file_path = f"{listener_dir}/{listener_file_name}"
        if os_path_exists(x_file_path):
            file_contents = open_file(listener_dir, listener_file_name)
            return agendaunit_get_from_json(file_contents)
        else:
            None


def agendahub_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID,
    econ_road: RoadUnit,
    nox_type: str = None,
    road_delimiter: str = None,
    planck: float = None,
) -> AgendaHub:
    x_usernox = usernox_shop(
        reals_dir=reals_dir,
        real_id=real_id,
        person_id=person_id,
        road_delimiter=road_delimiter,
        planck=planck,
    )
    x_agendahub = AgendaHub(
        reals_dir=x_usernox.reals_dir,
        real_id=x_usernox.real_id,
        person_id=x_usernox.person_id,
        econ_road=econ_road,
        _road_delimiter=x_usernox._road_delimiter,
        _planck=x_usernox._planck,
    )
    x_agendahub.set_nox_type(nox_type)
    return x_agendahub
