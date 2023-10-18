from src.fix.examples.example_collects import (
    get_healer_2deal as healer_examples_get_healer_2deal,
)
from src.fix.examples.collect_env_kit import (
    collect_dir_setup_cleanup,
    get_temp_collectunit_dir,
    get_temp_fix_handle,
)
from src.deal.deal import DealUnit


def test_collectunit_set_depot_deal_SetsCorrectInfo(collect_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_collectunit_dir()
    x_collect = healer_examples_get_healer_2deal(env_dir, get_temp_fix_handle())
    assert x_collect._isol.get_partys_depotlink_count() == 2
    print(f"{x_collect._isol._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_collect.set_depot_deal(DealUnit(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_collect.set_depot_deal(DealUnit(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{x_collect._isol._partys.keys()=}")
    assert x_collect._isol.get_partys_depotlink_count() == 4
