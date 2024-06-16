from src.agenda.agenda import agendaunit_shop
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import env_dir_setup_cleanup, get_texas_userhub
from src._instrument.sqlite import get_single_result, get_row_count_sqlstr
from src.money.treasury_sqlstr import (
    get_guytreasuryunit_dict,
    get_river_block_dict,
)


def get_agenda_guyunit_table_treasurying_attr_set_count_sqlstr():
    # def get_agenda_guyunit_table_treasurying_attr_set_count_sqlstr(cash_master:):
    #     return f"""
    # SELECT COUNT(*)
    # FROM agenda_guyunit
    # WHERE _treasury_due_paid IS NOT NULL
    #     AND owner_id = {cash_master}
    # """
    return """
SELECT COUNT(*) 
FROM agenda_guyunit
WHERE _treasury_due_paid IS NOT NULL
;
"""


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesguytreasuryunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"

    sal_agentunit = agendaunit_shop(_owner_id=sal_text)
    sal_agentunit.add_guyunit(guy_id=bob_text, credor_weight=1)
    sal_agentunit.add_guyunit(guy_id=tom_text, credor_weight=3)
    x_money.userhub.save_job_agenda(sal_agentunit)

    bob_agentunit = agendaunit_shop(_owner_id=bob_text)
    bob_agentunit.add_guyunit(guy_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agentunit)

    tom_agentunit = agendaunit_shop(_owner_id=tom_text)
    tom_agentunit.add_guyunit(guy_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(tom_agentunit)

    x_money.refresh_treasury_job_agendas_data()
    guyunit_count_sqlstr = get_row_count_sqlstr("agenda_guyunit")
    assert get_single_result(x_money.get_treasury_conn(), guyunit_count_sqlstr) == 4

    guytreasuryunit_count_sqlstr = (
        get_agenda_guyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 4
    with x_money.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)

    block_0 = river_blocks.get(0)
    block_1 = river_blocks.get(1)
    assert block_1.src_owner_id == sal_text and block_1.dst_owner_id == tom_text
    assert block_1.river_tree_level == 1
    assert block_1.cash_start == 0.25
    assert block_1.cash_close == 1
    assert block_1.parent_block_num is None
    block_2 = river_blocks.get(2)
    block_3 = river_blocks.get(3)
    assert block_3.src_owner_id == tom_text and block_3.dst_owner_id == sal_text
    assert block_3.river_tree_level == 2
    assert block_3.parent_block_num == 1

    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        guytreasuryunits = get_guytreasuryunit_dict(treasury_conn, sal_text)
    assert len(guytreasuryunits) == 2
    river_sal_due_bob = guytreasuryunits.get(bob_text)
    river_sal_due_tom = guytreasuryunits.get(tom_text)

    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")

    assert river_sal_due_bob.due_total == 0.25
    assert river_sal_due_tom.due_total == 0.75


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesguytreasuryunitTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agendas, 85% of river blocks to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_guyunit(guy_id=bob_text, credor_weight=2)
    sal_agenda.add_guyunit(guy_id=tom_text, credor_weight=7)
    sal_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_guyunit(guy_id=sal_text, credor_weight=3)
    bob_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_guyunit(guy_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    x_money.userhub.save_job_agenda(ava_agenda)
    x_money.refresh_treasury_job_agendas_data()

    guyunit_count_sqlstr = get_row_count_sqlstr("agenda_guyunit")
    assert get_single_result(x_money.get_treasury_conn(), guyunit_count_sqlstr) == 6

    guytreasuryunit_count_sqlstr = (
        get_agenda_guyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 6
    with x_money.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        guytreasuryunits = get_guytreasuryunit_dict(treasury_conn, sal_text)
    assert len(guytreasuryunits) == 2
    assert guytreasuryunits.get(bob_text) != None
    assert guytreasuryunits.get(tom_text) != None
    assert guytreasuryunits.get(ava_text) is None

    river_sal_due_bob = guytreasuryunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = guytreasuryunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesguytreasuryunitTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_guyunit(guy_id=bob_text, credor_weight=2)
    sal_agenda.add_guyunit(guy_id=tom_text, credor_weight=7)
    sal_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_guyunit(guy_id=sal_text, credor_weight=3)
    bob_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_guyunit(guy_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_guyunit(guy_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_guyunit(guy_id=ava_text, credor_weight=2)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    guyunit_count_sqlstr = get_row_count_sqlstr("agenda_guyunit")
    assert get_single_result(x_money.get_treasury_conn(), guyunit_count_sqlstr) == 8

    guytreasuryunit_count_sqlstr = (
        get_agenda_guyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    # with x_money.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        guytreasuryunits = get_guytreasuryunit_dict(treasury_conn, sal_text)
    assert len(guytreasuryunits) == 2
    assert guytreasuryunits.get(bob_text) != None
    assert guytreasuryunits.get(tom_text) != None
    assert guytreasuryunits.get(ava_text) is None

    river_sal_due_bob = guytreasuryunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = guytreasuryunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesguytreasuryunitTable05_v1(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_guyunit(guy_id=bob_text, credor_weight=2)
    sal_agenda.add_guyunit(guy_id=tom_text, credor_weight=7)
    sal_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_guyunit(guy_id=sal_text, credor_weight=3)
    bob_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_guyunit(guy_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_guyunit(guy_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_guyunit(guy_id=ava_text, credor_weight=19)
    elu_agenda.add_guyunit(guy_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    guyunit_count_sqlstr = get_row_count_sqlstr("agenda_guyunit")
    assert get_single_result(x_money.get_treasury_conn(), guyunit_count_sqlstr) == 9

    guytreasuryunit_count_sqlstr = (
        get_agenda_guyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    # with x_money.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        guytreasuryunits = get_guytreasuryunit_dict(treasury_conn, sal_text)
    assert len(guytreasuryunits) == 2
    assert guytreasuryunits.get(bob_text) != None
    assert guytreasuryunits.get(tom_text) != None
    assert guytreasuryunits.get(elu_text) is None
    assert guytreasuryunits.get(ava_text) is None

    river_sal_due_bob = guytreasuryunits.get(bob_text)
    river_sal_due_tom = guytreasuryunits.get(tom_text)
    river_sal_due_elu = guytreasuryunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyUsesMaxblocksCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_guyunit(guy_id=bob_text, credor_weight=2)
    sal_agenda.add_guyunit(guy_id=tom_text, credor_weight=7)
    sal_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_guyunit(guy_id=sal_text, credor_weight=3)
    bob_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_guyunit(guy_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_guyunit(guy_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_guyunit(guy_id=ava_text, credor_weight=19)
    elu_agenda.add_guyunit(guy_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    guyunit_count_sqlstr = get_row_count_sqlstr("agenda_guyunit")
    assert get_single_result(x_money.get_treasury_conn(), guyunit_count_sqlstr) == 9

    guytreasuryunit_count_sqlstr = (
        get_agenda_guyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    mbc = 13
    x_money.set_cred_flow_for_agenda(owner_id=sal_text, max_blocks_count=mbc)

    # THEN
    # with x_money.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == mbc
    )


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyPopulatesguytreasuryunitTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_guyunit(guy_id=bob_text, credor_weight=2)
    sal_agenda.add_guyunit(guy_id=tom_text, credor_weight=7)
    sal_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_guyunit(guy_id=sal_text, credor_weight=3)
    bob_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_guyunit(guy_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_guyunit(guy_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_guyunit(guy_id=ava_text, credor_weight=19)
    elu_agenda.add_guyunit(guy_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    guyunit_count_sqlstr = get_row_count_sqlstr("agenda_guyunit")
    assert get_single_result(x_money.get_treasury_conn(), guyunit_count_sqlstr) == 9

    guytreasuryunit_count_sqlstr = (
        get_agenda_guyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    with x_money.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), guytreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        guytreasuryunits = get_guytreasuryunit_dict(treasury_conn, sal_text)
    guytreasuryunits = x_money.get_guytreasuryunits(sal_text)
    assert len(guytreasuryunits) == 2
    assert guytreasuryunits.get(bob_text) != None
    assert guytreasuryunits.get(tom_text) != None
    assert guytreasuryunits.get(elu_text) is None
    assert guytreasuryunits.get(ava_text) is None

    river_sal_due_bob = guytreasuryunits.get(bob_text)
    river_sal_due_tom = guytreasuryunits.get(tom_text)
    river_sal_due_elu = guytreasuryunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyBuildsASingle_ContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_guyunit(guy_id=bob_text, credor_weight=2)
    sal_agenda.add_guyunit(guy_id=tom_text, credor_weight=7)
    sal_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_guyunit(guy_id=sal_text, credor_weight=3)
    bob_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_guyunit(guy_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_guyunit(guy_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_guyunit(guy_id=ava_text, credor_weight=19)
    elu_agenda.add_guyunit(guy_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)

    # THEN
    count_range_fails_sql = """
    SELECT COUNT(*)
    FROM (
        SELECT 
            rt1.cash_start x_row_start
        , lag(cash_close) OVER (ORDER BY cash_start, cash_close) AS prev_close
        , lag(cash_close) OVER (ORDER BY cash_start, cash_close) - rt1.cash_start prev_diff
        , rt1.block_num or_block_num
        , lag(block_num) OVER (ORDER BY cash_start, cash_close) AS prev_block_num
        , rt1.parent_block_num or_parent_block_num
        , lag(parent_block_num) OVER (ORDER BY cash_start, cash_close) AS prev_parent_block_num
        , river_tree_level
        , lag(river_tree_level) OVER (ORDER BY cash_start, cash_close) AS prev_parent_river_tree_level
        FROM river_block rt1
        --  WHERE dst_owner_id = 'sal' and cash_master = dst_owner_id
        ORDER BY rt1.cash_start, rt1.cash_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_single_result(treasury_conn, count_range_fails_sql) == 0


def test_MoneyUnit_set_cred_flow_for_agenda_CorrectlyUpatesAgendaGuyUnits(
    env_dir_setup_cleanup,
):
    """GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal"""
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda_src = agendaunit_shop(_owner_id=sal_text)
    sal_agenda_src.add_guyunit(guy_id=bob_text, credor_weight=2, debtor_weight=2)
    sal_agenda_src.add_guyunit(guy_id=tom_text, credor_weight=2, debtor_weight=1)
    sal_agenda_src.add_guyunit(guy_id=ava_text, credor_weight=2, debtor_weight=2)
    x_money.userhub.save_job_agenda(sal_agenda_src)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_guyunit(guy_id=sal_text, credor_weight=3)
    bob_agenda.add_guyunit(guy_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_guyunit(guy_id=sal_text)
    x_money.userhub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_guyunit(guy_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_guyunit(guy_id=ava_text, credor_weight=8)
    elu_agenda.add_guyunit(guy_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_agenda(elu_agenda)

    x_money.refresh_treasury_job_agendas_data()
    sal_agenda_before = x_money.userhub.get_job_agenda(owner_id=sal_text)

    x_money.set_cred_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)
    assert len(sal_agenda_before._guys) == 3
    print(f"{len(sal_agenda_before._guys)=}")
    bob_guy = sal_agenda_before._guys.get(bob_text)
    tom_guy = sal_agenda_before._guys.get(tom_text)
    ava_guy = sal_agenda_before._guys.get(ava_text)
    assert bob_guy._treasury_due_paid is None
    assert tom_guy._treasury_due_paid is None
    assert ava_guy._treasury_due_paid is None
    assert bob_guy._treasury_due_diff is None
    assert tom_guy._treasury_due_diff is None
    assert ava_guy._treasury_due_diff is None
    assert bob_guy._treasury_voice_rank is None
    assert tom_guy._treasury_voice_rank is None
    assert ava_guy._treasury_voice_rank is None
    assert bob_guy._treasury_voice_hx_lowest_rank is None
    assert tom_guy._treasury_voice_hx_lowest_rank is None
    assert ava_guy._treasury_voice_hx_lowest_rank is None

    # WHEN
    x_money.set_cred_flow_for_agenda(owner_id=sal_text)

    # THEN
    sal_guytreasuryunits = x_money.get_guytreasuryunits(owner_id=sal_text)
    assert len(sal_guytreasuryunits) == 2
    bob_guytreasury = sal_guytreasuryunits.get(bob_text)
    tom_guytreasury = sal_guytreasuryunits.get(tom_text)
    assert bob_guytreasury.due_owner_id == bob_text
    assert tom_guytreasury.due_owner_id == tom_text
    assert bob_guytreasury.cash_master == sal_text
    assert tom_guytreasury.cash_master == sal_text

    sal_agenda_after = x_money.userhub.get_job_agenda(owner_id=sal_text)
    bob_guy = sal_agenda_after._guys.get(bob_text)
    tom_guy = sal_agenda_after._guys.get(tom_text)
    ava_guy = sal_agenda_after._guys.get(ava_text)
    elu_guy = sal_agenda_after._guys.get(elu_text)

    assert bob_guytreasury.due_total == bob_guy._treasury_due_paid
    assert bob_guytreasury.due_diff == bob_guy._treasury_due_diff
    assert tom_guytreasury.due_total == tom_guy._treasury_due_paid
    assert tom_guytreasury.due_diff == tom_guy._treasury_due_diff
    assert elu_guy is None

    # for guytreasury_uid, sal_guytreasuryunit in sal_guytreasuryunits.items():
    #     print(f"{guytreasury_uid=} {sal_guytreasuryunit=}")
    #     assert sal_guytreasuryunit.cash_master == sal_text
    #     assert sal_guytreasuryunit.due_owner_id in [bob_text, tom_text, elu_text]
    #     x_guyunit = sal_agenda_after._guys.get(sal_guytreasuryunit.due_owner_id)
    #     if x_guyunit != None:
    #         # print(
    #         #     f"{sal_guytreasuryunit.cash_master=} {sal_guytreasuryunit.due_owner_id=} {x_guyunit.guy_id=} due_total: {sal_guytreasuryunit.due_total} _Due_ Paid: {x_guyunit._treasury_due_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_guytreasuryunit.cash_master=} {sal_guytreasuryunit.due_owner_id=} {x_guyunit.guy_id=} due_diff:  {sal_guytreasuryunit.due_diff} _Due_ Paid: {x_guyunit._treasury_due_diff}"
    #         # )
    #         assert sal_guytreasuryunit.due_total == x_guyunit._treasury_due_paid
    #         assert sal_guytreasuryunit.due_diff == x_guyunit._treasury_due_diff

    assert sal_guytreasuryunits.get(ava_text) is None
    assert ava_guy._treasury_due_paid is None
    assert ava_guy._treasury_due_diff is None

    # for x_guyunit in sal_agenda_after._guys.values():
    #     print(f"sal_agenda_after {x_guyunit.guy_id=} {x_guyunit._treasury_due_paid=}")
    #     guytreasuryunit_x = sal_guytreasuryunits.get(x_guyunit.guy_id)
    #     if guytreasuryunit_x is None:
    #         assert x_guyunit._treasury_due_paid is None
    #         assert x_guyunit._treasury_due_diff is None
    #     else:
    #         assert x_guyunit._treasury_due_paid != None
    #         assert x_guyunit._treasury_due_diff != None
    # assert sal_agenda_after != sal_agenda_before
