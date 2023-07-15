from datetime import datetime
from lib.agent.agent import AgentUnit, get_from_json
from lib.agent.examples.get_agent_examples_dir import get_agent_examples_dir
from lib.agent.idea import IdeaCore, IdeaKid
from lib.agent.road import Road
from lib.agent.required import RequiredUnit, SuffFactStatusFinder
from lib.agent.brand import brandunit_shop, brandlink_shop
from lib.agent.examples.example_agents import (
    get_agent_with_4_levels as example_agents_get_agent_with_4_levels,
    get_agent_with_4_levels_and_2requireds as example_agents_get_agent_with_4_levels_and_2requireds,
    get_agent_with7amCleanTableRequired as example_agents_get_agent_with7amCleanTableRequired,
    get_agent_with_4_levels_and_2requireds_2acptfacts as example_agents_get_agent_with_4_levels_and_2requireds_2acptfacts,
    agent_v001 as example_agents_agent_v001,
    agent_v001_with_large_agenda as example_agents_agent_v001_with_large_agenda,
    agent_v002 as example_agents_agent_v002,
)
from lib.agent.x_func import yr_tale, open_file as x_func_open_file


def test_get_agenda_returns_agenda():
    # GIVEN
    a1 = example_agents_get_agent_with_4_levels()

    # WHEN
    agenda_list = a1.get_agenda_items()

    # THEN
    assert agenda_list
    assert len(agenda_list) == 2
    assert agenda_list[0]._desc in ["work", "feed cat"]


def test_get_agenda_returns_agenda_with_only_required_allowed():
    # GIVEN
    a1 = example_agents_get_agent_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{a1._desc},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"
    a1.set_acptfact(base=week_road, pick=sun_road)

    # WHEN
    agenda_list = a1.get_agenda_items()

    # THEN
    assert agenda_list
    # for agenda_item in agenda_list:
    #     yr_tale(idea=agenda_item)
    yr_tale(idea=agenda_list[0])

    assert len(agenda_list) == 1
    print(f"{agenda_list=}")
    assert agenda_list[0]._desc in ["feed cat"]


def test_get_agenda_returns_agenda_with_agent_importance():
    # GIVEN
    a1 = example_agents_get_agent_with_4_levels_and_2requireds_2acptfacts()

    # WHEN
    agenda_list = a1.get_agenda_items()

    # THEN
    assert agenda_list
    assert len(agenda_list) == 2
    print(f"{agenda_list[0]._desc=}")
    assert agenda_list[0]._agent_importance

    print(f"{agenda_list[1]._desc=}")
    assert agenda_list[1]._agent_importance


def test_get_agenda_with_No7amItem():
    # GIVEN
    a1 = example_agents_get_agent_with7amCleanTableRequired()

    # WHEN
    agenda_list = a1.get_agenda_items()

    # THEN
    assert agenda_list
    assert len(agenda_list) == 1
    print(f"{agenda_list[0]._desc=}")
    assert len(agenda_list) == 1

    agenda_item = agenda_list[0]
    assert agenda_item._desc != "clean table"


def test_get_agenda_with_7amItem():
    # GIVEN
    # set acptfacts as midnight to 8am
    a1 = example_agents_get_agent_with7amCleanTableRequired()
    day24hr_road = f"{a1._desc},timetech,24hr day"
    day24hr_open = 0.0
    day24hr_nigh = 8.0
    housework_text = "housework"
    clean_text = "clean table"
    a1.set_acptfact(
        base=day24hr_road, pick=day24hr_road, open=day24hr_open, nigh=day24hr_nigh
    )
    print(a1._idearoot._acptfactunits[day24hr_road])
    print(a1._idearoot._kids[housework_text]._kids[clean_text]._requiredunits)
    print(a1._idearoot._kids[housework_text]._kids[clean_text]._active_status)

    # WHEN
    agenda_list = a1.get_agenda_items()

    # THEN
    # for agenda_item in agenda_list:
    #     print(agenda_item._desc)

    print(f"{len(agenda_list)=}")
    assert len(agenda_list) == 6
    clean_item = agenda_list[1]
    assert clean_item._desc == clean_text


def test_get_agenda_does_not_return_promise_items_outside_range():
    src = "src"
    a1 = AgentUnit(_desc=src)
    a1.set_time_hreg_ideas(c400_count=7)
    c_desc = "clean"
    c_idea = IdeaKid(_desc=c_desc, promise=True)
    a1.add_idea(idea_kid=c_idea, walk=src)
    c_road = f"{src},{c_desc}"
    jajatime = "src,time,jajatime"
    jajaday = "src,time,jajatime,day"

    a1.edit_idea_attr(
        road=c_road,
        required_base=jajatime,
        required_sufffact=jajaday,
        begin=480,
        close=480,
    )

    open_x = 1063971180
    nigh_x1 = 2063971523
    a1.set_acptfact(base=jajatime, pick=jajaday, open=open_x, nigh=nigh_x1)

    agenda_list = a1.get_agenda_items()
    assert len(agenda_list) == 1
    print(f"{agenda_list=}")
    assert agenda_list[0]._desc in [c_desc]

    nigh_x2 = 1063971923
    a1.set_acptfact(base=jajatime, pick=jajaday, open=open_x, nigh=nigh_x2)

    agenda_list = a1.get_agenda_items()
    assert len(agenda_list) == 0


def test_exammple_agenda_exists():
    # GIVEN
    a1 = example_agents_agent_v001()
    min_text = "TlME,day_minute"
    a1.set_acptfact(base=min_text, pick=min_text, open=0, nigh=1399)
    assert a1
    # for idea_kid in a1._idearoot._kids.values():
    #     # print(idea_kid._desc)
    #     assert str(type(idea_kid)) != "<class 'str'>"
    #     assert idea_kid.promise != None

    # WHEN
    agenda_list = a1.get_agenda_items()

    # THEN
    assert len(agenda_list) > 0
    assert len(agenda_list) == 17
    assert agenda_list[0].promise != None
    assert str(type(agenda_list[0])) != "<class 'str'>"
    assert str(type(agenda_list[9])) != "<class 'str'>"
    assert str(type(agenda_list[12])) != "<class 'str'>"


def test_exammple_AgendaHasCorrectAttributes():
    # GIVEN
    a1 = example_agents_agent_v001()

    src_road = "TlME"
    day_min_text = "day_minute"
    day_min_road = f"{src_road},{day_min_text}"
    a1.set_acptfact(base=day_min_road, pick=day_min_road, open=0, nigh=1399)
    month_week_text = "month_week"
    month_week_road = f"{src_road},{month_week_text}"
    nations_text = "Nation-States"
    nations_road = f"{src_road},{nations_text}"
    mood_text = "Moods"
    mood_road = f"{src_road},{mood_text}"
    aaron_text = "Aaron Donald sphere"
    aaron_road = f"{src_road},{aaron_text}"
    # internet_text = "Internet"
    # internet_road = f"{src_road},{internet_text}"
    year_month_text = "year_month"
    year_month_road = f"{src_road},{year_month_text}"
    a1.set_acptfact(base=month_week_road, pick=month_week_road)
    a1.set_acptfact(base=nations_road, pick=nations_road)
    a1.set_acptfact(base=mood_road, pick=mood_road)
    a1.set_acptfact(base=aaron_road, pick=aaron_road)
    # a1.set_acptfact(base=internet_road, pick=internet_road)
    a1.set_acptfact(base=year_month_road, pick=year_month_road)
    # season_text = "Seasons"
    # season_road = f"{src_road},{season_text}"
    # a1.set_acptfact(base=season_road, pick=season_road)
    ced_week_text = "ced_week"
    ced_week_road = f"{src_road},{ced_week_text}"
    a1.set_acptfact(base=ced_week_road, pick=ced_week_road)
    # water_text = "WaterBeing"
    # water_road = f"{src_road},{water_text}"
    # a1.set_acptfact(base=water_road, pick=water_road)
    # movie_text = "No Movie playing"
    # movie_road = f"{src_road},{movie_text}"
    # a1.set_acptfact(base=movie_road, pick=movie_text)

    # WHEN
    idea_action_list = a1.get_agenda_items()

    # THEN
    print("Test might be deprecated if it's not worthy it to fix this test source.")
    assert len(idea_action_list) == 27

    a1.set_acptfact(base=month_week_road, pick=f"{month_week_road},1st week")
    idea_action_list = a1.get_agenda_items()
    assert len(idea_action_list) == 27

    weekday_text = "weekdays"
    weekday_road = f"{src_road},{weekday_text}"
    monday_text = "Monday"
    monday_road = f"{weekday_road},{monday_text}"

    a1.set_acptfact(base=weekday_road, pick=monday_road)
    idea_action_list = a1.get_agenda_items()
    assert len(idea_action_list) == 39

    a1.set_acptfact(base=weekday_road, pick=weekday_road)
    idea_action_list = a1.get_agenda_items()
    assert len(idea_action_list) == 53

    # a1.set_acptfact(base=nations_road, pick=nations_road)
    # idea_action_list = a1.get_agenda_items()
    # assert len(idea_action_list) == 53

    # for base in a1.get_missing_acptfact_bases():
    #     print(f"{base=}")

    # for agenda_item in idea_action_list:
    #     print(f"{agenda_item._uid=} {agenda_item._walk=}")

    # for agenda_item in idea_action_list:
    #     # print(f"{agenda_item._walk=}")
    #     pass

    print(len(idea_action_list))


def test_exammple_AgendaCanFiltersOnBase():
    # GIVEN
    a1 = example_agents_agent_v001_with_large_agenda()
    weekdays = "TlME,weekdays"
    print(f"{type(a1)=}")
    # for base in a1.get_missing_acptfact_bases():
    #     print(f"{base=}")

    # for agenda_item in a1.get_agenda_items():
    #     print(
    #         f"{agenda_item._walk=} {agenda_item._desc} {len(agenda_item._requiredunits)=}"
    #     )
    #     for required in agenda_item._requiredunits.values():
    #         if required.base == weekdays:
    #             print(f"         {weekdays}")

    # a1.edit_idea_attr(
    #     road="TlME,sufffacts,cleaning,laundry wednesday",
    #     required_del_sufffact_base=weekdays,
    #     required_del_sufffact_need=weekdays,
    # )
    assert len(a1.get_agenda_items()) == 68

    # When
    action_list = a1.get_agenda_items(base=weekdays)

    # THEN
    assert len(action_list) != 69
    assert len(action_list) == 28


def test_set_agenda_task_as_complete_RangeWorksCorrectly():
    # GIVEN
    src_text = "src"
    run_text = "run"
    run_road = f"{src_text},{run_text}"
    time_text = "time"
    time_road = f"{src_text},{time_text}"
    day_text = "day"
    day_road = f"{time_road},{day_text}"
    a1 = AgentUnit(_desc=src_text)

    a1.add_idea(idea_kid=IdeaKid(_desc=run_text, promise=True), walk=src_text)
    a1.add_idea(idea_kid=IdeaKid(_desc=day_text, _begin=0, _close=500), walk=time_road)
    a1.edit_idea_attr(
        road=run_road,
        required_base=day_road,
        required_sufffact=day_road,
        required_sufffact_open=25,
        required_sufffact_nigh=81,
    )
    a1.set_acptfact(base=day_road, pick=day_road, open=30, nigh=87)
    a1.get_agenda_items()
    run_requiredunits = a1._idearoot._kids[run_text]._requiredunits[day_road]
    print(f"{run_requiredunits=}")
    print(f"{run_requiredunits.sufffacts[day_road]._status=}")
    print(f"{run_requiredunits.sufffacts[day_road]._task=}")
    print(f"{a1.get_required_bases()=}")
    assert len(a1.get_idea_list()) == 4
    assert len(a1.get_agenda_items()) == 1
    assert a1.get_agenda_items()[0]._task == True

    # When
    a1.set_agenda_task_complete(task_road=run_road, base=day_road)

    # Then
    agenda_list = a1.get_agenda_items()
    assert len(agenda_list) == 0
    assert agenda_list == []


def test_set_agenda_task_as_complete_DivisionWorksCorrectly():
    # GIVEN
    src_text = "src"
    run_text = "run"
    run_road = f"{src_text},{run_text}"
    time_text = "time"
    time_road = f"{src_text},{time_text}"
    day_text = "day"
    day_road = f"{time_road},{day_text}"
    a1 = AgentUnit(_desc=src_text)

    a1.add_idea(idea_kid=IdeaKid(_desc=run_text, promise=True), walk=src_text)
    a1.add_idea(idea_kid=IdeaKid(_desc=day_text, _begin=0, _close=500), walk=time_road)
    a1.edit_idea_attr(
        road=run_road,
        required_base=day_road,
        required_sufffact=day_road,
        required_sufffact_open=1,
        required_sufffact_nigh=1,
        required_sufffact_divisor=2,
    )

    run_idea = a1.get_idea_kid(road=run_road)
    # print(f"{run_idea._acptfactheirs=}")
    a1.set_acptfact(base=day_road, pick=day_road, open=1, nigh=2)
    assert len(a1.get_agenda_items()) == 1
    a1.set_acptfact(base=day_road, pick=day_road, open=2, nigh=2)
    assert len(a1.get_agenda_items()) == 0
    a1.set_acptfact(base=day_road, pick=day_road, open=400, nigh=400)
    assert len(a1.get_agenda_items()) == 0
    a1.set_acptfact(base=day_road, pick=day_road, open=401, nigh=402)
    assert len(a1.get_agenda_items()) == 1
    # print(f"{run_idea._acptfactheirs=}")
    print(f"{run_idea._acptfactunits=}")

    # When
    a1.set_agenda_task_complete(task_road=run_road, base=day_road)
    print(f"{run_idea._acptfactunits=}")
    # print(f"{run_idea._acptfactheirs=}")
    assert len(a1.get_agenda_items()) == 0


def test_agent_get_from_json_LoadsActionFromJSONCorrectly():
    # GIVEN
    file_dir = get_agent_examples_dir()
    file_name = "example_agent1.json"
    a1_json = x_func_open_file(dest_dir=file_dir, file_name=file_name)

    # WHEN
    a1 = get_from_json(lw_json=a1_json)

    # THEN
    assert len(a1.get_idea_list()) == 253
    print(f"{len(a1.get_idea_list())=}")
    veg_idea = a1._idea_dict.get("TlME,casa,body care,make veggies every morning")
    assert not veg_idea._active_status
    assert veg_idea.promise

    # idea_list = a1.get_idea_list()
    # action_true_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaKid'>") > 0:
    #         assert idea._active_status in (True, False)
    #     assert idea.promise in (True, False)
    #     # if idea._active_status == True:
    #     #     print(idea._desc)
    #     if idea.promise == True:
    #         action_true_count += 1
    #         # if idea.promise == False:
    #         #     print(f"action is false {idea._desc}")
    #         # for required in idea._requiredunits.values():
    #         #     assert required._status in (True, False)
    # assert action_true_count > 0

    a1.set_acptfact(base="TlME,day_minute", pick="TlME,day_minute", open=0, nigh=1399)
    assert len(a1.get_agenda_items()) > 0


def test_weekdayAgendaItemsCorrectlyReturned():
    # Given
    a1 = AgentUnit(_desc="src")

    a1._set_acptfacts_empty_if_null()
    a1.set_time_hreg_ideas(c400_count=7)

    things_text = "things to do"
    a1.add_idea(IdeaKid(_desc=things_text), walk=a1._desc)
    t_road = f"{a1._desc},{things_text}"
    clean = "clean"
    run = "run"
    swim = "swim"
    jog = "job"
    veg = "veg"
    lift = "life"
    a1.add_idea(IdeaKid(_desc=clean, promise=True), walk=t_road)
    a1.add_idea(IdeaKid(_desc=run, promise=True), walk=t_road)
    a1.add_idea(IdeaKid(_desc=swim, promise=True), walk=t_road)
    a1.add_idea(IdeaKid(_desc=jog, promise=True), walk=t_road)
    a1.add_idea(IdeaKid(_desc=veg, promise=True), walk=t_road)
    a1.add_idea(IdeaKid(_desc=lift, promise=True), walk=t_road)
    w_word = f"{a1._desc},time,tech,week"
    mon_road = f"{w_word},Monday"
    tue_road = f"{w_word},Tuesday"
    wed_road = f"{w_word},Wednesday"
    thu_road = f"{w_word},Thursday"
    fri_road = f"{w_word},Friday"
    sat_road = f"{w_word},Saturday"
    sun_road = f"{w_word},Sunday"
    t_road = f"{a1._desc},{things_text}"
    c_road = f"{t_road},{clean}"
    r_road = f"{t_road},{run}"
    s_road = f"{t_road},{swim}"
    j_road = f"{t_road},{jog}"
    v_road = f"{t_road},{veg}"
    l_road = f"{t_road},{lift}"

    a1.edit_idea_attr(
        road=c_road,
        required_base=tue_road,
        required_sufffact=tue_road,
    )
    a1.edit_idea_attr(
        road=r_road,
        required_base=wed_road,
        required_sufffact=wed_road,
    )
    a1.edit_idea_attr(
        road=s_road,
        required_base=thu_road,
        required_sufffact=thu_road,
    )
    a1.edit_idea_attr(
        road=j_road,
        required_base=fri_road,
        required_sufffact=fri_road,
    )
    a1.edit_idea_attr(
        road=v_road,
        required_base=sat_road,
        required_sufffact=sat_road,
    )
    a1.edit_idea_attr(
        road=l_road,
        required_base=sun_road,
        required_sufffact=sun_road,
    )

    c_idea = a1.get_idea_kid(road=c_road)
    c_required = c_idea._requiredunits
    # for required_y in c_required.values():
    #     for sufffact_y in required_y.sufffacts.values():
    #         print(
    #             f"Idea: {c_idea._walk},{c_idea._desc}  Required: {required_y.base} open:{sufffact_y.open} nigh:{sufffact_y.nigh} diff:{sufffact_y.nigh-sufffact_y.open}"
    #         )

    # for base, count_x in a1.get_required_bases().items():
    #     print(f"Requireds: {base=} Count: {count_x}")

    mon_dt = datetime(2000, 1, 3)
    tue_dt = datetime(2000, 1, 4)
    wed_dt = datetime(2000, 1, 5)
    thu_dt = datetime(2000, 1, 6)
    fri_dt = datetime(2000, 1, 7)
    sat_dt = datetime(2000, 1, 1)
    sun_dt = datetime(2000, 1, 2)
    mon_min = a1.get_time_min_from_dt(dt=mon_dt)
    tue_min = a1.get_time_min_from_dt(dt=tue_dt)
    wed_min = a1.get_time_min_from_dt(dt=wed_dt)
    thu_min = a1.get_time_min_from_dt(dt=thu_dt)
    fri_min = a1.get_time_min_from_dt(dt=fri_dt)
    sat_min = a1.get_time_min_from_dt(dt=sat_dt)
    sun_min = a1.get_time_min_from_dt(dt=sun_dt)
    assert a1._idearoot._acptfactunits.get("src,time,jajatime") is None

    # When
    print("\nset acptfact for Sunday")
    road_minute = f"{a1._desc},time,jajatime"
    a1.set_acptfact(base=road_minute, pick=road_minute, open=sun_min, nigh=sun_min)
    # for acptfact in a1._idearoot._acptfactunits.values():
    #     print(f"{acptfact.base=} (H: {acptfact.acptfact}) {acptfact.active=} {acptfact.open=} {acptfact.nigh=}")

    # Then
    tech_root = "src,time,tech"

    assert len(a1._idearoot._acptfactunits) == 7
    print(a1._idearoot._acptfactunits["src,time,jajatime"])
    print(a1._idearoot._acptfactunits[f"{tech_root},week,Saturday"])
    print(a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"])
    print(a1._idearoot._acptfactunits[f"{tech_root},week,Tuesday"])
    print(a1._idearoot._acptfactunits[f"{tech_root},week,Wednesday"])
    print(a1._idearoot._acptfactunits[f"{tech_root},week,Thursday"])
    print(a1._idearoot._acptfactunits[f"{tech_root},week,Friday"])
    assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"]
    assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].open == 1440
    assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].nigh == 1440
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].active == True

    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Tuesday"].active == False
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Wednesday"].active == False
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Thursday"].active == False
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Friday"].active == False
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Saturday"].active == False

    # When
    print("\nset acptfact for Sat through Monday")
    a1.set_acptfact(base=road_minute, pick=road_minute, open=sat_min, nigh=mon_min)
    # for acptfact in a1._idearoot._acptfactunits.values():
    #     print(f"{acptfact.base=} (H: {acptfact.acptfact}) {acptfact.active=} {acptfact.open=} {acptfact.nigh=}")

    # Then
    assert a1._idearoot._acptfactunits[f"{tech_root},week,Saturday"]
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Saturday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Tuesday"].active == False
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Wednesday"].active == False
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Thursday"].active == False
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Friday"].active == False

    assert a1._idearoot._acptfactunits[f"{tech_root},week,Saturday"].open == 0
    assert a1._idearoot._acptfactunits[f"{tech_root},week,Saturday"].nigh == 1440
    assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].open == 1440
    assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].nigh == 2880

    # When
    print("\nset acptfacts for Sunday through Friday")
    a1.set_acptfact(base=road_minute, pick=road_minute, open=sun_min, nigh=fri_min)
    # for acptfact in a1._idearoot._acptfactunits.values():
    #     print(f"{acptfact.base=} (H: {acptfact.acptfact}) {acptfact.active=} {acptfact.open=} {acptfact.nigh=}")

    # Then
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Saturday"].active == False
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Tuesday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Wednesday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Thursday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Friday"].active == False

    assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].open == 1440
    assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].nigh == 2880

    # When
    print("\nset acptfacts for 10 day stretch")
    dayzero_dt = datetime(2010, 1, 3)
    dayten_dt = datetime(2010, 1, 13)
    dayzero_min = a1.get_time_min_from_dt(dt=dayzero_dt)
    dayten_min = a1.get_time_min_from_dt(dt=dayten_dt)
    a1.set_acptfact(
        base=road_minute, pick=road_minute, open=dayzero_min, nigh=dayten_min
    )
    # for acptfact in a1._idearoot._acptfactunits.values():
    #     print(f"{acptfact.base=} (H: {acptfact.acptfact}) {acptfact.active=} {acptfact.open=} {acptfact.nigh=}")

    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Saturday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Sunday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Tuesday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Wednesday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Thursday"].active == True
    # assert a1._idearoot._acptfactunits[f"{tech_root},week,Friday"].active == True


def test_agent_create_agenda_item_CorrectlyCreatesAllAgentAttributes():
    # WHEN "I am cleaning the kitchen since I'm in the apartment and it's 8am and it's dirty and I'm doing this for my family"

    # GIVEN
    src_text = "mysun"
    src_road = Road(f"{src_text}")

    a1 = AgentUnit(_desc=src_text)

    a1.set_agent_metrics()
    assert len(a1._allys) == 0
    assert len(a1._brands) == 0
    assert len(a1._idearoot._kids) == 0

    clean_things_text = "cleaning things"
    clean_things_road = Road(f"{src_text},{clean_things_text}")
    clean_kitchen_text = "clean kitchen"
    clean_kitchen_road = Road(f"{src_text},{clean_things_text},{clean_kitchen_text}")
    clean_kitchen_idea = IdeaKid(_desc=clean_kitchen_text, _walk=clean_things_road)
    print(f"{clean_kitchen_idea.get_road()=}")
    home_text = "home"
    home_road = Road(f"{src_text},{home_text}")
    kitchen_room_text = "kitchen room"
    kitchen_room_road = Road(f"{src_text},{home_text},{kitchen_room_text}")
    kit_dirty_text = "dirty"
    kit_dirty_road = Road(f"{kitchen_room_road},{kit_dirty_text}")

    # create gregorian timeline
    a1.set_time_hreg_ideas(c400_count=7)
    daytime_road = Road(f"{src_text},time,jajatime,day")
    open_8am = 480
    nigh_8am = 480

    dirty_kitchen_required = RequiredUnit(base=kitchen_room_road, sufffacts={})
    dirty_kitchen_required.set_sufffact(sufffact=kit_dirty_road)
    clean_kitchen_idea.set_required_unit(required=dirty_kitchen_required)

    daytime_required = RequiredUnit(base=daytime_road, sufffacts={})
    daytime_required.set_sufffact(sufffact=daytime_road, open=open_8am, nigh=nigh_8am)
    clean_kitchen_idea.set_required_unit(required=daytime_required)

    # anna_text = "anna"
    # anna_allyunit = allyunit_shop(name=anna_text)
    # anna_allylink = allylink_shop(name=anna_text)
    # beto_text = "beto"
    # beto_allyunit = allyunit_shop(name=beto_text)
    # beto_allylink = allylink_shop(name=beto_text)

    family_text = "family"
    # brandunit_z = brandunit_shop(name=family_text)
    # brandunit_z.set_allylink(allylink=anna_allylink)
    # brandunit_z.set_allylink(allylink=beto_allylink)
    brandlink_z = brandlink_shop(name=family_text)
    clean_kitchen_idea.set_brandlink(brandlink=brandlink_z)

    assert len(a1._allys) == 0
    assert len(a1._brands) == 0
    assert len(a1._idearoot._kids) == 1
    assert a1.get_idea_kid(road=daytime_road)._begin == 0
    assert a1.get_idea_kid(road=daytime_road)._close == 1440
    print(f"{clean_kitchen_idea.get_road()=}")

    # GIVEN
    a1.set_dominate_promise_idea(idea_kid=clean_kitchen_idea)

    # THEN
    # for idea_kid in a1._idearoot._kids.keys():
    #     print(f"  {idea_kid=}")

    print(f"{clean_kitchen_idea.get_road()=}")
    assert a1.get_idea_kid(road=clean_kitchen_road) != None
    assert a1.get_idea_kid(road=clean_kitchen_road)._desc == clean_kitchen_text
    assert a1.get_idea_kid(road=clean_kitchen_road).promise
    assert len(a1.get_idea_kid(road=clean_kitchen_road)._requiredunits) == 2
    assert a1.get_idea_kid(road=clean_things_road) != None
    assert a1.get_idea_kid(road=kitchen_room_road) != None
    assert a1.get_idea_kid(road=kit_dirty_road) != None
    assert a1.get_idea_kid(road=daytime_road)._begin == 0
    assert a1.get_idea_kid(road=daytime_road)._close == 1440
    assert len(a1._brands) == 1
    assert a1._brands.get(family_text) != None
    assert a1._brands.get(family_text)._allys in (None, {})

    assert len(a1._idearoot._kids) == 3


def get_tasks_count(idea_list: list[IdeaCore]) -> int:
    return sum(bool(ideacore._task) for ideacore in idea_list)


def test_Issue116Resolved_correctlySetsTaskAsTrue():
    # GIVEN
    a1 = example_agents_agent_v002()

    assert len(a1.get_agenda_items()) == 44
    jajatime_road = f"{a1._desc},time,jajatime"

    # WHEN
    a1.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063998720, nigh=1064130373
    )
    action_idea_list = a1.get_agenda_items()

    # THEN
    assert len(action_idea_list) == 66
    jajatime_road = "Myagent,time,jajatime"
    night_text = "late_night_go_to_sleep"
    night_road = f"Myagent,D&B,{night_text}"
    night_idea = a1._idea_dict.get(night_road)
    # for idea_x in a1.get_agenda_items():
    #     # if idea_x._task != True:
    #     #     print(f"{len(action_idea_list)=} {idea_x._task=} {idea_x.get_road()}")
    #     if idea_x._desc == night_desc:
    #         night_idea = idea_x
    #         print(f"{idea_x.get_road()=}")

    print(f"\nIdea = '{night_text}' and required '{jajatime_road}'")
    acptfactheir_jajatime = night_idea._acptfactheirs.get(jajatime_road)
    print(f"\n{acptfactheir_jajatime=}")
    print(f"      {a1.get_jajatime_repeating_readable_text(open=1063998720)}")
    print(f"      {a1.get_jajatime_repeating_readable_text(open=1064130373)}")

    # for requiredheir in agenda_item._requiredheirs.values():
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
