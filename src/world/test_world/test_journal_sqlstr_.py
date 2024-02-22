from src._road.road import create_road
from src.world.journal_sqlstr import (
    get_road_ref_table_create_sqlstr,
    get_road_ref_table_single_insert_sqlstr,
    get_road_ref_table_row_id_select_sqlstr,
    get_atom_hx_table_create_sqlstr,
    get_atom_hx_table_insert_sqlstr,
    get_atom_curr_table_create_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
)
from src.instrument.sqlite import sqlite_text


def test_get_road_ref_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS road_ref (
  road VARCHAR(MAX) NOT NULL
, delimiter VARCHAR(255) NOT NULL
, UNIQUE(road, delimiter)
;"""
    assert example_sqlstr == get_road_ref_table_create_sqlstr()


def test_get_road_ref_table_single_insert_sqlstr_ReturnsCorrectStr():
    # GIVEN
    music_text = "Music"
    slash_text = "/"
    texas_road = create_road(music_text, "texas", delimiter=slash_text)

    # WHEN
    generate_sqlstr = get_road_ref_table_single_insert_sqlstr(texas_road, slash_text)

    # THEN
    example_sqlstr = f"""
INSERT OR IGNORE INTO road_ref (road, delimiter) 
VALUES (
  '{texas_road}'
, '{slash_text}'
)
;"""
    assert example_sqlstr == generate_sqlstr


def test_get_road_ref_table_row_id_select_sqlstr_ReturnsCorrectStr():
    # GIVEN
    music_text = "Music"
    slash_text = "/"
    texas_road = create_road(music_text, "texas", delimiter=slash_text)

    # WHEN
    generate_sqlstr = get_road_ref_table_row_id_select_sqlstr(texas_road, slash_text)

    # THEN
    example_sqlstr = f"""
SELECT rowid FROM road_ref  
WHERE road = '{texas_road}' 
  AND delimiter = '{slash_text}'
)
;"""
    assert example_sqlstr == generate_sqlstr


def test_get_atom_hx_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_atom_hx_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS atom_hx (
, person_id VARCHAR(255) NOT NULL"""

    assert generated_sqlstr.find(example_sqlstr) == 0
    example_idea_reasonunit_text = (
        "idea_reasonunit_UPDATE_suff_idea_active INTEGER NULL"
    )
    assert generated_sqlstr.find(example_idea_reasonunit_text) > 0
    assert generated_sqlstr.find(example_idea_reasonunit_text) == 2944


def test_get_atom_hx_table_insert_sqlstr_ReturnsCorrectStr():
    # GIVEN
    yao_text = "Yao"

    # WHEN
    generated_sqlstr = get_atom_hx_table_insert_sqlstr()

    # THEN
    example_sqlstr = """
INSERT INTO atom_hx (person_id..."""

    assert generated_sqlstr.find(example_sqlstr) == 0


def test_get_atom_curr_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_atom_curr_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS atom_curr (
, person_id VARCHAR(255) NOT NULL
, atom_hx_row_id INT NOT NULL"""

    assert generated_sqlstr.find(example_sqlstr) == 0
    example_idea_reasonunit_text = (
        "idea_reasonunit_UPDATE_suff_idea_active INTEGER NULL"
    )
    assert generated_sqlstr.find(example_idea_reasonunit_text) > 0
    assert generated_sqlstr.find(example_idea_reasonunit_text) == 2976


def test_get_create_table_if_not_exist_sqlstrs_HasCorrectNumberOfNumber():
    # GIVEN / WHEN / THEN
    assert len(get_create_table_if_not_exist_sqlstrs()) == 3

    # SELECT name FROM my_db.sqlite_master WHERE type='table
