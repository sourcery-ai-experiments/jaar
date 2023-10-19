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
    x_handle = get_temp_env_handle()
    x_project = projectunit_shop(handle=x_handle, projects_dir=get_test_projects_dir())
    x_project.create_dirs_if_null()
    y_deal = example_healers_get_1node_deal()
    y_path = f"{x_project.get_public_dir()}/{y_deal._healer}.json"
    assert os_path.exists(y_path) == False

    # WHEN
    x_project.save_public_deal(x_deal=y_deal)

    # THEN
    print(f"{y_path=}")
    assert os_path.exists(y_path)


def test_project_get_deal_currentlyGetsDeal(env_dir_setup_cleanup):
    # GIVEN
    x_handle = get_temp_env_handle()
    x_project = projectunit_shop(handle=x_handle, projects_dir=get_test_projects_dir())
    x_project.create_dirs_if_null(in_memory_bank=True)
    y_deal = example_healers_get_7nodeJRootWithH_deal()
    x_project.save_public_deal(x_deal=y_deal)

    # WHEN / THEN
    assert x_project.get_public_deal(healer=y_deal._healer) == y_deal


def test_project_rename_public_deal_ChangesDealTitle(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_handle = get_temp_env_handle()
    x_project = projectunit_shop(x_handle, get_test_projects_dir())
    x_project.create_dirs_if_null(in_memory_bank=True)
    old_deal_healer = "old1"
    y_deal = dealunit_shop(_healer=old_deal_healer)
    old_y_deal_path = f"{x_project.get_public_dir()}/{old_deal_healer}.json"
    x_project.save_public_deal(x_deal=y_deal)
    print(f"{old_y_deal_path=}")

    # WHEN
    new_deal_healer = "new1"
    new_y_deal_path = f"{x_project.get_public_dir()}/{new_deal_healer}.json"
    assert os_path.exists(new_y_deal_path) == False
    assert os_path.exists(old_y_deal_path)
    x_project.rename_public_deal(old_healer=old_deal_healer, new_healer=new_deal_healer)

    # THEN
    assert os_path.exists(old_y_deal_path) == False
    assert os_path.exists(new_y_deal_path)


def test_project_SetsIdeaRootLabel(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_handle = get_temp_env_handle()
    x_project = projectunit_shop(handle=x_handle, projects_dir=get_test_projects_dir())
    x_project.create_dirs_if_null(in_memory_bank=True)
    old_x_deal = example_deals_get_deal_1Task_1CE0MinutesRequired_1AcptFact()
    assert old_x_deal._idearoot._label == "A"

    # WHEN
    x_project.save_public_deal(old_x_deal)

    # THEN
    new_x_deal = x_project.get_public_deal(old_x_deal._healer)
    assert new_x_deal._idearoot._label == x_handle
