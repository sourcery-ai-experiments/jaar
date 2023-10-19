from os import path as os_path
from src.project.project import projectunit_shop
from src.project.examples.project_env_kit import (
    get_temp_env_handle,
    get_test_projects_dir,
    env_dir_setup_cleanup,
)


def test_projectunit_set_person_importance_CorrectsSetsData(env_dir_setup_cleanup):
    # GIVEN
    x_handle = get_temp_env_handle()
    x_project = projectunit_shop(handle=x_handle, projects_dir=get_test_projects_dir())
    assert x_project.handle == x_handle
    assert x_project._person_importance is None

    # WHEN
    x_person_importance = 0.77
    x_project.set_person_importance(x_person_importance)

    # THEN
    assert x_project._person_importance == x_person_importance
