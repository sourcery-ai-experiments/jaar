from pytest import raises as pytest_raises
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_irrational_example as example_agendas_get_agenda_irrational_example,
    from_list_get_active_status,
)
from src.agenda.idea import ideaunit_shop
from src.agenda.reason_idea import (
    premiseunit_shop,
    reasonunit_shop,
    reasonheir_shop,
)
from src.agenda.agenda import agendaunit_shop


def test_agenda_reasonunits_create():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    weekday_text = "weekdays"
    weekday_road = x_agenda.make_l1_road(weekday_text)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(weekday_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    work_wk_reason = reasonunit_shop(weekday_road, {wed_premise.need: wed_premise})
    print(f"{type(work_wk_reason.base)=}")
    print(f"{work_wk_reason.base=}")

    # WHEN
    x_agenda.edit_idea_attr(road=work_road, reason=work_wk_reason)

    # THEN
    work_idea = x_agenda.get_idea_obj(work_road)
    assert work_idea._reasonunits != None
    print(work_idea._reasonunits)
    assert work_idea._reasonunits[weekday_road] != None
    assert work_idea._reasonunits[weekday_road] == work_wk_reason


def test_agenda_edit_idea_attr_reasonunit_CorrectlySets_delimiter():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_road = x_agenda.make_l1_road("work")
    week_road = x_agenda.make_l1_road("weekdays")
    wed_road = x_agenda.make_road(week_road, "Wednesday")

    slash_text = "/"
    before_week_reason = reasonunit_shop(week_road, delimiter=slash_text)
    before_week_reason.set_premise(wed_road)
    assert before_week_reason.delimiter == slash_text

    # WHEN
    x_agenda.edit_idea_attr(road=work_road, reason=before_week_reason)

    # THEN
    work_idea = x_agenda.get_idea_obj(work_road)
    week_reasonunit = work_idea._reasonunits.get(week_road)
    assert week_reasonunit.delimiter != slash_text
    assert week_reasonunit.delimiter == x_agenda._road_delimiter


def test_agenda_edit_idea_attr_reason_base_CorrectlySets_delimiter():
    # GIVEN
    slash_text = "/"
    bob_agenda = agendaunit_shop("bob", _road_delimiter=slash_text)
    work_text = "work"
    week_text = "week"
    wed_text = "Wednesday"
    work_road = bob_agenda.make_road(bob_agenda._economy_id, work_text)
    week_road = bob_agenda.make_road(bob_agenda._economy_id, week_text)
    wed_road = bob_agenda.make_road(week_road, wed_text)
    bob_agenda.add_idea(ideaunit_shop(work_text), bob_agenda._economy_id)
    bob_agenda.add_idea(ideaunit_shop(week_text), bob_agenda._economy_id)
    bob_agenda.add_idea(ideaunit_shop(wed_text), week_road)
    print(f"{bob_agenda._idearoot._kids.keys()=}")
    wed_idea = bob_agenda.get_idea_obj(wed_road)
    assert wed_idea._road_delimiter == slash_text
    assert wed_idea._road_delimiter == bob_agenda._road_delimiter

    # WHEN
    bob_agenda.edit_idea_attr(
        road=work_road, reason_base=week_road, reason_premise=wed_road
    )

    # THEN
    work_idea = bob_agenda.get_idea_obj(work_road)
    assert work_idea._road_delimiter == slash_text
    week_reasonunit = work_idea._reasonunits.get(week_road)
    assert week_reasonunit.delimiter != ","
    assert week_reasonunit.delimiter == bob_agenda._road_delimiter


def test_agenda_set_reasonunits_status():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    weekday_text = "weekdays"
    weekday_road = x_agenda.make_l1_road(weekday_text)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(weekday_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    work_wk_reason = reasonunit_shop(
        base=weekday_road, premises={wed_premise.need: wed_premise}
    )
    print(f"{type(work_wk_reason.base)=}")
    print(f"{work_wk_reason.base=}")

    # WHEN
    x_agenda.edit_idea_attr(road=work_road, reason=work_wk_reason)

    # THEN
    work_idea = x_agenda.get_idea_obj(work_road)
    assert work_idea._reasonunits != None
    print(work_idea._reasonunits)
    assert work_idea._reasonunits[weekday_road] != None
    assert work_idea._reasonunits[weekday_road] == work_wk_reason


def test_intent_returned_WhenNoReasonsExist():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    work_road = x_agenda.make_l1_road("work")
    assert x_agenda.get_idea_obj(work_road)._task == True
    cat_road = x_agenda.make_l1_road("feed cat")
    assert x_agenda.get_idea_obj(cat_road)._task == True


def test_agenda_reasonheirs_AreCorrectlyInherited_v1():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    print(f"{x_agenda._economy_id=}")
    print(f"{x_agenda._idearoot._label=}")
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    week_label = "weekdays"
    week_road = x_agenda.make_l1_road(week_label)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(week_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = False
    wed_premise._task = False
    premises = {wed_premise.need: wed_premise}
    work_wk_build_reasonunit = reasonunit_shop(week_road, premises=premises)
    work_wk_built_reasonheir = reasonheir_shop(
        base=week_road,
        premises=premises,
        _status=False,
        _curr_idea_active_status=True,
    )
    print(f"{work_wk_build_reasonunit.base=}")
    x_agenda.edit_idea_attr(road=work_road, reason=work_wk_build_reasonunit)
    work_idea = x_agenda.get_idea_obj(work_road)
    assert work_idea._reasonunits != {}
    # print(work_idea._reasonunits)
    assert work_idea._reasonunits[week_road] != None
    assert work_idea._reasonunits[week_road] == work_wk_build_reasonunit
    try:
        work_idea._reasonheirs[week_road]
    except KeyError as e:
        assert str(e) == "'A,weekdays'"

    idea_list = x_agenda.get_idea_list()

    from_list_get_active_status(road=work_road, idea_list=idea_list)

    work_wk_cal_reasonheir = work_idea._reasonheirs[week_road]
    print(f"{len(work_wk_cal_reasonheir.premises)=}")
    assert len(work_wk_cal_reasonheir.premises) == 1
    premise_wed = work_wk_cal_reasonheir.premises.get(wed_road)
    assert (
        premise_wed._task == work_wk_built_reasonheir.premises[premise_wed.need]._task
    )
    assert premise_wed == work_wk_built_reasonheir.premises[premise_wed.need]
    # for premise in work_wk_cal_reasonheir.premises.values():
    #     # assert premise_task == work_wk_built_reasonheir.premises[premise.need]._task
    #     assert (
    #         premise._task == work_wk_built_reasonheir.premises[premise.need]._task
    #     )
    #     assert premise == work_wk_built_reasonheir.premises[premise.need]
    assert work_wk_cal_reasonheir.premises == work_wk_built_reasonheir.premises
    assert work_wk_cal_reasonheir == work_wk_built_reasonheir


def test_agenda_reasonheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # GIVEN
    a4_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = a4_agenda.make_road(a4_agenda._economy_id, work_text)
    week_text = "weekdays"
    week_road = a4_agenda.make_road(a4_agenda._economy_id, week_text)
    wed_text = "Wednesday"
    wed_road = a4_agenda.make_road(week_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = False
    wed_premise._task = False

    premises_x = {wed_premise.need: wed_premise}
    work_wk_build_reasonunit = reasonunit_shop(base=week_road, premises=premises_x)
    work_wk_built_reasonheir = reasonheir_shop(
        base=week_road,
        premises=premises_x,
        _status=False,
        _curr_idea_active_status=True,
    )
    a4_agenda.edit_idea_attr(road=work_road, reason=work_wk_build_reasonunit)

    # WHEN
    rla_text = "hp"
    rla_road = a4_agenda.make_road(work_road, rla_text)
    a4_agenda.add_idea(ideaunit_shop(rla_text), parent_road=rla_road)
    cost_text = "cost_tracking"
    cost_road = a4_agenda.make_road(rla_road, cost_text)
    a4_agenda.add_idea(ideaunit_shop(cost_text), parent_road=cost_road)
    a4_agenda.get_idea_list()

    # THEN
    work_idea = a4_agenda._idearoot._kids[work_text]
    rla_idea = work_idea._kids[rla_text]
    cost_idea = rla_idea._kids[cost_text]

    # 1
    work_wk_calc_reasonheir = work_idea._reasonheirs[week_road]
    assert work_wk_calc_reasonheir == work_wk_built_reasonheir

    # 2
    rla_week_reasonheir = rla_idea._reasonheirs[week_road]
    assert rla_week_reasonheir.base == work_wk_built_reasonheir.base
    assert rla_week_reasonheir.premises == work_wk_built_reasonheir.premises
    assert (
        rla_week_reasonheir.suff_idea_active_status
        == work_wk_built_reasonheir.suff_idea_active_status
    )
    assert rla_week_reasonheir._status == work_wk_built_reasonheir._status
    assert rla_week_reasonheir._task == work_wk_built_reasonheir._task
    assert rla_week_reasonheir._curr_idea_active_status
    assert rla_week_reasonheir._curr_idea_active_status != work_wk_built_reasonheir

    # 3
    cost_week_reasonheir = cost_idea._reasonheirs[week_road]
    assert cost_week_reasonheir.base == work_wk_built_reasonheir.base
    assert cost_week_reasonheir.premises == work_wk_built_reasonheir.premises
    assert (
        cost_week_reasonheir.suff_idea_active_status
        == work_wk_built_reasonheir.suff_idea_active_status
    )
    assert cost_week_reasonheir._status == work_wk_built_reasonheir._status
    assert cost_week_reasonheir._task == work_wk_built_reasonheir._task
    assert cost_week_reasonheir._curr_idea_active_status
    assert cost_week_reasonheir._curr_idea_active_status != work_wk_built_reasonheir


def test_agenda_reasonheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = a4_agenda.make_road(a4_agenda._economy_id, work_text)
    week_label = "weekdays"
    week_road = a4_agenda.make_road(a4_agenda._economy_id, week_label)
    wed_text = "Wednesday"
    wed_road = a4_agenda.make_road(week_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = False
    wed_premise._task = False
    premises = {wed_premise.need: wed_premise}
    work_wk_build_reasonunit = reasonunit_shop(week_road, premises=premises)
    work_wk_built_reasonheir = reasonheir_shop(
        base=week_road,
        premises=premises,
        _status=False,
        _curr_idea_active_status=True,
    )
    a4_agenda.edit_idea_attr(road=work_road, reason=work_wk_build_reasonunit)
    rla_text = "hp"
    rla_road = a4_agenda.make_road(work_road, rla_text)
    a4_agenda.add_idea(ideaunit_shop(rla_text), parent_road=rla_road)
    cost_text = "cost_tracking"
    cost_road = a4_agenda.make_road(rla_road, cost_text)
    a4_agenda.add_idea(ideaunit_shop(cost_text), parent_road=cost_road)

    work_idea = a4_agenda._idearoot.get_kid(work_text)
    rla_idea = work_idea.get_kid(rla_text)
    cost_idea = rla_idea.get_kid(cost_text)

    assert a4_agenda._idearoot._reasonheirs == {}
    assert work_idea._reasonheirs == {}
    assert rla_idea._reasonheirs == {}
    assert cost_idea._reasonheirs == {}

    # WHEN
    idea_list = a4_agenda.get_idea_list()

    # THEN
    assert a4_agenda._idearoot._reasonheirs == {}  # work_wk_built_reasonheir

    # 1
    assert work_idea._reasonheirs[week_road] == work_wk_built_reasonheir

    # 2
    rla_week_reasonheir = rla_idea._reasonheirs[week_road]
    assert rla_week_reasonheir.base == work_wk_built_reasonheir.base
    assert rla_week_reasonheir.premises == work_wk_built_reasonheir.premises
    assert (
        rla_week_reasonheir.suff_idea_active_status
        == work_wk_built_reasonheir.suff_idea_active_status
    )
    assert rla_week_reasonheir._status == work_wk_built_reasonheir._status
    assert rla_week_reasonheir._task == work_wk_built_reasonheir._task
    assert rla_week_reasonheir._curr_idea_active_status
    assert rla_week_reasonheir._curr_idea_active_status != work_wk_built_reasonheir

    # 3
    cost_week_reasonheir = cost_idea._reasonheirs[week_road]
    assert cost_week_reasonheir.base == work_wk_built_reasonheir.base
    assert cost_week_reasonheir.premises == work_wk_built_reasonheir.premises
    assert (
        cost_week_reasonheir.suff_idea_active_status
        == work_wk_built_reasonheir.suff_idea_active_status
    )
    assert cost_week_reasonheir._status == work_wk_built_reasonheir._status
    assert cost_week_reasonheir._task == work_wk_built_reasonheir._task
    assert cost_week_reasonheir._curr_idea_active_status
    assert cost_week_reasonheir._curr_idea_active_status != work_wk_built_reasonheir


def test_agenda_reasonunits_set_UnCoupledMethod():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(week_road, wed_text)

    # WHEN
    x_agenda.edit_idea_attr(
        road=work_road, reason_base=week_road, reason_premise=wed_road
    )

    # THEN
    work_idea1 = x_agenda.get_idea_obj(work_road)
    assert work_idea1._reasonunits != None
    print(work_idea1._reasonunits)
    assert work_idea1._reasonunits[week_road] != None
    assert work_idea1._reasonunits[week_road].premises[wed_road].open is None
    assert work_idea1._reasonunits[week_road].premises[wed_road].nigh is None

    work_wk_reason1 = reasonunit_shop(week_road)
    work_wk_reason1.set_premise(premise=wed_road)
    print(f" {type(work_wk_reason1.base)=}")
    print(f" {work_wk_reason1.base=}")
    assert work_idea1._reasonunits[week_road] == work_wk_reason1

    # GIVEN
    divisor_x = 34
    open_x = 12
    nigh_x = 12

    # WHEN
    x_agenda.edit_idea_attr(
        road=work_road,
        reason_base=week_road,
        reason_premise=wed_road,
        reason_premise_divisor=divisor_x,
        reason_premise_open=open_x,
        reason_premise_nigh=nigh_x,
    )

    # THEN
    assert work_idea1._reasonunits[week_road].premises[wed_road].open == 12
    assert work_idea1._reasonunits[week_road].premises[wed_road].nigh == 12

    wed_premise2 = premiseunit_shop(
        need=wed_road, divisor=divisor_x, open=open_x, nigh=nigh_x
    )
    work_wk_reason2 = reasonunit_shop(
        base=week_road, premises={wed_premise2.need: wed_premise2}
    )
    print(f"{type(work_wk_reason2.base)=}")
    print(f"{work_wk_reason2.base=}")
    assert work_idea1._reasonunits[week_road] == work_wk_reason2

    # WHEN
    thu_text = "Thursday"
    thu_road = x_agenda.make_road(week_road, thu_text)
    x_agenda.edit_idea_attr(
        road=work_road,
        reason_base=week_road,
        reason_premise=thu_road,
        reason_premise_divisor=divisor_x,
        reason_premise_open=open_x,
        reason_premise_nigh=nigh_x,
    )

    # THEN
    assert len(work_idea1._reasonunits[week_road].premises) == 2


def test_agenda_reasonunits_set_premiseIdeaWithDenomSetsPremiseDivision():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    time_text = "time"
    time_road = x_agenda.make_l1_road(time_text)
    week_text = "week"
    week_road = x_agenda.make_road(time_road, week_text)
    x_agenda.add_idea(
        idea_kid=ideaunit_shop(time_text, _begin=100, _close=2000),
        parent_road=x_agenda._economy_id,
    )
    x_agenda.add_idea(ideaunit_shop(week_text, _denom=7), parent_road=time_road)

    # WHEN
    x_agenda.edit_idea_attr(
        road=work_road,
        reason_base=time_road,
        reason_premise=week_road,
        reason_premise_open=2,
        reason_premise_nigh=5,
        reason_premise_divisor=None,
    )

    # THEN
    work_idea1 = x_agenda.get_idea_obj(work_road)
    assert work_idea1._reasonunits[time_road] != None
    assert work_idea1._reasonunits[time_road].premises[week_road].divisor == 7
    assert work_idea1._reasonunits[time_road].premises[week_road].open == 2
    assert work_idea1._reasonunits[time_road].premises[week_road].nigh == 5


def test_agenda_reasonunits_set_premiseIdeaWithBeginCloseSetsPremiseOpenNigh():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work = "work"
    work_road = x_agenda.make_l1_road(work)
    time = "time"
    time_road = x_agenda.make_l1_road(time)
    rus_war = "rus_war"
    rus_war_road = x_agenda.make_road(time_road, rus_war)
    x_agenda.add_idea(
        idea_kid=ideaunit_shop(time, _begin=100, _close=2000),
        parent_road=x_agenda._economy_id,
    )
    x_agenda.add_idea(
        idea_kid=ideaunit_shop(rus_war, _begin=22, _close=34), parent_road=time_road
    )

    # WHEN
    x_agenda.edit_idea_attr(
        road=work_road,
        reason_base=time_road,
        reason_premise=rus_war_road,
        reason_premise_open=None,
        reason_premise_nigh=None,
        reason_premise_divisor=None,
    )

    # THEN
    work_idea1 = x_agenda.get_idea_obj(work_road)
    assert work_idea1._reasonunits[time_road] != None
    assert work_idea1._reasonunits[time_road].premises[rus_war_road].divisor is None
    assert work_idea1._reasonunits[time_road].premises[rus_war_road].open == 22
    assert work_idea1._reasonunits[time_road].premises[rus_war_road].nigh == 34


def test_agenda_reasonunits_del_reason_premise_UncoupledMethod1():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_road = x_agenda.make_l1_road("work")
    weekday_road = x_agenda.make_l1_road("weekdays")
    wed_road = x_agenda.make_road(weekday_road, "Wednesday")

    x_agenda.edit_idea_attr(
        road=work_road, reason_base=weekday_road, reason_premise=wed_road
    )
    thu_road = x_agenda.make_road(weekday_road, "Thursday")
    x_agenda.edit_idea_attr(
        road=work_road,
        reason_base=weekday_road,
        reason_premise=thu_road,
    )
    work_idea1 = x_agenda.get_idea_obj(work_road)
    assert len(work_idea1._reasonunits[weekday_road].premises) == 2

    # WHEN
    x_agenda.del_idea_reason_premise(
        road=work_road,
        reason_base=weekday_road,
        reason_premise=thu_road,
    )

    # THEN
    assert len(work_idea1._reasonunits[weekday_road].premises) == 1

    # WHEN
    x_agenda.del_idea_reason_premise(
        road=work_road,
        reason_base=weekday_road,
        reason_premise=wed_road,
    )

    # THEN
    with pytest_raises(KeyError) as excinfo:
        work_idea1._reasonunits[weekday_road]
    assert str(excinfo.value) == f"'{weekday_road}'"
    assert work_idea1._reasonunits == {}


def test_agenda_reasonunits_del_reason_premise_UncoupledMethod2():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_road = x_agenda.make_l1_road("work")
    weekdays_road = x_agenda.make_l1_road("weekdays")
    work_idea1 = x_agenda.get_idea_obj(work_road)
    assert len(work_idea1._reasonunits) == 0

    # WHEN
    with pytest_raises(Exception) as excinfo:
        work_idea1.del_reasonunit_base(weekdays_road)
    assert str(excinfo.value) == f"No ReasonUnit at '{weekdays_road}'"


def test_agenda_edit_idea_attr_agendaIsAbleToEdit_suff_idea_active_status_AnyIdeaIfInvaildThrowsError():
    # _suff_idea_active_status: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)

    commute_text = "commute to work"
    commute_road = x_agenda.make_l1_road(commute_text)
    x_agenda.add_idea(
        idea_kid=ideaunit_shop(commute_text), parent_road=x_agenda._economy_id
    )
    x_agenda.get_idea_list()  # set tree metrics
    commute_idea = x_agenda.get_idea_obj(commute_road)
    assert len(commute_idea._reasonunits) == 0

    # WHEN
    x_agenda.edit_idea_attr(
        road=commute_road,
        reason_base=work_road,
        reason_suff_idea_active_status=True,
    )

    # THEN
    assert len(commute_idea._reasonunits) == 1
    reasonunit_work = commute_idea._reasonunits.get(work_road)
    assert reasonunit_work.base == work_road
    assert len(reasonunit_work.premises) == 0
    assert reasonunit_work.suff_idea_active_status == True

    # WHEN
    x_agenda.edit_idea_attr(
        road=commute_road,
        reason_base=work_road,
        reason_suff_idea_active_status=False,
    )

    # THEN
    assert len(commute_idea._reasonunits) == 1
    reasonunit_work = commute_idea._reasonunits.get(work_road)
    assert reasonunit_work.base == work_road
    assert len(reasonunit_work.premises) == 0
    assert reasonunit_work.suff_idea_active_status == False

    # WHEN
    x_agenda.edit_idea_attr(
        road=commute_road,
        reason_base=work_road,
        reason_suff_idea_active_status="Set to Ignore",
    )

    # THEN
    assert len(commute_idea._reasonunits) == 1
    reasonunit_work = commute_idea._reasonunits.get(work_road)
    assert reasonunit_work.base == work_road
    assert len(reasonunit_work.premises) == 0
    assert reasonunit_work.suff_idea_active_status is None


def test_agenda_reasonunits_IdeaUnitActiveStatusInfluencesReasonUnitStatus():
    # GIVEN an Agenda with 5 ideas, 1 Belief:
    # 1. idea(...,weekdays) exists
    # 2. idea(...,weekdays,wednesday) exists
    # 3. idea(...,weekdays,thursday) exists
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    weekdays_text = "weekdays"
    weekdays_road = x_agenda.make_l1_road(weekdays_text)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(weekdays_road, wed_text)
    thu_text = "Thursday"
    thu_road = x_agenda.make_road(weekdays_road, thu_text)

    # 4. idea(...,work) with
    # 4.1 ReasonUnit: base=weekdays_road, need=thu_road
    # 4.2 .active_status = False
    x_agenda.edit_idea_attr(
        road=work_road,
        reason_base=weekdays_road,
        reason_premise=thu_road,
    )
    x_agenda.get_idea_list()  # set tree metrics
    work_idea = x_agenda.get_idea_obj(work_road)
    assert work_idea._active_status == False

    # 5. idea(...,commute to work) with
    # 5.1. ReasonUnit: idea(base=...,work) has .suff_idea_active_status = True
    # 5.2. idea(...,work).active_status = False
    commute_text = "commute to work"
    commute_road = x_agenda.make_l1_road(commute_text)
    x_agenda.add_idea(
        idea_kid=ideaunit_shop(commute_text), parent_road=x_agenda._economy_id
    )
    x_agenda.edit_idea_attr(
        road=commute_road,
        reason_base=work_road,
        reason_suff_idea_active_status=True,
    )
    commute_idea = x_agenda.get_idea_obj(commute_road)
    x_agenda.get_idea_list()
    assert commute_idea._active_status == False

    # Belief: base: (...,weekdays) pick: (...,weekdays,wednesday)
    x_agenda.set_belief(base=weekdays_road, pick=wed_road)
    x_agenda.set_agenda_metrics()

    assert work_idea._active_status == False
    assert commute_idea._active_status == False

    # WHEN
    print("before changing belief")
    x_agenda.set_belief(base=weekdays_road, pick=thu_road)
    print("after changing belief")
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
