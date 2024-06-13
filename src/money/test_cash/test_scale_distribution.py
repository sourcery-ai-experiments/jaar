from src.money.cash import allot_scale
from pytest import raises as pytest_raises


def test_allot_scale_v01():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
    }
    print(f"{partys=}")
    scale_number = 100
    grain_unit = 0.5

    alloted_partys = allot_scale(partys, scale_number, grain_unit)
    print(alloted_partys)
    assert alloted_partys.get("obj1").get("alloted_value") == 16.5
    assert alloted_partys.get("obj2").get("alloted_value") == 33.5
    assert alloted_partys.get("obj3").get("alloted_value") == 50.0
    assert sum(obj["alloted_value"] for obj in partys.values()) == scale_number


def test_allot_scale_v02():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
    }
    print(f"{partys=}")
    scale_number = 100
    grain_unit = 0.3

    # WHEN / THEN
    swim_text = "swim"
    with pytest_raises(Exception) as excinfo:
        allot_scale(partys, scale_number, grain_unit)
    assert (
        str(excinfo.value)
        == f"The scale number '{scale_number}' must be a multiple of the grain unit '{grain_unit}'."
    )


def test_allot_scale_v03():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
    }
    print(f"{partys=}")
    scale_number = 100.5
    grain_unit = 0.5

    alloted_partys = allot_scale(partys, scale_number, grain_unit)
    print(alloted_partys)
    assert alloted_partys.get("obj1").get("alloted_value") == 17
    assert alloted_partys.get("obj2").get("alloted_value") == 33.5
    assert alloted_partys.get("obj3").get("alloted_value") == 50.0
    assert sum(obj["alloted_value"] for obj in partys.values()) == scale_number


def test_allot_scale_v03():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
    }
    print(f"{partys=}")
    scale_number = 101
    grain_unit = 0.5

    alloted_partys = allot_scale(partys, scale_number, grain_unit)
    print(alloted_partys)
    assert alloted_partys.get("obj1").get("alloted_value") == 17
    assert alloted_partys.get("obj2").get("alloted_value") == 33.5
    assert alloted_partys.get("obj3").get("alloted_value") == 50.5
    assert sum(obj["alloted_value"] for obj in partys.values()) == scale_number


def test_allot_scale_v04():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
        "obj4": {"creditor_weight": 7.0},
        "obj5": {"creditor_weight": 13.0},
        "obj6": {"creditor_weight": 99.0},
        "obj7": {"creditor_weight": 41.0},
    }
    print(f"{partys=}")
    scale_number = 101
    grain_unit = 0.5

    alloted_partys = allot_scale(partys, scale_number, grain_unit)
    print(alloted_partys)
    assert alloted_partys.get("obj1").get("alloted_value") == 0.5
    assert alloted_partys.get("obj2").get("alloted_value") == 1
    assert alloted_partys.get("obj3").get("alloted_value") == 2
    assert alloted_partys.get("obj4").get("alloted_value") == 4.5
    assert alloted_partys.get("obj5").get("alloted_value") == 8
    assert alloted_partys.get("obj6").get("alloted_value") == 60
    assert alloted_partys.get("obj7").get("alloted_value") == 25
    assert sum(obj["alloted_value"] for obj in partys.values()) == scale_number


def test_allot_scale_v05():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
        "obj4": {"creditor_weight": 7.0},
        "obj5": {"creditor_weight": 13.0},
        "obj6": {"creditor_weight": 99.0},
        "obj7": {"creditor_weight": 100000000.0},
    }
    print(f"{partys=}")
    scale_number = 101
    grain_unit = 0.5

    alloted_partys = allot_scale(partys, scale_number, grain_unit)
    print(alloted_partys)
    assert alloted_partys.get("obj1").get("alloted_value") == 0
    assert alloted_partys.get("obj2").get("alloted_value") == 0
    assert alloted_partys.get("obj3").get("alloted_value") == 0
    assert alloted_partys.get("obj4").get("alloted_value") == 0
    assert alloted_partys.get("obj5").get("alloted_value") == 0
    assert alloted_partys.get("obj6").get("alloted_value") == 0
    assert alloted_partys.get("obj7").get("alloted_value") == 101
    assert sum(obj["alloted_value"] for obj in partys.values()) == scale_number


def test_allot_scale_v06():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
        "obj4": {"creditor_weight": 7.0},
        "obj5": {"creditor_weight": 13.0},
        "obj6": {"creditor_weight": 99.0},
        "obj7": {"creditor_weight": 100000000.0},
    }
    print(f"{partys=}")
    scale_number = 1
    grain_unit = 0.5

    alloted_partys = allot_scale(partys, scale_number, grain_unit)
    print(alloted_partys)
    assert alloted_partys.get("obj1").get("alloted_value") == 0
    assert alloted_partys.get("obj2").get("alloted_value") == 0
    assert alloted_partys.get("obj3").get("alloted_value") == 0
    assert alloted_partys.get("obj4").get("alloted_value") == 0
    assert alloted_partys.get("obj5").get("alloted_value") == 0
    assert alloted_partys.get("obj6").get("alloted_value") == 0
    assert alloted_partys.get("obj7").get("alloted_value") == 1
    assert sum(obj["alloted_value"] for obj in partys.values()) == scale_number
