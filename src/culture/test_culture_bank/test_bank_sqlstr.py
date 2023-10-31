from src.agenda.agenda import agendaunit_shop
from src.culture.bank_sqlstr import (
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
    get_partyunit_table_update_bank_attr_sqlstr,
    get_river_block_reach_base_sqlstr,
)
from src.culture.y_func import sqlite_text


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
