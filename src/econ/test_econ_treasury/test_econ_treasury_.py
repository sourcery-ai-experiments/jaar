from src.instrument.file import delete_dir
from src.econ.econ import econunit_shop, EconUnit, treasury_db_filename
from os import path as os_path
from src.econ.examples.econ_env_kit import (
    get_temp_env_world_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.instrument.file import save_file, open_file
from src.instrument.sqlite import check_connection


def test_EconUnit_create_treasury_db_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    delete_dir(dir=x_econ.get_treasury_db_path())  # clear out any treasury.db file
    assert os_path.exists(x_econ.get_treasury_db_path()) == False

    # WHEN
    x_econ._create_treasury_db()

    # THEN
    assert os_path.exists(x_econ.get_treasury_db_path())


def test_EconUnit_create_treasury_db_DoesNotOverWriteDBIfItExists(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    delete_dir(dir=x_econ.get_treasury_db_path())  # clear out any treasury.db file
    x_econ._create_treasury_db()
    assert os_path.exists(x_econ.get_treasury_db_path())

    # Given
    x_file_text = "Texas Dallas ElPaso"
    db_file = treasury_db_filename()
    save_file(x_econ.econ_dir, file_name=db_file, file_text=x_file_text, replace=True)
    assert os_path.exists(x_econ.get_treasury_db_path())
    assert open_file(x_econ.econ_dir, file_name=db_file) == x_file_text

    # WHEN
    x_econ._create_treasury_db()
    # THEN
    assert open_file(x_econ.econ_dir, file_name=db_file) == x_file_text

    # # WHEN
    # x_econ._create_treasury_db(overwrite=True)
    # # THEN
    # assert open_file(x_econ.econ_dir, file_name=db_file) != x_file_text


def test_EconUnit_create_treasury_db_CanCreateTreasuryInMemory(env_dir_setup_cleanup):
    # GIVEN create econ
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())

    x_econ._treasury_db = None
    assert x_econ._treasury_db is None
    assert os_path.exists(x_econ.get_treasury_db_path()) == False

    # WHEN
    x_econ._create_treasury_db(in_memory=True)

    # THEN
    assert x_econ._treasury_db != None
    assert os_path.exists(x_econ.get_treasury_db_path()) == False


def test_EconUnit_refresh_treasury_job_agendas_data_CanConnectToTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    # x_econ._create_treasury_db(in_memory=True)
    assert os_path.exists(x_econ.get_treasury_db_path()) == False

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    assert os_path.exists(x_econ.get_treasury_db_path()) == False


def test_EconUnit_get_treasury_conn_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    x_econ = EconUnit(get_temp_env_world_id(), get_test_econ_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_econ.get_treasury_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_econ.set_econ_dirs(in_memory_treasury=True)

    # THEN
    assert check_connection(x_econ.get_treasury_conn())
