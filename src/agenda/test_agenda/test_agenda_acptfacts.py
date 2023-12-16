from src.agenda.required_idea import (
    acptfactunit_shop,
    acptfactunit_shop,
    acptfactheir_shop,
)
from src.agenda.idea import ideacore_shop, Road
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as examples_get_agenda_with_4_levels,
)
from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_agenda_acptfact_exists():
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    sunday_road = x_agenda.make_road(weekday_road, "Sunday")
    sunday_agenda_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_agenda_acptfact)
    x_agenda._idearoot._acptfactunits = {
        sunday_agenda_acptfact.base: sunday_agenda_acptfact
    }
    assert x_agenda._idearoot._acptfactunits != None
    x_agenda._idearoot._acptfactunits = None
    assert x_agenda._idearoot._acptfactunits is None
    x_agenda.set_acptfact(base=weekday_road, pick=sunday_road)
    assert x_agenda._idearoot._acptfactunits == {
        sunday_agenda_acptfact.base: sunday_agenda_acptfact
    }

    x_agenda._idearoot._acptfactunits = None
    assert x_agenda._idearoot._acptfactunits is None
    usa_week_road = x_agenda.make_l1_road("nation-state")
    usa_week_unit = acptfactunit_shop(
        base=usa_week_road, pick=usa_week_road, open=608, nigh=610
    )
    x_agenda._idearoot._acptfactunits = {usa_week_unit.base: usa_week_unit}

    x_agenda._idearoot._acptfactunits = None
    assert x_agenda._idearoot._acptfactunits is None
    x_agenda.set_acptfact(base=usa_week_road, pick=usa_week_road, open=608, nigh=610)
    assert x_agenda._idearoot._acptfactunits != None
    assert x_agenda._idearoot._acptfactunits == {usa_week_unit.base: usa_week_unit}


def test_agenda_acptfact_create():
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    sunday_road = x_agenda.make_road(weekday_road, "Sunday")
    x_agenda.set_acptfact(base=weekday_road, pick=sunday_road)
    sunday_agenda_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    assert x_agenda._idearoot._acptfactunits == {
        sunday_agenda_acptfact.base: sunday_agenda_acptfact
    }


def test_set_acptfact_FailsToCreateWhenBaseAndAcptFactAreDifferenctAndAcptFactIdeaIsNotRangeRoot():
    # GIVEN
    bob_text = "Bob"
    x_agenda = agendaunit_shop(bob_text)
    time_text = "time"
    x_agenda.add_idea(
        ideacore_shop(time_text, _begin=0, _close=140), x_agenda._culture_qid
    )
    time_road = x_agenda.make_l1_road(time_text)
    a1st = "age1st"
    x_agenda.add_idea(ideacore_shop(a1st, _begin=0, _close=20), pad=time_road)
    a1_road = x_agenda.make_road(time_road, a1st)
    a1e1st = "a1_era1st"
    x_agenda.add_idea(ideacore_shop(a1e1st, _begin=20, _close=30), pad=a1_road)
    a1e1_road = x_agenda.make_road(a1_road, a1e1st)
    assert x_agenda._idearoot._acptfactunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.set_acptfact(base=a1e1_road, pick=a1e1_road, open=20, nigh=23)
    assert (
        str(excinfo.value)
        == f"Non range-root acptfact:{a1e1_road} can only be set by range-root acptfact"
    )


def test_agenda_acptfact_create():
    # GIVEN
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    sunday_road = x_agenda.make_road(weekday_road, "Sunday")
    x_agenda.set_acptfact(base=weekday_road, pick=sunday_road)
    sunday_agenda_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    assert x_agenda._idearoot._acptfactunits == {
        sunday_agenda_acptfact.base: sunday_agenda_acptfact
    }

    # WHEN
    x_agenda.del_acptfact(base=weekday_road)

    # THEN
    assert x_agenda._idearoot._acptfactunits == {}


def test_agenda_get_idea_list_AcptFactHeirsCorrectlyInherited():
    # GIVEN
    bob_text = "Bob"
    x_agenda = agendaunit_shop(bob_text)
    swim_text = "swim"
    swim_road = x_agenda.make_l1_road(swim_text)
    x_agenda.add_idea(ideacore_shop(swim_text), pad=x_agenda._culture_qid)
    fast_text = "fast"
    slow_text = "slow"
    fast_road = x_agenda.make_road(swim_road, fast_text)
    slow_road = x_agenda.make_road(swim_road, slow_text)
    x_agenda.add_idea(ideacore_shop(fast_text), pad=swim_road)
    x_agenda.add_idea(ideacore_shop(slow_text), pad=swim_road)

    earth_text = "earth"
    earth_road = x_agenda.make_l1_road(earth_text)
    x_agenda.add_idea(ideacore_shop(earth_text), pad=x_agenda._culture_qid)

    swim_idea = x_agenda.get_idea_kid(swim_road)
    fast_idea = x_agenda.get_idea_kid(fast_road)
    slow_idea = x_agenda.get_idea_kid(slow_road)

    assert swim_idea._acptfactheirs is None
    assert fast_idea._acptfactheirs is None
    assert slow_idea._acptfactheirs is None

    # WHEN
    x_agenda.set_acptfact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)
    acptfactheir_set_range = acptfactheir_shop(earth_road, earth_road, 1.0, 5.0)
    acptfactheirs_set_range = {acptfactheir_set_range.base: acptfactheir_set_range}
    acptfact_none_range = acptfactheir_shop(earth_road, earth_road, None, None)
    acptfacts_none_range = {acptfact_none_range.base: acptfact_none_range}

    # THEN
    assert swim_idea._acptfactheirs != None
    assert fast_idea._acptfactheirs != None
    assert slow_idea._acptfactheirs != None
    assert swim_idea._acptfactheirs == acptfactheirs_set_range
    assert fast_idea._acptfactheirs == acptfactheirs_set_range
    assert slow_idea._acptfactheirs == acptfactheirs_set_range
    print(f"{swim_idea._acptfactheirs=}")
    assert len(swim_idea._acptfactheirs) == 1

    # WHEN
    swim_idea._acptfactheirs.get(earth_road).set_range_null()

    # THEN
    assert swim_idea._acptfactheirs == acptfacts_none_range
    assert fast_idea._acptfactheirs == acptfactheirs_set_range
    assert slow_idea._acptfactheirs == acptfactheirs_set_range

    acptfact_x1 = swim_idea._acptfactheirs.get(earth_road)
    acptfact_x1.set_range_null()
    print(type(acptfact_x1))
    assert str(type(acptfact_x1)).find(".required.AcptFactHeir'>")


def test_agenda_get_idea_list_AcptFactUnitCorrectlyTransformsacptfactheir_shop():
    # GIVEN
    bob_text = "Bob"
    x_agenda = agendaunit_shop(bob_text)
    swim_text = "swim"
    swim_road = x_agenda.make_l1_road(swim_text)
    x_agenda.add_idea(ideacore_shop(swim_text), pad=x_agenda._culture_qid)
    swim_idea = x_agenda.get_idea_kid(swim_road)

    fast_text = "fast"
    slow_text = "slow"
    x_agenda.add_idea(ideacore_shop(fast_text), pad=swim_road)
    x_agenda.add_idea(ideacore_shop(slow_text), pad=swim_road)

    earth_text = "earth"
    earth_road = x_agenda.make_l1_road(earth_text)
    x_agenda.add_idea(ideacore_shop(earth_text), pad=x_agenda._culture_qid)

    assert swim_idea._acptfactheirs is None

    # WHEN
    x_agenda.set_acptfact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)

    # THEN
    first_earthheir = acptfactheir_shop(
        base=earth_road, pick=earth_road, open=1.0, nigh=5.0
    )
    first_earthdict = {first_earthheir.base: first_earthheir}
    assert swim_idea._acptfactheirs == first_earthdict

    # WHEN
    # earth_curb = acptfactunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    # swim_y.set_acptfactunit(acptfactunit=earth_curb) Not sure what this is for. Testing how "set_acptfactunit" works?
    x_agenda.set_acptfact(base=earth_road, pick=earth_road, open=3.0, nigh=5.0)

    # THEN
    after_earthheir = acptfactheir_shop(
        base=earth_road, pick=earth_road, open=3.0, nigh=5.0
    )
    after_earthdict = {after_earthheir.base: after_earthheir}
    assert swim_idea._acptfactheirs == after_earthdict


def test_agenda_get_idea_list_AcptFactHeirCorrectlyDeletesAcptFactUnit():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    swim_text = "swim"
    swim_road = x_agenda.make_l1_road(swim_text)
    x_agenda.add_idea(ideacore_shop(swim_text), pad=x_agenda._culture_qid)
    fast_text = "fast"
    slow_text = "slow"
    x_agenda.add_idea(ideacore_shop(fast_text), pad=swim_road)
    x_agenda.add_idea(ideacore_shop(slow_text), pad=swim_road)
    earth_text = "earth"
    earth_road = x_agenda.make_l1_road(earth_text)
    x_agenda.add_idea(ideacore_shop(earth_text), pad=x_agenda._culture_qid)

    swim_idea = x_agenda.get_idea_kid(swim_road)

    first_earthheir = acptfactheir_shop(
        base=earth_road, pick=earth_road, open=200.0, nigh=500.0
    )
    first_earthdict = {first_earthheir.base: first_earthheir}

    assert swim_idea._acptfactheirs is None

    # WHEN
    x_agenda.set_acptfact(base=earth_road, pick=earth_road, open=200.0, nigh=500.0)

    # THEN
    assert swim_idea._acptfactheirs == first_earthdict

    earth_curb = acptfactunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    swim_idea.set_acptfactunit(acptfactunit=earth_curb)
    x_agenda.set_agenda_metrics()
    assert swim_idea._acptfactheirs == first_earthdict
    assert swim_idea._acptfactunits == {}


def test_get_ranged_acptfacts():
    # GIVEN a single ranged acptfact
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    time_x = "time_x"
    x_agenda.add_idea(
        idea_kid=ideacore_shop(time_x, _begin=0, _close=140),
        pad=x_agenda._culture_qid,
    )

    clean = "clean"
    x_agenda.add_idea(ideacore_shop(clean, promise=True), pad=x_agenda._culture_qid)
    c_road = x_agenda.make_l1_road(clean)
    t_x_road = x_agenda.make_l1_road(time_x)
    # x_agenda.edit_idea_attr(road=c_road, required_base=t_x_road, required_sufffact=t_x_road, required_sufffact_open=5, required_sufffact_nigh=10)

    x_agenda.set_acptfact(base=t_x_road, pick=t_x_road, open=5, nigh=10)
    print(f"Given a single ranged acptfact {x_agenda._idearoot._acptfactunits=}")
    assert len(x_agenda._idearoot._acptfactunits) == 1

    # WHEN / THEN
    assert len(x_agenda._get_rangeroot_acptfactunits()) == 1

    # WHEN one ranged acptfact added
    place = "place_x"
    x_agenda.add_idea(
        idea_kid=ideacore_shop(place, _begin=600, _close=800),
        pad=x_agenda._culture_qid,
    )
    p_road = x_agenda.make_l1_road(place)
    x_agenda.set_acptfact(base=p_road, pick=p_road, open=5, nigh=10)
    print(f"When one ranged acptfact added {x_agenda._idearoot._acptfactunits=}")
    assert len(x_agenda._idearoot._acptfactunits) == 2

    # THEN
    assert len(x_agenda._get_rangeroot_acptfactunits()) == 2

    # WHEN one non-ranged_acptfact added
    mood = "mood_x"
    x_agenda.add_idea(ideacore_shop(mood), pad=x_agenda._culture_qid)
    m_road = x_agenda.make_l1_road(mood)
    x_agenda.set_acptfact(base=m_road, pick=m_road)
    print(f"When one non-ranged_acptfact added {x_agenda._idearoot._acptfactunits=}")
    assert len(x_agenda._idearoot._acptfactunits) == 3

    # THEN
    assert len(x_agenda._get_rangeroot_acptfactunits()) == 2


def test_get_roots_ranged_acptfacts():
    # GIVEN a two ranged acptfacts where one is "range-root" get_root_ranged_acptfacts returns one "range-root" acptfact
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    time_x = "time_x"
    x_agenda.add_idea(
        idea_kid=ideacore_shop(time_x, _begin=0, _close=140),
        pad=x_agenda._culture_qid,
    )
    t_x_road = x_agenda.make_l1_road(time_x)
    mood_x = "mood_x"
    x_agenda.add_idea(ideacore_shop(mood_x), pad=x_agenda._culture_qid)
    m_x_road = x_agenda.make_l1_road(mood_x)
    happy = "happy"
    sad = "Sad"
    x_agenda.add_idea(ideacore_shop(happy), pad=m_x_road)
    x_agenda.add_idea(ideacore_shop(sad), pad=m_x_road)
    x_agenda.set_acptfact(base=t_x_road, pick=t_x_road, open=5, nigh=10)
    x_agenda.set_acptfact(base=m_x_road, pick=x_agenda.make_road(m_x_road, happy))
    print(
        f"Given a root ranged acptfact and non-range acptfact:\n{x_agenda._idearoot._acptfactunits=}"
    )
    assert len(x_agenda._idearoot._acptfactunits) == 2

    # WHEN / THEN
    assert len(x_agenda._get_rangeroot_acptfactunits()) == 1
    assert x_agenda._get_rangeroot_acptfactunits()[0].base == t_x_road

    # a acptfact who's idea range is defined by numeric_root is not "rangeroot"
    mirrow_x = "mirrow_x"
    x_agenda.add_idea(
        idea_kid=ideacore_shop(mirrow_x, _numeric_road=time_x),
        pad=x_agenda._culture_qid,
    )
    m_x_road = x_agenda.make_l1_road(mirrow_x)
    x_agenda.set_acptfact(base=m_x_road, pick=t_x_road, open=5, nigh=10)
    assert len(x_agenda._idearoot._acptfactunits) == 3

    # WHEN / THEN
    assert len(x_agenda._get_rangeroot_acptfactunits()) == 1
    assert x_agenda._get_rangeroot_acptfactunits()[0].base == t_x_road


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario1():
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    # # the action
    # clean = "clean"
    # x_agenda.add_idea(ideacore_shop(clean, promise=True), pad=x_agenda._culture_qid)

    time_x = "time_x"
    x_agenda.add_idea(
        idea_kid=ideacore_shop(time_x, _begin=0, _close=140),
        pad=x_agenda._culture_qid,
    )
    t_x_road = x_agenda.make_l1_road(time_x)
    age1st = "age1st"
    age2nd = "age2nd"
    age3rd = "age3rd"
    age4th = "age4th"
    age5th = "age5th"
    age6th = "age6th"
    age7th = "age7th"
    x_agenda.add_idea(ideacore_shop(age1st, _begin=0, _close=20), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age2nd, _begin=20, _close=40), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age3rd, _begin=40, _close=60), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age4th, _begin=60, _close=80), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age5th, _begin=80, _close=100), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age6th, _begin=100, _close=120), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age7th, _begin=120, _close=140), pad=t_x_road)

    # set for instant moment in 3rd age
    x_agenda.set_acptfact(base=time_x, pick=time_x, open=45, nigh=45)
    lemma_dict = x_agenda._get_lemma_acptfactunits()
    print(f"{len(lemma_dict)=}")
    print(f"{lemma_dict=}")
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[x_agenda.make_road(t_x_road, age1st)]
    age2nd_lemma = lemma_dict[x_agenda.make_road(t_x_road, age2nd)]
    age3rd_lemma = lemma_dict[x_agenda.make_road(t_x_road, age3rd)]
    age4th_lemma = lemma_dict[x_agenda.make_road(t_x_road, age4th)]
    age5th_lemma = lemma_dict[x_agenda.make_road(t_x_road, age5th)]
    age6th_lemma = lemma_dict[x_agenda.make_road(t_x_road, age6th)]
    age7th_lemma = lemma_dict[x_agenda.make_road(t_x_road, age7th)]
    # assert age1st_lemma.active == False
    # assert age2nd_lemma.active == False
    # assert age3rd_lemma.active == True
    # assert age4th_lemma.active == False
    # assert age5th_lemma.active == False
    # assert age6th_lemma.active == False
    # assert age7th_lemma.active == False
    assert age1st_lemma.open is None
    assert age2nd_lemma.open is None
    assert age3rd_lemma.open == 45
    assert age4th_lemma.open is None
    assert age5th_lemma.open is None
    assert age6th_lemma.open is None
    assert age7th_lemma.open is None
    assert age1st_lemma.nigh is None
    assert age2nd_lemma.nigh is None
    assert age3rd_lemma.nigh == 45
    assert age4th_lemma.nigh is None
    assert age5th_lemma.nigh is None
    assert age6th_lemma.nigh is None
    assert age7th_lemma.nigh is None


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario2():
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    # # the action
    # clean = "clean"
    # x_agenda.add_idea(ideacore_shop(clean, promise=True), pad=x_agenda._culture_qid)

    time_x = "time_x"
    x_agenda.add_idea(
        idea_kid=ideacore_shop(time_x, _begin=0, _close=140),
        pad=x_agenda._culture_qid,
    )
    t_x_road = x_agenda.make_l1_road(time_x)
    age1st = "age1st"
    age2nd = "age2nd"
    age3rd = "age3rd"
    age4th = "age4th"
    age5th = "age5th"
    age6th = "age6th"
    age7th = "age7th"
    x_agenda.add_idea(ideacore_shop(age1st, _begin=0, _close=20), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age2nd, _begin=20, _close=40), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age3rd, _begin=40, _close=60), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age4th, _begin=60, _close=80), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age5th, _begin=80, _close=100), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age6th, _begin=100, _close=120), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age7th, _begin=120, _close=140), pad=t_x_road)

    # set for instant moment in 3rd age
    x_agenda.set_acptfact(base=time_x, pick=time_x, open=35, nigh=65)
    lemma_dict = x_agenda._get_lemma_acptfactunits()
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[x_agenda.make_road(t_x_road, age1st)]
    age2nd_lemma = lemma_dict[x_agenda.make_road(t_x_road, age2nd)]
    age3rd_lemma = lemma_dict[x_agenda.make_road(t_x_road, age3rd)]
    age4th_lemma = lemma_dict[x_agenda.make_road(t_x_road, age4th)]
    age5th_lemma = lemma_dict[x_agenda.make_road(t_x_road, age5th)]
    age6th_lemma = lemma_dict[x_agenda.make_road(t_x_road, age6th)]
    age7th_lemma = lemma_dict[x_agenda.make_road(t_x_road, age7th)]
    # assert age1st_lemma.active == False
    # assert age2nd_lemma.active == True
    # assert age3rd_lemma.active == True
    # assert age4th_lemma.active == True
    # assert age5th_lemma.active == False
    # assert age6th_lemma.active == False
    # assert age7th_lemma.active == False
    assert age1st_lemma.open is None
    assert age2nd_lemma.open == 35
    assert age3rd_lemma.open == 40
    assert age4th_lemma.open == 60
    assert age5th_lemma.open is None
    assert age6th_lemma.open is None
    assert age7th_lemma.open is None
    assert age1st_lemma.nigh is None
    assert age2nd_lemma.nigh == 40
    assert age3rd_lemma.nigh == 60
    assert age4th_lemma.nigh == 65
    assert age5th_lemma.nigh is None
    assert age6th_lemma.nigh is None
    assert age7th_lemma.nigh is None


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario3():
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    # # the action
    # clean = "clean"
    # x_agenda.add_idea(ideacore_shop(clean, promise=True), pad=x_agenda._culture_qid)

    time_x = "time_x"
    x_agenda.add_idea(
        idea_kid=ideacore_shop(time_x, _begin=0, _close=140),
        pad=x_agenda._culture_qid,
    )
    t_x_road = x_agenda.make_l1_road(time_x)
    age1st = "age1st"
    age2nd = "age2nd"
    age3rd = "age3rd"
    age4th = "age4th"
    age5th = "age5th"
    age6th = "age6th"
    age7th = "age7th"
    x_agenda.add_idea(ideacore_shop(age1st, _begin=0, _close=20), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age2nd, _begin=20, _close=40), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age3rd, _begin=40, _close=60), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age4th, _begin=60, _close=80), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age5th, _begin=80, _close=100), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age6th, _begin=100, _close=120), pad=t_x_road)
    x_agenda.add_idea(ideacore_shop(age7th, _begin=120, _close=140), pad=t_x_road)

    a2_road = x_agenda.make_road(t_x_road, age2nd)
    a2e1st = "a1_era1st"
    a2e2nd = "a1_era2nd"
    a2e3rd = "a1_era3rd"
    a2e4th = "a1_era4th"
    x_agenda.add_idea(ideacore_shop(a2e1st, _begin=20, _close=30), pad=a2_road)
    x_agenda.add_idea(ideacore_shop(a2e2nd, _begin=30, _close=34), pad=a2_road)
    x_agenda.add_idea(ideacore_shop(a2e3rd, _begin=34, _close=38), pad=a2_road)
    x_agenda.add_idea(ideacore_shop(a2e4th, _begin=38, _close=40), pad=a2_road)

    a3_road = x_agenda.make_road(t_x_road, age3rd)
    a3e1st = "a3_era1st"
    a3e2nd = "a3_era2nd"
    a3e3rd = "a3_era3rd"
    a3e4th = "a3_era4th"
    x_agenda.add_idea(ideacore_shop(a3e1st, _begin=40, _close=45), pad=a3_road)
    x_agenda.add_idea(ideacore_shop(a3e2nd, _begin=45, _close=50), pad=a3_road)
    x_agenda.add_idea(ideacore_shop(a3e3rd, _begin=55, _close=58), pad=a3_road)
    x_agenda.add_idea(ideacore_shop(a3e4th, _begin=58, _close=60), pad=a3_road)

    # set for instant moment in 3rd age
    x_agenda.set_acptfact(base=time_x, pick=time_x, open=35, nigh=55)
    lemma_dict = x_agenda._get_lemma_acptfactunits()
    assert len(lemma_dict) == 15
    a2e1st_lemma = lemma_dict[x_agenda.make_road(a2_road, a2e1st)]
    a2e2nd_lemma = lemma_dict[x_agenda.make_road(a2_road, a2e2nd)]
    a2e3rd_lemma = lemma_dict[x_agenda.make_road(a2_road, a2e3rd)]
    a2e4th_lemma = lemma_dict[x_agenda.make_road(a2_road, a2e4th)]
    a3e1st_lemma = lemma_dict[x_agenda.make_road(a3_road, a3e1st)]
    a3e2nd_lemma = lemma_dict[x_agenda.make_road(a3_road, a3e2nd)]
    a3e3rd_lemma = lemma_dict[x_agenda.make_road(a3_road, a3e3rd)]
    a3e4th_lemma = lemma_dict[x_agenda.make_road(a3_road, a3e4th)]
    # assert a2e1st_lemma.active == False
    # assert a2e2nd_lemma.active == False
    # assert a2e3rd_lemma.active == True
    # assert a2e4th_lemma.active == True
    # assert a3e1st_lemma.active == True
    # assert a3e2nd_lemma.active == True
    # assert a3e3rd_lemma.active == False
    # assert a3e4th_lemma.active == False
    assert a2e1st_lemma.open is None
    assert a2e2nd_lemma.open is None
    assert a2e3rd_lemma.open == 35
    assert a2e4th_lemma.open == 38
    assert a3e1st_lemma.open == 40
    assert a3e2nd_lemma.open == 45
    assert a3e3rd_lemma.open is None
    assert a3e4th_lemma.open is None
    assert a2e1st_lemma.nigh is None
    assert a2e2nd_lemma.nigh is None
    assert a2e3rd_lemma.nigh == 38
    assert a2e4th_lemma.nigh == 40
    assert a3e1st_lemma.nigh == 45
    assert a3e2nd_lemma.nigh == 50
    assert a3e3rd_lemma.nigh is None
    assert a3e4th_lemma.nigh is None


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario4():
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    time_x = "time_x"
    arsub1 = "descretional_subsection1"
    as1_road = x_agenda.make_l1_road(arsub1)
    x_agenda.add_idea(
        ideacore_shop(arsub1, _begin=0, _close=140), pad=x_agenda._culture_qid
    )
    # range-root idea has range_source_road
    x_agenda.add_idea(
        ideacore_shop(time_x, _begin=0, _close=140, _range_source_road=as1_road),
        pad=x_agenda._culture_qid,
    )

    arsub2 = "descretional_subsection2"
    as2_road = x_agenda.make_l1_road(arsub2)
    x_agenda.add_idea(
        ideacore_shop(arsub2, _begin=0, _close=20), pad=x_agenda._culture_qid
    )

    # non-range-root child idea has range_source_road
    t_x_road = x_agenda.make_l1_road(time_x)
    age1st = "age1st"
    x_agenda.add_idea(
        ideacore_shop(age1st, _begin=0, _close=20, _range_source_road=as2_road),
        pad=t_x_road,
    )

    # set for instant moment in 3rd age
    x_agenda.set_acptfact(base=time_x, pick=time_x, open=35, nigh=55)
    lemma_dict = x_agenda._get_lemma_acptfactunits()
    assert len(lemma_dict) == 3
    a1_lemma = lemma_dict[x_agenda.make_road(t_x_road, age1st)]
    as1_lemma = lemma_dict[as1_road]
    as2_lemma = lemma_dict[as2_road]
    # assert a1_lemma.active == False
    # assert as1_lemma.active == True
    # assert as2_lemma.active == False
    assert a1_lemma.open is None
    assert as1_lemma.open == 35
    assert as2_lemma.open is None
    assert a1_lemma.nigh is None
    assert as1_lemma.nigh == 55
    assert as2_lemma.nigh is None


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario4_1():
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = x_agenda.make_l1_road("time")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")
    timetech_road = x_agenda.make_road(time_road, "tech")
    x_agenda.set_acptfact(base=jajatime_road, pick=jajatime_road, open=1500, nigh=1500)
    lhu = x_agenda._get_lemma_acptfactunits()

    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycle")].open == 1500
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycle")].nigh == 1500
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].open > 0
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].open < 1
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].nigh > 0
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].nigh < 1
    assert lhu[x_agenda.make_road(jajatime_road, "days")].open >= 1
    assert lhu[x_agenda.make_road(jajatime_road, "days")].open <= 2
    assert lhu[x_agenda.make_road(jajatime_road, "days")].nigh >= 1
    assert lhu[x_agenda.make_road(jajatime_road, "days")].nigh <= 2
    assert lhu[x_agenda.make_road(jajatime_road, "day")].open == 60
    assert lhu[x_agenda.make_road(jajatime_road, "day")].nigh == 60
    assert lhu[x_agenda.make_road(jajatime_road, "week")].open == 1500
    assert int(lhu[x_agenda.make_road(jajatime_road, "week")].nigh) == 1500
    assert lhu[x_agenda.make_road(timetech_road, "week")].open == 1500
    assert int(lhu[x_agenda.make_road(timetech_road, "week")].nigh) == 1500


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario5():
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = x_agenda.make_l1_road("time")
    timetech_road = x_agenda.make_road(time_road, "tech")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")
    x_agenda.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1500, nigh=1063954002
    )
    lhu = x_agenda._get_lemma_acptfactunits()

    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycle")].open == 0
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycle")].nigh == 210379680
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].open > 0
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].open < 1
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].nigh > 5
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].nigh < 6
    assert int(lhu[x_agenda.make_road(jajatime_road, "days")].open) == 1  # 0 / 1440
    assert (
        int(lhu[x_agenda.make_road(jajatime_road, "days")].nigh) == 738856
    )  # 1063953183 / 1440
    assert lhu[x_agenda.make_road(jajatime_road, "day")].open == 0  # 0 / 1440
    assert (
        lhu[x_agenda.make_road(jajatime_road, "day")].nigh == 1440
    )  # 1362  # 1063953183 / 1440
    assert lhu[x_agenda.make_road(jajatime_road, "week")].open == 0  # 0 / 1440
    assert (
        int(lhu[x_agenda.make_road(jajatime_road, "week")].nigh) == 10080
    )  # 1063953183 / 1440
    assert lhu[x_agenda.make_road(timetech_road, "week")].open == 0  # 0 / 1440
    assert (
        int(lhu[x_agenda.make_road(timetech_road, "week")].nigh) == 10080
    )  # 1063953183 / 1440


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario6():
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = x_agenda.make_l1_road("time")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")
    x_agenda.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063954000, nigh=1063954002
    )
    lhu = x_agenda._get_lemma_acptfactunits()

    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycle")].open == 12055600.0
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycle")].nigh == 12055602.0
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].open > 5
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].open < 6
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].nigh > 5
    assert lhu[x_agenda.make_road(jajatime_road, "400 year cycles")].nigh < 6
    assert (
        int(lhu[x_agenda.make_road(jajatime_road, "days")].open) == 738856
    )  # 1063954000 / 1440
    assert (
        int(lhu[x_agenda.make_road(jajatime_road, "days")].nigh) == 738856
    )  # 1063954000 / 1440
    assert lhu[x_agenda.make_road(jajatime_road, "day")].open == 1360  # 0 / 1440
    assert (
        int(lhu[x_agenda.make_road(jajatime_road, "day")].nigh) == 1362
    )  # 1063953183 / 1440


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario7():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = x_agenda.make_l1_road("time")
    timetech_road = x_agenda.make_road(time_road, "tech")
    techweek_road = x_agenda.make_road(timetech_road, "week")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")

    # WHEN given a minute range that should be Thursday to Monday midnight
    x_agenda.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063951200, nigh=1063956960
    )
    lhu = x_agenda._get_lemma_acptfactunits()

    # THEN
    week_open = lhu[x_agenda.make_road(jajatime_road, "week")].open
    week_nigh = lhu[x_agenda.make_road(jajatime_road, "week")].nigh
    week_text = "week"
    print(
        f"for {x_agenda.make_road(jajatime_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[x_agenda.make_road(jajatime_road, "week")].open == 7200
    assert lhu[x_agenda.make_road(jajatime_road, "week")].nigh == 2880

    week_open = lhu[x_agenda.make_road(timetech_road, "week")].open
    week_nigh = lhu[x_agenda.make_road(timetech_road, "week")].nigh
    print(
        f"for {x_agenda.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[x_agenda.make_road(timetech_road, "week")].open == 7200
    assert lhu[x_agenda.make_road(timetech_road, "week")].nigh == 2880
    print(f"{techweek_road=}")
    print(lhu[techweek_road])
    print(lhu[x_agenda.make_road(techweek_road, "Thursday")])
    print(lhu[x_agenda.make_road(techweek_road, "Friday")])
    print(lhu[x_agenda.make_road(techweek_road, "Saturday")])
    print(lhu[x_agenda.make_road(techweek_road, "Sunday")])
    print(lhu[x_agenda.make_road(techweek_road, "Monday")])
    print(lhu[x_agenda.make_road(techweek_road, "Tuesday")])
    print(lhu[x_agenda.make_road(techweek_road, "Wednesday")])

    # assert lhu[x_agenda.make_road(timetech_road,"week,Thursday")].active == True
    # assert lhu[x_agenda.make_road(timetech_road,"week,Friday")].active == True
    # assert lhu[x_agenda.make_road(timetech_road,"week,Saturday")].active == True
    # assert lhu[x_agenda.make_road(timetech_road,"week,Sunday")].active == True
    # assert lhu[x_agenda.make_road(timetech_road,"week,Monday")].active == False
    # assert lhu[x_agenda.make_road(timetech_road,"week,Tuesday")].active == False
    # assert lhu[x_agenda.make_road(timetech_road,"week,Wednesday")].active == False


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario8():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = x_agenda.make_l1_road("time")
    timetech_road = x_agenda.make_road(time_road, "tech")
    techweek_road = x_agenda.make_road(timetech_road, "week")
    jajatime_road = x_agenda.make_road(time_road, "jajatime")

    # WHEN given a minute range that should be Thursday to Monday midnight
    x_agenda.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063951200, nigh=1063951200
    )
    lhu = x_agenda._get_lemma_acptfactunits()

    # THEN
    week_open = lhu[techweek_road].open
    week_nigh = lhu[techweek_road].nigh
    print(f"for {techweek_road}: {week_open=} {week_nigh=}")
    assert lhu[techweek_road].open == 7200
    assert lhu[techweek_road].nigh == 7200

    week_open = lhu[x_agenda.make_road(timetech_road, "week")].open
    week_nigh = lhu[x_agenda.make_road(timetech_road, "week")].nigh
    week_text = "week"
    print(
        f"for {x_agenda.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[x_agenda.make_road(timetech_road, "week")].open == 7200
    assert lhu[x_agenda.make_road(timetech_road, "week")].nigh == 7200
    print(lhu[techweek_road])
    print(lhu[x_agenda.make_road(techweek_road, "Thursday")])
    print(lhu[x_agenda.make_road(techweek_road, "Friday")])
    print(lhu[x_agenda.make_road(techweek_road, "Saturday")])
    print(lhu[x_agenda.make_road(techweek_road, "Sunday")])
    print(lhu[x_agenda.make_road(techweek_road, "Monday")])
    print(lhu[x_agenda.make_road(techweek_road, "Tuesday")])
    print(lhu[x_agenda.make_road(techweek_road, "Wednesday")])

    # assert lhu[x_agenda.make_road(timetech_road,"week,Thursday")].active == True
    # assert lhu[x_agenda.make_road(timetech_road,"week,Friday")].active == False
    # assert lhu[x_agenda.make_road(timetech_road,"week,Saturday")].active == False
    # assert lhu[x_agenda.make_road(timetech_road,"week,Sunday")].active == False
    # assert lhu[x_agenda.make_road(timetech_road,"week,Monday")].active == False
    # assert lhu[x_agenda.make_road(timetech_road,"week,Tuesday")].active == False
    # assert lhu[x_agenda.make_road(timetech_road,"week,Wednesday")].active == False


def test_agenda_set_acptfact_create_missing_ideas_CreatesBaseAndAcptFact():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda._idearoot.set_kids_empty_if_null()
    issue_text = "issues"
    issue_road = x_agenda.make_l1_road(issue_text)
    climate_text = "climate"
    climate_road = x_agenda.make_road(issue_road, climate_text)
    assert x_agenda._idearoot._kids.get(issue_text) is None

    # WHEN
    x_agenda.set_acptfact(base=issue_road, pick=climate_road, create_missing_ideas=True)

    # THEN
    assert x_agenda._idearoot._kids.get(issue_text) != None
    assert x_agenda.get_idea_kid(issue_road) != None
    assert x_agenda.get_idea_kid(climate_road) != None


def test_agenda_get_acptfactunits_base_and_acptfact_list_CorrectlyReturnsListOfAcptFactUnits():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(healer_text)
    x_agenda._idearoot.set_kids_empty_if_null()

    issue_text = "issues"
    issue_road = x_agenda.make_l1_road(issue_text)
    climate_text = "climate"
    climate_road = x_agenda.make_road(issue_road, climate_text)
    x_agenda.set_acptfact(base=issue_road, pick=climate_road, create_missing_ideas=True)

    weather_text = "weather"
    weather_road = x_agenda.make_l1_road(weather_text)
    windy_text = "windy"
    windy_road = x_agenda.make_road(weather_road, windy_text)
    x_agenda.set_acptfact(base=weather_road, pick=windy_road, create_missing_ideas=True)
    hot_text = "hot"
    hot_road = x_agenda.make_road(weather_road, hot_text)
    x_agenda.set_acptfact(base=weather_road, pick=hot_road, create_missing_ideas=True)
    cold_text = "cold"
    cold_road = x_agenda.make_road(weather_road, cold_text)
    x_agenda.set_acptfact(base=weather_road, pick=cold_road, create_missing_ideas=True)

    games_text = "games"
    games_road = x_agenda.make_l1_road(games_text)
    football_text = "football"
    football_road = x_agenda.make_road(weather_road, football_text)
    x_agenda.set_acptfact(
        base=games_road, pick=football_road, create_missing_ideas=True
    )

    # WHEN
    acptfactunit_list_x = x_agenda.get_acptfactunits_base_and_acptfact_list()

    # THEN
    assert acptfactunit_list_x[0][0] == ""
    assert acptfactunit_list_x[1][0] == games_road
    assert acptfactunit_list_x[1][1] == football_road
    assert acptfactunit_list_x[2][0] == issue_road
    assert acptfactunit_list_x[2][1] == climate_road
    assert acptfactunit_list_x[3][0] == weather_road
    assert acptfactunit_list_x[3][1] == cold_road
    assert len(acptfactunit_list_x) == 4
