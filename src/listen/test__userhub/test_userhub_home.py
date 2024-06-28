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


def test_UserHub_being_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    assert os_path_exists(sue_userhub.being_path()) is False
    assert sue_userhub.being_file_exists() is False

    # WHEN
    save_file(
        dest_dir=sue_userhub.being_dir(),
        file_name=sue_userhub.being_file_name(),
        file_text=worldunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_userhub.being_path())
    assert sue_userhub.being_file_exists()


def test_UserHub_save_being_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    assert sue_userhub.being_file_exists() is False

    # WHEN
    sue_world = worldunit_shop(sue_text)
    bob_text = "Bob"
    sue_world.add_charunit(bob_text)
    sue_userhub.save_being_world(sue_world)

    # THEN
    assert sue_userhub.being_file_exists()

    being_file_text = open_file(sue_userhub.being_dir(), sue_userhub.being_file_name())
    print(f"{being_file_text=}")
    being_world = worldunit_get_from_json(being_file_text)
    assert being_world.char_exists(bob_text)

    # # WHEN
    sue2_world = worldunit_shop(sue_text)
    zia_text = "Zia"
    sue2_world.add_charunit(zia_text)
    sue_userhub.save_being_world(sue2_world)

    # THEN
    being_file_text = open_file(sue_userhub.being_dir(), sue_userhub.being_file_name())
    print(f"{being_file_text=}")
    being_world = worldunit_get_from_json(being_file_text)
    assert being_world.char_exists(zia_text)


def test_UserHub_save_being_file_RaisesErrorWhenWorld_being_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_being_world(worldunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"WorldUnit with owner_id '{yao_text}' cannot be saved as owner_id '{sue_text}''s being world."
    )


def test_UserHub_initialize_being_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    sue_world = worldunit_shop(sue_text, root_label())
    assert sue_userhub.being_file_exists() is False

    # WHEN
    sue_userhub.initialize_being_file(sue_world)

    # THEN
    being_world = sue_userhub.get_being_world()
    assert being_world._real_id == root_label()
    assert being_world._owner_id == sue_text
    bob_text = "Bob"
    assert being_world.char_exists(bob_text) is False

    # GIVEN
    sue_world = worldunit_shop(sue_text)
    sue_world.add_charunit(bob_text)
    sue_userhub.save_being_world(sue_world)
    being_world = sue_userhub.get_being_world()
    assert being_world.get_char(bob_text)

    # WHEN
    sue_userhub.initialize_being_file(sue_world)

    # THEN
    being_world = sue_userhub.get_being_world()
    assert being_world.get_char(bob_text)


def test_UserHub_initialize_being_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_pixel = 7
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None, pixel=sue_pixel)
    sue_world = worldunit_shop(sue_text, root_label(), _pixel=sue_pixel)
    sue_userhub.initialize_being_file(sue_world)
    assert sue_userhub.being_file_exists()
    delete_dir(sue_userhub.being_path())
    assert sue_userhub.being_file_exists() is False

    # WHEN
    bob_text = "Bob"
    sue_world.add_charunit(bob_text)
    sue_userhub.initialize_being_file(sue_world)

    # THEN
    assert sue_userhub.being_file_exists()

    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_owners_dir = f"{sue_real_dir}/owners"
    sue_owner_dir = f"{sue_owners_dir}/{sue_text}"
    sue_being_dir = f"{sue_owner_dir}/being"
    sue_being_file_name = f"{sue_text}.json"
    being_file_text = open_file(dest_dir=sue_being_dir, file_name=sue_being_file_name)
    print(f"{being_file_text=}")
    being_world = worldunit_get_from_json(being_file_text)
    assert being_world._real_id == root_label()
    assert being_world._owner_id == sue_text
    assert being_world._pixel == sue_pixel


def test_UserHub_initialize_being_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    delete_dir(sue_userhub.real_dir())
    assert os_path_exists(sue_userhub.being_path()) is False

    # WHEN
    sue_world = worldunit_shop(sue_text, root_label())
    sue_userhub.initialize_being_file(sue_world)

    # THEN
    assert os_path_exists(sue_userhub.being_path())
