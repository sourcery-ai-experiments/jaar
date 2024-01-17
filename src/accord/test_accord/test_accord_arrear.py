# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src.accord.accord import accordunit_shop, arrearunit_shop
from src.accord.examples.example_topics import (
    get_cooking_arrearunit,
    get_speedboat_action_arrearunit,
    get_climate_arrearunit,
)


def test_AccordUnit_set_arrearunit_SetsAttrCorrectly():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    assert farm_accordunit._arrearunits == {}

    # WHEN
    x_uid = 7
    x_weight = 3
    farm_accordunit.set_arrearunit(arrearunit_shop(x_uid, x_weight))

    # THEN
    assert len(farm_accordunit._arrearunits) == 1
    assert farm_accordunit._arrearunits.get(x_uid) != None
    x_arrearunit = farm_accordunit._arrearunits.get(x_uid)
    assert x_arrearunit == arrearunit_shop(x_uid, x_weight)
    assert x_arrearunit.weight == x_weight


def test_AccordUnit_get_arrearunit_ReturnsCorrectObj():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    farm_accordunit.set_arrearunit(arrearunit_shop(one_text))

    # WHEN / THEN
    assert farm_accordunit.get_arrearunit(one_text) != None


def test_AccordUnit_arrearunit_exists_ReturnsCorrectObj():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    assert farm_accordunit.arrearunit_exists(one_text) == False

    # WHEN
    farm_accordunit.set_arrearunit(arrearunit_shop(one_text))

    # THEN
    assert farm_accordunit.arrearunit_exists(one_text)


def test_AccordUnit_del_arrearunit_CorrectlySetsAttr():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    farm_accordunit.set_arrearunit(arrearunit_shop(one_text))
    assert farm_accordunit.arrearunit_exists(one_text)

    # WHEN
    farm_accordunit.del_arrearunit(one_text)

    # THEN
    assert farm_accordunit.arrearunit_exists(one_text) == False


def test_AccordUnit_add_arrearunit_SetsAttrCorrectly():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    assert farm_accordunit._arrearunits == {}

    # WHEN
    one_arrearunit = farm_accordunit.add_arrearunit()

    # THEN
    assert one_arrearunit.uid == 1
    assert one_arrearunit.get_arrear_id() == "Arrear 0001"
    assert len(farm_accordunit._arrearunits) == 1
    assert farm_accordunit.get_arrearunit(one_arrearunit.uid) != None

    # WHEN
    two_arrearunit = farm_accordunit.add_arrearunit()

    # THEN
    assert two_arrearunit.uid == 2
    assert two_arrearunit.get_arrear_id() == "Arrear 0002"
    assert len(farm_accordunit._arrearunits) == 2
    assert farm_accordunit.get_arrearunit(two_arrearunit.uid) != None

    x_int = 7
    farm_accordunit.set_arrearunit(arrearunit_shop(x_int))
    assert len(farm_accordunit._arrearunits) == 3

    # WHEN
    eight_arrearunit = farm_accordunit.add_arrearunit()

    # THEN
    assert eight_arrearunit.uid == 8
    assert eight_arrearunit.get_arrear_id() == "Arrear 0008"
    assert len(farm_accordunit._arrearunits) == 4
    assert farm_accordunit.get_arrearunit(eight_arrearunit.uid) != None


def test_AccordUnit_edit_arrearunit_attr_CorrectlySetsAttribute():
    # GIVEN
    tim_text = "Tim"
    farm_accordunit = accordunit_shop(_author="Bob", _reader=tim_text)
    x_uid = 7
    x_weight = 3
    farm_accordunit.set_arrearunit(arrearunit_shop(x_uid, x_weight))

    x_arrearunit = farm_accordunit._arrearunits.get(x_uid)
    assert x_arrearunit.weight == x_weight
    assert x_arrearunit.actor is None

    # WHEN
    y_weight = 7
    farm_accordunit.edit_arrearunit_attr(x_uid, weight=y_weight, actor=tim_text)

    # THEN
    x_arrearunit = farm_accordunit._arrearunits.get(x_uid)
    assert x_arrearunit.weight != x_weight
    assert x_arrearunit.weight == y_weight
    assert x_arrearunit.actor != None
    assert x_arrearunit.actor == tim_text


def test_AccordUnit_set_actor_arrearunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader="Tim")
    eight_arrearunit = get_cooking_arrearunit()
    farm_accordunit.set_arrearunit(eight_arrearunit)

    cooking_arrearunit = farm_accordunit.get_arrearunit(eight_arrearunit.uid)
    assert cooking_arrearunit.get_actor(bob_text) is None

    # WHEN
    farm_accordunit.set_actor(actor=bob_text, arrear_uid=eight_arrearunit.uid)

    # THEN
    assert cooking_arrearunit.get_actor(bob_text) != None


def test_AccordUnit_del_actor_arrearunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader="Tim")
    eight_arrearunit = get_cooking_arrearunit()
    farm_accordunit.set_arrearunit(eight_arrearunit)
    cooking_arrearunit = farm_accordunit.get_arrearunit(eight_arrearunit.uid)
    farm_accordunit.set_actor(actor=bob_text, arrear_uid=eight_arrearunit.uid)
    assert cooking_arrearunit.get_actor(bob_text) != None

    # WHEN
    farm_accordunit.del_actor(actor=bob_text, arrear_uid=eight_arrearunit.uid)

    # THEN
    assert cooking_arrearunit.get_actor(bob_text) is None


def test_AccordUnit_get_actor_arrearunits_ReturnsCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader="Tim")
    eight_arrearunit = get_cooking_arrearunit()
    farm_accordunit.set_arrearunit(eight_arrearunit)
    assert farm_accordunit.get_actor_arrearunits(eight_arrearunit.uid) == {}

    # WHEN
    farm_accordunit.set_actor(bob_text, arrear_uid=eight_arrearunit.uid)

    # THEN
    assert farm_accordunit.get_actor_arrearunits(bob_text) != {}
    bob_arrearunits = farm_accordunit.get_actor_arrearunits(bob_text)
    assert len(bob_arrearunits) == 1
    example_cooking_arrearunit = get_cooking_arrearunit()
    example_cooking_arrearunit.set_actor(bob_text)
    assert bob_arrearunits.get(eight_arrearunit.uid) == example_cooking_arrearunit


def test_AccordUnit_get_actor_arrearunits_ReturnsCorrectActionTopics():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader=yao_text)
    assert farm_accordunit.actor_has_arrearunit(bob_text, action_filter=True) == False
    assert farm_accordunit.actor_has_arrearunit(yao_text, action_filter=True) == False

    # WHEN
    farm_accordunit.set_arrearunit(get_cooking_arrearunit(), bob_text)
    farm_accordunit.set_arrearunit(get_speedboat_action_arrearunit(), yao_text)
    farm_accordunit.set_arrearunit(get_climate_arrearunit(), yao_text)

    # THEN
    assert farm_accordunit.actor_has_arrearunit(bob_text, action_filter=True) == False
    assert farm_accordunit.actor_has_arrearunit(yao_text, action_filter=True)


def test_AccordUnit_set_accord_metrics_CorrectlySetsArrear_relative_accord_weight():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader=yao_text)
    s1_arrearunit = farm_accordunit.add_arrearunit()
    farm_accordunit.edit_arrearunit_attr(s1_arrearunit.uid, weight=4)
    s1_arrearunit.set_actor(bob_text)
    s1_arrearunit.edit_attr(weight=4)
    s2_arrearunit = farm_accordunit.add_arrearunit()
    s2_arrearunit.set_actor(bob_text)
    s2_arrearunit.edit_attr(weight=6)
    assert s1_arrearunit._relative_accord_weight == 0
    assert s2_arrearunit._relative_accord_weight == 0

    # WHEN
    farm_accordunit.set_accord_metrics()

    # THEN
    assert s1_arrearunit._relative_accord_weight == 0.4
    assert s2_arrearunit._relative_accord_weight == 0.6
