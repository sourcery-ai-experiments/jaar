from src.agenda.agenda import agendaunit_shop
from src.agenda.oath import oathunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels_and_2reasons_2beliefs,
)
from pytest import raises as pytest_raises
from src.agenda.reason_oath import reasonunit_shop, beliefunit_shop
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
)


def test_AgendaUnit_edit_oath_label_FailsWhenOathDoesNotExist():
    # GIVEN
    tim_agenda = agendaunit_shop("Tim")

    casa_text = "casa"
    casa_road = tim_agenda.make_l1_road(casa_text)
    swim_text = "swim"
    tim_agenda.add_l1_oath(oathunit_shop(casa_text))
    tim_agenda.add_oath(oathunit_shop(swim_text), parent_road=casa_road)

    # WHEN / THEN
    no_oath_road = tim_agenda.make_l1_road("bees")
    with pytest_raises(Exception) as excinfo:
        tim_agenda.edit_oath_label(old_road=no_oath_road, new_label="pigeons")
    assert str(excinfo.value) == f"Oath old_road='{no_oath_road}' does not exist"


def test_AgendaUnit_edit_oath_label_RaisesErrorForLevel0OathWhen_real_id_isNone():
    # GIVEN
    tim_text = "Tim"
    tim_agenda = agendaunit_shop(_owner_id=tim_text)

    casa_text = "casa"
    casa_road = tim_agenda.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = tim_agenda.make_road(casa_road, swim_text)
    tim_agenda.add_l1_oath(oathunit_shop(casa_text))
    tim_agenda.add_oath(oathunit_shop(swim_text), parent_road=casa_road)
    assert tim_agenda._owner_id == tim_text
    assert tim_agenda._oathroot._label == tim_agenda._real_id
    casa_oath = tim_agenda.get_oath_obj(casa_road)
    assert casa_oath._parent_road == tim_agenda._real_id
    swim_oath = tim_agenda.get_oath_obj(swim_road)
    assert swim_oath._parent_road == casa_road

    # WHEN
    moon_text = "moon"
    tim_agenda.edit_oath_label(old_road=tim_agenda._real_id, new_label=moon_text)

    # THEN
    # with pytest_raises(Exception) as excinfo:
    #     moon_text = "moon"
    #     tim_agenda.edit_oath_label(old_road=tim_agenda._real_id, new_label=moon_text)
    # assert (
    #     str(excinfo.value)
    #     == f"Cannot set oathroot to string other than '{tim_agenda._real_id}'"
    # )

    assert tim_agenda._oathroot._label != moon_text
    assert tim_agenda._oathroot._label == tim_agenda._real_id


def test_AgendaUnit_edit_oath_label_RaisesErrorForLevel0When_real_id_IsDifferent():
    # GIVEN
    tim_text = "Tim"
    tim_agenda = agendaunit_shop(_owner_id=tim_text)
    casa_text = "casa"
    casa_road = tim_agenda.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = tim_agenda.make_road(casa_road, swim_text)
    tim_agenda.add_l1_oath(oathunit_shop(casa_text))
    tim_agenda.add_oath(oathunit_shop(swim_text), parent_road=casa_road)
    sun_text = "sun"
    tim_agenda._real_id = sun_text
    tim_agenda._oathroot._agenda_real_id = sun_text
    assert tim_agenda._owner_id == tim_text
    assert tim_agenda._real_id == sun_text
    assert tim_agenda._oathroot._agenda_real_id == sun_text
    assert tim_agenda._oathroot._label == root_label()
    casa_oath = tim_agenda.get_oath_obj(casa_road)
    assert casa_oath._parent_road == root_label()
    swim_oath = tim_agenda.get_oath_obj(swim_road)
    assert swim_oath._parent_road == casa_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        tim_agenda.edit_oath_label(old_road=root_label(), new_label=moon_text)
    assert (
        str(excinfo.value) == f"Cannot set oathroot to string other than '{sun_text}'"
    )


def test_agenda_set_real_id_CorrectlySetsAttr():
    # GIVEN
    tim_text = "Tim"
    tim_agenda = agendaunit_shop(_owner_id=tim_text)
    casa_text = "casa"
    old_casa_road = tim_agenda.make_l1_road(casa_text)
    swim_text = "swim"
    old_swim_road = tim_agenda.make_road(old_casa_road, swim_text)
    tim_agenda.add_l1_oath(oathunit_shop(casa_text))
    tim_agenda.add_oath(oathunit_shop(swim_text), parent_road=old_casa_road)
    assert tim_agenda._owner_id == tim_text
    assert tim_agenda._oathroot._label == tim_agenda._real_id
    casa_oath = tim_agenda.get_oath_obj(old_casa_road)
    assert casa_oath._parent_road == tim_agenda._real_id
    swim_oath = tim_agenda.get_oath_obj(old_swim_road)
    assert swim_oath._parent_road == old_casa_road
    assert tim_agenda._real_id == tim_agenda._real_id

    # WHEN
    real_id_text = "Sun"
    tim_agenda.set_real_id(real_id=real_id_text)

    # THEN
    new_casa_road = tim_agenda.make_l1_road(casa_text)
    swim_text = "swim"
    new_swim_road = tim_agenda.make_road(new_casa_road, swim_text)
    assert tim_agenda._real_id == real_id_text
    assert tim_agenda._oathroot._label == real_id_text
    casa_oath = tim_agenda.get_oath_obj(new_casa_road)
    assert casa_oath._parent_road == real_id_text
    swim_oath = tim_agenda.get_oath_obj(new_swim_road)
    assert swim_oath._parent_road == new_casa_road


def test_AgendaUnit_find_replace_road_CorrectlyModifies_kids_Scenario1():
    # GIVEN Oath with kids that will be different
    tim_text = "Tim"
    tim_agenda = agendaunit_shop(tim_text)

    old_casa_text = "casa"
    old_casa_road = tim_agenda.make_l1_road(old_casa_text)
    bloomers_text = "bloomers"
    old_bloomers_road = tim_agenda.make_road(old_casa_road, bloomers_text)
    roses_text = "roses"
    old_roses_road = tim_agenda.make_road(old_bloomers_road, roses_text)
    red_text = "red"
    old_red_road = tim_agenda.make_road(old_roses_road, red_text)

    tim_agenda.add_l1_oath(oathunit_shop(old_casa_text))
    tim_agenda.add_oath(oathunit_shop(bloomers_text), parent_road=old_casa_road)
    tim_agenda.add_oath(oathunit_shop(roses_text), parent_road=old_bloomers_road)
    tim_agenda.add_oath(oathunit_shop(red_text), parent_road=old_roses_road)
    r_oath_roses = tim_agenda.get_oath_obj(old_roses_road)
    r_oath_bloomers = tim_agenda.get_oath_obj(old_bloomers_road)

    assert r_oath_bloomers._kids.get(roses_text) != None
    assert r_oath_roses._parent_road == old_bloomers_road
    assert r_oath_roses._kids.get(red_text) != None
    r_oath_red = r_oath_roses._kids.get(red_text)
    assert r_oath_red._parent_road == old_roses_road

    # WHEN
    new_casa_text = "globe"
    new_casa_road = tim_agenda.make_l1_road(new_casa_text)
    tim_agenda.edit_oath_label(old_road=old_casa_road, new_label=new_casa_text)

    # THEN
    assert tim_agenda._oathroot._kids.get(new_casa_text) != None
    assert tim_agenda._oathroot._kids.get(old_casa_text) is None

    assert r_oath_bloomers._parent_road == new_casa_road
    assert r_oath_bloomers._kids.get(roses_text) != None

    r_oath_roses = r_oath_bloomers._kids.get(roses_text)
    new_bloomers_road = tim_agenda.make_road(new_casa_road, bloomers_text)
    assert r_oath_roses._parent_road == new_bloomers_road
    assert r_oath_roses._kids.get(red_text) != None
    r_oath_red = r_oath_roses._kids.get(red_text)
    new_roses_road = tim_agenda.make_road(new_bloomers_road, roses_text)
    assert r_oath_red._parent_road == new_roses_road


def test_agenda_edit_oath_label_Modifies_beliefunits():
    # GIVEN agenda with beliefunits that will be different
    tim_text = "Tim"
    tim_agenda = agendaunit_shop(tim_text)

    casa_text = "casa"
    casa_road = tim_agenda.make_l1_road(casa_text)
    bloomers_text = "bloomers"
    bloomers_road = tim_agenda.make_road(casa_road, bloomers_text)
    roses_text = "roses"
    roses_road = tim_agenda.make_road(bloomers_road, roses_text)
    old_water_text = "water"
    old_water_road = tim_agenda.make_l1_road(old_water_text)
    rain_text = "rain"
    old_rain_road = tim_agenda.make_road(old_water_road, rain_text)

    tim_agenda.add_l1_oath(oathunit_shop(casa_text))
    tim_agenda.add_oath(oathunit_shop(roses_text), parent_road=bloomers_road)
    tim_agenda.add_oath(oathunit_shop(rain_text), parent_road=old_water_road)
    tim_agenda.set_belief(base=old_water_road, pick=old_rain_road)

    oath_x = tim_agenda.get_oath_obj(roses_road)
    assert tim_agenda._oathroot._beliefunits[old_water_road] != None
    old_water_rain_beliefunit = tim_agenda._oathroot._beliefunits[old_water_road]
    assert old_water_rain_beliefunit.base == old_water_road
    assert old_water_rain_beliefunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = tim_agenda.make_l1_road(new_water_text)
    tim_agenda.add_l1_oath(oathunit_shop(new_water_text))
    assert tim_agenda._oathroot._beliefunits.get(new_water_road) is None
    tim_agenda.edit_oath_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    assert tim_agenda._oathroot._beliefunits.get(old_water_road) is None
    assert tim_agenda._oathroot._beliefunits.get(new_water_road) != None
    new_water_rain_beliefunit = tim_agenda._oathroot._beliefunits[new_water_road]
    assert new_water_rain_beliefunit.base == new_water_road
    new_rain_road = tim_agenda.make_road(new_water_road, rain_text)
    assert new_water_rain_beliefunit.pick == new_rain_road

    assert tim_agenda._oathroot._beliefunits.get(new_water_road)
    beliefunit_obj = tim_agenda._oathroot._beliefunits.get(new_water_road)
    # for beliefunit_key, beliefunit_obj in tim_agenda._oathroot._beliefunits.items():
    #     assert beliefunit_key == new_water_road
    assert beliefunit_obj.base == new_water_road
    assert beliefunit_obj.pick == new_rain_road


def test_agenda_edit_oath_label_Modifies_oathroot_range_source_road():
    # GIVEN this should never happen but best be thorough
    tim_agenda = agendaunit_shop("Tim")
    old_casa_text = "casa"
    old_casa_road = tim_agenda.make_l1_road(old_casa_text)
    tim_agenda.add_l1_oath(oathunit_shop(old_casa_text))
    tim_agenda.edit_oath_attr(tim_agenda._real_id, range_source_road=old_casa_road)
    assert tim_agenda._oathroot._range_source_road == old_casa_road

    # WHEN
    new_casa_text = "globe"
    tim_agenda.edit_oath_label(old_road=old_casa_road, new_label=new_casa_text)

    # THEN
    new_casa_road = tim_agenda.make_l1_road(new_casa_text)
    assert tim_agenda._oathroot._range_source_road == new_casa_road


def test_agenda_edit_oath_label_ModifiesOathUnitN_range_source_road():
    bob_agenda = agendaunit_shop("Bob")
    casa_text = "casa"
    casa_road = bob_agenda.make_l1_road(casa_text)
    old_water_text = "water"
    old_water_road = bob_agenda.make_road(casa_road, old_water_text)
    rain_text = "rain"
    old_rain_road = bob_agenda.make_road(old_water_road, rain_text)
    mood_text = "mood"
    mood_road = bob_agenda.make_l1_road(mood_text)
    bob_agenda.add_l1_oath(oathunit_shop(casa_text))
    bob_agenda.add_oath(oathunit_shop(old_water_text), parent_road=casa_road)
    bob_agenda.add_oath(oathunit_shop(rain_text), parent_road=old_water_road)
    bob_agenda.add_l1_oath(oathunit_shop(mood_text))

    bob_agenda.edit_oath_attr(road=mood_road, range_source_road=old_rain_road)
    mood_oath = bob_agenda.get_oath_obj(mood_road)
    assert mood_oath._range_source_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = bob_agenda.make_road(casa_road, new_water_text)
    new_rain_road = bob_agenda.make_road(new_water_road, rain_text)
    bob_agenda.edit_oath_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    # for oath_x in bob_agenda._oathroot._kids.values():
    #     print(f"{oath_x._parent_road=} {oath_x._label=}")
    #     for oath_y in oath_x._kids.values():
    #         print(f"{oath_y._parent_road=} {oath_y._label=}")
    #         for oath_z in oath_y._kids.values():
    #             print(f"{oath_z._parent_road=} {oath_z._label=}")
    assert old_rain_road != new_rain_road
    assert mood_oath._range_source_road == new_rain_road


def test_agenda_edit_oath_label_ModifiesOathReasonUnitsScenario1():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons_2beliefs()
    old_weekday_text = "weekdays"
    old_weekday_road = sue_agenda.make_l1_road(old_weekday_text)
    wednesday_text = "Wednesday"
    old_wednesday_road = sue_agenda.make_road(old_weekday_road, wednesday_text)
    casa_oath = sue_agenda.get_oath_obj(sue_agenda.make_l1_road("casa"))
    # casa_wk_reason = reasonunit_shop(weekday, premises={wed_premise.need: wed_premise})
    # nation_reason = reasonunit_shop(nationstate, premises={usa_premise.need: usa_premise})
    assert len(casa_oath._reasonunits) == 2
    assert casa_oath._reasonunits.get(old_weekday_road) != None
    wednesday_oath = sue_agenda.get_oath_obj(old_weekday_road)
    casa_weekday_reason = casa_oath._reasonunits.get(old_weekday_road)
    assert casa_weekday_reason.premises.get(old_wednesday_road) != None
    assert (
        casa_weekday_reason.premises.get(old_wednesday_road).need == old_wednesday_road
    )
    new_weekday_text = "days of week"
    new_weekday_road = sue_agenda.make_l1_road(new_weekday_text)
    new_wednesday_road = sue_agenda.make_road(new_weekday_road, wednesday_text)
    assert casa_oath._reasonunits.get(new_weekday_text) is None

    # WHEN
    # for key_x, reason_x in casa_oath._reasonunits.items():
    #     print(f"Before {key_x=} {reason_x.base=}")
    print(f"BEFORE {wednesday_oath._label=}")
    print(f"BEFORE {wednesday_oath._parent_road=}")
    sue_agenda.edit_oath_label(old_road=old_weekday_road, new_label=new_weekday_text)
    # for key_x, reason_x in casa_oath._reasonunits.items():
    #     print(f"AFTER {key_x=} {reason_x.base=}")
    print(f"AFTER {wednesday_oath._label=}")
    print(f"AFTER {wednesday_oath._parent_road=}")

    # THEN
    assert casa_oath._reasonunits.get(new_weekday_road) != None
    assert casa_oath._reasonunits.get(old_weekday_road) is None
    casa_weekday_reason = casa_oath._reasonunits.get(new_weekday_road)
    assert casa_weekday_reason.premises.get(new_wednesday_road) != None
    assert (
        casa_weekday_reason.premises.get(new_wednesday_road).need == new_wednesday_road
    )
    assert len(casa_oath._reasonunits) == 2


def test_agenda_set_owner_id_CorrectlyModifiesBoth():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons_2beliefs()
    assert sue_agenda._owner_id == "Sue"
    assert sue_agenda._oathroot._label == sue_agenda._real_id
    # mid_label1 = "Tim"
    # sue_agenda.edit_oath_label(old_road=old_label, new_label=mid_label1)
    # assert sue_agenda._owner_id == old_label
    # assert sue_agenda._oathroot._label == mid_label1

    # WHEN
    bob_text = "Bob"
    sue_agenda.set_owner_id(new_owner_id=bob_text)

    # THEN
    assert sue_agenda._owner_id == bob_text
    assert sue_agenda._oathroot._label == sue_agenda._real_id


def test_agenda_edit_oath_label_RaisesErrorIfdelimiterIsInLabel():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons_2beliefs()
    old_weekday_text = "weekdays"
    old_weekday_road = sue_agenda.make_l1_road(old_weekday_text)

    # WHEN / THEN
    new_weekday_text = "days, of week"
    with pytest_raises(Exception) as excinfo:
        sue_agenda.edit_oath_label(
            old_road=old_weekday_road, new_label=new_weekday_text
        )
    assert (
        str(excinfo.value)
        == f"Cannot modify '{old_weekday_road}' because new_label {new_weekday_text} contains delimiter {sue_agenda._road_delimiter}"
    )


def test_agenda_set_road_delimiter_RaisesErrorIfNew_delimiter_IsAnOath_label():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    print(f"{luca_agenda._max_tree_traverse=}")
    casa_text = "casa"
    casa_road = luca_agenda.make_l1_road(casa_text)
    luca_agenda.add_l1_oath(oathunit_shop(casa_text))
    slash_text = "/"
    home_text = f"home cook{slash_text}clean"
    luca_agenda.add_oath(oathunit_shop(home_text), parent_road=casa_road)

    # WHEN / THEN
    home_road = luca_agenda.make_road(casa_road, home_text)
    print(f"{home_road=}")
    with pytest_raises(Exception) as excinfo:
        luca_agenda.set_road_delimiter(slash_text)
    assert (
        str(excinfo.value)
        == f"Cannot modify delimiter to '{slash_text}' because it already exists an oath label '{home_road}'"
    )


def test_agenda_set_road_delimiter_CorrectlyModifies_parent_road():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    casa_text = "casa"
    luca_agenda.add_l1_oath(oathunit_shop(casa_text))
    comma_casa_road = luca_agenda.make_l1_road(casa_text)
    cook_text = "cook"
    luca_agenda.add_oath(oathunit_shop(cook_text), parent_road=comma_casa_road)
    comma_cook_road = luca_agenda.make_road(comma_casa_road, cook_text)
    cook_oath = luca_agenda.get_oath_obj(comma_cook_road)
    comma_text = ","
    assert luca_agenda._road_delimiter == comma_text
    comma_cook_road = luca_agenda.make_road(comma_casa_road, cook_text)
    # print(f"{luca_agenda._real_id=} {luca_agenda._oathroot._label=} {casa_road=}")
    # print(f"{cook_oath._parent_road=} {cook_oath._label=}")
    # comma_casa_oath = luca_agenda.get_oath_obj(comma_casa_road)
    # print(f"{comma_casa_oath._parent_road=} {comma_casa_oath._label=}")
    assert cook_oath.get_road() == comma_cook_road

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_delimiter(slash_text)

    # THEN
    assert cook_oath.get_road() != comma_cook_road
    luca_real_id = luca_agenda._real_id
    slash_casa_road = create_road(luca_real_id, casa_text, delimiter=slash_text)
    slash_cook_road = create_road(slash_casa_road, cook_text, delimiter=slash_text)
    assert cook_oath.get_road() == slash_cook_road


def test_agenda_set_road_delimiter_CorrectlyModifiesReasonUnit():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    casa_text = "casa"
    luca_agenda.add_l1_oath(oathunit_shop(casa_text))
    time_text = "time"
    comma_time_road = luca_agenda.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = luca_agenda.make_road(comma_time_road, _8am_text)

    comma_time_reasonunit = reasonunit_shop(base=comma_time_road)
    comma_time_reasonunit.set_premise(comma_8am_road)

    comma_casa_road = luca_agenda.make_l1_road(casa_text)
    luca_agenda.edit_oath_attr(road=comma_casa_road, reason=comma_time_reasonunit)
    casa_oath = luca_agenda.get_oath_obj(comma_casa_road)
    assert casa_oath._reasonunits.get(comma_time_road) != None
    gen_time_reasonunit = casa_oath._reasonunits.get(comma_time_road)
    assert gen_time_reasonunit.premises.get(comma_8am_road) != None

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_delimiter(slash_text)

    # THEN
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_8am_road = luca_agenda.make_road(slash_time_road, _8am_text)
    slash_casa_road = luca_agenda.make_l1_road(casa_text)
    casa_oath = luca_agenda.get_oath_obj(slash_casa_road)
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_8am_road = luca_agenda.make_road(slash_time_road, _8am_text)
    assert casa_oath._reasonunits.get(slash_time_road) != None
    gen_time_reasonunit = casa_oath._reasonunits.get(slash_time_road)
    assert gen_time_reasonunit.premises.get(slash_8am_road) != None

    assert casa_oath._reasonunits.get(comma_time_road) is None
    assert gen_time_reasonunit.premises.get(comma_8am_road) is None


def test_agenda_set_road_delimiter_CorrectlyModifiesBeliefUnit():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    casa_text = "casa"
    luca_agenda.add_l1_oath(oathunit_shop(casa_text))
    time_text = "time"
    comma_time_road = luca_agenda.make_l1_road(time_text)
    _8am_text = "8am"
    comma_8am_road = luca_agenda.make_road(comma_time_road, _8am_text)
    comma_time_beliefunit = beliefunit_shop(comma_time_road, comma_8am_road)

    comma_casa_road = luca_agenda.make_l1_road(casa_text)
    luca_agenda.edit_oath_attr(comma_casa_road, beliefunit=comma_time_beliefunit)
    casa_oath = luca_agenda.get_oath_obj(comma_casa_road)
    print(f"{casa_oath._beliefunits=} {comma_time_road=}")
    assert casa_oath._beliefunits.get(comma_time_road) != None
    gen_time_beliefunit = casa_oath._beliefunits.get(comma_time_road)

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_delimiter(slash_text)

    # THEN
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_casa_road = luca_agenda.make_l1_road(casa_text)
    casa_oath = luca_agenda.get_oath_obj(slash_casa_road)
    slash_time_road = luca_agenda.make_l1_road(time_text)
    slash_8am_road = luca_agenda.make_road(slash_time_road, _8am_text)
    assert casa_oath._beliefunits.get(slash_time_road) != None
    gen_time_beliefunit = casa_oath._beliefunits.get(slash_time_road)
    assert gen_time_beliefunit.base != None
    assert gen_time_beliefunit.base == slash_time_road
    assert gen_time_beliefunit.pick != None
    assert gen_time_beliefunit.pick == slash_8am_road

    assert casa_oath._beliefunits.get(comma_time_road) is None


def test_agenda_set_road_delimiter_CorrectlyModifies_numeric_roadAND_range_source_road():
    # GIVEN
    luca_agenda = agendaunit_shop("Luca", "Texas")
    casa_text = "casa"
    luca_agenda.add_l1_oath(oathunit_shop(casa_text))
    comma_casa_road = luca_agenda.make_l1_road(casa_text)
    cook_text = "cook"
    luca_agenda.add_oath(oathunit_shop(cook_text), parent_road=comma_casa_road)
    comma_cook_road = luca_agenda.make_road(comma_casa_road, cook_text)

    # numeric_road
    taste_text = "foot taste"
    luca_agenda.add_l1_oath(oathunit_shop(taste_text, _begin=0, _close=6))
    comma_taste_road = luca_agenda.make_l1_road(taste_text)
    luca_agenda.edit_oath_attr(comma_cook_road, numeric_road=comma_taste_road)

    # range_source
    heat_text = "heat numbers"
    luca_agenda.add_l1_oath(oathunit_shop(heat_text, _begin=0, _close=6))
    comma_heat_road = luca_agenda.make_l1_road(heat_text)
    luca_agenda.edit_oath_attr(comma_cook_road, range_source_road=comma_heat_road)

    cook_oath = luca_agenda.get_oath_obj(comma_cook_road)
    assert cook_oath._numeric_road == comma_taste_road
    assert cook_oath._range_source_road == comma_heat_road

    # WHEN
    slash_text = "/"
    luca_agenda.set_road_delimiter(slash_text)

    # THEN
    slash_taste_road = luca_agenda.make_l1_road(taste_text)
    assert cook_oath._numeric_road != comma_taste_road
    assert cook_oath._numeric_road == slash_taste_road
    slash_heat_road = luca_agenda.make_l1_road(heat_text)
    assert cook_oath._range_source_road != comma_heat_road
    assert cook_oath._range_source_road == slash_heat_road
