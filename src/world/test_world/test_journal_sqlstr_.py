from src.world.journal_sqlstr import (
    get_deal_hx_table_create_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
)
from src.instrument.sqlite import sqlite_text


def test_get_deal_hx_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_deal_hx_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS deal_hx (
, person_id VARCHAR(255) NOT NULL"""

    assert generated_sqlstr.find(example_sqlstr) == 0
    example_idea_reasonunit_text = (
        "idea_reasonunit_UPDATE_suff_idea_active INTEGER NULL"
    )
    assert generated_sqlstr.find(example_idea_reasonunit_text) > 0
    assert generated_sqlstr.find(example_idea_reasonunit_text) == 2944


def test_get_create_table_if_not_exist_sqlstrs_HasCorrectNumberOfNumber():
    # GIVEN / WHEN / THEN
    assert len(get_create_table_if_not_exist_sqlstrs()) == 2

    # SELECT name FROM my_db.sqlite_master WHERE type='table
