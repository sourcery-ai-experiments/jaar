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
    x_heldbeliefs = {1}

    # WHEN
    x_cultureunit = CultureUnit(_heldbeliefs=x_heldbeliefs)

    # THEN
    assert x_cultureunit
    assert x_cultureunit._heldbeliefs == x_heldbeliefs


def test_cultureunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    x_heldbeliefs = {1}

    # WHEN
    x_cultureunit = cultureunit_shop(_heldbeliefs=x_heldbeliefs)

    # THEN
    assert x_cultureunit
    assert x_cultureunit._heldbeliefs == x_heldbeliefs


def test_cultureunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    x_cultureunit = cultureunit_shop()

    # THEN
    assert x_cultureunit
    assert x_cultureunit._heldbeliefs == set()


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
    x_heldbeliefs = {bob_belief_id: bob_belief_id}
    culture_x = cultureunit_shop(_heldbeliefs=x_heldbeliefs)

    # WHEN
    obj_dict = culture_x.get_dict()

    # THEN
    assert obj_dict != None
    example_dict = {"_heldbeliefs": [bob_belief_id]}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_CultureUnit_set_heldbelief_CorrectlySets_heldbeliefs_v1():
    # GIVEN
    x_cultureunit = cultureunit_shop()
    assert len(x_cultureunit._heldbeliefs) == 0

    # WHEN
    jim_text = "Jim"
    x_cultureunit.set_heldbelief(belief_id=jim_text)

    # THEN
    assert len(x_cultureunit._heldbeliefs) == 1


def test_CultureUnit_heldbelief_exists_ReturnsCorrectObj():
    # GIVEN
    x_cultureunit = cultureunit_shop()
    jim_text = "Jim"
    assert x_cultureunit.heldbelief_exists(jim_text) is False

    # WHEN
    x_cultureunit.set_heldbelief(belief_id=jim_text)

    # THEN
    assert x_cultureunit.heldbelief_exists(jim_text)


def test_CultureUnit_del_heldbelief_CorrectlyDeletes_heldbeliefs_v1():
    # GIVEN
    x_cultureunit = cultureunit_shop()
    jim_text = "Jim"
    sue_text = "Sue"
    x_cultureunit.set_heldbelief(belief_id=jim_text)
    x_cultureunit.set_heldbelief(belief_id=sue_text)
    assert len(x_cultureunit._heldbeliefs) == 2

    # WHEN
    x_cultureunit.del_heldbelief(belief_id=sue_text)

    # THEN
    assert len(x_cultureunit._heldbeliefs) == 1


def test_CultureHeir_exists():
    # GIVEN
    x_heldbeliefs = {1}
    _owner_id_culture_x = True

    # WHEN
    culture_heir_x = CultureHeir(
        _heldbeliefs=x_heldbeliefs, _owner_id_culture=_owner_id_culture_x
    )

    # THEN
    assert culture_heir_x
    assert culture_heir_x._heldbeliefs == x_heldbeliefs
    assert culture_heir_x._owner_id_culture == _owner_id_culture_x


def test_cultureheir_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    x_heldbeliefs = {1}
    _owner_id_culture_x = "example"

    # WHEN
    culture_heir_x = cultureheir_shop(
        _heldbeliefs=x_heldbeliefs, _owner_id_culture=_owner_id_culture_x
    )

    # THEN
    assert culture_heir_x
    assert culture_heir_x._heldbeliefs == x_heldbeliefs
    assert culture_heir_x._owner_id_culture == _owner_id_culture_x


def test_CultureHeir_get_all_suff_chars_ReturnsSingleDictWithAllChars_v1():
    # GIVEN
    jim_text = "Jim"
    sue_text = "Sue"
    x_world = worldunit_shop(_owner_id=jim_text)
    x_world.add_charunit(char_id=jim_text)
    x_world.add_charunit(char_id=sue_text)

    x_heldbeliefs = {jim_text}
    culture_heir_x = cultureheir_shop(_heldbeliefs=x_heldbeliefs)

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

    x_heldbeliefs = {swim_text}
    culture_heir_x = cultureheir_shop(_heldbeliefs=x_heldbeliefs)

    # WHEN
    all_chars = culture_heir_x._get_all_suff_chars(world_beliefs=x_world._beliefs)

    # THEN
    assert len(all_chars) == 2


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_Emptyx_heldbeliefs():
    # GIVEN
    x_heldbeliefs = set()
    culture_heir_x = cultureheir_shop(_heldbeliefs=x_heldbeliefs)
    assert culture_heir_x._owner_id_culture is False

    # WHEN
    world_beliefs = set()
    culture_heir_x.set_owner_id_culture(world_beliefs=world_beliefs, world_owner_id="")

    # THEN
    assert culture_heir_x._owner_id_culture


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmptyx_heldbeliefs_v1():
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

    x_heldbeliefs = {jim_text}
    culture_heir_x = cultureheir_shop(_heldbeliefs=x_heldbeliefs)
    assert culture_heir_x._owner_id_culture is False

    # WHEN
    culture_heir_x.set_owner_id_culture(world_beliefs, world_owner_id)

    # THEN
    assert culture_heir_x._owner_id_culture


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmptyx_heldbeliefs_v2():
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

    x_heldbeliefs = {sue_text}
    culture_heir_x = cultureheir_shop(_heldbeliefs=x_heldbeliefs)
    assert culture_heir_x._owner_id_culture is False

    # WHEN
    culture_heir_x.set_owner_id_culture(world_beliefs, world_owner_id)

    # THEN
    assert culture_heir_x._owner_id_culture is False


def test_CultureHeir_set_owner_id_culture_CorrectlySetsAttribute_NonEmptyx_heldbeliefs_v3():
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

    x_heldbeliefs = {swim_text}
    culture_heir_x = cultureheir_shop(_heldbeliefs=x_heldbeliefs)
    assert culture_heir_x._owner_id_culture is False
    culture_heir_x.set_owner_id_culture(x_world._beliefs, x_world._owner_id)
    assert culture_heir_x._owner_id_culture

    # WHEN
    swim_belief.del_charlink(char_id=jim_text)
    x_world.set_beliefunit(y_beliefunit=swim_belief)
    culture_heir_x.set_owner_id_culture(x_world._beliefs, x_world._owner_id)

    # THEN
    assert culture_heir_x._owner_id_culture is False


def test_CultureHeir_set__CorrectlySetsAttribute_NonEmptyx_heldbeliefs_v3():
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

    x_heldbeliefs = {swim_text}
    culture_heir_x = cultureheir_shop(_heldbeliefs=x_heldbeliefs)
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
    x_cultureunit = cultureunit_shop()

    # WHEN
    culture_heir_x.set_heldbeliefs(
        parent_cultureheir=parent_cultureheir_empty,
        cultureunit=x_cultureunit,
        world_beliefs=None,
    )

    # THEN
    culture_heir_x._heldbeliefs = {}


def test_CultureHeir_set_heldbelief_CultureUnitNotEmpty_ParentCultureHeirIsNone():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_heldbelief(belief_id=kent_text)
    x_cultureunit.set_heldbelief(belief_id=swim_text)

    # WHEN
    culture_heir_x = cultureheir_shop()
    culture_heir_x.set_heldbeliefs(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )

    # THEN
    assert culture_heir_x._heldbeliefs == x_cultureunit._heldbeliefs


def test_CultureHeir_set_heldbelief_CultureUnitNotEmpty_ParentCultureHeirEmpty():
    # GIVEN
    kent_text = "kent"
    swim_text = ",swim"
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_heldbelief(belief_id=kent_text)
    x_cultureunit.set_heldbelief(belief_id=swim_text)

    # WHEN
    culture_heir_x = cultureheir_shop()
    parent_cultureheir_empty = cultureheir_shop()
    culture_heir_x.set_heldbeliefs(
        parent_cultureheir_empty, cultureunit=x_cultureunit, world_beliefs=None
    )

    # THEN
    assert culture_heir_x._heldbeliefs == x_cultureunit._heldbeliefs


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
    assert culture_heir_x._heldbeliefs == set()
    culture_heir_x.set_heldbeliefs(
        parent_culture_heir, cultureunit=cultureunit_empty, world_beliefs=None
    )

    # THEN
    assert len(culture_heir_x._heldbeliefs)
    assert culture_heir_x._heldbeliefs == parent_culture_heir._heldbeliefs


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
    assert culture_heir_x._heldbeliefs == set()
    culture_heir_x.set_heldbeliefs(
        parent_culture_heir, cultureunit=cultureunit_swim, world_beliefs=None
    )

    # THEN
    assert culture_heir_x._heldbeliefs == parent_culture_heir._heldbeliefs


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
    assert culture_heir_x._heldbeliefs == cultureunit_swim2._heldbeliefs
    assert len(culture_heir_x._heldbeliefs) == 1
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


def test_CultureHeir_belief_id_in_ReturnsCorrectBoolWhen_heldbeliefsNotEmpty():
    # GIVEN
    swim_text = ",swim"
    hike_text = ",hike"
    swim_dict = {swim_text}
    hike_dict = {hike_text}
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_heldbelief(belief_id=swim_text)
    x_cultureunit.set_heldbelief(belief_id=hike_text)
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_heldbeliefs(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert swim_text in x_cultureheir._heldbeliefs
    assert hike_text in x_cultureheir._heldbeliefs
    print(f"{hunt_text in x_cultureheir._heldbeliefs=}")
    assert hunt_text not in x_cultureheir._heldbeliefs
    assert play_text not in x_cultureheir._heldbeliefs
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_cultureheir.belief_in(swim_dict)
    assert x_cultureheir.belief_in(hike_dict)
    assert x_cultureheir.belief_in(hunt_dict) is False
    assert x_cultureheir.belief_in(hunt_hike_dict)
    assert x_cultureheir.belief_in(hunt_play_dict) is False


def test_CultureHeir_belief_in_ReturnsCorrectBoolWhen_heldbeliefsEmpty():
    # GIVEN
    hike_text = ",hike"
    hike_dict = {hike_text}
    x_cultureunit = cultureunit_shop()
    x_cultureheir = cultureheir_shop()
    x_cultureheir.set_heldbeliefs(
        parent_cultureheir=None, cultureunit=x_cultureunit, world_beliefs=None
    )
    hunt_text = ",hunt"
    hunt_dict = {hunt_text}
    play_text = ",play"
    play_dict = {play_text}
    assert x_cultureheir._heldbeliefs == set()
    hunt_hike_dict = {hunt_text, hike_text}
    hunt_play_dict = {hunt_text, play_text}

    # WHEN / THEN
    assert x_cultureheir.belief_in(hike_dict)
    assert x_cultureheir.belief_in(hunt_dict)
    assert x_cultureheir.belief_in(play_dict)
    assert x_cultureheir.belief_in(hunt_hike_dict)
    assert x_cultureheir.belief_in(hunt_play_dict)
