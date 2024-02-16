from src._road.road import create_road, get_default_econ_root_roadnode as root_label
from src.world.topic import topiclink_shop
from src.world.deal import VowUnit, vowunit_shop


def test_VowUnit_exists():
    # GIVEN / WHEN
    x_vowunit = VowUnit()

    # THEN
    assert x_vowunit.actor is None
    assert x_vowunit._topiclinks is None
    assert x_vowunit.uid is None
    assert x_vowunit.author_weight is None
    assert x_vowunit.reader_weight is None
    assert x_vowunit._relative_author_weight is None
    assert x_vowunit._relative_reader_weight is None


def test_vowunit_shop_ReturnsCorrectObj():
    # GIVEN
    x_uid = 5

    # WHEN
    farm_vowunit = vowunit_shop(x_uid)

    # THEN
    assert farm_vowunit.uid == x_uid
    assert farm_vowunit.actor is None
    assert farm_vowunit._topiclinks == {}
    assert farm_vowunit.author_weight == 1
    assert farm_vowunit.reader_weight == 1
    assert farm_vowunit._relative_author_weight == 0
    assert farm_vowunit._relative_reader_weight == 0


def test_VowUnit_set_topiclink_SetsAttrCorrectly():
    # GIVEN
    one_text = "1"
    farm_vowunit = vowunit_shop(one_text)
    assert farm_vowunit._topiclinks == {}

    # WHEN
    cook_topiclink = topiclink_shop(base=create_road(root_label(), "cooking"))
    farm_vowunit.set_topiclink(cook_topiclink)

    # THEN
    assert len(farm_vowunit._topiclinks) == 1
    assert farm_vowunit._topiclinks.get(cook_topiclink.base) != None
    assert farm_vowunit._topiclinks.get(cook_topiclink.base) == cook_topiclink


def test_VowUnit_edit_attr_SetsAttrCorrectly():
    # GIVEN
    one_text = "1"
    farm_vowunit = vowunit_shop(one_text)
    assert farm_vowunit.author_weight == 1
    assert farm_vowunit.reader_weight == 1
    assert farm_vowunit._relative_author_weight == 0
    assert farm_vowunit._relative_reader_weight == 0

    # WHEN
    new_author_weight = 7
    new_reader_weight = 7
    new_relative_author_weight = 0.66
    new_relative_reader_weight = 0.43
    farm_vowunit.edit_attr(
        author_weight=new_author_weight,
        reader_weight=new_reader_weight,
        _relative_author_weight=new_relative_author_weight,
        _relative_reader_weight=new_relative_reader_weight,
    )

    # THEN
    assert farm_vowunit.author_weight != 1
    assert farm_vowunit.reader_weight != 1
    assert farm_vowunit.author_weight == new_author_weight
    assert farm_vowunit.reader_weight == new_reader_weight
    assert farm_vowunit._relative_author_weight != 0
    assert farm_vowunit._relative_reader_weight != 0
    assert farm_vowunit._relative_author_weight == new_relative_author_weight
    assert farm_vowunit._relative_reader_weight == new_relative_reader_weight


def test_VowUnit_get_topiclink_ReturnsCorrectObj():
    # GIVEN
    one_text = "1"
    farm_vowunit = vowunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_vowunit.set_topiclink(topiclink_shop(base=cook_road))
    assert len(farm_vowunit._topiclinks) == 1

    # WHEN
    cook_topiclink = farm_vowunit.get_topiclink(cook_road)

    # THEN
    assert cook_topiclink != None
    assert cook_topiclink.base == cook_road


def test_VowUnit_topiclink_exists_ReturnsCorrectObj():
    # GIVEN
    one_text = "1"
    farm_vowunit = vowunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_vowunit.set_topiclink(topiclink_shop(base=cook_road))
    assert len(farm_vowunit._topiclinks) == 1

    # WHEN
    assert farm_vowunit.topiclink_exists(cook_road)


def test_VowUnit_del_topiclink_CorrectlySetsAttr():
    # GIVEN
    one_text = "1"
    farm_vowunit = vowunit_shop(one_text)
    cook_road = create_road(root_label(), "cooking")
    farm_vowunit.set_topiclink(topiclink_shop(base=cook_road))
    assert farm_vowunit.topiclink_exists(cook_road)

    # WHEN
    farm_vowunit.del_topiclink(cook_road)

    # THEN
    assert farm_vowunit.topiclink_exists(cook_road) == False


def test_VowUnit_set_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_vowunit = vowunit_shop(cook_road)
    assert cook_vowunit.actor is None

    # WHEN
    bob_text = "Bob"
    cook_vowunit.set_actor(x_actor=bob_text)

    # THEN
    assert cook_vowunit.actor != None
    assert cook_vowunit.actor == bob_text

    # WHEN
    tim_text = "Bob"
    cook_vowunit.set_actor(x_actor=tim_text)

    # THEN
    assert cook_vowunit.actor != None
    assert cook_vowunit.actor == tim_text


def test_VowUnit_del_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_vowunit = vowunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_vowunit.set_actor(bob_text)
    assert cook_vowunit.actor == bob_text

    # WHEN
    cook_vowunit.del_actor(bob_text)

    # THEN
    assert cook_vowunit.actor is None


def test_VowUnit_get_actor_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_vowunit = vowunit_shop(cook_road)
    bob_text = "Bob"
    cook_vowunit.set_actor(bob_text)

    # WHEN
    bob_actor = cook_vowunit.get_actor(bob_text)

    # THEN
    assert bob_actor != None
    assert bob_actor == bob_text


def test_VowUnit_actor_exists_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_vowunit = vowunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    assert cook_vowunit.actor_exists(bob_text) == False

    # WHEN / THEN
    cook_vowunit.set_actor(bob_text)
    assert cook_vowunit.actor_exists(bob_text)
    assert cook_vowunit.actor_exists(yao_text) == False

    # WHEN / THEN
    cook_vowunit.del_actor(bob_text)
    assert cook_vowunit.actor_exists(bob_text) == False
    assert cook_vowunit.actor_exists(yao_text) == False


def test_VowUnit_action_exists_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_vowunit = vowunit_shop(cook_road)
    assert cook_vowunit.has_action() == False

    # WHEN
    baking_road = create_road(cook_road, "baking")
    cook_vowunit.set_topiclink(topiclink_shop(baking_road))
    # THEN
    assert cook_vowunit.has_action() == False

    # WHEN
    clean_road = create_road(cook_road, "clean kitchen")
    cook_vowunit.set_topiclink(topiclink_shop(clean_road, action=True))
    # THEN
    assert cook_vowunit.has_action()

    # WHEN
    cook_vowunit.del_topiclink(clean_road)
    # THEN
    assert cook_vowunit.has_action() == False
