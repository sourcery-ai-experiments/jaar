from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideacore_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels_and_2requireds_2acptfacts,
)
from pytest import raises as pytest_raises
from src.agenda.required_idea import requiredunit_shop, acptfactunit_shop
from src.agenda.road import get_default_culture_root_label as root_label, get_road


def test_idea_label_fails_when_idea_does_not_exist():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)

    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    swim_text = "swim"
    x_agenda.add_idea(ideacore_shop(work_text), pad=x_agenda._culture_id)
    x_agenda.add_idea(ideacore_shop(swim_text), pad=work_road)

    # WHEN / THEN
    no_idea_road = x_agenda.make_l1_road("bees")
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_label(old_road=no_idea_road, new_label="pigeons")
    assert (
        str(excinfo.value)
        == f"Getting idea_label='bees' failed no item at '{no_idea_road}'"
    )


def test_Agenda_level0_idea_edit_idea_label_RaisesError_culture_id_IsNone():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    swim_text = "swim"
    swim_road = x_agenda.make_road(work_road, swim_text)
    x_agenda.add_idea(ideacore_shop(work_text), pad=x_agenda._culture_id)
    x_agenda.add_idea(ideacore_shop(swim_text), pad=work_road)
    assert x_agenda._healer == healer_text
    assert x_agenda._culture_id == x_agenda._culture_id
    assert x_agenda._idearoot._label == x_agenda._culture_id
    work_idea = x_agenda.get_idea_kid(work_road)
    assert work_idea._pad == x_agenda._culture_id
    swim_idea = x_agenda.get_idea_kid(swim_road)
    assert swim_idea._pad == work_road

    # WHEN
    moon_text = "moon"
    x_agenda.edit_idea_label(old_road=x_agenda._culture_id, new_label=moon_text)

    # THEN
    # with pytest_raises(Exception) as excinfo:
    #     moon_text = "moon"
    #     x_agenda.edit_idea_label(old_road=x_agenda._culture_id, new_label=moon_text)
    # assert (
    #     str(excinfo.value)
    #     == f"Cannot set idearoot to string other than '{x_agenda._culture_id}'"
    # )

    assert x_agenda._idearoot._label != moon_text
    assert x_agenda._idearoot._label == x_agenda._culture_id


def test_Agenda_level0_idea_edit_idea_label_RaisesError_culture_id_IsDifferent():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    swim_text = "swim"
    swim_road = x_agenda.make_road(work_road, swim_text)
    x_agenda.add_idea(ideacore_shop(work_text), pad=x_agenda._culture_id)
    x_agenda.add_idea(ideacore_shop(swim_text), pad=work_road)
    sun_text = "sun"
    x_agenda._culture_id = sun_text
    assert x_agenda._healer == healer_text
    assert x_agenda._culture_id == sun_text
    assert x_agenda._idearoot._label == root_label()
    work_idea = x_agenda.get_idea_kid(work_road)
    assert work_idea._pad == root_label()
    swim_idea = x_agenda.get_idea_kid(swim_road)
    assert swim_idea._pad == work_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        x_agenda.edit_idea_label(old_road=root_label(), new_label=moon_text)
    assert (
        str(excinfo.value) == f"Cannot set idearoot to string other than '{sun_text}'"
    )


def test_agenda_set_culture_id_CorrectlySetsAttr():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)
    work_text = "work"
    old_work_road = x_agenda.make_l1_road(work_text)
    swim_text = "swim"
    old_swim_road = x_agenda.make_road(old_work_road, swim_text)
    x_agenda.add_idea(ideacore_shop(work_text), pad=x_agenda._culture_id)
    x_agenda.add_idea(ideacore_shop(swim_text), pad=old_work_road)
    assert x_agenda._healer == healer_text
    assert x_agenda._idearoot._label == x_agenda._culture_id
    work_idea = x_agenda.get_idea_kid(old_work_road)
    assert work_idea._pad == x_agenda._culture_id
    swim_idea = x_agenda.get_idea_kid(old_swim_road)
    assert swim_idea._pad == old_work_road
    assert x_agenda._culture_id == x_agenda._culture_id

    # WHEN
    culture_id_text = "Sun"
    x_agenda.set_culture_id(culture_id=culture_id_text)

    # THEN
    new_work_road = x_agenda.make_road(culture_id_text, work_text)
    swim_text = "swim"
    new_swim_road = x_agenda.make_road(new_work_road, swim_text)
    assert x_agenda._culture_id == culture_id_text
    assert x_agenda._idearoot._label == culture_id_text
    work_idea = x_agenda.get_idea_kid(new_work_road)
    assert work_idea._pad == culture_id_text
    swim_idea = x_agenda.get_idea_kid(new_swim_road)
    assert swim_idea._pad == new_work_road


def test_idea_find_replace_road_Changes_kids_scenario1():
    # GIVEN Idea with kids that will be changed
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    old_healer_text = "healer"
    old_healer_road = x_agenda.make_l1_road(old_healer_text)
    bloomers_text = "bloomers"
    old_bloomers_road = x_agenda.make_road(old_healer_road, bloomers_text)
    roses_text = "roses"
    old_roses_road = x_agenda.make_road(old_bloomers_road, roses_text)
    red_text = "red"
    old_red_road = x_agenda.make_road(old_roses_road, red_text)

    x_agenda.add_idea(ideacore_shop(old_healer_text), pad=x_agenda._culture_id)
    x_agenda.add_idea(ideacore_shop(bloomers_text), pad=old_healer_road)
    x_agenda.add_idea(ideacore_shop(roses_text), pad=old_bloomers_road)
    x_agenda.add_idea(ideacore_shop(red_text), pad=old_roses_road)
    r_idea_roses = x_agenda.get_idea_kid(old_roses_road)
    r_idea_bloomers = x_agenda.get_idea_kid(old_bloomers_road)

    assert r_idea_bloomers._kids.get(roses_text) != None
    assert r_idea_roses._pad == old_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    assert r_idea_red._pad == old_roses_road

    # WHEN
    new_healer_text = "globe"
    new_healer_road = x_agenda.make_l1_road(new_healer_text)
    x_agenda.edit_idea_label(old_road=old_healer_road, new_label=new_healer_text)

    # THEN
    assert x_agenda._idearoot._kids.get(new_healer_text) != None
    assert x_agenda._idearoot._kids.get(old_healer_text) is None

    assert r_idea_bloomers._pad == new_healer_road
    assert r_idea_bloomers._kids.get(roses_text) != None

    r_idea_roses = r_idea_bloomers._kids.get(roses_text)
    new_bloomers_road = x_agenda.make_road(new_healer_road, bloomers_text)
    assert r_idea_roses._pad == new_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    new_roses_road = x_agenda.make_road(new_bloomers_road, roses_text)
    assert r_idea_red._pad == new_roses_road


def test_agenda_edit_idea_label_Changes_acptfactunits():
    # GIVEN agenda with acptfactunits that will be changed
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    healer_text = "healer"
    healer_road = x_agenda.make_l1_road(healer_text)
    bloomers_text = "bloomers"
    bloomers_road = x_agenda.make_road(healer_road, bloomers_text)
    roses_text = "roses"
    roses_road = x_agenda.make_road(bloomers_road, roses_text)
    old_water_text = "water"
    old_water_road = x_agenda.make_l1_road(old_water_text)
    rain_text = "rain"
    old_rain_road = x_agenda.make_road(old_water_road, rain_text)

    x_agenda.add_idea(ideacore_shop(healer_text), pad=x_agenda._culture_id)
    x_agenda.add_idea(ideacore_shop(roses_text), pad=bloomers_road)
    x_agenda.add_idea(ideacore_shop(rain_text), pad=old_water_road)
    x_agenda.set_acptfact(base=old_water_road, pick=old_rain_road)

    idea_x = x_agenda.get_idea_kid(roses_road)
    assert x_agenda._idearoot._acptfactunits[old_water_road] != None
    old_water_rain_acptfactunit = x_agenda._idearoot._acptfactunits[old_water_road]
    assert old_water_rain_acptfactunit.base == old_water_road
    assert old_water_rain_acptfactunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = x_agenda.make_l1_road(new_water_text)
    x_agenda.add_idea(ideacore_shop(new_water_text), pad=x_agenda._culture_id)
    assert x_agenda._idearoot._acptfactunits.get(new_water_road) is None
    x_agenda.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    assert x_agenda._idearoot._acptfactunits.get(old_water_road) is None
    assert x_agenda._idearoot._acptfactunits.get(new_water_road) != None
    new_water_rain_acptfactunit = x_agenda._idearoot._acptfactunits[new_water_road]
    assert new_water_rain_acptfactunit.base == new_water_road
    new_rain_road = x_agenda.make_road(new_water_road, rain_text)
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
    old_healer_road = x_agenda.make_l1_road(old_healer_text)
    x_agenda.add_idea(ideacore_shop(old_healer_text), pad=x_agenda._culture_id)
    x_agenda.edit_idea_attr(x_agenda._culture_id, range_source_road=old_healer_road)
    assert x_agenda._idearoot._range_source_road == old_healer_road

    # WHEN
    new_healer_text = "globe"
    x_agenda.edit_idea_label(old_road=old_healer_road, new_label=new_healer_text)

    # THEN
    new_healer_road = x_agenda.make_l1_road(new_healer_text)
    assert x_agenda._idearoot._range_source_road == new_healer_road


def test_agenda_edit_idea_label_ChangesIdeaKidN_range_source_road():
    healer_text = "Bob"
    x_agenda = agendaunit_shop(_healer=healer_text)

    healer_text = "healer"
    healer_road = x_agenda.make_l1_road(healer_text)
    old_water_text = "water"
    old_water_road = x_agenda.make_road(healer_road, old_water_text)
    rain_text = "rain"
    old_rain_road = x_agenda.make_road(old_water_road, rain_text)
    mood_text = "mood"
    mood_road = x_agenda.make_l1_road(mood_text)
    x_agenda.add_idea(ideacore_shop(healer_text), pad=x_agenda._culture_id)
    x_agenda.add_idea(ideacore_shop(old_water_text), pad=healer_road)
    x_agenda.add_idea(ideacore_shop(rain_text), pad=old_water_road)
    x_agenda.add_idea(ideacore_shop(mood_text), pad=x_agenda._culture_id)

    x_agenda.edit_idea_attr(road=mood_road, range_source_road=old_rain_road)
    mood_idea = x_agenda.get_idea_kid(mood_road)
    assert mood_idea._range_source_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = x_agenda.make_road(healer_road, new_water_text)
    new_rain_road = x_agenda.make_road(new_water_road, rain_text)
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
    old_weekday_road = x_agenda.make_l1_road(old_weekday_text)
    wednesday_text = "Wednesday"
    old_wednesday_road = x_agenda.make_road(old_weekday_road, wednesday_text)
    work_idea = x_agenda.get_idea_kid(x_agenda.make_l1_road("work"))
    # work_wk_required = requiredunit_shop(weekday, sufffacts={wed_sufffact.need: wed_sufffact})
    # nation_required = requiredunit_shop(nationstate, sufffacts={usa_sufffact.need: usa_sufffact})
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
    new_weekday_road = x_agenda.make_l1_road(new_weekday_text)
    new_wednesday_road = x_agenda.make_road(new_weekday_road, wednesday_text)
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
    assert x_agenda._idearoot._label == x_agenda._culture_id
    # mid_label1 = "tim"
    # x_agenda.edit_idea_label(old_road=old_label, new_label=mid_label1)
    # assert x_agenda._healer == old_label
    # assert x_agenda._idearoot._label == mid_label1

    # WHEN
    new_label2 = "bob"
    x_agenda.set_healer(new_healer=new_label2)

    # THEN
    assert x_agenda._healer == new_label2
    assert x_agenda._idearoot._label == x_agenda._culture_id


def test_agenda_edit_idea_label_RaisesErrorIfdelimiterIsInLabel():
    # GIVEN
    x_agenda = get_agenda_with_4_levels_and_2requireds_2acptfacts()
    old_weekday_text = "weekdays"
    old_weekday_road = x_agenda.make_l1_road(old_weekday_text)

    # WHEN / THEN
    new_weekday_text = "days, of week"
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
    assert (
        str(excinfo.value)
        == f"Cannot change '{old_weekday_road}' because new_label {new_weekday_text} contains delimiter {x_agenda._road_node_delimiter}"
    )


def test_agenda_set_road_node_delimiter_RaisesErrorIfNew_delimiter_IsAnIdeaLabel():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    print(f"{luca_agenda._max_tree_traverse=}")
    work_text = "work"
    work_road = luca_agenda.make_road(luca_agenda._culture_id, work_text)
    luca_agenda.add_idea(ideacore_shop(work_text), pad=luca_agenda._culture_id)
    slash_text = "/"
    home_text = f"home cooking{slash_text}cleaning"
    luca_agenda.add_idea(ideacore_shop(home_text), pad=work_road)

    # WHEN / THEN
    home_road = luca_agenda.make_road(work_road, home_text)
    print(f"{home_road=}")
    with pytest_raises(Exception) as excinfo:
        luca_agenda.set_road_node_delimiter(slash_text)
    assert (
        str(excinfo.value)
        == f"Cannot change delimiter to '{slash_text}' because it already exists an idea label '{home_road}'"
    )


def test_agenda_set_road_node_delimiter_CorrectlyChanges_pad():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    work_text = "work"
    luca_agenda.add_idea(ideacore_shop(work_text), pad=luca_agenda._culture_id)
    comma_work_road = luca_agenda.make_l1_road(work_text)
    cook_text = "cook cooking"
    luca_agenda.add_idea(ideacore_shop(cook_text), pad=comma_work_road)
    comma_cook_road = luca_agenda.make_road(comma_work_road, cook_text)
    cook_idea = luca_agenda.get_idea_kid(comma_cook_road)
    comma_text = ","
    comma_cook_road = get_road(comma_work_road, cook_text, delimiter=comma_text)
    # print(f"{luca_agenda._culture_id=} {luca_agenda._idearoot._label=} {work_road=}")
    # print(f"{cook_idea._pad=} {cook_idea._label=}")
    # comma_work_idea = luca_agenda.get_idea_kid(comma_work_road)
    # print(f"{comma_work_idea._pad=} {comma_work_idea._label=}")
    assert cook_idea.get_idea_road() == comma_cook_road

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_node_delimiter(slash_text)

    # THEN
    assert cook_idea.get_idea_road() != comma_cook_road
    slash_work_road = get_road(luca_agenda._culture_id, work_text, delimiter=slash_text)
    slash_cook_road = get_road(slash_work_road, cook_text, delimiter=slash_text)
    assert cook_idea.get_idea_road() == slash_cook_road


def test_agenda_set_road_node_delimiter_CorrectlyChangesRequiredUnit():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    work_text = "work"
    luca_agenda.add_idea(ideacore_shop(work_text), pad=luca_agenda._culture_id)
    time_text = "time"
    comma_time_road = luca_agenda.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = luca_agenda.make_road(comma_time_road, _8am_text)

    comma_time_requiredunit = requiredunit_shop(base=comma_time_road)
    comma_time_requiredunit.set_sufffact(comma_8am_road)

    comma_work_road = luca_agenda.make_l1_road(work_text)
    luca_agenda.edit_idea_attr(road=comma_work_road, required=comma_time_requiredunit)
    work_idea = luca_agenda.get_idea_kid(comma_work_road)
    assert work_idea._requiredunits.get(comma_time_road) != None
    gen_time_requiredunit = work_idea._requiredunits.get(comma_time_road)
    assert gen_time_requiredunit.sufffacts.get(comma_8am_road) != None

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_node_delimiter(slash_text)

    # THEN
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_8am_road = luca_agenda.make_road(slash_time_road, _8am_text)
    slash_work_road = luca_agenda.make_l1_road(work_text)
    work_idea = luca_agenda.get_idea_kid(slash_work_road)
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_8am_road = luca_agenda.make_road(slash_time_road, _8am_text)
    assert work_idea._requiredunits.get(slash_time_road) != None
    gen_time_requiredunit = work_idea._requiredunits.get(slash_time_road)
    assert gen_time_requiredunit.sufffacts.get(slash_8am_road) != None

    assert work_idea._requiredunits.get(comma_time_road) is None
    assert gen_time_requiredunit.sufffacts.get(comma_8am_road) is None


def test_agenda_set_road_node_delimiter_CorrectlyChangesAcptFactUnit():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    work_text = "work"
    luca_agenda.add_idea(ideacore_shop(work_text), pad=luca_agenda._culture_id)
    time_text = "time"
    comma_time_road = luca_agenda.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = luca_agenda.make_road(comma_time_road, _8am_text)
    comma_time_acptfactunit = acptfactunit_shop(comma_time_road, comma_8am_road)

    comma_work_road = luca_agenda.make_l1_road(work_text)
    luca_agenda.edit_idea_attr(comma_work_road, acptfactunit=comma_time_acptfactunit)
    work_idea = luca_agenda.get_idea_kid(comma_work_road)
    print(f"{work_idea._acptfactunits=} {comma_time_road=}")
    assert work_idea._acptfactunits.get(comma_time_road) != None
    gen_time_acptfactunit = work_idea._acptfactunits.get(comma_time_road)

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_node_delimiter(slash_text)

    # THEN
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_work_road = luca_agenda.make_l1_road(work_text)
    work_idea = luca_agenda.get_idea_kid(slash_work_road)
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_8am_road = luca_agenda.make_road(slash_time_road, _8am_text)
    assert work_idea._acptfactunits.get(slash_time_road) != None
    gen_time_acptfactunit = work_idea._acptfactunits.get(slash_time_road)
    assert gen_time_acptfactunit.base != None
    assert gen_time_acptfactunit.base == slash_time_road
    assert gen_time_acptfactunit.pick != None
    assert gen_time_acptfactunit.pick == slash_8am_road

    assert work_idea._acptfactunits.get(comma_time_road) is None


def test_agenda_set_road_node_delimiter_CorrectlyChanges_numeric_roadAND_range_source_road():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    work_text = "work"
    luca_agenda.add_idea(ideacore_shop(work_text), pad=luca_agenda._culture_id)
    comma_work_road = luca_agenda.make_l1_road(work_text)
    cook_text = "cook cooking"
    luca_agenda.add_idea(ideacore_shop(cook_text), pad=comma_work_road)
    comma_cook_road = luca_agenda.make_road(comma_work_road, cook_text)

    # numeric_road
    taste_text = "foot taste"
    luca_agenda.add_idea(
        ideacore_shop(taste_text, _begin=0, _close=6), pad=luca_agenda._culture_id
    )
    comma_taste_road = luca_agenda.make_l1_road(taste_text)
    luca_agenda.edit_idea_attr(comma_cook_road, numeric_road=comma_taste_road)

    # range_source
    heat_text = "heat numbers"
    luca_agenda.add_idea(
        ideacore_shop(heat_text, _begin=0, _close=6), pad=luca_agenda._culture_id
    )
    comma_heat_road = luca_agenda.make_l1_road(heat_text)
    luca_agenda.edit_idea_attr(comma_cook_road, range_source_road=comma_heat_road)

    cook_idea = luca_agenda.get_idea_kid(comma_cook_road)
    assert cook_idea._numeric_road == comma_taste_road
    assert cook_idea._range_source_road == comma_heat_road

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_node_delimiter(slash_text)

    # THEN
    slash_taste_road = luca_agenda.make_l1_road(taste_text)
    assert cook_idea._numeric_road != comma_taste_road
    assert cook_idea._numeric_road == slash_taste_road
    slash_heat_road = luca_agenda.make_l1_road(heat_text)
    assert cook_idea._range_source_road != comma_heat_road
    assert cook_idea._range_source_road == slash_heat_road
