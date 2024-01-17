# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src.accord.accord import accordunit_shop, sectionunit_shop
from src.accord.examples.example_topics import (
    get_cooking_sectionunit,
    get_speedboat_action_sectionunit,
    get_climate_sectionunit,
)


def test_AccordUnit_set_sectionunit_SetsAttrCorrectly():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    assert farm_accordunit._sectionunits == {}

    # WHEN
    x_uid = 7
    x_weight = 3
    farm_accordunit.set_sectionunit(sectionunit_shop(x_uid, x_weight))

    # THEN
    assert len(farm_accordunit._sectionunits) == 1
    assert farm_accordunit._sectionunits.get(x_uid) != None
    x_sectionunit = farm_accordunit._sectionunits.get(x_uid)
    assert x_sectionunit == sectionunit_shop(x_uid, x_weight)
    assert x_sectionunit.weight == x_weight


def test_AccordUnit_get_sectionunit_ReturnsCorrectObj():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    farm_accordunit.set_sectionunit(sectionunit_shop(one_text))

    # WHEN / THEN
    assert farm_accordunit.get_sectionunit(one_text) != None


def test_AccordUnit_sectionunit_exists_ReturnsCorrectObj():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    assert farm_accordunit.sectionunit_exists(one_text) == False

    # WHEN
    farm_accordunit.set_sectionunit(sectionunit_shop(one_text))

    # THEN
    assert farm_accordunit.sectionunit_exists(one_text)


def test_AccordUnit_del_sectionunit_CorrectlySetsAttr():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    farm_accordunit.set_sectionunit(sectionunit_shop(one_text))
    assert farm_accordunit.sectionunit_exists(one_text)

    # WHEN
    farm_accordunit.del_sectionunit(one_text)

    # THEN
    assert farm_accordunit.sectionunit_exists(one_text) == False


def test_AccordUnit_add_sectionunit_SetsAttrCorrectly():
    # GIVEN
    farm_accordunit = accordunit_shop(_author="Bob", _reader="Tim")
    assert farm_accordunit._sectionunits == {}

    # WHEN
    one_sectionunit = farm_accordunit.add_sectionunit()

    # THEN
    assert one_sectionunit.uid == 1
    assert one_sectionunit.get_section_id() == "Section 0001"
    assert len(farm_accordunit._sectionunits) == 1
    assert farm_accordunit.get_sectionunit(one_sectionunit.uid) != None

    # WHEN
    two_sectionunit = farm_accordunit.add_sectionunit()

    # THEN
    assert two_sectionunit.uid == 2
    assert two_sectionunit.get_section_id() == "Section 0002"
    assert len(farm_accordunit._sectionunits) == 2
    assert farm_accordunit.get_sectionunit(two_sectionunit.uid) != None

    x_int = 7
    farm_accordunit.set_sectionunit(sectionunit_shop(x_int))
    assert len(farm_accordunit._sectionunits) == 3

    # WHEN
    eight_sectionunit = farm_accordunit.add_sectionunit()

    # THEN
    assert eight_sectionunit.uid == 8
    assert eight_sectionunit.get_section_id() == "Section 0008"
    assert len(farm_accordunit._sectionunits) == 4
    assert farm_accordunit.get_sectionunit(eight_sectionunit.uid) != None


def test_AccordUnit_edit_sectionunit_attr_CorrectlySetsAttribute():
    # GIVEN
    tim_text = "Tim"
    farm_accordunit = accordunit_shop(_author="Bob", _reader=tim_text)
    x_uid = 7
    x_weight = 3
    farm_accordunit.set_sectionunit(sectionunit_shop(x_uid, x_weight))

    x_sectionunit = farm_accordunit._sectionunits.get(x_uid)
    assert x_sectionunit.weight == x_weight
    assert x_sectionunit.actor is None

    # WHEN
    y_weight = 7
    farm_accordunit.edit_sectionunit_attr(x_uid, weight=y_weight, actor=tim_text)

    # THEN
    x_sectionunit = farm_accordunit._sectionunits.get(x_uid)
    assert x_sectionunit.weight != x_weight
    assert x_sectionunit.weight == y_weight
    assert x_sectionunit.actor != None
    assert x_sectionunit.actor == tim_text


def test_AccordUnit_set_actor_sectionunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader="Tim")
    eight_sectionunit = get_cooking_sectionunit()
    farm_accordunit.set_sectionunit(eight_sectionunit)

    cooking_sectionunit = farm_accordunit.get_sectionunit(eight_sectionunit.uid)
    assert cooking_sectionunit.get_actor(bob_text) is None

    # WHEN
    farm_accordunit.set_actor(actor=bob_text, section_uid=eight_sectionunit.uid)

    # THEN
    assert cooking_sectionunit.get_actor(bob_text) != None


def test_AccordUnit_del_actor_sectionunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader="Tim")
    eight_sectionunit = get_cooking_sectionunit()
    farm_accordunit.set_sectionunit(eight_sectionunit)
    cooking_sectionunit = farm_accordunit.get_sectionunit(eight_sectionunit.uid)
    farm_accordunit.set_actor(actor=bob_text, section_uid=eight_sectionunit.uid)
    assert cooking_sectionunit.get_actor(bob_text) != None

    # WHEN
    farm_accordunit.del_actor(actor=bob_text, section_uid=eight_sectionunit.uid)

    # THEN
    assert cooking_sectionunit.get_actor(bob_text) is None


def test_AccordUnit_get_actor_sectionunits_ReturnsCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader="Tim")
    eight_sectionunit = get_cooking_sectionunit()
    farm_accordunit.set_sectionunit(eight_sectionunit)
    assert farm_accordunit.get_actor_sectionunits(eight_sectionunit.uid) == {}

    # WHEN
    farm_accordunit.set_actor(bob_text, section_uid=eight_sectionunit.uid)

    # THEN
    assert farm_accordunit.get_actor_sectionunits(bob_text) != {}
    bob_sectionunits = farm_accordunit.get_actor_sectionunits(bob_text)
    assert len(bob_sectionunits) == 1
    example_cooking_sectionunit = get_cooking_sectionunit()
    example_cooking_sectionunit.set_actor(bob_text)
    assert bob_sectionunits.get(eight_sectionunit.uid) == example_cooking_sectionunit


def test_AccordUnit_get_actor_sectionunits_ReturnsCorrectActionTopics():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader=yao_text)
    assert farm_accordunit.actor_has_sectionunit(bob_text, action_filter=True) == False
    assert farm_accordunit.actor_has_sectionunit(yao_text, action_filter=True) == False

    # WHEN
    farm_accordunit.set_sectionunit(get_cooking_sectionunit(), bob_text)
    farm_accordunit.set_sectionunit(get_speedboat_action_sectionunit(), yao_text)
    farm_accordunit.set_sectionunit(get_climate_sectionunit(), yao_text)

    # THEN
    assert farm_accordunit.actor_has_sectionunit(bob_text, action_filter=True) == False
    assert farm_accordunit.actor_has_sectionunit(yao_text, action_filter=True)


def test_AccordUnit_set_accord_metrics_CorrectlySetsSection_relative_accord_weight():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_accordunit = accordunit_shop(_author=bob_text, _reader=yao_text)
    s1_sectionunit = farm_accordunit.add_sectionunit()
    farm_accordunit.edit_sectionunit_attr(s1_sectionunit.uid, weight=4)
    s1_sectionunit.set_actor(bob_text)
    s1_sectionunit.edit_attr(weight=4)
    s2_sectionunit = farm_accordunit.add_sectionunit()
    s2_sectionunit.set_actor(bob_text)
    s2_sectionunit.edit_attr(weight=6)
    assert s1_sectionunit._relative_accord_weight == 0
    assert s2_sectionunit._relative_accord_weight == 0

    # WHEN
    farm_accordunit.set_accord_metrics()

    # THEN
    assert s1_sectionunit._relative_accord_weight == 0.4
    assert s2_sectionunit._relative_accord_weight == 0.6
