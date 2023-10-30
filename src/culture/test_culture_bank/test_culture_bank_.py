from src.agenda.x_func import delete_dir as x_func_delete_dir
from src.culture.culture import cultureunit_shop, CultureUnit
from os import path as os_path
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.culture.y_func import check_connection


def test_culture_create_bank_db_CreatesBankDBIfItDoesNotExist(env_dir_setup_cleanup):
    # GIVEN create culture
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_func_delete_dir(dir=x_culture.get_bank_db_path())  # clear out any bank.db file
    assert os_path.exists(x_culture.get_bank_db_path()) == False

    # WHEN
    x_culture._create_bank_db()

    # THEN
    assert os_path.exists(x_culture.get_bank_db_path())


def test_culture_create_bank_db_CanCreateBankInMemory(env_dir_setup_cleanup):
    # GIVEN create culture
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())

    x_culture._bank_db = None
    assert x_culture._bank_db is None
    assert os_path.exists(x_culture.get_bank_db_path()) == False

    # WHEN
    x_culture._create_bank_db(in_memory=True)

    # THEN
    assert x_culture._bank_db != None
    assert os_path.exists(x_culture.get_bank_db_path()) == False


def test_culture_refresh_bank_public_agendas_data_CanConnectToBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create culture
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    # x_culture._create_bank_db(in_memory=True)
    assert os_path.exists(x_culture.get_bank_db_path()) == False

    # WHEN
    x_culture.refresh_bank_public_agendas_data()

    # THEN
    assert os_path.exists(x_culture.get_bank_db_path()) == False


def test_culture_get_bank_db_conn_CreatesBankDBIfItDoesNotExist(env_dir_setup_cleanup):
    # GIVEN create culture
    x_culture = CultureUnit(get_temp_env_handle(), get_test_cultures_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_culture.get_bank_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_culture.create_dirs_if_null(in_memory_bank=True)

    # THEN
    assert check_connection(x_culture.get_bank_conn())
