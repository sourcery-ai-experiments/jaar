from src.fix.examples.example_remedys import (
    get_healer_2deal as healer_examples_get_healer_2deal,
)
from src.fix.examples.remedy_env_kit import (
    remedy_dir_setup_cleanup,
    get_temp_remedyunit_dir,
    get_temp_fix_handle,
)
from src.deal.deal import DealUnit


def test_remedyunit_set_depot_deal_SetsCorrectInfo(remedy_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_remedyunit_dir()
    x_remedy = healer_examples_get_healer_2deal(env_dir, get_temp_fix_handle())
    assert x_remedy._isol.get_partys_depotlink_count() == 2
    print(f"{x_remedy._isol._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_remedy.set_depot_deal(DealUnit(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_remedy.set_depot_deal(DealUnit(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{x_remedy._isol._partys.keys()=}")
    assert x_remedy._isol.get_partys_depotlink_count() == 4
