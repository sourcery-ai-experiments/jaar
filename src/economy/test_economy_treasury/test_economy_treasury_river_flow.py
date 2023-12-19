from src.agenda.agenda import agendaunit_shop
from src.economy.economy import economyunit_shop
from src.economy.examples.economy_env_kit import (
    get_temp_env_economy_id,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from src.economy.y_func import get_single_result
from src.economy.treasury_sqlstr import (
    get_partytreasuryunit_dict,
    get_river_block_dict,
    get_table_count_sqlstr,
)


def get_partyunit_table_treasurying_attr_set_count_sqlstr():
    # def get_partyunit_table_treasurying_attr_set_count_sqlstr(currency_master:):
    #     return f"""
    # SELECT COUNT(*)
    # FROM partyunit
    # WHERE _treasury_tax_paid IS NOT NULL
    #     AND agenda_healer = {currency_master}
    # """
    return """
SELECT COUNT(*) 
FROM partyunit
WHERE _treasury_tax_paid IS NOT NULL
;
"""


def test_economy_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    sal = agendaunit_shop(_healer=sal_text)
    sal.add_partyunit(pid=bob_text, creditor_weight=1)
    sal.add_partyunit(pid=tom_text, creditor_weight=3)
    x_economy.save_public_agenda(sal)

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(pid=sal_text, creditor_weight=1)
    x_economy.save_public_agenda(bob)

    tom = agendaunit_shop(_healer=tom_text)
    tom.add_partyunit(pid=sal_text, creditor_weight=1)
    x_economy.save_public_agenda(tom)

    x_economy.refresh_treasury_public_agendas_data()
    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_economy.get_treasury_conn(), partyunit_count_sqlstr) == 4

    partytreasuryunit_count_sqlstr = (
        get_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 0
    )
    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 4
    )
    with x_economy.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(
            treasury_conn, currency_agenda_healer=sal_text
        )

    block_0 = river_blocks.get(0)
    block_1 = river_blocks.get(1)
    assert block_1.src_healer == sal_text and block_1.dst_healer == tom_text
    assert block_1.river_tree_level == 1
    assert block_1.currency_start == 0.25
    assert block_1.currency_close == 1
    assert block_1.parent_block_num is None
    block_2 = river_blocks.get(2)
    block_3 = river_blocks.get(3)
    assert block_3.src_healer == tom_text and block_3.dst_healer == sal_text
    assert block_3.river_tree_level == 2
    assert block_3.parent_block_num == 1

    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_economy.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    assert len(partytreasuryunits) == 2
    river_sal_tax_bob = partytreasuryunits.get(bob_text)
    river_sal_tax_tom = partytreasuryunits.get(tom_text)

    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")

    assert river_sal_tax_bob.tax_total == 0.25
    assert river_sal_tax_tom.tax_total == 0.75


def test_economy_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agendas, 85% of river blocks to sal
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(pid=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(pid=sal_text, creditor_weight=2)
    x_economy.save_public_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    x_economy.save_public_agenda(ava_agenda)
    x_economy.refresh_treasury_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_economy.get_treasury_conn(), partyunit_count_sqlstr) == 6

    partytreasuryunit_count_sqlstr = (
        get_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 0
    )
    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 6
    )
    with x_economy.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(
            treasury_conn, currency_agenda_healer=sal_text
        )
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_economy.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    assert len(partytreasuryunits) == 2
    assert partytreasuryunits.get(bob_text) != None
    assert partytreasuryunits.get(tom_text) != None
    assert partytreasuryunits.get(ava_text) is None

    river_sal_tax_bob = partytreasuryunits.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = partytreasuryunits.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_economy_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(pid=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(pid=sal_text, creditor_weight=2)
    x_economy.save_public_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(pid=elu_text, creditor_weight=2)
    x_economy.save_public_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(pid=ava_text, creditor_weight=2)
    x_economy.save_public_agenda(elu_agenda)

    x_economy.refresh_treasury_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_economy.get_treasury_conn(), partyunit_count_sqlstr) == 8

    partytreasuryunit_count_sqlstr = (
        get_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 0
    )
    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    # with x_economy.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_economy.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    assert len(partytreasuryunits) == 2
    assert partytreasuryunits.get(bob_text) != None
    assert partytreasuryunits.get(tom_text) != None
    assert partytreasuryunits.get(ava_text) is None

    river_sal_tax_bob = partytreasuryunits.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = partytreasuryunits.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_economy_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable05_v1(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(pid=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(pid=sal_text, creditor_weight=2)
    x_economy.save_public_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(pid=elu_text, creditor_weight=2)
    x_economy.save_public_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(pid=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(pid=sal_text, creditor_weight=1)
    x_economy.save_public_agenda(elu_agenda)

    x_economy.refresh_treasury_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_economy.get_treasury_conn(), partyunit_count_sqlstr) == 9

    partytreasuryunit_count_sqlstr = (
        get_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 0
    )
    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    # with x_economy.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_economy.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    assert len(partytreasuryunits) == 2
    assert partytreasuryunits.get(bob_text) != None
    assert partytreasuryunits.get(tom_text) != None
    assert partytreasuryunits.get(elu_text) is None
    assert partytreasuryunits.get(ava_text) is None

    river_sal_tax_bob = partytreasuryunits.get(bob_text)
    river_sal_tax_tom = partytreasuryunits.get(tom_text)
    river_sal_tax_elu = partytreasuryunits.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7


def test_economy_set_credit_flow_for_agenda_CorrectlyUsesMaxblocksCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(pid=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(pid=sal_text, creditor_weight=2)
    x_economy.save_public_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(pid=elu_text, creditor_weight=2)
    x_economy.save_public_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(pid=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(pid=sal_text, creditor_weight=1)
    x_economy.save_public_agenda(elu_agenda)

    x_economy.refresh_treasury_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_economy.get_treasury_conn(), partyunit_count_sqlstr) == 9

    partytreasuryunit_count_sqlstr = (
        get_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 0
    )
    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    mbc = 13
    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=mbc)

    # THEN
    # with x_economy.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr)
        == mbc
    )


def test_economy_set_credit_flow_for_agenda_CorrectlyPopulatespartytreasuryunitTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(pid=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(pid=sal_text, creditor_weight=2)
    x_economy.save_public_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(pid=elu_text, creditor_weight=2)
    x_economy.save_public_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(pid=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(pid=sal_text, creditor_weight=1)
    x_economy.save_public_agenda(elu_agenda)

    x_economy.refresh_treasury_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_economy.get_treasury_conn(), partyunit_count_sqlstr) == 9

    partytreasuryunit_count_sqlstr = (
        get_partyunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 0
    )
    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result(x_economy.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    with x_economy.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(
            treasury_conn, currency_agenda_healer=sal_text
        )
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_economy.get_treasury_conn(), partytreasuryunit_count_sqlstr)
        == 2
    )

    with x_economy.get_treasury_conn() as treasury_conn:
        partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, sal_text)
    partytreasuryunits = x_economy.get_partytreasuryunits(sal_text)
    assert len(partytreasuryunits) == 2
    assert partytreasuryunits.get(bob_text) != None
    assert partytreasuryunits.get(tom_text) != None
    assert partytreasuryunits.get(elu_text) is None
    assert partytreasuryunits.get(ava_text) is None

    river_sal_tax_bob = partytreasuryunits.get(bob_text)
    river_sal_tax_tom = partytreasuryunits.get(tom_text)
    river_sal_tax_elu = partytreasuryunits.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7


def test_economy_set_credit_flow_for_agenda_CorrectlyBuildsASingleContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(pid=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(pid=sal_text, creditor_weight=2)
    x_economy.save_public_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(pid=elu_text, creditor_weight=2)
    x_economy.save_public_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(pid=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(pid=sal_text, creditor_weight=1)
    x_economy.save_public_agenda(elu_agenda)

    x_economy.refresh_treasury_public_agendas_data()

    # WHEN
    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=100)

    # THEN
    count_range_fails_sql = """
    SELECT COUNT(*)
    FROM (
        SELECT 
            rt1.currency_start current_row_start
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) AS prev_close
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) - rt1.currency_start prev_diff
        , rt1.block_num or_block_num
        , lag(block_num) OVER (ORDER BY currency_start, currency_close) AS prev_block_num
        , rt1.parent_block_num or_parent_block_num
        , lag(parent_block_num) OVER (ORDER BY currency_start, currency_close) AS prev_parent_block_num
        , river_tree_level
        , lag(river_tree_level) OVER (ORDER BY currency_start, currency_close) AS prev_parent_river_tree_level
        FROM river_block rt1
        --  WHERE dst_healer = 'sal' and currency_master = dst_healer
        ORDER BY rt1.currency_start, rt1.currency_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with x_economy.get_treasury_conn() as treasury_conn:
        assert get_single_result(treasury_conn, count_range_fails_sql) == 0


def test_economy_set_credit_flow_for_agenda_CorrectlyUpatesAgendaPartyUnits(
    env_dir_setup_cleanup,
):
    """GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal"""
    # GIVEN
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda_src = agendaunit_shop(_healer=sal_text)
    sal_agenda_src.add_partyunit(pid=bob_text, creditor_weight=2, debtor_weight=2)
    sal_agenda_src.add_partyunit(pid=tom_text, creditor_weight=2, debtor_weight=1)
    sal_agenda_src.add_partyunit(pid=ava_text, creditor_weight=2, debtor_weight=2)
    x_economy.save_public_agenda(sal_agenda_src)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(pid=sal_text)
    x_economy.save_public_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(pid=elu_text, creditor_weight=2)
    x_economy.save_public_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(pid=ava_text, creditor_weight=8)
    elu_agenda.add_partyunit(pid=sal_text, creditor_weight=2)
    x_economy.save_public_agenda(elu_agenda)

    x_economy.refresh_treasury_public_agendas_data()
    sal_agenda_before = x_economy.get_public_agenda(healer=sal_text)

    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=100)
    assert len(sal_agenda_before._partys) == 3
    print(f"{len(sal_agenda_before._partys)=}")
    bob_party = sal_agenda_before._partys.get(bob_text)
    tom_party = sal_agenda_before._partys.get(tom_text)
    ava_party = sal_agenda_before._partys.get(ava_text)
    assert bob_party._treasury_tax_paid is None
    assert tom_party._treasury_tax_paid is None
    assert ava_party._treasury_tax_paid is None
    assert bob_party._treasury_tax_diff is None
    assert tom_party._treasury_tax_diff is None
    assert ava_party._treasury_tax_diff is None
    assert bob_party._treasury_voice_rank is None
    assert tom_party._treasury_voice_rank is None
    assert ava_party._treasury_voice_rank is None
    assert bob_party._treasury_voice_hx_lowest_rank is None
    assert tom_party._treasury_voice_hx_lowest_rank is None
    assert ava_party._treasury_voice_hx_lowest_rank is None

    # WHEN
    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    sal_partytreasuryunits = x_economy.get_partytreasuryunits(agenda_healer=sal_text)
    assert len(sal_partytreasuryunits) == 2
    bob_partytreasury = sal_partytreasuryunits.get(bob_text)
    tom_partytreasury = sal_partytreasuryunits.get(tom_text)
    assert bob_partytreasury.tax_healer == bob_text
    assert tom_partytreasury.tax_healer == tom_text
    assert bob_partytreasury.currency_master == sal_text
    assert tom_partytreasury.currency_master == sal_text

    sal_agenda_after = x_economy.get_public_agenda(healer=sal_text)
    bob_party = sal_agenda_after._partys.get(bob_text)
    tom_party = sal_agenda_after._partys.get(tom_text)
    ava_party = sal_agenda_after._partys.get(ava_text)
    elu_party = sal_agenda_after._partys.get(elu_text)

    assert bob_partytreasury.tax_total == bob_party._treasury_tax_paid
    assert bob_partytreasury.tax_diff == bob_party._treasury_tax_diff
    assert tom_partytreasury.tax_total == tom_party._treasury_tax_paid
    assert tom_partytreasury.tax_diff == tom_party._treasury_tax_diff
    assert elu_party is None

    # for partytreasury_uid, sal_partytreasuryunit in sal_partytreasuryunits.items():
    #     print(f"{partytreasury_uid=} {sal_partytreasuryunit=}")
    #     assert sal_partytreasuryunit.currency_master == sal_text
    #     assert sal_partytreasuryunit.tax_healer in [bob_text, tom_text, elu_text]
    #     x_partyunit = sal_agenda_after._partys.get(sal_partytreasuryunit.tax_healer)
    #     if x_partyunit != None:
    #         # print(
    #         #     f"{sal_partytreasuryunit.currency_master=} {sal_partytreasuryunit.tax_healer=} {x_partyunit.pid=} tax_total: {sal_partytreasuryunit.tax_total} Tax Paid: {x_partyunit._treasury_tax_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_partytreasuryunit.currency_master=} {sal_partytreasuryunit.tax_healer=} {x_partyunit.pid=} tax_diff:  {sal_partytreasuryunit.tax_diff} Tax Paid: {x_partyunit._treasury_tax_diff}"
    #         # )
    #         assert sal_partytreasuryunit.tax_total == x_partyunit._treasury_tax_paid
    #         assert sal_partytreasuryunit.tax_diff == x_partyunit._treasury_tax_diff

    assert sal_partytreasuryunits.get(ava_text) is None
    assert ava_party._treasury_tax_paid is None
    assert ava_party._treasury_tax_diff is None

    # for x_partyunit in sal_agenda_after._partys.values():
    #     print(f"sal_agenda_after {x_partyunit.pid=} {x_partyunit._treasury_tax_paid=}")
    #     partytreasuryunit_x = sal_partytreasuryunits.get(x_partyunit.pid)
    #     if partytreasuryunit_x is None:
    #         assert x_partyunit._treasury_tax_paid is None
    #         assert x_partyunit._treasury_tax_diff is None
    #     else:
    #         assert x_partyunit._treasury_tax_paid != None
    #         assert x_partyunit._treasury_tax_diff != None
    # assert sal_agenda_after != sal_agenda_before
