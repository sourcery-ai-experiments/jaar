from src.agenda.road import (
    RoadUnit,
    change_road,
    is_sub_road,
    get_all_road_nodes,
    get_terminus_node_from_road,
    find_replace_road_key_dict,
    get_pad_from_road,
    get_road_without_root_node,
    road_validate,
    get_ancestor_roads,
    get_forefather_roads,
    get_default_economy_root_label as root_label,
    get_road_from_nodes,
    get_road_from_road_and_node,
    RoadNode,
    get_diff_road,
    get_road,
    is_heir_road,
    get_node_delimiter,
    replace_road_node_delimiter,
    ForkUnit,
    forkunit_shop,
    create_forkunit,
)
from src.agenda.required_idea import sufffactunit_shop
from src.agenda.idea import IdeaCore
from pytest import raises as pytest_raises


def test_ForkUnit_exists():
    # GIVEN / WHEN
    x_fork = ForkUnit()

    # THEN
    assert x_fork != None
    assert x_fork.base is None
    assert x_fork.descendents is None
    assert x_fork.delimiter is None


def test_ForkUnit_set_descendents_empty_if_none_CorrectlySetsAttr():
    # GIVEN
    x_fork = ForkUnit()
    assert x_fork.descendents is None

    # WHEN
    x_fork.set_descendents_empty_if_none()

    # THEN
    assert x_fork.descendents == {}


def test_forkunit_shop_CorrectlyReturnsObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")

    # WHEN
    cook_fork = forkunit_shop(base=cook_road)

    # THEN
    assert cook_fork.base == cook_road
    assert cook_fork.descendents == {}
    assert cook_fork.delimiter == get_node_delimiter()


def test_ForkUnit_set_descendent_CorrectlySetsAttr():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    assert cook_fork.descendents == {}

    # WHEN
    cheap_road = get_road(cook_road, "cheap food")
    x_affect = -2
    cook_fork.set_descendent(cheap_road, affect=x_affect)

    # THEN
    assert cook_fork.descendents != {}
    assert cook_fork.descendents.get(cheap_road) != None
    assert cook_fork.descendents.get(cheap_road) == x_affect


def test_ForkUnit_del_descendent_CorrectlySetsAttr():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    cheap_road = get_road(cook_road, "cheap food")
    metal_road = get_road(cook_road, "metal pots")
    cook_fork.set_descendent(cheap_road, affect=-2)
    cook_fork.set_descendent(metal_road, affect=3)
    assert len(cook_fork.descendents) == 2
    assert cook_fork.descendents.get(cheap_road) != None
    assert cook_fork.descendents.get(metal_road) != None

    # WHEN
    cook_fork.del_descendent(cheap_road)

    # THEN
    assert len(cook_fork.descendents) == 1
    assert cook_fork.descendents.get(cheap_road) is None
    assert cook_fork.descendents.get(metal_road) != None


def test_ForkUnit_is_dialectic_ReturnsCorrectBool():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)

    # WHEN / THEN
    assert len(cook_fork.descendents) == 0
    assert cook_fork.is_dialectic() == False

    # WHEN / THEN
    cook_fork.set_descendent(get_road(cook_road, "cheap food"), affect=-2)
    assert len(cook_fork.descendents) == 1
    assert cook_fork.is_dialectic() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    cook_fork.set_descendent(get_road(cook_road, farm_text), affect=3)
    assert len(cook_fork.descendents) == 2
    assert cook_fork.is_dialectic()

    # WHEN / THEN
    cook_fork.del_descendent(get_road(cook_road, farm_text))
    assert len(cook_fork.descendents) == 1
    assert cook_fork.is_dialectic() == False

    # WHEN / THEN
    cook_fork.set_descendent(get_road(cook_road, "plastic pots"), affect=-5)
    assert len(cook_fork.descendents) == 2
    assert cook_fork.is_dialectic() == False

    # WHEN / THEN
    cook_fork.set_descendent(get_road(cook_road, "metal pots"), affect=7)
    assert len(cook_fork.descendents) == 3
    assert cook_fork.is_dialectic()


def test_ForkUnit_get_good_descendents_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_affect = 3
    cook_fork.set_descendent(farm_road, affect=farm_affect)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_fork.set_descendent(cheap_road, affect=cheap_affect)

    # WHEN
    x_good_descendents = cook_fork.get_good_descendents()

    # THEN
    assert x_good_descendents != {}
    assert len(x_good_descendents) == 1
    assert x_good_descendents.get(farm_road) == farm_affect


def test_ForkUnit_get_bad_descendents_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_affect = 3
    cook_fork.set_descendent(farm_road, affect=farm_affect)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_fork.set_descendent(cheap_road, affect=cheap_affect)

    # WHEN
    x_bad_descendents = cook_fork.get_bad_descendents()

    # THEN
    assert x_bad_descendents != {}
    assert len(x_bad_descendents) == 1
    assert x_bad_descendents.get(cheap_road) == cheap_affect


def test_ForkUnit_get_1_good_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_affect = 3
    cook_fork.set_descendent(farm_road, affect=farm_affect)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_fork.set_descendent(cheap_road, affect=cheap_affect)

    # WHEN
    x_bad_descendent = cook_fork.get_1_good()

    # THEN
    assert x_bad_descendent == farm_road


def test_ForkUnit_get_1_bad_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_affect = 3
    cook_fork.set_descendent(farm_road, affect=farm_affect)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_fork.set_descendent(cheap_road, affect=cheap_affect)

    # WHEN
    x_bad_descendent = cook_fork.get_1_bad()

    # THEN
    assert x_bad_descendent == cheap_road


def test_ForkUnit_set_descendents_CorrectlyRaisesNoneZeroAffectException():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)

    # WHEN
    cheap_road = get_road(cook_road, "cheap food")
    x_affect = 0
    with pytest_raises(Exception) as excinfo:
        cook_fork.set_descendent(cheap_road, affect=x_affect)
    assert (
        str(excinfo.value)
        == f"set_descendent affect parameter {x_affect} must be Non-zero number"
    )


def test_ForkUnit_set_descendents_CorrectlyRaisesForkSubRoadUnitException():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    go_road = "going out"
    go_cheap_road = get_road(go_road, "cheap food")

    # WHEN
    x_affect = -2
    with pytest_raises(Exception) as excinfo:
        cook_fork.set_descendent(go_cheap_road, affect=x_affect)
    assert (
        str(excinfo.value)
        == f"ForkUnit cannot set descendent '{go_cheap_road}' because base road is '{cook_road}'."
    )


def test_ForkUnit_get_all_roads_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    cheap_text = "cheap food"
    farm_text = "farm fresh"
    plastic_text = "plastic pots"
    metal_text = "metal pots"
    cook_fork.set_descendent(get_road(cook_road, cheap_text), affect=-2)
    cook_fork.set_descendent(get_road(cook_road, farm_text), affect=3)
    cook_fork.set_descendent(get_road(cook_road, plastic_text), affect=-5)
    cook_fork.set_descendent(get_road(cook_road, metal_text), affect=7)
    assert len(cook_fork.descendents) == 4

    # WHEN
    all_roads_dict = cook_fork.get_all_roads()

    # THEN
    assert len(all_roads_dict) == 5
    assert all_roads_dict.get(cook_road) != None
    cheap_road = get_road(cook_road, cheap_text)
    farm_road = get_road(cook_road, farm_text)
    plastic_road = get_road(cook_road, plastic_text)
    metal_road = get_road(cook_road, metal_text)
    assert all_roads_dict.get(cheap_road) != None
    assert all_roads_dict.get(farm_road) != None
    assert all_roads_dict.get(plastic_road) != None
    assert all_roads_dict.get(metal_road) != None
    assert len(cook_fork.descendents) == 4


def test_create_forkunit_CorrectlyReturnsObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")

    # WHEN
    farm_text = "farm food"
    cheap_text = "cheap food"
    cook_fork = create_forkunit(base=cook_road, good=farm_text, bad=cheap_text)

    # THEN
    assert cook_fork.base == cook_road
    assert cook_fork.descendents != {}
    farm_road = get_road(cook_road, farm_text)
    cheap_road = get_road(cook_road, cheap_text)
    assert cook_fork.descendents.get(farm_road) == 1
    assert cook_fork.descendents.get(cheap_road) == -1
