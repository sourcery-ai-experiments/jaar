from src._instrument.file import delete_dir
from src._road.jaar_config import init_gift_id, get_test_real_id as real_id
from src.listen.userhub import userhub_shop
from src.listen.examples.example_listen_gifts import sue_2atomunits_giftunit
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_UserHub_default_soul_world_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"
    point_five_float = 0.5
    point_four_float = 0.4
    sue_userhub = userhub_shop(
        env_dir(),
        real_id(),
        sue_text,
        econ_road=None,
        road_delimiter=slash_text,
        pixel=point_five_float,
        penny=point_four_float,
    )

    # WHEN
    sue_default_soul = sue_userhub.default_soul_world()

    # THEN
    assert sue_default_soul._real_id == sue_userhub.real_id
    assert sue_default_soul._owner_id == sue_userhub.owner_id
    assert sue_default_soul._road_delimiter == sue_userhub.road_delimiter
    assert sue_default_soul._pixel == sue_userhub.pixel
    assert sue_default_soul._penny == sue_userhub.penny


def test_UserHub_delete_soul_file_DeletessoulFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_soul_world(sue_userhub.default_soul_world())
    assert sue_userhub.soul_file_exists()

    # WHEN
    sue_userhub.delete_soul_file()

    # THEN
    assert sue_userhub.soul_file_exists() is False


def test_UserHub_create_initial_gift_files_from_default_CorrectlySavesGiftUnitFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_gift_file_name = sue_userhub.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_userhub.gifts_dir()}/{init_gift_file_name}"
    assert os_path_exists(init_gift_file_path) is False
    assert sue_userhub.soul_file_exists() is False

    # WHEN
    sue_userhub._create_initial_gift_files_from_default()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_userhub.soul_file_exists() is False


def test_UserHub_create_soul_from_gifts_CreatessoulFileFromGiftFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_gift_file_name = sue_userhub.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_userhub.gifts_dir()}/{init_gift_file_name}"
    sue_userhub._create_initial_gift_files_from_default()
    assert os_path_exists(init_gift_file_path)
    assert sue_userhub.soul_file_exists() is False

    # WHEN
    sue_userhub._create_soul_from_gifts()

    # THEN
    assert sue_userhub.soul_file_exists()
    static_sue_soul = sue_userhub._merge_any_gifts(sue_userhub.default_soul_world())
    assert sue_userhub.get_soul_world().get_dict() == static_sue_soul.get_dict()


def test_UserHub_create_initial_gift_and_soul_files_CreatesGiftFilesAndsoulFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_gift_file_name = sue_userhub.gift_file_name(init_gift_id())
    init_gift_file_path = f"{sue_userhub.gifts_dir()}/{init_gift_file_name}"
    assert os_path_exists(init_gift_file_path) is False
    assert sue_userhub.soul_file_exists() is False

    # WHEN
    sue_userhub._create_initial_gift_and_soul_files()

    # THEN
    assert os_path_exists(init_gift_file_path)
    assert sue_userhub.soul_file_exists()
    static_sue_soul = sue_userhub._merge_any_gifts(sue_userhub.default_soul_world())
    assert sue_userhub.get_soul_world().get_dict() == static_sue_soul.get_dict()


def test_UserHub_create_initial_gift_files_from_soul_SavesOnlyGiftFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_soul_world = sue_userhub.default_soul_world()
    bob_text = "Bob"
    sue_soul_world.add_charunit(bob_text)
    assert sue_userhub.soul_file_exists() is False
    sue_userhub.save_soul_world(sue_soul_world)
    assert sue_userhub.soul_file_exists()
    init_gift_file_path = f"{sue_userhub.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_userhub._create_initial_gift_files_from_soul()

    # THEN
    assert os_path_exists(init_gift_file_path)


def test_UserHub_initialize_gift_soul_files_CorrectlySavessoulFileAndGiftFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    assert sue_userhub.soul_file_exists() is False
    init_gift_file_path = f"{sue_userhub.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_userhub.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_userhub.initialize_gift_soul_files()

    # THEN
    soul_world = sue_userhub.get_soul_world()
    assert soul_world._real_id == real_id()
    assert soul_world._owner_id == sue_text
    assert soul_world._pixel == seven_int
    assert os_path_exists(init_gift_file_path)


def test_UserHub_initialize_gift_soul_files_CorrectlySavesOnlysoulFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_userhub.initialize_gift_soul_files()
    assert sue_userhub.soul_file_exists()
    sue_userhub.delete_soul_file()
    assert sue_userhub.soul_file_exists() is False
    init_gift_file_path = f"{sue_userhub.gifts_dir()}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path)

    # WHEN
    sue_userhub.initialize_gift_soul_files()

    # THEN
    soul_world = sue_userhub.get_soul_world()
    assert soul_world._real_id == real_id()
    assert soul_world._owner_id == sue_text
    assert soul_world._pixel == seven_int
    assert os_path_exists(init_gift_file_path)


def test_UserHub_initialize_gift_soul_files_CorrectlySavesOnlygiftFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_userhub.initialize_gift_soul_files()
    sue_soul_world = sue_userhub.get_soul_world()
    bob_text = "Bob"
    sue_soul_world.add_charunit(bob_text)
    sue_userhub.save_soul_world(sue_soul_world)
    assert sue_userhub.soul_file_exists()
    init_gift_file_path = f"{sue_userhub.gifts_dir()}/{init_gift_id()}.json"
    delete_dir(sue_userhub.gifts_dir())
    assert os_path_exists(init_gift_file_path) is False

    # WHEN
    sue_userhub.initialize_gift_soul_files()

    # THEN
    assert sue_soul_world._real_id == real_id()
    assert sue_soul_world._owner_id == sue_text
    assert sue_soul_world._pixel == seven_int
    assert sue_soul_world.char_exists(bob_text)
    assert os_path_exists(init_gift_file_path)


def test_UserHub_append_gifts_to_soul_file_AddsgiftsTosoulFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.initialize_gift_soul_files()
    sue_userhub.save_gift_file(sue_2atomunits_giftunit())
    soul_world = sue_userhub.get_soul_world()
    print(f"{soul_world._real_id=}")
    sports_text = "sports"
    sports_road = soul_world.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = soul_world.make_road(sports_road, knee_text)
    assert soul_world.idea_exists(sports_road) is False
    assert soul_world.idea_exists(knee_road) is False

    # WHEN
    new_world = sue_userhub.append_gifts_to_soul_file()

    # THEN
    assert new_world != soul_world
    assert new_world.idea_exists(sports_road)
    assert new_world.idea_exists(knee_road)
