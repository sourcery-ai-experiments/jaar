from src.project.examples.example_kitchens import (
    get_healer_2deal as healer_examples_get_healer_2deal,
)
from src.project.examples.kitchen_env_kit import (
    kitchen_dir_setup_cleanup,
    get_temp_kitchenunit_dir,
    get_temp_project_handle,
)
from src.deal.deal import DealUnit


def test_kitchenunit_set_depot_deal_SetsCorrectInfo(kitchen_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_kitchenunit_dir()
    x_kitchen = healer_examples_get_healer_2deal(env_dir, get_temp_project_handle())
    assert x_kitchen._seed.get_partys_depotlink_count() == 2
    print(f"{x_kitchen._seed._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_kitchen.set_depot_deal(DealUnit(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_kitchen.set_depot_deal(DealUnit(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{x_kitchen._seed._partys.keys()=}")
    assert x_kitchen._seed.get_partys_depotlink_count() == 4
