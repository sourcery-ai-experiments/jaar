from os import path as os_path
from src.project.project import projectunit_shop
from src.project.examples.project_env_kit import (
    get_temp_env_handle,
    get_test_projects_dir,
    env_dir_setup_cleanup,
)


def test_projectunit_set_person_importance_CorrectsSetsData(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_handle()
    x_projectunit = projectunit_shop(
        handle=park_text, projects_dir=get_test_projects_dir()
    )
    assert x_projectunit.handle == park_text
    assert x_projectunit._person_importance is None

    # WHEN
    x_person_importance = 0.77
    x_projectunit.set_person_importance(x_person_importance)

    # THEN
    assert x_projectunit._person_importance == x_person_importance
