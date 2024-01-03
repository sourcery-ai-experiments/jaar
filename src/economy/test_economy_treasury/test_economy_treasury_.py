from src.tools.file import delete_dir
from src.economy.economy import economyunit_shop, EconomyUnit
from os import path as os_path
from src.economy.examples.economy_env_kit import (
    get_temp_env_economy_id,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.tools.sqlite import check_connection


def test_economy_create_treasury_db_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create economy
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())
    delete_dir(dir=x_economy.get_treasury_db_path())  # clear out any treasury.db file
    assert os_path.exists(x_economy.get_treasury_db_path()) == False

    # WHEN
    x_economy._create_treasury_db()

    # THEN
    assert os_path.exists(x_economy.get_treasury_db_path())


def test_economy_create_treasury_db_CanCreateTreasuryInMemory(env_dir_setup_cleanup):
    # GIVEN create economy
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    x_economy._treasury_db = None
    assert x_economy._treasury_db is None
    assert os_path.exists(x_economy.get_treasury_db_path()) == False

    # WHEN
    x_economy._create_treasury_db(in_memory=True)

    # THEN
    assert x_economy._treasury_db != None
    assert os_path.exists(x_economy.get_treasury_db_path()) == False


def test_economy_refresh_treasury_public_agendas_data_CanConnectToTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create economy
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())
    # x_economy._create_treasury_db(in_memory=True)
    assert os_path.exists(x_economy.get_treasury_db_path()) == False

    # WHEN
    x_economy.refresh_treasury_public_agendas_data()

    # THEN
    assert os_path.exists(x_economy.get_treasury_db_path()) == False


def test_economy_get_treasury_db_conn_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create economy
    x_economy = EconomyUnit(get_temp_env_economy_id(), get_test_economys_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_economy.get_treasury_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_economy.create_dirs_if_null(in_memory_treasury=True)

    # THEN
    assert check_connection(x_economy.get_treasury_conn())
