from src._instrument.file import open_file, save_file, delete_dir
from src._road.road import get_default_real_id_roadnode as root_label
from src._world.world import worldunit_shop, get_from_json as worldunit_get_from_json
from src.listen.userhub import userhub_shop
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_UserHub_home_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    assert os_path_exists(sue_userhub.home_path()) is False
    assert sue_userhub.home_file_exists() is False

    # WHEN
    save_file(
        dest_dir=sue_userhub.home_dir(),
        file_name=sue_userhub.home_file_name(),
        file_text=worldunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_userhub.home_path())
    assert sue_userhub.home_file_exists()


def test_UserHub_save_home_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    assert sue_userhub.home_file_exists() is False

    # WHEN
    sue_world = worldunit_shop(sue_text)
    bob_text = "Bob"
    sue_world.add_charunit(bob_text)
    sue_userhub.save_home_world(sue_world)

    # THEN
    assert sue_userhub.home_file_exists()

    home_file_text = open_file(sue_userhub.home_dir(), sue_userhub.home_file_name())
    print(f"{home_file_text=}")
    home_world = worldunit_get_from_json(home_file_text)
    assert home_world.char_exists(bob_text)

    # # WHEN
    sue2_world = worldunit_shop(sue_text)
    zia_text = "Zia"
    sue2_world.add_charunit(zia_text)
    sue_userhub.save_home_world(sue2_world)

    # THEN
    home_file_text = open_file(sue_userhub.home_dir(), sue_userhub.home_file_name())
    print(f"{home_file_text=}")
    home_world = worldunit_get_from_json(home_file_text)
    assert home_world.char_exists(zia_text)


def test_UserHub_save_home_file_RaisesErrorWhenWorld_home_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_home_world(worldunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"WorldUnit with owner_id '{yao_text}' cannot be saved as owner_id '{sue_text}''s home world."
    )


def test_UserHub_initialize_home_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    sue_world = worldunit_shop(sue_text, root_label())
    assert sue_userhub.home_file_exists() is False

    # WHEN
    sue_userhub.initialize_home_file(sue_world)

    # THEN
    home_world = sue_userhub.get_home_world()
    assert home_world._real_id == root_label()
    assert home_world._owner_id == sue_text
    bob_text = "Bob"
    assert home_world.char_exists(bob_text) is False

    # GIVEN
    sue_world = worldunit_shop(sue_text)
    sue_world.add_charunit(bob_text)
    sue_userhub.save_home_world(sue_world)
    home_world = sue_userhub.get_home_world()
    assert home_world.get_char(bob_text)

    # WHEN
    sue_userhub.initialize_home_file(sue_world)

    # THEN
    home_world = sue_userhub.get_home_world()
    assert home_world.get_char(bob_text)


def test_UserHub_initialize_home_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_pixel = 7
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None, pixel=sue_pixel)
    sue_world = worldunit_shop(sue_text, root_label(), _pixel=sue_pixel)
    sue_userhub.initialize_home_file(sue_world)
    assert sue_userhub.home_file_exists()
    delete_dir(sue_userhub.home_path())
    assert sue_userhub.home_file_exists() is False

    # WHEN
    bob_text = "Bob"
    sue_world.add_charunit(bob_text)
    sue_userhub.initialize_home_file(sue_world)

    # THEN
    assert sue_userhub.home_file_exists()

    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_owners_dir = f"{sue_real_dir}/owners"
    sue_owner_dir = f"{sue_owners_dir}/{sue_text}"
    sue_home_dir = f"{sue_owner_dir}/home"
    sue_home_file_name = f"{sue_text}.json"
    home_file_text = open_file(dest_dir=sue_home_dir, file_name=sue_home_file_name)
    print(f"{home_file_text=}")
    home_world = worldunit_get_from_json(home_file_text)
    assert home_world._real_id == root_label()
    assert home_world._owner_id == sue_text
    assert home_world._pixel == sue_pixel


def test_UserHub_initialize_home_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    delete_dir(sue_userhub.real_dir())
    assert os_path_exists(sue_userhub.home_path()) is False

    # WHEN
    sue_world = worldunit_shop(sue_text, root_label())
    sue_userhub.initialize_home_file(sue_world)

    # THEN
    assert os_path_exists(sue_userhub.home_path())
