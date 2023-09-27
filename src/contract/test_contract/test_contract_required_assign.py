from pytest import raises as pytest_raises
from src.contract.required_assign import (
    assigned_heir_shop,
    assigned_unit_shop,
)
from src.contract.contract import ContractUnit
from src.contract.idea import IdeaKid
from src.contract.group import groupunit_shop
from src.contract.road import get_economy_root_label as root_label


def test_contract_edit_idea_attr_CorrectlySetsAssignedUnit():
    # GIVEN
    owner_text = "Xio"
    c_x = ContractUnit(_owner=owner_text)
    run_text = "run"
    run_road = f"{root_label()},{run_text}"
    c_x.add_idea(IdeaKid(_label=run_text), walk=root_label())
    run_idea = c_x.get_idea_kid(road=run_road)
    assert run_idea._assignedunit is None

    # WHEN
    assigned_unit_x = assigned_unit_shop()
    c_x.edit_idea_attr(assignedunit=assigned_unit_x, road=run_road)

    # THEN
    assert run_idea._assignedunit == assigned_unit_x


def test_contract_idearoot_assignedunit_CorrectlySets_idea_assignedheir():
    # GIVEN
    assigned_unit_x = assigned_unit_shop()

    owner_text = "Tim"
    c_x = ContractUnit(_owner=owner_text)
    c_x.edit_idea_attr(assignedunit=assigned_unit_x, road=root_label())
    assert c_x._idearoot._assignedunit == assigned_unit_x
    assert c_x._idearoot._assignedheir is None

    # WHEN
    c_x.set_contract_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, contract_groups=None
    )
    assert c_x._idearoot._assignedheir != None
    assert c_x._idearoot._assignedheir == assigned_heir_x


def test_contract_ideakid_assignedunit_EmptyCorrectlySets_idea_assignedheir():
    # GIVEN
    bob_text = "bob"
    run_text = "run"
    run_road = f"{bob_text},{run_text}"
    assigned_unit_x = assigned_unit_shop()

    c_x = ContractUnit(_owner=bob_text)
    c_x.add_memberunit(name=bob_text)
    c_x.add_idea(IdeaKid(_label=run_text), walk=bob_text)
    c_x.edit_idea_attr(road=run_road, assignedunit=assigned_unit_x)
    run_idea = c_x.get_idea_kid(road=run_road)
    assert run_idea._assignedunit == assigned_unit_x
    assert run_idea._assignedheir is None

    # WHEN
    c_x.set_contract_metrics()

    # THEN
    assert run_idea._assignedheir != None
    assert run_idea._assignedheir._group_member == False

    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, contract_groups=c_x._groups
    )
    print(f"{assigned_heir_x._group_member=}")
    assert run_idea._assignedheir._group_member == assigned_heir_x._group_member
    assert run_idea._assignedheir == assigned_heir_x


def test_contract_ideakid_assignedunit_CorrectlySets_grandchild_idea_assignedheir():
    # GIVEN
    owner_text = "Noa"
    swim_text = "swiming"
    swim_road = f"{root_label()},{swim_text}"
    morn_text = "morning"
    morn_road = f"{swim_road},{morn_text}"
    four_text = "fourth"
    four_road = f"{morn_road},{four_text}"
    assigned_unit_x = assigned_unit_shop()
    swimmers_text = "swimmers"
    assigned_unit_x.set_suffgroup(name=swimmers_text)

    c_x = ContractUnit(_owner=owner_text)
    c_x.set_groupunit(groupunit=groupunit_shop(name=swimmers_text))
    c_x.add_idea(IdeaKid(_label=swim_text), walk=root_label())
    c_x.add_idea(IdeaKid(_label=morn_text), walk=swim_road)
    c_x.add_idea(IdeaKid(_label=four_text), walk=morn_road)
    c_x.edit_idea_attr(road=swim_road, assignedunit=assigned_unit_x)
    # print(f"{four_road=}\n{morn_road=}")
    four_idea = c_x.get_idea_kid(road=four_road)
    assert four_idea._assignedunit is None
    assert four_idea._assignedheir is None

    # WHEN
    c_x.set_contract_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, contract_groups=c_x._groups
    )
    assert four_idea._assignedheir != None
    assert four_idea._assignedheir == assigned_heir_x
