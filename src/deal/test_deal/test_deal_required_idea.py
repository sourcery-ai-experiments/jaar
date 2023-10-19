from pytest import raises as pytest_raises
from src.deal.examples.example_deals import (
    get_deal_with_4_levels as example_deals_get_deal_with_4_levels,
    get_deal_irrational_example as example_deals_get_deal_irrational_example,
)
from src.deal.idea import IdeaKid
from src.deal.required_idea import sufffactunit_shop, RequiredUnit, RequiredHeir
from src.deal.deal import dealunit_shop
from src.deal.x_func import from_list_get_active_status


def test_deal_requiredunits_create():
    x_deal = example_deals_get_deal_with_4_levels()
    work_text = "work"
    work_road = f"{x_deal._project_handle},{work_text}"
    weekday_text = "weekdays"
    weekday_road = f"{x_deal._project_handle},{weekday_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekday_road},{wed_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    work_wk_required = RequiredUnit(
        base=weekday_road, sufffacts={wed_sufffact.need: wed_sufffact}
    )
    print(f"{type(work_wk_required.base)=}")
    print(f"{work_wk_required.base=}")
    x_deal.edit_idea_attr(road=work_road, required=work_wk_required)
    work_idea = x_deal._idearoot._kids[work_text]
    assert work_idea._requiredunits != None
    print(work_idea._requiredunits)
    assert work_idea._requiredunits[weekday_road] != None
    assert work_idea._requiredunits[weekday_road] == work_wk_required


def test_deal_set_requiredunits_status():
    x_deal = example_deals_get_deal_with_4_levels()
    work_text = "work"
    work_road = f"{x_deal._project_handle},{work_text}"
    weekday_text = "weekdays"
    weekday_road = f"{x_deal._project_handle},{weekday_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekday_road},{wed_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    work_wk_required = RequiredUnit(
        base=weekday_road, sufffacts={wed_sufffact.need: wed_sufffact}
    )
    print(f"{type(work_wk_required.base)=}")
    print(f"{work_wk_required.base=}")
    x_deal.edit_idea_attr(road=work_road, required=work_wk_required)
    work_idea = x_deal._idearoot._kids[work_text]
    assert work_idea._requiredunits != None
    print(work_idea._requiredunits)
    assert work_idea._requiredunits[weekday_road] != None
    assert work_idea._requiredunits[weekday_road] == work_wk_required


def test_agenda_returned_WhenNoRequiredsExist():
    lw_x = example_deals_get_deal_with_4_levels()
    lw_x.set_deal_metrics()
    work_text = "work"
    assert lw_x._idearoot._kids[work_text]._task == True
    cat_text = "feed cat"
    assert lw_x._idearoot._kids[cat_text]._task == True


def test_deal_requiredheirs_AreCorrectlyInherited_v1():
    # GIVEN
    x_deal = example_deals_get_deal_with_4_levels()
    work_text = "work"
    work_road = f"{x_deal._project_handle},{work_text}"
    week_label = "weekdays"
    week_road = f"{x_deal._project_handle},{week_label}"
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
    x_deal.edit_idea_attr(road=work_road, required=work_wk_build_requiredunit)
    work_idea = x_deal._idearoot._kids[work_text]
    assert work_idea._requiredunits != None
    # print(work_idea._requiredunits)
    assert work_idea._requiredunits[week_road] != None
    assert work_idea._requiredunits[week_road] == work_wk_build_requiredunit
    try:
        work_idea._requiredheirs[week_road]
    except TypeError as e:
        assert str(e) == "'NoneType' object is not subscriptable"

    idea_list = x_deal.get_idea_list()

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


def test_deal_requiredheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # GIVEN
    a4_deal = example_deals_get_deal_with_4_levels()
    work_text = "work"
    work_road = f"{a4_deal._project_handle},{work_text}"
    week_text = "weekdays"
    week_road = f"{a4_deal._project_handle},{week_text}"
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
    a4_deal.edit_idea_attr(road=work_road, required=work_wk_build_requiredunit)

    # WHEN
    rla_text = "hp"
    rla_road = f"{work_road},{rla_text}"
    a4_deal.add_idea(idea_kid=IdeaKid(_label=rla_text), pad=rla_road)
    cost_text = "cost_tracking"
    cost_road = f"{rla_road},{cost_text}"
    a4_deal.add_idea(idea_kid=IdeaKid(_label=cost_text), pad=cost_road)
    a4_deal.get_idea_list()

    # THEN
    work_idea = a4_deal._idearoot._kids[work_text]
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


def test_deal_requiredheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4_deal = example_deals_get_deal_with_4_levels()
    work_text = "work"
    work_road = f"{a4_deal._project_handle},{work_text}"
    week_label = "weekdays"
    week_road = f"{a4_deal._project_handle},{week_label}"
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
    a4_deal.edit_idea_attr(road=work_road, required=work_wk_build_requiredunit)
    rla_text = "hp"
    rla_road = f"{work_road},{rla_text}"
    a4_deal.add_idea(idea_kid=IdeaKid(_label=rla_text), pad=rla_road)
    cost_text = "cost_tracking"
    cost_road = f"{rla_road},{cost_text}"
    a4_deal.add_idea(idea_kid=IdeaKid(_label=cost_text), pad=cost_road)

    work_idea = a4_deal._idearoot._kids[work_text]
    rla_idea = work_idea._kids[rla_text]
    cost_idea = rla_idea._kids[cost_text]

    assert a4_deal._idearoot._requiredheirs is None
    assert work_idea._requiredheirs is None
    assert rla_idea._requiredheirs is None
    assert cost_idea._requiredheirs is None

    # WHEN
    idea_list = a4_deal.get_idea_list()

    # THEN
    assert a4_deal._idearoot._requiredheirs == {}  # work_wk_built_requiredheir

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


def test_deal_requiredunits_set_UnCoupledMethod():
    # Given
    x_deal = example_deals_get_deal_with_4_levels()
    work_text = "work"
    work_road = f"{x_deal._project_handle},{work_text}"
    week_text = "weekdays"
    week_road = f"{x_deal._project_handle},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"

    # When
    x_deal.edit_idea_attr(
        road=work_road, required_base=week_road, required_sufffact=wed_road
    )

    # Then
    work_idea1 = x_deal.get_idea_kid(road=work_road)
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
    x_deal.edit_idea_attr(
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
    x_deal.edit_idea_attr(
        road=work_road,
        required_base=week_road,
        required_sufffact=thu_road,
        required_sufffact_divisor=divisor_x,
        required_sufffact_open=open_x,
        required_sufffact_nigh=nigh_x,
    )

    # Then
    assert len(work_idea1._requiredunits[week_road].sufffacts) == 2


def test_deal_requiredunits_set_sufffactIdeaWithDenomSetsSuffFactDivision():
    # Given
    x_deal = example_deals_get_deal_with_4_levels()
    work_text = "work"
    work_road = f"{x_deal._project_handle},{work_text}"
    time_text = "time"
    time_road = f"{x_deal._project_handle},{time_text}"
    week_text = "week"
    week_road = f"{x_deal._project_handle},{time_text},{week_text}"
    x_deal.add_idea(
        idea_kid=IdeaKid(_label=time_text, _begin=100, _close=2000),
        pad=x_deal._project_handle,
    )
    x_deal.add_idea(idea_kid=IdeaKid(_label=week_text, _denom=7), pad=time_road)

    # When
    x_deal.edit_idea_attr(
        road=work_road,
        required_base=time_road,
        required_sufffact=week_road,
        required_sufffact_open=2,
        required_sufffact_nigh=5,
        required_sufffact_divisor=None,
    )

    # Then
    work_idea1 = x_deal.get_idea_kid(road=work_road)
    assert work_idea1._requiredunits[time_road] != None
    assert work_idea1._requiredunits[time_road].sufffacts[week_road].divisor == 7
    assert work_idea1._requiredunits[time_road].sufffacts[week_road].open == 2
    assert work_idea1._requiredunits[time_road].sufffacts[week_road].nigh == 5


def test_deal_requiredunits_set_sufffactIdeaWithBeginCloseSetsSuffFactOpenNigh():
    # Given
    x_deal = example_deals_get_deal_with_4_levels()
    work = "work"
    work_road = f"{x_deal._project_handle},{work}"
    time = "time"
    time_road = f"{x_deal._project_handle},{time}"
    rus_war = "rus_war"
    rus_war_road = f"{x_deal._project_handle},{time},{rus_war}"
    x_deal.add_idea(
        idea_kid=IdeaKid(_label=time, _begin=100, _close=2000),
        pad=x_deal._project_handle,
    )
    x_deal.add_idea(
        idea_kid=IdeaKid(_label=rus_war, _begin=22, _close=34), pad=time_road
    )

    # When
    x_deal.edit_idea_attr(
        road=work_road,
        required_base=time_road,
        required_sufffact=rus_war_road,
        required_sufffact_open=None,
        required_sufffact_nigh=None,
        required_sufffact_divisor=None,
    )

    # Then
    work_idea1 = x_deal.get_idea_kid(road=work_road)
    assert work_idea1._requiredunits[time_road] != None
    assert work_idea1._requiredunits[time_road].sufffacts[rus_war_road].divisor is None
    assert work_idea1._requiredunits[time_road].sufffacts[rus_war_road].open == 22
    assert work_idea1._requiredunits[time_road].sufffacts[rus_war_road].nigh == 34


def test_deal_requiredunits_del_required_sufffact_UncoupledMethod1():
    # Given
    x_deal = example_deals_get_deal_with_4_levels()
    work_road = f"{x_deal._project_handle},work"
    weekday_road = f"{x_deal._project_handle},weekdays"
    wed_road = f"{x_deal._project_handle},weekdays,Wednesday"

    x_deal.edit_idea_attr(
        road=work_road, required_base=weekday_road, required_sufffact=wed_road
    )
    thu_road = f"{x_deal._project_handle},weekdays,Thursday"
    x_deal.edit_idea_attr(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=thu_road,
    )
    work_idea1 = x_deal.get_idea_kid(road=work_road)
    assert len(work_idea1._requiredunits[weekday_road].sufffacts) == 2

    # When
    x_deal.del_idea_required_sufffact(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=thu_road,
    )

    # Then
    assert len(work_idea1._requiredunits[weekday_road].sufffacts) == 1

    # When
    x_deal.del_idea_required_sufffact(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=wed_road,
    )

    # Then
    with pytest_raises(KeyError) as excinfo:
        work_idea1._requiredunits[weekday_road]
    assert str(excinfo.value) == f"'{weekday_road}'"
    assert work_idea1._requiredunits == {}


def test_deal_requiredunits_del_required_sufffact_UncoupledMethod2():
    # Given
    x_deal = example_deals_get_deal_with_4_levels()
    work_road = f"{x_deal._project_handle},work"
    weekdays_road = f"{x_deal._project_handle},weekdays"
    work_idea1 = x_deal.get_idea_kid(road=work_road)
    work_idea1.set_requiredunits_empty_if_null()
    assert len(work_idea1._requiredunits) == 0

    # When
    with pytest_raises(Exception) as excinfo:
        work_idea1.del_requiredunit_base(weekdays_road)
    assert str(excinfo.value) == f"No RequiredUnit at '{weekdays_road}'"


def test_deal_edit_idea_attr_dealIsAbleToEdit_suff_idea_active_status_AnyIdeaIfInvaildThrowsError():
    # _suff_idea_active_status: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # GIVEN
    x_deal = example_deals_get_deal_with_4_levels()
    work_text = "work"
    work_road = f"{x_deal._project_handle},{work_text}"

    commute_text = "commute to work"
    commute_road = f"{x_deal._project_handle},{commute_text}"
    x_deal.add_idea(idea_kid=IdeaKid(_label=commute_text), pad=x_deal._project_handle)
    x_deal.get_idea_list()  # set tree metrics
    commute_idea = x_deal.get_idea_kid(road=commute_road)
    assert len(commute_idea._requiredunits) == 0

    # WHEN
    x_deal.edit_idea_attr(
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
    x_deal.edit_idea_attr(
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
    x_deal.edit_idea_attr(
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


def test_deal_requiredunits_IdeaUnitActiveStatusInfluencesRequiredUnitStatus():
    # GIVEN an Deal with 5 ideas, 1 AcptFact:
    # 1. idea(...,weekdays) exists
    # 2. idea(...,weekdays,wednesday) exists
    # 3. idea(...,weekdays,thursday) exists
    x_deal = example_deals_get_deal_with_4_levels()
    work_text = "work"
    work_road = f"{x_deal._project_handle},{work_text}"
    weekdays_text = "weekdays"
    weekdays_road = f"{x_deal._project_handle},{weekdays_text}"
    wed_text = "Wednesday"
    wed_road = f"{weekdays_road},{wed_text}"
    thu_text = "Thursday"
    thu_road = f"{weekdays_road},{thu_text}"

    # 4. idea(...,work) with
    # 4.1 RequiredUnit: base=weekdays_road, need=thu_road
    # 4.2 .active_status = False
    x_deal.edit_idea_attr(
        road=work_road,
        required_base=weekdays_road,
        required_sufffact=thu_road,
    )
    x_deal.get_idea_list()  # set tree metrics
    work_idea = x_deal.get_idea_kid(road=work_road)
    assert work_idea._active_status == False

    # 5. idea(...,commute to work) with
    # 5.1. RequiredUnit: idea(base=...,work) has .suff_idea_active_status = True
    # 5.2. idea(...,work).active_status = False
    commute_text = "commute to work"
    commute_road = f"{x_deal._project_handle},{commute_text}"
    x_deal.add_idea(idea_kid=IdeaKid(_label=commute_text), pad=x_deal._project_handle)
    x_deal.edit_idea_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_idea_active_status=True,
    )
    commute_idea = x_deal.get_idea_kid(road=commute_road)
    x_deal.get_idea_list()
    assert commute_idea._active_status == False

    # AcptFact: base: (...,weekdays) pick: (...,weekdays,wednesday)
    x_deal.set_acptfact(base=weekdays_road, pick=wed_road)
    x_deal.set_deal_metrics()

    assert work_idea._active_status == False
    assert commute_idea._active_status == False

    # WHEN
    print("before changing acptfact")
    x_deal.set_acptfact(base=weekdays_road, pick=thu_road)
    print("after changing acptfact")
    x_deal.get_idea_list()
    assert work_idea._active_status == True

    # THEN
    assert commute_idea._active_status == True


def test_deal_set_deal_metrics_InitipartySetsRationalAttrToFalse():
    # GIVEN
    x_deal = example_deals_get_deal_with_4_levels()
    assert x_deal._rational == False
    # x_deal.set_deal_metrics()
    x_deal._rational = True
    assert x_deal._rational

    # WHEN
    # hack deal to set _max_tree_traverse = 1 (not allowed, should always be 2 or more)
    x_deal._max_tree_traverse = 1
    x_deal.set_deal_metrics()

    # THEN
    assert not x_deal._rational


def test_deal_tree_traverses_StopWhenNoChangeInStatusIsDetected():
    # GIVEN
    x_deal = example_deals_get_deal_with_4_levels()
    assert x_deal._max_tree_traverse != 2

    # WHEN
    x_deal.set_deal_metrics()
    # for idea_key in x_deal._idea_dict.keys():
    #     print(f"{idea_key=}")

    # THEN
    assert x_deal._tree_traverse_count == 2


def test_deal_tree_traverse_count_CorrectlyCountsTreeTraversesForIrrationalDeals():
    # GIVEN irrational deal
    x_deal = example_deals_get_deal_irrational_example()
    x_deal.set_deal_metrics()
    assert x_deal._tree_traverse_count == 3

    # WHEN
    x_deal.set_max_tree_traverse(int_x=21)
    x_deal.set_deal_metrics()

    # THEN
    assert x_deal._tree_traverse_count == 21
