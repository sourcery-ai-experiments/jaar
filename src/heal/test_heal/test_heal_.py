from src.contract.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.heal.heal import HealUnit, healunit_shop
from src.heal.examples.heal_env_kit import (
    get_temp_env_kind,
    get_test_heals_dir,
    rename_example_heal,
    copy_evaluation_heal,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_heal_exists():
    heal_kind = "test1"
    sx = HealUnit(kind=heal_kind, heals_dir=get_test_heals_dir())
    assert sx.kind == heal_kind
    assert sx.heals_dir == get_test_heals_dir()


def test_heal_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create heal
    heal_kind = get_temp_env_kind()
    sx = HealUnit(kind=heal_kind, heals_dir=get_test_heals_dir())
    print(f"{get_test_heals_dir()=} {sx.heals_dir=}")
    # x_func_delete_dir(sx.get_object_root_dir())
    print(f"delete {sx.get_object_root_dir()=}")
    heal_dir = f"src/heal/examples/heals/{heal_kind}"
    heal_file_title = "heal.json"
    heal_file_path = f"{heal_dir}/{heal_file_title}"
    contracts_dir = f"{heal_dir}/contracts"
    owners_dir = f"{heal_dir}/owners"
    bank_file_title = "bank.db"
    bank_file_path = f"{heal_dir}/{bank_file_title}"

    assert os_path.exists(heal_dir) is False
    assert os_path.isdir(heal_dir) is False
    assert os_path.exists(heal_file_path) is False
    assert os_path.exists(contracts_dir) is False
    assert os_path.exists(owners_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    sx.create_dirs_if_null(in_memory_bank=False)

    # THEN check contracts src directory created
    assert os_path.exists(heal_dir)
    assert os_path.isdir(heal_dir)
    assert os_path.exists(heal_file_path)
    assert os_path.exists(contracts_dir)
    assert os_path.exists(owners_dir)
    assert os_path.exists(bank_file_path)
    assert sx.get_object_root_dir() == heal_dir
    assert sx.get_public_dir() == contracts_dir
    assert sx.get_owners_dir() == owners_dir
    assert sx.get_bank_db_path() == bank_file_path


def test_rename_example_heal_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create heal
    old_heal_kind = get_temp_env_kind()
    old_heal_dir = f"src/heal/examples/heals/{old_heal_kind}"
    old_heal_file_title = "heal.json"
    old_heal_file_path = f"{old_heal_dir}/{old_heal_file_title}"
    old_contracts_dir = f"{old_heal_dir}/contracts"
    old_owners_dir = f"{old_heal_dir}/owners"

    new_heal_kind = "ex_env1"
    new_heal_dir = f"src/heal/examples/heals/{new_heal_kind}"
    new_heal_file_title = "heal.json"
    new_heal_file_path = f"{new_heal_dir}/{new_heal_file_title}"
    new_contracts_dir = f"{new_heal_dir}/contracts"
    new_owners_dir = f"{new_heal_dir}/owners"
    x_func_delete_dir(dir=new_heal_dir)
    print(f"{new_heal_dir=}")

    sx = healunit_shop(kind=old_heal_kind, heals_dir=get_test_heals_dir())
    # x_func_delete_dir(sx.get_object_root_dir())
    # print(f"{sx.get_object_root_dir()=}")

    sx.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_heal_dir)
    assert os_path.isdir(old_heal_dir)
    assert os_path.exists(old_heal_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_owners_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_owners_dir() == old_owners_dir

    assert os_path.exists(new_heal_dir) is False
    assert os_path.isdir(new_heal_dir) is False
    assert os_path.exists(new_heal_file_path) is False
    assert os_path.exists(new_contracts_dir) is False
    assert os_path.exists(new_owners_dir) is False
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_owners_dir() != new_owners_dir
    assert sx.kind != new_heal_kind

    # WHEN
    rename_example_heal(heal_obj=sx, new_title=new_heal_kind)

    # THEN check contracts src directory created
    assert os_path.exists(old_heal_dir) is False
    assert os_path.isdir(old_heal_dir) is False
    assert os_path.exists(old_heal_file_path) is False
    assert os_path.exists(old_contracts_dir) is False
    assert os_path.exists(old_owners_dir) is False
    assert sx.get_public_dir() != old_contracts_dir
    assert sx.get_owners_dir() != old_owners_dir

    assert os_path.exists(new_heal_dir)
    assert os_path.isdir(new_heal_dir)
    assert os_path.exists(new_heal_file_path)
    assert os_path.exists(new_contracts_dir)
    assert os_path.exists(new_owners_dir)
    assert sx.get_public_dir() == new_contracts_dir
    assert sx.get_owners_dir() == new_owners_dir
    assert sx.kind == new_heal_kind

    # Undo change to directory
    # x_func_delete_dir(dir=old_heal_dir)
    # print(f"{old_heal_dir=}")
    x_func_delete_dir(dir=new_heal_dir)
    print(f"{new_heal_dir=}")


def test_copy_evaluation_heal_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create heal
    old_heal_kind = get_temp_env_kind()
    old_heal_dir = f"src/heal/examples/heals/{old_heal_kind}"
    old_heal_file_title = "heal.json"
    old_heal_file_path = f"{old_heal_dir}/{old_heal_file_title}"
    old_contracts_dir = f"{old_heal_dir}/contracts"
    old_owners_dir = f"{old_heal_dir}/owners"

    sx = healunit_shop(kind=old_heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null()

    assert os_path.exists(old_heal_dir)
    assert os_path.isdir(old_heal_dir)
    assert os_path.exists(old_heal_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_owners_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_owners_dir() == old_owners_dir

    new_heal_kind = "ex_env1"
    new_heal_dir = f"src/heal/examples/heals/{new_heal_kind}"
    new_heal_file_title = "heal.json"
    new_heal_file_path = f"{new_heal_dir}/{new_heal_file_title}"
    new_contracts_dir = f"{new_heal_dir}/contracts"
    new_owners_dir = f"{new_heal_dir}/owners"

    assert os_path.exists(new_heal_dir) is False
    assert os_path.isdir(new_heal_dir) is False
    assert os_path.exists(new_heal_file_path) is False
    assert os_path.exists(new_contracts_dir) is False
    assert os_path.exists(new_owners_dir) is False
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_owners_dir() != new_owners_dir
    assert sx.kind != new_heal_kind

    # WHEN
    copy_evaluation_heal(src_kind=sx.kind, dest_kind=new_heal_kind)

    # THEN check contracts src directory created
    assert os_path.exists(old_heal_dir)
    assert os_path.isdir(old_heal_dir)
    assert os_path.exists(old_heal_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_owners_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_owners_dir() == old_owners_dir

    assert os_path.exists(new_heal_dir)
    assert os_path.isdir(new_heal_dir)
    assert os_path.exists(new_heal_file_path)
    assert os_path.exists(new_contracts_dir)
    assert os_path.exists(new_owners_dir)
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_owners_dir() != new_owners_dir
    assert sx.kind != new_heal_kind

    # Undo change to directory
    # x_func_delete_dir(sx.get_object_root_dir())
    # x_func_delete_dir(dir=old_heal_dir)
    x_func_delete_dir(dir=new_heal_dir)


def test_copy_evaluation_heal_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create heal
    old_heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=old_heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_heal(src_kind=sx.kind, dest_kind=old_heal_kind)
    assert (
        str(excinfo.value)
        == f"Cannot copy heal to '{sx.get_object_root_dir()}' directory because '{sx.get_object_root_dir()}' exists."
    )


def test_healunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_kind()
    heal_dir = f"src/heal/examples/heals/{park_text}"
    assert os_path.exists(heal_dir) is False

    # WHEN
    sx = healunit_shop(kind=park_text, heals_dir=get_test_heals_dir())

    # THEN
    assert sx != None
    assert sx.kind == park_text
    assert os_path.exists(heal_dir)
    assert sx._bank_db != None
