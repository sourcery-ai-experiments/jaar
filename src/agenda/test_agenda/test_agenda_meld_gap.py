from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import (
    agendaunit_shop,
    get_gap_agendaunit,
    set_gap_partyunits,
)
from src.agenda.group import groupunit_shop
from src.agenda.party import partyunit_shop, partylink_shop
from src.agenda.origin import originunit_shop
from pytest import raises as pytest_raises
from src.agenda.examples.example_agendas import agenda_v001
from copy import deepcopy as copy_deepcopy


def test_set_gap_partyunits_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_partyunit = partyunit_shop(yao_text)
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda.set_partyunit(yao_partyunit)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.set_partyunit(yao_partyunit)
    zia_text = "Zia"
    zia_partyunit = partyunit_shop(zia_text)
    bob2_agenda.set_partyunit(zia_partyunit)

    new_agendaunit = agendaunit_shop()
    assert len(new_agendaunit._partys) == 0

    # WHEN
    set_gap_partyunits(new_agendaunit, melder=bob1_agenda, melded=bob2_agenda)

    # THEN
    assert len(new_agendaunit._partys) == 1
    assert new_agendaunit.get_party(zia_text) == zia_partyunit


def test_get_gap_agendaunit_BaseScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_before = copy_deepcopy(bob1_agenda)
    bob2_agenda = agendaunit_shop(bob_text)
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # WHEN
    bob_diff_agenda = get_gap_agendaunit(melder=bob1_before, melded=bob1_agenda)

    # THEN
    assert bob2_agenda == bob_diff_agenda


def test_get_gap_agendaunit_WeightDoesNotCombine():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_before = copy_deepcopy(bob1_agenda)
    bob1_agenda._weight = 3
    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda._weight = 5
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # WHEN
    bob_diff_agenda = get_gap_agendaunit(melder=bob1_before, melded=bob1_agenda)

    # THEN
    # meldee agendaunit._weight information is lost in meld.
    assert bob2_agenda._weight != bob_diff_agenda._weight
    bob_diff_agenda._weight = bob2_agenda._weight
    assert bob2_agenda == bob_diff_agenda


def test_get_gap_agendaunit_PartyUnits():
    # GIVEN
    yao_text = "Yao"
    yao_partyunit = partyunit_shop(party_id=yao_text)

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda.set_partyunit(yao_partyunit)
    bob1_before = copy_deepcopy(bob1_agenda)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.set_partyunit(yao_partyunit)
    zia_text = "Zia"
    zia_partyunit = partyunit_shop(party_id=zia_text)
    bob2_agenda.set_partyunit(zia_partyunit)
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # WHEN
    bob_diff_agenda = get_gap_agendaunit(melder=bob1_before, melded=bob1_agenda)

    # THEN
    assert bob_diff_agenda.get_party(yao_text) is None
    assert bob_diff_agenda.get_party(zia_text) == zia_partyunit
    assert bob_diff_agenda.get_groupunit(yao_text) is None
    assert bob_diff_agenda.get_groupunit(zia_text) != None


def test_get_gap_agendaunit_GroupUnits_WhereGroupUnitIsMissing():
    # GIVEN
    run_text = "runners"
    run_groupunit = groupunit_shop(brand=run_text)

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda.set_groupunit(run_groupunit)
    bob1_before = copy_deepcopy(bob1_agenda)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.set_groupunit(run_groupunit)
    swim_text = "swimmers"
    swim_groupunit = groupunit_shop(brand=swim_text, uid=5)
    bob2_agenda.set_groupunit(swim_groupunit)
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # get_gap_agendaunit
    # WHEN
    bob_diff_agenda = get_gap_agendaunit(melder=bob1_before, melded=bob1_agenda)

    # THEN
    assert bob_diff_agenda.get_groupunit(run_text) is None
    assert bob_diff_agenda.get_groupunit(swim_text) != None


def test_get_gap_agendaunit_GroupUnits_WhereGroupUnitMembershipIsDifferent():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    sue_text = "Sue"
    bob1_agenda.set_partyunit(partyunit_shop(sue_text))

    run_text = "runners"
    bob1_agenda.set_groupunit(groupunit_shop(run_text))
    bob1_agenda.get_groupunit(run_text).set_partylink(partylink_shop(sue_text))
    bob1_before = copy_deepcopy(bob1_agenda)

    bob2_agenda = agendaunit_shop(bob_text)
    yao_text = "Yao"
    bob2_agenda.set_partyunit(partyunit_shop(yao_text))
    bob2_agenda.set_partyunit(partyunit_shop(sue_text))
    bob2_agenda.set_groupunit(groupunit_shop(run_text))
    bob2_agenda.get_groupunit(run_text).set_partylink(partylink_shop(yao_text))
    bob2_agenda.get_groupunit(run_text).set_partylink(partylink_shop(sue_text))
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # get_gap_agendaunit
    # WHEN
    bob_diff_agenda = get_gap_agendaunit(melder=bob1_before, melded=bob1_agenda)
    # THEN
    assert bob_diff_agenda.get_groupunit(run_text) != None
    run_diff_groupunit = bob_diff_agenda.get_groupunit(run_text)
    assert len(run_diff_groupunit._partys) == 1
    assert run_diff_groupunit.get_partylink(yao_text) != None
    assert run_diff_groupunit.get_partylink(sue_text) is None
