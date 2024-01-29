from src.tools.file import delete_dir
from pytest import fixture as pytest_fixture


def get_src_agenda_dir() -> str:
    return "src/agenda"


def get_agenda_examples_dir():
    return f"{get_src_agenda_dir()}/examples"


def get_agenda_temp_env_dir():
    return f"{get_agenda_examples_dir()}/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_agenda_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
