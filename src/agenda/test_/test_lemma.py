from src.agenda.required_idea import acptfactunit_shop
from src.agenda.lemma import Lemma, Lemmas, lemmas_shop
from src.agenda.idea import ideacore_shop
from src.agenda.road import (
    get_default_culture_root_label as root_label,
    get_road,
    get_node_delimiter,
)


def test_lemma_attributes_exist():
    x_lemma = Lemma(
        src_acptfact=1, calc_acptfact=2, idea_x=3, eval_status=4, eval_count=5
    )
    assert x_lemma.src_acptfact == 1
    assert x_lemma.calc_acptfact == 2
    assert x_lemma.idea_x == 3
    assert x_lemma.eval_status == 4
    assert x_lemma.eval_count == 5


def test_lemmas_attributes_exist():
    # GIVEN / WHEN
    x_lemma = Lemmas

    # THEN
    assert x_lemma.lemmas is None


def test_lemmas_shop_CorrectReturnsObj():
    # WHEN
    x_lemma = lemmas_shop()

    # THEN
    assert x_lemma.lemmas == {}


def test_lemmas_set_empty_if_null():
    # GIVEN
    x_lemmas = Lemmas()
    assert x_lemmas.lemmas is None

    # WHEN
    x_lemmas.set_empty_if_null()

    # THEN
    assert x_lemmas.lemmas == {}


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario1():
    # GIVEN
    x_lemmas_x = lemmas_shop()

    # WHEN
    pad_road = root_label()
    idea_kid = ideacore_shop("timerange1", _pad=pad_road, _begin=0, _close=12)
    src_idea = ideacore_shop("sub_timerange", _pad=pad_road, _begin=-13, _close=500)
    tr1 = get_road(idea_kid._pad, idea_kid._label)
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    new_acptfact = x_lemmas_x._create_new_acptfact(
        idea_x=idea_kid, src_acptfact=src_acptfact, src_idea=src_idea
    )

    # THEN
    assert new_acptfact.base == tr1
    assert new_acptfact.pick == tr1
    assert new_acptfact.open == 0
    assert new_acptfact.nigh == 12


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario2():
    # GIVEN
    x_lemmas_x = lemmas_shop()

    # WHEN
    pad_road = root_label()
    idea_kid = ideacore_shop("timerange1", _pad=pad_road, _begin=7, _close=12)
    tr1 = get_road(idea_kid._pad, idea_kid._label)
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    src_idea = ideacore_shop("sub_timerange", _pad=pad_road, _begin=-13, _close=500)
    new_acptfact = x_lemmas_x._create_new_acptfact(
        idea_x=idea_kid, src_acptfact=src_acptfact, src_idea=src_idea
    )

    # THEN
    assert new_acptfact.open == 7
    assert new_acptfact.nigh == 12


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario3_denom():
    # GIVEN
    lx = lemmas_shop()
    lx.set_empty_if_null()

    # WHEN
    pad_road = root_label()
    idea_kid = ideacore_shop(
        _label="timerange1",
        _pad=pad_road,
        _begin=0,
        _close=20,
        _numor=1,
        _denom=10,
        _reest=False,
    )
    tr1 = get_road(idea_kid._pad, idea_kid._label)
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    src_idea = ideacore_shop("sub_timerange", _pad=pad_road, _begin=-13, _close=500)
    new_acptfact = lx._create_new_acptfact(
        idea_x=idea_kid, src_acptfact=src_acptfact, src_idea=src_idea
    )

    # THEN
    assert new_acptfact.open == 0
    assert new_acptfact.nigh == 3


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario3_2_denom():
    # GIVEN
    lx = lemmas_shop()
    lx.set_empty_if_null()

    # WHEN
    pad_road = root_label()
    ex_idea = ideacore_shop("range_x", _pad=pad_road, _begin=0, _close=10080)
    idea_kid = ideacore_shop(
        _label="timerange1",
        _pad=get_road(root_label(), "range_x"),
        _begin=7200,
        _close=8440,
        _reest=False,
    )
    ex_road = get_road(ex_idea._pad, ex_idea._label)
    ex_acptfact = acptfactunit_shop(base=ex_road, pick=ex_road, open=7200, nigh=7200)
    new_acptfact = lx._create_new_acptfact(
        idea_x=idea_kid, src_acptfact=ex_acptfact, src_idea=ex_idea
    )

    # THEN
    assert new_acptfact.open == 7200
    assert new_acptfact.nigh == 7200


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario4_denomReest():
    # GIVEN
    x_lemmas_x = lemmas_shop()
    x_lemmas_x.set_empty_if_null()

    # WHEN
    pad_road = root_label()
    idea_kid = ideacore_shop(
        _label="timerange1",
        _pad=pad_road,
        _begin=0,
        _close=60,
        _numor=1,
        _denom=1,
        _reest=True,
    )
    tr1 = get_road(idea_kid._pad, idea_kid._label)
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=120, nigh=150)
    src_idea = ideacore_shop("sub_timerange", _pad=pad_road, _begin=-13, _close=500)
    new_acptfact = x_lemmas_x._create_new_acptfact(
        idea_x=idea_kid, src_acptfact=src_acptfact, src_idea=src_idea
    )

    # THEN
    assert new_acptfact.open == 0
    assert new_acptfact.nigh == 30


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario5_denomReest():
    # GIVEN
    x_lemmas_x = lemmas_shop()
    x_lemmas_x.set_empty_if_null()

    # WHEN
    pad_road = root_label()
    idea_kid = ideacore_shop(
        _label="timerange1",
        _pad=pad_road,
        _begin=0,
        _close=60,
        _numor=1,
        _denom=952,
        _reest=True,
    )
    tr1 = get_road(idea_kid._pad, idea_kid._label)
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=100, nigh=150)
    src_idea = ideacore_shop("sub_timerange", _pad=pad_road, _begin=-13, _close=500)
    new_acptfact = x_lemmas_x._create_new_acptfact(
        idea_x=idea_kid, src_acptfact=src_acptfact, src_idea=src_idea
    )

    # THEN
    assert new_acptfact.open == 40
    assert new_acptfact.nigh == 30


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario6_denomReest():
    # GIVEN
    pad_road = root_label()
    x_lemmas_x = lemmas_shop()
    x_lemmas_x.set_empty_if_null()
    idea_src = ideacore_shop(
        _label="timerange1",
        _pad=pad_road,
        _begin=0,
        _close=60,
    )

    # WHEN / THEN Check
    tr3_kid = ideacore_shop(
        _label="subera",
        _pad=pad_road,
        _begin=40,
        _close=50,
    )
    tr3 = get_road(tr3_kid._pad, tr3_kid._label)
    src_acptfact = acptfactunit_shop(base=tr3, pick=tr3, open=30, nigh=20)
    tr3_30_20_acptfact = x_lemmas_x._create_new_acptfact(
        idea_x=tr3_kid, src_acptfact=src_acptfact, src_idea=idea_src
    )
    assert tr3_30_20_acptfact.open == 40
    assert tr3_30_20_acptfact.nigh == 50

    # WHEN / THEN Check
    trb_kid = ideacore_shop(
        _label="subera",
        _pad=pad_road,
        _begin=40,
        _close=60,
    )
    trb = get_road(trb_kid._pad, trb_kid._label)
    src_acptfact = acptfactunit_shop(base=trb, pick=trb, open=30, nigh=20)
    trb_30_20_acptfact = x_lemmas_x._create_new_acptfact(
        idea_x=trb_kid, src_acptfact=src_acptfact, src_idea=idea_src
    )
    assert trb_30_20_acptfact.open == 40
    assert trb_30_20_acptfact.nigh == 60

    # WHEN / THEN Check
    tr4_kid = ideacore_shop(
        _label="subera",
        _pad=pad_road,
        _begin=55,
        _close=10,
    )
    tr4 = get_road(tr4_kid._pad, tr4_kid._label)
    src_acptfact = acptfactunit_shop(base=tr4, pick=tr4, open=30, nigh=20)
    tr4_30_20_acptfact = x_lemmas_x._create_new_acptfact(
        idea_x=tr4_kid, src_acptfact=src_acptfact, src_idea=idea_src
    )
    assert tr4_30_20_acptfact.open == 55
    assert tr4_30_20_acptfact.nigh == 10

    # WHEN / THEN Check
    tr5_kid = ideacore_shop(
        _label="subera",
        _pad=pad_road,
        _begin=0,
        _close=60,
    )
    tr5 = get_road(tr5_kid._pad, tr5_kid._label)
    src_acptfact = acptfactunit_shop(base=tr5, pick=tr5, open=30, nigh=20)
    tr5_0_60_acptfact = x_lemmas_x._create_new_acptfact(
        idea_x=tr5_kid, src_acptfact=src_acptfact, src_idea=idea_src
    )
    assert tr5_0_60_acptfact.open == 30
    assert tr5_0_60_acptfact.nigh == 20


def test_lemmas_create_new_acptfact_createsCorrectAcptFact_scenario7_denomReest():
    # GIVEN
    x_lemmas_x = lemmas_shop()
    x_lemmas_x.set_empty_if_null()

    # WHEN
    pad_road = root_label()
    idea_kid = ideacore_shop(
        _label="timerange1",
        _pad=pad_road,
        _begin=0,
        _close=60,
        _numor=1,
        _denom=1,
        _reest=True,
    )
    tr1 = get_road(idea_kid._pad, idea_kid._label)
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=90, nigh=150)
    src_idea = ideacore_shop("sub_timerange", _pad=pad_road, _begin=-13, _close=500)
    new_acptfact = x_lemmas_x._create_new_acptfact(
        idea_x=idea_kid, src_acptfact=src_acptfact, src_idea=src_idea
    )

    # THEN
    assert new_acptfact.open == 0
    assert new_acptfact.nigh == 60


def test_lemmas_get_unevaluated_lemma_ReturnsCorrectLemmaWhenEmpty():
    # GIVEN empty x_lemmas
    x_lemmas = lemmas_shop()
    x_lemmas.set_empty_if_null()

    # WHEN
    lem1x = x_lemmas.get_unevaluated_lemma()
    print(f"{lem1x=}")
    print(f"{x_lemmas.lemmas=}")

    # THEN
    assert x_lemmas.lemmas == {}
    assert lem1x is None


def test_lemmas_get_unevaluated_lemma_ReturnsCorrectLemmaWhenPopulated():
    # GIVEN 2 in x_lemmas
    pad_road = root_label()
    x_lemmas_x = lemmas_shop()
    x_lemmas_x.lemmas = {}
    src_idea = ideacore_shop("sub_timerange", _pad=pad_road, _begin=-13, _close=500)

    tr1_idea = ideacore_shop("timerange1", _pad=pad_road, _begin=7, _close=12)
    tr1 = get_road(tr1_idea._pad, tr1_idea._label)
    src_acptfact = acptfactunit_shop(base=tr1, pick=tr1, open=0, nigh=30)
    x_lemmas_x.eval(idea_x=tr1_idea, src_acptfact=src_acptfact, src_idea=src_idea)

    tr2_idea = ideacore_shop("timerange2", _pad=pad_road, _begin=40, _close=60)
    tr2 = get_road(tr2_idea._pad, tr2_idea._label)
    src_acptfact = acptfactunit_shop(base=tr2, pick=tr2, open=55, nigh=60)
    x_lemmas_x.eval(idea_x=tr2_idea, src_acptfact=src_acptfact, src_idea=src_idea)

    # WHEN
    lem1 = x_lemmas_x.get_unevaluated_lemma()
    print(f"{lem1.idea_x=}")
    print(f"{tr1=}")
    lem2 = x_lemmas_x.get_unevaluated_lemma()
    print(f"{lem2.idea_x=}")
    lem3 = x_lemmas_x.get_unevaluated_lemma()
    print(f"{lem3=}")

    # THEN
    assert lem1.idea_x in (tr1_idea, tr2_idea)
    assert lem2.idea_x in (tr1_idea, tr2_idea)
    assert lem3 is None

    x_lemmas_x = None


def test_lemmas_is_lemmas_incomplete_ReturnsCorrectBoolWhenPopulated():
    # GIVEN
    pad_road = root_label()
    z_lemmas = lemmas_shop()
    z_lemmas.lemmas = {}
    src_idea = ideacore_shop("sub_timerange", _pad=pad_road, _begin=-13, _close=500)

    # for x_lemma in z_lemmas.lemmas.values():
    #     print(f"Does not exist: {lemma.eval_status=} {lemma.calc_acptfact=}")

    tr1_idea = ideacore_shop("timerange1", _pad=pad_road, _begin=7, _close=12)
    tr1_road = get_road(tr1_idea._pad, tr1_idea._label)
    src_acptfact = acptfactunit_shop(base=tr1_road, pick=tr1_road, open=0, nigh=30)
    z_lemmas.eval(idea_x=tr1_idea, src_acptfact=src_acptfact, src_idea=src_idea)

    tr2_idea = ideacore_shop("timerange2", _pad=pad_road, _begin=40, _close=60)
    tr2_road = get_road(tr2_idea._pad, tr2_idea._label)
    src_acptfact = acptfactunit_shop(base=tr2_road, pick=tr2_road, open=55, nigh=60)
    z_lemmas.eval(idea_x=tr2_idea, src_acptfact=src_acptfact, src_idea=src_idea)

    # WHEN / THEN
    assert len(z_lemmas.lemmas) == 2
    tr1_lemma = z_lemmas.lemmas.get(tr1_road)
    tr2_lemma = z_lemmas.lemmas.get(tr2_road)
    tr1_src_acptfact = tr1_lemma.src_acptfact
    tr2_src_acptfact = tr2_lemma.src_acptfact
    print(f"0 changes: {tr1_src_acptfact.base=} {tr1_lemma.eval_status=}")
    print(f"0 changes: {tr2_src_acptfact.base=} {tr2_lemma.eval_status=}")
    assert z_lemmas.is_lemmas_evaluated() == False

    # WHEN
    lem1 = z_lemmas.get_unevaluated_lemma()
    # THEN
    assert len(z_lemmas.lemmas) == 2
    print(f"1 changes: {tr1_src_acptfact.base=} {tr1_lemma.eval_status=}")
    print(f"1 changes: {tr2_src_acptfact.base=} {tr2_lemma.eval_status=}")
    assert z_lemmas.is_lemmas_evaluated() == False

    # WHEN
    lem2 = z_lemmas.get_unevaluated_lemma()
    # THEN
    assert len(z_lemmas.lemmas) == 2
    print(f"2 changes: {tr1_src_acptfact.base=} {tr1_lemma.eval_status=}")
    print(f"2 changes: {tr2_src_acptfact.base=} {tr2_lemma.eval_status=}")
    assert z_lemmas.is_lemmas_evaluated() == True


def test_lemmas_is_lemmas_incomplete_ReturnsCorrectBoolWhenEmpty():
    # GIVEN
    z_lemmas = lemmas_shop()
    z_lemmas.lemmas = {}
    print(f"Does not exist: {z_lemmas=}")

    # WHEN / THEN
    assert not z_lemmas.lemmas
    assert z_lemmas.is_lemmas_evaluated() == True
