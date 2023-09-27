from src.economy.economy import economyunit_shop
from src.contract.contract import ContractUnit
from src.contract.member import memberunit_shop
from src.contract.road import get_default_economy_root_label as root_label
from src.economy.examples.economy_env_kit import (
    get_temp_env_title,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from src.economy.bank_sqlstr import (
    get_river_flow_table_insert_sqlstr as river_flow_insert,
    get_river_flow_dict,
    get_river_bucket_table_insert_sqlstr,
    get_river_bucket_dict,
    get_river_bucket_table_delete_sqlstr,
    get_river_tmember_table_insert_sqlstr,
    get_river_tmember_dict,
    get_ledger_table_insert_sqlstr,
    get_ledger_dict,
    LedgerUnit,
    RiverLedgerUnit,
    RiverFlowUnit,
    get_river_ledger_unit,
    get_idea_catalog_table_count,
    IdeaCatalog,
    get_idea_catalog_table_insert_sqlstr,
    get_idea_catalog_dict,
    get_acptfact_catalog_table_count,
    AcptFactCatalog,
    get_acptfact_catalog_table_insert_sqlstr,
    get_groupunit_catalog_table_count,
    GroupUnitCatalog,
    get_groupunit_catalog_table_insert_sqlstr,
    get_groupunit_catalog_dict,
    get_table_count_sqlstr,
)
from src.economy.examples.example_actors import (
    get_3node_contract,
    get_6node_contract,
    get_contract_3CleanNodesRandomWeights,
)
from src.economy.y_func import get_single_result_back


def test_economy_get_ledger_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows

    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    tim_text = "tim"
    contract_x = ContractUnit(_owner=bob_text)
    memberunit_x = memberunit_shop(
        name=tim_text,
        _contract_credit=0.9,
        _contract_debt=0.8,
        _contract_agenda_credit=0.7,
        _contract_agenda_debt=0.6,
        _contract_agenda_ratio_credit=0.5,
        _contract_agenda_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )

    insert_sqlstr = get_ledger_table_insert_sqlstr(
        contract_x=contract_x, memberunit_x=memberunit_x
    )
    print(insert_sqlstr)

    # WHEN
    with sx.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr)

    ledger_dict = get_ledger_dict(db_conn=sx.get_bank_conn(), payer_name=bob_text)
    # ledger_x = None
    # for key, value in ledger_dict.items():
    #     print(f"{key=} {value=}")
    #     ledger_x = value

    # THEN
    ledger_x = ledger_dict.get(tim_text)
    assert ledger_x.contract_owner == bob_text
    assert ledger_x.member_name == tim_text
    assert ledger_x._contract_credit == 0.9
    assert ledger_x._contract_debt == 0.8
    assert ledger_x._contract_agenda_credit == 0.7
    assert ledger_x._contract_agenda_debt == 0.6
    assert ledger_x._contract_agenda_ratio_credit == 0.5
    assert ledger_x._contract_agenda_ratio_debt == 0.4
    assert ledger_x._creditor_active
    assert ledger_x._debtor_active == False


def test_RiverFlowUnit_exists():
    # GIVEN
    bob_text = "bob"
    tom_text = "tom"
    currency_onset = 400
    currency_cease = 600
    river_tree_level = 6
    flow_num = 89
    parent_flow_num = None

    # WHEN
    river_flow_x = RiverFlowUnit(
        currency_contract_owner=bob_text,
        src_name=None,
        dst_name=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        flow_num=flow_num,
        parent_flow_num=parent_flow_num,
        river_tree_level=river_tree_level,
    )

    # THEN
    assert river_flow_x.currency_contract_owner == bob_text
    assert river_flow_x.src_name is None
    assert river_flow_x.dst_name == tom_text
    assert river_flow_x.currency_start == currency_onset
    assert river_flow_x.currency_close == currency_cease
    assert river_flow_x.flow_num == flow_num
    assert river_flow_x.parent_flow_num == parent_flow_num
    assert river_flow_x.river_tree_level == river_tree_level


def test_RiverFlowUnit_flow_returned_WorksCorrectly():
    # GIVEN
    bob_text = "bob"
    sal_text = "sal"
    tom_text = "tom"
    currency_onset = 400
    currency_cease = 600
    river_tree_level = 6
    flow_num = 89
    parent_flow_num = None

    # WHEN
    river_flow_x = RiverFlowUnit(
        currency_contract_owner=bob_text,
        src_name=sal_text,
        dst_name=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        flow_num=flow_num,
        parent_flow_num=parent_flow_num,
        river_tree_level=river_tree_level,
    )
    assert river_flow_x.currency_contract_owner != river_flow_x.dst_name

    # THEN
    assert river_flow_x.flow_returned() == False

    # WHEN
    river_flow_x.dst_name = bob_text

    # THEN
    assert river_flow_x.flow_returned()


def test_get_river_ledger_unit_CorrectlyReturnsRiverLedgerUnit(env_dir_setup_cleanup):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows

    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    sal_text = "sal"
    contract_bob = ContractUnit(_owner=bob_text)
    memberunit_sal = memberunit_shop(
        name=sal_text,
        _contract_credit=0.9,
        _contract_debt=0.8,
        _contract_agenda_credit=0.7,
        _contract_agenda_debt=0.6,
        _contract_agenda_ratio_credit=0.5,
        _contract_agenda_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_ledger_table_insert_sqlstr(
        contract_x=contract_bob, memberunit_x=memberunit_sal
    )

    tim_text = "tim"
    memberunit_tim = memberunit_shop(
        name=tim_text,
        _contract_credit=0.012,
        _contract_debt=0.017,
        _contract_agenda_credit=0.077,
        _contract_agenda_debt=0.066,
        _contract_agenda_ratio_credit=0.051,
        _contract_agenda_ratio_debt=0.049,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tim = get_ledger_table_insert_sqlstr(
        contract_x=contract_bob, memberunit_x=memberunit_tim
    )

    with sx.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr_sal)
        bank_conn.execute(insert_sqlstr_tim)
        ledger_dict_x = get_ledger_dict(db_conn=bank_conn, payer_name=bob_text)

    # WHEN
    river_flow_x = RiverFlowUnit(
        currency_contract_owner=bob_text,
        src_name=None,
        dst_name=bob_text,
        currency_start=0.225,
        currency_close=0.387,
        flow_num=51,
        parent_flow_num=6,
        river_tree_level=4,
    )
    with sx.get_bank_conn() as bank_conn:
        river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

    # THEN
    assert river_ledger_x.contract_owner == bob_text
    assert river_ledger_x.currency_onset == 0.225
    assert river_ledger_x.currency_cease == 0.387
    assert river_ledger_x.river_tree_level == 4
    assert river_ledger_x._ledgers == ledger_dict_x
    assert river_ledger_x.flow_num == 51


def test_river_flow_insert_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows

    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tim_text = "tim"
    sal_text = "sal"

    river_flow_unit = RiverFlowUnit(
        currency_contract_owner=bob_text,
        src_name=tim_text,
        dst_name=sal_text,
        currency_start=0.2,
        currency_close=0.5,
        flow_num=5,
        river_tree_level=6,
        parent_flow_num=8,
    )
    insert_sqlstr = river_flow_insert(river_flow_unit)
    print(insert_sqlstr)

    # WHEN
    with sx.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr)
        river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=bob_text)
        print(f"{river_flows=}")

    # THEN
    print(f"{river_flows.keys()=}")
    # for value in river_flows.values():
    flow_0 = river_flows.get(0)
    assert flow_0.currency_contract_owner == bob_text
    assert flow_0.src_name == tim_text
    assert flow_0.dst_name == sal_text
    assert flow_0.currency_start == 0.2
    assert flow_0.currency_close == 0.5
    assert flow_0.flow_num == 5
    assert flow_0.river_tree_level == 6
    assert flow_0.parent_flow_num == 8


def test_RiverLedgerUnit_Exists():
    # GIVEN
    bob_text = "bob"
    sal_text = "sal"
    tom_text = "tom"
    ledger_unit_01 = LedgerUnit(
        contract_owner=bob_text,
        member_name=sal_text,
        _contract_credit=0.66,
        _contract_debt=0.2,
        _contract_agenda_credit=0.4,
        _contract_agenda_debt=0.15,
        _contract_agenda_ratio_credit=0.5,
        _contract_agenda_ratio_debt=0.12,
        _creditor_active=True,
        _debtor_active=True,
    )
    ledger_unit_02 = LedgerUnit(
        contract_owner=bob_text,
        member_name=tom_text,
        _contract_credit=0.05,
        _contract_debt=0.09,
        _contract_agenda_credit=0.055,
        _contract_agenda_debt=0.0715,
        _contract_agenda_ratio_credit=0.00995,
        _contract_agenda_ratio_debt=0.00012,
        _creditor_active=True,
        _debtor_active=True,
    )
    ledger_dict = {
        ledger_unit_01.member_name: ledger_unit_01,
        ledger_unit_02.member_name: ledger_unit_02,
    }

    # WHEN
    river_ledger_unit = RiverLedgerUnit(
        contract_owner=bob_text,
        currency_onset=0.6,
        currency_cease=0.8,
        _ledgers=ledger_dict,
        river_tree_level=7,
        flow_num=89,
    )

    # THEN
    assert river_ledger_unit.contract_owner == bob_text
    assert river_ledger_unit.currency_onset == 0.6
    assert river_ledger_unit.currency_cease == 0.8
    assert river_ledger_unit.river_tree_level == 7
    assert river_ledger_unit.flow_num == 89
    assert river_ledger_unit._ledgers == ledger_dict
    assert abs(river_ledger_unit.get_range() - 0.2) < 0.00000001


def test_get_river_tmember_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows

    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    contract_bob = ContractUnit(_owner=bob_text)
    memberunit_tom = memberunit_shop(
        name=tom_text,
        _contract_credit=0.9,
        _contract_debt=0.8,
        _contract_agenda_credit=0.7,
        _contract_agenda_debt=0.6,
        _contract_agenda_ratio_credit=0.5,
        _contract_agenda_ratio_debt=0.411,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tom = get_ledger_table_insert_sqlstr(
        contract_x=contract_bob, memberunit_x=memberunit_tom
    )
    memberunit_sal = memberunit_shop(
        name=sal_text,
        _contract_credit=0.9,
        _contract_debt=0.8,
        _contract_agenda_credit=0.7,
        _contract_agenda_debt=0.6,
        _contract_agenda_ratio_credit=0.5,
        _contract_agenda_ratio_debt=0.455,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_ledger_table_insert_sqlstr(
        contract_x=contract_bob, memberunit_x=memberunit_sal
    )

    river_flow_1 = RiverFlowUnit(bob_text, bob_text, tom_text, 0.0, 0.2, 0, None, 1)
    river_flow_2 = RiverFlowUnit(bob_text, bob_text, sal_text, 0.2, 1.0, 0, None, 1)
    river_flow_3 = RiverFlowUnit(bob_text, tom_text, bob_text, 0.0, 0.2, 1, 0, 2)
    river_flow_4 = RiverFlowUnit(bob_text, sal_text, bob_text, 0.2, 1.0, 1, 0, 2)
    sb0 = river_flow_insert(river_flow_1)
    sb1 = river_flow_insert(river_flow_2)
    st0 = river_flow_insert(river_flow_3)
    ss0 = river_flow_insert(river_flow_4)

    with sx.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr_tom)
        bank_conn.execute(insert_sqlstr_sal)
        bank_conn.execute(sb0)
        bank_conn.execute(sb1)
        bank_conn.execute(st0)
        bank_conn.execute(ss0)

    # WHEN
    mstr_sqlstr = get_river_tmember_table_insert_sqlstr(
        currency_contract_owner=bob_text
    )
    with sx.get_bank_conn() as bank_conn:
        print(mstr_sqlstr)
        bank_conn.execute(mstr_sqlstr)

    # THEN
    with sx.get_bank_conn() as bank_conn:
        river_tmembers = get_river_tmember_dict(
            bank_conn, currency_contract_owner=bob_text
        )
        print(f"{river_tmembers=}")

    assert len(river_tmembers) == 2

    bob_tom_x = river_tmembers.get(tom_text)
    assert bob_tom_x.currency_name == bob_text
    assert bob_tom_x.tax_name == tom_text
    assert bob_tom_x.tax_total == 0.2
    assert bob_tom_x.debt == 0.411
    assert round(bob_tom_x.tax_diff, 15) == 0.211

    bob_sal_x = river_tmembers.get(sal_text)
    assert bob_sal_x.currency_name == bob_text
    assert bob_sal_x.tax_name == sal_text
    assert bob_sal_x.tax_total == 0.8
    assert bob_sal_x.debt == 0.455
    assert round(bob_sal_x.tax_diff, 15) == -0.345

    # for value in river_tmembers.values():
    #     assert value.currency_name == bob_text
    #     assert value.tax_name in [tom_text, sal_text]
    #     assert value.tax_total in [0.2, 0.8]
    #     assert value.debt in [0.411, 0.455]
    #     assert round(value.tax_diff, 15) in [0.211, -0.345]


def test_get_river_bucket_table_delete_sqlstr_CorrectlyDeletesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows

    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract = ContractUnit(_owner=sal_text)
    sal_contract.add_memberunit(name=bob_text, creditor_weight=2)
    sal_contract.add_memberunit(name=tom_text, creditor_weight=7)
    sal_contract.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_memberunit(name=sal_text, creditor_weight=3)
    bob_contract.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    sx.refresh_bank_metrics()
    sx.set_river_sphere_for_contract(contract_owner=sal_text)

    with sx.get_bank_conn() as bank_conn:
        assert len(get_river_bucket_dict(bank_conn, sal_text)) > 0

    # WHEN
    sqlstr = get_river_bucket_table_delete_sqlstr(sal_text)
    with sx.get_bank_conn() as bank_conn:
        bank_conn.execute(sqlstr)

    # THEN
    with sx.get_bank_conn() as bank_conn:
        assert len(get_river_bucket_dict(bank_conn, sal_text)) == 0


def test_get_river_bucket_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows

    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract = ContractUnit(_owner=sal_text)
    sal_contract.add_memberunit(name=bob_text, creditor_weight=2)
    sal_contract.add_memberunit(name=tom_text, creditor_weight=7)
    sal_contract.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_owner=bob_text)
    bob_contract.add_memberunit(name=sal_text, creditor_weight=3)
    bob_contract.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_owner=tom_text)
    tom_contract.add_memberunit(name=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_owner=ava_text)
    ava_contract.add_memberunit(name=elu_text, creditor_weight=2)
    sx.save_public_contract(contract_x=ava_contract)

    elu_contract = ContractUnit(_owner=elu_text)
    elu_contract.add_memberunit(name=ava_text, creditor_weight=19)
    elu_contract.add_memberunit(name=sal_text, creditor_weight=1)
    sx.save_public_contract(contract_x=elu_contract)

    sx.refresh_bank_metrics()
    sx.set_river_sphere_for_contract(contract_owner=sal_text, max_flows_count=100)
    with sx.get_bank_conn() as bank_conn:
        bank_conn.execute(get_river_bucket_table_delete_sqlstr(sal_text))
        assert (
            len(get_river_bucket_dict(bank_conn, currency_contract_owner=sal_text)) == 0
        )

    # WHEN / THEN
    mstr_sqlstr = get_river_bucket_table_insert_sqlstr(currency_contract_owner=sal_text)
    with sx.get_bank_conn() as bank_conn:
        print(mstr_sqlstr)
        bank_conn.execute(mstr_sqlstr)
        # river_flows = get_river_flow_dict(bank_conn, currency_contract_owner=sal_text)
        # for river_flow in river_flows.values():
        #     print(f"{river_flow=}")

    # THEN
    with sx.get_bank_conn() as bank_conn:
        river_buckets = get_river_bucket_dict(
            bank_conn, currency_contract_owner=sal_text
        )
        # for river_bucket in river_buckets.values():
        #     print(f"huh {river_bucket=}")

    assert len(river_buckets) == 2
    # for river_bucket in river_buckets:
    #     print(f"{river_bucket=}")

    bucket_0 = river_buckets[0]
    assert bucket_0.currency_name == sal_text
    assert bucket_0.dst_name == sal_text
    assert bucket_0.bucket_num == 0
    assert bucket_0.curr_start == 0.04401266686517654
    assert bucket_0.curr_close == 0.1

    bucket_1 = river_buckets[1]
    assert bucket_1.currency_name == sal_text
    assert bucket_1.dst_name == sal_text
    assert bucket_1.bucket_num == 1
    assert bucket_1.curr_start == 0.12316456150798766
    assert bucket_1.curr_close == 1.0

    # for value in river_buckets.values():
    #     assert value.currency_name == sal_text
    #     assert value.dst_name == sal_text
    #     assert value.bucket_num in [0, 1]
    #     assert value.curr_start in [0.12316456150798766, 0.04401266686517654]
    #     assert value.curr_close in [0.1, 1.0]


def test_economy_get_idea_catalog_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    with sx.get_bank_conn() as bank_conn:
        assert get_idea_catalog_table_count(bank_conn, bob_text) == 0

    # WHEN
    water_road = f"{root_label()},elements,water"
    water_idea_catalog = IdeaCatalog(contract_owner=bob_text, idea_road=water_road)
    water_insert_sqlstr = get_idea_catalog_table_insert_sqlstr(water_idea_catalog)
    with sx.get_bank_conn() as bank_conn:
        print(water_insert_sqlstr)
        bank_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_idea_catalog_table_count(bank_conn, bob_text) == 1


def test_refresh_bank_metrics_Populates_idea_catalog_table(env_dir_setup_cleanup):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows
    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    sal_text = "sal"
    tim_text = "tim"
    bob_contract = get_3node_contract()
    tim_contract = get_6node_contract()
    sal_contract = get_contract_3CleanNodesRandomWeights()
    bob_contract.set_owner(new_owner=bob_text)
    tim_contract.set_owner(new_owner=tim_text)
    sal_contract.set_owner(new_owner=sal_text)
    sx.save_public_contract(contract_x=bob_contract)
    sx.save_public_contract(contract_x=tim_contract)
    sx.save_public_contract(contract_x=sal_contract)

    with sx.get_bank_conn() as bank_conn:
        assert get_idea_catalog_table_count(bank_conn, bob_text) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    with sx.get_bank_conn() as bank_conn:
        assert get_idea_catalog_table_count(bank_conn, bob_text) == 3
        assert get_idea_catalog_table_count(bank_conn, tim_text) == 6
        assert get_idea_catalog_table_count(bank_conn, sal_text) == 5


def test_economy_get_idea_catalog_dict_ReturnsCorrectData(env_dir_setup_cleanup):
    # GIVEN
    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    sal_text = "sal"
    tim_text = "tim"
    elu_text = "elu"
    bob_contract = get_3node_contract()
    tim_contract = get_6node_contract()
    sal_contract = get_contract_3CleanNodesRandomWeights()
    elu_contract = get_6node_contract()
    bob_contract.set_owner(new_owner=bob_text)
    tim_contract.set_owner(new_owner=tim_text)
    sal_contract.set_owner(new_owner=sal_text)
    elu_contract.set_owner(new_owner=elu_text)
    sx.save_public_contract(contract_x=bob_contract)
    sx.save_public_contract(contract_x=tim_contract)
    sx.save_public_contract(contract_x=sal_contract)
    sx.save_public_contract(contract_x=elu_contract)
    sx.refresh_bank_metrics()
    i_count_sqlstr = get_table_count_sqlstr("idea_catalog")
    with sx.get_bank_conn() as bank_conn:
        print(f"{i_count_sqlstr=}")
        assert get_single_result_back(sx.get_bank_conn(), i_count_sqlstr) == 20

    # WHEN / THEN
    assert len(get_idea_catalog_dict(sx.get_bank_conn())) == 20
    b_road = f"{root_label()},B"
    assert len(get_idea_catalog_dict(sx.get_bank_conn(), b_road)) == 3
    ce_road = f"{root_label()},C,E"
    assert len(get_idea_catalog_dict(sx.get_bank_conn(), ce_road)) == 2
    ex_road = f"{root_label()}"
    assert len(get_idea_catalog_dict(sx.get_bank_conn(), ex_road)) == 4


def test_economy_get_acptfact_catalog_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows

    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    with sx.get_bank_conn() as bank_conn:
        assert get_acptfact_catalog_table_count(bank_conn, bob_text) == 0

    # WHEN
    weather_rain = AcptFactCatalog(
        contract_owner=bob_text,
        base=f"{root_label()},weather",
        pick=f"{root_label()},weather,rain",
    )
    water_insert_sqlstr = get_acptfact_catalog_table_insert_sqlstr(weather_rain)
    with sx.get_bank_conn() as bank_conn:
        print(water_insert_sqlstr)
        bank_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_acptfact_catalog_table_count(bank_conn, bob_text) == 1


def test_refresh_bank_metrics_Populates_acptfact_catalog_table(
    env_dir_setup_cleanup,
):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows

    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    # TODO create 3 contracts with varying numbers of acpt facts
    bob_text = "bob"
    sal_text = "sal"
    tim_text = "tim"
    bob_contract = get_3node_contract()
    tim_contract = get_6node_contract()
    sal_contract = get_contract_3CleanNodesRandomWeights()
    bob_contract.set_owner(new_owner=bob_text)
    tim_contract.set_owner(new_owner=tim_text)
    sal_contract.set_owner(new_owner=sal_text)
    c_text = "C"
    c_road = f"{tim_contract._owner},{c_text}"
    f_text = "F"
    f_road = f"{c_road},{f_text}"
    b_text = "B"
    b_road = f"{tim_contract._owner},{b_text}"
    # for idea_x in tim_contract._idea_dict.values():
    #     print(f"{f_road=} {idea_x.get_road()=}")
    tim_contract.set_acptfact(base=c_road, pick=f_road)

    bob_contract.set_acptfact(base=c_road, pick=f_road)
    bob_contract.set_acptfact(base=b_road, pick=b_road)

    casa_text = "casa"
    casa_road = f"{sal_contract._owner},{casa_text}"
    cookery_text = "clean cookery"
    cookery_road = f"{casa_road},{cookery_text}"
    sal_contract.set_acptfact(base=cookery_road, pick=cookery_road)

    sx.save_public_contract(contract_x=bob_contract)
    sx.save_public_contract(contract_x=tim_contract)
    sx.save_public_contract(contract_x=sal_contract)

    with sx.get_bank_conn() as bank_conn:
        assert get_acptfact_catalog_table_count(bank_conn, bob_text) == 0
        assert get_acptfact_catalog_table_count(bank_conn, tim_text) == 0
        assert get_acptfact_catalog_table_count(bank_conn, sal_text) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    print(f"{get_acptfact_catalog_table_count(bank_conn, bob_text)=}")
    print(f"{get_acptfact_catalog_table_count(bank_conn, tim_text)=}")
    print(f"{get_acptfact_catalog_table_count(bank_conn, sal_text)=}")
    with sx.get_bank_conn() as bank_conn:
        assert get_acptfact_catalog_table_count(bank_conn, bob_text) == 2
        assert get_acptfact_catalog_table_count(bank_conn, tim_text) == 1
        assert get_acptfact_catalog_table_count(bank_conn, sal_text) == 1


def test_economy_get_groupunit_catalog_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example economy with 4 Actors, each with 3 Memberunits = 12 ledger rows

    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    with sx.get_bank_conn() as bank_conn:
        assert get_groupunit_catalog_table_count(bank_conn, bob_text) == 0

    # WHEN
    bob_group_x = GroupUnitCatalog(
        contract_owner=bob_text,
        groupunit_name="US Dollar",
        memberlinks_set_by_economy_road=f"{root_label()},USA",
    )
    bob_group_sqlstr = get_groupunit_catalog_table_insert_sqlstr(bob_group_x)
    with sx.get_bank_conn() as bank_conn:
        print(bob_group_sqlstr)
        bank_conn.execute(bob_group_sqlstr)

    # THEN
    assert get_groupunit_catalog_table_count(bank_conn, bob_text) == 1


def test_get_groupunit_catalog_dict_CorrectlyReturnsGroupUnitData(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = economyunit_shop(
        title=get_temp_env_title(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"
    bob_contract = ContractUnit(_owner=bob_text)
    tom_contract = ContractUnit(_owner=tom_text)
    bob_contract.add_memberunit(name=tom_text)
    tom_contract.add_memberunit(name=bob_text)
    tom_contract.add_memberunit(name=elu_text)
    sx.save_public_contract(contract_x=bob_contract)
    sx.save_public_contract(contract_x=tom_contract)
    sx.refresh_bank_metrics()
    sqlstr = get_table_count_sqlstr("groupunit_catalog")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr) == 3

    # WHEN
    with sx.get_bank_conn() as bank_conn:
        print("try to grab GroupUnit data")
        groupunit_catalog_dict = get_groupunit_catalog_dict(db_conn=bank_conn)

    # THEN
    assert len(groupunit_catalog_dict) == 3
    bob_contract_tom_group = f"{bob_text} {tom_text}"
    tom_contract_bob_group = f"{tom_text} {bob_text}"
    tom_contract_elu_group = f"{tom_text} {elu_text}"
    assert groupunit_catalog_dict.get(bob_contract_tom_group) != None
    assert groupunit_catalog_dict.get(tom_contract_bob_group) != None
    assert groupunit_catalog_dict.get(tom_contract_elu_group) != None
