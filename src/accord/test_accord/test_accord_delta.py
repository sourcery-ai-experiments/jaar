# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src.accord.delta import deltaunit_shop
from src.accord.accord import accordunit_shop
from src.accord.examples.example_deltas import get_bob_personroad, get_sue_personroad

# from src.accord.examples.example_deltas import get_adam_party_road
from pytest import raises as pytest_raises


def test_AccordUnit_set_deltaunit_SetsAttrCorrectly():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    farm_accordunit = accordunit_shop(get_bob_personroad(), get_sue_personroad())
    assert farm_accordunit._members_deltaunits == {bob_text: {}, sue_text: {}}

    # WHEN
    adam_text = "Adam"
    adam_creditor_weight = 3
    adam_debtor_weight = 9
    farm_accordunit.set_deltaunit(
        member=bob_text,
        x_delta=deltaunit_shop(
            party_id=adam_text,
            creditor_weight=adam_creditor_weight,
            debtor_weight=adam_debtor_weight,
            depotlink_type=None,
        ),
    )

    # THEN
    print(f"{farm_accordunit._members_deltaunits.keys()=}")
    assert len(farm_accordunit._members_deltaunits) == 2
    assert farm_accordunit._members_deltaunits.get(bob_text) != None
    assert farm_accordunit._members_deltaunits.get(sue_text) != None
    bob_deltaunits = farm_accordunit._members_deltaunits.get(bob_text)
    # sue_deltaunits = farm_accordunit._members_deltaunits.get(sue_text)
    assert bob_deltaunits != None
    adam_deltaunit = bob_deltaunits.get(adam_text)
    assert adam_deltaunit != None
    assert adam_deltaunit.creditor_weight == adam_creditor_weight
    assert adam_deltaunit.debtor_weight == adam_debtor_weight
    assert adam_deltaunit.depotlink_type != None


def test_AccordUnit_get_deltaunit_ReturnsCorrectObj():
    # GIVEN.
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(get_bob_personroad(), get_sue_personroad())
    adam_text = "Adam"
    farm_accordunit.set_deltaunit(bob_text, deltaunit_shop(None, adam_text))

    # WHEN
    adam_deltaunit = farm_accordunit.get_deltaunit(bob_text, adam_text)

    # THEN
    assert adam_deltaunit != None
    assert adam_deltaunit == deltaunit_shop(bob_text, adam_text)


def test_AccordUnit_deltaunit_exists_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(get_bob_personroad(), get_sue_personroad())
    adam_text = "Adam"
    assert farm_accordunit.deltaunit_exists(x_party_id=adam_text) == False

    # WHEN
    farm_accordunit.set_deltaunit(bob_text, deltaunit_shop(None, adam_text))

    # THEN
    assert farm_accordunit.deltaunit_exists(x_party_id=adam_text)


def test_AccordUnit_del_deltaunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(get_bob_personroad(), get_sue_personroad())
    adam_text = "Adam"
    farm_accordunit.set_deltaunit(bob_text, deltaunit_shop(None, adam_text))
    assert farm_accordunit.deltaunit_exists(adam_text)

    # WHEN
    farm_accordunit.del_deltaunit(member=bob_text, x_party_id=adam_text)

    # THEN
    assert farm_accordunit.deltaunit_exists(adam_text) == False


def test_AccordUnit_edit_deltaunit_attr_CorrectlySetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_accordunit = accordunit_shop(get_bob_personroad(), get_sue_personroad())
    adam_text = "Adam"
    adam_creditor_weight = 3
    adam_debtor_weight = 9
    adam_depotlink_type = "ignore"
    farm_accordunit.set_deltaunit(
        bob_text,
        deltaunit_shop(
            None,
            adam_text,
            adam_creditor_weight,
            adam_debtor_weight,
            adam_depotlink_type,
        ),
    )

    adam_deltaunit = farm_accordunit.get_deltaunit(bob_text, x_party_id=adam_text)
    assert adam_deltaunit.creditor_weight == adam_creditor_weight
    assert adam_deltaunit.debtor_weight == adam_debtor_weight
    assert adam_deltaunit.depotlink_type == adam_depotlink_type

    # WHEN
    y_creditor_weight = 5
    y_debtor_weight = 13
    y_depotlink_type = "assignment"
    farm_accordunit.edit_deltaunit_attr(
        member=bob_text,
        x_party_id=adam_text,
        x_creditor_weight=y_creditor_weight,
        x_debtor_weight=y_debtor_weight,
        x_depotlink_type=y_depotlink_type,
    )

    # THEN
    assert adam_deltaunit.creditor_weight == y_creditor_weight
    assert adam_deltaunit.debtor_weight == y_debtor_weight
    assert adam_deltaunit.depotlink_type == y_depotlink_type


# def test_AccordUnit_set_actor_deltaunit_CorrectlySetsAttr():
#     # GIVEN
#     bob_text = "Bob"
#     farm_accordunit = accordunit_shop(_author_road=bob_text, _reader_road="Tim")
#     eight_deltaunit = get_cooking_deltaunit()
#     farm_accordunit.set_deltaunit(eight_deltaunit)

#     cooking_deltaunit = farm_accordunit.get_deltaunit(eight_deltaunit.uid)
#     assert cooking_deltaunit.get_actor(bob_text) is None

#     # WHEN
#     farm_accordunit.set_actor(actor=bob_text, delta_uid=eight_deltaunit.uid)

#     # THEN
#     assert cooking_deltaunit.get_actor(bob_text) != None


# def test_AccordUnit_del_actor_deltaunit_CorrectlySetsAttr():
#     # GIVEN
#     bob_text = "Bob"
#     farm_accordunit = accordunit_shop(_author_road=bob_text, _reader_road="Tim")
#     eight_deltaunit = get_cooking_deltaunit()
#     farm_accordunit.set_deltaunit(eight_deltaunit)
#     cooking_deltaunit = farm_accordunit.get_deltaunit(eight_deltaunit.uid)
#     farm_accordunit.set_actor(actor=bob_text, delta_uid=eight_deltaunit.uid)
#     assert cooking_deltaunit.get_actor(bob_text) != None

#     # WHEN
#     farm_accordunit.del_actor(actor=bob_text, delta_uid=eight_deltaunit.uid)

#     # THEN
#     assert cooking_deltaunit.get_actor(bob_text) is None


# def test_AccordUnit_get_actor_deltaunits_ReturnsCorrectObjs():
#     # GIVEN
#     bob_text = "Bob"
#     farm_accordunit = accordunit_shop(_author_road=bob_text, _reader_road="Tim")
#     eight_deltaunit = get_cooking_deltaunit()
#     farm_accordunit.set_deltaunit(eight_deltaunit)
#     assert farm_accordunit.get_actor_deltaunits(eight_deltaunit.uid) == {}

#     # WHEN
#     farm_accordunit.set_actor(bob_text, delta_uid=eight_deltaunit.uid)

#     # THEN
#     assert farm_accordunit.get_actor_deltaunits(bob_text) != {}
#     bob_deltaunits = farm_accordunit.get_actor_deltaunits(bob_text)
#     assert len(bob_deltaunits) == 1
#     example_cooking_deltaunit = get_cooking_deltaunit()
#     example_cooking_deltaunit.set_actor(bob_text)
#     assert bob_deltaunits.get(eight_deltaunit.uid) == example_cooking_deltaunit


# def test_AccordUnit_get_actor_deltaunits_ReturnsCorrectActionTopics():
#     # GIVEN
#     bob_text = "Bob"
#     yao_text = "Yao"
#     farm_accordunit = accordunit_shop(_author_road=bob_text, _reader_road=yao_text)
#     assert farm_accordunit.actor_has_deltaunit(bob_text, action_filter=True) == False
#     assert farm_accordunit.actor_has_deltaunit(yao_text, action_filter=True) == False

#     # WHEN
#     farm_accordunit.set_deltaunit(get_cooking_deltaunit(), bob_text)
#     farm_accordunit.set_deltaunit(get_speedboat_action_deltaunit(), yao_text)
#     farm_accordunit.set_deltaunit(get_climate_deltaunit(), yao_text)

#     # THEN
#     assert farm_accordunit.actor_has_deltaunit(bob_text, action_filter=True) == False
#     assert farm_accordunit.actor_has_deltaunit(yao_text, action_filter=True)


# def test_AccordUnit_set_accord_metrics_CorrectlySetsDue_relative_accord_weight():
#     # GIVEN
#     bob_text = "Bob"
#     yao_text = "Yao"
#     farm_accordunit = accordunit_shop(_author_road=bob_text, _reader_road=yao_text)
#     s1_deltaunit = farm_accordunit.add_deltaunit()
#     s1_deltaunit.set_actor(bob_text)
#     s1_deltaunit.edit_attr(author_weight=4, reader_weight=1)
#     s2_deltaunit = farm_accordunit.add_deltaunit()
#     s2_deltaunit.set_actor(bob_text)
#     s2_deltaunit.edit_attr(author_weight=6, reader_weight=3)
#     assert s1_deltaunit._relative_author_weight == 0
#     assert s1_deltaunit._relative_reader_weight == 0
#     assert s2_deltaunit._relative_author_weight == 0
#     assert s2_deltaunit._relative_reader_weight == 0

#     # WHEN
#     farm_accordunit.set_accord_metrics()

#     # THEN
#     assert s1_deltaunit._relative_author_weight == 0.4
#     assert s1_deltaunit._relative_reader_weight == 0.25
#     assert s2_deltaunit._relative_author_weight == 0.6
#     assert s2_deltaunit._relative_reader_weight == 0.75


# def test_AccordUnit_set_accord_metrics_RaisesErrorWhen_author_weight_IsZero():
#     # GIVEN
#     bob_text = "Bob"
#     yao_text = "Yao"
#     farm_accordunit = accordunit_shop(_author_road=bob_text, _reader_road=yao_text)
#     s1_deltaunit = farm_accordunit.add_deltaunit()
#     s1_deltaunit.set_actor(bob_text)
#     s1_deltaunit.edit_attr(author_weight=0, reader_weight=1)
#     s2_deltaunit = farm_accordunit.add_deltaunit()
#     s2_deltaunit.set_actor(bob_text)
#     s2_deltaunit.edit_attr(author_weight=0, reader_weight=3)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         farm_accordunit.set_accord_metrics()
#     assert (
#         str(excinfo.value) == "Cannot set accord metrics because delta_author_sum == 0."
#     )
