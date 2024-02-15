from src._prime.road import default_road_delimiter_if_none, create_road
from src.instrument.file import delete_dir
from os import path as os_path
from src.market.market import (
    MarketUnit,
    marketunit_shop,
    get_temp_env_person_id,
    get_temp_env_problem_id,
    get_temp_env_healer_id,
    get_temp_env_market_id,
)
from src.market.examples.market_env_kit import (
    get_test_market_dir,
    change_market_id_example_market,
    copy_evaluation_market,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_load_marketunit_CorrectlyLoadsMarketFromPersistentFiles(
    env_dir_setup_cleanup,
):
    # create marketunit1 "texas", create two clerkunits with contract agendas. Create bank and cash river
    # assert bank table row population
    # load marketunit2 "texas2", load two clerkunits with contract agendas.
    # Connect to bank and assert table row population.
    pass
