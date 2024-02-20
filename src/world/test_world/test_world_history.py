from src._road.road import default_road_delimiter_if_none
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)

from src.world.person import personunit_shop
from src.instrument.file import delete_dir, save_file, open_file
from os import path as os_path
from pytest import raises as pytest_raises


def test_WorldUnit_get_history_db_path_ReturnsCorrectObj():
    # GIVEN
    music_text = "music"
    music_world = WorldUnit(world_id=music_text, worlds_dir=get_test_worlds_dir())

    # WHEN
    x_history_db_path = music_world.get_history_db_path()

    # THEN
    x_world_dir = f"{get_test_worlds_dir()}/{music_text}"
    history_file_name = "history.db"
    assert x_history_db_path == f"{x_world_dir}/{history_file_name}"


def test_WorldUnit_create_history_db_CreatesDBIfItDoesNotExist(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
    assert os_path.exists(music_world.get_history_db_path())
    delete_dir(music_world.get_history_db_path())
    assert os_path.exists(music_world.get_history_db_path()) == False

    # WHEN
    music_world._create_history_db()

    # THEN
    assert os_path.exists(music_world.get_history_db_path())


def test_WorldUnit_create_history_db_DoesNotOverWriteDBIfItExists(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
    delete_dir(dir=music_world.get_history_db_path())  # clear out any treasury.db file
    music_world._create_history_db()
    assert os_path.exists(music_world.get_history_db_path())

    # SETUP
    x_file_text = "Texas Dallas ElPaso"
    db_file = "history.db"
    save_file(music_world._world_dir, db_file, file_text=x_file_text, replace=True)
    assert os_path.exists(music_world.get_history_db_path())
    assert open_file(music_world._world_dir, file_name=db_file) == x_file_text

    # WHEN
    music_world._create_history_db()
    # THEN
    assert open_file(music_world._world_dir, file_name=db_file) == x_file_text

    # # WHEN
    # x_econ._create_treasury_db(overwrite=True)
    # # THEN
    # assert open_file(x_econ.econ_dir, file_name=db_file) != x_file_text


def test_WorldUnit_create_history_db_CanCreateInMemory(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_history_db=True
    )

    music_world._history_db = None
    assert music_world._history_db is None
    assert os_path.exists(music_world.get_history_db_path()) == False

    # WHEN
    music_world._create_history_db(in_memory=True)

    # THEN
    assert music_world._history_db != None
    assert os_path.exists(music_world.get_history_db_path()) == False
