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


def test_BeliefUnit_exists():
    # GIVEN / WHEN
    x_belief = BeliefUnit()

    # THEN
    assert x_belief != None
    assert x_belief.base is None
    assert x_belief.opinionunits is None
    assert x_belief.delimiter is None
    assert x_belief.owners is None


def test_beliefunit_shop_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    cook_belief = beliefunit_shop(base=cook_road)

    # THEN
    assert cook_belief.base == cook_road
    assert cook_belief.opinionunits == {}
    assert cook_belief.delimiter == default_road_delimiter_if_none()
    assert cook_belief.owners == {}


def test_BeliefUnit_set_owner_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    assert cook_belief.owners == {}

    # WHEN
    bob_text = "Bob"
    cook_belief.set_owner(x_owner=bob_text)

    # THEN
    assert cook_belief.owners != {}
    assert cook_belief.owners.get(bob_text) != None
    assert cook_belief.owners.get(bob_text) == bob_text


def test_BeliefUnit_del_owner_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_belief.set_owner(bob_text)
    cook_belief.set_owner(yao_text)
    assert len(cook_belief.owners) == 2
    assert cook_belief.owners.get(bob_text) != None
    assert cook_belief.owners.get(yao_text) != None

    # WHEN
    cook_belief.del_owner(bob_text)

    # THEN
    assert len(cook_belief.owners) == 1
    assert cook_belief.owners.get(bob_text) is None
    assert cook_belief.owners.get(yao_text) != None


def test_BeliefUnit_get_owners_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_belief.set_owner(bob_text)
    cook_belief.set_owner(yao_text)

    # WHEN
    bob_owner = cook_belief.get_owner(bob_text)

    # THEN
    assert bob_owner != None
    assert bob_owner == bob_text


def test_BeliefUnit_set_opinionunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    assert cook_belief.opinionunits == {}

    # WHEN
    cheap_road = create_road(cook_road, "cheap food")
    x_affect = -2
    cheap_opinionunit = opinionunit_shop(cheap_road, affect=x_affect)
    cook_belief.set_opinionunit(x_opinionunit=cheap_opinionunit)

    # THEN
    assert cook_belief.opinionunits != {}
    assert cook_belief.opinionunits.get(cheap_road) != None
    assert cook_belief.opinionunits.get(cheap_road) == cheap_opinionunit


def test_BeliefUnit_del_opinionunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    metal_road = create_road(cook_road, "metal pots")
    cheap_opinionunit = opinionunit_shop(cheap_road, affect=-2)
    metal_opinionunit = opinionunit_shop(metal_road, affect=3)
    cook_belief.set_opinionunit(cheap_opinionunit)
    cook_belief.set_opinionunit(metal_opinionunit)
    assert len(cook_belief.opinionunits) == 2
    assert cook_belief.opinionunits.get(cheap_road) != None
    assert cook_belief.opinionunits.get(metal_road) != None

    # WHEN
    cook_belief.del_opinionunit(cheap_road)

    # THEN
    assert len(cook_belief.opinionunits) == 1
    assert cook_belief.opinionunits.get(cheap_road) is None
    assert cook_belief.opinionunits.get(metal_road) != None


def test_BeliefUnit_get_opinionunits_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_opinionunit = opinionunit_shop(farm_road, farm_affect)
    cook_belief.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_good_opinionunits = cook_belief.get_opinionunits(good=True)

    # THEN
    assert x_good_opinionunits != {}
    assert len(x_good_opinionunits) == 1
    assert x_good_opinionunits.get(farm_road) == farm_opinionunit


def test_BeliefUnit_get_opinionunits_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_opinionunit = opinionunit_shop(farm_road, farm_affect)
    cook_belief.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cheap_opinionunit = opinionunit_shop(cheap_road, cheap_affect)
    cook_belief.set_opinionunit(cheap_opinionunit)

    # WHEN
    x_bad_opinionunits = cook_belief.get_opinionunits(bad=True)

    # THEN
    assert x_bad_opinionunits != {}
    assert len(x_bad_opinionunits) == 1
    assert x_bad_opinionunits.get(cheap_road) == cheap_opinionunit


def test_BeliefUnit_get_1_opinionunit_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_belief.set_opinionunit(opinionunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_opinionunit = cook_belief.get_1_opinionunit(good=True)

    # THEN
    assert x_bad_opinionunit == farm_road


def test_BeliefUnit_get_1_opinionunit_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_belief.set_opinionunit(opinionunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_opinionunit = cook_belief.get_1_opinionunit(bad=True)

    # THEN
    assert x_bad_opinionunit == cheap_road


def test_BeliefUnit_get_opinionunits_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=farm_love)
    cook_belief.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_in_tribe_opinionunits = cook_belief.get_opinionunits(in_tribe=True)

    # THEN
    assert x_in_tribe_opinionunits != {}
    assert len(x_in_tribe_opinionunits) == 1
    assert x_in_tribe_opinionunits.get(farm_road) == farm_opinionunit


def test_BeliefUnit_get_opinionunits_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=farm_love)
    cook_belief.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cheap_opinionunit = opinionunit_shop(cheap_road, -2, love=cheap_love)
    cook_belief.set_opinionunit(cheap_opinionunit)

    # WHEN
    x_out_tribe_opinionunits = cook_belief.get_opinionunits(out_tribe=True)

    # THEN.
    assert x_out_tribe_opinionunits != {}
    assert len(x_out_tribe_opinionunits) == 1
    assert x_out_tribe_opinionunits.get(cheap_road) == cheap_opinionunit


def test_BeliefUnit_get_1_opinionunit_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_belief.set_opinionunit(opinionunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_opinionunit = cook_belief.get_1_opinionunit(in_tribe=True)

    # THEN
    assert x_out_tribe_opinionunit == farm_road


def test_BeliefUnit_get_1_opinionunit_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_belief.set_opinionunit(opinionunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_belief.set_opinionunit(opinionunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_opinionunit = cook_belief.get_1_opinionunit(out_tribe=True)

    # THEN
    assert x_out_tribe_opinionunit == cheap_road


def test_BeliefUnit_set_opinionunits_CorrectlyRaisesBeliefSubRoadUnitException():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    go_road = "going out"
    go_cheap_road = create_road(go_road, "cheap food")
    go_cheap_opinionunit = opinionunit_shop(go_cheap_road, affect=-3)

    # WHEN
    x_affect = -2
    with pytest_raises(Exception) as excinfo:
        cook_belief.set_opinionunit(go_cheap_opinionunit)
    assert (
        str(excinfo.value)
        == f"BeliefUnit cannot set opinionunit '{go_cheap_road}' because base road is '{cook_road}'."
    )


def test_BeliefUnit_is_moral_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)

    # WHEN / THEN
    assert len(cook_belief.opinionunits) == 0
    assert cook_belief.is_moral() == False

    # WHEN / THEN
    cheap_opinionunit = opinionunit_shop(create_road(cook_road, "cheap food"), -2)
    cook_belief.set_opinionunit(cheap_opinionunit)
    assert len(cook_belief.opinionunits) == 1
    assert cook_belief.is_moral() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_opinionunit = opinionunit_shop(create_road(cook_road, farm_text), 3)
    cook_belief.set_opinionunit(farm_opinionunit)
    assert len(cook_belief.opinionunits) == 2
    assert cook_belief.is_moral()

    # WHEN / THEN
    cook_belief.del_opinionunit(create_road(cook_road, farm_text))
    assert len(cook_belief.opinionunits) == 1
    assert cook_belief.is_moral() == False

    # WHEN / THEN
    plastic_opinionunit = opinionunit_shop(create_road(cook_road, "plastic pots"), -5)
    cook_belief.set_opinionunit(plastic_opinionunit)
    assert len(cook_belief.opinionunits) == 2
    assert cook_belief.is_moral() == False

    # WHEN / THEN
    metal_opinionunit = opinionunit_shop(create_road(cook_road, "metal pots"), 7)
    cook_belief.set_opinionunit(metal_opinionunit)
    assert len(cook_belief.opinionunits) == 3
    assert cook_belief.is_moral()


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
    cook_belief.set_opinionunit(opinionunit_shop(warm_proc_road, affect=44, love=-9))
    cook_belief.set_opinionunit(opinionunit_shop(cold_proc_road, affect=-5, love=-4))
    cook_belief.set_opinionunit(opinionunit_shop(warm_farm_road, affect=33, love=77))
    cook_belief.set_opinionunit(opinionunit_shop(cold_farm_road, affect=-7, love=88))
    assert len(cook_belief.opinionunits) == 4
    assert cook_belief.is_tribal()
    assert cook_belief.is_moral()
    assert cook_belief.is_dialectic()

    # WHEN / THEN
    cook_belief.del_opinionunit(cold_proc_road)
    assert len(cook_belief.opinionunits) == 3
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
    cook_belief.set_opinionunit(
        opinionunit_shop(create_road(cook_road, cheap_text), -2)
    )
    cook_belief.set_opinionunit(opinionunit_shop(create_road(cook_road, farm_text), 3))
    cook_belief.set_opinionunit(
        opinionunit_shop(create_road(cook_road, plastic_text), -5)
    )
    cook_belief.set_opinionunit(opinionunit_shop(create_road(cook_road, metal_text), 7))
    assert len(cook_belief.opinionunits) == 4

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
    assert len(cook_belief.opinionunits) == 4


def test_create_beliefunit_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    farm_text = "farm food"
    cheap_text = "cheap food"
    cook_belief = create_beliefunit(base=cook_road, good=farm_text, bad=cheap_text)

    # THEN
    assert cook_belief.base == cook_road
    assert cook_belief.opinionunits != {}
    farm_road = create_road(cook_road, farm_text)
    cheap_road = create_road(cook_road, cheap_text)
    assert cook_belief.opinionunits.get(farm_road) == opinionunit_shop(farm_road, 1)
    assert cook_belief.opinionunits.get(cheap_road) == opinionunit_shop(cheap_road, -1)
