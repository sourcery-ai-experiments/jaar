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
    role_str,
    job_str,
    get_test_reals_dir,
    get_test_real_id,
    get_rootpart_of_econ_dir,
)
from os.path import exists as os_path_exists
from dataclasses import dataclass


@dataclass
class UserDir:
    person_id: PersonID = None
    reals_dir: str = None
    real_id: str = None
    _road_delimiter: str = None
    _planck: float = None

    def real_dir(self):
        return f"{self.reals_dir}/{self.real_id}"

    def persons_dir(self):
        return f"{self.real_dir()}/persons"

    def person_dir(self):
        return f"{self.persons_dir()}/{self.person_id}"

    def econs_dir(self):
        return f"{self.person_dir()}/econs"

    def atoms_dir(self):
        return f"{self.person_dir()}/atoms"

    def changes_dir(self):
        return f"{self.person_dir()}/{get_changes_folder()}"

    def duty_file_name(self):
        return f"{duty_str()}.json"

    def duty_path(self):
        return f"{self.person_dir()}/{self.duty_file_name()}"

    def work_file_name(self):
        return f"{work_str()}.json"

    def work_path(self):
        return f"{self.person_dir()}/{self.work_file_name()}"

    def save_file_duty(self, file_text: str, replace: bool):
        save_file(
            dest_dir=self.person_dir(),
            file_name=self.duty_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def save_file_work(self, file_text: str, replace: bool):
        save_file(
            dest_dir=self.person_dir(),
            file_name=self.work_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def duty_file_exists(self) -> bool:
        return os_path_exists(self.duty_path())

    def work_file_exists(self) -> bool:
        return os_path_exists(self.work_path())

    def open_file_duty(self):
        return open_file(self.person_dir(), self.duty_file_name())

    def open_file_work(self):
        return open_file(self.person_dir(), self.work_file_name())

    # duty delete
    # work delete


def userdir_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID,
    road_delimiter: str = None,
    planck: float = None,
) -> UserDir:
    if reals_dir is None:
        reals_dir = get_test_reals_dir()
    if real_id is None:
        real_id = get_test_real_id()

    return UserDir(
        person_id=validate_roadnode(person_id, road_delimiter),
        real_id=real_id,
        reals_dir=reals_dir,
        _road_delimiter=default_road_delimiter_if_none(road_delimiter),
        _planck=default_planck_if_none(planck),
    )


def get_econ_path(x_userdir: UserDir, x_road: RoadNode) -> str:
    econ_root = get_rootpart_of_econ_dir()
    x_road = rebuild_road(x_road, x_userdir.real_id, econ_root)
    x_list = get_all_road_nodes(x_road, x_userdir._road_delimiter)
    return f"{x_userdir.econs_dir()}{get_directory_path(x_list=[*x_list])}"


@dataclass
class EconDir(UserDir):
    econ_road: RoadUnit = None

    def econ_dir(self):
        return get_econ_path(self, self.econ_road)

    def role_file_name(self):
        return f"{role_str()}.json"

    def role_path(self) -> str:
        return f"{self.econ_dir()}/{self.role_file_name()}"

    def job_file_name(self):
        return f"{job_str()}.json"

    def job_path(self) -> str:
        return f"{self.econ_dir()}/{self.job_file_name()}"

    def save_file_role(self, file_text: str, replace: bool):
        save_file(
            dest_dir=self.econ_dir(),
            file_name=self.role_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def save_file_job(self, file_text: str, replace: bool):
        save_file(
            dest_dir=self.econ_dir(),
            file_name=self.job_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def role_file_exists(self) -> bool:
        return os_path_exists(self.role_path())

    def job_file_exists(self) -> bool:
        return os_path_exists(self.job_path())

    def open_file_role(self) -> str:
        return open_file(self.econ_dir(), self.role_file_name())

    def open_file_job(self) -> str:
        return open_file(self.econ_dir(), self.job_file_name())

    # role save
    # role delete
    # job save
    # job delete


def econdir_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID,
    econ_road: RoadUnit,
    road_delimiter: str = None,
    planck: float = None,
) -> EconDir:
    x_userdir = userdir_shop(
        reals_dir=reals_dir,
        real_id=real_id,
        person_id=person_id,
        road_delimiter=road_delimiter,
        planck=planck,
    )
    return EconDir(
        reals_dir=x_userdir.reals_dir,
        real_id=x_userdir.real_id,
        person_id=x_userdir.person_id,
        econ_road=econ_road,
        _road_delimiter=x_userdir._road_delimiter,
        _planck=x_userdir._planck,
    )
