# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road, get_default_economy_root_roadnode as root_label
from src._prime.topic import topiclink_shop
from src._prime.deal import SectionUnit, sectionunit_shop
from src._prime.examples.example_topics import (
    get_cooking_topic,
    get_speedboats_action_topic,
    get_climate_topic,
    get_gasheater_action_topic,
)


def test_SectionUnit_exists():
    # GIVEN / WHEN
    x_sectionunit = SectionUnit()

    # THEN
    assert x_sectionunit.actors is None
    assert x_sectionunit._topiclinks is None
    assert x_sectionunit.uid is None


def test_sectionunit_shop_ReturnsCorrectObj():
    # GIVEN
    x_uid = 5

    # WHEN
    farm_sectionunit = sectionunit_shop(x_uid)

    # THEN
    assert farm_sectionunit.uid == x_uid
    assert farm_sectionunit.actors == {}
    assert farm_sectionunit._topiclinks == {}


def test_SectionUnit_set_topiclink_SetsAttrCorrectly():
    # GIVEN
    one_text = "1"
    farm_sectionunit = sectionunit_shop(one_text)
    assert farm_sectionunit._topiclinks == {}

    # WHEN
    cook_topiclink = topiclink_shop(base=create_road(root_label(), "cooking"))
    farm_sectionunit.set_topiclink(cook_topiclink)

    # THEN
    assert len(farm_sectionunit._topiclinks) == 1
    assert farm_sectionunit._topiclinks.get(cook_topiclink.base) != None
    assert farm_sectionunit._topiclinks.get(cook_topiclink.base) == cook_topiclink


def test_SectionUnit_get_topiclink_ReturnsCorrectObj():
    # GIVEN
    one_text = "1"
    farm_sectionunit = sectionunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_sectionunit.set_topiclink(topiclink_shop(base=cook_road))
    assert len(farm_sectionunit._topiclinks) == 1

    # WHEN
    cook_topiclink = farm_sectionunit.get_topiclink(cook_road)

    # THEN
    assert cook_topiclink != None
    assert cook_topiclink.base == cook_road


def test_SectionUnit_topiclink_exists_ReturnsCorrectObj():
    # GIVEN
    one_text = "1"
    farm_sectionunit = sectionunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_sectionunit.set_topiclink(topiclink_shop(base=cook_road))
    assert len(farm_sectionunit._topiclinks) == 1

    # WHEN
    assert farm_sectionunit.topiclink_exists(cook_road)


def test_SectionUnit_del_topiclink_CorrectlySetsAttr():
    # GIVEN
    one_text = "1"
    farm_sectionunit = sectionunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_sectionunit.set_topiclink(topiclink_shop(base=cook_road))
    assert farm_sectionunit.topiclink_exists(cook_road)

    # WHEN
    farm_sectionunit.del_topiclink(cook_road)

    # THEN
    assert farm_sectionunit.topiclink_exists(cook_road) == False


def test_SectionUnit_set_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = sectionunit_shop(cook_road)
    assert cook_topic.actors == {}

    # WHEN
    bob_text = "Bob"
    cook_topic.set_actor(x_actor=bob_text)

    # THEN
    assert cook_topic.actors != {}
    assert cook_topic.actors.get(bob_text) != None
    assert cook_topic.actors.get(bob_text) == bob_text


def test_SectionUnit_del_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = sectionunit_shop(cook_road)
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


def test_SectionUnit_get_actor_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = sectionunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_topic.set_actor(bob_text)
    cook_topic.set_actor(yao_text)

    # WHEN
    bob_actor = cook_topic.get_actor(bob_text)

    # THEN
    assert bob_actor != None
    assert bob_actor == bob_text


def test_SectionUnit_actor_exists_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = sectionunit_shop(cook_road)
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
