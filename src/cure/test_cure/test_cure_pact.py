from src.pact.pact import PactUnit
from src.pact.examples.example_pacts import (
    get_pact_1Task_1CE0MinutesRequired_1AcptFact as example_pacts_get_pact_1Task_1CE0MinutesRequired_1AcptFact,
    pact_v001 as example_pacts_pact_v001,
)
from src.cure.cure import cureunit_shop
from src.cure.examples.example_healers import (
    get_1node_pact as example_healers_get_1node_pact,
    get_1node_pact as example_healers_get_7nodeJRootWithH_pact,
)
from src.cure.examples.cure_env_kit import (
    get_temp_env_handle,
    get_test_cures_dir,
    env_dir_setup_cleanup,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_cure_set_pact_CreatesPactFile(env_dir_setup_cleanup):
    # GIVEN
    cure_handle = get_temp_env_handle()
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null()
    sx1_obj = example_healers_get_1node_pact()
    sx1_path = f"{sx.get_public_dir()}/{sx1_obj._healer}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    sx.save_public_pact(pact_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_cure_get_pact_currentlyGetsPact(env_dir_setup_cleanup):
    # GIVEN
    cure_handle = get_temp_env_handle()
    e5 = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_healers_get_7nodeJRootWithH_pact()
    e5.save_public_pact(pact_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_public_pact(healer=sx5_obj._healer) == sx5_obj


def test_cure_rename_public_pact_ChangesPactTitle(
    env_dir_setup_cleanup,
):
    # GIVEN
    cure_handle = get_temp_env_handle()
    e5 = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_pact_healer = "old1"
    sx5_obj = PactUnit(_healer=old_pact_healer)
    old_sx5_path = f"{e5.get_public_dir()}/{old_pact_healer}.json"
    e5.save_public_pact(pact_x=sx5_obj)
    print(f"{old_sx5_path=}")

    # WHEN
    new_pact_healer = "new1"
    new_sx5_path = f"{e5.get_public_dir()}/{new_pact_healer}.json"
    assert os_path.exists(new_sx5_path) == False
    assert os_path.exists(old_sx5_path)
    e5.rename_public_pact(old_healer=old_pact_healer, new_healer=new_pact_healer)

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
    pact_x = example_pacts_get_pact_1Task_1CE0MinutesRequired_1AcptFact()
    assert pact_x._idearoot._label == "A"

    # WHEN
    e5.save_public_pact(pact_x)

    # THEN
    pact_after = e5.get_public_pact(pact_x._healer)
    assert pact_after._idearoot._label == cure_handle
