from src.agenda.agenda import agendaunit_shop
from src.culture.bank_sqlstr import (
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
    # get_create_river_reach_sqlstr,
    # get_select_river_reach_sqlstr,
    # get_delete_river_reach_sqlstr,
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
    example_sqlstr = f"""
UPDATE agendaunit
SET rational = {sqlite_text(bob_rational)}
WHERE healer = '{bob_healer}'
;
"""
    assert gen_sqlstr == example_sqlstr


def test_get_agendaunits_select_sqlstr_ReturnsCorrectObj():
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


# def test_create_river_reach_sqlstr_ReturnsCorrectObj():
#     # GIVEN / WHEN
#     generated_sqlstr = get_create_river_reach_sqlstr()

#     # THEN
#     example_sqlstr = """
# CREATE TABLE IF NOT EXISTS river_reach (
#   currency_healer VARCHAR(255) NOT NULL
# , src_healer VARCHAR(255) NOT NULL
# , dst_healer VARCHAR(255) NOT NULL
# , reach_num INT NOT NULL
# , curr_start FLOAT NOT NULL
# , curr_close FLOAT NOT NULL
# , FOREIGN KEY(currency_healer) REFERENCES agendaunit(healer)
# , FOREIGN KEY(src_healer) REFERENCES agendaunit(healer)
# , FOREIGN KEY(dst_healer) REFERENCES agendaunit(healer)
# )
# ;
# """
#     assert generated_sqlstr == example_sqlstr
