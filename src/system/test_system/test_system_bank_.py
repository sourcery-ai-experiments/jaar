from src.system.system import SystemUnit
from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaKid
from src.calendar.group import groupunit_shop
from src.calendar.member import memberlink_shop
from src.calendar.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.system.examples.system_env_kit import (
    get_temp_env_name,
    get_test_systems_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.system.y_func import check_connection, get_single_result_back
from sqlite3 import connect as sqlite3_connect, Connection
from src.system.bank_sqlstr import (
    get_db_tables,
    get_groupunit_catalog_table_count,
    get_table_count_sqlstr,
)


def test_system_create_bank_db_CreatesBankDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create system
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null()

    # clear out any bank.db file
    x_func_delete_dir(dir=e1.get_bank_db_path())
    assert os_path.exists(e1.get_bank_db_path()) == False

    # WHEN
    e1._create_bank_db()

    # THEN
    assert os_path.exists(e1.get_bank_db_path())


def test_system_create_bank_db_CanCreateBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create system
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    # clear out any bank.db file
    e1._bank_db = None
    assert e1._bank_db is None
    assert os_path.exists(e1.get_bank_db_path()) == False

    # WHEN
    e1._create_bank_db(in_memory=True)

    # THEN
    assert e1._bank_db != None
    assert os_path.exists(e1.get_bank_db_path()) == False


def test_system_refresh_bank_metrics_CanConnectToBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create system
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)
    # e1._create_bank_db(in_memory=True)
    assert os_path.exists(e1.get_bank_db_path()) == False

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert os_path.exists(e1.get_bank_db_path()) == False


def test_system_get_bank_db_conn_CreatesBankDBIfItDoesNotExist(env_dir_setup_cleanup):
    # GIVEN create system
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(e1.get_bank_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    e1.create_dirs_if_null(in_memory_bank=True)

    # THEN
    assert check_connection(e1.get_bank_conn())
