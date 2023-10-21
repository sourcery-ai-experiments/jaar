from pytest import raises as pytest_raises
from src.agenda.required_assign import (
    assigned_heir_shop,
    assigned_unit_shop,
)
from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideacore_shop
from src.agenda.group import groupunit_shop


def test_agenda_edit_idea_attr_CorrectlySetsAssignedUnit():
    # GIVEN
    healer_text = "Xio"
    x_agenda = agendaunit_shop(_healer=healer_text)
    run_text = "run"
    run_road = f"{x_agenda._culture_handle},{run_text}"
    x_agenda.add_idea(ideacore_shop(_label=run_text), pad=x_agenda._culture_handle)
    run_idea = x_agenda.get_idea_kid(road=run_road)
    assert run_idea._assignedunit is None

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
    x_agenda.edit_idea_attr(assignedunit=assigned_unit_x, road=x_agenda._culture_handle)
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
    run_text = "run"
    run_road = f"{bob_text},{run_text}"
    assigned_unit_x = assigned_unit_shop()

    x_agenda = agendaunit_shop(_healer=bob_text)
    x_agenda.add_partyunit(title=bob_text)
    x_agenda.add_idea(ideacore_shop(_label=run_text), pad=bob_text)
    x_agenda.edit_idea_attr(road=run_road, assignedunit=assigned_unit_x)
    run_idea = x_agenda.get_idea_kid(road=run_road)
    assert run_idea._assignedunit == assigned_unit_x
    assert run_idea._assignedheir is None

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert run_idea._assignedheir != None
    assert run_idea._assignedheir._group_party == False

    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None,
        assignunit=assigned_unit_x,
        agenda_groups=x_agenda._groups,
    )
    print(f"{assigned_heir_x._group_party=}")
    assert run_idea._assignedheir._group_party == assigned_heir_x._group_party
    assert run_idea._assignedheir == assigned_heir_x


def test_agenda_ideakid_assignedunit_CorrectlySets_grandchild_idea_assignedheir():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    swim_text = "swiming"
    swim_road = f"{x_agenda._culture_handle},{swim_text}"
    morn_text = "morning"
    morn_road = f"{swim_road},{morn_text}"
    four_text = "fourth"
    four_road = f"{morn_road},{four_text}"
    assigned_unit_x = assigned_unit_shop()
    swimmers_text = "swimmers"
    assigned_unit_x.set_suffgroup(title=swimmers_text)

    x_agenda.set_groupunit(groupunit=groupunit_shop(brand=swimmers_text))
    x_agenda.add_idea(ideacore_shop(_label=swim_text), pad=x_agenda._culture_handle)
    x_agenda.add_idea(ideacore_shop(_label=morn_text), pad=swim_road)
    x_agenda.add_idea(ideacore_shop(_label=four_text), pad=morn_road)
    x_agenda.edit_idea_attr(road=swim_road, assignedunit=assigned_unit_x)
    # print(f"{four_road=}\n{morn_road=}")
    four_idea = x_agenda.get_idea_kid(road=four_road)
    assert four_idea._assignedunit is None
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
    x_agenda1.add_partyunit(title=xia_text)
    x_agenda1.add_partyunit(title=zoa_text)

    work_text = "work"
    work_road = f"{x_agenda1._culture_handle},{work_text}"
    swim_text = "swim"
    swim_road = f"{x_agenda1._culture_handle},{swim_text}"
    x_agenda1.add_idea(ideacore_shop(_label=work_text), pad=x_agenda1._culture_handle)
    x_agenda1.add_idea(ideacore_shop(_label=swim_text), pad=x_agenda1._culture_handle)
    swim_assignedunit = assigned_unit_shop()
    swim_assignedunit.set_suffgroup(title=xia_text)
    swim_assignedunit.set_suffgroup(title=zoa_text)
    x_agenda1.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    x_agenda1_swim_idea = x_agenda1.get_idea_kid(swim_road)
    x_agenda1_swim_suffgroups = x_agenda1_swim_idea._assignedunit._suffgroups
    assert len(x_agenda1_swim_suffgroups) == 2

    # WHEN
    x_agenda2 = agendaunit_shop(_healer=healer_text)
    x_agenda2.add_partyunit(title=xia_text)
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
    x_agenda1.add_partyunit(title=xia_text)
    x_agenda1.add_partyunit(title=zoa_text)

    work_text = "work"
    work_road = f"{x_agenda1._culture_handle},{work_text}"
    swim_text = "swim"
    swim_road = f"{x_agenda1._culture_handle},{swim_text}"
    x_agenda1.add_idea(ideacore_shop(_label=work_text), pad=x_agenda1._culture_handle)
    x_agenda1.add_idea(ideacore_shop(_label=swim_text), pad=x_agenda1._culture_handle)
    swim_assignedunit = assigned_unit_shop()
    swim_assignedunit.set_suffgroup(title=xia_text)
    swim_assignedunit.set_suffgroup(title=zoa_text)
    x_agenda1.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    x_agenda1_swim_idea = x_agenda1.get_idea_kid(swim_road)
    x_agenda1_swim_suffgroups = x_agenda1_swim_idea._assignedunit._suffgroups
    assert len(x_agenda1_swim_suffgroups) == 2

    # WHEN
    x_agenda2 = agendaunit_shop(_healer=healer_text)
    x_agenda2.add_partyunit(title=xia_text)
    x_agenda2.add_idea(
        idea_kid=x_agenda1_swim_idea,
        pad=x_agenda2._culture_handle,
        create_missing_ideas_groups=False,
    )

    # THEN
    x_agenda2_swim_idea = x_agenda2.get_idea_kid(swim_road)
    x_agenda2_swim_suffgroups = x_agenda2_swim_idea._assignedunit._suffgroups
    assert len(x_agenda2_swim_suffgroups) == 1
    assert list(x_agenda2_swim_suffgroups) == [xia_text]
