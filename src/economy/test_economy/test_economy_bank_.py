from src.contract.x_func import delete_dir as x_func_delete_dir
from src.economy.economy import economyunit_shop, EconomyUnit
from os import path as os_path
from src.economy.examples.economy_env_kit import (
    get_temp_env_title,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.economy.y_func import check_connection


def test_economy_create_bank_db_CreatesBankDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create economy
    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )

    # clear out any bank.db file
    x_func_delete_dir(dir=sx.get_bank_db_path())
    assert os_path.exists(sx.get_bank_db_path()) == False

    # WHEN
    sx._create_bank_db()

    # THEN
    assert os_path.exists(sx.get_bank_db_path())


def test_economy_create_bank_db_CanCreateBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create economy
    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)

    # clear out any bank.db file
    sx._bank_db = None
    assert sx._bank_db is None
    assert os_path.exists(sx.get_bank_db_path()) == False

    # WHEN
    sx._create_bank_db(in_memory=True)

    # THEN
    assert sx._bank_db != None
    assert os_path.exists(sx.get_bank_db_path()) == False


def test_economy_refresh_bank_metrics_CanConnectToBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create economy
    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    # sx._create_bank_db(in_memory=True)
    assert os_path.exists(sx.get_bank_db_path()) == False

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert os_path.exists(sx.get_bank_db_path()) == False


def test_economy_get_bank_db_conn_CreatesBankDBIfItDoesNotExist(env_dir_setup_cleanup):
    # GIVEN create economy
    sx = EconomyUnit(title=get_temp_env_title(), economys_dir=get_test_economys_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(sx.get_bank_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    sx.create_dirs_if_null(in_memory_bank=True)

    # THEN
    assert check_connection(sx.get_bank_conn())
