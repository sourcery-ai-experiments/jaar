from src._instrument.file import get_directory_path, save_file, open_file
from src._road.road import (
    PersonID,
    RealID,
    RoadNode,
    RoadUnit,
    rebuild_road,
    get_all_road_nodes,
)
from src._road.jaar_config import (
    duty_str,
    work_str,
    roles_str,
    jobs_str,
    get_rootpart_of_econ_dir,
)
from src._road.worldnox import UserNox, usernox_shop, get_file_name
from src.agenda.agenda import AgendaUnit, get_from_json as agendaunit_get_from_json
from os.path import exists as os_path_exists
from dataclasses import dataclass


class Invalid_nox_type_Exception(Exception):
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
class AgendaNox(UserNox):
    econ_road: RoadUnit = None
    _nox_type: str = None  # can be "duty_work", "role_job", "job_work"

    def econ_dir(self) -> str:
        return get_econ_path(self, self.econ_road)

    def owner_file_name(self, owner_id: PersonID) -> str:
        return get_file_name(owner_id)

    def role_path(self, owner_id: PersonID) -> str:
        return f"{self.roles_dir()}/{self.owner_file_name(owner_id)}"

    def job_path(self, owner_id: PersonID) -> str:
        return f"{self.jobs_dir()}/{self.owner_file_name(owner_id)}"

    def roles_dir(self) -> str:
        return get_econ_roles_dir(self.econ_dir())

    def jobs_dir(self) -> str:
        return get_econ_jobs_dir(self.econ_dir())

    def save_file_role(self, owner_id: PersonID, file_text: str, replace: bool):
        save_file(
            dest_dir=self.roles_dir(),
            file_name=self.owner_file_name(owner_id),
            file_text=file_text,
            replace=replace,
        )

    def save_file_job(self, owner_id: PersonID, file_text: str, replace: bool):
        save_file(
            dest_dir=self.jobs_dir(),
            file_name=self.owner_file_name(owner_id),
            file_text=file_text,
            replace=replace,
        )

    def role_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.role_path(owner_id))

    def job_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.job_path(owner_id))

    def open_file_role(self, owner_id: PersonID) -> str:
        return open_file(self.roles_dir(), self.owner_file_name(owner_id))

    def open_file_job(self, owner_id: PersonID) -> str:
        return open_file(self.jobs_dir(), self.owner_file_name(owner_id))

    def set_nox_type(self, nox_type: str):
        if nox_type is None or nox_type in get_nox_type_set():
            self._nox_type = nox_type
        else:
            raise Invalid_nox_type_Exception(f"'{nox_type}' is an invalid nox_type")

    def speaker_dir(self, x_person_id: PersonID = None):
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
            return speaker_usernox.person_dir()

    def speaker_file_name(self, person_id: PersonID = None):
        if self._nox_type == pipeline_role_job_text():
            return get_file_name(person_id)
        if self._nox_type == pipeline_duty_work_text():
            return get_file_name(work_str())

    def listener_dir(self, x_person_id: PersonID = None):
        if self._nox_type == pipeline_role_job_text():
            return self.roles_dir()
        if self._nox_type == pipeline_duty_work_text():
            return self.person_dir()

    def listener_file_name(self, person_id: PersonID = None):
        if self._nox_type == pipeline_role_job_text():
            return get_file_name(person_id)
        if self._nox_type == pipeline_duty_work_text():
            return get_file_name(duty_str())

    def destination_dir(self, person_id: PersonID = None):
        if self._nox_type == pipeline_role_job_text():
            return self.jobs_dir()
        if self._nox_type == pipeline_duty_work_text():
            return self.person_dir()

    def destination_file_name(self, person_id: PersonID = None):
        if self._nox_type == pipeline_role_job_text():
            return get_file_name(person_id)
        if self._nox_type == pipeline_duty_work_text():
            return get_file_name(work_str())

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


def agendanox_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID,
    econ_road: RoadUnit,
    nox_type: str = None,
    road_delimiter: str = None,
    planck: float = None,
) -> AgendaNox:
    x_usernox = usernox_shop(
        reals_dir=reals_dir,
        real_id=real_id,
        person_id=person_id,
        road_delimiter=road_delimiter,
        planck=planck,
    )
    x_agendanox = AgendaNox(
        reals_dir=x_usernox.reals_dir,
        real_id=x_usernox.real_id,
        person_id=x_usernox.person_id,
        econ_road=econ_road,
        _road_delimiter=x_usernox._road_delimiter,
        _planck=x_usernox._planck,
    )
    x_agendanox.set_nox_type(nox_type)
    return x_agendanox
