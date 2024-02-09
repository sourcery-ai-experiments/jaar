from src.agenda.healer import HealerHold, healerhold_shop
from src.agenda.group import GroupID, groupunit_shop
from src.agenda.party import partylink_shop
from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_HealerHold_exists():
    # GIVEN
    run_text = ",runners"
    run_group_ids = {run_text}

    # WHEN
    x_healerhold = HealerHold(_group_ids=run_group_ids)

    # THEN
    assert x_healerhold
    assert x_healerhold._group_ids == run_group_ids


def test_healerhold_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    run_text = ",runners"
    run_group_ids = {run_text}

    # WHEN
    x_healerhold = healerhold_shop(_group_ids=run_group_ids)

    # THEN
    assert x_healerhold
    assert x_healerhold._group_ids == run_group_ids


def test_healerhold_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    x_healerhold = healerhold_shop()

    # THEN
    assert x_healerhold
    assert x_healerhold._group_ids == set()


def test_HealerHold_get_dict_ReturnsCorrectDictWithSingleGroup_id():
    # GIVEN
    bob_group_id = GroupID("Bob")
    run_group_ids = {bob_group_id}
    assigned_x = healerhold_shop(_group_ids=run_group_ids)

    # WHEN
    obj_dict = assigned_x.get_dict()

    # THEN
    assert obj_dict != None
    run_list = [bob_group_id]
    example_dict = {"_group_ids": run_list}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_HealerHold_set_group_id_CorrectlySets_group_ids_v1():
    # GIVEN
    x_healerhold = healerhold_shop()
    assert len(x_healerhold._group_ids) == 0

    # WHEN
    jim_text = "jim"
    x_healerhold.set_group_id(x_group_id=jim_text)

    # THEN
    assert len(x_healerhold._group_ids) == 1


def test_HealerHold_del_group_id_CorrectlyDeletes_group_ids_v1():
    # GIVEN
    x_healerhold = healerhold_shop()
    jim_text = "jim"
    sue_text = "sue"
    x_healerhold.set_group_id(x_group_id=jim_text)
    x_healerhold.set_group_id(x_group_id=sue_text)
    assert len(x_healerhold._group_ids) == 2

    # WHEN
    x_healerhold.del_group_id(x_group_id=sue_text)

    # THEN
    assert len(x_healerhold._group_ids) == 1


def test_HealerHold_group_id_exists_ReturnsCorrectObj():
    # GIVEN
    x_healerhold = healerhold_shop()
    jim_text = "jim"
    sue_text = "sue"
    assert x_healerhold.group_id_exists(jim_text) == False
    assert x_healerhold.group_id_exists(sue_text) == False

    # WHEN
    x_healerhold.set_group_id(x_group_id=jim_text)

    # THEN
    assert x_healerhold.group_id_exists(jim_text)
    assert x_healerhold.group_id_exists(sue_text) == False


def test_HealerHold_any_group_id_exists_ReturnsCorrectObj():
    # GIVEN
    x_healerhold = healerhold_shop()
    assert x_healerhold.any_group_id_exists() == False

    # WHEN / THEN
    sue_text = "sue"
    x_healerhold.set_group_id(x_group_id=sue_text)
    assert x_healerhold.any_group_id_exists()

    # WHEN / THEN
    jim_text = "Jim"
    x_healerhold.set_group_id(x_group_id=jim_text)
    assert x_healerhold.any_group_id_exists()

    # WHEN / THEN
    x_healerhold.del_group_id(x_group_id=jim_text)
    assert x_healerhold.any_group_id_exists()

    # WHEN / THEN
    x_healerhold.del_group_id(x_group_id=sue_text)
    assert x_healerhold.any_group_id_exists() == False


# def test_assigned_heir_shop_ReturnsCorrectWithCorrectAttributes_v1():
#     # GIVEN
#     _group_ids_x = {1: 2}
#     _agent_id_assigned_x = "example"

#     # WHEN
#     assigned_heir_x = assigned_heir_shop(
#         _group_ids=_group_ids_x, _agent_id_assigned=_agent_id_assigned_x
#     )

#     # THEN
#     assert assigned_heir_x
#     assert assigned_heir_x._group_ids == _group_ids_x
#     assert assigned_heir_x._agent_id_assigned == _agent_id_assigned_x


# def test_AssignedHeir_get_all_suff_partys_ReturnsSingleDictWithAllPartys_v1():
#     # GIVEN
#     jim_text = "jim"
#     sue_text = "sue"
#     x_agenda = agendaunit_shop(_agent_id=jim_text)
#     x_agenda.add_partyunit(party_id=jim_text)
#     x_agenda.add_partyunit(party_id=sue_text)

#     _group_ids_x = {jim_text: -1}
#     assigned_heir_x = assigned_heir_shop(_group_ids=_group_ids_x)

#     # WHEN
#     all_partys = assigned_heir_x._get_all_suff_partys(agenda_groups=x_agenda._groups)

#     # THEN
#     assert len(all_partys) == 1


# def test_AssignedHeir_get_all_suff_partys_ReturnsSingleDictWithAllPartys_v2():
#     # GIVEN
#     jim_text = "jim"
#     sue_text = "sue"
#     bob_text = "Bob"
#     x_agenda = agendaunit_shop(_agent_id=jim_text)
#     x_agenda.add_partyunit(party_id=jim_text)
#     x_agenda.add_partyunit(party_id=sue_text)
#     x_agenda.add_partyunit(party_id=bob_text)

#     swim_text = ",swim"
#     swim_group = groupunit_shop(group_id=swim_text)
#     swim_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
#     swim_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
#     x_agenda.set_groupunit(y_groupunit=swim_group)

#     _group_ids_x = {swim_text: -1}
#     assigned_heir_x = assigned_heir_shop(_group_ids=_group_ids_x)

#     # WHEN
#     all_partys = assigned_heir_x._get_all_suff_partys(agenda_groups=x_agenda._groups)

#     # THEN
#     assert len(all_partys) == 2


# def test_AssignedHeir_set_agent_id_assigned_CorrectlySetsAttribute_Empty_group_ids_x():
#     # GIVEN
#     _group_ids_x = {}
#     assigned_heir_x = assigned_heir_shop(_group_ids=_group_ids_x)
#     assert assigned_heir_x._agent_id_assigned == False

#     # WHEN
#     agenda_groups = {}
#     assigned_heir_x.set_agent_id_assigned(
#         agenda_groups=agenda_groups, agenda_agent_id=""
#     )

#     # THEN
#     assert assigned_heir_x._agent_id_assigned


# def test_AssignedHeir_set_agent_id_assigned_CorrectlySetsAttribute_NonEmpty_group_ids_x_v1():
#     # GIVEN
#     jim_text = "jim"
#     sue_text = "sue"

#     x_agenda = agendaunit_shop(_agent_id=jim_text)
#     x_agenda.add_partyunit(party_id=jim_text)
#     x_agenda.add_partyunit(party_id=sue_text)
#     agenda_agent_id = x_agenda._agent_id
#     agenda_groups = x_agenda._groups
#     print(f"{len(agenda_groups)=}")
#     # print(f"{agenda_groups.get(jim_text)=}")
#     # print(f"{agenda_groups.get(sue_text)=}")

#     _group_ids_x = {jim_text: -1}
#     assigned_heir_x = assigned_heir_shop(_group_ids=_group_ids_x)
#     assert assigned_heir_x._agent_id_assigned == False

#     # WHEN
#     assigned_heir_x.set_agent_id_assigned(agenda_groups, agenda_agent_id)

#     # THEN
#     assert assigned_heir_x._agent_id_assigned


# def test_AssignedHeir_set_agent_id_assigned_CorrectlySetsAttribute_NonEmpty_group_ids_x_v2():
#     # GIVEN
#     jim_text = "jim"
#     sue_text = "sue"

#     x_agenda = agendaunit_shop(_agent_id=jim_text)
#     x_agenda.add_partyunit(party_id=jim_text)
#     x_agenda.add_partyunit(party_id=sue_text)
#     agenda_agent_id = x_agenda._agent_id
#     agenda_groups = x_agenda._groups
#     print(f"{len(agenda_groups)=}")
#     # print(f"{agenda_groups.get(jim_text)=}")
#     # print(f"{agenda_groups.get(sue_text)=}")

#     _group_ids_x = {sue_text: -1}
#     assigned_heir_x = assigned_heir_shop(_group_ids=_group_ids_x)
#     assert assigned_heir_x._agent_id_assigned == False

#     # WHEN
#     assigned_heir_x.set_agent_id_assigned(agenda_groups, agenda_agent_id)

#     # THEN
#     assert assigned_heir_x._agent_id_assigned == False


# def test_AssignedHeir_set_agent_id_assigned_CorrectlySetsAttribute_NonEmpty_group_ids_x_v3():
#     # GIVEN
#     jim_text = "jim"
#     sue_text = "sue"
#     bob_text = "Bob"
#     x_agenda = agendaunit_shop(_agent_id=jim_text)
#     x_agenda.add_partyunit(party_id=jim_text)
#     x_agenda.add_partyunit(party_id=sue_text)
#     x_agenda.add_partyunit(party_id=bob_text)

#     swim_text = ",swim"
#     swim_group = groupunit_shop(group_id=swim_text)
#     swim_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
#     swim_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
#     x_agenda.set_groupunit(y_groupunit=swim_group)

#     _group_ids_x = {swim_text: -1}
#     assigned_heir_x = assigned_heir_shop(_group_ids=_group_ids_x)
#     assert assigned_heir_x._agent_id_assigned == False
#     assigned_heir_x.set_agent_id_assigned(x_agenda._groups, x_agenda._agent_id)
#     assert assigned_heir_x._agent_id_assigned

#     # WHEN
#     swim_group.del_partylink(party_id=jim_text)
#     x_agenda.set_groupunit(y_groupunit=swim_group)
#     assigned_heir_x.set_agent_id_assigned(x_agenda._groups, x_agenda._agent_id)

#     # THEN
#     assert assigned_heir_x._agent_id_assigned == False


# def test_AssignedHeir_set__CorrectlySetsAttribute_NonEmpty_group_ids_x_v3():
#     # GIVEN
#     jim_text = "jim"
#     sue_text = "sue"
#     bob_text = "Bob"
#     x_agenda = agendaunit_shop(_agent_id=jim_text)
#     x_agenda.add_partyunit(party_id=jim_text)
#     x_agenda.add_partyunit(party_id=sue_text)
#     x_agenda.add_partyunit(party_id=bob_text)

#     swim_text = ",swim"
#     swim_group = groupunit_shop(group_id=swim_text)
#     swim_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
#     swim_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
#     x_agenda.set_groupunit(y_groupunit=swim_group)

#     _group_ids_x = {swim_text: -1}
#     assigned_heir_x = assigned_heir_shop(_group_ids=_group_ids_x)
#     assert assigned_heir_x._agent_id_assigned == False
#     assigned_heir_x.set_agent_id_assigned(x_agenda._groups, x_agenda._agent_id)
#     assert assigned_heir_x._agent_id_assigned

#     # WHEN
#     swim_group.del_partylink(party_id=jim_text)
#     x_agenda.set_groupunit(y_groupunit=swim_group)
#     assigned_heir_x.set_agent_id_assigned(x_agenda._groups, x_agenda._agent_id)

#     # THEN
#     assert assigned_heir_x._agent_id_assigned == False


# def test_AssignedHeir_set_group_id_HealerHoldEmpty_ParentAssignedHeirEmpty():
#     # GIVEN
#     assigned_heir_x = assigned_heir_shop(_group_ids={})
#     parent_assignheir_empty = assigned_heir_shop()
#     x_healerhold = healerhold_shop()

#     # WHEN
#     assigned_heir_x.set_group_ids(
#         parent_assignheir=parent_assignheir_empty,
#         assignunit=x_healerhold,
#         agenda_groups=None,
#     )

#     # THEN
#     assigned_heir_x._group_ids = {}


# def test_AssignedHeir_set_group_id_HealerHoldNotEmpty_ParentAssignedHeirIsNone():
#     # GIVEN
#     kent_text = "kent"
#     swim_text = ",swim"
#     x_healerhold = healerhold_shop()
#     x_healerhold.set_group_id(x_group_id=kent_text)
#     x_healerhold.set_group_id(x_group_id=swim_text)

#     # WHEN
#     assigned_heir_x = assigned_heir_shop()
#     assigned_heir_x.set_group_ids(
#         parent_assignheir=None, assignunit=x_healerhold, agenda_groups=None
#     )

#     # THEN
#     assert assigned_heir_x._group_ids.keys() == x_healerhold._group_ids.keys()


# def test_AssignedHeir_set_group_id_HealerHoldNotEmpty_ParentAssignedHeirEmpty():
#     # GIVEN
#     kent_text = "kent"
#     swim_text = ",swim"
#     x_healerhold = healerhold_shop()
#     x_healerhold.set_group_id(x_group_id=kent_text)
#     x_healerhold.set_group_id(x_group_id=swim_text)

#     # WHEN
#     assigned_heir_x = assigned_heir_shop()
#     parent_assignheir_empty = assigned_heir_shop()
#     assigned_heir_x.set_group_ids(
#         parent_assignheir_empty, assignunit=x_healerhold, agenda_groups=None
#     )

#     # THEN
#     assert assigned_heir_x._group_ids.keys() == x_healerhold._group_ids.keys()


# def test_AssignedHeir_set_group_id_HealerHoldEmpty_ParentAssignedHeirNotEmpty():
#     # GIVEN
#     kent_text = "kent"
#     swim_text = ",swim"
#     healerhold_swim = healerhold_shop()
#     healerhold_swim.set_group_id(x_group_id=kent_text)
#     healerhold_swim.set_group_id(x_group_id=swim_text)
#     empty_assigned_heir = assigned_heir_shop()

#     parent_assigned_heir = assigned_heir_shop()
#     parent_assigned_heir.set_group_ids(
#         empty_assigned_heir, healerhold_swim, agenda_groups=None
#     )

#     healerhold_empty = healerhold_shop()

#     # WHEN
#     assigned_heir_x = assigned_heir_shop()
#     assert assigned_heir_x._group_ids == {}
#     assigned_heir_x.set_group_ids(
#         parent_assigned_heir, assignunit=healerhold_empty, agenda_groups=None
#     )

#     # THEN
#     assert len(assigned_heir_x._group_ids.keys())
#     assert assigned_heir_x._group_ids.keys() == parent_assigned_heir._group_ids.keys()


# def test_AssignedHeir_set_group_id_HealerHoldEqualParentAssignedHeir_NonEmpty():
#     # GIVEN
#     kent_text = "kent"
#     swim_text = ",swim"
#     healerhold_swim = healerhold_shop()
#     healerhold_swim.set_group_id(x_group_id=kent_text)
#     healerhold_swim.set_group_id(x_group_id=swim_text)
#     empty_assigned_heir = assigned_heir_shop()

#     parent_assigned_heir = assigned_heir_shop()
#     parent_assigned_heir.set_group_ids(
#         empty_assigned_heir, healerhold_swim, agenda_groups=None
#     )

#     # WHEN
#     assigned_heir_x = assigned_heir_shop()
#     assert assigned_heir_x._group_ids == {}
#     assigned_heir_x.set_group_ids(
#         parent_assigned_heir, assignunit=healerhold_swim, agenda_groups=None
#     )

#     # THEN
#     assert assigned_heir_x._group_ids.keys() == parent_assigned_heir._group_ids.keys()


# def test_AssignedHeir_set_group_id_HealerHold_NotEqual_ParentAssignedHeir_NonEmpty():
#     # GIVEN
#     jim_text = "jim"
#     sue_text = "sue"
#     bob_text = "Bob"
#     tom_text = "tom"
#     x_agenda = agendaunit_shop(_agent_id=jim_text)
#     x_agenda.add_partyunit(party_id=jim_text)
#     x_agenda.add_partyunit(party_id=sue_text)
#     x_agenda.add_partyunit(party_id=bob_text)
#     x_agenda.add_partyunit(party_id=tom_text)

#     swim2_text = ",swim2"
#     swim2_group = groupunit_shop(group_id=swim2_text)
#     swim2_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
#     swim2_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
#     x_agenda.set_groupunit(y_groupunit=swim2_group)

#     swim3_text = ",swim3"
#     swim3_group = groupunit_shop(group_id=swim3_text)
#     swim3_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
#     swim3_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
#     swim3_group.set_partylink(partylink=partylink_shop(party_id=tom_text))
#     x_agenda.set_groupunit(y_groupunit=swim3_group)

#     parent_healerhold = healerhold_shop()
#     parent_healerhold.set_group_id(x_group_id=swim3_text)
#     parent_assigned_heir = assigned_heir_shop()
#     parent_assigned_heir.set_group_ids(
#         parent_assignheir=None, assignunit=parent_healerhold, agenda_groups=None
#     )

#     healerhold_swim2 = healerhold_shop()
#     healerhold_swim2.set_group_id(x_group_id=swim2_text)

#     # WHEN
#     assigned_heir_x = assigned_heir_shop()
#     assigned_heir_x.set_group_ids(
#         parent_assigned_heir, healerhold_swim2, agenda_groups=x_agenda._groups
#     )

#     # THEN
#     assert assigned_heir_x._group_ids.keys() == healerhold_swim2._group_ids.keys()
#     assert len(assigned_heir_x._group_ids.keys()) == 1
#     assert list(assigned_heir_x._group_ids) == [swim2_text]


# def test_AssignedHeir_set_group_id_HealerHold_NotEqualParentAssignedHeir_RaisesError():
#     # GIVEN
#     jim_text = "jim"
#     sue_text = "sue"
#     bob_text = "Bob"
#     tom_text = "tom"
#     x_agenda = agendaunit_shop(_agent_id=jim_text)
#     x_agenda.add_partyunit(party_id=jim_text)
#     x_agenda.add_partyunit(party_id=sue_text)
#     x_agenda.add_partyunit(party_id=bob_text)
#     x_agenda.add_partyunit(party_id=tom_text)

#     swim2_text = ",swim2"
#     swim2_group = groupunit_shop(group_id=swim2_text)
#     swim2_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
#     swim2_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
#     x_agenda.set_groupunit(y_groupunit=swim2_group)

#     swim3_text = ",swim3"
#     swim3_group = groupunit_shop(group_id=swim3_text)
#     swim3_group.set_partylink(partylink=partylink_shop(party_id=jim_text))
#     swim3_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
#     swim3_group.set_partylink(partylink=partylink_shop(party_id=tom_text))
#     x_agenda.set_groupunit(y_groupunit=swim3_group)

#     parent_healerhold = healerhold_shop()
#     parent_healerhold.set_group_id(x_group_id=swim2_text)
#     parent_assigned_heir = assigned_heir_shop()
#     parent_assigned_heir.set_group_ids(
#         parent_assignheir=None, assignunit=parent_healerhold, agenda_groups=None
#     )

#     healerhold_swim3 = healerhold_shop()
#     healerhold_swim3.set_group_id(x_group_id=swim3_text)

#     # WHEN / THEN
#     assigned_heir_x = assigned_heir_shop()
#     all_parent_assignedheir_partys = {jim_text, sue_text}
#     all_healerhold_partys = {jim_text, sue_text, tom_text}
#     with pytest_raises(Exception) as excinfo:
#         assigned_heir_x.set_group_ids(
#             parent_assigned_heir, healerhold_swim3, agenda_groups=x_agenda._groups
#         )
#     assert (
#         str(excinfo.value)
#         == f"parent_assigned_heir does not contain all partys of the idea's healerhold\n{set(all_parent_assignedheir_partys)=}\n\n{set(all_healerhold_partys)=}"
#     )


# def test_HealerHold_get_group_id_ReturnsCorrectObj():
#     # GIVEN
#     climb_text = ",climbers"
#     walk_text = ",walkers"
#     swim_text = ",swimmers"
#     run_text = ",runners"

#     x_healerhold = healerhold_shop()
#     x_healerhold.set_group_id(climb_text)
#     x_healerhold.set_group_id(walk_text)
#     x_healerhold.set_group_id(swim_text)

#     # WHEN / THEN
#     assert x_healerhold.get_group_id(walk_text) != None
#     assert x_healerhold.get_group_id(swim_text) != None
#     assert x_healerhold.get_group_id(run_text) is None


# def test_AssignedHeir_group_in_ReturnsCorrectBoolWhen_group_idsNotEmpty():
#     # GIVEN
#     swim_text = ",swim"
#     hike_text = ",hike"
#     swim_dict = {swim_text: -1}
#     hike_dict = {hike_text: -1}
#     x_healerhold = healerhold_shop()
#     x_healerhold.set_group_id(x_group_id=swim_text)
#     x_healerhold.set_group_id(x_group_id=hike_text)
#     assignedheir_x = assigned_heir_shop()
#     assignedheir_x.set_group_ids(
#         parent_assignheir=None, assignunit=x_healerhold, agenda_groups=None
#     )
#     hunt_text = ",hunt"
#     hunt_dict = {hunt_text: -1}
#     play_text = ",play"
#     play_dict = {play_text: -1}
#     assert assignedheir_x._group_ids.get(swim_text) != None
#     assert assignedheir_x._group_ids.get(hike_text) != None
#     assert assignedheir_x._group_ids.get(hunt_text) is None
#     assert assignedheir_x._group_ids.get(play_text) is None
#     hunt_hike_dict = {hunt_text: -1, hike_text: -1}
#     hunt_play_dict = {hunt_text: -1, play_text: -1}

#     # WHEN / THEN
#     assert assignedheir_x.group_in(swim_dict)
#     assert assignedheir_x.group_in(hike_dict)
#     assert assignedheir_x.group_in(hunt_dict) == False
#     assert assignedheir_x.group_in(hunt_hike_dict)
#     assert assignedheir_x.group_in(hunt_play_dict) == False


# def test_AssignedHeir_group_in_ReturnsCorrectBoolWhen_group_idsEmpty():
#     # GIVEN
#     hike_text = ",hike"
#     hike_dict = {hike_text: -1}
#     x_healerhold = healerhold_shop()
#     assignedheir_x = assigned_heir_shop()
#     assignedheir_x.set_group_ids(
#         parent_assignheir=None, assignunit=x_healerhold, agenda_groups=None
#     )
#     hunt_text = ",hunt"
#     hunt_dict = {hunt_text: -1}
#     play_text = ",play"
#     play_dict = {play_text: -1}
#     assert assignedheir_x._group_ids == {}
#     hunt_hike_dict = {hunt_text: -1, hike_text: -1}
#     hunt_play_dict = {hunt_text: -1, play_text: -1}

#     # WHEN / THEN
#     assert assignedheir_x.group_in(hike_dict)
#     assert assignedheir_x.group_in(hunt_dict)
#     assert assignedheir_x.group_in(play_dict)
#     assert assignedheir_x.group_in(hunt_hike_dict)
#     assert assignedheir_x.group_in(hunt_play_dict)
