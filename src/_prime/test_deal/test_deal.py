# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src._prime.topic import topicunit_shop
from src._prime.deal import DealUnit, dealunit_shop
from src._prime.examples.example_topics import (
    get_cooking_topic,
    get_speedboats_action_topic,
    get_climate_topic,
    get_gasheater_action_topic,
    get_cooking_sectionunit,
    get_speedboat_action_sectionunit,
    get_climate_sectionunit,
)


def test_DealUnit_exists():
    # GIVEN / WHEN
    x_dealunit = DealUnit()

    # THEN
    assert x_dealunit._author is None
    assert x_dealunit._reader is None
    assert x_dealunit._topicunits is None
    assert x_dealunit._sectionunits is None


def test_dealunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"

    # WHEN
    farm_dealunit = dealunit_shop(_author=bob_text, _reader=tim_text)

    # THEN
    assert farm_dealunit._author == bob_text
    assert farm_dealunit._reader == tim_text
    assert farm_dealunit._topicunits == {}
    assert farm_dealunit._sectionunits == {}


def test_DealUnit_set_topicunit_SetsAttrCorrectly():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    assert farm_dealunit._topicunits == {}

    # WHEN
    cooking_topicunit = get_cooking_topic()
    farm_dealunit.set_topicunit(cooking_topicunit)

    # THEN
    assert len(farm_dealunit._topicunits) == 1
    assert farm_dealunit._topicunits.get(cooking_topicunit.base) != None
    assert farm_dealunit._topicunits.get(cooking_topicunit.base) == cooking_topicunit


def test_DealUnit_get_topicunit_ReturnsCorrectObj():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    cooking_topicunit = get_cooking_topic()
    farm_dealunit.set_topicunit(cooking_topicunit)

    # WHEN / THEN
    assert farm_dealunit.get_topicunit(cooking_topicunit.base) != None


def test_DealUnit_topicunit_exists_ReturnsCorrectObj():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    cooking_topicunit = get_cooking_topic()
    assert farm_dealunit.topicunit_exists(cooking_topicunit.base) == False

    # WHEN
    farm_dealunit.set_topicunit(cooking_topicunit)

    # THEN
    assert farm_dealunit.topicunit_exists(cooking_topicunit.base)


def test_DealUnit_del_topicunit_CorrectlySetsAttr():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    cooking_topicunit = get_cooking_topic()
    farm_dealunit.set_topicunit(cooking_topicunit)
    assert len(farm_dealunit._topicunits) == 1

    # WHEN
    farm_dealunit.del_topicunit(cooking_topicunit.base)

    # THEN
    assert len(farm_dealunit._topicunits) == 0


def test_DealUnit_set_actor_sectionunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader="Tim")
    eight_sectionunit = get_cooking_sectionunit()
    farm_dealunit.set_sectionunit(eight_sectionunit)

    cooking_sectionunit = farm_dealunit.get_sectionunit(eight_sectionunit.uid)
    assert cooking_sectionunit.get_actor(bob_text) is None

    # WHEN
    farm_dealunit.set_actor(actor=bob_text, section_uid=eight_sectionunit.uid)

    # THEN
    assert cooking_sectionunit.get_actor(bob_text) != None


def test_DealUnit_del_actor_sectionunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader="Tim")
    eight_sectionunit = get_cooking_sectionunit()
    farm_dealunit.set_sectionunit(eight_sectionunit)
    cooking_sectionunit = farm_dealunit.get_sectionunit(eight_sectionunit.uid)
    farm_dealunit.set_actor(actor=bob_text, section_uid=eight_sectionunit.uid)
    assert cooking_sectionunit.get_actor(bob_text) != None

    # WHEN
    farm_dealunit.del_actor(actor=bob_text, section_uid=eight_sectionunit.uid)

    # THEN
    assert cooking_sectionunit.get_actor(bob_text) is None


def test_DealUnit_get_actor_sectionunits_ReturnsCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader="Tim")
    eight_sectionunit = get_cooking_sectionunit()
    farm_dealunit.set_sectionunit(eight_sectionunit)
    assert farm_dealunit.get_actor_sectionunits(eight_sectionunit.uid) == {}

    # WHEN
    farm_dealunit.set_actor(bob_text, section_uid=eight_sectionunit.uid)

    # THEN
    assert farm_dealunit.get_actor_sectionunits(bob_text) != {}
    bob_sectionunits = farm_dealunit.get_actor_sectionunits(bob_text)
    assert len(bob_sectionunits) == 1
    example_cooking_sectionunit = get_cooking_sectionunit()
    example_cooking_sectionunit.set_actor(bob_text)
    assert bob_sectionunits.get(eight_sectionunit.uid) == example_cooking_sectionunit


def test_DealUnit_get_actor_sectionunits_ReturnsCorrectActionTopics():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader=yao_text)
    assert farm_dealunit.actor_has_sectionunit(bob_text, action_filter=True) == False
    assert farm_dealunit.actor_has_sectionunit(yao_text, action_filter=True) == False

    # WHEN
    farm_dealunit.set_sectionunit(get_cooking_sectionunit(), bob_text)
    farm_dealunit.set_sectionunit(get_speedboat_action_sectionunit(), yao_text)
    farm_dealunit.set_sectionunit(get_climate_sectionunit(), yao_text)

    # THEN
    assert farm_dealunit.actor_has_sectionunit(bob_text, action_filter=True) == False
    assert farm_dealunit.actor_has_sectionunit(yao_text, action_filter=True)


def test_DealUnit_set_sectionunit_WithactorSetsCorrectAttrs():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader="Tim")

    # WHEN
    farm_dealunit.set_sectionunit(get_cooking_sectionunit(), actor=bob_text)

    # THEN
    bob_sectionunits = farm_dealunit.get_actor_sectionunits(bob_text)
    assert len(bob_sectionunits) == 1
    example_cooking_sectionunit = get_cooking_sectionunit()
    example_cooking_sectionunit.set_actor(bob_text)
    assert (
        bob_sectionunits.get(get_cooking_sectionunit().uid)
        == example_cooking_sectionunit
    )


def test_DealUnit_is_meaningful_ReturnsCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"

    # WHEN
    farm_dealunit = dealunit_shop(_author=bob_text, _reader=yao_text)
    # THEN
    assert farm_dealunit.is_meaningful() == False

    # WHEN
    farm_dealunit.set_topicunit(get_cooking_topic())
    # THEN
    assert farm_dealunit.is_meaningful()

    # WHEN
    farm_dealunit.set_topicunit(get_speedboats_action_topic())
    farm_dealunit.set_topicunit(get_climate_topic())

    # THEN
    assert farm_dealunit.is_meaningful()

    # WHEN
    farm_dealunit.set_topicunit(get_gasheater_action_topic())

    # THEN
    assert farm_dealunit.is_meaningful() == False


# def test_RequestUnit_get_str_summary_ReturnsCorrectObj():
#     # GIVEN
#      = examples_get_farm_()

#     # WHEN
#     generated_farm_str = .get_str_summary()

#     # THEN
#     bob_text = "Bob"
#     real_text = "Real Farmers"
#     yao_text = "Yao"
#     texas_text = "Texas"
#     luca_text = "Luca"
#     food_text = "food"
#     farm_text = "farm food"
#     cheap_text = "cheap food"
#     action_text = "cultivate"
#     positive_text = "cultivate well"
#     negative_text = "cultivate poorly"
#     static_farm_string = f"""RequestUnit: Within {luca_text}'s {texas_text} economy subject: {food_text}
#  {cheap_text} is bad.
#  {farm_text} is good.
#  Within the action domain of '{action_text}'
#  It is good to {positive_text}
#  It is bad to {negative_text}
#  ['{bob_text}', '{yao_text}'] are in groups ['{real_text}'] and are asked to be good."""

#     assert generated_farm_str == static_farm_string
