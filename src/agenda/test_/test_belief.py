from src.agenda.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src.agenda.belief import (
    BeliefUnit,
    beliefunit_shop,
    create_beliefunit,
    IdeaLink,
    idealink_shop,
)
from pytest import raises as pytest_raises


def test_IdeaLink_exists():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    beef_idealink = IdeaLink(road=gas_road)

    # THEN
    assert beef_idealink != None
    assert beef_idealink.road == gas_road
    assert beef_idealink.affect is None
    assert beef_idealink.love is None


def test_IdeaLink_set_affect_CorrectSetsAttrs():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    beef_idealink = IdeaLink(road=gas_road)
    assert beef_idealink.affect is None

    # WHEN
    beef_affect = -3
    beef_idealink.set_affect(beef_affect)

    # THEN
    assert beef_idealink.affect == beef_affect


def test_IdeaLink_set_love_CorrectSetsAttrs():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")
    beef_idealink = IdeaLink(road=gas_road)
    assert beef_idealink.love is None

    # WHEN
    beef_love = -7
    beef_idealink.set_love(beef_love)

    # THEN
    assert beef_idealink.love == beef_love


def test_idealink_shop_CorrectlyReturnsObj():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    cook_idealink = idealink_shop(road=gas_road, affect=7, love=11)

    # THEN
    assert cook_idealink.road == gas_road
    assert cook_idealink.affect == 7
    assert cook_idealink.love == 11


def test_idealink_shop_Sets_love_NoneIf():
    # GIVEN
    gas_road = create_road(root_label(), "gas cooking")

    # WHEN
    cook_idealink = idealink_shop(road=gas_road, affect=7)

    # THEN
    assert cook_idealink.road == gas_road
    assert cook_idealink.affect == 7
    assert cook_idealink.love == 0


def test_IdeaLink_set_affect_CorrectlyRaisesNoneZeroAffectException():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cheap_road = create_road(cook_road, "cheap food")
    cheap_idealink = idealink_shop(cheap_road, affect=-5)

    # WHEN
    zero_int = 0
    with pytest_raises(Exception) as excinfo:
        cheap_idealink.set_affect(x_affect=zero_int)
    assert (
        str(excinfo.value)
        == f"set_affect affect parameter {zero_int} must be Non-zero number"
    )


def test_BeliefUnit_exists():
    # GIVEN / WHEN
    x_belief = BeliefUnit()

    # THEN
    assert x_belief != None
    assert x_belief.base is None
    assert x_belief.idealinks is None
    assert x_belief.delimiter is None


def test_beliefunit_shop_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    cook_belief = beliefunit_shop(base=cook_road)

    # THEN
    assert cook_belief.base == cook_road
    assert cook_belief.idealinks == {}
    assert cook_belief.delimiter == default_road_delimiter_if_none()


def test_BeliefUnit_set_idealink_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    assert cook_belief.idealinks == {}

    # WHEN
    cheap_road = create_road(cook_road, "cheap food")
    x_affect = -2
    cheap_idealink = idealink_shop(cheap_road, affect=x_affect)
    cook_belief.set_idealink(x_idealink=cheap_idealink)

    # THEN
    assert cook_belief.idealinks != {}
    assert cook_belief.idealinks.get(cheap_road) != None
    assert cook_belief.idealinks.get(cheap_road) == cheap_idealink


def test_BeliefUnit_del_idealink_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    metal_road = create_road(cook_road, "metal pots")
    cheap_idealink = idealink_shop(cheap_road, affect=-2)
    metal_idealink = idealink_shop(metal_road, affect=3)
    cook_belief.set_idealink(cheap_idealink)
    cook_belief.set_idealink(metal_idealink)
    assert len(cook_belief.idealinks) == 2
    assert cook_belief.idealinks.get(cheap_road) != None
    assert cook_belief.idealinks.get(metal_road) != None

    # WHEN
    cook_belief.del_idealink(cheap_road)

    # THEN
    assert len(cook_belief.idealinks) == 1
    assert cook_belief.idealinks.get(cheap_road) is None
    assert cook_belief.idealinks.get(metal_road) != None


def test_BeliefUnit_get_idealinks_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_idealink = idealink_shop(farm_road, farm_affect)
    cook_belief.set_idealink(farm_idealink)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_belief.set_idealink(idealink_shop(cheap_road, cheap_affect))

    # WHEN
    x_good_idealinks = cook_belief.get_idealinks(good=True)

    # THEN
    assert x_good_idealinks != {}
    assert len(x_good_idealinks) == 1
    assert x_good_idealinks.get(farm_road) == farm_idealink


def test_BeliefUnit_get_idealinks_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_idealink = idealink_shop(farm_road, farm_affect)
    cook_belief.set_idealink(farm_idealink)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cheap_idealink = idealink_shop(cheap_road, cheap_affect)
    cook_belief.set_idealink(cheap_idealink)

    # WHEN
    x_bad_idealinks = cook_belief.get_idealinks(bad=True)

    # THEN
    assert x_bad_idealinks != {}
    assert len(x_bad_idealinks) == 1
    assert x_bad_idealinks.get(cheap_road) == cheap_idealink


def test_BeliefUnit_get_1_idealink_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_belief.set_idealink(idealink_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_belief.set_idealink(idealink_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_idealink = cook_belief.get_1_idealink(good=True)

    # THEN
    assert x_bad_idealink == farm_road


def test_BeliefUnit_get_1_idealink_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_belief.set_idealink(idealink_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_belief.set_idealink(idealink_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_idealink = cook_belief.get_1_idealink(bad=True)

    # THEN
    assert x_bad_idealink == cheap_road


def test_BeliefUnit_get_idealinks_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_idealink = idealink_shop(farm_road, -2, love=farm_love)
    cook_belief.set_idealink(farm_idealink)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_belief.set_idealink(idealink_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_in_tribe_idealinks = cook_belief.get_idealinks(in_tribe=True)

    # THEN
    assert x_in_tribe_idealinks != {}
    assert len(x_in_tribe_idealinks) == 1
    assert x_in_tribe_idealinks.get(farm_road) == farm_idealink


def test_BeliefUnit_get_idealinks_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_idealink = idealink_shop(farm_road, -2, love=farm_love)
    cook_belief.set_idealink(farm_idealink)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cheap_idealink = idealink_shop(cheap_road, -2, love=cheap_love)
    cook_belief.set_idealink(cheap_idealink)

    # WHEN
    x_out_tribe_idealinks = cook_belief.get_idealinks(out_tribe=True)

    # THEN.
    assert x_out_tribe_idealinks != {}
    assert len(x_out_tribe_idealinks) == 1
    assert x_out_tribe_idealinks.get(cheap_road) == cheap_idealink


def test_BeliefUnit_get_1_idealink_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_belief.set_idealink(idealink_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_belief.set_idealink(idealink_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_idealink = cook_belief.get_1_idealink(in_tribe=True)

    # THEN
    assert x_out_tribe_idealink == farm_road


def test_BeliefUnit_get_1_idealink_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_belief.set_idealink(idealink_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_belief.set_idealink(idealink_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_idealink = cook_belief.get_1_idealink(out_tribe=True)

    # THEN
    assert x_out_tribe_idealink == cheap_road


def test_BeliefUnit_set_idealinks_CorrectlyRaisesBeliefSubRoadUnitException():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    go_road = "going out"
    go_cheap_road = create_road(go_road, "cheap food")
    go_cheap_idealink = idealink_shop(go_cheap_road, affect=-3)

    # WHEN
    x_affect = -2
    with pytest_raises(Exception) as excinfo:
        cook_belief.set_idealink(go_cheap_idealink)
    assert (
        str(excinfo.value)
        == f"BeliefUnit cannot set idealink '{go_cheap_road}' because base road is '{cook_road}'."
    )


def test_BeliefUnit_is_moral_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)

    # WHEN / THEN
    assert len(cook_belief.idealinks) == 0
    assert cook_belief.is_moral() == False

    # WHEN / THEN
    cheap_idealink = idealink_shop(create_road(cook_road, "cheap food"), -2)
    cook_belief.set_idealink(cheap_idealink)
    assert len(cook_belief.idealinks) == 1
    assert cook_belief.is_moral() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_idealink = idealink_shop(create_road(cook_road, farm_text), 3)
    cook_belief.set_idealink(farm_idealink)
    assert len(cook_belief.idealinks) == 2
    assert cook_belief.is_moral()

    # WHEN / THEN
    cook_belief.del_idealink(create_road(cook_road, farm_text))
    assert len(cook_belief.idealinks) == 1
    assert cook_belief.is_moral() == False

    # WHEN / THEN
    plastic_idealink = idealink_shop(create_road(cook_road, "plastic pots"), -5)
    cook_belief.set_idealink(plastic_idealink)
    assert len(cook_belief.idealinks) == 2
    assert cook_belief.is_moral() == False

    # WHEN / THEN
    metal_idealink = idealink_shop(create_road(cook_road, "metal pots"), 7)
    cook_belief.set_idealink(metal_idealink)
    assert len(cook_belief.idealinks) == 3
    assert cook_belief.is_moral()


def test_BeliefUnit_is_tribal_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)

    # WHEN / THEN
    assert cook_belief.is_tribal() == False

    # WHEN / THEN
    cheap_road = create_road(cook_road, "cheap food")
    cheap_idealink = idealink_shop(cheap_road, -2, love=77)
    cook_belief.set_idealink(cheap_idealink)
    assert cook_belief.is_tribal() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_road = create_road(cook_road, farm_text)
    farm_idealink = idealink_shop(farm_road, -2, love=-55)
    cook_belief.set_idealink(farm_idealink)
    assert cook_belief.is_tribal()

    # WHEN / THEN
    cook_belief.del_idealink(farm_road)
    assert len(cook_belief.idealinks) == 1
    assert cook_belief.is_tribal() == False

    # WHEN / THEN
    plastic_road = create_road(cook_road, "plastic pots")
    plastic_idealink = idealink_shop(plastic_road, -2, love=99)
    cook_belief.set_idealink(plastic_idealink)
    assert len(cook_belief.idealinks) == 2
    assert cook_belief.is_tribal() == False

    # WHEN / THEN
    metal_road = create_road(cook_road, "metal pots")
    metal_idealink = idealink_shop(metal_road, -2, love=-44)
    cook_belief.set_idealink(metal_idealink)
    assert len(cook_belief.idealinks) == 3
    assert cook_belief.is_tribal()


def test_BeliefUnit_is_dialectic_ReturnsCorrectBool_v1():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)

    # WHEN / THEN
    assert cook_belief.is_tribal() == False
    assert cook_belief.is_moral() == False
    assert cook_belief.is_dialectic() == False


def test_BeliefUnit_is_dialectic_ReturnsCorrectBool_v2():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    warm_proc_road = create_road(cook_road, "warm processed food")
    cold_proc_road = create_road(cook_road, "cold processed food")
    warm_farm_road = create_road(cook_road, "warm farmed food")
    cold_farm_road = create_road(cook_road, "cold farmed food")
    cook_belief.set_idealink(idealink_shop(warm_proc_road, affect=44, love=-9))
    cook_belief.set_idealink(idealink_shop(cold_proc_road, affect=-5, love=-4))
    cook_belief.set_idealink(idealink_shop(warm_farm_road, affect=33, love=77))
    cook_belief.set_idealink(idealink_shop(cold_farm_road, affect=-7, love=88))
    assert len(cook_belief.idealinks) == 4
    assert cook_belief.is_tribal()
    assert cook_belief.is_moral()
    assert cook_belief.is_dialectic()

    # WHEN / THEN
    cook_belief.del_idealink(cold_proc_road)
    assert len(cook_belief.idealinks) == 3
    assert cook_belief.is_tribal()
    assert cook_belief.is_moral()
    assert cook_belief.is_dialectic() == False


def test_BeliefUnit_get_all_roads_ReturnsCorrectObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    cheap_text = "cheap food"
    farm_text = "farm fresh"
    plastic_text = "plastic pots"
    metal_text = "metal pots"
    cook_belief.set_idealink(idealink_shop(create_road(cook_road, cheap_text), -2))
    cook_belief.set_idealink(idealink_shop(create_road(cook_road, farm_text), 3))
    cook_belief.set_idealink(idealink_shop(create_road(cook_road, plastic_text), -5))
    cook_belief.set_idealink(idealink_shop(create_road(cook_road, metal_text), 7))
    assert len(cook_belief.idealinks) == 4

    # WHEN
    all_roads_dict = cook_belief.get_all_roads()

    # THEN
    assert len(all_roads_dict) == 5
    assert all_roads_dict.get(cook_road) != None
    cheap_road = create_road(cook_road, cheap_text)
    farm_road = create_road(cook_road, farm_text)
    plastic_road = create_road(cook_road, plastic_text)
    metal_road = create_road(cook_road, metal_text)
    assert all_roads_dict.get(cheap_road) != None
    assert all_roads_dict.get(farm_road) != None
    assert all_roads_dict.get(plastic_road) != None
    assert all_roads_dict.get(metal_road) != None
    assert len(cook_belief.idealinks) == 4


def test_create_beliefunit_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    farm_text = "farm food"
    cheap_text = "cheap food"
    cook_belief = create_beliefunit(base=cook_road, good=farm_text, bad=cheap_text)

    # THEN
    assert cook_belief.base == cook_road
    assert cook_belief.idealinks != {}
    farm_road = create_road(cook_road, farm_text)
    cheap_road = create_road(cook_road, cheap_text)
    assert cook_belief.idealinks.get(farm_road) == idealink_shop(farm_road, 1)
    assert cook_belief.idealinks.get(cheap_road) == idealink_shop(cheap_road, -1)
