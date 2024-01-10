# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src._prime.issue import issueunit_shop
from src.world.deal import DealUnit, dealunit_shop
from src._prime.examples.example_issues import (
    get_cooking_issue,
    get_speedboats_action_issue,
    get_climate_issue,
    get_gasheater_action_issue,
)


def test_DealUnit_exists():
    # GIVEN / WHEN
    x_dealunit = DealUnit()

    # THEN
    assert x_dealunit._author is None
    assert x_dealunit._reader is None
    assert x_dealunit._issueunits is None


def test_dealunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"

    # WHEN
    farm_dealunit = dealunit_shop(_author=bob_text, _reader=tim_text)

    # THEN
    assert farm_dealunit._author == bob_text
    assert farm_dealunit._reader == tim_text
    assert farm_dealunit._issueunits == {}


def test_DealUnit_set_issueunit_SetsAttrCorrectly():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    assert farm_dealunit._issueunits == {}

    # WHEN
    cooking_issueunit = get_cooking_issue()
    farm_dealunit.set_issueunit(cooking_issueunit)

    # THEN
    assert len(farm_dealunit._issueunits) == 1
    assert farm_dealunit._issueunits.get(cooking_issueunit.base) != None
    assert farm_dealunit._issueunits.get(cooking_issueunit.base) == cooking_issueunit


def test_DealUnit_get_issueunit_ReturnsCorrectObj():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    cooking_issueunit = get_cooking_issue()
    farm_dealunit.set_issueunit(cooking_issueunit)

    # WHEN / THEN
    assert farm_dealunit.get_issueunit(cooking_issueunit.base) != None


def test_DealUnit_issueunit_exists_ReturnsCorrectObj():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    cooking_issueunit = get_cooking_issue()
    assert farm_dealunit.issueunit_exists(cooking_issueunit.base) == False

    # WHEN
    farm_dealunit.set_issueunit(cooking_issueunit)

    # THEN
    assert farm_dealunit.issueunit_exists(cooking_issueunit.base)


def test_DealUnit_del_issueunit_CorrectlySetsAttr():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    cooking_issueunit = get_cooking_issue()
    farm_dealunit.set_issueunit(cooking_issueunit)
    assert len(farm_dealunit._issueunits) == 1

    # WHEN
    farm_dealunit.del_issueunit(cooking_issueunit.base)

    # THEN
    assert len(farm_dealunit._issueunits) == 0


def test_DealUnit_set_actor_issueunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader="Tim")
    farm_dealunit.set_issueunit(get_cooking_issue())

    cooking_base = get_cooking_issue().base
    cooking_issueunit = farm_dealunit.get_issueunit(cooking_base)
    assert cooking_issueunit.get_actor(bob_text) is None

    # WHEN
    farm_dealunit.set_actor(actor=bob_text, issuebase=cooking_base)

    # THEN
    assert cooking_issueunit.get_actor(bob_text) != None


def test_DealUnit_del_actor_issueunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader="Tim")
    farm_dealunit.set_issueunit(get_cooking_issue())

    cooking_base = get_cooking_issue().base
    cooking_issueunit = farm_dealunit.get_issueunit(cooking_base)
    farm_dealunit.set_actor(actor=bob_text, issuebase=cooking_base)
    assert cooking_issueunit.get_actor(bob_text) != None

    # WHEN
    farm_dealunit.del_actor(actor=bob_text, issuebase=cooking_base)

    # THEN
    assert cooking_issueunit.get_actor(bob_text) is None


def test_DealUnit_get_actor_issueunits_ReturnsCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader="Tim")
    farm_dealunit.set_issueunit(get_cooking_issue())
    assert farm_dealunit.get_actor_issueunits(bob_text) == {}

    # WHEN
    cooking_base = get_cooking_issue().base
    farm_dealunit.get_issueunit(cooking_base)
    farm_dealunit.set_actor(actor=bob_text, issuebase=cooking_base)

    # THEN
    assert farm_dealunit.get_actor_issueunits(bob_text) != {}
    bob_issueunits = farm_dealunit.get_actor_issueunits(bob_text)
    assert len(bob_issueunits) == 1
    example_cooking_issueunit = get_cooking_issue()
    example_cooking_issueunit.set_actor(bob_text)
    assert bob_issueunits.get(cooking_base) == example_cooking_issueunit


def test_DealUnit_get_actor_issueunits_ReturnsCorrectActionIssues():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader=yao_text)
    assert farm_dealunit.actor_has_issue(bob_text, action_filter=True) == False
    assert farm_dealunit.actor_has_issue(yao_text, action_filter=True) == False

    # WHEN
    farm_dealunit.set_issueunit(get_cooking_issue(), bob_text)
    farm_dealunit.set_issueunit(get_speedboats_action_issue(), yao_text)
    farm_dealunit.set_issueunit(get_climate_issue(), yao_text)

    # THEN
    assert farm_dealunit.actor_has_issue(bob_text, action_filter=True) == False
    assert farm_dealunit.actor_has_issue(yao_text, action_filter=True)


def test_DealUnit_set_issueunit_WithactorSetsCorrectAttrs():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader="Tim")

    # WHEN
    farm_dealunit.set_issueunit(get_cooking_issue(), actor=bob_text)

    # THEN
    bob_issueunits = farm_dealunit.get_actor_issueunits(bob_text)
    assert len(bob_issueunits) == 1
    example_cooking_issueunit = get_cooking_issue()
    example_cooking_issueunit.set_actor(bob_text)
    cooking_base = get_cooking_issue().base
    assert bob_issueunits.get(cooking_base) == example_cooking_issueunit


def test_DealUnit_actors_has_issues_ReturnsCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_dealunit = dealunit_shop(_author=bob_text, _reader=yao_text)
    farm_dealunit.set_issueunit(get_cooking_issue(), bob_text)

    # WHEN / THEN
    bob_list = [bob_text]
    assert farm_dealunit.actors_has_issues(bob_list)
    bob_yao_list = [bob_text, yao_text]
    assert farm_dealunit.actors_has_issues(bob_yao_list) == False

    # WHEN / THEN
    farm_dealunit.set_issueunit(get_speedboats_action_issue(), yao_text)
    farm_dealunit.set_issueunit(get_climate_issue(), yao_text)
    assert farm_dealunit.actors_has_issues(bob_yao_list)


def test_DealUnit_is_meaningful_ReturnsCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"

    # WHEN
    farm_dealunit = dealunit_shop(_author=bob_text, _reader=yao_text)
    # THEN
    assert farm_dealunit.is_meaningful() == False

    # WHEN
    farm_dealunit.set_issueunit(get_cooking_issue(), bob_text)
    # THEN
    assert farm_dealunit.is_meaningful()

    # WHEN
    farm_dealunit.set_issueunit(get_speedboats_action_issue(), yao_text)
    farm_dealunit.set_issueunit(get_climate_issue(), yao_text)

    # THEN
    assert farm_dealunit.is_meaningful()

    # WHEN
    farm_dealunit.set_issueunit(get_gasheater_action_issue(), yao_text)

    # THEN
    assert farm_dealunit.is_meaningful() == False


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
