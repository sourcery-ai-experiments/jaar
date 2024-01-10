from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
)
from src._prime.issue import FactUnit, factunit_shop
from pytest import raises as pytest_raises


def test_FactUnit_exists():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    beef_factunit = FactUnit(road=gas_road)

    # THEN
    assert beef_factunit != None
    assert beef_factunit.road == gas_road
    assert beef_factunit.affect is None
    assert beef_factunit.love is None


def test_FactUnit_set_affect_CorrectSetsAttrs():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    beef_factunit = FactUnit(road=gas_road)
    assert beef_factunit.affect is None

    # WHEN
    beef_affect = -3
    beef_factunit.set_affect(beef_affect)

    # THEN
    assert beef_factunit.affect == beef_affect


def test_FactUnit_set_love_CorrectSetsAttrs():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    beef_factunit = FactUnit(road=gas_road)
    assert beef_factunit.love is None

    # WHEN
    beef_love = -7
    beef_factunit.set_love(beef_love)

    # THEN
    assert beef_factunit.love == beef_love


def test_factunit_shop_CorrectlyReturnsObj():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    cook_factunit = factunit_shop(road=gas_road, affect=7, love=11)

    # THEN
    assert cook_factunit.road == gas_road
    assert cook_factunit.affect == 7
    assert cook_factunit.love == 11


def test_factunit_shop_Sets_love_NoneIf():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    cook_factunit = factunit_shop(road=gas_road, affect=7)

    # THEN
    assert cook_factunit.road == gas_road
    assert cook_factunit.affect == 7
    assert cook_factunit.love == 0


def test_FactUnit_set_affect_CorrectlyRaisesNoneZeroAffectException():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cheap_road = create_road(cook_road, "cheap food")
    cheap_factunit = factunit_shop(cheap_road, affect=-5)

    # WHEN
    zero_int = 0
    with pytest_raises(Exception) as excinfo:
        cheap_factunit.set_affect(x_affect=zero_int)
    assert (
        str(excinfo.value)
        == f"set_affect affect parameter {zero_int} must be Non-zero number"
    )
