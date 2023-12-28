from src.agenda.required_assign import assigned_heir_shop, assigned_unit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideacore_shop
from src.agenda.group import groupunit_shop


def test_agenda_edit_idea_attr_CorrectlySetsAssignedUnit():
    # GIVEN
    healer_text = "Xio"
    x_agenda = agendaunit_shop(_healer=healer_text)
    run_text = "run"
    run_road = x_agenda.make_l1_road(run_text)
    x_agenda.add_idea(ideacore_shop(run_text), parent_road=x_agenda._economy_id)
    run_idea = x_agenda.get_idea_obj(run_road)
    assert run_idea._assignedunit == assigned_unit_shop()

    # WHEN
    assigned_unit_x = assigned_unit_shop()
    x_agenda.edit_idea_attr(assignedunit=assigned_unit_x, road=run_road)

    # THEN
    assert run_idea._assignedunit == assigned_unit_x


def test_agenda_idearoot_assignedunit_CorrectlySets_idea_assignedheir():
    # GIVEN
    assigned_unit_x = assigned_unit_shop()

    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.edit_idea_attr(assignedunit=assigned_unit_x, road=x_agenda._economy_id)
    assert x_agenda._idearoot._assignedunit == assigned_unit_x
    assert x_agenda._idearoot._assignedheir is None

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, agenda_groups=None
    )
    assert x_agenda._idearoot._assignedheir != None
    assert x_agenda._idearoot._assignedheir == assigned_heir_x


def test_agenda_ideakid_assignedunit_EmptyCorrectlySets_idea_assignedheir():
    # GIVEN
    bob_text = "bob"
    assigned_unit_x = assigned_unit_shop()

    x_agenda = agendaunit_shop(_healer=bob_text)
    run_text = "run"
    run_road = x_agenda.make_road(bob_text, run_text)
    x_agenda.add_partyunit(pid=bob_text)
    x_agenda.add_idea(ideacore_shop(run_text), parent_road=x_agenda._economy_id)
    x_agenda.edit_idea_attr(road=run_road, assignedunit=assigned_unit_x)
    run_idea = x_agenda.get_idea_obj(run_road)
    assert run_idea._assignedunit == assigned_unit_x
    assert run_idea._assignedheir is None

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert run_idea._assignedheir != None
    assert run_idea._assignedheir._healer_assigned == False

    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None,
        assignunit=assigned_unit_x,
        agenda_groups=x_agenda._groups,
    )
    print(f"{assigned_heir_x._healer_assigned=}")
    assert run_idea._assignedheir._healer_assigned == assigned_heir_x._healer_assigned
    assert run_idea._assignedheir == assigned_heir_x


def test_agenda_ideakid_assignedunit_CorrectlySets_grandchild_idea_assignedheir():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    swim_text = "swiming"
    swim_road = x_agenda.make_l1_road(swim_text)
    morn_text = "morning"
    morn_road = x_agenda.make_road(swim_road, morn_text)
    four_text = "fourth"
    four_road = x_agenda.make_road(morn_road, four_text)
    assigned_unit_x = assigned_unit_shop()
    swimmers_text = "swimmers"
    assigned_unit_x.set_suffgroup(brand=swimmers_text)

    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=swimmers_text))
    x_agenda.add_idea(ideacore_shop(swim_text), parent_road=x_agenda._economy_id)
    x_agenda.add_idea(ideacore_shop(morn_text), parent_road=swim_road)
    x_agenda.add_idea(ideacore_shop(four_text), parent_road=morn_road)
    x_agenda.edit_idea_attr(road=swim_road, assignedunit=assigned_unit_x)
    # print(x_agenda.make_road(four_road=}\n{morn_road=))
    four_idea = x_agenda.get_idea_obj(four_road)
    assert four_idea._assignedunit == assigned_unit_shop()
    assert four_idea._assignedheir is None

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None,
        assignunit=assigned_unit_x,
        agenda_groups=x_agenda._groups,
    )
    assert four_idea._assignedheir != None
    assert four_idea._assignedheir == assigned_heir_x


def test_AgendaUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_AssignUnit():
    # GIVEN
    healer_text = "Noa"
    x_agenda1 = agendaunit_shop(_healer=healer_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x_agenda1.add_partyunit(pid=xia_text)
    x_agenda1.add_partyunit(pid=zoa_text)

    work_text = "work"
    work_road = x_agenda1.make_road(x_agenda1._economy_id, work_text)
    swim_text = "swim"
    swim_road = x_agenda1.make_road(x_agenda1._economy_id, swim_text)
    x_agenda1.add_idea(ideacore_shop(work_text), parent_road=x_agenda1._economy_id)
    x_agenda1.add_idea(ideacore_shop(swim_text), parent_road=x_agenda1._economy_id)
    swim_assignedunit = assigned_unit_shop()
    swim_assignedunit.set_suffgroup(brand=xia_text)
    swim_assignedunit.set_suffgroup(brand=zoa_text)
    x_agenda1.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    x_agenda1_swim_idea = x_agenda1.get_idea_obj(swim_road)
    x_agenda1_swim_suffgroups = x_agenda1_swim_idea._assignedunit._suffgroups
    assert len(x_agenda1_swim_suffgroups) == 2

    # WHEN
    x_agenda2 = agendaunit_shop(_healer=healer_text)
    x_agenda2.add_partyunit(pid=xia_text)
    filtered_idea = x_agenda2._get_filtered_balancelinks_idea(x_agenda1_swim_idea)

    # THEN
    filtered_swim_suffgroups = filtered_idea._assignedunit._suffgroups
    assert len(filtered_swim_suffgroups) == 1
    assert list(filtered_swim_suffgroups) == [xia_text]


def test_AgendaUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    healer_text = "Noa"
    x_agenda1 = agendaunit_shop(_healer=healer_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x_agenda1.add_partyunit(pid=xia_text)
    x_agenda1.add_partyunit(pid=zoa_text)

    work_text = "work"
    work_road = x_agenda1.make_road(x_agenda1._economy_id, work_text)
    swim_text = "swim"
    swim_road = x_agenda1.make_road(x_agenda1._economy_id, swim_text)
    x_agenda1.add_idea(ideacore_shop(work_text), parent_road=x_agenda1._economy_id)
    x_agenda1.add_idea(ideacore_shop(swim_text), parent_road=x_agenda1._economy_id)
    swim_assignedunit = assigned_unit_shop()
    swim_assignedunit.set_suffgroup(brand=xia_text)
    swim_assignedunit.set_suffgroup(brand=zoa_text)
    x_agenda1.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    x_agenda1_swim_idea = x_agenda1.get_idea_obj(swim_road)
    x_agenda1_swim_suffgroups = x_agenda1_swim_idea._assignedunit._suffgroups
    assert len(x_agenda1_swim_suffgroups) == 2

    # WHEN
    x_agenda2 = agendaunit_shop(_healer=healer_text)
    x_agenda2.add_partyunit(pid=xia_text)
    x_agenda2.add_idea(
        idea_kid=x_agenda1_swim_idea,
        parent_road=x_agenda2._economy_id,
        create_missing_ideas_groups=False,
    )

    # THEN
    x_agenda2_swim_idea = x_agenda2.get_idea_obj(swim_road)
    x_agenda2_swim_suffgroups = x_agenda2_swim_idea._assignedunit._suffgroups
    assert len(x_agenda2_swim_suffgroups) == 1
    assert list(x_agenda2_swim_suffgroups) == [xia_text]
