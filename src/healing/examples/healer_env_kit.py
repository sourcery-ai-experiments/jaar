# from os import listdir as os_listdir
from pytest import fixture as pytest_fixture
from src.contract.contract import ContractUnit
from src.contract.x_func import delete_dir, save_file as x_func_save_file


def get_temp_healer_dir() -> str:
    return f"src/healing/examples/{get_temp_healing_handle()}"


def get_temp_healing_handle() -> str:
    return "ex_env"


@pytest_fixture()
def healer_dir_setup_cleanup():
    healer_dir = get_temp_healer_dir()
    delete_dir(dir=healer_dir)
    yield healer_dir
    delete_dir(dir=healer_dir)


def create_contract_file(contract_healer_dir: str, contract_healer: str):
    contract_x = ContractUnit(_healer=contract_healer)
    # file_path = f"{contract_healer_dir}/{contract_x._healer}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {contract_x._healer=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {contract_x._healer=} to {file_path=}")
    #     f.write(contract_x.get_json())
    x_func_save_file(
        dest_dir=contract_healer_dir,
        file_title=f"{contract_x._healer}.json",
        file_text=contract_x.get_json(),
    )
    # print(f"print all {contract_dir=} {os_listdir(path=contract_dir)}")
    # for file_path_y in os_listdir(path=contract_dir):
    #     print(f"{file_path_y}")
