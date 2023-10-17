from pytest import raises as pytest_raises
from src.pact.required_assign import (
    assigned_heir_shop,
    assigned_unit_shop,
)
from src.pact.pact import PactUnit
from src.pact.idea import IdeaKid
from src.pact.group import groupunit_shop


def test_pact_edit_idea_attr_CorrectlySetsAssignedUnit():
    # GIVEN
    healer_text = "Xio"
    x_pact = PactUnit(_healer=healer_text)
    run_text = "run"
    run_road = f"{x_pact._cure_handle},{run_text}"
    x_pact.add_idea(IdeaKid(_label=run_text), pad=x_pact._cure_handle)
    run_idea = x_pact.get_idea_kid(road=run_road)
    assert run_idea._assignedunit is None

    # WHEN
    assigned_unit_x = assigned_unit_shop()
    x_pact.edit_idea_attr(assignedunit=assigned_unit_x, road=run_road)

    # THEN
    assert run_idea._assignedunit == assigned_unit_x


def test_pact_idearoot_assignedunit_CorrectlySets_idea_assignedheir():
    # GIVEN
    assigned_unit_x = assigned_unit_shop()

    healer_text = "Tim"
    x_pact = PactUnit(_healer=healer_text)
    x_pact.edit_idea_attr(assignedunit=assigned_unit_x, road=x_pact._cure_handle)
    assert x_pact._idearoot._assignedunit == assigned_unit_x
    assert x_pact._idearoot._assignedheir is None

    # WHEN
    x_pact.set_pact_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, pact_groups=None
    )
    assert x_pact._idearoot._assignedheir != None
    assert x_pact._idearoot._assignedheir == assigned_heir_x


def test_pact_ideakid_assignedunit_EmptyCorrectlySets_idea_assignedheir():
    # GIVEN
    bob_text = "bob"
    run_text = "run"
    run_road = f"{bob_text},{run_text}"
    assigned_unit_x = assigned_unit_shop()

    x_pact = PactUnit(_healer=bob_text)
    x_pact.add_partyunit(title=bob_text)
    x_pact.add_idea(IdeaKid(_label=run_text), pad=bob_text)
    x_pact.edit_idea_attr(road=run_road, assignedunit=assigned_unit_x)
    run_idea = x_pact.get_idea_kid(road=run_road)
    assert run_idea._assignedunit == assigned_unit_x
    assert run_idea._assignedheir is None

    # WHEN
    x_pact.set_pact_metrics()

    # THEN
    assert run_idea._assignedheir != None
    assert run_idea._assignedheir._group_party == False

    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, pact_groups=x_pact._groups
    )
    print(f"{assigned_heir_x._group_party=}")
    assert run_idea._assignedheir._group_party == assigned_heir_x._group_party
    assert run_idea._assignedheir == assigned_heir_x


def test_pact_ideakid_assignedunit_CorrectlySets_grandchild_idea_assignedheir():
    # GIVEN
    healer_text = "Noa"
    x_pact = PactUnit(_healer=healer_text)
    swim_text = "swiming"
    swim_road = f"{x_pact._cure_handle},{swim_text}"
    morn_text = "morning"
    morn_road = f"{swim_road},{morn_text}"
    four_text = "fourth"
    four_road = f"{morn_road},{four_text}"
    assigned_unit_x = assigned_unit_shop()
    swimmers_text = "swimmers"
    assigned_unit_x.set_suffgroup(title=swimmers_text)

    x_pact.set_groupunit(groupunit=groupunit_shop(brand=swimmers_text))
    x_pact.add_idea(IdeaKid(_label=swim_text), pad=x_pact._cure_handle)
    x_pact.add_idea(IdeaKid(_label=morn_text), pad=swim_road)
    x_pact.add_idea(IdeaKid(_label=four_text), pad=morn_road)
    x_pact.edit_idea_attr(road=swim_road, assignedunit=assigned_unit_x)
    # print(f"{four_road=}\n{morn_road=}")
    four_idea = x_pact.get_idea_kid(road=four_road)
    assert four_idea._assignedunit is None
    assert four_idea._assignedheir is None

    # WHEN
    x_pact.set_pact_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, pact_groups=x_pact._groups
    )
    assert four_idea._assignedheir != None
    assert four_idea._assignedheir == assigned_heir_x


def test_PactUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_AssignUnit():
    # GIVEN
    healer_text = "Noa"
    x_pact1 = PactUnit(_healer=healer_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x_pact1.add_partyunit(title=xia_text)
    x_pact1.add_partyunit(title=zoa_text)

    work_text = "work"
    work_road = f"{x_pact1._cure_handle},{work_text}"
    swim_text = "swim"
    swim_road = f"{x_pact1._cure_handle},{swim_text}"
    x_pact1.add_idea(IdeaKid(_label=work_text), pad=x_pact1._cure_handle)
    x_pact1.add_idea(IdeaKid(_label=swim_text), pad=x_pact1._cure_handle)
    swim_assignedunit = assigned_unit_shop()
    swim_assignedunit.set_suffgroup(title=xia_text)
    swim_assignedunit.set_suffgroup(title=zoa_text)
    x_pact1.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    x_pact1_swim_idea = x_pact1.get_idea_kid(swim_road)
    x_pact1_swim_suffgroups = x_pact1_swim_idea._assignedunit._suffgroups
    assert len(x_pact1_swim_suffgroups) == 2

    # WHEN
    x_pact2 = PactUnit(_healer=healer_text)
    x_pact2.add_partyunit(title=xia_text)
    filtered_idea = x_pact2._get_filtered_balancelinks_idea(x_pact1_swim_idea)

    # THEN
    filtered_swim_suffgroups = filtered_idea._assignedunit._suffgroups
    assert len(filtered_swim_suffgroups) == 1
    assert list(filtered_swim_suffgroups) == [xia_text]


def test_PactUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    healer_text = "Noa"
    x_pact1 = PactUnit(_healer=healer_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x_pact1.add_partyunit(title=xia_text)
    x_pact1.add_partyunit(title=zoa_text)

    work_text = "work"
    work_road = f"{x_pact1._cure_handle},{work_text}"
    swim_text = "swim"
    swim_road = f"{x_pact1._cure_handle},{swim_text}"
    x_pact1.add_idea(IdeaKid(_label=work_text), pad=x_pact1._cure_handle)
    x_pact1.add_idea(IdeaKid(_label=swim_text), pad=x_pact1._cure_handle)
    swim_assignedunit = assigned_unit_shop()
    swim_assignedunit.set_suffgroup(title=xia_text)
    swim_assignedunit.set_suffgroup(title=zoa_text)
    x_pact1.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    x_pact1_swim_idea = x_pact1.get_idea_kid(swim_road)
    x_pact1_swim_suffgroups = x_pact1_swim_idea._assignedunit._suffgroups
    assert len(x_pact1_swim_suffgroups) == 2

    # WHEN
    x_pact2 = PactUnit(_healer=healer_text)
    x_pact2.add_partyunit(title=xia_text)
    x_pact2.add_idea(
        idea_kid=x_pact1_swim_idea,
        pad=x_pact2._cure_handle,
        create_missing_ideas_groups=False,
    )

    # THEN
    x_pact2_swim_idea = x_pact2.get_idea_kid(swim_road)
    x_pact2_swim_suffgroups = x_pact2_swim_idea._assignedunit._suffgroups
    assert len(x_pact2_swim_suffgroups) == 1
    assert list(x_pact2_swim_suffgroups) == [xia_text]
