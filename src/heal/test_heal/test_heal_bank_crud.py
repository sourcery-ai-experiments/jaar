from src.contract.contract import ContractUnit, IdeaKid, groupunit_shop, partylink_shop
from src.heal.heal import healunit_shop
from src.heal.examples.heal_env_kit import (
    get_temp_env_kind,
    get_test_heals_dir,
    env_dir_setup_cleanup,
)
from src.heal.y_func import get_single_result_back
from src.heal.bank_sqlstr import (
    get_db_tables,
    get_table_count_sqlstr,
)


def test_heal_create_dirs_if_null_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create heal
    sx = healunit_shop(kind=get_temp_env_kind(), heals_dir=get_test_heals_dir())

    # WHEN
    sx.create_dirs_if_null(in_memory_bank=True)

    # THEN
    with sx.get_bank_conn() as bank_conn:
        tables_dict = get_db_tables(bank_conn)

    # row_count = 0
    # for table_title, table_x in tables_dict.items():
    #     row_count += 1
    #     print(f" {table_x=} {row_count}. {table_title=}")

    curr_tables = {
        0: "contractunits",
        1: "ledger",
        2: "river_tparty",
        3: "river_flow",
        4: "river_bucket",
        5: "idea_catalog",
        6: "acptfact_catalog",
        7: "groupunit_catalog",
    }

    assert tables_dict.get(curr_tables[0]) != None
    assert tables_dict.get(curr_tables[1]) != None
    assert tables_dict.get(curr_tables[2]) != None
    assert tables_dict.get(curr_tables[3]) != None
    assert tables_dict.get(curr_tables[4]) != None
    assert tables_dict.get(curr_tables[5]) != None
    assert tables_dict.get(curr_tables[6]) != None
    assert tables_dict.get(curr_tables[7]) != None
    assert len(tables_dict) == len(curr_tables)


def test_heal_refresh_bank_metrics_CorrectlyDeletesOldBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = healunit_shop(kind=get_temp_env_kind(), heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"

    bob = ContractUnit(_owner=bob_text)
    bob.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    sx.save_public_contract(contract_x=bob)
    sx.refresh_bank_metrics()
    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 1

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 1


def test_heal_refresh_bank_metrics_CorrectlyDeletesOldBankFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = healunit_shop(kind=get_temp_env_kind(), heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=False)

    bob_text = "bob"
    tom_text = "tom"

    bob = ContractUnit(_owner=bob_text)
    bob.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    sx.save_public_contract(contract_x=bob)
    sx.refresh_bank_metrics()
    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 1

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 1


def test_heal_refresh_bank_metrics_CorrectlyPopulatesLedgerTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example heal with 4 Owners, each with 3 Partyunits = 12 ledger rows
    sx = healunit_shop(kind=get_temp_env_kind(), heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    bob = ContractUnit(_owner=bob_text)
    bob.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    bob.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=4)
    bob.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    sx.save_public_contract(contract_x=bob)

    sal = ContractUnit(_owner=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    sal.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    sx.save_public_contract(contract_x=sal)

    tom = ContractUnit(_owner=tom_text)
    tom.add_partyunit(title=bob_text, creditor_weight=3, debtor_weight=1)
    tom.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=4)
    tom.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    sx.save_public_contract(contract_x=tom)

    elu = ContractUnit(_owner=elu_text)
    elu.add_partyunit(title=bob_text, creditor_weight=3, debtor_weight=1)
    elu.add_partyunit(title=tom_text, creditor_weight=1, debtor_weight=4)
    elu.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    sx.save_public_contract(contract_x=elu)

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 12


def test_heal_refresh_bank_metrics_CorrectlyPopulatesContractTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example heal with 4 Owners, each with 3 Partyunits = 12 ledger rows
    sx = healunit_shop(kind=get_temp_env_kind(), heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    sx.save_public_contract(contract_x=ContractUnit(_owner=bob_text))
    sx.save_public_contract(contract_x=ContractUnit(_owner=tom_text))
    sx.save_public_contract(contract_x=ContractUnit(_owner=sal_text))
    sx.save_public_contract(contract_x=ContractUnit(_owner=elu_text))

    sqlstr_count_contracts = get_table_count_sqlstr("contractunits")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_contracts) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_contracts) == 4


def test_heal_refresh_bank_metrics_CorrectlyPopulatesContractTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example heal with 4 Owners, each with 3 Partyunits = 12 ledger rows
    sx = healunit_shop(kind=get_temp_env_kind(), heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    sx.save_public_contract(contract_x=ContractUnit(_owner=bob_text))
    sx.save_public_contract(contract_x=ContractUnit(_owner=tom_text))
    sx.save_public_contract(contract_x=ContractUnit(_owner=sal_text))
    sx.save_public_contract(contract_x=ContractUnit(_owner=elu_text))

    sqlstr_count_contracts = get_table_count_sqlstr("contractunits")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_contracts) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_contracts) == 4


def test_heal_refresh_bank_metrics_CorrectlyPopulates_groupunit_catalog(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = healunit_shop(kind=get_temp_env_kind(), heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"
    bob_contract = ContractUnit(_owner=bob_text)
    tom_contract = ContractUnit(_owner=tom_text)
    bob_contract.add_partyunit(title=tom_text)
    tom_contract.add_partyunit(title=bob_text)
    tom_contract.add_partyunit(title=elu_text)
    sx.save_public_contract(contract_x=bob_contract)
    sx.save_public_contract(contract_x=tom_contract)

    sqlstr = get_table_count_sqlstr("groupunit_catalog")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr) == 3


def test_heal_set_contract_bank_attrs_CorrectlyPopulatesContract_Groupunit_Partylinks(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = healunit_shop(kind=get_temp_env_kind(), heals_dir=get_test_heals_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    # create 4 contracts, 1 with group "swimming expert" linked to 1 party
    # two others have idea f"{root_label()},sports,swimming"
    # run set_bank_metrics
    # assert
    # _partylinks_set_by_heal_road
    # assert group "swimming expert" has 1 party
    # change groupunit "swimming expert" _partylinks_set_by_heal_road ==  f"{root_label()}sports,swimmer"
    # run set_bank_metrics
    # assert group "swimming expert" has 2 different party

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_contract = ContractUnit(_owner=sal_text)
    bob_contract = ContractUnit(_owner=bob_text)
    tom_contract = ContractUnit(_owner=tom_text)
    ava_contract = ContractUnit(_owner=ava_text)

    swim_text = "swimming"
    sports_text = "sports"
    sal_sports_road = f"{sx.kind},{sports_text}"
    bob_sports_road = f"{sx.kind},{sports_text}"
    tom_sports_road = f"{sx.kind},{sports_text}"

    sal_contract.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=sal_sports_road)
    bob_contract.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=bob_sports_road)
    tom_contract.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=tom_sports_road)

    sal_contract.add_partyunit(title=bob_text, creditor_weight=2, debtor_weight=2)

    swim_group_text = "swimming expert"
    swim_group_unit = groupunit_shop(brand=swim_group_text)
    bob_link = partylink_shop(title=bob_text)
    swim_group_unit.set_partylink(partylink=bob_link)
    sal_contract.set_groupunit(groupunit=swim_group_unit)

    sx.save_public_contract(contract_x=sal_contract)
    sx.save_public_contract(contract_x=bob_contract)
    sx.save_public_contract(contract_x=tom_contract)
    sx.save_public_contract(contract_x=ava_contract)

    sx.set_contract_bank_attrs(contract_owner=sal_text)
    e1_sal_contract = sx.get_public_contract(owner=sal_text)
    assert len(e1_sal_contract._groups.get(swim_group_text)._partys) == 1

    # WHEN
    # change groupunit "swimming expert" _partylinks_set_by_heal_road ==  f"{root_label()},sports,swimmer"
    sal_swim_road = f"{sal_sports_road},{swim_text}"
    swim_group_unit.set_attr(_partylinks_set_by_heal_road=sal_swim_road)
    sal_contract.set_groupunit(groupunit=swim_group_unit)
    sx.save_public_contract(contract_x=sal_contract)
    sx.set_contract_bank_attrs(contract_owner=sal_text)

    # THEN
    e1_sal_contract = sx.get_public_contract(owner=sal_text)
    assert len(e1_sal_contract._groups.get(swim_group_text)._partys) == 2
