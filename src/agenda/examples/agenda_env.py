from src._instrument.file import delete_dir
from src._road.road import create_road_from_nodes, get_default_real_id_roadnode
from pytest import fixture as pytest_fixture


def get_codespace_agenda_dir() -> str:
    return "src/agenda"


def get_agenda_examples_dir():
    return f"{get_codespace_agenda_dir()}/examples"


def get_agenda_temp_env_dir():
    return f"{get_agenda_examples_dir()}/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_agenda_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
