from src.instrument.file import delete_dir
from src.market.market import marketunit_shop, MarketUnit
from os import path as os_path
from src.market.examples.market_env_kit import (
    get_temp_env_market_id,
    get_test_markets_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.instrument.sqlite import check_connection


def test_market_create_treasury_db_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create market
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())
    delete_dir(dir=x_market.get_treasury_db_path())  # clear out any treasury.db file
    assert os_path.exists(x_market.get_treasury_db_path()) == False

    # WHEN
    x_market._create_treasury_db()

    # THEN
    assert os_path.exists(x_market.get_treasury_db_path())


def test_market_create_treasury_db_CanCreateTreasuryInMemory(env_dir_setup_cleanup):
    # GIVEN create market
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    x_market._treasury_db = None
    assert x_market._treasury_db is None
    assert os_path.exists(x_market.get_treasury_db_path()) == False

    # WHEN
    x_market._create_treasury_db(in_memory=True)

    # THEN
    assert x_market._treasury_db != None
    assert os_path.exists(x_market.get_treasury_db_path()) == False


def test_market_refresh_treasury_forum_agendas_data_CanConnectToTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create market
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())
    # x_market._create_treasury_db(in_memory=True)
    assert os_path.exists(x_market.get_treasury_db_path()) == False

    # WHEN
    x_market.refresh_treasury_forum_agendas_data()

    # THEN
    assert os_path.exists(x_market.get_treasury_db_path()) == False


def test_market_get_treasury_db_conn_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create market
    x_market = MarketUnit(get_temp_env_market_id(), get_test_markets_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_market.get_treasury_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_market.create_dirs_if_null(in_memory_treasury=True)

    # THEN
    assert check_connection(x_market.get_treasury_conn())
