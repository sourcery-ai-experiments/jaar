from src.world.partyedit import partyeditunit_shop
from src.world.deal import dealunit_shop
from src.world.examples.example_deals import get_bob_personroad, get_sue_personroad


def test_DealUnit_set_partyeditunit_SetsAttrCorrectly():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    farm_dealunit = dealunit_shop(get_bob_personroad(), get_sue_personroad())
    assert farm_dealunit._members_partyeditunits == {bob_text: {}, sue_text: {}}

    # WHEN
    adam_text = "Adam"
    adam_creditor_change = 3
    adam_debtor_change = 9
    farm_dealunit.set_partyeditunit(
        member=bob_text,
        x_partyeditunit=partyeditunit_shop(
            party_id=adam_text,
            creditor_change=adam_creditor_change,
            debtor_change=adam_debtor_change,
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
    assert adam_partyeditunit.creditor_change == adam_creditor_change
    assert adam_partyeditunit.debtor_change == adam_debtor_change
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
    adam_creditor_change = 3
    adam_debtor_change = 9
    adam_depotlink_type = "ignore"
    farm_dealunit.set_partyeditunit(
        bob_text,
        partyeditunit_shop(
            None,
            adam_text,
            adam_creditor_change,
            adam_debtor_change,
            adam_depotlink_type,
        ),
    )

    adam_partyeditunit = farm_dealunit.get_partyeditunit(bob_text, x_party_id=adam_text)
    assert adam_partyeditunit.creditor_change == adam_creditor_change
    assert adam_partyeditunit.debtor_change == adam_debtor_change
    assert adam_partyeditunit.depotlink_type == adam_depotlink_type

    # WHEN
    y_creditor_change = 5
    y_debtor_change = 13
    y_depotlink_type = "assignment"
    farm_dealunit.edit_partyeditunit_attr(
        member=bob_text,
        x_party_id=adam_text,
        x_creditor_change=y_creditor_change,
        x_debtor_change=y_debtor_change,
        x_depotlink_type=y_depotlink_type,
    )

    # THEN
    assert adam_partyeditunit.creditor_change == y_creditor_change
    assert adam_partyeditunit.debtor_change == y_debtor_change
    assert adam_partyeditunit.depotlink_type == y_depotlink_type
