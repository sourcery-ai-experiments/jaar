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
    real_dir: str = None
    reals_dir: str = None
    real_id: str = None
    persons_dir: str = None
    person_dir: str = None
    _econs_dir: str = None
    _atoms_dir: str = None
    _changes_dir: str = None
    _duty_file_name: str = None
    _duty_path: str = None
    _work_file_name: str = None
    _work_path: str = None
    _road_delimiter: str = None
    _planck: float = None


def userdir_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID,
    road_delimiter: str = None,
    planck: float = None,
) -> UserDir:
    planck = default_planck_if_none(planck)
    if reals_dir is None:
        reals_dir = get_test_reals_dir()
    if real_id is None:
        real_id = get_test_real_id()
    road_delimiter = default_road_delimiter_if_none(road_delimiter)
    real_dir = f"{reals_dir}/{real_id}"
    persons_dir = f"{real_dir}/persons"
    person_id = validate_roadnode(person_id, road_delimiter)
    person_dir = f"{persons_dir}/{person_id}"
    econs_dir = f"{person_dir}/econs"
    atoms_dir = f"{person_dir}/atoms"
    changes_dir = f"{person_dir}/{get_changes_folder()}"
    duty_file_name = f"{duty_str()}.json"
    duty_path = f"{person_dir}/{duty_file_name}"
    work_file_name = f"{work_str()}.json"
    work_path = f"{person_dir}/{work_file_name}"

    return UserDir(
        person_id=person_id,
        real_id=real_id,
        real_dir=real_dir,
        reals_dir=reals_dir,
        persons_dir=persons_dir,
        person_dir=person_dir,
        _econs_dir=econs_dir,
        _atoms_dir=atoms_dir,
        _changes_dir=changes_dir,
        _duty_file_name=duty_file_name,
        _duty_path=duty_path,
        _work_file_name=work_file_name,
        _work_path=work_path,
        _road_delimiter=road_delimiter,
        _planck=planck,
    )


def get_econ_path(x_userdir: UserDir, x_road: RoadNode) -> str:
    econ_root = get_rootpart_of_econ_dir()
    x_road = rebuild_road(x_road, x_userdir.real_id, econ_root)
    x_list = get_all_road_nodes(x_road, x_userdir._road_delimiter)
    return f"{x_userdir._econs_dir}{get_directory_path(x_list=[*x_list])}"
