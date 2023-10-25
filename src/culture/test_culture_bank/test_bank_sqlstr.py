from src.agenda.agenda import agendaunit_shop
from src.culture.bank_sqlstr import (
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
    get_create_river_circle_table_sqlstr,
    get_select_river_circle_table_sqlstr,
    # get_delete_river_circle_sqlstr,
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


def test_get_create_river_circle_table_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_create_river_circle_table_sqlstr()

    # THEN
    example_sqlstr = """CREATE TABLE IF NOT EXISTS river_circle (
  currency_healer VARCHAR(255) NOT NULL
, currency_start FLOAT NOT NULL
, currency_close FLOAT NOT NULL
, circle_num INT NOT NULL
, FOREIGN KEY(currency_healer) REFERENCES agendaunit(healer)
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_select_river_circle_table_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    bob_text = "Bob"
    generated_sqlstr = get_select_river_circle_table_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
SELECT 
  currency_healer VARCHAR(255) NOT NULL
, currency_start FLOAT NOT NULL
, currency_close FLOAT NOT NULL
, circle_num INT NOT NULL
FROM river_circle
WHERE currency_healer = '{bob_text}'
)
;
"""
    assert generated_sqlstr == example_sqlstr
