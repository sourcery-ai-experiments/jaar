from pytest import raises as pytest_raises
from src.calendar.examples.example_calendars import (
    get_calendar_with_4_levels as example_calendars_get_calendar_with_4_levels,
    get_calendar_irrational_example as example_calendars_get_calendar_irrational_example,
)
from src.calendar.idea import IdeaKid
from src.calendar.required_idea import sufffactunit_shop, RequiredUnit, RequiredHeir
from src.calendar.calendar import CalendarUnit
from src.calendar.road import get_global_root_desc as root_desc
from src.calendar.x_func import from_list_get_active_status


def test_calendar_requiredunits_create():
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{calendar_x._owner},{work_text}"
    weekday_text = "weekdays"
    weekday_road = f"{calendar_x._owner},{weekday_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekday_road},{wed_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    work_wk_required = RequiredUnit(
        base=weekday_road, sufffacts={wed_sufffact.need: wed_sufffact}
    )
    print(f"{type(work_wk_required.base)=}")
    print(f"{work_wk_required.base=}")
    calendar_x.edit_idea_attr(road=work_road, required=work_wk_required)
    work_idea = calendar_x._idearoot._kids[work_text]
    assert work_idea._requiredunits != None
    print(work_idea._requiredunits)
    assert work_idea._requiredunits[weekday_road] != None
    assert work_idea._requiredunits[weekday_road] == work_wk_required


def test_calendar_set_requiredunits_status():
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{calendar_x._owner},{work_text}"
    weekday_text = "weekdays"
    weekday_road = f"{calendar_x._owner},{weekday_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekday_road},{wed_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    work_wk_required = RequiredUnit(
        base=weekday_road, sufffacts={wed_sufffact.need: wed_sufffact}
    )
    print(f"{type(work_wk_required.base)=}")
    print(f"{work_wk_required.base=}")
    calendar_x.edit_idea_attr(road=work_road, required=work_wk_required)
    work_idea = calendar_x._idearoot._kids[work_text]
    assert work_idea._requiredunits != None
    print(work_idea._requiredunits)
    assert work_idea._requiredunits[weekday_road] != None
    assert work_idea._requiredunits[weekday_road] == work_wk_required


def test_agenda_returned_WhenNoRequiredsExist():
    lw_x = example_calendars_get_calendar_with_4_levels()
    lw_x.set_calendar_metrics()
    work_text = "work"
    assert lw_x._idearoot._kids[work_text]._task == True
    cat_text = "feed cat"
    assert lw_x._idearoot._kids[cat_text]._task == True


def test_calendar_requiredheirs_AreCorrectlyInherited_v1():
    # GIVEN
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{root_desc()},{work_text}"
    week_desc = "weekdays"
    week_road = f"{root_desc()},{week_desc}"
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
        _curr_idea_active_status=True,
    )
    print(f"{work_wk_build_requiredunit.base=}")
    calendar_x.edit_idea_attr(road=work_road, required=work_wk_build_requiredunit)
    work_idea = calendar_x._idearoot._kids[work_text]
    assert work_idea._requiredunits != None
    # print(work_idea._requiredunits)
    assert work_idea._requiredunits[week_road] != None
    assert work_idea._requiredunits[week_road] == work_wk_build_requiredunit
    try:
        work_idea._requiredheirs[week_road]
    except TypeError as e:
        assert str(e) == "'NoneType' object is not subscriptable"

    idea_list = calendar_x.get_idea_list()

    from_list_get_active_status(road=work_road, idea_list=idea_list)

    work_wk_cal_requiredheir = work_idea._requiredheirs[week_road]
    print(f"{len(work_wk_cal_requiredheir.sufffacts)=}")
    assert len(work_wk_cal_requiredheir.sufffacts) == 1
    sufffact_wed = work_wk_cal_requiredheir.sufffacts.get(wed_road)
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


def test_calendar_requiredheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # GIVEN
    a4 = example_calendars_get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{a4._owner},{work_text}"
    week_text = "weekdays"
    week_road = f"{a4._owner},{week_text}"
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
        _curr_idea_active_status=True,
    )
    a4.edit_idea_attr(road=work_road, required=work_wk_build_requiredunit)

    # WHEN
    rla_text = "hp"
    rla_road = f"{work_road},{rla_text}"
    a4.add_idea(idea_kid=IdeaKid(_desc=rla_text), walk=rla_road)
    cost_text = "cost_tracking"
    cost_road = f"{rla_road},{cost_text}"
    a4.add_idea(idea_kid=IdeaKid(_desc=cost_text), walk=cost_road)
    a4.get_idea_list()

    # THEN
    work_idea = a4._idearoot._kids[work_text]
    rla_idea = work_idea._kids[rla_text]
    cost_idea = rla_idea._kids[cost_text]

    # 1
    work_wk_calc_requiredheir = work_idea._requiredheirs[week_road]
    assert work_wk_calc_requiredheir == work_wk_built_requiredheir

    # 2
    rla_week_requiredheir = rla_idea._requiredheirs[week_road]
    assert rla_week_requiredheir.base == work_wk_built_requiredheir.base
    assert rla_week_requiredheir.sufffacts == work_wk_built_requiredheir.sufffacts
    assert (
        rla_week_requiredheir.suff_idea_active_status
        == work_wk_built_requiredheir.suff_idea_active_status
    )
    assert rla_week_requiredheir._status == work_wk_built_requiredheir._status
    assert rla_week_requiredheir._task == work_wk_built_requiredheir._task
    assert rla_week_requiredheir._curr_idea_active_status
    assert rla_week_requiredheir._curr_idea_active_status != work_wk_built_requiredheir

    # 3
    cost_week_requiredheir = cost_idea._requiredheirs[week_road]
    assert cost_week_requiredheir.base == work_wk_built_requiredheir.base
    assert cost_week_requiredheir.sufffacts == work_wk_built_requiredheir.sufffacts
    assert (
        cost_week_requiredheir.suff_idea_active_status
        == work_wk_built_requiredheir.suff_idea_active_status
    )
    assert cost_week_requiredheir._status == work_wk_built_requiredheir._status
    assert cost_week_requiredheir._task == work_wk_built_requiredheir._task
    assert cost_week_requiredheir._curr_idea_active_status
    assert cost_week_requiredheir._curr_idea_active_status != work_wk_built_requiredheir


def test_calendar_requiredheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4 = example_calendars_get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{a4._owner},{work_text}"
    week_desc = "weekdays"
    week_road = f"{a4._owner},{week_desc}"
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
        _curr_idea_active_status=True,
    )
    a4.edit_idea_attr(road=work_road, required=work_wk_build_requiredunit)
    rla_text = "hp"
    rla_road = f"{work_road},{rla_text}"
    a4.add_idea(idea_kid=IdeaKid(_desc=rla_text), walk=rla_road)
    cost_text = "cost_tracking"
    cost_road = f"{rla_road},{cost_text}"
    a4.add_idea(idea_kid=IdeaKid(_desc=cost_text), walk=cost_road)

    work_idea = a4._idearoot._kids[work_text]
    rla_idea = work_idea._kids[rla_text]
    cost_idea = rla_idea._kids[cost_text]

    assert a4._idearoot._requiredheirs is None
    assert work_idea._requiredheirs is None
    assert rla_idea._requiredheirs is None
    assert cost_idea._requiredheirs is None

    # WHEN
    idea_list = a4.get_idea_list()

    # THEN
    assert a4._idearoot._requiredheirs == {}  # work_wk_built_requiredheir

    # 1
    assert work_idea._requiredheirs[week_road] == work_wk_built_requiredheir

    # 2
    rla_week_requiredheir = rla_idea._requiredheirs[week_road]
    assert rla_week_requiredheir.base == work_wk_built_requiredheir.base
    assert rla_week_requiredheir.sufffacts == work_wk_built_requiredheir.sufffacts
    assert (
        rla_week_requiredheir.suff_idea_active_status
        == work_wk_built_requiredheir.suff_idea_active_status
    )
    assert rla_week_requiredheir._status == work_wk_built_requiredheir._status
    assert rla_week_requiredheir._task == work_wk_built_requiredheir._task
    assert rla_week_requiredheir._curr_idea_active_status
    assert rla_week_requiredheir._curr_idea_active_status != work_wk_built_requiredheir

    # 3
    cost_week_requiredheir = cost_idea._requiredheirs[week_road]
    assert cost_week_requiredheir.base == work_wk_built_requiredheir.base
    assert cost_week_requiredheir.sufffacts == work_wk_built_requiredheir.sufffacts
    assert (
        cost_week_requiredheir.suff_idea_active_status
        == work_wk_built_requiredheir.suff_idea_active_status
    )
    assert cost_week_requiredheir._status == work_wk_built_requiredheir._status
    assert cost_week_requiredheir._task == work_wk_built_requiredheir._task
    assert cost_week_requiredheir._curr_idea_active_status
    assert cost_week_requiredheir._curr_idea_active_status != work_wk_built_requiredheir


def test_calendar_requiredunits_set_UnCoupledMethod():
    # Given
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{root_desc()},{work_text}"
    week_text = "weekdays"
    week_road = f"{root_desc()},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"

    # When
    calendar_x.edit_idea_attr(
        road=work_road, required_base=week_road, required_sufffact=wed_road
    )

    # Then
    work_idea1 = calendar_x.get_idea_kid(road=work_road)
    assert work_idea1._requiredunits != None
    print(work_idea1._requiredunits)
    assert work_idea1._requiredunits[week_road] != None
    assert work_idea1._requiredunits[week_road].sufffacts[wed_road].open is None
    assert work_idea1._requiredunits[week_road].sufffacts[wed_road].nigh is None

    work_wk_required1 = RequiredUnit(base=week_road, sufffacts=None)
    work_wk_required1.set_sufffact(sufffact=wed_road)
    print(f" {type(work_wk_required1.base)=}")
    print(f" {work_wk_required1.base=}")
    assert work_idea1._requiredunits[week_road] == work_wk_required1

    # Given
    divisor_x = 34
    open_x = 12
    nigh_x = 12

    # When
    calendar_x.edit_idea_attr(
        road=work_road,
        required_base=week_road,
        required_sufffact=wed_road,
        required_sufffact_divisor=divisor_x,
        required_sufffact_open=open_x,
        required_sufffact_nigh=nigh_x,
    )

    # Then
    assert work_idea1._requiredunits[week_road].sufffacts[wed_road].open == 12
    assert work_idea1._requiredunits[week_road].sufffacts[wed_road].nigh == 12

    wed_sufffact2 = sufffactunit_shop(
        need=wed_road, divisor=divisor_x, open=open_x, nigh=nigh_x
    )
    work_wk_required2 = RequiredUnit(
        base=week_road, sufffacts={wed_sufffact2.need: wed_sufffact2}
    )
    print(f"{type(work_wk_required2.base)=}")
    print(f"{work_wk_required2.base=}")
    assert work_idea1._requiredunits[week_road] == work_wk_required2

    # When
    thu_text = "Thursday"
    thu_road = f"{week_road},{thu_text}"
    calendar_x.edit_idea_attr(
        road=work_road,
        required_base=week_road,
        required_sufffact=thu_road,
        required_sufffact_divisor=divisor_x,
        required_sufffact_open=open_x,
        required_sufffact_nigh=nigh_x,
    )

    # Then
    assert len(work_idea1._requiredunits[week_road].sufffacts) == 2


def test_calendar_requiredunits_set_sufffactIdeaWithDenomSetsSuffFactDivision():
    # Given
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{root_desc()},{work_text}"
    time_text = "time"
    time_road = f"{root_desc()},{time_text}"
    week_text = "week"
    week_road = f"{root_desc()},{time_text},{week_text}"
    calendar_x.add_idea(
        idea_kid=IdeaKid(_desc=time_text, _begin=100, _close=2000),
        walk=root_desc(),
    )
    calendar_x.add_idea(idea_kid=IdeaKid(_desc=week_text, _denom=7), walk=time_road)

    # When
    calendar_x.edit_idea_attr(
        road=work_road,
        required_base=time_road,
        required_sufffact=week_road,
        required_sufffact_open=2,
        required_sufffact_nigh=5,
        required_sufffact_divisor=None,
    )

    # Then
    work_idea1 = calendar_x.get_idea_kid(road=work_road)
    assert work_idea1._requiredunits[time_road] != None
    assert work_idea1._requiredunits[time_road].sufffacts[week_road].divisor == 7
    assert work_idea1._requiredunits[time_road].sufffacts[week_road].open == 2
    assert work_idea1._requiredunits[time_road].sufffacts[week_road].nigh == 5


def test_calendar_requiredunits_set_sufffactIdeaWithBeginCloseSetsSuffFactOpenNigh():
    # Given
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work = "work"
    work_road = f"{root_desc()},{work}"
    time = "time"
    time_road = f"{root_desc()},{time}"
    rus_war = "rus_war"
    rus_war_road = f"{root_desc()},{time},{rus_war}"
    calendar_x.add_idea(
        idea_kid=IdeaKid(_desc=time, _begin=100, _close=2000), walk=root_desc()
    )
    calendar_x.add_idea(
        idea_kid=IdeaKid(_desc=rus_war, _begin=22, _close=34), walk=time_road
    )

    # When
    calendar_x.edit_idea_attr(
        road=work_road,
        required_base=time_road,
        required_sufffact=rus_war_road,
        required_sufffact_open=None,
        required_sufffact_nigh=None,
        required_sufffact_divisor=None,
    )

    # Then
    work_idea1 = calendar_x.get_idea_kid(road=work_road)
    assert work_idea1._requiredunits[time_road] != None
    assert work_idea1._requiredunits[time_road].sufffacts[rus_war_road].divisor is None
    assert work_idea1._requiredunits[time_road].sufffacts[rus_war_road].open == 22
    assert work_idea1._requiredunits[time_road].sufffacts[rus_war_road].nigh == 34


def test_calendar_requiredunits_del_required_sufffact_UncoupledMethod1():
    # Given
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work_road = f"{root_desc()},work"
    weekday_road = f"{root_desc()},weekdays"
    wed_road = f"{root_desc()},weekdays,Wednesday"

    calendar_x.edit_idea_attr(
        road=work_road, required_base=weekday_road, required_sufffact=wed_road
    )
    thu_road = f"{root_desc()},weekdays,Thursday"
    calendar_x.edit_idea_attr(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=thu_road,
    )
    work_idea1 = calendar_x.get_idea_kid(road=work_road)
    assert len(work_idea1._requiredunits[weekday_road].sufffacts) == 2

    # When
    calendar_x.del_idea_required_sufffact(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=thu_road,
    )

    # Then
    assert len(work_idea1._requiredunits[weekday_road].sufffacts) == 1

    # When
    calendar_x.del_idea_required_sufffact(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=wed_road,
    )

    # Then
    with pytest_raises(KeyError) as excinfo:
        work_idea1._requiredunits[weekday_road]
    assert str(excinfo.value) == f"'{weekday_road}'"
    assert work_idea1._requiredunits == {}


def test_calendar_requiredunits_del_required_sufffact_UncoupledMethod2():
    # Given
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work_road = f"{root_desc()},work"
    weekdays_road = f"{root_desc()},weekdays"
    work_idea1 = calendar_x.get_idea_kid(road=work_road)
    work_idea1.set_requiredunits_empty_if_null()
    assert len(work_idea1._requiredunits) == 0

    # When
    with pytest_raises(Exception) as excinfo:
        work_idea1.del_requiredunit_base(weekdays_road)
    assert str(excinfo.value) == f"No RequiredUnit at '{weekdays_road}'"


def test_calendar_edit_idea_attr_calendarIsAbleToEdit_suff_idea_active_status_AnyIdeaIfInvaildThrowsError():
    # _suff_idea_active_status: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # GIVEN
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{root_desc()},{work_text}"

    commute_text = "commute to work"
    commute_road = f"{root_desc()},{commute_text}"
    calendar_x.add_idea(idea_kid=IdeaKid(_desc=commute_text), walk=root_desc())
    calendar_x.get_idea_list()  # set tree metrics
    commute_idea = calendar_x.get_idea_kid(road=commute_road)
    assert len(commute_idea._requiredunits) == 0

    # WHEN
    calendar_x.edit_idea_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_idea_active_status=True,
    )

    # THEN
    assert len(commute_idea._requiredunits) == 1
    requiredunit_work = commute_idea._requiredunits.get(work_road)
    assert requiredunit_work.base == work_road
    assert len(requiredunit_work.sufffacts) == 0
    assert requiredunit_work.suff_idea_active_status == True

    # WHEN
    calendar_x.edit_idea_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_idea_active_status=False,
    )

    # THEN
    assert len(commute_idea._requiredunits) == 1
    requiredunit_work = commute_idea._requiredunits.get(work_road)
    assert requiredunit_work.base == work_road
    assert len(requiredunit_work.sufffacts) == 0
    assert requiredunit_work.suff_idea_active_status == False

    # WHEN
    calendar_x.edit_idea_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_idea_active_status="Set to Ignore",
    )

    # THEN
    assert len(commute_idea._requiredunits) == 1
    requiredunit_work = commute_idea._requiredunits.get(work_road)
    assert requiredunit_work.base == work_road
    assert len(requiredunit_work.sufffacts) == 0
    assert requiredunit_work.suff_idea_active_status is None


def test_calendar_requiredunits_IdeaUnitActiveStatusInfluencesRequiredUnitStatus():
    # GIVEN an Calendar with 5 ideas, 1 AcptFact:
    # 1. idea(...,weekdays) exists
    # 2. idea(...,weekdays,wednesday) exists
    # 3. idea(...,weekdays,thursday) exists
    calendar_x = example_calendars_get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{root_desc()},{work_text}"
    weekdays_text = "weekdays"
    weekdays_road = f"{root_desc()},{weekdays_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekdays_road},{wed_text}"
    thu_text = "Thursday"
    thu_road = f"{weekdays_road},{thu_text}"

    # 4. idea(...,work) with
    # 4.1 RequiredUnit: base=weekdays_road, need=thu_road
    # 4.2 .active_status = False
    calendar_x.edit_idea_attr(
        road=work_road,
        required_base=weekdays_road,
        required_sufffact=thu_road,
    )
    calendar_x.get_idea_list()  # set tree metrics
    work_idea = calendar_x.get_idea_kid(road=work_road)
    assert work_idea._active_status == False

    # 5. idea(...,commute to work) with
    # 5.1. RequiredUnit: idea(base=...,work) has .suff_idea_active_status = True
    # 5.2. idea(...,work).active_status = False
    commute_text = "commute to work"
    commute_road = f"{root_desc()},{commute_text}"
    calendar_x.add_idea(idea_kid=IdeaKid(_desc=commute_text), walk=root_desc())
    calendar_x.edit_idea_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_idea_active_status=True,
    )
    commute_idea = calendar_x.get_idea_kid(road=commute_road)
    calendar_x.get_idea_list()
    assert commute_idea._active_status == False

    # AcptFact: base: (...,weekdays) pick: (...,weekdays,wednesday)
    calendar_x.set_acptfact(base=weekdays_road, pick=wed_road)
    calendar_x.set_calendar_metrics()

    assert work_idea._active_status == False
    assert commute_idea._active_status == False

    # WHEN
    print("before changing acptfact")
    calendar_x.set_acptfact(base=weekdays_road, pick=thu_road)
    print("after changing acptfact")
    calendar_x.get_idea_list()
    assert work_idea._active_status == True

    # THEN
    assert commute_idea._active_status == True


def test_calendar_set_calendar_metrics_InitimemberSetsRationalAttrToFalse():
    # GIVEN
    calendar_x = example_calendars_get_calendar_with_4_levels()
    assert calendar_x._rational == False
    # calendar_x.set_calendar_metrics()
    calendar_x._rational = True
    assert calendar_x._rational

    # WHEN
    # hack calendar to set _max_tree_traverse = 1 (not allowed, should always be 2 or more)
    calendar_x._max_tree_traverse = 1
    calendar_x.set_calendar_metrics()

    # THEN
    assert not calendar_x._rational


def test_calendar_tree_traverses_StopWhenNoChangeInStatusIsDetected():
    # GIVEN
    calendar_x = example_calendars_get_calendar_with_4_levels()
    assert calendar_x._max_tree_traverse != 2

    # WHEN
    calendar_x.set_calendar_metrics()
    # for idea_key in calendar_x._idea_dict.keys():
    #     print(f"{idea_key=}")

    # THEN
    assert calendar_x._tree_traverse_count == 2


def test_calendar_tree_traverse_count_CorrectlyCountsTreeTraversesForIrrationalCalendars():
    # GIVEN irrational calendar
    calendar_x = example_calendars_get_calendar_irrational_example()
    calendar_x.set_calendar_metrics()
    assert calendar_x._tree_traverse_count == 3

    # WHEN
    calendar_x.set_max_tree_traverse(int_x=21)
    calendar_x.set_calendar_metrics()

    # THEN
    assert calendar_x._tree_traverse_count == 21
