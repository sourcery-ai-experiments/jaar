from src._instrument.file import delete_dir
from pytest import fixture as pytest_fixture


def get_test_real_id():
    return "music_45"


def get_test_reals_dir():
    return "src/real/examples/reals"


def get_test_real_dir():
    return f"{get_test_reals_dir()}/{get_test_real_id()}"


@pytest_fixture()
def reals_dir_setup_cleanup():
    env_dir = get_test_reals_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)
