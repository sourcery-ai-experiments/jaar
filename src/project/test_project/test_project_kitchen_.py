from src.project.project import projectunit_shop
from src.project.kitchen import kitchenunit_shop
from src.project.examples.project_env_kit import (
    get_temp_env_dir,
    get_temp_env_handle,
    env_dir_setup_cleanup,
    get_test_projects_dir,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_project_set_healer_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    project_handle = get_temp_env_handle()
    sx = projectunit_shop(handle=project_handle, projects_dir=get_test_projects_dir())
    print(f"create env '{project_handle}' directories.")
    sx.create_dirs_if_null(in_memory_bank=True)
    timmy_text = "timmy"
    wx_path = f"{sx.get_kitchenunits_dir()}/{timmy_text}"
    print(f"{wx_path=}")
    assert os_path.exists(wx_path) == False

    # WHEN
    sx.create_new_kitchenunit(kitchen_title=timmy_text)

    # THEN
    print(f"{wx_path=}")
    assert os_path.exists(wx_path)


def test_project_create_kitchenunit_from_public_RaisesErrorWhenHealerDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    project_handle = get_temp_env_handle()
    sx = projectunit_shop(handle=project_handle, projects_dir=get_test_projects_dir())

    # WHEN / THEN
    bobs_text = "bobs wurld"
    with pytest_raises(Exception) as excinfo:
        sx.create_kitchenunit_from_public(title=bobs_text)
    assert (
        str(excinfo.value)
        == f"Could not load file {sx.get_public_dir()}/{bobs_text}.json (2, 'No such file or directory')"
    )


def test_project_rename_kitchenunit_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    project_handle = get_temp_env_handle()
    e5 = projectunit_shop(handle=project_handle, projects_dir=get_test_projects_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{e5.get_kitchenunits_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/seed_deal.json"
    wx5_obj = kitchenunit_shop(
        old_bob_text, e5.get_object_root_dir(), get_temp_env_handle()
    )
    e5.set_kitchenunits_empty_if_null()
    e5.set_kitchenunit_to_project(wx5_obj)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{e5.get_kitchenunits_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/seed_deal.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_x_kitchen = e5.get_kitchenunit(title=old_bob_text)
    assert e5.get_kitchenunit(title=new_bob_text) is None
    assert old_x_kitchen._admin._kitchenunit_dir == old_bob_dir
    assert old_x_kitchen._admin._kitchenunit_dir != new_bob_dir

    # WHEN
    e5.rename_kitchenunit(old_title=old_bob_text, new_title=new_bob_text)

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    assert e5.get_kitchenunit(title=old_bob_text) is None
    new_x_kitchen = e5.get_kitchenunit(title=new_bob_text)
    assert new_x_kitchen._admin._kitchenunit_dir != old_bob_dir
    assert new_x_kitchen._admin._kitchenunit_dir == new_bob_dir


def test_project_del_kitchenunit_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    project_handle = get_temp_env_handle()
    sx = projectunit_shop(handle=project_handle, projects_dir=get_test_projects_dir())
    xia_text = "Xia"
    xia_dir = f"{sx.get_kitchenunits_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/seed_deal.json"
    sx.create_new_kitchenunit(kitchen_title=xia_text)
    sx.save_kitchenunit_file(kitchen_title=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    sx.del_kitchenunit_dir(kitchen_title=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False
