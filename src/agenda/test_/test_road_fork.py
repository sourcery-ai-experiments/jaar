from src.agenda.road import (
    RoadPath,
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
    get_default_culture_root_label as root_label,
    get_road_from_nodes,
    get_road_from_road_and_node,
    RoadNode,
    get_diff_road,
    get_road,
    is_heir_road,
    get_node_delimiter,
    replace_road_node_delimiter,
    ForkRoad,
    forkroad_shop,
    create_forkroad,
)
from src.agenda.required_idea import sufffactunit_shop
from src.agenda.idea import IdeaCore
from pytest import raises as pytest_raises


def test_ForkRoad_exists():
    # GIVEN / WHEN
    x_fork = ForkRoad()

    # THEN
    assert x_fork != None
    assert x_fork.base is None
    assert x_fork.descendents is None
    assert x_fork.delimiter is None


def test_ForkRoad_set_descendents_empty_if_none_CorrectlySetsAttr():
    # GIVEN
    x_fork = ForkRoad()
    assert x_fork.descendents is None

    # WHEN
    x_fork.set_descendents_empty_if_none()

    # THEN
    assert x_fork.descendents == {}


def test_forkroad_shop_CorrectlyReturnsObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")

    # WHEN
    cook_fork = forkroad_shop(base=cook_road)

    # THEN
    assert cook_fork.base == cook_road
    assert cook_fork.descendents == {}
    assert cook_fork.delimiter == get_node_delimiter()


def test_ForkRoad_set_descendents_CorrectlySetsAttr():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkroad_shop(cook_road)
    assert cook_fork.descendents == {}

    # WHEN
    cheap_road = get_road(cook_road, "cheap food")
    x_sway = -2
    cook_fork.set_descendent(cheap_road, sway=x_sway)

    # THEN
    assert cook_fork.descendents != {}
    assert cook_fork.descendents.get(cheap_road) != None
    assert cook_fork.descendents.get(cheap_road) == x_sway


def test_ForkRoad_get_good_descendents_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkroad_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_sway = 3
    cook_fork.set_descendent(farm_road, sway=farm_sway)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_sway = -3
    cook_fork.set_descendent(cheap_road, sway=cheap_sway)

    # WHEN
    x_good_descendents = cook_fork.get_good_descendents()

    # THEN
    assert x_good_descendents != {}
    assert len(x_good_descendents) == 1
    assert x_good_descendents.get(farm_road) == farm_sway


def test_ForkRoad_get_bad_descendents_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkroad_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_sway = 3
    cook_fork.set_descendent(farm_road, sway=farm_sway)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_sway = -3
    cook_fork.set_descendent(cheap_road, sway=cheap_sway)

    # WHEN
    x_bad_descendents = cook_fork.get_bad_descendents()

    # THEN
    assert x_bad_descendents != {}
    assert len(x_bad_descendents) == 1
    assert x_bad_descendents.get(cheap_road) == cheap_sway


def test_ForkRoad_get_1_good_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkroad_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_sway = 3
    cook_fork.set_descendent(farm_road, sway=farm_sway)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_sway = -3
    cook_fork.set_descendent(cheap_road, sway=cheap_sway)

    # WHEN
    x_bad_descendent = cook_fork.get_1_good()

    # THEN
    assert x_bad_descendent == farm_road


def test_ForkRoad_get_1_bad_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkroad_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_sway = 3
    cook_fork.set_descendent(farm_road, sway=farm_sway)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_sway = -3
    cook_fork.set_descendent(cheap_road, sway=cheap_sway)

    # WHEN
    x_bad_descendent = cook_fork.get_1_bad()

    # THEN
    assert x_bad_descendent == cheap_road


def test_ForkRoad_set_descendents_CorrectlyRaisesNoneZeroSwayException():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkroad_shop(cook_road)

    # WHEN
    cheap_road = get_road(cook_road, "cheap food")
    x_sway = 0
    with pytest_raises(Exception) as excinfo:
        cook_fork.set_descendent(cheap_road, sway=x_sway)
    assert (
        str(excinfo.value)
        == f"set_descendent sway parameter {x_sway} must be Non-zero number"
    )


def test_ForkRoad_set_descendents_CorrectlyRaisesForkSubRoadPathException():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkroad_shop(cook_road)
    go_road = "going out"
    go_cheap_road = get_road(go_road, "cheap food")

    # WHEN
    x_sway = -2
    with pytest_raises(Exception) as excinfo:
        cook_fork.set_descendent(go_cheap_road, sway=x_sway)
    assert (
        str(excinfo.value)
        == f"ForkRoad cannot set descendent '{go_cheap_road}' because base road is '{cook_road}'."
    )

    # _concern_subject: RoadPath = None
    # _concern_good: RoadPath = None  # cause that is wanted
    # _concern_bad: RoadPath = None  # pain and cause is not wanted
    # farm_road = get_road("farm food", sway=3)


def test_create_forkroad_CorrectlyReturnsObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")

    # WHEN
    farm_text = "farm food"
    cheap_text = "cheap food"
    cook_fork = create_forkroad(base=cook_road, good=farm_text, bad=cheap_text)

    # THEN
    assert cook_fork.base == cook_road
    assert cook_fork.descendents != {}
    farm_road = get_road(cook_road, farm_text)
    cheap_road = get_road(cook_road, cheap_text)
    assert cook_fork.descendents.get(farm_road) == 1
    assert cook_fork.descendents.get(cheap_road) == -1
