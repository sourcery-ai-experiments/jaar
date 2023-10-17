from src.oath.oath import OathUnit, partyunit_shop
from src.cure.cure import cureunit_shop
from src.cure.examples.cure_env_kit import (
    get_temp_env_handle,
    get_test_cures_dir,
    env_dir_setup_cleanup,
)
from src.cure.bank_sqlstr import (
    get_river_flow_table_insert_sqlstr as river_flow_insert,
    get_river_flow_dict,
    get_river_bucket_table_insert_sqlstr,
    get_river_bucket_dict,
    get_river_bucket_table_delete_sqlstr,
    get_river_tparty_table_insert_sqlstr,
    get_river_tparty_dict,
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
from src.cure.examples.example_healers import (
    get_3node_oath,
    get_6node_oath,
    get_oath_3CleanNodesRandomWeights,
)
from src.cure.y_func import get_single_result_back


def test_cure_get_ledger_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows

    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    tim_text = "tim"
    oath_x = OathUnit(_healer=bob_text)
    partyunit_x = partyunit_shop(
        title=tim_text,
        _oath_credit=0.9,
        _oath_debt=0.8,
        _oath_agenda_credit=0.7,
        _oath_agenda_debt=0.6,
        _oath_agenda_ratio_credit=0.5,
        _oath_agenda_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )

    insert_sqlstr = get_ledger_table_insert_sqlstr(
        oath_x=oath_x, partyunit_x=partyunit_x
    )
    print(insert_sqlstr)

    # WHEN
    with sx.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr)

    ledger_dict = get_ledger_dict(db_conn=sx.get_bank_conn(), payer_title=bob_text)
    # ledger_x = None
    # for key, value in ledger_dict.items():
    #     print(f"{key=} {value=}")
    #     ledger_x = value

    # THEN
    ledger_x = ledger_dict.get(tim_text)
    assert ledger_x.oath_healer == bob_text
    assert ledger_x.party_title == tim_text
    assert ledger_x._oath_credit == 0.9
    assert ledger_x._oath_debt == 0.8
    assert ledger_x._oath_agenda_credit == 0.7
    assert ledger_x._oath_agenda_debt == 0.6
    assert ledger_x._oath_agenda_ratio_credit == 0.5
    assert ledger_x._oath_agenda_ratio_debt == 0.4
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
        currency_oath_healer=bob_text,
        src_title=None,
        dst_title=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        flow_num=flow_num,
        parent_flow_num=parent_flow_num,
        river_tree_level=river_tree_level,
    )

    # THEN
    assert river_flow_x.currency_oath_healer == bob_text
    assert river_flow_x.src_title is None
    assert river_flow_x.dst_title == tom_text
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
        currency_oath_healer=bob_text,
        src_title=sal_text,
        dst_title=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        flow_num=flow_num,
        parent_flow_num=parent_flow_num,
        river_tree_level=river_tree_level,
    )
    assert river_flow_x.currency_oath_healer != river_flow_x.dst_title

    # THEN
    assert river_flow_x.flow_returned() == False

    # WHEN
    river_flow_x.dst_title = bob_text

    # THEN
    assert river_flow_x.flow_returned()


def test_get_river_ledger_unit_CorrectlyReturnsRiverLedgerUnit(env_dir_setup_cleanup):
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows

    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    sal_text = "sal"
    oath_bob = OathUnit(_healer=bob_text)
    partyunit_sal = partyunit_shop(
        title=sal_text,
        _oath_credit=0.9,
        _oath_debt=0.8,
        _oath_agenda_credit=0.7,
        _oath_agenda_debt=0.6,
        _oath_agenda_ratio_credit=0.5,
        _oath_agenda_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_ledger_table_insert_sqlstr(
        oath_x=oath_bob, partyunit_x=partyunit_sal
    )

    tim_text = "tim"
    partyunit_tim = partyunit_shop(
        title=tim_text,
        _oath_credit=0.012,
        _oath_debt=0.017,
        _oath_agenda_credit=0.077,
        _oath_agenda_debt=0.066,
        _oath_agenda_ratio_credit=0.051,
        _oath_agenda_ratio_debt=0.049,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tim = get_ledger_table_insert_sqlstr(
        oath_x=oath_bob, partyunit_x=partyunit_tim
    )

    with sx.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr_sal)
        bank_conn.execute(insert_sqlstr_tim)
        ledger_dict_x = get_ledger_dict(db_conn=bank_conn, payer_title=bob_text)

    # WHEN
    river_flow_x = RiverFlowUnit(
        currency_oath_healer=bob_text,
        src_title=None,
        dst_title=bob_text,
        currency_start=0.225,
        currency_close=0.387,
        flow_num=51,
        parent_flow_num=6,
        river_tree_level=4,
    )
    with sx.get_bank_conn() as bank_conn:
        river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

    # THEN
    assert river_ledger_x.oath_healer == bob_text
    assert river_ledger_x.currency_onset == 0.225
    assert river_ledger_x.currency_cease == 0.387
    assert river_ledger_x.river_tree_level == 4
    assert river_ledger_x._ledgers == ledger_dict_x
    assert river_ledger_x.flow_num == 51


def test_river_flow_insert_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows

    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tim_text = "tim"
    sal_text = "sal"

    river_flow_unit = RiverFlowUnit(
        currency_oath_healer=bob_text,
        src_title=tim_text,
        dst_title=sal_text,
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
        river_flows = get_river_flow_dict(bank_conn, currency_oath_healer=bob_text)
        print(f"{river_flows=}")

    # THEN
    print(f"{river_flows.keys()=}")
    # for value in river_flows.values():
    flow_0 = river_flows.get(0)
    assert flow_0.currency_oath_healer == bob_text
    assert flow_0.src_title == tim_text
    assert flow_0.dst_title == sal_text
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
        oath_healer=bob_text,
        party_title=sal_text,
        _oath_credit=0.66,
        _oath_debt=0.2,
        _oath_agenda_credit=0.4,
        _oath_agenda_debt=0.15,
        _oath_agenda_ratio_credit=0.5,
        _oath_agenda_ratio_debt=0.12,
        _creditor_active=True,
        _debtor_active=True,
    )
    ledger_unit_02 = LedgerUnit(
        oath_healer=bob_text,
        party_title=tom_text,
        _oath_credit=0.05,
        _oath_debt=0.09,
        _oath_agenda_credit=0.055,
        _oath_agenda_debt=0.0715,
        _oath_agenda_ratio_credit=0.00995,
        _oath_agenda_ratio_debt=0.00012,
        _creditor_active=True,
        _debtor_active=True,
    )
    ledger_dict = {
        ledger_unit_01.party_title: ledger_unit_01,
        ledger_unit_02.party_title: ledger_unit_02,
    }

    # WHEN
    river_ledger_unit = RiverLedgerUnit(
        oath_healer=bob_text,
        currency_onset=0.6,
        currency_cease=0.8,
        _ledgers=ledger_dict,
        river_tree_level=7,
        flow_num=89,
    )

    # THEN
    assert river_ledger_unit.oath_healer == bob_text
    assert river_ledger_unit.currency_onset == 0.6
    assert river_ledger_unit.currency_cease == 0.8
    assert river_ledger_unit.river_tree_level == 7
    assert river_ledger_unit.flow_num == 89
    assert river_ledger_unit._ledgers == ledger_dict
    assert abs(river_ledger_unit.get_range() - 0.2) < 0.00000001


def test_get_river_tparty_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows

    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    oath_bob = OathUnit(_healer=bob_text)
    partyunit_tom = partyunit_shop(
        title=tom_text,
        _oath_credit=0.9,
        _oath_debt=0.8,
        _oath_agenda_credit=0.7,
        _oath_agenda_debt=0.6,
        _oath_agenda_ratio_credit=0.5,
        _oath_agenda_ratio_debt=0.411,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tom = get_ledger_table_insert_sqlstr(
        oath_x=oath_bob, partyunit_x=partyunit_tom
    )
    partyunit_sal = partyunit_shop(
        title=sal_text,
        _oath_credit=0.9,
        _oath_debt=0.8,
        _oath_agenda_credit=0.7,
        _oath_agenda_debt=0.6,
        _oath_agenda_ratio_credit=0.5,
        _oath_agenda_ratio_debt=0.455,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_ledger_table_insert_sqlstr(
        oath_x=oath_bob, partyunit_x=partyunit_sal
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
    mstr_sqlstr = get_river_tparty_table_insert_sqlstr(currency_oath_healer=bob_text)
    with sx.get_bank_conn() as bank_conn:
        print(mstr_sqlstr)
        bank_conn.execute(mstr_sqlstr)

    # THEN
    with sx.get_bank_conn() as bank_conn:
        river_tpartys = get_river_tparty_dict(bank_conn, currency_oath_healer=bob_text)
        print(f"{river_tpartys=}")

    assert len(river_tpartys) == 2

    bob_tom_x = river_tpartys.get(tom_text)
    assert bob_tom_x.currency_title == bob_text
    assert bob_tom_x.tax_title == tom_text
    assert bob_tom_x.tax_total == 0.2
    assert bob_tom_x.debt == 0.411
    assert round(bob_tom_x.tax_diff, 15) == 0.211

    bob_sal_x = river_tpartys.get(sal_text)
    assert bob_sal_x.currency_title == bob_text
    assert bob_sal_x.tax_title == sal_text
    assert bob_sal_x.tax_total == 0.8
    assert bob_sal_x.debt == 0.455
    assert round(bob_sal_x.tax_diff, 15) == -0.345

    # for value in river_tpartys.values():
    #     assert value.currency_title == bob_text
    #     assert value.tax_title in [tom_text, sal_text]
    #     assert value.tax_total in [0.2, 0.8]
    #     assert value.debt in [0.411, 0.455]
    #     assert round(value.tax_diff, 15) in [0.211, -0.345]


def test_get_river_bucket_table_delete_sqlstr_CorrectlyDeletesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows

    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_oath = OathUnit(_healer=sal_text)
    sal_oath.add_partyunit(title=bob_text, creditor_weight=2)
    sal_oath.add_partyunit(title=tom_text, creditor_weight=7)
    sal_oath.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_oath(oath_x=sal_oath)

    bob_oath = OathUnit(_healer=bob_text)
    bob_oath.add_partyunit(title=sal_text, creditor_weight=3)
    bob_oath.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_oath(oath_x=bob_oath)

    sx.refresh_bank_metrics()
    sx.set_river_sphere_for_oath(oath_healer=sal_text)

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
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows

    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_oath = OathUnit(_healer=sal_text)
    sal_oath.add_partyunit(title=bob_text, creditor_weight=2)
    sal_oath.add_partyunit(title=tom_text, creditor_weight=7)
    sal_oath.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_oath(oath_x=sal_oath)

    bob_oath = OathUnit(_healer=bob_text)
    bob_oath.add_partyunit(title=sal_text, creditor_weight=3)
    bob_oath.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_oath(oath_x=bob_oath)

    tom_oath = OathUnit(_healer=tom_text)
    tom_oath.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_oath(oath_x=tom_oath)

    ava_oath = OathUnit(_healer=ava_text)
    ava_oath.add_partyunit(title=elu_text, creditor_weight=2)
    sx.save_public_oath(oath_x=ava_oath)

    elu_oath = OathUnit(_healer=elu_text)
    elu_oath.add_partyunit(title=ava_text, creditor_weight=19)
    elu_oath.add_partyunit(title=sal_text, creditor_weight=1)
    sx.save_public_oath(oath_x=elu_oath)

    sx.refresh_bank_metrics()
    sx.set_river_sphere_for_oath(oath_healer=sal_text, max_flows_count=100)
    with sx.get_bank_conn() as bank_conn:
        bank_conn.execute(get_river_bucket_table_delete_sqlstr(sal_text))
        assert len(get_river_bucket_dict(bank_conn, currency_oath_healer=sal_text)) == 0

    # WHEN / THEN
    mstr_sqlstr = get_river_bucket_table_insert_sqlstr(currency_oath_healer=sal_text)
    with sx.get_bank_conn() as bank_conn:
        print(mstr_sqlstr)
        bank_conn.execute(mstr_sqlstr)
        # river_flows = get_river_flow_dict(bank_conn, currency_oath_healer=sal_text)
        # for river_flow in river_flows.values():
        #     print(f"{river_flow=}")

    # THEN
    with sx.get_bank_conn() as bank_conn:
        river_buckets = get_river_bucket_dict(bank_conn, currency_oath_healer=sal_text)
        # for river_bucket in river_buckets.values():
        #     print(f"huh {river_bucket=}")

    assert len(river_buckets) == 2
    # for river_bucket in river_buckets:
    #     print(f"{river_bucket=}")

    bucket_0 = river_buckets[0]
    assert bucket_0.currency_title == sal_text
    assert bucket_0.dst_title == sal_text
    assert bucket_0.bucket_num == 0
    assert bucket_0.curr_start == 0.04401266686517654
    assert bucket_0.curr_close == 0.1

    bucket_1 = river_buckets[1]
    assert bucket_1.currency_title == sal_text
    assert bucket_1.dst_title == sal_text
    assert bucket_1.bucket_num == 1
    assert bucket_1.curr_start == 0.12316456150798766
    assert bucket_1.curr_close == 1.0

    # for value in river_buckets.values():
    #     assert value.currency_title == sal_text
    #     assert value.dst_title == sal_text
    #     assert value.bucket_num in [0, 1]
    #     assert value.curr_start in [0.12316456150798766, 0.04401266686517654]
    #     assert value.curr_close in [0.1, 1.0]


def test_cure_get_idea_catalog_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    with sx.get_bank_conn() as bank_conn:
        assert get_idea_catalog_table_count(bank_conn, bob_text) == 0

    # WHEN
    water_road = f"{get_temp_env_handle()},elements,water"
    water_idea_catalog = IdeaCatalog(oath_healer=bob_text, idea_road=water_road)
    water_insert_sqlstr = get_idea_catalog_table_insert_sqlstr(water_idea_catalog)
    with sx.get_bank_conn() as bank_conn:
        print(water_insert_sqlstr)
        bank_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_idea_catalog_table_count(bank_conn, bob_text) == 1


def test_refresh_bank_metrics_Populates_idea_catalog_table(env_dir_setup_cleanup):
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows
    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    sal_text = "sal"
    tim_text = "tim"
    bob_oath = get_3node_oath()
    tim_oath = get_6node_oath()
    sal_oath = get_oath_3CleanNodesRandomWeights()
    bob_oath.set_healer(new_healer=bob_text)
    tim_oath.set_healer(new_healer=tim_text)
    sal_oath.set_healer(new_healer=sal_text)
    sx.save_public_oath(oath_x=bob_oath)
    sx.save_public_oath(oath_x=tim_oath)
    sx.save_public_oath(oath_x=sal_oath)

    with sx.get_bank_conn() as bank_conn:
        assert get_idea_catalog_table_count(bank_conn, bob_text) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    with sx.get_bank_conn() as bank_conn:
        assert get_idea_catalog_table_count(bank_conn, bob_text) == 3
        assert get_idea_catalog_table_count(bank_conn, tim_text) == 6
        assert get_idea_catalog_table_count(bank_conn, sal_text) == 5


def test_cure_get_idea_catalog_dict_ReturnsCorrectData(env_dir_setup_cleanup):
    # GIVEN
    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    sal_text = "sal"
    tim_text = "tim"
    elu_text = "elu"
    bob_oath = get_3node_oath()
    tim_oath = get_6node_oath()
    sal_oath = get_oath_3CleanNodesRandomWeights()
    elu_oath = get_6node_oath()
    bob_oath.set_healer(new_healer=bob_text)
    tim_oath.set_healer(new_healer=tim_text)
    sal_oath.set_healer(new_healer=sal_text)
    elu_oath.set_healer(new_healer=elu_text)
    sx.save_public_oath(oath_x=bob_oath)
    sx.save_public_oath(oath_x=tim_oath)
    sx.save_public_oath(oath_x=sal_oath)
    sx.save_public_oath(oath_x=elu_oath)
    sx.refresh_bank_metrics()
    i_count_sqlstr = get_table_count_sqlstr("idea_catalog")
    with sx.get_bank_conn() as bank_conn:
        print(f"{i_count_sqlstr=}")
        assert get_single_result_back(sx.get_bank_conn(), i_count_sqlstr) == 20

    # WHEN / THEN
    assert len(get_idea_catalog_dict(sx.get_bank_conn())) == 20
    b_road = f"{get_temp_env_handle()},B"
    assert len(get_idea_catalog_dict(sx.get_bank_conn(), b_road)) == 3
    ce_road = f"{get_temp_env_handle()},C,E"
    assert len(get_idea_catalog_dict(sx.get_bank_conn(), ce_road)) == 2
    ex_road = f"{get_temp_env_handle()}"
    assert len(get_idea_catalog_dict(sx.get_bank_conn(), ex_road)) == 4


def test_cure_get_acptfact_catalog_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows

    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    with sx.get_bank_conn() as bank_conn:
        assert get_acptfact_catalog_table_count(bank_conn, bob_text) == 0

    # WHEN
    weather_rain = AcptFactCatalog(
        oath_healer=bob_text,
        base=f"{get_temp_env_handle()},weather",
        pick=f"{get_temp_env_handle()},weather,rain",
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
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows

    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    # TODO create 3 oaths with varying numbers of acpt facts
    bob_text = "bob"
    sal_text = "sal"
    tim_text = "tim"
    bob_oath = get_3node_oath()
    tim_oath = get_6node_oath()
    sal_oath = get_oath_3CleanNodesRandomWeights()
    bob_oath.set_healer(new_healer=bob_text)
    tim_oath.set_healer(new_healer=tim_text)
    sal_oath.set_healer(new_healer=sal_text)
    c_text = "C"
    c_road = f"{tim_oath._healer},{c_text}"
    f_text = "F"
    f_road = f"{c_road},{f_text}"
    b_text = "B"
    b_road = f"{tim_oath._healer},{b_text}"
    # for idea_x in tim_oath._idea_dict.values():
    #     print(f"{f_road=} {idea_x.get_road()=}")
    tim_oath.set_acptfact(base=c_road, pick=f_road)

    bob_oath.set_acptfact(base=c_road, pick=f_road)
    bob_oath.set_acptfact(base=b_road, pick=b_road)

    casa_text = "casa"
    casa_road = f"{sal_oath._healer},{casa_text}"
    cookery_text = "clean cookery"
    cookery_road = f"{casa_road},{cookery_text}"
    sal_oath.set_acptfact(base=cookery_road, pick=cookery_road)

    sx.save_public_oath(oath_x=bob_oath)
    sx.save_public_oath(oath_x=tim_oath)
    sx.save_public_oath(oath_x=sal_oath)

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


def test_cure_get_groupunit_catalog_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example cure with 4 Healers, each with 3 Partyunits = 12 ledger rows

    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.refresh_bank_metrics()

    bob_text = "bob"
    with sx.get_bank_conn() as bank_conn:
        assert get_groupunit_catalog_table_count(bank_conn, bob_text) == 0

    # WHEN
    bob_group_x = GroupUnitCatalog(
        oath_healer=bob_text,
        groupunit_brand="US Dollar",
        partylinks_set_by_cure_road=f"{get_temp_env_handle()},USA",
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
    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"
    bob_oath = OathUnit(_healer=bob_text)
    tom_oath = OathUnit(_healer=tom_text)
    bob_oath.add_partyunit(title=tom_text)
    tom_oath.add_partyunit(title=bob_text)
    tom_oath.add_partyunit(title=elu_text)
    sx.save_public_oath(oath_x=bob_oath)
    sx.save_public_oath(oath_x=tom_oath)
    sx.refresh_bank_metrics()
    sqlstr = get_table_count_sqlstr("groupunit_catalog")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr) == 3

    # WHEN
    with sx.get_bank_conn() as bank_conn:
        print("try to grab GroupUnit data")
        groupunit_catalog_dict = get_groupunit_catalog_dict(db_conn=bank_conn)

    # THEN
    assert len(groupunit_catalog_dict) == 3
    bob_oath_tom_group = f"{bob_text} {tom_text}"
    tom_oath_bob_group = f"{tom_text} {bob_text}"
    tom_oath_elu_group = f"{tom_text} {elu_text}"
    assert groupunit_catalog_dict.get(bob_oath_tom_group) != None
    assert groupunit_catalog_dict.get(tom_oath_bob_group) != None
    assert groupunit_catalog_dict.get(tom_oath_elu_group) != None
