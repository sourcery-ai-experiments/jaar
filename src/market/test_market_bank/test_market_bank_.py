from src.instrument.file import delete_dir
from src.market.market import marketunit_shop, MarketUnit
from os import path as os_path
from src.market.examples.market_env_kit import (
    get_temp_env_market_id,
    get_test_market_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.instrument.sqlite import check_connection


def test_market_create_bank_db_CreatesBankDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create market
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_market_dir())
    delete_dir(dir=x_market.get_bank_db_path())  # clear out any bank.db file
    assert os_path.exists(x_market.get_bank_db_path()) == False

    # WHEN
    x_market._create_bank_db()

    # THEN
    assert os_path.exists(x_market.get_bank_db_path())


def test_market_create_bank_db_CanCreateBankInMemory(env_dir_setup_cleanup):
    # GIVEN create market
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_market_dir())

    x_market._bank_db = None
    assert x_market._bank_db is None
    assert os_path.exists(x_market.get_bank_db_path()) == False

    # WHEN
    x_market._create_bank_db(in_memory=True)

    # THEN
    assert x_market._bank_db != None
    assert os_path.exists(x_market.get_bank_db_path()) == False


def test_market_refresh_bank_forum_agendas_data_CanConnectToBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create market
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_market_dir())
    # x_market._create_bank_db(in_memory=True)
    assert os_path.exists(x_market.get_bank_db_path()) == False

    # WHEN
    x_market.refresh_bank_forum_agendas_data()

    # THEN
    assert os_path.exists(x_market.get_bank_db_path()) == False


def test_market_get_bank_db_conn_CreatesBankDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create market
    x_market = MarketUnit(get_temp_env_market_id(), get_test_market_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_market.get_bank_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_market.set_market_dirs(in_memory_bank=True)

    # THEN
    assert check_connection(x_market.get_bank_conn())
