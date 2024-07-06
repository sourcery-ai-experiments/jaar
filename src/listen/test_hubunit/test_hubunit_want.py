from src._instrument.file import delete_dir
from src._road.jaar_config import init_gift_id, get_test_real_id as real_id
from src.listen.hubunit import hubunit_shop
from src.listen.examples.example_listen_gifts import sue_2atomunits_giftunit
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_HubUnit_default_want_world_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"
    point_five_float = 0.5
    point_four_float = 0.4
    sue_hubunit = hubunit_shop(
        env_dir(),
        real_id(),
        sue_text,
        econ_road=None,
        road_delimiter=slash_text,
        pixel=point_five_float,
        penny=point_four_float,
    )

    # WHEN
    sue_default_want = sue_hubunit.default_want_world()

    # THEN
    assert sue_default_want._real_id == sue_hubunit.real_id
    assert sue_default_want._owner_id == sue_hubunit.owner_id
    assert sue_default_want._road_delimiter == sue_hubunit.road_delimiter
    assert sue_default_want._pixel == sue_hubunit.pixel
    assert sue_default_want._penny == sue_hubunit.penny


def test_HubUnit_delete_want_file_DeleteswantFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    sue_hubunit.save_want_world(sue_hubunit.default_want_world())
    assert sue_hubunit.want_file_exists()

    # WHEN
    sue_hubunit.delete_want_file()

    # THEN
    assert sue_hubunit.want_file_exists() is False


def test_HubUnit_create_initial_gift_files_from_default_CorrectlySavesGiftUnitFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    assert os_path_exists(init_gift_file_path) is False
    assert sue_hubunit.want_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_gift_files_from_default()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.want_file_exists() is False


def test_HubUnit_create_want_from_gifts_CreateswantFileFromGiftFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    sue_hubunit._create_initial_gift_files_from_default()
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.want_file_exists() is False

    # WHEN
    sue_hubunit._create_want_from_gifts()

    # THEN
    assert sue_hubunit.want_file_exists()
    static_sue_want = sue_hubunit._merge_any_gifts(sue_hubunit.default_want_world())
    assert sue_hubunit.get_want_world().get_dict() == static_sue_want.get_dict()


def test_HubUnit_create_initial_gift_and_want_files_CreatesGiftFilesAndwantFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    assert os_path_exists(init_gift_file_path) is False
    assert sue_hubunit.want_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_gift_and_want_files()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.want_file_exists()
    static_sue_want = sue_hubunit._merge_any_gifts(sue_hubunit.default_want_world())
    assert sue_hubunit.get_want_world().get_dict() == static_sue_want.get_dict()


def test_HubUnit_create_initial_gift_files_from_want_SavesOnlyGiftFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_want_world = sue_hubunit.default_want_world()
    bob_text = "Bob"
    sue_want_world.add_charunit(bob_text)
    assert sue_hubunit.want_file_exists() is False
    sue_hubunit.save_want_world(sue_want_world)
    assert sue_hubunit.want_file_exists()
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit._create_initial_gift_files_from_want()

    # THEN
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_want_files_CorrectlySaveswantFileAndGiftFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    assert sue_hubunit.want_file_exists() is False
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_hubunit.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit.initialize_gift_want_files()

    # THEN
    want_world = sue_hubunit.get_want_world()
    assert want_world._real_id == real_id()
    assert want_world._owner_id == sue_text
    assert want_world._pixel == seven_int
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_want_files_CorrectlySavesOnlywantFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_hubunit.initialize_gift_want_files()
    assert sue_hubunit.want_file_exists()
    sue_hubunit.delete_want_file()
    assert sue_hubunit.want_file_exists() is False
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path)

    # WHEN
    sue_hubunit.initialize_gift_want_files()

    # THEN
    want_world = sue_hubunit.get_want_world()
    assert want_world._real_id == real_id()
    assert want_world._owner_id == sue_text
    assert want_world._pixel == seven_int
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_want_files_CorrectlySavesOnlygiftFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_hubunit.initialize_gift_want_files()
    sue_want_world = sue_hubunit.get_want_world()
    bob_text = "Bob"
    sue_want_world.add_charunit(bob_text)
    sue_hubunit.save_want_world(sue_want_world)
    assert sue_hubunit.want_file_exists()
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_hubunit.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit.initialize_gift_want_files()

    # THEN
    assert sue_want_world._real_id == real_id()
    assert sue_want_world._owner_id == sue_text
    assert sue_want_world._pixel == seven_int
    assert sue_want_world.char_exists(bob_text)
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_append_gifts_to_want_file_AddsgiftsTowantFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    sue_hubunit.initialize_gift_want_files()
    sue_hubunit.save_gift_file(sue_2atomunits_giftunit())
    want_world = sue_hubunit.get_want_world()
    print(f"{want_world._real_id=}")
    sports_text = "sports"
    sports_road = want_world.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = want_world.make_road(sports_road, knee_text)
    assert want_world.idea_exists(sports_road) is False
    assert want_world.idea_exists(knee_road) is False

    # WHEN
    new_world = sue_hubunit.append_gifts_to_want_file()

    # THEN
    assert new_world != want_world
    assert new_world.idea_exists(sports_road)
    assert new_world.idea_exists(knee_road)
