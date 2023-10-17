from src.cure.examples.example_healers import (
    get_healer_2pact as healer_examples_get_healer_2pact,
)
from src.cure.examples.healer_env_kit import (
    healer_dir_setup_cleanup,
    get_temp_healingunit_dir,
    get_temp_cure_handle,
)
from src.pact.pact import PactUnit


def test_healingunit_set_depot_pact_SetsCorrectInfo(healer_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_healingunit_dir()
    x_healing = healer_examples_get_healer_2pact(env_dir, get_temp_cure_handle())
    assert x_healing._isol.get_partys_depotlink_count() == 2
    print(f"{x_healing._isol._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_healing.set_depot_pact(PactUnit(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_healing.set_depot_pact(PactUnit(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{x_healing._isol._partys.keys()=}")
    assert x_healing._isol.get_partys_depotlink_count() == 4
