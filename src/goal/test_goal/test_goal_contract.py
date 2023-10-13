from src.contract.contract import ContractUnit
from src.contract.examples.example_contracts import (
    get_contract_1Task_1CE0MinutesRequired_1AcptFact as example_contracts_get_contract_1Task_1CE0MinutesRequired_1AcptFact,
    contract_v001 as example_contracts_contract_v001,
)
from src.goal.goal import goalunit_shop
from src.goal.examples.example_owners import (
    get_1node_contract as example_owners_get_1node_contract,
    get_1node_contract as example_owners_get_7nodeJRootWithH_contract,
)
from src.goal.examples.goal_env_kit import (
    get_temp_env_kind,
    get_test_goals_dir,
    env_dir_setup_cleanup,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_goal_set_contract_CreatesContractFile(env_dir_setup_cleanup):
    # GIVEN
    goal_kind = get_temp_env_kind()
    sx = goalunit_shop(kind=goal_kind, goals_dir=get_test_goals_dir())
    sx.create_dirs_if_null()
    sx1_obj = example_owners_get_1node_contract()
    sx1_path = f"{sx.get_public_dir()}/{sx1_obj._owner}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    sx.save_public_contract(contract_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_goal_get_contract_currentlyGetsContract(env_dir_setup_cleanup):
    # GIVEN
    goal_kind = get_temp_env_kind()
    e5 = goalunit_shop(kind=goal_kind, goals_dir=get_test_goals_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_owners_get_7nodeJRootWithH_contract()
    e5.save_public_contract(contract_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_public_contract(owner=sx5_obj._owner) == sx5_obj


def test_goal_rename_public_contract_ChangesContractTitle(
    env_dir_setup_cleanup,
):
    # GIVEN
    goal_kind = get_temp_env_kind()
    e5 = goalunit_shop(kind=goal_kind, goals_dir=get_test_goals_dir())
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


def test_goal_SetsIdeaRootLabel(
    env_dir_setup_cleanup,
):
    # GIVEN
    goal_kind = get_temp_env_kind()
    e5 = goalunit_shop(kind=goal_kind, goals_dir=get_test_goals_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    contract_x = example_contracts_get_contract_1Task_1CE0MinutesRequired_1AcptFact()
    assert contract_x._idearoot._label == "A"

    # WHEN
    e5.save_public_contract(contract_x)

    # THEN
    contract_after = e5.get_public_contract(contract_x._owner)
    assert contract_after._idearoot._label == goal_kind
