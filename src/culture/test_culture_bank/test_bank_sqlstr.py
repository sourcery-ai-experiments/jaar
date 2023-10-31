from src.agenda.agenda import agendaunit_shop
from src.culture.bank_sqlstr import (
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
    get_partyunit_table_update_bank_attr_sqlstr,
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
    WHERE block.currency_healer='{bob_text}' 
        AND block.dst_healer=block.currency_healer
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
