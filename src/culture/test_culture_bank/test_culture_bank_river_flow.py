from src.agenda.agenda import agendaunit_shop, partyunit_shop
from src.culture.culture import (
    cultureunit_shop,
    set_bank_river_tallys_to_agenda_partyunits,
)
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.bank_sqlstr import (
    get_river_flow_table_insert_sqlstr as river_flow_insert,
    get_river_flow_dict,
    get_river_bucket_table_insert_sqlstr,
    get_river_bucket_dict,
    get_river_bucket_table_delete_sqlstr,
    RiverTallyUnit,
    get_river_tally_table_insert_sqlstr,
    get_river_tally_dict,
    get_ledger_table_insert_sqlstr,
    get_ledger_dict,
    LedgerUnit,
    RiverLedgerUnit,
    RiverFlowUnit,
    get_river_ledger_unit,
)


def test_culture_get_ledger_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows

    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    x_culture.refresh_bank_agenda_data()

    bob_text = "bob"
    tim_text = "tim"
    bob_agenda = agendaunit_shop(_healer=bob_text)
    partyunit_x = partyunit_shop(
        title=tim_text,
        _agenda_credit=0.9,
        _agenda_debt=0.8,
        _agenda_goal_credit=0.7,
        _agenda_goal_debt=0.6,
        _agenda_goal_ratio_credit=0.5,
        _agenda_goal_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )

    insert_sqlstr = get_ledger_table_insert_sqlstr(bob_agenda, partyunit_x)
    print(insert_sqlstr)

    # WHEN
    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr)

    ledger_dict = get_ledger_dict(
        db_conn=x_culture.get_bank_conn(), payer_healer=bob_text
    )
    # ledger_x = None
    # for key, value in ledger_dict.items():
    #     print(f"{key=} {value=}")
    #     ledger_x = value

    # THEN
    ledger_x = ledger_dict.get(tim_text)
    assert ledger_x.agenda_healer == bob_text
    assert ledger_x.party_title == tim_text
    assert ledger_x._agenda_credit == 0.9
    assert ledger_x._agenda_debt == 0.8
    assert ledger_x._agenda_goal_credit == 0.7
    assert ledger_x._agenda_goal_debt == 0.6
    assert ledger_x._agenda_goal_ratio_credit == 0.5
    assert ledger_x._agenda_goal_ratio_debt == 0.4
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
        currency_agenda_healer=bob_text,
        src_healer=None,
        dst_healer=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        flow_num=flow_num,
        parent_flow_num=parent_flow_num,
        river_tree_level=river_tree_level,
    )

    # THEN
    assert river_flow_x.currency_agenda_healer == bob_text
    assert river_flow_x.src_healer is None
    assert river_flow_x.dst_healer == tom_text
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
        currency_agenda_healer=bob_text,
        src_healer=sal_text,
        dst_healer=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        flow_num=flow_num,
        parent_flow_num=parent_flow_num,
        river_tree_level=river_tree_level,
    )
    assert river_flow_x.currency_agenda_healer != river_flow_x.dst_healer

    # THEN
    assert river_flow_x.flow_returned() == False

    # WHEN
    river_flow_x.dst_healer = bob_text

    # THEN
    assert river_flow_x.flow_returned()


def test_get_river_ledger_unit_CorrectlyReturnsRiverLedgerUnit(env_dir_setup_cleanup):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows

    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    x_culture.refresh_bank_agenda_data()

    bob_text = "bob"
    sal_text = "sal"
    bob_agenda = agendaunit_shop(_healer=bob_text)
    partyunit_sal = partyunit_shop(
        title=sal_text,
        _agenda_credit=0.9,
        _agenda_debt=0.8,
        _agenda_goal_credit=0.7,
        _agenda_goal_debt=0.6,
        _agenda_goal_ratio_credit=0.5,
        _agenda_goal_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_ledger_table_insert_sqlstr(bob_agenda, partyunit_sal)

    tim_text = "tim"
    partyunit_tim = partyunit_shop(
        title=tim_text,
        _agenda_credit=0.012,
        _agenda_debt=0.017,
        _agenda_goal_credit=0.077,
        _agenda_goal_debt=0.066,
        _agenda_goal_ratio_credit=0.051,
        _agenda_goal_ratio_debt=0.049,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tim = get_ledger_table_insert_sqlstr(bob_agenda, partyunit_tim)

    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr_sal)
        bank_conn.execute(insert_sqlstr_tim)
        ledger_dict_x = get_ledger_dict(db_conn=bank_conn, payer_healer=bob_text)

    # WHEN
    river_flow_x = RiverFlowUnit(
        currency_agenda_healer=bob_text,
        src_healer=None,
        dst_healer=bob_text,
        currency_start=0.225,
        currency_close=0.387,
        flow_num=51,
        parent_flow_num=6,
        river_tree_level=4,
    )
    with x_culture.get_bank_conn() as bank_conn:
        river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

    # THEN
    assert river_ledger_x.agenda_healer == bob_text
    assert river_ledger_x.currency_onset == 0.225
    assert river_ledger_x.currency_cease == 0.387
    assert river_ledger_x.river_tree_level == 4
    assert river_ledger_x._ledgers == ledger_dict_x
    assert river_ledger_x.flow_num == 51


def test_river_flow_insert_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows

    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tim_text = "tim"
    sal_text = "sal"

    river_flow_unit = RiverFlowUnit(
        currency_agenda_healer=bob_text,
        src_healer=tim_text,
        dst_healer=sal_text,
        currency_start=0.2,
        currency_close=0.5,
        flow_num=5,
        river_tree_level=6,
        parent_flow_num=8,
    )
    insert_sqlstr = river_flow_insert(river_flow_unit)
    print(insert_sqlstr)

    # WHEN
    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr)
        river_flows = get_river_flow_dict(bank_conn, currency_agenda_healer=bob_text)
        print(f"{river_flows=}")

    # THEN
    print(f"{river_flows.keys()=}")
    # for value in river_flows.values():
    flow_0 = river_flows.get(0)
    assert flow_0.currency_agenda_healer == bob_text
    assert flow_0.src_healer == tim_text
    assert flow_0.dst_healer == sal_text
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
        agenda_healer=bob_text,
        party_title=sal_text,
        _agenda_credit=0.66,
        _agenda_debt=0.2,
        _agenda_goal_credit=0.4,
        _agenda_goal_debt=0.15,
        _agenda_goal_ratio_credit=0.5,
        _agenda_goal_ratio_debt=0.12,
        _creditor_active=True,
        _debtor_active=True,
    )
    ledger_unit_02 = LedgerUnit(
        agenda_healer=bob_text,
        party_title=tom_text,
        _agenda_credit=0.05,
        _agenda_debt=0.09,
        _agenda_goal_credit=0.055,
        _agenda_goal_debt=0.0715,
        _agenda_goal_ratio_credit=0.00995,
        _agenda_goal_ratio_debt=0.00012,
        _creditor_active=True,
        _debtor_active=True,
    )
    ledger_dict = {
        ledger_unit_01.party_title: ledger_unit_01,
        ledger_unit_02.party_title: ledger_unit_02,
    }

    # WHEN
    river_ledger_unit = RiverLedgerUnit(
        agenda_healer=bob_text,
        currency_onset=0.6,
        currency_cease=0.8,
        _ledgers=ledger_dict,
        river_tree_level=7,
        flow_num=89,
    )

    # THEN
    assert river_ledger_unit.agenda_healer == bob_text
    assert river_ledger_unit.currency_onset == 0.6
    assert river_ledger_unit.currency_cease == 0.8
    assert river_ledger_unit.river_tree_level == 7
    assert river_ledger_unit.flow_num == 89
    assert river_ledger_unit._ledgers == ledger_dict
    assert abs(river_ledger_unit.get_range() - 0.2) < 0.00000001


def test_RiverTallyUnit_exists():
    # GIVEN
    x_currency_healer = "x_currency_healer"
    x_tax_healer = "x_tax_healer"
    x_tax_total = "x_tax_total"
    x_debt = "x_debt"
    x_tax_diff = "x_tax_diff"
    x_credit_score = "credit_score"
    x_voice_rank = "voice_rank"

    # WHEN
    x_rivertally = RiverTallyUnit(
        currency_healer=x_currency_healer,
        tax_healer=x_tax_healer,
        tax_total=x_tax_total,
        debt=x_debt,
        tax_diff=x_tax_diff,
        credit_score=x_credit_score,
        voice_rank=x_voice_rank,
    )

    # THEN
    assert x_rivertally.currency_healer == x_currency_healer
    assert x_rivertally.tax_healer == x_tax_healer
    assert x_rivertally.tax_total == x_tax_total
    assert x_rivertally.debt == x_debt
    assert x_rivertally.tax_diff == x_tax_diff
    assert x_rivertally.credit_score == x_credit_score
    assert x_rivertally.voice_rank == x_voice_rank


def test_agenda_set_banking_data_partyunits_CorrectlySetsPartyUnitBankingAttr():
    # GIVEN
    bob_text = "bob"
    x_agenda = agendaunit_shop(_healer=bob_text)
    x_agenda.set_partys_empty_if_null()
    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    x_agenda.set_partyunit(partyunit=partyunit_shop(title=sam_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(title=wil_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(title=fry_text))
    assert x_agenda._partys.get(sam_text)._bank_tax_paid is None
    assert x_agenda._partys.get(sam_text)._bank_tax_diff is None
    assert x_agenda._partys.get(wil_text)._bank_tax_paid is None
    assert x_agenda._partys.get(wil_text)._bank_tax_diff is None
    assert x_agenda._partys.get(fry_text)._bank_tax_paid is None
    assert x_agenda._partys.get(fry_text)._bank_tax_diff is None
    elu_partyunit = partyunit_shop(title=elu_text)
    elu_partyunit._bank_tax_paid = 0.003
    elu_partyunit._bank_tax_diff = 0.007
    x_agenda.set_partyunit(partyunit=elu_partyunit)
    assert x_agenda._partys.get(elu_text)._bank_tax_paid == 0.003
    assert x_agenda._partys.get(elu_text)._bank_tax_diff == 0.007

    river_tally_sam = RiverTallyUnit(bob_text, sam_text, 0.209, 0, 0.034, None, None)
    river_tally_wil = RiverTallyUnit(bob_text, wil_text, 0.501, 0, 0.024, None, None)
    river_tally_fry = RiverTallyUnit(bob_text, fry_text, 0.111, 0, 0.006, None, None)
    river_tallys = {
        river_tally_sam.tax_healer: river_tally_sam,
        river_tally_wil.tax_healer: river_tally_wil,
        river_tally_fry.tax_healer: river_tally_fry,
    }
    # WHEN
    set_bank_river_tallys_to_agenda_partyunits(x_agenda, river_tallys=river_tallys)

    # THEN
    assert x_agenda._partys.get(sam_text)._bank_tax_paid == 0.209
    assert x_agenda._partys.get(sam_text)._bank_tax_diff == 0.034
    assert x_agenda._partys.get(wil_text)._bank_tax_paid == 0.501
    assert x_agenda._partys.get(wil_text)._bank_tax_diff == 0.024
    assert x_agenda._partys.get(fry_text)._bank_tax_paid == 0.111
    assert x_agenda._partys.get(fry_text)._bank_tax_diff == 0.006
    assert x_agenda._partys.get(elu_text)._bank_tax_paid is None
    assert x_agenda._partys.get(elu_text)._bank_tax_diff is None


def test_get_river_tally_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows

    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    bob_agenda = agendaunit_shop(_healer=bob_text)
    partyunit_tom = partyunit_shop(
        title=tom_text,
        _agenda_credit=0.9,
        _agenda_debt=0.8,
        _agenda_goal_credit=0.7,
        _agenda_goal_debt=0.6,
        _agenda_goal_ratio_credit=0.5,
        _agenda_goal_ratio_debt=0.411,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tom = get_ledger_table_insert_sqlstr(
        x_agenda=bob_agenda, partyunit_x=partyunit_tom
    )
    partyunit_sal = partyunit_shop(
        title=sal_text,
        _agenda_credit=0.9,
        _agenda_debt=0.8,
        _agenda_goal_credit=0.7,
        _agenda_goal_debt=0.6,
        _agenda_goal_ratio_credit=0.5,
        _agenda_goal_ratio_debt=0.455,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_ledger_table_insert_sqlstr(
        x_agenda=bob_agenda, partyunit_x=partyunit_sal
    )

    river_flow_1 = RiverFlowUnit(bob_text, bob_text, tom_text, 0.0, 0.2, 0, None, 1)
    river_flow_2 = RiverFlowUnit(bob_text, bob_text, sal_text, 0.2, 1.0, 0, None, 1)
    river_flow_3 = RiverFlowUnit(bob_text, tom_text, bob_text, 0.0, 0.2, 1, 0, 2)
    river_flow_4 = RiverFlowUnit(bob_text, sal_text, bob_text, 0.2, 1.0, 1, 0, 2)
    sb0 = river_flow_insert(river_flow_1)
    sb1 = river_flow_insert(river_flow_2)
    st0 = river_flow_insert(river_flow_3)
    ss0 = river_flow_insert(river_flow_4)

    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr_tom)
        bank_conn.execute(insert_sqlstr_sal)
        bank_conn.execute(sb0)
        bank_conn.execute(sb1)
        bank_conn.execute(st0)
        bank_conn.execute(ss0)

    # WHEN
    mstr_sqlstr = get_river_tally_table_insert_sqlstr(currency_agenda_healer=bob_text)
    with x_culture.get_bank_conn() as bank_conn:
        print(mstr_sqlstr)
        bank_conn.execute(mstr_sqlstr)

    # THEN
    with x_culture.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, currency_agenda_healer=bob_text)
        print(f"{river_tallys=}")

    assert len(river_tallys) == 2

    bob_tom_x = river_tallys.get(tom_text)
    assert bob_tom_x.currency_healer == bob_text
    assert bob_tom_x.tax_healer == tom_text
    assert bob_tom_x.tax_total == 0.2
    assert bob_tom_x.debt == 0.411
    assert round(bob_tom_x.tax_diff, 15) == 0.211

    bob_sal_x = river_tallys.get(sal_text)
    assert bob_sal_x.currency_healer == bob_text
    assert bob_sal_x.tax_healer == sal_text
    assert bob_sal_x.tax_total == 0.8
    assert bob_sal_x.debt == 0.455
    assert round(bob_sal_x.tax_diff, 15) == -0.345

    # for value in river_tallys.values():
    #     assert value.currency_healer == bob_text
    #     assert value.tax_healer in [tom_text, sal_text]
    #     assert value.tax_total in [0.2, 0.8]
    #     assert value.debt in [0.411, 0.455]
    #     assert round(value.tax_diff, 15) in [0.211, -0.345]


def test_get_river_bucket_table_delete_sqlstr_CorrectlyDeletesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows

    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(title=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(title=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(title=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    x_culture.refresh_bank_agenda_data()
    x_culture.set_river_sphere_for_agenda(agenda_healer=sal_text)

    with x_culture.get_bank_conn() as bank_conn:
        assert len(get_river_bucket_dict(bank_conn, sal_text)) > 0

    # WHEN
    sqlstr = get_river_bucket_table_delete_sqlstr(sal_text)
    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(sqlstr)

    # THEN
    with x_culture.get_bank_conn() as bank_conn:
        assert len(get_river_bucket_dict(bank_conn, sal_text)) == 0


def test_get_river_bucket_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows

    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(title=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(title=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(title=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(title=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(title=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(title=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(title=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_agenda_data()
    x_culture.set_river_sphere_for_agenda(agenda_healer=sal_text, max_flows_count=100)
    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(get_river_bucket_table_delete_sqlstr(sal_text))
        assert (
            len(get_river_bucket_dict(bank_conn, currency_agenda_healer=sal_text)) == 0
        )

    # WHEN / THEN
    mstr_sqlstr = get_river_bucket_table_insert_sqlstr(currency_agenda_healer=sal_text)
    with x_culture.get_bank_conn() as bank_conn:
        print(mstr_sqlstr)
        bank_conn.execute(mstr_sqlstr)
        # river_flows = get_river_flow_dict(bank_conn, currency_agenda_healer=sal_text)
        # for river_flow in river_flows.values():
        #     print(f"{river_flow=}")

    # THEN
    with x_culture.get_bank_conn() as bank_conn:
        river_buckets = get_river_bucket_dict(
            bank_conn, currency_agenda_healer=sal_text
        )
        # for river_bucket in river_buckets.values():
        #     print(f"huh {river_bucket=}")

    assert len(river_buckets) == 2
    # for river_bucket in river_buckets:
    #     print(f"{river_bucket=}")

    bucket_0 = river_buckets[0]
    assert bucket_0.currency_healer == sal_text
    assert bucket_0.dst_healer == sal_text
    assert bucket_0.bucket_num == 0
    assert bucket_0.curr_start == 0.04401266686517654
    assert bucket_0.curr_close == 0.1

    bucket_1 = river_buckets[1]
    assert bucket_1.currency_healer == sal_text
    assert bucket_1.dst_healer == sal_text
    assert bucket_1.bucket_num == 1
    assert bucket_1.curr_start == 0.12316456150798766
    assert bucket_1.curr_close == 1.0

    # for value in river_buckets.values():
    #     assert value.currency_healer == sal_text
    #     assert value.dst_healer == sal_text
    #     assert value.bucket_num in [0, 1]
    #     assert value.curr_start in [0.12316456150798766, 0.04401266686517654]
    #     assert value.curr_close in [0.1, 1.0]
