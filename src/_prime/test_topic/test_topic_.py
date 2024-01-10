from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._prime.topic import (
    TopicUnit,
    topicunit_shop,
    create_topicunit,
    factunit_shop,
)
from pytest import raises as pytest_raises


def test_TopicUnit_exists():
    # GIVEN / WHEN
    x_topic = TopicUnit()

    # THEN
    assert x_topic != None
    assert x_topic.base is None
    assert x_topic.action is None
    assert x_topic.factunits is None
    assert x_topic.delimiter is None
    assert x_topic.actors is None
    assert x_topic._calc_is_meaningful is None
    assert x_topic._calc_is_tribal is None
    assert x_topic._calc_is_dialectic is None


def test_topicunit_shop_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    cook_topic = topicunit_shop(base=cook_road)

    # THEN
    assert cook_topic.base == cook_road
    assert cook_topic.action == False
    assert cook_topic.factunits == {}
    assert cook_topic.delimiter == default_road_delimiter_if_none()
    assert cook_topic.actors == {}
    assert cook_topic._calc_is_meaningful == False
    assert cook_topic._calc_is_tribal == False
    assert cook_topic._calc_is_dialectic == False


def test_TopicUnit_set_action_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    assert cook_topic.action == False

    # WHEN / THEN
    cook_topic.set_action(True)
    assert cook_topic.action

    # WHEN / THEN
    cook_topic.set_action(False)
    assert cook_topic.action == False


def test_TopicUnit_set_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    assert cook_topic.actors == {}

    # WHEN
    bob_text = "Bob"
    cook_topic.set_actor(x_actor=bob_text)

    # THEN
    assert cook_topic.actors != {}
    assert cook_topic.actors.get(bob_text) != None
    assert cook_topic.actors.get(bob_text) == bob_text


def test_TopicUnit_del_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_topic.set_actor(bob_text)
    cook_topic.set_actor(yao_text)
    assert len(cook_topic.actors) == 2
    assert cook_topic.actors.get(bob_text) != None
    assert cook_topic.actors.get(yao_text) != None

    # WHEN
    cook_topic.del_actor(bob_text)

    # THEN
    assert len(cook_topic.actors) == 1
    assert cook_topic.actors.get(bob_text) is None
    assert cook_topic.actors.get(yao_text) != None


def test_TopicUnit_get_actor_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_topic.set_actor(bob_text)
    cook_topic.set_actor(yao_text)

    # WHEN
    bob_actor = cook_topic.get_actor(bob_text)

    # THEN
    assert bob_actor != None
    assert bob_actor == bob_text


def test_TopicUnit_actor_exists_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    assert cook_topic.actor_exists(bob_text) == False
    assert cook_topic.actor_exists(yao_text) == False

    # WHEN / THEN
    cook_topic.set_actor(bob_text)
    cook_topic.set_actor(yao_text)
    assert cook_topic.actor_exists(bob_text)
    assert cook_topic.actor_exists(yao_text)

    # WHEN / THEN
    cook_topic.del_actor(yao_text)
    assert cook_topic.actor_exists(bob_text)
    assert cook_topic.actor_exists(yao_text) == False


def test_TopicUnit_set_factunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    assert cook_topic.factunits == {}

    # WHEN
    cheap_road = create_road(cook_road, "cheap food")
    x_affect = -2
    cheap_factunit = factunit_shop(cheap_road, affect=x_affect)
    cook_topic.set_factunit(x_factunit=cheap_factunit)

    # THEN
    assert cook_topic.factunits != {}
    assert cook_topic.factunits.get(cheap_road) != None
    assert cook_topic.factunits.get(cheap_road) == cheap_factunit


def test_TopicUnit_del_factunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    metal_road = create_road(cook_road, "metal pots")
    cheap_factunit = factunit_shop(cheap_road, affect=-2)
    metal_factunit = factunit_shop(metal_road, affect=3)
    cook_topic.set_factunit(cheap_factunit)
    cook_topic.set_factunit(metal_factunit)
    assert len(cook_topic.factunits) == 2
    assert cook_topic.factunits.get(cheap_road) != None
    assert cook_topic.factunits.get(metal_road) != None

    # WHEN
    cook_topic.del_factunit(cheap_road)

    # THEN
    assert len(cook_topic.factunits) == 1
    assert cook_topic.factunits.get(cheap_road) is None
    assert cook_topic.factunits.get(metal_road) != None


def test_TopicUnit_get_factunit_ReturnsCorrectObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_topic.set_factunit(factunit_shop(farm_road, farm_affect))

    # WHEN
    farm_factunit = cook_topic.get_factunit(farm_road)

    # THEN
    assert farm_factunit != None
    assert farm_factunit.road == farm_road
    assert farm_factunit.affect == farm_affect


def test_TopicUnit_get_factunits_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_factunit = factunit_shop(farm_road, farm_affect)
    cook_topic.set_factunit(farm_factunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_topic.set_factunit(factunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_good_factunits = cook_topic.get_factunits(good=True)

    # THEN
    assert x_good_factunits != {}
    assert len(x_good_factunits) == 1
    assert x_good_factunits.get(farm_road) == farm_factunit


def test_TopicUnit_get_factunits_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_factunit = factunit_shop(farm_road, farm_affect)
    cook_topic.set_factunit(farm_factunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cheap_factunit = factunit_shop(cheap_road, cheap_affect)
    cook_topic.set_factunit(cheap_factunit)

    # WHEN
    x_bad_factunits = cook_topic.get_factunits(bad=True)

    # THEN
    assert x_bad_factunits != {}
    assert len(x_bad_factunits) == 1
    assert x_bad_factunits.get(cheap_road) == cheap_factunit


def test_TopicUnit_get_1_factunit_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_topic.set_factunit(factunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_topic.set_factunit(factunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_factunit = cook_topic.get_1_factunit(good=True)

    # THEN
    assert x_bad_factunit == farm_road


def test_TopicUnit_get_1_factunit_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_topic.set_factunit(factunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_topic.set_factunit(factunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_factunit = cook_topic.get_1_factunit(bad=True)

    # THEN
    assert x_bad_factunit == cheap_road


def test_TopicUnit_get_factunits_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_factunit = factunit_shop(farm_road, -2, love=farm_love)
    cook_topic.set_factunit(farm_factunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_topic.set_factunit(factunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_in_tribe_factunits = cook_topic.get_factunits(in_tribe=True)

    # THEN
    assert x_in_tribe_factunits != {}
    assert len(x_in_tribe_factunits) == 1
    assert x_in_tribe_factunits.get(farm_road) == farm_factunit


def test_TopicUnit_get_factunits_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_factunit = factunit_shop(farm_road, -2, love=farm_love)
    cook_topic.set_factunit(farm_factunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cheap_factunit = factunit_shop(cheap_road, -2, love=cheap_love)
    cook_topic.set_factunit(cheap_factunit)

    # WHEN
    x_out_tribe_factunits = cook_topic.get_factunits(out_tribe=True)

    # THEN.
    assert x_out_tribe_factunits != {}
    assert len(x_out_tribe_factunits) == 1
    assert x_out_tribe_factunits.get(cheap_road) == cheap_factunit


def test_TopicUnit_get_1_factunit_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_topic.set_factunit(factunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_topic.set_factunit(factunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_factunit = cook_topic.get_1_factunit(in_tribe=True)

    # THEN
    assert x_out_tribe_factunit == farm_road


def test_TopicUnit_get_1_factunit_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_topic.set_factunit(factunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_topic.set_factunit(factunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_factunit = cook_topic.get_1_factunit(out_tribe=True)

    # THEN
    assert x_out_tribe_factunit == cheap_road


def test_TopicUnit_set_factunits_CorrectlyRaisesTopicSubRoadUnitException():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    go_road = "going out"
    go_cheap_road = create_road(go_road, "cheap food")
    go_cheap_factunit = factunit_shop(go_cheap_road, affect=-3)

    # WHEN
    x_affect = -2
    with pytest_raises(Exception) as excinfo:
        cook_topic.set_factunit(go_cheap_factunit)
    assert (
        str(excinfo.value)
        == f"TopicUnit cannot set factunit '{go_cheap_road}' because base road is '{cook_road}'."
    )


def test_TopicUnit_get_all_roads_ReturnsCorrectObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    cheap_text = "cheap food"
    farm_text = "farm fresh"
    plastic_text = "plastic pots"
    metal_text = "metal pots"
    cook_topic.set_factunit(factunit_shop(create_road(cook_road, cheap_text), -2))
    cook_topic.set_factunit(factunit_shop(create_road(cook_road, farm_text), 3))
    cook_topic.set_factunit(factunit_shop(create_road(cook_road, plastic_text), -5))
    cook_topic.set_factunit(factunit_shop(create_road(cook_road, metal_text), 7))
    assert len(cook_topic.factunits) == 4

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
    assert len(cook_topic.factunits) == 4


def test_create_topicunit_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    farm_text = "farm food"
    cheap_text = "cheap food"
    cook_topic = create_topicunit(base=cook_road, good=farm_text, bad=cheap_text)

    # THEN
    assert cook_topic.base == cook_road
    assert cook_topic.factunits != {}
    farm_road = create_road(cook_road, farm_text)
    cheap_road = create_road(cook_road, cheap_text)
    farm_factunit = factunit_shop(farm_road, 1)
    cheap_factunit = factunit_shop(cheap_road, -1)
    farm_factunit.set_topic_affect_ratio(1, -1)
    cheap_factunit.set_topic_affect_ratio(1, -1)
    farm_factunit.set_topic_love_ratio(1, -1)
    cheap_factunit.set_topic_love_ratio(1, -1)
    assert cook_topic.get_factunit(farm_road) == farm_factunit
    assert cook_topic.get_factunit(cheap_road) == cheap_factunit
