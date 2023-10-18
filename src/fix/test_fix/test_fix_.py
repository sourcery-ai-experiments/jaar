from src.deal.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.fix.fix import FixUnit, fixunit_shop
from src.fix.examples.fix_env_kit import (
    get_temp_env_handle,
    get_test_fixs_dir,
    rename_example_fix,
    copy_evaluation_fix,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_fix_exists():
    # GIVEN
    fix_handle = "test1"

    # WHEN
    x_fixunit = FixUnit(handle=fix_handle, fixs_dir=get_test_fixs_dir())

    # THEN
    assert x_fixunit.handle == fix_handle
    assert x_fixunit.fixs_dir == get_test_fixs_dir()
    assert x_fixunit._person_importance is None


def test_fix_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create fix
    fix_handle = get_temp_env_handle()
    x_fixunit = FixUnit(handle=fix_handle, fixs_dir=get_test_fixs_dir())
    print(f"{get_test_fixs_dir()=} {x_fixunit.fixs_dir=}")
    # x_func_delete_dir(x_fixunit.get_object_root_dir())
    print(f"delete {x_fixunit.get_object_root_dir()=}")
    fix_dir = f"src/fix/examples/fixs/{fix_handle}"
    fix_file_title = "fix.json"
    fix_file_path = f"{fix_dir}/{fix_file_title}"
    deals_dir = f"{fix_dir}/deals"
    remedyunits_dir = f"{fix_dir}/remedyunits"
    bank_file_title = "bank.db"
    bank_file_path = f"{fix_dir}/{bank_file_title}"

    assert os_path.exists(fix_dir) is False
    assert os_path.isdir(fix_dir) is False
    assert os_path.exists(fix_file_path) is False
    assert os_path.exists(deals_dir) is False
    assert os_path.exists(remedyunits_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    x_fixunit.create_dirs_if_null(in_memory_bank=False)

    # THEN check deals src directory created
    assert os_path.exists(fix_dir)
    assert os_path.isdir(fix_dir)
    assert os_path.exists(fix_file_path)
    assert os_path.exists(deals_dir)
    assert os_path.exists(remedyunits_dir)
    assert os_path.exists(bank_file_path)
    assert x_fixunit.get_object_root_dir() == fix_dir
    assert x_fixunit.get_public_dir() == deals_dir
    assert x_fixunit.get_remedyunits_dir() == remedyunits_dir
    assert x_fixunit.get_bank_db_path() == bank_file_path


def test_rename_example_fix_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create fix
    old_fix_handle = get_temp_env_handle()
    old_fix_dir = f"src/fix/examples/fixs/{old_fix_handle}"
    old_fix_file_title = "fix.json"
    old_fix_file_path = f"{old_fix_dir}/{old_fix_file_title}"
    old_deals_dir = f"{old_fix_dir}/deals"
    old_remedyunits_dir = f"{old_fix_dir}/remedyunits"

    new_fix_handle = "ex_env1"
    new_fix_dir = f"src/fix/examples/fixs/{new_fix_handle}"
    new_fix_file_title = "fix.json"
    new_fix_file_path = f"{new_fix_dir}/{new_fix_file_title}"
    new_deals_dir = f"{new_fix_dir}/deals"
    new_remedyunits_dir = f"{new_fix_dir}/remedyunits"
    x_func_delete_dir(dir=new_fix_dir)
    print(f"{new_fix_dir=}")

    x_fixunit = fixunit_shop(handle=old_fix_handle, fixs_dir=get_test_fixs_dir())
    # x_func_delete_dir(x_fixunit.get_object_root_dir())
    # print(f"{x_fixunit.get_object_root_dir()=}")

    x_fixunit.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_fix_dir)
    assert os_path.isdir(old_fix_dir)
    assert os_path.exists(old_fix_file_path)
    assert os_path.exists(old_deals_dir)
    assert os_path.exists(old_remedyunits_dir)
    assert x_fixunit.get_public_dir() == old_deals_dir
    assert x_fixunit.get_remedyunits_dir() == old_remedyunits_dir

    assert os_path.exists(new_fix_dir) is False
    assert os_path.isdir(new_fix_dir) is False
    assert os_path.exists(new_fix_file_path) is False
    assert os_path.exists(new_deals_dir) is False
    assert os_path.exists(new_remedyunits_dir) is False
    assert x_fixunit.get_public_dir() != new_deals_dir
    assert x_fixunit.get_remedyunits_dir() != new_remedyunits_dir
    assert x_fixunit.handle != new_fix_handle

    # WHEN
    rename_example_fix(fix_obj=x_fixunit, new_title=new_fix_handle)

    # THEN check deals src directory created
    assert os_path.exists(old_fix_dir) is False
    assert os_path.isdir(old_fix_dir) is False
    assert os_path.exists(old_fix_file_path) is False
    assert os_path.exists(old_deals_dir) is False
    assert os_path.exists(old_remedyunits_dir) is False
    assert x_fixunit.get_public_dir() != old_deals_dir
    assert x_fixunit.get_remedyunits_dir() != old_remedyunits_dir

    assert os_path.exists(new_fix_dir)
    assert os_path.isdir(new_fix_dir)
    assert os_path.exists(new_fix_file_path)
    assert os_path.exists(new_deals_dir)
    assert os_path.exists(new_remedyunits_dir)
    assert x_fixunit.get_public_dir() == new_deals_dir
    assert x_fixunit.get_remedyunits_dir() == new_remedyunits_dir
    assert x_fixunit.handle == new_fix_handle

    # Undo change to directory
    # x_func_delete_dir(dir=old_fix_dir)
    # print(f"{old_fix_dir=}")
    x_func_delete_dir(dir=new_fix_dir)
    print(f"{new_fix_dir=}")


def test_copy_evaluation_fix_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create fix
    old_fix_handle = get_temp_env_handle()
    old_fix_dir = f"src/fix/examples/fixs/{old_fix_handle}"
    old_fix_file_title = "fix.json"
    old_fix_file_path = f"{old_fix_dir}/{old_fix_file_title}"
    old_deals_dir = f"{old_fix_dir}/deals"
    old_remedyunits_dir = f"{old_fix_dir}/remedyunits"

    x_fixunit = fixunit_shop(handle=old_fix_handle, fixs_dir=get_test_fixs_dir())
    x_fixunit.create_dirs_if_null()

    assert os_path.exists(old_fix_dir)
    assert os_path.isdir(old_fix_dir)
    assert os_path.exists(old_fix_file_path)
    assert os_path.exists(old_deals_dir)
    assert os_path.exists(old_remedyunits_dir)
    assert x_fixunit.get_public_dir() == old_deals_dir
    assert x_fixunit.get_remedyunits_dir() == old_remedyunits_dir

    new_fix_handle = "ex_env1"
    new_fix_dir = f"src/fix/examples/fixs/{new_fix_handle}"
    new_fix_file_title = "fix.json"
    new_fix_file_path = f"{new_fix_dir}/{new_fix_file_title}"
    new_deals_dir = f"{new_fix_dir}/deals"
    new_remedyunits_dir = f"{new_fix_dir}/remedyunits"

    assert os_path.exists(new_fix_dir) is False
    assert os_path.isdir(new_fix_dir) is False
    assert os_path.exists(new_fix_file_path) is False
    assert os_path.exists(new_deals_dir) is False
    assert os_path.exists(new_remedyunits_dir) is False
    assert x_fixunit.get_public_dir() != new_deals_dir
    assert x_fixunit.get_remedyunits_dir() != new_remedyunits_dir
    assert x_fixunit.handle != new_fix_handle

    # WHEN
    copy_evaluation_fix(src_handle=x_fixunit.handle, dest_handle=new_fix_handle)

    # THEN check deals src directory created
    assert os_path.exists(old_fix_dir)
    assert os_path.isdir(old_fix_dir)
    assert os_path.exists(old_fix_file_path)
    assert os_path.exists(old_deals_dir)
    assert os_path.exists(old_remedyunits_dir)
    assert x_fixunit.get_public_dir() == old_deals_dir
    assert x_fixunit.get_remedyunits_dir() == old_remedyunits_dir

    assert os_path.exists(new_fix_dir)
    assert os_path.isdir(new_fix_dir)
    assert os_path.exists(new_fix_file_path)
    assert os_path.exists(new_deals_dir)
    assert os_path.exists(new_remedyunits_dir)
    assert x_fixunit.get_public_dir() != new_deals_dir
    assert x_fixunit.get_remedyunits_dir() != new_remedyunits_dir
    assert x_fixunit.handle != new_fix_handle

    # Undo change to directory
    # x_func_delete_dir(x_fixunit.get_object_root_dir())
    # x_func_delete_dir(dir=old_fix_dir)
    x_func_delete_dir(dir=new_fix_dir)


def test_copy_evaluation_fix_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create fix
    old_fix_handle = get_temp_env_handle()
    x_fixunit = fixunit_shop(handle=old_fix_handle, fixs_dir=get_test_fixs_dir())
    x_fixunit.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_fix(src_handle=x_fixunit.handle, dest_handle=old_fix_handle)
    assert (
        str(excinfo.value)
        == f"Cannot copy fix to '{x_fixunit.get_object_root_dir()}' directory because '{x_fixunit.get_object_root_dir()}' exists."
    )


def test_fixunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_handle()
    fix_dir = f"src/fix/examples/fixs/{park_text}"
    assert os_path.exists(fix_dir) is False

    # WHEN
    x_fixunit = fixunit_shop(handle=park_text, fixs_dir=get_test_fixs_dir())

    # THEN
    assert x_fixunit != None
    assert x_fixunit.handle == park_text
    assert os_path.exists(fix_dir)
    assert x_fixunit._bank_db != None
    assert x_fixunit._person_importance is None
