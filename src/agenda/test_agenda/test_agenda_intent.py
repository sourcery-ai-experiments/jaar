from datetime import datetime
from src._prime.road import RoadUnit
from src.agenda.agenda import agendaunit_shop, get_from_json
from src.agenda.examples.agenda_env import get_agenda_examples_dir
from src.agenda.idea import IdeaUnit, ideaunit_shop
from src.agenda.reason_idea import reasonunit_shop
from src.agenda.group import groupunit_shop, balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_assign import assigned_unit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_with_4_levels_and_2reasons as example_agendas_get_agenda_with_4_levels_and_2reasons,
    get_agenda_with7amCleanTableReason as example_agendas_get_agenda_with7amCleanTableReason,
    get_agenda_with_4_levels_and_2reasons_2beliefs as example_agendas_get_agenda_with_4_levels_and_2reasons_2beliefs,
    agenda_v001 as example_agendas_agenda_v001,
    agenda_v001_with_large_intent as example_agendas_agenda_v001_with_large_intent,
    agenda_v002 as example_agendas_agenda_v002,
    yr_explanation,
)
from src.instrument.file import open_file


def test_get_intent_dict_ReturnsCorrectObj():
    # GIVEN
    bob_agenda = example_agendas_get_agenda_with_4_levels()

    # WHEN
    intent_dict = bob_agenda.get_intent_dict()

    # THEN
    assert intent_dict
    assert len(intent_dict) == 2
    print(f"{intent_dict.keys()=}")
    assert bob_agenda.make_l1_road("work") in intent_dict.keys()
    assert bob_agenda.make_l1_road("feed cat") in intent_dict.keys()


def test_agenda_get_intent_dict_ReturnsIntentWithOnlyCorrectItems():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = x_agenda.make_road(week_road, sun_text)
    x_agenda.set_belief(base=week_road, pick=sun_road)

    # WHEN
    intent_dict = x_agenda.get_intent_dict()

    # THEN
    assert intent_dict
    # for intent_item in intent_dict:
    #     yr_explanation(idea=intent_item)
    # yr_explanation(idea=intent_dict[0])

    assert len(intent_dict) == 1
    print(f"{intent_dict=}")
    assert x_agenda.make_l1_road("feed cat") in intent_dict.keys()


def test_get_intent_returns_intent_WithAgendaImportance():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels_and_2reasons_2beliefs()

    # WHEN
    intent_dict = x_agenda.get_intent_dict()

    # THEN
    assert intent_dict
    assert len(intent_dict) == 2
    assert intent_dict.get(x_agenda.make_l1_road("feed cat"))._agenda_importance

    work_text = "work"
    print(f"{intent_dict.keys()=} {x_agenda.make_l1_road(work_text)=}")
    print(f"{intent_dict.get(x_agenda.make_l1_road(work_text))._label=}")
    assert intent_dict.get(x_agenda.make_l1_road(work_text))._agenda_importance


def test_get_intent_with_No7amItem():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with7amCleanTableReason()

    # WHEN
    intent_dict = x_agenda.get_intent_dict()

    # THEN
    assert intent_dict
    assert len(intent_dict) == 1
    clean_text = "clean table"
    print(f"{intent_dict.keys()=} {x_agenda.make_l1_road(clean_text)=}")
    # print(f"{intent_dict[0]._label=}")
    assert len(intent_dict) == 1

    cat_text = "feed cat"
    cat_intent_item = intent_dict.get(x_agenda.make_l1_road(cat_text))
    assert cat_intent_item._label != clean_text


def test_get_intent_with_7amItem():
    # GIVEN
    # set beliefs as midnight to 8am
    x_agenda = example_agendas_get_agenda_with7amCleanTableReason()
    print(f"{len(x_agenda.get_intent_dict())=}")
    assert len(x_agenda.get_intent_dict()) == 1

    # WHEN
    timetech_road = x_agenda.make_l1_road("timetech")
    day24hr_road = x_agenda.make_road(timetech_road, "24hr day")
    day24hr_open = 0.0
    day24hr_nigh = 8.0
    housework_text = "housework"
    housework_road = x_agenda.make_l1_road(housework_text)
    clean_text = "clean table"
    clean_road = x_agenda.make_road(housework_road, clean_text)
    x_agenda.set_belief(
        base=day24hr_road, pick=day24hr_road, open=day24hr_open, nigh=day24hr_nigh
    )
    print(x_agenda._idearoot._beliefunits[day24hr_road])
    print(x_agenda._idearoot._kids[housework_text]._kids[clean_text]._reasonunits)
    print(x_agenda._idearoot._kids[housework_text]._kids[clean_text]._active)

    # THEN
    intent_dict = x_agenda.get_intent_dict()
    print(f"{len(intent_dict)=} {intent_dict.keys()=}")
    assert len(intent_dict) == 6
    clean_item = intent_dict.get(clean_road)
    assert clean_item._label == clean_text


def test_get_intent_does_not_return_promise_items_outside_range():
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.set_time_hreg_ideas(c400_count=7)
    clean_text = "clean"
    clean_road = zia_agenda.make_l1_road(clean_text)
    zia_agenda.add_l1_idea(ideaunit_shop(clean_text, promise=True))
    time_road = zia_agenda.make_l1_road("time")
    jajatime_road = zia_agenda.make_road(time_road, "jajatime")
    jajaday = zia_agenda.make_road(jajatime_road, "day")

    zia_agenda.edit_idea_attr(
        road=clean_road,
        reason_base=jajatime_road,
        reason_premise=jajaday,
        begin=480,
        close=480,
    )

    open_x = 1063971180
    nigh_x1 = 2063971523
    zia_agenda.set_belief(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x1)

    intent_dict = zia_agenda.get_intent_dict()
    print(f"{intent_dict.keys()=}")
    assert len(intent_dict) == 1
    assert clean_road in intent_dict.keys()

    nigh_x2 = 1063971923
    zia_agenda.set_belief(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x2)

    intent_dict = zia_agenda.get_intent_dict()
    assert len(intent_dict) == 0


def test_example_agendas_agenda_v001_IntentExists():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    min_text = "day_minute"
    min_road = x_agenda.make_l1_road(min_text)
    x_agenda.set_belief(base=min_road, pick=min_road, open=0, nigh=1399)
    assert x_agenda
    # for idea_kid in x_agenda._idearoot._kids.values():
    #     # print(idea_kid._label)
    #     assert str(type(idea_kid)) != "<class 'str'>"
    #     assert idea_kid.promise != None

    # WHEN
    intent_dict = x_agenda.get_intent_dict()

    # THEN
    assert len(intent_dict) > 0
    assert len(intent_dict) == 17
    # assert intent_dict[0].promise != None
    # assert str(type(intent_dict[0])) != "<class 'str'>"
    # assert str(type(intent_dict[9])) != "<class 'str'>"
    # assert str(type(intent_dict[12])) != "<class 'str'>"


def test_exammple_AgendaHasCorrectAttributes():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()

    day_min_text = "day_minute"
    day_min_road = x_agenda.make_l1_road(day_min_text)
    x_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=1399)
    month_week_text = "month_week"
    month_week_road = x_agenda.make_l1_road(month_week_text)
    nations_text = "Nation-States"
    nations_road = x_agenda.make_l1_road(nations_text)
    mood_text = "Moods"
    mood_road = x_agenda.make_l1_road(mood_text)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = x_agenda.make_l1_road(aaron_text)
    # internet_text = "Internet"
    # internet_road = x_agenda.make_l1_road(internet_text)
    year_month_text = "year_month"
    year_month_road = x_agenda.make_l1_road(year_month_text)
    x_agenda.set_belief(base=month_week_road, pick=month_week_road)
    x_agenda.set_belief(base=nations_road, pick=nations_road)
    x_agenda.set_belief(base=mood_road, pick=mood_road)
    x_agenda.set_belief(base=aaron_road, pick=aaron_road)
    # x_agenda.set_belief(base=internet_road, pick=internet_road)
    x_agenda.set_belief(base=year_month_road, pick=year_month_road)
    # season_text = "Seasons"
    # season_road = x_agenda.make_l1_road(season_text)
    # x_agenda.set_belief(base=season_road, pick=season_road)
    ced_week_text = "ced_week"
    ced_week_road = x_agenda.make_l1_road(ced_week_text)
    x_agenda.set_belief(base=ced_week_road, pick=ced_week_road)
    # water_text = "WaterExistence"
    # water_road = x_agenda.make_l1_road(water_text)
    # x_agenda.set_belief(base=water_road, pick=water_road)
    # movie_text = "No Movie playing"
    # movie_road = x_agenda.make_l1_road(movie_text)
    # x_agenda.set_belief(base=movie_road, pick=movie_text)

    # WHEN
    idea_action_list = x_agenda.get_intent_dict()

    # THEN
    assert len(idea_action_list) == 27

    week1_road = x_agenda.make_road(month_week_road, "1st week")
    x_agenda.set_belief(month_week_road, week1_road)
    idea_action_list = x_agenda.get_intent_dict()
    assert len(idea_action_list) == 27

    weekday_text = "weekdays"
    weekday_road = x_agenda.make_l1_road(weekday_text)
    monday_text = "Monday"
    monday_road = x_agenda.make_road(weekday_road, monday_text)

    x_agenda.set_belief(base=weekday_road, pick=monday_road)
    idea_action_list = x_agenda.get_intent_dict()
    assert len(idea_action_list) == 39

    x_agenda.set_belief(base=weekday_road, pick=weekday_road)
    idea_action_list = x_agenda.get_intent_dict()
    assert len(idea_action_list) == 53

    # x_agenda.set_belief(base=nations_road, pick=nations_road)
    # idea_action_list = x_agenda.get_intent_dict()
    # assert len(idea_action_list) == 53

    # for base in x_agenda.get_missing_belief_bases():
    #     print(f"{base=}")

    # for intent_item in idea_action_list:
    #     print(f"{intent_item._uid=} {intent_item._parent_road=}")

    # for intent_item in idea_action_list:
    #     # print(f"{intent_item._parent_road=}")
    #     pass

    print(len(idea_action_list))


def test_exammple_AgendaCanFiltersOnBase():
    # GIVEN
    x_agenda = example_agendas_agenda_v001_with_large_intent()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    print(f"{type(x_agenda)=}")
    # for base in x_agenda.get_missing_belief_bases():
    #     print(f"{base=}")

    # for intent_item in x_agenda.get_intent_dict():
    #     print(
    #         f"{intent_item._parent_road=} {intent_item._label} {len(intent_item._reasonunits)=}"
    #     )
    #     for reason in intent_item._reasonunits.values():
    #         if reason.base == weekdays:
    #             print(f"         {weekdays}")

    # this list went from 68 to 63 when the method of identifying activees was improved.
    assert len(x_agenda.get_intent_dict()) == 63

    # WHEN
    action_list = x_agenda.get_intent_dict(base=week_road)

    # THEN
    assert len(action_list) != 63
    # this list went from 28 to 29 when the method of identifying activees was improved.
    assert len(action_list) == 29


def test_set_intent_task_as_complete_RangeWorksCorrectly():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    run_text = "run"
    run_road = zia_agenda.make_l1_road(run_text)
    time_road = zia_agenda.make_l1_road("time")
    day_text = "day"
    day_road = zia_agenda.make_road(time_road, day_text)

    zia_agenda.add_l1_idea(ideaunit_shop(run_text, promise=True))
    zia_agenda.add_idea(ideaunit_shop(day_text, _begin=0, _close=500), time_road)
    zia_agenda.edit_idea_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=25,
        reason_premise_nigh=81,
    )
    zia_agenda.set_belief(base=day_road, pick=day_road, open=30, nigh=87)
    zia_agenda.get_intent_dict()
    run_reasonunits = zia_agenda._idearoot._kids[run_text]._reasonunits[day_road]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.premises[day_road]._status=}")
    print(f"{run_reasonunits.premises[day_road]._task=}")
    print(f"{zia_agenda.get_reason_bases()=}")
    assert len(zia_agenda.get_idea_dict()) == 4
    assert len(zia_agenda.get_intent_dict()) == 1
    print(f"{zia_agenda.get_intent_dict().keys()=}")
    assert zia_agenda.get_intent_dict().get(run_road)._task == True

    # WHEN
    zia_agenda.set_intent_task_complete(task_road=run_road, base=day_road)

    # THEN
    intent_dict = zia_agenda.get_intent_dict()
    assert len(intent_dict) == 0
    assert intent_dict == {}


def test_set_intent_task_as_complete_DivisionWorksCorrectly():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    run_text = "run"
    run_road = zia_agenda.make_l1_road(run_text)
    time_text = "time"
    time_road = zia_agenda.make_l1_road(time_text)
    day_text = "day"
    day_road = zia_agenda.make_road(time_road, day_text)

    zia_agenda.add_l1_idea(ideaunit_shop(run_text, promise=True))
    zia_agenda.add_idea(ideaunit_shop(day_text, _begin=0, _close=500), time_road)
    zia_agenda.edit_idea_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=1,
        reason_premise_nigh=1,
        reason_premise_divisor=2,
    )

    run_idea = zia_agenda.get_idea_obj(run_road)
    # print(f"{run_idea._beliefheirs=}")
    zia_agenda.set_belief(base=day_road, pick=day_road, open=1, nigh=2)
    assert len(zia_agenda.get_intent_dict()) == 1
    zia_agenda.set_belief(base=day_road, pick=day_road, open=2, nigh=2)
    assert len(zia_agenda.get_intent_dict()) == 0
    zia_agenda.set_belief(base=day_road, pick=day_road, open=400, nigh=400)
    assert len(zia_agenda.get_intent_dict()) == 0
    zia_agenda.set_belief(base=day_road, pick=day_road, open=401, nigh=402)
    assert len(zia_agenda.get_intent_dict()) == 1
    # print(f"{run_idea._beliefheirs=}")
    print(f"{run_idea._beliefunits=}")

    # WHEN
    zia_agenda.set_intent_task_complete(task_road=run_road, base=day_road)
    print(f"{run_idea._beliefunits=}")
    # print(f"{run_idea._beliefheirs=}")
    assert len(zia_agenda.get_intent_dict()) == 0


def test_agenda_get_from_json_CorrectlyLoadsActionFromJSON():
    # GIVEN
    file_dir = get_agenda_examples_dir()
    file_name = "example_agenda1.json"
    x_agenda_json = open_file(dest_dir=file_dir, file_name=file_name)

    # WHEN
    x_agenda = get_from_json(x_agenda_json=x_agenda_json)

    # THEN
    assert len(x_agenda.get_idea_dict()) == 253
    print(f"{len(x_agenda.get_idea_dict())=}")
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    body_text = "workout"
    body_road = x_agenda.make_road(casa_road, body_text)
    veg_text = "cook veggies every morning"
    veg_road = x_agenda.make_road(body_road, veg_text)
    veg_idea = x_agenda.get_idea_obj(veg_road)
    assert not veg_idea._active
    assert veg_idea.promise

    # idea_list = x_agenda.get_idea_dict()
    # action_true_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
    #         assert idea._active in (True, False)
    #     assert idea.promise in (True, False)
    #     # if idea._active == True:
    #     #     print(idea._label)
    #     if idea.promise == True:
    #         action_true_count += 1
    #         # if idea.promise == False:
    #         #     print(f"action is false {idea._label}")
    #         # for reason in idea._reasonunits.values():
    #         #     assert reason._status in (True, False)
    # assert action_true_count > 0

    # WHEN
    day_min_text = "day_minute"
    day_min_road = x_agenda.make_l1_road(day_min_text)
    x_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=1399)

    # THEN
    assert len(x_agenda.get_intent_dict()) > 0


def test_weekdayAgendaItemsCorrectlyReturned():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")
    zia_agenda.set_time_hreg_ideas(c400_count=7)

    things_text = "things to do"
    zia_agenda.add_l1_idea(ideaunit_shop(things_text))
    t_road = zia_agenda.make_l1_road(things_text)
    clean = "clean"
    run = "run"
    swim = "swim"
    jog = "jog"
    veg = "veg"
    lift = "life"
    zia_agenda.add_idea(ideaunit_shop(clean, promise=True), parent_road=t_road)
    zia_agenda.add_idea(ideaunit_shop(run, promise=True), parent_road=t_road)
    zia_agenda.add_idea(ideaunit_shop(swim, promise=True), parent_road=t_road)
    zia_agenda.add_idea(ideaunit_shop(jog, promise=True), parent_road=t_road)
    zia_agenda.add_idea(ideaunit_shop(veg, promise=True), parent_road=t_road)
    zia_agenda.add_idea(ideaunit_shop(lift, promise=True), parent_road=t_road)
    time_text = "time"
    time_road = zia_agenda.make_l1_road(time_text)
    jaja_text = "jajatime"
    jaja_road = zia_agenda.make_road(time_road, jaja_text)
    tech_text = "tech"
    tech_road = zia_agenda.make_road(time_road, tech_text)
    w_road = zia_agenda.make_road(tech_road, "week")
    mon_road = zia_agenda.make_road(w_road, "Monday")
    tue_road = zia_agenda.make_road(w_road, "Tuesday")
    wed_road = zia_agenda.make_road(w_road, "Wednesday")
    thu_road = zia_agenda.make_road(w_road, "Thursday")
    fri_road = zia_agenda.make_road(w_road, "Friday")
    sat_road = zia_agenda.make_road(w_road, "Saturday")
    sun_road = zia_agenda.make_road(w_road, "Sunday")
    t_road = zia_agenda.make_l1_road(things_text)
    c_road = zia_agenda.make_road(t_road, clean)
    r_road = zia_agenda.make_road(t_road, run)
    s_road = zia_agenda.make_road(t_road, swim)
    j_road = zia_agenda.make_road(t_road, jog)
    v_road = zia_agenda.make_road(t_road, veg)
    l_road = zia_agenda.make_road(t_road, lift)

    zia_agenda.edit_idea_attr(c_road, reason_base=tue_road, reason_premise=tue_road)
    zia_agenda.edit_idea_attr(r_road, reason_base=wed_road, reason_premise=wed_road)
    zia_agenda.edit_idea_attr(s_road, reason_base=thu_road, reason_premise=thu_road)
    zia_agenda.edit_idea_attr(j_road, reason_base=fri_road, reason_premise=fri_road)
    zia_agenda.edit_idea_attr(v_road, reason_base=sat_road, reason_premise=sat_road)
    zia_agenda.edit_idea_attr(l_road, reason_base=sun_road, reason_premise=sun_road)

    c_idea = zia_agenda.get_idea_obj(c_road)
    c_reason = c_idea._reasonunits
    # for reason_y in c_reason.values():
    #     for premise_y in reason_y.premises.values():
    #         print(
    #             f"Idea: {c_idea.get_road()}  Reason: {reason_y.base} open:{premise_y.open} nigh:{premise_y.nigh} diff:{premise_y.nigh-premise_y.open}"
    #         )

    # for base, count_x in zia_agenda.get_reason_bases().items():
    #     print(f"Reasons: {base=} Count: {count_x}")

    mon_dt = datetime(2000, 1, 3)
    tue_dt = datetime(2000, 1, 4)
    wed_dt = datetime(2000, 1, 5)
    thu_dt = datetime(2000, 1, 6)
    fri_dt = datetime(2000, 1, 7)
    sat_dt = datetime(2000, 1, 1)
    sun_dt = datetime(2000, 1, 2)
    mon_min = zia_agenda.get_time_min_from_dt(dt=mon_dt)
    tue_min = zia_agenda.get_time_min_from_dt(dt=tue_dt)
    wed_min = zia_agenda.get_time_min_from_dt(dt=wed_dt)
    thu_min = zia_agenda.get_time_min_from_dt(dt=thu_dt)
    fri_min = zia_agenda.get_time_min_from_dt(dt=fri_dt)
    sat_min = zia_agenda.get_time_min_from_dt(dt=sat_dt)
    sun_min = zia_agenda.get_time_min_from_dt(dt=sun_dt)
    assert zia_agenda._idearoot._beliefunits.get(jaja_road) is None

    # WHEN
    print("\nset belief for Sunday")
    zia_agenda.set_belief(base=jaja_road, pick=jaja_road, open=sun_min, nigh=sun_min)
    # for belief in zia_agenda._idearoot._beliefunits.values():
    #     print(f"{belief.base=} (H: {belief.belief}) {belief.=} {belief.open=} {belief.nigh=}")

    # THEN
    assert len(zia_agenda._idearoot._beliefunits) == 7
    print(zia_agenda._idearoot._beliefunits[jaja_road])
    print(zia_agenda._idearoot._beliefunits[sat_road])
    print(zia_agenda._idearoot._beliefunits[sun_road])
    print(zia_agenda._idearoot._beliefunits[tue_road])
    print(zia_agenda._idearoot._beliefunits[wed_road])
    print(zia_agenda._idearoot._beliefunits[thu_road])
    print(zia_agenda._idearoot._beliefunits[fri_road])
    assert zia_agenda._idearoot._beliefunits[sun_road]
    assert zia_agenda._idearoot._beliefunits[sun_road].open == 1440
    assert zia_agenda._idearoot._beliefunits[sun_road].nigh == 1440

    # WHEN
    print("\nset belief for Sat through Monday")
    zia_agenda.set_belief(base=jaja_road, pick=jaja_road, open=sat_min, nigh=mon_min)
    # for belief in zia_agenda._idearoot._beliefunits.values():
    #     print(f"{belief.base=} (H: {belief.belief}) {belief.=} {belief.open=} {belief.nigh=}")

    # THEN
    assert zia_agenda._idearoot._beliefunits[sat_road]
    assert zia_agenda._idearoot._beliefunits[sat_road].open == 0
    assert zia_agenda._idearoot._beliefunits[sat_road].nigh == 1440
    assert zia_agenda._idearoot._beliefunits[sun_road].open == 1440
    assert zia_agenda._idearoot._beliefunits[sun_road].nigh == 2880

    # WHEN
    print("\nset beliefs for Sunday through Friday")
    zia_agenda.set_belief(base=jaja_road, pick=jaja_road, open=sun_min, nigh=fri_min)
    # for belief in zia_agenda._idearoot._beliefunits.values():
    #     print(f"{belief.base=} (H: {belief.belief}) {belief.=} {belief.open=} {belief.nigh=}")

    # THEN
    assert zia_agenda._idearoot._beliefunits[sun_road].open == 1440
    assert zia_agenda._idearoot._beliefunits[sun_road].nigh == 2880

    # # WHEN
    # print("\nset beliefs for 10 day stretch")
    # dayzero_dt = datetime(2010, 1, 3)
    # dayten_dt = datetime(2010, 1, 13)
    # dayzero_min = zia_agenda.get_time_min_from_dt(dt=dayzero_dt)
    # dayten_min = zia_agenda.get_time_min_from_dt(dt=dayten_dt)
    # zia_agenda.set_belief(jaja_road, jaja_road, open=dayzero_min, nigh=dayten_min)
    # for belief in zia_agenda._idearoot._beliefunits.values():
    #     print(f"{belief.base=} (H: {belief.belief}) {belief.=} {belief.open=} {belief.nigh=}")


def test_agenda_create_intent_item_CorrectlyCreatesAllAgendaAttributes():
    # WHEN "I am cleaning the cookery since I'm in the apartment and it's 8am and it's dirty and I'm doing this for my family"

    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    zia_agenda.set_agenda_metrics()
    assert len(zia_agenda._partys) == 0
    assert len(zia_agenda._groups) == 0
    assert len(zia_agenda._idearoot._kids) == 0

    clean_things_text = "cleaning things"
    clean_things_road = zia_agenda.make_l1_road(clean_things_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = zia_agenda.make_road(clean_things_road, clean_cookery_text)
    clean_cookery_idea = ideaunit_shop(
        _label=clean_cookery_text, _parent_road=clean_things_road
    )
    print(f"{clean_cookery_idea.get_road()=}")
    house_text = "house"
    house_road = zia_agenda.make_l1_road(house_text)
    cookery_room_text = "cookery room"
    cookery_room_road = zia_agenda.make_road(house_road, cookery_room_text)
    cookery_dirty_text = "dirty"
    cookery_dirty_road = zia_agenda.make_road(cookery_room_road, cookery_dirty_text)

    # create gregorian timeline
    zia_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = zia_agenda.make_l1_road("time")
    jajatime_road = zia_agenda.make_road(time_road, "jajatime")
    daytime_road = zia_agenda.make_road(jajatime_road, "day")
    open_8am = 480
    nigh_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_road)
    dirty_cookery_reason.set_premise(premise=cookery_dirty_road)
    clean_cookery_idea.set_reasonunit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_road)
    daytime_reason.set_premise(premise=daytime_road, open=open_8am, nigh=nigh_8am)
    clean_cookery_idea.set_reasonunit(reason=daytime_reason)

    # anna_text = "anna"
    # anna_partyunit = partyunit_shop(party_id=anna_text)
    # anna_partylink = partylink_shop(party_id=anna_text)
    # beto_text = "beto"
    # beto_partyunit = partyunit_shop(party_id=beto_text)
    # beto_partylink = partylink_shop(party_id=beto_text)

    family_text = ",family"
    # groupunit_z = groupunit_shop(group_id=family_text)
    # groupunit_z.set_partylink(partylink=anna_partylink)
    # groupunit_z.set_partylink(partylink=beto_partylink)
    balancelink_z = balancelink_shop(group_id=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)

    assert len(zia_agenda._partys) == 0
    assert len(zia_agenda._groups) == 0
    assert len(zia_agenda._idearoot._kids) == 1
    assert zia_agenda.get_idea_obj(daytime_road)._begin == 0
    assert zia_agenda.get_idea_obj(daytime_road)._close == 1440
    print(f"{clean_cookery_idea.get_road()=}")

    # GIVEN
    zia_agenda.set_dominate_promise_idea(idea_kid=clean_cookery_idea)

    # THEN
    # for idea_kid in zia_agenda._idearoot._kids.keys():
    #     print(f"  {idea_kid=}")

    print(f"{clean_cookery_idea.get_road()=}")
    assert zia_agenda.get_idea_obj(clean_cookery_road) != None
    assert zia_agenda.get_idea_obj(clean_cookery_road)._label == clean_cookery_text
    assert zia_agenda.get_idea_obj(clean_cookery_road).promise
    assert len(zia_agenda.get_idea_obj(clean_cookery_road)._reasonunits) == 2
    assert zia_agenda.get_idea_obj(clean_things_road) != None
    assert zia_agenda.get_idea_obj(cookery_room_road) != None
    assert zia_agenda.get_idea_obj(cookery_dirty_road) != None
    assert zia_agenda.get_idea_obj(daytime_road)._begin == 0
    assert zia_agenda.get_idea_obj(daytime_road)._close == 1440
    assert len(zia_agenda._groups) == 1
    assert zia_agenda._groups.get(family_text) != None
    assert zia_agenda._groups.get(family_text)._partys in (None, {})

    assert len(zia_agenda._idearoot._kids) == 3


def get_tasks_count(intent_dict: dict[RoadUnit:IdeaUnit]) -> int:
    return sum(bool(x_ideaunit._task) for x_ideaunit in intent_dict.values())


def test_Isue116Resolved_correctlySetsTaskAsTrue():
    # GIVEN
    bob_agenda = example_agendas_agenda_v002()

    assert len(bob_agenda.get_intent_dict()) == 44
    time_road = bob_agenda.make_l1_road("time")
    jajatime_road = bob_agenda.make_road(time_road, "jajatime")

    # WHEN
    bob_agenda.set_belief(
        base=jajatime_road, pick=jajatime_road, open=1063998720, nigh=1064130373
    )
    action_idea_list = bob_agenda.get_intent_dict()

    # THEN
    assert len(action_idea_list) == 66
    db_road = bob_agenda.make_l1_road("D&B")
    night_text = "late_night_go_to_sleep"
    night_road = bob_agenda.make_road(db_road, night_text)
    night_idea = bob_agenda._idea_dict.get(night_road)
    # for idea_x in bob_agenda.get_intent_dict():
    #     # if idea_x._task != True:
    #     #     print(f"{len(action_idea_list)=} {idea_x._task=} {idea_x.get_road()}")
    #     if idea_x._label == night_label:
    #         night_idea = idea_x
    #         print(f"{idea_x.get_road()=}")

    print(f"\nIdea = '{night_text}' and reason '{jajatime_road}'")
    beliefheir_jajatime = night_idea._beliefheirs.get(jajatime_road)
    print(f"\n{beliefheir_jajatime=}")
    print(f"      {bob_agenda.get_jajatime_repeating_legible_text(open=1063998720)}")
    print(f"      {bob_agenda.get_jajatime_repeating_legible_text(open=1064130373)}")

    # for reasonheir in intent_item._reasonheirs.values():
    #     print(f"{reasonheir.base=} {reasonheir._status=} {reasonheir._task=}")
    reasonheir_jajatime = night_idea._reasonheirs.get(jajatime_road)
    reasonheir_text = f"\nreasonheir_jajatime= '{reasonheir_jajatime.base}', status={reasonheir_jajatime._status}, task={reasonheir_jajatime._task}"
    print(reasonheir_text)

    premiseunit = reasonheir_jajatime.premises.get(jajatime_road)
    print(f"----\n {premiseunit=}")
    print(f" {premiseunit._get_task_status(beliefheir=beliefheir_jajatime)=}")
    print(f" {premiseunit._status=} , {premiseunit._is_range()=} premiseunit fails")
    print(
        f" {premiseunit._status=} , {premiseunit._is_segregate()=} premiseunit passes"
    )
    # segr_obj = premisestatusfinder_shop(
    #     premise_open=premiseunit.open,
    #     premise_nigh=premiseunit.nigh,
    #     premise_divisor=premiseunit.divisor,
    #     belief_open_full=beliefheir_jajatime.open,
    #     belief_nigh_full=beliefheir_jajatime.nigh,
    # )
    # print(
    #     f"----\n  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    # )
    # print(
    #     f"       {segr_obj.belief_open_full=}         {segr_obj.belief_nigh_full=} \tdifference:{segr_obj.belief_nigh_full-segr_obj.belief_open_full}"
    # )

    # # print(f"  {segr_obj.premise_open_trans=}  {segr_obj.premise_nigh_trans=}")
    # print(f"  {segr_obj.get_active()=}  {segr_obj.get_task_status()=}")
    assert get_tasks_count(action_idea_list) == 64


def test_intent_IsSetByAssignedUnit_1PartyGroup():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text)
    work_text = "work"
    work_road = bob_agenda.make_road(bob_text, work_text)
    bob_agenda.add_l1_idea(ideaunit_shop(work_text, promise=True))
    assert len(bob_agenda.get_intent_dict()) == 1

    sue_text = "sue"
    bob_agenda.add_partyunit(party_id=sue_text)
    assigned_unit_sue = assigned_unit_shop()
    assigned_unit_sue.set_suffgroup(group_id=sue_text)
    assert len(bob_agenda.get_intent_dict()) == 1

    # WHEN
    bob_agenda.edit_idea_attr(road=work_road, assignedunit=assigned_unit_sue)

    # THEN
    assert len(bob_agenda.get_intent_dict()) == 0

    # WHEN
    bob_agenda.add_partyunit(party_id=bob_text)
    assigned_unit_bob = assigned_unit_shop()
    assigned_unit_bob.set_suffgroup(group_id=bob_text)

    # WHEN
    bob_agenda.edit_idea_attr(road=work_road, assignedunit=assigned_unit_bob)

    # THEN
    assert len(bob_agenda.get_intent_dict()) == 1

    # intent_dict = bob_agenda.get_intent_dict()
    # print(f"{intent_dict[0]._label=}")


def test_intent_IsSetByAssignedUnit_2PartyGroup():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text)
    bob_agenda.add_partyunit(party_id=bob_text)
    work_text = "work"
    work_road = bob_agenda.make_road(bob_text, work_text)
    bob_agenda.add_l1_idea(ideaunit_shop(work_text, promise=True))

    sue_text = "sue"
    bob_agenda.add_partyunit(party_id=sue_text)

    run_text = ",runners"
    run_group = groupunit_shop(group_id=run_text)
    run_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    bob_agenda.set_groupunit(y_groupunit=run_group)

    run_assignedunit = assigned_unit_shop()
    run_assignedunit.set_suffgroup(group_id=run_text)
    assert len(bob_agenda.get_intent_dict()) == 1

    # WHEN
    bob_agenda.edit_idea_attr(road=work_road, assignedunit=run_assignedunit)

    # THEN
    assert len(bob_agenda.get_intent_dict()) == 0

    # WHEN
    run_group.set_partylink(partylink=partylink_shop(party_id=bob_text))
    bob_agenda.set_groupunit(y_groupunit=run_group)

    # THEN
    assert len(bob_agenda.get_intent_dict()) == 1


def test_IdeaCore_get_intent_dict_ReturnsCorrectObj_BugFindAndFix_active_SettingError():  # https://github.com/jschalk/jaar/issues/69
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    bob_agenda.set_time_hreg_ideas(7)

    casa_text = "casa"
    casa_road = bob_agenda.make_l1_road(casa_text)
    laundry_text = "do_laundry"
    laundry_road = bob_agenda.make_road(casa_road, laundry_text)
    bob_agenda.add_l1_idea(ideaunit_shop(casa_text))
    bob_agenda.add_idea(ideaunit_shop(laundry_text, promise=True), casa_road)
    time_road = bob_agenda.make_l1_road("time")
    jajatime_road = bob_agenda.make_road(time_road, "jajatime")
    bob_agenda.edit_idea_attr(
        road=laundry_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=3420.0,
        reason_premise_nigh=3420.0,
        reason_premise_divisor=10080.0,
    )
    print("set first belief")
    bob_agenda.set_belief(jajatime_road, jajatime_road, 1064131200, nigh=1064135133)
    print("get 1st intent dictionary")
    bob_intent_dict = bob_agenda.get_intent_dict()
    print(f"{bob_intent_dict.keys()=}")
    assert bob_intent_dict == {}

    laundry_idea = bob_agenda.get_idea_obj(laundry_road)
    laundry_reasonheir = laundry_idea.get_reasonheir(jajatime_road)
    laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
    laundry_beliefheir = laundry_idea._beliefheirs.get(jajatime_road)
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_beliefheir.open % 10080=}"
    # )
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_beliefheir.nigh % 10080=}"
    # )
    # print(f"{laundry_reasonheir.base=} {laundry_premise=}")
    # for x_ideaunit in bob_agenda._idea_dict.values():
    #     if x_ideaunit._label in [laundry_text]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")

    # WHEN
    print("set 2nd belief")
    bob_agenda.set_belief(jajatime_road, jajatime_road, 1064131200, nigh=1064136133)
    print("get 2nd intent dictionary")
    bob_intent_dict = bob_agenda.get_intent_dict()
    print(f"{bob_intent_dict.keys()=}")

    laundry_idea = bob_agenda.get_idea_obj(laundry_road)
    laundry_reasonheir = laundry_idea.get_reasonheir(jajatime_road)
    laundry_premise = laundry_reasonheir.get_premise(jajatime_road)
    laundry_beliefheir = laundry_idea._beliefheirs.get(jajatime_road)
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.open=} {laundry_beliefheir.open % 10080=}"
    # )
    # print(
    #     f"{laundry_idea._active=} {laundry_premise.nigh=} {laundry_beliefheir.nigh % 10080=}"
    # )
    # for x_ideaunit in bob_agenda._idea_dict.values():
    #     if x_ideaunit._label in [laundry_text]:
    #         print(f"{x_ideaunit._label=} {x_ideaunit._begin=} {x_ideaunit._close=}")
    #         print(f"{x_ideaunit._kids.keys()=}")
    #         jaja_beliefheir = x_ideaunit._beliefheirs.get(jajatime_road)
    #         print(f"{jaja_beliefheir.open % 10080=}")
    #         print(f"{jaja_beliefheir.nigh % 10080=}")

    # THEN
    assert bob_intent_dict == {}
