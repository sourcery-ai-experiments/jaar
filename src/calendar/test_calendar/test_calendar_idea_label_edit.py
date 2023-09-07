from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaKid
from src.calendar.examples.example_calendars import (
    get_calendar_with_4_levels_and_2requireds_2acptfacts,
)
from pytest import raises as pytest_raises
from src.calendar.required_idea import Road, AcptFactUnit
from src.calendar.road import get_global_root_label as root_label


def test_idea_label_fails_when_idea_does_not_exist():
    # GIVEN
    work_text = "work"
    work_road = f"{root_label()},{work_text}"
    swim_text = "swim"
    owner_text = "Noa"
    sx = CalendarUnit(_owner=owner_text)
    sx.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=work_text))
    sx.add_idea(walk=work_road, idea_kid=IdeaKid(_label=swim_text))

    # When/Then
    no_idea_road = Road(f"{root_label()},bees")
    with pytest_raises(Exception) as excinfo:
        sx.edit_idea_label(old_road=no_idea_road, new_label="pigeons")
    assert (
        str(excinfo.value)
        == f"Getting idea_label='bees' failed no item at '{no_idea_road}'"
    )


# when editing a idea _label it's possible that the change breaks a required.base, sufffact.need or acptfact.base or acptfact.acptfact
# fixing this quickly looks difficult. Maybe push it off
def test_where_level0_idea_label_change_breaks_idea_walk_of_child_ideas():
    # GIVEN

    work_text = "work"
    work_road = f"{root_label()},{work_text}"
    swim_text = "swim"
    swim_road = f"{root_label()},{work_text},{swim_text}"
    owner_text = "Tim"
    sx = CalendarUnit(_owner=owner_text)
    sx.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=work_text))
    sx.add_idea(walk=work_road, idea_kid=IdeaKid(_label=swim_text))
    assert sx._owner == owner_text
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
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_label()}'"
    )

    # moon = "moon"
    # sx.edit_idea_label(old_road=root_label(), new_label=moon)

    # # THEN
    # assert sx._owner == root_label()
    # assert sx._idearoot._label == root_label()
    # assert sx._idearoot._walk == ""
    # assert work_idea._walk == root_label()
    # assert swim_idea._walk == f"{root_label()},{work_text}"


def test_idea_find_replace_road_Changes_kids_scenario1():
    # GIVEN Idea with kids that will be changed

    old_person_text = "person"
    old_person_road = Road(f"{root_label()},{old_person_text}")
    bloomers_text = "bloomers"
    old_bloomers_road = Road(f"{root_label()},{old_person_text},{bloomers_text}")
    roses_text = "roses"
    old_roses_road = Road(
        f"{root_label()},{old_person_text},{bloomers_text},{roses_text}"
    )
    red_text = "red"
    old_red_road = Road(
        f"{root_label()},{old_person_text},{bloomers_text},{roses_text},{red_text}"
    )

    owner_text = "Tim"
    sx = CalendarUnit(_owner=owner_text)
    sx.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=old_person_text))
    sx.add_idea(walk=old_person_road, idea_kid=IdeaKid(_label=bloomers_text))
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
    new_person_text = "globe"
    new_person_road = Road(f"{root_label()},{new_person_text}")
    sx.edit_idea_label(old_road=old_person_road, new_label=new_person_text)

    # THEN
    assert sx._idearoot._kids.get(new_person_text) != None
    assert sx._idearoot._kids.get(old_person_text) is None

    assert r_idea_bloomers._walk == new_person_road
    assert r_idea_bloomers._kids.get(roses_text) != None

    r_idea_roses = r_idea_bloomers._kids.get(roses_text)
    new_bloomers_road = Road(f"{root_label()},{new_person_text},{bloomers_text}")
    assert r_idea_roses._walk == new_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    new_roses_road = Road(
        f"{root_label()},{new_person_text},{bloomers_text},{roses_text}"
    )
    assert r_idea_red._walk == new_roses_road


def test_calendar_edit_idea_label_Changes_acptfactunits():
    # GIVEN calendar with acptfactunits that will be changed

    person = "person"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()},{person},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_label()},{person},{bloomers_text},{roses_text}"
    old_water_text = "water"
    old_water_road = f"{root_label()},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{root_label()},{old_water_text},{rain_text}"

    owner_text = "Tim"
    sx = CalendarUnit(_owner=owner_text)
    sx.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=person))
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
    new_water_road = f"{root_label()},{new_water_text}"
    sx.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=new_water_text))
    assert sx._idearoot._acptfactunits.get(new_water_road) is None
    sx.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    assert sx._idearoot._acptfactunits.get(old_water_road) is None
    assert sx._idearoot._acptfactunits.get(new_water_road) != None
    new_water_rain_acptfactunit = sx._idearoot._acptfactunits[new_water_road]
    assert new_water_rain_acptfactunit.base == new_water_road
    new_rain_road = f"{root_label()},{new_water_text},{rain_text}"
    assert new_water_rain_acptfactunit.pick == new_rain_road

    assert sx._idearoot._acptfactunits.get(new_water_road)
    acptfactunit_obj = sx._idearoot._acptfactunits.get(new_water_road)
    # for acptfactunit_key, acptfactunit_obj in sx._idearoot._acptfactunits.items():
    #     assert acptfactunit_key == new_water_road
    assert acptfactunit_obj.base == new_water_road
    assert acptfactunit_obj.pick == new_rain_road


def test_calendar_edit_idea_label_ChangesIdeaRoot_special_road():
    # GIVEN this should never happen but it's not currently banned

    old_person_text = "person"
    old_person_road = Road(f"{root_label()},{old_person_text}")
    owner_text = "Tim"
    sx = CalendarUnit(_owner=owner_text)
    sx.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=old_person_text))
    sx.edit_idea_attr(road=root_label(), special_road=old_person_road)
    assert sx._idearoot._special_road == old_person_road

    # WHEN
    new_person_text = "globe"
    sx.edit_idea_label(old_road=old_person_road, new_label=new_person_text)

    # THEN
    new_person_road = Road(f"{root_label()},{new_person_text}")
    assert sx._idearoot._special_road == new_person_road


def test_calendar_edit_idea_label_ChangesIdeaKidN_special_road():
    person_text = "person"
    person_road = Road(f"{root_label()},{person_text}")
    old_water_text = "water"
    old_water_road = f"{root_label()},{person_text},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{root_label()},{person_text},{old_water_text},{rain_text}"
    mood_text = "mood"
    mood_road = Road(f"{root_label()},{mood_text}")

    owner_text = "Bob"
    sx = CalendarUnit(_owner=owner_text)
    sx.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=person_text))
    sx.add_idea(walk=person_road, idea_kid=IdeaKid(_label=old_water_text))
    sx.add_idea(walk=old_water_road, idea_kid=IdeaKid(_label=rain_text))
    sx.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=mood_text))

    sx.edit_idea_attr(road=mood_road, special_road=old_rain_road)
    mood_idea = sx.get_idea_kid(road=mood_road)
    assert mood_idea._special_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_rain_road = f"{root_label()},{person_text},{new_water_text},{rain_text}"
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
    assert mood_idea._special_road == new_rain_road


def test_calendar_edit_idea_label_ChangesIdeaRequiredUnitsScenario1():
    # GIVEN
    calendar_x = get_calendar_with_4_levels_and_2requireds_2acptfacts()
    old_weekday_text = "weekdays"
    old_weekday_road = f"{root_label()},{old_weekday_text}"
    wednesday_text = "Wednesday"
    old_wednesday_road = f"{root_label()},{old_weekday_text},{wednesday_text}"
    work_idea = calendar_x.get_idea_kid(f"{root_label()},work")
    usa = f"{root_label()},nation-state,USA"
    nationstate = f"{root_label()},nation-state"
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
    new_weekday_road = f"{root_label()},{new_weekday_text}"
    new_wednesday_road = f"{root_label()},{new_weekday_text},{wednesday_text}"
    assert work_idea._requiredunits.get(new_weekday_text) is None

    # WHEN
    # for key_x, required_x in work_idea._requiredunits.items():
    #     print(f"Before {key_x=} {required_x.base=}")
    print(f"BEFORE {wednesday_idea._label=}")
    print(f"BEFORE {wednesday_idea._walk=}")
    calendar_x.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
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


def test_calendar_set_owner_CorrectlyChangesBoth():
    # GIVEN
    calendar_x = get_calendar_with_4_levels_and_2requireds_2acptfacts()
    assert calendar_x._owner == "Noa"
    assert calendar_x._idearoot._label == root_label()
    # mid_label1 = "tim"
    # calendar_x.edit_idea_label(old_road=old_label, new_label=mid_label1)
    # assert calendar_x._owner == old_label
    # assert calendar_x._idearoot._label == mid_label1

    # WHEN
    new_label2 = "bob"
    calendar_x.set_owner(new_owner=new_label2)

    # THEN
    assert calendar_x._owner == new_label2
    assert calendar_x._idearoot._label == root_label()
