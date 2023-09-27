from src.economy.economy import economyunit_shop
from src.contract.contract import ContractUnit
from src.contract.examples.example_contracts import (
    get_contract_1Task_1CE0MinutesRequired_1AcptFact as example_contracts_get_contract_1Task_1CE0MinutesRequired_1AcptFact,
    contract_v001 as example_contracts_contract_v001,
)
import src.economy.examples.example_actors as example_actors
from os import path as os_path
from src.economy.examples.economy_env_kit import (
    get_temp_env_title,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_economy_set_contract_CreatesContractFile(env_dir_setup_cleanup):
    # GIVEN
    economy_title = get_temp_env_title()
    sx = economyunit_shop(title=economy_title, economys_dir=get_test_economys_dir())
    sx.create_dirs_if_null()
    sx1_obj = example_actors.get_1node_contract()
    sx1_path = f"{sx.get_public_dir()}/{sx1_obj._owner}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    sx.save_public_contract(contract_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_economy_get_contract_currentlyGetsContract(env_dir_setup_cleanup):
    # GIVEN
    economy_title = get_temp_env_title()
    e5 = economyunit_shop(title=economy_title, economys_dir=get_test_economys_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_actors.get_7nodeJRootWithH_contract()
    e5.save_public_contract(contract_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_public_contract(owner=sx5_obj._owner) == sx5_obj


def test_economy_rename_public_contract_ChangesContractName(
    env_dir_setup_cleanup,
):
    # GIVEN
    economy_title = get_temp_env_title()
    e5 = economyunit_shop(title=economy_title, economys_dir=get_test_economys_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_contract_owner = "old1"
    sx5_obj = ContractUnit(_owner=old_contract_owner)
    old_sx5_path = f"{e5.get_public_dir()}/{old_contract_owner}.json"
    e5.save_public_contract(contract_x=sx5_obj)
    print(f"{old_sx5_path=}")

    # WHEN
    new_contract_owner = "new1"
    new_sx5_path = f"{e5.get_public_dir()}/{new_contract_owner}.json"
    assert os_path.exists(new_sx5_path) == False
    assert os_path.exists(old_sx5_path)
    e5.rename_public_contract(
        old_owner=old_contract_owner, new_owner=new_contract_owner
    )

    # THEN
    assert os_path.exists(old_sx5_path) == False
    assert os_path.exists(new_sx5_path)


def test_economy_SetsIdeaRootLabel(
    env_dir_setup_cleanup,
):
    # GIVEN
    economy_title = get_temp_env_title()
    e5 = economyunit_shop(title=economy_title, economys_dir=get_test_economys_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    contract_x = example_contracts_get_contract_1Task_1CE0MinutesRequired_1AcptFact()
    assert contract_x._idearoot._label == "A"

    # WHEN
    e5.save_public_contract(contract_x)

    # THEN
    contract_after = e5.get_public_contract(contract_x._owner)
    assert contract_after._idearoot._label == economy_title
