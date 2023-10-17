from os import path as os_path
from src.cure.cure import cureunit_shop
from src.cure.examples.cure_env_kit import (
    get_temp_env_handle,
    get_test_cures_dir,
    env_dir_setup_cleanup,
)


def test_cureunit_set_person_importance_CorrectsSetsData(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_handle()
    x_cureunit = cureunit_shop(handle=park_text, cures_dir=get_test_cures_dir())
    assert x_cureunit.handle == park_text
    assert x_cureunit._person_importance is None

    # WHEN
    x_person_importance = 0.77
    x_cureunit.set_person_importance(x_person_importance)

    # THEN
    assert x_cureunit._person_importance == x_person_importance
