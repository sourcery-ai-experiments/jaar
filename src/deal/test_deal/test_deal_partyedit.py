# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src.deal.partyedit import partyeditunit_shop
from src.deal.deal import dealunit_shop
from src.deal.examples.example_partyeditunits import (
    get_bob_personroad,
    get_sue_personroad,
)

# from src.deal.examples.example_partyeditunits import get_adam_party_road
from pytest import raises as pytest_raises


def test_DealUnit_set_partyeditunit_SetsAttrCorrectly():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    farm_dealunit = dealunit_shop(get_bob_personroad(), get_sue_personroad())
    assert farm_dealunit._members_partyeditunits == {bob_text: {}, sue_text: {}}

    # WHEN
    adam_text = "Adam"
    adam_creditor_weight = 3
    adam_debtor_weight = 9
    farm_dealunit.set_partyeditunit(
        member=bob_text,
        x_partyeditunit=partyeditunit_shop(
            party_id=adam_text,
            creditor_weight=adam_creditor_weight,
            debtor_weight=adam_debtor_weight,
            depotlink_type=None,
        ),
    )

    # THEN
    print(f"{farm_dealunit._members_partyeditunits.keys()=}")
    assert len(farm_dealunit._members_partyeditunits) == 2
    assert farm_dealunit._members_partyeditunits.get(bob_text) != None
    assert farm_dealunit._members_partyeditunits.get(sue_text) != None
    bob_partyeditunits = farm_dealunit._members_partyeditunits.get(bob_text)
    # sue_partyeditunits = farm_dealunit._members_partyeditunits.get(sue_text)
    assert bob_partyeditunits != None
    adam_partyeditunit = bob_partyeditunits.get(adam_text)
    assert adam_partyeditunit != None
    assert adam_partyeditunit.creditor_weight == adam_creditor_weight
    assert adam_partyeditunit.debtor_weight == adam_debtor_weight
    assert adam_partyeditunit.depotlink_type != None


def test_DealUnit_get_partyeditunit_ReturnsCorrectObj():
    # GIVEN.
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(get_bob_personroad(), get_sue_personroad())
    adam_text = "Adam"
    farm_dealunit.set_partyeditunit(bob_text, partyeditunit_shop(None, adam_text))

    # WHEN
    adam_partyeditunit = farm_dealunit.get_partyeditunit(bob_text, adam_text)

    # THEN
    assert adam_partyeditunit != None
    assert adam_partyeditunit == partyeditunit_shop(bob_text, adam_text)


def test_DealUnit_partyeditunit_exists_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(get_bob_personroad(), get_sue_personroad())
    adam_text = "Adam"
    assert farm_dealunit.partyeditunit_exists(x_party_id=adam_text) == False

    # WHEN
    farm_dealunit.set_partyeditunit(bob_text, partyeditunit_shop(None, adam_text))

    # THEN
    assert farm_dealunit.partyeditunit_exists(x_party_id=adam_text)


def test_DealUnit_del_partyeditunit_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(get_bob_personroad(), get_sue_personroad())
    adam_text = "Adam"
    farm_dealunit.set_partyeditunit(bob_text, partyeditunit_shop(None, adam_text))
    assert farm_dealunit.partyeditunit_exists(adam_text)

    # WHEN
    farm_dealunit.del_partyeditunit(member=bob_text, x_party_id=adam_text)

    # THEN
    assert farm_dealunit.partyeditunit_exists(adam_text) == False


def test_DealUnit_edit_partyeditunit_attr_CorrectlySetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_dealunit = dealunit_shop(get_bob_personroad(), get_sue_personroad())
    adam_text = "Adam"
    adam_creditor_weight = 3
    adam_debtor_weight = 9
    adam_depotlink_type = "ignore"
    farm_dealunit.set_partyeditunit(
        bob_text,
        partyeditunit_shop(
            None,
            adam_text,
            adam_creditor_weight,
            adam_debtor_weight,
            adam_depotlink_type,
        ),
    )

    adam_partyeditunit = farm_dealunit.get_partyeditunit(bob_text, x_party_id=adam_text)
    assert adam_partyeditunit.creditor_weight == adam_creditor_weight
    assert adam_partyeditunit.debtor_weight == adam_debtor_weight
    assert adam_partyeditunit.depotlink_type == adam_depotlink_type

    # WHEN
    y_creditor_weight = 5
    y_debtor_weight = 13
    y_depotlink_type = "assignment"
    farm_dealunit.edit_partyeditunit_attr(
        member=bob_text,
        x_party_id=adam_text,
        x_creditor_weight=y_creditor_weight,
        x_debtor_weight=y_debtor_weight,
        x_depotlink_type=y_depotlink_type,
    )

    # THEN
    assert adam_partyeditunit.creditor_weight == y_creditor_weight
    assert adam_partyeditunit.debtor_weight == y_debtor_weight
    assert adam_partyeditunit.depotlink_type == y_depotlink_type


# def test_DealUnit_set_actor_partyeditunit_CorrectlySetsAttr():
#     # GIVEN
#     bob_text = "Bob"
#     farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road="Tim")
#     eight_partyeditunit = get_cooking_partyeditunit()
#     farm_dealunit.set_partyeditunit(eight_partyeditunit)

#     cooking_partyeditunit = farm_dealunit.get_partyeditunit(eight_partyeditunit.uid)
#     assert cooking_partyeditunit.get_actor(bob_text) is None

#     # WHEN
#     farm_dealunit.set_actor(actor=bob_text, partyedit_uid=eight_partyeditunit.uid)

#     # THEN
#     assert cooking_partyeditunit.get_actor(bob_text) != None


# def test_DealUnit_del_actor_partyeditunit_CorrectlySetsAttr():
#     # GIVEN
#     bob_text = "Bob"
#     farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road="Tim")
#     eight_partyeditunit = get_cooking_partyeditunit()
#     farm_dealunit.set_partyeditunit(eight_partyeditunit)
#     cooking_partyeditunit = farm_dealunit.get_partyeditunit(eight_partyeditunit.uid)
#     farm_dealunit.set_actor(actor=bob_text, partyedit_uid=eight_partyeditunit.uid)
#     assert cooking_partyeditunit.get_actor(bob_text) != None

#     # WHEN
#     farm_dealunit.del_actor(actor=bob_text, partyedit_uid=eight_partyeditunit.uid)

#     # THEN
#     assert cooking_partyeditunit.get_actor(bob_text) is None


# def test_DealUnit_get_actor_partyeditunits_ReturnsCorrectObjs():
#     # GIVEN
#     bob_text = "Bob"
#     farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road="Tim")
#     eight_partyeditunit = get_cooking_partyeditunit()
#     farm_dealunit.set_partyeditunit(eight_partyeditunit)
#     assert farm_dealunit.get_actor_partyeditunits(eight_partyeditunit.uid) == {}

#     # WHEN
#     farm_dealunit.set_actor(bob_text, partyedit_uid=eight_partyeditunit.uid)

#     # THEN
#     assert farm_dealunit.get_actor_partyeditunits(bob_text) != {}
#     bob_partyeditunits = farm_dealunit.get_actor_partyeditunits(bob_text)
#     assert len(bob_partyeditunits) == 1
#     example_cooking_partyeditunit = get_cooking_partyeditunit()
#     example_cooking_partyeditunit.set_actor(bob_text)
#     assert bob_partyeditunits.get(eight_partyeditunit.uid) == example_cooking_partyeditunit


# def test_DealUnit_get_actor_partyeditunits_ReturnsCorrectActionTopics():
#     # GIVEN
#     bob_text = "Bob"
#     yao_text = "Yao"
#     farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road=yao_text)
#     assert farm_dealunit.actor_has_partyeditunit(bob_text, action_filter=True) == False
#     assert farm_dealunit.actor_has_partyeditunit(yao_text, action_filter=True) == False

#     # WHEN
#     farm_dealunit.set_partyeditunit(get_cooking_partyeditunit(), bob_text)
#     farm_dealunit.set_partyeditunit(get_speedboat_action_partyeditunit(), yao_text)
#     farm_dealunit.set_partyeditunit(get_climate_partyeditunit(), yao_text)

#     # THEN
#     assert farm_dealunit.actor_has_partyeditunit(bob_text, action_filter=True) == False
#     assert farm_dealunit.actor_has_partyeditunit(yao_text, action_filter=True)


# def test_DealUnit_set_deal_metrics_CorrectlySetsDue_relative_deal_weight():
#     # GIVEN
#     bob_text = "Bob"
#     yao_text = "Yao"
#     farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road=yao_text)
#     s1_partyeditunit = farm_dealunit.add_partyeditunit()
#     s1_partyeditunit.set_actor(bob_text)
#     s1_partyeditunit.edit_attr(author_weight=4, reader_weight=1)
#     s2_partyeditunit = farm_dealunit.add_partyeditunit()
#     s2_partyeditunit.set_actor(bob_text)
#     s2_partyeditunit.edit_attr(author_weight=6, reader_weight=3)
#     assert s1_partyeditunit._relative_author_weight == 0
#     assert s1_partyeditunit._relative_reader_weight == 0
#     assert s2_partyeditunit._relative_author_weight == 0
#     assert s2_partyeditunit._relative_reader_weight == 0

#     # WHEN
#     farm_dealunit.set_deal_metrics()

#     # THEN
#     assert s1_partyeditunit._relative_author_weight == 0.4
#     assert s1_partyeditunit._relative_reader_weight == 0.25
#     assert s2_partyeditunit._relative_author_weight == 0.6
#     assert s2_partyeditunit._relative_reader_weight == 0.75


# def test_DealUnit_set_deal_metrics_RaisesErrorWhen_author_weight_IsZero():
#     # GIVEN
#     bob_text = "Bob"
#     yao_text = "Yao"
#     farm_dealunit = dealunit_shop(_author_road=bob_text, _reader_road=yao_text)
#     s1_partyeditunit = farm_dealunit.add_partyeditunit()
#     s1_partyeditunit.set_actor(bob_text)
#     s1_partyeditunit.edit_attr(author_weight=0, reader_weight=1)
#     s2_partyeditunit = farm_dealunit.add_partyeditunit()
#     s2_partyeditunit.set_actor(bob_text)
#     s2_partyeditunit.edit_attr(author_weight=0, reader_weight=3)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         farm_dealunit.set_deal_metrics()
#     assert (
#         str(excinfo.value) == "Cannot set deal metrics because partyedit_author_sum == 0."
#     )
