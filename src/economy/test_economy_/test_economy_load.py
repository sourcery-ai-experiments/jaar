from src._prime.road import default_road_delimiter_if_none, create_road
from src.tools.file import delete_dir
from os import path as os_path
from src.economy.economy import (
    EconomyUnit,
    economyunit_shop,
    get_temp_env_person_id,
    get_temp_env_problem_id,
    get_temp_env_healer_id,
    get_temp_env_economy_id,
)
from src.economy.examples.economy_env_kit import (
    get_test_economys_dir,
    change_economy_id_example_economy,
    copy_evaluation_economy,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_load_economyunit_CorrectlyLoadsEconomyFromPersistentFiles(
    env_dir_setup_cleanup,
):
    # create economyunit1 "texas", create two clerkunits with contract agendas. Create treasury and currency river
    # assert treasury table row population
    # load economyunit2 "texas2", load two clerkunits with contract agendas.
    # Connect to treasury and assert table row population.
    pass
