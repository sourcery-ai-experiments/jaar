from src._road.jaar_config import (
    same_str,
    live_str,
    get_rootpart_of_econ_dir,
    treasury_file_name,
    max_tree_traverse_default,
    default_river_blocks_count,
)


def test_same_str():
    assert same_str() == "same"


def test_live_str():
    assert live_str() == "live"


def test_get_rootpart_of_econ_dir_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert get_rootpart_of_econ_dir() == "idearoot"


def test_treasury_file_name_ReturnsObj() -> str:
    assert treasury_file_name() == "treasury.db"


def test_max_tree_traverse_default_ReturnsObj() -> str:
    assert max_tree_traverse_default() == 20


def test_default_river_blocks_count_ReturnsObj() -> str:
    assert default_river_blocks_count() == 40
