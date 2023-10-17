from os import path as os_path
from src.fix.fix import fixunit_shop
from src.fix.examples.fix_env_kit import (
    get_temp_env_handle,
    get_test_fixs_dir,
    env_dir_setup_cleanup,
)


def test_fixunit_set_person_importance_CorrectsSetsData(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_handle()
    x_fixunit = fixunit_shop(handle=park_text, fixs_dir=get_test_fixs_dir())
    assert x_fixunit.handle == park_text
    assert x_fixunit._person_importance is None

    # WHEN
    x_person_importance = 0.77
    x_fixunit.set_person_importance(x_person_importance)

    # THEN
    assert x_fixunit._person_importance == x_person_importance
