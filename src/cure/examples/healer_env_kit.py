# from os import listdir as os_listdir
from pytest import fixture as pytest_fixture
from src.pact.pact import PactUnit
from src.pact.x_func import delete_dir, save_file as x_func_save_file


def get_temp_healer_dir() -> str:
    return f"src/cure/examples/{get_temp_cure_handle()}"


def get_temp_cure_handle() -> str:
    return "ex_env"


@pytest_fixture()
def healer_dir_setup_cleanup():
    healer_dir = get_temp_healer_dir()
    delete_dir(dir=healer_dir)
    yield healer_dir
    delete_dir(dir=healer_dir)


def create_pact_file(pact_healer_dir: str, pact_healer: str):
    pact_x = PactUnit(_healer=pact_healer)
    # file_path = f"{pact_healer_dir}/{pact_x._healer}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {pact_x._healer=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {pact_x._healer=} to {file_path=}")
    #     f.write(pact_x.get_json())
    x_func_save_file(
        dest_dir=pact_healer_dir,
        file_title=f"{pact_x._healer}.json",
        file_text=pact_x.get_json(),
    )
    # print(f"print all {pact_dir=} {os_listdir(path=pact_dir)}")
    # for file_path_y in os_listdir(path=pact_dir):
    #     print(f"{file_path_y}")
