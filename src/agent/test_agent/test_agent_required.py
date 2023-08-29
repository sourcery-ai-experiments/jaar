from pytest import raises as pytest_raises
from src.agent.examples.example_agents import (
    get_agent_with_4_levels as example_agents_get_agent_with_4_levels,
    get_agent_irrational_example as example_agents_get_agent_irrational_example,
)
from src.agent.tool import ToolKid
from src.agent.required import sufffactunit_shop, RequiredUnit, RequiredHeir
from src.agent.agent import AgentUnit
from src.agent.x_func import from_list_get_active_status


def test_agent_requiredunits_create():
    agent_x = example_agents_get_agent_with_4_levels()
    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"
    weekday_text = "weekdays"
    weekday_road = f"{agent_x._desc},{weekday_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekday_road},{wed_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    work_wk_required = RequiredUnit(
        base=weekday_road, sufffacts={wed_sufffact.need: wed_sufffact}
    )
    print(f"{type(work_wk_required.base)=}")
    print(f"{work_wk_required.base=}")
    agent_x.edit_tool_attr(road=work_road, required=work_wk_required)
    work_tool = agent_x._toolroot._kids[work_text]
    assert work_tool._requiredunits != None
    print(work_tool._requiredunits)
    assert work_tool._requiredunits[weekday_road] != None
    assert work_tool._requiredunits[weekday_road] == work_wk_required


def test_agent_set_requiredunits_status():
    agent_x = example_agents_get_agent_with_4_levels()
    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"
    weekday_text = "weekdays"
    weekday_road = f"{agent_x._desc},{weekday_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekday_road},{wed_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    work_wk_required = RequiredUnit(
        base=weekday_road, sufffacts={wed_sufffact.need: wed_sufffact}
    )
    print(f"{type(work_wk_required.base)=}")
    print(f"{work_wk_required.base=}")
    agent_x.edit_tool_attr(road=work_road, required=work_wk_required)
    work_tool = agent_x._toolroot._kids[work_text]
    assert work_tool._requiredunits != None
    print(work_tool._requiredunits)
    assert work_tool._requiredunits[weekday_road] != None
    assert work_tool._requiredunits[weekday_road] == work_wk_required


def test_agenda_returned_WhenNoRequiredsExist():
    lw_x = example_agents_get_agent_with_4_levels()
    lw_x.set_agent_metrics()
    work_text = "work"
    assert lw_x._toolroot._kids[work_text]._task == True
    cat_text = "feed cat"
    assert lw_x._toolroot._kids[cat_text]._task == True


def test_agent_requiredheirs_AreCorrectlyInherited():
    # GIVEN
    agent_x = example_agents_get_agent_with_4_levels()
    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"
    weekday_desc = "weekdays"
    weekday_road = f"{agent_x._desc},{weekday_desc}"
    wed_text = "Wednesday"
    wed_road = f"{weekday_road},{wed_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffact._status = False
    wed_sufffact._task = False
    sufffacts = {wed_sufffact.need: wed_sufffact}
    work_wk_build_requiredunit = RequiredUnit(base=weekday_road, sufffacts=sufffacts)
    work_wk_built_requiredheir = RequiredHeir(
        base=weekday_road,
        sufffacts=sufffacts,
        _status=False,
        _curr_tool_active_status=True,
    )
    print(f"{work_wk_build_requiredunit.base=}")
    agent_x.edit_tool_attr(road=work_road, required=work_wk_build_requiredunit)
    work_tool = agent_x._toolroot._kids[work_text]
    assert work_tool._requiredunits != None
    # print(work_tool._requiredunits)
    assert work_tool._requiredunits[weekday_road] != None
    assert work_tool._requiredunits[weekday_road] == work_wk_build_requiredunit
    try:
        work_tool._requiredheirs[weekday_road]
    except TypeError as e:
        assert str(e) == "'NoneType' object is not subscriptable"

    tool_list = agent_x.get_tool_list()

    from_list_get_active_status(road=work_road, tool_list=tool_list)

    work_wk_cal_requiredheir = work_tool._requiredheirs[weekday_road]
    print(f"{len(work_wk_cal_requiredheir.sufffacts)=}")
    assert len(work_wk_cal_requiredheir.sufffacts) == 1
    sufffact_wed = work_wk_cal_requiredheir.sufffacts.get("src,weekdays,Wednesday")
    assert (
        sufffact_wed._task
        == work_wk_built_requiredheir.sufffacts[sufffact_wed.need]._task
    )
    assert sufffact_wed == work_wk_built_requiredheir.sufffacts[sufffact_wed.need]
    # for sufffact in work_wk_cal_requiredheir.sufffacts.values():
    #     # assert sufffact_task == work_wk_built_requiredheir.sufffacts[sufffact.need]._task
    #     assert (
    #         sufffact._task == work_wk_built_requiredheir.sufffacts[sufffact.need]._task
    #     )
    #     assert sufffact == work_wk_built_requiredheir.sufffacts[sufffact.need]
    assert work_wk_cal_requiredheir.sufffacts == work_wk_built_requiredheir.sufffacts
    assert work_wk_cal_requiredheir == work_wk_built_requiredheir


def test_agent_requiredheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # GIVEN
    a4 = example_agents_get_agent_with_4_levels()
    work_text = "work"
    work_road = f"{a4._desc},{work_text}"
    week_text = "weekdays"
    week_road = f"{a4._desc},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffact._status = False
    wed_sufffact._task = False

    sufffacts_x = {wed_sufffact.need: wed_sufffact}
    work_wk_build_requiredunit = RequiredUnit(base=week_road, sufffacts=sufffacts_x)
    work_wk_built_requiredheir = RequiredHeir(
        base=week_road,
        sufffacts=sufffacts_x,
        _status=False,
        _curr_tool_active_status=True,
    )
    a4.edit_tool_attr(road=work_road, required=work_wk_build_requiredunit)

    # WHEN
    rla_text = "hp"
    rla_road = f"{work_road},{rla_text}"
    a4.add_tool(tool_kid=ToolKid(_desc=rla_text), walk=rla_road)
    cost_text = "cost_tracking"
    cost_road = f"{rla_road},{cost_text}"
    a4.add_tool(tool_kid=ToolKid(_desc=cost_text), walk=cost_road)
    a4.get_tool_list()

    # THEN
    work_tool = a4._toolroot._kids[work_text]
    rla_tool = work_tool._kids[rla_text]
    cost_tool = rla_tool._kids[cost_text]

    # 1
    work_wk_calc_requiredheir = work_tool._requiredheirs[week_road]
    assert work_wk_calc_requiredheir == work_wk_built_requiredheir

    # 2
    rla_week_requiredheir = rla_tool._requiredheirs[week_road]
    assert rla_week_requiredheir.base == work_wk_built_requiredheir.base
    assert rla_week_requiredheir.sufffacts == work_wk_built_requiredheir.sufffacts
    assert (
        rla_week_requiredheir.suff_tool_active_status
        == work_wk_built_requiredheir.suff_tool_active_status
    )
    assert rla_week_requiredheir._status == work_wk_built_requiredheir._status
    assert rla_week_requiredheir._task == work_wk_built_requiredheir._task
    assert rla_week_requiredheir._curr_tool_active_status
    assert rla_week_requiredheir._curr_tool_active_status != work_wk_built_requiredheir

    # 3
    cost_week_requiredheir = cost_tool._requiredheirs[week_road]
    assert cost_week_requiredheir.base == work_wk_built_requiredheir.base
    assert cost_week_requiredheir.sufffacts == work_wk_built_requiredheir.sufffacts
    assert (
        cost_week_requiredheir.suff_tool_active_status
        == work_wk_built_requiredheir.suff_tool_active_status
    )
    assert cost_week_requiredheir._status == work_wk_built_requiredheir._status
    assert cost_week_requiredheir._task == work_wk_built_requiredheir._task
    assert cost_week_requiredheir._curr_tool_active_status
    assert cost_week_requiredheir._curr_tool_active_status != work_wk_built_requiredheir


def test_agent_requiredheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4 = example_agents_get_agent_with_4_levels()
    work_text = "work"
    work_road = f"{a4._desc},{work_text}"
    week_desc = "weekdays"
    week_road = f"{a4._desc},{week_desc}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffact._status = False
    wed_sufffact._task = False
    sufffacts = {wed_sufffact.need: wed_sufffact}
    work_wk_build_requiredunit = RequiredUnit(base=week_road, sufffacts=sufffacts)
    work_wk_built_requiredheir = RequiredHeir(
        base=week_road,
        sufffacts=sufffacts,
        _status=False,
        _curr_tool_active_status=True,
    )
    a4.edit_tool_attr(road=work_road, required=work_wk_build_requiredunit)
    rla_text = "hp"
    rla_road = f"{work_road},{rla_text}"
    a4.add_tool(tool_kid=ToolKid(_desc=rla_text), walk=rla_road)
    cost_text = "cost_tracking"
    cost_road = f"{rla_road},{cost_text}"
    a4.add_tool(tool_kid=ToolKid(_desc=cost_text), walk=cost_road)

    work_tool = a4._toolroot._kids[work_text]
    rla_tool = work_tool._kids[rla_text]
    cost_tool = rla_tool._kids[cost_text]

    assert a4._toolroot._requiredheirs is None
    assert work_tool._requiredheirs is None
    assert rla_tool._requiredheirs is None
    assert cost_tool._requiredheirs is None

    # WHEN
    tool_list = a4.get_tool_list()

    # THEN
    assert a4._toolroot._requiredheirs == {}  # work_wk_built_requiredheir

    # 1
    assert work_tool._requiredheirs[week_road] == work_wk_built_requiredheir

    # 2
    rla_week_requiredheir = rla_tool._requiredheirs[week_road]
    assert rla_week_requiredheir.base == work_wk_built_requiredheir.base
    assert rla_week_requiredheir.sufffacts == work_wk_built_requiredheir.sufffacts
    assert (
        rla_week_requiredheir.suff_tool_active_status
        == work_wk_built_requiredheir.suff_tool_active_status
    )
    assert rla_week_requiredheir._status == work_wk_built_requiredheir._status
    assert rla_week_requiredheir._task == work_wk_built_requiredheir._task
    assert rla_week_requiredheir._curr_tool_active_status
    assert rla_week_requiredheir._curr_tool_active_status != work_wk_built_requiredheir

    # 3
    cost_week_requiredheir = cost_tool._requiredheirs[week_road]
    assert cost_week_requiredheir.base == work_wk_built_requiredheir.base
    assert cost_week_requiredheir.sufffacts == work_wk_built_requiredheir.sufffacts
    assert (
        cost_week_requiredheir.suff_tool_active_status
        == work_wk_built_requiredheir.suff_tool_active_status
    )
    assert cost_week_requiredheir._status == work_wk_built_requiredheir._status
    assert cost_week_requiredheir._task == work_wk_built_requiredheir._task
    assert cost_week_requiredheir._curr_tool_active_status
    assert cost_week_requiredheir._curr_tool_active_status != work_wk_built_requiredheir


def test_agent_requiredunits_set_UnCoupledMethod():
    # Given
    agent_x = example_agents_get_agent_with_4_levels()
    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"
    weekday_text = "weekdays"
    weekday_road = f"{agent_x._desc},{weekday_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekday_road},{wed_text}"

    # When
    agent_x.edit_tool_attr(
        road=work_road, required_base=weekday_road, required_sufffact=wed_road
    )

    # Then
    work_tool1 = agent_x.get_tool_kid(road=work_road)
    assert work_tool1._requiredunits != None
    print(work_tool1._requiredunits)
    assert work_tool1._requiredunits[weekday_road] != None
    assert work_tool1._requiredunits[weekday_road].sufffacts[wed_road].open is None
    assert work_tool1._requiredunits[weekday_road].sufffacts[wed_road].nigh is None

    work_wk_required1 = RequiredUnit(base=weekday_road, sufffacts=None)
    work_wk_required1.set_sufffact(sufffact=wed_road)
    print(f" {type(work_wk_required1.base)=}")
    print(f" {work_wk_required1.base=}")
    assert work_tool1._requiredunits[weekday_road] == work_wk_required1

    # Given
    divisor_x = 34
    open_x = 12
    nigh_x = 12

    # When
    agent_x.edit_tool_attr(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=wed_road,
        required_sufffact_divisor=divisor_x,
        required_sufffact_open=open_x,
        required_sufffact_nigh=nigh_x,
    )

    # Then
    assert work_tool1._requiredunits[weekday_road].sufffacts[wed_road].open == 12
    assert work_tool1._requiredunits[weekday_road].sufffacts[wed_road].nigh == 12

    wed_sufffact2 = sufffactunit_shop(
        need=wed_road, divisor=divisor_x, open=open_x, nigh=nigh_x
    )
    work_wk_required2 = RequiredUnit(
        base=weekday_road, sufffacts={wed_sufffact2.need: wed_sufffact2}
    )
    print(f"{type(work_wk_required2.base)=}")
    print(f"{work_wk_required2.base=}")
    assert work_tool1._requiredunits[weekday_road] == work_wk_required2

    # When
    thu_text = "Thursday"
    thu_road = f"{weekday_road},{thu_text}"
    agent_x.edit_tool_attr(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=thu_road,
        required_sufffact_divisor=divisor_x,
        required_sufffact_open=open_x,
        required_sufffact_nigh=nigh_x,
    )

    # Then
    assert len(work_tool1._requiredunits[weekday_road].sufffacts) == 2


def test_agent_requiredunits_set_sufffactToolWithDenomSetsSuffFactDivision():
    # Given
    agent_x = example_agents_get_agent_with_4_levels()
    work = "work"
    work_road = f"{agent_x._desc},{work}"
    time = "time"
    time_road = f"{agent_x._desc},{time}"
    week = "week"
    week_road = f"{agent_x._desc},{time},{week}"
    agent_x.add_tool(
        tool_kid=ToolKid(_desc=time, _begin=100, _close=2000), walk=agent_x._desc
    )
    agent_x.add_tool(tool_kid=ToolKid(_desc=week, _denom=7), walk=time_road)

    # When
    agent_x.edit_tool_attr(
        road=work_road,
        required_base=time_road,
        required_sufffact=week_road,
        required_sufffact_open=2,
        required_sufffact_nigh=5,
        required_sufffact_divisor=None,
    )

    # Then
    work_tool1 = agent_x.get_tool_kid(road=work_road)
    assert work_tool1._requiredunits[time_road] != None
    assert work_tool1._requiredunits[time_road].sufffacts[week_road].divisor == 7
    assert work_tool1._requiredunits[time_road].sufffacts[week_road].open == 2
    assert work_tool1._requiredunits[time_road].sufffacts[week_road].nigh == 5


def test_agent_requiredunits_set_sufffactToolWithBeginCloseSetsSuffFactOpenNigh():
    # Given
    agent_x = example_agents_get_agent_with_4_levels()
    work = "work"
    work_road = f"{agent_x._desc},{work}"
    time = "time"
    time_road = f"{agent_x._desc},{time}"
    rus_war = "rus_war"
    rus_war_road = f"{agent_x._desc},{time},{rus_war}"
    agent_x.add_tool(
        tool_kid=ToolKid(_desc=time, _begin=100, _close=2000), walk=agent_x._desc
    )
    agent_x.add_tool(
        tool_kid=ToolKid(_desc=rus_war, _begin=22, _close=34), walk=time_road
    )

    # When
    agent_x.edit_tool_attr(
        road=work_road,
        required_base=time_road,
        required_sufffact=rus_war_road,
        required_sufffact_open=None,
        required_sufffact_nigh=None,
        required_sufffact_divisor=None,
    )

    # Then
    work_tool1 = agent_x.get_tool_kid(road=work_road)
    assert work_tool1._requiredunits[time_road] != None
    assert work_tool1._requiredunits[time_road].sufffacts[rus_war_road].divisor is None
    assert work_tool1._requiredunits[time_road].sufffacts[rus_war_road].open == 22
    assert work_tool1._requiredunits[time_road].sufffacts[rus_war_road].nigh == 34


def test_agent_requiredunits_del_required_sufffact_UncoupledMethod1():
    # Given
    agent_x = example_agents_get_agent_with_4_levels()
    work_road = f"{agent_x._desc},work"
    weekday_road = f"{agent_x._desc},weekdays"
    wed_road = f"{agent_x._desc},weekdays,Wednesday"

    agent_x.edit_tool_attr(
        road=work_road, required_base=weekday_road, required_sufffact=wed_road
    )
    thu_road = f"{agent_x._desc},weekdays,Thursday"
    agent_x.edit_tool_attr(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=thu_road,
    )
    work_tool1 = agent_x.get_tool_kid(road=work_road)
    assert len(work_tool1._requiredunits[weekday_road].sufffacts) == 2

    # When
    agent_x.del_tool_required_sufffact(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=thu_road,
    )

    # Then
    assert len(work_tool1._requiredunits[weekday_road].sufffacts) == 1

    # When
    agent_x.del_tool_required_sufffact(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=wed_road,
    )

    # Then
    with pytest_raises(KeyError) as excinfo:
        work_tool1._requiredunits[weekday_road]
    assert str(excinfo.value) == f"'{weekday_road}'"
    assert work_tool1._requiredunits == {}


def test_agent_requiredunits_del_required_sufffact_UncoupledMethod2():
    # Given
    agent_x = example_agents_get_agent_with_4_levels()
    work_road = f"{agent_x._desc},work"
    weekdays_road = f"{agent_x._desc},weekdays"
    work_tool1 = agent_x.get_tool_kid(road=work_road)
    work_tool1.set_requiredunits_empty_if_null()
    assert len(work_tool1._requiredunits) == 0

    # When
    with pytest_raises(Exception) as excinfo:
        work_tool1.del_requiredunit_base(weekdays_road)
    assert str(excinfo.value) == f"No RequiredUnit at '{weekdays_road}'"


def test_agent_edit_tool_attr_agentIsAbleToEdit_suff_tool_active_status_AnyToolIfInvaildThrowsError():
    # _suff_tool_active_status: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # GIVEN
    agent_x = example_agents_get_agent_with_4_levels()
    src_road = agent_x._desc
    work_text = "work"
    work_road = f"{src_road},{work_text}"

    commute_text = "commute to work"
    commute_road = f"{src_road},{commute_text}"
    agent_x.add_tool(tool_kid=ToolKid(_desc=commute_text), walk=src_road)
    agent_x.get_tool_list()  # set tree metrics
    commute_tool = agent_x.get_tool_kid(road=commute_road)
    assert len(commute_tool._requiredunits) == 0

    # WHEN
    agent_x.edit_tool_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_tool_active_status=True,
    )

    # THEN
    assert len(commute_tool._requiredunits) == 1
    requiredunit_work = commute_tool._requiredunits.get(work_road)
    assert requiredunit_work.base == work_road
    assert len(requiredunit_work.sufffacts) == 0
    assert requiredunit_work.suff_tool_active_status == True

    # WHEN
    agent_x.edit_tool_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_tool_active_status=False,
    )

    # THEN
    assert len(commute_tool._requiredunits) == 1
    requiredunit_work = commute_tool._requiredunits.get(work_road)
    assert requiredunit_work.base == work_road
    assert len(requiredunit_work.sufffacts) == 0
    assert requiredunit_work.suff_tool_active_status == False

    # WHEN
    agent_x.edit_tool_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_tool_active_status="Set to Ignore",
    )

    # THEN
    assert len(commute_tool._requiredunits) == 1
    requiredunit_work = commute_tool._requiredunits.get(work_road)
    assert requiredunit_work.base == work_road
    assert len(requiredunit_work.sufffacts) == 0
    assert requiredunit_work.suff_tool_active_status is None


def test_agent_requiredunits_ToolUnitActiveStatusInfluencesRequiredUnitStatus():
    # GIVEN an Agent with 5 tools, 1 AcptFact:
    # 1. tool(...,weekdays) exists
    # 2. tool(...,weekdays,wednesday) exists
    # 3. tool(...,weekdays,thursday) exists
    agent_x = example_agents_get_agent_with_4_levels()
    src_road = agent_x._desc
    work_text = "work"
    work_road = f"{src_road},{work_text}"
    weekdays_text = "weekdays"
    weekdays_road = f"{src_road},{weekdays_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekdays_road},{wed_text}"
    thu_text = "Thursday"
    thu_road = f"{weekdays_road},{thu_text}"

    # 4. tool(...,work) with
    # 4.1 RequiredUnit: base=weekdays_road, need=thu_road
    # 4.2 .active_status = False
    agent_x.edit_tool_attr(
        road=work_road,
        required_base=weekdays_road,
        required_sufffact=thu_road,
    )
    agent_x.get_tool_list()  # set tree metrics
    work_tool = agent_x.get_tool_kid(road=work_road)
    assert work_tool._active_status == False

    # 5. tool(...,commute to work) with
    # 5.1. RequiredUnit: tool(base=...,work) has .suff_tool_active_status = True
    # 5.2. tool(...,work).active_status = False
    commute_text = "commute to work"
    commute_road = f"{src_road},{commute_text}"
    agent_x.add_tool(tool_kid=ToolKid(_desc=commute_text), walk=src_road)
    agent_x.edit_tool_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_tool_active_status=True,
    )
    commute_tool = agent_x.get_tool_kid(road=commute_road)
    agent_x.get_tool_list()
    assert commute_tool._active_status == False

    # AcptFact: base: (...,weekdays) pick: (...,weekdays,wednesday)
    agent_x.set_acptfact(base=weekdays_road, pick=wed_road)
    agent_x.set_agent_metrics()

    assert work_tool._active_status == False
    assert commute_tool._active_status == False

    # WHEN
    print("before changing acptfact")
    agent_x.set_acptfact(base=weekdays_road, pick=thu_road)
    print("after changing acptfact")
    agent_x.get_tool_list()
    assert work_tool._active_status == True

    # THEN
    assert commute_tool._active_status == True


def test_agent_set_agent_metrics_InitimemberSetsRationalAttrToFalse():
    # GIVEN
    agent_x = example_agents_get_agent_with_4_levels()
    assert agent_x._rational == False
    # agent_x.set_agent_metrics()
    agent_x._rational = True
    assert agent_x._rational

    # WHEN
    # hack agent to set _max_tree_traverse = 1 (not allowed, should always be 2 or more)
    agent_x._max_tree_traverse = 1
    agent_x.set_agent_metrics()

    # THEN
    assert not agent_x._rational


def test_agent_tree_traverses_StopWhenNoChangeInStatusIsDetected():
    # GIVEN
    agent_x = example_agents_get_agent_with_4_levels()
    assert agent_x._max_tree_traverse != 2

    # WHEN
    agent_x.set_agent_metrics()
    # for tool_key in agent_x._tool_dict.keys():
    #     print(f"{tool_key=}")

    # THEN
    assert agent_x._tree_traverse_count == 2


def test_agent_tree_traverse_count_CorrectlyCountsTreeTraversesForIrrationalAgents():
    # GIVEN irrational agent
    agent_x = example_agents_get_agent_irrational_example()
    agent_x.set_agent_metrics()
    assert agent_x._tree_traverse_count == 3

    # WHEN
    agent_x.set_max_tree_traverse(int_x=21)
    agent_x.set_agent_metrics()

    # THEN
    assert agent_x._tree_traverse_count == 21
