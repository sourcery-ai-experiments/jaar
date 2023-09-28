# from os import listdir as os_listdir
from pytest import fixture as pytest_fixture
from src.contract.contract import ContractUnit
from src.contract.x_func import delete_dir, save_file as x_func_save_file


def get_temp_actor_dir() -> str:
    return f"src/economy/examples/{get_temp_economy_title()}"


def get_temp_economy_title() -> str:
    return "ex_env"


@pytest_fixture()
def actor_dir_setup_cleanup():
    actor_dir = get_temp_actor_dir()
    delete_dir(dir=actor_dir)
    yield actor_dir
    delete_dir(dir=actor_dir)


def create_contract_file(contract_actor_dir: str, contract_owner: str):
    contract_x = ContractUnit(_owner=contract_owner)
    # file_path = f"{contract_actor_dir}/{contract_x._owner}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {contract_x._owner=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {contract_x._owner=} to {file_path=}")
    #     f.write(contract_x.get_json())
    x_func_save_file(
        dest_dir=contract_actor_dir,
        file_name=f"{contract_x._owner}.json",
        file_text=contract_x.get_json(),
    )
    # print(f"print all {contract_dir=} {os_listdir(path=contract_dir)}")
    # for file_path_y in os_listdir(path=contract_dir):
    #     print(f"{file_path_y}")
