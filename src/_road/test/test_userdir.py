from src._road.road import (
    default_road_delimiter_if_none,
    create_road_from_nodes,
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src._road.finance import default_planck_if_none
from src._road.userdir import (
    RealDir,
    realdir_shop,
    UserDir,
    userdir_shop,
    get_econ_path,
    EconDir,
    econdir_shop,
)
from src._road.jaar_config import (
    get_changes_folder,
    duty_str,
    work_str,
    get_test_reals_dir,
    get_test_real_id,
    get_rootpart_of_econ_dir,
)
from src._road.examples.road_env import (
    env_dir_setup_cleanup,
    get_road_temp_env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_RealDir_Exists():
    # GIVEN / WHEN
    x_realdir = RealDir()

    # THEN
    assert x_realdir.reals_dir is None
    assert x_realdir.real_id is None
    assert x_realdir._road_delimiter is None
    assert x_realdir._planck is None


def test_realdir_shop_ReturnsCorrectObj():
    # GIVEN
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    x_road_delimiter = "/"
    x_planck = 3

    # WHEN
    x_realdir = realdir_shop(x_reals_dir, x_real_id, x_road_delimiter, x_planck)

    # THEN
    assert x_realdir.reals_dir == x_reals_dir
    assert x_realdir.real_id == x_real_id
    assert x_realdir._road_delimiter == x_road_delimiter
    assert x_realdir._planck == x_planck

    assert x_realdir.real_dir() == f"{x_reals_dir}/{x_real_id}"

    sue_text = "Sue"
    sue_real_dir = f"{x_realdir.real_dir()}/persons"
    sue_dir_dir = f"{x_realdir.persons_dir()}/{sue_text}"
    sue_econs_dir = f"{x_realdir.person_dir(sue_text)}/econs"
    sue_atoms_dir = f"{x_realdir.person_dir(sue_text)}/atoms"
    sue_changes_dir = f"{x_realdir.person_dir(sue_text)}/{get_changes_folder()}"
    sue_duty_path = f"{x_realdir.person_dir(sue_text)}/{x_realdir.duty_file_name()}"
    sue_work_path = f"{x_realdir.person_dir(sue_text)}/{x_realdir.work_file_name()}"

    assert x_realdir.persons_dir() == sue_real_dir
    assert x_realdir.person_dir(sue_text) == sue_dir_dir
    assert x_realdir.econs_dir(sue_text) == sue_econs_dir
    assert x_realdir.atoms_dir(sue_text) == sue_atoms_dir
    assert x_realdir.changes_dir(sue_text) == sue_changes_dir
    assert x_realdir.duty_file_name() == f"{duty_str()}.json"
    assert x_realdir.duty_path(sue_text) == sue_duty_path
    assert x_realdir.work_file_name() == f"{work_str()}.json"
    assert x_realdir.work_path(sue_text) == sue_work_path


def test_realdir_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"

    # WHEN
    sue_realdir = realdir_shop(None, None)

    # THEN
    assert sue_realdir.reals_dir == get_test_reals_dir()
    assert sue_realdir.real_id == get_test_real_id()
    assert sue_realdir.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_realdir._road_delimiter == default_road_delimiter_if_none()
    assert sue_realdir._planck == default_planck_if_none()

    sue_text = "Sue"
    sue_person_dir = f"{sue_realdir.persons_dir()}/{sue_text}"
    sue_econs_dir = f"{sue_realdir.person_dir(sue_text)}/econs"
    sue_atoms_dir = f"{sue_realdir.person_dir(sue_text)}/atoms"
    x_changes_dir = f"{sue_realdir.person_dir(sue_text)}/{get_changes_folder()}"
    x_duty_path = f"{sue_realdir.person_dir(sue_text)}/{sue_realdir.duty_file_name()}"
    x_workpath = f"{sue_realdir.person_dir(sue_text)}/{sue_realdir.work_file_name()}"
    assert sue_realdir.persons_dir() == f"{sue_realdir.real_dir()}/persons"
    assert sue_realdir.person_dir(sue_text) == sue_person_dir
    assert sue_realdir.econs_dir(sue_text) == sue_econs_dir
    assert sue_realdir.atoms_dir(sue_text) == sue_atoms_dir
    assert sue_realdir.changes_dir(sue_text) == x_changes_dir
    assert sue_realdir.duty_file_name() == f"{duty_str()}.json"
    assert sue_realdir.duty_path(sue_text) == x_duty_path
    assert sue_realdir.work_file_name() == f"{work_str()}.json"
    assert sue_realdir.work_path(sue_text) == x_workpath


def test_RealDir_save_file_duty_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realdir = realdir_shop(get_road_temp_env_dir(), None)
    assert os_path_exists(sue_realdir.duty_path(sue_text)) == False

    # WHEN
    sue_realdir.save_file_duty(sue_text, file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_realdir.duty_path(sue_text))


def test_RealDir_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realdir = realdir_shop(get_road_temp_env_dir(), None)
    assert sue_realdir.duty_file_exists(sue_text) == False

    # WHEN
    sue_realdir.save_file_duty(sue_text, file_text="fooboo", replace=True)

    # THEN
    assert sue_realdir.duty_file_exists(sue_text)


def test_RealDir_open_file_duty_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realdir = realdir_shop(get_road_temp_env_dir(), None)
    example_text = "fooboo"
    sue_realdir.save_file_duty(sue_text, example_text, replace=True)

    # WHEN / THEN
    assert sue_realdir.open_file_duty(sue_text) == example_text


def test_RealDir_save_file_work_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realdir = realdir_shop(get_road_temp_env_dir(), None)
    assert os_path_exists(sue_realdir.work_path(sue_text)) == False

    # WHEN
    sue_realdir.save_file_work(sue_text, file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_realdir.work_path(sue_text))


def test_RealDir_work_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realdir = realdir_shop(get_road_temp_env_dir(), None)
    assert sue_realdir.work_file_exists(sue_text) == False

    # WHEN
    sue_realdir.save_file_work(sue_text, file_text="fooboo", replace=True)

    # THEN
    assert sue_realdir.work_file_exists(sue_text)


def test_RealDir_open_file_work_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_realdir = realdir_shop(get_road_temp_env_dir(), None)
    example_text = "fooboo"
    sue_realdir.save_file_work(sue_text, example_text, replace=True)

    # WHEN / THEN
    assert sue_realdir.open_file_work(sue_text) == example_text


def test_UserDir_Exists():
    # GIVEN / WHEN
    x_userdir = UserDir()

    # THEN
    assert x_userdir.reals_dir is None
    assert x_userdir.real_id is None
    assert x_userdir.person_id is None
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
    assert x_userdir.reals_dir == x_reals_dir
    assert x_userdir.real_id == x_real_id
    assert x_userdir.person_id == sue_text
    assert x_userdir._road_delimiter == x_road_delimiter
    assert x_userdir._planck == x_planck

    assert x_userdir.real_dir() == f"{x_reals_dir}/{x_real_id}"
    assert x_userdir.persons_dir() == f"{x_userdir.real_dir()}/persons"
    assert x_userdir.person_dir() == f"{x_userdir.persons_dir()}/{sue_text}"
    assert x_userdir.econs_dir() == f"{x_userdir.person_dir()}/econs"
    assert x_userdir.atoms_dir() == f"{x_userdir.person_dir()}/atoms"
    assert x_userdir.changes_dir() == f"{x_userdir.person_dir()}/{get_changes_folder()}"
    assert x_userdir.duty_file_name() == f"{duty_str()}.json"
    x_duty_path = f"{x_userdir.person_dir()}/{x_userdir.duty_file_name()}"
    assert x_userdir.duty_path() == x_duty_path
    assert x_userdir.work_file_name() == f"{work_str()}.json"
    x_workpath = f"{x_userdir.person_dir()}/{x_userdir.work_file_name()}"
    assert x_userdir.work_path() == x_workpath


def test_userdir_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"

    # WHEN
    sue_userdir = userdir_shop(None, None, sue_text)

    # THEN
    assert sue_userdir.reals_dir == get_test_reals_dir()
    assert sue_userdir.real_id == get_test_real_id()
    assert sue_userdir.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_userdir.person_id == sue_text
    assert sue_userdir._road_delimiter == default_road_delimiter_if_none()
    assert sue_userdir._planck == default_planck_if_none()
    assert sue_userdir.persons_dir() == f"{sue_userdir.real_dir()}/persons"
    assert sue_userdir.person_dir() == f"{sue_userdir.persons_dir()}/{sue_text}"
    assert sue_userdir.econs_dir() == f"{sue_userdir.person_dir()}/econs"
    assert sue_userdir.atoms_dir() == f"{sue_userdir.person_dir()}/atoms"
    x_changes_dir = f"{sue_userdir.person_dir()}/{get_changes_folder()}"
    assert sue_userdir.changes_dir() == x_changes_dir
    assert sue_userdir.duty_file_name() == f"{duty_str()}.json"
    x_duty_path = f"{sue_userdir.person_dir()}/{sue_userdir.duty_file_name()}"
    assert sue_userdir.duty_path() == x_duty_path
    assert sue_userdir.work_file_name() == f"{work_str()}.json"
    x_workpath = f"{sue_userdir.person_dir()}/{sue_userdir.work_file_name()}"
    assert sue_userdir.work_path() == x_workpath


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


def test_UserDir_save_file_duty_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(get_road_temp_env_dir(), None, sue_text)
    assert os_path_exists(sue_userdir.duty_path()) == False

    # WHEN
    sue_userdir.save_file_duty(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_userdir.duty_path())


def test_UserDir_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(get_road_temp_env_dir(), None, sue_text)
    assert sue_userdir.duty_file_exists() == False

    # WHEN
    sue_userdir.save_file_duty(file_text="fooboo", replace=True)

    # THEN
    assert sue_userdir.duty_file_exists()


def test_UserDir_open_file_duty_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(get_road_temp_env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_userdir.save_file_duty(example_text, replace=True)

    # WHEN / THEN
    assert sue_userdir.open_file_duty() == example_text


def test_UserDir_save_file_work_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(get_road_temp_env_dir(), None, sue_text)
    assert os_path_exists(sue_userdir.work_path()) == False

    # WHEN
    sue_userdir.save_file_work(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_userdir.work_path())


def test_UserDir_work_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(get_road_temp_env_dir(), None, sue_text)
    assert sue_userdir.work_file_exists() == False

    # WHEN
    sue_userdir.save_file_work(file_text="fooboo", replace=True)

    # THEN
    assert sue_userdir.work_file_exists()


def test_UserDir_open_file_work_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(get_road_temp_env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_userdir.save_file_work(example_text, replace=True)

    # WHEN / THEN
    assert sue_userdir.open_file_work() == example_text


def test_get_econ_path_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    peru_text = "peru"
    sue_userdir = userdir_shop(None, real_id=peru_text, person_id=sue_text)
    texas_text = "texas"
    dallas_text = "dallas"
    elpaso_text = "el paso"
    kern_text = "kern"
    idearoot = get_rootpart_of_econ_dir()
    texas_road = create_road_from_nodes([idearoot, texas_text])
    dallas_road = create_road_from_nodes([idearoot, texas_text, dallas_text])
    elpaso_road = create_road_from_nodes([idearoot, texas_text, elpaso_text])
    kern_road = create_road_from_nodes([idearoot, texas_text, elpaso_text, kern_text])

    # WHEN
    texas_path = get_econ_path(sue_userdir, texas_road)
    dallas_path = get_econ_path(sue_userdir, dallas_road)
    elpaso_path = get_econ_path(sue_userdir, elpaso_road)
    kern_path = get_econ_path(sue_userdir, kern_road)

    # THEN
    idearoot_dir = f"{sue_userdir.econs_dir()}/{get_rootpart_of_econ_dir()}"
    print(f"{kern_road=}")
    print(f"{idearoot_dir=}")
    assert texas_path == f"{idearoot_dir}/{texas_text}"
    assert dallas_path == f"{idearoot_dir}/{texas_text}/{dallas_text}"
    assert elpaso_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}"
    assert kern_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}/{kern_text}"

    # WHEN / THEN
    diff_root_texas_road = create_road_from_nodes([peru_text, texas_text])
    diff_root_dallas_road = create_road_from_nodes([peru_text, texas_text, dallas_text])
    diff_root_elpaso_road = create_road_from_nodes([peru_text, texas_text, elpaso_text])
    assert texas_path == get_econ_path(sue_userdir, diff_root_texas_road)
    assert dallas_path == get_econ_path(sue_userdir, diff_root_dallas_road)
    assert elpaso_path == get_econ_path(sue_userdir, diff_root_elpaso_road)


def test_EconDir_Exists():
    # GIVEN / WHEN
    x_econdir = EconDir()

    # THEN
    assert x_econdir.reals_dir is None
    assert x_econdir.real_id is None
    assert x_econdir.person_id is None
    assert x_econdir.econ_road is None
    assert x_econdir._road_delimiter is None
    assert x_econdir._planck is None


def test_econdir_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)

    # WHEN
    sue_econdir = econdir_shop(None, None, sue_text, econ_road=texas_road)

    # THEN
    assert sue_econdir.reals_dir == get_test_reals_dir()
    assert sue_econdir.real_id == get_test_real_id()
    assert sue_econdir.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_econdir.person_id == sue_text
    assert sue_econdir._road_delimiter == default_road_delimiter_if_none()
    assert sue_econdir._planck == default_planck_if_none()
    assert sue_econdir.persons_dir() == f"{sue_econdir.real_dir()}/persons"
    x_userdir = userdir_shop(None, None, sue_text)
    assert sue_econdir.econ_road == texas_road
    assert sue_econdir.econ_dir() == get_econ_path(x_userdir, texas_road)
    bob_text = "Bob"
    assert sue_econdir.roles_dir() == f"{sue_econdir.econ_dir()}/roles"
    assert sue_econdir.jobs_dir() == f"{sue_econdir.econ_dir()}/jobs"
    assert (
        sue_econdir.role_path(bob_text) == f"{sue_econdir.roles_dir()}/{bob_text}.json"
    )
    assert sue_econdir.job_path(bob_text) == f"{sue_econdir.jobs_dir()}/{bob_text}.json"


def test_EconDir_save_file_role_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econdir = econdir_shop(get_road_temp_env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    assert os_path_exists(sue_econdir.role_path(bob_text)) == False

    # WHEN
    sue_econdir.save_file_role(bob_text, file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_econdir.role_path(bob_text))


def test_EconDir_role_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econdir = econdir_shop(get_road_temp_env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    assert sue_econdir.role_file_exists(bob_text) == False

    # WHEN
    sue_econdir.save_file_role(bob_text, file_text="fooboo", replace=True)

    # THEN
    assert sue_econdir.role_file_exists(bob_text)


def test_EconDir_open_file_role_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econdir = econdir_shop(get_road_temp_env_dir(), None, sue_text, texas_road)
    example_text = "fooboo"
    bob_text = "Bob"
    sue_econdir.save_file_role(bob_text, example_text, replace=True)

    # WHEN / THEN
    assert sue_econdir.open_file_role(bob_text) == example_text


def test_EconDir_save_file_job_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econdir = econdir_shop(get_road_temp_env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    assert os_path_exists(sue_econdir.job_path(bob_text)) == False

    # WHEN
    sue_econdir.save_file_job(bob_text, file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_econdir.job_path(bob_text))


def test_EconDir_job_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econdir = econdir_shop(get_road_temp_env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    assert sue_econdir.job_file_exists(bob_text) == False

    # WHEN
    sue_econdir.save_file_job(bob_text, file_text="fooboo", replace=True)

    # THEN
    assert sue_econdir.job_file_exists(bob_text)


def test_EconDir_open_file_job_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econdir = econdir_shop(get_road_temp_env_dir(), None, sue_text, texas_road)
    example_text = "fooboo"
    bob_text = "Bob"
    sue_econdir.save_file_job(bob_text, example_text, replace=True)

    # WHEN / THEN
    assert sue_econdir.open_file_job(bob_text) == example_text
