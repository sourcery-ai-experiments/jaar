from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideacore_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels_and_2requireds_2acptfacts,
)
from pytest import raises as pytest_raises
from src.agenda.required_idea import Road, AcptFactUnit
from src.agenda.road import get_default_culture_root_label as root_label


def test_idea_label_fails_when_idea_does_not_exist():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)

    work_text = "work"
    work_road = f"{x_agenda._culture_title},{work_text}"
    swim_text = "swim"
    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=work_text)
    )
    x_agenda.add_idea(pad=work_road, idea_kid=ideacore_shop(_label=swim_text))

    # When/Then
    no_idea_road = Road(f"{x_agenda._culture_title},bees")
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_label(old_road=no_idea_road, new_label="pigeons")
    assert (
        str(excinfo.value)
        == f"Getting idea_label='bees' failed no item at '{no_idea_road}'"
    )


def test_Agenda_level0_idea_edit_idea_label_RaisesError_culture_title_IsNone():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    work_text = "work"
    work_road = f"{x_agenda._culture_title},{work_text}"
    swim_text = "swim"
    swim_road = f"{x_agenda._culture_title},{work_text},{swim_text}"
    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=work_text)
    )
    x_agenda.add_idea(pad=work_road, idea_kid=ideacore_shop(_label=swim_text))
    assert x_agenda._healer == healer_text
    assert x_agenda._culture_title == x_agenda._culture_title
    assert x_agenda._idearoot._label == x_agenda._culture_title
    work_idea = x_agenda.get_idea_kid(road=work_road)
    assert work_idea._pad == x_agenda._culture_title
    swim_idea = x_agenda.get_idea_kid(road=swim_road)
    assert swim_idea._pad == work_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        x_agenda.edit_idea_label(old_road=x_agenda._culture_title, new_label=moon_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{x_agenda._culture_title}'"
    )


def test_Agenda_level0_idea_edit_idea_label_RaisesError_culture_title_IsDifferent():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)
    work_text = "work"
    work_road = f"{x_agenda._culture_title},{work_text}"
    swim_text = "swim"
    swim_road = f"{x_agenda._culture_title},{work_text},{swim_text}"
    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=work_text)
    )
    x_agenda.add_idea(pad=work_road, idea_kid=ideacore_shop(_label=swim_text))
    sun_text = "sun"
    x_agenda._culture_title = sun_text
    assert x_agenda._healer == healer_text
    assert x_agenda._culture_title == sun_text
    assert x_agenda._idearoot._label == root_label()
    work_idea = x_agenda.get_idea_kid(road=work_road)
    assert work_idea._pad == root_label()
    swim_idea = x_agenda.get_idea_kid(road=swim_road)
    assert swim_idea._pad == work_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        x_agenda.edit_idea_label(old_road=root_label(), new_label=moon_text)
    assert (
        str(excinfo.value) == f"Cannot set idearoot to string other than '{sun_text}'"
    )


def test_agenda_set_culture_title_CorrectlySetsAttr():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)
    work_text = "work"
    old_work_road = f"{x_agenda._culture_title},{work_text}"
    swim_text = "swim"
    old_swim_road = f"{old_work_road},{swim_text}"
    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=work_text)
    )
    x_agenda.add_idea(pad=old_work_road, idea_kid=ideacore_shop(_label=swim_text))
    assert x_agenda._healer == healer_text
    assert x_agenda._idearoot._label == x_agenda._culture_title
    work_idea = x_agenda.get_idea_kid(road=old_work_road)
    assert work_idea._pad == x_agenda._culture_title
    swim_idea = x_agenda.get_idea_kid(road=old_swim_road)
    assert swim_idea._pad == old_work_road
    assert x_agenda._culture_title == x_agenda._culture_title

    # WHEN
    culture_title_text = "Sun"
    x_agenda.set_culture_title(culture_title=culture_title_text)

    # THEN
    new_work_road = f"{culture_title_text},{work_text}"
    swim_text = "swim"
    new_swim_road = f"{new_work_road},{swim_text}"
    assert x_agenda._culture_title == culture_title_text
    assert x_agenda._idearoot._label == culture_title_text
    work_idea = x_agenda.get_idea_kid(road=new_work_road)
    assert work_idea._pad == culture_title_text
    swim_idea = x_agenda.get_idea_kid(road=new_swim_road)
    assert swim_idea._pad == new_work_road


def test_idea_find_replace_road_Changes_kids_scenario1():
    # GIVEN Idea with kids that will be changed
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    old_healer_text = "healer"
    old_healer_road = Road(f"{x_agenda._culture_title},{old_healer_text}")
    bloomers_text = "bloomers"
    old_bloomers_road = Road(
        f"{x_agenda._culture_title},{old_healer_text},{bloomers_text}"
    )
    roses_text = "roses"
    old_roses_road = Road(
        f"{x_agenda._culture_title},{old_healer_text},{bloomers_text},{roses_text}"
    )
    red_text = "red"
    old_red_road = Road(
        f"{x_agenda._culture_title},{old_healer_text},{bloomers_text},{roses_text},{red_text}"
    )

    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=old_healer_text)
    )
    x_agenda.add_idea(pad=old_healer_road, idea_kid=ideacore_shop(_label=bloomers_text))
    x_agenda.add_idea(pad=old_bloomers_road, idea_kid=ideacore_shop(_label=roses_text))
    x_agenda.add_idea(pad=old_roses_road, idea_kid=ideacore_shop(_label=red_text))
    r_idea_roses = x_agenda.get_idea_kid(old_roses_road)
    r_idea_bloomers = x_agenda.get_idea_kid(old_bloomers_road)

    assert r_idea_bloomers._kids.get(roses_text) != None
    assert r_idea_roses._pad == old_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    assert r_idea_red._pad == old_roses_road

    # WHEN
    new_healer_text = "globe"
    new_healer_road = Road(f"{x_agenda._culture_title},{new_healer_text}")
    x_agenda.edit_idea_label(old_road=old_healer_road, new_label=new_healer_text)

    # THEN
    assert x_agenda._idearoot._kids.get(new_healer_text) != None
    assert x_agenda._idearoot._kids.get(old_healer_text) is None

    assert r_idea_bloomers._pad == new_healer_road
    assert r_idea_bloomers._kids.get(roses_text) != None

    r_idea_roses = r_idea_bloomers._kids.get(roses_text)
    new_bloomers_road = Road(
        f"{x_agenda._culture_title},{new_healer_text},{bloomers_text}"
    )
    assert r_idea_roses._pad == new_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    new_roses_road = Road(
        f"{x_agenda._culture_title},{new_healer_text},{bloomers_text},{roses_text}"
    )
    assert r_idea_red._pad == new_roses_road


def test_agenda_edit_idea_label_Changes_acptfactunits():
    # GIVEN agenda with acptfactunits that will be changed
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    healer = "healer"
    bloomers_text = "bloomers"
    bloomers_road = f"{x_agenda._culture_title},{healer},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{x_agenda._culture_title},{healer},{bloomers_text},{roses_text}"
    old_water_text = "water"
    old_water_road = f"{x_agenda._culture_title},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{x_agenda._culture_title},{old_water_text},{rain_text}"

    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=healer)
    )
    x_agenda.add_idea(pad=bloomers_road, idea_kid=ideacore_shop(_label=roses_text))
    x_agenda.add_idea(pad=old_water_road, idea_kid=ideacore_shop(_label=rain_text))
    x_agenda.set_acptfact(base=old_water_road, pick=old_rain_road)

    idea_x = x_agenda.get_idea_kid(road=roses_road)
    assert x_agenda._idearoot._acptfactunits[old_water_road] != None
    old_water_rain_acptfactunit = x_agenda._idearoot._acptfactunits[old_water_road]
    assert old_water_rain_acptfactunit.base == old_water_road
    assert old_water_rain_acptfactunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{x_agenda._culture_title},{new_water_text}"
    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=new_water_text)
    )
    assert x_agenda._idearoot._acptfactunits.get(new_water_road) is None
    x_agenda.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    assert x_agenda._idearoot._acptfactunits.get(old_water_road) is None
    assert x_agenda._idearoot._acptfactunits.get(new_water_road) != None
    new_water_rain_acptfactunit = x_agenda._idearoot._acptfactunits[new_water_road]
    assert new_water_rain_acptfactunit.base == new_water_road
    new_rain_road = f"{x_agenda._culture_title},{new_water_text},{rain_text}"
    assert new_water_rain_acptfactunit.pick == new_rain_road

    assert x_agenda._idearoot._acptfactunits.get(new_water_road)
    acptfactunit_obj = x_agenda._idearoot._acptfactunits.get(new_water_road)
    # for acptfactunit_key, acptfactunit_obj in x_agenda._idearoot._acptfactunits.items():
    #     assert acptfactunit_key == new_water_road
    assert acptfactunit_obj.base == new_water_road
    assert acptfactunit_obj.pick == new_rain_road


def test_agenda_edit_idea_label_ChangesIdeaRoot_range_source_road():
    # GIVEN this should never happen but it's not currently banned
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    old_healer_text = "healer"
    old_healer_road = Road(f"{x_agenda._culture_title},{old_healer_text}")
    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=old_healer_text)
    )
    x_agenda.edit_idea_attr(
        road=x_agenda._culture_title, range_source_road=old_healer_road
    )
    assert x_agenda._idearoot._range_source_road == old_healer_road

    # WHEN
    new_healer_text = "globe"
    x_agenda.edit_idea_label(old_road=old_healer_road, new_label=new_healer_text)

    # THEN
    new_healer_road = Road(f"{x_agenda._culture_title},{new_healer_text}")
    assert x_agenda._idearoot._range_source_road == new_healer_road


def test_agenda_edit_idea_label_ChangesIdeaKidN_range_source_road():
    healer_text = "Bob"
    x_agenda = agendaunit_shop(_healer=healer_text)

    healer_text = "healer"
    healer_road = Road(f"{x_agenda._culture_title},{healer_text}")
    old_water_text = "water"
    old_water_road = f"{x_agenda._culture_title},{healer_text},{old_water_text}"
    rain_text = "rain"
    old_rain_road = (
        f"{x_agenda._culture_title},{healer_text},{old_water_text},{rain_text}"
    )
    mood_text = "mood"
    mood_road = Road(f"{x_agenda._culture_title},{mood_text}")
    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=healer_text)
    )
    x_agenda.add_idea(pad=healer_road, idea_kid=ideacore_shop(_label=old_water_text))
    x_agenda.add_idea(pad=old_water_road, idea_kid=ideacore_shop(_label=rain_text))
    x_agenda.add_idea(
        pad=x_agenda._culture_title, idea_kid=ideacore_shop(_label=mood_text)
    )

    x_agenda.edit_idea_attr(road=mood_road, range_source_road=old_rain_road)
    mood_idea = x_agenda.get_idea_kid(road=mood_road)
    assert mood_idea._range_source_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_rain_road = (
        f"{x_agenda._culture_title},{healer_text},{new_water_text},{rain_text}"
    )
    x_agenda.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    # for idea_x in x_agenda._idearoot._kids.values():
    #     print(f"{idea_x._pad=} {idea_x._label=}")
    #     idea_x.set_kids_empty_if_null()
    #     for idea_y in idea_x._kids.values():
    #         print(f"{idea_y._pad=} {idea_y._label=}")
    #         idea_y.set_kids_empty_if_null()
    #         for idea_z in idea_y._kids.values():
    #             print(f"{idea_z._pad=} {idea_z._label=}")
    assert old_rain_road != new_rain_road
    assert mood_idea._range_source_road == new_rain_road


def test_agenda_edit_idea_label_ChangesIdeaRequiredUnitsScenario1():
    # GIVEN
    x_agenda = get_agenda_with_4_levels_and_2requireds_2acptfacts()
    old_weekday_text = "weekdays"
    old_weekday_road = f"{x_agenda._culture_title},{old_weekday_text}"
    wednesday_text = "Wednesday"
    old_wednesday_road = (
        f"{x_agenda._culture_title},{old_weekday_text},{wednesday_text}"
    )
    work_idea = x_agenda.get_idea_kid(f"{x_agenda._culture_title},work")
    usa = f"{x_agenda._culture_title},nation-state,USA"
    nationstate = f"{x_agenda._culture_title},nation-state"
    # work_wk_required = RequiredUnit(base=weekday, sufffacts={wed_sufffact.need: wed_sufffact})
    # nation_required = RequiredUnit(base=nationstate, sufffacts={usa_sufffact.need: usa_sufffact})
    assert len(work_idea._requiredunits) == 2
    assert work_idea._requiredunits.get(old_weekday_road) != None
    wednesday_idea = x_agenda.get_idea_kid(old_weekday_road)
    work_weekday_required = work_idea._requiredunits.get(old_weekday_road)
    assert work_weekday_required.sufffacts.get(old_wednesday_road) != None
    assert (
        work_weekday_required.sufffacts.get(old_wednesday_road).need
        == old_wednesday_road
    )
    new_weekday_text = "days of week"
    new_weekday_road = f"{x_agenda._culture_title},{new_weekday_text}"
    new_wednesday_road = (
        f"{x_agenda._culture_title},{new_weekday_text},{wednesday_text}"
    )
    assert work_idea._requiredunits.get(new_weekday_text) is None

    # WHEN
    # for key_x, required_x in work_idea._requiredunits.items():
    #     print(f"Before {key_x=} {required_x.base=}")
    print(f"BEFORE {wednesday_idea._label=}")
    print(f"BEFORE {wednesday_idea._pad=}")
    x_agenda.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
    # for key_x, required_x in work_idea._requiredunits.items():
    #     print(f"AFTER {key_x=} {required_x.base=}")
    print(f"AFTER {wednesday_idea._label=}")
    print(f"AFTER {wednesday_idea._pad=}")

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


def test_agenda_set_healer_CorrectlyChangesBoth():
    # GIVEN
    x_agenda = get_agenda_with_4_levels_and_2requireds_2acptfacts()
    assert x_agenda._healer == "Noa"
    assert x_agenda._idearoot._label == x_agenda._culture_title
    # mid_label1 = "tim"
    # x_agenda.edit_idea_label(old_road=old_label, new_label=mid_label1)
    # assert x_agenda._healer == old_label
    # assert x_agenda._idearoot._label == mid_label1

    # WHEN
    new_label2 = "bob"
    x_agenda.set_healer(new_healer=new_label2)

    # THEN
    assert x_agenda._healer == new_label2
    assert x_agenda._idearoot._label == x_agenda._culture_title
