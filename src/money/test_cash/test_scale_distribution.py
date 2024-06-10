from src.money.cash import distribute_scale
from pytest import raises as pytest_raises


def test_distribute_scale_v01():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
    }
    print(f"{partys=}")
    scale_number = 100
    grain_unit = 0.5

    distributed_partys = distribute_scale(partys, scale_number, grain_unit)
    print(distributed_partys)
    assert distributed_partys.get("obj1").get("distributed_value") == 16.5
    assert distributed_partys.get("obj2").get("distributed_value") == 33.5
    assert distributed_partys.get("obj3").get("distributed_value") == 50.0
    assert sum(obj["distributed_value"] for obj in partys.values()) == scale_number


def test_distribute_scale_v02():
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
        distribute_scale(partys, scale_number, grain_unit)
    assert (
        str(excinfo.value)
        == f"The scale number '{scale_number}' must be a multiple of the grain unit '{grain_unit}'."
    )


def test_distribute_scale_v03():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
    }
    print(f"{partys=}")
    scale_number = 100.5
    grain_unit = 0.5

    distributed_partys = distribute_scale(partys, scale_number, grain_unit)
    print(distributed_partys)
    assert distributed_partys.get("obj1").get("distributed_value") == 17
    assert distributed_partys.get("obj2").get("distributed_value") == 33.5
    assert distributed_partys.get("obj3").get("distributed_value") == 50.0
    assert sum(obj["distributed_value"] for obj in partys.values()) == scale_number


def test_distribute_scale_v03():
    # Example usage:
    partys = {
        "obj1": {"creditor_weight": 1.0},
        "obj2": {"creditor_weight": 2.0},
        "obj3": {"creditor_weight": 3.0},
    }
    print(f"{partys=}")
    scale_number = 101
    grain_unit = 0.5

    distributed_partys = distribute_scale(partys, scale_number, grain_unit)
    print(distributed_partys)
    assert distributed_partys.get("obj1").get("distributed_value") == 17
    assert distributed_partys.get("obj2").get("distributed_value") == 33.5
    assert distributed_partys.get("obj3").get("distributed_value") == 50.5
    assert sum(obj["distributed_value"] for obj in partys.values()) == scale_number


def test_distribute_scale_v04():
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

    distributed_partys = distribute_scale(partys, scale_number, grain_unit)
    print(distributed_partys)
    assert distributed_partys.get("obj1").get("distributed_value") == 0.5
    assert distributed_partys.get("obj2").get("distributed_value") == 1
    assert distributed_partys.get("obj3").get("distributed_value") == 2
    assert distributed_partys.get("obj4").get("distributed_value") == 4.5
    assert distributed_partys.get("obj5").get("distributed_value") == 8
    assert distributed_partys.get("obj6").get("distributed_value") == 60
    assert distributed_partys.get("obj7").get("distributed_value") == 25
    assert sum(obj["distributed_value"] for obj in partys.values()) == scale_number


def test_distribute_scale_v05():
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

    distributed_partys = distribute_scale(partys, scale_number, grain_unit)
    print(distributed_partys)
    assert distributed_partys.get("obj1").get("distributed_value") == 0
    assert distributed_partys.get("obj2").get("distributed_value") == 0
    assert distributed_partys.get("obj3").get("distributed_value") == 0
    assert distributed_partys.get("obj4").get("distributed_value") == 0
    assert distributed_partys.get("obj5").get("distributed_value") == 0
    assert distributed_partys.get("obj6").get("distributed_value") == 0
    assert distributed_partys.get("obj7").get("distributed_value") == 101
    assert sum(obj["distributed_value"] for obj in partys.values()) == scale_number


def test_distribute_scale_v06():
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

    distributed_partys = distribute_scale(partys, scale_number, grain_unit)
    print(distributed_partys)
    assert distributed_partys.get("obj1").get("distributed_value") == 0
    assert distributed_partys.get("obj2").get("distributed_value") == 0
    assert distributed_partys.get("obj3").get("distributed_value") == 0
    assert distributed_partys.get("obj4").get("distributed_value") == 0
    assert distributed_partys.get("obj5").get("distributed_value") == 0
    assert distributed_partys.get("obj6").get("distributed_value") == 0
    assert distributed_partys.get("obj7").get("distributed_value") == 1
    assert sum(obj["distributed_value"] for obj in partys.values()) == scale_number
