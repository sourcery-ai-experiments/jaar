# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import (
    create_road,
    get_default_economy_root_roadnode as root_label,
)
from src.accord.topic import topiclink_shop
from src.accord.accord import DueUnit, dueunit_shop
from src.accord.examples.example_topics import (
    get_cooking_topic,
    get_speedboats_action_topic,
    get_climate_topic,
    get_gasheater_action_topic,
)


def test_DueUnit_exists():
    # GIVEN / WHEN
    x_dueunit = DueUnit()

    # THEN
    assert x_dueunit.actor is None
    assert x_dueunit._topiclinks is None
    assert x_dueunit.uid is None
    assert x_dueunit.author_weight is None
    assert x_dueunit.reader_weight is None
    assert x_dueunit._relative_author_weight is None
    assert x_dueunit._relative_reader_weight is None


def test_dueunit_shop_ReturnsCorrectObj():
    # GIVEN
    x_uid = 5

    # WHEN
    farm_dueunit = dueunit_shop(x_uid)

    # THEN
    assert farm_dueunit.uid == x_uid
    assert farm_dueunit.actor is None
    assert farm_dueunit._topiclinks == {}
    assert farm_dueunit.author_weight == 1
    assert farm_dueunit.reader_weight == 1
    assert farm_dueunit._relative_author_weight == 0
    assert farm_dueunit._relative_reader_weight == 0


def test_DueUnit_set_topiclink_SetsAttrCorrectly():
    # GIVEN
    one_text = "1"
    farm_dueunit = dueunit_shop(one_text)
    assert farm_dueunit._topiclinks == {}

    # WHEN
    cook_topiclink = topiclink_shop(base=create_road(root_label(), "cooking"))
    farm_dueunit.set_topiclink(cook_topiclink)

    # THEN
    assert len(farm_dueunit._topiclinks) == 1
    assert farm_dueunit._topiclinks.get(cook_topiclink.base) != None
    assert farm_dueunit._topiclinks.get(cook_topiclink.base) == cook_topiclink


def test_DueUnit_edit_attr_SetsAttrCorrectly():
    # GIVEN
    one_text = "1"
    farm_dueunit = dueunit_shop(one_text)
    assert farm_dueunit.author_weight == 1
    assert farm_dueunit.reader_weight == 1
    assert farm_dueunit._relative_author_weight == 0
    assert farm_dueunit._relative_reader_weight == 0

    # WHEN
    new_author_weight = 7
    new_reader_weight = 7
    new_relative_author_weight = 0.66
    new_relative_reader_weight = 0.43
    farm_dueunit.edit_attr(
        author_weight=new_author_weight,
        reader_weight=new_reader_weight,
        _relative_author_weight=new_relative_author_weight,
        _relative_reader_weight=new_relative_reader_weight,
    )

    # THEN
    assert farm_dueunit.author_weight != 1
    assert farm_dueunit.reader_weight != 1
    assert farm_dueunit.author_weight == new_author_weight
    assert farm_dueunit.reader_weight == new_reader_weight
    assert farm_dueunit._relative_author_weight != 0
    assert farm_dueunit._relative_reader_weight != 0
    assert farm_dueunit._relative_author_weight == new_relative_author_weight
    assert farm_dueunit._relative_reader_weight == new_relative_reader_weight


def test_DueUnit_get_topiclink_ReturnsCorrectObj():
    # GIVEN
    one_text = "1"
    farm_dueunit = dueunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_dueunit.set_topiclink(topiclink_shop(base=cook_road))
    assert len(farm_dueunit._topiclinks) == 1

    # WHEN
    cook_topiclink = farm_dueunit.get_topiclink(cook_road)

    # THEN
    assert cook_topiclink != None
    assert cook_topiclink.base == cook_road


def test_DueUnit_topiclink_exists_ReturnsCorrectObj():
    # GIVEN
    one_text = "1"
    farm_dueunit = dueunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_dueunit.set_topiclink(topiclink_shop(base=cook_road))
    assert len(farm_dueunit._topiclinks) == 1

    # WHEN
    assert farm_dueunit.topiclink_exists(cook_road)


def test_DueUnit_del_topiclink_CorrectlySetsAttr():
    # GIVEN
    one_text = "1"
    farm_dueunit = dueunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_dueunit.set_topiclink(topiclink_shop(base=cook_road))
    assert farm_dueunit.topiclink_exists(cook_road)

    # WHEN
    farm_dueunit.del_topiclink(cook_road)

    # THEN
    assert farm_dueunit.topiclink_exists(cook_road) == False


def test_DueUnit_set_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_dueunit = dueunit_shop(cook_road)
    assert cook_dueunit.actor is None

    # WHEN
    bob_text = "Bob"
    cook_dueunit.set_actor(x_actor=bob_text)

    # THEN
    assert cook_dueunit.actor != None
    assert cook_dueunit.actor == bob_text

    # WHEN
    tim_text = "Bob"
    cook_dueunit.set_actor(x_actor=tim_text)

    # THEN
    assert cook_dueunit.actor != None
    assert cook_dueunit.actor == tim_text


def test_DueUnit_del_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_dueunit = dueunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_dueunit.set_actor(bob_text)
    assert cook_dueunit.actor == bob_text

    # WHEN
    cook_dueunit.del_actor(bob_text)

    # THEN
    assert cook_dueunit.actor is None


def test_DueUnit_get_actor_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_dueunit = dueunit_shop(cook_road)
    bob_text = "Bob"
    cook_dueunit.set_actor(bob_text)

    # WHEN
    bob_actor = cook_dueunit.get_actor(bob_text)

    # THEN
    assert bob_actor != None
    assert bob_actor == bob_text


def test_DueUnit_actor_exists_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_dueunit = dueunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    assert cook_dueunit.actor_exists(bob_text) == False

    # WHEN / THEN
    cook_dueunit.set_actor(bob_text)
    assert cook_dueunit.actor_exists(bob_text)
    assert cook_dueunit.actor_exists(yao_text) == False

    # WHEN / THEN
    cook_dueunit.del_actor(bob_text)
    assert cook_dueunit.actor_exists(bob_text) == False
    assert cook_dueunit.actor_exists(yao_text) == False


def test_DueUnit_action_exists_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_dueunit = dueunit_shop(cook_road)
    assert cook_dueunit.has_action() == False

    # WHEN
    baking_road = create_road(cook_road, "baking")
    cook_dueunit.set_topiclink(topiclink_shop(baking_road))
    # THEN
    assert cook_dueunit.has_action() == False

    # WHEN
    clean_road = create_road(cook_road, "clean kitchen")
    cook_dueunit.set_topiclink(topiclink_shop(clean_road, action=True))
    # THEN
    assert cook_dueunit.has_action()

    # WHEN
    cook_dueunit.del_topiclink(clean_road)
    # THEN
    assert cook_dueunit.has_action() == False
