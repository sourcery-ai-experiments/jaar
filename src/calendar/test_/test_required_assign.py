from src.calendar.required_assign import (
    AssignedUnit,
    assigned_unit_shop,
    AssignedHeir,
    assigned_heir_shop,
    #     RequiredHeir,
    #     RequiredUnit,
    #     acptfactheir_shop,
    #     sufffactunit_shop,
    #     Road,
)
from src.calendar.group import GroupName, groupunit_shop
from src.calendar.member import memberlink_shop
from src.calendar.calendar import CalendarUnit

# from pytest import raises as pytest_raises


def test_AssignedUnit_exists():
    # GIVEN
    _suffgroups_x = {1: 2}

    # WHEN
    assigned_unit_x = AssignedUnit(_suffgroups=_suffgroups_x)

    # THEN
    assert assigned_unit_x
    assert assigned_unit_x._suffgroups == _suffgroups_x


def test_assigned_unit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffgroups_x = {1: 2}
    _group_member_x = "example"

    # WHEN
    assigned_unit_x = assigned_unit_shop(_suffgroups=_suffgroups_x)

    # THEN
    assert assigned_unit_x
    assert assigned_unit_x._suffgroups == _suffgroups_x


def test_assigned_unit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    assigned_unit_x = assigned_unit_shop()

    # THEN
    assert assigned_unit_x
    assert assigned_unit_x._suffgroups == {}


def test_AssignedUnit_get_dict_ReturnsCorrectDictWithSingleSuffGroup():
    # GIVEN
    bob_group_name = GroupName("bob")
    _suffgroups_x = {bob_group_name: bob_group_name}
    assigned_x = assigned_unit_shop(_suffgroups=_suffgroups_x)

    # WHEN
    obj_dict = assigned_x.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_suffgroups": {bob_group_name: bob_group_name}}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_AssignedUnit_set_suffgroup_CorrectlySets_suffgroups_v1():
    # GIVEN
    assigned_unit_x = assigned_unit_shop(_suffgroups={})
    assert len(assigned_unit_x._suffgroups) == 0

    # WHEN
    jim_text = "jim"
    assigned_unit_x.set_suffgroup(name=jim_text)

    # THEN
    assert len(assigned_unit_x._suffgroups) == 1


def test_AssignedUnit_del_suffgroup_CorrectlyDeletes_suffgroups_v1():
    # GIVEN
    assigned_unit_x = assigned_unit_shop(_suffgroups={})
    jim_text = "jim"
    sue_text = "sue"
    assigned_unit_x.set_suffgroup(name=jim_text)
    assigned_unit_x.set_suffgroup(name=sue_text)
    assert len(assigned_unit_x._suffgroups) == 2

    # WHEN
    assigned_unit_x.del_suffgroup(name=sue_text)

    # THEN
    assert len(assigned_unit_x._suffgroups) == 1


def test_AssignedHeir_exists():
    # GIVEN
    _suffgroups_x = {1: 2}
    _group_member_x = "example"

    # WHEN
    assigned_heir_x = AssignedHeir(
        _suffgroups=_suffgroups_x, _group_member=_group_member_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffgroups == _suffgroups_x
    assert assigned_heir_x._group_member == _group_member_x


def test_assigned_heir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffgroups_x = {1: 2}
    _group_member_x = "example"

    # WHEN
    assigned_heir_x = assigned_heir_shop(
        _suffgroups=_suffgroups_x, _group_member=_group_member_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffgroups == _suffgroups_x
    assert assigned_heir_x._group_member == _group_member_x


def test_AssignedHeir_get_all_suff_members_CorrectlyReturnsSingleDictWithAllMembers_v1():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    c_x = CalendarUnit(_desc=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)

    _suffgroups_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)

    # WHEN
    all_members = assigned_heir_x._get_all_suff_members(calendar_groups=c_x._groups)

    # THEN
    assert len(all_members) == 1


def test_AssignedHeir_get_all_suff_members_CorrectlyReturnsSingleDictWithAllMembers_v2():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "bob"
    c_x = CalendarUnit(_desc=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)
    c_x.add_memberunit(name=bob_text)

    swim_text = "swim"
    swim_group = groupunit_shop(name=swim_text)
    swim_group.set_memberlink(memberlink=memberlink_shop(name=jim_text))
    swim_group.set_memberlink(memberlink=memberlink_shop(name=sue_text))
    c_x.set_groupunit(groupunit=swim_group)

    _suffgroups_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)

    # WHEN
    all_members = assigned_heir_x._get_all_suff_members(calendar_groups=c_x._groups)

    # THEN
    assert len(all_members) == 2


def test_AssignedHeir_set_group_member_CorrectlySetsAttribute_Empty_suffgroups_x():
    # GIVEN
    _suffgroups_x = {}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._group_member == False

    # WHEN
    calendar_groups = {}
    assigned_heir_x.set_group_member(calendar_groups=calendar_groups, calendar_owner="")

    # THEN
    assert assigned_heir_x._group_member


def test_AssignedHeir_set_group_member_CorrectlySetsAttribute_NonEmpty_suffgroups_x_v1():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"

    c_x = CalendarUnit(_desc=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)
    calendar_owner = c_x._desc
    calendar_groups = c_x._groups
    print(f"{len(calendar_groups)=}")
    # print(f"{calendar_groups.get(jim_text)=}")
    # print(f"{calendar_groups.get(sue_text)=}")

    _suffgroups_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._group_member == False

    # WHEN
    assigned_heir_x.set_group_member(calendar_groups, calendar_owner)

    # THEN
    assert assigned_heir_x._group_member


def test_AssignedHeir_set_group_member_CorrectlySetsAttribute_NonEmpty_suffgroups_x_v2():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"

    c_x = CalendarUnit(_desc=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)
    calendar_owner = c_x._desc
    calendar_groups = c_x._groups
    print(f"{len(calendar_groups)=}")
    # print(f"{calendar_groups.get(jim_text)=}")
    # print(f"{calendar_groups.get(sue_text)=}")

    _suffgroups_x = {sue_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._group_member == False

    # WHEN
    assigned_heir_x.set_group_member(calendar_groups, calendar_owner)

    # THEN
    assert assigned_heir_x._group_member == False


def test_AssignedHeir_set_group_member_CorrectlySetsAttribute_NonEmpty_suffgroups_x_v3():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "bob"
    c_x = CalendarUnit(_desc=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)
    c_x.add_memberunit(name=bob_text)

    swim_text = "swim"
    swim_group = groupunit_shop(name=swim_text)
    swim_group.set_memberlink(memberlink=memberlink_shop(name=jim_text))
    swim_group.set_memberlink(memberlink=memberlink_shop(name=sue_text))
    c_x.set_groupunit(groupunit=swim_group)

    _suffgroups_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._group_member == False
    assigned_heir_x.set_group_member(c_x._groups, c_x._desc)
    assert assigned_heir_x._group_member

    # WHEN
    swim_group.del_memberlink(name=jim_text)
    c_x.set_groupunit(groupunit=swim_group)
    assigned_heir_x.set_group_member(c_x._groups, c_x._desc)

    # THEN
    assert assigned_heir_x._group_member == False


def test_AssignedHeir_set__CorrectlySetsAttribute_NonEmpty_suffgroups_x_v3():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "bob"
    c_x = CalendarUnit(_desc=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)
    c_x.add_memberunit(name=bob_text)

    swim_text = "swim"
    swim_group = groupunit_shop(name=swim_text)
    swim_group.set_memberlink(memberlink=memberlink_shop(name=jim_text))
    swim_group.set_memberlink(memberlink=memberlink_shop(name=sue_text))
    c_x.set_groupunit(groupunit=swim_group)

    _suffgroups_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._group_member == False
    assigned_heir_x.set_group_member(c_x._groups, c_x._desc)
    assert assigned_heir_x._group_member

    # WHEN
    swim_group.del_memberlink(name=jim_text)
    c_x.set_groupunit(groupunit=swim_group)
    assigned_heir_x.set_group_member(c_x._groups, c_x._desc)

    # THEN
    assert assigned_heir_x._group_member == False


# def test_AssignedHeir_
#  tree traverse: Idea.AssignedUnit != None, parent_idea.AssignedHeir is None -> idea.AssignedHeir set by Idea.AssignedUnit
#  tree traverse: Idea.AssignedUnit is None, parent_idea.AssignedHeir != None -> idea.AssignedHeir set by parent_idea.AssignedHeir
#  tree traverse: Idea.AssignedUnit != None, parent_idea.AssignedHeir != None AND unit_members are subset of heir_members -> idea.AssignedHeir set by Idea.AssignedUnit
#  tree traverse: Idea.AssignedUnit != None, parent_idea.AssignedHeir != None AND unit_members are subset of heir_members -> raise Error
