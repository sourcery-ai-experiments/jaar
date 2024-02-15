from src.instrument.file import delete_dir
from src.econ.econ import econunit_shop, EconUnit
from os import path as os_path
from src.econ.examples.econ_env_kit import (
    get_temp_env_econ_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.instrument.sqlite import check_connection


def test_econ_create_treasury_db_CreatesBankDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    delete_dir(dir=x_econ.get_treasury_db_path())  # clear out any treasury.db file
    assert os_path.exists(x_econ.get_treasury_db_path()) == False

    # WHEN
    x_econ._create_treasury_db()

    # THEN
    assert os_path.exists(x_econ.get_treasury_db_path())


def test_econ_create_treasury_db_CanCreateBankInMemory(env_dir_setup_cleanup):
    # GIVEN create econ
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())

    x_econ._treasury_db = None
    assert x_econ._treasury_db is None
    assert os_path.exists(x_econ.get_treasury_db_path()) == False

    # WHEN
    x_econ._create_treasury_db(in_memory=True)

    # THEN
    assert x_econ._treasury_db != None
    assert os_path.exists(x_econ.get_treasury_db_path()) == False


def test_econ_refresh_treasury_forum_agendas_data_CanConnectToBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    # x_econ._create_treasury_db(in_memory=True)
    assert os_path.exists(x_econ.get_treasury_db_path()) == False

    # WHEN
    x_econ.refresh_treasury_forum_agendas_data()

    # THEN
    assert os_path.exists(x_econ.get_treasury_db_path()) == False


def test_econ_get_treasury_db_conn_CreatesBankDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    x_econ = EconUnit(get_temp_env_econ_id(), get_test_econ_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_econ.get_treasury_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_econ.set_econ_dirs(in_memory_treasury=True)

    # THEN
    assert check_connection(x_econ.get_treasury_conn())
