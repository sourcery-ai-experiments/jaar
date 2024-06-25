from src._world.reason_assign import (
    AssignedUnit,
    assignedunit_shop,
    AssignedHeir,
    assigned_heir_shop,
    create_assignedunit,
)
from src._world.belief import BeliefID, beliefunit_shop
from src._world.person import belieflink_shop
from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_AssignedUnit_exists():
    # GIVEN
    _suffbeliefs_x = {1: 2}

    # WHEN
    assignedunit_x = AssignedUnit(_suffbeliefs=_suffbeliefs_x)

    # THEN
    assert assignedunit_x
    assert assignedunit_x._suffbeliefs == _suffbeliefs_x


def test_assignedunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffbeliefs_x = {1: 2}

    # WHEN
    assignedunit_x = assignedunit_shop(_suffbeliefs=_suffbeliefs_x)

    # THEN
    assert assignedunit_x
    assert assignedunit_x._suffbeliefs == _suffbeliefs_x


def test_assignedunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    assignedunit_x = assignedunit_shop()

    # THEN
    assert assignedunit_x
    assert assignedunit_x._suffbeliefs == {}


def test_create_assignedunit_ReturnsCorrectObj():
    # GIVEN
    swim_belief_id = BeliefID("swimmers")

    # WHEN
    swim_assignedunit = create_assignedunit(swim_belief_id)

    # THEN
    assert swim_assignedunit
    assert len(swim_assignedunit._suffbeliefs) == 1


def test_AssignedUnit_get_dict_ReturnsCorrectDictWithSingleSuffBelief():
    # GIVEN
    bob_belief_id = BeliefID("Bob")
    _suffbeliefs_x = {bob_belief_id: bob_belief_id}
    assigned_x = assignedunit_shop(_suffbeliefs=_suffbeliefs_x)

    # WHEN
    obj_dict = assigned_x.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_suffbeliefs": {bob_belief_id: bob_belief_id}}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_AssignedUnit_set_suffbelief_CorrectlySets_suffbeliefs_v1():
    # GIVEN
    assignedunit_x = assignedunit_shop(_suffbeliefs={})
    assert len(assignedunit_x._suffbeliefs) == 0

    # WHEN
    jim_text = "Jim"
    assignedunit_x.set_suffbelief(belief_id=jim_text)

    # THEN
    assert len(assignedunit_x._suffbeliefs) == 1


def test_AssignedUnit_suffbelief_exists_ReturnsCorrectObj():
    # GIVEN
    assignedunit_x = assignedunit_shop(_suffbeliefs={})
    jim_text = "Jim"
    assert assignedunit_x.suffbelief_exists(jim_text) is False

    # WHEN
    assignedunit_x.set_suffbelief(belief_id=jim_text)

    # THEN
    assert assignedunit_x.suffbelief_exists(jim_text)


def test_AssignedUnit_del_suffbelief_CorrectlyDeletes_suffbeliefs_v1():
    # GIVEN
    assignedunit_x = assignedunit_shop(_suffbeliefs={})
    jim_text = "Jim"
    sue_text = "Sue"
    assignedunit_x.set_suffbelief(belief_id=jim_text)
    assignedunit_x.set_suffbelief(belief_id=sue_text)
    assert len(assignedunit_x._suffbeliefs) == 2

    # WHEN
    assignedunit_x.del_suffbelief(belief_id=sue_text)

    # THEN
    assert len(assignedunit_x._suffbeliefs) == 1


def test_AssignedHeir_exists():
    # GIVEN
    _suffbeliefs_x = {1: 2}
    _owner_id_assigned_x = True

    # WHEN
    assigned_heir_x = AssignedHeir(
        _suffbeliefs=_suffbeliefs_x, _owner_id_assigned=_owner_id_assigned_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffbeliefs == _suffbeliefs_x
    assert assigned_heir_x._owner_id_assigned == _owner_id_assigned_x


def test_assigned_heir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _suffbeliefs_x = {1: 2}
    _owner_id_assigned_x = "example"

    # WHEN
    assigned_heir_x = assigned_heir_shop(
        _suffbeliefs=_suffbeliefs_x, _owner_id_assigned=_owner_id_assigned_x
    )

    # THEN
    assert assigned_heir_x
    assert assigned_heir_x._suffbeliefs == _suffbeliefs_x
    assert assigned_heir_x._owner_id_assigned == _owner_id_assigned_x


def test_AssignedHeir_get_all_suff_persons_ReturnsSingleDictWithAllPersons_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_personunit(person_id=jim_text)
    x_world.add_personunit(person_id=sue_text)

    _suffbeliefs_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffbeliefs=_suffbeliefs_x)

    # WHEN
    all_persons = assigned_heir_x._get_all_suff_persons(world_beliefs=x_world._beliefs)

    # THEN
    assert len(all_persons) == 1


def test_AssignedHeir_get_all_suff_persons_ReturnsSingleDictWithAllPersons_v2():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_personunit(person_id=jim_text)
    x_world.add_personunit(person_id=sue_text)
    x_world.add_personunit(person_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_belieflink(belieflink=belieflink_shop(person_id=jim_text))
    swim_belief.set_belieflink(belieflink=belieflink_shop(person_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)

    _suffbeliefs_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffbeliefs=_suffbeliefs_x)

    # WHEN
    all_persons = assigned_heir_x._get_all_suff_persons(world_beliefs=x_world._beliefs)

    # THEN
    assert len(all_persons) == 2


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_Empty_suffbeliefs_x():
    # GIVEN
    _suffbeliefs_x = {}
    assigned_heir_x = assigned_heir_shop(_suffbeliefs=_suffbeliefs_x)
    assert assigned_heir_x._owner_id_assigned is False

    # WHEN
    world_beliefs = {}
    assigned_heir_x.set_owner_id_assigned(
        world_beliefs=world_beliefs, world_owner_id=""
    )

    # THEN
    assert assigned_heir_x._owner_id_assigned


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_NonEmpty_suffbeliefs_x_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_personunit(person_id=jim_text)
    x_world.add_personunit(person_id=sue_text)
    world_owner_id = x_world._owner_id
    world_beliefs = x_world._beliefs
    print(f"{len(world_beliefs)=}")
    # print(f"{world_beliefs.get(jim_text)=}")
    # print(f"{world_beliefs.get(sue_text)=}")

    _suffbeliefs_x = {jim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffbeliefs=_suffbeliefs_x)
    assert assigned_heir_x._owner_id_assigned is False

    # WHEN
    assigned_heir_x.set_owner_id_assigned(world_beliefs, world_owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_NonEmpty_suffbeliefs_x_v2():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_personunit(person_id=jim_text)
    x_world.add_personunit(person_id=sue_text)
    world_owner_id = x_world._owner_id
    world_beliefs = x_world._beliefs
    print(f"{len(world_beliefs)=}")
    # print(f"{world_beliefs.get(jim_text)=}")
    # print(f"{world_beliefs.get(sue_text)=}")

    _suffbeliefs_x = {sue_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffbeliefs=_suffbeliefs_x)
    assert assigned_heir_x._owner_id_assigned is False

    # WHEN
    assigned_heir_x.set_owner_id_assigned(world_beliefs, world_owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned is False


def test_AssignedHeir_set_owner_id_assigned_CorrectlySetsAttribute_NonEmpty_suffbeliefs_x_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_personunit(person_id=jim_text)
    x_world.add_personunit(person_id=sue_text)
    x_world.add_personunit(person_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_belieflink(belieflink=belieflink_shop(person_id=jim_text))
    swim_belief.set_belieflink(belieflink=belieflink_shop(person_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)

    _suffbeliefs_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffbeliefs=_suffbeliefs_x)
    assert assigned_heir_x._owner_id_assigned is False
    assigned_heir_x.set_owner_id_assigned(x_world._beliefs, x_world._owner_id)
    assert assigned_heir_x._owner_id_assigned

    # WHEN
    swim_belief.del_belieflink(person_id=jim_text)
    x_world.set_beliefunit(y_beliefunit=swim_belief)
    assigned_heir_x.set_owner_id_assigned(x_world._beliefs, x_world._owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned is False


def test_AssignedHeir_set__CorrectlySetsAttribute_NonEmpty_suffbeliefs_x_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_personunit(person_id=jim_text)
    x_world.add_personunit(person_id=sue_text)
    x_world.add_personunit(person_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_belieflink(belieflink=belieflink_shop(person_id=jim_text))
    swim_belief.set_belieflink(belieflink=belieflink_shop(person_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)

    _suffbeliefs_x = {swim_text: -1}
    assigned_heir_x = assigned_heir_shop(_suffbeliefs=_suffbeliefs_x)
    assert assigned_heir_x._owner_id_assigned is False
    assigned_heir_x.set_owner_id_assigned(x_world._beliefs, x_world._owner_id)
    assert assigned_heir_x._owner_id_assigned

    # WHEN
    swim_belief.del_belieflink(person_id=jim_text)
    x_world.set_beliefunit(y_beliefunit=swim_belief)
    assigned_heir_x.set_owner_id_assigned(x_world._beliefs, x_world._owner_id)

    # THEN
    assert assigned_heir_x._owner_id_assigned is False


def test_AssignedHeir_set_suffbelief_AssignedUnitEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    assigned_heir_x = assigned_heir_shop(_suffbeliefs={})
    parent_assignheir_empty = assigned_heir_shop()
    assignedunit_x = assignedunit_shop()

    # WHEN
    assigned_heir_x.set_suffbeliefs(
        parent_assignheir=parent_assignheir_empty,
        assignunit=assignedunit_x,
        world_beliefs=None,
    )

    # THEN
    assigned_heir_x._suffbeliefs = {}


def test_AssignedHeir_set_suffbelief_AssignedUnitNotEmpty_ParentAssignedHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_x = assignedunit_shop()
    assignedunit_x.set_suffbelief(belief_id=kent_text)
    assignedunit_x.set_suffbelief(belief_id=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffbeliefs(
        parent_assignheir=None, assignunit=assignedunit_x, world_beliefs=None
    )

    # THEN
    assert assigned_heir_x._suffbeliefs.keys() == assignedunit_x._suffbeliefs.keys()


def test_AssignedHeir_set_suffbelief_AssignedUnitNotEmpty_ParentAssignedHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_x = assignedunit_shop()
    assignedunit_x.set_suffbelief(belief_id=kent_text)
    assignedunit_x.set_suffbelief(belief_id=swim_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    parent_assignheir_empty = assigned_heir_shop()
    assigned_heir_x.set_suffbeliefs(
        parent_assignheir_empty, assignunit=assignedunit_x, world_beliefs=None
    )

    # THEN
    assert assigned_heir_x._suffbeliefs.keys() == assignedunit_x._suffbeliefs.keys()


def test_AssignedHeir_set_suffbelief_AssignedUnitEmpty_ParentAssignedHeirNotEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_swim = assignedunit_shop()
    assignedunit_swim.set_suffbelief(belief_id=kent_text)
    assignedunit_swim.set_suffbelief(belief_id=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffbeliefs(
        empty_assigned_heir, assignedunit_swim, world_beliefs=None
    )

    assignedunit_empty = assignedunit_shop()

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffbeliefs == {}
    assigned_heir_x.set_suffbeliefs(
        parent_assigned_heir, assignunit=assignedunit_empty, world_beliefs=None
    )

    # THEN
    assert len(assigned_heir_x._suffbeliefs.keys())
    assert (
        assigned_heir_x._suffbeliefs.keys() == parent_assigned_heir._suffbeliefs.keys()
    )


def test_AssignedHeir_set_suffbelief_AssignedUnitEqualParentAssignedHeir_NonEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    assignedunit_swim = assignedunit_shop()
    assignedunit_swim.set_suffbelief(belief_id=kent_text)
    assignedunit_swim.set_suffbelief(belief_id=swim_text)
    empty_assigned_heir = assigned_heir_shop()

    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffbeliefs(
        empty_assigned_heir, assignedunit_swim, world_beliefs=None
    )

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assert assigned_heir_x._suffbeliefs == {}
    assigned_heir_x.set_suffbeliefs(
        parent_assigned_heir, assignunit=assignedunit_swim, world_beliefs=None
    )

    # THEN
    assert (
        assigned_heir_x._suffbeliefs.keys() == parent_assigned_heir._suffbeliefs.keys()
    )


def test_AssignedHeir_set_suffbelief_AssignedUnit_NotEqual_ParentAssignedHeir_NonEmpty():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    tom_text = "Tom"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_personunit(person_id=jim_text)
    x_world.add_personunit(person_id=sue_text)
    x_world.add_personunit(person_id=bob_text)
    x_world.add_personunit(person_id=tom_text)

    swim2_text = ",swim2"
    swim2_belief = beliefunit_shop(belief_id=swim2_text)
    swim2_belief.set_belieflink(belieflink=belieflink_shop(person_id=jim_text))
    swim2_belief.set_belieflink(belieflink=belieflink_shop(person_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim2_belief)

    swim3_text = ",swim3"
    swim3_belief = beliefunit_shop(belief_id=swim3_text)
    swim3_belief.set_belieflink(belieflink=belieflink_shop(person_id=jim_text))
    swim3_belief.set_belieflink(belieflink=belieflink_shop(person_id=sue_text))
    swim3_belief.set_belieflink(belieflink=belieflink_shop(person_id=tom_text))
    x_world.set_beliefunit(y_beliefunit=swim3_belief)

    parent_assignedunit = assignedunit_shop()
    parent_assignedunit.set_suffbelief(belief_id=swim3_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffbeliefs(
        parent_assignheir=None, assignunit=parent_assignedunit, world_beliefs=None
    )

    assignedunit_swim2 = assignedunit_shop()
    assignedunit_swim2.set_suffbelief(belief_id=swim2_text)

    # WHEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffbeliefs(
        parent_assigned_heir, assignedunit_swim2, world_beliefs=x_world._beliefs
    )

    # THEN
    assert assigned_heir_x._suffbeliefs.keys() == assignedunit_swim2._suffbeliefs.keys()
    assert len(assigned_heir_x._suffbeliefs.keys()) == 1
    assert list(assigned_heir_x._suffbeliefs) == [swim2_text]


def test_AssignedHeir_set_suffbelief_AssignedUnit_NotEqualParentAssignedHeir_RaisesError():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    tom_text = "Tom"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_personunit(person_id=jim_text)
    x_world.add_personunit(person_id=sue_text)
    x_world.add_personunit(person_id=bob_text)
    x_world.add_personunit(person_id=tom_text)

    swim2_text = ",swim2"
    swim2_belief = beliefunit_shop(belief_id=swim2_text)
    swim2_belief.set_belieflink(belieflink=belieflink_shop(person_id=jim_text))
    swim2_belief.set_belieflink(belieflink=belieflink_shop(person_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim2_belief)

    swim3_text = ",swim3"
    swim3_belief = beliefunit_shop(belief_id=swim3_text)
    swim3_belief.set_belieflink(belieflink=belieflink_shop(person_id=jim_text))
    swim3_belief.set_belieflink(belieflink=belieflink_shop(person_id=sue_text))
    swim3_belief.set_belieflink(belieflink=belieflink_shop(person_id=tom_text))
    x_world.set_beliefunit(y_beliefunit=swim3_belief)

    parent_assignedunit = assignedunit_shop()
    parent_assignedunit.set_suffbelief(belief_id=swim2_text)
    parent_assigned_heir = assigned_heir_shop()
    parent_assigned_heir.set_suffbeliefs(
        parent_assignheir=None, assignunit=parent_assignedunit, world_beliefs=None
    )

    assignedunit_swim3 = assignedunit_shop()
    assignedunit_swim3.set_suffbelief(belief_id=swim3_text)

    # WHEN / THEN
    assigned_heir_x = assigned_heir_shop()
    all_parent_assignedheir_persons = {jim_text, sue_text}
    all_assignedunit_persons = {jim_text, sue_text, tom_text}
    with pytest_raises(Exception) as excinfo:
        assigned_heir_x.set_suffbeliefs(
            parent_assigned_heir, assignedunit_swim3, world_beliefs=x_world._beliefs
        )
    assert (
        str(excinfo.value)
        == f"parent_assigned_heir does not contain all persons of the idea's assignedunit\n{set(all_parent_assignedheir_persons)=}\n\n{set(all_assignedunit_persons)=}"
    )


def test_AssignedUnit_get_suffbelief_ReturnsCorrectObj():
    # GIVEN
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffbelief(climb_text)
    x_assignedunit.set_suffbelief(walk_text)
    x_assignedunit.set_suffbelief(swim_text)

    # WHEN / THEN
    assert x_assignedunit.get_suffbelief(walk_text) != None
    assert x_assignedunit.get_suffbelief(swim_text) != None
    assert x_assignedunit.get_suffbelief(run_text) is None


def test_AssignedHeir_belief_in_ReturnsCorrectBoolWhen_suffbeliefsNotEmpty():
    # GIVEN
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text: -1}
    hike_dict = {hike_text: -1}
    assignedunit_x = assignedunit_shop()
    assignedunit_x.set_suffbelief(belief_id=swim_text)
    assignedunit_x.set_suffbelief(belief_id=hike_text)
    assignedheir_x = assigned_heir_shop()
    assignedheir_x.set_suffbeliefs(
        parent_assignheir=None, assignunit=assignedunit_x, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text: -1}
    play_text = ",play"
    play_dict = {play_text: -1}
    assert assignedheir_x._suffbeliefs.get(swim_text) != None
    assert assignedheir_x._suffbeliefs.get(hike_text) != None
    assert assignedheir_x._suffbeliefs.get(hunt_text) is None
    assert assignedheir_x._suffbeliefs.get(play_text) is None
    hunt_hike_dict = {hunt_text: -1, hike_text: -1}
    hunt_play_dict = {hunt_text: -1, play_text: -1}

    # WHEN / THEN
    assert assignedheir_x.belief_in(swim_dict)
    assert assignedheir_x.belief_in(hike_dict)
    assert assignedheir_x.belief_in(hunt_dict) is False
    assert assignedheir_x.belief_in(hunt_hike_dict)
    assert assignedheir_x.belief_in(hunt_play_dict) is False


def test_AssignedHeir_belief_in_ReturnsCorrectBoolWhen_suffbeliefsEmpty():
    # GIVEN
    hike_text = ",hike"
    hike_dict = {hike_text: -1}
    assignedunit_x = assignedunit_shop()
    assignedheir_x = assigned_heir_shop()
    assignedheir_x.set_suffbeliefs(
        parent_assignheir=None, assignunit=assignedunit_x, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text: -1}
    play_text = ",play"
    play_dict = {play_text: -1}
    assert assignedheir_x._suffbeliefs == {}
    hunt_hike_dict = {hunt_text: -1, hike_text: -1}
    hunt_play_dict = {hunt_text: -1, play_text: -1}

    # WHEN / THEN
    assert assignedheir_x.belief_in(hike_dict)
    assert assignedheir_x.belief_in(hunt_dict)
    assert assignedheir_x.belief_in(play_dict)
    assert assignedheir_x.belief_in(hunt_hike_dict)
    assert assignedheir_x.belief_in(hunt_play_dict)
