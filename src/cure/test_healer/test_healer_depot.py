from src.cure.examples.example_healers import (
    get_healer_2contract as healer_examples_get_healer_2contract,
)
from src.cure.examples.healer_env_kit import (
    healer_dir_setup_cleanup,
    get_temp_healer_dir,
    get_temp_cure_handle,
)
from src.contract.contract import ContractUnit


def test_healer_set_depot_contract_SetsCorrectInfo(healer_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_healer_dir()
    healer_x = healer_examples_get_healer_2contract(env_dir, get_temp_cure_handle())
    assert healer_x._isol.get_partys_depotlink_count() == 2
    print(f"{healer_x._isol._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    healer_x.set_depot_contract(ContractUnit(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    healer_x.set_depot_contract(ContractUnit(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{healer_x._isol._partys.keys()=}")
    assert healer_x._isol.get_partys_depotlink_count() == 4
