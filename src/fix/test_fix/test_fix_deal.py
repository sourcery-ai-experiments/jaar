from src.deal.deal import DealUnit
from src.deal.examples.example_deals import (
    get_deal_1Task_1CE0MinutesRequired_1AcptFact as example_deals_get_deal_1Task_1CE0MinutesRequired_1AcptFact,
    deal_v001 as example_deals_deal_v001,
)
from src.fix.fix import fixunit_shop
from src.fix.examples.example_collects import (
    get_1node_deal as example_healers_get_1node_deal,
    get_1node_deal as example_healers_get_7nodeJRootWithH_deal,
)
from src.fix.examples.fix_env_kit import (
    get_temp_env_handle,
    get_test_fixs_dir,
    env_dir_setup_cleanup,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_fix_set_deal_CreatesDealFile(env_dir_setup_cleanup):
    # GIVEN
    fix_handle = get_temp_env_handle()
    sx = fixunit_shop(handle=fix_handle, fixs_dir=get_test_fixs_dir())
    sx.create_dirs_if_null()
    sx1_obj = example_healers_get_1node_deal()
    sx1_path = f"{sx.get_public_dir()}/{sx1_obj._healer}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    sx.save_public_deal(deal_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_fix_get_deal_currentlyGetsDeal(env_dir_setup_cleanup):
    # GIVEN
    fix_handle = get_temp_env_handle()
    e5 = fixunit_shop(handle=fix_handle, fixs_dir=get_test_fixs_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_healers_get_7nodeJRootWithH_deal()
    e5.save_public_deal(deal_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_public_deal(healer=sx5_obj._healer) == sx5_obj


def test_fix_rename_public_deal_ChangesDealTitle(
    env_dir_setup_cleanup,
):
    # GIVEN
    fix_handle = get_temp_env_handle()
    e5 = fixunit_shop(handle=fix_handle, fixs_dir=get_test_fixs_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_deal_healer = "old1"
    sx5_obj = DealUnit(_healer=old_deal_healer)
    old_sx5_path = f"{e5.get_public_dir()}/{old_deal_healer}.json"
    e5.save_public_deal(deal_x=sx5_obj)
    print(f"{old_sx5_path=}")

    # WHEN
    new_deal_healer = "new1"
    new_sx5_path = f"{e5.get_public_dir()}/{new_deal_healer}.json"
    assert os_path.exists(new_sx5_path) == False
    assert os_path.exists(old_sx5_path)
    e5.rename_public_deal(old_healer=old_deal_healer, new_healer=new_deal_healer)

    # THEN
    assert os_path.exists(old_sx5_path) == False
    assert os_path.exists(new_sx5_path)


def test_fix_SetsIdeaRootLabel(
    env_dir_setup_cleanup,
):
    # GIVEN
    fix_handle = get_temp_env_handle()
    e5 = fixunit_shop(handle=fix_handle, fixs_dir=get_test_fixs_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    deal_x = example_deals_get_deal_1Task_1CE0MinutesRequired_1AcptFact()
    assert deal_x._idearoot._label == "A"

    # WHEN
    e5.save_public_deal(deal_x)

    # THEN
    deal_after = e5.get_public_deal(deal_x._healer)
    assert deal_after._idearoot._label == fix_handle
