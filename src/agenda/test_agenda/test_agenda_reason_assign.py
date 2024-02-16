from src.agenda.reason_assign import assigned_heir_shop, assignedunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.group import groupunit_shop


def test_agenda_edit_idea_attr_CorrectlySetsAssignedUnit():
    # GIVEN
    xio_agenda = agendaunit_shop("Xio")
    run_text = "run"
    run_road = xio_agenda.make_l1_road(run_text)
    xio_agenda.add_l1_idea(ideaunit_shop(run_text))
    run_idea = xio_agenda.get_idea_obj(run_road)
    assert run_idea._assignedunit == assignedunit_shop()

    # WHEN
    assignedunit_x = assignedunit_shop()
    xio_agenda.edit_idea_attr(assignedunit=assignedunit_x, road=run_road)

    # THEN
    assert run_idea._assignedunit == assignedunit_x


def test_agenda_idearoot_assignedunit_CorrectlySets_idea_assignedheir():
    # GIVEN
    assignedunit_x = assignedunit_shop()

    tim_agenda = agendaunit_shop("Tim")
    tim_agenda.edit_idea_attr(assignedunit=assignedunit_x, road=tim_agenda._world_id)
    assert tim_agenda._idearoot._assignedunit == assignedunit_x
    assert tim_agenda._idearoot._assignedheir is None

    # WHEN
    tim_agenda.set_agenda_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assignedunit_x, agenda_groups=None
    )
    assert tim_agenda._idearoot._assignedheir != None
    assert tim_agenda._idearoot._assignedheir == assigned_heir_x


def test_agenda_ideakid_assignedunit_EmptyCorrectlySets_idea_assignedheir():
    # GIVEN
    bob_text = "Bob"
    assignedunit_x = assignedunit_shop()

    bob_agenda = agendaunit_shop(bob_text)
    run_text = "run"
    run_road = bob_agenda.make_road(bob_text, run_text)
    bob_agenda.add_partyunit(party_id=bob_text)
    bob_agenda.add_l1_idea(ideaunit_shop(run_text))
    bob_agenda.edit_idea_attr(road=run_road, assignedunit=assignedunit_x)
    run_idea = bob_agenda.get_idea_obj(run_road)
    assert run_idea._assignedunit == assignedunit_x
    assert run_idea._assignedheir is None

    # WHEN
    bob_agenda.set_agenda_metrics()

    # THEN
    assert run_idea._assignedheir != None
    assert run_idea._assignedheir._agent_id_assigned == False

    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None,
        assignunit=assignedunit_x,
        agenda_groups=bob_agenda._groups,
    )
    print(f"{assigned_heir_x._agent_id_assigned=}")
    assert (
        run_idea._assignedheir._agent_id_assigned == assigned_heir_x._agent_id_assigned
    )
    assert run_idea._assignedheir == assigned_heir_x


def test_agenda_ideakid_assignedunit_CorrectlySets_grandchild_idea_assignedheir():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    swim_text = "swimming"
    swim_road = noa_agenda.make_l1_road(swim_text)
    morn_text = "morning"
    morn_road = noa_agenda.make_road(swim_road, morn_text)
    four_text = "fourth"
    four_road = noa_agenda.make_road(morn_road, four_text)
    assignedunit_x = assignedunit_shop()
    swimmers_text = ",swimmers"
    assignedunit_x.set_suffgroup(group_id=swimmers_text)

    noa_agenda.set_groupunit(y_groupunit=groupunit_shop(group_id=swimmers_text))
    noa_agenda.add_l1_idea(ideaunit_shop(swim_text))
    noa_agenda.add_idea(ideaunit_shop(morn_text), parent_road=swim_road)
    noa_agenda.add_idea(ideaunit_shop(four_text), parent_road=morn_road)
    noa_agenda.edit_idea_attr(road=swim_road, assignedunit=assignedunit_x)
    # print(noa_agenda.make_road(four_road=}\n{morn_road=))
    four_idea = noa_agenda.get_idea_obj(four_road)
    assert four_idea._assignedunit == assignedunit_shop()
    assert four_idea._assignedheir is None

    # WHEN
    noa_agenda.set_agenda_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None,
        assignunit=assignedunit_x,
        agenda_groups=noa_agenda._groups,
    )
    assert four_idea._assignedheir != None
    assert four_idea._assignedheir == assigned_heir_x


def test_AgendaUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_AssignUnit():
    # GIVEN
    noa_text = "Noa"
    noa1_agenda = agendaunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    noa1_agenda.add_partyunit(party_id=xia_text)
    noa1_agenda.add_partyunit(party_id=zoa_text)

    gig_text = "gig"
    gig_road = noa1_agenda.make_l1_road(gig_text)
    swim_text = "swim"
    swim_road = noa1_agenda.make_l1_road(swim_text)
    noa1_agenda.add_idea(ideaunit_shop(gig_text), parent_road=noa1_agenda._world_id)
    noa1_agenda.add_idea(ideaunit_shop(swim_text), parent_road=noa1_agenda._world_id)
    swim_assignedunit = assignedunit_shop()
    swim_assignedunit.set_suffgroup(group_id=xia_text)
    swim_assignedunit.set_suffgroup(group_id=zoa_text)
    noa1_agenda.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    noa1_agenda_swim_idea = noa1_agenda.get_idea_obj(swim_road)
    noa1_agenda_swim_suffgroups = noa1_agenda_swim_idea._assignedunit._suffgroups
    assert len(noa1_agenda_swim_suffgroups) == 2

    # WHEN
    noa2_agenda = agendaunit_shop(noa_text)
    noa2_agenda.add_partyunit(party_id=xia_text)
    filtered_idea = noa2_agenda._get_filtered_balancelinks_idea(noa1_agenda_swim_idea)

    # THEN
    filtered_swim_suffgroups = filtered_idea._assignedunit._suffgroups
    assert len(filtered_swim_suffgroups) == 1
    assert list(filtered_swim_suffgroups) == [xia_text]


def test_AgendaUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    noa1_agenda = agendaunit_shop("Noa")
    xia_text = "Xia"
    zoa_text = "Zoa"
    noa1_agenda.add_partyunit(party_id=xia_text)
    noa1_agenda.add_partyunit(party_id=zoa_text)

    gig_text = "gig"
    gig_road = noa1_agenda.make_l1_road(gig_text)
    swim_text = "swim"
    swim_road = noa1_agenda.make_l1_road(swim_text)
    noa1_agenda.add_idea(ideaunit_shop(gig_text), parent_road=noa1_agenda._world_id)
    noa1_agenda.add_idea(ideaunit_shop(swim_text), parent_road=noa1_agenda._world_id)
    swim_assignedunit = assignedunit_shop()
    swim_assignedunit.set_suffgroup(group_id=xia_text)
    swim_assignedunit.set_suffgroup(group_id=zoa_text)
    noa1_agenda.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    noa1_agenda_swim_idea = noa1_agenda.get_idea_obj(swim_road)
    noa1_agenda_swim_suffgroups = noa1_agenda_swim_idea._assignedunit._suffgroups
    assert len(noa1_agenda_swim_suffgroups) == 2

    # WHEN
    noa2_agenda = agendaunit_shop("Noa")
    noa2_agenda.add_partyunit(party_id=xia_text)
    noa2_agenda.add_l1_idea(noa1_agenda_swim_idea, create_missing_ideas_groups=False)

    # THEN
    noa2_agenda_swim_idea = noa2_agenda.get_idea_obj(swim_road)
    noa2_agenda_swim_suffgroups = noa2_agenda_swim_idea._assignedunit._suffgroups
    assert len(noa2_agenda_swim_suffgroups) == 1
    assert list(noa2_agenda_swim_suffgroups) == [xia_text]
