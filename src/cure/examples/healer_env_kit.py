# from os import listdir as os_listdir
from pytest import fixture as pytest_fixture
from src.oath.oath import OathUnit
from src.oath.x_func import delete_dir, save_file as x_func_save_file


def get_temp_healingunit_dir() -> str:
    return f"src/cure/examples/{get_temp_cure_handle()}"


def get_temp_cure_handle() -> str:
    return "ex_env"


@pytest_fixture()
def healer_dir_setup_cleanup():
    healer_dir = get_temp_healingunit_dir()
    delete_dir(dir=healer_dir)
    yield healer_dir
    delete_dir(dir=healer_dir)


def create_oath_file(oath_healingunit_dir: str, oath_healer: str):
    oath_x = OathUnit(_healer=oath_healer)
    # file_path = f"{oath_healingunit_dir}/{oath_x._healer}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {oath_x._healer=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {oath_x._healer=} to {file_path=}")
    #     f.write(oath_x.get_json())
    x_func_save_file(
        dest_dir=oath_healingunit_dir,
        file_title=f"{oath_x._healer}.json",
        file_text=oath_x.get_json(),
    )
    # print(f"print all {oath_dir=} {os_listdir(path=oath_dir)}")
    # for file_path_y in os_listdir(path=oath_dir):
    #     print(f"{file_path_y}")
