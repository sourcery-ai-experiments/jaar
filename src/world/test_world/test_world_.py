# from src.economy.economy import EconomyUnit, economyunit_shop
# from src.contract.x_func import delete_dir as x_func_delete_dir
# from os import path as os_path
# from src.economy.examples.economy_env_kit import (
#     get_temp_env_title,
#     get_test_economys_dir,
#     rename_example_economy,
#     copy_evaluation_economy,
#     env_dir_setup_cleanup,
# )
# from pytest import raises as pytest_raises
# from src.world.world import WorldUnit, worldunit_shop


# def test_world_exists():
#     world_title = "test1"
#     sx = WorldUnit(title=world_title, worlds_dir=get_test_worlds_dir())
#     assert sx.title == world_title
#     assert sx.worlds_dir == get_test_worlds_dir()


# def test_world_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
#     # GIVEN create world
#     world_title = get_temp_env_title()
#     sx = EconomyUnit(title=world_title, worlds_dir=get_test_economys_dir())
#     print(f"{get_test_economys_dir()=} {sx.economys_dir=}")
#     # x_func_delete_dir(sx.get_object_root_dir())
#     print(f"delete {sx.get_object_root_dir()=}")
#     economy_dir = f"src/economy/examples/economys/{economy_title}"
#     economy_file_name = "economy.json"
#     economy_file_path = f"{economy_dir}/{economy_file_name}"
#     contracts_dir = f"{economy_dir}/contracts"
#     owners_dir = f"{economy_dir}/owners"
#     bank_file_name = "bank.db"
#     bank_file_path = f"{economy_dir}/{bank_file_name}"

#     assert os_path.exists(economy_dir) is False
#     assert os_path.isdir(economy_dir) is False
#     assert os_path.exists(economy_file_path) is False
#     assert os_path.exists(contracts_dir) is False
#     assert os_path.exists(owners_dir) is False
#     assert os_path.exists(bank_file_path) is False

#     # WHEN
#     sx.create_dirs_if_null(in_memory_bank=False)

#     # THEN check contracts src directory created
#     assert os_path.exists(economy_dir)
#     assert os_path.isdir(economy_dir)
#     assert os_path.exists(economy_file_path)
#     assert os_path.exists(contracts_dir)
#     assert os_path.exists(owners_dir)
#     assert os_path.exists(bank_file_path)
#     assert sx.get_object_root_dir() == economy_dir
#     assert sx.get_public_dir() == contracts_dir
#     assert sx.get_owners_dir() == owners_dir
#     assert sx.get_bank_db_path() == bank_file_path


# def test_rename_example_economy_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
#     # GIVEN create economy
#     old_economy_title = get_temp_env_title()
#     old_economy_dir = f"src/economy/examples/economys/{old_economy_title}"
#     old_economy_file_name = "economy.json"
#     old_economy_file_path = f"{old_economy_dir}/{old_economy_file_name}"
#     old_contracts_dir = f"{old_economy_dir}/contracts"
#     old_owners_dir = f"{old_economy_dir}/owners"

#     new_economy_title = "ex_env1"
#     new_economy_dir = f"src/economy/examples/economys/{new_economy_title}"
#     new_economy_file_name = "economy.json"
#     new_economy_file_path = f"{new_economy_dir}/{new_economy_file_name}"
#     new_contracts_dir = f"{new_economy_dir}/contracts"
#     new_owners_dir = f"{new_economy_dir}/owners"
#     x_func_delete_dir(dir=new_economy_dir)
#     print(f"{new_economy_dir=}")

#     sx = economyunit_shop(title=old_economy_title, economys_dir=get_test_economys_dir())
#     # x_func_delete_dir(sx.get_object_root_dir())
#     # print(f"{sx.get_object_root_dir()=}")

#     sx.create_dirs_if_null(in_memory_bank=True)

#     assert os_path.exists(old_economy_dir)
#     assert os_path.isdir(old_economy_dir)
#     assert os_path.exists(old_economy_file_path)
#     assert os_path.exists(old_contracts_dir)
#     assert os_path.exists(old_owners_dir)
#     assert sx.get_public_dir() == old_contracts_dir
#     assert sx.get_owners_dir() == old_owners_dir

#     assert os_path.exists(new_economy_dir) is False
#     assert os_path.isdir(new_economy_dir) is False
#     assert os_path.exists(new_economy_file_path) is False
#     assert os_path.exists(new_contracts_dir) is False
#     assert os_path.exists(new_owners_dir) is False
#     assert sx.get_public_dir() != new_contracts_dir
#     assert sx.get_owners_dir() != new_owners_dir
#     assert sx.title != new_economy_title

#     # WHEN
#     rename_example_economy(economy_obj=sx, new_name=new_economy_title)

#     # THEN check contracts src directory created
#     assert os_path.exists(old_economy_dir) is False
#     assert os_path.isdir(old_economy_dir) is False
#     assert os_path.exists(old_economy_file_path) is False
#     assert os_path.exists(old_contracts_dir) is False
#     assert os_path.exists(old_owners_dir) is False
#     assert sx.get_public_dir() != old_contracts_dir
#     assert sx.get_owners_dir() != old_owners_dir

#     assert os_path.exists(new_economy_dir)
#     assert os_path.isdir(new_economy_dir)
#     assert os_path.exists(new_economy_file_path)
#     assert os_path.exists(new_contracts_dir)
#     assert os_path.exists(new_owners_dir)
#     assert sx.get_public_dir() == new_contracts_dir
#     assert sx.get_owners_dir() == new_owners_dir
#     assert sx.title == new_economy_title

#     # Undo change to directory
#     # x_func_delete_dir(dir=old_economy_dir)
#     # print(f"{old_economy_dir=}")
#     x_func_delete_dir(dir=new_economy_dir)
#     print(f"{new_economy_dir=}")


# def test_copy_evaluation_economy_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
#     # GIVEN create economy
#     old_economy_title = get_temp_env_title()
#     old_economy_dir = f"src/economy/examples/economys/{old_economy_title}"
#     old_economy_file_name = "economy.json"
#     old_economy_file_path = f"{old_economy_dir}/{old_economy_file_name}"
#     old_contracts_dir = f"{old_economy_dir}/contracts"
#     old_owners_dir = f"{old_economy_dir}/owners"

#     sx = economyunit_shop(title=old_economy_title, economys_dir=get_test_economys_dir())
#     sx.create_dirs_if_null()

#     assert os_path.exists(old_economy_dir)
#     assert os_path.isdir(old_economy_dir)
#     assert os_path.exists(old_economy_file_path)
#     assert os_path.exists(old_contracts_dir)
#     assert os_path.exists(old_owners_dir)
#     assert sx.get_public_dir() == old_contracts_dir
#     assert sx.get_owners_dir() == old_owners_dir

#     new_economy_title = "ex_env1"
#     new_economy_dir = f"src/economy/examples/economys/{new_economy_title}"
#     new_economy_file_name = "economy.json"
#     new_economy_file_path = f"{new_economy_dir}/{new_economy_file_name}"
#     new_contracts_dir = f"{new_economy_dir}/contracts"
#     new_owners_dir = f"{new_economy_dir}/owners"

#     assert os_path.exists(new_economy_dir) is False
#     assert os_path.isdir(new_economy_dir) is False
#     assert os_path.exists(new_economy_file_path) is False
#     assert os_path.exists(new_contracts_dir) is False
#     assert os_path.exists(new_owners_dir) is False
#     assert sx.get_public_dir() != new_contracts_dir
#     assert sx.get_owners_dir() != new_owners_dir
#     assert sx.title != new_economy_title

#     # WHEN
#     copy_evaluation_economy(src_title=sx.title, dest_title=new_economy_title)

#     # THEN check contracts src directory created
#     assert os_path.exists(old_economy_dir)
#     assert os_path.isdir(old_economy_dir)
#     assert os_path.exists(old_economy_file_path)
#     assert os_path.exists(old_contracts_dir)
#     assert os_path.exists(old_owners_dir)
#     assert sx.get_public_dir() == old_contracts_dir
#     assert sx.get_owners_dir() == old_owners_dir

#     assert os_path.exists(new_economy_dir)
#     assert os_path.isdir(new_economy_dir)
#     assert os_path.exists(new_economy_file_path)
#     assert os_path.exists(new_contracts_dir)
#     assert os_path.exists(new_owners_dir)
#     assert sx.get_public_dir() != new_contracts_dir
#     assert sx.get_owners_dir() != new_owners_dir
#     assert sx.title != new_economy_title

#     # Undo change to directory
#     # x_func_delete_dir(sx.get_object_root_dir())
#     # x_func_delete_dir(dir=old_economy_dir)
#     x_func_delete_dir(dir=new_economy_dir)


# def test_copy_evaluation_economy_CorrectlyRaisesError(env_dir_setup_cleanup):
#     # GIVEN create economy
#     old_economy_title = get_temp_env_title()
#     sx = economyunit_shop(title=old_economy_title, economys_dir=get_test_economys_dir())
#     sx.create_dirs_if_null()

#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         copy_evaluation_economy(src_title=sx.title, dest_title=old_economy_title)
#     assert (
#         str(excinfo.value)
#         == f"Cannot copy economy to '{sx.get_object_root_dir()}' directory because '{sx.get_object_root_dir()}' exists."
#     )


# def test_economyunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
#     # GIVEN
#     park_text = get_temp_env_title()
#     economy_dir = f"src/economy/examples/economys/{park_text}"
#     assert os_path.exists(economy_dir) is False

#     # WHEN
#     sx = economyunit_shop(title=park_text, economys_dir=get_test_economys_dir())

#     # THEN
#     assert sx != None
#     assert sx.title == park_text
#     assert os_path.exists(economy_dir)
#     assert sx._bank_db != None
