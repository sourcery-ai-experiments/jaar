from src._road.road import (
    default_road_delimiter_if_none,
    create_road_from_nodes,
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src._road.finance import default_pixel_if_none, default_penny_if_none
from src._road.jaar_config import (
    get_gifts_folder,
    get_test_reals_dir,
    get_test_real_id,
    get_rootpart_of_econ_dir,
)
from src._world.world import worldunit_shop
from src.listen.userhub import UserHub, userhub_shop, get_econ_path
from src.listen.examples.example_listen_worlds import get_world_with_4_levels
from src.listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_get_econ_path_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    peru_text = "peru"
    sue_userhub = userhub_shop(None, real_id=peru_text, owner_id=sue_text)
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
    texas_path = get_econ_path(sue_userhub, texas_road)
    dallas_path = get_econ_path(sue_userhub, dallas_road)
    elpaso_path = get_econ_path(sue_userhub, elpaso_road)
    kern_path = get_econ_path(sue_userhub, kern_road)

    # THEN
    idearoot_dir = f"{sue_userhub.econs_dir()}/{get_rootpart_of_econ_dir()}"
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
    assert texas_path == get_econ_path(sue_userhub, diff_root_texas_road)
    assert dallas_path == get_econ_path(sue_userhub, diff_root_dallas_road)
    assert elpaso_path == get_econ_path(sue_userhub, diff_root_elpaso_road)


def test_UserHub_Exists():
    # GIVEN / WHEN
    x_userhub = UserHub()

    # THEN
    assert x_userhub.reals_dir is None
    assert x_userhub.real_id is None
    assert x_userhub.owner_id is None
    assert x_userhub.econ_road is None
    assert x_userhub.road_delimiter is None
    assert x_userhub.pixel is None
    assert x_userhub.penny is None
    assert x_userhub.econ_money_magnitude is None


def test_UserHub_RaisesError_econ_road_DoesNotExist():
    # GIVEN
    bob_text = "Bob"
    bob_userhub = UserHub(bob_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_userhub.econ_dir()
    assert (
        str(excinfo.value)
        == f"UserHub '{bob_text}' cannot save to econ_dir because it does not have econ_road."
    )


def test_userhub_shop_ReturnsCorrectObj():
    # GIVEN
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    sue_text = "Sue"
    x_road_delimiter = "/"
    x_pixel = 9
    x_penny = 3
    x_money_magnitude = 900

    # WHEN
    x_userhub = userhub_shop(
        reals_dir=x_reals_dir,
        real_id=x_real_id,
        owner_id=sue_text,
        econ_road=None,
        road_delimiter=x_road_delimiter,
        pixel=x_pixel,
        penny=x_penny,
        econ_money_magnitude=x_money_magnitude,
    )

    # THEN
    assert x_userhub.reals_dir == x_reals_dir
    assert x_userhub.real_id == x_real_id
    assert x_userhub.owner_id == sue_text
    assert x_userhub.road_delimiter == x_road_delimiter
    assert x_userhub.pixel == x_pixel
    assert x_userhub.penny == x_penny
    assert x_userhub.econ_money_magnitude == x_money_magnitude
    assert x_userhub.real_dir() == f"{x_reals_dir}/{x_real_id}"
    assert x_userhub.owners_dir() == f"{x_userhub.real_dir()}/owners"
    assert x_userhub.owner_dir() == f"{x_userhub.owners_dir()}/{sue_text}"
    assert x_userhub.econs_dir() == f"{x_userhub.owner_dir()}/econs"
    assert x_userhub.atoms_dir() == f"{x_userhub.owner_dir()}/atoms"
    assert x_userhub.soul_dir() == f"{x_userhub.owner_dir()}/soul"
    assert x_userhub.home_dir() == f"{x_userhub.owner_dir()}/home"
    assert x_userhub.gifts_dir() == f"{x_userhub.owner_dir()}/{get_gifts_folder()}"
    assert x_userhub.soul_file_name() == f"{sue_text}.json"
    x_soul_file_path = f"{x_userhub.soul_dir()}/{x_userhub.soul_file_name()}"
    assert x_userhub.soul_file_path() == x_soul_file_path
    assert x_userhub.home_file_name() == f"{sue_text}.json"
    x_homepath = f"{x_userhub.home_dir()}/{x_userhub.home_file_name()}"
    assert x_userhub.home_path() == x_homepath


def test_userhub_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)

    # WHEN
    sue_userhub = userhub_shop(None, None, sue_text, texas_road)

    # THEN
    assert sue_userhub.reals_dir == get_test_reals_dir()
    assert sue_userhub.real_id == get_test_real_id()
    assert sue_userhub.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_userhub.owner_id == sue_text
    assert sue_userhub.road_delimiter == default_road_delimiter_if_none()
    assert sue_userhub.pixel == default_pixel_if_none()
    assert sue_userhub.penny == default_penny_if_none()
    assert sue_userhub.owners_dir() == f"{sue_userhub.real_dir()}/owners"
    x_userhub = userhub_shop(None, None, sue_text)
    assert sue_userhub.econ_road == texas_road
    assert sue_userhub.econ_dir() == get_econ_path(x_userhub, texas_road)
    bob_text = "Bob"
    assert sue_userhub.dutys_dir() == f"{sue_userhub.econ_dir()}/dutys"
    assert sue_userhub.jobs_dir() == f"{sue_userhub.econ_dir()}/jobs"
    assert sue_userhub.grades_dir() == f"{sue_userhub.econ_dir()}/grades"
    sue_dutys_dir = sue_userhub.dutys_dir()
    sue_jobs_dir = sue_userhub.jobs_dir()
    sue_grades_dir = sue_userhub.grades_dir()
    assert sue_userhub.duty_path(bob_text) == f"{sue_dutys_dir}/{bob_text}.json"
    assert sue_userhub.job_path(bob_text) == f"{sue_jobs_dir}/{bob_text}.json"
    assert sue_userhub.grade_path(bob_text) == f"{sue_grades_dir}/{bob_text}.json"
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{sue_userhub.econ_dir()}/{treasury_file_name}"
    assert sue_userhub.treasury_file_name() == treasury_file_name
    assert sue_userhub.treasury_db_path() == treasury_file_path


def test_userhub_shop_RaisesErrorIf_owner_id_Contains_road_delimiter():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        userhub_shop(None, None, owner_id=bob_text, road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_UserHub_save_file_soul_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), None, sue_text)
    assert os_path_exists(sue_userhub.soul_file_path()) is False

    # WHEN
    sue_userhub.save_file_soul(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_userhub.soul_file_path())


def test_UserHub_soul_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), None, sue_text)
    assert sue_userhub.soul_file_exists() is False

    # WHEN
    sue_userhub.save_file_soul(file_text="fooboo", replace=True)

    # THEN
    assert sue_userhub.soul_file_exists()


def test_UserHub_open_file_soul_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_userhub.save_file_soul(example_text, replace=True)

    # WHEN / THEN
    assert sue_userhub.open_file_soul() == example_text


def test_UserHub_save_file_home_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), None, sue_text)
    assert os_path_exists(sue_userhub.home_path()) is False

    # WHEN
    sue_userhub.save_file_home(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_userhub.home_path())


def test_UserHub_home_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), None, sue_text)
    assert sue_userhub.home_file_exists() is False

    # WHEN
    sue_userhub.save_file_home(file_text="fooboo", replace=True)

    # THEN
    assert sue_userhub.home_file_exists()


def test_UserHub_open_file_home_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_userhub.save_file_home(example_text, replace=True)

    # WHEN / THEN
    assert sue_userhub.open_file_home() == example_text


def test_UserHub_save_soul_world_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_worldunit = get_world_with_4_levels()
    sue_text = sue_worldunit._owner_id
    real_id = root_label()
    sue_userhub = userhub_shop(env_dir(), real_id, sue_text, None)

    print(f"{sue_userhub.soul_file_path()=}")
    assert sue_userhub.soul_file_exists() is False

    # WHEN
    sue_userhub.save_soul_world(sue_worldunit)

    # THEN
    assert sue_userhub.soul_file_exists()


def test_UserHub_save_soul_world_RaisesErrorWhenWorld_home_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"

    real_id = root_label()
    sue_userhub = userhub_shop(env_dir(), real_id, sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_soul_world(worldunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"WorldUnit with owner_id '{yao_text}' cannot be saved as owner_id '{sue_text}''s soul world."
    )


def test_UserHub_get_soul_world_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_worldunit = get_world_with_4_levels()
    sue_text = sue_worldunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    sue_userhub.save_soul_world(sue_worldunit)

    # WHEN / THEN
    assert sue_userhub.get_soul_world().get_dict() == sue_worldunit.get_dict()


def test_UserHub_save_home_world_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_worldunit = get_world_with_4_levels()
    sue_text = sue_worldunit._owner_id

    real_id = root_label()
    sue_userhub = userhub_shop(env_dir(), real_id, sue_text, None)

    print(f"{sue_userhub.home_path()=}")
    assert sue_userhub.home_file_exists() is False

    # WHEN
    sue_userhub.save_home_world(sue_worldunit)

    # THEN
    assert sue_userhub.home_file_exists()


def test_UserHub_get_home_world_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_worldunit = get_world_with_4_levels()
    sue_text = sue_worldunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    sue_userhub.save_home_world(sue_worldunit)

    # WHEN / THEN
    assert sue_userhub.get_home_world().get_dict() == sue_worldunit.get_dict()


def test_UserHub_get_home_world_ReturnsNoneIfFileDoesNotExist(env_dir_setup_cleanup):
    # GIVEN
    sue_worldunit = get_world_with_4_levels()
    sue_text = sue_worldunit._owner_id
    sue_userhub = userhub_shop(env_dir(), None, sue_text)

    # WHEN / THEN
    assert sue_userhub.get_home_world() is None


def test_UserHub_save_home_world_RaisesErrorWhenWorld_home_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"

    real_id = root_label()
    sue_userhub = userhub_shop(env_dir(), real_id, sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_home_world(worldunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"WorldUnit with owner_id '{yao_text}' cannot be saved as owner_id '{sue_text}''s home world."
    )
