from src.deal.x_func import delete_dir as x_func_delete_dir
from src.project.project import projectunit_shop, ProjectUnit
from os import path as os_path
from src.project.examples.project_env_kit import (
    get_temp_env_handle,
    get_test_projects_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.project.y_func import check_connection


def test_project_create_bank_db_CreatesBankDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create project
    x_project = projectunit_shop(
        handle=get_temp_env_handle(), projects_dir=get_test_projects_dir()
    )

    # clear out any bank.db file
    x_func_delete_dir(dir=x_project.get_bank_db_path())
    assert os_path.exists(x_project.get_bank_db_path()) == False

    # WHEN
    x_project._create_bank_db()

    # THEN
    assert os_path.exists(x_project.get_bank_db_path())


def test_project_create_bank_db_CanCreateBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create project
    x_project = projectunit_shop(
        handle=get_temp_env_handle(), projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    # clear out any bank.db file
    x_project._bank_db = None
    assert x_project._bank_db is None
    assert os_path.exists(x_project.get_bank_db_path()) == False

    # WHEN
    x_project._create_bank_db(in_memory=True)

    # THEN
    assert x_project._bank_db != None
    assert os_path.exists(x_project.get_bank_db_path()) == False


def test_project_refresh_bank_metrics_CanConnectToBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create project
    x_project = projectunit_shop(
        handle=get_temp_env_handle(), projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)
    # x_project._create_bank_db(in_memory=True)
    assert os_path.exists(x_project.get_bank_db_path()) == False

    # WHEN
    x_project.refresh_bank_metrics()

    # THEN
    assert os_path.exists(x_project.get_bank_db_path()) == False


def test_project_get_bank_db_conn_CreatesBankDBIfItDoesNotExist(env_dir_setup_cleanup):
    # GIVEN create project
    x_project = ProjectUnit(
        handle=get_temp_env_handle(), projects_dir=get_test_projects_dir()
    )
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_project.get_bank_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_project.create_dirs_if_null(in_memory_bank=True)

    # THEN
    assert check_connection(x_project.get_bank_conn())
