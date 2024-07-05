from src._instrument.file import delete_dir
from src._road.jaar_config import init_gift_id, get_test_real_id as real_id
from src.listen.hubunit import hubunit_shop
from src.listen.examples.example_listen_gifts import sue_2atomunits_giftunit
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_HubUnit_default_suis_world_ReturnsCorrectObj():
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
    sue_default_suis = sue_hubunit.default_suis_world()

    # THEN
    assert sue_default_suis._real_id == sue_hubunit.real_id
    assert sue_default_suis._owner_id == sue_hubunit.owner_id
    assert sue_default_suis._road_delimiter == sue_hubunit.road_delimiter
    assert sue_default_suis._pixel == sue_hubunit.pixel
    assert sue_default_suis._penny == sue_hubunit.penny


def test_HubUnit_delete_suis_file_DeletessuisFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    sue_hubunit.save_suis_world(sue_hubunit.default_suis_world())
    assert sue_hubunit.suis_file_exists()

    # WHEN
    sue_hubunit.delete_suis_file()

    # THEN
    assert sue_hubunit.suis_file_exists() is False


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
    assert sue_hubunit.suis_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_gift_files_from_default()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.suis_file_exists() is False


def test_HubUnit_create_suis_from_gifts_CreatessuisFileFromGiftFiles(
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
    assert sue_hubunit.suis_file_exists() is False

    # WHEN
    sue_hubunit._create_suis_from_gifts()

    # THEN
    assert sue_hubunit.suis_file_exists()
    static_sue_suis = sue_hubunit._merge_any_gifts(sue_hubunit.default_suis_world())
    assert sue_hubunit.get_suis_world().get_dict() == static_sue_suis.get_dict()


def test_HubUnit_create_initial_gift_and_suis_files_CreatesGiftFilesAndsuisFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_gift_file_name = sue_hubunit.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_file_name}"
    assert os_path_exists(init_gift_file_path) is False
    assert sue_hubunit.suis_file_exists() is False

    # WHEN
    sue_hubunit._create_initial_gift_and_suis_files()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_hubunit.suis_file_exists()
    static_sue_suis = sue_hubunit._merge_any_gifts(sue_hubunit.default_suis_world())
    assert sue_hubunit.get_suis_world().get_dict() == static_sue_suis.get_dict()


def test_HubUnit_create_initial_gift_files_from_suis_SavesOnlyGiftFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_suis_world = sue_hubunit.default_suis_world()
    bob_text = "Bob"
    sue_suis_world.add_charunit(bob_text)
    assert sue_hubunit.suis_file_exists() is False
    sue_hubunit.save_suis_world(sue_suis_world)
    assert sue_hubunit.suis_file_exists()
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit._create_initial_gift_files_from_suis()

    # THEN
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_suis_files_CorrectlySavessuisFileAndGiftFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    assert sue_hubunit.suis_file_exists() is False
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_hubunit.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit.initialize_gift_suis_files()

    # THEN
    suis_world = sue_hubunit.get_suis_world()
    assert suis_world._real_id == real_id()
    assert suis_world._owner_id == sue_text
    assert suis_world._pixel == seven_int
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_suis_files_CorrectlySavesOnlysuisFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_hubunit.initialize_gift_suis_files()
    assert sue_hubunit.suis_file_exists()
    sue_hubunit.delete_suis_file()
    assert sue_hubunit.suis_file_exists() is False
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path)

    # WHEN
    sue_hubunit.initialize_gift_suis_files()

    # THEN
    suis_world = sue_hubunit.get_suis_world()
    assert suis_world._real_id == real_id()
    assert suis_world._owner_id == sue_text
    assert suis_world._pixel == seven_int
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_initialize_gift_suis_files_CorrectlySavesOnlygiftFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_hubunit.initialize_gift_suis_files()
    sue_suis_world = sue_hubunit.get_suis_world()
    bob_text = "Bob"
    sue_suis_world.add_charunit(bob_text)
    sue_hubunit.save_suis_world(sue_suis_world)
    assert sue_hubunit.suis_file_exists()
    init_gift_file_path = f"{sue_hubunit.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_hubunit.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_hubunit.initialize_gift_suis_files()

    # THEN
    assert sue_suis_world._real_id == real_id()
    assert sue_suis_world._owner_id == sue_text
    assert sue_suis_world._pixel == seven_int
    assert sue_suis_world.char_exists(bob_text)
    assert os_path_exists(init_gift_file_path)


def test_HubUnit_append_gifts_to_suis_file_AddsgiftsTosuisFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), real_id(), sue_text)
    sue_hubunit.initialize_gift_suis_files()
    sue_hubunit.save_gift_file(sue_2atomunits_giftunit())
    suis_world = sue_hubunit.get_suis_world()
    print(f"{suis_world._real_id=}")
    sports_text = "sports"
    sports_road = suis_world.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = suis_world.make_road(sports_road, knee_text)
    assert suis_world.idea_exists(sports_road) is False
    assert suis_world.idea_exists(knee_road) is False

    # WHEN
    new_world = sue_hubunit.append_gifts_to_suis_file()

    # THEN
    assert new_world != suis_world
    assert new_world.idea_exists(sports_road)
    assert new_world.idea_exists(knee_road)
