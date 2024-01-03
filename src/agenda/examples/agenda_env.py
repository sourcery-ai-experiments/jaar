from src.tools.file import delete_dir
from pytest import fixture as pytest_fixture


def agenda_env():
    return "src/agenda/examples"


def get_agenda_temp_env_dir():
    return "src/agenda/examples/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_agenda_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
