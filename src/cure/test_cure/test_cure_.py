from src.contract.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.cure.cure import CureUnit, cureunit_shop
from src.cure.examples.cure_env_kit import (
    get_temp_env_handle,
    get_test_cures_dir,
    rename_example_cure,
    copy_evaluation_cure,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_cure_exists():
    cure_handle = "test1"
    sx = CureUnit(handle=cure_handle, cures_dir=get_test_cures_dir())
    assert sx.handle == cure_handle
    assert sx.cures_dir == get_test_cures_dir()


def test_cure_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create cure
    cure_handle = get_temp_env_handle()
    sx = CureUnit(handle=cure_handle, cures_dir=get_test_cures_dir())
    print(f"{get_test_cures_dir()=} {sx.cures_dir=}")
    # x_func_delete_dir(sx.get_object_root_dir())
    print(f"delete {sx.get_object_root_dir()=}")
    cure_dir = f"src/cure/examples/cures/{cure_handle}"
    cure_file_title = "cure.json"
    cure_file_path = f"{cure_dir}/{cure_file_title}"
    contracts_dir = f"{cure_dir}/contracts"
    healers_dir = f"{cure_dir}/healers"
    bank_file_title = "bank.db"
    bank_file_path = f"{cure_dir}/{bank_file_title}"

    assert os_path.exists(cure_dir) is False
    assert os_path.isdir(cure_dir) is False
    assert os_path.exists(cure_file_path) is False
    assert os_path.exists(contracts_dir) is False
    assert os_path.exists(healers_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    sx.create_dirs_if_null(in_memory_bank=False)

    # THEN check contracts src directory created
    assert os_path.exists(cure_dir)
    assert os_path.isdir(cure_dir)
    assert os_path.exists(cure_file_path)
    assert os_path.exists(contracts_dir)
    assert os_path.exists(healers_dir)
    assert os_path.exists(bank_file_path)
    assert sx.get_object_root_dir() == cure_dir
    assert sx.get_public_dir() == contracts_dir
    assert sx.get_healers_dir() == healers_dir
    assert sx.get_bank_db_path() == bank_file_path


def test_rename_example_cure_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create cure
    old_cure_handle = get_temp_env_handle()
    old_cure_dir = f"src/cure/examples/cures/{old_cure_handle}"
    old_cure_file_title = "cure.json"
    old_cure_file_path = f"{old_cure_dir}/{old_cure_file_title}"
    old_contracts_dir = f"{old_cure_dir}/contracts"
    old_healers_dir = f"{old_cure_dir}/healers"

    new_cure_handle = "ex_env1"
    new_cure_dir = f"src/cure/examples/cures/{new_cure_handle}"
    new_cure_file_title = "cure.json"
    new_cure_file_path = f"{new_cure_dir}/{new_cure_file_title}"
    new_contracts_dir = f"{new_cure_dir}/contracts"
    new_healers_dir = f"{new_cure_dir}/healers"
    x_func_delete_dir(dir=new_cure_dir)
    print(f"{new_cure_dir=}")

    sx = cureunit_shop(handle=old_cure_handle, cures_dir=get_test_cures_dir())
    # x_func_delete_dir(sx.get_object_root_dir())
    # print(f"{sx.get_object_root_dir()=}")

    sx.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_cure_dir)
    assert os_path.isdir(old_cure_dir)
    assert os_path.exists(old_cure_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_healers_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_healers_dir() == old_healers_dir

    assert os_path.exists(new_cure_dir) is False
    assert os_path.isdir(new_cure_dir) is False
    assert os_path.exists(new_cure_file_path) is False
    assert os_path.exists(new_contracts_dir) is False
    assert os_path.exists(new_healers_dir) is False
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_healers_dir() != new_healers_dir
    assert sx.handle != new_cure_handle

    # WHEN
    rename_example_cure(cure_obj=sx, new_title=new_cure_handle)

    # THEN check contracts src directory created
    assert os_path.exists(old_cure_dir) is False
    assert os_path.isdir(old_cure_dir) is False
    assert os_path.exists(old_cure_file_path) is False
    assert os_path.exists(old_contracts_dir) is False
    assert os_path.exists(old_healers_dir) is False
    assert sx.get_public_dir() != old_contracts_dir
    assert sx.get_healers_dir() != old_healers_dir

    assert os_path.exists(new_cure_dir)
    assert os_path.isdir(new_cure_dir)
    assert os_path.exists(new_cure_file_path)
    assert os_path.exists(new_contracts_dir)
    assert os_path.exists(new_healers_dir)
    assert sx.get_public_dir() == new_contracts_dir
    assert sx.get_healers_dir() == new_healers_dir
    assert sx.handle == new_cure_handle

    # Undo change to directory
    # x_func_delete_dir(dir=old_cure_dir)
    # print(f"{old_cure_dir=}")
    x_func_delete_dir(dir=new_cure_dir)
    print(f"{new_cure_dir=}")


def test_copy_evaluation_cure_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create cure
    old_cure_handle = get_temp_env_handle()
    old_cure_dir = f"src/cure/examples/cures/{old_cure_handle}"
    old_cure_file_title = "cure.json"
    old_cure_file_path = f"{old_cure_dir}/{old_cure_file_title}"
    old_contracts_dir = f"{old_cure_dir}/contracts"
    old_healers_dir = f"{old_cure_dir}/healers"

    sx = cureunit_shop(handle=old_cure_handle, cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null()

    assert os_path.exists(old_cure_dir)
    assert os_path.isdir(old_cure_dir)
    assert os_path.exists(old_cure_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_healers_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_healers_dir() == old_healers_dir

    new_cure_handle = "ex_env1"
    new_cure_dir = f"src/cure/examples/cures/{new_cure_handle}"
    new_cure_file_title = "cure.json"
    new_cure_file_path = f"{new_cure_dir}/{new_cure_file_title}"
    new_contracts_dir = f"{new_cure_dir}/contracts"
    new_healers_dir = f"{new_cure_dir}/healers"

    assert os_path.exists(new_cure_dir) is False
    assert os_path.isdir(new_cure_dir) is False
    assert os_path.exists(new_cure_file_path) is False
    assert os_path.exists(new_contracts_dir) is False
    assert os_path.exists(new_healers_dir) is False
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_healers_dir() != new_healers_dir
    assert sx.handle != new_cure_handle

    # WHEN
    copy_evaluation_cure(src_handle=sx.handle, dest_handle=new_cure_handle)

    # THEN check contracts src directory created
    assert os_path.exists(old_cure_dir)
    assert os_path.isdir(old_cure_dir)
    assert os_path.exists(old_cure_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_healers_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_healers_dir() == old_healers_dir

    assert os_path.exists(new_cure_dir)
    assert os_path.isdir(new_cure_dir)
    assert os_path.exists(new_cure_file_path)
    assert os_path.exists(new_contracts_dir)
    assert os_path.exists(new_healers_dir)
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_healers_dir() != new_healers_dir
    assert sx.handle != new_cure_handle

    # Undo change to directory
    # x_func_delete_dir(sx.get_object_root_dir())
    # x_func_delete_dir(dir=old_cure_dir)
    x_func_delete_dir(dir=new_cure_dir)


def test_copy_evaluation_cure_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create cure
    old_cure_handle = get_temp_env_handle()
    sx = cureunit_shop(handle=old_cure_handle, cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_cure(src_handle=sx.handle, dest_handle=old_cure_handle)
    assert (
        str(excinfo.value)
        == f"Cannot copy cure to '{sx.get_object_root_dir()}' directory because '{sx.get_object_root_dir()}' exists."
    )


def test_cureunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_handle()
    cure_dir = f"src/cure/examples/cures/{park_text}"
    assert os_path.exists(cure_dir) is False

    # WHEN
    sx = cureunit_shop(handle=park_text, cures_dir=get_test_cures_dir())

    # THEN
    assert sx != None
    assert sx.handle == park_text
    assert os_path.exists(cure_dir)
    assert sx._bank_db != None
