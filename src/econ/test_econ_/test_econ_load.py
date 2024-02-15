from src._prime.road import default_road_delimiter_if_none, create_road
from src.instrument.file import delete_dir
from os import path as os_path
from src.econ.econ import (
    EconUnit,
    econunit_shop,
    get_temp_env_person_id,
    get_temp_env_problem_id,
    get_temp_env_healer_id,
    get_temp_env_econ_id,
)
from src.econ.examples.econ_env_kit import (
    get_test_econ_dir,
    change_econ_id_example_econ,
    copy_evaluation_econ,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_load_econunit_CorrectlyLoadsEconFromPersistentFiles(
    env_dir_setup_cleanup,
):
    # create econunit1 "texas", create two clerkunits with contract agendas. Create treasury and cash river
    # assert treasury table row population
    # load econunit2 "texas2", load two clerkunits with contract agendas.
    # Connect to treasury and assert table row population.
    pass
