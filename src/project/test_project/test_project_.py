from src.deal.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.project.project import ProjectUnit, projectunit_shop
from src.project.examples.project_env_kit import (
    get_temp_env_handle,
    get_test_projects_dir,
    rename_example_project,
    copy_evaluation_project,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_project_exists():
    # GIVEN
    project_handle = "test1"

    # WHEN
    x_projectunit = ProjectUnit(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )

    # THEN
    assert x_projectunit.handle == project_handle
    assert x_projectunit.projects_dir == get_test_projects_dir()
    assert x_projectunit._person_importance is None


def test_project_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create project
    project_handle = get_temp_env_handle()
    x_projectunit = ProjectUnit(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    print(f"{get_test_projects_dir()=} {x_projectunit.projects_dir=}")
    # x_func_delete_dir(x_projectunit.get_object_root_dir())
    print(f"delete {x_projectunit.get_object_root_dir()=}")
    project_dir = f"src/project/examples/projects/{project_handle}"
    project_file_title = "project.json"
    project_file_path = f"{project_dir}/{project_file_title}"
    deals_dir = f"{project_dir}/deals"
    kitchenunits_dir = f"{project_dir}/kitchenunits"
    bank_file_title = "bank.db"
    bank_file_path = f"{project_dir}/{bank_file_title}"

    assert os_path.exists(project_dir) is False
    assert os_path.isdir(project_dir) is False
    assert os_path.exists(project_file_path) is False
    assert os_path.exists(deals_dir) is False
    assert os_path.exists(kitchenunits_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    x_projectunit.create_dirs_if_null(in_memory_bank=False)

    # THEN check deals src directory created
    assert os_path.exists(project_dir)
    assert os_path.isdir(project_dir)
    assert os_path.exists(project_file_path)
    assert os_path.exists(deals_dir)
    assert os_path.exists(kitchenunits_dir)
    assert os_path.exists(bank_file_path)
    assert x_projectunit.get_object_root_dir() == project_dir
    assert x_projectunit.get_public_dir() == deals_dir
    assert x_projectunit.get_kitchenunits_dir() == kitchenunits_dir
    assert x_projectunit.get_bank_db_path() == bank_file_path


def test_rename_example_project_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create project
    old_project_handle = get_temp_env_handle()
    old_project_dir = f"src/project/examples/projects/{old_project_handle}"
    old_project_file_title = "project.json"
    old_project_file_path = f"{old_project_dir}/{old_project_file_title}"
    old_deals_dir = f"{old_project_dir}/deals"
    old_kitchenunits_dir = f"{old_project_dir}/kitchenunits"

    new_project_handle = "ex_env1"
    new_project_dir = f"src/project/examples/projects/{new_project_handle}"
    new_project_file_title = "project.json"
    new_project_file_path = f"{new_project_dir}/{new_project_file_title}"
    new_deals_dir = f"{new_project_dir}/deals"
    new_kitchenunits_dir = f"{new_project_dir}/kitchenunits"
    x_func_delete_dir(dir=new_project_dir)
    print(f"{new_project_dir=}")

    x_projectunit = projectunit_shop(
        handle=old_project_handle, projects_dir=get_test_projects_dir()
    )
    # x_func_delete_dir(x_projectunit.get_object_root_dir())
    # print(f"{x_projectunit.get_object_root_dir()=}")

    x_projectunit.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_project_dir)
    assert os_path.isdir(old_project_dir)
    assert os_path.exists(old_project_file_path)
    assert os_path.exists(old_deals_dir)
    assert os_path.exists(old_kitchenunits_dir)
    assert x_projectunit.get_public_dir() == old_deals_dir
    assert x_projectunit.get_kitchenunits_dir() == old_kitchenunits_dir

    assert os_path.exists(new_project_dir) is False
    assert os_path.isdir(new_project_dir) is False
    assert os_path.exists(new_project_file_path) is False
    assert os_path.exists(new_deals_dir) is False
    assert os_path.exists(new_kitchenunits_dir) is False
    assert x_projectunit.get_public_dir() != new_deals_dir
    assert x_projectunit.get_kitchenunits_dir() != new_kitchenunits_dir
    assert x_projectunit.handle != new_project_handle

    # WHEN
    rename_example_project(project_obj=x_projectunit, new_title=new_project_handle)

    # THEN check deals src directory created
    assert os_path.exists(old_project_dir) is False
    assert os_path.isdir(old_project_dir) is False
    assert os_path.exists(old_project_file_path) is False
    assert os_path.exists(old_deals_dir) is False
    assert os_path.exists(old_kitchenunits_dir) is False
    assert x_projectunit.get_public_dir() != old_deals_dir
    assert x_projectunit.get_kitchenunits_dir() != old_kitchenunits_dir

    assert os_path.exists(new_project_dir)
    assert os_path.isdir(new_project_dir)
    assert os_path.exists(new_project_file_path)
    assert os_path.exists(new_deals_dir)
    assert os_path.exists(new_kitchenunits_dir)
    assert x_projectunit.get_public_dir() == new_deals_dir
    assert x_projectunit.get_kitchenunits_dir() == new_kitchenunits_dir
    assert x_projectunit.handle == new_project_handle

    # Undo change to directory
    # x_func_delete_dir(dir=old_project_dir)
    # print(f"{old_project_dir=}")
    x_func_delete_dir(dir=new_project_dir)
    print(f"{new_project_dir=}")


def test_copy_evaluation_project_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create project
    old_project_handle = get_temp_env_handle()
    old_project_dir = f"src/project/examples/projects/{old_project_handle}"
    old_project_file_title = "project.json"
    old_project_file_path = f"{old_project_dir}/{old_project_file_title}"
    old_deals_dir = f"{old_project_dir}/deals"
    old_kitchenunits_dir = f"{old_project_dir}/kitchenunits"

    x_projectunit = projectunit_shop(
        handle=old_project_handle, projects_dir=get_test_projects_dir()
    )
    x_projectunit.create_dirs_if_null()

    assert os_path.exists(old_project_dir)
    assert os_path.isdir(old_project_dir)
    assert os_path.exists(old_project_file_path)
    assert os_path.exists(old_deals_dir)
    assert os_path.exists(old_kitchenunits_dir)
    assert x_projectunit.get_public_dir() == old_deals_dir
    assert x_projectunit.get_kitchenunits_dir() == old_kitchenunits_dir

    new_project_handle = "ex_env1"
    new_project_dir = f"src/project/examples/projects/{new_project_handle}"
    new_project_file_title = "project.json"
    new_project_file_path = f"{new_project_dir}/{new_project_file_title}"
    new_deals_dir = f"{new_project_dir}/deals"
    new_kitchenunits_dir = f"{new_project_dir}/kitchenunits"

    assert os_path.exists(new_project_dir) is False
    assert os_path.isdir(new_project_dir) is False
    assert os_path.exists(new_project_file_path) is False
    assert os_path.exists(new_deals_dir) is False
    assert os_path.exists(new_kitchenunits_dir) is False
    assert x_projectunit.get_public_dir() != new_deals_dir
    assert x_projectunit.get_kitchenunits_dir() != new_kitchenunits_dir
    assert x_projectunit.handle != new_project_handle

    # WHEN
    copy_evaluation_project(
        src_handle=x_projectunit.handle, dest_handle=new_project_handle
    )

    # THEN check deals src directory created
    assert os_path.exists(old_project_dir)
    assert os_path.isdir(old_project_dir)
    assert os_path.exists(old_project_file_path)
    assert os_path.exists(old_deals_dir)
    assert os_path.exists(old_kitchenunits_dir)
    assert x_projectunit.get_public_dir() == old_deals_dir
    assert x_projectunit.get_kitchenunits_dir() == old_kitchenunits_dir

    assert os_path.exists(new_project_dir)
    assert os_path.isdir(new_project_dir)
    assert os_path.exists(new_project_file_path)
    assert os_path.exists(new_deals_dir)
    assert os_path.exists(new_kitchenunits_dir)
    assert x_projectunit.get_public_dir() != new_deals_dir
    assert x_projectunit.get_kitchenunits_dir() != new_kitchenunits_dir
    assert x_projectunit.handle != new_project_handle

    # Undo change to directory
    # x_func_delete_dir(x_projectunit.get_object_root_dir())
    # x_func_delete_dir(dir=old_project_dir)
    x_func_delete_dir(dir=new_project_dir)


def test_copy_evaluation_project_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create project
    old_project_handle = get_temp_env_handle()
    x_projectunit = projectunit_shop(
        handle=old_project_handle, projects_dir=get_test_projects_dir()
    )
    x_projectunit.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_project(
            src_handle=x_projectunit.handle, dest_handle=old_project_handle
        )
    assert (
        str(excinfo.value)
        == f"Cannot copy project to '{x_projectunit.get_object_root_dir()}' directory because '{x_projectunit.get_object_root_dir()}' exists."
    )


def test_projectunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_handle()
    project_dir = f"src/project/examples/projects/{park_text}"
    assert os_path.exists(project_dir) is False

    # WHEN
    x_projectunit = projectunit_shop(
        handle=park_text, projects_dir=get_test_projects_dir()
    )

    # THEN
    assert x_projectunit != None
    assert x_projectunit.handle == park_text
    assert os_path.exists(project_dir)
    assert x_projectunit._bank_db != None
    assert x_projectunit._person_importance is None
