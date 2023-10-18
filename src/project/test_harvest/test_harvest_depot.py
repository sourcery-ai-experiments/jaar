from src.project.examples.example_harvests import (
    get_healer_2deal as healer_examples_get_healer_2deal,
)
from src.project.examples.harvest_env_kit import (
    harvest_dir_setup_cleanup,
    get_temp_harvestunit_dir,
    get_temp_project_handle,
)
from src.deal.deal import DealUnit


def test_harvestunit_set_depot_deal_SetsCorrectInfo(harvest_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_harvestunit_dir()
    x_harvest = healer_examples_get_healer_2deal(env_dir, get_temp_project_handle())
    assert x_harvest._seed.get_partys_depotlink_count() == 2
    print(f"{x_harvest._seed._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_harvest.set_depot_deal(DealUnit(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_harvest.set_depot_deal(DealUnit(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{x_harvest._seed._partys.keys()=}")
    assert x_harvest._seed.get_partys_depotlink_count() == 4
