from src.calendar.x_func import delete_dir as x_func_delete_dir
from pytest import fixture as pytest_fixture


def calendar_env():
    return "src/calendar/examples"


def get_calendar_temp_env_dir():
    return "src/calendar/examples/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_calendar_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)
