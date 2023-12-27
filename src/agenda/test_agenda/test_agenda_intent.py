from datetime import datetime
from src.agenda.agenda import agendaunit_shop, get_from_json
from src.agenda.examples.agenda_env import agenda_env
from src.agenda.idea import IdeaCore, ideacore_shop
from src.agenda.required_idea import requiredunit_shop, SuffFactStatusFinder
from src.agenda.group import groupunit_shop, balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.required_assign import assigned_unit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_with_4_levels_and_2requireds as example_agendas_get_agenda_with_4_levels_and_2requireds,
    get_agenda_with7amCleanTableRequired as example_agendas_get_agenda_with7amCleanTableRequired,
    get_agenda_with_4_levels_and_2requireds_2acptfacts as example_agendas_get_agenda_with_4_levels_and_2requireds_2acptfacts,
    agenda_v001 as example_agendas_agenda_v001,
    agenda_v001_with_large_intent as example_agendas_agenda_v001_with_large_intent,
    agenda_v002 as example_agendas_agenda_v002,
)
from src.agenda.x_func import yr_explanation, open_file as x_func_open_file


def test_get_intent_returns_intent():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()

    # WHEN
    intent_list = x_agenda.get_intent_items()

    # THEN
    assert intent_list
    assert len(intent_list) == 2
    assert intent_list[0]._label in ["work", "feed cat"]


def test_get_intent_returns_intent_with_only_required_allowed():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = x_agenda.make_road(week_road, sun_text)
    x_agenda.set_acptfact(base=week_road, pick=sun_road)

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
    x_agenda = example_agendas_get_agenda_with_4_levels_and_2requireds_2acptfacts()

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
    x_agenda = example_agendas_get_agenda_with7amCleanTableRequired()

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
    # set acptfacts as midnight to 8am
    x_agenda = example_agendas_get_agenda_with7amCleanTableRequired()
    print(f"{len(x_agenda.get_intent_items())=}")
    assert len(x_agenda.get_intent_items()) == 1

    # WHEN
    timetech_road = x_agenda.make_l1_road("timetech")
    day24hr_road = x_agenda.make_road(timetech_road, "24hr day")
    day24hr_open = 0.0
    day24hr_nigh = 8.0
    housework_text = "housework"
    clean_text = "clean table"
    x_agenda.set_acptfact(
        base=day24hr_road, pick=day24hr_road, open=day24hr_open, nigh=day24hr_nigh
    )
    print(x_agenda._idearoot._acptfactunits[day24hr_road])
    print(x_agenda._idearoot._kids[housework_text]._kids[clean_text]._requiredunits)
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
    c_idea = ideacore_shop(c_label, promise=True)
    x_agenda.add_idea(c_idea, pad=x_agenda._economy_id)
    c_road = x_agenda.make_l1_road(c_label)
    time_road = x_agenda.make_l1_road("time")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")
    jajaday = x_agenda.make_road(jajatime_road, "day")

    x_agenda.edit_idea_attr(
        road=c_road,
        required_base=jajatime_road,
        required_sufffact=jajaday,
        begin=480,
        close=480,
    )

    open_x = 1063971180
    nigh_x1 = 2063971523
    x_agenda.set_acptfact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x1)

    intent_list = x_agenda.get_intent_items()
    assert len(intent_list) == 1
    print(f"{intent_list=}")
    assert intent_list[0]._label in [c_label]

    nigh_x2 = 1063971923
    x_agenda.set_acptfact(base=jajatime_road, pick=jajaday, open=open_x, nigh=nigh_x2)

    intent_list = x_agenda.get_intent_items()
    assert len(intent_list) == 0


def test_exammple_intent_exists():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    min_text = "day_minute"
    min_road = x_agenda.make_l1_road(min_text)
    x_agenda.set_acptfact(base=min_road, pick=min_road, open=0, nigh=1399)
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
    x_agenda.set_acptfact(base=day_min_road, pick=day_min_road, open=0, nigh=1399)
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
    x_agenda.set_acptfact(base=month_week_road, pick=month_week_road)
    x_agenda.set_acptfact(base=nations_road, pick=nations_road)
    x_agenda.set_acptfact(base=mood_road, pick=mood_road)
    x_agenda.set_acptfact(base=aaron_road, pick=aaron_road)
    # x_agenda.set_acptfact(base=internet_road, pick=internet_road)
    x_agenda.set_acptfact(base=year_month_road, pick=year_month_road)
    # season_text = "Seasons"
    # season_road = x_agenda.make_road(x_agenda._economy_id,season_text)
    # x_agenda.set_acptfact(base=season_road, pick=season_road)
    ced_week_text = "ced_week"
    ced_week_road = x_agenda.make_l1_road(ced_week_text)
    x_agenda.set_acptfact(base=ced_week_road, pick=ced_week_road)
    # water_text = "WaterBeing"
    # water_road = x_agenda.make_road(x_agenda._economy_id,water_text)
    # x_agenda.set_acptfact(base=water_road, pick=water_road)
    # movie_text = "No Movie playing"
    # movie_road = x_agenda.make_road(x_agenda._economy_id,movie_text)
    # x_agenda.set_acptfact(base=movie_road, pick=movie_text)

    # WHEN
    idea_action_list = x_agenda.get_intent_items()

    # THEN
    assert len(idea_action_list) == 27

    week1_road = x_agenda.make_road(month_week_road, "1st week")
    x_agenda.set_acptfact(month_week_road, week1_road)
    idea_action_list = x_agenda.get_intent_items()
    assert len(idea_action_list) == 27

    weekday_text = "weekdays"
    weekday_road = x_agenda.make_l1_road(weekday_text)
    monday_text = "Monday"
    monday_road = x_agenda.make_road(weekday_road, monday_text)

    x_agenda.set_acptfact(base=weekday_road, pick=monday_road)
    idea_action_list = x_agenda.get_intent_items()
    assert len(idea_action_list) == 39

    x_agenda.set_acptfact(base=weekday_road, pick=weekday_road)
    idea_action_list = x_agenda.get_intent_items()
    assert len(idea_action_list) == 53

    # x_agenda.set_acptfact(base=nations_road, pick=nations_road)
    # idea_action_list = x_agenda.get_intent_items()
    # assert len(idea_action_list) == 53

    # for base in x_agenda.get_missing_acptfact_bases():
    #     print(f"{base=}")

    # for intent_item in idea_action_list:
    #     print(f"{intent_item._uid=} {intent_item._pad=}")

    # for intent_item in idea_action_list:
    #     # print(f"{intent_item._pad=}")
    #     pass

    print(len(idea_action_list))


def test_exammple_AgendaCanFiltersOnBase():
    # GIVEN
    x_agenda = example_agendas_agenda_v001_with_large_intent()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    print(f"{type(x_agenda)=}")
    # for base in x_agenda.get_missing_acptfact_bases():
    #     print(f"{base=}")

    # for intent_item in x_agenda.get_intent_items():
    #     print(
    #         f"{intent_item._pad=} {intent_item._label} {len(intent_item._requiredunits)=}"
    #     )
    #     for required in intent_item._requiredunits.values():
    #         if required.base == weekdays:
    #             print(f"         {weekdays}")

    # x_agenda.edit_idea_attr(
    #     road="{x_agenda._economy_id},sufffacts,cleaning,laundry wednesday",
    #     required_del_sufffact_base=weekdays,
    #     required_del_sufffact_need=weekdays,
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
        idea_kid=ideacore_shop(run_text, promise=True),
        pad=x_agenda._economy_id,
    )
    x_agenda.add_idea(
        idea_kid=ideacore_shop(day_text, _begin=0, _close=500), pad=time_road
    )
    x_agenda.edit_idea_attr(
        road=run_road,
        required_base=day_road,
        required_sufffact=day_road,
        required_sufffact_open=25,
        required_sufffact_nigh=81,
    )
    x_agenda.set_acptfact(base=day_road, pick=day_road, open=30, nigh=87)
    x_agenda.get_intent_items()
    run_requiredunits = x_agenda._idearoot._kids[run_text]._requiredunits[day_road]
    print(f"{run_requiredunits=}")
    print(f"{run_requiredunits.sufffacts[day_road]._status=}")
    print(f"{run_requiredunits.sufffacts[day_road]._task=}")
    print(f"{x_agenda.get_required_bases()=}")
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
        idea_kid=ideacore_shop(run_text, promise=True),
        pad=x_agenda._economy_id,
    )
    x_agenda.add_idea(
        idea_kid=ideacore_shop(day_text, _begin=0, _close=500), pad=time_road
    )
    x_agenda.edit_idea_attr(
        road=run_road,
        required_base=day_road,
        required_sufffact=day_road,
        required_sufffact_open=1,
        required_sufffact_nigh=1,
        required_sufffact_divisor=2,
    )

    run_idea = x_agenda.get_idea_kid(run_road)
    # print(f"{run_idea._acptfactheirs=}")
    x_agenda.set_acptfact(base=day_road, pick=day_road, open=1, nigh=2)
    assert len(x_agenda.get_intent_items()) == 1
    x_agenda.set_acptfact(base=day_road, pick=day_road, open=2, nigh=2)
    assert len(x_agenda.get_intent_items()) == 0
    x_agenda.set_acptfact(base=day_road, pick=day_road, open=400, nigh=400)
    assert len(x_agenda.get_intent_items()) == 0
    x_agenda.set_acptfact(base=day_road, pick=day_road, open=401, nigh=402)
    assert len(x_agenda.get_intent_items()) == 1
    # print(f"{run_idea._acptfactheirs=}")
    print(f"{run_idea._acptfactunits=}")

    # WHEN
    x_agenda.set_intent_task_complete(task_road=run_road, base=day_road)
    print(f"{run_idea._acptfactunits=}")
    # print(f"{run_idea._acptfactheirs=}")
    assert len(x_agenda.get_intent_items()) == 0


def test_agenda_get_from_json_LoadsActionFromJSONCorrectly():
    # GIVEN
    file_dir = agenda_env()
    file_name = "example_agenda1.json"
    x_agenda_json = x_func_open_file(dest_dir=file_dir, file_name=file_name)

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
    veg_idea = x_agenda.get_idea_kid(veg_road)
    assert not veg_idea._active_status
    assert veg_idea.promise

    # idea_list = x_agenda.get_idea_list()
    # action_true_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaKid'>") > 0:
    #         assert idea._active_status in (True, False)
    #     assert idea.promise in (True, False)
    #     # if idea._active_status == True:
    #     #     print(idea._label)
    #     if idea.promise == True:
    #         action_true_count += 1
    #         # if idea.promise == False:
    #         #     print(f"action is false {idea._label}")
    #         # for required in idea._requiredunits.values():
    #         #     assert required._status in (True, False)
    # assert action_true_count > 0

    # WHEN
    day_min_text = "day_minute"
    day_min_road = x_agenda.make_l1_road(day_min_text)
    x_agenda.set_acptfact(base=day_min_road, pick=day_min_road, open=0, nigh=1399)

    # THEN
    assert len(x_agenda.get_intent_items()) > 0


def test_weekdayAgendaItemsCorrectlyReturned():
    # GIVEN
    healer_text = "Zia"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.set_time_hreg_ideas(c400_count=7)

    things_text = "things to do"
    x_agenda.add_idea(ideacore_shop(things_text), pad=x_agenda._economy_id)
    t_road = x_agenda.make_l1_road(things_text)
    clean = "clean"
    run = "run"
    swim = "swim"
    jog = "jog"
    veg = "veg"
    lift = "life"
    x_agenda.add_idea(ideacore_shop(clean, promise=True), pad=t_road)
    x_agenda.add_idea(ideacore_shop(run, promise=True), pad=t_road)
    x_agenda.add_idea(ideacore_shop(swim, promise=True), pad=t_road)
    x_agenda.add_idea(ideacore_shop(jog, promise=True), pad=t_road)
    x_agenda.add_idea(ideacore_shop(veg, promise=True), pad=t_road)
    x_agenda.add_idea(ideacore_shop(lift, promise=True), pad=t_road)
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

    x_agenda.edit_idea_attr(c_road, required_base=tue_road, required_sufffact=tue_road)
    x_agenda.edit_idea_attr(r_road, required_base=wed_road, required_sufffact=wed_road)
    x_agenda.edit_idea_attr(s_road, required_base=thu_road, required_sufffact=thu_road)
    x_agenda.edit_idea_attr(j_road, required_base=fri_road, required_sufffact=fri_road)
    x_agenda.edit_idea_attr(v_road, required_base=sat_road, required_sufffact=sat_road)
    x_agenda.edit_idea_attr(l_road, required_base=sun_road, required_sufffact=sun_road)

    c_idea = x_agenda.get_idea_kid(c_road)
    c_required = c_idea._requiredunits
    # for required_y in c_required.values():
    #     for sufffact_y in required_y.sufffacts.values():
    #         print(
    #             f"Idea: {c_idea._pad},{c_idea._label}  Required: {required_y.base} open:{sufffact_y.open} nigh:{sufffact_y.nigh} diff:{sufffact_y.nigh-sufffact_y.open}"
    #         )

    # for base, count_x in x_agenda.get_required_bases().items():
    #     print(f"Requireds: {base=} Count: {count_x}")

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
    assert x_agenda._idearoot._acptfactunits.get(jaja_road) is None

    # WHEN
    print("\nset acptfact for Sunday")
    x_agenda.set_acptfact(base=jaja_road, pick=jaja_road, open=sun_min, nigh=sun_min)
    # for acptfact in x_agenda._idearoot._acptfactunits.values():
    #     print(f"{acptfact.base=} (H: {acptfact.acptfact}) {acptfact.active=} {acptfact.open=} {acptfact.nigh=}")

    # THEN
    assert len(x_agenda._idearoot._acptfactunits) == 7
    print(x_agenda._idearoot._acptfactunits[jaja_road])
    print(x_agenda._idearoot._acptfactunits[sat_road])
    print(x_agenda._idearoot._acptfactunits[sun_road])
    print(x_agenda._idearoot._acptfactunits[tue_road])
    print(x_agenda._idearoot._acptfactunits[wed_road])
    print(x_agenda._idearoot._acptfactunits[thu_road])
    print(x_agenda._idearoot._acptfactunits[fri_road])
    assert x_agenda._idearoot._acptfactunits[sun_road]
    assert x_agenda._idearoot._acptfactunits[sun_road].open == 1440
    assert x_agenda._idearoot._acptfactunits[sun_road].nigh == 1440
    # assert x_agenda._idearoot._acptfactunits[sun_road].active == True

    # assert x_agenda._idearoot._acptfactunits[tue_road].active == False
    # assert x_agenda._idearoot._acptfactunits[wed_road].active == False
    # assert x_agenda._idearoot._acptfactunits[thu_road].active == False
    # assert x_agenda._idearoot._acptfactunits[fri_road].active == False
    # assert x_agenda._idearoot._acptfactunits[sat_road].active == False

    # WHEN
    print("\nset acptfact for Sat through Monday")
    x_agenda.set_acptfact(base=jaja_road, pick=jaja_road, open=sat_min, nigh=mon_min)
    # for acptfact in x_agenda._idearoot._acptfactunits.values():
    #     print(f"{acptfact.base=} (H: {acptfact.acptfact}) {acptfact.active=} {acptfact.open=} {acptfact.nigh=}")

    # THEN
    assert x_agenda._idearoot._acptfactunits[sat_road]
    # assert x_agenda._idearoot._acptfactunits[sat_road].active == True
    # assert x_agenda._idearoot._acptfactunits[sun_road].active == True
    # assert x_agenda._idearoot._acptfactunits[tue_road].active == False
    # assert x_agenda._idearoot._acptfactunits[wed_road].active == False
    # assert x_agenda._idearoot._acptfactunits[thu_road].active == False
    # assert x_agenda._idearoot._acptfactunits[fri_road].active == False

    assert x_agenda._idearoot._acptfactunits[sat_road].open == 0
    assert x_agenda._idearoot._acptfactunits[sat_road].nigh == 1440
    assert x_agenda._idearoot._acptfactunits[sun_road].open == 1440
    assert x_agenda._idearoot._acptfactunits[sun_road].nigh == 2880

    # WHEN
    print("\nset acptfacts for Sunday through Friday")
    x_agenda.set_acptfact(base=jaja_road, pick=jaja_road, open=sun_min, nigh=fri_min)
    # for acptfact in x_agenda._idearoot._acptfactunits.values():
    #     print(f"{acptfact.base=} (H: {acptfact.acptfact}) {acptfact.active=} {acptfact.open=} {acptfact.nigh=}")

    # THEN
    # assert x_agenda._idearoot._acptfactunits[sat_road].active == False
    # assert x_agenda._idearoot._acptfactunits[sun_road].active == True
    # assert x_agenda._idearoot._acptfactunits[tue_road].active == True
    # assert x_agenda._idearoot._acptfactunits[wed_road].active == True
    # assert x_agenda._idearoot._acptfactunits[thu_road].active == True
    # assert x_agenda._idearoot._acptfactunits[fri_road].active == False

    assert x_agenda._idearoot._acptfactunits[sun_road].open == 1440
    assert x_agenda._idearoot._acptfactunits[sun_road].nigh == 2880

    # WHEN
    print("\nset acptfacts for 10 day stretch")
    dayzero_dt = datetime(2010, 1, 3)
    dayten_dt = datetime(2010, 1, 13)
    dayzero_min = x_agenda.get_time_min_from_dt(dt=dayzero_dt)
    dayten_min = x_agenda.get_time_min_from_dt(dt=dayten_dt)
    x_agenda.set_acptfact(
        base=jaja_road, pick=jaja_road, open=dayzero_min, nigh=dayten_min
    )
    # for acptfact in x_agenda._idearoot._acptfactunits.values():
    #     print(f"{acptfact.base=} (H: {acptfact.acptfact}) {acptfact.active=} {acptfact.open=} {acptfact.nigh=}")

    # assert x_agenda._idearoot._acptfactunits[sat_road].active == True
    # assert x_agenda._idearoot._acptfactunits[sun_road].active == True
    # assert x_agenda._idearoot._acptfactunits[tue_road].active == True
    # assert x_agenda._idearoot._acptfactunits[wed_road].active == True
    # assert x_agenda._idearoot._acptfactunits[thu_road].active == True
    # assert x_agenda._idearoot._acptfactunits[fri_road].active == True


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
    clean_cookery_idea = ideacore_shop(
        _label=clean_cookery_text, _pad=clean_things_road
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

    dirty_cookery_required = requiredunit_shop(cookery_room_road)
    dirty_cookery_required.set_sufffact(sufffact=cookery_dirty_road)
    clean_cookery_idea.set_required_unit(required=dirty_cookery_required)

    daytime_required = requiredunit_shop(daytime_road)
    daytime_required.set_sufffact(sufffact=daytime_road, open=open_8am, nigh=nigh_8am)
    clean_cookery_idea.set_required_unit(required=daytime_required)

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
    assert x_agenda.get_idea_kid(daytime_road)._begin == 0
    assert x_agenda.get_idea_kid(daytime_road)._close == 1440
    print(f"{clean_cookery_idea.get_road()=}")

    # GIVEN
    x_agenda.set_dominate_promise_idea(idea_kid=clean_cookery_idea)

    # THEN
    # for idea_kid in x_agenda._idearoot._kids.keys():
    #     print(f"  {idea_kid=}")

    print(f"{clean_cookery_idea.get_road()=}")
    assert x_agenda.get_idea_kid(clean_cookery_road) != None
    assert x_agenda.get_idea_kid(clean_cookery_road)._label == clean_cookery_text
    assert x_agenda.get_idea_kid(clean_cookery_road).promise
    assert len(x_agenda.get_idea_kid(clean_cookery_road)._requiredunits) == 2
    assert x_agenda.get_idea_kid(clean_things_road) != None
    assert x_agenda.get_idea_kid(cookery_room_road) != None
    assert x_agenda.get_idea_kid(cookery_dirty_road) != None
    assert x_agenda.get_idea_kid(daytime_road)._begin == 0
    assert x_agenda.get_idea_kid(daytime_road)._close == 1440
    assert len(x_agenda._groups) == 1
    assert x_agenda._groups.get(family_text) != None
    assert x_agenda._groups.get(family_text)._partys in (None, {})

    assert len(x_agenda._idearoot._kids) == 3


def get_tasks_count(idea_list: list[IdeaCore]) -> int:
    return sum(bool(ideacore._task) for ideacore in idea_list)


def test_Issue116Resolved_correctlySetsTaskAsTrue():
    # GIVEN
    x_agenda = example_agendas_agenda_v002()

    assert len(x_agenda.get_intent_items()) == 44
    time_road = x_agenda.make_l1_road("time")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")

    # WHEN
    x_agenda.set_acptfact(
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

    print(f"\nIdea = '{night_text}' and required '{jajatime_road}'")
    acptfactheir_jajatime = night_idea._acptfactheirs.get(jajatime_road)
    print(f"\n{acptfactheir_jajatime=}")
    print(f"      {x_agenda.get_jajatime_repeating_legible_text(open=1063998720)}")
    print(f"      {x_agenda.get_jajatime_repeating_legible_text(open=1064130373)}")

    # for requiredheir in intent_item._requiredheirs.values():
    #     print(f"{requiredheir.base=} {requiredheir._status=} {requiredheir._task=}")
    requiredheir_jajatime = night_idea._requiredheirs.get(jajatime_road)
    requiredheir_text = f"\nrequiredheir_jajatime= '{requiredheir_jajatime.base}', status={requiredheir_jajatime._status}, task={requiredheir_jajatime._task}"
    print(requiredheir_text)

    sufffactunit = requiredheir_jajatime.sufffacts.get(jajatime_road)
    print(f"----\n {sufffactunit=}")
    print(f" {sufffactunit._get_task_status(acptfactheir=acptfactheir_jajatime)=}")
    print(f" {sufffactunit._status=} , {sufffactunit._is_range()=} sufffactunit fails")
    print(
        f" {sufffactunit._status=} , {sufffactunit._is_segregate()=} sufffactunit passes"
    )
    segr_obj = SuffFactStatusFinder(
        acptfact_open=acptfactheir_jajatime.open,
        acptfact_nigh=acptfactheir_jajatime.nigh,
        sufffact_open=sufffactunit.open,
        sufffact_nigh=sufffactunit.nigh,
        sufffact_divisor=sufffactunit.divisor,
    )
    print(
        f"----\n  {segr_obj.sufffact_open=}  {segr_obj.sufffact_nigh=}  {segr_obj.sufffact_divisor=}"
    )
    print(
        f"       {segr_obj.acptfact_open=}         {segr_obj.acptfact_nigh=} \tdifference:{segr_obj.acptfact_nigh-segr_obj.acptfact_open}"
    )

    print(f"  {segr_obj.sufffact_open_trans=}  {segr_obj.sufffact_nigh_trans=}")
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")
    assert get_tasks_count(action_idea_list) == 64


def test_intent_IsSetByAssignedUnit_1PartyGroup():
    # GIVEN
    bob_text = "bob"
    x_agenda = agendaunit_shop(bob_text)
    work_text = "work"
    work_road = x_agenda.make_road(bob_text, work_text)
    x_agenda.add_idea(ideacore_shop(work_text, promise=True), pad=bob_text)
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
    x_agenda.add_idea(ideacore_shop(work_text, promise=True), pad=bob_text)

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
