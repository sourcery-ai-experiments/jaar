# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src.world.deal import dealunit_shop, vowunit_shop
from src.world.examples.example_topics import (
    get_cooking_vowunit,
    get_speedboat_action_vowunit,
    get_climate_vowunit,
)
from pytest import raises as pytest_raises


def test_DealUnit_set_vowunit_SetsAttrCorrectly():
    # GIVEN
    farm_dealunit = dealunit_shop(_author_road="Bob", _reader_road="Tim")
    assert farm_dealunit._vowunits == {}

    # WHEN
    x_uid = 7
    x_author_weight = 3
    x_reader_weight = 9
    farm_dealunit.set_vowunit(vowunit_shop(x_uid, x_author_weight, x_reader_weight))

    # THEN
    assert len(farm_dealunit._vowunits) == 1
    assert farm_dealunit._vowunits.get(x_uid) != None
    x_vowunit = farm_dealunit._vowunits.get(x_uid)
    assert x_vowunit.author_weight == x_author_weight
    assert x_vowunit.reader_weight == x_reader_weight
    assert x_vowunit == vowunit_shop(x_uid, x_author_weight, x_reader_weight)


def test_DealUnit_get_vowunit_ReturnsCorrectObj():
    # GIVEN
    farm_dealunit = dealunit_shop(_author_road="Bob", _reader_road="Tim")
    one_text = "1"
    farm_dealunit.set_vowunit(vowunit_shop(one_text))

    # WHEN / THEN
    assert farm_dealunit.get_vowunit(one_text) != None


def test_DealUnit_vowunit_exists_ReturnsCorrectObj():
    # GIVEN
    farm_dealunit = dealunit_shop(_author_road="Bob", _reader_road="Tim")
    one_text = "1"
    assert farm_dealunit.vowunit_exists(one_text) == False

    # WHEN
    farm_dealunit.set_vowunit(vowunit_shop(one_text))

    # THEN
    assert farm_dealunit.vowunit_exists(one_text)


def test_DealUnit_del_vowunit_CorrectlySetsAttr():
    # GIVEN
    farm_dealunit = dealunit_shop(_author_road="Bob", _reader_road="Tim")
    one_text = "1"
    farm_dealunit.set_vowunit(vowunit_shop(one_text))
    assert farm_dealunit.vowunit_exists(one_text)

    # WHEN
    farm_dealunit.del_vowunit(one_text)

    # THEN
    assert farm_dealunit.vowunit_exists(one_text) == False


def test_DealUnit_add_vowunit_SetsAttrCorrectly():
    # GIVEN
    farm_dealunit = dealunit_shop(_author_road="Bob", _reader_road="Tim")
    assert farm_dealunit._vowunits == {}

    # WHEN
    one_vowunit = farm_dealunit.add_vowunit()

    # THEN
    assert one_vowunit.uid == 1
    assert one_vowunit.get_vow_id() == "Vow 0001"
    assert len(farm_dealunit._vowunits) == 1
    assert farm_dealunit.get_vowunit(one_vowunit.uid) != None

    # WHEN
    two_vowunit = farm_dealunit.add_vowunit()

    # THEN
    assert two_vowunit.uid == 2
    assert two_vowunit.get_vow_id() == "Vow 0002"
    assert len(farm_dealunit._vowunits) == 2
    assert farm_dealunit.get_vowunit(two_vowunit.uid) != None

    x_int = 7
    farm_dealunit.set_vowunit(vowunit_shop(x_int))
    assert len(farm_dealunit._vowunits) == 3

    # WHEN
    eight_vowunit = farm_dealunit.add_vowunit()

    # THEN
    assert eight_vowunit.uid == 8
    assert eight_vowunit.get_vow_id() == "Vow 0008"
    assert len(farm_dealunit._vowunits) == 4
    assert farm_dealunit.get_vowunit(eight_vowunit.uid) != None


def test_DealUnit_edit_vowunit_attr_CorrectlySetsAttribute():
    # GIVEN
    tim_text = "Tim"
    farm_dealunit = dealunit_shop(_author_road="Bob", _reader_road=tim_text)
    x_uid = 7
    x_author_weight = 3
    x_reader_weight = 3
    farm_dealunit.set_vowunit(vowunit_shop(x_uid, x_author_weight, x_reader_weight))

    x_vowunit = farm_dealunit._vowunits.get(x_uid)
    assert x_vowunit.author_weight == x_author_weight
    assert x_vowunit.reader_weight == x_reader_weight
    assert x_vowunit.actor is None

    # WHEN
    y_author_weight = 7
    y_reader_weight = 15
    farm_dealunit.edit_vowunit_attr(
        x_uid,
        author_weight=y_author_weight,
        reader_weight=y_reader_weight,
        actor=tim_text,
    )

    # THEN
    x_vowunit = farm_dealunit._vowunits.get(x_uid)
    assert x_vowunit.author_weight != x_author_weight
    assert x_vowunit.reader_weight != x_reader_weight
    assert x_vowunit.author_weight == y_author_weight
    assert x_vowunit.reader_weight == y_reader_weight
    assert x_vowunit.actor != None
    assert x_vowunit.actor == tim_text


def test_DealUnit_set_actor_vowunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road="Tim")
    eight_vowunit = get_cooking_vowunit()
    farm_dealunit.set_vowunit(eight_vowunit)

    cooking_vowunit = farm_dealunit.get_vowunit(eight_vowunit.uid)
    assert cooking_vowunit.get_actor(bob_text) is None

    # WHEN
    farm_dealunit.set_actor(actor=bob_text, vow_uid=eight_vowunit.uid)

    # THEN
    assert cooking_vowunit.get_actor(bob_text) != None


def test_DealUnit_del_actor_vowunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road="Tim")
    eight_vowunit = get_cooking_vowunit()
    farm_dealunit.set_vowunit(eight_vowunit)
    cooking_vowunit = farm_dealunit.get_vowunit(eight_vowunit.uid)
    farm_dealunit.set_actor(actor=bob_text, vow_uid=eight_vowunit.uid)
    assert cooking_vowunit.get_actor(bob_text) != None

    # WHEN
    farm_dealunit.del_actor(actor=bob_text, vow_uid=eight_vowunit.uid)

    # THEN
    assert cooking_vowunit.get_actor(bob_text) is None


def test_DealUnit_get_actor_vowunits_ReturnsCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road="Tim")
    eight_vowunit = get_cooking_vowunit()
    farm_dealunit.set_vowunit(eight_vowunit)
    assert farm_dealunit.get_actor_vowunits(eight_vowunit.uid) == {}

    # WHEN
    farm_dealunit.set_actor(bob_text, vow_uid=eight_vowunit.uid)

    # THEN
    assert farm_dealunit.get_actor_vowunits(bob_text) != {}
    bob_vowunits = farm_dealunit.get_actor_vowunits(bob_text)
    assert len(bob_vowunits) == 1
    example_cooking_vowunit = get_cooking_vowunit()
    example_cooking_vowunit.set_actor(bob_text)
    assert bob_vowunits.get(eight_vowunit.uid) == example_cooking_vowunit


def test_DealUnit_get_actor_vowunits_ReturnsCorrectActionTopics():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road=yao_text)
    assert farm_dealunit.actor_has_vowunit(bob_text, action_filter=True) == False
    assert farm_dealunit.actor_has_vowunit(yao_text, action_filter=True) == False

    # WHEN
    farm_dealunit.set_vowunit(get_cooking_vowunit(), bob_text)
    farm_dealunit.set_vowunit(get_speedboat_action_vowunit(), yao_text)
    farm_dealunit.set_vowunit(get_climate_vowunit(), yao_text)

    # THEN
    assert farm_dealunit.actor_has_vowunit(bob_text, action_filter=True) == False
    assert farm_dealunit.actor_has_vowunit(yao_text, action_filter=True)


def test_DealUnit_set_deal_metrics_CorrectlySetsVow_relative_deal_weight():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road=yao_text)
    s1_vowunit = farm_dealunit.add_vowunit()
    s1_vowunit.set_actor(bob_text)
    s1_vowunit.edit_attr(author_weight=4, reader_weight=1)
    s2_vowunit = farm_dealunit.add_vowunit()
    s2_vowunit.set_actor(bob_text)
    s2_vowunit.edit_attr(author_weight=6, reader_weight=3)
    assert s1_vowunit._relative_author_weight == 0
    assert s1_vowunit._relative_reader_weight == 0
    assert s2_vowunit._relative_author_weight == 0
    assert s2_vowunit._relative_reader_weight == 0

    # WHEN
    farm_dealunit.set_deal_metrics()

    # THEN
    assert s1_vowunit._relative_author_weight == 0.4
    assert s1_vowunit._relative_reader_weight == 0.25
    assert s2_vowunit._relative_author_weight == 0.6
    assert s2_vowunit._relative_reader_weight == 0.75


def test_DealUnit_set_deal_metrics_RaisesErrorWhen_author_weight_IsZero():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road=yao_text)
    s1_vowunit = farm_dealunit.add_vowunit()
    s1_vowunit.set_actor(bob_text)
    s1_vowunit.edit_attr(author_weight=0, reader_weight=1)
    s2_vowunit = farm_dealunit.add_vowunit()
    s2_vowunit.set_actor(bob_text)
    s2_vowunit.edit_attr(author_weight=0, reader_weight=3)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        farm_dealunit.set_deal_metrics()
    assert str(excinfo.value) == "Cannot set deal metrics because vow_author_sum == 0."
