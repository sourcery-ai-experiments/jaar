from src.contract.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.healing.healing import HealingUnit, healingunit_shop
from src.healing.examples.healing_env_kit import (
    get_temp_env_handle,
    get_test_healings_dir,
    rename_example_healing,
    copy_evaluation_healing,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_healing_exists():
    healing_handle = "test1"
    sx = HealingUnit(handle=healing_handle, healings_dir=get_test_healings_dir())
    assert sx.handle == healing_handle
    assert sx.healings_dir == get_test_healings_dir()


def test_healing_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create healing
    healing_handle = get_temp_env_handle()
    sx = HealingUnit(handle=healing_handle, healings_dir=get_test_healings_dir())
    print(f"{get_test_healings_dir()=} {sx.healings_dir=}")
    # x_func_delete_dir(sx.get_object_root_dir())
    print(f"delete {sx.get_object_root_dir()=}")
    healing_dir = f"src/healing/examples/healings/{healing_handle}"
    healing_file_title = "healing.json"
    healing_file_path = f"{healing_dir}/{healing_file_title}"
    contracts_dir = f"{healing_dir}/contracts"
    healers_dir = f"{healing_dir}/healers"
    bank_file_title = "bank.db"
    bank_file_path = f"{healing_dir}/{bank_file_title}"

    assert os_path.exists(healing_dir) is False
    assert os_path.isdir(healing_dir) is False
    assert os_path.exists(healing_file_path) is False
    assert os_path.exists(contracts_dir) is False
    assert os_path.exists(healers_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    sx.create_dirs_if_null(in_memory_bank=False)

    # THEN check contracts src directory created
    assert os_path.exists(healing_dir)
    assert os_path.isdir(healing_dir)
    assert os_path.exists(healing_file_path)
    assert os_path.exists(contracts_dir)
    assert os_path.exists(healers_dir)
    assert os_path.exists(bank_file_path)
    assert sx.get_object_root_dir() == healing_dir
    assert sx.get_public_dir() == contracts_dir
    assert sx.get_healers_dir() == healers_dir
    assert sx.get_bank_db_path() == bank_file_path


def test_rename_example_healing_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create healing
    old_healing_handle = get_temp_env_handle()
    old_healing_dir = f"src/healing/examples/healings/{old_healing_handle}"
    old_healing_file_title = "healing.json"
    old_healing_file_path = f"{old_healing_dir}/{old_healing_file_title}"
    old_contracts_dir = f"{old_healing_dir}/contracts"
    old_healers_dir = f"{old_healing_dir}/healers"

    new_healing_handle = "ex_env1"
    new_healing_dir = f"src/healing/examples/healings/{new_healing_handle}"
    new_healing_file_title = "healing.json"
    new_healing_file_path = f"{new_healing_dir}/{new_healing_file_title}"
    new_contracts_dir = f"{new_healing_dir}/contracts"
    new_healers_dir = f"{new_healing_dir}/healers"
    x_func_delete_dir(dir=new_healing_dir)
    print(f"{new_healing_dir=}")

    sx = healingunit_shop(
        handle=old_healing_handle, healings_dir=get_test_healings_dir()
    )
    # x_func_delete_dir(sx.get_object_root_dir())
    # print(f"{sx.get_object_root_dir()=}")

    sx.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_healing_dir)
    assert os_path.isdir(old_healing_dir)
    assert os_path.exists(old_healing_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_healers_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_healers_dir() == old_healers_dir

    assert os_path.exists(new_healing_dir) is False
    assert os_path.isdir(new_healing_dir) is False
    assert os_path.exists(new_healing_file_path) is False
    assert os_path.exists(new_contracts_dir) is False
    assert os_path.exists(new_healers_dir) is False
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_healers_dir() != new_healers_dir
    assert sx.handle != new_healing_handle

    # WHEN
    rename_example_healing(healing_obj=sx, new_title=new_healing_handle)

    # THEN check contracts src directory created
    assert os_path.exists(old_healing_dir) is False
    assert os_path.isdir(old_healing_dir) is False
    assert os_path.exists(old_healing_file_path) is False
    assert os_path.exists(old_contracts_dir) is False
    assert os_path.exists(old_healers_dir) is False
    assert sx.get_public_dir() != old_contracts_dir
    assert sx.get_healers_dir() != old_healers_dir

    assert os_path.exists(new_healing_dir)
    assert os_path.isdir(new_healing_dir)
    assert os_path.exists(new_healing_file_path)
    assert os_path.exists(new_contracts_dir)
    assert os_path.exists(new_healers_dir)
    assert sx.get_public_dir() == new_contracts_dir
    assert sx.get_healers_dir() == new_healers_dir
    assert sx.handle == new_healing_handle

    # Undo change to directory
    # x_func_delete_dir(dir=old_healing_dir)
    # print(f"{old_healing_dir=}")
    x_func_delete_dir(dir=new_healing_dir)
    print(f"{new_healing_dir=}")


def test_copy_evaluation_healing_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create healing
    old_healing_handle = get_temp_env_handle()
    old_healing_dir = f"src/healing/examples/healings/{old_healing_handle}"
    old_healing_file_title = "healing.json"
    old_healing_file_path = f"{old_healing_dir}/{old_healing_file_title}"
    old_contracts_dir = f"{old_healing_dir}/contracts"
    old_healers_dir = f"{old_healing_dir}/healers"

    sx = healingunit_shop(
        handle=old_healing_handle, healings_dir=get_test_healings_dir()
    )
    sx.create_dirs_if_null()

    assert os_path.exists(old_healing_dir)
    assert os_path.isdir(old_healing_dir)
    assert os_path.exists(old_healing_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_healers_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_healers_dir() == old_healers_dir

    new_healing_handle = "ex_env1"
    new_healing_dir = f"src/healing/examples/healings/{new_healing_handle}"
    new_healing_file_title = "healing.json"
    new_healing_file_path = f"{new_healing_dir}/{new_healing_file_title}"
    new_contracts_dir = f"{new_healing_dir}/contracts"
    new_healers_dir = f"{new_healing_dir}/healers"

    assert os_path.exists(new_healing_dir) is False
    assert os_path.isdir(new_healing_dir) is False
    assert os_path.exists(new_healing_file_path) is False
    assert os_path.exists(new_contracts_dir) is False
    assert os_path.exists(new_healers_dir) is False
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_healers_dir() != new_healers_dir
    assert sx.handle != new_healing_handle

    # WHEN
    copy_evaluation_healing(src_handle=sx.handle, dest_handle=new_healing_handle)

    # THEN check contracts src directory created
    assert os_path.exists(old_healing_dir)
    assert os_path.isdir(old_healing_dir)
    assert os_path.exists(old_healing_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_healers_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_healers_dir() == old_healers_dir

    assert os_path.exists(new_healing_dir)
    assert os_path.isdir(new_healing_dir)
    assert os_path.exists(new_healing_file_path)
    assert os_path.exists(new_contracts_dir)
    assert os_path.exists(new_healers_dir)
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_healers_dir() != new_healers_dir
    assert sx.handle != new_healing_handle

    # Undo change to directory
    # x_func_delete_dir(sx.get_object_root_dir())
    # x_func_delete_dir(dir=old_healing_dir)
    x_func_delete_dir(dir=new_healing_dir)


def test_copy_evaluation_healing_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create healing
    old_healing_handle = get_temp_env_handle()
    sx = healingunit_shop(
        handle=old_healing_handle, healings_dir=get_test_healings_dir()
    )
    sx.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_healing(src_handle=sx.handle, dest_handle=old_healing_handle)
    assert (
        str(excinfo.value)
        == f"Cannot copy healing to '{sx.get_object_root_dir()}' directory because '{sx.get_object_root_dir()}' exists."
    )


def test_healingunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_handle()
    healing_dir = f"src/healing/examples/healings/{park_text}"
    assert os_path.exists(healing_dir) is False

    # WHEN
    sx = healingunit_shop(handle=park_text, healings_dir=get_test_healings_dir())

    # THEN
    assert sx != None
    assert sx.handle == park_text
    assert os_path.exists(healing_dir)
    assert sx._bank_db != None
