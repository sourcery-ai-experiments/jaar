from src._world.reason_culture import (
    CultureUnit,
    cultureunit_shop,
    CultureHeir,
    cultureheir_shop,
    create_cultureunit,
)
from src._world.beliefunit import BeliefID, beliefunit_shop
from src._world.char import charlink_shop
from src._world.world import worldunit_shop
from pytest import raises as pytest_raises


def test_CultureUnit_exists():
    # GIVEN
    _heldbeliefs_x = {1: 2}

    # WHEN
    cultureunit_x = CultureUnit(_heldbeliefs=_heldbeliefs_x)

    # THEN
    assert cultureunit_x
    assert cultureunit_x._heldbeliefs == _heldbeliefs_x


def test_cultureunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _heldbeliefs_x = {1: 2}

    # WHEN
    cultureunit_x = cultureunit_shop(_heldbeliefs=_heldbeliefs_x)

    # THEN
    assert cultureunit_x
    assert cultureunit_x._heldbeliefs == _heldbeliefs_x


def test_cultureunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    cultureunit_x = cultureunit_shop()

    # THEN
    assert cultureunit_x
    assert cultureunit_x._heldbeliefs == {}


def test_create_cultureunit_ReturnsCorrectObj():
    # GIVEN
    swim_belief_id = BeliefID("swimmers")

    # WHEN
    swim_cultureunit = create_cultureunit(swim_belief_id)

    # THEN
    assert swim_cultureunit
    assert len(swim_cultureunit._heldbeliefs) == 1


def test_CultureUnit_get_dict_ReturnsCorrectDictWithSingle_heldbelief():
    # GIVEN
    bob_belief_id = BeliefID("Bob")
    _heldbeliefs_x = {bob_belief_id: bob_belief_id}
    culture_x = cultureunit_shop(_heldbeliefs=_heldbeliefs_x)

    # WHEN
    obj_dict = culture_x.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_heldbeliefs": {bob_belief_id: bob_belief_id}}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_CultureUnit_set_heldbelief_CorrectlySets_heldbeliefs_v1():
    # GIVEN
    cultureunit_x = cultureunit_shop(_heldbeliefs={})
    assert len(cultureunit_x._heldbeliefs) == 0

    # WHEN
    jim_text = "Jim"
    cultureunit_x.set_heldbelief(belief_id=jim_text)

    # THEN
    assert len(cultureunit_x._heldbeliefs) == 1


def test_CultureUnit_heldbelief_exists_ReturnsCorrectObj():
    # GIVEN
    cultureunit_x = cultureunit_shop(_heldbeliefs={})
    jim_text = "Jim"
    assert cultureunit_x.heldbelief_exists(jim_text) is False

    # WHEN
    cultureunit_x.set_heldbelief(belief_id=jim_text)

    # THEN
    assert cultureunit_x.heldbelief_exists(jim_text)


def test_CultureUnit_del_heldbelief_CorrectlyDeletes_heldbeliefs_v1():
    # GIVEN
    cultureunit_x = cultureunit_shop(_heldbeliefs={})
    jim_text = "Jim"
    sue_text = "Sue"
    cultureunit_x.set_heldbelief(belief_id=jim_text)
    cultureunit_x.set_heldbelief(belief_id=sue_text)
    assert len(cultureunit_x._heldbeliefs) == 2

    # WHEN
    cultureunit_x.del_heldbelief(belief_id=sue_text)

    # THEN
    assert len(cultureunit_x._heldbeliefs) == 1


def test_CultureHeir_exists():
    # GIVEN
    _heldbeliefs_x = {1: 2}
    _owner_id_culture_x = True

    # WHEN
    culture_heir_x = CultureHeir(
        _heldbeliefs=_heldbeliefs_x, _owner_id_culture=_owner_id_culture_x
    )

    # THEN
    assert culture_heir_x
    assert culture_heir_x._heldbeliefs == _heldbeliefs_x
    assert culture_heir_x._owner_id_culture == _owner_id_culture_x


def test_cultureheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    _heldbeliefs_x = {1: 2}
    _owner_id_culture_x = "example"

    # WHEN
    culture_heir_x = cultureheir_shop(
        _heldbeliefs=_heldbeliefs_x, _owner_id_culture=_owner_id_culture_x
    )

    # THEN
    assert culture_heir_x
    assert culture_heir_x._heldbeliefs == _heldbeliefs_x
    assert culture_heir_x._owner_id_culture == _owner_id_culture_x


def test_CultureHeir_get_all_suff_chars_ReturnsSingleDictWithAllChars_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)

    _heldbeliefs_x = {jim_text: -1}
    culture_heir_x = cultureheir_shop(_heldbeliefs=_heldbeliefs_x)

    # WHEN
    all_chars = culture_heir_x._get_all_suff_chars(world_beliefs=x_world._beliefs)

    # THEN
    assert len(all_chars) == 1


def test_CultureHeir_get_all_suff_chars_ReturnsSingleDictWithAllChars_v2():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)

    _heldbeliefs_x = {swim_text: -1}
    culture_heir_x = cultureheir_shop(_heldbeliefs=_heldbeliefs_x)

    # WHEN
    all_chars = culture_heir_x._get_all_suff_chars(world_beliefs=x_world._beliefs)

    # THEN
    assert len(all_chars) == 2


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_Empty_heldbeliefs_x():
    # GIVEN
    _heldbeliefs_x = {}
    culture_heir_x = cultureheir_shop(_heldbeliefs=_heldbeliefs_x)
    assert culture_heir_x._owner_id_culture is False

    # WHEN
    world_beliefs = {}
    culture_heir_x.set_owner_id_culture(world_beliefs=world_beliefs, world_owner_id="")

    # THEN
    assert culture_heir_x._owner_id_culture


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmpty_heldbeliefs_x_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    world_owner_id = x_world._owner_id
    world_beliefs = x_world._beliefs
    print(f"{len(world_beliefs)=}")
    # print(f"{world_beliefs.get(jim_text)=}")
    # print(f"{world_beliefs.get(sue_text)=}")

    _heldbeliefs_x = {jim_text: -1}
    culture_heir_x = cultureheir_shop(_heldbeliefs=_heldbeliefs_x)
    assert culture_heir_x._owner_id_culture is False

    # WHEN
    culture_heir_x.set_owner_id_culture(world_beliefs, world_owner_id)

    # THEN
    assert culture_heir_x._owner_id_culture


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmpty_heldbeliefs_x_v2():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"

    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    world_owner_id = x_world._owner_id
    world_beliefs = x_world._beliefs
    print(f"{len(world_beliefs)=}")
    # print(f"{world_beliefs.get(jim_text)=}")
    # print(f"{world_beliefs.get(sue_text)=}")

    _heldbeliefs_x = {sue_text: -1}
    culture_heir_x = cultureheir_shop(_heldbeliefs=_heldbeliefs_x)
    assert culture_heir_x._owner_id_culture is False

    # WHEN
    culture_heir_x.set_owner_id_culture(world_beliefs, world_owner_id)

    # THEN
    assert culture_heir_x._owner_id_culture is False


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmpty_heldbeliefs_x_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)

    _heldbeliefs_x = {swim_text: -1}
    culture_heir_x = cultureheir_shop(_heldbeliefs=_heldbeliefs_x)
    assert culture_heir_x._owner_id_culture is False
    culture_heir_x.set_owner_id_culture(x_world._beliefs, x_world._owner_id)
    assert culture_heir_x._owner_id_culture

    # WHEN
    swim_belief.del_charlink(char_id=jim_text)
    x_world.set_beliefunit(y_beliefunit=swim_belief)
    culture_heir_x.set_owner_id_culture(x_world._beliefs, x_world._owner_id)

    # THEN
    assert culture_heir_x._owner_id_culture is False


def test_CultureHeir_set__CorrectlySetsAttribute_NonEmpty_heldbeliefs_x_v3():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)

    swim_text = ",swim"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim_belief)

    _heldbeliefs_x = {swim_text: -1}
    culture_heir_x = cultureheir_shop(_heldbeliefs=_heldbeliefs_x)
    assert culture_heir_x._owner_id_culture is False
    culture_heir_x.set_owner_id_culture(x_world._beliefs, x_world._owner_id)
    assert culture_heir_x._owner_id_culture

    # WHEN
    swim_belief.del_charlink(char_id=jim_text)
    x_world.set_beliefunit(y_beliefunit=swim_belief)
    culture_heir_x.set_owner_id_culture(x_world._beliefs, x_world._owner_id)

    # THEN
    assert culture_heir_x._owner_id_culture is False


def test_CultureHeir_set_heldbelief_CultureUnitEmpty_ParentCultureHeirEmpty():
    # GIVEN
    culture_heir_x = cultureheir_shop(_heldbeliefs={})
    parent_cultureheir_empty = cultureheir_shop()
    cultureunit_x = cultureunit_shop()

    # WHEN
    culture_heir_x.set_heldbeliefs(
        parent_cultureheir=parent_cultureheir_empty,
        cultureunit=cultureunit_x,
        world_beliefs=None,
    )

    # THEN
    culture_heir_x._heldbeliefs = {}


def test_CultureHeir_set_heldbelief_CultureUnitNotEmpty_ParentCultureHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    cultureunit_x = cultureunit_shop()
    cultureunit_x.set_heldbelief(belief_id=kent_text)
    cultureunit_x.set_heldbelief(belief_id=swim_text)

    # WHEN
    culture_heir_x = cultureheir_shop()
    culture_heir_x.set_heldbeliefs(
        parent_cultureheir=None, cultureunit=cultureunit_x, world_beliefs=None
    )

    # THEN
    assert culture_heir_x._heldbeliefs.keys() == cultureunit_x._heldbeliefs.keys()


def test_CultureHeir_set_heldbelief_CultureUnitNotEmpty_ParentCultureHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    cultureunit_x = cultureunit_shop()
    cultureunit_x.set_heldbelief(belief_id=kent_text)
    cultureunit_x.set_heldbelief(belief_id=swim_text)

    # WHEN
    culture_heir_x = cultureheir_shop()
    parent_cultureheir_empty = cultureheir_shop()
    culture_heir_x.set_heldbeliefs(
        parent_cultureheir_empty, cultureunit=cultureunit_x, world_beliefs=None
    )

    # THEN
    assert culture_heir_x._heldbeliefs.keys() == cultureunit_x._heldbeliefs.keys()


def test_CultureHeir_set_heldbelief_CultureUnitEmpty_ParentCultureHeirNotEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    cultureunit_swim = cultureunit_shop()
    cultureunit_swim.set_heldbelief(belief_id=kent_text)
    cultureunit_swim.set_heldbelief(belief_id=swim_text)
    empty_culture_heir = cultureheir_shop()

    parent_culture_heir = cultureheir_shop()
    parent_culture_heir.set_heldbeliefs(
        empty_culture_heir, cultureunit_swim, world_beliefs=None
    )

    cultureunit_empty = cultureunit_shop()

    # WHEN
    culture_heir_x = cultureheir_shop()
    assert culture_heir_x._heldbeliefs == {}
    culture_heir_x.set_heldbeliefs(
        parent_culture_heir, cultureunit=cultureunit_empty, world_beliefs=None
    )

    # THEN
    assert len(culture_heir_x._heldbeliefs.keys())
    assert culture_heir_x._heldbeliefs.keys() == parent_culture_heir._heldbeliefs.keys()


def test_CultureHeir_set_heldbelief_CultureUnitEqualParentCultureHeir_NonEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    cultureunit_swim = cultureunit_shop()
    cultureunit_swim.set_heldbelief(belief_id=kent_text)
    cultureunit_swim.set_heldbelief(belief_id=swim_text)
    empty_culture_heir = cultureheir_shop()

    parent_culture_heir = cultureheir_shop()
    parent_culture_heir.set_heldbeliefs(
        empty_culture_heir, cultureunit_swim, world_beliefs=None
    )

    # WHEN
    culture_heir_x = cultureheir_shop()
    assert culture_heir_x._heldbeliefs == {}
    culture_heir_x.set_heldbeliefs(
        parent_culture_heir, cultureunit=cultureunit_swim, world_beliefs=None
    )

    # THEN
    assert culture_heir_x._heldbeliefs.keys() == parent_culture_heir._heldbeliefs.keys()


def test_CultureHeir_set_heldbelief_CultureUnit_NotEqual_ParentCultureHeir_NonEmpty():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    tom_text = "Tom"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)
    x_world.add_charunit(char_id=tom_text)

    swim2_text = ",swim2"
    swim2_belief = beliefunit_shop(belief_id=swim2_text)
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim2_belief)

    swim3_text = ",swim3"
    swim3_belief = beliefunit_shop(belief_id=swim3_text)
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=tom_text))
    x_world.set_beliefunit(y_beliefunit=swim3_belief)

    parent_cultureunit = cultureunit_shop()
    parent_cultureunit.set_heldbelief(belief_id=swim3_text)
    parent_culture_heir = cultureheir_shop()
    parent_culture_heir.set_heldbeliefs(
        parent_cultureheir=None, cultureunit=parent_cultureunit, world_beliefs=None
    )

    cultureunit_swim2 = cultureunit_shop()
    cultureunit_swim2.set_heldbelief(belief_id=swim2_text)

    # WHEN
    culture_heir_x = cultureheir_shop()
    culture_heir_x.set_heldbeliefs(
        parent_culture_heir, cultureunit_swim2, world_beliefs=x_world._beliefs
    )

    # THEN
    assert culture_heir_x._heldbeliefs.keys() == cultureunit_swim2._heldbeliefs.keys()
    assert len(culture_heir_x._heldbeliefs.keys()) == 1
    assert list(culture_heir_x._heldbeliefs) == [swim2_text]


def test_CultureHeir_set_heldbelief_CultureUnit_NotEqualParentCultureHeir_RaisesError():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    bob_text = "Bob"
    tom_text = "Tom"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)
    x_world.add_charunit(char_id=bob_text)
    x_world.add_charunit(char_id=tom_text)

    swim2_text = ",swim2"
    swim2_belief = beliefunit_shop(belief_id=swim2_text)
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim2_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    x_world.set_beliefunit(y_beliefunit=swim2_belief)

    swim3_text = ",swim3"
    swim3_belief = beliefunit_shop(belief_id=swim3_text)
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=jim_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    swim3_belief.set_charlink(charlink=charlink_shop(char_id=tom_text))
    x_world.set_beliefunit(y_beliefunit=swim3_belief)

    parent_cultureunit = cultureunit_shop()
    parent_cultureunit.set_heldbelief(belief_id=swim2_text)
    parent_culture_heir = cultureheir_shop()
    parent_culture_heir.set_heldbeliefs(
        parent_cultureheir=None, cultureunit=parent_cultureunit, world_beliefs=None
    )

    cultureunit_swim3 = cultureunit_shop()
    cultureunit_swim3.set_heldbelief(belief_id=swim3_text)

    # WHEN / THEN
    culture_heir_x = cultureheir_shop()
    all_parent_cultureheir_chars = {jim_text, sue_text}
    all_cultureunit_chars = {jim_text, sue_text, tom_text}
    with pytest_raises(Exception) as excinfo:
        culture_heir_x.set_heldbeliefs(
            parent_culture_heir, cultureunit_swim3, world_beliefs=x_world._beliefs
        )
    assert (
        str(excinfo.value)
        == f"parent_culture_heir does not contain all chars of the idea's cultureunit\n{set(all_parent_cultureheir_chars)=}\n\n{set(all_cultureunit_chars)=}"
    )


def test_CultureUnit_get_heldbelief_ReturnsCorrectObj():
    # GIVEN
    climb_text = ",climbers"
    walk_text = ",walkers"
    swim_text = ",swimmers"
    run_text = ",runners"

    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_heldbelief(climb_text)
    x_cultureunit.set_heldbelief(walk_text)
    x_cultureunit.set_heldbelief(swim_text)

    # WHEN / THEN
    assert x_cultureunit.get_heldbelief(walk_text) != None
    assert x_cultureunit.get_heldbelief(swim_text) != None
    assert x_cultureunit.get_heldbelief(run_text) is None


def test_CultureHeir_belief_in_ReturnsCorrectBoolWhen_heldbeliefsNotEmpty():
    # GIVEN
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text: -1}
    hike_dict = {hike_text: -1}
    cultureunit_x = cultureunit_shop()
    cultureunit_x.set_heldbelief(belief_id=swim_text)
    cultureunit_x.set_heldbelief(belief_id=hike_text)
    cultureheir_x = cultureheir_shop()
    cultureheir_x.set_heldbeliefs(
        parent_cultureheir=None, cultureunit=cultureunit_x, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text: -1}
    play_text = ",play"
    play_dict = {play_text: -1}
    assert cultureheir_x._heldbeliefs.get(swim_text) != None
    assert cultureheir_x._heldbeliefs.get(hike_text) != None
    assert cultureheir_x._heldbeliefs.get(hunt_text) is None
    assert cultureheir_x._heldbeliefs.get(play_text) is None
    hunt_hike_dict = {hunt_text: -1, hike_text: -1}
    hunt_play_dict = {hunt_text: -1, play_text: -1}

    # WHEN / THEN
    assert cultureheir_x.belief_in(swim_dict)
    assert cultureheir_x.belief_in(hike_dict)
    assert cultureheir_x.belief_in(hunt_dict) is False
    assert cultureheir_x.belief_in(hunt_hike_dict)
    assert cultureheir_x.belief_in(hunt_play_dict) is False


def test_CultureHeir_belief_in_ReturnsCorrectBoolWhen_heldbeliefsEmpty():
    # GIVEN
    hike_text = ",hike"
    hike_dict = {hike_text: -1}
    cultureunit_x = cultureunit_shop()
    cultureheir_x = cultureheir_shop()
    cultureheir_x.set_heldbeliefs(
        parent_cultureheir=None, cultureunit=cultureunit_x, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text: -1}
    play_text = ",play"
    play_dict = {play_text: -1}
    assert cultureheir_x._heldbeliefs == {}
    hunt_hike_dict = {hunt_text: -1, hike_text: -1}
    hunt_play_dict = {hunt_text: -1, play_text: -1}

    # WHEN / THEN
    assert cultureheir_x.belief_in(hike_dict)
    assert cultureheir_x.belief_in(hunt_dict)
    assert cultureheir_x.belief_in(play_dict)
    assert cultureheir_x.belief_in(hunt_hike_dict)
    assert cultureheir_x.belief_in(hunt_play_dict)
