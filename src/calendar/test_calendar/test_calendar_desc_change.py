from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaKid
from src.calendar.examples.example_calendars import (
    get_calendar_with_4_levels_and_2requireds_2acptfacts,
)
from pytest import raises as pytest_raises
from src.calendar.required_idea import Road, AcptFactUnit
from src.calendar.road import get_global_root_desc as root_desc


def test_idea_desc_fails_when_idea_does_not_exist():
    # GIVEN
    work_text = "work"
    work_road = f"{root_desc()},{work_text}"
    swim_text = "swim"
    owner_text = "Noa"
    sx = CalendarUnit(_owner=owner_text)
    sx.add_idea(walk=root_desc(), idea_kid=IdeaKid(_desc=work_text))
    sx.add_idea(walk=work_road, idea_kid=IdeaKid(_desc=swim_text))

    # When/Then
    no_idea_road = Road(f"{root_desc()},bees")
    with pytest_raises(Exception) as excinfo:
        sx.edit_idea_desc(old_road=no_idea_road, new_desc="pigeons")
    assert (
        str(excinfo.value)
        == f"Getting idea_desc='bees' failed no item at '{no_idea_road}'"
    )


# when editing a idea description it's possible that the change breaks a required.base, sufffact.need or acptfact.base or acptfact.acptfact
# fixing this quickly looks difficult. Maybe push it off
def test_where_level0_idea_desc_change_breaks_idea_walk_of_child_ideas():
    # GIVEN

    work_text = "work"
    work_road = f"{root_desc()},{work_text}"
    swim_text = "swim"
    swim_road = f"{root_desc()},{work_text},{swim_text}"
    sx = CalendarUnit(_owner=root_desc())
    sx.add_idea(walk=root_desc(), idea_kid=IdeaKid(_desc=work_text))
    sx.add_idea(walk=work_road, idea_kid=IdeaKid(_desc=swim_text))
    assert sx._owner == root_desc()
    assert sx._idearoot._desc == root_desc()
    work_idea = sx.get_idea_kid(road=work_road)
    assert work_idea._walk == root_desc()
    swim_idea = sx.get_idea_kid(road=swim_road)
    assert swim_idea._walk == work_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        sx.edit_idea_desc(old_road=root_desc(), new_desc=moon_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_desc()}'"
    )

    # moon = "moon"
    # sx.edit_idea_desc(old_road=root_desc(), new_desc=moon)

    # # THEN
    # assert sx._owner == root_desc()
    # assert sx._idearoot._desc == root_desc()
    # assert sx._idearoot._walk == ""
    # assert work_idea._walk == root_desc()
    # assert swim_idea._walk == f"{root_desc()},{work_text}"


def test_idea_find_replace_road_Changes_kids_scenario1():
    # GIVEN Idea with kids that will be changed

    old_person_text = "person"
    old_person_road = Road(f"{root_desc()},{old_person_text}")
    bloomers_text = "bloomers"
    old_bloomers_road = Road(f"{root_desc()},{old_person_text},{bloomers_text}")
    roses_text = "roses"
    old_roses_road = Road(
        f"{root_desc()},{old_person_text},{bloomers_text},{roses_text}"
    )
    red_text = "red"
    old_red_road = Road(
        f"{root_desc()},{old_person_text},{bloomers_text},{roses_text},{red_text}"
    )

    sx = CalendarUnit(_owner=root_desc())
    sx.add_idea(walk=root_desc(), idea_kid=IdeaKid(_desc=old_person_text))
    sx.add_idea(walk=old_person_road, idea_kid=IdeaKid(_desc=bloomers_text))
    sx.add_idea(walk=old_bloomers_road, idea_kid=IdeaKid(_desc=roses_text))
    sx.add_idea(walk=old_roses_road, idea_kid=IdeaKid(_desc=red_text))
    r_idea_roses = sx.get_idea_kid(old_roses_road)
    r_idea_bloomers = sx.get_idea_kid(old_bloomers_road)

    assert r_idea_bloomers._kids.get(roses_text) != None
    assert r_idea_roses._walk == old_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    assert r_idea_red._walk == old_roses_road

    # WHEN
    new_person_text = "globe"
    new_person_road = Road(f"{root_desc()},{new_person_text}")
    sx.edit_idea_desc(old_road=old_person_road, new_desc=new_person_text)

    # THEN
    assert sx._idearoot._kids.get(new_person_text) != None
    assert sx._idearoot._kids.get(old_person_text) is None

    assert r_idea_bloomers._walk == new_person_road
    assert r_idea_bloomers._kids.get(roses_text) != None

    r_idea_roses = r_idea_bloomers._kids.get(roses_text)
    new_bloomers_road = Road(f"{root_desc()},{new_person_text},{bloomers_text}")
    assert r_idea_roses._walk == new_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    new_roses_road = Road(
        f"{root_desc()},{new_person_text},{bloomers_text},{roses_text}"
    )
    assert r_idea_red._walk == new_roses_road


def test_calendar_edit_idea_desc_Changes_acptfactunits():
    # GIVEN calendar with acptfactunits that will be changed

    person = "person"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_desc()},{person},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_desc()},{person},{bloomers_text},{roses_text}"
    old_water_text = "water"
    old_water_road = f"{root_desc()},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{root_desc()},{old_water_text},{rain_text}"

    sx = CalendarUnit(_owner=root_desc())
    sx.add_idea(walk=root_desc(), idea_kid=IdeaKid(_desc=person))
    sx.add_idea(walk=bloomers_road, idea_kid=IdeaKid(_desc=roses_text))
    sx.add_idea(walk=old_water_road, idea_kid=IdeaKid(_desc=rain_text))
    sx.set_acptfact(base=old_water_road, pick=old_rain_road)

    idea_x = sx.get_idea_kid(road=roses_road)
    assert sx._idearoot._acptfactunits[old_water_road] != None
    old_water_rain_acptfactunit = sx._idearoot._acptfactunits[old_water_road]
    assert old_water_rain_acptfactunit.base == old_water_road
    assert old_water_rain_acptfactunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{root_desc()},{new_water_text}"
    sx.add_idea(walk=root_desc(), idea_kid=IdeaKid(_desc=new_water_text))
    assert sx._idearoot._acptfactunits.get(new_water_road) is None
    sx.edit_idea_desc(old_road=old_water_road, new_desc=new_water_text)

    # THEN
    assert sx._idearoot._acptfactunits.get(old_water_road) is None
    assert sx._idearoot._acptfactunits.get(new_water_road) != None
    new_water_rain_acptfactunit = sx._idearoot._acptfactunits[new_water_road]
    assert new_water_rain_acptfactunit.base == new_water_road
    new_rain_road = f"{root_desc()},{new_water_text},{rain_text}"
    assert new_water_rain_acptfactunit.pick == new_rain_road

    assert sx._idearoot._acptfactunits.get(new_water_road)
    acptfactunit_obj = sx._idearoot._acptfactunits.get(new_water_road)
    # for acptfactunit_key, acptfactunit_obj in sx._idearoot._acptfactunits.items():
    #     assert acptfactunit_key == new_water_road
    assert acptfactunit_obj.base == new_water_road
    assert acptfactunit_obj.pick == new_rain_road


def test_calendar_edit_idea_desc_ChangesIdeaRoot_special_road():
    # GIVEN this should never happen but it's not currently banned

    old_person_text = "person"
    old_person_road = Road(f"{root_desc()},{old_person_text}")
    sx = CalendarUnit(_owner=root_desc())
    sx.add_idea(walk=root_desc(), idea_kid=IdeaKid(_desc=old_person_text))
    sx.edit_idea_attr(road=root_desc(), special_road=old_person_road)
    assert sx._idearoot._special_road == old_person_road

    # WHEN
    new_person_text = "globe"
    sx.edit_idea_desc(old_road=old_person_road, new_desc=new_person_text)

    # THEN
    new_person_road = Road(f"{root_desc()},{new_person_text}")
    assert sx._idearoot._special_road == new_person_road


def test_calendar_edit_idea_desc_ChangesIdeaKidN_special_road():
    person_text = "person"
    person_road = Road(f"{root_desc()},{person_text}")
    old_water_text = "water"
    old_water_road = f"{root_desc()},{person_text},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{root_desc()},{person_text},{old_water_text},{rain_text}"
    mood_text = "mood"
    mood_road = Road(f"{root_desc()},{mood_text}")

    owner_text = "Bob"
    sx = CalendarUnit(_owner=owner_text)
    sx.add_idea(walk=root_desc(), idea_kid=IdeaKid(_desc=person_text))
    sx.add_idea(walk=person_road, idea_kid=IdeaKid(_desc=old_water_text))
    sx.add_idea(walk=old_water_road, idea_kid=IdeaKid(_desc=rain_text))
    sx.add_idea(walk=root_desc(), idea_kid=IdeaKid(_desc=mood_text))

    sx.edit_idea_attr(road=mood_road, special_road=old_rain_road)
    mood_idea = sx.get_idea_kid(road=mood_road)
    assert mood_idea._special_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_rain_road = f"{root_desc()},{person_text},{new_water_text},{rain_text}"
    sx.edit_idea_desc(old_road=old_water_road, new_desc=new_water_text)

    # THEN
    # for idea_x in sx._idearoot._kids.values():
    #     print(f"{idea_x._walk=} {idea_x._desc=}")
    #     idea_x.set_kids_empty_if_null()
    #     for idea_y in idea_x._kids.values():
    #         print(f"{idea_y._walk=} {idea_y._desc=}")
    #         idea_y.set_kids_empty_if_null()
    #         for idea_z in idea_y._kids.values():
    #             print(f"{idea_z._walk=} {idea_z._desc=}")
    assert mood_idea._special_road == new_rain_road


def test_calendar_owner_change_ChangesIdeaRequiredUnitsScenario1():
    # GIVEN
    calendar_x = get_calendar_with_4_levels_and_2requireds_2acptfacts()
    old_weekday_text = "weekdays"
    old_weekday_road = f"{root_desc()},{old_weekday_text}"
    wednesday_text = "Wednesday"
    old_wednesday_road = f"{root_desc()},{old_weekday_text},{wednesday_text}"
    work_idea = calendar_x.get_idea_kid(f"{root_desc()},work")
    usa = f"{root_desc()},nation-state,USA"
    nationstate = f"{root_desc()},nation-state"
    # work_wk_required = RequiredUnit(base=weekday, sufffacts={wed_sufffact.need: wed_sufffact})
    # nation_required = RequiredUnit(base=nationstate, sufffacts={usa_sufffact.need: usa_sufffact})
    assert len(work_idea._requiredunits) == 2
    assert work_idea._requiredunits.get(old_weekday_road) != None
    wednesday_idea = calendar_x.get_idea_kid(old_weekday_road)
    work_weekday_required = work_idea._requiredunits.get(old_weekday_road)
    assert work_weekday_required.sufffacts.get(old_wednesday_road) != None
    assert (
        work_weekday_required.sufffacts.get(old_wednesday_road).need
        == old_wednesday_road
    )
    new_weekday_text = "days of week"
    new_weekday_road = f"{root_desc()},{new_weekday_text}"
    new_wednesday_road = f"{root_desc()},{new_weekday_text},{wednesday_text}"
    assert work_idea._requiredunits.get(new_weekday_text) is None

    # WHEN
    # for key_x, required_x in work_idea._requiredunits.items():
    #     print(f"Before {key_x=} {required_x.base=}")
    print(f"BEFORE {wednesday_idea._desc=}")
    print(f"BEFORE {wednesday_idea._walk=}")
    calendar_x.edit_idea_desc(old_road=old_weekday_road, new_desc=new_weekday_text)
    # for key_x, required_x in work_idea._requiredunits.items():
    #     print(f"AFTER {key_x=} {required_x.base=}")
    print(f"AFTER {wednesday_idea._desc=}")
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


def test_calendar_calendar_owner_edit_CorrectlyChangesBoth():
    # GIVEN
    calendar_x = get_calendar_with_4_levels_and_2requireds_2acptfacts()
    assert calendar_x._owner == "Noa"
    assert calendar_x._idearoot._desc == root_desc()
    # mid_desc1 = "tim"
    # calendar_x.edit_idea_desc(old_road=old_desc, new_desc=mid_desc1)
    # assert calendar_x._owner == old_desc
    # assert calendar_x._idearoot._desc == mid_desc1

    # WHEN
    new_desc2 = "bob"
    calendar_x.calendar_owner_edit(new_owner=new_desc2)

    # THEN
    assert calendar_x._owner == new_desc2
    assert calendar_x._idearoot._desc == root_desc()
