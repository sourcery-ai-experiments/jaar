from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
)
from src._prime.belief import OpinionUnit, opinionunit_shop
from pytest import raises as pytest_raises


def test_OpinionUnit_exists():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    beef_opinionunit = OpinionUnit(road=gas_road)

    # THEN
    assert beef_opinionunit != None
    assert beef_opinionunit.road == gas_road
    assert beef_opinionunit.affect is None
    assert beef_opinionunit.love is None


def test_OpinionUnit_set_affect_CorrectSetsAttrs():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    beef_opinionunit = OpinionUnit(road=gas_road)
    assert beef_opinionunit.affect is None

    # WHEN
    beef_affect = -3
    beef_opinionunit.set_affect(beef_affect)

    # THEN
    assert beef_opinionunit.affect == beef_affect


def test_OpinionUnit_set_love_CorrectSetsAttrs():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    beef_opinionunit = OpinionUnit(road=gas_road)
    assert beef_opinionunit.love is None

    # WHEN
    beef_love = -7
    beef_opinionunit.set_love(beef_love)

    # THEN
    assert beef_opinionunit.love == beef_love


def test_opinionunit_shop_CorrectlyReturnsObj():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    cook_opinionunit = opinionunit_shop(road=gas_road, affect=7, love=11)

    # THEN
    assert cook_opinionunit.road == gas_road
    assert cook_opinionunit.affect == 7
    assert cook_opinionunit.love == 11


def test_opinionunit_shop_Sets_love_NoneIf():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    cook_opinionunit = opinionunit_shop(road=gas_road, affect=7)

    # THEN
    assert cook_opinionunit.road == gas_road
    assert cook_opinionunit.affect == 7
    assert cook_opinionunit.love == 0


def test_OpinionUnit_set_affect_CorrectlyRaisesNoneZeroAffectException():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cheap_road = create_road(cook_road, "cheap food")
    cheap_opinionunit = opinionunit_shop(cheap_road, affect=-5)

    # WHEN
    zero_int = 0
    with pytest_raises(Exception) as excinfo:
        cheap_opinionunit.set_affect(x_affect=zero_int)
    assert (
        str(excinfo.value)
        == f"set_affect affect parameter {zero_int} must be Non-zero number"
    )
