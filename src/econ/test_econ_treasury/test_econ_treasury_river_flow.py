from src.agenda.agenda import agendaunit_shop
from src.econ.econ import econunit_shop
from src.econ.examples.econ_env_kit import env_dir_setup_cleanup, get_texas_agendahub
from src._instrument.sqlite import get_single_result, get_row_count_sqlstr
from src.econ.treasury_sqlstr import (
    get_partytreasuryunit_dict,
    get_river_block_dict,
)


def get_agenda_partyunit_table_treasurying_attr_set_count_sqlstr():
    # def get_agenda_partyunit_table_treasurying_attr_set_count_sqlstr(cash_master:):
    #     return f"""
    # SELECT COUNT(*)
    # FROM agenda_partyunit
    # WHERE _treasury_due_paid IS NOT NULL
    #     AND owner_id = {cash_master}
    # """
    return """
SELECT COUNT(*) 
FROM agenda_partyunit
WHERE _treasury_due_paid IS NOT NULL
;
"""


def test_EconUnit_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(get_texas_agendahub())

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"

    sal_agentunit = agendaunit_shop(_owner_id=sal_text)
    sal_agentunit.add_partyunit(party_id=bob_text, creditor_weight=1)
    sal_agentunit.add_partyunit(party_id=tom_text, creditor_weight=3)
    x_econ.agendahub.save_file_job(sal_agentunit)

    bob_agentunit = agendaunit_shop(_owner_id=bob_text)
    bob_agentunit.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(bob_agentunit)

    tom_agentunit = agendaunit_shop(_owner_id=tom_text)
    tom_agentunit.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(tom_agentunit)

    x_econ.refresh_treasury_job_agendas_data()
    partyunit_count_sqlstr = get_row_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 4

    partytreasuryunit_count_sqlstr = (
        get_agenda_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 4
    with x_econ.get_treasury_conn() as treasury_conn:
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
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_econ.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    assert len(partytreasuryunits) == 2
    river_sal_due_bob = partytreasuryunits.get(bob_text)
    river_sal_due_tom = partytreasuryunits.get(tom_text)

    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")

    assert river_sal_due_bob.due_total == 0.25
    assert river_sal_due_tom.due_total == 0.75


def test_EconUnit_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agendas, 85% of river blocks to sal
    x_econ = econunit_shop(get_texas_agendahub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    x_econ.agendahub.save_file_job(ava_agenda)
    x_econ.refresh_treasury_job_agendas_data()

    partyunit_count_sqlstr = get_row_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 6

    partytreasuryunit_count_sqlstr = (
        get_agenda_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 6
    with x_econ.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_econ.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    assert len(partytreasuryunits) == 2
    assert partytreasuryunits.get(bob_text) != None
    assert partytreasuryunits.get(tom_text) != None
    assert partytreasuryunits.get(ava_text) is None

    river_sal_due_bob = partytreasuryunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = partytreasuryunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_EconUnit_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop
    x_econ = econunit_shop(get_texas_agendahub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()

    partyunit_count_sqlstr = get_row_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 8

    partytreasuryunit_count_sqlstr = (
        get_agenda_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 40
    # with x_econ.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_econ.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    assert len(partytreasuryunits) == 2
    assert partytreasuryunits.get(bob_text) != None
    assert partytreasuryunits.get(tom_text) != None
    assert partytreasuryunits.get(ava_text) is None

    river_sal_due_bob = partytreasuryunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = partytreasuryunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_EconUnit_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable05_v1(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_econ = econunit_shop(get_texas_agendahub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()

    partyunit_count_sqlstr = get_row_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 9

    partytreasuryunit_count_sqlstr = (
        get_agenda_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 40
    # with x_econ.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_econ.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    assert len(partytreasuryunits) == 2
    assert partytreasuryunits.get(bob_text) != None
    assert partytreasuryunits.get(tom_text) != None
    assert partytreasuryunits.get(elu_text) is None
    assert partytreasuryunits.get(ava_text) is None

    river_sal_due_bob = partytreasuryunits.get(bob_text)
    river_sal_due_tom = partytreasuryunits.get(tom_text)
    river_sal_due_elu = partytreasuryunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_EconUnit_set_credit_flow_for_agenda_CorrectlyUsesMaxblocksCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_econ = econunit_shop(get_texas_agendahub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()

    partyunit_count_sqlstr = get_row_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 9

    partytreasuryunit_count_sqlstr = (
        get_agenda_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    mbc = 13
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text, max_blocks_count=mbc)

    # THEN
    # with x_econ.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == mbc
    )


def test_EconUnit_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_econ = econunit_shop(get_texas_agendahub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()

    partyunit_count_sqlstr = get_row_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 9

    partytreasuryunit_count_sqlstr = (
        get_agenda_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text)

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), river_block_count_sqlstr) == 40
    with x_econ.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_econ.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_econ.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    partytreasuryunits = x_econ.get_partytreasuryunits(sal_text)
    assert len(partytreasuryunits) == 2
    assert partytreasuryunits.get(bob_text) != None
    assert partytreasuryunits.get(tom_text) != None
    assert partytreasuryunits.get(elu_text) is None
    assert partytreasuryunits.get(ava_text) is None

    river_sal_due_bob = partytreasuryunits.get(bob_text)
    river_sal_due_tom = partytreasuryunits.get(tom_text)
    river_sal_due_elu = partytreasuryunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_EconUnit_set_credit_flow_for_agenda_CorrectlyBuildsASingle_ContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_econ = econunit_shop(get_texas_agendahub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()

    # WHEN
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)

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
    with x_econ.get_treasury_conn() as treasury_conn:
        assert get_single_result(treasury_conn, count_range_fails_sql) == 0


def test_EconUnit_set_credit_flow_for_agenda_CorrectlyUpatesAgendaPartyUnits(
    env_dir_setup_cleanup,
):
    """GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal"""
    # GIVEN
    x_econ = econunit_shop(get_texas_agendahub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda_src = agendaunit_shop(_owner_id=sal_text)
    sal_agenda_src.add_partyunit(party_id=bob_text, creditor_weight=2, debtor_weight=2)
    sal_agenda_src.add_partyunit(party_id=tom_text, creditor_weight=2, debtor_weight=1)
    sal_agenda_src.add_partyunit(party_id=ava_text, creditor_weight=2, debtor_weight=2)
    x_econ.agendahub.save_file_job(sal_agenda_src)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_file_job(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text)
    x_econ.agendahub.save_file_job(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=8)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.agendahub.save_file_job(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()
    sal_agenda_before = x_econ.agendahub.get_job_agenda(owner_id=sal_text)

    x_econ.set_credit_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)
    assert len(sal_agenda_before._partys) == 3
    print(f"{len(sal_agenda_before._partys)=}")
    bob_party = sal_agenda_before._partys.get(bob_text)
    tom_party = sal_agenda_before._partys.get(tom_text)
    ava_party = sal_agenda_before._partys.get(ava_text)
    assert bob_party._treasury_due_paid is None
    assert tom_party._treasury_due_paid is None
    assert ava_party._treasury_due_paid is None
    assert bob_party._treasury_due_diff is None
    assert tom_party._treasury_due_diff is None
    assert ava_party._treasury_due_diff is None
    assert bob_party._treasury_voice_rank is None
    assert tom_party._treasury_voice_rank is None
    assert ava_party._treasury_voice_rank is None
    assert bob_party._treasury_voice_hx_lowest_rank is None
    assert tom_party._treasury_voice_hx_lowest_rank is None
    assert ava_party._treasury_voice_hx_lowest_rank is None

    # WHEN
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text)

    # THEN
    sal_partytreasuryunits = x_econ.get_partytreasuryunits(owner_id=sal_text)
    assert len(sal_partytreasuryunits) == 2
    bob_partytreasury = sal_partytreasuryunits.get(bob_text)
    tom_partytreasury = sal_partytreasuryunits.get(tom_text)
    assert bob_partytreasury.due_owner_id == bob_text
    assert tom_partytreasury.due_owner_id == tom_text
    assert bob_partytreasury.cash_master == sal_text
    assert tom_partytreasury.cash_master == sal_text

    sal_agenda_after = x_econ.agendahub.get_job_agenda(owner_id=sal_text)
    bob_party = sal_agenda_after._partys.get(bob_text)
    tom_party = sal_agenda_after._partys.get(tom_text)
    ava_party = sal_agenda_after._partys.get(ava_text)
    elu_party = sal_agenda_after._partys.get(elu_text)

    assert bob_partytreasury.due_total == bob_party._treasury_due_paid
    assert bob_partytreasury.due_diff == bob_party._treasury_due_diff
    assert tom_partytreasury.due_total == tom_party._treasury_due_paid
    assert tom_partytreasury.due_diff == tom_party._treasury_due_diff
    assert elu_party is None

    # for partytreasury_uid, sal_partytreasuryunit in sal_partytreasuryunits.items():
    #     print(f"{partytreasury_uid=} {sal_partytreasuryunit=}")
    #     assert sal_partytreasuryunit.cash_master == sal_text
    #     assert sal_partytreasuryunit.due_owner_id in [bob_text, tom_text, elu_text]
    #     x_partyunit = sal_agenda_after._partys.get(sal_partytreasuryunit.due_owner_id)
    #     if x_partyunit != None:
    #         # print(
    #         #     f"{sal_partytreasuryunit.cash_master=} {sal_partytreasuryunit.due_owner_id=} {x_partyunit.party_id=} due_total: {sal_partytreasuryunit.due_total} _Due_ Paid: {x_partyunit._treasury_due_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_partytreasuryunit.cash_master=} {sal_partytreasuryunit.due_owner_id=} {x_partyunit.party_id=} due_diff:  {sal_partytreasuryunit.due_diff} _Due_ Paid: {x_partyunit._treasury_due_diff}"
    #         # )
    #         assert sal_partytreasuryunit.due_total == x_partyunit._treasury_due_paid
    #         assert sal_partytreasuryunit.due_diff == x_partyunit._treasury_due_diff

    assert sal_partytreasuryunits.get(ava_text) is None
    assert ava_party._treasury_due_paid is None
    assert ava_party._treasury_due_diff is None

    # for x_partyunit in sal_agenda_after._partys.values():
    #     print(f"sal_agenda_after {x_partyunit.party_id=} {x_partyunit._treasury_due_paid=}")
    #     partytreasuryunit_x = sal_partytreasuryunits.get(x_partyunit.party_id)
    #     if partytreasuryunit_x is None:
    #         assert x_partyunit._treasury_due_paid is None
    #         assert x_partyunit._treasury_due_diff is None
    #     else:
    #         assert x_partyunit._treasury_due_paid != None
    #         assert x_partyunit._treasury_due_diff != None
    # assert sal_agenda_after != sal_agenda_before
