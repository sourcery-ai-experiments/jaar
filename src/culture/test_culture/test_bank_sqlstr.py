from src.culture.bank_sqlstr import (
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
)


def test_get_agendaunit_update_sqlstr_ReturnsCorrectObj():
    # GIVEN
    bob_healer = "Bob"
    voice_rank = 5

    # WHEN
    gen_sqlstr = get_agendaunit_update_sqlstr(healer=bob_healer, voice_rank=voice_rank)

    # THEN
    ex_sqlstr = f"""
UPDATE agendaunit
SET voice_rank = {voice_rank}
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
, voice_rank
FROM agendaunit
;
"""
    assert gen_sqlstr == ex_sqlstr
