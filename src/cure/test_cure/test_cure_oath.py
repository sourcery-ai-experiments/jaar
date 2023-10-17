from src.oath.oath import OathUnit
from src.oath.examples.example_oaths import (
    get_oath_1Task_1CE0MinutesRequired_1AcptFact as example_oaths_get_oath_1Task_1CE0MinutesRequired_1AcptFact,
    oath_v001 as example_oaths_oath_v001,
)
from src.cure.cure import cureunit_shop
from src.cure.examples.example_healers import (
    get_1node_oath as example_healers_get_1node_oath,
    get_1node_oath as example_healers_get_7nodeJRootWithH_oath,
)
from src.cure.examples.cure_env_kit import (
    get_temp_env_handle,
    get_test_cures_dir,
    env_dir_setup_cleanup,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_cure_set_oath_CreatesOathFile(env_dir_setup_cleanup):
    # GIVEN
    cure_handle = get_temp_env_handle()
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null()
    sx1_obj = example_healers_get_1node_oath()
    sx1_path = f"{sx.get_public_dir()}/{sx1_obj._healer}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    sx.save_public_oath(oath_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_cure_get_oath_currentlyGetsOath(env_dir_setup_cleanup):
    # GIVEN
    cure_handle = get_temp_env_handle()
    e5 = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_healers_get_7nodeJRootWithH_oath()
    e5.save_public_oath(oath_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_public_oath(healer=sx5_obj._healer) == sx5_obj


def test_cure_rename_public_oath_ChangesOathTitle(
    env_dir_setup_cleanup,
):
    # GIVEN
    cure_handle = get_temp_env_handle()
    e5 = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_oath_healer = "old1"
    sx5_obj = OathUnit(_healer=old_oath_healer)
    old_sx5_path = f"{e5.get_public_dir()}/{old_oath_healer}.json"
    e5.save_public_oath(oath_x=sx5_obj)
    print(f"{old_sx5_path=}")

    # WHEN
    new_oath_healer = "new1"
    new_sx5_path = f"{e5.get_public_dir()}/{new_oath_healer}.json"
    assert os_path.exists(new_sx5_path) == False
    assert os_path.exists(old_sx5_path)
    e5.rename_public_oath(old_healer=old_oath_healer, new_healer=new_oath_healer)

    # THEN
    assert os_path.exists(old_sx5_path) == False
    assert os_path.exists(new_sx5_path)


def test_cure_SetsIdeaRootLabel(
    env_dir_setup_cleanup,
):
    # GIVEN
    cure_handle = get_temp_env_handle()
    e5 = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    oath_x = example_oaths_get_oath_1Task_1CE0MinutesRequired_1AcptFact()
    assert oath_x._idearoot._label == "A"

    # WHEN
    e5.save_public_oath(oath_x)

    # THEN
    oath_after = e5.get_public_oath(oath_x._healer)
    assert oath_after._idearoot._label == cure_handle
