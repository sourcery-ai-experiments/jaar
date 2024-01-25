from src.agenda.reason_assign import (
    AssignedUnit,
    assigned_unit_shop,
    AssignedHeir,
    assigned_heir_shop,
    create_assignedunit,
)
from src.agenda.group import GroupBrand, groupunit_shop
from src.agenda.party import partylink_shop
from src.agenda.agenda import agendaunit_shop
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


def test_create_assignedunit_ReturnsCorrectObj():
    # GIVEN
    swim_groupbrand = GroupBrand("swimmers")

    # WHEN
    swim_assignedunit = create_assignedunit(swim_groupbrand)

    # THEN
    assert swim_assignedunit
    assert len(swim_assignedunit._suffgroups) == 1


def test_AssignedUnit_get_dict_ReturnsCorrectDictWithSingleSuffGroup():
    # GIVEN
    bob_groupbrand = GroupBrand("Bob")
    _suffgroups_x = {bob_groupbrand: bob_groupbrand}
    assigned_x = assigned_unit_shop(_suffgroups=_suffgroups_x)

    # WHEN
    obj_dict = assigned_x.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_suffgroups": {bob_groupbrand: bob_groupbrand}}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_AssignedUnit_set_suffgroup_CorrectlySets_suffgroups_v1():
    # GIVEN
    assigned_unit_x = assigned_unit_shop(_suffgroups={})
    assert len(assigned_unit_x._suffgroups) == 0

    # WHEN
    jim_text = "jim"
    assigned_unit_x.set_suffgroup(brand=jim_text)

    # THEN
    assert len(assigned_unit_x._suffgroups) == 1


def test_AssignedUnit_del_suffgroup_CorrectlyDeletes_suffgroups_v1():
    # GIVEN
    assigned_unit_x = assigned_unit_shop(_suffgroups={})
    jim_text = "jim"
    sue_text = "sue"
    assigned_unit_x.set_suffgroup(brand=jim_text)
    assigned_unit_x.set_suffgroup(brand=sue_text)
    assert len(assigned_unit_x._suffgroups) == 2

    # WHEN
    assigned_unit_x.del_suffgroup(brand=sue_text)

    # THEN
    assert len(assigned_unit_x._suffgroups) == 1


def test_AssignedHeir_exists():
    # GIVEN
    _suffgroups_x = {1: 2}
    _agent_id_assigned_x = True

    # WHEN
    assigned_heir_x = AssignedHeir(
        _suffgroups=_suffgroups_x, _agent_id_assigned=_agent_id_assigned_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffgroups == _suffgroups_x
    assert assigned_heir_x._agent_id_assigned == _agent_id_assigned_x


def test_assigned_heir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffgroups_x = {1: 2}
    _agent_id_assigned_x = "example"

    # WHEN
    assigned_heir_x = assigned_heir_shop(
        _suffgroups=_suffgroups_x, _agent_id_assigned=_agent_id_assigned_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffgroups == _suffgroups_x
    assert assigned_heir_x._agent_id_assigned == _agent_id_assigned_x


def test_AssignedHeir_get_all_suff_partys_CorrectlyReturnsSingleDictWithAllPartys_v1():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    x_agenda = agendaunit_shop(_agent_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)

    _suffgroups_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)

    # WHEN
    all_partys = assigned_heir_x._get_all_suff_partys(agenda_groups=x_agenda._groups)

    # THEN
    assert len(all_partys) == 1


def test_AssignedHeir_get_all_suff_partys_CorrectlyReturnsSingleDictWithAllPartys_v2():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "Bob"
    x_agenda = agendaunit_shop(_agent_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)

    swim_text = ",swim"
    swim_group = groupunit_shop(brand=swim_text)
    swim_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim_group)

    _suffgroups_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)

    # WHEN
    all_partys = assigned_heir_x._get_all_suff_partys(agenda_groups=x_agenda._groups)

    # THEN
    assert len(all_partys) == 2


def test_AssignedHeir_set_agent_id_assigned_CorrectlySetsAttribute_Empty_suffgroups_x():
    # GIVEN
    _suffgroups_x = {}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._agent_id_assigned == False

    # WHEN
    agenda_groups = {}
    assigned_heir_x.set_agent_id_assigned(
        agenda_groups=agenda_groups, agenda_agent_id=""
    )

    # THEN
    assert assigned_heir_x._agent_id_assigned


def test_AssignedHeir_set_agent_id_assigned_CorrectlySetsAttribute_NonEmpty_suffgroups_x_v1():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"

    x_agenda = agendaunit_shop(_agent_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    agenda_agent_id = x_agenda._agent_id
    agenda_groups = x_agenda._groups
    print(f"{len(agenda_groups)=}")
    # print(f"{agenda_groups.get(jim_text)=}")
    # print(f"{agenda_groups.get(sue_text)=}")

    _suffgroups_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._agent_id_assigned == False

    # WHEN
    assigned_heir_x.set_agent_id_assigned(agenda_groups, agenda_agent_id)

    # THEN
    assert assigned_heir_x._agent_id_assigned


def test_AssignedHeir_set_agent_id_assigned_CorrectlySetsAttribute_NonEmpty_suffgroups_x_v2():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"

    x_agenda = agendaunit_shop(_agent_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    agenda_agent_id = x_agenda._agent_id
    agenda_groups = x_agenda._groups
    print(f"{len(agenda_groups)=}")
    # print(f"{agenda_groups.get(jim_text)=}")
    # print(f"{agenda_groups.get(sue_text)=}")

    _suffgroups_x = {sue_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._agent_id_assigned == False

    # WHEN
    assigned_heir_x.set_agent_id_assigned(agenda_groups, agenda_agent_id)

    # THEN
    assert assigned_heir_x._agent_id_assigned == False


def test_AssignedHeir_set_agent_id_assigned_CorrectlySetsAttribute_NonEmpty_suffgroups_x_v3():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "Bob"
    x_agenda = agendaunit_shop(_agent_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)

    swim_text = ",swim"
    swim_group = groupunit_shop(brand=swim_text)
    swim_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim_group)

    _suffgroups_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._agent_id_assigned == False
    assigned_heir_x.set_agent_id_assigned(x_agenda._groups, x_agenda._agent_id)
    assert assigned_heir_x._agent_id_assigned

    # WHEN
    swim_group.del_partylink(party_id=jim_text)
    x_agenda.set_groupunit(y_groupunit=swim_group)
    assigned_heir_x.set_agent_id_assigned(x_agenda._groups, x_agenda._agent_id)

    # THEN
    assert assigned_heir_x._agent_id_assigned == False


def test_AssignedHeir_set__CorrectlySetsAttribute_NonEmpty_suffgroups_x_v3():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "Bob"
    x_agenda = agendaunit_shop(_agent_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)

    swim_text = ",swim"
    swim_group = groupunit_shop(brand=swim_text)
    swim_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim_group)

    _suffgroups_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffgroups=_suffgroups_x)
    assert assigned_heir_x._agent_id_assigned == False
    assigned_heir_x.set_agent_id_assigned(x_agenda._groups, x_agenda._agent_id)
    assert assigned_heir_x._agent_id_assigned

    # WHEN
    swim_group.del_partylink(party_id=jim_text)
    x_agenda.set_groupunit(y_groupunit=swim_group)
    assigned_heir_x.set_agent_id_assigned(x_agenda._groups, x_agenda._agent_id)

    # THEN
    assert assigned_heir_x._agent_id_assigned == False


def test_AssignedHeir_set_suffgroup_AssignedUnitEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    assigned_heir_x = assigned_heir_shop(_suffgroups={})
    parent_assignheir_empty = assigned_heir_shop()
    assigned_unit_x = assigned_unit_shop()

    # WHEN
    assigned_heir_x.set_suffgroups(
        parent_assignheir=parent_assignheir_empty,
        assignunit=assigned_unit_x,
        agenda_groups=None,
    )

    # THEN
    assigned_heir_x._suffgroups = {}


def test_AssignedHeir_set_suffgroup_AssignedUnitNotEmpty_ParentAssignedHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(brand=kent_text)
    assigned_unit_x.set_suffgroup(brand=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir=None, assignunit=assigned_unit_x, agenda_groups=None
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == assigned_unit_x._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnitNotEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(brand=kent_text)
    assigned_unit_x.set_suffgroup(brand=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    parent_assignheir_empty = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assignheir_empty, assignunit=assigned_unit_x, agenda_groups=None
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == assigned_unit_x._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnitEmpty_ParentAssignedHeirNotEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assigned_unit_swim = assigned_unit_shop()
    assigned_unit_swim.set_suffgroup(brand=kent_text)
    assigned_unit_swim.set_suffgroup(brand=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        empty_assigned_heir, assigned_unit_swim, agenda_groups=None
    )

    assigned_unit_empty = assigned_unit_shop()

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffgroups == {}
    assigned_heir_x.set_suffgroups(
        parent_assigned_heir, assignunit=assigned_unit_empty, agenda_groups=None
    )

    # THEN
    assert len(assigned_heir_x._suffgroups.keys())
    assert assigned_heir_x._suffgroups.keys() == parent_assigned_heir._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnitEqualParentAssignedHeir_NonEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assigned_unit_swim = assigned_unit_shop()
    assigned_unit_swim.set_suffgroup(brand=kent_text)
    assigned_unit_swim.set_suffgroup(brand=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        empty_assigned_heir, assigned_unit_swim, agenda_groups=None
    )

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffgroups == {}
    assigned_heir_x.set_suffgroups(
        parent_assigned_heir, assignunit=assigned_unit_swim, agenda_groups=None
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == parent_assigned_heir._suffgroups.keys()


def test_AssignedHeir_set_suffgroup_AssignedUnit_NotEqual_ParentAssignedHeir_NonEmpty():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "Bob"
    tom_text = "tom"
    x_agenda = agendaunit_shop(_agent_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)
    x_agenda.add_partyunit(party_id=tom_text)

    swim2_text = ",swim2"
    swim2_group = groupunit_shop(brand=swim2_text)
    swim2_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim2_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim2_group)

    swim3_text = ",swim3"
    swim3_group = groupunit_shop(brand=swim3_text)
    swim3_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim3_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    swim3_group.set_partylink(partylink=partylink_shop(party_id=tom_text))
    x_agenda.set_groupunit(y_groupunit=swim3_group)

    parent_assigned_unit = assigned_unit_shop()
    parent_assigned_unit.set_suffgroup(brand=swim3_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        parent_assignheir=None, assignunit=parent_assigned_unit, agenda_groups=None
    )

    assigned_unit_swim2 = assigned_unit_shop()
    assigned_unit_swim2.set_suffgroup(brand=swim2_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        parent_assigned_heir, assigned_unit_swim2, agenda_groups=x_agenda._groups
    )

    # THEN
    assert assigned_heir_x._suffgroups.keys() == assigned_unit_swim2._suffgroups.keys()
    assert len(assigned_heir_x._suffgroups.keys()) == 1
    assert list(assigned_heir_x._suffgroups) == [swim2_text]


def test_AssignedHeir_set_suffgroup_AssignedUnit_NotEqualParentAssignedHeir_RaisesError():
    # GIVEN
    jim_text = "jim"
    sue_text = "sue"
    bob_text = "Bob"
    tom_text = "tom"
    x_agenda = agendaunit_shop(_agent_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)
    x_agenda.add_partyunit(party_id=tom_text)

    swim2_text = ",swim2"
    swim2_group = groupunit_shop(brand=swim2_text)
    swim2_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim2_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_groupunit(y_groupunit=swim2_group)

    swim3_text = ",swim3"
    swim3_group = groupunit_shop(brand=swim3_text)
    swim3_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim3_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    swim3_group.set_partylink(partylink=partylink_shop(party_id=tom_text))
    x_agenda.set_groupunit(y_groupunit=swim3_group)

    parent_assigned_unit = assigned_unit_shop()
    parent_assigned_unit.set_suffgroup(brand=swim2_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffgroups(
        parent_assignheir=None, assignunit=parent_assigned_unit, agenda_groups=None
    )

    assigned_unit_swim3 = assigned_unit_shop()
    assigned_unit_swim3.set_suffgroup(brand=swim3_text)

    # WHEN / THEN
    assigned_heir_x = assigned_heir_shop()
    all_parent_assignedheir_partys = {jim_text, sue_text}
    all_assignedunit_partys = {jim_text, sue_text, tom_text}
    with pytest_raises(Exception) as excinfo:
        assigned_heir_x.set_suffgroups(
            parent_assigned_heir, assigned_unit_swim3, agenda_groups=x_agenda._groups
        )
    assert (
        str(excinfo.value)
        == f"parent_assigned_heir does not contain all partys of the idea's assigned_unit\n{set(all_parent_assignedheir_partys)=}\n\n{set(all_assignedunit_partys)=}"
    )


def test_AssignedUnit_get_suffgroup_ReturnsCorrectObj():
    # GIVEN
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_assigned_unit = assigned_unit_shop()
    x_assigned_unit.set_suffgroup(climb_text)
    x_assigned_unit.set_suffgroup(walk_text)
    x_assigned_unit.set_suffgroup(swim_text)

    # WHEN / THEN
    assert x_assigned_unit.get_suffgroup(walk_text) != None
    assert x_assigned_unit.get_suffgroup(swim_text) != None
    assert x_assigned_unit.get_suffgroup(run_text) is None


def test_AssignedHeir_group_in_ReturnsCorrectBoolWhen_suffgroupsNotEmpty():
    # GIVEN
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text: -1}
    hike_dict = {hike_text: -1}
    assignedunit_x = assigned_unit_shop()
    assignedunit_x.set_suffgroup(brand=swim_text)
    assignedunit_x.set_suffgroup(brand=hike_text)
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
    assert assignedheir_x.group_in(hunt_dict) == False
    assert assignedheir_x.group_in(hunt_hike_dict)
    assert assignedheir_x.group_in(hunt_play_dict) == False


def test_AssignedHeir_group_in_ReturnsCorrectBoolWhen_suffgroupsEmpty():
    # GIVEN
    hike_text = ",hike"
    hike_dict = {hike_text: -1}
    assignedunit_x = assigned_unit_shop()
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
