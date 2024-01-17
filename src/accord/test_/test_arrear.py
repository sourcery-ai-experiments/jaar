# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import (
    create_road,
    get_default_economy_root_roadnode as root_label,
)
from src.accord.topic import topiclink_shop
from src.accord.accord import ArrearUnit, arrearunit_shop
from src.accord.examples.example_topics import (
    get_cooking_topic,
    get_speedboats_action_topic,
    get_climate_topic,
    get_gasheater_action_topic,
)


def test_ArrearUnit_exists():
    # GIVEN / WHEN
    x_arrearunit = ArrearUnit()

    # THEN
    assert x_arrearunit.actor is None
    assert x_arrearunit._topiclinks is None
    assert x_arrearunit.uid is None
    assert x_arrearunit.weight is None
    assert x_arrearunit._relative_accord_weight is None


def test_arrearunit_shop_ReturnsCorrectObj():
    # GIVEN
    x_uid = 5

    # WHEN
    farm_arrearunit = arrearunit_shop(x_uid)

    # THEN
    assert farm_arrearunit.uid == x_uid
    assert farm_arrearunit.actor is None
    assert farm_arrearunit._topiclinks == {}
    assert farm_arrearunit.weight == 1
    assert farm_arrearunit._relative_accord_weight == 0


def test_ArrearUnit_set_topiclink_SetsAttrCorrectly():
    # GIVEN
    one_text = "1"
    farm_arrearunit = arrearunit_shop(one_text)
    assert farm_arrearunit._topiclinks == {}

    # WHEN
    cook_topiclink = topiclink_shop(base=create_road(root_label(), "cooking"))
    farm_arrearunit.set_topiclink(cook_topiclink)

    # THEN
    assert len(farm_arrearunit._topiclinks) == 1
    assert farm_arrearunit._topiclinks.get(cook_topiclink.base) != None
    assert farm_arrearunit._topiclinks.get(cook_topiclink.base) == cook_topiclink


def test_ArrearUnit_edit_attr_SetsAttrCorrectly():
    # GIVEN
    one_text = "1"
    farm_arrearunit = arrearunit_shop(one_text)
    assert farm_arrearunit.weight == 1
    assert farm_arrearunit._relative_accord_weight == 0

    # WHEN
    new_weight = 7
    new_relative_accord_weight = 0.66
    farm_arrearunit.edit_attr(
        weight=new_weight, _relative_accord_weight=new_relative_accord_weight
    )

    # THEN
    assert farm_arrearunit.weight != 1
    assert farm_arrearunit.weight == new_weight
    assert farm_arrearunit._relative_accord_weight != 0
    assert farm_arrearunit._relative_accord_weight == new_relative_accord_weight


def test_ArrearUnit_get_topiclink_ReturnsCorrectObj():
    # GIVEN
    one_text = "1"
    farm_arrearunit = arrearunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_arrearunit.set_topiclink(topiclink_shop(base=cook_road))
    assert len(farm_arrearunit._topiclinks) == 1

    # WHEN
    cook_topiclink = farm_arrearunit.get_topiclink(cook_road)

    # THEN
    assert cook_topiclink != None
    assert cook_topiclink.base == cook_road


def test_ArrearUnit_topiclink_exists_ReturnsCorrectObj():
    # GIVEN
    one_text = "1"
    farm_arrearunit = arrearunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_arrearunit.set_topiclink(topiclink_shop(base=cook_road))
    assert len(farm_arrearunit._topiclinks) == 1

    # WHEN
    assert farm_arrearunit.topiclink_exists(cook_road)


def test_ArrearUnit_del_topiclink_CorrectlySetsAttr():
    # GIVEN
    one_text = "1"
    farm_arrearunit = arrearunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_arrearunit.set_topiclink(topiclink_shop(base=cook_road))
    assert farm_arrearunit.topiclink_exists(cook_road)

    # WHEN
    farm_arrearunit.del_topiclink(cook_road)

    # THEN
    assert farm_arrearunit.topiclink_exists(cook_road) == False


def test_ArrearUnit_set_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_arrearunit = arrearunit_shop(cook_road)
    assert cook_arrearunit.actor is None

    # WHEN
    bob_text = "Bob"
    cook_arrearunit.set_actor(x_actor=bob_text)

    # THEN
    assert cook_arrearunit.actor != None
    assert cook_arrearunit.actor == bob_text

    # WHEN
    tim_text = "Bob"
    cook_arrearunit.set_actor(x_actor=tim_text)

    # THEN
    assert cook_arrearunit.actor != None
    assert cook_arrearunit.actor == tim_text


def test_ArrearUnit_del_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_arrearunit = arrearunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_arrearunit.set_actor(bob_text)
    assert cook_arrearunit.actor == bob_text

    # WHEN
    cook_arrearunit.del_actor(bob_text)

    # THEN
    assert cook_arrearunit.actor is None


def test_ArrearUnit_get_actor_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_arrearunit = arrearunit_shop(cook_road)
    bob_text = "Bob"
    cook_arrearunit.set_actor(bob_text)

    # WHEN
    bob_actor = cook_arrearunit.get_actor(bob_text)

    # THEN
    assert bob_actor != None
    assert bob_actor == bob_text


def test_ArrearUnit_actor_exists_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_arrearunit = arrearunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    assert cook_arrearunit.actor_exists(bob_text) == False

    # WHEN / THEN
    cook_arrearunit.set_actor(bob_text)
    assert cook_arrearunit.actor_exists(bob_text)
    assert cook_arrearunit.actor_exists(yao_text) == False

    # WHEN / THEN
    cook_arrearunit.del_actor(bob_text)
    assert cook_arrearunit.actor_exists(bob_text) == False
    assert cook_arrearunit.actor_exists(yao_text) == False


def test_ArrearUnit_action_exists_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_arrearunit = arrearunit_shop(cook_road)
    assert cook_arrearunit.has_action() == False

    # WHEN
    baking_road = create_road(cook_road, "baking")
    cook_arrearunit.set_topiclink(topiclink_shop(baking_road))
    # THEN
    assert cook_arrearunit.has_action() == False

    # WHEN
    clean_road = create_road(cook_road, "clean kitchen")
    cook_arrearunit.set_topiclink(topiclink_shop(clean_road, action=True))
    # THEN
    assert cook_arrearunit.has_action()

    # WHEN
    cook_arrearunit.del_topiclink(clean_road)
    # THEN
    assert cook_arrearunit.has_action() == False
