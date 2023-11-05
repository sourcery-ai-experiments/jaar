from src.agenda.agenda import agendaunit_shop, partyunit_shop
from src.culture.culture import (
    cultureunit_shop,
    set_bank_partybankunits_to_agenda_partyunits,
)
from src.culture.examples.culture_env_kit import (
    get_temp_env_title,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.bank_sqlstr import (
    get_river_block_table_insert_sqlstr as river_block_insert,
    get_river_block_dict,
    get_partyunit_table_update_bank_tax_paid_sqlstr,
    PartyBankUnit,
    get_partybankunit_dict,
    get_partyunit_table_insert_sqlstr,
    get_partyview_dict,
    PartyDBUnit,
    RiverLedgerUnit,
    RiverBlockUnit,
    get_river_ledger_unit,
)


def test_culture_get_partyunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())
    x_culture.refresh_bank_public_agendas_data()

    bob_text = "bob"
    tim_text = "tim"
    bob_agenda = agendaunit_shop(_healer=bob_text)
    tim_partyunit = partyunit_shop(
        handle=tim_text,
        _agenda_credit=0.9,
        _agenda_debt=0.8,
        _agenda_intent_credit=0.7,
        _agenda_intent_debt=0.6,
        _agenda_intent_ratio_credit=0.5,
        _agenda_intent_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )
    tim_tax_paid = 0.5151
    tim_credit_score = 0.5252
    tim_voice_rank = 33
    tim_partyunit.set_banking_data(tim_tax_paid, None, tim_credit_score, tim_voice_rank)
    assert tim_partyunit._bank_tax_paid == tim_tax_paid
    assert tim_partyunit._bank_credit_score == tim_credit_score
    assert tim_partyunit._bank_voice_rank == tim_voice_rank

    insert_sqlstr = get_partyunit_table_insert_sqlstr(bob_agenda, tim_partyunit)
    print(insert_sqlstr)

    # WHEN
    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr)

    ledger_dict = get_partyview_dict(
        db_conn=x_culture.get_bank_conn(), payer_healer=bob_text
    )
    # tim_ledger = None
    # for key, value in ledger_dict.items():
    #     print(f"{key=} {value=}")
    #     tim_ledger = value

    # THEN
    tim_ledger = ledger_dict.get(tim_text)
    assert tim_ledger.agenda_healer == bob_text
    assert tim_ledger.handle == tim_text
    assert tim_ledger._agenda_credit == 0.9
    assert tim_ledger._agenda_debt == 0.8
    assert tim_ledger._agenda_intent_credit == 0.7
    assert tim_ledger._agenda_intent_debt == 0.6
    assert tim_ledger._agenda_intent_ratio_credit == 0.5
    assert tim_ledger._agenda_intent_ratio_debt == 0.4
    assert tim_ledger._creditor_active
    assert tim_ledger._debtor_active == False
    assert tim_ledger._bank_tax_paid == tim_tax_paid
    assert tim_ledger._bank_credit_score == tim_credit_score
    assert tim_ledger._bank_voice_rank == tim_voice_rank


def test_RiverBlockUnit_exists():
    # GIVEN
    bob_text = "bob"
    tom_text = "tom"
    currency_onset = 400
    currency_cease = 600
    river_tree_level = 6
    block_num = 89
    parent_block_num = None

    # WHEN
    river_block_x = RiverBlockUnit(
        currency_agenda_healer=bob_text,
        src_healer=None,
        dst_healer=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        block_num=block_num,
        parent_block_num=parent_block_num,
        river_tree_level=river_tree_level,
    )

    # THEN
    assert river_block_x.currency_agenda_healer == bob_text
    assert river_block_x.src_healer is None
    assert river_block_x.dst_healer == tom_text
    assert river_block_x.currency_start == currency_onset
    assert river_block_x.currency_close == currency_cease
    assert river_block_x.block_num == block_num
    assert river_block_x.parent_block_num == parent_block_num
    assert river_block_x.river_tree_level == river_tree_level


def test_RiverBlockUnit_block_returned_WorksCorrectly():
    # GIVEN
    bob_text = "bob"
    sal_text = "sal"
    tom_text = "tom"
    currency_onset = 400
    currency_cease = 600
    river_tree_level = 6
    block_num = 89
    parent_block_num = None

    # WHEN
    river_block_x = RiverBlockUnit(
        currency_agenda_healer=bob_text,
        src_healer=sal_text,
        dst_healer=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        block_num=block_num,
        parent_block_num=parent_block_num,
        river_tree_level=river_tree_level,
    )
    assert river_block_x.currency_agenda_healer != river_block_x.dst_healer

    # THEN
    assert river_block_x.block_returned() == False

    # WHEN
    river_block_x.dst_healer = bob_text

    # THEN
    assert river_block_x.block_returned()


def test_get_river_ledger_unit_CorrectlyReturnsRiverLedgerUnit(env_dir_setup_cleanup):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())
    x_culture.refresh_bank_public_agendas_data()

    bob_text = "bob"
    sal_text = "sal"
    bob_agenda = agendaunit_shop(_healer=bob_text)
    partyunit_sal = partyunit_shop(
        handle=sal_text,
        _agenda_credit=0.9,
        _agenda_debt=0.8,
        _agenda_intent_credit=0.7,
        _agenda_intent_debt=0.6,
        _agenda_intent_ratio_credit=0.5,
        _agenda_intent_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_partyunit_table_insert_sqlstr(bob_agenda, partyunit_sal)

    tim_text = "tim"
    partyunit_tim = partyunit_shop(
        handle=tim_text,
        _agenda_credit=0.012,
        _agenda_debt=0.017,
        _agenda_intent_credit=0.077,
        _agenda_intent_debt=0.066,
        _agenda_intent_ratio_credit=0.051,
        _agenda_intent_ratio_debt=0.049,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tim = get_partyunit_table_insert_sqlstr(bob_agenda, partyunit_tim)

    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr_sal)
        bank_conn.execute(insert_sqlstr_tim)
        partyview_dict_x = get_partyview_dict(db_conn=bank_conn, payer_healer=bob_text)

    # WHEN
    river_block_x = RiverBlockUnit(
        currency_agenda_healer=bob_text,
        src_healer=None,
        dst_healer=bob_text,
        currency_start=0.225,
        currency_close=0.387,
        block_num=51,
        parent_block_num=6,
        river_tree_level=4,
    )
    with x_culture.get_bank_conn() as bank_conn:
        river_ledger_x = get_river_ledger_unit(bank_conn, river_block_x)

    # THEN
    assert river_ledger_x.agenda_healer == bob_text
    assert river_ledger_x.currency_onset == 0.225
    assert river_ledger_x.currency_cease == 0.387
    assert river_ledger_x.river_tree_level == 4
    assert river_ledger_x._partyviews == partyview_dict_x
    assert river_ledger_x.block_num == 51


def test_river_block_insert_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    bob_text = "bob"
    tim_text = "tim"
    sal_text = "sal"

    river_block_unit = RiverBlockUnit(
        currency_agenda_healer=bob_text,
        src_healer=tim_text,
        dst_healer=sal_text,
        currency_start=0.2,
        currency_close=0.5,
        block_num=5,
        river_tree_level=6,
        parent_block_num=8,
    )
    insert_sqlstr = river_block_insert(river_block_unit)
    print(insert_sqlstr)

    # WHEN
    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr)
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=bob_text)
        print(f"{river_blocks=}")

    # THEN
    print(f"{river_blocks.keys()=}")
    # for value in river_blocks.values():
    block_0 = river_blocks.get(0)
    assert block_0.currency_agenda_healer == bob_text
    assert block_0.src_healer == tim_text
    assert block_0.dst_healer == sal_text
    assert block_0.currency_start == 0.2
    assert block_0.currency_close == 0.5
    assert block_0.block_num == 5
    assert block_0.river_tree_level == 6
    assert block_0.parent_block_num == 8


def test_RiverLedgerUnit_Exists():
    # GIVEN
    bob_text = "bob"
    sal_text = "sal"
    tom_text = "tom"
    x1_partydbunit = PartyDBUnit(
        agenda_healer=bob_text,
        handle=sal_text,
        _agenda_credit=0.66,
        _agenda_debt=0.2,
        _agenda_intent_credit=0.4,
        _agenda_intent_debt=0.15,
        _agenda_intent_ratio_credit=0.5,
        _agenda_intent_ratio_debt=0.12,
        _creditor_active=True,
        _debtor_active=True,
    )
    x2_partydbunit = PartyDBUnit(
        agenda_healer=bob_text,
        handle=tom_text,
        _agenda_credit=0.05,
        _agenda_debt=0.09,
        _agenda_intent_credit=0.055,
        _agenda_intent_debt=0.0715,
        _agenda_intent_ratio_credit=0.00995,
        _agenda_intent_ratio_debt=0.00012,
        _creditor_active=True,
        _debtor_active=True,
    )
    x_partyview_dict = {
        x1_partydbunit.handle: x1_partydbunit,
        x2_partydbunit.handle: x2_partydbunit,
    }
    # WHEN
    river_ledger_unit = RiverLedgerUnit(
        agenda_healer=bob_text,
        currency_onset=0.6,
        currency_cease=0.8,
        _partyviews=x_partyview_dict,
        river_tree_level=7,
        block_num=89,
    )

    # THEN
    assert river_ledger_unit.agenda_healer == bob_text
    assert river_ledger_unit.currency_onset == 0.6
    assert river_ledger_unit.currency_cease == 0.8
    assert river_ledger_unit.river_tree_level == 7
    assert river_ledger_unit.block_num == 89
    assert river_ledger_unit._partyviews == x_partyview_dict
    assert abs(river_ledger_unit.get_range() - 0.2) < 0.00000001


def test_PartyBankUnit_exists():
    # GIVEN
    x_currency_master = "x_currency_master"
    x_tax_healer = "x_tax_healer"
    x_tax_total = "x_tax_total"
    x_debt = "x_debt"
    x_tax_diff = "x_tax_diff"
    x_credit_score = "credit_score"
    x_voice_rank = "voice_rank"

    # WHEN
    x_partybank = PartyBankUnit(
        currency_master=x_currency_master,
        tax_healer=x_tax_healer,
        tax_total=x_tax_total,
        debt=x_debt,
        tax_diff=x_tax_diff,
        credit_score=x_credit_score,
        voice_rank=x_voice_rank,
    )

    # THEN
    assert x_partybank.currency_master == x_currency_master
    assert x_partybank.tax_healer == x_tax_healer
    assert x_partybank.tax_total == x_tax_total
    assert x_partybank.debt == x_debt
    assert x_partybank.tax_diff == x_tax_diff
    assert x_partybank.credit_score == x_credit_score
    assert x_partybank.voice_rank == x_voice_rank


def test_agenda_set_banking_data_partyunits_CorrectlySetsPartyUnitBankingAttr():
    # GIVEN
    bob_text = "bob"
    x_agenda = agendaunit_shop(_healer=bob_text)
    x_agenda.set_partys_empty_if_null()
    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    x_agenda.set_partyunit(partyunit=partyunit_shop(handle=sam_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(handle=wil_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(handle=fry_text))
    assert x_agenda._partys.get(sam_text)._bank_tax_paid is None
    assert x_agenda._partys.get(sam_text)._bank_tax_diff is None
    assert x_agenda._partys.get(wil_text)._bank_tax_paid is None
    assert x_agenda._partys.get(wil_text)._bank_tax_diff is None
    assert x_agenda._partys.get(fry_text)._bank_tax_paid is None
    assert x_agenda._partys.get(fry_text)._bank_tax_diff is None
    elu_partyunit = partyunit_shop(handle=elu_text)
    elu_partyunit._bank_tax_paid = 0.003
    elu_partyunit._bank_tax_diff = 0.007
    x_agenda.set_partyunit(partyunit=elu_partyunit)
    assert x_agenda._partys.get(elu_text)._bank_tax_paid == 0.003
    assert x_agenda._partys.get(elu_text)._bank_tax_diff == 0.007

    partybankunit_sam = PartyBankUnit(bob_text, sam_text, 0.209, 0, 0.034, None, None)
    partybankunit_wil = PartyBankUnit(bob_text, wil_text, 0.501, 0, 0.024, None, None)
    partybankunit_fry = PartyBankUnit(bob_text, fry_text, 0.111, 0, 0.006, None, None)
    partybankunits = {
        partybankunit_sam.tax_healer: partybankunit_sam,
        partybankunit_wil.tax_healer: partybankunit_wil,
        partybankunit_fry.tax_healer: partybankunit_fry,
    }
    # WHEN
    set_bank_partybankunits_to_agenda_partyunits(
        x_agenda, partybankunits=partybankunits
    )

    # THEN
    assert x_agenda._partys.get(sam_text)._bank_tax_paid == 0.209
    assert x_agenda._partys.get(sam_text)._bank_tax_diff == 0.034
    assert x_agenda._partys.get(wil_text)._bank_tax_paid == 0.501
    assert x_agenda._partys.get(wil_text)._bank_tax_diff == 0.024
    assert x_agenda._partys.get(fry_text)._bank_tax_paid == 0.111
    assert x_agenda._partys.get(fry_text)._bank_tax_diff == 0.006
    assert x_agenda._partys.get(elu_text)._bank_tax_paid is None
    assert x_agenda._partys.get(elu_text)._bank_tax_diff is None


def test_get_partyunit_table_update_bank_tax_paid_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    bob_agenda = agendaunit_shop(_healer=bob_text)
    partyunit_tom = partyunit_shop(
        handle=tom_text,
        _agenda_credit=0.9,
        _agenda_debt=0.8,
        _agenda_intent_credit=0.7,
        _agenda_intent_debt=0.6,
        _agenda_intent_ratio_credit=0.5,
        _agenda_intent_ratio_debt=0.411,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tom = get_partyunit_table_insert_sqlstr(
        x_agenda=bob_agenda, partyunit_x=partyunit_tom
    )
    partyunit_sal = partyunit_shop(
        handle=sal_text,
        _agenda_credit=0.9,
        _agenda_debt=0.8,
        _agenda_intent_credit=0.7,
        _agenda_intent_debt=0.6,
        _agenda_intent_ratio_credit=0.5,
        _agenda_intent_ratio_debt=0.455,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_partyunit_table_insert_sqlstr(
        x_agenda=bob_agenda, partyunit_x=partyunit_sal
    )

    river_block_1 = RiverBlockUnit(bob_text, bob_text, tom_text, 0.0, 0.2, 0, None, 1)
    river_block_2 = RiverBlockUnit(bob_text, bob_text, sal_text, 0.2, 1.0, 0, None, 1)
    river_block_3 = RiverBlockUnit(bob_text, tom_text, bob_text, 0.0, 0.2, 1, 0, 2)
    river_block_4 = RiverBlockUnit(bob_text, sal_text, bob_text, 0.2, 1.0, 1, 0, 2)
    sb0 = river_block_insert(river_block_1)
    sb1 = river_block_insert(river_block_2)
    st0 = river_block_insert(river_block_3)
    ss0 = river_block_insert(river_block_4)

    with x_culture.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr_tom)
        bank_conn.execute(insert_sqlstr_sal)
        bank_conn.execute(sb0)
        bank_conn.execute(sb1)
        bank_conn.execute(st0)
        bank_conn.execute(ss0)

    # WHEN
    mstr_sqlstr = get_partyunit_table_update_bank_tax_paid_sqlstr(
        currency_agenda_healer=bob_text
    )
    with x_culture.get_bank_conn() as bank_conn:
        print(mstr_sqlstr)
        bank_conn.execute(mstr_sqlstr)

    # THEN
    with x_culture.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(
            bank_conn, currency_agenda_healer=bob_text
        )
        print(f"{partybankunits=}")

    assert len(partybankunits) == 2

    bob_tom_x = partybankunits.get(tom_text)
    assert bob_tom_x.currency_master == bob_text
    assert bob_tom_x.tax_healer == tom_text
    assert bob_tom_x.tax_total == 0.2
    assert bob_tom_x.debt == 0.411
    assert round(bob_tom_x.tax_diff, 15) == 0.211

    bob_sal_x = partybankunits.get(sal_text)
    assert bob_sal_x.currency_master == bob_text
    assert bob_sal_x.tax_healer == sal_text
    assert bob_sal_x.tax_total == 0.8
    assert bob_sal_x.debt == 0.455
    assert round(bob_sal_x.tax_diff, 15) == -0.345

    # for value in partybankunits.values():
    #     assert value.currency_master == bob_text
    #     assert value.tax_healer in [tom_text, sal_text]
    #     assert value.tax_total in [0.2, 0.8]
    #     assert value.debt in [0.411, 0.455]
    #     assert round(value.tax_diff, 15) in [0.211, -0.345]
