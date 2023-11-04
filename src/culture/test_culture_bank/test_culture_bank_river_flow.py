from src.agenda.agenda import agendaunit_shop
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_title,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.y_func import get_single_result
from src.culture.bank_sqlstr import (
    get_partybankunit_dict,
    get_river_block_dict,
    get_table_count_sqlstr,
)


def get_partyunit_table_banking_attr_set_count_sqlstr():
    # def get_partyunit_table_banking_attr_set_count_sqlstr(currency_master:):
    #     return f"""
    # SELECT COUNT(*)
    # FROM partyunit
    # WHERE _bank_tax_paid IS NOT NULL
    #     AND agenda_healer = {currency_master}
    # """
    return """
SELECT COUNT(*) 
FROM partyunit
WHERE _bank_tax_paid IS NOT NULL
;
"""


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    sal = agendaunit_shop(_healer=sal_text)
    sal.add_partyunit(handle=bob_text, creditor_weight=1)
    sal.add_partyunit(handle=tom_text, creditor_weight=3)
    x_culture.save_public_agenda(x_agenda=sal)

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(handle=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob)

    tom = agendaunit_shop(_healer=tom_text)
    tom.add_partyunit(handle=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=tom)

    x_culture.refresh_bank_public_agendas_data()
    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_culture.get_bank_conn(), partyunit_count_sqlstr) == 4

    partybankunit_count_sqlstr = get_partyunit_table_banking_attr_set_count_sqlstr()
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 4
    with x_culture.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)

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

    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_culture.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    assert len(partybankunits) == 2
    river_sal_tax_bob = partybankunits.get(bob_text)
    river_sal_tax_tom = partybankunits.get(tom_text)

    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")

    assert river_sal_tax_bob.tax_total == 0.25
    assert river_sal_tax_tom.tax_total == 0.75


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agendas, 85% of river blocks to sal
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(handle=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(handle=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(handle=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(handle=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    x_culture.save_public_agenda(x_agenda=ava_agenda)
    x_culture.refresh_bank_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_culture.get_bank_conn(), partyunit_count_sqlstr) == 6

    partybankunit_count_sqlstr = get_partyunit_table_banking_attr_set_count_sqlstr()
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 6
    with x_culture.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_culture.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    assert len(partybankunits) == 2
    assert partybankunits.get(bob_text) != None
    assert partybankunits.get(tom_text) != None
    assert partybankunits.get(ava_text) is None

    river_sal_tax_bob = partybankunits.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = partybankunits.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(handle=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(handle=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(handle=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(handle=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(handle=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(handle=ava_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_culture.get_bank_conn(), partyunit_count_sqlstr) == 8

    partybankunit_count_sqlstr = get_partyunit_table_banking_attr_set_count_sqlstr()
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 40
    # with x_culture.get_bank_conn() as bank_conn:
    #     river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_culture.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    assert len(partybankunits) == 2
    assert partybankunits.get(bob_text) != None
    assert partybankunits.get(tom_text) != None
    assert partybankunits.get(ava_text) is None

    river_sal_tax_bob = partybankunits.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = partybankunits.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable05_v1(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(handle=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(handle=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(handle=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(handle=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(handle=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(handle=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(handle=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_culture.get_bank_conn(), partyunit_count_sqlstr) == 9

    partybankunit_count_sqlstr = get_partyunit_table_banking_attr_set_count_sqlstr()
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 40
    # with x_culture.get_bank_conn() as bank_conn:
    #     river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_culture.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    assert len(partybankunits) == 2
    assert partybankunits.get(bob_text) != None
    assert partybankunits.get(tom_text) != None
    assert partybankunits.get(elu_text) is None
    assert partybankunits.get(ava_text) is None

    river_sal_tax_bob = partybankunits.get(bob_text)
    river_sal_tax_tom = partybankunits.get(tom_text)
    river_sal_tax_elu = partybankunits.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7


def test_culture_set_credit_flow_for_agenda_CorrectlyUsesMaxblocksCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(handle=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(handle=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(handle=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(handle=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(handle=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(handle=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(handle=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_culture.get_bank_conn(), partyunit_count_sqlstr) == 9

    partybankunit_count_sqlstr = get_partyunit_table_banking_attr_set_count_sqlstr()
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    mbc = 13
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=mbc)

    # THEN
    # with x_culture.get_bank_conn() as bank_conn:
    #     river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == mbc


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatespartybankunitTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(handle=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(handle=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(handle=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(handle=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(handle=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(handle=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(handle=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_culture.get_bank_conn(), partyunit_count_sqlstr) == 9

    partybankunit_count_sqlstr = get_partyunit_table_banking_attr_set_count_sqlstr()
    river_block_count_sqlstr = get_table_count_sqlstr("river_block")
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 0
    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 0

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert get_single_result(x_culture.get_bank_conn(), river_block_count_sqlstr) == 40
    with x_culture.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert get_single_result(x_culture.get_bank_conn(), partybankunit_count_sqlstr) == 2

    with x_culture.get_bank_conn() as bank_conn:
        partybankunits = get_partybankunit_dict(bank_conn, sal_text)
    partybankunits = x_culture.get_partybankunits(sal_text)
    assert len(partybankunits) == 2
    assert partybankunits.get(bob_text) != None
    assert partybankunits.get(tom_text) != None
    assert partybankunits.get(elu_text) is None
    assert partybankunits.get(ava_text) is None

    river_sal_tax_bob = partybankunits.get(bob_text)
    river_sal_tax_tom = partybankunits.get(tom_text)
    river_sal_tax_elu = partybankunits.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7


def test_culture_set_credit_flow_for_agenda_CorrectlyBuildsASingleContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(handle=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(handle=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(handle=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(handle=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(handle=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(handle=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(handle=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=100)

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
    with x_culture.get_bank_conn() as bank_conn:
        assert get_single_result(bank_conn, count_range_fails_sql) == 0


def test_culture_set_credit_flow_for_agenda_CorrectlyUpatesAgendaPartyUnits(
    env_dir_setup_cleanup,
):
    """GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal"""
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda_src = agendaunit_shop(_healer=sal_text)
    sal_agenda_src.add_partyunit(handle=bob_text, creditor_weight=2, debtor_weight=2)
    sal_agenda_src.add_partyunit(handle=tom_text, creditor_weight=2, debtor_weight=1)
    sal_agenda_src.add_partyunit(handle=ava_text, creditor_weight=2, debtor_weight=2)
    x_culture.save_public_agenda(x_agenda=sal_agenda_src)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(handle=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(handle=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(handle=sal_text)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(handle=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(handle=ava_text, creditor_weight=8)
    elu_agenda.add_partyunit(handle=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()
    sal_agenda_before = x_culture.get_public_agenda(healer=sal_text)

    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=100)
    assert len(sal_agenda_before._partys) == 3
    print(f"{len(sal_agenda_before._partys)=}")
    bob_party = sal_agenda_before._partys.get(bob_text)
    tom_party = sal_agenda_before._partys.get(tom_text)
    ava_party = sal_agenda_before._partys.get(ava_text)
    assert bob_party._bank_tax_paid is None
    assert tom_party._bank_tax_paid is None
    assert ava_party._bank_tax_paid is None
    assert bob_party._bank_tax_diff is None
    assert tom_party._bank_tax_diff is None
    assert ava_party._bank_tax_diff is None
    assert bob_party._bank_voice_rank is None
    assert tom_party._bank_voice_rank is None
    assert ava_party._bank_voice_rank is None
    assert bob_party._bank_voice_hx_lowest_rank is None
    assert tom_party._bank_voice_hx_lowest_rank is None
    assert ava_party._bank_voice_hx_lowest_rank is None

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    sal_partybankunits = x_culture.get_partybankunits(agenda_healer=sal_text)
    assert len(sal_partybankunits) == 2
    bob_partybank = sal_partybankunits.get(bob_text)
    tom_partybank = sal_partybankunits.get(tom_text)
    assert bob_partybank.tax_healer == bob_text
    assert tom_partybank.tax_healer == tom_text
    assert bob_partybank.currency_master == sal_text
    assert tom_partybank.currency_master == sal_text

    sal_agenda_after = x_culture.get_public_agenda(healer=sal_text)
    bob_party = sal_agenda_after._partys.get(bob_text)
    tom_party = sal_agenda_after._partys.get(tom_text)
    ava_party = sal_agenda_after._partys.get(ava_text)
    elu_party = sal_agenda_after._partys.get(elu_text)

    assert bob_partybank.tax_total == bob_party._bank_tax_paid
    assert bob_partybank.tax_diff == bob_party._bank_tax_diff
    assert tom_partybank.tax_total == tom_party._bank_tax_paid
    assert tom_partybank.tax_diff == tom_party._bank_tax_diff
    assert elu_party is None

    # for partybank_uid, sal_partybankunit in sal_partybankunits.items():
    #     print(f"{partybank_uid=} {sal_partybankunit=}")
    #     assert sal_partybankunit.currency_master == sal_text
    #     assert sal_partybankunit.tax_healer in [bob_text, tom_text, elu_text]
    #     partyunit_x = sal_agenda_after._partys.get(sal_partybankunit.tax_healer)
    #     if partyunit_x != None:
    #         # print(
    #         #     f"{sal_partybankunit.currency_master=} {sal_partybankunit.tax_healer=} {partyunit_x.handle=} tax_total: {sal_partybankunit.tax_total} Tax Paid: {partyunit_x._bank_tax_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_partybankunit.currency_master=} {sal_partybankunit.tax_healer=} {partyunit_x.handle=} tax_diff:  {sal_partybankunit.tax_diff} Tax Paid: {partyunit_x._bank_tax_diff}"
    #         # )
    #         assert sal_partybankunit.tax_total == partyunit_x._bank_tax_paid
    #         assert sal_partybankunit.tax_diff == partyunit_x._bank_tax_diff

    assert sal_partybankunits.get(ava_text) is None
    assert ava_party._bank_tax_paid is None
    assert ava_party._bank_tax_diff is None

    # for partyunit_x in sal_agenda_after._partys.values():
    #     print(f"sal_agenda_after {partyunit_x.handle=} {partyunit_x._bank_tax_paid=}")
    #     partybankunit_x = sal_partybankunits.get(partyunit_x.handle)
    #     if partybankunit_x is None:
    #         assert partyunit_x._bank_tax_paid is None
    #         assert partyunit_x._bank_tax_diff is None
    #     else:
    #         assert partyunit_x._bank_tax_paid != None
    #         assert partyunit_x._bank_tax_diff != None
    # assert sal_agenda_after != sal_agenda_before
