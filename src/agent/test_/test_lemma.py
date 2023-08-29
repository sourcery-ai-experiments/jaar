from src.agent.required import acptfactunit_shop
from src.agent.lemma import Lemma, Lemmas
from src.agent.tool import ToolKid


def test_lemma_attributes_exist():
    lemma = Lemma(
        src_acptfact=1, calc_acptfact=2, tool_x=3, eval_status=4, eval_count=5
    )
    assert lemma.src_acptfact == 1
    assert lemma.calc_acptfact == 2
    assert lemma.tool_x == 3
    assert lemma.eval_status == 4
    assert lemma.eval_count == 5


def test_lemmas_attributes_exist():
    lemma = Lemmas()
    assert lemma.lemmas is None


def test_lemmas_set_empty_if_null():
    lemmas = Lemmas()
    assert lemmas.lemmas is None
    lemmas.set_empty_if_null()
    assert lemmas.lemmas == {}


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario1():
    # Given
    lemmas_x = Lemmas()

    # When
    tool_kid = ToolKid(_desc="timerange1", _walk="src", _begin=0, _close=12)
    src_tool = ToolKid(_desc="whatever", _walk="src", _begin=-13, _close=500)
    tr1 = f"{tool_kid._walk},{tool_kid._desc}"
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    new_acptfact = lemmas_x._create_new_acptfact(
        tool_x=tool_kid, src_acptfact=src_acptfact, src_tool=src_tool
    )

    # Then
    assert new_acptfact.base == tr1
    assert new_acptfact.pick == tr1
    assert new_acptfact.open == 0
    assert new_acptfact.nigh == 12


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario2():
    # Given
    lemmas_x = Lemmas()

    # When
    tool_kid = ToolKid(_desc="timerange1", _walk="src", _begin=7, _close=12)
    tr1 = f"{tool_kid._walk},{tool_kid._desc}"
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    src_tool = ToolKid(_desc="whatever", _walk="src", _begin=-13, _close=500)
    new_acptfact = lemmas_x._create_new_acptfact(
        tool_x=tool_kid, src_acptfact=src_acptfact, src_tool=src_tool
    )

    # Then
    assert new_acptfact.open == 7
    assert new_acptfact.nigh == 12


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario3_denom():
    # Given
    lx = Lemmas()
    lx.set_empty_if_null()

    # When
    tool_kid = ToolKid(
        _desc="timerange1",
        _walk="src",
        _begin=0,
        _close=20,
        _numor=1,
        _denom=10,
        _reest=False,
    )
    tr1 = f"{tool_kid._walk},{tool_kid._desc}"
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    src_tool = ToolKid(_desc="whatever", _walk="src", _begin=-13, _close=500)
    new_acptfact = lx._create_new_acptfact(
        tool_x=tool_kid, src_acptfact=src_acptfact, src_tool=src_tool
    )

    # Then
    assert new_acptfact.open == 0
    assert new_acptfact.nigh == 3


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario3_2_denom():
    # Given
    lx = Lemmas()
    lx.set_empty_if_null()

    # When
    src_tool = ToolKid(_desc="range_x", _walk="src", _begin=0, _close=10080)
    tool_kid = ToolKid(
        _desc="timerange1",
        _walk="src,range_x",
        _begin=7200,
        _close=8440,
        _reest=False,
    )
    src_road = f"{src_tool._walk},{src_tool._desc}"
    src_acptfact = acptfactunit_shop(base=src_road, pick=src_road, open=7200, nigh=7200)
    new_acptfact = lx._create_new_acptfact(
        tool_x=tool_kid, src_acptfact=src_acptfact, src_tool=src_tool
    )

    # Then
    assert new_acptfact.open == 7200
    assert new_acptfact.nigh == 7200


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario4_denomReest():
    # Given
    lemmas_x = Lemmas()
    lemmas_x.set_empty_if_null()

    # When
    tool_kid = ToolKid(
        _desc="timerange1",
        _walk="src",
        _begin=0,
        _close=60,
        _numor=1,
        _denom=1,
        _reest=True,
    )
    tr1 = f"{tool_kid._walk},{tool_kid._desc}"
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=120, nigh=150)
    src_tool = ToolKid(_desc="whatever", _walk="src", _begin=-13, _close=500)
    new_acptfact = lemmas_x._create_new_acptfact(
        tool_x=tool_kid, src_acptfact=src_acptfact, src_tool=src_tool
    )

    # Then
    assert new_acptfact.open == 0
    assert new_acptfact.nigh == 30


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario5_denomReest():
    # Given
    lemmas_x = Lemmas()
    lemmas_x.set_empty_if_null()

    # When
    tool_kid = ToolKid(
        _desc="timerange1",
        _walk="src",
        _begin=0,
        _close=60,
        _numor=1,
        _denom=952,
        _reest=True,
    )
    tr1 = f"{tool_kid._walk},{tool_kid._desc}"
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=100, nigh=150)
    src_tool = ToolKid(_desc="whatever", _walk="src", _begin=-13, _close=500)
    new_acptfact = lemmas_x._create_new_acptfact(
        tool_x=tool_kid, src_acptfact=src_acptfact, src_tool=src_tool
    )

    # Then
    assert new_acptfact.open == 40
    assert new_acptfact.nigh == 30


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario6_denomReest():
    # Given
    lemmas_x = Lemmas()
    lemmas_x.set_empty_if_null()
    tool_src = ToolKid(
        _desc="timerange1",
        _walk="src",
        _begin=0,
        _close=60,
    )

    # When/Then Check
    tr3_kid = ToolKid(
        _desc="subera",
        _walk="src",
        _begin=40,
        _close=50,
    )
    tr3 = f"{tr3_kid._walk},{tr3_kid._desc}"
    src_acptfact = acptfactunit_shop(base=tr3, pick=tr3, open=30, nigh=20)
    tr3_30_20_acptfact = lemmas_x._create_new_acptfact(
        tool_x=tr3_kid, src_acptfact=src_acptfact, src_tool=tool_src
    )
    assert tr3_30_20_acptfact.open == 40
    assert tr3_30_20_acptfact.nigh == 50

    # When/Then Check
    trb_kid = ToolKid(
        _desc="subera",
        _walk="src",
        _begin=40,
        _close=60,
    )
    trb = f"{trb_kid._walk},{trb_kid._desc}"
    src_acptfact = acptfactunit_shop(base=trb, pick=trb, open=30, nigh=20)
    trb_30_20_acptfact = lemmas_x._create_new_acptfact(
        tool_x=trb_kid, src_acptfact=src_acptfact, src_tool=tool_src
    )
    assert trb_30_20_acptfact.open == 40
    assert trb_30_20_acptfact.nigh == 60

    # When/Then Check
    tr4_kid = ToolKid(
        _desc="subera",
        _walk="src",
        _begin=55,
        _close=10,
    )
    tr4 = f"{tr4_kid._walk},{tr4_kid._desc}"
    src_acptfact = acptfactunit_shop(base=tr4, pick=tr4, open=30, nigh=20)
    tr4_30_20_acptfact = lemmas_x._create_new_acptfact(
        tool_x=tr4_kid, src_acptfact=src_acptfact, src_tool=tool_src
    )
    assert tr4_30_20_acptfact.open == 55
    assert tr4_30_20_acptfact.nigh == 10

    # When/Then Check
    tr5_kid = ToolKid(
        _desc="subera",
        _walk="src",
        _begin=0,
        _close=60,
    )
    tr5 = f"{tr5_kid._walk},{tr5_kid._desc}"
    src_acptfact = acptfactunit_shop(base=tr5, pick=tr5, open=30, nigh=20)
    tr5_0_60_acptfact = lemmas_x._create_new_acptfact(
        tool_x=tr5_kid, src_acptfact=src_acptfact, src_tool=tool_src
    )
    assert tr5_0_60_acptfact.open == 30
    assert tr5_0_60_acptfact.nigh == 20


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario7_denomReest():
    # Given
    lemmas_x = Lemmas()
    lemmas_x.set_empty_if_null()

    # When
    tool_kid = ToolKid(
        _desc="timerange1",
        _walk="src",
        _begin=0,
        _close=60,
        _numor=1,
        _denom=1,
        _reest=True,
    )
    tr1 = f"{tool_kid._walk},{tool_kid._desc}"
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=90, nigh=150)
    src_tool = ToolKid(_desc="whatever", _walk="src", _begin=-13, _close=500)
    new_acptfact = lemmas_x._create_new_acptfact(
        tool_x=tool_kid, src_acptfact=src_acptfact, src_tool=src_tool
    )

    # Then
    assert new_acptfact.open == 0
    assert new_acptfact.nigh == 60


def test_lemmas_get_unevaluated_lemma_ReturnsCorrectLemmaWhenEmpty():
    # Given empty lemmas
    lemmas_y = Lemmas()
    lemmas_y.set_empty_if_null()

    # When
    lem1x = lemmas_y.get_unevaluated_lemma()
    print(f"{lem1x=}")
    print(f"{lemmas_y.lemmas=}")

    # Then
    assert lemmas_y.lemmas == {}
    assert lem1x is None


def test_lemmas_get_unevaluated_lemma_ReturnsCorrectLemmaWhenPopulated():
    # Given 2 in lemmas
    lemmas_x = Lemmas()
    lemmas_x.lemmas = {}
    src_tool = ToolKid(_desc="whatever", _walk="src", _begin=-13, _close=500)

    tr1_tool = ToolKid(_desc="timerange1", _walk="src", _begin=7, _close=12)
    tr1 = f"{tr1_tool._walk},{tr1_tool._desc}"
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    lemmas_x.eval(tool_x=tr1_tool, src_acptfact=src_acptfact, src_tool=src_tool)

    tr2_tool = ToolKid(_desc="timerange2", _walk="src", _begin=40, _close=60)
    tr2 = f"{tr2_tool._walk},{tr2_tool._desc}"
    src_acptfact = acptfactunit_shop(base=tr2, pick=tr2, open=55, nigh=60)
    lemmas_x.eval(tool_x=tr2_tool, src_acptfact=src_acptfact, src_tool=src_tool)

    # When
    lem1 = lemmas_x.get_unevaluated_lemma()
    print(f"{lem1.tool_x=}")
    print(f"{tr1=}")
    lem2 = lemmas_x.get_unevaluated_lemma()
    print(f"{lem2.tool_x=}")
    lem3 = lemmas_x.get_unevaluated_lemma()
    print(f"{lem3=}")

    # Then
    assert lem1.tool_x in (tr1_tool, tr2_tool)
    assert lem2.tool_x in (tr1_tool, tr2_tool)
    assert lem3 is None

    lemmas_x = None


def test_lemmas_is_lemmas_incomplete_ReturnsCorrectBoolWhenPopulated():
    # Given
    lemmas_z = Lemmas()
    lemmas_z.lemmas = {}
    src_tool = ToolKid(_desc="whatever", _walk="src", _begin=-13, _close=500)

    # for lemma in lemmas_z.lemmas.values():
    #     print(f"Does not exist: {lemma.eval_status=} {lemma.calc_acptfact=}")

    tr1_tool = ToolKid(_desc="timerange1", _walk="src", _begin=7, _close=12)
    tr1_road = f"{tr1_tool._walk},{tr1_tool._desc}"
    src_acptfact = acptfactunit_shop(base=tr1_road, pick=tr1_road, open=0, nigh=30)
    lemmas_z.eval(tool_x=tr1_tool, src_acptfact=src_acptfact, src_tool=src_tool)

    tr2_tool = ToolKid(_desc="timerange2", _walk="src", _begin=40, _close=60)
    tr2_road = f"{tr2_tool._walk},{tr2_tool._desc}"
    src_acptfact = acptfactunit_shop(base=tr2_road, pick=tr2_road, open=55, nigh=60)
    lemmas_z.eval(tool_x=tr2_tool, src_acptfact=src_acptfact, src_tool=src_tool)

    # When/Then
    assert len(lemmas_z.lemmas) == 2
    tr1_lemma = lemmas_z.lemmas.get(tr1_road)
    tr2_lemma = lemmas_z.lemmas.get(tr2_road)
    tr1_src_acptfact = tr1_lemma.src_acptfact
    tr2_src_acptfact = tr2_lemma.src_acptfact
    print(f"0 changes: {tr1_src_acptfact.base=} {tr1_lemma.eval_status=}")
    print(f"0 changes: {tr2_src_acptfact.base=} {tr2_lemma.eval_status=}")
    assert lemmas_z.is_lemmas_evaluated() == False

    # When
    lem1 = lemmas_z.get_unevaluated_lemma()
    # Then
    assert len(lemmas_z.lemmas) == 2
    print(f"1 changes: {tr1_src_acptfact.base=} {tr1_lemma.eval_status=}")
    print(f"1 changes: {tr2_src_acptfact.base=} {tr2_lemma.eval_status=}")
    assert lemmas_z.is_lemmas_evaluated() == False

    # When
    lem2 = lemmas_z.get_unevaluated_lemma()
    # Then
    assert len(lemmas_z.lemmas) == 2
    print(f"2 changes: {tr1_src_acptfact.base=} {tr1_lemma.eval_status=}")
    print(f"2 changes: {tr2_src_acptfact.base=} {tr2_lemma.eval_status=}")
    assert lemmas_z.is_lemmas_evaluated() == True


def test_lemmas_is_lemmas_incomplete_ReturnsCorrectBoolWhenEmpty():
    # Given
    lemmas_z = Lemmas()
    lemmas_z.lemmas = {}
    print(f"Does not exist: {lemmas_z=}")

    # When/Then
    assert not lemmas_z.lemmas
    assert lemmas_z.is_lemmas_evaluated() == True
