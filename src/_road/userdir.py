from src._instrument.file import get_directory_path
from src._road.finance import default_planck_if_none
from src._road.road import (
    default_road_delimiter_if_none,
    PersonID,
    RealID,
    validate_roadnode,
    RoadNode,
    rebuild_road,
    get_all_road_nodes,
)
from src._road.jaar_config import (
    get_changes_folder,
    duty_str,
    work_str,
    get_test_reals_dir,
    get_test_real_id,
    get_rootpart_of_econ_dir,
)
from dataclasses import dataclass


@dataclass
class UserDir:
    person_id: PersonID = None
    reals_dir: str = None
    real_id: str = None
    _road_delimiter: str = None
    _planck: float = None
    # real_dir: str = None
    # persons_dir: str = None
    # person_dir: str = None
    # econs_dir: str = None
    # atoms_dir: str = None
    # changes_dir: str = None
    # duty_file_name: str = None
    # duty_path: str = None
    # work_file_name: str = None
    # work_path: str = None

    # road_delimiter = default_road_delimiter_if_none(road_delimiter)
    # real_dir = f"{reals_dir}/{real_id}"
    # persons_dir = f"{real_dir}/persons"
    # person_id = validate_roadnode(person_id, road_delimiter)
    # person_dir = f"{persons_dir}/{person_id}"
    # econs_dir = f"{person_dir}/econs"
    # atoms_dir = f"{person_dir}/atoms"
    # changes_dir = f"{person_dir}/{get_changes_folder()}"
    # duty_file_name = f"{duty_str()}.json"
    # duty_path = f"{person_dir}/{duty_file_name}"
    # work_file_name = f"{work_str()}.json"
    # work_path = f"{person_dir}/{work_file_name}"

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
