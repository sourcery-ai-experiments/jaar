from src.agenda.road import get_road
from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideacore_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels_and_2requireds_2acptfacts,
)
from pytest import raises as pytest_raises
from src.agenda.required_idea import AcptFactUnit
from src.agenda.road import get_default_culture_root_label as root_label


def test_idea_label_fails_when_idea_does_not_exist():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)

    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)
    swim_text = "swim"
    x_agenda.add_idea(
        pad=x_agenda._culture_qid, idea_kid=ideacore_shop(_label=work_text)
    )
    x_agenda.add_idea(pad=work_road, idea_kid=ideacore_shop(_label=swim_text))

    # WHEN / THEN
    no_idea_road = get_road(x_agenda._culture_qid, "bees")
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_label(old_road=no_idea_road, new_label="pigeons")
    assert (
        str(excinfo.value)
        == f"Getting idea_label='bees' failed no item at '{no_idea_road}'"
    )


def test_Agenda_level0_idea_edit_idea_label_RaisesError_culture_qid_IsNone():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)
    swim_text = "swim"
    swim_road = get_road(work_road, swim_text)
    x_agenda.add_idea(
        pad=x_agenda._culture_qid, idea_kid=ideacore_shop(_label=work_text)
    )
    x_agenda.add_idea(pad=work_road, idea_kid=ideacore_shop(_label=swim_text))
    assert x_agenda._healer == healer_text
    assert x_agenda._culture_qid == x_agenda._culture_qid
    assert x_agenda._idearoot._label == x_agenda._culture_qid
    work_idea = x_agenda.get_idea_kid(work_road)
    assert work_idea._pad == x_agenda._culture_qid
    swim_idea = x_agenda.get_idea_kid(swim_road)
    assert swim_idea._pad == work_road

    # WHEN

    with pytest_raises(Exception) as excinfo:
        moon_text = "moon"
        x_agenda.edit_idea_label(old_road=x_agenda._culture_qid, new_label=moon_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{x_agenda._culture_qid}'"
    )


def test_Agenda_level0_idea_edit_idea_label_RaisesError_culture_qid_IsDifferent():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)
    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)
    swim_text = "swim"
    swim_road = get_road(work_road, swim_text)
    x_agenda.add_idea(
        pad=x_agenda._culture_qid, idea_kid=ideacore_shop(_label=work_text)
    )
    x_agenda.add_idea(pad=work_road, idea_kid=ideacore_shop(_label=swim_text))
    sun_text = "sun"
    x_agenda._culture_qid = sun_text
    assert x_agenda._healer == healer_text
    assert x_agenda._culture_qid == sun_text
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


def test_agenda_set_culture_qid_CorrectlySetsAttr():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)
    work_text = "work"
    old_work_road = get_road(x_agenda._culture_qid, work_text)
    swim_text = "swim"
    old_swim_road = get_road(old_work_road, swim_text)
    x_agenda.add_idea(
        pad=x_agenda._culture_qid, idea_kid=ideacore_shop(_label=work_text)
    )
    x_agenda.add_idea(pad=old_work_road, idea_kid=ideacore_shop(_label=swim_text))
    assert x_agenda._healer == healer_text
    assert x_agenda._idearoot._label == x_agenda._culture_qid
    work_idea = x_agenda.get_idea_kid(old_work_road)
    assert work_idea._pad == x_agenda._culture_qid
    swim_idea = x_agenda.get_idea_kid(old_swim_road)
    assert swim_idea._pad == old_work_road
    assert x_agenda._culture_qid == x_agenda._culture_qid

    # WHEN
    culture_qid_text = "Sun"
    x_agenda.set_culture_qid(culture_qid=culture_qid_text)

    # THEN
    new_work_road = get_road(culture_qid_text, work_text)
    swim_text = "swim"
    new_swim_road = get_road(new_work_road, swim_text)
    assert x_agenda._culture_qid == culture_qid_text
    assert x_agenda._idearoot._label == culture_qid_text
    work_idea = x_agenda.get_idea_kid(new_work_road)
    assert work_idea._pad == culture_qid_text
    swim_idea = x_agenda.get_idea_kid(new_swim_road)
    assert swim_idea._pad == new_work_road


def test_idea_find_replace_road_Changes_kids_scenario1():
    # GIVEN Idea with kids that will be changed
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    old_healer_text = "healer"
    old_healer_road = get_road(x_agenda._culture_qid, old_healer_text)
    bloomers_text = "bloomers"
    old_bloomers_road = get_road(old_healer_road, bloomers_text)
    roses_text = "roses"
    old_roses_road = get_road(old_bloomers_road, roses_text)
    red_text = "red"
    old_red_road = get_road(old_roses_road, red_text)

    x_agenda.add_idea(ideacore_shop(old_healer_text), pad=x_agenda._culture_qid)
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
    new_healer_road = get_road(x_agenda._culture_qid, new_healer_text)
    x_agenda.edit_idea_label(old_road=old_healer_road, new_label=new_healer_text)

    # THEN
    assert x_agenda._idearoot._kids.get(new_healer_text) != None
    assert x_agenda._idearoot._kids.get(old_healer_text) is None

    assert r_idea_bloomers._pad == new_healer_road
    assert r_idea_bloomers._kids.get(roses_text) != None

    r_idea_roses = r_idea_bloomers._kids.get(roses_text)
    new_bloomers_road = get_road(new_healer_road, bloomers_text)
    assert r_idea_roses._pad == new_bloomers_road
    assert r_idea_roses._kids.get(red_text) != None
    r_idea_red = r_idea_roses._kids.get(red_text)
    new_roses_road = get_road(new_bloomers_road, roses_text)
    assert r_idea_red._pad == new_roses_road


def test_agenda_edit_idea_label_Changes_acptfactunits():
    # GIVEN agenda with acptfactunits that will be changed
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    healer_text = "healer"
    healer_road = get_road(x_agenda._culture_qid, healer_text)
    bloomers_text = "bloomers"
    bloomers_road = get_road(healer_road, bloomers_text)
    roses_text = "roses"
    roses_road = get_road(bloomers_road, roses_text)
    old_water_text = "water"
    old_water_road = get_road(x_agenda._culture_qid, old_water_text)
    rain_text = "rain"
    old_rain_road = get_road(old_water_road, rain_text)

    x_agenda.add_idea(ideacore_shop(healer_text), pad=x_agenda._culture_qid)
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
    new_water_road = get_road(x_agenda._culture_qid, new_water_text)
    x_agenda.add_idea(ideacore_shop(new_water_text), pad=x_agenda._culture_qid)
    assert x_agenda._idearoot._acptfactunits.get(new_water_road) is None
    x_agenda.edit_idea_label(old_road=old_water_road, new_label=new_water_text)

    # THEN
    assert x_agenda._idearoot._acptfactunits.get(old_water_road) is None
    assert x_agenda._idearoot._acptfactunits.get(new_water_road) != None
    new_water_rain_acptfactunit = x_agenda._idearoot._acptfactunits[new_water_road]
    assert new_water_rain_acptfactunit.base == new_water_road
    new_rain_road = get_road(new_water_road, rain_text)
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
    old_healer_road = get_road(x_agenda._culture_qid, old_healer_text)
    x_agenda.add_idea(ideacore_shop(old_healer_text), pad=x_agenda._culture_qid)
    x_agenda.edit_idea_attr(x_agenda._culture_qid, range_source_road=old_healer_road)
    assert x_agenda._idearoot._range_source_road == old_healer_road

    # WHEN
    new_healer_text = "globe"
    x_agenda.edit_idea_label(old_road=old_healer_road, new_label=new_healer_text)

    # THEN
    new_healer_road = get_road(x_agenda._culture_qid, new_healer_text)
    assert x_agenda._idearoot._range_source_road == new_healer_road


def test_agenda_edit_idea_label_ChangesIdeaKidN_range_source_road():
    healer_text = "Bob"
    x_agenda = agendaunit_shop(_healer=healer_text)

    healer_text = "healer"
    healer_road = get_road(x_agenda._culture_qid, healer_text)
    old_water_text = "water"
    old_water_road = get_road(healer_road, old_water_text)
    rain_text = "rain"
    old_rain_road = get_road(old_water_road, rain_text)
    mood_text = "mood"
    mood_road = get_road(x_agenda._culture_qid, mood_text)
    x_agenda.add_idea(
        pad=x_agenda._culture_qid, idea_kid=ideacore_shop(_label=healer_text)
    )
    x_agenda.add_idea(pad=healer_road, idea_kid=ideacore_shop(_label=old_water_text))
    x_agenda.add_idea(pad=old_water_road, idea_kid=ideacore_shop(_label=rain_text))
    x_agenda.add_idea(
        pad=x_agenda._culture_qid, idea_kid=ideacore_shop(_label=mood_text)
    )

    x_agenda.edit_idea_attr(road=mood_road, range_source_road=old_rain_road)
    mood_idea = x_agenda.get_idea_kid(mood_road)
    assert mood_idea._range_source_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = get_road(healer_road, new_water_text)
    new_rain_road = get_road(new_water_road, rain_text)
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
    old_weekday_road = get_road(x_agenda._culture_qid, old_weekday_text)
    wednesday_text = "Wednesday"
    old_wednesday_road = get_road(old_weekday_road, wednesday_text)
    work_idea = x_agenda.get_idea_kid(get_road(x_agenda._culture_qid, "work"))
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
    new_weekday_road = get_road(x_agenda._culture_qid, new_weekday_text)
    new_wednesday_road = get_road(new_weekday_road, wednesday_text)
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
    assert x_agenda._idearoot._label == x_agenda._culture_qid
    # mid_label1 = "tim"
    # x_agenda.edit_idea_label(old_road=old_label, new_label=mid_label1)
    # assert x_agenda._healer == old_label
    # assert x_agenda._idearoot._label == mid_label1

    # WHEN
    new_label2 = "bob"
    x_agenda.set_healer(new_healer=new_label2)

    # THEN
    assert x_agenda._healer == new_label2
    assert x_agenda._idearoot._label == x_agenda._culture_qid


def test_agenda_edit_idea_label_RaisesErrorIfSeparatorIsInLabel():
    # GIVEN
    x_agenda = get_agenda_with_4_levels_and_2requireds_2acptfacts()
    old_weekday_text = "weekdays"
    old_weekday_road = get_road(x_agenda._culture_qid, old_weekday_text)

    # WHEN / THEN
    new_weekday_text = "days, of week"
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_label(old_road=old_weekday_road, new_label=new_weekday_text)
    assert (
        str(excinfo.value)
        == f"Cannot change '{old_weekday_road}' because new_label {new_weekday_text} contains separator {x_agenda._road_node_separator}"
    )
