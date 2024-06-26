from src._road.finance import allot_scale
from pytest import raises as pytest_raises


def test_allot_scale_v01():
    # GIVEN
    credorledger = {"obj1": 1.0, "obj2": 2.0, "obj3": 3.0}
    print(f"{credorledger=}")
    scale_number = 100
    grain_unit = 0.5

    # WHEN
    alloted_chars = allot_scale(credorledger, scale_number, grain_unit)

    # THEN
    print(alloted_chars)
    assert alloted_chars.get("obj1") == 16.5
    assert alloted_chars.get("obj2") == 33.5
    assert alloted_chars.get("obj3") == 50.0
    assert sum(alloted_chars.values()) == scale_number


def test_allot_scale_v02():
    # Example usage:
    chars = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
    }
    print(f"{chars=}")
    scale_number = 100
    grain_unit = 0.3

    # WHEN / THEN
    swim_text = "swim"
    with pytest_raises(Exception) as excinfo:
        allot_scale(chars, scale_number, grain_unit)
    assert (
        str(excinfo.value)
        == f"The scale number '{scale_number}' must be a multiple of the grain unit '{grain_unit}'."
    )


def test_allot_scale_v03():
    # Example usage:
    chars = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
    }
    print(f"{chars=}")
    scale_number = 100.5
    grain_unit = 0.5

    alloted_chars = allot_scale(chars, scale_number, grain_unit)
    print(alloted_chars)
    assert alloted_chars.get("obj1") == 17
    assert alloted_chars.get("obj2") == 33.5
    assert alloted_chars.get("obj3") == 50.0
    assert sum(alloted_chars.values()) == scale_number


def test_allot_scale_v04():
    # Example usage:
    chars = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
    }
    print(f"{chars=}")
    scale_number = 101
    grain_unit = 0.5

    alloted_chars = allot_scale(chars, scale_number, grain_unit)
    print(alloted_chars)
    assert alloted_chars.get("obj1") == 17
    assert alloted_chars.get("obj2") == 33.5
    assert alloted_chars.get("obj3") == 50.5
    assert sum(alloted_chars.values()) == scale_number


def test_allot_scale_v05():
    # Example usage:
    chars = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
        "obj4": 7.0,
        "obj5": 13.0,
        "obj6": 99.0,
        "obj7": 41.0,
    }
    print(f"{chars=}")
    scale_number = 101
    grain_unit = 0.5

    alloted_chars = allot_scale(chars, scale_number, grain_unit)
    print(alloted_chars)
    assert alloted_chars.get("obj1") == 0.5
    assert alloted_chars.get("obj2") == 1
    assert alloted_chars.get("obj3") == 2
    assert alloted_chars.get("obj4") == 4.5
    assert alloted_chars.get("obj5") == 8
    assert alloted_chars.get("obj6") == 60
    assert alloted_chars.get("obj7") == 25
    assert sum(alloted_chars.values()) == scale_number


def test_allot_scale_v06():
    # Example usage:
    chars = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
        "obj4": 7.0,
        "obj5": 13.0,
        "obj6": 99.0,
        "obj7": 100000000.0,
    }
    print(f"{chars=}")
    scale_number = 101
    grain_unit = 0.5

    alloted_chars = allot_scale(chars, scale_number, grain_unit)
    print(alloted_chars)
    assert alloted_chars.get("obj1") == 0
    assert alloted_chars.get("obj2") == 0
    assert alloted_chars.get("obj3") == 0
    assert alloted_chars.get("obj4") == 0
    assert alloted_chars.get("obj5") == 0
    assert alloted_chars.get("obj6") == 0
    assert alloted_chars.get("obj7") == 101
    assert sum(alloted_chars.values()) == scale_number


def test_allot_scale_v07():
    # Example usage:
    chars = {
        "obj1": 1.0,
        "obj2": 2.0,
        "obj3": 3.0,
        "obj4": 7.0,
        "obj5": 13.0,
        "obj6": 99.0,
        "obj7": 100000000.0,
    }
    print(f"{chars=}")
    scale_number = 1
    grain_unit = 0.5

    alloted_chars = allot_scale(chars, scale_number, grain_unit)
    print(alloted_chars)
    assert alloted_chars.get("obj1") == 0
    assert alloted_chars.get("obj2") == 0
    assert alloted_chars.get("obj3") == 0
    assert alloted_chars.get("obj4") == 0
    assert alloted_chars.get("obj5") == 0
    assert alloted_chars.get("obj6") == 0
    assert alloted_chars.get("obj7") == 1
    assert sum(alloted_chars.values()) == scale_number
