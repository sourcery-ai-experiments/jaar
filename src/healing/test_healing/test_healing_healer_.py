from src.healing.healing import healingunit_shop
from src.healing.healer import healerunit_shop
from src.healing.examples.healing_env_kit import (
    get_temp_env_dir,
    get_temp_env_handle,
    env_dir_setup_cleanup,
    get_test_healings_dir,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_healing_set_healer_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    healing_handle = get_temp_env_handle()
    sx = healingunit_shop(handle=healing_handle, healings_dir=get_test_healings_dir())
    print(f"create env '{healing_handle}' directories.")
    sx.create_dirs_if_null(in_memory_bank=True)
    timmy_text = "timmy"
    wx_path = f"{sx.get_healers_dir()}/{timmy_text}"
    print(f"{wx_path=}")
    assert os_path.exists(wx_path) == False

    # WHEN
    sx.create_new_healerunit(healer_title=timmy_text)

    # THEN
    print(f"{wx_path=}")
    assert os_path.exists(wx_path)


def test_healing_create_healerunit_from_public_RaisesErrorWhenHealerDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    healing_handle = get_temp_env_handle()
    sx = healingunit_shop(handle=healing_handle, healings_dir=get_test_healings_dir())

    # WHEN / THEN
    bobs_text = "bobs wurld"
    with pytest_raises(Exception) as excinfo:
        sx.create_healerunit_from_public(title=bobs_text)
    assert (
        str(excinfo.value)
        == f"Could not load file {sx.get_public_dir()}/{bobs_text}.json (2, 'No such file or directory')"
    )


def test_healing_rename_healerunit_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    healing_handle = get_temp_env_handle()
    e5 = healingunit_shop(handle=healing_handle, healings_dir=get_test_healings_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{e5.get_healers_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/isol_contract.json"
    wx5_obj = healerunit_shop(
        old_bob_text, e5.get_object_root_dir(), get_temp_env_handle()
    )
    e5.set_healerunits_empty_if_null()
    e5.set_healerunit_to_healing(healer=wx5_obj)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{e5.get_healers_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/isol_contract.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_healer_x = e5.get_healer_obj(title=old_bob_text)
    assert e5.get_healer_obj(title=new_bob_text) is None
    assert old_healer_x._admin._healer_dir == old_bob_dir
    assert old_healer_x._admin._healer_dir != new_bob_dir

    # WHEN
    e5.rename_healerunit(old_title=old_bob_text, new_title=new_bob_text)

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    assert e5.get_healer_obj(title=old_bob_text) is None
    new_healer_x = e5.get_healer_obj(title=new_bob_text)
    assert new_healer_x._admin._healer_dir != old_bob_dir
    assert new_healer_x._admin._healer_dir == new_bob_dir


def test_healing_del_healer_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    healing_handle = get_temp_env_handle()
    sx = healingunit_shop(handle=healing_handle, healings_dir=get_test_healings_dir())
    xia_text = "Xia"
    xia_dir = f"{sx.get_healers_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/isol_contract.json"
    sx.create_new_healerunit(healer_title=xia_text)
    sx.save_healer_file(healer_title=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    sx.del_healer_dir(healer_title=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False
