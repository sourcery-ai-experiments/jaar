from src.agent.required import acptfactunit_shop, acptfactunit_shop, acptfactheir_shop
from src.agent.tool import ToolKid, Road
from src.agent.examples.example_agents import (
    get_agent_with_4_levels as examples_get_agent_with_4_levels,
)
from src.agent.agent import AgentUnit
from pytest import raises as pytest_raises


def test_agent_acptfact_exists():
    agent_x = examples_get_agent_with_4_levels()
    sunday_road = Road(f"{agent_x._desc},weekdays,Sunday")
    weekday_road = Road(f"{agent_x._desc},weekdays")
    sunday_lw_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_lw_acptfact)
    agent_x._toolroot._acptfactunits = {sunday_lw_acptfact.base: sunday_lw_acptfact}
    assert agent_x._toolroot._acptfactunits != None
    agent_x._toolroot._acptfactunits = None
    assert agent_x._toolroot._acptfactunits is None
    agent_x.set_acptfact(base=weekday_road, pick=sunday_road)
    assert agent_x._toolroot._acptfactunits == {
        sunday_lw_acptfact.base: sunday_lw_acptfact
    }

    agent_x._toolroot._acptfactunits = None
    assert agent_x._toolroot._acptfactunits is None
    usa_week_road = Road(f"{agent_x._desc},nation-state")
    usa_week_unit = acptfactunit_shop(
        base=usa_week_road, pick=usa_week_road, open=608, nigh=610
    )
    agent_x._toolroot._acptfactunits = {usa_week_unit.base: usa_week_unit}

    agent_x._toolroot._acptfactunits = None
    assert agent_x._toolroot._acptfactunits is None
    agent_x.set_acptfact(base=usa_week_road, pick=usa_week_road, open=608, nigh=610)
    assert agent_x._toolroot._acptfactunits != None
    assert agent_x._toolroot._acptfactunits == {usa_week_unit.base: usa_week_unit}


def test_agent_acptfact_create():
    agent_x = examples_get_agent_with_4_levels()
    sunday_road = Road(f"{agent_x._desc},weekdays,Sunday")
    weekday_road = Road(f"{agent_x._desc},weekdays")
    agent_x.set_acptfact(base=weekday_road, pick=sunday_road)
    sunday_lw_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    assert agent_x._toolroot._acptfactunits == {
        sunday_lw_acptfact.base: sunday_lw_acptfact
    }


def test_set_acptfact_FailsToCreateWhenBaseAndAcptFactAreDifferenctAndAcptFactToolIsNotRangeRoot():
    # Given
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    time_x = "time_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=time_x, _begin=0, _close=140), walk=src_text)
    t_x_road = Road(f"{src_text},{time_x}")
    age1st = "age1st"
    lw_x.add_tool(tool_kid=ToolKid(_desc=age1st, _begin=0, _close=20), walk=t_x_road)
    a1_road = Road(f"{t_x_road},{age1st}")
    a1e1st = "a1_era1st"
    lw_x.add_tool(tool_kid=ToolKid(_desc=a1e1st, _begin=20, _close=30), walk=a1_road)
    a1e1_road = Road(f"{a1_road},{a1e1st}")
    assert lw_x._toolroot._acptfactunits in (None, {})

    # When/Then
    with pytest_raises(Exception) as excinfo:
        lw_x.set_acptfact(base=a1e1_road, pick=a1e1_road, open=20, nigh=23)
    assert (
        str(excinfo.value)
        == f"Non range-root acptfact:{a1e1_road} can only be set by range-root acptfact"
    )


def test_agent_acptfact_create():
    # Given
    agent_x = examples_get_agent_with_4_levels()
    sunday_road = Road(f"{agent_x._desc},weekdays,Sunday")
    weekday_road = Road(f"{agent_x._desc},weekdays")
    agent_x.set_acptfact(base=weekday_road, pick=sunday_road)
    sunday_lw_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    assert agent_x._toolroot._acptfactunits == {
        sunday_lw_acptfact.base: sunday_lw_acptfact
    }

    # When
    agent_x.del_acptfact(base=weekday_road)

    # Then
    assert agent_x._toolroot._acptfactunits == {}


def test_agent_get_tool_list_AcptFactHeirsCorrectlyInherited():
    # GIVEN
    src_text = "src"
    agent_x = AgentUnit(_desc=src_text)
    swim_text = "swim"
    swim_road = Road(f"{src_text},{swim_text}")
    agent_x.add_tool(tool_kid=ToolKid(_desc=swim_text), walk=src_text)
    fast_text = "fast"
    slow_text = "slow"
    fast_road = Road(f"{swim_road},{fast_text}")
    slow_road = Road(f"{swim_road},{slow_text}")
    agent_x.add_tool(tool_kid=ToolKid(_desc=fast_text), walk=swim_road)
    agent_x.add_tool(tool_kid=ToolKid(_desc=slow_text), walk=swim_road)

    earth_text = "earth"
    earth_road = Road(f"{src_text},{earth_text}")
    agent_x.add_tool(tool_kid=ToolKid(_desc=earth_text), walk=src_text)

    swim_tool = agent_x.get_tool_kid(road=swim_road)
    fast_tool = agent_x.get_tool_kid(road=fast_road)
    slow_tool = agent_x.get_tool_kid(road=slow_road)

    assert swim_tool._acptfactheirs is None
    assert fast_tool._acptfactheirs is None
    assert slow_tool._acptfactheirs is None

    # WHEN
    agent_x.set_acptfact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)
    acptfactheir_set_range = acptfactheir_shop(earth_road, earth_road, 1.0, 5.0)
    acptfactheirs_set_range = {acptfactheir_set_range.base: acptfactheir_set_range}
    acptfact_none_range = acptfactheir_shop(earth_road, earth_road, None, None)
    acptfacts_none_range = {acptfact_none_range.base: acptfact_none_range}

    # THEN
    assert swim_tool._acptfactheirs != None
    assert fast_tool._acptfactheirs != None
    assert slow_tool._acptfactheirs != None
    assert swim_tool._acptfactheirs == acptfactheirs_set_range
    assert fast_tool._acptfactheirs == acptfactheirs_set_range
    assert slow_tool._acptfactheirs == acptfactheirs_set_range
    print(f"{swim_tool._acptfactheirs=}")
    assert len(swim_tool._acptfactheirs) == 1

    # WHEN
    swim_tool._acptfactheirs.get(earth_road).set_range_null()

    # THEN
    assert swim_tool._acptfactheirs == acptfacts_none_range
    assert fast_tool._acptfactheirs == acptfactheirs_set_range
    assert slow_tool._acptfactheirs == acptfactheirs_set_range

    acptfact_x1 = swim_tool._acptfactheirs.get(earth_road)
    acptfact_x1.set_range_null()
    print(type(acptfact_x1))
    assert str(type(acptfact_x1)).find(".required.AcptFactHeir'>")


def test_agent_get_tool_list_AcptFactUnitCorrectlyTransformsacptfactheir_shop():
    # GIVEN
    src_text = "src"
    agent_x = AgentUnit(_desc=src_text)
    swim_text = "swim"
    swim_road = f"{src_text},{swim_text}"
    agent_x.add_tool(tool_kid=ToolKid(_desc=swim_text), walk=src_text)
    swim_tool = agent_x.get_tool_kid(road=swim_road)

    fast_text = "fast"
    slow_text = "slow"
    agent_x.add_tool(tool_kid=ToolKid(_desc=fast_text), walk=swim_road)
    agent_x.add_tool(tool_kid=ToolKid(_desc=slow_text), walk=swim_road)

    earth_text = "earth"
    earth_road = Road(f"{src_text},{earth_text}")
    agent_x.add_tool(tool_kid=ToolKid(_desc=earth_text), walk=src_text)

    assert swim_tool._acptfactheirs is None

    # WHEN
    agent_x.set_acptfact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)

    # THEN
    first_earthheir = acptfactheir_shop(
        base=earth_road, pick=earth_road, open=1.0, nigh=5.0
    )
    first_earthdict = {first_earthheir.base: first_earthheir}
    assert swim_tool._acptfactheirs == first_earthdict

    # WHEN
    # earth_curb = acptfactunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    # swim_y.set_acptfactunit(acptfactunit=earth_curb) Not sure what this is for. Testing how "set_acptfactunit" works?
    agent_x.set_acptfact(base=earth_road, pick=earth_road, open=3.0, nigh=5.0)

    # THEN
    after_earthheir = acptfactheir_shop(
        base=earth_road, pick=earth_road, open=3.0, nigh=5.0
    )
    after_earthdict = {after_earthheir.base: after_earthheir}
    assert swim_tool._acptfactheirs == after_earthdict


def test_agent_get_tool_list_AcptFactHeirCorrectlyDeletesAcptFactUnit():
    # GIVEN
    src_text = "src"
    agent_x = AgentUnit(_desc=src_text)
    swim_text = "swim"
    swim_road = Road(f"{src_text},{swim_text}")
    agent_x.add_tool(tool_kid=ToolKid(_desc=swim_text), walk=src_text)
    fast_text = "fast"
    slow_text = "slow"
    fast_road = Road(f"{swim_road},{fast_text}")
    slow_road = Road(f"{swim_road},{slow_text}")
    agent_x.add_tool(tool_kid=ToolKid(_desc=fast_text), walk=swim_road)
    agent_x.add_tool(tool_kid=ToolKid(_desc=slow_text), walk=swim_road)

    earth_text = "earth"
    earth_road = Road(f"{src_text},{earth_text}")
    agent_x.add_tool(tool_kid=ToolKid(_desc=earth_text), walk=src_text)

    swim_tool = agent_x.get_tool_kid(road=swim_road)

    first_earthheir = acptfactheir_shop(
        base=earth_road, pick=earth_road, open=200.0, nigh=500.0
    )
    first_earthdict = {first_earthheir.base: first_earthheir}

    assert swim_tool._acptfactheirs is None

    # WHEN
    agent_x.set_acptfact(base=earth_road, pick=earth_road, open=200.0, nigh=500.0)

    # THEN
    assert swim_tool._acptfactheirs == first_earthdict

    earth_curb = acptfactunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    swim_tool.set_acptfactunit(acptfactunit=earth_curb)
    agent_x.set_agent_metrics()
    assert swim_tool._acptfactheirs == first_earthdict
    assert swim_tool._acptfactunits == {}


def test_get_ranged_acptfacts():
    # Given a single ranged acptfact
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    time_x = "time_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=time_x, _begin=0, _close=140), walk=src_text)

    clean = "clean"
    lw_x.add_tool(tool_kid=ToolKid(_desc=clean, promise=True), walk=src_text)
    c_road = f"{src_text},{clean}"
    t_x_road = f"{src_text},{time_x}"
    # lw_x.edit_tool_attr(road=c_road, required_base=t_x_road, required_sufffact=t_x_road, required_sufffact_open=5, required_sufffact_nigh=10)

    lw_x.set_acptfact(base=t_x_road, pick=t_x_road, open=5, nigh=10)
    print(f"Given a single ranged acptfact {lw_x._toolroot._acptfactunits=}")
    assert len(lw_x._toolroot._acptfactunits) == 1

    # When/Then
    assert len(lw_x._get_rangeroot_acptfactunits()) == 1

    # When one ranged acptfact added
    place = "place_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=place, _begin=600, _close=800), walk=src_text)
    p_road = f"{src_text},{place}"
    lw_x.set_acptfact(base=p_road, pick=p_road, open=5, nigh=10)
    print(f"When one ranged acptfact added {lw_x._toolroot._acptfactunits=}")
    assert len(lw_x._toolroot._acptfactunits) == 2

    # Then
    assert len(lw_x._get_rangeroot_acptfactunits()) == 2

    # When one non-ranged_acptfact added
    mood = "mood_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=mood), walk=src_text)
    m_road = f"{src_text},{mood}"
    lw_x.set_acptfact(base=m_road, pick=m_road)
    print(f"When one non-ranged_acptfact added {lw_x._toolroot._acptfactunits=}")
    assert len(lw_x._toolroot._acptfactunits) == 3

    # Then
    assert len(lw_x._get_rangeroot_acptfactunits()) == 2


def test_get_roots_ranged_acptfacts():
    # Given a two ranged acptfacts where one is "range-root" get_root_ranged_acptfacts returns one "range-root" acptfact
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    time_x = "time_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=time_x, _begin=0, _close=140), walk=src_text)
    t_x_road = f"{src_text},{time_x}"
    mood_x = "mood_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=mood_x), walk=src_text)
    m_x_road = f"{src_text},{mood_x}"
    happy = "happy"
    sad = "Sad"
    lw_x.add_tool(tool_kid=ToolKid(_desc=happy), walk=m_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=sad), walk=m_x_road)
    lw_x.set_acptfact(base=t_x_road, pick=t_x_road, open=5, nigh=10)
    lw_x.set_acptfact(base=m_x_road, pick=f"{m_x_road},{happy}")
    print(
        f"Given a root ranged acptfact and non-range acptfact:\n{lw_x._toolroot._acptfactunits=}"
    )
    assert len(lw_x._toolroot._acptfactunits) == 2

    # When/Then
    assert len(lw_x._get_rangeroot_acptfactunits()) == 1
    assert lw_x._get_rangeroot_acptfactunits()[0].base == t_x_road

    # a acptfact who's tool range is defined by numeric_root is not "rangeroot"
    mirrow_x = "mirrow_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=mirrow_x, _numeric_road=time_x), walk=src_text)
    m_x_road = f"{src_text},{mirrow_x}"
    lw_x.set_acptfact(base=m_x_road, pick=t_x_road, open=5, nigh=10)
    assert len(lw_x._toolroot._acptfactunits) == 3

    # When/Then
    assert len(lw_x._get_rangeroot_acptfactunits()) == 1
    assert lw_x._get_rangeroot_acptfactunits()[0].base == t_x_road


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario1():
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    # # the action
    # clean = "clean"
    # lw_x.add_tool(tool_kid=ToolKid(_desc=clean, promise=True), walk=src_text)

    time_x = "time_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=time_x, _begin=0, _close=140), walk=src_text)
    t_x_road = f"{src_text},{time_x}"
    age1st = "age1st"
    age2nd = "age2nd"
    age3rd = "age3rd"
    age4th = "age4th"
    age5th = "age5th"
    age6th = "age6th"
    age7th = "age7th"
    lw_x.add_tool(tool_kid=ToolKid(_desc=age1st, _begin=0, _close=20), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age2nd, _begin=20, _close=40), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age3rd, _begin=40, _close=60), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age4th, _begin=60, _close=80), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age5th, _begin=80, _close=100), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age6th, _begin=100, _close=120), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age7th, _begin=120, _close=140), walk=t_x_road)

    # set for instant moment in 3rd age
    lw_x.set_acptfact(base=time_x, pick=time_x, open=45, nigh=45)
    lemma_dict = lw_x._get_lemma_acptfactunits()
    print(f"{len(lemma_dict)=}")
    print(f"{lemma_dict=}")
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[f"{t_x_road},{age1st}"]
    age2nd_lemma = lemma_dict[f"{t_x_road},{age2nd}"]
    age3rd_lemma = lemma_dict[f"{t_x_road},{age3rd}"]
    age4th_lemma = lemma_dict[f"{t_x_road},{age4th}"]
    age5th_lemma = lemma_dict[f"{t_x_road},{age5th}"]
    age6th_lemma = lemma_dict[f"{t_x_road},{age6th}"]
    age7th_lemma = lemma_dict[f"{t_x_road},{age7th}"]
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
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    # # the action
    # clean = "clean"
    # lw_x.add_tool(tool_kid=ToolKid(_desc=clean, promise=True), walk=src_text)

    time_x = "time_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=time_x, _begin=0, _close=140), walk=src_text)
    t_x_road = f"{src_text},{time_x}"
    age1st = "age1st"
    age2nd = "age2nd"
    age3rd = "age3rd"
    age4th = "age4th"
    age5th = "age5th"
    age6th = "age6th"
    age7th = "age7th"
    lw_x.add_tool(tool_kid=ToolKid(_desc=age1st, _begin=0, _close=20), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age2nd, _begin=20, _close=40), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age3rd, _begin=40, _close=60), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age4th, _begin=60, _close=80), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age5th, _begin=80, _close=100), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age6th, _begin=100, _close=120), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age7th, _begin=120, _close=140), walk=t_x_road)

    # set for instant moment in 3rd age
    lw_x.set_acptfact(base=time_x, pick=time_x, open=35, nigh=65)
    lemma_dict = lw_x._get_lemma_acptfactunits()
    assert len(lemma_dict) == 7
    age1st_lemma = lemma_dict[f"{t_x_road},{age1st}"]
    age2nd_lemma = lemma_dict[f"{t_x_road},{age2nd}"]
    age3rd_lemma = lemma_dict[f"{t_x_road},{age3rd}"]
    age4th_lemma = lemma_dict[f"{t_x_road},{age4th}"]
    age5th_lemma = lemma_dict[f"{t_x_road},{age5th}"]
    age6th_lemma = lemma_dict[f"{t_x_road},{age6th}"]
    age7th_lemma = lemma_dict[f"{t_x_road},{age7th}"]
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
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    # # the action
    # clean = "clean"
    # lw_x.add_tool(tool_kid=ToolKid(_desc=clean, promise=True), walk=src_text)

    time_x = "time_x"
    lw_x.add_tool(tool_kid=ToolKid(_desc=time_x, _begin=0, _close=140), walk=src_text)
    t_x_road = f"{src_text},{time_x}"
    age1st = "age1st"
    age2nd = "age2nd"
    age3rd = "age3rd"
    age4th = "age4th"
    age5th = "age5th"
    age6th = "age6th"
    age7th = "age7th"
    lw_x.add_tool(tool_kid=ToolKid(_desc=age1st, _begin=0, _close=20), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age2nd, _begin=20, _close=40), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age3rd, _begin=40, _close=60), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age4th, _begin=60, _close=80), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age5th, _begin=80, _close=100), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age6th, _begin=100, _close=120), walk=t_x_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=age7th, _begin=120, _close=140), walk=t_x_road)

    a2_road = f"{t_x_road},{age2nd}"
    a2e1st = "a1_era1st"
    a2e2nd = "a1_era2nd"
    a2e3rd = "a1_era3rd"
    a2e4th = "a1_era4th"
    lw_x.add_tool(tool_kid=ToolKid(_desc=a2e1st, _begin=20, _close=30), walk=a2_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=a2e2nd, _begin=30, _close=34), walk=a2_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=a2e3rd, _begin=34, _close=38), walk=a2_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=a2e4th, _begin=38, _close=40), walk=a2_road)

    a3_road = f"{t_x_road},{age3rd}"
    a3e1st = "a3_era1st"
    a3e2nd = "a3_era2nd"
    a3e3rd = "a3_era3rd"
    a3e4th = "a3_era4th"
    lw_x.add_tool(tool_kid=ToolKid(_desc=a3e1st, _begin=40, _close=45), walk=a3_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=a3e2nd, _begin=45, _close=50), walk=a3_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=a3e3rd, _begin=55, _close=58), walk=a3_road)
    lw_x.add_tool(tool_kid=ToolKid(_desc=a3e4th, _begin=58, _close=60), walk=a3_road)

    # set for instant moment in 3rd age
    lw_x.set_acptfact(base=time_x, pick=time_x, open=35, nigh=55)
    lemma_dict = lw_x._get_lemma_acptfactunits()
    assert len(lemma_dict) == 15
    a2e1st_lemma = lemma_dict[f"{a2_road},{a2e1st}"]
    a2e2nd_lemma = lemma_dict[f"{a2_road},{a2e2nd}"]
    a2e3rd_lemma = lemma_dict[f"{a2_road},{a2e3rd}"]
    a2e4th_lemma = lemma_dict[f"{a2_road},{a2e4th}"]
    a3e1st_lemma = lemma_dict[f"{a3_road},{a3e1st}"]
    a3e2nd_lemma = lemma_dict[f"{a3_road},{a3e2nd}"]
    a3e3rd_lemma = lemma_dict[f"{a3_road},{a3e3rd}"]
    a3e4th_lemma = lemma_dict[f"{a3_road},{a3e4th}"]
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
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    time_x = "time_x"
    arsub1 = "arbitary_subsection1"
    as1_road = f"{src_text},{arsub1}"
    lw_x.add_tool(tool_kid=ToolKid(_desc=arsub1, _begin=0, _close=140), walk=src_text)
    # range-root tool has special_road
    lw_x.add_tool(
        tool_kid=ToolKid(_desc=time_x, _begin=0, _close=140, _special_road=as1_road),
        walk=src_text,
    )

    arsub2 = "arbitary_subsection2"
    as2_road = f"{src_text},{arsub2}"
    lw_x.add_tool(tool_kid=ToolKid(_desc=arsub2, _begin=0, _close=20), walk=src_text)

    # non-range-root child tool has special_road
    t_x_road = f"{src_text},{time_x}"
    age1st = "age1st"
    lw_x.add_tool(
        tool_kid=ToolKid(_desc=age1st, _begin=0, _close=20, _special_road=as2_road),
        walk=t_x_road,
    )

    # set for instant moment in 3rd age
    lw_x.set_acptfact(base=time_x, pick=time_x, open=35, nigh=55)
    lemma_dict = lw_x._get_lemma_acptfactunits()
    assert len(lemma_dict) == 3
    a1_lemma = lemma_dict[f"{t_x_road},{age1st}"]
    as1_lemma = lemma_dict[f"{as1_road}"]
    as2_lemma = lemma_dict[f"{as2_road}"]
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
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    lw_x.set_time_hreg_tools(c400_count=7)
    jajatime_road = "src,time,jajatime"
    lw_x.set_acptfact(base=jajatime_road, pick=jajatime_road, open=1500, nigh=1500)
    lhu = lw_x._get_lemma_acptfactunits()

    assert lhu["src,time,jajatime,400 year cycle"].open == 1500
    assert lhu["src,time,jajatime,400 year cycle"].nigh == 1500
    assert lhu["src,time,jajatime,400 year cycles"].open > 0
    assert lhu["src,time,jajatime,400 year cycles"].open < 1
    assert lhu["src,time,jajatime,400 year cycles"].nigh > 0
    assert lhu["src,time,jajatime,400 year cycles"].nigh < 1
    assert lhu["src,time,jajatime,days"].open >= 1
    assert lhu["src,time,jajatime,days"].open <= 2
    assert lhu["src,time,jajatime,days"].nigh >= 1
    assert lhu["src,time,jajatime,days"].nigh <= 2
    assert lhu["src,time,jajatime,day"].open == 60
    assert lhu["src,time,jajatime,day"].nigh == 60
    assert lhu["src,time,jajatime,week"].open == 1500
    assert int(lhu["src,time,jajatime,week"].nigh) == 1500
    assert lhu["src,time,tech,week"].open == 1500
    assert int(lhu["src,time,tech,week"].nigh) == 1500


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario5():
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    lw_x.set_time_hreg_tools(c400_count=7)
    jajatime_road = "src,time,jajatime"
    lw_x.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1500, nigh=1063954002
    )
    lhu = lw_x._get_lemma_acptfactunits()

    assert lhu["src,time,jajatime,400 year cycle"].open == 0
    assert lhu["src,time,jajatime,400 year cycle"].nigh == 210379680
    assert lhu["src,time,jajatime,400 year cycles"].open > 0
    assert lhu["src,time,jajatime,400 year cycles"].open < 1
    assert lhu["src,time,jajatime,400 year cycles"].nigh > 5
    assert lhu["src,time,jajatime,400 year cycles"].nigh < 6
    assert int(lhu["src,time,jajatime,days"].open) == 1  # 0 / 1440
    assert int(lhu["src,time,jajatime,days"].nigh) == 738856  # 1063953183 / 1440
    assert lhu["src,time,jajatime,day"].open == 0  # 0 / 1440
    assert lhu["src,time,jajatime,day"].nigh == 1440  # 1362  # 1063953183 / 1440
    assert lhu["src,time,jajatime,week"].open == 0  # 0 / 1440
    assert int(lhu["src,time,jajatime,week"].nigh) == 10080  # 1063953183 / 1440
    assert lhu["src,time,tech,week"].open == 0  # 0 / 1440
    assert int(lhu["src,time,tech,week"].nigh) == 10080  # 1063953183 / 1440


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario6():
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    lw_x.set_time_hreg_tools(c400_count=7)
    jajatime_road = "src,time,jajatime"
    lw_x.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063954000, nigh=1063954002
    )
    lhu = lw_x._get_lemma_acptfactunits()

    assert lhu["src,time,jajatime,400 year cycle"].open == 12055600.0
    assert lhu["src,time,jajatime,400 year cycle"].nigh == 12055602.0
    assert lhu["src,time,jajatime,400 year cycles"].open > 5
    assert lhu["src,time,jajatime,400 year cycles"].open < 6
    assert lhu["src,time,jajatime,400 year cycles"].nigh > 5
    assert lhu["src,time,jajatime,400 year cycles"].nigh < 6
    assert int(lhu["src,time,jajatime,days"].open) == 738856  # 1063954000 / 1440
    assert int(lhu["src,time,jajatime,days"].nigh) == 738856  # 1063954000 / 1440
    assert lhu["src,time,jajatime,day"].open == 1360  # 0 / 1440
    assert int(lhu["src,time,jajatime,day"].nigh) == 1362  # 1063953183 / 1440


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario7():
    # Given
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    lw_x.set_time_hreg_tools(c400_count=7)
    jajatime_road = "src,time,jajatime"

    # When given a minute range that should be Thursday to Monday midnight
    lw_x.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063951200, nigh=1063956960
    )
    lhu = lw_x._get_lemma_acptfactunits()

    # Then
    week_open = lhu["src,time,jajatime,week"].open
    week_nigh = lhu["src,time,jajatime,week"].nigh
    print(f"for src,time,jajatime,week: {week_open=} {week_nigh=}")
    assert lhu["src,time,jajatime,week"].open == 7200
    assert lhu["src,time,jajatime,week"].nigh == 2880

    week_open = lhu["src,time,tech,week"].open
    week_nigh = lhu["src,time,tech,week"].nigh
    print(f"for src,time,tech,week: {week_open=} {week_nigh=}")
    assert lhu["src,time,tech,week"].open == 7200
    assert lhu["src,time,tech,week"].nigh == 2880
    print(lhu["src,time,tech,week"])
    print(lhu["src,time,tech,week,Thursday"])
    print(lhu["src,time,tech,week,Friday"])
    print(lhu["src,time,tech,week,Saturday"])
    print(lhu["src,time,tech,week,Sunday"])
    print(lhu["src,time,tech,week,Monday"])
    print(lhu["src,time,tech,week,Tuesday"])
    print(lhu["src,time,tech,week,Wednesday"])

    # assert lhu["src,time,tech,week,Thursday"].active == True
    # assert lhu["src,time,tech,week,Friday"].active == True
    # assert lhu["src,time,tech,week,Saturday"].active == True
    # assert lhu["src,time,tech,week,Sunday"].active == True
    # assert lhu["src,time,tech,week,Monday"].active == False
    # assert lhu["src,time,tech,week,Tuesday"].active == False
    # assert lhu["src,time,tech,week,Wednesday"].active == False


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario8():
    # Given
    src_text = "src"
    lw_x = AgentUnit(_desc=src_text)
    lw_x.set_time_hreg_tools(c400_count=7)
    jajatime_road = "src,time,jajatime"

    # When given a minute range that should be Thursday to Monday midnight
    lw_x.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063951200, nigh=1063951200
    )
    lhu = lw_x._get_lemma_acptfactunits()

    # Then
    week_open = lhu["src,time,jajatime,week"].open
    week_nigh = lhu["src,time,jajatime,week"].nigh
    print(f"for src,time,jajatime,week: {week_open=} {week_nigh=}")
    assert lhu["src,time,jajatime,week"].open == 7200
    assert lhu["src,time,jajatime,week"].nigh == 7200

    week_open = lhu["src,time,tech,week"].open
    week_nigh = lhu["src,time,tech,week"].nigh
    print(f"for src,time,tech,week: {week_open=} {week_nigh=}")
    assert lhu["src,time,tech,week"].open == 7200
    assert lhu["src,time,tech,week"].nigh == 7200
    print(lhu["src,time,tech,week"])
    print(lhu["src,time,tech,week,Thursday"])
    print(lhu["src,time,tech,week,Friday"])
    print(lhu["src,time,tech,week,Saturday"])
    print(lhu["src,time,tech,week,Sunday"])
    print(lhu["src,time,tech,week,Monday"])
    print(lhu["src,time,tech,week,Tuesday"])
    print(lhu["src,time,tech,week,Wednesday"])

    # assert lhu["src,time,tech,week,Thursday"].active == True
    # assert lhu["src,time,tech,week,Friday"].active == False
    # assert lhu["src,time,tech,week,Saturday"].active == False
    # assert lhu["src,time,tech,week,Sunday"].active == False
    # assert lhu["src,time,tech,week,Monday"].active == False
    # assert lhu["src,time,tech,week,Tuesday"].active == False
    # assert lhu["src,time,tech,week,Wednesday"].active == False


def test_agent_set_acptfact_create_missing_tools_CreatesBaseAndAcptFact():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx._toolroot.set_kids_empty_if_null()
    prob_text = "problems"
    prob_road = Road(f"{src_text},{prob_text}")
    climate_text = "climate"
    climate_road = Road(f"{src_text},{prob_text},{climate_text}")
    assert sx._toolroot._kids.get(prob_text) is None

    # WHEN
    sx.set_acptfact(base=prob_road, pick=climate_road, create_missing_tools=True)

    # THEN
    assert sx._toolroot._kids.get(prob_text) != None
    assert sx.get_tool_kid(road=prob_road) != None
    assert sx.get_tool_kid(road=climate_road) != None


def test_agent_get_acptfactunits_base_and_acptfact_list_CorrectlyReturnsListOfAcptFactUnits():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx._toolroot.set_kids_empty_if_null()

    prob_text = "problems"
    prob_road = Road(f"{src_text},{prob_text}")
    climate_text = "climate"
    climate_road = Road(f"{src_text},{prob_text},{climate_text}")
    sx.set_acptfact(base=prob_road, pick=climate_road, create_missing_tools=True)

    weather_text = "weather"
    weather_road = Road(f"{src_text},{weather_text}")
    windy_text = "windy"
    windy_road = Road(f"{src_text},{weather_text},{windy_text}")
    sx.set_acptfact(base=weather_road, pick=windy_road, create_missing_tools=True)
    hot_text = "hot"
    hot_road = Road(f"{src_text},{weather_text},{hot_text}")
    sx.set_acptfact(base=weather_road, pick=hot_road, create_missing_tools=True)
    cold_text = "cold"
    cold_road = Road(f"{src_text},{weather_text},{cold_text}")
    sx.set_acptfact(base=weather_road, pick=cold_road, create_missing_tools=True)

    games_text = "games"
    games_road = Road(f"{src_text},{games_text}")
    football_text = "football"
    football_road = Road(f"{src_text},{games_text},{football_text}")
    sx.set_acptfact(base=games_road, pick=football_road, create_missing_tools=True)

    # WHEN
    acptfactunit_list_x = sx.get_acptfactunits_base_and_acptfact_list()

    # THEN
    assert acptfactunit_list_x[0][0] == ""
    assert acptfactunit_list_x[1][0] == games_road
    assert acptfactunit_list_x[1][1] == football_road
    assert acptfactunit_list_x[2][0] == prob_road
    assert acptfactunit_list_x[2][1] == climate_road
    assert acptfactunit_list_x[3][0] == weather_road
    assert acptfactunit_list_x[3][1] == cold_road
    assert len(acptfactunit_list_x) == 4
