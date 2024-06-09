from src._road.road import create_road
from src.atom.quark import quarkunit_shop, quark_insert, quark_hx_table_name
from src.real.journal_sqlstr import (
    get_quark_nuc_link_table_create_sqlstr,
    get_quark_hx_table_create_sqlstr,
    get_quark_hx_table_insert_sqlstr,
    get_quark_mstr_table_create_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_nuc_atom_link_table_create_sqlstr,
    get_nuc_table_create_sqlstr,
    get_atom_table_create_sqlstr,
    get_atom_person_link_table_create_sqlstr,
    get_person_mstr_table_create_sqlstr,
    get_road_ref_table_create_sqlstr,
    get_road_ref_table_single_insert_sqlstr,
    get_road_ref_table_row_id_select_sqlstr,
)


def test_get_nuc_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS nuc_mstr (
  author_person_id VARCHAR(255) NOT NULL
, author_nuc_number INT NOT NULL
, UNIQUE(author_person_id, author_nuc_number)
)
;"""
    assert example_sqlstr == get_nuc_table_create_sqlstr()


def test_get_quark_nuc_link_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE quark_nuc_link
(
  quark_rowid INT NOT NULL
, nuc_rowid INT NOT NULL
, UNIQUE(quark_rowid, nuc_rowid)
, CONSTRAINT quark_fk FOREIGN KEY (quark_rowid) REFERENCES quark_mstr (rowid)
, CONSTRAINT nuc_fk FOREIGN KEY (nuc_rowid) REFERENCES nuc_mstr (rowid)
)
;"""
    assert example_sqlstr == get_quark_nuc_link_table_create_sqlstr()


def test_get_atom_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS atom_mstr (
  author_person_id VARCHAR(255) NOT NULL
, author_atom_number INT NOT NULL
, UNIQUE(author_person_id, author_atom_number)
)
;"""
    assert example_sqlstr == get_atom_table_create_sqlstr()


def test_get_nuc_atom_link_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE nuc_atom_link
(
  nuc_rowid INT NOT NULL
, atom_rowid INT NOT NULL
, UNIQUE(nuc_rowid, atom_rowid)
, CONSTRAINT quark_fk FOREIGN KEY (nuc_rowid) REFERENCES nuc_mstr (rowid)
, CONSTRAINT nuc_fk FOREIGN KEY (atom_rowid) REFERENCES atom_mstr (rowid)
)
;"""
    assert example_sqlstr == get_nuc_atom_link_table_create_sqlstr()


def test_get_atom_person_link_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN / THEN
    example_sqlstr = """
CREATE TABLE atom_person_link
(
  atom_rowid INT NOT NULL
, person_rowid INT NOT NULL
, UNIQUE(atom_rowid, person_rowid)
, CONSTRAINT nuc_fk FOREIGN KEY (atom_rowid) REFERENCES atom_mstr (rowid)
, CONSTRAINT person_fk FOREIGN KEY (person_rowid) REFERENCES person (rowid)
)
;"""
    assert example_sqlstr == get_atom_person_link_table_create_sqlstr()


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


def test_get_quark_hx_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_quark_hx_table_create_sqlstr()

    # THEN
    begin_sqlstr = """
CREATE TABLE IF NOT EXISTS quark_hx (
  person_id VARCHAR(255) NOT NULL"""
    end_sqlstr = """)
;"""

    assert generated_sqlstr.find(begin_sqlstr) == 0
    assert generated_sqlstr.find(end_sqlstr) > 0
    assert generated_sqlstr.find(end_sqlstr) == 6171
    example_idea_reasonunit_text = (
        "idea_reasonunit_UPDATE_suff_idea_active INTEGER NULL"
    )
    assert generated_sqlstr.find(example_idea_reasonunit_text) > 0
    assert generated_sqlstr.find(example_idea_reasonunit_text) == 3592


def test_get_quark_hx_table_insert_sqlstr_ReturnsCorrectStr():
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
    update_disc_quarkunit = quarkunit_shop(x_category, quark_insert())
    update_disc_quarkunit.set_required_arg(road_text, ball_road)
    update_disc_quarkunit.set_required_arg(base_text, knee_road)
    update_disc_quarkunit.set_optional_arg(open_text, knee_open)

    # THEN
    example_sqlstr = f"""INSERT INTO {quark_hx_table_name()} (
  {x_category}_{quark_insert()}_{road_text}
, {x_category}_{quark_insert()}_{base_text}
, {x_category}_{quark_insert()}_{open_text}
)
VALUES (
  '{ball_road}'
, '{knee_road}'
, {knee_open}
)
;"""
    assert get_quark_hx_table_insert_sqlstr(update_disc_quarkunit) == example_sqlstr


def test_get_quark_mstr_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_quark_mstr_table_create_sqlstr()

    # THEN
    begin_sqlstr = """
CREATE TABLE IF NOT EXISTS quark_mstr (
  person_id VARCHAR(255) NOT NULL
, quark_hx_row_id INT NOT NULL"""
    end_sqlstr = """)
;"""
    assert generated_sqlstr.find(begin_sqlstr) == 0
    assert generated_sqlstr.find(end_sqlstr) > 0
    assert generated_sqlstr.find(end_sqlstr) == 6204
    example_idea_reasonunit_text = (
        "idea_reasonunit_UPDATE_suff_idea_active INTEGER NULL"
    )
    assert generated_sqlstr.find(example_idea_reasonunit_text) > 0
    assert generated_sqlstr.find(example_idea_reasonunit_text) == 3625


def test_get_create_table_if_not_exist_sqlstrs_HasCorrectNumberOfNumber():
    # GIVEN / WHEN / THEN
    assert len(get_create_table_if_not_exist_sqlstrs()) == 9

    # SELECT name FROM my_db.sqlite_master WHERE type='table
