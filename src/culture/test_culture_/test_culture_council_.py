from src.culture.culture import cultureunit_shop
from src.culture.council import councilunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_dir,
    get_temp_env_title,
    env_dir_setup_cleanup,
    get_test_cultures_dir,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_culture_set_healer_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_title = get_temp_env_title()
    x_culture = cultureunit_shop(title=x_title, cultures_dir=get_test_cultures_dir())
    print(f"create env '{x_title}' directories.")
    x_culture.create_dirs_if_null(in_memory_bank=True)
    timmy_text = "timmy"
    wx_path = f"{x_culture.get_councilunits_dir()}/{timmy_text}"
    print(f"{wx_path=}")
    assert os_path.exists(wx_path) == False

    # WHEN
    x_culture.create_new_councilunit(council_dub=timmy_text)

    # THEN
    print(f"{wx_path=}")
    assert os_path.exists(wx_path)


def test_culture_change_councilunit_dub_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_title = get_temp_env_title()
    x_culture = cultureunit_shop(title=x_title, cultures_dir=get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{x_culture.get_councilunits_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/seed_agenda.json"
    wx5_obj = councilunit_shop(
        old_bob_text, x_culture.get_object_root_dir(), get_temp_env_title()
    )
    x_culture.set_councilunits_empty_if_null()
    x_culture.set_councilunit_to_culture(wx5_obj)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{x_culture.get_councilunits_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/seed_agenda.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_x_council = x_culture.get_councilunit(dub=old_bob_text)
    assert x_culture.get_councilunit(dub=new_bob_text) is None
    assert old_x_council._admin._councilunit_dir == old_bob_dir
    assert old_x_council._admin._councilunit_dir != new_bob_dir

    # WHEN
    x_culture.change_councilunit_dub(old_dub=old_bob_text, new_dub=new_bob_text)

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    assert x_culture.get_councilunit(dub=old_bob_text) is None
    new_x_council = x_culture.get_councilunit(dub=new_bob_text)
    assert new_x_council._admin._councilunit_dir != old_bob_dir
    assert new_x_council._admin._councilunit_dir == new_bob_dir


def test_culture_del_councilunit_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_title = get_temp_env_title()
    x_culture = cultureunit_shop(title=x_title, cultures_dir=get_test_cultures_dir())
    xia_text = "Xia"
    xia_dir = f"{x_culture.get_councilunits_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/seed_agenda.json"
    x_culture.create_new_councilunit(council_dub=xia_text)
    x_culture.save_councilunit_file(council_dub=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    x_culture.del_councilunit_dir(council_dub=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False
