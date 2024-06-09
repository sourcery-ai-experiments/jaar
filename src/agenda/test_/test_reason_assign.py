from src.agenda.reason_assign import (
    AssignedUnit,
    assignedunit_shop,
    AssignedHeir,
    assigned_heir_shop,
    create_assignedunit,
)
from src.agenda.group import GroupID, groupunit_shop
from src.agenda.party import partylink_shop
from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_AssignedUnit_exists():
    # GIVEN
    _suffgroups_x = {1: 2}

    # WHEN
    assignedunit_x = AssignedUnit(_suffgroups=_suffgroups_x)

    # THEN
    assert assignedunit_x
    assert assignedunit_x._suffgroups == _suffgroups_x


def test_assignedunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffgroups_x = {1: 2}

    # WHEN
    assignedunit_x = assignedunit_shop(_suffgroups=_suffgroups_x)

    # THEN
    assert assignedunit_x
    assert assignedunit_x._suffgroups == _suffgroups_x


def test_assignedunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    assignedunit_x = assignedunit_shop()

    # THEN
    assert assignedunit_x
    assert assignedunit_x._suffgroups == {}


def test_create_assignedunit_ReturnsCorrectObj():
    # GIVEN
    swim_group_id = GroupID("swimmers")

    # WHEN
    swim_assignedunit = create_assignedunit(swim_group_id)

    # THEN
    assert swim_assignedunit
    assert len(swim_assignedunit._suffgroups) == 1


def test_AssignedUnit_get_dict_ReturnsCorrectDictWithSingleSuffGroup():
    # GIVEN
    bob_group_id = GroupID("Bob")
    _suffgroups_x = {bob_group_id: bob_group_id}
    assigned_x = assignedunit_shop(_suffgroups=_suffgroups_x)

    # WHEN
    obj_dict = assigned_x.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_suffgroups": {bob_group_id: bob_group_id}}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_AssignedUnit_set_suffgroup_CorrectlySets_suffgroups_v1():
    # GIVEN
    assignedunit_x = assignedunit_shop(_suffgroups={})
    assert len(assignedunit_x._suffgroups) == 0

    # WHEN
    jim_text = "Jim"
    assignedunit_x.set_suffgroup(group_id=jim_text)

    # THEN
    assert len(assignedunit_x._suffgroups) == 1


def test_AssignedUnit_suffgroup_exists_ReturnsCorrectObj():
    # GIVEN
    assignedunit_x = assignedunit_shop(_suffgroups={})
    jim_text = "Jim"
    assert assignedunit_x.suffgroup_exists(jim_text) is False

    # WHEN
    assignedunit_x.set_suffgroup(group_id=jim_text)

    # THEN
    assert assignedunit_x.suffgroup_exists(jim_text)


def test_AssignedUnit_del_suffgroup_CorrectlyDeletes_suffgroups_v1():
    # GIVEN
    assignedunit_x = assignedunit_shop(_suffgroups={})
    jim_text = "Jim"
    sue_text = "Sue"
    assignedunit_x.set_suffgroup(group_id=jim_text)
    assignedunit_x.set_suffgroup(group_id=sue_text)
    assert len(assignedunit_x._suffgroups) == 2

    # WHEN
    assignedunit_x.del_suffgroup(group_id=sue_text)

    # THEN
    assert len(assignedunit_x._suffgroups) == 1


def test_AssignedHeir_exists():
    # GIVEN
    _suffgroups_x = {1: 2}
    _owner_id_assigned_x = True

    # WHEN
    assigned_heir_x = AssignedHeir(
        _suffgroups=_suffgroups_x, _owner_id_assigned=_owner_id_assigned_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffgroups == _suffgroups_x
    assert assigned_heir_x._owner_id_assigned == _owner_id_assigned_x


def test_assigned_heir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffgroups_x = {1: 2}
    _owner_id_assigned_x = "example"

    # WHEN
    assigned_heir_x = assigned_heir_shop(
        _suffgroups=_suffgroups_x, _owner_id_assigned=_owner_id_assigned_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffgroups == _suffgroups_x
    assert assigned_heir_x._owner_id_assigned == _owner_id_assigned_x


def test_AssignedHeir_get_all_suff_partys_ReturnsSingleDictWithAllPartys_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)

    _suffgroups_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)

    # WHEN
    all_partys = assigned_heir_x._get_all_suff_partys(agenda_groups=x_agenda._groups)

    # THEN
    assert len(all_partys) == 1


def test_AssignedHeir_get_all_suff_partys_ReturnsSingleDictWithAllPartys_v2():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)

    swim_text = ",swim"
    swim_group = groupunit_shop(group_id=swim_text)
    swim_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim_group)

    _suffgroups_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)

    # WHEN
    all_partys = assigned_heir_x._get_all_suff_partys(agenda_groups=x_agenda._groups)

    # THEN
    assert len(all_partys) == 2


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_Empty_suffgroups_x():
    # GIVEN
    _suffgroups_x = {}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._owner_id_assigned is False

    # WHEN
    agenda_groups = {}
    assigned_heir_x.set_owner_id_assigned(
        agenda_groups=agenda_groups, agenda_owner_id=""
    )

    # THEN
    assert assigned_heir_x._owner_id_assigned


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_NonEmpty_suffgroups_x_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    agenda_owner_id = x_agenda._owner_id
    agenda_groups = x_agenda._groups
    print(f"{len(agenda_groups)=}")
    # print(f"{agenda_groups.get(jim_text)=}")
    # print(f"{agenda_groups.get(sue_text)=}")

    _suffgroups_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._owner_id_assigned is False

    # WHEN
    assigned_heir_x.set_owner_id_assigned(agenda_groups, agenda_owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_NonEmpty_suffgroups_x_v2():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    agenda_owner_id = x_agenda._owner_id
    agenda_groups = x_agenda._groups
    print(f"{len(agenda_groups)=}")
    # print(f"{agenda_groups.get(jim_text)=}")
    # print(f"{agenda_groups.get(sue_text)=}")

    _suffgroups_x = {sue_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._owner_id_assigned is False

    # WHEN
    assigned_heir_x.set_owner_id_assigned(agenda_groups, agenda_owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned is False


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_NonEmpty_suffgroups_x_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)

    swim_text = ",swim"
    swim_group = groupunit_shop(group_id=swim_text)
    swim_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim_group)

    _suffgroups_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._owner_id_assigned is False
    assigned_heir_x.set_owner_id_assigned(x_agenda._groups, x_agenda._owner_id)
    assert assigned_heir_x._owner_id_assigned

    # WHEN
    swim_group.del_partylink(party_id=jim_text)
    x_agenda.set_groupunit(y_groupunit=swim_group)
    assigned_heir_x.set_owner_id_assigned(x_agenda._groups, x_agenda._owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned is False


def test_AssignedHeir_set__CorrectlySetsAttribute_NonEmpty_suffgroups_x_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)

    swim_text = ",swim"
    swim_group = groupunit_shop(group_id=swim_text)
    swim_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim_group)

    _suffgroups_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._owner_id_assigned is False
    assigned_heir_x.set_owner_id_assigned(x_agenda._groups, x_agenda._owner_id)
    assert assigned_heir_x._owner_id_assigned

    # WHEN
    swim_group.del_partylink(party_id=jim_text)
    x_agenda.set_groupunit(y_groupunit=swim_group)
    assigned_heir_x.set_owner_id_assigned(x_agenda._groups, x_agenda._owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned is False


def test_AssignedHeir_set_suffgroup_AssignedUnitEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    assigned_heir_x = assigned_heir_shop(_suffgroups={})
    parent_assignheir_empty = assigned_heir_shop()
    assignedunit_x = assignedunit_shop()

    # WHEN
    assigned_heir_x.set_suffgroups(
        parent_assignheir=parent_assignheir_empty,
        assignunit=assignedunit_x,
        agenda_groups=None,
    )

    # THEN
    assigned_heir_x._suffgroups = {}


def test_AssignedHeir_set_suffgroup_AssignedUnitNotEmpty_ParentAssignedHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_x = assignedunit_shop()
    assignedunit_x.set_suffgroup(group_id=kent_text)
    assignedunit_x.set_suffgroup(group_id=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assignedunit_x, agenda_groups=None
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == assignedunit_x._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnitNotEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_x = assignedunit_shop()
    assignedunit_x.set_suffgroup(group_id=kent_text)
    assignedunit_x.set_suffgroup(group_id=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    parent_assignheir_empty = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir_empty, assignunit=assignedunit_x, agenda_groups=None
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == assignedunit_x._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnitEmpty_ParentAssignedHeirNotEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_swim = assignedunit_shop()
    assignedunit_swim.set_suffgroup(group_id=kent_text)
    assignedunit_swim.set_suffgroup(group_id=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        empty_assigned_heir, assignedunit_swim, agenda_groups=None
    )

    assignedunit_empty = assignedunit_shop()

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffgroups == {}
    assigned_heir_x.set_suffgroups(
        parent_assigned_heir, assignunit=assignedunit_empty, agenda_groups=None
    )

    # THEN
    assert len(assigned_heir_x._suffgroups.keys())
    assert assigned_heir_x._suffgroups.keys() == parent_assigned_heir._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnitEqualParentAssignedHeir_NonEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_swim = assignedunit_shop()
    assignedunit_swim.set_suffgroup(group_id=kent_text)
    assignedunit_swim.set_suffgroup(group_id=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        empty_assigned_heir, assignedunit_swim, agenda_groups=None
    )

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffgroups == {}
    assigned_heir_x.set_suffgroups(
        parent_assigned_heir, assignunit=assignedunit_swim, agenda_groups=None
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == parent_assigned_heir._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnit_NotEqual_ParentAssignedHeir_NonEmpty():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    tom_text = "Tom"
    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)
    x_agenda.add_partyunit(party_id=tom_text)

    swim2_text = ",swim2"
    swim2_group = groupunit_shop(group_id=swim2_text)
    swim2_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim2_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim2_group)

    swim3_text = ",swim3"
    swim3_group = groupunit_shop(group_id=swim3_text)
    swim3_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim3_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    swim3_group.set_partylink(partylink=partylink_shop(party_id=tom_text))
    x_agenda.set_groupunit(y_groupunit=swim3_group)

    parent_assignedunit = assignedunit_shop()
    parent_assignedunit.set_suffgroup(group_id=swim3_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        parent_assignheir=None, assignunit=parent_assignedunit, agenda_groups=None
    )

    assignedunit_swim2 = assignedunit_shop()
    assignedunit_swim2.set_suffgroup(group_id=swim2_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assigned_heir, assignedunit_swim2, agenda_groups=x_agenda._groups
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == assignedunit_swim2._suffgroups.keys()
    assert len(assigned_heir_x._suffgroups.keys()) == 1
    assert list(assigned_heir_x._suffgroups) == [swim2_text]


def test_AssignedHeir_set_suffgroup_AssignedUnit_NotEqualParentAssignedHeir_RaisesError():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    tom_text = "Tom"
    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)
    x_agenda.add_partyunit(party_id=tom_text)

    swim2_text = ",swim2"
    swim2_group = groupunit_shop(group_id=swim2_text)
    swim2_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim2_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim2_group)

    swim3_text = ",swim3"
    swim3_group = groupunit_shop(group_id=swim3_text)
    swim3_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim3_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    swim3_group.set_partylink(partylink=partylink_shop(party_id=tom_text))
    x_agenda.set_groupunit(y_groupunit=swim3_group)

    parent_assignedunit = assignedunit_shop()
    parent_assignedunit.set_suffgroup(group_id=swim2_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        parent_assignheir=None, assignunit=parent_assignedunit, agenda_groups=None
    )

    assignedunit_swim3 = assignedunit_shop()
    assignedunit_swim3.set_suffgroup(group_id=swim3_text)

    # WHEN / THEN
    assigned_heir_x = assigned_heir_shop()
    all_parent_assignedheir_partys = {jim_text, sue_text}
    all_assignedunit_partys = {jim_text, sue_text, tom_text}
    with pytest_raises(Exception) as excinfo:
        assigned_heir_x.set_suffgroups(
            parent_assigned_heir, assignedunit_swim3, agenda_groups=x_agenda._groups
        )
    assert (
        str(excinfo.value)
        == f"parent_assigned_heir does not contain all partys of the idea's assignedunit\n{set(all_parent_assignedheir_partys)=}\n\n{set(all_assignedunit_partys)=}"
    )


def test_AssignedUnit_get_suffgroup_ReturnsCorrectObj():
    # GIVEN
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffgroup(climb_text)
    x_assignedunit.set_suffgroup(walk_text)
    x_assignedunit.set_suffgroup(swim_text)

    # WHEN / THEN
    assert x_assignedunit.get_suffgroup(walk_text) != None
    assert x_assignedunit.get_suffgroup(swim_text) != None
    assert x_assignedunit.get_suffgroup(run_text) is None


def test_AssignedHeir_group_in_ReturnsCorrectBoolWhen_suffgroupsNotEmpty():
    # GIVEN
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text: -1}
    hike_dict = {hike_text: -1}
    assignedunit_x = assignedunit_shop()
    assignedunit_x.set_suffgroup(group_id=swim_text)
    assignedunit_x.set_suffgroup(group_id=hike_text)
    assignedheir_x = assigned_heir_shop()
    assignedheir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assignedunit_x, agenda_groups=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text: -1}
    play_text = ",play"
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
    assert assignedheir_x.group_in(hunt_dict) is False
    assert assignedheir_x.group_in(hunt_hike_dict)
    assert assignedheir_x.group_in(hunt_play_dict) is False


def test_AssignedHeir_group_in_ReturnsCorrectBoolWhen_suffgroupsEmpty():
    # GIVEN
    hike_text = ",hike"
    hike_dict = {hike_text: -1}
    assignedunit_x = assignedunit_shop()
    assignedheir_x = assigned_heir_shop()
    assignedheir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assignedunit_x, agenda_groups=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text: -1}
    play_text = ",play"
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
