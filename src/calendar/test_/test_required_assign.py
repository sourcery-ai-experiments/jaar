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
from src.calendar.group import GroupName

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
    _group_member_status_x = "example"

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
    example_dict = {
        "_suffgroups": {bob_group_name: bob_group_name},
    }
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_AssignedHeir_exists():
    # GIVEN
    _suffgroups_x = {1: 2}
    _group_member_status_x = "example"

    # WHEN
    assigned_heir_x = AssignedHeir(
        _suffgroups=_suffgroups_x, _group_member_status=_group_member_status_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffgroups == _suffgroups_x
    assert assigned_heir_x._group_member_status == _group_member_status_x


def test_assigned_heir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffgroups_x = {1: 2}
    _group_member_status_x = "example"

    # WHEN
    assigned_heir_x = assigned_heir_shop(
        _suffgroups=_suffgroups_x, _group_member_status=_group_member_status_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffgroups == _suffgroups_x
    assert assigned_heir_x._group_member_status == _group_member_status_x
