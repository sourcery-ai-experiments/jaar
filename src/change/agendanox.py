from src._instrument.file import get_directory_path, save_file, open_file
from src._road.finance import default_planck_if_none
from src._road.road import (
    default_road_delimiter_if_none,
    PersonID,
    RealID,
    validate_roadnode,
    RoadNode,
    RoadUnit,
    rebuild_road,
    get_all_road_nodes,
)
from src._road.jaar_config import (
    get_changes_folder,
    duty_str,
    work_str,
    roles_str,
    jobs_str,
    get_test_reals_dir,
    get_test_real_id,
    get_rootpart_of_econ_dir,
)
from src._road.worldnox import UserNox, usernox_shop, get_file_name
from os.path import exists as os_path_exists
from dataclasses import dataclass


def get_econ_path(x_usernox: UserNox, x_road: RoadNode) -> str:
    econ_root = get_rootpart_of_econ_dir()
    x_road = rebuild_road(x_road, x_usernox.real_id, econ_root)
    x_list = get_all_road_nodes(x_road, x_usernox._road_delimiter)
    return f"{x_usernox.econs_dir()}{get_directory_path(x_list=[*x_list])}"


def get_econ_roles_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{roles_str()}"


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{jobs_str()}"


@dataclass
class AgendaNox(UserNox):
    econ_road: RoadUnit = None

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

    # role delete
    # job delete


def agendanox_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID,
    econ_road: RoadUnit,
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
    return AgendaNox(
        reals_dir=x_usernox.reals_dir,
        real_id=x_usernox.real_id,
        person_id=x_usernox.person_id,
        econ_road=econ_road,
        _road_delimiter=x_usernox._road_delimiter,
        _planck=x_usernox._planck,
    )
