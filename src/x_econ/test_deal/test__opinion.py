from src._prime.road import (
    get_default_market_root_roadnode as root_label,
    create_road,
)
from src.x_econ.topic import OpinionUnit, opinionunit_shop
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
    assert beef_opinionunit._topic_affect_ratio is None
    assert beef_opinionunit._topic_love_ratio is None


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
    assert beef_opinionunit._topic_affect_ratio is None
    assert beef_opinionunit._topic_love_ratio is None


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


def test_opinionunit_shop_ReturnsObj():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    cook_opinionunit = opinionunit_shop(road=gas_road, affect=7, love=11)

    # THEN
    assert cook_opinionunit.road == gas_road
    assert cook_opinionunit.affect == 7
    assert cook_opinionunit.love == 11
    assert cook_opinionunit._topic_affect_ratio is None
    assert cook_opinionunit._topic_love_ratio is None


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


def test_OpinionUnit_set_topic_affect_ratio_CorrectSetsAttrs_good():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    good_affect = 7
    beef_opinionunit = opinionunit_shop(road=gas_road, affect=good_affect)
    assert beef_opinionunit._topic_affect_ratio is None

    # WHEN
    sum_good_affect = 28
    sum_bad_affect = 77
    beef_opinionunit.set_topic_affect_ratio(sum_good_affect, sum_bad_affect)

    # THEN
    assert beef_opinionunit._topic_affect_ratio == good_affect / sum_good_affect
    assert beef_opinionunit._topic_affect_ratio == 0.25


def test_OpinionUnit_set_topic_affect_ratio_CorrectSetsAttrs_bad():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    bad_affect = -8
    beef_opinionunit = opinionunit_shop(road=gas_road, affect=bad_affect)
    assert beef_opinionunit._topic_affect_ratio is None

    # WHEN
    sum_good_affect = 2
    sum_bad_affect = 10
    beef_opinionunit.set_topic_affect_ratio(sum_good_affect, sum_bad_affect)

    # THEN
    assert beef_opinionunit._topic_affect_ratio == -0.80
    assert beef_opinionunit._topic_affect_ratio == bad_affect / sum_bad_affect


def test_OpinionUnit_set_topic_love_ratio_CorrectSetsAttrWhen_in_tribe():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    in_tribe_love = 7
    beef_opinionunit = opinionunit_shop(gas_road, 3, love=in_tribe_love)
    assert beef_opinionunit._topic_love_ratio is None

    # WHEN
    sum_in_tribe_love = 28
    sum_out_tribe_love = None
    beef_opinionunit.set_topic_love_ratio(sum_in_tribe_love, sum_out_tribe_love)

    # THEN
    assert beef_opinionunit._topic_love_ratio == in_tribe_love / sum_in_tribe_love
    assert beef_opinionunit._topic_love_ratio == 0.25


def test_OpinionUnit_set_topic_love_ratio_CorrectSetsAttrWhen_out_tribe():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    out_tribe_love = -8
    beef_opinionunit = opinionunit_shop(gas_road, 3, love=out_tribe_love)
    assert beef_opinionunit._topic_love_ratio is None

    # WHEN
    sum_good_love = 2
    sum_out_tribe_love = 10
    beef_opinionunit.set_topic_love_ratio(sum_good_love, sum_out_tribe_love)

    # THEN
    assert beef_opinionunit._topic_love_ratio == -0.80
    assert beef_opinionunit._topic_love_ratio == out_tribe_love / sum_out_tribe_love


def test_OpinionUnit_set_topic_love_ratio_CorrectSetsAttrsWhen_zero():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    no_tribe_love = 0
    beef_opinionunit = opinionunit_shop(gas_road, 3, love=no_tribe_love)
    assert beef_opinionunit._topic_love_ratio is None

    # WHEN
    beef_opinionunit.set_topic_love_ratio(None, None)

    # THEN
    assert beef_opinionunit._topic_love_ratio == 0
