import src.economy.examples.example_owners as owner_examples
from src.economy.examples.owner_env_kit import (
    owner_dir_setup_cleanup,
    get_temp_owner_dir,
    get_temp_economy_title,
)
from src.contract.contract import ContractUnit


def test_owner_set_depot_contract_SetsCorrectInfo(owner_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_owner_dir()
    owner_x = owner_examples.get_owner_2contract(env_dir, get_temp_economy_title())
    assert owner_x._isol.get_members_depotlink_count() == 2
    print(f"{owner_x._isol._members.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    owner_x.set_depot_contract(ContractUnit(_owner=zia_text), assignment_text)
    zoa_text = "Zoa"
    owner_x.set_depot_contract(ContractUnit(_owner=zoa_text), assignment_text)

    # THEN
    print(f"{owner_x._isol._members.keys()=}")
    assert owner_x._isol.get_members_depotlink_count() == 4
