# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src._prime.belief import beliefunit_shop
from src.world.deal import DealUnit, dealunit_shop
from src.world.examples.example_beliefs import get_cooking_beliefunit


def test_DealUnit_exists():
    # GIVEN / WHEN
    x_dealunit = DealUnit()

    # THEN
    assert x_dealunit._author is None
    assert x_dealunit._reader is None
    assert x_dealunit._beliefunits is None


def test_dealunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"

    # WHEN
    farm_dealunit = dealunit_shop(_author=bob_text, _reader=tim_text)

    # THEN
    assert farm_dealunit._author == bob_text
    assert farm_dealunit._reader == tim_text
    assert farm_dealunit._beliefunits == {}


def test_DealUnit_set_beliefunit_SetsAttrCorrectly():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    assert farm_dealunit._beliefunits == {}

    # WHEN
    cooking_beliefunit = get_cooking_beliefunit()
    farm_dealunit.set_beliefunit(cooking_beliefunit)

    # THEN
    assert len(farm_dealunit._beliefunits) == 1
    assert farm_dealunit._beliefunits.get(cooking_beliefunit.base) != None
    assert farm_dealunit._beliefunits.get(cooking_beliefunit.base) == cooking_beliefunit


def test_DealUnit_get_beliefunit_ReturnsCorrectObj():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    cooking_beliefunit = get_cooking_beliefunit()
    farm_dealunit.set_beliefunit(cooking_beliefunit)

    # WHEN / THEN
    assert farm_dealunit.get_beliefunit(cooking_beliefunit.base) != None


def test_DealUnit_del_beliefunit_CorrectlySetsAttr():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    cooking_beliefunit = get_cooking_beliefunit()
    farm_dealunit.set_beliefunit(cooking_beliefunit)
    assert len(farm_dealunit._beliefunits) == 1

    # WHEN
    farm_dealunit.del_beliefunit(cooking_beliefunit.base)

    # THEN
    assert len(farm_dealunit._beliefunits) == 0


# def test_create_dealunit_ReturnsCorrectObj():
#     # GIVEN
#     farm_requestunit = examples_get_farm_requestunit()

#     # WHEN
#     bob_text = "Bob"
#     farm_requestunit = create_requestunit(farm_wantunit, requestee_pid=bob_text)

#     # THEN
#     assert farm_requestunit._wantunit == farm_wantunit
#     assert farm_requestunit._action_weight == 1
#     bob_dict = {bob_text: None}
#     assert farm_requestunit._requestee_pids == bob_dict
#     bob_group_dict = {bob_text: bob_text}
#     assert farm_requestunit._requestee_groups == bob_group_dict
#     assert farm_requestunit._requester_pid == "Luca"


# def test_RequestUnit_get_str_summary_ReturnsCorrectObj():
#     # GIVEN
#     farm_requestunit = examples_get_farm_requestunit()

#     # WHEN
#     generated_farm_str = farm_requestunit.get_str_summary()

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
