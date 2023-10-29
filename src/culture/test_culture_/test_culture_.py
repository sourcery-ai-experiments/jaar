from src.agenda.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.culture.culture import CultureUnit, cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    get_test_cultures_dir,
    rename_example_culture,
    copy_evaluation_culture,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_culture_exists():
    # GIVEN
    x_handle = "test1"

    # WHEN
    x_culture = CultureUnit(handle=x_handle, cultures_dir=get_test_cultures_dir())

    # THEN
    assert x_culture.handle == x_handle
    assert x_culture.cultures_dir == get_test_cultures_dir()
    assert x_culture._manager_name is None


def test_culture_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create culture
    x_handle = get_temp_env_handle()
    x_culture = CultureUnit(handle=x_handle, cultures_dir=get_test_cultures_dir())
    print(f"{get_test_cultures_dir()=} {x_culture.cultures_dir=}")
    # x_func_delete_dir(x_culture.get_object_root_dir())
    print(f"delete {x_culture.get_object_root_dir()=}")
    culture_dir = f"src/culture/examples/cultures/{x_handle}"
    culture_file_name = "culture.json"
    culture_file_path = f"{culture_dir}/{culture_file_name}"
    agendas_dir = f"{culture_dir}/agendas"
    councilunits_dir = f"{culture_dir}/councilunits"
    bank_file_name = "bank.db"
    bank_file_path = f"{culture_dir}/{bank_file_name}"

    assert os_path.exists(culture_dir) is False
    assert os_path.isdir(culture_dir) is False
    assert os_path.exists(culture_file_path) is False
    assert os_path.exists(agendas_dir) is False
    assert os_path.exists(councilunits_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    x_culture.create_dirs_if_null(in_memory_bank=False)

    # THEN check agendas src directory created
    assert os_path.exists(culture_dir)
    assert os_path.isdir(culture_dir)
    assert os_path.exists(culture_file_path)
    assert os_path.exists(agendas_dir)
    assert os_path.exists(councilunits_dir)
    assert os_path.exists(bank_file_path)
    assert x_culture.get_object_root_dir() == culture_dir
    assert x_culture.get_public_dir() == agendas_dir
    assert x_culture.get_councilunits_dir() == councilunits_dir
    assert x_culture.get_bank_db_path() == bank_file_path


def test_rename_example_culture_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create culture
    old_x_handle = get_temp_env_handle()
    old_culture_dir = f"src/culture/examples/cultures/{old_x_handle}"
    old_culture_file_name = "culture.json"
    old_culture_file_path = f"{old_culture_dir}/{old_culture_file_name}"
    old_agendas_dir = f"{old_culture_dir}/agendas"
    old_councilunits_dir = f"{old_culture_dir}/councilunits"

    new_x_handle = "ex_env1"
    new_culture_dir = f"src/culture/examples/cultures/{new_x_handle}"
    new_culture_file_name = "culture.json"
    new_culture_file_path = f"{new_culture_dir}/{new_culture_file_name}"
    new_agendas_dir = f"{new_culture_dir}/agendas"
    new_councilunits_dir = f"{new_culture_dir}/councilunits"
    x_func_delete_dir(dir=new_culture_dir)
    print(f"{new_culture_dir=}")

    x_culture = cultureunit_shop(
        handle=old_x_handle, cultures_dir=get_test_cultures_dir()
    )
    # x_func_delete_dir(x_culture.get_object_root_dir())
    # print(f"{x_culture.get_object_root_dir()=}")

    x_culture.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_culture_dir)
    assert os_path.isdir(old_culture_dir)
    assert os_path.exists(old_culture_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_councilunits_dir)
    assert x_culture.get_public_dir() == old_agendas_dir
    assert x_culture.get_councilunits_dir() == old_councilunits_dir

    assert os_path.exists(new_culture_dir) is False
    assert os_path.isdir(new_culture_dir) is False
    assert os_path.exists(new_culture_file_path) is False
    assert os_path.exists(new_agendas_dir) is False
    assert os_path.exists(new_councilunits_dir) is False
    assert x_culture.get_public_dir() != new_agendas_dir
    assert x_culture.get_councilunits_dir() != new_councilunits_dir
    assert x_culture.handle != new_x_handle

    # WHEN
    rename_example_culture(culture_obj=x_culture, new_handle=new_x_handle)

    # THEN check agendas src directory created
    assert os_path.exists(old_culture_dir) is False
    assert os_path.isdir(old_culture_dir) is False
    assert os_path.exists(old_culture_file_path) is False
    assert os_path.exists(old_agendas_dir) is False
    assert os_path.exists(old_councilunits_dir) is False
    assert x_culture.get_public_dir() != old_agendas_dir
    assert x_culture.get_councilunits_dir() != old_councilunits_dir

    assert os_path.exists(new_culture_dir)
    assert os_path.isdir(new_culture_dir)
    assert os_path.exists(new_culture_file_path)
    assert os_path.exists(new_agendas_dir)
    assert os_path.exists(new_councilunits_dir)
    assert x_culture.get_public_dir() == new_agendas_dir
    assert x_culture.get_councilunits_dir() == new_councilunits_dir
    assert x_culture.handle == new_x_handle

    # Undo change to directory
    # x_func_delete_dir(dir=old_culture_dir)
    # print(f"{old_culture_dir=}")
    x_func_delete_dir(dir=new_culture_dir)
    print(f"{new_culture_dir=}")


def test_copy_evaluation_culture_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create culture
    old_x_handle = get_temp_env_handle()
    old_culture_dir = f"src/culture/examples/cultures/{old_x_handle}"
    old_culture_file_name = "culture.json"
    old_culture_file_path = f"{old_culture_dir}/{old_culture_file_name}"
    old_agendas_dir = f"{old_culture_dir}/agendas"
    old_councilunits_dir = f"{old_culture_dir}/councilunits"

    x_culture = cultureunit_shop(old_x_handle, get_test_cultures_dir())
    x_culture.create_dirs_if_null()

    assert os_path.exists(old_culture_dir)
    assert os_path.isdir(old_culture_dir)
    assert os_path.exists(old_culture_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_councilunits_dir)
    assert x_culture.get_public_dir() == old_agendas_dir
    assert x_culture.get_councilunits_dir() == old_councilunits_dir

    new_x_handle = "ex_env1"
    new_culture_dir = f"src/culture/examples/cultures/{new_x_handle}"
    new_culture_file_name = "culture.json"
    new_culture_file_path = f"{new_culture_dir}/{new_culture_file_name}"
    new_agendas_dir = f"{new_culture_dir}/agendas"
    new_councilunits_dir = f"{new_culture_dir}/councilunits"

    assert os_path.exists(new_culture_dir) is False
    assert os_path.isdir(new_culture_dir) is False
    assert os_path.exists(new_culture_file_path) is False
    assert os_path.exists(new_agendas_dir) is False
    assert os_path.exists(new_councilunits_dir) is False
    assert x_culture.get_public_dir() != new_agendas_dir
    assert x_culture.get_councilunits_dir() != new_councilunits_dir
    assert x_culture.handle != new_x_handle

    # WHEN
    copy_evaluation_culture(src_handle=x_culture.handle, dest_handle=new_x_handle)

    # THEN check agendas src directory created
    assert os_path.exists(old_culture_dir)
    assert os_path.isdir(old_culture_dir)
    assert os_path.exists(old_culture_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_councilunits_dir)
    assert x_culture.get_public_dir() == old_agendas_dir
    assert x_culture.get_councilunits_dir() == old_councilunits_dir

    assert os_path.exists(new_culture_dir)
    assert os_path.isdir(new_culture_dir)
    assert os_path.exists(new_culture_file_path)
    assert os_path.exists(new_agendas_dir)
    assert os_path.exists(new_councilunits_dir)
    assert x_culture.get_public_dir() != new_agendas_dir
    assert x_culture.get_councilunits_dir() != new_councilunits_dir
    assert x_culture.handle != new_x_handle

    # Undo change to directory
    # x_func_delete_dir(x_culture.get_object_root_dir())
    # x_func_delete_dir(dir=old_culture_dir)
    x_func_delete_dir(dir=new_culture_dir)


def test_copy_evaluation_culture_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create culture
    old_x_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(old_x_handle, get_test_cultures_dir())
    x_culture.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_culture(src_handle=x_culture.handle, dest_handle=old_x_handle)
    assert (
        str(excinfo.value)
        == f"Cannot copy culture to '{x_culture.get_object_root_dir()}' directory because '{x_culture.get_object_root_dir()}' exists."
    )


def test_cultureunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_handle = get_temp_env_handle()
    culture_dir = f"src/culture/examples/cultures/{x_handle}"
    sue_text = "Sue"
    assert os_path.exists(culture_dir) is False

    # WHEN
    x_culture = cultureunit_shop(
        handle=x_handle, cultures_dir=get_test_cultures_dir(), _manager_name=sue_text
    )

    # THEN
    assert x_culture != None
    assert x_culture.handle == x_handle
    assert os_path.exists(culture_dir)
    assert x_culture._bank_db != None
    assert x_culture._manager_name == sue_text


def test_cultureunit_set_manager_name_CorrectsSetsData(env_dir_setup_cleanup):
    # GIVEN
    x_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(handle=x_handle, cultures_dir=get_test_cultures_dir())
    assert x_culture.handle == x_handle
    assert x_culture._manager_name is None

    # WHEN
    zuo_text = "Zuo"
    x_culture.set_manager_name(zuo_text)

    # THEN
    assert x_culture._manager_name == zuo_text
