from src.contract.contract import ContractUnit
from src.contract.idea import IdeaKid
from src.contract.examples.example_contracts import (
    get_contract_with_4_levels_and_2requireds_2acptfacts,
)
from pytest import raises as pytest_raises
from src.contract.required_idea import Road, AcptFactUnit
from src.contract.road import get_default_economy_root_label as root_label


def test_idea_label_fails_when_idea_does_not_exist():
    # GIVEN
    owner_text = "Noa"
    sx = ContractUnit(_owner=owner_text)

    work_text = "work"
    work_road = f"{sx._economy_tag},{work_text}"
    swim_text = "swim"
    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=work_text))
    sx.add_idea(walk=work_road, idea_kid=IdeaKid(_label=swim_text))

    # When/Then
    no_idea_road = Road(f"{sx._economy_tag},bees")
    with pytest_raises(Exception) as excinfo:
        sx.edit_idea_label(old_road=no_idea_road, new_label="pigeons")
    assert (
        str(excinfo.value)
        == f"Getting idea_label='bees' failed no item at '{no_idea_road}'"
    )


def test_Contract_level0_idea_edit_idea_label_RaisesError_economy_tag_IsNone():
    # GIVEN
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)

    work_text = "work"
    work_road = f"{sx._economy_tag},{work_text}"
    swim_text = "swim"
    swim_road = f"{sx._economy_tag},{work_text},{swim_text}"
    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=work_text))
    sx.add_idea(walk=work_road, idea_kid=IdeaKid(_label=swim_text))
    assert sx._owner == owner_text
    assert sx._economy_tag == sx._economy_tag
    assert sx._idearoot._label == sx._economy_tag
    work_idea = sx.get_idea_kid(road=work_road)
    assert work_idea._walk == sx._economy_tag
    swim_idea = sx.get_idea_kid(road=swim_road)
    assert swim_idea._walk == work_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        sx.edit_idea_label(old_road=sx._economy_tag, new_label=moon_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{sx._economy_tag}'"
    )


# when editing a idea _label it's possible that the change breaks a required.base, sufffact.need or acptfact.base or acptfact.acptfact
# fixing this quickly looks difficult. Maybe push it off
def test_Contract_level0_idea_edit_idea_label_RaisesError_economy_tag_IsDifferent():
    # GIVEN
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    work_text = "work"
    work_road = f"{sx._economy_tag},{work_text}"
    swim_text = "swim"
    swim_road = f"{sx._economy_tag},{work_text},{swim_text}"
    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=work_text))
    sx.add_idea(walk=work_road, idea_kid=IdeaKid(_label=swim_text))
    sun_text = "sun"
    sx._economy_tag = sun_text
    assert sx._owner == owner_text
    assert sx._economy_tag == sun_text
    assert sx._idearoot._label == root_label()
    work_idea = sx.get_idea_kid(road=work_road)
    assert work_idea._walk == root_label()
    swim_idea = sx.get_idea_kid(road=swim_road)
    assert swim_idea._walk == work_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        sx.edit_idea_label(old_road=root_label(), new_label=moon_text)
    assert (
        str(excinfo.value) == f"Cannot set idearoot to string other than '{sun_text}'"
    )


def test_contract_set_economy_tag_CorrectlySetsAttr():
    # GIVEN
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    work_text = "work"
    old_work_road = f"{sx._economy_tag},{work_text}"
    swim_text = "swim"
    old_swim_road = f"{old_work_road},{swim_text}"
    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=work_text))
    sx.add_idea(walk=old_work_road, idea_kid=IdeaKid(_label=swim_text))
    assert sx._owner == owner_text
    assert sx._idearoot._label == sx._economy_tag
    work_idea = sx.get_idea_kid(road=old_work_road)
    assert work_idea._walk == sx._economy_tag
    swim_idea = sx.get_idea_kid(road=old_swim_road)
    assert swim_idea._walk == old_work_road
    assert sx._economy_tag == sx._economy_tag

    # WHEN
    economy_tag_text = "Sun"
    sx.set_economy_tag(economy_tag=economy_tag_text)

    # THEN
    new_work_road = f"{economy_tag_text},{work_text}"
    swim_text = "swim"
    new_swim_road = f"{new_work_road},{swim_text}"
    assert sx._economy_tag == economy_tag_text
    assert sx._idearoot._label == economy_tag_text
    work_idea = sx.get_idea_kid(road=new_work_road)
    assert work_idea._walk == economy_tag_text
    swim_idea = sx.get_idea_kid(road=new_swim_road)
    assert swim_idea._walk == new_work_road


def test_idea_find_replace_road_Changes_kids_scenario1():
    # GIVEN Idea with kids that will be changed
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)

    old_owner_text = "owner"
    old_owner_road = Road(f"{sx._economy_tag},{old_owner_text}")
    bloomers_text = "bloomers"
    old_bloomers_road = Road(f"{sx._economy_tag},{old_owner_text},{bloomers_text}")
    roses_text = "roses"
    old_roses_road = Road(
        f"{sx._economy_tag},{old_owner_text},{bloomers_text},{roses_text}"
    )
    red_text = "red"
    old_red_road = Road(
        f"{sx._economy_tag},{old_owner_text},{bloomers_text},{roses_text},{red_text}"
    )

    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=old_owner_text))
    sx.add_idea(walk=old_owner_road, idea_kid=IdeaKid(_label=bloomers_text))
    sx.add_idea(walk=old_bloomers_road, idea_kid=IdeaKid(_label=roses_text))
    sx.add_idea(walk=old_roses_road, idea_kid=IdeaKid(_label=red_text))
    r_idea_roses = sx.get_idea_kid(old_roses_road)
    r_idea_bloomers = sx.get_idea_kid(old_bloomers_road)

    assert r_idea_bloomers._kids.get(roses_text) != None
    assert r_idea_roses._walk == old_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    assert r_idea_red._walk == old_roses_road

    # WHEN
    new_owner_text = "globe"
    new_owner_road = Road(f"{sx._economy_tag},{new_owner_text}")
    sx.edit_idea_label(old_road=old_owner_road, new_label=new_owner_text)

    # THEN
    assert sx._idearoot._kids.get(new_owner_text) != None
    assert sx._idearoot._kids.get(old_owner_text) is None

    assert r_idea_bloomers._walk == new_owner_road
    assert r_idea_bloomers._kids.get(roses_text) != None

    r_idea_roses = r_idea_bloomers._kids.get(roses_text)
    new_bloomers_road = Road(f"{sx._economy_tag},{new_owner_text},{bloomers_text}")
    assert r_idea_roses._walk == new_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    new_roses_road = Road(
        f"{sx._economy_tag},{new_owner_text},{bloomers_text},{roses_text}"
    )
    assert r_idea_red._walk == new_roses_road


def test_contract_edit_idea_label_Changes_acptfactunits():
    # GIVEN contract with acptfactunits that will be changed
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)

    owner = "owner"
    bloomers_text = "bloomers"
    bloomers_road = f"{sx._economy_tag},{owner},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{sx._economy_tag},{owner},{bloomers_text},{roses_text}"
    old_water_text = "water"
    old_water_road = f"{sx._economy_tag},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{sx._economy_tag},{old_water_text},{rain_text}"

    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=owner))
    sx.add_idea(walk=bloomers_road, idea_kid=IdeaKid(_label=roses_text))
    sx.add_idea(walk=old_water_road, idea_kid=IdeaKid(_label=rain_text))
    sx.set_acptfact(base=old_water_road, pick=old_rain_road)

    idea_x = sx.get_idea_kid(road=roses_road)
    assert sx._idearoot._acptfactunits[old_water_road] != None
    old_water_rain_acptfactunit = sx._idearoot._acptfactunits[old_water_road]
    assert old_water_rain_acptfactunit.base == old_water_road
    assert old_water_rain_acptfactunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{sx._economy_tag},{new_water_text}"
    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=new_water_text))
    assert sx._idearoot._acptfactunits.get(new_water_road) is None
    sx.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    assert sx._idearoot._acptfactunits.get(old_water_road) is None
    assert sx._idearoot._acptfactunits.get(new_water_road) != None
    new_water_rain_acptfactunit = sx._idearoot._acptfactunits[new_water_road]
    assert new_water_rain_acptfactunit.base == new_water_road
    new_rain_road = f"{sx._economy_tag},{new_water_text},{rain_text}"
    assert new_water_rain_acptfactunit.pick == new_rain_road

    assert sx._idearoot._acptfactunits.get(new_water_road)
    acptfactunit_obj = sx._idearoot._acptfactunits.get(new_water_road)
    # for acptfactunit_key, acptfactunit_obj in sx._idearoot._acptfactunits.items():
    #     assert acptfactunit_key == new_water_road
    assert acptfactunit_obj.base == new_water_road
    assert acptfactunit_obj.pick == new_rain_road


def test_contract_edit_idea_label_ChangesIdeaRoot_range_source_road():
    # GIVEN this should never happen but it's not currently banned
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)

    old_owner_text = "owner"
    old_owner_road = Road(f"{sx._economy_tag},{old_owner_text}")
    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=old_owner_text))
    sx.edit_idea_attr(road=sx._economy_tag, range_source_road=old_owner_road)
    assert sx._idearoot._range_source_road == old_owner_road

    # WHEN
    new_owner_text = "globe"
    sx.edit_idea_label(old_road=old_owner_road, new_label=new_owner_text)

    # THEN
    new_owner_road = Road(f"{sx._economy_tag},{new_owner_text}")
    assert sx._idearoot._range_source_road == new_owner_road


def test_contract_edit_idea_label_ChangesIdeaKidN_range_source_road():
    owner_text = "Bob"
    sx = ContractUnit(_owner=owner_text)

    owner_text = "owner"
    owner_road = Road(f"{sx._economy_tag},{owner_text}")
    old_water_text = "water"
    old_water_road = f"{sx._economy_tag},{owner_text},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{sx._economy_tag},{owner_text},{old_water_text},{rain_text}"
    mood_text = "mood"
    mood_road = Road(f"{sx._economy_tag},{mood_text}")
    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=owner_text))
    sx.add_idea(walk=owner_road, idea_kid=IdeaKid(_label=old_water_text))
    sx.add_idea(walk=old_water_road, idea_kid=IdeaKid(_label=rain_text))
    sx.add_idea(walk=sx._economy_tag, idea_kid=IdeaKid(_label=mood_text))

    sx.edit_idea_attr(road=mood_road, range_source_road=old_rain_road)
    mood_idea = sx.get_idea_kid(road=mood_road)
    assert mood_idea._range_source_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_rain_road = f"{sx._economy_tag},{owner_text},{new_water_text},{rain_text}"
    sx.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    # for idea_x in sx._idearoot._kids.values():
    #     print(f"{idea_x._walk=} {idea_x._label=}")
    #     idea_x.set_kids_empty_if_null()
    #     for idea_y in idea_x._kids.values():
    #         print(f"{idea_y._walk=} {idea_y._label=}")
    #         idea_y.set_kids_empty_if_null()
    #         for idea_z in idea_y._kids.values():
    #             print(f"{idea_z._walk=} {idea_z._label=}")
    assert old_rain_road != new_rain_road
    assert mood_idea._range_source_road == new_rain_road


def test_contract_edit_idea_label_ChangesIdeaRequiredUnitsScenario1():
    # GIVEN
    sx = get_contract_with_4_levels_and_2requireds_2acptfacts()
    old_weekday_text = "weekdays"
    old_weekday_road = f"{sx._economy_tag},{old_weekday_text}"
    wednesday_text = "Wednesday"
    old_wednesday_road = f"{sx._economy_tag},{old_weekday_text},{wednesday_text}"
    work_idea = sx.get_idea_kid(f"{sx._economy_tag},work")
    usa = f"{sx._economy_tag},nation-state,USA"
    nationstate = f"{sx._economy_tag},nation-state"
    # work_wk_required = RequiredUnit(base=weekday, sufffacts={wed_sufffact.need: wed_sufffact})
    # nation_required = RequiredUnit(base=nationstate, sufffacts={usa_sufffact.need: usa_sufffact})
    assert len(work_idea._requiredunits) == 2
    assert work_idea._requiredunits.get(old_weekday_road) != None
    wednesday_idea = sx.get_idea_kid(old_weekday_road)
    work_weekday_required = work_idea._requiredunits.get(old_weekday_road)
    assert work_weekday_required.sufffacts.get(old_wednesday_road) != None
    assert (
        work_weekday_required.sufffacts.get(old_wednesday_road).need
        == old_wednesday_road
    )
    new_weekday_text = "days of week"
    new_weekday_road = f"{sx._economy_tag},{new_weekday_text}"
    new_wednesday_road = f"{sx._economy_tag},{new_weekday_text},{wednesday_text}"
    assert work_idea._requiredunits.get(new_weekday_text) is None

    # WHEN
    # for key_x, required_x in work_idea._requiredunits.items():
    #     print(f"Before {key_x=} {required_x.base=}")
    print(f"BEFORE {wednesday_idea._label=}")
    print(f"BEFORE {wednesday_idea._walk=}")
    sx.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
    # for key_x, required_x in work_idea._requiredunits.items():
    #     print(f"AFTER {key_x=} {required_x.base=}")
    print(f"AFTER {wednesday_idea._label=}")
    print(f"AFTER {wednesday_idea._walk=}")

    # THEN
    assert work_idea._requiredunits.get(new_weekday_road) != None
    assert work_idea._requiredunits.get(old_weekday_road) is None
    work_weekday_required = work_idea._requiredunits.get(new_weekday_road)
    assert work_weekday_required.sufffacts.get(new_wednesday_road) != None
    assert (
        work_weekday_required.sufffacts.get(new_wednesday_road).need
        == new_wednesday_road
    )
    assert len(work_idea._requiredunits) == 2


def test_contract_set_owner_CorrectlyChangesBoth():
    # GIVEN
    sx = get_contract_with_4_levels_and_2requireds_2acptfacts()
    assert sx._owner == "Noa"
    assert sx._idearoot._label == sx._economy_tag
    # mid_label1 = "tim"
    # sx.edit_idea_label(old_road=old_label, new_label=mid_label1)
    # assert sx._owner == old_label
    # assert sx._idearoot._label == mid_label1

    # WHEN
    new_label2 = "bob"
    sx.set_owner(new_owner=new_label2)

    # THEN
    assert sx._owner == new_label2
    assert sx._idearoot._label == sx._economy_tag
