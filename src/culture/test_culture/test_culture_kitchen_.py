from src.culture.culture import cultureunit_shop
from src.culture.kitchen import kitchenunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_dir,
    get_temp_env_handle,
    env_dir_setup_cleanup,
    get_test_cultures_dir,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_culture_set_healer_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(handle=x_handle, cultures_dir=get_test_cultures_dir())
    print(f"create env '{x_handle}' directories.")
    x_culture.create_dirs_if_null(in_memory_bank=True)
    timmy_text = "timmy"
    wx_path = f"{x_culture.get_kitchenunits_dir()}/{timmy_text}"
    print(f"{wx_path=}")
    assert os_path.exists(wx_path) == False

    # WHEN
    x_culture.create_new_kitchenunit(kitchen_dub=timmy_text)

    # THEN
    print(f"{wx_path=}")
    assert os_path.exists(wx_path)


def test_culture_rename_kitchenunit_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(handle=x_handle, cultures_dir=get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{x_culture.get_kitchenunits_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/seed_agenda.json"
    wx5_obj = kitchenunit_shop(
        old_bob_text, x_culture.get_object_root_dir(), get_temp_env_handle()
    )
    x_culture.set_kitchenunits_empty_if_null()
    x_culture.set_kitchenunit_to_culture(wx5_obj)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{x_culture.get_kitchenunits_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/seed_agenda.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_x_kitchen = x_culture.get_kitchenunit(dub=old_bob_text)
    assert x_culture.get_kitchenunit(dub=new_bob_text) is None
    assert old_x_kitchen._admin._kitchenunit_dir == old_bob_dir
    assert old_x_kitchen._admin._kitchenunit_dir != new_bob_dir

    # WHEN
    x_culture.rename_kitchenunit(old_dub=old_bob_text, new_dub=new_bob_text)

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    assert x_culture.get_kitchenunit(dub=old_bob_text) is None
    new_x_kitchen = x_culture.get_kitchenunit(dub=new_bob_text)
    assert new_x_kitchen._admin._kitchenunit_dir != old_bob_dir
    assert new_x_kitchen._admin._kitchenunit_dir == new_bob_dir


def test_culture_del_kitchenunit_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(handle=x_handle, cultures_dir=get_test_cultures_dir())
    xia_text = "Xia"
    xia_dir = f"{x_culture.get_kitchenunits_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/seed_agenda.json"
    x_culture.create_new_kitchenunit(kitchen_dub=xia_text)
    x_culture.save_kitchenunit_file(kitchen_dub=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    x_culture.del_kitchenunit_dir(kitchen_dub=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False
