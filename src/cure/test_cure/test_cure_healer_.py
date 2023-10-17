from src.cure.cure import cureunit_shop
from src.cure.healing import healingunit_shop
from src.cure.examples.cure_env_kit import (
    get_temp_env_dir,
    get_temp_env_handle,
    env_dir_setup_cleanup,
    get_test_cures_dir,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_cure_set_healer_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    cure_handle = get_temp_env_handle()
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    print(f"create env '{cure_handle}' directories.")
    sx.create_dirs_if_null(in_memory_bank=True)
    timmy_text = "timmy"
    wx_path = f"{sx.get_healingunits_dir()}/{timmy_text}"
    print(f"{wx_path=}")
    assert os_path.exists(wx_path) == False

    # WHEN
    sx.create_new_healingunit(healing_title=timmy_text)

    # THEN
    print(f"{wx_path=}")
    assert os_path.exists(wx_path)


def test_cure_create_healingunit_from_public_RaisesErrorWhenHealerDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    cure_handle = get_temp_env_handle()
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())

    # WHEN / THEN
    bobs_text = "bobs wurld"
    with pytest_raises(Exception) as excinfo:
        sx.create_healingunit_from_public(title=bobs_text)
    assert (
        str(excinfo.value)
        == f"Could not load file {sx.get_public_dir()}/{bobs_text}.json (2, 'No such file or directory')"
    )


def test_cure_rename_healingunit_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    cure_handle = get_temp_env_handle()
    e5 = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{e5.get_healingunits_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/isol_deal.json"
    wx5_obj = healingunit_shop(
        old_bob_text, e5.get_object_root_dir(), get_temp_env_handle()
    )
    e5.set_healingunits_empty_if_null()
    e5.set_healingunit_to_cure(wx5_obj)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{e5.get_healingunits_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/isol_deal.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_x_healing = e5.get_healingunit(title=old_bob_text)
    assert e5.get_healingunit(title=new_bob_text) is None
    assert old_x_healing._admin._healingunit_dir == old_bob_dir
    assert old_x_healing._admin._healingunit_dir != new_bob_dir

    # WHEN
    e5.rename_healingunit(old_title=old_bob_text, new_title=new_bob_text)

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    assert e5.get_healingunit(title=old_bob_text) is None
    new_x_healing = e5.get_healingunit(title=new_bob_text)
    assert new_x_healing._admin._healingunit_dir != old_bob_dir
    assert new_x_healing._admin._healingunit_dir == new_bob_dir


def test_cure_del_healingunit_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    cure_handle = get_temp_env_handle()
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    xia_text = "Xia"
    xia_dir = f"{sx.get_healingunits_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/isol_deal.json"
    sx.create_new_healingunit(healing_title=xia_text)
    sx.save_healingunit_file(healing_title=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    sx.del_healingunit_dir(healing_title=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False
