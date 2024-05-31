from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.listen import (
    get_all_partys_with_debtor_weight,
    get_ordered_debtors_roll,
    listen_to_speaker_beliefs,
)


def test_get_all_partys_with_debtor_weight_ReturnsObj():
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.calc_agenda_metrics()

    # WHEN
    yao_roll = get_all_partys_with_debtor_weight(yao_role)

    # THEN
    zia_partyunit = yao_role.get_party(zia_text)
    assert yao_roll == [zia_partyunit]


def test_get_all_partys_with_debtor_weight_ReturnsObjIgnoresZero_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    wei_text = "Wei"
    wei_creditor_weight = 67
    wei_debtor_weight = 0
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.add_partyunit(wei_text, wei_creditor_weight, wei_debtor_weight)
    yao_role.calc_agenda_metrics()

    # WHEN
    yao_roll = get_all_partys_with_debtor_weight(yao_role)

    # THEN
    zia_partyunit = yao_role.get_party(zia_text)
    assert yao_roll == [zia_partyunit]


def test_get_ordered_debtors_roll_ReturnsObjsInOrder():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_creditor_weight = 57
    sue_debtor_weight = 51
    yao_agenda.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_agenda.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_agenda.set_party_pool(yao_pool)

    # WHEN
    ordered_partys1 = get_ordered_debtors_roll(yao_agenda)

    # THEN
    zia_party = yao_agenda.get_party(zia_text)
    sue_party = yao_agenda.get_party(sue_text)
    assert ordered_partys1[0].get_dict() == sue_party.get_dict()
    assert ordered_partys1 == [sue_party, zia_party]

    # GIVEN
    bob_text = "Bob"
    bob_debtor_weight = 75
    yao_agenda.add_partyunit(bob_text, 0, bob_debtor_weight)
    bob_party = yao_agenda.get_party(bob_text)

    # WHEN
    ordered_partys2 = get_ordered_debtors_roll(yao_agenda)

    # THEN
    assert ordered_partys2[0].get_dict() == bob_party.get_dict()
    assert ordered_partys2 == [bob_party, sue_party, zia_party]


def test_get_ordered_debtors_roll_DoesNotReturnZero_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_debtor_weight = 51
    yao_pool = 92
    yao_agenda.set_party_pool(yao_pool)
    bob_text = "Bob"
    bob_debtor_weight = 75
    xio_text = "Xio"
    yao_agenda.add_partyunit(zia_text, 0, zia_debtor_weight)
    yao_agenda.add_partyunit(sue_text, 0, sue_debtor_weight)
    yao_agenda.add_partyunit(bob_text, 0, bob_debtor_weight)
    yao_agenda.add_partyunit(yao_text, 0, 0)
    yao_agenda.add_partyunit(xio_text, 0, 0)

    # WHEN
    ordered_partys2 = get_ordered_debtors_roll(yao_agenda)

    # THEN
    assert len(ordered_partys2) == 3
    zia_party = yao_agenda.get_party(zia_text)
    sue_party = yao_agenda.get_party(sue_text)
    bob_party = yao_agenda.get_party(bob_text)
    assert ordered_partys2[0].get_dict() == bob_party.get_dict()
    assert ordered_partys2 == [bob_party, sue_party, zia_party]


def test_set_listen_to_speaker_beliefs_SetsBelief():
    # GIVEN
    yao_text = "Yao"
    yao_listener = agendaunit_shop(yao_text)
    casa_text = "casa"
    casa_road = yao_listener.make_l1_road(casa_text)
    status_text = "status"
    status_road = yao_listener.make_road(casa_road, status_text)
    clean_text = "clean"
    clean_road = yao_listener.make_road(status_road, clean_text)
    dirty_text = "dirty"
    dirty_road = yao_listener.make_road(status_road, dirty_text)
    sweep_text = "sweep"
    sweep_road = yao_listener.make_road(casa_road, sweep_text)

    yao_listener.add_partyunit(yao_text)
    yao_listener.set_party_pool(20)
    yao_listener.add_idea(ideaunit_shop(clean_text), status_road)
    yao_listener.add_idea(ideaunit_shop(dirty_text), status_road)
    yao_listener.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
    yao_listener.edit_idea_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    missing_belief_bases = list(yao_listener.get_missing_belief_bases().keys())

    yao_speaker = agendaunit_shop(yao_text)
    yao_speaker.set_belief(status_road, clean_road, create_missing_ideas=True)
    assert yao_listener.get_missing_belief_bases().keys() == {status_road}

    # WHEN
    listen_to_speaker_beliefs(yao_listener, yao_speaker, missing_belief_bases)

    # THEN
    assert len(yao_listener.get_missing_belief_bases().keys()) == 0


def test_set_listen_to_speaker_beliefs_DoesNotOverrideBelief():
    # GIVEN
    yao_text = "Yao"
    yao_listener = agendaunit_shop(yao_text)
    yao_listener.add_partyunit(yao_text)
    yao_listener.set_party_pool(20)
    casa_text = "casa"
    casa_road = yao_listener.make_l1_road(casa_text)
    status_text = "status"
    status_road = yao_listener.make_road(casa_road, status_text)
    clean_text = "clean"
    clean_road = yao_listener.make_road(status_road, clean_text)
    dirty_text = "dirty"
    dirty_road = yao_listener.make_road(status_road, dirty_text)
    sweep_text = "sweep"
    sweep_road = yao_listener.make_road(casa_road, sweep_text)
    fridge_text = "fridge"
    fridge_road = yao_listener.make_road(casa_road, fridge_text)
    running_text = "running"
    running_road = yao_listener.make_road(fridge_road, running_text)

    yao_listener.add_idea(ideaunit_shop(running_text), fridge_road)
    yao_listener.add_idea(ideaunit_shop(clean_text), status_road)
    yao_listener.add_idea(ideaunit_shop(dirty_text), status_road)
    yao_listener.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
    yao_listener.edit_idea_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    yao_listener.edit_idea_attr(
        sweep_road, reason_base=fridge_road, reason_premise=running_road
    )
    assert len(yao_listener.get_missing_belief_bases()) == 2
    yao_listener.set_belief(status_road, dirty_road)
    assert len(yao_listener.get_missing_belief_bases()) == 1
    assert yao_listener.get_belief(status_road).pick == dirty_road

    # WHEN
    yao_speaker = agendaunit_shop(yao_text)
    yao_speaker.set_belief(status_road, clean_road, create_missing_ideas=True)
    yao_speaker.set_belief(fridge_road, running_road, create_missing_ideas=True)
    missing_belief_bases = list(yao_listener.get_missing_belief_bases().keys())
    listen_to_speaker_beliefs(yao_listener, yao_speaker, missing_belief_bases)

    # THEN
    assert len(yao_listener.get_missing_belief_bases()) == 0
    # did not grab speaker's beliefunit
    assert yao_listener.get_belief(status_road).pick == dirty_road
    # grabed speaker's beliefunit
    assert yao_listener.get_belief(fridge_road).pick == running_road
