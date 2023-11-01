from src.agenda.agenda import agendaunit_shop
from src.culture.bank_sqlstr import (
    get_table_count_sqlstr,
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
    get_partyunit_table_update_bank_attr_sqlstr,
    get_river_block_reach_base_sqlstr,
    get_river_circle_table_create_sqlstr,
    get_river_block_table_create_sqlstr,
)
from src.culture.y_func import sqlite_text, get_single_result
from sqlite3 import connect as sqlite3_connect


def test_get_agendaunit_update_sqlstr_ReturnsCorrectStr():
    # GIVEN
    bob_healer = "Bob"
    bob_rational = False
    bob_agenda = agendaunit_shop(_healer=bob_healer)
    bob_agenda._rational = bob_rational

    # WHEN
    gen_sqlstr = get_agendaunit_update_sqlstr(agenda=bob_agenda)

    # THEN
    example_sqlstr = f"""
UPDATE agendaunit
SET rational = {sqlite_text(bob_rational)}
WHERE healer = '{bob_healer}'
;
"""
    assert gen_sqlstr == example_sqlstr


def test_get_agendaunits_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_agendaunits_select_sqlstr()

    # THEN
    example_sqlstr = """
SELECT 
  healer
, rational
FROM agendaunit
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_partyunit_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    bob_text = "bob"
    generated_sqlstr = get_partyunit_table_update_bank_attr_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
UPDATE partyunit
SET _bank_tax_paid = (
    SELECT SUM(block.currency_close-block.currency_start) 
    FROM river_block block
    WHERE block.currency_master='{bob_text}' 
        AND block.dst_healer=block.currency_master
        AND block.src_healer = partyunit.title
    )
WHERE EXISTS (
    SELECT block.currency_close
    FROM river_block block
    WHERE partyunit.agenda_healer='{bob_text}' 
        AND partyunit.title = block.dst_healer
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_block_reach_base_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    bob_text = "bob"
    generated_sqlstr = get_river_block_reach_base_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
SELECT 
  block.currency_master
, block.src_healer src
, block.dst_healer dst
, CASE 
    WHEN block.currency_start < circle.curr_start 
        AND block.currency_close > circle.curr_start
        AND block.currency_close <= circle.curr_close
        THEN circle.curr_start --'leftside' 
    WHEN block.currency_start >= circle.curr_start 
        AND block.currency_start < circle.curr_close
        AND block.currency_close > circle.curr_close
        THEN block.currency_start--'rightside' 
    WHEN block.currency_start < circle.curr_start 
        AND block.currency_close > circle.curr_close
        THEN circle.curr_start--'outside' 
    WHEN block.currency_start >= circle.curr_start 
        AND block.currency_close <= circle.curr_close
        THEN block.currency_start --'inside' 
        END reach_start
, CASE 
    WHEN block.currency_start < circle.curr_start 
        AND block.currency_close > circle.curr_start
        AND block.currency_close <= circle.curr_close
        THEN block.currency_close --'leftside' 
    WHEN block.currency_start >= circle.curr_start 
        AND block.currency_start < circle.curr_close
        AND block.currency_close > circle.curr_close
        THEN circle.curr_close --'rightside' 
    WHEN block.currency_start < circle.curr_start 
        AND block.currency_close > circle.curr_close
        THEN circle.curr_close--'outside' 
    WHEN block.currency_start >= circle.curr_start 
        AND block.currency_close <= circle.curr_close
        THEN block.currency_close --'inside' 
        END reach_close
FROM river_block block
JOIN river_circle circle on 
           (block.currency_start < circle.curr_start 
        AND block.currency_close > circle.curr_close)
    OR     (block.currency_start >= circle.curr_start 
        AND block.currency_close <= circle.curr_close)
    OR     (block.currency_start < circle.curr_start 
        AND block.currency_close > circle.curr_start
        AND block.currency_close <= circle.curr_close)
    OR     (block.currency_start >= circle.curr_start 
        AND block.currency_start < circle.curr_close
        AND block.currency_close > circle.curr_close)
WHERE block.currency_master = '{bob_text}'
    AND block.src_healer != block.currency_master
ORDER BY 
  block.src_healer
, block.dst_healer
, block.currency_start
, block.currency_close
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_block_reach_base_sqlstr_QuerySelectsCorrectResults():
    # GIVEN
    x_db = sqlite3_connect(":memory:")
    with x_db as bank_conn:
        x_db.execute(get_river_block_table_create_sqlstr())
        x_db.execute(get_river_circle_table_create_sqlstr())

    block_text = "river_block"
    circle_text = "river_circle"
    with x_db as bank_conn:
        assert 0 == get_single_result(x_db, get_table_count_sqlstr(block_text))
        assert 0 == get_single_result(x_db, get_table_count_sqlstr(circle_text))
    insert_block_values_str = """
INSERT INTO river_block (currency_master, src_healer, dst_healer, currency_start, currency_close, block_num, parent_block_num, river_tree_level)
VALUES ('sal', 'sal', 'ava', 0.0, 0.1, 0, NULL, 1)
,('sal', 'sal', 'bob', 0.1, 0.3, 1, NULL, 1)
,('sal', 'sal', 'tom', 0.3, 1.0, 2, NULL, 1)
,('sal', 'ava', 'elu', 0.0, 0.1, 3, 0, 2)
,('sal', 'bob', 'ava', 0.1, 0.15, 4, 1, 2)
,('sal', 'bob', 'sal', 0.15, 0.3, 5, 1, 2)
,('sal', 'tom', 'sal', 0.3, 1.0, 6, 2, 2)
,('sal', 'elu', 'ava', 0.0, 0.095, 7, 3, 3)
,('sal', 'elu', 'sal', 0.095, 0.1, 8, 3, 3)
,('sal', 'ava', 'elu', 0.1, 0.15, 9, 4, 3)
,('sal', 'ava', 'elu', 0.0, 0.095, 10, 7, 4)
,('sal', 'elu', 'ava', 0.1, 0.1475, 11, 9, 4)
,('sal', 'elu', 'sal', 0.1475, 0.15, 12, 9, 4)
,('sal', 'elu', 'ava', 0.0, 0.09025, 13, 10, 5)
,('sal', 'elu', 'sal', 0.09025, 0.095, 14, 10, 5)
,('sal', 'ava', 'elu', 0.1, 0.1475, 15, 11, 5)
,('sal', 'ava', 'elu', 0.0, 0.09025, 16, 13, 6)
,('sal', 'elu', 'ava', 0.1, 0.145125, 17, 15, 6)
,('sal', 'elu', 'sal', 0.145125, 0.1475, 18, 15, 6)
,('sal', 'elu', 'ava', 0.0, 0.0857375, 19, 16, 7)
,('sal', 'elu', 'sal', 0.0857375, 0.09025, 20, 16, 7)
,('sal', 'ava', 'elu', 0.1, 0.145125, 21, 17, 7)
,('sal', 'ava', 'elu', 0.0, 0.0857375, 22, 19, 8)
,('sal', 'elu', 'ava', 0.1, 0.14286875, 23, 21, 8)
,('sal', 'elu', 'sal', 0.14286875, 0.145125, 24, 21, 8)
,('sal', 'elu', 'ava', 0.0, 0.081450625, 25, 22, 9)
,('sal', 'elu', 'sal', 0.081450625, 0.0857375, 26, 22, 9)
,('sal', 'ava', 'elu', 0.1, 0.14286875, 27, 23, 9)
,('sal', 'ava', 'elu', 0.0, 0.081450625, 28, 25, 10)
,('sal', 'elu', 'ava', 0.1, 0.1407253125, 29, 27, 10)
,('sal', 'elu', 'sal', 0.1407253125, 0.14286875, 30, 27, 10)
,('sal', 'elu', 'ava', 0.0, 0.07737809375, 31, 28, 11)
,('sal', 'elu', 'sal', 0.07737809375, 0.081450625, 32, 28, 11)
,('sal', 'ava', 'elu', 0.1, 0.1407253125, 33, 29, 11)
,('sal', 'ava', 'elu', 0.0, 0.07737809375, 34, 31, 12)
,('sal', 'elu', 'ava', 0.1, 0.138689046875, 35, 33, 12)
,('sal', 'elu', 'sal', 0.138689046875, 0.1407253125, 36, 33, 12)
,('sal', 'elu', 'ava', 0.0, 0.0735091890625, 37, 34, 13)
,('sal', 'elu', 'sal', 0.0735091890625, 0.07737809375, 38, 34, 13)
,('sal', 'ava', 'elu', 0.1, 0.138689046875, 39, 35, 13)
,('sal', 'ava', 'elu', 0.0, 0.0735091890625, 40, 37, 14)
,('sal', 'elu', 'ava', 0.1, 0.13675459453125, 41, 39, 14)
,('sal', 'elu', 'sal', 0.13675459453125, 0.138689046875, 42, 39, 14)
,('sal', 'elu', 'ava', 0.0, 0.069833729609375, 43, 40, 15)
,('sal', 'elu', 'sal', 0.069833729609375, 0.0735091890625, 44, 40, 15)
,('sal', 'ava', 'elu', 0.1, 0.13675459453125, 45, 41, 15)
,('sal', 'ava', 'elu', 0.0, 0.069833729609375, 46, 43, 16)
,('sal', 'elu', 'ava', 0.1, 0.134916864804687, 47, 45, 16)
,('sal', 'elu', 'sal', 0.134916864804687, 0.13675459453125, 48, 45, 16)
,('sal', 'elu', 'ava', 0.0, 0.0663420431289062, 49, 46, 17)
,('sal', 'elu', 'sal', 0.0663420431289062, 0.069833729609375, 50, 46, 17)
,('sal', 'ava', 'elu', 0.1, 0.134916864804687, 51, 47, 17)
,('sal', 'ava', 'elu', 0.0, 0.0663420431289062, 52, 49, 18)
,('sal', 'elu', 'ava', 0.1, 0.133171021564453, 53, 51, 18)
,('sal', 'elu', 'sal', 0.133171021564453, 0.134916864804687, 54, 51, 18)
,('sal', 'elu', 'ava', 0.0, 0.0630249409724609, 55, 52, 19)
,('sal', 'elu', 'sal', 0.0630249409724609, 0.0663420431289062, 56, 52, 19)
,('sal', 'ava', 'elu', 0.1, 0.133171021564453, 57, 53, 19)
,('sal', 'ava', 'elu', 0.0, 0.0630249409724609, 58, 55, 20)
,('sal', 'elu', 'ava', 0.1, 0.13151247048623, 59, 57, 20)
,('sal', 'elu', 'sal', 0.13151247048623, 0.133171021564453, 60, 57, 20)
,('sal', 'elu', 'ava', 0.0, 0.0598736939238379, 61, 58, 21)
,('sal', 'elu', 'sal', 0.0598736939238379, 0.0630249409724609, 62, 58, 21)
,('sal', 'ava', 'elu', 0.1, 0.13151247048623, 63, 59, 21)
,('sal', 'ava', 'elu', 0.0, 0.0598736939238379, 64, 61, 22)
,('sal', 'elu', 'ava', 0.1, 0.129936846961919, 65, 63, 22)
,('sal', 'elu', 'sal', 0.129936846961919, 0.13151247048623, 66, 63, 22)
,('sal', 'elu', 'ava', 0.0, 0.056880009227646, 67, 64, 23)
,('sal', 'elu', 'sal', 0.056880009227646, 0.0598736939238379, 68, 64, 23)
,('sal', 'ava', 'elu', 0.1, 0.129936846961919, 69, 65, 23)
,('sal', 'ava', 'elu', 0.0, 0.056880009227646, 70, 67, 24)
,('sal', 'elu', 'ava', 0.1, 0.128440004613823, 71, 69, 24)
,('sal', 'elu', 'sal', 0.128440004613823, 0.129936846961919, 72, 69, 24)
,('sal', 'elu', 'ava', 0.0, 0.0540360087662637, 73, 70, 25)
,('sal', 'elu', 'sal', 0.0540360087662637, 0.056880009227646, 74, 70, 25)
,('sal', 'ava', 'elu', 0.1, 0.128440004613823, 75, 71, 25)
,('sal', 'ava', 'elu', 0.0, 0.0540360087662637, 76, 73, 26)
,('sal', 'elu', 'ava', 0.1, 0.127018004383132, 77, 75, 26)
,('sal', 'elu', 'sal', 0.127018004383132, 0.128440004613823, 78, 75, 26)
,('sal', 'elu', 'ava', 0.0, 0.0513342083279505, 79, 76, 27)
,('sal', 'elu', 'sal', 0.0513342083279505, 0.0540360087662637, 80, 76, 27)
,('sal', 'ava', 'elu', 0.1, 0.127018004383132, 81, 77, 27)
,('sal', 'ava', 'elu', 0.0, 0.0513342083279505, 82, 79, 28)
,('sal', 'elu', 'ava', 0.1, 0.125667104163975, 83, 81, 28)
,('sal', 'elu', 'sal', 0.125667104163975, 0.127018004383132, 84, 81, 28)
,('sal', 'elu', 'ava', 0.0, 0.048767497911553, 85, 82, 29)
,('sal', 'elu', 'sal', 0.048767497911553, 0.0513342083279505, 86, 82, 29)
,('sal', 'ava', 'elu', 0.1, 0.125667104163975, 87, 83, 29)
,('sal', 'ava', 'elu', 0.0, 0.048767497911553, 88, 85, 30)
,('sal', 'elu', 'ava', 0.1, 0.124383748955776, 89, 87, 30)
,('sal', 'elu', 'sal', 0.124383748955776, 0.125667104163975, 90, 87, 30)
,('sal', 'elu', 'ava', 0.0, 0.0463291230159753, 91, 88, 31)
,('sal', 'elu', 'sal', 0.0463291230159753, 0.048767497911553, 92, 88, 31)
,('sal', 'ava', 'elu', 0.1, 0.124383748955776, 93, 89, 31)
,('sal', 'ava', 'elu', 0.0, 0.0463291230159753, 94, 91, 32)
,('sal', 'elu', 'ava', 0.1, 0.123164561507988, 95, 93, 32)
,('sal', 'elu', 'sal', 0.123164561507988, 0.124383748955776, 96, 93, 32)
,('sal', 'elu', 'ava', 0.0, 0.0440126668651765, 97, 94, 33)
,('sal', 'elu', 'sal', 0.0440126668651765, 0.0463291230159753, 98, 94, 33)
,('sal', 'ava', 'elu', 0.1, 0.123164561507988, 99, 95, 33)
;
"""
    insert_circle_values_str = """
INSERT INTO river_circle (currency_master, dst_healer, circle_num, curr_start, curr_close)
VALUES ('sal', 'sal', 0, 0.0440126668651765, 0.1)
, ('sal', 'sal', 1, 0.123164561507988, 1.0)
;
"""
    with x_db as bank_conn:
        x_db.execute(insert_block_values_str)
        x_db.execute(insert_circle_values_str)

        assert 100 == get_single_result(x_db, get_table_count_sqlstr(block_text))
        assert 2 == get_single_result(x_db, get_table_count_sqlstr(circle_text))

    # WHEN
    sal_text = "sal"
    reach_sqlstr = get_river_block_reach_base_sqlstr(sal_text)
    reach_count_sqlstr = f"""SELECT COUNT(*) FROM ({reach_sqlstr}) x;"""
    reach_rows_num = get_single_result(x_db, reach_count_sqlstr)

    # THEN
    assert reach_rows_num == 94
