from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels_and_2reasons_2beliefs,
)
from pytest import raises as pytest_raises
from src.agenda.reason_idea import reasonunit_shop, beliefunit_shop
from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
)


def test_idea_edit_idea_label_FailsWhenIdeaDoesNotExist():
    # GIVEN
    tim_agenda = agendaunit_shop("Tim")

    work_text = "work"
    work_road = tim_agenda.make_l1_road(work_text)
    swim_text = "swim"
    tim_agenda.add_idea(ideaunit_shop(work_text), parent_road=tim_agenda._economy_id)
    tim_agenda.add_idea(ideaunit_shop(swim_text), parent_road=work_road)

    # WHEN / THEN
    no_idea_road = tim_agenda.make_l1_road("bees")
    with pytest_raises(Exception) as excinfo:
        tim_agenda.edit_idea_label(old_road=no_idea_road, new_label="pigeons")
    assert str(excinfo.value) == f"Idea old_road='{no_idea_road}' does not exist"


def test_AgendaUnit_edit_idea_label_RaisesErrorForLevel0IdeaWhenEconomyIDisNone():
    # GIVEN
    tim_text = "Tim"
    tim_agenda = agendaunit_shop(_agent_id=tim_text)

    work_text = "work"
    work_road = tim_agenda.make_l1_road(work_text)
    swim_text = "swim"
    swim_road = tim_agenda.make_road(work_road, swim_text)
    tim_agenda.add_idea(ideaunit_shop(work_text), parent_road=tim_agenda._economy_id)
    tim_agenda.add_idea(ideaunit_shop(swim_text), parent_road=work_road)
    assert tim_agenda._agent_id == tim_text
    assert tim_agenda._idearoot._label == tim_agenda._economy_id
    work_idea = tim_agenda.get_idea_obj(work_road)
    assert work_idea._parent_road == tim_agenda._economy_id
    swim_idea = tim_agenda.get_idea_obj(swim_road)
    assert swim_idea._parent_road == work_road

    # WHEN
    moon_text = "moon"
    tim_agenda.edit_idea_label(old_road=tim_agenda._economy_id, new_label=moon_text)

    # THEN
    # with pytest_raises(Exception) as excinfo:
    #     moon_text = "moon"
    #     tim_agenda.edit_idea_label(old_road=tim_agenda._economy_id, new_label=moon_text)
    # assert (
    #     str(excinfo.value)
    #     == f"Cannot set idearoot to string other than '{tim_agenda._economy_id}'"
    # )

    assert tim_agenda._idearoot._label != moon_text
    assert tim_agenda._idearoot._label == tim_agenda._economy_id


def test_AgendaUnit_edit_idea_label_RaisesErrorForLevel0When_economy_id_IsDifferent():
    # GIVEN
    tim_text = "Tim"
    tim_agenda = agendaunit_shop(_agent_id=tim_text)
    work_text = "work"
    work_road = tim_agenda.make_l1_road(work_text)
    swim_text = "swim"
    swim_road = tim_agenda.make_road(work_road, swim_text)
    tim_agenda.add_idea(ideaunit_shop(work_text), parent_road=tim_agenda._economy_id)
    tim_agenda.add_idea(ideaunit_shop(swim_text), parent_road=work_road)
    sun_text = "sun"
    tim_agenda._economy_id = sun_text
    tim_agenda._idearoot._agenda_economy_id = sun_text
    assert tim_agenda._agent_id == tim_text
    assert tim_agenda._economy_id == sun_text
    assert tim_agenda._idearoot._agenda_economy_id == sun_text
    assert tim_agenda._idearoot._label == root_label()
    work_idea = tim_agenda.get_idea_obj(work_road)
    assert work_idea._parent_road == root_label()
    swim_idea = tim_agenda.get_idea_obj(swim_road)
    assert swim_idea._parent_road == work_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        tim_agenda.edit_idea_label(old_road=root_label(), new_label=moon_text)
    assert (
        str(excinfo.value) == f"Cannot set idearoot to string other than '{sun_text}'"
    )


def test_agenda_set_economy_id_CorrectlySetsAttr():
    # GIVEN
    tim_text = "Tim"
    tim_agenda = agendaunit_shop(_agent_id=tim_text)
    work_text = "work"
    old_work_road = tim_agenda.make_l1_road(work_text)
    swim_text = "swim"
    old_swim_road = tim_agenda.make_road(old_work_road, swim_text)
    tim_agenda.add_idea(ideaunit_shop(work_text), parent_road=tim_agenda._economy_id)
    tim_agenda.add_idea(ideaunit_shop(swim_text), parent_road=old_work_road)
    assert tim_agenda._agent_id == tim_text
    assert tim_agenda._idearoot._label == tim_agenda._economy_id
    work_idea = tim_agenda.get_idea_obj(old_work_road)
    assert work_idea._parent_road == tim_agenda._economy_id
    swim_idea = tim_agenda.get_idea_obj(old_swim_road)
    assert swim_idea._parent_road == old_work_road
    assert tim_agenda._economy_id == tim_agenda._economy_id

    # WHEN
    economy_id_text = "Sun"
    tim_agenda.set_economy_id(economy_id=economy_id_text)

    # THEN
    new_work_road = tim_agenda.make_road(economy_id_text, work_text)
    swim_text = "swim"
    new_swim_road = tim_agenda.make_road(new_work_road, swim_text)
    assert tim_agenda._economy_id == economy_id_text
    assert tim_agenda._idearoot._label == economy_id_text
    work_idea = tim_agenda.get_idea_obj(new_work_road)
    assert work_idea._parent_road == economy_id_text
    swim_idea = tim_agenda.get_idea_obj(new_swim_road)
    assert swim_idea._parent_road == new_work_road


def test_idea_find_replace_road_Changes_kids_scenario1():
    # GIVEN Idea with kids that will be changed
    healer_text = "Tim"
    tim_agenda = agendaunit_shop(_agent_id=healer_text)

    old_healer_text = "healer"
    old_healer_road = tim_agenda.make_l1_road(old_healer_text)
    bloomers_text = "bloomers"
    old_bloomers_road = tim_agenda.make_road(old_healer_road, bloomers_text)
    roses_text = "roses"
    old_roses_road = tim_agenda.make_road(old_bloomers_road, roses_text)
    red_text = "red"
    old_red_road = tim_agenda.make_road(old_roses_road, red_text)

    tim_agenda.add_idea(
        ideaunit_shop(old_healer_text), parent_road=tim_agenda._economy_id
    )
    tim_agenda.add_idea(ideaunit_shop(bloomers_text), parent_road=old_healer_road)
    tim_agenda.add_idea(ideaunit_shop(roses_text), parent_road=old_bloomers_road)
    tim_agenda.add_idea(ideaunit_shop(red_text), parent_road=old_roses_road)
    r_idea_roses = tim_agenda.get_idea_obj(old_roses_road)
    r_idea_bloomers = tim_agenda.get_idea_obj(old_bloomers_road)

    assert r_idea_bloomers._kids.get(roses_text) != None
    assert r_idea_roses._parent_road == old_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    assert r_idea_red._parent_road == old_roses_road

    # WHEN
    new_healer_text = "globe"
    new_healer_road = tim_agenda.make_l1_road(new_healer_text)
    tim_agenda.edit_idea_label(old_road=old_healer_road, new_label=new_healer_text)

    # THEN
    assert tim_agenda._idearoot._kids.get(new_healer_text) != None
    assert tim_agenda._idearoot._kids.get(old_healer_text) is None

    assert r_idea_bloomers._parent_road == new_healer_road
    assert r_idea_bloomers._kids.get(roses_text) != None

    r_idea_roses = r_idea_bloomers._kids.get(roses_text)
    new_bloomers_road = tim_agenda.make_road(new_healer_road, bloomers_text)
    assert r_idea_roses._parent_road == new_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    new_roses_road = tim_agenda.make_road(new_bloomers_road, roses_text)
    assert r_idea_red._parent_road == new_roses_road


def test_agenda_edit_idea_label_Changes_beliefunits():
    # GIVEN agenda with beliefunits that will be changed
    healer_text = "Tim"
    tim_agenda = agendaunit_shop(_agent_id=healer_text)

    healer_text = "healer"
    healer_road = tim_agenda.make_l1_road(healer_text)
    bloomers_text = "bloomers"
    bloomers_road = tim_agenda.make_road(healer_road, bloomers_text)
    roses_text = "roses"
    roses_road = tim_agenda.make_road(bloomers_road, roses_text)
    old_water_text = "water"
    old_water_road = tim_agenda.make_l1_road(old_water_text)
    rain_text = "rain"
    old_rain_road = tim_agenda.make_road(old_water_road, rain_text)

    tim_agenda.add_idea(ideaunit_shop(healer_text), parent_road=tim_agenda._economy_id)
    tim_agenda.add_idea(ideaunit_shop(roses_text), parent_road=bloomers_road)
    tim_agenda.add_idea(ideaunit_shop(rain_text), parent_road=old_water_road)
    tim_agenda.set_belief(base=old_water_road, pick=old_rain_road)

    idea_x = tim_agenda.get_idea_obj(roses_road)
    assert tim_agenda._idearoot._beliefunits[old_water_road] != None
    old_water_rain_beliefunit = tim_agenda._idearoot._beliefunits[old_water_road]
    assert old_water_rain_beliefunit.base == old_water_road
    assert old_water_rain_beliefunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = tim_agenda.make_l1_road(new_water_text)
    tim_agenda.add_idea(
        ideaunit_shop(new_water_text), parent_road=tim_agenda._economy_id
    )
    assert tim_agenda._idearoot._beliefunits.get(new_water_road) is None
    tim_agenda.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    assert tim_agenda._idearoot._beliefunits.get(old_water_road) is None
    assert tim_agenda._idearoot._beliefunits.get(new_water_road) != None
    new_water_rain_beliefunit = tim_agenda._idearoot._beliefunits[new_water_road]
    assert new_water_rain_beliefunit.base == new_water_road
    new_rain_road = tim_agenda.make_road(new_water_road, rain_text)
    assert new_water_rain_beliefunit.pick == new_rain_road

    assert tim_agenda._idearoot._beliefunits.get(new_water_road)
    beliefunit_obj = tim_agenda._idearoot._beliefunits.get(new_water_road)
    # for beliefunit_key, beliefunit_obj in tim_agenda._idearoot._beliefunits.items():
    #     assert beliefunit_key == new_water_road
    assert beliefunit_obj.base == new_water_road
    assert beliefunit_obj.pick == new_rain_road


def test_agenda_edit_idea_label_Changes_idearoot_range_source_road():
    # GIVEN this should never happen but it's not currently banned
    tim_agenda = agendaunit_shop("Tim")
    old_casa_text = "casa"
    old_casa_road = tim_agenda.make_l1_road(old_casa_text)
    tim_agenda.add_idea(
        ideaunit_shop(old_casa_text), parent_road=tim_agenda._economy_id
    )
    tim_agenda.edit_idea_attr(tim_agenda._economy_id, range_source_road=old_casa_road)
    assert tim_agenda._idearoot._range_source_road == old_casa_road

    # WHEN
    new_casa_text = "globe"
    tim_agenda.edit_idea_label(old_road=old_casa_road, new_label=new_casa_text)

    # THEN
    new_casa_road = tim_agenda.make_l1_road(new_casa_text)
    assert tim_agenda._idearoot._range_source_road == new_casa_road


def test_agenda_edit_idea_label_ChangesIdeaUnitN_range_source_road():
    bob_agenda = agendaunit_shop("Bob")
    healer_text = "healer"
    healer_road = bob_agenda.make_l1_road(healer_text)
    old_water_text = "water"
    old_water_road = bob_agenda.make_road(healer_road, old_water_text)
    rain_text = "rain"
    old_rain_road = bob_agenda.make_road(old_water_road, rain_text)
    mood_text = "mood"
    mood_road = bob_agenda.make_l1_road(mood_text)
    bob_agenda.add_idea(ideaunit_shop(healer_text), parent_road=bob_agenda._economy_id)
    bob_agenda.add_idea(ideaunit_shop(old_water_text), parent_road=healer_road)
    bob_agenda.add_idea(ideaunit_shop(rain_text), parent_road=old_water_road)
    bob_agenda.add_idea(ideaunit_shop(mood_text), parent_road=bob_agenda._economy_id)

    bob_agenda.edit_idea_attr(road=mood_road, range_source_road=old_rain_road)
    mood_idea = bob_agenda.get_idea_obj(mood_road)
    assert mood_idea._range_source_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = bob_agenda.make_road(healer_road, new_water_text)
    new_rain_road = bob_agenda.make_road(new_water_road, rain_text)
    bob_agenda.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    # for idea_x in bob_agenda._idearoot._kids.values():
    #     print(f"{idea_x._parent_road=} {idea_x._label=}")
    #     for idea_y in idea_x._kids.values():
    #         print(f"{idea_y._parent_road=} {idea_y._label=}")
    #         for idea_z in idea_y._kids.values():
    #             print(f"{idea_z._parent_road=} {idea_z._label=}")
    assert old_rain_road != new_rain_road
    assert mood_idea._range_source_road == new_rain_road


def test_agenda_edit_idea_label_ChangesIdeaReasonUnitsScenario1():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons_2beliefs()
    old_weekday_text = "weekdays"
    old_weekday_road = sue_agenda.make_l1_road(old_weekday_text)
    wednesday_text = "Wednesday"
    old_wednesday_road = sue_agenda.make_road(old_weekday_road, wednesday_text)
    work_idea = sue_agenda.get_idea_obj(sue_agenda.make_l1_road("work"))
    # work_wk_reason = reasonunit_shop(weekday, premises={wed_premise.need: wed_premise})
    # nation_reason = reasonunit_shop(nationstate, premises={usa_premise.need: usa_premise})
    assert len(work_idea._reasonunits) == 2
    assert work_idea._reasonunits.get(old_weekday_road) != None
    wednesday_idea = sue_agenda.get_idea_obj(old_weekday_road)
    work_weekday_reason = work_idea._reasonunits.get(old_weekday_road)
    assert work_weekday_reason.premises.get(old_wednesday_road) != None
    assert (
        work_weekday_reason.premises.get(old_wednesday_road).need == old_wednesday_road
    )
    new_weekday_text = "days of week"
    new_weekday_road = sue_agenda.make_l1_road(new_weekday_text)
    new_wednesday_road = sue_agenda.make_road(new_weekday_road, wednesday_text)
    assert work_idea._reasonunits.get(new_weekday_text) is None

    # WHEN
    # for key_x, reason_x in work_idea._reasonunits.items():
    #     print(f"Before {key_x=} {reason_x.base=}")
    print(f"BEFORE {wednesday_idea._label=}")
    print(f"BEFORE {wednesday_idea._parent_road=}")
    sue_agenda.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
    # for key_x, reason_x in work_idea._reasonunits.items():
    #     print(f"AFTER {key_x=} {reason_x.base=}")
    print(f"AFTER {wednesday_idea._label=}")
    print(f"AFTER {wednesday_idea._parent_road=}")

    # THEN
    assert work_idea._reasonunits.get(new_weekday_road) != None
    assert work_idea._reasonunits.get(old_weekday_road) is None
    work_weekday_reason = work_idea._reasonunits.get(new_weekday_road)
    assert work_weekday_reason.premises.get(new_wednesday_road) != None
    assert (
        work_weekday_reason.premises.get(new_wednesday_road).need == new_wednesday_road
    )
    assert len(work_idea._reasonunits) == 2


def test_agenda_set_healer_CorrectlyChangesBoth():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons_2beliefs()
    assert sue_agenda._agent_id == "Sue"
    assert sue_agenda._idearoot._label == sue_agenda._economy_id
    # mid_label1 = "tim"
    # sue_agenda.edit_idea_label(old_road=old_label, new_label=mid_label1)
    # assert sue_agenda._agent_id == old_label
    # assert sue_agenda._idearoot._label == mid_label1

    # WHEN
    bob_text = "bob"
    sue_agenda.set_agent_id(new_agent_id=bob_text)

    # THEN
    assert sue_agenda._agent_id == bob_text
    assert sue_agenda._idearoot._label == sue_agenda._economy_id


def test_agenda_edit_idea_label_RaisesErrorIfdelimiterIsInLabel():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons_2beliefs()
    old_weekday_text = "weekdays"
    old_weekday_road = sue_agenda.make_l1_road(old_weekday_text)

    # WHEN / THEN
    new_weekday_text = "days, of week"
    with pytest_raises(Exception) as excinfo:
        sue_agenda.edit_idea_label(
            old_road=old_weekday_road, new_label=new_weekday_text
        )
    assert (
        str(excinfo.value)
        == f"Cannot change '{old_weekday_road}' because new_label {new_weekday_text} contains delimiter {sue_agenda._road_delimiter}"
    )


def test_agenda_set_road_delimiter_RaisesErrorIfNew_delimiter_IsAnIdea_label():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    print(f"{luca_agenda._max_tree_traverse=}")
    work_text = "work"
    work_road = luca_agenda.make_road(luca_agenda._economy_id, work_text)
    luca_agenda.add_idea(ideaunit_shop(work_text), parent_road=luca_agenda._economy_id)
    slash_text = "/"
    home_text = f"home cooking{slash_text}cleaning"
    luca_agenda.add_idea(ideaunit_shop(home_text), parent_road=work_road)

    # WHEN / THEN
    home_road = luca_agenda.make_road(work_road, home_text)
    print(f"{home_road=}")
    with pytest_raises(Exception) as excinfo:
        luca_agenda.set_road_delimiter(slash_text)
    assert (
        str(excinfo.value)
        == f"Cannot change delimiter to '{slash_text}' because it already exists an idea label '{home_road}'"
    )


def test_agenda_set_road_delimiter_CorrectlyChanges_parent_road():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    work_text = "work"
    luca_agenda.add_idea(ideaunit_shop(work_text), parent_road=luca_agenda._economy_id)
    comma_work_road = luca_agenda.make_l1_road(work_text)
    cook_text = "cook cooking"
    luca_agenda.add_idea(ideaunit_shop(cook_text), parent_road=comma_work_road)
    comma_cook_road = luca_agenda.make_road(comma_work_road, cook_text)
    cook_idea = luca_agenda.get_idea_obj(comma_cook_road)
    comma_text = ","
    assert luca_agenda._road_delimiter == comma_text
    comma_cook_road = luca_agenda.make_road(comma_work_road, cook_text)
    # print(f"{luca_agenda._economy_id=} {luca_agenda._idearoot._label=} {work_road=}")
    # print(f"{cook_idea._parent_road=} {cook_idea._label=}")
    # comma_work_idea = luca_agenda.get_idea_obj(comma_work_road)
    # print(f"{comma_work_idea._parent_road=} {comma_work_idea._label=}")
    assert cook_idea.get_road() == comma_cook_road

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_delimiter(slash_text)

    # THEN
    assert cook_idea.get_road() != comma_cook_road
    slash_work_road = create_road(
        luca_agenda._economy_id, work_text, delimiter=slash_text
    )
    slash_cook_road = create_road(slash_work_road, cook_text, delimiter=slash_text)
    assert cook_idea.get_road() == slash_cook_road


def test_agenda_set_road_delimiter_CorrectlyChangesReasonUnit():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    work_text = "work"
    luca_agenda.add_idea(ideaunit_shop(work_text), parent_road=luca_agenda._economy_id)
    time_text = "time"
    comma_time_road = luca_agenda.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = luca_agenda.make_road(comma_time_road, _8am_text)

    comma_time_reasonunit = reasonunit_shop(base=comma_time_road)
    comma_time_reasonunit.set_premise(comma_8am_road)

    comma_work_road = luca_agenda.make_l1_road(work_text)
    luca_agenda.edit_idea_attr(road=comma_work_road, reason=comma_time_reasonunit)
    work_idea = luca_agenda.get_idea_obj(comma_work_road)
    assert work_idea._reasonunits.get(comma_time_road) != None
    gen_time_reasonunit = work_idea._reasonunits.get(comma_time_road)
    assert gen_time_reasonunit.premises.get(comma_8am_road) != None

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_delimiter(slash_text)

    # THEN
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_8am_road = luca_agenda.make_road(slash_time_road, _8am_text)
    slash_work_road = luca_agenda.make_l1_road(work_text)
    work_idea = luca_agenda.get_idea_obj(slash_work_road)
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_8am_road = luca_agenda.make_road(slash_time_road, _8am_text)
    assert work_idea._reasonunits.get(slash_time_road) != None
    gen_time_reasonunit = work_idea._reasonunits.get(slash_time_road)
    assert gen_time_reasonunit.premises.get(slash_8am_road) != None

    assert work_idea._reasonunits.get(comma_time_road) is None
    assert gen_time_reasonunit.premises.get(comma_8am_road) is None


def test_agenda_set_road_delimiter_CorrectlyChangesBeliefUnit():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    work_text = "work"
    luca_agenda.add_idea(ideaunit_shop(work_text), parent_road=luca_agenda._economy_id)
    time_text = "time"
    comma_time_road = luca_agenda.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = luca_agenda.make_road(comma_time_road, _8am_text)
    comma_time_beliefunit = beliefunit_shop(comma_time_road, comma_8am_road)

    comma_work_road = luca_agenda.make_l1_road(work_text)
    luca_agenda.edit_idea_attr(comma_work_road, beliefunit=comma_time_beliefunit)
    work_idea = luca_agenda.get_idea_obj(comma_work_road)
    print(f"{work_idea._beliefunits=} {comma_time_road=}")
    assert work_idea._beliefunits.get(comma_time_road) != None
    gen_time_beliefunit = work_idea._beliefunits.get(comma_time_road)

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_delimiter(slash_text)

    # THEN
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_work_road = luca_agenda.make_l1_road(work_text)
    work_idea = luca_agenda.get_idea_obj(slash_work_road)
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_8am_road = luca_agenda.make_road(slash_time_road, _8am_text)
    assert work_idea._beliefunits.get(slash_time_road) != None
    gen_time_beliefunit = work_idea._beliefunits.get(slash_time_road)
    assert gen_time_beliefunit.base != None
    assert gen_time_beliefunit.base == slash_time_road
    assert gen_time_beliefunit.pick != None
    assert gen_time_beliefunit.pick == slash_8am_road

    assert work_idea._beliefunits.get(comma_time_road) is None


def test_agenda_set_road_delimiter_CorrectlyChanges_numeric_roadAND_range_source_road():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    work_text = "work"
    luca_agenda.add_idea(ideaunit_shop(work_text), parent_road=luca_agenda._economy_id)
    comma_work_road = luca_agenda.make_l1_road(work_text)
    cook_text = "cook cooking"
    luca_agenda.add_idea(ideaunit_shop(cook_text), parent_road=comma_work_road)
    comma_cook_road = luca_agenda.make_road(comma_work_road, cook_text)

    # numeric_road
    taste_text = "foot taste"
    luca_agenda.add_idea(
        ideaunit_shop(taste_text, _begin=0, _close=6),
        parent_road=luca_agenda._economy_id,
    )
    comma_taste_road = luca_agenda.make_l1_road(taste_text)
    luca_agenda.edit_idea_attr(comma_cook_road, numeric_road=comma_taste_road)

    # range_source
    heat_text = "heat numbers"
    luca_agenda.add_idea(
        ideaunit_shop(heat_text, _begin=0, _close=6),
        parent_road=luca_agenda._economy_id,
    )
    comma_heat_road = luca_agenda.make_l1_road(heat_text)
    luca_agenda.edit_idea_attr(comma_cook_road, range_source_road=comma_heat_road)

    cook_idea = luca_agenda.get_idea_obj(comma_cook_road)
    assert cook_idea._numeric_road == comma_taste_road
    assert cook_idea._range_source_road == comma_heat_road

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_delimiter(slash_text)

    # THEN
    slash_taste_road = luca_agenda.make_l1_road(taste_text)
    assert cook_idea._numeric_road != comma_taste_road
    assert cook_idea._numeric_road == slash_taste_road
    slash_heat_road = luca_agenda.make_l1_road(heat_text)
    assert cook_idea._range_source_road != comma_heat_road
    assert cook_idea._range_source_road == slash_heat_road
