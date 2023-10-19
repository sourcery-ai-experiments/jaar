from src.deal.deal import dealunit_shop
from src.deal.examples.example_deals import (
    get_deal_1Task_1CE0MinutesRequired_1AcptFact as example_deals_get_deal_1Task_1CE0MinutesRequired_1AcptFact,
    deal_v001 as example_deals_deal_v001,
)
from src.project.project import projectunit_shop
from src.project.examples.example_kitchens import (
    get_1node_deal as example_healers_get_1node_deal,
    get_1node_deal as example_healers_get_7nodeJRootWithH_deal,
)
from src.project.examples.project_env_kit import (
    get_temp_env_handle,
    get_test_projects_dir,
    env_dir_setup_cleanup,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_project_set_deal_CreatesDealFile(env_dir_setup_cleanup):
    # GIVEN
    project_handle = get_temp_env_handle()
    sx = projectunit_shop(handle=project_handle, projects_dir=get_test_projects_dir())
    sx.create_dirs_if_null()
    sx1_obj = example_healers_get_1node_deal()
    sx1_path = f"{sx.get_public_dir()}/{sx1_obj._healer}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    sx.save_public_deal(deal_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_project_get_deal_currentlyGetsDeal(env_dir_setup_cleanup):
    # GIVEN
    project_handle = get_temp_env_handle()
    e5 = projectunit_shop(handle=project_handle, projects_dir=get_test_projects_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_healers_get_7nodeJRootWithH_deal()
    e5.save_public_deal(deal_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_public_deal(healer=sx5_obj._healer) == sx5_obj


def test_project_rename_public_deal_ChangesDealTitle(
    env_dir_setup_cleanup,
):
    # GIVEN
    project_handle = get_temp_env_handle()
    e5 = projectunit_shop(handle=project_handle, projects_dir=get_test_projects_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_deal_healer = "old1"
    sx5_obj = dealunit_shop(_healer=old_deal_healer)
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


def test_project_SetsIdeaRootLabel(
    env_dir_setup_cleanup,
):
    # GIVEN
    project_handle = get_temp_env_handle()
    e5 = projectunit_shop(handle=project_handle, projects_dir=get_test_projects_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    deal_x = example_deals_get_deal_1Task_1CE0MinutesRequired_1AcptFact()
    assert deal_x._idearoot._label == "A"

    # WHEN
    e5.save_public_deal(deal_x)

    # THEN
    deal_after = e5.get_public_deal(deal_x._healer)
    assert deal_after._idearoot._label == project_handle
