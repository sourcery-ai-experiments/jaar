from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src.accord.topic import TopicUnit, topicunit_shop


def test_TopicUnit_exists():
    # GIVEN / WHEN
    x_topic = TopicUnit()

    # THEN
    assert x_topic != None
    assert x_topic.base is None
    assert x_topic.suff_idea_active_status is None
    assert x_topic.opinionunits is None
    assert x_topic.delimiter is None
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
    assert cook_topic.suff_idea_active_status is None
    assert cook_topic.opinionunits == {}
    assert cook_topic.delimiter == default_road_delimiter_if_none()
    assert cook_topic._calc_is_meaningful == False
    assert cook_topic._calc_is_tribal == False
    assert cook_topic._calc_is_dialectic == False
