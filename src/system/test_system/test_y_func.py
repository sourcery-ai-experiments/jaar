from src.system.y_func import sqlite_bool, sqlite_text, sqlite_null
from pytest import raises as pytest_raises


def test_sqlite_bool_WorksCorrectly():
    assert sqlite_bool(int_x=0) == False
    assert sqlite_bool(int_x=1)
    assert sqlite_bool(int_x=None) == "NULL"


def test_sqlite_text_WorksCorrectly():
    assert sqlite_text(True) == "TRUE"
    assert sqlite_text(False) == "FALSE"
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sqlite_text("bob")
    assert str(excinfo.value) == "function requires boolean"


def test_sqlite_null_WorksCorrectly():
    assert sqlite_null(True) == True
    assert sqlite_null("yea") == "yea"
    assert sqlite_null(None) == "NULL"
