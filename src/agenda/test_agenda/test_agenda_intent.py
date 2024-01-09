from datetime import datetime
from src.agenda.agenda import agendaunit_shop, get_from_json
from src.agenda.examples.agenda_env import agenda_env
from src.agenda.idea import IdeaUnit, ideaunit_shop
from src.agenda.reason_idea import reasonunit_shop, PremiseStatusFinder
from src.agenda.group import groupunit_shop, balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_assign import assigned_unit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_with_4_levels_and_2reasons as example_agendas_get_agenda_with_4_levels_and_2reasons,
    get_agenda_with7amCleanTableReason as example_agendas_get_agenda_with7amCleanTableReason,
    get_agenda_with_4_levels_and_2reasons_2facts as example_agendas_get_agenda_with_4_levels_and_2reasons_2facts,
    agenda_v001 as example_agendas_agenda_v001,
    agenda_v001_with_large_intent as example_agendas_agenda_v001_with_large_intent,
    agenda_v002 as example_agendas_agenda_v002,
    yr_explanation,
)
from src.tools.file import open_file


def test_get_intent_returns_intent():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()

    # WHEN
    intent_list = x_agenda.get_intent_items()

    # THEN
    assert intent_list
    assert len(intent_list) == 2
    assert intent_list[0]._label in ["work", "feed cat"]


def test_agenda_get_intent_items_ReturnsIntentWithOnlyCorrectItems():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = x_agenda.make_road(week_road, sun_text)
    x_agenda.set_fact(base=week_road, pick=sun_road)

    # WHEN
    intent_list = x_agenda.get_intent_items()

    # THEN
    assert intent_list
    # for intent_item in intent_list:
    #     yr_explanation(idea=intent_item)
    yr_explanation(idea=intent_list[0])

    assert len(intent_list) == 1
    print(f"{intent_list=}")
    assert intent_list[0]._label in ["feed cat"]


def test_get_intent_returns_intent_with_agenda_importance():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels_and_2reasons_2facts()

    # WHEN
    intent_list = x_agenda.get_intent_items()

    # THEN
    assert intent_list
    assert len(intent_list) == 2
    print(f"{intent_list[0]._label=}")
    assert intent_list[0]._agenda_importance

    print(f"{intent_list[1]._label=}")
    assert intent_list[1]._agenda_importance


def test_get_intent_with_No7amItem():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with7amCleanTableReason()

    # WHEN
    intent_list = x_agenda.get_intent_items()

    # THEN
    assert intent_list
    assert len(intent_list) == 1
    print(f"{intent_list[0]._label=}")
    assert len(intent_list) == 1

    intent_item = intent_list[0]
    assert intent_item._label != "clean table"


def test_get_intent_with_7amItem():
    # GIVEN
    # set facts as midnight to 8am
    x_agenda = example_agendas_get_agenda_with7amCleanTableReason()
    print(f"{len(x_agenda.get_intent_items())=}")
    assert len(x_agenda.get_intent_items()) == 1

    # WHEN
    timetech_road = x_agenda.make_l1_road("timetech")
    day24hr_road = x_agenda.make_road(timetech_road, "24hr day")
    day24hr_open = 0.0
    day24hr_nigh = 8.0
    housework_text = "housework"
    clean_text = "clean table"
    x_agenda.set_fact(
        base=day24hr_road, pick=day24hr_road, open=day24hr_open, nigh=day24hr_nigh
    )
    print(x_agenda._idearoot._factunits[day24hr_road])
    print(x_agenda._idearoot._kids[housework_text]._kids[clean_text]._reasonunits)
    print(x_agenda._idearoot._kids[housework_text]._kids[clean_text]._active_status)

    # THEN
    intent_list = x_agenda.get_intent_items()
    print(f"{len(intent_list)=}")
    assert len(intent_list) == 6
    clean_item = intent_list[1]
    assert clean_item._label == clean_text


def test_get_intent_does_not_return_promise_items_outside_range():
    healer_text = "Zia"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.set_time_hreg_ideas(c400_count=7)
    c_label = "clean"
    c_idea = ideaunit_shop(c_label, promise=True)
    x_agenda.add_idea(c_idea, parent_road=x_agenda._economy_id)
    c_road = x_agenda.make_l1_road(c_label)
    time_road = x_agenda.make_l1_road("time")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")
    jajaday = x_agenda.make_road(jajatime_road, "day")

    x_agenda.edit_idea_attr(
        road=c_road,
        reason_base=jajatime_road,
        reason_premise=jajaday,
        begin=480,
        close=480,
    )

    open_x = 1063971180
    nigh_x1 = 2063971523
    x_agenda.set_fact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x1)

    intent_list = x_agenda.get_intent_items()
    assert len(intent_list) == 1
    print(f"{intent_list=}")
    assert intent_list[0]._label in [c_label]

    nigh_x2 = 1063971923
    x_agenda.set_fact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x2)

    intent_list = x_agenda.get_intent_items()
    assert len(intent_list) == 0


def test_exammple_intent_exists():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    min_text = "day_minute"
    min_road = x_agenda.make_l1_road(min_text)
    x_agenda.set_fact(base=min_road, pick=min_road, open=0, nigh=1399)
    assert x_agenda
    # for idea_kid in x_agenda._idearoot._kids.values():
    #     # print(idea_kid._label)
    #     assert str(type(idea_kid)) != "<class 'str'>"
    #     assert idea_kid.promise != None

    # WHEN
    intent_list = x_agenda.get_intent_items()

    # THEN
    assert len(intent_list) > 0
    assert len(intent_list) == 17
    assert intent_list[0].promise != None
    assert str(type(intent_list[0])) != "<class 'str'>"
    assert str(type(intent_list[9])) != "<class 'str'>"
    assert str(type(intent_list[12])) != "<class 'str'>"


def test_exammple_AgendaHasCorrectAttributes():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()

    day_min_text = "day_minute"
    day_min_road = x_agenda.make_l1_road(day_min_text)
    x_agenda.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=1399)
    month_week_text = "month_week"
    month_week_road = x_agenda.make_l1_road(month_week_text)
    nations_text = "Nation-States"
    nations_road = x_agenda.make_l1_road(nations_text)
    mood_text = "Moods"
    mood_road = x_agenda.make_l1_road(mood_text)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = x_agenda.make_l1_road(aaron_text)
    # internet_text = "Internet"
    # internet_road = x_agenda.make_road(x_agenda._economy_id,internet_text)
    year_month_text = "year_month"
    year_month_road = x_agenda.make_l1_road(year_month_text)
    x_agenda.set_fact(base=month_week_road, pick=month_week_road)
    x_agenda.set_fact(base=nations_road, pick=nations_road)
    x_agenda.set_fact(base=mood_road, pick=mood_road)
    x_agenda.set_fact(base=aaron_road, pick=aaron_road)
    # x_agenda.set_fact(base=internet_road, pick=internet_road)
    x_agenda.set_fact(base=year_month_road, pick=year_month_road)
    # season_text = "Seasons"
    # season_road = x_agenda.make_road(x_agenda._economy_id,season_text)
    # x_agenda.set_fact(base=season_road, pick=season_road)
    ced_week_text = "ced_week"
    ced_week_road = x_agenda.make_l1_road(ced_week_text)
    x_agenda.set_fact(base=ced_week_road, pick=ced_week_road)
    # water_text = "WaterBeing"
    # water_road = x_agenda.make_road(x_agenda._economy_id,water_text)
    # x_agenda.set_fact(base=water_road, pick=water_road)
    # movie_text = "No Movie playing"
    # movie_road = x_agenda.make_road(x_agenda._economy_id,movie_text)
    # x_agenda.set_fact(base=movie_road, pick=movie_text)

    # WHEN
    idea_action_list = x_agenda.get_intent_items()

    # THEN
    assert len(idea_action_list) == 27

    week1_road = x_agenda.make_road(month_week_road, "1st week")
    x_agenda.set_fact(month_week_road, week1_road)
    idea_action_list = x_agenda.get_intent_items()
    assert len(idea_action_list) == 27

    weekday_text = "weekdays"
    weekday_road = x_agenda.make_l1_road(weekday_text)
    monday_text = "Monday"
    monday_road = x_agenda.make_road(weekday_road, monday_text)

    x_agenda.set_fact(base=weekday_road, pick=monday_road)
    idea_action_list = x_agenda.get_intent_items()
    assert len(idea_action_list) == 39

    x_agenda.set_fact(base=weekday_road, pick=weekday_road)
    idea_action_list = x_agenda.get_intent_items()
    assert len(idea_action_list) == 53

    # x_agenda.set_fact(base=nations_road, pick=nations_road)
    # idea_action_list = x_agenda.get_intent_items()
    # assert len(idea_action_list) == 53

    # for base in x_agenda.get_missing_fact_bases():
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
    # for base in x_agenda.get_missing_fact_bases():
    #     print(f"{base=}")

    # for intent_item in x_agenda.get_intent_items():
    #     print(
    #         f"{intent_item._parent_road=} {intent_item._label} {len(intent_item._reasonunits)=}"
    #     )
    #     for reason in intent_item._reasonunits.values():
    #         if reason.base == weekdays:
    #             print(f"         {weekdays}")

    # x_agenda.edit_idea_attr(
    #     road="{x_agenda._economy_id},premises,cleaning,laundry wednesday",
    #     reason_del_premise_base=weekdays,
    #     reason_del_premise_need=weekdays,
    # )
    assert len(x_agenda.get_intent_items()) == 68

    # WHEN
    action_list = x_agenda.get_intent_items(base=week_road)

    # THEN
    assert len(action_list) != 69
    assert len(action_list) == 28


def test_set_intent_task_as_complete_RangeWorksCorrectly():
    # GIVEN
    healer_text = "Zia"
    x_agenda = agendaunit_shop(healer_text)

    run_text = "run"
    run_road = x_agenda.make_l1_road(run_text)
    time_text = "time"
    time_road = x_agenda.make_l1_road(time_text)
    day_text = "day"
    day_road = x_agenda.make_road(time_road, day_text)

    x_agenda.add_idea(
        idea_kid=ideaunit_shop(run_text, promise=True),
        parent_road=x_agenda._economy_id,
    )
    x_agenda.add_idea(
        idea_kid=ideaunit_shop(day_text, _begin=0, _close=500), parent_road=time_road
    )
    x_agenda.edit_idea_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=25,
        reason_premise_nigh=81,
    )
    x_agenda.set_fact(base=day_road, pick=day_road, open=30, nigh=87)
    x_agenda.get_intent_items()
    run_reasonunits = x_agenda._idearoot._kids[run_text]._reasonunits[day_road]
    print(f"{run_reasonunits=}")
    print(f"{run_reasonunits.premises[day_road]._status=}")
    print(f"{run_reasonunits.premises[day_road]._task=}")
    print(f"{x_agenda.get_reason_bases()=}")
    assert len(x_agenda.get_idea_list()) == 4
    assert len(x_agenda.get_intent_items()) == 1
    assert x_agenda.get_intent_items()[0]._task == True

    # WHEN
    x_agenda.set_intent_task_complete(task_road=run_road, base=day_road)

    # THEN
    intent_list = x_agenda.get_intent_items()
    assert len(intent_list) == 0
    assert intent_list == []


def test_set_intent_task_as_complete_DivisionWorksCorrectly():
    # GIVEN
    healer_text = "Zia"
    x_agenda = agendaunit_shop(healer_text)

    run_text = "run"
    run_road = x_agenda.make_l1_road(run_text)
    time_text = "time"
    time_road = x_agenda.make_l1_road(time_text)
    day_text = "day"
    day_road = x_agenda.make_road(time_road, day_text)

    x_agenda.add_idea(
        idea_kid=ideaunit_shop(run_text, promise=True),
        parent_road=x_agenda._economy_id,
    )
    x_agenda.add_idea(
        idea_kid=ideaunit_shop(day_text, _begin=0, _close=500), parent_road=time_road
    )
    x_agenda.edit_idea_attr(
        road=run_road,
        reason_base=day_road,
        reason_premise=day_road,
        reason_premise_open=1,
        reason_premise_nigh=1,
        reason_premise_divisor=2,
    )

    run_idea = x_agenda.get_idea_obj(run_road)
    # print(f"{run_idea._factheirs=}")
    x_agenda.set_fact(base=day_road, pick=day_road, open=1, nigh=2)
    assert len(x_agenda.get_intent_items()) == 1
    x_agenda.set_fact(base=day_road, pick=day_road, open=2, nigh=2)
    assert len(x_agenda.get_intent_items()) == 0
    x_agenda.set_fact(base=day_road, pick=day_road, open=400, nigh=400)
    assert len(x_agenda.get_intent_items()) == 0
    x_agenda.set_fact(base=day_road, pick=day_road, open=401, nigh=402)
    assert len(x_agenda.get_intent_items()) == 1
    # print(f"{run_idea._factheirs=}")
    print(f"{run_idea._factunits=}")

    # WHEN
    x_agenda.set_intent_task_complete(task_road=run_road, base=day_road)
    print(f"{run_idea._factunits=}")
    # print(f"{run_idea._factheirs=}")
    assert len(x_agenda.get_intent_items()) == 0


def test_agenda_get_from_json_LoadsActionFromJSONCorrectly():
    # GIVEN
    file_dir = agenda_env()
    file_name = "example_agenda1.json"
    x_agenda_json = open_file(dest_dir=file_dir, file_name=file_name)

    # WHEN
    x_agenda = get_from_json(x_agenda_json=x_agenda_json)

    # THEN
    assert len(x_agenda.get_idea_list()) == 253
    print(f"{len(x_agenda.get_idea_list())=}")
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    body_text = "workout"
    body_road = x_agenda.make_road(casa_road, body_text)
    veg_text = "cook veggies every morning"
    veg_road = x_agenda.make_road(body_road, veg_text)
    veg_idea = x_agenda.get_idea_obj(veg_road)
    assert not veg_idea._active_status
    assert veg_idea.promise

    # idea_list = x_agenda.get_idea_list()
    # action_true_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
    #         assert idea._active_status in (True, False)
    #     assert idea.promise in (True, False)
    #     # if idea._active_status == True:
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
    x_agenda.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=1399)

    # THEN
    assert len(x_agenda.get_intent_items()) > 0


def test_weekdayAgendaItemsCorrectlyReturned():
    # GIVEN
    healer_text = "Zia"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.set_time_hreg_ideas(c400_count=7)

    things_text = "things to do"
    x_agenda.add_idea(ideaunit_shop(things_text), parent_road=x_agenda._economy_id)
    t_road = x_agenda.make_l1_road(things_text)
    clean = "clean"
    run = "run"
    swim = "swim"
    jog = "jog"
    veg = "veg"
    lift = "life"
    x_agenda.add_idea(ideaunit_shop(clean, promise=True), parent_road=t_road)
    x_agenda.add_idea(ideaunit_shop(run, promise=True), parent_road=t_road)
    x_agenda.add_idea(ideaunit_shop(swim, promise=True), parent_road=t_road)
    x_agenda.add_idea(ideaunit_shop(jog, promise=True), parent_road=t_road)
    x_agenda.add_idea(ideaunit_shop(veg, promise=True), parent_road=t_road)
    x_agenda.add_idea(ideaunit_shop(lift, promise=True), parent_road=t_road)
    time_text = "time"
    time_road = x_agenda.make_l1_road(time_text)
    jaja_text = "jajatime"
    jaja_road = x_agenda.make_road(time_road, jaja_text)
    tech_text = "tech"
    tech_road = x_agenda.make_road(time_road, tech_text)
    w_road = x_agenda.make_road(tech_road, "week")
    mon_road = x_agenda.make_road(w_road, "Monday")
    tue_road = x_agenda.make_road(w_road, "Tuesday")
    wed_road = x_agenda.make_road(w_road, "Wednesday")
    thu_road = x_agenda.make_road(w_road, "Thursday")
    fri_road = x_agenda.make_road(w_road, "Friday")
    sat_road = x_agenda.make_road(w_road, "Saturday")
    sun_road = x_agenda.make_road(w_road, "Sunday")
    t_road = x_agenda.make_l1_road(things_text)
    c_road = x_agenda.make_road(t_road, clean)
    r_road = x_agenda.make_road(t_road, run)
    s_road = x_agenda.make_road(t_road, swim)
    j_road = x_agenda.make_road(t_road, jog)
    v_road = x_agenda.make_road(t_road, veg)
    l_road = x_agenda.make_road(t_road, lift)

    x_agenda.edit_idea_attr(c_road, reason_base=tue_road, reason_premise=tue_road)
    x_agenda.edit_idea_attr(r_road, reason_base=wed_road, reason_premise=wed_road)
    x_agenda.edit_idea_attr(s_road, reason_base=thu_road, reason_premise=thu_road)
    x_agenda.edit_idea_attr(j_road, reason_base=fri_road, reason_premise=fri_road)
    x_agenda.edit_idea_attr(v_road, reason_base=sat_road, reason_premise=sat_road)
    x_agenda.edit_idea_attr(l_road, reason_base=sun_road, reason_premise=sun_road)

    c_idea = x_agenda.get_idea_obj(c_road)
    c_reason = c_idea._reasonunits
    # for reason_y in c_reason.values():
    #     for premise_y in reason_y.premises.values():
    #         print(
    #             f"Idea: {c_idea._parent_road},{c_idea._label}  Reason: {reason_y.base} open:{premise_y.open} nigh:{premise_y.nigh} diff:{premise_y.nigh-premise_y.open}"
    #         )

    # for base, count_x in x_agenda.get_reason_bases().items():
    #     print(f"Reasons: {base=} Count: {count_x}")

    mon_dt = datetime(2000, 1, 3)
    tue_dt = datetime(2000, 1, 4)
    wed_dt = datetime(2000, 1, 5)
    thu_dt = datetime(2000, 1, 6)
    fri_dt = datetime(2000, 1, 7)
    sat_dt = datetime(2000, 1, 1)
    sun_dt = datetime(2000, 1, 2)
    mon_min = x_agenda.get_time_min_from_dt(dt=mon_dt)
    tue_min = x_agenda.get_time_min_from_dt(dt=tue_dt)
    wed_min = x_agenda.get_time_min_from_dt(dt=wed_dt)
    thu_min = x_agenda.get_time_min_from_dt(dt=thu_dt)
    fri_min = x_agenda.get_time_min_from_dt(dt=fri_dt)
    sat_min = x_agenda.get_time_min_from_dt(dt=sat_dt)
    sun_min = x_agenda.get_time_min_from_dt(dt=sun_dt)
    assert x_agenda._idearoot._factunits.get(jaja_road) is None

    # WHEN
    print("\nset fact for Sunday")
    x_agenda.set_fact(base=jaja_road, pick=jaja_road, open=sun_min, nigh=sun_min)
    # for fact in x_agenda._idearoot._factunits.values():
    #     print(f"{fact.base=} (H: {fact.fact}) {fact.active=} {fact.open=} {fact.nigh=}")

    # THEN
    assert len(x_agenda._idearoot._factunits) == 7
    print(x_agenda._idearoot._factunits[jaja_road])
    print(x_agenda._idearoot._factunits[sat_road])
    print(x_agenda._idearoot._factunits[sun_road])
    print(x_agenda._idearoot._factunits[tue_road])
    print(x_agenda._idearoot._factunits[wed_road])
    print(x_agenda._idearoot._factunits[thu_road])
    print(x_agenda._idearoot._factunits[fri_road])
    assert x_agenda._idearoot._factunits[sun_road]
    assert x_agenda._idearoot._factunits[sun_road].open == 1440
    assert x_agenda._idearoot._factunits[sun_road].nigh == 1440
    # assert x_agenda._idearoot._factunits[sun_road].active == True

    # assert x_agenda._idearoot._factunits[tue_road].active == False
    # assert x_agenda._idearoot._factunits[wed_road].active == False
    # assert x_agenda._idearoot._factunits[thu_road].active == False
    # assert x_agenda._idearoot._factunits[fri_road].active == False
    # assert x_agenda._idearoot._factunits[sat_road].active == False

    # WHEN
    print("\nset fact for Sat through Monday")
    x_agenda.set_fact(base=jaja_road, pick=jaja_road, open=sat_min, nigh=mon_min)
    # for fact in x_agenda._idearoot._factunits.values():
    #     print(f"{fact.base=} (H: {fact.fact}) {fact.active=} {fact.open=} {fact.nigh=}")

    # THEN
    assert x_agenda._idearoot._factunits[sat_road]
    # assert x_agenda._idearoot._factunits[sat_road].active == True
    # assert x_agenda._idearoot._factunits[sun_road].active == True
    # assert x_agenda._idearoot._factunits[tue_road].active == False
    # assert x_agenda._idearoot._factunits[wed_road].active == False
    # assert x_agenda._idearoot._factunits[thu_road].active == False
    # assert x_agenda._idearoot._factunits[fri_road].active == False

    assert x_agenda._idearoot._factunits[sat_road].open == 0
    assert x_agenda._idearoot._factunits[sat_road].nigh == 1440
    assert x_agenda._idearoot._factunits[sun_road].open == 1440
    assert x_agenda._idearoot._factunits[sun_road].nigh == 2880

    # WHEN
    print("\nset facts for Sunday through Friday")
    x_agenda.set_fact(base=jaja_road, pick=jaja_road, open=sun_min, nigh=fri_min)
    # for fact in x_agenda._idearoot._factunits.values():
    #     print(f"{fact.base=} (H: {fact.fact}) {fact.active=} {fact.open=} {fact.nigh=}")

    # THEN
    # assert x_agenda._idearoot._factunits[sat_road].active == False
    # assert x_agenda._idearoot._factunits[sun_road].active == True
    # assert x_agenda._idearoot._factunits[tue_road].active == True
    # assert x_agenda._idearoot._factunits[wed_road].active == True
    # assert x_agenda._idearoot._factunits[thu_road].active == True
    # assert x_agenda._idearoot._factunits[fri_road].active == False

    assert x_agenda._idearoot._factunits[sun_road].open == 1440
    assert x_agenda._idearoot._factunits[sun_road].nigh == 2880

    # WHEN
    print("\nset facts for 10 day stretch")
    dayzero_dt = datetime(2010, 1, 3)
    dayten_dt = datetime(2010, 1, 13)
    dayzero_min = x_agenda.get_time_min_from_dt(dt=dayzero_dt)
    dayten_min = x_agenda.get_time_min_from_dt(dt=dayten_dt)
    x_agenda.set_fact(base=jaja_road, pick=jaja_road, open=dayzero_min, nigh=dayten_min)
    # for fact in x_agenda._idearoot._factunits.values():
    #     print(f"{fact.base=} (H: {fact.fact}) {fact.active=} {fact.open=} {fact.nigh=}")

    # assert x_agenda._idearoot._factunits[sat_road].active == True
    # assert x_agenda._idearoot._factunits[sun_road].active == True
    # assert x_agenda._idearoot._factunits[tue_road].active == True
    # assert x_agenda._idearoot._factunits[wed_road].active == True
    # assert x_agenda._idearoot._factunits[thu_road].active == True
    # assert x_agenda._idearoot._factunits[fri_road].active == True


def test_agenda_create_intent_item_CorrectlyCreatesAllAgendaAttributes():
    # WHEN "I am cleaning the cookery since I'm in the apartment and it's 8am and it's dirty and I'm doing this for my family"

    # GIVEN
    healer_text = "Zia"
    x_agenda = agendaunit_shop(healer_text)

    x_agenda.set_agenda_metrics()
    assert len(x_agenda._partys) == 0
    assert len(x_agenda._groups) == 0
    assert len(x_agenda._idearoot._kids) == 0

    clean_things_text = "cleaning things"
    clean_things_road = x_agenda.make_l1_road(clean_things_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = x_agenda.make_road(clean_things_road, clean_cookery_text)
    clean_cookery_idea = ideaunit_shop(
        _label=clean_cookery_text, _parent_road=clean_things_road
    )
    print(f"{clean_cookery_idea.get_road()=}")
    house_text = "house"
    house_road = x_agenda.make_l1_road(house_text)
    cookery_room_text = "cookery room"
    cookery_room_road = x_agenda.make_road(house_road, cookery_room_text)
    cookery_dirty_text = "dirty"
    cookery_dirty_road = x_agenda.make_road(cookery_room_road, cookery_dirty_text)

    # create gregorian timeline
    x_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = x_agenda.make_l1_road("time")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")
    daytime_road = x_agenda.make_road(jajatime_road, "day")
    open_8am = 480
    nigh_8am = 480

    dirty_cookery_reason = reasonunit_shop(cookery_room_road)
    dirty_cookery_reason.set_premise(premise=cookery_dirty_road)
    clean_cookery_idea.set_reason_unit(reason=dirty_cookery_reason)

    daytime_reason = reasonunit_shop(daytime_road)
    daytime_reason.set_premise(premise=daytime_road, open=open_8am, nigh=nigh_8am)
    clean_cookery_idea.set_reason_unit(reason=daytime_reason)

    # anna_text = "anna"
    # anna_partyunit = partyunit_shop(pid=anna_text)
    # anna_partylink = partylink_shop(pid=anna_text)
    # beto_text = "beto"
    # beto_partyunit = partyunit_shop(pid=beto_text)
    # beto_partylink = partylink_shop(pid=beto_text)

    family_text = "family"
    # groupunit_z = groupunit_shop(brand=family_text)
    # groupunit_z.set_partylink(partylink=anna_partylink)
    # groupunit_z.set_partylink(partylink=beto_partylink)
    balancelink_z = balancelink_shop(brand=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)

    assert len(x_agenda._partys) == 0
    assert len(x_agenda._groups) == 0
    assert len(x_agenda._idearoot._kids) == 1
    assert x_agenda.get_idea_obj(daytime_road)._begin == 0
    assert x_agenda.get_idea_obj(daytime_road)._close == 1440
    print(f"{clean_cookery_idea.get_road()=}")

    # GIVEN
    x_agenda.set_dominate_promise_idea(idea_kid=clean_cookery_idea)

    # THEN
    # for idea_kid in x_agenda._idearoot._kids.keys():
    #     print(f"  {idea_kid=}")

    print(f"{clean_cookery_idea.get_road()=}")
    assert x_agenda.get_idea_obj(clean_cookery_road) != None
    assert x_agenda.get_idea_obj(clean_cookery_road)._label == clean_cookery_text
    assert x_agenda.get_idea_obj(clean_cookery_road).promise
    assert len(x_agenda.get_idea_obj(clean_cookery_road)._reasonunits) == 2
    assert x_agenda.get_idea_obj(clean_things_road) != None
    assert x_agenda.get_idea_obj(cookery_room_road) != None
    assert x_agenda.get_idea_obj(cookery_dirty_road) != None
    assert x_agenda.get_idea_obj(daytime_road)._begin == 0
    assert x_agenda.get_idea_obj(daytime_road)._close == 1440
    assert len(x_agenda._groups) == 1
    assert x_agenda._groups.get(family_text) != None
    assert x_agenda._groups.get(family_text)._partys in (None, {})

    assert len(x_agenda._idearoot._kids) == 3


def get_tasks_count(idea_list: list[IdeaUnit]) -> int:
    return sum(bool(ideaunit._task) for ideaunit in idea_list)


def test_Isue116Resolved_correctlySetsTaskAsTrue():
    # GIVEN
    x_agenda = example_agendas_agenda_v002()

    assert len(x_agenda.get_intent_items()) == 44
    time_road = x_agenda.make_l1_road("time")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")

    # WHEN
    x_agenda.set_fact(
        base=jajatime_road, pick=jajatime_road, open=1063998720, nigh=1064130373
    )
    action_idea_list = x_agenda.get_intent_items()

    # THEN
    assert len(action_idea_list) == 66
    db_road = x_agenda.make_l1_road("D&B")
    night_text = "late_night_go_to_sleep"
    night_road = x_agenda.make_road(db_road, night_text)
    night_idea = x_agenda._idea_dict.get(night_road)
    # for idea_x in x_agenda.get_intent_items():
    #     # if idea_x._task != True:
    #     #     print(f"{len(action_idea_list)=} {idea_x._task=} {idea_x.get_road()}")
    #     if idea_x._label == night_label:
    #         night_idea = idea_x
    #         print(f"{idea_x.get_road()=}")

    print(f"\nIdea = '{night_text}' and reason '{jajatime_road}'")
    factheir_jajatime = night_idea._factheirs.get(jajatime_road)
    print(f"\n{factheir_jajatime=}")
    print(f"      {x_agenda.get_jajatime_repeating_legible_text(open=1063998720)}")
    print(f"      {x_agenda.get_jajatime_repeating_legible_text(open=1064130373)}")

    # for reasonheir in intent_item._reasonheirs.values():
    #     print(f"{reasonheir.base=} {reasonheir._status=} {reasonheir._task=}")
    reasonheir_jajatime = night_idea._reasonheirs.get(jajatime_road)
    reasonheir_text = f"\nreasonheir_jajatime= '{reasonheir_jajatime.base}', status={reasonheir_jajatime._status}, task={reasonheir_jajatime._task}"
    print(reasonheir_text)

    premiseunit = reasonheir_jajatime.premises.get(jajatime_road)
    print(f"----\n {premiseunit=}")
    print(f" {premiseunit._get_task_status(factheir=factheir_jajatime)=}")
    print(f" {premiseunit._status=} , {premiseunit._is_range()=} premiseunit fails")
    print(
        f" {premiseunit._status=} , {premiseunit._is_segregate()=} premiseunit passes"
    )
    segr_obj = PremiseStatusFinder(
        fact_open=factheir_jajatime.open,
        fact_nigh=factheir_jajatime.nigh,
        premise_open=premiseunit.open,
        premise_nigh=premiseunit.nigh,
        premise_divisor=premiseunit.divisor,
    )
    print(
        f"----\n  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(
        f"       {segr_obj.fact_open=}         {segr_obj.fact_nigh=} \tdifference:{segr_obj.fact_nigh-segr_obj.fact_open}"
    )

    print(f"  {segr_obj.premise_open_trans=}  {segr_obj.premise_nigh_trans=}")
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")
    assert get_tasks_count(action_idea_list) == 64


def test_intent_IsSetByAssignedUnit_1PartyGroup():
    # GIVEN
    bob_text = "bob"
    x_agenda = agendaunit_shop(bob_text)
    work_text = "work"
    work_road = x_agenda.make_road(bob_text, work_text)
    x_agenda.add_idea(
        ideaunit_shop(work_text, promise=True), parent_road=x_agenda._economy_id
    )
    assert len(x_agenda.get_intent_items()) == 1

    sue_text = "sue"
    x_agenda.add_partyunit(pid=sue_text)
    assigned_unit_sue = assigned_unit_shop()
    assigned_unit_sue.set_suffgroup(brand=sue_text)
    assert len(x_agenda.get_intent_items()) == 1

    # WHEN
    x_agenda.edit_idea_attr(road=work_road, assignedunit=assigned_unit_sue)

    # THEN
    assert len(x_agenda.get_intent_items()) == 0

    # WHEN
    x_agenda.add_partyunit(pid=bob_text)
    assigned_unit_bob = assigned_unit_shop()
    assigned_unit_bob.set_suffgroup(brand=bob_text)

    # WHEN
    x_agenda.edit_idea_attr(road=work_road, assignedunit=assigned_unit_bob)

    # THEN
    assert len(x_agenda.get_intent_items()) == 1

    # intent_list = x_agenda.get_intent_items()
    # print(f"{intent_list[0]._label=}")


def test_intent_IsSetByAssignedUnit_2PartyGroup():
    # GIVEN
    bob_text = "bob"
    x_agenda = agendaunit_shop(bob_text)
    x_agenda.add_partyunit(pid=bob_text)
    work_text = "work"
    work_road = x_agenda.make_road(bob_text, work_text)
    x_agenda.add_idea(
        ideaunit_shop(work_text, promise=True), parent_road=x_agenda._economy_id
    )

    sue_text = "sue"
    x_agenda.add_partyunit(pid=sue_text)

    run_text = "runners"
    run_group = groupunit_shop(brand=run_text)
    run_group.set_partylink(partylink=partylink_shop(pid=sue_text))
    x_agenda.set_groupunit(y_groupunit=run_group)

    run_assignedunit = assigned_unit_shop()
    run_assignedunit.set_suffgroup(brand=run_text)
    assert len(x_agenda.get_intent_items()) == 1

    # WHEN
    x_agenda.edit_idea_attr(road=work_road, assignedunit=run_assignedunit)

    # THEN
    assert len(x_agenda.get_intent_items()) == 0

    # WHEN
    run_group.set_partylink(partylink=partylink_shop(pid=bob_text))
    x_agenda.set_groupunit(y_groupunit=run_group)

    # THEN
    assert len(x_agenda.get_intent_items()) == 1
