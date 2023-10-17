from src.deal.x_func import delete_dir as x_func_delete_dir
from pytest import fixture as pytest_fixture


def deal_env():
    return "src/deal/examples"


def get_deal_temp_env_dir():
    return "src/deal/examples/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_deal_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)
