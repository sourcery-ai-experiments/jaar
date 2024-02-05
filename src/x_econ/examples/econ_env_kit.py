from src.instrument.file import delete_dir, dir_files
from pytest import fixture as pytest_fixture


def get_temp_market_id():
    return "ex_env77"


def get_temp_econ_dir():
    return f"{get_test_econs_dir()}/{get_temp_market_id()}"


def get_test_econs_dir():
    return "src/econ/examples/econs"


@pytest_fixture()
def econs_dir_setup_cleanup():
    env_dir = get_test_econs_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def create_example_econs_list():
    return dir_files(
        dir_path=get_test_econs_dir(), include_dirs=True, include_files=False
    )


def get_src_econ_dir():
    return "src/econ/"
