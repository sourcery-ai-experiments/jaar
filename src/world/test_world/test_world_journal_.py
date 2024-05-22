from src._road.road import default_road_delimiter_if_none
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_world_id,
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)
from src.world.person import personunit_shop
from src._instrument.python import get_dict_from_json, get_nested_value
from src._instrument.file import delete_dir, save_file, open_file
from src._instrument.sqlite import (
    get_db_tables,
    get_db_columns,
    check_connection,
    check_table_column_existence,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_WorldUnit_get_journal_db_path_ReturnsCorrectObj():
    # GIVEN
    music_text = "music"
    music_world = WorldUnit(world_id=music_text, worlds_dir=get_test_worlds_dir())

    # WHEN
    x_journal_db_path = music_world.get_journal_db_path()

    # THEN
    x_world_dir = f"{get_test_worlds_dir()}/{music_text}"
    journal_file_name = "journal.db"
    assert x_journal_db_path == f"{x_world_dir}/{journal_file_name}"


def test_WorldUnit_create_journal_db_CreatesDBIfItDoesNotExist(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
    assert os_path.exists(music_world.get_journal_db_path())
    delete_dir(music_world.get_journal_db_path())
    assert os_path.exists(music_world.get_journal_db_path()) == False

    # WHEN
    music_world._create_journal_db()

    # THEN
    assert os_path.exists(music_world.get_journal_db_path())


def test_WorldUnit_create_journal_db_DoesNotOverWriteDBIfItExists(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
    delete_dir(dir=music_world.get_journal_db_path())  # clear out any treasury.db file
    music_world._create_journal_db()
    assert os_path.exists(music_world.get_journal_db_path())

    # SETUP
    x_file_text = "Texas Dallas ElPaso"
    db_file = "journal.db"
    save_file(music_world._world_dir, db_file, file_text=x_file_text, replace=True)
    assert os_path.exists(music_world.get_journal_db_path())
    assert open_file(music_world._world_dir, file_name=db_file) == x_file_text

    # WHEN
    music_world._create_journal_db()
    # THEN
    assert open_file(music_world._world_dir, file_name=db_file) == x_file_text

    # # WHEN
    # music_world._create_journal_db(overwrite=True)
    # # THEN
    # assert open_file(music_world._world_dir, file_name=db_file) != x_file_text


def test_WorldUnit_create_journal_db_CanCreateInMemory(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_journal=True
    )

    music_world._journal_db = None
    assert music_world._journal_db is None
    assert os_path.exists(music_world.get_journal_db_path()) == False

    # WHEN
    music_world._create_journal_db(in_memory=True)

    # THEN
    assert music_world._journal_db != None
    assert os_path.exists(music_world.get_journal_db_path()) == False


def test_WorldUnit_get_journal_conn_CreatesTreasuryDBIfItDoesNotExist(
    worlds_dir_setup_cleanup,
):
    # GIVEN create World
    x_world = WorldUnit(get_test_world_id(), get_test_worlds_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_world.get_journal_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_world._set_world_dirs(in_memory_journal=True)

    # THEN
    assert check_connection(x_world.get_journal_conn())


def test_world_set_world_dirs_CorrectlyCreatesDBTables(worlds_dir_setup_cleanup):
    # GIVEN create world
    x_world = worldunit_shop(get_test_world_id(), get_test_worlds_dir())

    # WHEN
    x_world._set_world_dirs(in_memory_journal=True)

    # THEN
    # grab config.json
    config_text = open_file(dest_dir="src/world", file_name="journal_db_check.json")
    config_dict = get_dict_from_json(config_text)
    tables_dict = get_nested_value(config_dict, ["tables"])
    print(f"{tables_dict=}")

    with x_world.get_journal_conn() as journal_conn:
        assert check_table_column_existence(tables_dict, journal_conn)
