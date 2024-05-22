from src._road.road import create_road
from src.agenda.atom import agendaatom_shop, atom_insert, atom_hx_table_name
from src.world.journal_sqlstr import (
    get_atom_book_link_table_create_sqlstr,
    get_atom_hx_table_create_sqlstr,
    get_atom_hx_table_insert_sqlstr,
    get_atom_mstr_table_create_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_book_gift_link_table_create_sqlstr,
    get_book_table_create_sqlstr,
    get_gift_table_create_sqlstr,
    get_gift_person_link_table_create_sqlstr,
    get_person_mstr_table_create_sqlstr,
    get_road_ref_table_create_sqlstr,
    get_road_ref_table_single_insert_sqlstr,
    get_road_ref_table_row_id_select_sqlstr,
)
from src._instrument.sqlite import sqlite_text


def test_get_book_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS book_mstr (
  author_person_id VARCHAR(255) NOT NULL
, author_book_number INT NOT NULL
, UNIQUE(author_person_id, author_book_number)
)
;"""
    assert example_sqlstr == get_book_table_create_sqlstr()


def test_get_atom_book_link_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE atom_book_link
(
  atom_rowid INT NOT NULL
, book_rowid INT NOT NULL
, UNIQUE(atom_rowid, book_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (atom_rowid) REFERENCES atom_mstr (rowid)
, CONSTRAINT book_fk FOREIGN KEY (book_rowid) REFERENCES book_mstr (rowid)
)
;"""
    assert example_sqlstr == get_atom_book_link_table_create_sqlstr()


def test_get_gift_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS gift_mstr (
  author_person_id VARCHAR(255) NOT NULL
, author_gift_number INT NOT NULL
, UNIQUE(author_person_id, author_gift_number)
)
;"""
    assert example_sqlstr == get_gift_table_create_sqlstr()


def test_get_book_gift_link_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE book_gift_link
(
  book_rowid INT NOT NULL
, gift_rowid INT NOT NULL
, UNIQUE(book_rowid, gift_rowid)
, CONSTRAINT atom_fk FOREIGN KEY (book_rowid) REFERENCES book_mstr (rowid)
, CONSTRAINT book_fk FOREIGN KEY (gift_rowid) REFERENCES gift_mstr (rowid)
)
;"""
    assert example_sqlstr == get_book_gift_link_table_create_sqlstr()


def test_get_gift_person_link_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE gift_person_link
(
  gift_rowid INT NOT NULL
, person_rowid INT NOT NULL
, UNIQUE(gift_rowid, person_rowid)
, CONSTRAINT book_fk FOREIGN KEY (gift_rowid) REFERENCES gift_mstr (rowid)
, CONSTRAINT person_fk FOREIGN KEY (person_rowid) REFERENCES person (rowid)
)
;"""
    assert example_sqlstr == get_gift_person_link_table_create_sqlstr()


def test_get_person_mstr_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE person_mstr
(
  person_id VARCHAR(255) NOT NULL
, UNIQUE(person_id)
)
;"""
    assert example_sqlstr == get_person_mstr_table_create_sqlstr()


def test_get_road_ref_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS road_ref (
  road VARCHAR(255) NOT NULL
, delimiter VARCHAR(255) NOT NULL
, UNIQUE(road, delimiter)
)
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
    begin_sqlstr = """
CREATE TABLE IF NOT EXISTS atom_hx (
  person_id VARCHAR(255) NOT NULL"""
    end_sqlstr = """)
;"""

    assert generated_sqlstr.find(begin_sqlstr) == 0
    assert generated_sqlstr.find(end_sqlstr) > 0
    assert generated_sqlstr.find(end_sqlstr) == 6169
    example_idea_reasonunit_text = (
        "idea_reasonunit_UPDATE_suff_idea_active INTEGER NULL"
    )
    assert generated_sqlstr.find(example_idea_reasonunit_text) > 0
    assert generated_sqlstr.find(example_idea_reasonunit_text) == 3591


def test_get_atom_hx_table_insert_sqlstr_ReturnsCorrectStr():
    # WHEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    knee_open = 7

    # WHEN
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    update_disc_agendaatom = agendaatom_shop(x_category, atom_insert())
    update_disc_agendaatom.set_required_arg(road_text, ball_road)
    update_disc_agendaatom.set_required_arg(base_text, knee_road)
    update_disc_agendaatom.set_optional_arg(open_text, knee_open)

    # THEN
    example_sqlstr = f"""INSERT INTO {atom_hx_table_name()} (
  {x_category}_{atom_insert()}_{road_text}
, {x_category}_{atom_insert()}_{base_text}
, {x_category}_{atom_insert()}_{open_text}
)
VALUES (
  '{ball_road}'
, '{knee_road}'
, {knee_open}
)
;"""
    assert get_atom_hx_table_insert_sqlstr(update_disc_agendaatom) == example_sqlstr


def test_get_atom_mstr_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_atom_mstr_table_create_sqlstr()

    # THEN
    begin_sqlstr = """
CREATE TABLE IF NOT EXISTS atom_mstr (
  person_id VARCHAR(255) NOT NULL
, atom_hx_row_id INT NOT NULL"""
    end_sqlstr = """)
;"""
    assert generated_sqlstr.find(begin_sqlstr) == 0
    assert generated_sqlstr.find(end_sqlstr) > 0
    assert generated_sqlstr.find(end_sqlstr) == 6201
    example_idea_reasonunit_text = (
        "idea_reasonunit_UPDATE_suff_idea_active INTEGER NULL"
    )
    assert generated_sqlstr.find(example_idea_reasonunit_text) > 0
    assert generated_sqlstr.find(example_idea_reasonunit_text) == 3623


def test_get_create_table_if_not_exist_sqlstrs_HasCorrectNumberOfNumber():
    # GIVEN / WHEN / THEN
    assert len(get_create_table_if_not_exist_sqlstrs()) == 9

    # SELECT name FROM my_db.sqlite_master WHERE type='table
