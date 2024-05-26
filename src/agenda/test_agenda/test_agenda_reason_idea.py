from pytest import raises as pytest_raises
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_irrational_example as example_agendas_get_agenda_irrational_example,
    from_list_get_active,
)
from src.agenda.idea import ideaunit_shop
from src.agenda.reason_idea import (
    premiseunit_shop,
    reasonunit_shop,
    reasonheir_shop,
)
from src.agenda.agenda import agendaunit_shop


def test_AgendaUnit_ReasonUnits_create():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    weekday_text = "weekdays"
    weekday_road = x_agenda.make_l1_road(weekday_text)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(weekday_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    casa_wk_reason = reasonunit_shop(weekday_road, {wed_premise.need: wed_premise})
    print(f"{type(casa_wk_reason.base)=}")
    print(f"{casa_wk_reason.base=}")

    # WHEN
    x_agenda.edit_idea_attr(road=casa_road, reason=casa_wk_reason)

    # THEN
    casa_idea = x_agenda.get_idea_obj(casa_road)
    assert casa_idea._reasonunits != None
    print(casa_idea._reasonunits)
    assert casa_idea._reasonunits[weekday_road] != None
    assert casa_idea._reasonunits[weekday_road] == casa_wk_reason


def test_AgendaUnit_edit_idea_attr_reasonunit_CorrectlySets_delimiter():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_road = x_agenda.make_l1_road("casa")
    week_road = x_agenda.make_l1_road("weekdays")
    wed_road = x_agenda.make_road(week_road, "Wednesday")

    slash_text = "/"
    before_week_reason = reasonunit_shop(week_road, delimiter=slash_text)
    before_week_reason.set_premise(wed_road)
    assert before_week_reason.delimiter == slash_text

    # WHEN
    x_agenda.edit_idea_attr(road=casa_road, reason=before_week_reason)

    # THEN
    casa_idea = x_agenda.get_idea_obj(casa_road)
    week_reasonunit = casa_idea._reasonunits.get(week_road)
    assert week_reasonunit.delimiter != slash_text
    assert week_reasonunit.delimiter == x_agenda._road_delimiter


def test_AgendaUnit_edit_idea_attr_reason_base_CorrectlySets_delimiter():
    # GIVEN
    slash_text = "/"
    bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_text)
    casa_text = "casa"
    week_text = "week"
    wed_text = "Wednesday"
    casa_road = bob_agenda.make_l1_road(casa_text)
    week_road = bob_agenda.make_l1_road(week_text)
    wed_road = bob_agenda.make_road(week_road, wed_text)
    bob_agenda.add_l1_idea(ideaunit_shop(casa_text))
    bob_agenda.add_l1_idea(ideaunit_shop(week_text))
    bob_agenda.add_idea(ideaunit_shop(wed_text), week_road)
    print(f"{bob_agenda._idearoot._kids.keys()=}")
    wed_idea = bob_agenda.get_idea_obj(wed_road)
    assert wed_idea._road_delimiter == slash_text
    assert wed_idea._road_delimiter == bob_agenda._road_delimiter

    # WHEN
    bob_agenda.edit_idea_attr(
        road=casa_road, reason_base=week_road, reason_premise=wed_road
    )

    # THEN
    casa_idea = bob_agenda.get_idea_obj(casa_road)
    assert casa_idea._road_delimiter == slash_text
    week_reasonunit = casa_idea._reasonunits.get(week_road)
    assert week_reasonunit.delimiter != ","
    assert week_reasonunit.delimiter == bob_agenda._road_delimiter


def test_AgendaUnit_set_reasonunits_status():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    weekday_text = "weekdays"
    weekday_road = x_agenda.make_l1_road(weekday_text)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(weekday_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    casa_wk_reason = reasonunit_shop(
        base=weekday_road, premises={wed_premise.need: wed_premise}
    )
    print(f"{type(casa_wk_reason.base)=}")
    print(f"{casa_wk_reason.base=}")

    # WHEN
    x_agenda.edit_idea_attr(road=casa_road, reason=casa_wk_reason)

    # THEN
    casa_idea = x_agenda.get_idea_obj(casa_road)
    assert casa_idea._reasonunits != None
    print(casa_idea._reasonunits)
    assert casa_idea._reasonunits[weekday_road] != None
    assert casa_idea._reasonunits[weekday_road] == casa_wk_reason


def test_intent_returned_WhenNoReasonsExist():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN
    casa_road = x_agenda.make_l1_road("casa")
    assert x_agenda.get_idea_obj(casa_road)._task == True
    cat_road = x_agenda.make_l1_road("feed cat")
    assert x_agenda.get_idea_obj(cat_road)._task == True


def test_AgendaUnit_reasonheirs_AreCorrectlyInherited_v1():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    print(f"{x_agenda._real_id=}")
    print(f"{x_agenda._idearoot._label=}")
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    week_label = "weekdays"
    week_road = x_agenda.make_l1_road(week_label)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(week_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = False
    wed_premise._task = False
    premises = {wed_premise.need: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(week_road, premises=premises)
    casa_wk_built_reasonheir = reasonheir_shop(
        base=week_road,
        premises=premises,
        _status=False,
        _base_idea_active=True,
    )
    print(f"{casa_wk_build_reasonunit.base=}")
    x_agenda.edit_idea_attr(road=casa_road, reason=casa_wk_build_reasonunit)
    casa_idea = x_agenda.get_idea_obj(casa_road)
    assert casa_idea._reasonunits != {}
    # print(casa_idea._reasonunits)
    assert casa_idea._reasonunits[week_road] != None
    assert casa_idea._reasonunits[week_road] == casa_wk_build_reasonunit
    try:
        casa_idea._reasonheirs[week_road]
    except KeyError as e:
        assert str(e) == f"'{x_agenda._real_id},weekdays'"

    x_agenda.calc_agenda_metrics()
    # idea_dict = x_agenda.get_idea_dict()
    # from_list_get_active(road=casa_road, idea_dict=idea_dict)

    casa_wk_cal_reasonheir = casa_idea._reasonheirs[week_road]
    print(f"{len(casa_wk_cal_reasonheir.premises)=}")
    assert len(casa_wk_cal_reasonheir.premises) == 1
    premise_wed = casa_wk_cal_reasonheir.premises.get(wed_road)
    assert (
        premise_wed._task == casa_wk_built_reasonheir.premises[premise_wed.need]._task
    )
    assert premise_wed == casa_wk_built_reasonheir.premises[premise_wed.need]
    # for premise in casa_wk_cal_reasonheir.premises.values():
    #     # assert premise_task == casa_wk_built_reasonheir.premises[premise.need]._task
    #     assert (
    #         premise._task == casa_wk_built_reasonheir.premises[premise.need]._task
    #     )
    #     assert premise == casa_wk_built_reasonheir.premises[premise.need]
    assert casa_wk_cal_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert casa_wk_cal_reasonheir == casa_wk_built_reasonheir


def test_AgendaUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromRoot():
    # GIVEN
    a4_agenda = example_agendas_get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = a4_agenda.make_l1_road(casa_text)
    week_text = "weekdays"
    week_road = a4_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = a4_agenda.make_road(week_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = False
    wed_premise._task = False

    premises_x = {wed_premise.need: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(base=week_road, premises=premises_x)
    casa_wk_built_reasonheir = reasonheir_shop(
        base=week_road,
        premises=premises_x,
        _status=False,
        _base_idea_active=True,
    )
    a4_agenda.edit_idea_attr(road=casa_road, reason=casa_wk_build_reasonunit)

    # WHEN
    rla_text = "hp"
    rla_road = a4_agenda.make_road(casa_road, rla_text)
    a4_agenda.add_idea(ideaunit_shop(rla_text), parent_road=rla_road)
    cost_text = "cost_quantification"
    cost_road = a4_agenda.make_road(rla_road, cost_text)
    a4_agenda.add_idea(ideaunit_shop(cost_text), parent_road=cost_road)
    a4_agenda.calc_agenda_metrics()

    # THEN
    casa_idea = a4_agenda._idearoot._kids[casa_text]
    rla_idea = casa_idea._kids[rla_text]
    cost_idea = rla_idea._kids[cost_text]

    # 1
    casa_wk_calc_reasonheir = casa_idea._reasonheirs[week_road]
    assert casa_wk_calc_reasonheir == casa_wk_built_reasonheir

    # 2
    rla_week_reasonheir = rla_idea._reasonheirs[week_road]
    assert rla_week_reasonheir.base == casa_wk_built_reasonheir.base
    assert rla_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_week_reasonheir.suff_idea_active
        == casa_wk_built_reasonheir.suff_idea_active
    )
    assert rla_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert rla_week_reasonheir._base_idea_active
    assert rla_week_reasonheir._base_idea_active != casa_wk_built_reasonheir

    # 3
    cost_week_reasonheir = cost_idea._reasonheirs[week_road]
    assert cost_week_reasonheir.base == casa_wk_built_reasonheir.base
    assert cost_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_week_reasonheir.suff_idea_active
        == casa_wk_built_reasonheir.suff_idea_active
    )
    assert cost_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert cost_week_reasonheir._base_idea_active
    assert cost_week_reasonheir._base_idea_active != casa_wk_built_reasonheir


def test_AgendaUnit_reasonheirs_AreCorrectlyInheritedTo4LevelsFromLevel2():
    a4_agenda = example_agendas_get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = a4_agenda.make_l1_road(casa_text)
    week_label = "weekdays"
    week_road = a4_agenda.make_l1_road(week_label)
    wed_text = "Wednesday"
    wed_road = a4_agenda.make_road(week_road, wed_text)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = False
    wed_premise._task = False
    premises = {wed_premise.need: wed_premise}
    casa_wk_build_reasonunit = reasonunit_shop(week_road, premises=premises)
    casa_wk_built_reasonheir = reasonheir_shop(
        base=week_road,
        premises=premises,
        _status=False,
        _base_idea_active=True,
    )
    a4_agenda.edit_idea_attr(road=casa_road, reason=casa_wk_build_reasonunit)
    rla_text = "hp"
    rla_road = a4_agenda.make_road(casa_road, rla_text)
    a4_agenda.add_idea(ideaunit_shop(rla_text), parent_road=rla_road)
    cost_text = "cost_quantification"
    cost_road = a4_agenda.make_road(rla_road, cost_text)
    a4_agenda.add_idea(ideaunit_shop(cost_text), parent_road=cost_road)

    casa_idea = a4_agenda._idearoot.get_kid(casa_text)
    rla_idea = casa_idea.get_kid(rla_text)
    cost_idea = rla_idea.get_kid(cost_text)

    assert a4_agenda._idearoot._reasonheirs == {}
    assert casa_idea._reasonheirs == {}
    assert rla_idea._reasonheirs == {}
    assert cost_idea._reasonheirs == {}

    # WHEN
    a4_agenda.calc_agenda_metrics()

    # THEN
    assert a4_agenda._idearoot._reasonheirs == {}  # casa_wk_built_reasonheir

    # 1
    assert casa_idea._reasonheirs[week_road] == casa_wk_built_reasonheir

    # 2
    rla_week_reasonheir = rla_idea._reasonheirs[week_road]
    assert rla_week_reasonheir.base == casa_wk_built_reasonheir.base
    assert rla_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        rla_week_reasonheir.suff_idea_active
        == casa_wk_built_reasonheir.suff_idea_active
    )
    assert rla_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert rla_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert rla_week_reasonheir._base_idea_active
    assert rla_week_reasonheir._base_idea_active != casa_wk_built_reasonheir

    # 3
    cost_week_reasonheir = cost_idea._reasonheirs[week_road]
    assert cost_week_reasonheir.base == casa_wk_built_reasonheir.base
    assert cost_week_reasonheir.premises == casa_wk_built_reasonheir.premises
    assert (
        cost_week_reasonheir.suff_idea_active
        == casa_wk_built_reasonheir.suff_idea_active
    )
    assert cost_week_reasonheir._status == casa_wk_built_reasonheir._status
    assert cost_week_reasonheir._task == casa_wk_built_reasonheir._task
    assert cost_week_reasonheir._base_idea_active
    assert cost_week_reasonheir._base_idea_active != casa_wk_built_reasonheir


def test_AgendaUnit_ReasonUnits_set_UnCoupledMethod():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(week_road, wed_text)

    # WHEN
    x_agenda.edit_idea_attr(
        road=casa_road, reason_base=week_road, reason_premise=wed_road
    )

    # THEN
    casa_idea1 = x_agenda.get_idea_obj(casa_road)
    assert casa_idea1._reasonunits != None
    print(casa_idea1._reasonunits)
    assert casa_idea1._reasonunits[week_road] != None
    assert casa_idea1._reasonunits[week_road].premises[wed_road].open is None
    assert casa_idea1._reasonunits[week_road].premises[wed_road].nigh is None

    casa_wk_reason1 = reasonunit_shop(week_road)
    casa_wk_reason1.set_premise(premise=wed_road)
    print(f" {type(casa_wk_reason1.base)=}")
    print(f" {casa_wk_reason1.base=}")
    assert casa_idea1._reasonunits[week_road] == casa_wk_reason1

    # GIVEN
    divisor_x = 34
    open_x = 12
    nigh_x = 12

    # WHEN
    x_agenda.edit_idea_attr(
        road=casa_road,
        reason_base=week_road,
        reason_premise=wed_road,
        reason_premise_divisor=divisor_x,
        reason_premise_open=open_x,
        reason_premise_nigh=nigh_x,
    )

    # THEN
    assert casa_idea1._reasonunits[week_road].premises[wed_road].open == 12
    assert casa_idea1._reasonunits[week_road].premises[wed_road].nigh == 12

    wed_premise2 = premiseunit_shop(
        need=wed_road, divisor=divisor_x, open=open_x, nigh=nigh_x
    )
    casa_wk_reason2 = reasonunit_shop(
        base=week_road, premises={wed_premise2.need: wed_premise2}
    )
    print(f"{type(casa_wk_reason2.base)=}")
    print(f"{casa_wk_reason2.base=}")
    assert casa_idea1._reasonunits[week_road] == casa_wk_reason2

    # WHEN
    thu_text = "Thursday"
    thu_road = x_agenda.make_road(week_road, thu_text)
    x_agenda.edit_idea_attr(
        road=casa_road,
        reason_base=week_road,
        reason_premise=thu_road,
        reason_premise_divisor=divisor_x,
        reason_premise_open=open_x,
        reason_premise_nigh=nigh_x,
    )

    # THEN
    assert len(casa_idea1._reasonunits[week_road].premises) == 2


def test_AgendaUnit_ReasonUnits_set_premiseIdeaWithDenomSetsPremiseDivision():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    time_text = "time"
    time_road = x_agenda.make_l1_road(time_text)
    week_text = "week"
    week_road = x_agenda.make_road(time_road, week_text)
    x_agenda.add_l1_idea(ideaunit_shop(time_text, _begin=100, _close=2000))
    x_agenda.add_idea(ideaunit_shop(week_text, _denom=7), parent_road=time_road)

    # WHEN
    x_agenda.edit_idea_attr(
        road=casa_road,
        reason_base=time_road,
        reason_premise=week_road,
        reason_premise_open=2,
        reason_premise_nigh=5,
        reason_premise_divisor=None,
    )

    # THEN
    casa_idea1 = x_agenda.get_idea_obj(casa_road)
    assert casa_idea1._reasonunits[time_road] != None
    assert casa_idea1._reasonunits[time_road].premises[week_road].divisor == 7
    assert casa_idea1._reasonunits[time_road].premises[week_road].open == 2
    assert casa_idea1._reasonunits[time_road].premises[week_road].nigh == 5


def test_AgendaUnit_ReasonUnits_set_premiseIdeaWithBeginCloseSetsPremiseOpenNigh():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa = "casa"
    casa_road = x_agenda.make_l1_road(casa)
    time = "time"
    time_road = x_agenda.make_l1_road(time)
    rus_war = "rus_war"
    rus_war_road = x_agenda.make_road(time_road, rus_war)
    x_agenda.add_idea(ideaunit_shop(time, _begin=100, _close=2000), x_agenda._real_id)
    x_agenda.add_idea(ideaunit_shop(rus_war, _begin=22, _close=34), time_road)

    # WHEN
    x_agenda.edit_idea_attr(
        road=casa_road,
        reason_base=time_road,
        reason_premise=rus_war_road,
        reason_premise_open=None,
        reason_premise_nigh=None,
        reason_premise_divisor=None,
    )

    # THEN
    casa_idea1 = x_agenda.get_idea_obj(casa_road)
    assert casa_idea1._reasonunits[time_road] != None
    assert casa_idea1._reasonunits[time_road].premises[rus_war_road].divisor is None
    assert casa_idea1._reasonunits[time_road].premises[rus_war_road].open == 22
    assert casa_idea1._reasonunits[time_road].premises[rus_war_road].nigh == 34


def test_AgendaUnit_ReasonUnits_edit_idea_attr_CorrectlyDeletes_ReasonUnits_And_PremiseUnits():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_road = x_agenda.make_l1_road("casa")
    weekday_road = x_agenda.make_l1_road("weekdays")
    wed_road = x_agenda.make_road(weekday_road, "Wednesday")

    x_agenda.edit_idea_attr(
        road=casa_road, reason_base=weekday_road, reason_premise=wed_road
    )
    thu_road = x_agenda.make_road(weekday_road, "Thursday")
    x_agenda.edit_idea_attr(
        road=casa_road,
        reason_base=weekday_road,
        reason_premise=thu_road,
    )
    casa_idea1 = x_agenda.get_idea_obj(casa_road)
    assert len(casa_idea1._reasonunits[weekday_road].premises) == 2

    # WHEN
    x_agenda.edit_idea_attr(
        road=casa_road,
        reason_del_premise_base=weekday_road,
        reason_del_premise_need=thu_road,
    )

    # THEN
    assert len(casa_idea1._reasonunits[weekday_road].premises) == 1

    # WHEN
    x_agenda.edit_idea_attr(
        road=casa_road,
        reason_del_premise_base=weekday_road,
        reason_del_premise_need=wed_road,
    )

    # THEN
    with pytest_raises(KeyError) as excinfo:
        casa_idea1._reasonunits[weekday_road]
    assert str(excinfo.value) == f"'{weekday_road}'"
    assert casa_idea1._reasonunits == {}


def test_AgendaUnit_ReasonUnits_del_reason_premise_UncoupledMethod2():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_road = x_agenda.make_l1_road("casa")
    weekdays_road = x_agenda.make_l1_road("weekdays")
    casa_idea1 = x_agenda.get_idea_obj(casa_road)
    assert len(casa_idea1._reasonunits) == 0

    # WHEN
    with pytest_raises(Exception) as excinfo:
        casa_idea1.del_reasonunit_base(weekdays_road)
    assert str(excinfo.value) == f"No ReasonUnit at '{weekdays_road}'"


def test_AgendaUnit_edit_idea_attr_agendaIsAbleToEdit_suff_idea_active_AnyIdeaIfInvaildThrowsError():
    # _suff_idea_active: str = None
    # must be 1 of 3: bool: True, bool: False, str="Set to Ignore"
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)

    commute_text = "commute to casa"
    commute_road = x_agenda.make_l1_road(commute_text)
    x_agenda.add_idea(ideaunit_shop(commute_text), x_agenda._real_id)
    x_agenda.calc_agenda_metrics()  # set tree metrics
    commute_idea = x_agenda.get_idea_obj(commute_road)
    assert len(commute_idea._reasonunits) == 0

    # WHEN
    x_agenda.edit_idea_attr(
        road=commute_road,
        reason_base=casa_road,
        reason_suff_idea_active=True,
    )

    # THEN
    assert len(commute_idea._reasonunits) == 1
    reasonunit_casa = commute_idea._reasonunits.get(casa_road)
    assert reasonunit_casa.base == casa_road
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.suff_idea_active == True

    # WHEN
    x_agenda.edit_idea_attr(
        road=commute_road,
        reason_base=casa_road,
        reason_suff_idea_active=False,
    )

    # THEN
    assert len(commute_idea._reasonunits) == 1
    reasonunit_casa = commute_idea._reasonunits.get(casa_road)
    assert reasonunit_casa.base == casa_road
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.suff_idea_active == False

    # WHEN
    x_agenda.edit_idea_attr(
        road=commute_road,
        reason_base=casa_road,
        reason_suff_idea_active="Set to Ignore",
    )

    # THEN
    assert len(commute_idea._reasonunits) == 1
    reasonunit_casa = commute_idea._reasonunits.get(casa_road)
    assert reasonunit_casa.base == casa_road
    assert len(reasonunit_casa.premises) == 0
    assert reasonunit_casa.suff_idea_active is None


def test_AgendaUnit_ReasonUnits_IdeaUnit_active_InfluencesReasonUnitStatus():
    # GIVEN an Agenda with 5 ideas, 1 Belief:
    # 1. idea(...,weekdays) exists
    # 2. idea(...,weekdays,wednesday) exists
    # 3. idea(...,weekdays,thursday) exists
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    weekdays_text = "weekdays"
    weekdays_road = x_agenda.make_l1_road(weekdays_text)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(weekdays_road, wed_text)
    thu_text = "Thursday"
    thu_road = x_agenda.make_road(weekdays_road, thu_text)

    # 4. idea(...,casa) with
    # 4.1 ReasonUnit: base=weekdays_road, need=thu_road
    # 4.2 .active = False
    x_agenda.edit_idea_attr(
        road=casa_road,
        reason_base=weekdays_road,
        reason_premise=thu_road,
    )
    x_agenda.calc_agenda_metrics()  # set tree metrics
    casa_idea = x_agenda.get_idea_obj(casa_road)
    assert casa_idea._active == False

    # 5. idea(...,commute to casa) with
    # 5.1. ReasonUnit: idea(base=...,casa) has .suff_idea_active = True
    # 5.2. idea(...,casa).active = False
    commute_text = "commute to casa"
    commute_road = x_agenda.make_l1_road(commute_text)
    x_agenda.add_idea(ideaunit_shop(commute_text), x_agenda._real_id)
    x_agenda.edit_idea_attr(
        road=commute_road,
        reason_base=casa_road,
        reason_suff_idea_active=True,
    )
    commute_idea = x_agenda.get_idea_obj(commute_road)
    x_agenda.calc_agenda_metrics()
    assert commute_idea._active == False

    # Belief: base: (...,weekdays) pick: (...,weekdays,wednesday)
    x_agenda.set_belief(base=weekdays_road, pick=wed_road)
    x_agenda.calc_agenda_metrics()

    assert casa_idea._active == False
    assert commute_idea._active == False

    # WHEN
    print("before changing belief")
    x_agenda.set_belief(base=weekdays_road, pick=thu_road)
    print("after changing belief")
    x_agenda.calc_agenda_metrics()
    assert casa_idea._active == True

    # THEN
    assert commute_idea._active == True


def test_AgendaUnit_calc_agenda_metrics_SetsRationalAttrToFalseWhen_max_tree_traverse_Is1():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    assert x_agenda._rational == False
    # x_agenda.calc_agenda_metrics()
    x_agenda._rational = True
    assert x_agenda._rational

    # WHEN
    # hack agenda to set _max_tree_traverse = 1 (not allowed, should be 2 or more)
    x_agenda._max_tree_traverse = 1
    x_agenda.calc_agenda_metrics()

    # THEN
    assert not x_agenda._rational


def test_AgendaUnit_tree_traverses_StopWhenNoChangeInStatusIsDetected():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    assert x_agenda._max_tree_traverse != 2

    # WHEN
    x_agenda.calc_agenda_metrics()
    # for idea_key in x_agenda._idea_dict.keys():
    #     print(f"{idea_key=}")

    # THEN
    assert x_agenda._tree_traverse_count == 2


def test_AgendaUnit_tree_traverse_count_CorrectlyCountsTreeTraversesForIrrationalAgendas():
    # GIVEN irrational agenda
    x_agenda = example_agendas_get_agenda_irrational_example()
    x_agenda.calc_agenda_metrics()
    assert x_agenda._tree_traverse_count == 3

    # WHEN
    x_agenda.set_max_tree_traverse(int_x=21)
    x_agenda.calc_agenda_metrics()

    # THEN
    assert x_agenda._tree_traverse_count == 21
