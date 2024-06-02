from src._road.road import (
    default_road_delimiter_if_none,
    create_road_from_nodes,
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src._road.finance import default_planck_if_none
from src.change.agendanox import usernox_shop, get_econ_path, EconNox, econnox_shop
from src._road.jaar_config import (
    get_changes_folder,
    duty_str,
    work_str,
    get_test_reals_dir,
    get_test_real_id,
    get_rootpart_of_econ_dir,
)
from src.change.examples.change_env import (
    env_dir_setup_cleanup,
    get_change_temp_env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_get_econ_path_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    peru_text = "peru"
    sue_usernox = usernox_shop(None, real_id=peru_text, person_id=sue_text)
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
    texas_path = get_econ_path(sue_usernox, texas_road)
    dallas_path = get_econ_path(sue_usernox, dallas_road)
    elpaso_path = get_econ_path(sue_usernox, elpaso_road)
    kern_path = get_econ_path(sue_usernox, kern_road)

    # THEN
    idearoot_dir = f"{sue_usernox.econs_dir()}/{get_rootpart_of_econ_dir()}"
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
    assert texas_path == get_econ_path(sue_usernox, diff_root_texas_road)
    assert dallas_path == get_econ_path(sue_usernox, diff_root_dallas_road)
    assert elpaso_path == get_econ_path(sue_usernox, diff_root_elpaso_road)


def test_EconNox_Exists():
    # GIVEN / WHEN
    x_econnox = EconNox()

    # THEN
    assert x_econnox.reals_dir is None
    assert x_econnox.real_id is None
    assert x_econnox.person_id is None
    assert x_econnox.econ_road is None
    assert x_econnox._road_delimiter is None
    assert x_econnox._planck is None


def test_econnox_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)

    # WHEN
    sue_econnox = econnox_shop(None, None, sue_text, econ_road=texas_road)

    # THEN
    assert sue_econnox.reals_dir == get_test_reals_dir()
    assert sue_econnox.real_id == get_test_real_id()
    assert sue_econnox.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_econnox.person_id == sue_text
    assert sue_econnox._road_delimiter == default_road_delimiter_if_none()
    assert sue_econnox._planck == default_planck_if_none()
    assert sue_econnox.persons_dir() == f"{sue_econnox.real_dir()}/persons"
    x_usernox = usernox_shop(None, None, sue_text)
    assert sue_econnox.econ_road == texas_road
    assert sue_econnox.econ_dir() == get_econ_path(x_usernox, texas_road)
    bob_text = "Bob"
    assert sue_econnox.roles_dir() == f"{sue_econnox.econ_dir()}/roles"
    assert sue_econnox.jobs_dir() == f"{sue_econnox.econ_dir()}/jobs"
    assert (
        sue_econnox.role_path(bob_text) == f"{sue_econnox.roles_dir()}/{bob_text}.json"
    )
    assert sue_econnox.job_path(bob_text) == f"{sue_econnox.jobs_dir()}/{bob_text}.json"


def test_EconNox_save_file_role_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econnox = econnox_shop(get_change_temp_env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    assert os_path_exists(sue_econnox.role_path(bob_text)) == False

    # WHEN
    sue_econnox.save_file_role(bob_text, file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_econnox.role_path(bob_text))


def test_EconNox_role_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econnox = econnox_shop(get_change_temp_env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    assert sue_econnox.role_file_exists(bob_text) == False

    # WHEN
    sue_econnox.save_file_role(bob_text, file_text="fooboo", replace=True)

    # THEN
    assert sue_econnox.role_file_exists(bob_text)


def test_EconNox_open_file_role_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econnox = econnox_shop(get_change_temp_env_dir(), None, sue_text, texas_road)
    example_text = "fooboo"
    bob_text = "Bob"
    sue_econnox.save_file_role(bob_text, example_text, replace=True)

    # WHEN / THEN
    assert sue_econnox.open_file_role(bob_text) == example_text


def test_EconNox_save_file_job_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econnox = econnox_shop(get_change_temp_env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    assert os_path_exists(sue_econnox.job_path(bob_text)) == False

    # WHEN
    sue_econnox.save_file_job(bob_text, file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_econnox.job_path(bob_text))


def test_EconNox_job_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econnox = econnox_shop(get_change_temp_env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    assert sue_econnox.job_file_exists(bob_text) == False

    # WHEN
    sue_econnox.save_file_job(bob_text, file_text="fooboo", replace=True)

    # THEN
    assert sue_econnox.job_file_exists(bob_text)


def test_EconNox_open_file_job_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_econnox = econnox_shop(get_change_temp_env_dir(), None, sue_text, texas_road)
    example_text = "fooboo"
    bob_text = "Bob"
    sue_econnox.save_file_job(bob_text, example_text, replace=True)

    # WHEN / THEN
    assert sue_econnox.open_file_job(bob_text) == example_text
