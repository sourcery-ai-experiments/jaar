from src._road.jaar_config import (
    duty_str,
    work_str,
    get_rootpart_of_econ_dir,
    treasury_file_name,
    max_tree_traverse_default,
)


def test_duty_str():
    assert duty_str() == "duty"


def test_work_str():
    assert work_str() == "work"


def test_get_rootpart_of_econ_dir_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert get_rootpart_of_econ_dir() == "idearoot"


def test_treasury_file_name_ReturnsObj() -> str:
    assert treasury_file_name() == "treasury.db"


def test_max_tree_traverse_default_ReturnsObj() -> str:
    assert max_tree_traverse_default() == 20
