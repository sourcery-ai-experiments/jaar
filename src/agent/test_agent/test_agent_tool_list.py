from src.agent.x_func import from_list_get_active_status
from src.agent.examples.example_agents import (
    get_agent_with_4_levels_and_2requireds,
    get_agent_with7amCleanTableRequired,
    agent_v001,
)
from src.agent.tool import ToolKid
from src.agent.required import sufffactunit_shop, RequiredUnit, RequiredHeir
from src.agent.road import Road
from src.agent.agent import AgentUnit


def _check_all_elements_in_dict_are_correct_type(x_dict: dict, type_str: str) -> bool:
    bool_x = True
    for x_value in x_dict.values():
        if type_str not in str(type(x_value)):
            bool_x = False
        print(f"/t{type(x_value)=} {type_str=} {str(type(x_value)).find(type_str)=}")
    return bool_x


def test_agent_yoke_dict_isDictionaryAndIsFullyPopulated():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()

    # WHEN
    agent_x.set_agent_metrics()

    # THEN
    assert len(agent_x._tool_dict) == 17


def test_agent_get_tool_list_SetsSatiateStatusCorrectlyWhenAcptFactSaysNo():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{agent_x._desc},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"

    # WHEN
    agent_x.set_acptfact(base=week_road, pick=sun_road)
    tool_list = agent_x.get_tool_list()

    # THEN
    assert tool_list
    assert len(tool_list) == 17

    # for tool in agent_x._tool_dict.values():
    #     print(f"{work_road=} {tool.get_road()=}")
    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"
    assert agent_x._tool_dict.get(work_road)._active_status == False


def test_agent_get_tool_list_SetsSatiateStatusCorrectlyWhenAcptFactChanges():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{agent_x._desc},{week_text}"
    sun_text = "Wednesday"
    sun_road = f"{week_road},{sun_text}"
    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"

    # WHEN
    agent_x.set_acptfact(base=week_road, pick=sun_road)

    # THEN
    tool_list = agent_x.get_tool_list()
    assert tool_list
    assert len(tool_list) == 17
    assert agent_x._tool_dict.get(work_road)._active_status == False

    # WHEN
    states_text = "nation-state"
    states_road = f"{agent_x._desc},{states_text}"
    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    agent_x.set_acptfact(base=states_road, pick=usa_road)

    # THEN
    tool_list = agent_x.get_tool_list()
    assert tool_list
    assert len(tool_list) == 17
    assert agent_x._tool_dict.get(work_road)._active_status

    # WHEN
    france_text = "France"
    france_road = f"{states_road},{france_text}"
    agent_x.set_acptfact(base=states_road, pick=france_road)

    # THEN
    tool_list = agent_x.get_tool_list()
    assert tool_list
    assert len(tool_list) == 17
    assert agent_x._tool_dict.get(work_road)._active_status == False


def test_agent_get_tool_list_returns_correct_list():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{agent_x._desc},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    state_text = "nation-state"
    state_road = f"{agent_x._desc},{state_text}"
    france_text = "France"
    france_road = f"{state_road},{france_text}"
    agent_x.set_acptfact(base=week_road, pick=wed_road)
    agent_x.set_acptfact(base=state_road, pick=france_road)

    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"
    work_tool = agent_x.get_tool_kid(work_road)
    print(f"{agent_x._desc=} {len(work_tool._requiredunits)=}")
    # print(f"{work_tool._requiredunits=}")
    print(f"{agent_x._desc=} {len(agent_x._toolroot._acptfactunits)=}")
    # print(f"{agent_x._toolroot._acptfactunits=}")

    tool_list = agent_x.get_tool_list()
    assert tool_list
    assert len(tool_list) == 17

    usa_text = "USA"
    usa_road = f"{state_road},{usa_text}"
    oregon_text = "Oregon"
    oregon_road = f"{usa_road},{oregon_text}"

    wed = sufffactunit_shop(need=wed_road)
    wed._status = True
    wed._task = False
    usa = sufffactunit_shop(need=usa_road)
    usa._status = True
    usa._task = False

    wed_lu = RequiredUnit(base=week_road, sufffacts={wed.need: wed})
    sta_lu = RequiredUnit(base=state_road, sufffacts={usa.need: usa})
    wed_lh = RequiredHeir(
        base=week_road,
        sufffacts={wed.need: wed},
        _status=True,
        _task=False,
        _curr_tool_active_status=True,
    )
    sta_lh = RequiredHeir(
        base=state_road,
        sufffacts={usa.need: usa},
        _status=True,
        _task=False,
        _curr_tool_active_status=True,
    )

    x1_requiredunits = {
        wed_lu.base: wed_lu,
        sta_lu.base: sta_lu,
    }
    x1_requiredheirs = {
        wed_lh.base: wed_lh,
        sta_lh.base: sta_lh,
    }

    # WHEN
    agent_x.set_acptfact(base=state_road, pick=oregon_road)

    # THEN
    work_tool = agent_x._tool_dict.get(work_road)
    print(f"\nlook at {work_tool.get_road()=}")
    assert work_tool._walk == f"{agent_x._desc}"
    assert work_tool._kids == {}
    assert work_tool._weight == 30
    assert work_tool._desc == work_text
    assert work_tool._level == 1
    assert work_tool._active_status
    assert work_tool.promise
    # print(f"{work_tool._requiredheirs=}")
    curr_requiredheir_state = work_tool._requiredheirs[state_road]
    print(f"  {curr_requiredheir_state=}")
    print(f"  {curr_requiredheir_state._status=}\n")
    # assert work_tool._requiredheirs == x1_requiredheirs

    assert len(work_tool._requiredheirs) == len(x1_requiredheirs)
    week_requiredheir = work_tool._requiredheirs.get(week_road)
    # usa_sufffact = week_requiredheir.sufffacts.get(usa_road)
    print(f"    {work_tool._desc=}")
    # print(f"    {usa_sufffact.base=}")
    # print(f"    {usa_sufffact._task=}")
    # print(f"    {usa_sufffact._task=}")
    assert week_requiredheir._task == False
    # print(f"      sufffacts: {w=}")
    # w_need = usa_sufffact.sufffacts[wed_road].need
    # print(f"      {w_need=}")
    # assert usa_sufffact._task == w_need._task
    # assert usa_sufffact._status == w_need._status
    # assert week_requiredheir.sufffacts == week_requiredheir.sufffacts

    # assert work_tool._requiredunits == x1_requiredunits

    # print("iterate through every tool...")
    # for curr_tool in tool_list:
    #     if str(type(curr_tool)).find(".tool.ToolKid'>") > 0:
    #         assert curr_tool._active_status != None

    #     # print("")
    #     # print(f"{curr_tool._desc=}")
    #     # print(f"{len(curr_tool._requiredunits)=}")
    #     print(
    #         f"  {curr_tool._desc} iterate through every requiredheir... {len(curr_tool._requiredheirs)=} {curr_tool._desc=}"
    #     )
    #     # print(f"{curr_tool._requiredheirs=}")
    #     for required in curr_tool._requiredheirs.values():
    #         assert str(type(required)).find(".required.RequiredHeir'>") > 0
    #         print(f"    {required.base=}")
    #         assert required._status != None
    #         for sufffact_x in required.sufffacts.values():
    #             assert sufffact_x._status != None
    #         assert _check_all_elements_in_dict_are_correct_type(
    #             x_dict=required.sufffacts, type_str="src.agent.required.SuffFactUnit"
    #         )


def test_agent_set_agent_metrics_CorrectlyClears_agent_coin():
    # GIVEN
    ax = get_agent_with7amCleanTableRequired()
    src_text = "src"
    work_text = "work"
    catt_text = "feed cat"
    week_text = "weekdays"
    ax._toolroot._agent_coin_onset = 13
    ax._toolroot._agent_coin_cease = 13
    ax._toolroot._kids.get(work_text)._agent_coin_onset = 13
    ax._toolroot._kids.get(work_text)._agent_coin_cease = 13
    ax._toolroot._kids.get(catt_text)._agent_coin_onset = 13
    ax._toolroot._kids.get(catt_text)._agent_coin_cease = 13
    ax._toolroot._kids.get(week_text)._agent_coin_onset = 13
    ax._toolroot._kids.get(week_text)._agent_coin_cease = 13

    assert ax._toolroot._agent_coin_onset == 13
    assert ax._toolroot._agent_coin_cease == 13
    assert ax._toolroot._kids.get(work_text)._agent_coin_onset == 13
    assert ax._toolroot._kids.get(work_text)._agent_coin_cease == 13
    assert ax._toolroot._kids.get(catt_text)._agent_coin_onset == 13
    assert ax._toolroot._kids.get(catt_text)._agent_coin_cease == 13
    assert ax._toolroot._kids.get(week_text)._agent_coin_onset == 13
    assert ax._toolroot._kids.get(week_text)._agent_coin_cease == 13

    # WHEN
    ax.set_agent_metrics()

    # THEN
    assert ax._toolroot._agent_coin_onset != 13
    assert ax._toolroot._agent_coin_cease != 13
    assert ax._toolroot._kids.get(work_text)._agent_coin_onset != 13
    assert ax._toolroot._kids.get(work_text)._agent_coin_cease != 13
    assert ax._toolroot._kids.get(catt_text)._agent_coin_onset != 13
    assert ax._toolroot._kids.get(catt_text)._agent_coin_cease != 13
    assert ax._toolroot._kids.get(week_text)._agent_coin_onset != 13
    assert ax._toolroot._kids.get(week_text)._agent_coin_cease != 13


def test_agent_get_tool_list_CorrectlyCalculatesToolAttr_agent_coin():
    # GIVEN
    src_text = "src"
    ax = AgentUnit(_weight=10, _desc=src_text)

    auto_text = "auto"
    auto_tool = ToolKid(_desc=auto_text, _weight=10)
    ax.add_tool(tool_kid=auto_tool, walk=src_text)

    barn_text = "barn"
    barn_road = f"{src_text},{barn_text}"
    barn_tool = ToolKid(_desc=barn_text, _weight=60)
    ax.add_tool(tool_kid=barn_tool, walk=src_text)
    lamb_text = "lambs"
    lamb_road = f"{barn_road},{lamb_text}"
    lamb_tool = ToolKid(_desc=lamb_text, _weight=1)
    ax.add_tool(tool_kid=lamb_tool, walk=barn_road)
    duck_text = "ducks"
    duck_road = f"{barn_road},{duck_text}"
    duck_tool = ToolKid(_desc=duck_text, _weight=2)
    ax.add_tool(tool_kid=duck_tool, walk=barn_road)

    coal_text = "coal"
    coal_tool = ToolKid(_desc=coal_text, _weight=30)
    ax.add_tool(tool_kid=coal_tool, walk=src_text)

    assert ax._toolroot._agent_coin_onset is None
    assert ax._toolroot._agent_coin_cease is None
    assert ax._toolroot._kids.get(auto_text)._agent_coin_onset is None
    assert ax._toolroot._kids.get(auto_text)._agent_coin_cease is None
    assert ax._toolroot._kids.get(barn_text)._agent_coin_onset is None
    assert ax._toolroot._kids.get(barn_text)._agent_coin_cease is None
    assert ax._toolroot._kids.get(coal_text)._agent_coin_onset is None
    assert ax._toolroot._kids.get(coal_text)._agent_coin_cease is None
    lamb_before = ax.get_tool_kid(road=lamb_road)
    assert lamb_before._agent_coin_onset is None
    assert lamb_before._agent_coin_cease is None
    duck_before = ax.get_tool_kid(road=duck_road)
    assert duck_before._agent_coin_onset is None
    assert duck_before._agent_coin_cease is None

    # WHEN
    ax.set_agent_metrics()

    # THEN
    assert ax._toolroot._agent_coin_onset == 0.0
    assert ax._toolroot._agent_coin_cease == 1.0
    assert ax._toolroot._kids.get(auto_text)._agent_coin_onset == 0.0
    assert ax._toolroot._kids.get(auto_text)._agent_coin_cease == 0.1
    assert ax._toolroot._kids.get(barn_text)._agent_coin_onset == 0.1
    assert ax._toolroot._kids.get(barn_text)._agent_coin_cease == 0.7
    assert ax._toolroot._kids.get(coal_text)._agent_coin_onset == 0.7
    assert ax._toolroot._kids.get(coal_text)._agent_coin_cease == 1.0

    duck_after = ax.get_tool_kid(road=duck_road)
    assert duck_after._agent_coin_onset == 0.1
    assert duck_after._agent_coin_cease == 0.5
    lamb_after = ax.get_tool_kid(road=lamb_road)
    assert lamb_after._agent_coin_onset == 0.5
    assert lamb_after._agent_coin_cease == 0.7


def test_agent_get_tool_list_without_root_CorrectlyCalculatesToolAttributes():
    # GIVEN
    agent_x = get_agent_with7amCleanTableRequired()

    # WHEN
    tool_list_without_toolroot = agent_x.get_tool_list_without_toolroot()
    tool_list_with_toolroot = agent_x.get_tool_list()

    # THEN
    assert len(tool_list_without_toolroot) == 29
    assert len(tool_list_without_toolroot) + 1 == len(tool_list_with_toolroot)

    # for tool in agent_x.get_tool_list_without_toolroot():
    #     assert str(type(tool)).find(".tool.ToolKid'>") > 0

    # for tool in agent_x.get_tool_list_without_toolroot():
    #     print(f"{tool._desc=}")


def test_agent_get_tool_list_CorrectlyCalculatesRangeAttributes():
    # GIVEN
    agent_x = get_agent_with7amCleanTableRequired()
    tool_list = agent_x.get_tool_list()
    housework = "housework"
    house_road = f"{agent_x._desc},{housework}"
    clean_text = "clean table"
    clean_road = f"{house_road},{clean_text}"
    assert agent_x._tool_dict.get(clean_road)._active_status == False

    # set acptfacts as midnight to 8am
    day24hr_base = f"{agent_x._desc},timetech,24hr day"
    day24hr_pick = f"{agent_x._desc},timetech,24hr day"
    day24hr_open = 0.0
    day24hr_nigh = 8.0

    # WHEN
    agent_x.set_acptfact(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )

    # THEN
    agent_x.set_agent_metrics()
    assert agent_x._tool_dict.get(clean_road)._active_status

    # WHEN
    # set acptfacts as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(agent_x._toolroot._acptfactunits["src,timetech,24hr day"])
    agent_x.set_acptfact(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )
    print(agent_x._toolroot._acptfactunits["src,timetech,24hr day"])
    print(agent_x._toolroot._kids["housework"]._kids[clean_text]._requiredunits)
    # agent_x._toolroot._kids["housework"]._kids[clean_text]._active_status = None

    # THEN
    agent_x.set_agent_metrics()
    assert agent_x._tool_dict.get(clean_road)._active_status == False


def test_get_agenda_items():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()

    # WHEN
    promise_items = agent_x.get_agenda_items()

    # THEN
    assert promise_items != None
    assert len(promise_items) > 0
    assert len(promise_items) == 1


def test_exammple_tool_list_HasCorrectData():
    agent_x = agent_v001()
    print(f"{agent_x.get_required_bases()=}")
    # day_hour = "TlME,day_hour"
    # agent_x.set_acptfact(base=day_hour, pick=day_hour, open=0, nigh=23)
    hour_minute = "TlME,day_minute"
    agent_x.set_acptfact(base=hour_minute, pick=hour_minute, open=0, nigh=1439)
    print("yeahyea")
    mood = "TlME,Moods"
    agent_x.set_acptfact(base=mood, pick=mood)
    print(f"{agent_x.get_required_bases()=}")
    year_month = "TlME,year_month"
    agent_x.set_acptfact(base=year_month, pick=year_month)
    internet = "TlME,Internet"
    agent_x.set_acptfact(base=internet, pick=internet)
    assert agent_x != None
    # print(f"{agent_x._desc=}")
    # print(f"{len(agent_x._toolroot._kids)=}")
    ulty_text = "Ultimate Frisbee"
    ulty_road = f"{agent_x._desc},{ulty_text}"

    # if agent_x._toolroot._kids["Ultimate Frisbee"]._desc == "Ultimate Frisbee":
    assert agent_x._toolroot._kids[ulty_text]._requiredunits != None
    assert agent_x._desc != None

    # for acptfact in agent_x._toolroot._acptfactunits.values():
    #     print(f"{acptfact=}")

    tool_list = agent_x.get_tool_list()
    # print(f"{str(type(tool))=}")
    # print(f"{len(tool_list)=}")
    laundry_text = "laundry monday"
    laundry_road = f"{agent_x._desc},casa,cleaning,{laundry_text}"

    # for tool in tool_list:
    #     assert (
    #         str(type(tool)).find(".tool.ToolRoot'>") > 0
    #         or str(type(tool)).find(".tool.ToolKid'>") > 0
    #     )
    #     # print(f"{tool._desc=}")
    #     if tool._desc == laundry_text:
    #         for required in tool._requiredunits.values():
    #             print(f"{tool._desc=} {required.base=}")  # {required.sufffacts=}")
    # assert tool._active_status == False
    assert agent_x._tool_dict.get(laundry_road)._active_status == False

    # WHEN
    agent_x.set_acptfact(base="TlME,weekdays", pick="TlME,weekdays,Monday")

    agent_x.set_agent_metrics()

    # THEN
    assert agent_x._tool_dict.get(laundry_road)._active_status == False


def test_exammple_tool_list_OptionWeekdaysCorrectlyWork():
    # GIVEN
    agent_x = agent_v001()
    day_hour = "TlME,day_hour"
    agent_x.set_acptfact(base=day_hour, pick=day_hour, open=0, nigh=23)
    day_minute = "TlME,day_minute"
    agent_x.set_acptfact(base=day_minute, pick=day_minute, open=0, nigh=59)
    month_week = "TlME,month_week"
    agent_x.set_acptfact(base=month_week, pick=month_week)
    nations = "TlME,Nation-States"
    agent_x.set_acptfact(base=nations, pick=nations)
    mood = "TlME,Moods"
    agent_x.set_acptfact(base=mood, pick=mood)
    aaron = "TlME,Aaron Donald sphere"
    agent_x.set_acptfact(base=aaron, pick=aaron)
    internet = "TlME,Internet"
    agent_x.set_acptfact(base=internet, pick=internet)
    year_month = "TlME,year_month"
    agent_x.set_acptfact(base=year_month, pick=year_month, open=0, nigh=1000)

    tool_list = agent_x.get_tool_list()
    missing_acptfacts = agent_x.get_missing_acptfact_bases()
    # for missing_acptfact, count in missing_acptfacts.items():
    #     print(f"{missing_acptfact=} {count=}")

    weekday_road = "TlME,weekdays"
    mon_road = "TlME,weekdays,Monday"
    tue_road = "TlME,weekdays,Tuesday"
    mon_sufffact_x = sufffactunit_shop(need=mon_road)
    tue_sufffact_x = sufffactunit_shop(need=tue_road)
    mt_sufffacts = {
        mon_sufffact_x.need: mon_sufffact_x,
        tue_sufffact_x.need: tue_sufffact_x,
    }
    mt_required = RequiredUnit(base=weekday_road, sufffacts=mt_sufffacts)
    mt_required_x = RequiredHeir(base=weekday_road, sufffacts=mt_sufffacts)
    agent_x._toolroot.set_required_unit(required=mt_required)
    # print(f"{agent_x._requiredunits[weekday_road].base=}")
    # print(f"{agent_x._requiredunits[weekday_road].sufffacts[mon_road].need=}")
    # print(f"{agent_x._requiredunits[weekday_road].sufffacts[tue_road].need=}")
    print(f"{agent_x._toolroot._requiredunits[weekday_road].sufffacts=}")
    sufffact_mon = agent_x._toolroot._requiredunits[weekday_road].sufffacts.get(
        mon_road
    )
    sufffact_tue = agent_x._toolroot._requiredunits[weekday_road].sufffacts.get(
        tue_road
    )
    assert sufffact_mon
    assert sufffact_mon == mt_required.sufffacts[sufffact_mon.need]
    assert sufffact_tue
    assert sufffact_tue == mt_required.sufffacts[sufffact_tue.need]
    assert agent_x._toolroot._requiredunits[weekday_road] == mt_required

    # WHEN
    tool_list = agent_x.get_tool_list()

    # THEN
    assert sufffact_mon
    assert sufffact_mon == mt_required.sufffacts[sufffact_mon.need]
    assert sufffact_tue
    assert sufffact_tue == mt_required.sufffacts[sufffact_tue.need]

    assert agent_x._toolroot._requiredheirs[weekday_road] == mt_required_x

    bird_walk = "TlME,casa"
    bird_desc = "say hi to birds"
    bird_road = Road(f"{bird_walk},{bird_desc}")
    assert from_list_get_active_status(road=bird_road, tool_list=tool_list) == False

    agent_x.set_acptfact(base="TlME,weekdays", pick="TlME,weekdays,Monday")
    tool_list = agent_x.get_tool_list()
    casa_tool = agent_x._toolroot._kids["casa"]
    twee_tool = casa_tool._kids["say hi to birds"]
    print(f"{len(agent_x._toolroot._requiredheirs)=}")
    print(f"{len(casa_tool._requiredheirs)=}")
    print(f"{len(twee_tool._requiredheirs)=}")

    # assert YR.get_active_status(road=bird_tool, tool_list=tool_list) == True

    # agent_x.set_acptfact(base="TlME,weekdays", pick="TlME,weekdays,Tuesday")
    # tool_list = agent_x.get_tool_list()
    # assert YR.get_active_status(road=bird_tool, tool_list=tool_list) == True

    # agent_x.set_acptfact(base="TlME,weekdays", pick="TlME,weekdays,Wednesday")
    # tool_list = agent_x.get_tool_list()
    # assert YR.get_active_status(road=bird_tool, tool_list=tool_list) == False


def test_exammple_tool_list_Every6WeeksRequired():
    # GIVEN
    agent_x = agent_v001()
    src_text = "TlME"
    day_text = "day_hour"
    day_road = f"{src_text},{day_text}"
    min_text = "day_minute"
    min_road = f"{src_text},{day_text}"

    # WHEN
    agent_x.set_acptfact(base=day_road, pick=day_road, open=0, nigh=23)
    agent_x.set_acptfact(base=min_road, pick=min_road, open=0, nigh=59)
    tool_list = agent_x.get_tool_list()

    # THEN
    ced_week_base = f"{src_text},ced_week"

    sufffact_divisor = None
    sufffact_open = None
    sufffact_nigh = None
    print(f"{len(tool_list)=}")

    clean_sheet_road = "TlME,casa,cleaning,clean sheets couch blankets"
    clean_sheet_tool = agent_x.get_tool_kid(road=clean_sheet_road)
    # print(f"{clean_sheet_tool._requiredunits.values()=}")
    ced_week_required = clean_sheet_tool._requiredunits.get(ced_week_base)
    ced_week_suffact = ced_week_required.sufffacts.get(ced_week_base)
    print(
        f"{clean_sheet_tool._desc=} {ced_week_required.base=} {ced_week_suffact.need=}"
    )
    # print(f"{clean_sheet_tool._desc=} {ced_week_required.base=} {sufffact_x=}")
    sufffact_divisor = ced_week_suffact.divisor
    sufffact_open = ced_week_suffact.open
    sufffact_nigh = ced_week_suffact.nigh
    # print(f"{tool._requiredunits=}")
    assert clean_sheet_tool._active_status == False

    # for tool in tool_list:
    #     # print(f"{tool._walk=}")
    #     if tool._desc == "clean sheets couch blankets":
    #         print(f"{tool.get_road()=}")

    assert sufffact_divisor == 6
    assert sufffact_open == 1
    print(
        "There exists a tool with a required_base TlME,ced_week that also has lemmet div =6 and open/nigh =1"
    )
    # print(f"{len(tool_list)=}")
    ced_week_open = 6001

    # WHEN
    agent_x.set_acptfact(
        base=ced_week_base, pick=ced_week_base, open=ced_week_open, nigh=ced_week_open
    )
    nation_text = "Nation-States"
    nation_road = f"{src_text},{nation_text}"
    agent_x.set_acptfact(base=nation_road, pick=nation_road)
    print(
        f"Nation-states set and also acptfact set: {ced_week_base=} with {ced_week_open=} and {ced_week_open=}"
    )
    print(f"{agent_x._toolroot._acptfactunits=}")
    tool_list = agent_x.get_tool_list()

    # THEN
    week_text = "ced_week"
    week_road = f"TlME,{week_text}"
    clean_couch_text = "clean sheets couch blankets"
    clean_couch_road = f"TlME,casa,cleaning,{clean_couch_text}"
    clean_couch_tool = agent_x.get_tool_kid(road=clean_couch_road)
    week_required = clean_couch_tool._requiredunits.get(week_road)
    week_sufffact = week_required.sufffacts.get(week_road)
    print(f"{clean_couch_tool._desc=} {week_required.base=} {week_sufffact=}")
    assert week_sufffact.divisor == 6 and week_sufffact.open == 1


def print_sufffact_info(road: str, tool_list):
    satiate_status = None
    sufffact_divisor = None
    sufffact_open = None
    sufffact_nigh = None

    for tool in tool_list:
        if tool._walk == road:
            for required in tool._requiredunits.values():
                for sufffact_x in required.sufffacts.values():
                    print(
                        f"{tool._desc=} base:{required.base} need:{sufffact_x.need} open:{sufffact_x.open} nigh:{sufffact_x.nigh} div:{sufffact_x.divisor} status:{sufffact_x._status}"
                    )


def test_exammple_tool_list_EveryToolHasSatiateStatus():
    # GIVEN
    agent_x = agent_v001()

    # WHEN
    tool_list = agent_x.get_tool_list()

    # THEN
    print(f"{len(tool_list)=}")
    # first_tool_kid_count = 0
    # first_tool_kid_none_count = 0
    # first_tool_kid_true_count = 0
    # first_tool_kid_false_count = 0
    # for tool in tool_list:
    #     if str(type(tool)).find(".tool.ToolKid'>") > 0:
    #         first_tool_kid_count += 1
    #         if tool._active_status is None:
    #             first_tool_kid_none_count += 1
    #         elif tool._active_status:
    #             first_tool_kid_true_count += 1
    #         elif tool._active_status == False:
    #             first_tool_kid_false_count += 1

    # print(f"{first_tool_kid_count=}")
    # print(f"{first_tool_kid_none_count=}")
    # print(f"{first_tool_kid_true_count=}")
    # print(f"{first_tool_kid_false_count=}")

    # tool_kid_count = 0
    # for tool in tool_list_without_toolroot:
    #     tool_kid_count += 1
    #     print(f"{tool._desc=} {tool_kid_count=}")
    #     assert tool._active_status != None
    #     assert tool._active_status in (True, False)
    # assert tool_kid_count == len(tool_list_without_toolroot)

    assert len(tool_list) - 1 == sum(tool._active_status != None for tool in tool_list)
    assert 1 == sum(tool._active_status is None for tool in tool_list)


def test_exammple_tool_list_EveryOtherMonthWorks():
    # GIVEN
    agent_x = agent_v001()
    src_road = "TlME"
    minute_text = "day_minute"
    minute_road = f"{src_road},{minute_text}"
    agent_x.set_acptfact(base=minute_road, pick=minute_road, open=0, nigh=1399)
    month_text = "month_week"
    month_road = f"{src_road},{month_text}"
    agent_x.set_acptfact(base=month_road, pick=month_road)
    nations_text = "Nation-States"
    nations_road = f"{src_road},{nations_text}"
    agent_x.set_acptfact(base=nations_road, pick=nations_road)
    mood_text = "Moods"
    mood_road = f"{src_road},{mood_text}"
    agent_x.set_acptfact(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald sphere"
    aaron_road = f"{src_road},{aaron_text}"
    agent_x.set_acptfact(base=aaron_road, pick=aaron_road)
    internet_text = "Internet"
    internet_road = f"{src_road},{internet_text}"
    agent_x.set_acptfact(base=internet_road, pick=internet_road)
    weekdays_text = "weekdays"
    weekdays_road = f"{src_road},{weekdays_text}"
    agent_x.set_acptfact(base=weekdays_road, pick=weekdays_road)
    tool_list = agent_x.get_tool_list()
    print(f"{len(tool_list)=}")

    casa_text = "casa"
    casa_road = f"{src_road},{casa_text}"
    clean_text = "cleaning"
    clean_road = f"{casa_road},{clean_text}"
    mat_desc = "deep clean play mat"
    mat_road = Road(f"{clean_road},{mat_desc}")
    # commented out since it's difficult to understand
    assert from_list_get_active_status(road=mat_road, tool_list=tool_list) == False

    year_month_base = "TlME,year_month"
    print(f"{year_month_base=}, {year_month_base=}")

    # WHEN
    agent_x.set_acptfact(base=year_month_base, pick=year_month_base, open=0, nigh=8)
    ced_week = "TlME,ced_week"
    agent_x.set_acptfact(base=ced_week, pick=ced_week, open=0, nigh=4)

    # THEN
    tool_list = agent_x.get_tool_list()
    print(f"{len(tool_list)=}")
    print(f"{len(agent_x._toolroot._acptfactunits)=}")
    # from_list_get_active_status(road=mat_road, tool_list=tool_list)
    assert from_list_get_active_status(road=mat_road, tool_list=tool_list)
