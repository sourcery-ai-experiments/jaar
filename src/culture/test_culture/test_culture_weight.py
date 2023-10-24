from os import path as os_path
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)


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
