from src.agenda.agenda import agendaunit_shop, otherunit_shop
from src.money.money import (
    moneyunit_shop,
    set_treasury_othertreasuryunits_to_agenda_otherunits,
)
from src.money.examples.econ_env import env_dir_setup_cleanup, get_texas_userhub
from src.money.treasury_sqlstr import (
    get_river_block_table_insert_sqlstr as river_block_insert,
    get_river_block_dict,
    get_agenda_otherunit_table_update_treasury_due_paid_sqlstr,
    OtherTreasuryUnit,
    get_othertreasuryunit_dict,
    get_agenda_otherunit_table_insert_sqlstr,
    get_otherview_dict,
    OtherDBUnit,
    RiverLedgerUnit,
    RiverBlockUnit,
    get_river_ledger_unit,
)


def test_MoneyUnit_get_agenda_otherunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 ledger rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    tim_text = "Tim"
    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    tim_otherunit = otherunit_shop(
        other_id=tim_text,
        _credor_operational=True,
        _debtor_operational=False,
    )
    tim_otherunit._agenda_cred = 0.9
    tim_otherunit._agenda_debt = 0.8
    tim_otherunit._agenda_intent_cred = 0.7
    tim_otherunit._agenda_intent_debt = 0.6
    tim_otherunit._agenda_intent_ratio_cred = 0.5
    tim_otherunit._agenda_intent_ratio_debt = 0.4

    tim_due_paid = 0.5151
    tim_cred_score = 0.5252
    tim_voice_rank = 33
    tim_otherunit.set_treasury_attr(tim_due_paid, None, tim_cred_score, tim_voice_rank)
    assert tim_otherunit._treasury_due_paid == tim_due_paid
    assert tim_otherunit._treasury_cred_score == tim_cred_score
    assert tim_otherunit._treasury_voice_rank == tim_voice_rank

    insert_sqlstr = get_agenda_otherunit_table_insert_sqlstr(bob_agenda, tim_otherunit)
    print(insert_sqlstr)

    # WHEN
    with x_money.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(insert_sqlstr)

    ledger_dict = get_otherview_dict(
        db_conn=x_money.get_treasury_conn(), payer_owner_id=bob_text
    )
    # tim_ledger = None
    # for key, value in ledger_dict.items():
    #     print(f"{key=} {value=}")
    #     tim_ledger = value

    # THEN
    tim_ledger = ledger_dict.get(tim_text)
    assert tim_ledger.owner_id == bob_text
    assert tim_ledger.other_id == tim_text
    assert tim_ledger._agenda_cred == 0.9
    assert tim_ledger._agenda_debt == 0.8
    assert tim_ledger._agenda_intent_cred == 0.7
    assert tim_ledger._agenda_intent_debt == 0.6
    assert tim_ledger._agenda_intent_ratio_cred == 0.5
    assert tim_ledger._agenda_intent_ratio_debt == 0.4
    assert tim_ledger._credor_operational
    assert tim_ledger._debtor_operational == 0
    assert tim_ledger._treasury_due_paid == tim_due_paid
    assert tim_ledger._treasury_cred_score == tim_cred_score
    assert tim_ledger._treasury_voice_rank == tim_voice_rank


def test_RiverBlockUnit_exists():
    # GIVEN
    bob_text = "Bob"
    tom_text = "Tom"
    cash_onset = 400
    cash_cease = 600
    river_tree_level = 6
    block_num = 89
    parent_block_num = None

    # WHEN
    river_block_x = RiverBlockUnit(
        cash_owner_id=bob_text,
        src_owner_id=None,
        dst_owner_id=tom_text,
        cash_start=cash_onset,
        cash_close=cash_cease,
        block_num=block_num,
        parent_block_num=parent_block_num,
        river_tree_level=river_tree_level,
    )

    # THEN
    assert river_block_x.cash_owner_id == bob_text
    assert river_block_x.src_owner_id is None
    assert river_block_x.dst_owner_id == tom_text
    assert river_block_x.cash_start == cash_onset
    assert river_block_x.cash_close == cash_cease
    assert river_block_x.block_num == block_num
    assert river_block_x.parent_block_num == parent_block_num
    assert river_block_x.river_tree_level == river_tree_level


def test_RiverBlockUnit_block_returned_ReturnsCorrectBool():
    # GIVEN
    bob_text = "Bob"
    sal_text = "Sal"
    tom_text = "Tom"
    cash_onset = 400
    cash_cease = 600
    river_tree_level = 6
    block_num = 89
    parent_block_num = None

    # WHEN
    river_block_x = RiverBlockUnit(
        cash_owner_id=bob_text,
        src_owner_id=sal_text,
        dst_owner_id=tom_text,
        cash_start=cash_onset,
        cash_close=cash_cease,
        block_num=block_num,
        parent_block_num=parent_block_num,
        river_tree_level=river_tree_level,
    )
    assert river_block_x.cash_owner_id != river_block_x.dst_owner_id

    # THEN
    assert river_block_x.block_returned() is False

    # WHEN
    river_block_x.dst_owner_id = bob_text

    # THEN
    assert river_block_x.block_returned()


def test_MoneyUnit_get_river_ledger_unit_ReturnsRiverLedgerUnit(env_dir_setup_cleanup):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 ledger rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    sal_text = "Sal"
    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    sal_otherunit = otherunit_shop(
        sal_text, _credor_operational=True, _debtor_operational=False
    )
    sal_otherunit._agenda_cred = 0.9
    sal_otherunit._agenda_debt = 0.8
    sal_otherunit._agenda_intent_cred = 0.7
    sal_otherunit._agenda_intent_debt = 0.6
    sal_otherunit._agenda_intent_ratio_cred = 0.5
    sal_otherunit._agenda_intent_ratio_debt = 0.4

    insert_sqlstr_sal = get_agenda_otherunit_table_insert_sqlstr(
        bob_agenda, sal_otherunit
    )

    tim_text = "Tim"
    tim_otherunit = otherunit_shop(
        tim_text, _credor_operational=True, _debtor_operational=False
    )
    tim_otherunit._agenda_cred = 0.012
    tim_otherunit._agenda_debt = 0.017
    tim_otherunit._agenda_intent_cred = 0.077
    tim_otherunit._agenda_intent_debt = 0.066
    tim_otherunit._agenda_intent_ratio_cred = 0.051
    tim_otherunit._agenda_intent_ratio_debt = 0.049

    insert_sqlstr_tim = get_agenda_otherunit_table_insert_sqlstr(
        bob_agenda, tim_otherunit
    )

    with x_money.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(insert_sqlstr_sal)
        treasury_conn.execute(insert_sqlstr_tim)
        otherview_dict_x = get_otherview_dict(
            db_conn=treasury_conn, payer_owner_id=bob_text
        )

    # WHEN
    river_block_x = RiverBlockUnit(
        cash_owner_id=bob_text,
        src_owner_id=None,
        dst_owner_id=bob_text,
        cash_start=0.225,
        cash_close=0.387,
        block_num=51,
        parent_block_num=6,
        river_tree_level=4,
    )
    with x_money.get_treasury_conn() as treasury_conn:
        river_ledger_x = get_river_ledger_unit(treasury_conn, river_block_x)

    # THEN
    assert river_ledger_x.owner_id == bob_text
    assert river_ledger_x.cash_onset == 0.225
    assert river_ledger_x.cash_cease == 0.387
    assert river_ledger_x.river_tree_level == 4
    assert river_ledger_x._otherviews == otherview_dict_x
    assert river_ledger_x.block_num == 51


def test_river_block_insert_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 ledger rows
    x_money = moneyunit_shop(get_texas_userhub())

    bob_text = "Bob"
    tim_text = "Tim"
    sal_text = "Sal"

    river_block_unit = RiverBlockUnit(
        cash_owner_id=bob_text,
        src_owner_id=tim_text,
        dst_owner_id=sal_text,
        cash_start=0.2,
        cash_close=0.5,
        block_num=5,
        river_tree_level=6,
        parent_block_num=8,
    )
    insert_sqlstr = river_block_insert(river_block_unit)
    print(insert_sqlstr)

    # WHEN
    with x_money.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(insert_sqlstr)
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=bob_text)
        print(f"{river_blocks=}")

    # THEN
    print(f"{river_blocks.keys()=}")
    # for value in river_blocks.values():
    block_0 = river_blocks.get(0)
    assert block_0.cash_owner_id == bob_text
    assert block_0.src_owner_id == tim_text
    assert block_0.dst_owner_id == sal_text
    assert block_0.cash_start == 0.2
    assert block_0.cash_close == 0.5
    assert block_0.block_num == 5
    assert block_0.river_tree_level == 6
    assert block_0.parent_block_num == 8


def test_RiverLedgerUnit_Exists():
    # GIVEN
    bob_text = "Bob"
    sal_text = "Sal"
    tom_text = "Tom"
    x1_otherdbunit = OtherDBUnit(
        owner_id=bob_text,
        other_id=sal_text,
        _agenda_cred=0.66,
        _agenda_debt=0.2,
        _agenda_intent_cred=0.4,
        _agenda_intent_debt=0.15,
        _agenda_intent_ratio_cred=0.5,
        _agenda_intent_ratio_debt=0.12,
        _credor_operational=True,
        _debtor_operational=True,
    )
    x2_otherdbunit = OtherDBUnit(
        owner_id=bob_text,
        other_id=tom_text,
        _agenda_cred=0.05,
        _agenda_debt=0.09,
        _agenda_intent_cred=0.055,
        _agenda_intent_debt=0.0715,
        _agenda_intent_ratio_cred=0.00995,
        _agenda_intent_ratio_debt=0.00012,
        _credor_operational=True,
        _debtor_operational=True,
    )
    x_otherview_dict = {
        x1_otherdbunit.other_id: x1_otherdbunit,
        x2_otherdbunit.other_id: x2_otherdbunit,
    }
    # WHEN
    river_ledger_unit = RiverLedgerUnit(
        owner_id=bob_text,
        cash_onset=0.6,
        cash_cease=0.8,
        _otherviews=x_otherview_dict,
        river_tree_level=7,
        block_num=89,
    )

    # THEN
    assert river_ledger_unit.owner_id == bob_text
    assert river_ledger_unit.cash_onset == 0.6
    assert river_ledger_unit.cash_cease == 0.8
    assert river_ledger_unit.river_tree_level == 7
    assert river_ledger_unit.block_num == 89
    assert river_ledger_unit._otherviews == x_otherview_dict
    assert abs(river_ledger_unit.get_range() - 0.2) < 0.00000001


def test_OtherTreasuryUnit_exists():
    # GIVEN
    x_cash_master = "x_cash_master"
    x_due_owner_id = "x_due_owner_id"
    x_due_total = "x_due_total"
    x_debt = "x_debt"
    x_due_diff = "x_due_diff"
    x_cred_score = "cred_score"
    x_voice_rank = "voice_rank"

    # WHEN
    x_othertreasury = OtherTreasuryUnit(
        cash_master=x_cash_master,
        due_owner_id=x_due_owner_id,
        due_total=x_due_total,
        debt=x_debt,
        due_diff=x_due_diff,
        cred_score=x_cred_score,
        voice_rank=x_voice_rank,
    )

    # THEN
    assert x_othertreasury.cash_master == x_cash_master
    assert x_othertreasury.due_owner_id == x_due_owner_id
    assert x_othertreasury.due_total == x_due_total
    assert x_othertreasury.debt == x_debt
    assert x_othertreasury.due_diff == x_due_diff
    assert x_othertreasury.cred_score == x_cred_score
    assert x_othertreasury.voice_rank == x_voice_rank


def test_agenda_set_treasury_attr_otherunits_CorrectlySetsOtherUnitTreasuryingAttr():
    # GIVEN
    bob_text = "Bob"
    x_agenda = agendaunit_shop(_owner_id=bob_text)
    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "Elu"
    x_agenda.set_otherunit(otherunit=otherunit_shop(other_id=sam_text))
    x_agenda.set_otherunit(otherunit=otherunit_shop(other_id=wil_text))
    x_agenda.set_otherunit(otherunit=otherunit_shop(other_id=fry_text))
    assert x_agenda._others.get(sam_text)._treasury_due_paid is None
    assert x_agenda._others.get(sam_text)._treasury_due_diff is None
    assert x_agenda._others.get(wil_text)._treasury_due_paid is None
    assert x_agenda._others.get(wil_text)._treasury_due_diff is None
    assert x_agenda._others.get(fry_text)._treasury_due_paid is None
    assert x_agenda._others.get(fry_text)._treasury_due_diff is None
    elu_otherunit = otherunit_shop(other_id=elu_text)
    elu_otherunit._treasury_due_paid = 0.003
    elu_otherunit._treasury_due_diff = 0.007
    x_agenda.set_otherunit(otherunit=elu_otherunit)
    assert x_agenda._others.get(elu_text)._treasury_due_paid == 0.003
    assert x_agenda._others.get(elu_text)._treasury_due_diff == 0.007

    othertreasuryunit_sam = OtherTreasuryUnit(
        bob_text, sam_text, 0.209, 0, 0.034, None, None
    )
    othertreasuryunit_wil = OtherTreasuryUnit(
        bob_text, wil_text, 0.501, 0, 0.024, None, None
    )
    othertreasuryunit_fry = OtherTreasuryUnit(
        bob_text, fry_text, 0.111, 0, 0.006, None, None
    )
    othertreasuryunits = {
        othertreasuryunit_sam.due_owner_id: othertreasuryunit_sam,
        othertreasuryunit_wil.due_owner_id: othertreasuryunit_wil,
        othertreasuryunit_fry.due_owner_id: othertreasuryunit_fry,
    }
    # WHEN
    set_treasury_othertreasuryunits_to_agenda_otherunits(
        x_agenda, othertreasuryunits=othertreasuryunits
    )

    # THEN
    assert x_agenda._others.get(sam_text)._treasury_due_paid == 0.209
    assert x_agenda._others.get(sam_text)._treasury_due_diff == 0.034
    assert x_agenda._others.get(wil_text)._treasury_due_paid == 0.501
    assert x_agenda._others.get(wil_text)._treasury_due_diff == 0.024
    assert x_agenda._others.get(fry_text)._treasury_due_paid == 0.111
    assert x_agenda._others.get(fry_text)._treasury_due_diff == 0.006
    assert x_agenda._others.get(elu_text)._treasury_due_paid is None
    assert x_agenda._others.get(elu_text)._treasury_due_diff is None


def test_MoneyUnit_get_agenda_otherunit_table_update_treasury_due_paid_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 ledger rows
    x_money = moneyunit_shop(get_texas_userhub())

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    tom_otherunit = otherunit_shop(
        tom_text, _credor_operational=True, _debtor_operational=False
    )
    tom_otherunit._agenda_cred = 0.9
    tom_otherunit._agenda_debt = 0.8
    tom_otherunit._agenda_intent_cred = 0.7
    tom_otherunit._agenda_intent_debt = 0.6
    tom_otherunit._agenda_intent_ratio_cred = 0.5
    tom_otherunit._agenda_intent_ratio_debt = 0.411

    insert_sqlstr_tom = get_agenda_otherunit_table_insert_sqlstr(
        bob_agenda, tom_otherunit
    )
    sal_otherunit = otherunit_shop(
        sal_text, _credor_operational=True, _debtor_operational=False
    )
    sal_otherunit._agenda_cred = 0.9
    sal_otherunit._agenda_debt = 0.8
    sal_otherunit._agenda_intent_cred = 0.7
    sal_otherunit._agenda_intent_debt = 0.6
    sal_otherunit._agenda_intent_ratio_cred = 0.5
    sal_otherunit._agenda_intent_ratio_debt = 0.455

    insert_sqlstr_sal = get_agenda_otherunit_table_insert_sqlstr(
        bob_agenda, sal_otherunit
    )

    river_block_1 = RiverBlockUnit(bob_text, bob_text, tom_text, 0.0, 0.2, 0, None, 1)
    river_block_2 = RiverBlockUnit(bob_text, bob_text, sal_text, 0.2, 1.0, 0, None, 1)
    river_block_3 = RiverBlockUnit(bob_text, tom_text, bob_text, 0.0, 0.2, 1, 0, 2)
    river_block_4 = RiverBlockUnit(bob_text, sal_text, bob_text, 0.2, 1.0, 1, 0, 2)
    sb0 = river_block_insert(river_block_1)
    sb1 = river_block_insert(river_block_2)
    st0 = river_block_insert(river_block_3)
    ss0 = river_block_insert(river_block_4)

    with x_money.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(insert_sqlstr_tom)
        treasury_conn.execute(insert_sqlstr_sal)
        treasury_conn.execute(sb0)
        treasury_conn.execute(sb1)
        treasury_conn.execute(st0)
        treasury_conn.execute(ss0)

    # WHEN
    mstr_sqlstr = get_agenda_otherunit_table_update_treasury_due_paid_sqlstr(
        cash_owner_id=bob_text
    )
    with x_money.get_treasury_conn() as treasury_conn:
        print(mstr_sqlstr)
        treasury_conn.execute(mstr_sqlstr)

    # THEN
    with x_money.get_treasury_conn() as treasury_conn:
        othertreasuryunits = get_othertreasuryunit_dict(
            treasury_conn, cash_owner_id=bob_text
        )
        print(f"{othertreasuryunits=}")

    assert len(othertreasuryunits) == 2

    bob_tom_x = othertreasuryunits.get(tom_text)
    assert bob_tom_x.cash_master == bob_text
    assert bob_tom_x.due_owner_id == tom_text
    assert bob_tom_x.due_total == 0.2
    assert bob_tom_x.debt == 0.411
    assert round(bob_tom_x.due_diff, 15) == 0.211

    bob_sal_x = othertreasuryunits.get(sal_text)
    assert bob_sal_x.cash_master == bob_text
    assert bob_sal_x.due_owner_id == sal_text
    assert bob_sal_x.due_total == 0.8
    assert bob_sal_x.debt == 0.455
    assert round(bob_sal_x.due_diff, 15) == -0.345

    # for value in othertreasuryunits.values():
    #     assert value.cash_master == bob_text
    #     assert value.due_owner_id in [tom_text, sal_text]
    #     assert value.due_total in [0.2, 0.8]
    #     assert value.debt in [0.411, 0.455]
    #     assert round(value.due_diff, 15) in [0.211, -0.345]
