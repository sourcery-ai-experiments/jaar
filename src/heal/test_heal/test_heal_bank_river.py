from src.contract.contract import ContractUnit
from src.heal.heal import healunit_shop
from src.heal.examples.heal_env_kit import (
    get_temp_env_kind,
    get_test_heals_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.heal.y_func import check_connection, get_single_result_back
from src.heal.bank_sqlstr import (
    get_river_tparty_dict,
    get_river_flow_dict,
    get_table_count_sqlstr,
)


def test_heal_set_river_sphere_for_contract_CorrectlyPopulatesriver_tpartyTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example heal with 4 Owners, each with 3 Partyunits = 12 ledger rows
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    sal = ContractUnit(_owner=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1)
    sal.add_partyunit(title=tom_text, creditor_weight=3)
    sx.save_public_contract(contract_x=sal)

    bob = ContractUnit(_owner=bob_text)
    bob.add_partyunit(title=sal_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob)

    tom = ContractUnit(_owner=tom_text)
    tom.add_partyunit(title=sal_text, creditor_weight=1)
    sx.save_public_contract(contract_x=tom)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 4

    sqlstr_count_river_tparty = get_table_count_sqlstr("river_tparty")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 0

    # WHEN
    sx.set_river_sphere_for_contract(contract_owner=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 4
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)

    flow_0 = river_flows.get(0)
    flow_1 = river_flows.get(1)
    assert flow_1.src_title == "sal" and flow_1.dst_title == "tom"
    assert flow_1.river_tree_level == 1
    assert flow_1.currency_start == 0.25
    assert flow_1.currency_close == 1
    assert flow_1.parent_flow_num is None
    flow_2 = river_flows.get(2)
    flow_3 = river_flows.get(3)
    assert flow_3.src_title == "tom" and flow_3.dst_title == "sal"
    assert flow_3.river_tree_level == 2
    assert flow_3.parent_flow_num == 1

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 2

    with sx.get_bank_conn() as bank_conn:
        river_tpartys = get_river_tparty_dict(bank_conn, sal_text)
    assert len(river_tpartys) == 2
    river_sal_tax_bob = river_tpartys.get(bob_text)
    river_sal_tax_tom = river_tpartys.get(tom_text)

    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")

    assert river_sal_tax_bob.tax_total == 0.25
    assert river_sal_tax_tom.tax_total == 0.75


def test_heal_set_river_sphere_for_contract_CorrectlyPopulatesriver_tpartyTable02(
    env_dir_setup_cleanup,
):
    # GIVEN 4 contracts, 100% of river flows to sal
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = ContractUnit(_owner=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    sx.save_public_contract(contract_x=sal)

    bob = ContractUnit(_owner=bob_text)
    bob.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_partyunit(title=tom_text, creditor_weight=1, debtor_weight=1)
    sx.save_public_contract(contract_x=bob)

    tom = ContractUnit(_owner=tom_text)
    tom.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=8)
    sx.save_public_contract(contract_x=tom)

    elu = ContractUnit(_owner=elu_text)
    elu.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=8)
    sx.save_public_contract(contract_x=elu)
    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tparty = get_table_count_sqlstr("river_tparty")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 0

    # WHEN
    sx.set_river_sphere_for_contract(contract_owner=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 9
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 1

    with sx.get_bank_conn() as bank_conn:
        river_tpartys = get_river_tparty_dict(bank_conn, sal_text)
    assert len(river_tpartys) == 1
    assert river_tpartys.get(bob_text) is None
    assert river_tpartys.get(tom_text) is None
    river_sal_tax_elu = river_tpartys.get(elu_text)

    print(f"{river_sal_tax_elu=}")
    assert river_sal_tax_elu.tax_total == 1.0


def test_heal_set_river_sphere_for_contract_CorrectlyPopulatesriver_tpartyTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 contracts, 85% of river flows to sal
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_contract = ContractUnit(_owner=sal_text)
    sal_contract.add_partyunit(title=bob_text, creditor_weight=2)
    sal_contract.add_partyunit(title=tom_text, creditor_weight=7)
    sal_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_partyunit(title=sal_text, creditor_weight=3)
    bob_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_owner=tom_text)
    tom_contract.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_owner=ava_text)
    sx.save_public_contract(contract_x=ava_contract)
    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tparty = get_table_count_sqlstr("river_tparty")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 0

    # WHEN
    sx.set_river_sphere_for_contract(contract_owner=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 6
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 2

    with sx.get_bank_conn() as bank_conn:
        river_tpartys = get_river_tparty_dict(bank_conn, sal_text)
    assert len(river_tpartys) == 2
    assert river_tpartys.get(bob_text) != None
    assert river_tpartys.get(tom_text) != None
    assert river_tpartys.get(ava_text) is None

    river_sal_tax_bob = river_tpartys.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = river_tpartys.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_heal_set_river_sphere_for_contract_CorrectlyPopulatesriver_tpartyTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 contracts, 85% of river flows to sal, left over %15 goes on endless loop
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract = ContractUnit(_owner=sal_text)
    sal_contract.add_partyunit(title=bob_text, creditor_weight=2)
    sal_contract.add_partyunit(title=tom_text, creditor_weight=7)
    sal_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_partyunit(title=sal_text, creditor_weight=3)
    bob_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_owner=tom_text)
    tom_contract.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_owner=ava_text)
    ava_contract.add_partyunit(title=elu_text, creditor_weight=2)
    sx.save_public_contract(contract_x=ava_contract)

    elu_contract = ContractUnit(_owner=elu_text)
    elu_contract.add_partyunit(title=ava_text, creditor_weight=2)
    sx.save_public_contract(contract_x=elu_contract)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 8

    sqlstr_count_river_tparty = get_table_count_sqlstr("river_tparty")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 0

    # WHEN
    sx.set_river_sphere_for_contract(contract_owner=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 40
    # with sx.get_bank_conn() as bank_conn:
    #     river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 2

    with sx.get_bank_conn() as bank_conn:
        river_tpartys = get_river_tparty_dict(bank_conn, sal_text)
    assert len(river_tpartys) == 2
    assert river_tpartys.get(bob_text) != None
    assert river_tpartys.get(tom_text) != None
    assert river_tpartys.get(ava_text) is None

    river_sal_tax_bob = river_tpartys.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = river_tpartys.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_heal_set_river_sphere_for_contract_CorrectlyPopulatesriver_tpartyTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 contracts, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract = ContractUnit(_owner=sal_text)
    sal_contract.add_partyunit(title=bob_text, creditor_weight=2)
    sal_contract.add_partyunit(title=tom_text, creditor_weight=7)
    sal_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_partyunit(title=sal_text, creditor_weight=3)
    bob_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_owner=tom_text)
    tom_contract.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_owner=ava_text)
    ava_contract.add_partyunit(title=elu_text, creditor_weight=2)
    sx.save_public_contract(contract_x=ava_contract)

    elu_contract = ContractUnit(_owner=elu_text)
    elu_contract.add_partyunit(title=ava_text, creditor_weight=19)
    elu_contract.add_partyunit(title=sal_text, creditor_weight=1)
    sx.save_public_contract(contract_x=elu_contract)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tparty = get_table_count_sqlstr("river_tparty")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 0

    # WHEN
    sx.set_river_sphere_for_contract(contract_owner=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 40
    # with sx.get_bank_conn() as bank_conn:
    #     river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 3

    with sx.get_bank_conn() as bank_conn:
        river_tpartys = get_river_tparty_dict(bank_conn, sal_text)
    assert len(river_tpartys) == 3
    assert river_tpartys.get(bob_text) != None
    assert river_tpartys.get(tom_text) != None
    assert river_tpartys.get(elu_text) != None
    assert river_tpartys.get(ava_text) is None

    river_sal_tax_bob = river_tpartys.get(bob_text)
    river_sal_tax_tom = river_tpartys.get(tom_text)
    river_sal_tax_elu = river_tpartys.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7
    # assert round(river_sal_tax_elu.tax_total, 15) == 0.048741092066406
    assert round(river_sal_tax_elu.tax_total, 15) == 0.0378017640625


def test_heal_set_river_sphere_for_contract_CorrectlyDeletesPreviousRiver(
    env_dir_setup_cleanup,
):
    # GIVEN 4 contracts, 100% of river flows to sal
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = ContractUnit(_owner=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    sx.save_public_contract(contract_x=sal)

    bob = ContractUnit(_owner=bob_text)
    bob.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_partyunit(title=tom_text, creditor_weight=1, debtor_weight=1)
    sx.save_public_contract(contract_x=bob)

    tom = ContractUnit(_owner=tom_text)
    tom.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=8)
    sx.save_public_contract(contract_x=tom)

    elu = ContractUnit(_owner=elu_text)
    elu.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=8)
    sx.save_public_contract(contract_x=elu)
    sx.refresh_bank_metrics()

    sx.set_river_sphere_for_contract(contract_owner=sal_text)
    sx.set_river_sphere_for_contract(contract_owner=elu_text)

    sqlstr_count_river_tparty = get_table_count_sqlstr("river_tparty")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 16

    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 3

    # WHEN
    # sal.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    # sx.save_public_contract(contract_x=sal)
    sx.set_river_sphere_for_contract(contract_owner=sal_text)

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 16
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 3


def test_heal_set_river_sphere_for_contract_CorrectlyUsesMaxFlowsCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 contracts, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract = ContractUnit(_owner=sal_text)
    sal_contract.add_partyunit(title=bob_text, creditor_weight=2)
    sal_contract.add_partyunit(title=tom_text, creditor_weight=7)
    sal_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_partyunit(title=sal_text, creditor_weight=3)
    bob_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_owner=tom_text)
    tom_contract.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_owner=ava_text)
    ava_contract.add_partyunit(title=elu_text, creditor_weight=2)
    sx.save_public_contract(contract_x=ava_contract)

    elu_contract = ContractUnit(_owner=elu_text)
    elu_contract.add_partyunit(title=ava_text, creditor_weight=19)
    elu_contract.add_partyunit(title=sal_text, creditor_weight=1)
    sx.save_public_contract(contract_x=elu_contract)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tparty = get_table_count_sqlstr("river_tparty")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 0

    # WHEN
    mtc = 13
    sx.set_river_sphere_for_contract(contract_owner=sal_text, max_flows_count=mtc)

    # THEN
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == mtc


def test_heal_set_river_sphere_for_contract_CorrectlyPopulatesriver_tpartyTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 contracts, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract = ContractUnit(_owner=sal_text)
    sal_contract.add_partyunit(title=bob_text, creditor_weight=2)
    sal_contract.add_partyunit(title=tom_text, creditor_weight=7)
    sal_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_partyunit(title=sal_text, creditor_weight=3)
    bob_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_owner=tom_text)
    tom_contract.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_owner=ava_text)
    ava_contract.add_partyunit(title=elu_text, creditor_weight=2)
    sx.save_public_contract(contract_x=ava_contract)

    elu_contract = ContractUnit(_owner=elu_text)
    elu_contract.add_partyunit(title=ava_text, creditor_weight=19)
    elu_contract.add_partyunit(title=sal_text, creditor_weight=1)
    sx.save_public_contract(contract_x=elu_contract)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tparty = get_table_count_sqlstr("river_tparty")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 0

    # WHEN
    sx.set_river_sphere_for_contract(contract_owner=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 40
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tparty) == 3

    with sx.get_bank_conn() as bank_conn:
        river_tpartys = get_river_tparty_dict(bank_conn, sal_text)
    river_tpartys = sx.get_river_tpartys(sal_text)
    assert len(river_tpartys) == 3
    assert river_tpartys.get(bob_text) != None
    assert river_tpartys.get(tom_text) != None
    assert river_tpartys.get(elu_text) != None
    assert river_tpartys.get(ava_text) is None

    river_sal_tax_bob = river_tpartys.get(bob_text)
    river_sal_tax_tom = river_tpartys.get(tom_text)
    river_sal_tax_elu = river_tpartys.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7
    # assert round(river_sal_tax_elu.tax_total, 15) == 0.048741092066406
    assert round(river_sal_tax_elu.tax_total, 15) == 0.0378017640625


def test_heal_set_river_sphere_for_contract_CorrectlyBuildsASingleContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 contracts, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract = ContractUnit(_owner=sal_text)
    sal_contract.add_partyunit(title=bob_text, creditor_weight=2)
    sal_contract.add_partyunit(title=tom_text, creditor_weight=7)
    sal_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_partyunit(title=sal_text, creditor_weight=3)
    bob_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_owner=tom_text)
    tom_contract.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_owner=ava_text)
    ava_contract.add_partyunit(title=elu_text, creditor_weight=2)
    sx.save_public_contract(contract_x=ava_contract)

    elu_contract = ContractUnit(_owner=elu_text)
    elu_contract.add_partyunit(title=ava_text, creditor_weight=19)
    elu_contract.add_partyunit(title=sal_text, creditor_weight=1)
    sx.save_public_contract(contract_x=elu_contract)

    sx.refresh_bank_metrics()

    # WHEN
    sx.set_river_sphere_for_contract(contract_owner=sal_text, max_flows_count=100)

    # THEN
    count_range_fails_sql = """
    SELECT COUNT(*)
    FROM (
        SELECT 
            rt1.currency_start current_row_start
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) AS prev_close
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) - rt1.currency_start prev_diff
        , rt1.flow_num or_flow_num
        , lag(flow_num) OVER (ORDER BY currency_start, currency_close) AS prev_flow_num
        , rt1.parent_flow_num or_parent_flow_num
        , lag(parent_flow_num) OVER (ORDER BY currency_start, currency_close) AS prev_parent_flow_num
        , river_tree_level
        , lag(river_tree_level) OVER (ORDER BY currency_start, currency_close) AS prev_parent_river_tree_level
        FROM river_flow rt1
        --  WHERE dst_title = 'sal' and currency_title = dst_title
        ORDER BY rt1.currency_start, rt1.currency_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with sx.get_bank_conn() as bank_conn:
        assert get_single_result_back(bank_conn, count_range_fails_sql) == 0


def test_heal_set_river_sphere_for_contract_CorrectlyUpatesContractPartyUnits(
    env_dir_setup_cleanup,
):
    # GIVEN 5 contracts, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    heal_kind = get_temp_env_kind()
    sx = healunit_shop(kind=heal_kind, heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract_src = ContractUnit(_owner=sal_text)
    sal_contract_src.add_partyunit(title=bob_text, creditor_weight=2, debtor_weight=2)
    sal_contract_src.add_partyunit(title=tom_text, creditor_weight=2, debtor_weight=1)
    sal_contract_src.add_partyunit(title=ava_text, creditor_weight=2, debtor_weight=2)
    sx.save_public_contract(contract_x=sal_contract_src)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_partyunit(title=sal_text, creditor_weight=3)
    bob_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_owner=tom_text)
    tom_contract.add_partyunit(title=sal_text)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_owner=ava_text)
    ava_contract.add_partyunit(title=elu_text, creditor_weight=2)
    sx.save_public_contract(contract_x=ava_contract)

    elu_contract = ContractUnit(_owner=elu_text)
    elu_contract.add_partyunit(title=ava_text, creditor_weight=8)
    elu_contract.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=elu_contract)

    sx.refresh_bank_metrics()
    sal_contract_before = sx.get_public_contract(owner=sal_text)

    sx.set_river_sphere_for_contract(contract_owner=sal_text, max_flows_count=100)
    assert len(sal_contract_before._partys) == 3
    print(f"{len(sal_contract_before._partys)=}")
    bob_party = sal_contract_before._partys.get(bob_text)
    tom_party = sal_contract_before._partys.get(tom_text)
    ava_party = sal_contract_before._partys.get(ava_text)
    assert bob_party._bank_tax_paid is None
    assert bob_party._bank_tax_diff is None
    assert tom_party._bank_tax_paid is None
    assert tom_party._bank_tax_diff is None
    assert ava_party._bank_tax_paid is None
    assert ava_party._bank_tax_diff is None

    # WHEN
    sx.set_river_sphere_for_contract(contract_owner=sal_text)

    # THEN
    sal_river_tpartys = sx.get_river_tpartys(contract_owner=sal_text)
    assert len(sal_river_tpartys) == 3

    sal_contract_after = sx.get_public_contract(owner=sal_text)

    bob_tparty = sal_river_tpartys.get(bob_text)
    tom_tparty = sal_river_tpartys.get(tom_text)
    elu_tparty = sal_river_tpartys.get(elu_text)
    assert bob_tparty.tax_title == bob_text
    assert tom_tparty.tax_title == tom_text
    assert elu_tparty.tax_title == elu_text
    assert bob_tparty.currency_title == sal_text
    assert tom_tparty.currency_title == sal_text
    assert elu_tparty.currency_title == sal_text

    bob_party = sal_contract_after._partys.get(bob_text)
    tom_party = sal_contract_after._partys.get(tom_text)
    ava_party = sal_contract_after._partys.get(ava_text)
    elu_party = sal_contract_after._partys.get(elu_text)

    assert bob_tparty.tax_total == bob_party._bank_tax_paid
    assert bob_tparty.tax_diff == bob_party._bank_tax_diff
    assert tom_tparty.tax_total == tom_party._bank_tax_paid
    assert tom_tparty.tax_diff == tom_party._bank_tax_diff
    assert elu_party is None
    assert elu_tparty.tax_total < 0.31 and elu_tparty.tax_total > 0.3
    assert elu_tparty.tax_diff is None

    # for tparty_uid, sal_river_tparty in sal_river_tpartys.items():
    #     print(f"{tparty_uid=} {sal_river_tparty=}")
    #     assert sal_river_tparty.currency_title == sal_text
    #     assert sal_river_tparty.tax_title in [bob_text, tom_text, elu_text]
    #     partyunit_x = sal_contract_after._partys.get(sal_river_tparty.tax_title)
    #     if partyunit_x != None:
    #         # print(
    #         #     f"{sal_river_tparty.currency_title=} {sal_river_tparty.tax_title=} {partyunit_x.title=} tax_total: {sal_river_tparty.tax_total} Tax Paid: {partyunit_x._bank_tax_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_river_tparty.currency_title=} {sal_river_tparty.tax_title=} {partyunit_x.title=} tax_diff:  {sal_river_tparty.tax_diff} Tax Paid: {partyunit_x._bank_tax_diff}"
    #         # )
    #         assert sal_river_tparty.tax_total == partyunit_x._bank_tax_paid
    #         assert sal_river_tparty.tax_diff == partyunit_x._bank_tax_diff

    assert sal_river_tpartys.get(ava_text) is None
    assert ava_party._bank_tax_paid is None
    assert ava_party._bank_tax_diff is None

    # for partyunit_x in sal_contract_after._partys.values():
    #     print(f"sal_contract_after {partyunit_x.title=} {partyunit_x._bank_tax_paid=}")
    #     river_tparty_x = sal_river_tpartys.get(partyunit_x.title)
    #     if river_tparty_x is None:
    #         assert partyunit_x._bank_tax_paid is None
    #         assert partyunit_x._bank_tax_diff is None
    #     else:
    #         assert partyunit_x._bank_tax_paid != None
    #         assert partyunit_x._bank_tax_diff != None
    # assert sal_contract_after != sal_contract_before
