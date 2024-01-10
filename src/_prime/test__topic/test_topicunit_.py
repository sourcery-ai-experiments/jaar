from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._prime.topic import TopicUnit, topicunit_shop


def test_TopicUnit_exists():
    # GIVEN / WHEN
    x_topic = TopicUnit()

    # THEN
    assert x_topic != None
    assert x_topic.base is None
    assert x_topic.action is None
    assert x_topic.opinionunits is None
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
    assert cook_topic.opinionunits == {}
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
