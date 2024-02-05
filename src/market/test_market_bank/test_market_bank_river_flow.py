from src.agenda.agenda import agendaunit_shop
from src.market.market import marketunit_shop
from src.market.examples.market_env_kit import (
    get_temp_env_market_id,
    get_test_markets_dir,
    env_dir_setup_cleanup,
)
from src.instrument.sqlite import get_single_result
from src.market.bank_sqlstr import (
    get_partybankunit_dict,
    get_river_block_dict,
    get_table_count_sqlstr,
)


def get_agenda_partyunit_table_banking_attr_set_count_sqlstr():
    # def get_agenda_partyunit_table_banking_attr_set_count_sqlstr(cash_master:):
    #     return f"""
    # SELECT COUNT(*)
    # FROM agenda_partyunit
    # WHERE _bank_due_paid IS NOT NULL
    #     AND agent_id = {cash_master}
    # """
    return """
SELECT COUNT(*) 
FROM agenda_partyunit
WHERE _bank_due_paid IS NOT NULL
;
"""


def test_market_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    sal_agentunit = agendaunit_shop(_agent_id=sal_text)
    sal_agentunit.add_partyunit(party_id=bob_text, creditor_weight=1)
    sal_agentunit.add_partyunit(party_id=tom_text, creditor_weight=3)
    x_market.save_forum_agenda(sal_agentunit)

    bob_agentunit = agendaunit_shop(_agent_id=bob_text)
    bob_agentunit.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_market.save_forum_agenda(bob_agentunit)

    tom_agentunit = agendaunit_shop(_agent_id=tom_text)
    tom_agentunit.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_market.save_forum_agenda(tom_agentunit)

    x_market.refresh_bank_forum_agendas_data()
    partyunit_count_sqlstr = get_table_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_market.get_bank_conn(), partyunit_count_sqlstr) == 4

    partybankunit_count_sqlstr = (
        get_agenda_partyunit_table_banking_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_market.set_credit_flow_for_agenda(agent_id=sal_text)

    # THEN
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 4
    with x_market.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, cash_agent_id=sal_text)

    block_0 = river_blocks.get(0)
    block_1 = river_blocks.get(1)
    assert block_1.src_agent_id == sal_text and block_1.dst_agent_id == tom_text
    assert block_1.river_tree_level == 1
    assert block_1.cash_start == 0.25
    assert block_1.cash_close == 1
    assert block_1.parent_block_num is None
    block_2 = river_blocks.get(2)
    block_3 = river_blocks.get(3)
    assert block_3.src_agent_id == tom_text and block_3.dst_agent_id == sal_text
    assert block_3.river_tree_level == 2
    assert block_3.parent_block_num == 1

    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_market.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    assert len(partybankunits) == 2
    river_sal_due_bob = partybankunits.get(bob_text)
    river_sal_due_tom = partybankunits.get(tom_text)

    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")

    assert river_sal_due_bob.due_total == 0.25
    assert river_sal_due_tom.due_total == 0.75


def test_market_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agendas, 85% of river blocks to sal
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_agenda = agendaunit_shop(_agent_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_agent_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_agent_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_market.save_forum_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_agent_id=ava_text)
    x_market.save_forum_agenda(ava_agenda)
    x_market.refresh_bank_forum_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_market.get_bank_conn(), partyunit_count_sqlstr) == 6

    partybankunit_count_sqlstr = (
        get_agenda_partyunit_table_banking_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_market.set_credit_flow_for_agenda(agent_id=sal_text)

    # THEN
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 6
    with x_market.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, cash_agent_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_market.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    assert len(partybankunits) == 2
    assert partybankunits.get(bob_text) != None
    assert partybankunits.get(tom_text) != None
    assert partybankunits.get(ava_text) is None

    river_sal_due_bob = partybankunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = partybankunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_market_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_agent_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_agent_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_agent_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_market.save_forum_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_agent_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_market.save_forum_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_agent_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=2)
    x_market.save_forum_agenda(elu_agenda)

    x_market.refresh_bank_forum_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_market.get_bank_conn(), partyunit_count_sqlstr) == 8

    partybankunit_count_sqlstr = (
        get_agenda_partyunit_table_banking_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_market.set_credit_flow_for_agenda(agent_id=sal_text)

    # THEN
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 40
    # with x_market.get_bank_conn() as bank_conn:
    #     river_blocks = get_river_block_dict(bank_conn, cash_agent_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_market.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    assert len(partybankunits) == 2
    assert partybankunits.get(bob_text) != None
    assert partybankunits.get(tom_text) != None
    assert partybankunits.get(ava_text) is None

    river_sal_due_bob = partybankunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = partybankunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_market_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable05_v1(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_agent_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_agent_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_agent_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_market.save_forum_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_agent_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_market.save_forum_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_agent_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_market.save_forum_agenda(elu_agenda)

    x_market.refresh_bank_forum_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_market.get_bank_conn(), partyunit_count_sqlstr) == 9

    partybankunit_count_sqlstr = (
        get_agenda_partyunit_table_banking_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_market.set_credit_flow_for_agenda(agent_id=sal_text)

    # THEN
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 40
    # with x_market.get_bank_conn() as bank_conn:
    #     river_blocks = get_river_block_dict(bank_conn, cash_agent_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_market.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    assert len(partybankunits) == 2
    assert partybankunits.get(bob_text) != None
    assert partybankunits.get(tom_text) != None
    assert partybankunits.get(elu_text) is None
    assert partybankunits.get(ava_text) is None

    river_sal_due_bob = partybankunits.get(bob_text)
    river_sal_due_tom = partybankunits.get(tom_text)
    river_sal_due_elu = partybankunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_market_set_credit_flow_for_agenda_CorrectlyUsesMaxblocksCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_agent_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_agent_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_agent_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_market.save_forum_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_agent_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_market.save_forum_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_agent_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_market.save_forum_agenda(elu_agenda)

    x_market.refresh_bank_forum_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_market.get_bank_conn(), partyunit_count_sqlstr) == 9

    partybankunit_count_sqlstr = (
        get_agenda_partyunit_table_banking_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    mbc = 13
    x_market.set_credit_flow_for_agenda(agent_id=sal_text, max_blocks_count=mbc)

    # THEN
    # with x_market.get_bank_conn() as bank_conn:
    #     river_blocks = get_river_block_dict(bank_conn, cash_agent_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == mbc


def test_market_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_agent_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_agent_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_agent_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_market.save_forum_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_agent_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_market.save_forum_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_agent_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_market.save_forum_agenda(elu_agenda)

    x_market.refresh_bank_forum_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_market.get_bank_conn(), partyunit_count_sqlstr) == 9

    partybankunit_count_sqlstr = (
        get_agenda_partyunit_table_banking_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_market.set_credit_flow_for_agenda(agent_id=sal_text)

    # THEN
    assert get_single_result(x_market.get_bank_conn(), river_block_count_sqlstr) == 40
    with x_market.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, cash_agent_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_market.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_market.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    partybankunits = x_market.get_partybankunits(sal_text)
    assert len(partybankunits) == 2
    assert partybankunits.get(bob_text) != None
    assert partybankunits.get(tom_text) != None
    assert partybankunits.get(elu_text) is None
    assert partybankunits.get(ava_text) is None

    river_sal_due_bob = partybankunits.get(bob_text)
    river_sal_due_tom = partybankunits.get(tom_text)
    river_sal_due_elu = partybankunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_market_set_credit_flow_for_agenda_CorrectlyBuildsASingle_ContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_agent_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_agent_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_agent_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_market.save_forum_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_agent_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_market.save_forum_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_agent_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_market.save_forum_agenda(elu_agenda)

    x_market.refresh_bank_forum_agendas_data()

    # WHEN
    x_market.set_credit_flow_for_agenda(agent_id=sal_text, max_blocks_count=100)

    # THEN
    count_range_fails_sql = """
    SELECT COUNT(*)
    FROM (
        SELECT 
            rt1.cash_start current_row_start
        , lag(cash_close) OVER (ORDER BY cash_start, cash_close) AS prev_close
        , lag(cash_close) OVER (ORDER BY cash_start, cash_close) - rt1.cash_start prev_diff
        , rt1.block_num or_block_num
        , lag(block_num) OVER (ORDER BY cash_start, cash_close) AS prev_block_num
        , rt1.parent_block_num or_parent_block_num
        , lag(parent_block_num) OVER (ORDER BY cash_start, cash_close) AS prev_parent_block_num
        , river_tree_level
        , lag(river_tree_level) OVER (ORDER BY cash_start, cash_close) AS prev_parent_river_tree_level
        FROM river_block rt1
        --  WHERE dst_agent_id = 'sal' and cash_master = dst_agent_id
        ORDER BY rt1.cash_start, rt1.cash_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with x_market.get_bank_conn() as bank_conn:
        assert get_single_result(bank_conn, count_range_fails_sql) == 0


def test_market_set_credit_flow_for_agenda_CorrectlyUpatesAgendaPartyUnits(
    env_dir_setup_cleanup,
):
    """GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal"""
    # GIVEN
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda_src = agendaunit_shop(_agent_id=sal_text)
    sal_agenda_src.add_partyunit(party_id=bob_text, creditor_weight=2, debtor_weight=2)
    sal_agenda_src.add_partyunit(party_id=tom_text, creditor_weight=2, debtor_weight=1)
    sal_agenda_src.add_partyunit(party_id=ava_text, creditor_weight=2, debtor_weight=2)
    x_market.save_forum_agenda(sal_agenda_src)

    bob_agenda = agendaunit_shop(_agent_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_agent_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text)
    x_market.save_forum_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_agent_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_market.save_forum_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_agent_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=8)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_market.save_forum_agenda(elu_agenda)

    x_market.refresh_bank_forum_agendas_data()
    sal_agenda_before = x_market.get_forum_agenda(agent_id=sal_text)

    x_market.set_credit_flow_for_agenda(agent_id=sal_text, max_blocks_count=100)
    assert len(sal_agenda_before._partys) == 3
    print(f"{len(sal_agenda_before._partys)=}")
    bob_party = sal_agenda_before._partys.get(bob_text)
    tom_party = sal_agenda_before._partys.get(tom_text)
    ava_party = sal_agenda_before._partys.get(ava_text)
    assert bob_party._bank_due_paid is None
    assert tom_party._bank_due_paid is None
    assert ava_party._bank_due_paid is None
    assert bob_party._bank_due_diff is None
    assert tom_party._bank_due_diff is None
    assert ava_party._bank_due_diff is None
    assert bob_party._bank_voice_rank is None
    assert tom_party._bank_voice_rank is None
    assert ava_party._bank_voice_rank is None
    assert bob_party._bank_voice_hx_lowest_rank is None
    assert tom_party._bank_voice_hx_lowest_rank is None
    assert ava_party._bank_voice_hx_lowest_rank is None

    # WHEN
    x_market.set_credit_flow_for_agenda(agent_id=sal_text)

    # THEN
    sal_partybankunits = x_market.get_partybankunits(agent_id=sal_text)
    assert len(sal_partybankunits) == 2
    bob_partybank = sal_partybankunits.get(bob_text)
    tom_partybank = sal_partybankunits.get(tom_text)
    assert bob_partybank.due_agent_id == bob_text
    assert tom_partybank.due_agent_id == tom_text
    assert bob_partybank.cash_master == sal_text
    assert tom_partybank.cash_master == sal_text

    sal_agenda_after = x_market.get_forum_agenda(agent_id=sal_text)
    bob_party = sal_agenda_after._partys.get(bob_text)
    tom_party = sal_agenda_after._partys.get(tom_text)
    ava_party = sal_agenda_after._partys.get(ava_text)
    elu_party = sal_agenda_after._partys.get(elu_text)

    assert bob_partybank.due_total == bob_party._bank_due_paid
    assert bob_partybank.due_diff == bob_party._bank_due_diff
    assert tom_partybank.due_total == tom_party._bank_due_paid
    assert tom_partybank.due_diff == tom_party._bank_due_diff
    assert elu_party is None

    # for partybank_uid, sal_partybankunit in sal_partybankunits.items():
    #     print(f"{partybank_uid=} {sal_partybankunit=}")
    #     assert sal_partybankunit.cash_master == sal_text
    #     assert sal_partybankunit.due_agent_id in [bob_text, tom_text, elu_text]
    #     x_partyunit = sal_agenda_after._partys.get(sal_partybankunit.due_agent_id)
    #     if x_partyunit != None:
    #         # print(
    #         #     f"{sal_partybankunit.cash_master=} {sal_partybankunit.due_agent_id=} {x_partyunit.party_id=} due_total: {sal_partybankunit.due_total} _Due_ Paid: {x_partyunit._bank_due_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_partybankunit.cash_master=} {sal_partybankunit.due_agent_id=} {x_partyunit.party_id=} due_diff:  {sal_partybankunit.due_diff} _Due_ Paid: {x_partyunit._bank_due_diff}"
    #         # )
    #         assert sal_partybankunit.due_total == x_partyunit._bank_due_paid
    #         assert sal_partybankunit.due_diff == x_partyunit._bank_due_diff

    assert sal_partybankunits.get(ava_text) is None
    assert ava_party._bank_due_paid is None
    assert ava_party._bank_due_diff is None

    # for x_partyunit in sal_agenda_after._partys.values():
    #     print(f"sal_agenda_after {x_partyunit.party_id=} {x_partyunit._bank_due_paid=}")
    #     partybankunit_x = sal_partybankunits.get(x_partyunit.party_id)
    #     if partybankunit_x is None:
    #         assert x_partyunit._bank_due_paid is None
    #         assert x_partyunit._bank_due_diff is None
    #     else:
    #         assert x_partyunit._bank_due_paid != None
    #         assert x_partyunit._bank_due_diff != None
    # assert sal_agenda_after != sal_agenda_before
