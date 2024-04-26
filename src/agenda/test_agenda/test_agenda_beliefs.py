from src.agenda.reason_idea import (
    beliefunit_shop,
    beliefunit_shop,
    beliefheir_shop,
)
from src.agenda.idea import ideaunit_shop, RoadUnit
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as examples_get_agenda_with_4_levels,
)
from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_AgendaUnit_set_belief_CorrectlyChangesAttr_1():
    # GIVEN
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    sunday_road = x_agenda.make_road(weekday_road, "Sunday")
    sunday_agenda_belief = beliefunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_agenda_belief)
    x_idearoot = x_agenda._idearoot
    x_idearoot._beliefunits = {sunday_agenda_belief.base: sunday_agenda_belief}
    assert x_idearoot._beliefunits != None
    x_idearoot._beliefunits = {}
    assert not x_idearoot._beliefunits

    # GIVEN
    x_agenda.set_belief(base=weekday_road, pick=sunday_road)

    # THEN
    assert x_idearoot._beliefunits == {sunday_agenda_belief.base: sunday_agenda_belief}

    # GIVEN
    x_idearoot._beliefunits = {}
    assert not x_idearoot._beliefunits
    usa_week_road = x_agenda.make_l1_road("nation-state")
    usa_week_unit = beliefunit_shop(usa_week_road, usa_week_road, open=608, nigh=610)
    x_idearoot._beliefunits = {usa_week_unit.base: usa_week_unit}

    x_idearoot._beliefunits = {}
    assert not x_idearoot._beliefunits

    # WHEN
    x_agenda.set_belief(base=usa_week_road, pick=usa_week_road, open=608, nigh=610)

    # THEN
    assert x_idearoot._beliefunits != None
    assert x_idearoot._beliefunits == {usa_week_unit.base: usa_week_unit}


def test_AgendaUnit_set_belief_CorrectlyChangesAttr_2():
    # GIVEN
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    sunday_road = x_agenda.make_road(weekday_road, "Sunday")

    # WHEN
    x_agenda.set_belief(base=weekday_road, pick=sunday_road)

    # THEN
    sunday_agenda_belief = beliefunit_shop(base=weekday_road, pick=sunday_road)
    x_idearoot = x_agenda._idearoot
    assert x_idearoot._beliefunits == {sunday_agenda_belief.base: sunday_agenda_belief}


def test_AgendaUnit_set_belief_CorrectlyChangesAttrWhen_pick_IsNone():
    # GIVEN
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")

    # WHEN
    x_agenda.set_belief(base=weekday_road, open=5, nigh=7)

    # THEN
    sunday_agenda_belief = beliefunit_shop(weekday_road, weekday_road, 5, 7)
    x_idearoot = x_agenda._idearoot
    assert x_idearoot._beliefunits == {sunday_agenda_belief.base: sunday_agenda_belief}


def test_AgendaUnit_set_belief_CorrectlyChangesAttrWhen_open_IsNone():
    # GIVEN
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    x_agenda.set_belief(base=weekday_road, open=5, nigh=7)
    x_idearoot = x_agenda._idearoot
    assert x_idearoot._beliefunits.get(weekday_road) == beliefunit_shop(
        weekday_road, weekday_road, 5, 7
    )

    # WHEN
    x_agenda.set_belief(base=weekday_road, nigh=10)

    # THEN
    assert x_idearoot._beliefunits.get(weekday_road) == beliefunit_shop(
        weekday_road, weekday_road, 5, 10
    )


def test_AgendaUnit_set_belief_FailsToCreateWhenBaseAndBeliefAreDifferenctAndBeliefIdeaIsNotRangeRoot():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    bob_agenda.add_l1_idea(time_idea)
    time_road = bob_agenda.make_l1_road(time_text)
    a1st = "age1st"
    a1st_road = bob_agenda.make_road(time_road, a1st)
    a1st_idea = ideaunit_shop(a1st, _begin=0, _close=20)
    bob_agenda.add_idea(a1st_idea, parent_road=time_road)
    a1e1st_text = "a1_era1st"
    a1e1st_idea = ideaunit_shop(a1e1st_text, _begin=20, _close=30)
    bob_agenda.add_idea(a1e1st_idea, parent_road=a1st_road)
    a1e1_road = bob_agenda.make_road(a1st_road, a1e1st_text)
    assert bob_agenda._idearoot._beliefunits in (None, {})

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_agenda.set_belief(base=a1e1_road, pick=a1e1_road, open=20, nigh=23)
    assert (
        str(excinfo.value)
        == f"Non range-root belief:{a1e1_road} can only be set by range-root belief"
    )


def test_AgendaUnit_del_belief_CorrectlyChangesAttr():
    # GIVEN
    x_agenda = examples_get_agenda_with_4_levels()
    weekday_road = x_agenda.make_l1_road("weekdays")
    sunday_road = x_agenda.make_road(weekday_road, "Sunday")
    x_agenda.set_belief(base=weekday_road, pick=sunday_road)
    sunday_agenda_belief = beliefunit_shop(base=weekday_road, pick=sunday_road)
    x_idearoot = x_agenda._idearoot
    assert x_idearoot._beliefunits == {sunday_agenda_belief.base: sunday_agenda_belief}

    # WHEN
    x_agenda.del_belief(base=weekday_road)

    # THEN
    assert x_idearoot._beliefunits == {}


def test_AgendaUnit_get_idea_list_BeliefHeirsCorrectlyInherited():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    swim_text = "swim"
    swim_road = bob_agenda.make_l1_road(swim_text)
    bob_agenda.add_l1_idea(ideaunit_shop(swim_text))
    fast_text = "fast"
    slow_text = "slow"
    fast_road = bob_agenda.make_road(swim_road, fast_text)
    slow_road = bob_agenda.make_road(swim_road, slow_text)
    bob_agenda.add_idea(ideaunit_shop(fast_text), parent_road=swim_road)
    bob_agenda.add_idea(ideaunit_shop(slow_text), parent_road=swim_road)

    earth_text = "earth"
    earth_road = bob_agenda.make_l1_road(earth_text)
    bob_agenda.add_l1_idea(ideaunit_shop(earth_text))

    swim_idea = bob_agenda.get_idea_obj(swim_road)
    fast_idea = bob_agenda.get_idea_obj(fast_road)
    slow_idea = bob_agenda.get_idea_obj(slow_road)

    assert swim_idea._beliefheirs == {}
    assert fast_idea._beliefheirs == {}
    assert slow_idea._beliefheirs == {}

    # WHEN
    bob_agenda.set_belief(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)
    beliefheir_set_range = beliefheir_shop(earth_road, earth_road, 1.0, 5.0)
    beliefheirs_set_range = {beliefheir_set_range.base: beliefheir_set_range}
    belief_none_range = beliefheir_shop(earth_road, earth_road, None, None)
    beliefs_none_range = {belief_none_range.base: belief_none_range}

    # THEN
    assert swim_idea._beliefheirs != None
    assert fast_idea._beliefheirs != None
    assert slow_idea._beliefheirs != None
    assert swim_idea._beliefheirs == beliefheirs_set_range
    assert fast_idea._beliefheirs == beliefheirs_set_range
    assert slow_idea._beliefheirs == beliefheirs_set_range
    print(f"{swim_idea._beliefheirs=}")
    assert len(swim_idea._beliefheirs) == 1

    # WHEN
    swim_idea._beliefheirs.get(earth_road).set_range_null()

    # THEN
    assert swim_idea._beliefheirs == beliefs_none_range
    assert fast_idea._beliefheirs == beliefheirs_set_range
    assert slow_idea._beliefheirs == beliefheirs_set_range

    belief_x1 = swim_idea._beliefheirs.get(earth_road)
    belief_x1.set_range_null()
    print(type(belief_x1))
    assert str(type(belief_x1)).find(".reason.BeliefHeir'>")


def test_AgendaUnit_get_idea_list_BeliefUnitCorrectlyTransformsbeliefheir_shop():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    swim_text = "swim"
    swim_road = bob_agenda.make_l1_road(swim_text)
    bob_agenda.add_l1_idea(ideaunit_shop(swim_text))
    swim_idea = bob_agenda.get_idea_obj(swim_road)

    fast_text = "fast"
    slow_text = "slow"
    bob_agenda.add_idea(ideaunit_shop(fast_text), parent_road=swim_road)
    bob_agenda.add_idea(ideaunit_shop(slow_text), parent_road=swim_road)

    earth_text = "earth"
    earth_road = bob_agenda.make_l1_road(earth_text)
    bob_agenda.add_l1_idea(ideaunit_shop(earth_text))

    assert swim_idea._beliefheirs == {}

    # WHEN
    bob_agenda.set_belief(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)

    # THEN
    first_earthheir = beliefheir_shop(earth_road, earth_road, open=1.0, nigh=5.0)
    first_earthdict = {first_earthheir.base: first_earthheir}
    assert swim_idea._beliefheirs == first_earthdict

    # WHEN
    # earth_curb = beliefunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    # swim_y.set_beliefunit(beliefunit=earth_curb) Not sure what this is for. Testing what "set_beliefunit" does with the parameters, but what?
    bob_agenda.set_belief(base=earth_road, pick=earth_road, open=3.0, nigh=5.0)

    # THEN
    after_earthheir = beliefheir_shop(earth_road, earth_road, open=3.0, nigh=5.0)
    after_earthdict = {after_earthheir.base: after_earthheir}
    assert swim_idea._beliefheirs == after_earthdict


def test_AgendaUnit_get_idea_list_BeliefHeirCorrectlyDeletesBeliefUnit():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    swim_text = "swim"
    swim_road = sue_agenda.make_l1_road(swim_text)
    sue_agenda.add_l1_idea(ideaunit_shop(swim_text))
    fast_text = "fast"
    slow_text = "slow"
    sue_agenda.add_idea(ideaunit_shop(fast_text), parent_road=swim_road)
    sue_agenda.add_idea(ideaunit_shop(slow_text), parent_road=swim_road)
    earth_text = "earth"
    earth_road = sue_agenda.make_l1_road(earth_text)
    sue_agenda.add_l1_idea(ideaunit_shop(earth_text))

    swim_idea = sue_agenda.get_idea_obj(swim_road)

    first_earthheir = beliefheir_shop(earth_road, earth_road, open=200.0, nigh=500.0)
    first_earthdict = {first_earthheir.base: first_earthheir}

    assert swim_idea._beliefheirs == {}

    # WHEN
    sue_agenda.set_belief(base=earth_road, pick=earth_road, open=200.0, nigh=500.0)

    # THEN
    assert swim_idea._beliefheirs == first_earthdict

    earth_curb = beliefunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    swim_idea.set_beliefunit(beliefunit=earth_curb)
    sue_agenda.set_agenda_metrics()
    assert swim_idea._beliefheirs == first_earthdict
    assert swim_idea._beliefunits == {}


def test_get_ranged_beliefs():
    # GIVEN a single ranged belief
    sue_agenda = agendaunit_shop("Sue")
    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    sue_agenda.add_l1_idea(time_idea)

    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text, promise=True)
    sue_agenda.add_l1_idea(clean_idea)
    c_road = sue_agenda.make_l1_road(clean_text)
    time_road = sue_agenda.make_l1_road(time_text)
    # sue_agenda.edit_idea_attr(road=c_road, reason_base=time_road, reason_premise=time_road, reason_premise_open=5, reason_premise_nigh=10)

    sue_agenda.set_belief(base=time_road, pick=time_road, open=5, nigh=10)
    print(f"Given a single ranged belief {sue_agenda._idearoot._beliefunits=}")
    assert len(sue_agenda._idearoot._beliefunits) == 1

    # WHEN / THEN
    assert len(sue_agenda._get_rangeroot_beliefunits()) == 1

    # WHEN one ranged belief added
    place_text = "place_x"
    place_idea = ideaunit_shop(place_text, _begin=600, _close=800)
    sue_agenda.add_l1_idea(place_idea)
    place_road = sue_agenda.make_l1_road(place_text)
    sue_agenda.set_belief(base=place_road, pick=place_road, open=5, nigh=10)
    print(f"When one ranged belief added {sue_agenda._idearoot._beliefunits=}")
    assert len(sue_agenda._idearoot._beliefunits) == 2

    # THEN
    assert len(sue_agenda._get_rangeroot_beliefunits()) == 2

    # WHEN one non-ranged_belief added
    mood = "mood_x"
    sue_agenda.add_l1_idea(ideaunit_shop(mood))
    m_road = sue_agenda.make_l1_road(mood)
    sue_agenda.set_belief(base=m_road, pick=m_road)
    print(f"When one non-ranged_belief added {sue_agenda._idearoot._beliefunits=}")
    assert len(sue_agenda._idearoot._beliefunits) == 3

    # THEN
    assert len(sue_agenda._get_rangeroot_beliefunits()) == 2


def test_get_roots_ranged_beliefs():
    # GIVEN a two ranged beliefs where one is "range-root" get_root_ranged_beliefs returns one "range-root" belief
    sue_agenda = agendaunit_shop("Sue")
    time_text = "time"
    sue_agenda.add_l1_idea(ideaunit_shop(time_text, _begin=0, _close=140))
    time_road = sue_agenda.make_l1_road(time_text)
    mood_x = "mood_x"
    sue_agenda.add_l1_idea(ideaunit_shop(mood_x))
    m_x_road = sue_agenda.make_l1_road(mood_x)
    happy = "happy"
    sad = "Sad"
    sue_agenda.add_idea(ideaunit_shop(happy), parent_road=m_x_road)
    sue_agenda.add_idea(ideaunit_shop(sad), parent_road=m_x_road)
    sue_agenda.set_belief(base=time_road, pick=time_road, open=5, nigh=10)
    sue_agenda.set_belief(base=m_x_road, pick=sue_agenda.make_road(m_x_road, happy))
    print(
        f"Given a root ranged belief and non-range belief:\n{sue_agenda._idearoot._beliefunits=}"
    )
    assert len(sue_agenda._idearoot._beliefunits) == 2

    # WHEN / THEN
    assert len(sue_agenda._get_rangeroot_beliefunits()) == 1
    assert sue_agenda._get_rangeroot_beliefunits()[0].base == time_road

    # a belief who's idea range is defined by numeric_root is not "rangeroot"
    mirror_x = "mirror_x"
    sue_agenda.add_l1_idea(ideaunit_shop(mirror_x, _numeric_road=time_text))
    m_x_road = sue_agenda.make_l1_road(mirror_x)
    sue_agenda.set_belief(base=m_x_road, pick=time_road, open=5, nigh=10)
    assert len(sue_agenda._idearoot._beliefunits) == 3

    # WHEN / THEN
    assert len(sue_agenda._get_rangeroot_beliefunits()) == 1
    assert sue_agenda._get_rangeroot_beliefunits()[0].base == time_road


def test_create_lemma_beliefs_CorrectlyCreates1stLevelLemmaBelief_Scenario1():
    sue_agenda = agendaunit_shop("Sue")
    # # the action
    # clean = "clean"
    # sue_agenda.add_idea(ideaunit_shop(clean, promise=True))

    time_text = "time"
    sue_agenda.add_l1_idea(ideaunit_shop(time_text, _begin=0, _close=140))
    time_road = sue_agenda.make_l1_road(time_text)
    age1st_text = "age1st"
    age2nd_text = "age2nd"
    age3rd_text = "age3rd"
    age4th_text = "age4th"
    age5th_text = "age5th"
    age6th_text = "age6th"
    age7th_text = "age7th"
    age1st_idea = ideaunit_shop(age1st_text, _begin=0, _close=20)
    age2nd_idea = ideaunit_shop(age2nd_text, _begin=20, _close=40)
    age3rd_idea = ideaunit_shop(age3rd_text, _begin=40, _close=60)
    age4th_idea = ideaunit_shop(age4th_text, _begin=60, _close=80)
    age5th_idea = ideaunit_shop(age5th_text, _begin=80, _close=100)
    age6th_idea = ideaunit_shop(age6th_text, _begin=100, _close=120)
    age7th_idea = ideaunit_shop(age7th_text, _begin=120, _close=140)
    sue_agenda.add_idea(age1st_idea, parent_road=time_road)
    sue_agenda.add_idea(age2nd_idea, parent_road=time_road)
    sue_agenda.add_idea(age3rd_idea, parent_road=time_road)
    sue_agenda.add_idea(age4th_idea, parent_road=time_road)
    sue_agenda.add_idea(age5th_idea, parent_road=time_road)
    sue_agenda.add_idea(age6th_idea, parent_road=time_road)
    sue_agenda.add_idea(age7th_idea, parent_road=time_road)

    # set for instant moment in 3rd age
    sue_agenda.set_belief(base=time_road, pick=time_road, open=45, nigh=45)
    lemma_dict = sue_agenda._get_lemma_beliefunits()
    print(f"{len(lemma_dict)=}")
    print(f"{lemma_dict=}")
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[sue_agenda.make_road(time_road, age1st_text)]
    age2nd_lemma = lemma_dict[sue_agenda.make_road(time_road, age2nd_text)]
    age3rd_lemma = lemma_dict[sue_agenda.make_road(time_road, age3rd_text)]
    age4th_lemma = lemma_dict[sue_agenda.make_road(time_road, age4th_text)]
    age5th_lemma = lemma_dict[sue_agenda.make_road(time_road, age5th_text)]
    age6th_lemma = lemma_dict[sue_agenda.make_road(time_road, age6th_text)]
    age7th_lemma = lemma_dict[sue_agenda.make_road(time_road, age7th_text)]
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


def test_create_lemma_beliefs_CorrectlyCreates1stLevelLemmaBelief_Scenario2():
    sue_agenda = agendaunit_shop("Sue")
    # # the action
    # clean = "clean"
    # sue_agenda.add_idea(ideaunit_shop(clean, promise=True))

    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    time_road = sue_agenda.make_l1_road(time_text)
    sue_agenda.add_l1_idea(time_idea)
    age1st_text = "age1st"
    age2nd_text = "age2nd"
    age3rd_text = "age3rd"
    age4th_text = "age4th"
    age5th_text = "age5th"
    age6th_text = "age6th"
    age7th_text = "age7th"
    age1st_idea = ideaunit_shop(age1st_text, _begin=0, _close=20)
    age2nd_idea = ideaunit_shop(age2nd_text, _begin=20, _close=40)
    age3rd_idea = ideaunit_shop(age3rd_text, _begin=40, _close=60)
    age4th_idea = ideaunit_shop(age4th_text, _begin=60, _close=80)
    age5th_idea = ideaunit_shop(age5th_text, _begin=80, _close=100)
    age6th_idea = ideaunit_shop(age6th_text, _begin=100, _close=120)
    age7th_idea = ideaunit_shop(age7th_text, _begin=120, _close=140)
    sue_agenda.add_idea(age1st_idea, parent_road=time_road)
    sue_agenda.add_idea(age2nd_idea, parent_road=time_road)
    sue_agenda.add_idea(age3rd_idea, parent_road=time_road)
    sue_agenda.add_idea(age4th_idea, parent_road=time_road)
    sue_agenda.add_idea(age5th_idea, parent_road=time_road)
    sue_agenda.add_idea(age6th_idea, parent_road=time_road)
    sue_agenda.add_idea(age7th_idea, parent_road=time_road)

    # set for instant moment in 3rd age
    sue_agenda.set_belief(base=time_road, pick=time_road, open=35, nigh=65)
    lemma_dict = sue_agenda._get_lemma_beliefunits()
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[sue_agenda.make_road(time_road, age1st_text)]
    age2nd_lemma = lemma_dict[sue_agenda.make_road(time_road, age2nd_text)]
    age3rd_lemma = lemma_dict[sue_agenda.make_road(time_road, age3rd_text)]
    age4th_lemma = lemma_dict[sue_agenda.make_road(time_road, age4th_text)]
    age5th_lemma = lemma_dict[sue_agenda.make_road(time_road, age5th_text)]
    age6th_lemma = lemma_dict[sue_agenda.make_road(time_road, age6th_text)]
    age7th_lemma = lemma_dict[sue_agenda.make_road(time_road, age7th_text)]
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


def test_create_lemma_beliefs_CorrectlyCreates1stLevelLemmaBelief_Scenario3():
    sue_agenda = agendaunit_shop("Sue")
    # # the action
    # clean = "clean"
    # sue_agenda.add_idea(ideaunit_shop(clean, promise=True))

    time_text = "time"
    time_idea = ideaunit_shop(time_text, _begin=0, _close=140)
    time_road = sue_agenda.make_l1_road(time_text)
    sue_agenda.add_l1_idea(time_idea)
    age1st_text = "age1st"
    age2nd_text = "age2nd"
    age3rd_text = "age3rd"
    age4th_text = "age4th"
    age5th_text = "age5th"
    age6th_text = "age6th"
    age7th_text = "age7th"
    age1st_idea = ideaunit_shop(age1st_text, _begin=0, _close=20)
    age2nd_idea = ideaunit_shop(age2nd_text, _begin=20, _close=40)
    age3rd_idea = ideaunit_shop(age3rd_text, _begin=40, _close=60)
    age4th_idea = ideaunit_shop(age4th_text, _begin=60, _close=80)
    age5th_idea = ideaunit_shop(age5th_text, _begin=80, _close=100)
    age6th_idea = ideaunit_shop(age6th_text, _begin=100, _close=120)
    age7th_idea = ideaunit_shop(age7th_text, _begin=120, _close=140)
    sue_agenda.add_idea(age1st_idea, parent_road=time_road)
    sue_agenda.add_idea(age2nd_idea, parent_road=time_road)
    sue_agenda.add_idea(age3rd_idea, parent_road=time_road)
    sue_agenda.add_idea(age4th_idea, parent_road=time_road)
    sue_agenda.add_idea(age5th_idea, parent_road=time_road)
    sue_agenda.add_idea(age6th_idea, parent_road=time_road)
    sue_agenda.add_idea(age7th_idea, parent_road=time_road)

    a2_road = sue_agenda.make_road(time_road, age2nd_text)
    a2e1st_text = "a1_era1st"
    a2e2nd_text = "a1_era2nd"
    a2e3rd_text = "a1_era3rd"
    a2e4th_text = "a1_era4th"
    a2e1st_idea = ideaunit_shop(a2e1st_text, _begin=20, _close=30)
    a2e2nd_idea = ideaunit_shop(a2e2nd_text, _begin=30, _close=34)
    a2e3rd_idea = ideaunit_shop(a2e3rd_text, _begin=34, _close=38)
    a2e4th_idea = ideaunit_shop(a2e4th_text, _begin=38, _close=40)
    sue_agenda.add_idea(a2e1st_idea, parent_road=a2_road)
    sue_agenda.add_idea(a2e2nd_idea, parent_road=a2_road)
    sue_agenda.add_idea(a2e3rd_idea, parent_road=a2_road)
    sue_agenda.add_idea(a2e4th_idea, parent_road=a2_road)

    a3_road = sue_agenda.make_road(time_road, age3rd_text)
    a3e1st_text = "a3_era1st"
    a3e2nd_text = "a3_era2nd"
    a3e3rd_text = "a3_era3rd"
    a3e4th_text = "a3_era4th"
    a3e1st_idea = ideaunit_shop(a3e1st_text, _begin=40, _close=45)
    a3e2nd_idea = ideaunit_shop(a3e2nd_text, _begin=45, _close=50)
    a3e3rd_idea = ideaunit_shop(a3e3rd_text, _begin=55, _close=58)
    a3e4th_idea = ideaunit_shop(a3e4th_text, _begin=58, _close=60)
    sue_agenda.add_idea(a3e1st_idea, parent_road=a3_road)
    sue_agenda.add_idea(a3e2nd_idea, parent_road=a3_road)
    sue_agenda.add_idea(a3e3rd_idea, parent_road=a3_road)
    sue_agenda.add_idea(a3e4th_idea, parent_road=a3_road)

    # set for instant moment in 3rd age
    sue_agenda.set_belief(base=time_road, pick=time_road, open=35, nigh=55)
    lemma_dict = sue_agenda._get_lemma_beliefunits()
    assert len(lemma_dict) == 15
    a2e1st_lemma = lemma_dict[sue_agenda.make_road(a2_road, a2e1st_text)]
    a2e2nd_lemma = lemma_dict[sue_agenda.make_road(a2_road, a2e2nd_text)]
    a2e3rd_lemma = lemma_dict[sue_agenda.make_road(a2_road, a2e3rd_text)]
    a2e4th_lemma = lemma_dict[sue_agenda.make_road(a2_road, a2e4th_text)]
    a3e1st_lemma = lemma_dict[sue_agenda.make_road(a3_road, a3e1st_text)]
    a3e2nd_lemma = lemma_dict[sue_agenda.make_road(a3_road, a3e2nd_text)]
    a3e3rd_lemma = lemma_dict[sue_agenda.make_road(a3_road, a3e3rd_text)]
    a3e4th_lemma = lemma_dict[sue_agenda.make_road(a3_road, a3e4th_text)]
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


def test_create_lemma_beliefs_CorrectlyCreates1stLevelLemmaBelief_Scenario4():
    sue_agenda = agendaunit_shop("Sue")
    arsub1 = "descending_subsecction1"
    arsub1_idea = ideaunit_shop(arsub1, _begin=0, _close=140)
    as1_road = sue_agenda.make_l1_road(arsub1)
    sue_agenda.add_l1_idea(arsub1_idea)
    # range-root idea has range_source_road
    time_text = "time"
    time_idea = ideaunit_shop(
        time_text, _begin=0, _close=140, _range_source_road=as1_road
    )
    sue_agenda.add_l1_idea(time_idea)

    arsub2 = "descending_subsecction2"
    arsub2_idea = ideaunit_shop(arsub2, _begin=0, _close=20)
    as2_road = sue_agenda.make_l1_road(arsub2)
    sue_agenda.add_l1_idea(arsub2_idea)

    # non-range-root child idea has range_source_road
    time_road = sue_agenda.make_l1_road(time_text)
    age1st = "age1st"
    age1st_idea = ideaunit_shop(
        age1st, _begin=0, _close=20, _range_source_road=as2_road
    )
    sue_agenda.add_idea(age1st_idea, parent_road=time_road)

    # set for instant moment in 3rd age
    sue_agenda.set_belief(base=time_road, pick=time_road, open=35, nigh=55)
    lemma_dict = sue_agenda._get_lemma_beliefunits()
    assert len(lemma_dict) == 3
    a1_lemma = lemma_dict[sue_agenda.make_road(time_road, age1st)]
    as1_lemma = lemma_dict[as1_road]
    as2_lemma = lemma_dict[as2_road]
    assert a1_lemma.open is None
    assert as1_lemma.open == 35
    assert as2_lemma.open is None
    assert a1_lemma.nigh is None
    assert as1_lemma.nigh == 55
    assert as2_lemma.nigh is None


def test_create_lemma_beliefs_CorrectlyCreatesNthLevelLemmaBelief_Scenario4_1():
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")
    timetech_road = sue_agenda.make_road(time_road, "tech")
    sue_agenda.set_belief(jajatime_road, jajatime_road, open=1500, nigh=1500)
    lhu = sue_agenda._get_lemma_beliefunits()

    assert lhu[sue_agenda.make_road(jajatime_road, "400 year pattern")].open == 1500
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year pattern")].nigh == 1500
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].open > 0
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].open < 1
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].nigh > 0
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].nigh < 1
    assert lhu[sue_agenda.make_road(jajatime_road, "days")].open >= 1
    assert lhu[sue_agenda.make_road(jajatime_road, "days")].open <= 2
    assert lhu[sue_agenda.make_road(jajatime_road, "days")].nigh >= 1
    assert lhu[sue_agenda.make_road(jajatime_road, "days")].nigh <= 2
    assert lhu[sue_agenda.make_road(jajatime_road, "day")].open == 60
    assert lhu[sue_agenda.make_road(jajatime_road, "day")].nigh == 60
    assert lhu[sue_agenda.make_road(jajatime_road, "week")].open == 1500
    assert int(lhu[sue_agenda.make_road(jajatime_road, "week")].nigh) == 1500
    assert lhu[sue_agenda.make_road(timetech_road, "week")].open == 1500
    assert int(lhu[sue_agenda.make_road(timetech_road, "week")].nigh) == 1500


def test_create_lemma_beliefs_CorrectlyCreatesNthLevelLemmaBelief_Scenario5():
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    timetech_road = sue_agenda.make_road(time_road, "tech")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")
    sue_agenda.set_belief(jajatime_road, jajatime_road, 1500, nigh=1063954002)
    lhu = sue_agenda._get_lemma_beliefunits()

    assert lhu[sue_agenda.make_road(jajatime_road, "400 year pattern")].open == 0
    assert (
        lhu[sue_agenda.make_road(jajatime_road, "400 year pattern")].nigh == 210379680
    )
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].open > 0
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].open < 1
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].nigh > 5
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].nigh < 6
    lemma_days = lhu[sue_agenda.make_road(jajatime_road, "days")]
    assert int(lemma_days.open) == 1  # 0 / 1440
    assert int(lemma_days.nigh) == 738856  # 1063953183 / 1440
    lemma_day = lhu[sue_agenda.make_road(jajatime_road, "day")]
    assert lemma_day.open == 0  # 0 / 1440
    assert lemma_day.nigh == 1440  # 1362  # 1063953183 / 1440
    lemma_jajatime_week = lhu[sue_agenda.make_road(jajatime_road, "week")]
    assert lemma_jajatime_week.open == 0  # 0 / 1440
    assert int(lemma_jajatime_week.nigh) == 10080  # 1063953183 / 1440
    lemma_timetech_week = lhu[sue_agenda.make_road(jajatime_road, "week")]
    assert lemma_timetech_week.open == 0  # 0 / 1440
    assert int(lemma_timetech_week.nigh) == 10080  # 1063953183 / 1440


def test_create_lemma_beliefs_CorrectlyCreatesNthLevelLemmaBelief_Scenario6():
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")
    sue_agenda.set_belief(jajatime_road, jajatime_road, 1063954000, nigh=1063954002)
    lhu = sue_agenda._get_lemma_beliefunits()

    assert (
        lhu[sue_agenda.make_road(jajatime_road, "400 year pattern")].open == 12055600.0
    )
    assert (
        lhu[sue_agenda.make_road(jajatime_road, "400 year pattern")].nigh == 12055602.0
    )
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].open > 5
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].open < 6
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].nigh > 5
    assert lhu[sue_agenda.make_road(jajatime_road, "400 year patterns")].nigh < 6
    lemma_days = lhu[sue_agenda.make_road(jajatime_road, "days")]
    assert int(lemma_days.open) == 738856  # 1063954000 / 1440
    assert int(lemma_days.nigh) == 738856  # 1063954000 / 1440
    lemma_day = lhu[sue_agenda.make_road(jajatime_road, "day")]
    assert lemma_day.open == 1360  # 0 / 1440
    assert int(lemma_day.nigh) == 1362  # 1063953183 / 1440


def test_create_lemma_beliefs_CorrectlyCreatesNthLevelLemmaBelief_Scenario7():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    timetech_road = sue_agenda.make_road(time_road, "tech")
    techweek_road = sue_agenda.make_road(timetech_road, "week")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")

    # WHEN given a minute range that should be Thursday to Monday midnight
    sue_agenda.set_belief(jajatime_road, jajatime_road, 1063951200, nigh=1063956960)
    lhu = sue_agenda._get_lemma_beliefunits()

    # THEN
    week_open = lhu[sue_agenda.make_road(jajatime_road, "week")].open
    week_nigh = lhu[sue_agenda.make_road(jajatime_road, "week")].nigh
    week_text = "week"
    print(
        f"for {sue_agenda.make_road(jajatime_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[sue_agenda.make_road(jajatime_road, "week")].open == 7200
    assert lhu[sue_agenda.make_road(jajatime_road, "week")].nigh == 2880

    week_open = lhu[sue_agenda.make_road(timetech_road, "week")].open
    week_nigh = lhu[sue_agenda.make_road(timetech_road, "week")].nigh
    print(
        f"for {sue_agenda.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[sue_agenda.make_road(timetech_road, "week")].open == 7200
    assert lhu[sue_agenda.make_road(timetech_road, "week")].nigh == 2880
    print(f"{techweek_road=}")
    print(lhu[techweek_road])
    print(lhu[sue_agenda.make_road(techweek_road, "Thursday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Friday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Saturday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Sunday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Monday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Tuesday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Wednesday")])


def test_create_lemma_beliefs_CorrectlyCreatesNthLevelLemmaBelief_Scenario8():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_time_hreg_ideas(c400_count=7)
    time_road = sue_agenda.make_l1_road("time")
    timetech_road = sue_agenda.make_road(time_road, "tech")
    techweek_road = sue_agenda.make_road(timetech_road, "week")
    jajatime_road = sue_agenda.make_road(time_road, "jajatime")

    # WHEN given a minute range that should be Thursday to Monday midnight
    sue_agenda.set_belief(jajatime_road, jajatime_road, 1063951200, nigh=1063951200)
    lhu = sue_agenda._get_lemma_beliefunits()

    # THEN
    week_open = lhu[techweek_road].open
    week_nigh = lhu[techweek_road].nigh
    print(f"for {techweek_road}: {week_open=} {week_nigh=}")
    assert lhu[techweek_road].open == 7200
    assert lhu[techweek_road].nigh == 7200

    week_open = lhu[sue_agenda.make_road(timetech_road, "week")].open
    week_nigh = lhu[sue_agenda.make_road(timetech_road, "week")].nigh
    week_text = "week"
    print(
        f"for {sue_agenda.make_road(timetech_road,week_text)}: {week_open=} {week_nigh=}"
    )
    assert lhu[sue_agenda.make_road(timetech_road, "week")].open == 7200
    assert lhu[sue_agenda.make_road(timetech_road, "week")].nigh == 7200
    print(lhu[techweek_road])
    print(lhu[sue_agenda.make_road(techweek_road, "Thursday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Friday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Saturday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Sunday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Monday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Tuesday")])
    print(lhu[sue_agenda.make_road(techweek_road, "Wednesday")])


def test_AgendaUnit_set_belief_create_missing_ideas_CreatesBaseAndBelief():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    trouble_text = ""
    trouble_road = sue_agenda.make_l1_road(trouble_text)
    climate_text = "climate"
    climate_road = sue_agenda.make_road(trouble_road, climate_text)
    assert sue_agenda._idearoot.get_kid(trouble_text) is None

    # WHEN
    sue_agenda.set_belief(trouble_road, climate_road, create_missing_ideas=True)

    # THEN
    assert sue_agenda._idearoot.get_kid(trouble_text) != None
    assert sue_agenda.get_idea_obj(trouble_road) != None
    assert sue_agenda.get_idea_obj(climate_road) != None


def test_AgendaUnit_get_beliefunits_base_and_belief_list_ReturnsListOfBeliefUnits():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    trouble_text = "troubles"
    trouble_road = sue_agenda.make_l1_road(trouble_text)
    climate_text = "climate"
    climate_road = sue_agenda.make_road(trouble_road, climate_text)
    sue_agenda.set_belief(trouble_road, climate_road, create_missing_ideas=True)

    weather_text = "weather"
    weather_road = sue_agenda.make_l1_road(weather_text)
    windy_text = "windy"
    windy_road = sue_agenda.make_road(weather_road, windy_text)
    sue_agenda.set_belief(weather_road, windy_road, create_missing_ideas=True)
    hot_text = "hot"
    hot_road = sue_agenda.make_road(weather_road, hot_text)
    sue_agenda.set_belief(base=weather_road, pick=hot_road, create_missing_ideas=True)
    cold_text = "cold"
    cold_road = sue_agenda.make_road(weather_road, cold_text)
    sue_agenda.set_belief(weather_road, cold_road, create_missing_ideas=True)

    games_text = "games"
    games_road = sue_agenda.make_l1_road(games_text)
    football_text = "football"
    football_road = sue_agenda.make_road(weather_road, football_text)
    sue_agenda.set_belief(games_road, football_road, create_missing_ideas=True)

    # WHEN
    beliefunit_list_x = sue_agenda.get_beliefunits_base_and_belief_list()

    # THEN
    assert beliefunit_list_x[0][0] == ""
    assert beliefunit_list_x[1][0] == games_road
    assert beliefunit_list_x[1][1] == football_road
    assert beliefunit_list_x[2][0] == trouble_road
    assert beliefunit_list_x[2][1] == climate_road
    assert beliefunit_list_x[3][0] == weather_road
    assert beliefunit_list_x[3][1] == cold_road
    assert len(beliefunit_list_x) == 4
