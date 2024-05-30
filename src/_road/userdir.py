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
from os.path import exists as os_path_exists
from dataclasses import dataclass


@dataclass
class RealDir:
    reals_dir: str = None
    real_id: str = None
    _road_delimiter: str = None
    _planck: float = None

    def real_dir(self) -> str:
        return f"{self.reals_dir}/{self.real_id}"

    def persons_dir(self) -> str:
        return f"{self.real_dir()}/persons"

    def person_dir(self, person_id: PersonID) -> str:
        return f"{self.persons_dir()}/{person_id}"

    def econs_dir(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/econs"

    def atoms_dir(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/atoms"

    def changes_dir(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/{get_changes_folder()}"

    def duty_file_name(self):
        return f"{duty_str()}.json"

    def duty_path(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/{self.duty_file_name()}"

    def work_file_name(self):
        return f"{work_str()}.json"

    def work_path(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/{self.work_file_name()}"

    def save_file_duty(self, person_id: PersonID, file_text: str, replace: bool):
        save_file(
            dest_dir=self.person_dir(person_id),
            file_name=self.duty_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def save_file_work(self, person_id: PersonID, file_text: str, replace: bool):
        save_file(
            dest_dir=self.person_dir(person_id),
            file_name=self.work_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def duty_file_exists(self, person_id: PersonID) -> bool:
        return os_path_exists(self.duty_path(person_id))

    def work_file_exists(self, person_id: PersonID) -> bool:
        return os_path_exists(self.work_path(person_id))

    def open_file_duty(self, person_id: PersonID):
        return open_file(self.person_dir(person_id), self.duty_file_name())

    def open_file_work(self, person_id: PersonID):
        return open_file(self.person_dir(person_id), self.work_file_name())


def realdir_shop(
    reals_dir: str,
    real_id: RealID,
    road_delimiter: str = None,
    planck: float = None,
) -> RealDir:
    if reals_dir is None:
        reals_dir = get_test_reals_dir()
    if real_id is None:
        real_id = get_test_real_id()

    return RealDir(
        real_id=validate_roadnode(real_id, road_delimiter),
        reals_dir=reals_dir,
        _road_delimiter=default_road_delimiter_if_none(road_delimiter),
        _planck=default_planck_if_none(planck),
    )


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


def get_econ_roles_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{roles_str()}"


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{jobs_str()}"


@dataclass
class EconDir(UserDir):
    econ_road: RoadUnit = None

    def econ_dir(self) -> str:
        return get_econ_path(self, self.econ_road)

    def owner_file_name(self, owner_id: PersonID) -> str:
        return f"{owner_id}.json"

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
