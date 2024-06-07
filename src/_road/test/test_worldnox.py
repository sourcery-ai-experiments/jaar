from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_planck_if_none
from src._road.worldnox import RealNox, realnox_shop, UserNox, usernox_shop
from src._road.jaar_config import (
    get_changes_folder,
    duty_str,
    work_str,
    get_test_reals_dir,
    get_test_real_id,
)
from src._road.examples.road_env import env_dir_setup_cleanup, get_road_temp_env_dir
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_RealNox_Exists():
    # GIVEN / WHEN
    x_realnox = RealNox()

    # THEN
    assert x_realnox.reals_dir is None
    assert x_realnox.real_id is None
    assert x_realnox._road_delimiter is None
    assert x_realnox._planck is None


def test_realnox_shop_ReturnsCorrectObj():
    # GIVEN
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    x_road_delimiter = "/"
    x_planck = 3

    # WHEN
    x_realnox = realnox_shop(x_reals_dir, x_real_id, x_road_delimiter, x_planck)

    # THEN
    assert x_realnox.reals_dir == x_reals_dir
    assert x_realnox.real_id == x_real_id
    assert x_realnox._road_delimiter == x_road_delimiter
    assert x_realnox._planck == x_planck

    assert x_realnox.real_dir() == f"{x_reals_dir}/{x_real_id}"

    sue_text = "Sue"
    sue_real_dir = f"{x_realnox.real_dir()}/persons"
    sue_dir_dir = f"{x_realnox.persons_dir()}/{sue_text}"
    sue_econs_dir = f"{x_realnox.person_dir(sue_text)}/econs"
    sue_atoms_dir = f"{x_realnox.person_dir(sue_text)}/atoms"
    sue_changes_dir = f"{x_realnox.person_dir(sue_text)}/{get_changes_folder()}"
    sue_person_dir = x_realnox.person_dir(sue_text)
    sue_duty_path = f"{sue_person_dir}/{x_realnox.duty_file_name(sue_text)}"
    sue_work_path = f"{sue_person_dir}/{x_realnox.work_file_name(sue_text)}"

    assert x_realnox.persons_dir() == sue_real_dir
    assert x_realnox.person_dir(sue_text) == sue_dir_dir
    assert x_realnox.econs_dir(sue_text) == sue_econs_dir
    assert x_realnox.atoms_dir(sue_text) == sue_atoms_dir
    assert x_realnox.changes_dir(sue_text) == sue_changes_dir
    assert x_realnox.duty_file_name(sue_text) == f"{sue_text}.json"
    assert x_realnox.duty_path(sue_text) == sue_duty_path
    assert x_realnox.work_file_name(sue_text) == f"{sue_text}.json"
    assert x_realnox.work_path(sue_text) == sue_work_path


def test_realnox_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"

    # WHEN
    sue_realnox = realnox_shop(None, None)

    # THEN
    assert sue_realnox.reals_dir == get_test_reals_dir()
    assert sue_realnox.real_id == get_test_real_id()
    assert sue_realnox.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_realnox._road_delimiter == default_road_delimiter_if_none()
    assert sue_realnox._planck == default_planck_if_none()

    sue_text = "Sue"
    sue_person_dir = f"{sue_realnox.persons_dir()}/{sue_text}"
    sue_econs_dir = f"{sue_realnox.person_dir(sue_text)}/econs"
    sue_atoms_dir = f"{sue_realnox.person_dir(sue_text)}/atoms"
    sue_duty_dir = f"{sue_realnox.person_dir(sue_text)}/duty"
    sue_work_dir = f"{sue_realnox.person_dir(sue_text)}/work"
    x_changes_dir = f"{sue_realnox.person_dir(sue_text)}/{get_changes_folder()}"
    x_duty_path = f"{sue_person_dir}/{sue_realnox.duty_file_name(sue_text)}"
    x_workpath = f"{sue_person_dir}/{sue_realnox.work_file_name(sue_text)}"
    assert sue_realnox.persons_dir() == f"{sue_realnox.real_dir()}/persons"
    assert sue_realnox.person_dir(sue_text) == sue_person_dir
    assert sue_realnox.econs_dir(sue_text) == sue_econs_dir
    assert sue_realnox.atoms_dir(sue_text) == sue_atoms_dir
    assert sue_realnox.duty_dir(sue_text) == sue_duty_dir
    assert sue_realnox.work_dir(sue_text) == sue_work_dir
    assert sue_realnox.changes_dir(sue_text) == x_changes_dir
    assert sue_realnox.duty_file_name(sue_text) == f"{sue_text}.json"
    assert sue_realnox.duty_path(sue_text) == x_duty_path
    assert sue_realnox.work_file_name(sue_text) == f"{sue_text}.json"
    assert sue_realnox.work_path(sue_text) == x_workpath


def test_RealNox_save_file_duty_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realnox = realnox_shop(get_road_temp_env_dir(), None)
    assert os_path_exists(sue_realnox.duty_path(sue_text)) == False

    # WHEN
    sue_realnox.save_file_duty(sue_text, file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_realnox.duty_path(sue_text))
    with open(sue_realnox.duty_path(sue_text), "r") as file:
        assert file.read() == "fooboo"


def test_RealNox_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realnox = realnox_shop(get_road_temp_env_dir(), None)
    assert sue_realnox.duty_file_exists(sue_text) == False

    # WHEN
    sue_realnox.save_file_duty(sue_text, file_text="fooboo", replace=True)

    # THEN
    assert sue_realnox.duty_file_exists(sue_text)


def test_RealNox_open_file_duty_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realnox = realnox_shop(get_road_temp_env_dir(), None)
    example_text = "fooboo"
    sue_realnox.save_file_duty(sue_text, example_text, replace=True)

    # WHEN / THEN
    assert sue_realnox.open_file_duty(sue_text) == example_text


def test_RealNox_save_file_work_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realnox = realnox_shop(get_road_temp_env_dir(), None)
    assert os_path_exists(sue_realnox.work_path(sue_text)) == False

    # WHEN
    sue_realnox.save_file_work(sue_text, file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_realnox.work_path(sue_text))


def test_RealNox_work_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realnox = realnox_shop(get_road_temp_env_dir(), None)
    assert sue_realnox.work_file_exists(sue_text) == False

    # WHEN
    sue_realnox.save_file_work(sue_text, file_text="fooboo", replace=True)

    # THEN
    assert sue_realnox.work_file_exists(sue_text)


def test_RealNox_open_file_work_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realnox = realnox_shop(get_road_temp_env_dir(), None)
    example_text = "fooboo"
    sue_realnox.save_file_work(sue_text, example_text, replace=True)

    # WHEN / THEN
    assert sue_realnox.open_file_work(sue_text) == example_text


def test_UserNox_Exists():
    # GIVEN / WHEN
    x_usernox = UserNox()

    # THEN
    assert x_usernox.reals_dir is None
    assert x_usernox.real_id is None
    assert x_usernox.person_id is None
    assert x_usernox._road_delimiter is None
    assert x_usernox._planck is None


def test_usernox_shop_ReturnsCorrectObj():
    # GIVEN
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    sue_text = "Sue"
    x_road_delimiter = "/"
    x_planck = 3

    # WHEN
    x_usernox = usernox_shop(
        x_reals_dir, x_real_id, sue_text, x_road_delimiter, x_planck
    )

    # THEN
    assert x_usernox.reals_dir == x_reals_dir
    assert x_usernox.real_id == x_real_id
    assert x_usernox.person_id == sue_text
    assert x_usernox._road_delimiter == x_road_delimiter
    assert x_usernox._planck == x_planck

    assert x_usernox.real_dir() == f"{x_reals_dir}/{x_real_id}"
    assert x_usernox.persons_dir() == f"{x_usernox.real_dir()}/persons"
    assert x_usernox.person_dir() == f"{x_usernox.persons_dir()}/{sue_text}"
    assert x_usernox.econs_dir() == f"{x_usernox.person_dir()}/econs"
    assert x_usernox.atoms_dir() == f"{x_usernox.person_dir()}/atoms"
    assert x_usernox.duty_dir() == f"{x_usernox.person_dir()}/duty"
    assert x_usernox.work_dir() == f"{x_usernox.person_dir()}/work"
    assert x_usernox.changes_dir() == f"{x_usernox.person_dir()}/{get_changes_folder()}"
    assert x_usernox.duty_file_name() == f"{sue_text}.json"
    x_duty_path = f"{x_usernox.duty_dir()}/{x_usernox.duty_file_name()}"
    assert x_usernox.duty_path() == x_duty_path
    assert x_usernox.work_file_name() == f"{sue_text}.json"
    x_workpath = f"{x_usernox.work_dir()}/{x_usernox.work_file_name()}"
    assert x_usernox.work_path() == x_workpath


def test_usernox_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"

    # WHEN
    sue_usernox = usernox_shop(None, None, sue_text)

    # THEN
    assert sue_usernox.reals_dir == get_test_reals_dir()
    assert sue_usernox.real_id == get_test_real_id()
    assert sue_usernox.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_usernox.person_id == sue_text
    assert sue_usernox._road_delimiter == default_road_delimiter_if_none()
    assert sue_usernox._planck == default_planck_if_none()
    assert sue_usernox.persons_dir() == f"{sue_usernox.real_dir()}/persons"
    assert sue_usernox.person_dir() == f"{sue_usernox.persons_dir()}/{sue_text}"
    assert sue_usernox.econs_dir() == f"{sue_usernox.person_dir()}/econs"
    assert sue_usernox.atoms_dir() == f"{sue_usernox.person_dir()}/atoms"
    x_changes_dir = f"{sue_usernox.person_dir()}/{get_changes_folder()}"
    assert sue_usernox.changes_dir() == x_changes_dir
    assert sue_usernox.duty_file_name() == f"{sue_text}.json"
    x_duty_path = f"{sue_usernox.duty_dir()}/{sue_usernox.duty_file_name()}"
    assert sue_usernox.duty_path() == x_duty_path
    assert sue_usernox.work_file_name() == f"{sue_text}.json"
    x_workpath = f"{sue_usernox.work_dir()}/{sue_usernox.work_file_name()}"
    assert sue_usernox.work_path() == x_workpath


def test_usernox_shop_RaisesErrorIf_person_id_Contains_road_delimiter():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        usernox_shop(None, None, person_id=bob_text, road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_UserNox_save_file_duty_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_usernox = usernox_shop(get_road_temp_env_dir(), None, sue_text)
    assert os_path_exists(sue_usernox.duty_path()) == False

    # WHEN
    sue_usernox.save_file_duty(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_usernox.duty_path())


def test_UserNox_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_usernox = usernox_shop(get_road_temp_env_dir(), None, sue_text)
    assert sue_usernox.duty_file_exists() == False

    # WHEN
    sue_usernox.save_file_duty(file_text="fooboo", replace=True)

    # THEN
    assert sue_usernox.duty_file_exists()


def test_UserNox_open_file_duty_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_usernox = usernox_shop(get_road_temp_env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_usernox.save_file_duty(example_text, replace=True)

    # WHEN / THEN
    assert sue_usernox.open_file_duty() == example_text


def test_UserNox_save_file_work_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_usernox = usernox_shop(get_road_temp_env_dir(), None, sue_text)
    assert os_path_exists(sue_usernox.work_path()) == False

    # WHEN
    sue_usernox.save_file_work(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_usernox.work_path())


def test_UserNox_work_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_usernox = usernox_shop(get_road_temp_env_dir(), None, sue_text)
    assert sue_usernox.work_file_exists() == False

    # WHEN
    sue_usernox.save_file_work(file_text="fooboo", replace=True)

    # THEN
    assert sue_usernox.work_file_exists()


def test_UserNox_open_file_work_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_usernox = usernox_shop(get_road_temp_env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_usernox.save_file_work(example_text, replace=True)

    # WHEN / THEN
    assert sue_usernox.open_file_work() == example_text
