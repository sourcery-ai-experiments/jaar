from src.world.deal import dealunit_shop
from src.world.examples.example_topics import (
    get_cooking_topic,
    get_speedboats_action_topic,
    get_climate_topic,
    get_gasheater_action_topic,
)


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
#     actual_text = "actual Farmers"
#     yao_text = "Yao"
#     texas_text = "Texas"
#     luca_text = "Luca"
#     food_text = "food"
#     farm_text = "farm food"
#     cheap_text = "cheap food"
#     action_text = "cultivate"
#     positive_text = "cultivate well"
#     negative_text = "cultivate poorly"
#     static_farm_string = f"""RequestUnit: Within {luca_text}'s {texas_text} market subject: {food_text}
#  {cheap_text} is bad.
#  {farm_text} is good.
#  Within the action domain of '{action_text}'
#  It is good to {positive_text}
#  It is bad to {negative_text}
#  ['{bob_text}', '{yao_text}'] are in groups ['{actual_text}'] and are asked to be good."""

#     assert generated_farm_str == static_farm_string
