from src.contract.required_idea import (
    acptfactunit_shop,
    acptfactunit_shop,
    acptfactheir_shop,
)
from src.contract.idea import IdeaKid, Road
from src.contract.examples.example_contracts import (
    get_contract_with_4_levels as examples_get_contract_with_4_levels,
)
from src.contract.contract import ContractUnit
from pytest import raises as pytest_raises


def test_contract_acptfact_exists():
    sx = examples_get_contract_with_4_levels()
    weekday_road = Road(f"{sx._economy_tag},weekdays")
    sunday_road = Road(f"{sx._economy_tag},weekdays,Sunday")
    sunday_cx_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_cx_acptfact)
    sx._idearoot._acptfactunits = {sunday_cx_acptfact.base: sunday_cx_acptfact}
    assert sx._idearoot._acptfactunits != None
    sx._idearoot._acptfactunits = None
    assert sx._idearoot._acptfactunits is None
    sx.set_acptfact(base=weekday_road, pick=sunday_road)
    assert sx._idearoot._acptfactunits == {sunday_cx_acptfact.base: sunday_cx_acptfact}

    sx._idearoot._acptfactunits = None
    assert sx._idearoot._acptfactunits is None
    usa_week_road = Road(f"{sx._economy_tag},nation-state")
    usa_week_unit = acptfactunit_shop(
        base=usa_week_road, pick=usa_week_road, open=608, nigh=610
    )
    sx._idearoot._acptfactunits = {usa_week_unit.base: usa_week_unit}

    sx._idearoot._acptfactunits = None
    assert sx._idearoot._acptfactunits is None
    sx.set_acptfact(base=usa_week_road, pick=usa_week_road, open=608, nigh=610)
    assert sx._idearoot._acptfactunits != None
    assert sx._idearoot._acptfactunits == {usa_week_unit.base: usa_week_unit}


def test_contract_acptfact_create():
    sx = examples_get_contract_with_4_levels()
    sunday_road = Road(f"{sx._economy_tag},weekdays,Sunday")
    weekday_road = Road(f"{sx._economy_tag},weekdays")
    sx.set_acptfact(base=weekday_road, pick=sunday_road)
    sunday_cx_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    assert sx._idearoot._acptfactunits == {sunday_cx_acptfact.base: sunday_cx_acptfact}


def test_set_acptfact_FailsToCreateWhenBaseAndAcptFactAreDifferenctAndAcptFactIdeaIsNotRangeRoot():
    # Given
    owner_text = "Bob"
    sx = ContractUnit(_owner=owner_text)
    time_x = "time_x"
    sx.add_idea(
        idea_kid=IdeaKid(_label=time_x, _begin=0, _close=140), walk=sx._economy_tag
    )
    t_x_road = Road(f"{sx._economy_tag},{time_x}")
    age1st = "age1st"
    sx.add_idea(idea_kid=IdeaKid(_label=age1st, _begin=0, _close=20), walk=t_x_road)
    a1_road = Road(f"{t_x_road},{age1st}")
    a1e1st = "a1_era1st"
    sx.add_idea(idea_kid=IdeaKid(_label=a1e1st, _begin=20, _close=30), walk=a1_road)
    a1e1_road = Road(f"{a1_road},{a1e1st}")
    assert sx._idearoot._acptfactunits in (None, {})

    # When/Then
    with pytest_raises(Exception) as excinfo:
        sx.set_acptfact(base=a1e1_road, pick=a1e1_road, open=20, nigh=23)
    assert (
        str(excinfo.value)
        == f"Non range-root acptfact:{a1e1_road} can only be set by range-root acptfact"
    )


def test_contract_acptfact_create():
    # Given
    sx = examples_get_contract_with_4_levels()
    sunday_road = Road(f"{sx._economy_tag},weekdays,Sunday")
    weekday_road = Road(f"{sx._economy_tag},weekdays")
    sx.set_acptfact(base=weekday_road, pick=sunday_road)
    sunday_cx_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    assert sx._idearoot._acptfactunits == {sunday_cx_acptfact.base: sunday_cx_acptfact}

    # When
    sx.del_acptfact(base=weekday_road)

    # Then
    assert sx._idearoot._acptfactunits == {}


def test_contract_get_idea_list_AcptFactHeirsCorrectlyInherited():
    # GIVEN
    owner_text = "Bob"
    sx = ContractUnit(_owner=owner_text)
    swim_text = "swim"
    swim_road = Road(f"{sx._economy_tag},{swim_text}")
    sx.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=sx._economy_tag)
    fast_text = "fast"
    slow_text = "slow"
    fast_road = Road(f"{swim_road},{fast_text}")
    slow_road = Road(f"{swim_road},{slow_text}")
    sx.add_idea(idea_kid=IdeaKid(_label=fast_text), walk=swim_road)
    sx.add_idea(idea_kid=IdeaKid(_label=slow_text), walk=swim_road)

    earth_text = "earth"
    earth_road = Road(f"{sx._economy_tag},{earth_text}")
    sx.add_idea(idea_kid=IdeaKid(_label=earth_text), walk=sx._economy_tag)

    swim_idea = sx.get_idea_kid(road=swim_road)
    fast_idea = sx.get_idea_kid(road=fast_road)
    slow_idea = sx.get_idea_kid(road=slow_road)

    assert swim_idea._acptfactheirs is None
    assert fast_idea._acptfactheirs is None
    assert slow_idea._acptfactheirs is None

    # WHEN
    sx.set_acptfact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)
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


def test_contract_get_idea_list_AcptFactUnitCorrectlyTransformsacptfactheir_shop():
    # GIVEN
    owner_text = "Bob"
    sx = ContractUnit(_owner=owner_text)
    swim_text = "swim"
    swim_road = f"{sx._economy_tag},{swim_text}"
    sx.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=sx._economy_tag)
    swim_idea = sx.get_idea_kid(road=swim_road)

    fast_text = "fast"
    slow_text = "slow"
    sx.add_idea(idea_kid=IdeaKid(_label=fast_text), walk=swim_road)
    sx.add_idea(idea_kid=IdeaKid(_label=slow_text), walk=swim_road)

    earth_text = "earth"
    earth_road = Road(f"{sx._economy_tag},{earth_text}")
    sx.add_idea(idea_kid=IdeaKid(_label=earth_text), walk=sx._economy_tag)

    assert swim_idea._acptfactheirs is None

    # WHEN
    sx.set_acptfact(base=earth_road, pick=earth_road, open=1.0, nigh=5.0)

    # THEN
    first_earthheir = acptfactheir_shop(
        base=earth_road, pick=earth_road, open=1.0, nigh=5.0
    )
    first_earthdict = {first_earthheir.base: first_earthheir}
    assert swim_idea._acptfactheirs == first_earthdict

    # WHEN
    # earth_curb = acptfactunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    # swim_y.set_acptfactunit(acptfactunit=earth_curb) Not sure what this is for. Testing how "set_acptfactunit" works?
    sx.set_acptfact(base=earth_road, pick=earth_road, open=3.0, nigh=5.0)

    # THEN
    after_earthheir = acptfactheir_shop(
        base=earth_road, pick=earth_road, open=3.0, nigh=5.0
    )
    after_earthdict = {after_earthheir.base: after_earthheir}
    assert swim_idea._acptfactheirs == after_earthdict


def test_contract_get_idea_list_AcptFactHeirCorrectlyDeletesAcptFactUnit():
    # GIVEN
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    swim_text = "swim"
    swim_road = Road(f"{sx._economy_tag},{swim_text}")
    sx.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=sx._economy_tag)
    fast_text = "fast"
    slow_text = "slow"
    fast_road = Road(f"{swim_road},{fast_text}")
    slow_road = Road(f"{swim_road},{slow_text}")
    sx.add_idea(idea_kid=IdeaKid(_label=fast_text), walk=swim_road)
    sx.add_idea(idea_kid=IdeaKid(_label=slow_text), walk=swim_road)

    earth_text = "earth"
    earth_road = Road(f"{sx._economy_tag},{earth_text}")
    sx.add_idea(idea_kid=IdeaKid(_label=earth_text), walk=sx._economy_tag)

    swim_idea = sx.get_idea_kid(road=swim_road)

    first_earthheir = acptfactheir_shop(
        base=earth_road, pick=earth_road, open=200.0, nigh=500.0
    )
    first_earthdict = {first_earthheir.base: first_earthheir}

    assert swim_idea._acptfactheirs is None

    # WHEN
    sx.set_acptfact(base=earth_road, pick=earth_road, open=200.0, nigh=500.0)

    # THEN
    assert swim_idea._acptfactheirs == first_earthdict

    earth_curb = acptfactunit_shop(base=earth_road, pick=earth_road, open=3.0, nigh=4.0)
    swim_idea.set_acptfactunit(acptfactunit=earth_curb)
    sx.set_contract_metrics()
    assert swim_idea._acptfactheirs == first_earthdict
    assert swim_idea._acptfactunits == {}


def test_get_ranged_acptfacts():
    # Given a single ranged acptfact
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    time_x = "time_x"
    sx.add_idea(
        idea_kid=IdeaKid(_label=time_x, _begin=0, _close=140), walk=sx._economy_tag
    )

    clean = "clean"
    sx.add_idea(idea_kid=IdeaKid(_label=clean, promise=True), walk=sx._economy_tag)
    c_road = f"{sx._economy_tag},{clean}"
    t_x_road = f"{sx._economy_tag},{time_x}"
    # sx.edit_idea_attr(road=c_road, required_base=t_x_road, required_sufffact=t_x_road, required_sufffact_open=5, required_sufffact_nigh=10)

    sx.set_acptfact(base=t_x_road, pick=t_x_road, open=5, nigh=10)
    print(f"Given a single ranged acptfact {sx._idearoot._acptfactunits=}")
    assert len(sx._idearoot._acptfactunits) == 1

    # When/Then
    assert len(sx._get_rangeroot_acptfactunits()) == 1

    # When one ranged acptfact added
    place = "place_x"
    sx.add_idea(
        idea_kid=IdeaKid(_label=place, _begin=600, _close=800), walk=sx._economy_tag
    )
    p_road = f"{sx._economy_tag},{place}"
    sx.set_acptfact(base=p_road, pick=p_road, open=5, nigh=10)
    print(f"When one ranged acptfact added {sx._idearoot._acptfactunits=}")
    assert len(sx._idearoot._acptfactunits) == 2

    # Then
    assert len(sx._get_rangeroot_acptfactunits()) == 2

    # When one non-ranged_acptfact added
    mood = "mood_x"
    sx.add_idea(idea_kid=IdeaKid(_label=mood), walk=sx._economy_tag)
    m_road = f"{sx._economy_tag},{mood}"
    sx.set_acptfact(base=m_road, pick=m_road)
    print(f"When one non-ranged_acptfact added {sx._idearoot._acptfactunits=}")
    assert len(sx._idearoot._acptfactunits) == 3

    # Then
    assert len(sx._get_rangeroot_acptfactunits()) == 2


def test_get_roots_ranged_acptfacts():
    # Given a two ranged acptfacts where one is "range-root" get_root_ranged_acptfacts returns one "range-root" acptfact
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    time_x = "time_x"
    sx.add_idea(
        idea_kid=IdeaKid(_label=time_x, _begin=0, _close=140), walk=sx._economy_tag
    )
    t_x_road = f"{sx._economy_tag},{time_x}"
    mood_x = "mood_x"
    sx.add_idea(idea_kid=IdeaKid(_label=mood_x), walk=sx._economy_tag)
    m_x_road = f"{sx._economy_tag},{mood_x}"
    happy = "happy"
    sad = "Sad"
    sx.add_idea(idea_kid=IdeaKid(_label=happy), walk=m_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=sad), walk=m_x_road)
    sx.set_acptfact(base=t_x_road, pick=t_x_road, open=5, nigh=10)
    sx.set_acptfact(base=m_x_road, pick=f"{m_x_road},{happy}")
    print(
        f"Given a root ranged acptfact and non-range acptfact:\n{sx._idearoot._acptfactunits=}"
    )
    assert len(sx._idearoot._acptfactunits) == 2

    # When/Then
    assert len(sx._get_rangeroot_acptfactunits()) == 1
    assert sx._get_rangeroot_acptfactunits()[0].base == t_x_road

    # a acptfact who's idea range is defined by numeric_root is not "rangeroot"
    mirrow_x = "mirrow_x"
    sx.add_idea(
        idea_kid=IdeaKid(_label=mirrow_x, _numeric_road=time_x), walk=sx._economy_tag
    )
    m_x_road = f"{sx._economy_tag},{mirrow_x}"
    sx.set_acptfact(base=m_x_road, pick=t_x_road, open=5, nigh=10)
    assert len(sx._idearoot._acptfactunits) == 3

    # When/Then
    assert len(sx._get_rangeroot_acptfactunits()) == 1
    assert sx._get_rangeroot_acptfactunits()[0].base == t_x_road


def test_create_lemma_acptfacts_CorrectlyCreates1stLevelLemmaAcptFact_Scenario1():
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    # # the action
    # clean = "clean"
    # sx.add_idea(idea_kid=IdeaKid(_label=clean, promise=True), walk=sx._economy_tag)

    time_x = "time_x"
    sx.add_idea(
        idea_kid=IdeaKid(_label=time_x, _begin=0, _close=140), walk=sx._economy_tag
    )
    t_x_road = f"{sx._economy_tag},{time_x}"
    age1st = "age1st"
    age2nd = "age2nd"
    age3rd = "age3rd"
    age4th = "age4th"
    age5th = "age5th"
    age6th = "age6th"
    age7th = "age7th"
    sx.add_idea(idea_kid=IdeaKid(_label=age1st, _begin=0, _close=20), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age2nd, _begin=20, _close=40), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age3rd, _begin=40, _close=60), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age4th, _begin=60, _close=80), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age5th, _begin=80, _close=100), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age6th, _begin=100, _close=120), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age7th, _begin=120, _close=140), walk=t_x_road)

    # set for instant moment in 3rd age
    sx.set_acptfact(base=time_x, pick=time_x, open=45, nigh=45)
    lemma_dict = sx._get_lemma_acptfactunits()
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
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    # # the action
    # clean = "clean"
    # sx.add_idea(idea_kid=IdeaKid(_label=clean, promise=True), walk=sx._economy_tag)

    time_x = "time_x"
    sx.add_idea(
        idea_kid=IdeaKid(_label=time_x, _begin=0, _close=140), walk=sx._economy_tag
    )
    t_x_road = f"{sx._economy_tag},{time_x}"
    age1st = "age1st"
    age2nd = "age2nd"
    age3rd = "age3rd"
    age4th = "age4th"
    age5th = "age5th"
    age6th = "age6th"
    age7th = "age7th"
    sx.add_idea(idea_kid=IdeaKid(_label=age1st, _begin=0, _close=20), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age2nd, _begin=20, _close=40), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age3rd, _begin=40, _close=60), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age4th, _begin=60, _close=80), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age5th, _begin=80, _close=100), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age6th, _begin=100, _close=120), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age7th, _begin=120, _close=140), walk=t_x_road)

    # set for instant moment in 3rd age
    sx.set_acptfact(base=time_x, pick=time_x, open=35, nigh=65)
    lemma_dict = sx._get_lemma_acptfactunits()
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
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    # # the action
    # clean = "clean"
    # sx.add_idea(idea_kid=IdeaKid(_label=clean, promise=True), walk=sx._economy_tag)

    time_x = "time_x"
    sx.add_idea(
        idea_kid=IdeaKid(_label=time_x, _begin=0, _close=140), walk=sx._economy_tag
    )
    t_x_road = f"{sx._economy_tag},{time_x}"
    age1st = "age1st"
    age2nd = "age2nd"
    age3rd = "age3rd"
    age4th = "age4th"
    age5th = "age5th"
    age6th = "age6th"
    age7th = "age7th"
    sx.add_idea(idea_kid=IdeaKid(_label=age1st, _begin=0, _close=20), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age2nd, _begin=20, _close=40), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age3rd, _begin=40, _close=60), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age4th, _begin=60, _close=80), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age5th, _begin=80, _close=100), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age6th, _begin=100, _close=120), walk=t_x_road)
    sx.add_idea(idea_kid=IdeaKid(_label=age7th, _begin=120, _close=140), walk=t_x_road)

    a2_road = f"{t_x_road},{age2nd}"
    a2e1st = "a1_era1st"
    a2e2nd = "a1_era2nd"
    a2e3rd = "a1_era3rd"
    a2e4th = "a1_era4th"
    sx.add_idea(idea_kid=IdeaKid(_label=a2e1st, _begin=20, _close=30), walk=a2_road)
    sx.add_idea(idea_kid=IdeaKid(_label=a2e2nd, _begin=30, _close=34), walk=a2_road)
    sx.add_idea(idea_kid=IdeaKid(_label=a2e3rd, _begin=34, _close=38), walk=a2_road)
    sx.add_idea(idea_kid=IdeaKid(_label=a2e4th, _begin=38, _close=40), walk=a2_road)

    a3_road = f"{t_x_road},{age3rd}"
    a3e1st = "a3_era1st"
    a3e2nd = "a3_era2nd"
    a3e3rd = "a3_era3rd"
    a3e4th = "a3_era4th"
    sx.add_idea(idea_kid=IdeaKid(_label=a3e1st, _begin=40, _close=45), walk=a3_road)
    sx.add_idea(idea_kid=IdeaKid(_label=a3e2nd, _begin=45, _close=50), walk=a3_road)
    sx.add_idea(idea_kid=IdeaKid(_label=a3e3rd, _begin=55, _close=58), walk=a3_road)
    sx.add_idea(idea_kid=IdeaKid(_label=a3e4th, _begin=58, _close=60), walk=a3_road)

    # set for instant moment in 3rd age
    sx.set_acptfact(base=time_x, pick=time_x, open=35, nigh=55)
    lemma_dict = sx._get_lemma_acptfactunits()
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
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    time_x = "time_x"
    arsub1 = "arbitary_subsection1"
    as1_road = f"{sx._economy_tag},{arsub1}"
    sx.add_idea(
        idea_kid=IdeaKid(_label=arsub1, _begin=0, _close=140), walk=sx._economy_tag
    )
    # range-root idea has range_source_road
    sx.add_idea(
        idea_kid=IdeaKid(
            _label=time_x, _begin=0, _close=140, _range_source_road=as1_road
        ),
        walk=sx._economy_tag,
    )

    arsub2 = "arbitary_subsection2"
    as2_road = f"{sx._economy_tag},{arsub2}"
    sx.add_idea(
        idea_kid=IdeaKid(_label=arsub2, _begin=0, _close=20), walk=sx._economy_tag
    )

    # non-range-root child idea has range_source_road
    t_x_road = f"{sx._economy_tag},{time_x}"
    age1st = "age1st"
    sx.add_idea(
        idea_kid=IdeaKid(
            _label=age1st, _begin=0, _close=20, _range_source_road=as2_road
        ),
        walk=t_x_road,
    )

    # set for instant moment in 3rd age
    sx.set_acptfact(base=time_x, pick=time_x, open=35, nigh=55)
    lemma_dict = sx._get_lemma_acptfactunits()
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
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    sx.set_time_hreg_ideas(c400_count=7)
    jajatime_road = f"{sx._economy_tag},time,jajatime"
    sx.set_acptfact(base=jajatime_road, pick=jajatime_road, open=1500, nigh=1500)
    lhu = sx._get_lemma_acptfactunits()

    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycle"].open == 1500
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycle"].nigh == 1500
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].open > 0
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].open < 1
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].nigh > 0
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].nigh < 1
    assert lhu[f"{sx._economy_tag},time,jajatime,days"].open >= 1
    assert lhu[f"{sx._economy_tag},time,jajatime,days"].open <= 2
    assert lhu[f"{sx._economy_tag},time,jajatime,days"].nigh >= 1
    assert lhu[f"{sx._economy_tag},time,jajatime,days"].nigh <= 2
    assert lhu[f"{sx._economy_tag},time,jajatime,day"].open == 60
    assert lhu[f"{sx._economy_tag},time,jajatime,day"].nigh == 60
    assert lhu[f"{sx._economy_tag},time,jajatime,week"].open == 1500
    assert int(lhu[f"{sx._economy_tag},time,jajatime,week"].nigh) == 1500
    assert lhu[f"{sx._economy_tag},time,tech,week"].open == 1500
    assert int(lhu[f"{sx._economy_tag},time,tech,week"].nigh) == 1500


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario5():
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    sx.set_time_hreg_ideas(c400_count=7)
    jajatime_road = f"{sx._economy_tag},time,jajatime"
    sx.set_acptfact(base=jajatime_road, pick=jajatime_road, open=1500, nigh=1063954002)
    lhu = sx._get_lemma_acptfactunits()

    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycle"].open == 0
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycle"].nigh == 210379680
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].open > 0
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].open < 1
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].nigh > 5
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].nigh < 6
    assert int(lhu[f"{sx._economy_tag},time,jajatime,days"].open) == 1  # 0 / 1440
    assert (
        int(lhu[f"{sx._economy_tag},time,jajatime,days"].nigh) == 738856
    )  # 1063953183 / 1440
    assert lhu[f"{sx._economy_tag},time,jajatime,day"].open == 0  # 0 / 1440
    assert (
        lhu[f"{sx._economy_tag},time,jajatime,day"].nigh == 1440
    )  # 1362  # 1063953183 / 1440
    assert lhu[f"{sx._economy_tag},time,jajatime,week"].open == 0  # 0 / 1440
    assert (
        int(lhu[f"{sx._economy_tag},time,jajatime,week"].nigh) == 10080
    )  # 1063953183 / 1440
    assert lhu[f"{sx._economy_tag},time,tech,week"].open == 0  # 0 / 1440
    assert (
        int(lhu[f"{sx._economy_tag},time,tech,week"].nigh) == 10080
    )  # 1063953183 / 1440


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario6():
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    sx.set_time_hreg_ideas(c400_count=7)
    jajatime_road = f"{sx._economy_tag},time,jajatime"
    sx.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063954000, nigh=1063954002
    )
    lhu = sx._get_lemma_acptfactunits()

    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycle"].open == 12055600.0
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycle"].nigh == 12055602.0
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].open > 5
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].open < 6
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].nigh > 5
    assert lhu[f"{sx._economy_tag},time,jajatime,400 year cycles"].nigh < 6
    assert (
        int(lhu[f"{sx._economy_tag},time,jajatime,days"].open) == 738856
    )  # 1063954000 / 1440
    assert (
        int(lhu[f"{sx._economy_tag},time,jajatime,days"].nigh) == 738856
    )  # 1063954000 / 1440
    assert lhu[f"{sx._economy_tag},time,jajatime,day"].open == 1360  # 0 / 1440
    assert (
        int(lhu[f"{sx._economy_tag},time,jajatime,day"].nigh) == 1362
    )  # 1063953183 / 1440


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario7():
    # Given
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    sx.set_time_hreg_ideas(c400_count=7)
    jajatime_road = f"{sx._economy_tag},time,jajatime"

    # When given a minute range that should be Thursday to Monday midnight
    sx.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063951200, nigh=1063956960
    )
    lhu = sx._get_lemma_acptfactunits()

    # Then
    week_open = lhu[f"{sx._economy_tag},time,jajatime,week"].open
    week_nigh = lhu[f"{sx._economy_tag},time,jajatime,week"].nigh
    print(f"for {sx._economy_tag},time,jajatime,week: {week_open=} {week_nigh=}")
    assert lhu[f"{sx._economy_tag},time,jajatime,week"].open == 7200
    assert lhu[f"{sx._economy_tag},time,jajatime,week"].nigh == 2880

    week_open = lhu[f"{sx._economy_tag},time,tech,week"].open
    week_nigh = lhu[f"{sx._economy_tag},time,tech,week"].nigh
    print(f"for {sx._economy_tag},time,tech,week: {week_open=} {week_nigh=}")
    assert lhu[f"{sx._economy_tag},time,tech,week"].open == 7200
    assert lhu[f"{sx._economy_tag},time,tech,week"].nigh == 2880
    print(lhu[f"{sx._economy_tag},time,tech,week"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Thursday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Friday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Saturday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Sunday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Monday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Tuesday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Wednesday"])

    # assert lhu[f"{sx._economy_tag},time,tech,week,Thursday"].active == True
    # assert lhu[f"{sx._economy_tag},time,tech,week,Friday"].active == True
    # assert lhu[f"{sx._economy_tag},time,tech,week,Saturday"].active == True
    # assert lhu[f"{sx._economy_tag},time,tech,week,Sunday"].active == True
    # assert lhu[f"{sx._economy_tag},time,tech,week,Monday"].active == False
    # assert lhu[f"{sx._economy_tag},time,tech,week,Tuesday"].active == False
    # assert lhu[f"{sx._economy_tag},time,tech,week,Wednesday"].active == False


def test_create_lemma_acptfacts_CorrectlyCreatesNthLevelLemmaAcptFact_Scenario8():
    # Given
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    sx.set_time_hreg_ideas(c400_count=7)
    jajatime_road = f"{sx._economy_tag},time,jajatime"

    # When given a minute range that should be Thursday to Monday midnight
    sx.set_acptfact(
        base=jajatime_road, pick=jajatime_road, open=1063951200, nigh=1063951200
    )
    lhu = sx._get_lemma_acptfactunits()

    # Then
    week_open = lhu[f"{sx._economy_tag},time,jajatime,week"].open
    week_nigh = lhu[f"{sx._economy_tag},time,jajatime,week"].nigh
    print(f"for {sx._economy_tag},time,jajatime,week: {week_open=} {week_nigh=}")
    assert lhu[f"{sx._economy_tag},time,jajatime,week"].open == 7200
    assert lhu[f"{sx._economy_tag},time,jajatime,week"].nigh == 7200

    week_open = lhu[f"{sx._economy_tag},time,tech,week"].open
    week_nigh = lhu[f"{sx._economy_tag},time,tech,week"].nigh
    print(f"for {sx._economy_tag},time,tech,week: {week_open=} {week_nigh=}")
    assert lhu[f"{sx._economy_tag},time,tech,week"].open == 7200
    assert lhu[f"{sx._economy_tag},time,tech,week"].nigh == 7200
    print(lhu[f"{sx._economy_tag},time,tech,week"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Thursday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Friday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Saturday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Sunday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Monday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Tuesday"])
    print(lhu[f"{sx._economy_tag},time,tech,week,Wednesday"])

    # assert lhu[f"{sx._economy_tag},time,tech,week,Thursday"].active == True
    # assert lhu[f"{sx._economy_tag},time,tech,week,Friday"].active == False
    # assert lhu[f"{sx._economy_tag},time,tech,week,Saturday"].active == False
    # assert lhu[f"{sx._economy_tag},time,tech,week,Sunday"].active == False
    # assert lhu[f"{sx._economy_tag},time,tech,week,Monday"].active == False
    # assert lhu[f"{sx._economy_tag},time,tech,week,Tuesday"].active == False
    # assert lhu[f"{sx._economy_tag},time,tech,week,Wednesday"].active == False


def test_contract_set_acptfact_create_missing_ideas_CreatesBaseAndAcptFact():
    # GIVEN
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    sx._idearoot.set_kids_empty_if_null()
    prob_text = "problems"
    prob_road = Road(f"{sx._economy_tag},{prob_text}")
    climate_text = "climate"
    climate_road = Road(f"{sx._economy_tag},{prob_text},{climate_text}")
    assert sx._idearoot._kids.get(prob_text) is None

    # WHEN
    sx.set_acptfact(base=prob_road, pick=climate_road, create_missing_ideas=True)

    # THEN
    assert sx._idearoot._kids.get(prob_text) != None
    assert sx.get_idea_kid(road=prob_road) != None
    assert sx.get_idea_kid(road=climate_road) != None


def test_contract_get_acptfactunits_base_and_acptfact_list_CorrectlyReturnsListOfAcptFactUnits():
    # GIVEN
    owner_text = "Tim"
    sx = ContractUnit(_owner=owner_text)
    sx._idearoot.set_kids_empty_if_null()

    prob_text = "problems"
    prob_road = Road(f"{sx._economy_tag},{prob_text}")
    climate_text = "climate"
    climate_road = Road(f"{sx._economy_tag},{prob_text},{climate_text}")
    sx.set_acptfact(base=prob_road, pick=climate_road, create_missing_ideas=True)

    weather_text = "weather"
    weather_road = Road(f"{sx._economy_tag},{weather_text}")
    windy_text = "windy"
    windy_road = Road(f"{sx._economy_tag},{weather_text},{windy_text}")
    sx.set_acptfact(base=weather_road, pick=windy_road, create_missing_ideas=True)
    hot_text = "hot"
    hot_road = Road(f"{sx._economy_tag},{weather_text},{hot_text}")
    sx.set_acptfact(base=weather_road, pick=hot_road, create_missing_ideas=True)
    cold_text = "cold"
    cold_road = Road(f"{sx._economy_tag},{weather_text},{cold_text}")
    sx.set_acptfact(base=weather_road, pick=cold_road, create_missing_ideas=True)

    games_text = "games"
    games_road = Road(f"{sx._economy_tag},{games_text}")
    football_text = "football"
    football_road = Road(f"{sx._economy_tag},{games_text},{football_text}")
    sx.set_acptfact(base=games_road, pick=football_road, create_missing_ideas=True)

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
