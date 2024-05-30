from src._road.jaar_config import get_test_real_id, get_test_reals_dir
from src._instrument.file import delete_dir
from pytest import fixture as pytest_fixture


@pytest_fixture()
def reals_dir_setup_cleanup():
    env_dir = get_test_reals_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
