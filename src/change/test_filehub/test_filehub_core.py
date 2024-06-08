from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_planck_if_none
from src._road.jaar_config import (
    get_changes_folder,
    duty_str,
    work_str,
    get_test_reals_dir,
    get_test_real_id,
)
from src._road.examples.road_env import env_dir_setup_cleanup, get_road_temp_env_dir
from src.change.filehub import FileHub, filehub_shop
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_FileHub_Exists():
    # GIVEN / WHEN
    x_filehub = FileHub()

    # THEN
    assert x_filehub.reals_dir is None
    assert x_filehub.real_id is None
    assert x_filehub.person_id is None
    assert x_filehub.road_delimiter is None
    assert x_filehub.planck is None


def test_filehub_shop_ReturnsCorrectObj():
    # GIVEN
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    sue_text = "Sue"
    x_road_delimiter = "/"
    x_planck = 3

    # WHEN
    x_filehub = filehub_shop(
        x_reals_dir, x_real_id, sue_text, None, None, x_road_delimiter, x_planck
    )

    # THEN
    assert x_filehub.reals_dir == x_reals_dir
    assert x_filehub.real_id == x_real_id
    assert x_filehub.person_id == sue_text
    assert x_filehub.road_delimiter == x_road_delimiter
    assert x_filehub.planck == x_planck

    assert x_filehub.real_dir() == f"{x_reals_dir}/{x_real_id}"
    assert x_filehub.persons_dir() == f"{x_filehub.real_dir()}/persons"
    assert x_filehub.person_dir() == f"{x_filehub.persons_dir()}/{sue_text}"
    assert x_filehub.econs_dir() == f"{x_filehub.person_dir()}/econs"
    assert x_filehub.atoms_dir() == f"{x_filehub.person_dir()}/atoms"
    assert x_filehub.duty_dir() == f"{x_filehub.person_dir()}/duty"
    assert x_filehub.work_dir() == f"{x_filehub.person_dir()}/work"
    assert x_filehub.changes_dir() == f"{x_filehub.person_dir()}/{get_changes_folder()}"
    assert x_filehub.duty_file_name() == f"{sue_text}.json"
    x_duty_file_path = f"{x_filehub.duty_dir()}/{x_filehub.duty_file_name()}"
    assert x_filehub.duty_file_path() == x_duty_file_path
    assert x_filehub.work_file_name() == f"{sue_text}.json"
    x_workpath = f"{x_filehub.work_dir()}/{x_filehub.work_file_name()}"
    assert x_filehub.work_path() == x_workpath


def test_filehub_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"

    # WHEN
    sue_filehub = filehub_shop(None, None, sue_text)

    # THEN
    assert sue_filehub.reals_dir == get_test_reals_dir()
    assert sue_filehub.real_id == get_test_real_id()
    assert sue_filehub.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_filehub.person_id == sue_text
    assert sue_filehub.road_delimiter == default_road_delimiter_if_none()
    assert sue_filehub.planck == default_planck_if_none()
    assert sue_filehub.persons_dir() == f"{sue_filehub.real_dir()}/persons"
    assert sue_filehub.person_dir() == f"{sue_filehub.persons_dir()}/{sue_text}"
    assert sue_filehub.econs_dir() == f"{sue_filehub.person_dir()}/econs"
    assert sue_filehub.atoms_dir() == f"{sue_filehub.person_dir()}/atoms"
    x_changes_dir = f"{sue_filehub.person_dir()}/{get_changes_folder()}"
    assert sue_filehub.changes_dir() == x_changes_dir
    assert sue_filehub.duty_file_name() == f"{sue_text}.json"
    x_duty_file_path = f"{sue_filehub.duty_dir()}/{sue_filehub.duty_file_name()}"
    assert sue_filehub.duty_file_path() == x_duty_file_path
    assert sue_filehub.work_file_name() == f"{sue_text}.json"
    x_workpath = f"{sue_filehub.work_dir()}/{sue_filehub.work_file_name()}"
    assert sue_filehub.work_path() == x_workpath


def test_filehub_shop_RaisesErrorIf_person_id_Contains_road_delimiter():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        filehub_shop(None, None, person_id=bob_text, road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_FileHub_save_file_duty_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(get_road_temp_env_dir(), None, sue_text)
    assert os_path_exists(sue_filehub.duty_file_path()) == False

    # WHEN
    sue_filehub.save_file_duty(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_filehub.duty_file_path())


def test_FileHub_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(get_road_temp_env_dir(), None, sue_text)
    assert sue_filehub.duty_file_exists() == False

    # WHEN
    sue_filehub.save_file_duty(file_text="fooboo", replace=True)

    # THEN
    assert sue_filehub.duty_file_exists()


def test_FileHub_open_file_duty_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(get_road_temp_env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_filehub.save_file_duty(example_text, replace=True)

    # WHEN / THEN
    assert sue_filehub.open_file_duty() == example_text


def test_FileHub_save_file_work_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(get_road_temp_env_dir(), None, sue_text)
    assert os_path_exists(sue_filehub.work_path()) == False

    # WHEN
    sue_filehub.save_file_work(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_filehub.work_path())


def test_FileHub_work_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(get_road_temp_env_dir(), None, sue_text)
    assert sue_filehub.work_file_exists() == False

    # WHEN
    sue_filehub.save_file_work(file_text="fooboo", replace=True)

    # THEN
    assert sue_filehub.work_file_exists()


def test_FileHub_open_file_work_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(get_road_temp_env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_filehub.save_file_work(example_text, replace=True)

    # WHEN / THEN
    assert sue_filehub.open_file_work() == example_text
