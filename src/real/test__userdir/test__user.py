from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_planck_if_none
from src.agenda.agenda import duty_str, work_str
from src.real.userdir import UserDir, userdir_shop
from src.real.change import get_changes_folder
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_UserDir_Exists():
    # GIVEN / WHEN
    x_userdir = UserDir()

    # THEN
    assert x_userdir.person_id is None
    assert x_userdir.real_id is None
    assert x_userdir.real_dir is None
    assert x_userdir.reals_dir is None
    assert x_userdir.persons_dir is None
    assert x_userdir.person_dir is None
    assert x_userdir._econs_dir is None
    assert x_userdir._atoms_dir is None
    assert x_userdir._changes_dir is None
    assert x_userdir._duty_file_name is None
    assert x_userdir._duty_path is None
    assert x_userdir._work_file_name is None
    assert x_userdir._work_path is None
    assert x_userdir._road_delimiter is None
    assert x_userdir._planck is None


def test_userdir_shop_ReturnsCorrectObj():
    # GIVEN
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    sue_text = "Sue"
    x_road_delimiter = "/"
    x_planck = 3

    # WHEN
    x_userdir = userdir_shop(
        x_reals_dir, x_real_id, sue_text, x_road_delimiter, x_planck
    )

    # THEN
    assert x_userdir.real_dir == f"{x_reals_dir}/{x_real_id}"
    assert x_userdir.persons_dir == f"{x_userdir.real_dir}/persons"
    assert x_userdir.person_id == sue_text
    assert x_userdir.person_dir == f"{x_userdir.persons_dir}/{sue_text}"
    assert x_userdir._econs_dir == f"{x_userdir.person_dir}/econs"
    assert x_userdir._atoms_dir == f"{x_userdir.person_dir}/atoms"
    assert x_userdir._changes_dir == f"{x_userdir.person_dir}/{get_changes_folder()}"
    assert x_userdir._duty_file_name == f"{duty_str()}.json"
    x_duty_path = f"{x_userdir.person_dir}/{x_userdir._duty_file_name}"
    assert x_userdir._duty_path == x_duty_path
    assert x_userdir._work_file_name == f"{work_str()}.json"
    x_workpath = f"{x_userdir.person_dir}/{x_userdir._work_file_name}"
    assert x_userdir._work_path == x_workpath
    assert x_userdir._road_delimiter == x_road_delimiter
    assert x_userdir._planck == x_planck


def test_userdir_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"

    # WHEN
    sue_userdir = userdir_shop(None, None, sue_text)

    # THEN
    assert sue_userdir.real_dir == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_userdir.persons_dir == f"{sue_userdir.real_dir}/persons"
    assert sue_userdir.person_id == sue_text
    assert sue_userdir.person_dir == f"{sue_userdir.persons_dir}/{sue_text}"
    assert sue_userdir._econs_dir == f"{sue_userdir.person_dir}/econs"
    assert sue_userdir._atoms_dir == f"{sue_userdir.person_dir}/atoms"
    assert (
        sue_userdir._changes_dir == f"{sue_userdir.person_dir}/{get_changes_folder()}"
    )
    assert sue_userdir._duty_file_name == f"{duty_str()}.json"
    x_duty_path = f"{sue_userdir.person_dir}/{sue_userdir._duty_file_name}"
    assert sue_userdir._duty_path == x_duty_path
    assert sue_userdir._work_file_name == f"{work_str()}.json"
    x_workpath = f"{sue_userdir.person_dir}/{sue_userdir._work_file_name}"
    assert sue_userdir._work_path == x_workpath
    assert sue_userdir._road_delimiter == default_road_delimiter_if_none()
    assert sue_userdir._planck == default_planck_if_none()


def test_userdir_shop_RaisesErrorIf_person_id_Contains_road_delimiter():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        userdir_shop(None, None, person_id=bob_text, road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )
