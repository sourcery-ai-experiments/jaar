from src.contract.x_func import delete_dir as x_func_delete_dir
from pytest import fixture as pytest_fixture


def contract_env():
    return "src/contract/examples"


def get_contract_temp_env_dir():
    return "src/contract/examples/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_contract_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)
