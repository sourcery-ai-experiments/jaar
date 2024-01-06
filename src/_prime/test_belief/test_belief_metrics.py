from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._prime.belief import (
    BeliefUnit,
    beliefunit_shop,
    create_beliefunit,
    OpinionUnit,
    opinionunit_shop,
)
from pytest import raises as pytest_raises


def test_BeliefUnit_is_meaningful_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)

    # WHEN / THEN
    assert len(cook_belief.opinionunits) == 0
    assert cook_belief.is_meaningful() == False

    # WHEN / THEN
    cheap_opinionunit = opinionunit_shop(create_road(cook_road, "cheap food"), -2)
    cook_belief.set_opinionunit(cheap_opinionunit)
    assert len(cook_belief.opinionunits) == 1
    assert cook_belief.is_meaningful() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_opinionunit = opinionunit_shop(create_road(cook_road, farm_text), 3)
    cook_belief.set_opinionunit(farm_opinionunit)
    assert len(cook_belief.opinionunits) == 2
    assert cook_belief.is_meaningful()

    # WHEN / THEN
    cook_belief.del_opinionunit(create_road(cook_road, farm_text))
    assert len(cook_belief.opinionunits) == 1
    assert cook_belief.is_meaningful() == False

    # WHEN / THEN
    plastic_opinionunit = opinionunit_shop(create_road(cook_road, "plastic pots"), -5)
    cook_belief.set_opinionunit(plastic_opinionunit)
    assert len(cook_belief.opinionunits) == 2
    assert cook_belief.is_meaningful() == False

    # WHEN / THEN
    metal_opinionunit = opinionunit_shop(create_road(cook_road, "metal pots"), 7)
    cook_belief.set_opinionunit(metal_opinionunit)
    assert len(cook_belief.opinionunits) == 3
    assert cook_belief.is_meaningful()


def test_BeliefUnit_is_tribal_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)

    # WHEN / THEN
    assert cook_belief.is_tribal() == False

    # WHEN / THEN
    cheap_road = create_road(cook_road, "cheap food")
    cheap_opinionunit = opinionunit_shop(cheap_road, -2, love=77)
    cook_belief.set_opinionunit(cheap_opinionunit)
    assert cook_belief.is_tribal() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_road = create_road(cook_road, farm_text)
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=-55)
    cook_belief.set_opinionunit(farm_opinionunit)
    assert cook_belief.is_tribal()

    # WHEN / THEN
    cook_belief.del_opinionunit(farm_road)
    assert len(cook_belief.opinionunits) == 1
    assert cook_belief.is_tribal() == False

    # WHEN / THEN
    plastic_road = create_road(cook_road, "plastic pots")
    plastic_opinionunit = opinionunit_shop(plastic_road, -2, love=99)
    cook_belief.set_opinionunit(plastic_opinionunit)
    assert len(cook_belief.opinionunits) == 2
    assert cook_belief.is_tribal() == False

    # WHEN / THEN
    metal_road = create_road(cook_road, "metal pots")
    metal_opinionunit = opinionunit_shop(metal_road, -2, love=-44)
    cook_belief.set_opinionunit(metal_opinionunit)
    assert len(cook_belief.opinionunits) == 3
    assert cook_belief.is_tribal()


def test_BeliefUnit_is_dialectic_ReturnsCorrectBool_v1():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)

    # WHEN / THEN
    assert cook_belief.is_tribal() == False
    assert cook_belief.is_meaningful() == False
    assert cook_belief.is_dialectic() == False


def test_BeliefUnit_is_dialectic_ReturnsCorrectBool_v2():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    warm_proc_road = create_road(cook_road, "warm processed food")
    cold_proc_road = create_road(cook_road, "cold processed food")
    warm_farm_road = create_road(cook_road, "warm farmed food")
    cold_farm_road = create_road(cook_road, "cold farmed food")
    cook_belief.set_opinionunit(opinionunit_shop(warm_proc_road, affect=44, love=-9))
    cook_belief.set_opinionunit(opinionunit_shop(cold_proc_road, affect=-5, love=-4))
    cook_belief.set_opinionunit(opinionunit_shop(warm_farm_road, affect=33, love=77))
    cook_belief.set_opinionunit(opinionunit_shop(cold_farm_road, affect=-7, love=88))
    assert len(cook_belief.opinionunits) == 4
    assert cook_belief.is_tribal()
    assert cook_belief.is_meaningful()
    assert cook_belief.is_dialectic()

    # WHEN / THEN
    cook_belief.del_opinionunit(cold_proc_road)
    assert len(cook_belief.opinionunits) == 3
    assert cook_belief.is_tribal()
    assert cook_belief.is_meaningful()
    assert cook_belief.is_dialectic() == False


def test_BeliefUnit_set_metrics_SetsAttr_calc_is_meaningful_Correctly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    assert cook_belief._calc_is_meaningful == False

    # WHEN
    cook_belief.set_metrics()
    # THEN
    assert cook_belief._calc_is_meaningful == False

    # GIVEN
    cheap_opinionunit = opinionunit_shop(create_road(cook_road, "cheap food"), -2)
    cook_belief.set_opinionunit(cheap_opinionunit, set_metrics=False)
    farm_text = "farm fresh"
    farm_opinionunit = opinionunit_shop(create_road(cook_road, farm_text), 3)
    cook_belief.set_opinionunit(farm_opinionunit, set_metrics=False)
    assert len(cook_belief.opinionunits) == 2
    assert cook_belief.is_meaningful()
    assert cook_belief._calc_is_meaningful == False

    # WHEN
    cook_belief.set_metrics()
    # THEN
    assert cook_belief._calc_is_meaningful


def test_BeliefUnit_set_metrics_SetsAttr_calc_is_tribal_Correctly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    assert cook_belief.is_tribal() == False
    # WHEN
    cook_belief.set_metrics()
    # THEN
    assert cook_belief.is_tribal() == False

    # WHEN / THEN
    cheap_road = create_road(cook_road, "cheap food")
    cheap_opinionunit = opinionunit_shop(cheap_road, -2, love=77)
    cook_belief.set_opinionunit(cheap_opinionunit, set_metrics=False)
    farm_text = "farm fresh"
    farm_road = create_road(cook_road, farm_text)
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=-55)
    cook_belief.set_opinionunit(farm_opinionunit, set_metrics=False)
    assert cook_belief.is_tribal()
    assert cook_belief._calc_is_tribal == False
    # WHEN
    cook_belief.set_metrics()
    # THEN
    assert cook_belief._calc_is_tribal


def test_BeliefUnit_set_metrics_SetsAttr_calc_is_dialectic_Correctly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    warm_proc_road = create_road(cook_road, "warm processed food")
    cold_proc_road = create_road(cook_road, "cold processed food")
    warm_farm_road = create_road(cook_road, "warm farmed food")
    cold_farm_road = create_road(cook_road, "cold farmed food")
    warm_proc_opinionunit = opinionunit_shop(warm_proc_road, affect=44, love=-9)
    cold_proc_opinionunit = opinionunit_shop(cold_proc_road, affect=-5, love=-4)
    warm_farm_opinionunit = opinionunit_shop(warm_farm_road, affect=33, love=77)
    cold_farm_opinionunit = opinionunit_shop(cold_farm_road, affect=-7, love=88)
    cook_belief.set_opinionunit(warm_proc_opinionunit, set_metrics=False)
    cook_belief.set_opinionunit(cold_proc_opinionunit, set_metrics=False)
    cook_belief.set_opinionunit(warm_farm_opinionunit, set_metrics=False)
    cook_belief.set_opinionunit(cold_farm_opinionunit, set_metrics=False)
    assert len(cook_belief.opinionunits) == 4
    assert cook_belief.is_tribal()
    assert cook_belief.is_meaningful()
    assert cook_belief.is_dialectic()
    assert cook_belief._calc_is_tribal == False
    assert cook_belief._calc_is_meaningful == False
    assert cook_belief._calc_is_dialectic == False

    # WHEN
    cook_belief.set_metrics()
    # THEN
    assert cook_belief._calc_is_tribal
    assert cook_belief._calc_is_meaningful
    assert cook_belief._calc_is_dialectic

    # GIVEN
    cook_belief.del_opinionunit(cold_proc_road)
    assert len(cook_belief.opinionunits) == 3
    assert cook_belief.is_tribal()
    assert cook_belief.is_meaningful()
    assert cook_belief.is_dialectic() == False

    # WHEN
    cook_belief.set_metrics()
    # THEN
    assert cook_belief._calc_is_tribal
    assert cook_belief._calc_is_meaningful
    assert cook_belief._calc_is_dialectic == False

    # WHEN
    cook_belief.set_opinionunit(opinionunit_shop(cold_proc_road, affect=-5, love=-4))
    # THEN
    assert cook_belief._calc_is_tribal
    assert cook_belief._calc_is_meaningful
    assert cook_belief._calc_is_dialectic
