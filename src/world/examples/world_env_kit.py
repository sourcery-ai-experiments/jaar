# from lw.contract import ContractUnit
# from src.contract.contract import ContractUnit
from src.contract.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    copy_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)

# from src.contract.examples.example_contracts import (
#     contract_v001 as example_contracts_contract_v001,
#     contract_v002 as example_contracts_contract_v002,
#     get_contract_1Task_1CE0MinutesRequired_1AcptFact as example_contracts_get_contract_1Task_1CE0MinutesRequired_1AcptFact,
#     get_contract_with7amCleanTableRequired as example_contracts_get_contract_with7amCleanTableRequired,
#     get_contract_base_time_example as example_contracts_get_contract_base_time_example,
#     get_contract_x1_3levels_1required_1acptfacts as example_contracts_get_contract_x1_3levels_1required_1acptfacts,
# )

# from src.goal.goal import GoalUnit, goalunit_shop
# from src.goal.examples.example_owners import (
#     get_1node_contract as example_owners_get_1node_contract,
#     get_7nodeJRootWithH_contract as example_owners_get_7nodeJRootWithH_contract,
#     get_contract_2CleanNodesRandomWeights as example_owners_get_contract_2CleanNodesRandomWeights,
#     get_contract_3CleanNodesRandomWeights as example_owners_get_contract_3CleanNodesRandomWeights,
# )
from os import listdir as os_listdir, rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture


def get_temp_env_kind():
    return "ex_env77"


def get_temp_env_dir():
    return f"{get_test_worlds_dir()}/{get_temp_env_kind()}"


def get_test_worlds_dir():
    return "src/world/examples/worlds"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)


def create_example_worlds_list():
    return x_func_dir_files(
        dir_path=get_test_worlds_dir(), include_dirs=True, include_files=False
    )


# def create_example_world(world_kind: str):
#     sx = worldunit_shop(kind=world_kind, worlds_dir=get_test_worlds_dir())
#     sx.create_dirs_if_null(in_memory_bank=True)


# def delete_dir_example_world(world_obj: GoalUnit):
#     x_func_delete_dir(world_obj.get_object_root_dir())


# def rename_example_world(world_obj: GoalUnit, new_title):
#     # base_dir = world_obj.get_object_root_dir()
#     base_dir = "src/world/examples/worlds"
#     src_dir = f"{base_dir}/{world_obj.kind}"
#     dst_dir = f"{base_dir}/{new_title}"
#     os_rename(src=src_dir, dst=dst_dir)
#     world_obj.set_worldunit_kind(kind=new_title)


# class InvalidGoalCopyException(Exception):
#     pass


# def copy_evaluation_world(src_kind: str, dest_kind: str):
#     base_dir = "src/world/examples/worlds"
#     new_dir = f"{base_dir}/{dest_kind}"
#     if os_path.exists(new_dir):
#         raise InvalidGoalCopyException(
#             f"Cannot copy world to '{new_dir}' directory because '{new_dir}' exists."
#         )
#     # base_dir = world_obj.get_object_root_dir()
#     src_dir = f"{base_dir}/{src_kind}"
#     dest_dir = f"{base_dir}/{dest_kind}"
#     copy_dir(src_dir=src_dir, dest_dir=dest_dir)
