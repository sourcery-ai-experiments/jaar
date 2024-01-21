from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src.deal.topic import TopicLink, topiclink_shop
from pytest import raises as pytest_raises


def test_TopicLink_exists():
    # GIVEN / WHEN
    x_topiclink = TopicLink()

    # THEN
    assert x_topiclink != None
    assert x_topiclink.base is None
    assert x_topiclink.action is None
    assert x_topiclink.weight is None


def test_topiclink_shop_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    cook_topiclink = topiclink_shop(base=cook_road)

    # THEN
    assert cook_topiclink.base == cook_road
    assert cook_topiclink.action == False
    assert cook_topiclink.weight == 1


def test_TopicLink_set_action_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topiclink = topiclink_shop(cook_road)
    assert cook_topiclink.action == False

    # WHEN / THEN
    cook_topiclink.set_action(True)
    assert cook_topiclink.action

    # WHEN / THEN
    cook_topiclink.set_action(False)
    assert cook_topiclink.action == False
