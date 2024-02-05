from src._prime.road import get_default_market_root_roadnode as root_label, create_road
from src.x_econ.topic import (
    TopicUnit,
    topicunit_shop,
    create_topicunit,
    opinionunit_shop,
)
from pytest import raises as pytest_raises


def test_TopicUnit_set_opinionunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    assert cook_topic.opinionunits == {}

    # WHEN
    cheap_road = create_road(cook_road, "cheap food")
    x_affect = -2
    cheap_opinionunit = opinionunit_shop(cheap_road, affect=x_affect)
    cook_topic.set_opinionunit(x_opinionunit=cheap_opinionunit)

    # THEN
    assert cook_topic.opinionunits != {}
    assert cook_topic.opinionunits.get(cheap_road) != None
    assert cook_topic.opinionunits.get(cheap_road) == cheap_opinionunit


def test_TopicUnit_del_opinionunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    metal_road = create_road(cook_road, "metal pots")
    cheap_opinionunit = opinionunit_shop(cheap_road, affect=-2)
    metal_opinionunit = opinionunit_shop(metal_road, affect=3)
    cook_topic.set_opinionunit(cheap_opinionunit)
    cook_topic.set_opinionunit(metal_opinionunit)
    assert len(cook_topic.opinionunits) == 2
    assert cook_topic.opinionunits.get(cheap_road) != None
    assert cook_topic.opinionunits.get(metal_road) != None

    # WHEN
    cook_topic.del_opinionunit(cheap_road)

    # THEN
    assert len(cook_topic.opinionunits) == 1
    assert cook_topic.opinionunits.get(cheap_road) is None
    assert cook_topic.opinionunits.get(metal_road) != None


def test_TopicUnit_get_opinionunit_ReturnsCorrectObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_topic.set_opinionunit(opinionunit_shop(farm_road, farm_affect))

    # WHEN
    farm_opinionunit = cook_topic.get_opinionunit(farm_road)

    # THEN
    assert farm_opinionunit != None
    assert farm_opinionunit.road == farm_road
    assert farm_opinionunit.affect == farm_affect


def test_TopicUnit_get_opinionunits_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_opinionunit = opinionunit_shop(farm_road, farm_affect)
    cook_topic.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_topic.set_opinionunit(opinionunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_good_opinionunits = cook_topic.get_opinionunits(good=True)

    # THEN
    assert x_good_opinionunits != {}
    assert len(x_good_opinionunits) == 1
    assert x_good_opinionunits.get(farm_road) == farm_opinionunit


def test_TopicUnit_get_opinionunits_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_opinionunit = opinionunit_shop(farm_road, farm_affect)
    cook_topic.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cheap_opinionunit = opinionunit_shop(cheap_road, cheap_affect)
    cook_topic.set_opinionunit(cheap_opinionunit)

    # WHEN
    x_bad_opinionunits = cook_topic.get_opinionunits(bad=True)

    # THEN
    assert x_bad_opinionunits != {}
    assert len(x_bad_opinionunits) == 1
    assert x_bad_opinionunits.get(cheap_road) == cheap_opinionunit


def test_TopicUnit_get_1_opinionunit_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_topic.set_opinionunit(opinionunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_topic.set_opinionunit(opinionunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_opinionunit = cook_topic.get_1_opinionunit(good=True)

    # THEN
    assert x_bad_opinionunit == farm_road


def test_TopicUnit_get_1_opinionunit_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_topic.set_opinionunit(opinionunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_topic.set_opinionunit(opinionunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_opinionunit = cook_topic.get_1_opinionunit(bad=True)

    # THEN
    assert x_bad_opinionunit == cheap_road


def test_TopicUnit_get_opinionunits_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=farm_love)
    cook_topic.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_topic.set_opinionunit(opinionunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_in_tribe_opinionunits = cook_topic.get_opinionunits(in_tribe=True)

    # THEN
    assert x_in_tribe_opinionunits != {}
    assert len(x_in_tribe_opinionunits) == 1
    assert x_in_tribe_opinionunits.get(farm_road) == farm_opinionunit


def test_TopicUnit_get_opinionunits_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=farm_love)
    cook_topic.set_opinionunit(farm_opinionunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cheap_opinionunit = opinionunit_shop(cheap_road, -2, love=cheap_love)
    cook_topic.set_opinionunit(cheap_opinionunit)

    # WHEN
    x_out_tribe_opinionunits = cook_topic.get_opinionunits(out_tribe=True)

    # THEN.
    assert x_out_tribe_opinionunits != {}
    assert len(x_out_tribe_opinionunits) == 1
    assert x_out_tribe_opinionunits.get(cheap_road) == cheap_opinionunit


def test_TopicUnit_get_1_opinionunit_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_topic.set_opinionunit(opinionunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_topic.set_opinionunit(opinionunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_opinionunit = cook_topic.get_1_opinionunit(in_tribe=True)

    # THEN
    assert x_out_tribe_opinionunit == farm_road


def test_TopicUnit_get_1_opinionunit_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_topic.set_opinionunit(opinionunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_topic.set_opinionunit(opinionunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_opinionunit = cook_topic.get_1_opinionunit(out_tribe=True)

    # THEN
    assert x_out_tribe_opinionunit == cheap_road


def test_TopicUnit_set_opinionunits_CorrectlyRaisesTopicSubRoadUnitException():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    go_road = "going out"
    go_cheap_road = create_road(go_road, "cheap food")
    go_cheap_opinionunit = opinionunit_shop(go_cheap_road, affect=-3)

    # WHEN
    x_affect = -2
    with pytest_raises(Exception) as excinfo:
        cook_topic.set_opinionunit(go_cheap_opinionunit)
    assert (
        str(excinfo.value)
        == f"TopicUnit cannot set opinionunit '{go_cheap_road}' because base road is '{cook_road}'."
    )


def test_TopicUnit_get_all_roads_ReturnsCorrectObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    cheap_text = "cheap food"
    farm_text = "farm fresh"
    plastic_text = "plastic pots"
    metal_text = "metal pots"
    cook_topic.set_opinionunit(opinionunit_shop(create_road(cook_road, cheap_text), -2))
    cook_topic.set_opinionunit(opinionunit_shop(create_road(cook_road, farm_text), 3))
    cook_topic.set_opinionunit(
        opinionunit_shop(create_road(cook_road, plastic_text), -5)
    )
    cook_topic.set_opinionunit(opinionunit_shop(create_road(cook_road, metal_text), 7))
    assert len(cook_topic.opinionunits) == 4

    # WHEN
    all_roads_dict = cook_topic.get_all_roads()

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
    assert len(cook_topic.opinionunits) == 4


def test_create_topicunit_ReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    farm_text = "farm food"
    cheap_text = "cheap food"
    cook_topic = create_topicunit(base=cook_road, good=farm_text, bad=cheap_text)

    # THEN
    assert cook_topic.base == cook_road
    assert cook_topic.opinionunits != {}
    farm_road = create_road(cook_road, farm_text)
    cheap_road = create_road(cook_road, cheap_text)
    farm_opinionunit = opinionunit_shop(farm_road, 1)
    cheap_opinionunit = opinionunit_shop(cheap_road, -1)
    farm_opinionunit.set_topic_affect_ratio(1, -1)
    cheap_opinionunit.set_topic_affect_ratio(1, -1)
    farm_opinionunit.set_topic_love_ratio(1, -1)
    cheap_opinionunit.set_topic_love_ratio(1, -1)
    assert cook_topic.get_opinionunit(farm_road) == farm_opinionunit
    assert cook_topic.get_opinionunit(cheap_road) == cheap_opinionunit
