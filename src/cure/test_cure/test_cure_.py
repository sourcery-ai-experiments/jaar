from src.deal.x_func import delete_dir as x_func_delete_dir
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
    # GIVEN
    cure_handle = "test1"

    # WHEN
    x_cureunit = CureUnit(handle=cure_handle, cures_dir=get_test_cures_dir())

    # THEN
    assert x_cureunit.handle == cure_handle
    assert x_cureunit.cures_dir == get_test_cures_dir()
    assert x_cureunit._person_importance is None


def test_cure_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create cure
    cure_handle = get_temp_env_handle()
    x_cureunit = CureUnit(handle=cure_handle, cures_dir=get_test_cures_dir())
    print(f"{get_test_cures_dir()=} {x_cureunit.cures_dir=}")
    # x_func_delete_dir(x_cureunit.get_object_root_dir())
    print(f"delete {x_cureunit.get_object_root_dir()=}")
    cure_dir = f"src/cure/examples/cures/{cure_handle}"
    cure_file_title = "cure.json"
    cure_file_path = f"{cure_dir}/{cure_file_title}"
    deals_dir = f"{cure_dir}/deals"
    healingunits_dir = f"{cure_dir}/healingunits"
    bank_file_title = "bank.db"
    bank_file_path = f"{cure_dir}/{bank_file_title}"

    assert os_path.exists(cure_dir) is False
    assert os_path.isdir(cure_dir) is False
    assert os_path.exists(cure_file_path) is False
    assert os_path.exists(deals_dir) is False
    assert os_path.exists(healingunits_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    x_cureunit.create_dirs_if_null(in_memory_bank=False)

    # THEN check deals src directory created
    assert os_path.exists(cure_dir)
    assert os_path.isdir(cure_dir)
    assert os_path.exists(cure_file_path)
    assert os_path.exists(deals_dir)
    assert os_path.exists(healingunits_dir)
    assert os_path.exists(bank_file_path)
    assert x_cureunit.get_object_root_dir() == cure_dir
    assert x_cureunit.get_public_dir() == deals_dir
    assert x_cureunit.get_healingunits_dir() == healingunits_dir
    assert x_cureunit.get_bank_db_path() == bank_file_path


def test_rename_example_cure_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create cure
    old_cure_handle = get_temp_env_handle()
    old_cure_dir = f"src/cure/examples/cures/{old_cure_handle}"
    old_cure_file_title = "cure.json"
    old_cure_file_path = f"{old_cure_dir}/{old_cure_file_title}"
    old_deals_dir = f"{old_cure_dir}/deals"
    old_healingunits_dir = f"{old_cure_dir}/healingunits"

    new_cure_handle = "ex_env1"
    new_cure_dir = f"src/cure/examples/cures/{new_cure_handle}"
    new_cure_file_title = "cure.json"
    new_cure_file_path = f"{new_cure_dir}/{new_cure_file_title}"
    new_deals_dir = f"{new_cure_dir}/deals"
    new_healingunits_dir = f"{new_cure_dir}/healingunits"
    x_func_delete_dir(dir=new_cure_dir)
    print(f"{new_cure_dir=}")

    x_cureunit = cureunit_shop(handle=old_cure_handle, cures_dir=get_test_cures_dir())
    # x_func_delete_dir(x_cureunit.get_object_root_dir())
    # print(f"{x_cureunit.get_object_root_dir()=}")

    x_cureunit.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_cure_dir)
    assert os_path.isdir(old_cure_dir)
    assert os_path.exists(old_cure_file_path)
    assert os_path.exists(old_deals_dir)
    assert os_path.exists(old_healingunits_dir)
    assert x_cureunit.get_public_dir() == old_deals_dir
    assert x_cureunit.get_healingunits_dir() == old_healingunits_dir

    assert os_path.exists(new_cure_dir) is False
    assert os_path.isdir(new_cure_dir) is False
    assert os_path.exists(new_cure_file_path) is False
    assert os_path.exists(new_deals_dir) is False
    assert os_path.exists(new_healingunits_dir) is False
    assert x_cureunit.get_public_dir() != new_deals_dir
    assert x_cureunit.get_healingunits_dir() != new_healingunits_dir
    assert x_cureunit.handle != new_cure_handle

    # WHEN
    rename_example_cure(cure_obj=x_cureunit, new_title=new_cure_handle)

    # THEN check deals src directory created
    assert os_path.exists(old_cure_dir) is False
    assert os_path.isdir(old_cure_dir) is False
    assert os_path.exists(old_cure_file_path) is False
    assert os_path.exists(old_deals_dir) is False
    assert os_path.exists(old_healingunits_dir) is False
    assert x_cureunit.get_public_dir() != old_deals_dir
    assert x_cureunit.get_healingunits_dir() != old_healingunits_dir

    assert os_path.exists(new_cure_dir)
    assert os_path.isdir(new_cure_dir)
    assert os_path.exists(new_cure_file_path)
    assert os_path.exists(new_deals_dir)
    assert os_path.exists(new_healingunits_dir)
    assert x_cureunit.get_public_dir() == new_deals_dir
    assert x_cureunit.get_healingunits_dir() == new_healingunits_dir
    assert x_cureunit.handle == new_cure_handle

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
    old_deals_dir = f"{old_cure_dir}/deals"
    old_healingunits_dir = f"{old_cure_dir}/healingunits"

    x_cureunit = cureunit_shop(handle=old_cure_handle, cures_dir=get_test_cures_dir())
    x_cureunit.create_dirs_if_null()

    assert os_path.exists(old_cure_dir)
    assert os_path.isdir(old_cure_dir)
    assert os_path.exists(old_cure_file_path)
    assert os_path.exists(old_deals_dir)
    assert os_path.exists(old_healingunits_dir)
    assert x_cureunit.get_public_dir() == old_deals_dir
    assert x_cureunit.get_healingunits_dir() == old_healingunits_dir

    new_cure_handle = "ex_env1"
    new_cure_dir = f"src/cure/examples/cures/{new_cure_handle}"
    new_cure_file_title = "cure.json"
    new_cure_file_path = f"{new_cure_dir}/{new_cure_file_title}"
    new_deals_dir = f"{new_cure_dir}/deals"
    new_healingunits_dir = f"{new_cure_dir}/healingunits"

    assert os_path.exists(new_cure_dir) is False
    assert os_path.isdir(new_cure_dir) is False
    assert os_path.exists(new_cure_file_path) is False
    assert os_path.exists(new_deals_dir) is False
    assert os_path.exists(new_healingunits_dir) is False
    assert x_cureunit.get_public_dir() != new_deals_dir
    assert x_cureunit.get_healingunits_dir() != new_healingunits_dir
    assert x_cureunit.handle != new_cure_handle

    # WHEN
    copy_evaluation_cure(src_handle=x_cureunit.handle, dest_handle=new_cure_handle)

    # THEN check deals src directory created
    assert os_path.exists(old_cure_dir)
    assert os_path.isdir(old_cure_dir)
    assert os_path.exists(old_cure_file_path)
    assert os_path.exists(old_deals_dir)
    assert os_path.exists(old_healingunits_dir)
    assert x_cureunit.get_public_dir() == old_deals_dir
    assert x_cureunit.get_healingunits_dir() == old_healingunits_dir

    assert os_path.exists(new_cure_dir)
    assert os_path.isdir(new_cure_dir)
    assert os_path.exists(new_cure_file_path)
    assert os_path.exists(new_deals_dir)
    assert os_path.exists(new_healingunits_dir)
    assert x_cureunit.get_public_dir() != new_deals_dir
    assert x_cureunit.get_healingunits_dir() != new_healingunits_dir
    assert x_cureunit.handle != new_cure_handle

    # Undo change to directory
    # x_func_delete_dir(x_cureunit.get_object_root_dir())
    # x_func_delete_dir(dir=old_cure_dir)
    x_func_delete_dir(dir=new_cure_dir)


def test_copy_evaluation_cure_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create cure
    old_cure_handle = get_temp_env_handle()
    x_cureunit = cureunit_shop(handle=old_cure_handle, cures_dir=get_test_cures_dir())
    x_cureunit.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_cure(src_handle=x_cureunit.handle, dest_handle=old_cure_handle)
    assert (
        str(excinfo.value)
        == f"Cannot copy cure to '{x_cureunit.get_object_root_dir()}' directory because '{x_cureunit.get_object_root_dir()}' exists."
    )


def test_cureunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_handle()
    cure_dir = f"src/cure/examples/cures/{park_text}"
    assert os_path.exists(cure_dir) is False

    # WHEN
    x_cureunit = cureunit_shop(handle=park_text, cures_dir=get_test_cures_dir())

    # THEN
    assert x_cureunit != None
    assert x_cureunit.handle == park_text
    assert os_path.exists(cure_dir)
    assert x_cureunit._bank_db != None
    assert x_cureunit._person_importance is None
