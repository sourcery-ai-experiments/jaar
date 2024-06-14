from src.agenda.reason_assign import (
    AssignedUnit,
    assignedunit_shop,
    AssignedHeir,
    assigned_heir_shop,
    create_assignedunit,
)
from src.agenda.idea import IdeaID, ideaunit_shop
from src.agenda.party import partylink_shop
from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_AssignedUnit_exists():
    # GIVEN
    _suffideas_x = {1: 2}

    # WHEN
    assignedunit_x = AssignedUnit(_suffideas=_suffideas_x)

    # THEN
    assert assignedunit_x
    assert assignedunit_x._suffideas == _suffideas_x


def test_assignedunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffideas_x = {1: 2}

    # WHEN
    assignedunit_x = assignedunit_shop(_suffideas=_suffideas_x)

    # THEN
    assert assignedunit_x
    assert assignedunit_x._suffideas == _suffideas_x


def test_assignedunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    assignedunit_x = assignedunit_shop()

    # THEN
    assert assignedunit_x
    assert assignedunit_x._suffideas == {}


def test_create_assignedunit_ReturnsCorrectObj():
    # GIVEN
    swim_idea_id = IdeaID("swimmers")

    # WHEN
    swim_assignedunit = create_assignedunit(swim_idea_id)

    # THEN
    assert swim_assignedunit
    assert len(swim_assignedunit._suffideas) == 1


def test_AssignedUnit_get_dict_ReturnsCorrectDictWithSingleSuffIdea():
    # GIVEN
    bob_idea_id = IdeaID("Bob")
    _suffideas_x = {bob_idea_id: bob_idea_id}
    assigned_x = assignedunit_shop(_suffideas=_suffideas_x)

    # WHEN
    obj_dict = assigned_x.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_suffideas": {bob_idea_id: bob_idea_id}}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_AssignedUnit_set_suffidea_CorrectlySets_suffideas_v1():
    # GIVEN
    assignedunit_x = assignedunit_shop(_suffideas={})
    assert len(assignedunit_x._suffideas) == 0

    # WHEN
    jim_text = "Jim"
    assignedunit_x.set_suffidea(idea_id=jim_text)

    # THEN
    assert len(assignedunit_x._suffideas) == 1


def test_AssignedUnit_suffidea_exists_ReturnsCorrectObj():
    # GIVEN
    assignedunit_x = assignedunit_shop(_suffideas={})
    jim_text = "Jim"
    assert assignedunit_x.suffidea_exists(jim_text) is False

    # WHEN
    assignedunit_x.set_suffidea(idea_id=jim_text)

    # THEN
    assert assignedunit_x.suffidea_exists(jim_text)


def test_AssignedUnit_del_suffidea_CorrectlyDeletes_suffideas_v1():
    # GIVEN
    assignedunit_x = assignedunit_shop(_suffideas={})
    jim_text = "Jim"
    sue_text = "Sue"
    assignedunit_x.set_suffidea(idea_id=jim_text)
    assignedunit_x.set_suffidea(idea_id=sue_text)
    assert len(assignedunit_x._suffideas) == 2

    # WHEN
    assignedunit_x.del_suffidea(idea_id=sue_text)

    # THEN
    assert len(assignedunit_x._suffideas) == 1


def test_AssignedHeir_exists():
    # GIVEN
    _suffideas_x = {1: 2}
    _owner_id_assigned_x = True

    # WHEN
    assigned_heir_x = AssignedHeir(
        _suffideas=_suffideas_x, _owner_id_assigned=_owner_id_assigned_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffideas == _suffideas_x
    assert assigned_heir_x._owner_id_assigned == _owner_id_assigned_x


def test_assigned_heir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffideas_x = {1: 2}
    _owner_id_assigned_x = "example"

    # WHEN
    assigned_heir_x = assigned_heir_shop(
        _suffideas=_suffideas_x, _owner_id_assigned=_owner_id_assigned_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffideas == _suffideas_x
    assert assigned_heir_x._owner_id_assigned == _owner_id_assigned_x


def test_AssignedHeir_get_all_suff_partys_ReturnsSingleDictWithAllPartys_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)

    _suffideas_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffideas=_suffideas_x)

    # WHEN
    all_partys = assigned_heir_x._get_all_suff_partys(agenda_ideas=x_agenda._ideas)

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
    swim_idea = ideaunit_shop(idea_id=swim_text)
    swim_idea.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim_idea.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_ideaunit(y_ideaunit=swim_idea)

    _suffideas_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffideas=_suffideas_x)

    # WHEN
    all_partys = assigned_heir_x._get_all_suff_partys(agenda_ideas=x_agenda._ideas)

    # THEN
    assert len(all_partys) == 2


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_Empty_suffideas_x():
    # GIVEN
    _suffideas_x = {}
    assigned_heir_x = assigned_heir_shop(_suffideas=_suffideas_x)
    assert assigned_heir_x._owner_id_assigned is False

    # WHEN
    agenda_ideas = {}
    assigned_heir_x.set_owner_id_assigned(agenda_ideas=agenda_ideas, agenda_owner_id="")

    # THEN
    assert assigned_heir_x._owner_id_assigned


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_NonEmpty_suffideas_x_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    agenda_owner_id = x_agenda._owner_id
    agenda_ideas = x_agenda._ideas
    print(f"{len(agenda_ideas)=}")
    # print(f"{agenda_ideas.get(jim_text)=}")
    # print(f"{agenda_ideas.get(sue_text)=}")

    _suffideas_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffideas=_suffideas_x)
    assert assigned_heir_x._owner_id_assigned is False

    # WHEN
    assigned_heir_x.set_owner_id_assigned(agenda_ideas, agenda_owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_NonEmpty_suffideas_x_v2():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    agenda_owner_id = x_agenda._owner_id
    agenda_ideas = x_agenda._ideas
    print(f"{len(agenda_ideas)=}")
    # print(f"{agenda_ideas.get(jim_text)=}")
    # print(f"{agenda_ideas.get(sue_text)=}")

    _suffideas_x = {sue_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffideas=_suffideas_x)
    assert assigned_heir_x._owner_id_assigned is False

    # WHEN
    assigned_heir_x.set_owner_id_assigned(agenda_ideas, agenda_owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned is False


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_NonEmpty_suffideas_x_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)

    swim_text = ",swim"
    swim_idea = ideaunit_shop(idea_id=swim_text)
    swim_idea.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim_idea.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_ideaunit(y_ideaunit=swim_idea)

    _suffideas_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffideas=_suffideas_x)
    assert assigned_heir_x._owner_id_assigned is False
    assigned_heir_x.set_owner_id_assigned(x_agenda._ideas, x_agenda._owner_id)
    assert assigned_heir_x._owner_id_assigned

    # WHEN
    swim_idea.del_partylink(party_id=jim_text)
    x_agenda.set_ideaunit(y_ideaunit=swim_idea)
    assigned_heir_x.set_owner_id_assigned(x_agenda._ideas, x_agenda._owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned is False


def test_AssignedHeir_set__CorrectlySetsAttribute_NonEmpty_suffideas_x_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_agenda = agendaunit_shop(_owner_id=jim_text)
    x_agenda.add_partyunit(party_id=jim_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda.add_partyunit(party_id=bob_text)

    swim_text = ",swim"
    swim_idea = ideaunit_shop(idea_id=swim_text)
    swim_idea.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim_idea.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_ideaunit(y_ideaunit=swim_idea)

    _suffideas_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffideas=_suffideas_x)
    assert assigned_heir_x._owner_id_assigned is False
    assigned_heir_x.set_owner_id_assigned(x_agenda._ideas, x_agenda._owner_id)
    assert assigned_heir_x._owner_id_assigned

    # WHEN
    swim_idea.del_partylink(party_id=jim_text)
    x_agenda.set_ideaunit(y_ideaunit=swim_idea)
    assigned_heir_x.set_owner_id_assigned(x_agenda._ideas, x_agenda._owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned is False


def test_AssignedHeir_set_suffidea_AssignedUnitEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    assigned_heir_x = assigned_heir_shop(_suffideas={})
    parent_assignheir_empty = assigned_heir_shop()
    assignedunit_x = assignedunit_shop()

    # WHEN
    assigned_heir_x.set_suffideas(
        parent_assignheir=parent_assignheir_empty,
        assignunit=assignedunit_x,
        agenda_ideas=None,
    )

    # THEN
    assigned_heir_x._suffideas = {}


def test_AssignedHeir_set_suffidea_AssignedUnitNotEmpty_ParentAssignedHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_x = assignedunit_shop()
    assignedunit_x.set_suffidea(idea_id=kent_text)
    assignedunit_x.set_suffidea(idea_id=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffideas(
        parent_assignheir=None, assignunit=assignedunit_x, agenda_ideas=None
    )

    # THEN
    assert assigned_heir_x._suffideas.keys() == assignedunit_x._suffideas.keys()


def test_AssignedHeir_set_suffidea_AssignedUnitNotEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_x = assignedunit_shop()
    assignedunit_x.set_suffidea(idea_id=kent_text)
    assignedunit_x.set_suffidea(idea_id=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    parent_assignheir_empty = assigned_heir_shop()
    assigned_heir_x.set_suffideas(
        parent_assignheir_empty, assignunit=assignedunit_x, agenda_ideas=None
    )

    # THEN
    assert assigned_heir_x._suffideas.keys() == assignedunit_x._suffideas.keys()


def test_AssignedHeir_set_suffidea_AssignedUnitEmpty_ParentAssignedHeirNotEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_swim = assignedunit_shop()
    assignedunit_swim.set_suffidea(idea_id=kent_text)
    assignedunit_swim.set_suffidea(idea_id=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffideas(
        empty_assigned_heir, assignedunit_swim, agenda_ideas=None
    )

    assignedunit_empty = assignedunit_shop()

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffideas == {}
    assigned_heir_x.set_suffideas(
        parent_assigned_heir, assignunit=assignedunit_empty, agenda_ideas=None
    )

    # THEN
    assert len(assigned_heir_x._suffideas.keys())
    assert assigned_heir_x._suffideas.keys() == parent_assigned_heir._suffideas.keys()


def test_AssignedHeir_set_suffidea_AssignedUnitEqualParentAssignedHeir_NonEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_swim = assignedunit_shop()
    assignedunit_swim.set_suffidea(idea_id=kent_text)
    assignedunit_swim.set_suffidea(idea_id=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffideas(
        empty_assigned_heir, assignedunit_swim, agenda_ideas=None
    )

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffideas == {}
    assigned_heir_x.set_suffideas(
        parent_assigned_heir, assignunit=assignedunit_swim, agenda_ideas=None
    )

    # THEN
    assert assigned_heir_x._suffideas.keys() == parent_assigned_heir._suffideas.keys()


def test_AssignedHeir_set_suffidea_AssignedUnit_NotEqual_ParentAssignedHeir_NonEmpty():
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
    swim2_idea = ideaunit_shop(idea_id=swim2_text)
    swim2_idea.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim2_idea.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_ideaunit(y_ideaunit=swim2_idea)

    swim3_text = ",swim3"
    swim3_idea = ideaunit_shop(idea_id=swim3_text)
    swim3_idea.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim3_idea.set_partylink(partylink=partylink_shop(party_id=sue_text))
    swim3_idea.set_partylink(partylink=partylink_shop(party_id=tom_text))
    x_agenda.set_ideaunit(y_ideaunit=swim3_idea)

    parent_assignedunit = assignedunit_shop()
    parent_assignedunit.set_suffidea(idea_id=swim3_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffideas(
        parent_assignheir=None, assignunit=parent_assignedunit, agenda_ideas=None
    )

    assignedunit_swim2 = assignedunit_shop()
    assignedunit_swim2.set_suffidea(idea_id=swim2_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffideas(
        parent_assigned_heir, assignedunit_swim2, agenda_ideas=x_agenda._ideas
    )

    # THEN
    assert assigned_heir_x._suffideas.keys() == assignedunit_swim2._suffideas.keys()
    assert len(assigned_heir_x._suffideas.keys()) == 1
    assert list(assigned_heir_x._suffideas) == [swim2_text]


def test_AssignedHeir_set_suffidea_AssignedUnit_NotEqualParentAssignedHeir_RaisesError():
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
    swim2_idea = ideaunit_shop(idea_id=swim2_text)
    swim2_idea.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim2_idea.set_partylink(partylink=partylink_shop(party_id=sue_text))
    x_agenda.set_ideaunit(y_ideaunit=swim2_idea)

    swim3_text = ",swim3"
    swim3_idea = ideaunit_shop(idea_id=swim3_text)
    swim3_idea.set_partylink(partylink=partylink_shop(party_id=jim_text))
    swim3_idea.set_partylink(partylink=partylink_shop(party_id=sue_text))
    swim3_idea.set_partylink(partylink=partylink_shop(party_id=tom_text))
    x_agenda.set_ideaunit(y_ideaunit=swim3_idea)

    parent_assignedunit = assignedunit_shop()
    parent_assignedunit.set_suffidea(idea_id=swim2_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffideas(
        parent_assignheir=None, assignunit=parent_assignedunit, agenda_ideas=None
    )

    assignedunit_swim3 = assignedunit_shop()
    assignedunit_swim3.set_suffidea(idea_id=swim3_text)

    # WHEN / THEN
    assigned_heir_x = assigned_heir_shop()
    all_parent_assignedheir_partys = {jim_text, sue_text}
    all_assignedunit_partys = {jim_text, sue_text, tom_text}
    with pytest_raises(Exception) as excinfo:
        assigned_heir_x.set_suffideas(
            parent_assigned_heir, assignedunit_swim3, agenda_ideas=x_agenda._ideas
        )
    assert (
        str(excinfo.value)
        == f"parent_assigned_heir does not contain all partys of the fact's assignedunit\n{set(all_parent_assignedheir_partys)=}\n\n{set(all_assignedunit_partys)=}"
    )


def test_AssignedUnit_get_suffidea_ReturnsCorrectObj():
    # GIVEN
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffidea(climb_text)
    x_assignedunit.set_suffidea(walk_text)
    x_assignedunit.set_suffidea(swim_text)

    # WHEN / THEN
    assert x_assignedunit.get_suffidea(walk_text) != None
    assert x_assignedunit.get_suffidea(swim_text) != None
    assert x_assignedunit.get_suffidea(run_text) is None


def test_AssignedHeir_idea_in_ReturnsCorrectBoolWhen_suffideasNotEmpty():
    # GIVEN
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text: -1}
    hike_dict = {hike_text: -1}
    assignedunit_x = assignedunit_shop()
    assignedunit_x.set_suffidea(idea_id=swim_text)
    assignedunit_x.set_suffidea(idea_id=hike_text)
    assignedheir_x = assigned_heir_shop()
    assignedheir_x.set_suffideas(
        parent_assignheir=None, assignunit=assignedunit_x, agenda_ideas=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text: -1}
    play_text = ",play"
    play_dict = {play_text: -1}
    assert assignedheir_x._suffideas.get(swim_text) != None
    assert assignedheir_x._suffideas.get(hike_text) != None
    assert assignedheir_x._suffideas.get(hunt_text) is None
    assert assignedheir_x._suffideas.get(play_text) is None
    hunt_hike_dict = {hunt_text: -1, hike_text: -1}
    hunt_play_dict = {hunt_text: -1, play_text: -1}

    # WHEN / THEN
    assert assignedheir_x.idea_in(swim_dict)
    assert assignedheir_x.idea_in(hike_dict)
    assert assignedheir_x.idea_in(hunt_dict) is False
    assert assignedheir_x.idea_in(hunt_hike_dict)
    assert assignedheir_x.idea_in(hunt_play_dict) is False


def test_AssignedHeir_idea_in_ReturnsCorrectBoolWhen_suffideasEmpty():
    # GIVEN
    hike_text = ",hike"
    hike_dict = {hike_text: -1}
    assignedunit_x = assignedunit_shop()
    assignedheir_x = assigned_heir_shop()
    assignedheir_x.set_suffideas(
        parent_assignheir=None, assignunit=assignedunit_x, agenda_ideas=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text: -1}
    play_text = ",play"
    play_dict = {play_text: -1}
    assert assignedheir_x._suffideas == {}
    hunt_hike_dict = {hunt_text: -1, hike_text: -1}
    hunt_play_dict = {hunt_text: -1, play_text: -1}

    # WHEN / THEN
    assert assignedheir_x.idea_in(hike_dict)
    assert assignedheir_x.idea_in(hunt_dict)
    assert assignedheir_x.idea_in(play_dict)
    assert assignedheir_x.idea_in(hunt_hike_dict)
    assert assignedheir_x.idea_in(hunt_play_dict)
