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
from pytest import raises as pytest_raises


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
    c_x = CalendarUnit(_owner=jim_text)
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
    c_x = CalendarUnit(_owner=jim_text)
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

    c_x = CalendarUnit(_owner=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)
    calendar_owner = c_x._owner
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

    c_x = CalendarUnit(_owner=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)
    calendar_owner = c_x._owner
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
    c_x = CalendarUnit(_owner=jim_text)
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
    assigned_heir_x.set_group_member(c_x._groups, c_x._owner)
    assert assigned_heir_x._group_member

    # WHEN
    swim_group.del_memberlink(name=jim_text)
    c_x.set_groupunit(groupunit=swim_group)
    assigned_heir_x.set_group_member(c_x._groups, c_x._owner)

    # THEN
    assert assigned_heir_x._group_member == False


def test_AssignedHeir_set__CorrectlySetsAttribute_NonEmpty_suffgroups_x_v3():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "bob"
    c_x = CalendarUnit(_owner=jim_text)
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
    assigned_heir_x.set_group_member(c_x._groups, c_x._owner)
    assert assigned_heir_x._group_member

    # WHEN
    swim_group.del_memberlink(name=jim_text)
    c_x.set_groupunit(groupunit=swim_group)
    assigned_heir_x.set_group_member(c_x._groups, c_x._owner)

    # THEN
    assert assigned_heir_x._group_member == False


def test_AssignedHeir_set_suffgroup_AssignedUnitEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    assigned_heir_x = assigned_heir_shop(_suffgroups={})
    parent_assignheir_empty = assigned_heir_shop()
    assigned_unit_x = assigned_unit_shop()

    # WHEN
    assigned_heir_x.set_suffgroups(
        parent_assignheir=parent_assignheir_empty,
        assignunit=assigned_unit_x,
        calendar_groups=None,
    )

    # THEN
    assigned_heir_x._suffgroups = {}


def test_AssignedHeir_set_suffgroup_AssignedUnitNotEmpty_ParentAssignedHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = "swim"
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(name=kent_text)
    assigned_unit_x.set_suffgroup(name=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, calendar_groups=None
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == assigned_unit_x._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnitNotEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = "swim"
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(name=kent_text)
    assigned_unit_x.set_suffgroup(name=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    parent_assignheir_empty = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir_empty, assignunit=assigned_unit_x, calendar_groups=None
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == assigned_unit_x._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnitEmpty_ParentAssignedHeirNotEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = "swim"
    assigned_unit_swim = assigned_unit_shop()
    assigned_unit_swim.set_suffgroup(name=kent_text)
    assigned_unit_swim.set_suffgroup(name=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        empty_assigned_heir, assigned_unit_swim, calendar_groups=None
    )

    assigned_unit_empty = assigned_unit_shop()

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffgroups == {}
    assigned_heir_x.set_suffgroups(
        parent_assigned_heir, assignunit=assigned_unit_empty, calendar_groups=None
    )

    # THEN
    assert len(assigned_heir_x._suffgroups.keys())
    assert assigned_heir_x._suffgroups.keys() == parent_assigned_heir._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnitEqualParentAssignedHeir_NonEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = "swim"
    assigned_unit_swim = assigned_unit_shop()
    assigned_unit_swim.set_suffgroup(name=kent_text)
    assigned_unit_swim.set_suffgroup(name=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        empty_assigned_heir, assigned_unit_swim, calendar_groups=None
    )

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffgroups == {}
    assigned_heir_x.set_suffgroups(
        parent_assigned_heir, assignunit=assigned_unit_swim, calendar_groups=None
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == parent_assigned_heir._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnit_NotEqual_ParentAssignedHeir_NonEmpty():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "bob"
    tom_text = "tom"
    c_x = CalendarUnit(_owner=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)
    c_x.add_memberunit(name=bob_text)
    c_x.add_memberunit(name=tom_text)

    swim2_text = "swim2"
    swim2_group = groupunit_shop(name=swim2_text)
    swim2_group.set_memberlink(memberlink=memberlink_shop(name=jim_text))
    swim2_group.set_memberlink(memberlink=memberlink_shop(name=sue_text))
    c_x.set_groupunit(groupunit=swim2_group)

    swim3_text = "swim3"
    swim3_group = groupunit_shop(name=swim3_text)
    swim3_group.set_memberlink(memberlink=memberlink_shop(name=jim_text))
    swim3_group.set_memberlink(memberlink=memberlink_shop(name=sue_text))
    swim3_group.set_memberlink(memberlink=memberlink_shop(name=tom_text))
    c_x.set_groupunit(groupunit=swim3_group)

    parent_assigned_unit = assigned_unit_shop()
    parent_assigned_unit.set_suffgroup(name=swim3_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        parent_assignheir=None, assignunit=parent_assigned_unit, calendar_groups=None
    )

    assigned_unit_swim2 = assigned_unit_shop()
    assigned_unit_swim2.set_suffgroup(name=swim2_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assigned_heir, assigned_unit_swim2, calendar_groups=c_x._groups
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == assigned_unit_swim2._suffgroups.keys()
    assert len(assigned_heir_x._suffgroups.keys()) == 1
    assert list(assigned_heir_x._suffgroups) == [swim2_text]


def test_AssignedHeir_set_suffgroup_AssignedUnit_NotEqualParentAssignedHeir_RaisesError():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "bob"
    tom_text = "tom"
    c_x = CalendarUnit(_owner=jim_text)
    c_x.add_memberunit(name=jim_text)
    c_x.add_memberunit(name=sue_text)
    c_x.add_memberunit(name=bob_text)
    c_x.add_memberunit(name=tom_text)

    swim2_text = "swim2"
    swim2_group = groupunit_shop(name=swim2_text)
    swim2_group.set_memberlink(memberlink=memberlink_shop(name=jim_text))
    swim2_group.set_memberlink(memberlink=memberlink_shop(name=sue_text))
    c_x.set_groupunit(groupunit=swim2_group)

    swim3_text = "swim3"
    swim3_group = groupunit_shop(name=swim3_text)
    swim3_group.set_memberlink(memberlink=memberlink_shop(name=jim_text))
    swim3_group.set_memberlink(memberlink=memberlink_shop(name=sue_text))
    swim3_group.set_memberlink(memberlink=memberlink_shop(name=tom_text))
    c_x.set_groupunit(groupunit=swim3_group)

    parent_assigned_unit = assigned_unit_shop()
    parent_assigned_unit.set_suffgroup(name=swim2_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        parent_assignheir=None, assignunit=parent_assigned_unit, calendar_groups=None
    )

    assigned_unit_swim3 = assigned_unit_shop()
    assigned_unit_swim3.set_suffgroup(name=swim3_text)

    # WHEN / THEN
    assigned_heir_x = assigned_heir_shop()
    all_parent_assignedheir_members = {jim_text, sue_text}
    all_assignedunit_members = {jim_text, sue_text, tom_text}
    with pytest_raises(Exception) as excinfo:
        assigned_heir_x.set_suffgroups(
            parent_assigned_heir, assigned_unit_swim3, calendar_groups=c_x._groups
        )
    assert (
        str(excinfo.value)
        == f"parent_assigned_heir does not contain all members of the idea's assigned_unit\n{set(all_parent_assignedheir_members)=}\n\n{set(all_assignedunit_members)=}"
    )


def test_AssignedHeir_group_in_ReturnsCorrectBoolWhen_suffgroupsNotEmpty():
    # GIVEN
    swim_text = "swim"
    hike_text = "hike"
    swim_dict = {swim_text: -1}
    hike_dict = {hike_text: -1}
    assignedunit_x = assigned_unit_shop()
    assignedunit_x.set_suffgroup(name=swim_text)
    assignedunit_x.set_suffgroup(name=hike_text)
    assignedheir_x = assigned_heir_shop()
    assignedheir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assignedunit_x, calendar_groups=None
    )
    hunt_text = "hunt"
    hunt_dict = {hunt_text: -1}
    play_text = "play"
    play_dict = {play_text: -1}
    assert assignedheir_x._suffgroups.get(swim_text) != None
    assert assignedheir_x._suffgroups.get(hike_text) != None
    assert assignedheir_x._suffgroups.get(hunt_text) is None
    assert assignedheir_x._suffgroups.get(play_text) is None
    hunt_hike_dict = {hunt_text: -1, hike_text: -1}
    hunt_play_dict = {hunt_text: -1, play_text: -1}

    # WHEN / THEN
    assert assignedheir_x.group_in(swim_dict)
    assert assignedheir_x.group_in(hike_dict)
    assert assignedheir_x.group_in(hunt_dict) == False
    assert assignedheir_x.group_in(hunt_hike_dict)
    assert assignedheir_x.group_in(hunt_play_dict) == False


def test_AssignedHeir_group_in_ReturnsCorrectBoolWhen_suffgroupsEmpty():
    # GIVEN
    hike_text = "hike"
    hike_dict = {hike_text: -1}
    assignedunit_x = assigned_unit_shop()
    assignedheir_x = assigned_heir_shop()
    assignedheir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assignedunit_x, calendar_groups=None
    )
    hunt_text = "hunt"
    hunt_dict = {hunt_text: -1}
    play_text = "play"
    play_dict = {play_text: -1}
    assert assignedheir_x._suffgroups == {}
    hunt_hike_dict = {hunt_text: -1, hike_text: -1}
    hunt_play_dict = {hunt_text: -1, play_text: -1}

    # WHEN / THEN
    assert assignedheir_x.group_in(hike_dict)
    assert assignedheir_x.group_in(hunt_dict)
    assert assignedheir_x.group_in(play_dict)
    assert assignedheir_x.group_in(hunt_hike_dict)
    assert assignedheir_x.group_in(hunt_play_dict)
