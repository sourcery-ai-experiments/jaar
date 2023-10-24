from src.agenda.agenda import agendaunit_shop
from src.culture.bank_sqlstr import (
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
)
from src.culture.y_func import sqlite_text


def test_get_agendaunit_update_sqlstr_ReturnsCorrectObj():
    # GIVEN
    bob_healer = "Bob"
    bob_rational = False
    bob_agenda = agendaunit_shop(_healer=bob_healer)
    bob_agenda._rational = bob_rational

    # WHEN
    gen_sqlstr = get_agendaunit_update_sqlstr(agenda=bob_agenda)

    # THEN
    ex_sqlstr = f"""
UPDATE agendaunit
SET rational = {sqlite_text(bob_rational)}
WHERE healer = '{bob_healer}'
;
"""
    assert gen_sqlstr == ex_sqlstr


def test_get_agendaunits_select_sqlstr_ReturnsCorrectObj():
    # GIVEN / WHEN
    gen_sqlstr = get_agendaunits_select_sqlstr()

    # THEN
    ex_sqlstr = """
SELECT 
  healer
, rational
FROM agendaunit
;
"""
    assert gen_sqlstr == ex_sqlstr
