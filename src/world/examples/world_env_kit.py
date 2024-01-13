from src.tools.file import delete_dir, dir_files
from pytest import fixture as pytest_fixture


def get_temp_economy_id():
    return "ex_env77"


def get_temp_world_dir():
    return f"{get_test_worlds_dir()}/{get_temp_economy_id()}"


def get_test_worlds_dir():
    return "src/world/examples/worlds"


@pytest_fixture()
def worlds_dir_setup_cleanup():
    env_dir = get_test_worlds_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def create_example_worlds_list():
    return dir_files(
        dir_path=get_test_worlds_dir(), include_dirs=True, include_files=False
    )
