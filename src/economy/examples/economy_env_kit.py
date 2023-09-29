# from lw.contract import ContractUnit
from src.economy.economy import EconomyUnit, economyunit_shop
from os import listdir as os_listdir, rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture
from src.contract.examples.example_contracts import (
    contract_v001 as example_contracts_contract_v001,
    contract_v002 as example_contracts_contract_v002,
    get_contract_1Task_1CE0MinutesRequired_1AcptFact as example_contracts_get_contract_1Task_1CE0MinutesRequired_1AcptFact,
    get_contract_with7amCleanTableRequired as example_contracts_get_contract_with7amCleanTableRequired,
    get_contract_base_time_example as example_contracts_get_contract_base_time_example,
    get_contract_x1_3levels_1required_1acptfacts as example_contracts_get_contract_x1_3levels_1required_1acptfacts,
)
from src.economy.examples.example_owners import (
    get_1node_contract as example_owners_get_1node_contract,
    get_7nodeJRootWithH_contract as example_owners_get_7nodeJRootWithH_contract,
    get_contract_2CleanNodesRandomWeights as example_owners_get_contract_2CleanNodesRandomWeights,
    get_contract_3CleanNodesRandomWeights as example_owners_get_contract_3CleanNodesRandomWeights,
)
from src.contract.contract import ContractUnit
from src.economy.owner import ownerunit_shop
from src.contract.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    copy_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)


def get_temp_env_title():
    return "ex_env04"


def get_temp_env_dir():
    return f"{get_test_economys_dir()}/{get_temp_env_title()}"


def get_test_economys_dir():
    return "src/economy/examples/economys"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)


def create_contract_file_for_economys(economy_dir: str, contract_owner: str):
    contract_x = ContractUnit(_owner=contract_owner)
    contract_dir = f"{economy_dir}/contracts"
    # file_path = f"{contract_dir}/{contract_x._owner}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {contract_x._owner=}")

    x_func_save_file(
        dest_dir=contract_dir,
        file_name=f"{contract_x._owner}.json",
        file_text=contract_x.get_json(),
    )


def create_example_economys_list():
    return x_func_dir_files(
        dir_path=get_test_economys_dir(), include_dirs=True, include_files=False
    )


def setup_test_example_environment():
    _delete_and_set_ex3()
    _delete_and_set_ex4()
    _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex3():
    economy_title = "ex3"
    sx = economyunit_shop(title=economy_title, economys_dir=get_test_economys_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sx.save_public_contract(contract_x=example_owners_get_1node_contract())
    sx.save_public_contract(
        contract_x=example_contracts_get_contract_1Task_1CE0MinutesRequired_1AcptFact()
    )
    sx.save_public_contract(contract_x=example_contracts_contract_v001())
    sx.save_public_contract(contract_x=example_contracts_contract_v002())

    # sx.set_owner(owner_x=ownerunit_shop(name="w1", env_dir=sx.get_object_root_dir()))
    # sx.set_owner(owner_x=ownerunit_shop(name="w2", env_dir=sx.get_object_root_dir()))
    xia_text = "Xia"
    sx.create_new_ownerunit(owner_name=xia_text)
    owner_text = "Mycontract"
    sx.set_owner_depotlink(
        xia_text, contract_owner=owner_text, depotlink_type="blind_trust"
    )
    # w1_obj = sx.get_owner_obj(name=w1_text)

    bob_text = "bob wurld"
    create_contract_file_for_economys(sx.get_object_root_dir(), bob_text)
    # print(f"create contract_list {w1_text=}")
    sx.create_depotlink_to_generated_contract(
        owner_name=xia_text, contract_owner=bob_text, depotlink_type="ignore"
    )
    land_text = "tim wurld"
    create_contract_file_for_economys(
        economy_dir=sx.get_object_root_dir(), contract_owner=land_text
    )
    sx.create_depotlink_to_generated_contract(
        owner_name=xia_text, contract_owner=land_text, depotlink_type="blind_trust"
    )
    # sx.create_depotlink_to_generated_contract(owner_name=w1_text, contract_owner="test9")
    # sx.create_depotlink_to_generated_contract(owner_name=w1_text, contract_owner="Bobs contract")
    sx.save_owner_file(owner_name=xia_text)
    # print(f"WHAT WHAT {sx.get_object_root_dir()}")
    # print(f"WHAT WHAT {sx.get_object_root_dir()}/owners/w1/w1.json")
    # file_text = x_func_open_file(
    #     dest_dir=f"{sx.get_object_root_dir}/owners/w1", file_name="w1.json"
    # )
    # print(f"{file_text=}")
    # print(f"{len(sx._ownerunits.get(w1_text)._depotlinks)=}")
    # print(f"{sx._ownerunits.get(w1_text)._depotlinks.get(bob_text)=}")
    # print(f"{sx._ownerunits.get(w1_text).get_json=}")

    w2_text = "w2"
    sx.create_new_ownerunit(owner_name=w2_text)  # , env_dir=sx.get_object_root_dir())
    sx.save_owner_file(owner_name=w2_text)


def _delete_and_set_ex4():
    economy_title = "ex4"
    sx = economyunit_shop(title=economy_title, economys_dir=get_test_economys_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.save_public_contract(example_owners_get_7nodeJRootWithH_contract())
    sx.save_public_contract(example_contracts_get_contract_with7amCleanTableRequired())
    sx.save_public_contract(example_contracts_get_contract_base_time_example())
    sx.save_public_contract(
        example_contracts_get_contract_x1_3levels_1required_1acptfacts()
    )


def _delete_and_set_ex5():
    economy_title = "ex5"
    sx = economyunit_shop(title=economy_title, economys_dir=get_test_economys_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    # ethical code ernie
    # ethical code steve
    # ethical code Jessica
    # ethical code Francine
    # ethical code Clay
    contract_1 = example_owners_get_contract_2CleanNodesRandomWeights(_owner="ernie")
    contract_2 = example_owners_get_contract_2CleanNodesRandomWeights(_owner="steve")
    contract_3 = example_owners_get_contract_2CleanNodesRandomWeights(_owner="jessica")
    contract_4 = example_owners_get_contract_2CleanNodesRandomWeights(_owner="francine")
    contract_5 = example_owners_get_contract_2CleanNodesRandomWeights(_owner="clay")

    sx.save_public_contract(contract_x=contract_1)
    sx.save_public_contract(contract_x=contract_2)
    sx.save_public_contract(contract_x=contract_3)
    sx.save_public_contract(contract_x=contract_4)
    sx.save_public_contract(contract_x=contract_5)

    sx.create_new_ownerunit(owner_name=contract_1._owner)
    sx.create_new_ownerunit(owner_name=contract_2._owner)
    sx.create_new_ownerunit(owner_name=contract_3._owner)
    sx.create_new_ownerunit(owner_name=contract_4._owner)
    sx.create_new_ownerunit(owner_name=contract_5._owner)

    sx.set_owner_depotlink(contract_1._owner, contract_2._owner, "blind_trust", 3, 3.1)
    sx.set_owner_depotlink(contract_1._owner, contract_3._owner, "blind_trust", 7, 7.1)
    sx.set_owner_depotlink(contract_1._owner, contract_4._owner, "blind_trust", 4, 4.1)
    sx.set_owner_depotlink(contract_1._owner, contract_5._owner, "blind_trust", 5, 5.1)

    sx.set_owner_depotlink(contract_2._owner, contract_1._owner, "blind_trust", 3, 3.1)
    sx.set_owner_depotlink(contract_2._owner, contract_3._owner, "blind_trust", 7, 7.1)
    sx.set_owner_depotlink(contract_2._owner, contract_4._owner, "blind_trust", 4, 4.1)
    icx = example_owners_get_contract_3CleanNodesRandomWeights()
    sx.set_owner_depotlink(contract_2._owner, contract_5._owner, "ignore", 5, 5.1, icx)

    sx.set_owner_depotlink(contract_3._owner, contract_1._owner, "blind_trust", 3, 3.1)
    sx.set_owner_depotlink(contract_3._owner, contract_2._owner, "blind_trust", 7, 7.1)
    sx.set_owner_depotlink(contract_3._owner, contract_4._owner, "blind_trust", 4, 4.1)
    sx.set_owner_depotlink(contract_3._owner, contract_5._owner, "blind_trust", 5, 5.1)

    sx.set_owner_depotlink(contract_4._owner, contract_1._owner, "blind_trust", 3, 3.1)
    sx.set_owner_depotlink(contract_4._owner, contract_2._owner, "blind_trust", 7, 7.1)
    sx.set_owner_depotlink(contract_4._owner, contract_3._owner, "blind_trust", 4, 4.1)
    sx.set_owner_depotlink(contract_4._owner, contract_5._owner, "blind_trust", 5, 5.1)

    sx.set_owner_depotlink(contract_5._owner, contract_1._owner, "blind_trust", 3, 3.1)
    sx.set_owner_depotlink(contract_5._owner, contract_2._owner, "blind_trust", 7, 7.1)
    sx.set_owner_depotlink(contract_5._owner, contract_3._owner, "blind_trust", 4, 4.1)
    sx.set_owner_depotlink(contract_5._owner, contract_4._owner, "blind_trust", 5, 5.1)

    sx.save_owner_file(owner_name=contract_1._owner)
    sx.save_owner_file(owner_name=contract_2._owner)
    sx.save_owner_file(owner_name=contract_3._owner)
    sx.save_owner_file(owner_name=contract_4._owner)
    sx.save_owner_file(owner_name=contract_5._owner)


def _delete_and_set_ex6():
    economy_title = "ex6"
    sx = economyunit_shop(title=economy_title, economys_dir=get_test_economys_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=False)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract = ContractUnit(_owner=sal_text)
    sal_contract.add_partyunit(name=bob_text, creditor_weight=2)
    sal_contract.add_partyunit(name=tom_text, creditor_weight=7)
    sal_contract.add_partyunit(name=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_partyunit(name=sal_text, creditor_weight=3)
    bob_contract.add_partyunit(name=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_owner=tom_text)
    tom_contract.add_partyunit(name=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_owner=ava_text)
    ava_contract.add_partyunit(name=elu_text, creditor_weight=2)
    sx.save_public_contract(contract_x=ava_contract)

    elu_contract = ContractUnit(_owner=elu_text)
    elu_contract.add_partyunit(name=ava_text, creditor_weight=19)
    elu_contract.add_partyunit(name=sal_text, creditor_weight=1)
    sx.save_public_contract(contract_x=elu_contract)

    sx.refresh_bank_metrics()
    sx.set_river_sphere_for_contract(contract_owner=sal_text, max_flows_count=100)


def create_example_economy(economy_title: str):
    sx = economyunit_shop(title=economy_title, economys_dir=get_test_economys_dir())
    sx.create_dirs_if_null(in_memory_bank=True)


def delete_dir_example_economy(economy_obj: EconomyUnit):
    x_func_delete_dir(economy_obj.get_object_root_dir())


def rename_example_economy(economy_obj: EconomyUnit, new_name):
    # base_dir = economy_obj.get_object_root_dir()
    base_dir = "src/economy/examples/economys"
    src_dir = f"{base_dir}/{economy_obj.title}"
    dst_dir = f"{base_dir}/{new_name}"
    os_rename(src=src_dir, dst=dst_dir)
    economy_obj.set_economyunit_title(title=new_name)


class InvalidEconomyCopyException(Exception):
    pass


def copy_evaluation_economy(src_title: str, dest_title: str):
    base_dir = "src/economy/examples/economys"
    new_dir = f"{base_dir}/{dest_title}"
    if os_path.exists(new_dir):
        raise InvalidEconomyCopyException(
            f"Cannot copy economy to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = economy_obj.get_object_root_dir()
    src_dir = f"{base_dir}/{src_title}"
    dest_dir = f"{base_dir}/{dest_title}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
