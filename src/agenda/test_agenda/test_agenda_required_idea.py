from pytest import raises as pytest_raises
from src.agenda.road import get_road
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_irrational_example as example_agendas_get_agenda_irrational_example,
)
from src.agenda.idea import ideacore_shop
from src.agenda.required_idea import (
    sufffactunit_shop,
    requiredunit_shop,
    requiredheir_shop,
)
from src.agenda.x_func import from_list_get_active_status


def test_agenda_requiredunits_create():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)
    weekday_text = "weekdays"
    weekday_road = get_road(x_agenda._culture_qid, weekday_text)
    wed_text = "Wednesday"
    wed_road = get_road(weekday_road, wed_text)

    wed_sufffact = sufffactunit_shop(need=wed_road)
    work_wk_required = requiredunit_shop(
        weekday_road, {wed_sufffact.need: wed_sufffact}
    )
    print(f"{type(work_wk_required.base)=}")
    print(f"{work_wk_required.base=}")
    x_agenda.edit_idea_attr(road=work_road, required=work_wk_required)
    work_idea = x_agenda._idearoot._kids[work_text]
    assert work_idea._requiredunits != None
    print(work_idea._requiredunits)
    assert work_idea._requiredunits[weekday_road] != None
    assert work_idea._requiredunits[weekday_road] == work_wk_required


def test_agenda_set_requiredunits_status():
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)
    weekday_text = "weekdays"
    weekday_road = get_road(x_agenda._culture_qid, weekday_text)
    wed_text = "Wednesday"
    wed_road = get_road(weekday_road, wed_text)

    wed_sufffact = sufffactunit_shop(need=wed_road)
    work_wk_required = requiredunit_shop(
        base=weekday_road, sufffacts={wed_sufffact.need: wed_sufffact}
    )
    print(f"{type(work_wk_required.base)=}")
    print(f"{work_wk_required.base=}")
    x_agenda.edit_idea_attr(road=work_road, required=work_wk_required)
    work_idea = x_agenda._idearoot._kids[work_text]
    assert work_idea._requiredunits != None
    print(work_idea._requiredunits)
    assert work_idea._requiredunits[weekday_road] != None
    assert work_idea._requiredunits[weekday_road] == work_wk_required


def test_intent_returned_WhenNoRequiredsExist():
    agenda_x = example_agendas_get_agenda_with_4_levels()
    agenda_x.set_agenda_metrics()
    work_text = "work"
    assert agenda_x._idearoot._kids[work_text]._task == True
    cat_text = "feed cat"
    assert agenda_x._idearoot._kids[cat_text]._task == True


def test_agenda_requiredheirs_AreCorrectlyInherited_v1():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)
    week_label = "weekdays"
    week_road = get_road(x_agenda._culture_qid, week_label)
    wed_text = "Wednesday"
    wed_road = get_road(week_road, wed_text)

    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffact._status = False
    wed_sufffact._task = False
    sufffacts = {wed_sufffact.need: wed_sufffact}
    work_wk_build_requiredunit = requiredunit_shop(base=week_road, sufffacts=sufffacts)
    work_wk_built_requiredheir = requiredheir_shop(
        base=week_road,
        sufffacts=sufffacts,
        _status=False,
        _curr_idea_active_status=True,
    )
    print(f"{work_wk_build_requiredunit.base=}")
    x_agenda.edit_idea_attr(road=work_road, required=work_wk_build_requiredunit)
    work_idea = x_agenda._idearoot._kids[work_text]
    assert work_idea._requiredunits != None
    # print(work_idea._requiredunits)
    assert work_idea._requiredunits[week_road] != None
    assert work_idea._requiredunits[week_road] == work_wk_build_requiredunit
    try:
        work_idea._requiredheirs[week_road]
    except TypeError as e:
        assert str(e) == "'NoneType' object is not subscriptable"

    idea_list = x_agenda.get_idea_list()

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


def test_agenda_requiredheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # GIVEN
    a4_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = get_road(a4_agenda._culture_qid, work_text)
    week_text = "weekdays"
    week_road = get_road(a4_agenda._culture_qid, week_text)
    wed_text = "Wednesday"
    wed_road = get_road(week_road, wed_text)

    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffact._status = False
    wed_sufffact._task = False

    sufffacts_x = {wed_sufffact.need: wed_sufffact}
    work_wk_build_requiredunit = requiredunit_shop(
        base=week_road, sufffacts=sufffacts_x
    )
    work_wk_built_requiredheir = requiredheir_shop(
        base=week_road,
        sufffacts=sufffacts_x,
        _status=False,
        _curr_idea_active_status=True,
    )
    a4_agenda.edit_idea_attr(road=work_road, required=work_wk_build_requiredunit)

    # WHEN
    rla_text = "hp"
    rla_road = get_road(work_road, rla_text)
    a4_agenda.add_idea(idea_kid=ideacore_shop(_label=rla_text), pad=rla_road)
    cost_text = "cost_tracking"
    cost_road = get_road(rla_road, cost_text)
    a4_agenda.add_idea(idea_kid=ideacore_shop(_label=cost_text), pad=cost_road)
    a4_agenda.get_idea_list()

    # THEN
    work_idea = a4_agenda._idearoot._kids[work_text]
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


def test_agenda_requiredheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = get_road(a4_agenda._culture_qid, work_text)
    week_label = "weekdays"
    week_road = get_road(a4_agenda._culture_qid, week_label)
    wed_text = "Wednesday"
    wed_road = get_road(week_road, wed_text)

    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffact._status = False
    wed_sufffact._task = False
    sufffacts = {wed_sufffact.need: wed_sufffact}
    work_wk_build_requiredunit = requiredunit_shop(base=week_road, sufffacts=sufffacts)
    work_wk_built_requiredheir = requiredheir_shop(
        base=week_road,
        sufffacts=sufffacts,
        _status=False,
        _curr_idea_active_status=True,
    )
    a4_agenda.edit_idea_attr(road=work_road, required=work_wk_build_requiredunit)
    rla_text = "hp"
    rla_road = get_road(work_road, rla_text)
    a4_agenda.add_idea(idea_kid=ideacore_shop(_label=rla_text), pad=rla_road)
    cost_text = "cost_tracking"
    cost_road = get_road(rla_road, cost_text)
    a4_agenda.add_idea(idea_kid=ideacore_shop(_label=cost_text), pad=cost_road)

    work_idea = a4_agenda._idearoot._kids[work_text]
    rla_idea = work_idea._kids[rla_text]
    cost_idea = rla_idea._kids[cost_text]

    assert a4_agenda._idearoot._requiredheirs is None
    assert work_idea._requiredheirs is None
    assert rla_idea._requiredheirs is None
    assert cost_idea._requiredheirs is None

    # WHEN
    idea_list = a4_agenda.get_idea_list()

    # THEN
    assert a4_agenda._idearoot._requiredheirs == {}  # work_wk_built_requiredheir

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


def test_agenda_requiredunits_set_UnCoupledMethod():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)
    week_text = "weekdays"
    week_road = get_road(x_agenda._culture_qid, week_text)
    wed_text = "Wednesday"
    wed_road = get_road(week_road, wed_text)

    # WHEN
    x_agenda.edit_idea_attr(
        road=work_road, required_base=week_road, required_sufffact=wed_road
    )

    # THEN
    work_idea1 = x_agenda.get_idea_kid(road=work_road)
    assert work_idea1._requiredunits != None
    print(work_idea1._requiredunits)
    assert work_idea1._requiredunits[week_road] != None
    assert work_idea1._requiredunits[week_road].sufffacts[wed_road].open is None
    assert work_idea1._requiredunits[week_road].sufffacts[wed_road].nigh is None

    work_wk_required1 = requiredunit_shop(base=week_road, sufffacts=None)
    work_wk_required1.set_sufffact(sufffact=wed_road)
    print(f" {type(work_wk_required1.base)=}")
    print(f" {work_wk_required1.base=}")
    assert work_idea1._requiredunits[week_road] == work_wk_required1

    # GIVEN
    divisor_x = 34
    open_x = 12
    nigh_x = 12

    # WHEN
    x_agenda.edit_idea_attr(
        road=work_road,
        required_base=week_road,
        required_sufffact=wed_road,
        required_sufffact_divisor=divisor_x,
        required_sufffact_open=open_x,
        required_sufffact_nigh=nigh_x,
    )

    # THEN
    assert work_idea1._requiredunits[week_road].sufffacts[wed_road].open == 12
    assert work_idea1._requiredunits[week_road].sufffacts[wed_road].nigh == 12

    wed_sufffact2 = sufffactunit_shop(
        need=wed_road, divisor=divisor_x, open=open_x, nigh=nigh_x
    )
    work_wk_required2 = requiredunit_shop(
        base=week_road, sufffacts={wed_sufffact2.need: wed_sufffact2}
    )
    print(f"{type(work_wk_required2.base)=}")
    print(f"{work_wk_required2.base=}")
    assert work_idea1._requiredunits[week_road] == work_wk_required2

    # WHEN
    thu_text = "Thursday"
    thu_road = get_road(week_road, thu_text)
    x_agenda.edit_idea_attr(
        road=work_road,
        required_base=week_road,
        required_sufffact=thu_road,
        required_sufffact_divisor=divisor_x,
        required_sufffact_open=open_x,
        required_sufffact_nigh=nigh_x,
    )

    # THEN
    assert len(work_idea1._requiredunits[week_road].sufffacts) == 2


def test_agenda_requiredunits_set_sufffactIdeaWithDenomSetsSuffFactDivision():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)
    time_text = "time"
    time_road = get_road(x_agenda._culture_qid, time_text)
    week_text = "week"
    week_road = get_road(time_road, week_text)
    x_agenda.add_idea(
        idea_kid=ideacore_shop(_label=time_text, _begin=100, _close=2000),
        pad=x_agenda._culture_qid,
    )
    x_agenda.add_idea(idea_kid=ideacore_shop(_label=week_text, _denom=7), pad=time_road)

    # WHEN
    x_agenda.edit_idea_attr(
        road=work_road,
        required_base=time_road,
        required_sufffact=week_road,
        required_sufffact_open=2,
        required_sufffact_nigh=5,
        required_sufffact_divisor=None,
    )

    # THEN
    work_idea1 = x_agenda.get_idea_kid(road=work_road)
    assert work_idea1._requiredunits[time_road] != None
    assert work_idea1._requiredunits[time_road].sufffacts[week_road].divisor == 7
    assert work_idea1._requiredunits[time_road].sufffacts[week_road].open == 2
    assert work_idea1._requiredunits[time_road].sufffacts[week_road].nigh == 5


def test_agenda_requiredunits_set_sufffactIdeaWithBeginCloseSetsSuffFactOpenNigh():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work = "work"
    work_road = get_road(x_agenda._culture_qid, work)
    time = "time"
    time_road = get_road(x_agenda._culture_qid, time)
    rus_war = "rus_war"
    rus_war_road = get_road(time_road, rus_war)
    x_agenda.add_idea(
        idea_kid=ideacore_shop(_label=time, _begin=100, _close=2000),
        pad=x_agenda._culture_qid,
    )
    x_agenda.add_idea(
        idea_kid=ideacore_shop(_label=rus_war, _begin=22, _close=34), pad=time_road
    )

    # WHEN
    x_agenda.edit_idea_attr(
        road=work_road,
        required_base=time_road,
        required_sufffact=rus_war_road,
        required_sufffact_open=None,
        required_sufffact_nigh=None,
        required_sufffact_divisor=None,
    )

    # THEN
    work_idea1 = x_agenda.get_idea_kid(road=work_road)
    assert work_idea1._requiredunits[time_road] != None
    assert work_idea1._requiredunits[time_road].sufffacts[rus_war_road].divisor is None
    assert work_idea1._requiredunits[time_road].sufffacts[rus_war_road].open == 22
    assert work_idea1._requiredunits[time_road].sufffacts[rus_war_road].nigh == 34


def test_agenda_requiredunits_del_required_sufffact_UncoupledMethod1():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_road = get_road(x_agenda._culture_qid, "work")
    weekday_road = get_road(x_agenda._culture_qid, "weekdays")
    wed_road = get_road(weekday_road, "Wednesday")

    x_agenda.edit_idea_attr(
        road=work_road, required_base=weekday_road, required_sufffact=wed_road
    )
    thu_road = get_road(weekday_road, "Thursday")
    x_agenda.edit_idea_attr(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=thu_road,
    )
    work_idea1 = x_agenda.get_idea_kid(road=work_road)
    assert len(work_idea1._requiredunits[weekday_road].sufffacts) == 2

    # WHEN
    x_agenda.del_idea_required_sufffact(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=thu_road,
    )

    # THEN
    assert len(work_idea1._requiredunits[weekday_road].sufffacts) == 1

    # WHEN
    x_agenda.del_idea_required_sufffact(
        road=work_road,
        required_base=weekday_road,
        required_sufffact=wed_road,
    )

    # THEN
    with pytest_raises(KeyError) as excinfo:
        work_idea1._requiredunits[weekday_road]
    assert str(excinfo.value) == f"'{weekday_road}'"
    assert work_idea1._requiredunits == {}


def test_agenda_requiredunits_del_required_sufffact_UncoupledMethod2():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_road = get_road(x_agenda._culture_qid, "work")
    weekdays_road = get_road(x_agenda._culture_qid, "weekdays")
    work_idea1 = x_agenda.get_idea_kid(road=work_road)
    work_idea1.set_requiredunits_empty_if_null()
    assert len(work_idea1._requiredunits) == 0

    # WHEN
    with pytest_raises(Exception) as excinfo:
        work_idea1.del_requiredunit_base(weekdays_road)
    assert str(excinfo.value) == f"No RequiredUnit at '{weekdays_road}'"


def test_agenda_edit_idea_attr_agendaIsAbleToEdit_suff_idea_active_status_AnyIdeaIfInvaildThrowsError():
    # _suff_idea_active_status: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)

    commute_text = "commute to work"
    commute_road = get_road(x_agenda._culture_qid, commute_text)
    x_agenda.add_idea(
        idea_kid=ideacore_shop(_label=commute_text), pad=x_agenda._culture_qid
    )
    x_agenda.get_idea_list()  # set tree metrics
    commute_idea = x_agenda.get_idea_kid(road=commute_road)
    assert len(commute_idea._requiredunits) == 0

    # WHEN
    x_agenda.edit_idea_attr(
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
    x_agenda.edit_idea_attr(
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
    x_agenda.edit_idea_attr(
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


def test_agenda_requiredunits_IdeaUnitActiveStatusInfluencesRequiredUnitStatus():
    # GIVEN an Agenda with 5 ideas, 1 AcptFact:
    # 1. idea(...,weekdays) exists
    # 2. idea(...,weekdays,wednesday) exists
    # 3. idea(...,weekdays,thursday) exists
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = get_road(x_agenda._culture_qid, work_text)
    weekdays_text = "weekdays"
    weekdays_road = get_road(x_agenda._culture_qid, weekdays_text)
    wed_text = "Wednesday"
    wed_road = get_road(weekdays_road, wed_text)
    thu_text = "Thursday"
    thu_road = get_road(weekdays_road, thu_text)

    # 4. idea(...,work) with
    # 4.1 RequiredUnit: base=weekdays_road, need=thu_road
    # 4.2 .active_status = False
    x_agenda.edit_idea_attr(
        road=work_road,
        required_base=weekdays_road,
        required_sufffact=thu_road,
    )
    x_agenda.get_idea_list()  # set tree metrics
    work_idea = x_agenda.get_idea_kid(road=work_road)
    assert work_idea._active_status == False

    # 5. idea(...,commute to work) with
    # 5.1. RequiredUnit: idea(base=...,work) has .suff_idea_active_status = True
    # 5.2. idea(...,work).active_status = False
    commute_text = "commute to work"
    commute_road = get_road(x_agenda._culture_qid, commute_text)
    x_agenda.add_idea(
        idea_kid=ideacore_shop(_label=commute_text), pad=x_agenda._culture_qid
    )
    x_agenda.edit_idea_attr(
        road=commute_road,
        required_base=work_road,
        required_suff_idea_active_status=True,
    )
    commute_idea = x_agenda.get_idea_kid(road=commute_road)
    x_agenda.get_idea_list()
    assert commute_idea._active_status == False

    # AcptFact: base: (...,weekdays) pick: (...,weekdays,wednesday)
    x_agenda.set_acptfact(base=weekdays_road, pick=wed_road)
    x_agenda.set_agenda_metrics()

    assert work_idea._active_status == False
    assert commute_idea._active_status == False

    # WHEN
    print("before changing acptfact")
    x_agenda.set_acptfact(base=weekdays_road, pick=thu_road)
    print("after changing acptfact")
    x_agenda.get_idea_list()
    assert work_idea._active_status == True

    # THEN
    assert commute_idea._active_status == True


def test_agenda_set_agenda_metrics_InitipartySetsRationalAttrToFalse():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    assert x_agenda._rational == False
    # x_agenda.set_agenda_metrics()
    x_agenda._rational = True
    assert x_agenda._rational

    # WHEN
    # hack agenda to set _max_tree_traverse = 1 (not allowed, should always be 2 or more)
    x_agenda._max_tree_traverse = 1
    x_agenda.set_agenda_metrics()

    # THEN
    assert not x_agenda._rational


def test_agenda_tree_traverses_StopWhenNoChangeInStatusIsDetected():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    assert x_agenda._max_tree_traverse != 2

    # WHEN
    x_agenda.set_agenda_metrics()
    # for idea_key in x_agenda._idea_dict.keys():
    #     print(f"{idea_key=}")

    # THEN
    assert x_agenda._tree_traverse_count == 2


def test_agenda_tree_traverse_count_CorrectlyCountsTreeTraversesForIrrationalAgendas():
    # GIVEN irrational agenda
    x_agenda = example_agendas_get_agenda_irrational_example()
    x_agenda.set_agenda_metrics()
    assert x_agenda._tree_traverse_count == 3

    # WHEN
    x_agenda.set_max_tree_traverse(int_x=21)
    x_agenda.set_agenda_metrics()

    # THEN
    assert x_agenda._tree_traverse_count == 21
