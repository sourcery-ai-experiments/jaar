from pytest import raises as pytest_raises
from src.contract.required_assign import (
    assigned_heir_shop,
    assigned_unit_shop,
)
from src.contract.contract import ContractUnit
from src.contract.idea import IdeaKid
from src.contract.group import groupunit_shop


def test_contract_edit_idea_attr_CorrectlySetsAssignedUnit():
    # GIVEN
    owner_text = "Xio"
    cx = ContractUnit(_owner=owner_text)
    run_text = "run"
    run_road = f"{cx._goal_kind},{run_text}"
    cx.add_idea(IdeaKid(_label=run_text), walk=cx._goal_kind)
    run_idea = cx.get_idea_kid(road=run_road)
    assert run_idea._assignedunit is None

    # WHEN
    assigned_unit_x = assigned_unit_shop()
    cx.edit_idea_attr(assignedunit=assigned_unit_x, road=run_road)

    # THEN
    assert run_idea._assignedunit == assigned_unit_x


def test_contract_idearoot_assignedunit_CorrectlySets_idea_assignedheir():
    # GIVEN
    assigned_unit_x = assigned_unit_shop()

    owner_text = "Tim"
    cx = ContractUnit(_owner=owner_text)
    cx.edit_idea_attr(assignedunit=assigned_unit_x, road=cx._goal_kind)
    assert cx._idearoot._assignedunit == assigned_unit_x
    assert cx._idearoot._assignedheir is None

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, contract_groups=None
    )
    assert cx._idearoot._assignedheir != None
    assert cx._idearoot._assignedheir == assigned_heir_x


def test_contract_ideakid_assignedunit_EmptyCorrectlySets_idea_assignedheir():
    # GIVEN
    bob_text = "bob"
    run_text = "run"
    run_road = f"{bob_text},{run_text}"
    assigned_unit_x = assigned_unit_shop()

    cx = ContractUnit(_owner=bob_text)
    cx.add_partyunit(title=bob_text)
    cx.add_idea(IdeaKid(_label=run_text), walk=bob_text)
    cx.edit_idea_attr(road=run_road, assignedunit=assigned_unit_x)
    run_idea = cx.get_idea_kid(road=run_road)
    assert run_idea._assignedunit == assigned_unit_x
    assert run_idea._assignedheir is None

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assert run_idea._assignedheir != None
    assert run_idea._assignedheir._group_party == False

    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, contract_groups=cx._groups
    )
    print(f"{assigned_heir_x._group_party=}")
    assert run_idea._assignedheir._group_party == assigned_heir_x._group_party
    assert run_idea._assignedheir == assigned_heir_x


def test_contract_ideakid_assignedunit_CorrectlySets_grandchild_idea_assignedheir():
    # GIVEN
    owner_text = "Noa"
    cx = ContractUnit(_owner=owner_text)
    swim_text = "swiming"
    swim_road = f"{cx._goal_kind},{swim_text}"
    morn_text = "morning"
    morn_road = f"{swim_road},{morn_text}"
    four_text = "fourth"
    four_road = f"{morn_road},{four_text}"
    assigned_unit_x = assigned_unit_shop()
    swimmers_text = "swimmers"
    assigned_unit_x.set_suffgroup(title=swimmers_text)

    cx.set_groupunit(groupunit=groupunit_shop(brand=swimmers_text))
    cx.add_idea(IdeaKid(_label=swim_text), walk=cx._goal_kind)
    cx.add_idea(IdeaKid(_label=morn_text), walk=swim_road)
    cx.add_idea(IdeaKid(_label=four_text), walk=morn_road)
    cx.edit_idea_attr(road=swim_road, assignedunit=assigned_unit_x)
    # print(f"{four_road=}\n{morn_road=}")
    four_idea = cx.get_idea_kid(road=four_road)
    assert four_idea._assignedunit is None
    assert four_idea._assignedheir is None

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, contract_groups=cx._groups
    )
    assert four_idea._assignedheir != None
    assert four_idea._assignedheir == assigned_heir_x


def test_ContractUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_AssignUnit():
    # GIVEN
    owner_text = "Noa"
    cx1 = ContractUnit(_owner=owner_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    cx1.add_partyunit(title=xia_text)
    cx1.add_partyunit(title=zoa_text)

    work_text = "work"
    work_road = f"{cx1._goal_kind},{work_text}"
    swim_text = "swim"
    swim_road = f"{cx1._goal_kind},{swim_text}"
    cx1.add_idea(IdeaKid(_label=work_text), walk=cx1._goal_kind)
    cx1.add_idea(IdeaKid(_label=swim_text), walk=cx1._goal_kind)
    swim_assignedunit = assigned_unit_shop()
    swim_assignedunit.set_suffgroup(title=xia_text)
    swim_assignedunit.set_suffgroup(title=zoa_text)
    cx1.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    cx1_swim_idea = cx1.get_idea_kid(swim_road)
    cx1_swim_suffgroups = cx1_swim_idea._assignedunit._suffgroups
    assert len(cx1_swim_suffgroups) == 2

    # WHEN
    cx2 = ContractUnit(_owner=owner_text)
    cx2.add_partyunit(title=xia_text)
    filtered_idea = cx2._get_filtered_balancelinks_idea(cx1_swim_idea)

    # THEN
    filtered_swim_suffgroups = filtered_idea._assignedunit._suffgroups
    assert len(filtered_swim_suffgroups) == 1
    assert list(filtered_swim_suffgroups) == [xia_text]


def test_ContractUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    owner_text = "Noa"
    cx1 = ContractUnit(_owner=owner_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    cx1.add_partyunit(title=xia_text)
    cx1.add_partyunit(title=zoa_text)

    work_text = "work"
    work_road = f"{cx1._goal_kind},{work_text}"
    swim_text = "swim"
    swim_road = f"{cx1._goal_kind},{swim_text}"
    cx1.add_idea(IdeaKid(_label=work_text), walk=cx1._goal_kind)
    cx1.add_idea(IdeaKid(_label=swim_text), walk=cx1._goal_kind)
    swim_assignedunit = assigned_unit_shop()
    swim_assignedunit.set_suffgroup(title=xia_text)
    swim_assignedunit.set_suffgroup(title=zoa_text)
    cx1.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    cx1_swim_idea = cx1.get_idea_kid(swim_road)
    cx1_swim_suffgroups = cx1_swim_idea._assignedunit._suffgroups
    assert len(cx1_swim_suffgroups) == 2

    # WHEN
    cx2 = ContractUnit(_owner=owner_text)
    cx2.add_partyunit(title=xia_text)
    cx2.add_idea(
        idea_kid=cx1_swim_idea,
        walk=cx2._goal_kind,
        create_missing_ideas_groups=False,
    )

    # THEN
    cx2_swim_idea = cx2.get_idea_kid(swim_road)
    cx2_swim_suffgroups = cx2_swim_idea._assignedunit._suffgroups
    assert len(cx2_swim_suffgroups) == 1
    assert list(cx2_swim_suffgroups) == [xia_text]
