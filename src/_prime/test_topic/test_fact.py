from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
)
from src._prime.topic import FactUnit, factunit_shop
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
    assert beef_factunit._topic_affect_ratio is None
    assert beef_factunit._topic_love_ratio is None


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
    assert beef_factunit._topic_affect_ratio is None
    assert beef_factunit._topic_love_ratio is None


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
    assert cook_factunit._topic_affect_ratio is None
    assert cook_factunit._topic_love_ratio is None


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


def test_FactUnit_set_topic_affect_ratio_CorrectSetsAttrs_good():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    good_affect = 7
    beef_factunit = factunit_shop(road=gas_road, affect=good_affect)
    assert beef_factunit._topic_affect_ratio is None

    # WHEN
    sum_good_affect = 28
    sum_bad_affect = 77
    beef_factunit.set_topic_affect_ratio(sum_good_affect, sum_bad_affect)

    # THEN
    assert beef_factunit._topic_affect_ratio == good_affect / sum_good_affect
    assert beef_factunit._topic_affect_ratio == 0.25


def test_FactUnit_set_topic_affect_ratio_CorrectSetsAttrs_bad():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    bad_affect = -8
    beef_factunit = factunit_shop(road=gas_road, affect=bad_affect)
    assert beef_factunit._topic_affect_ratio is None

    # WHEN
    sum_good_affect = 2
    sum_bad_affect = 10
    beef_factunit.set_topic_affect_ratio(sum_good_affect, sum_bad_affect)

    # THEN
    assert beef_factunit._topic_affect_ratio == -0.80
    assert beef_factunit._topic_affect_ratio == bad_affect / sum_bad_affect


def test_FactUnit_set_topic_love_ratio_CorrectSetsAttrWhen_in_tribe():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    in_tribe_love = 7
    beef_factunit = factunit_shop(gas_road, 3, love=in_tribe_love)
    assert beef_factunit._topic_love_ratio is None

    # WHEN
    sum_in_tribe_love = 28
    sum_out_tribe_love = None
    beef_factunit.set_topic_love_ratio(sum_in_tribe_love, sum_out_tribe_love)

    # THEN
    assert beef_factunit._topic_love_ratio == in_tribe_love / sum_in_tribe_love
    assert beef_factunit._topic_love_ratio == 0.25


def test_FactUnit_set_topic_love_ratio_CorrectSetsAttrWhen_out_tribe():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    out_tribe_love = -8
    beef_factunit = factunit_shop(gas_road, 3, love=out_tribe_love)
    assert beef_factunit._topic_love_ratio is None

    # WHEN
    sum_good_love = 2
    sum_out_tribe_love = 10
    beef_factunit.set_topic_love_ratio(sum_good_love, sum_out_tribe_love)

    # THEN
    assert beef_factunit._topic_love_ratio == -0.80
    assert beef_factunit._topic_love_ratio == out_tribe_love / sum_out_tribe_love


def test_FactUnit_set_topic_love_ratio_CorrectSetsAttrsWhen_zero():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    no_tribe_love = 0
    beef_factunit = factunit_shop(gas_road, 3, love=no_tribe_love)
    assert beef_factunit._topic_love_ratio is None

    # WHEN
    beef_factunit.set_topic_love_ratio(None, None)

    # THEN
    assert beef_factunit._topic_love_ratio == 0
