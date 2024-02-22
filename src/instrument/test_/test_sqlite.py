from src.instrument.sqlite import (
    sqlite_bool,
    sqlite_text,
    sqlite_null,
    create_insert_sqlstr,
)
from pytest import raises as pytest_raises


def test_sqlite_bool_ReturnsCorrectObj():
    assert sqlite_bool(int_x=0) == False
    assert sqlite_bool(int_x=1)
    assert sqlite_bool(int_x=None) == "NULL"


def test_sqlite_text_ReturnsCorrectObj():
    assert sqlite_text(True) == "TRUE"
    assert sqlite_text(False) == "FALSE"
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sqlite_text("Bob")
    assert str(excinfo.value) == "function requires boolean"


def test_sqlite_null_ReturnsCorrectObj():
    assert sqlite_null(True) == True
    assert sqlite_null("yea") == "yea"
    assert sqlite_null(None) == "NULL"


def test_sqlite_create_insert_sqlstr_ReturnsCorrectObj():
    # GIVEN
    x_table = "kubo_trains"
    person_id_text = "person_id"
    train_id_text = "train_id"
    train_color_text = "train_color"
    x_columns = [person_id_text, train_id_text, train_color_text]
    person_id_value = 47
    train_id_value = "TR34"
    train_color_value = "red"
    x_values = [person_id_value, train_id_value, train_color_value]

    # WHEN
    gen_sqlstr = create_insert_sqlstr(x_table, x_columns, x_values)

    # THEN
    example_sqlstr = f"""INSERT INTO {x_table} (
  {person_id_text}
, {train_id_text}
, {train_color_text}
)
VALUES (
  {person_id_value}
, '{train_id_value}'
, '{train_color_value}'
)
;"""
    print(example_sqlstr)
    assert example_sqlstr == gen_sqlstr
