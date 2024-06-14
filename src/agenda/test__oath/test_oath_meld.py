from src.agenda.fact import factunit_shop, FactAttrFilter, FactUnit
from src.agenda.idea import BalanceLink, IdeaID, balancelink_shop
from src.agenda.reason_fact import (
    reasonunit_shop,
    ReasonUnit,
    beliefunit_shop as c_beliefunit,
    RoadUnit,
)
from src._road.road import get_default_real_id_roadnode as root_label, create_road
from src.agenda.origin import originunit_shop
from pytest import raises as pytest_raises
from copy import deepcopy


def arbitrarily_set_fact_attr(
    fact: FactUnit,
    weight: int = None,
    uid: int = None,
    reason: ReasonUnit = None,  # delete/replace ReasonUnit
    reason_base: RoadUnit = None,
    reason_premise: RoadUnit = None,
    reason_premise_open: float = None,
    reason_premise_nigh: float = None,
    reason_premise_divisor: int = None,
    reason_del_premise_base: RoadUnit = None,
    reason_del_premise_need: RoadUnit = None,
    reason_suff_fact_active: str = None,
    begin: float = None,
    close: float = None,
    addin: int = None,
    numor: int = None,
    denom: int = None,
    reest: bool = None,
    numeric_road: RoadUnit = None,
    range_source_road: float = None,
    descendant_pledge_count: int = None,
    all_party_cred: bool = None,
    all_party_debt: bool = None,
    balancelink: BalanceLink = None,
    balancelink_del: IdeaID = None,
    is_expanded: bool = None,
    pledge: bool = None,
    meld_strategy: str = None,
):
    fact_attr = FactAttrFilter(
        weight=weight,
        uid=uid,
        reason=reason,
        reason_base=reason_base,
        reason_premise=reason_premise,
        reason_premise_open=reason_premise_open,
        reason_premise_nigh=reason_premise_nigh,
        reason_premise_divisor=reason_premise_divisor,
        reason_del_premise_base=reason_del_premise_base,
        reason_del_premise_need=reason_del_premise_need,
        reason_suff_fact_active=reason_suff_fact_active,
        begin=begin,
        close=close,
        addin=addin,
        numor=numor,
        denom=denom,
        reest=reest,
        numeric_road=numeric_road,
        range_source_road=range_source_road,
        descendant_pledge_count=descendant_pledge_count,
        all_party_cred=all_party_cred,
        all_party_debt=all_party_debt,
        balancelink=balancelink,
        balancelink_del=balancelink_del,
        is_expanded=is_expanded,
        pledge=pledge,
        meld_strategy=meld_strategy,
    )

    fact._set_fact_attr(fact_attr=fact_attr)


def test_FactUnit_meld_ReturnsCorrectObj_BaseScenario_reasonunits():
    # GIVEN
    ball_text = "ball"
    ball_road = create_road(root_label(), ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    reason_base_x1 = run_road

    _label_text = "clean"
    x1_fact = factunit_shop(_label_text)
    arbitrarily_set_fact_attr(
        fact=x1_fact,
        reason_base=reason_base_x1,
        reason_premise=reason_base_x1,
    )

    x2_fact = factunit_shop(_label_text)
    arbitrarily_set_fact_attr(
        fact=x2_fact,
        reason_base=reason_base_x1,
        reason_premise=reason_base_x1,
    )

    # WHEN
    x1_fact.meld(other_fact=x2_fact)

    # THEN
    lu_x = reasonunit_shop(base=reason_base_x1)
    lu_x.set_premise(premise=reason_base_x1)
    reasonunits_x = {lu_x.base: lu_x}
    assert x1_fact._reasonunits == reasonunits_x
    print(f"{x1_fact._meld_strategy=}")
    assert x1_fact._weight == 1


def test_FactUnit_meld_ReturnsCorrectObj_TwoReasonsScenario_reasonunits():
    # GIVEN
    ball_text = "ball"
    ball_road = create_road(root_label(), ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    swim_text = "swim"
    swim_road = create_road(ball_road, swim_text)
    reason_base_x1 = run_road
    reason_base_x2 = swim_road

    _label_text = "clean"
    x1_fact = factunit_shop(_label_text)
    arbitrarily_set_fact_attr(
        fact=x1_fact,
        reason_base=reason_base_x1,
        reason_premise=reason_base_x1,
    )

    x2_fact = factunit_shop(_label_text)
    arbitrarily_set_fact_attr(
        fact=x2_fact,
        reason_base=reason_base_x2,
        reason_premise=reason_base_x2,
    )

    # WHEN
    x1_fact.meld(other_fact=x2_fact)

    # THEN
    assert len(x1_fact._reasonunits) == 2
    assert x1_fact._reasonunits[reason_base_x1] != None
    assert x1_fact._reasonunits[reason_base_x2] != None


def test_FactUnit_meld_ReturnsCorrectObj_TwoReasonsMeldScenario_reasonunits():
    # GIVEN
    ball_text = "ball"
    ball_road = create_road(root_label(), ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    swim_text = "swim"
    swim_road = create_road(ball_road, swim_text)
    reason_base_x1 = run_road
    reason_base_x2 = swim_road

    _label_text = "clean"
    x1_fact = factunit_shop(_label_text)
    arbitrarily_set_fact_attr(
        fact=x1_fact,
        reason_base=reason_base_x1,
        reason_premise=reason_base_x1,
    )
    arbitrarily_set_fact_attr(
        fact=x1_fact,
        reason_base=reason_base_x2,
        reason_premise=reason_base_x2,
    )

    x2_fact = factunit_shop(_label_text)
    arbitrarily_set_fact_attr(
        fact=x2_fact,
        reason_base=reason_base_x2,
        reason_premise=reason_base_x2,
    )

    # WHEN
    x1_fact.meld(other_fact=x2_fact)

    # THEN
    # lu_x = reasonunit_shop(base=reason_base_x1)
    # lu_x.set_premise(premise=reason_base_x1)
    # lu_x.set_premise(premise=reason_base_x2)
    # reasonunits_x = {lu_x.base: lu_x}
    assert len(x1_fact._reasonunits) == 2
    assert x1_fact._reasonunits[reason_base_x1] != None
    assert x1_fact._reasonunits[reason_base_x2] != None


def test_FactUnit_meld_ReturnsCorrectObj_BaseScenario_balancelinkWhen_meld_strategyEquals_default():
    # GIVEN
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    br1 = "Running"
    default_text = "default"
    arbitrarily_set_fact_attr(fact=x1_fact, meld_strategy=default_text)
    arbitrarily_set_fact_attr(
        fact=x1_fact, balancelink=balancelink_shop(idea_id=br1, credor_weight=2)
    )
    x2_fact = factunit_shop("Swimming")
    arbitrarily_set_fact_attr(fact=x2_fact, meld_strategy=default_text)
    arbitrarily_set_fact_attr(
        fact=x2_fact, balancelink=balancelink_shop(idea_id=br1, credor_weight=3)
    )

    # WHEN
    x1_fact.meld(other_fact=x2_fact)

    # THEN
    bl_x = balancelink_shop(idea_id=br1, credor_weight=2)
    assert x1_fact._balancelinks[br1] == bl_x


def test_FactUnit_meld_ReturnsCorrectObj_BaseScenario_balancelinkWhen_meld_strategyEquals_sum():
    # GIVEN
    sum_text = "sum"
    casa_text = "casa"

    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    br1 = "Running"
    arbitrarily_set_fact_attr(fact=x1_fact, meld_strategy=sum_text)
    arbitrarily_set_fact_attr(
        fact=x1_fact,
        balancelink=balancelink_shop(idea_id=br1, credor_weight=2, debtor_weight=3),
    )
    x2_fact = factunit_shop("Swimming")
    arbitrarily_set_fact_attr(fact=x2_fact, meld_strategy=sum_text)
    arbitrarily_set_fact_attr(
        fact=x2_fact,
        balancelink=balancelink_shop(idea_id=br1, credor_weight=2, debtor_weight=3),
    )

    # WHEN
    x1_fact.meld(other_fact=x2_fact)

    # THEN
    lu_x = balancelink_shop(idea_id=br1, credor_weight=4, debtor_weight=6)
    assert x1_fact._balancelinks[br1] == lu_x


def test_FactUnit_meld_ReturnsCorrectObj_TwoIdeasScenario_balancelink():
    # GIVEN
    sum_text = "sum"
    casa_text = "casa"

    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    br1 = "Running"
    arbitrarily_set_fact_attr(fact=x1_fact, meld_strategy=sum_text)
    arbitrarily_set_fact_attr(
        fact=x1_fact, balancelink=balancelink_shop(idea_id=br1, credor_weight=2)
    )

    br2 = "Bears"
    x2_fact = factunit_shop("Swimming")
    arbitrarily_set_fact_attr(fact=x1_fact, meld_strategy=sum_text)
    arbitrarily_set_fact_attr(
        fact=x2_fact, balancelink=balancelink_shop(idea_id=br2, credor_weight=2)
    )

    # WHEN
    x1_fact.meld(other_fact=x2_fact)

    # THEN
    lu_x1 = balancelink_shop(idea_id=br1, credor_weight=2)
    lu_x2 = balancelink_shop(idea_id=br2, credor_weight=2)
    assert x1_fact._balancelinks[br1] == lu_x1
    assert x1_fact._balancelinks[br2] == lu_x2


def test_FactUnit_meld_ReturnsCorrectObj_BaseScenario_beliefunits():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    casa_text = "casa"
    hc_1 = c_beliefunit(base=tech_road, pick=bowl_road)
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    x1_fact.set_beliefunit(beliefunit=hc_1)

    hc_2 = c_beliefunit(base=tech_road, pick=bowl_road)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)
    x2_fact.set_beliefunit(beliefunit=hc_2)

    # WHEN
    x1_fact.meld(x2_fact)

    # THEN
    assert len(x1_fact._beliefunits) == 1
    assert len(x1_fact._beliefunits) == len(x2_fact._beliefunits)
    assert x1_fact._beliefunits == x2_fact._beliefunits


def test_FactUnit_meld_ReturnsCorrectObj_2BeliefUnits_beliefunits():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    plate_text = "plate"
    plate_road = create_road(tech_road, plate_text)
    casa_text = "casa"

    hc_1 = c_beliefunit(base=tech_road, pick=bowl_road)
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    x1_fact.set_beliefunit(beliefunit=hc_1)

    hc_2 = c_beliefunit(base=plate_road, pick=plate_road)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)
    x2_fact.set_beliefunit(beliefunit=hc_2)

    # WHEN
    x1_fact.meld(other_fact=x2_fact)

    # THEN
    assert len(x1_fact._beliefunits) == 2
    assert len(x1_fact._beliefunits) == len(x2_fact._beliefunits) + 1
    assert x1_fact._beliefunits != x2_fact._beliefunits


def test_FactUnit_meld_CorrectlyMeldsRangeAttributesWhen_meld_strategyEquals_default():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    plate_text = "plate"
    plate_road = create_road(tech_road, plate_text)

    x_uid = "uid1xx"
    x_all_party_cred = "am_cx"
    x_all_party_debt = "am_dx"

    label1_text = "clean"
    texas_text = "texas"
    x1_fact = factunit_shop(label1_text, _agenda_real_id=texas_text)
    arbitrarily_set_fact_attr(
        fact=x1_fact,
        uid=x_uid,
        weight=7,
        begin=1,
        close=2,
        addin=3,
        denom=4,
        numor=5,
        reest=6,
        range_source_road=plate_road,
        numeric_road=bowl_road,
        pledge=True,
        all_party_cred=x_all_party_cred,
        all_party_debt=x_all_party_debt,
        is_expanded=True,
    )

    label2_text = "cook"
    x2_fact = factunit_shop(label2_text, _agenda_real_id=texas_text)
    arbitrarily_set_fact_attr(
        fact=x2_fact,
        uid=x_uid,
        weight=7,
        begin=1,
        close=2,
        addin=3,
        denom=4,
        numor=5,
        reest=6,
        range_source_road=plate_road,
        numeric_road=bowl_road,
        pledge=True,
        all_party_cred=x_all_party_cred,
        all_party_debt=x_all_party_debt,
        is_expanded=True,
    )

    # WHEN
    x1_fact.meld(x2_fact)

    # THEN
    assert x1_fact._uid == x_uid
    assert x1_fact._weight == 7
    assert x1_fact._begin == 1
    assert x1_fact._close == 2
    assert x1_fact._addin == 3
    assert x1_fact._denom == 4
    assert x1_fact._numor == 5
    assert x1_fact._reest == 6
    assert x1_fact._range_source_road == plate_road
    assert x1_fact._numeric_road == bowl_road
    assert x1_fact.pledge == True
    assert x1_fact._all_party_cred == x_all_party_cred
    assert x1_fact._all_party_debt == x_all_party_debt
    assert x1_fact._is_expanded == True
    assert x1_fact._agenda_real_id == texas_text


def test_FactUnit_meld_CorrectlyMeldsRangeAttributesWhen_meld_strategyEquals_override():
    # GIVEN
    tech_road = create_road(root_label(), "tech")
    bowl_road = create_road(tech_road, "bowl")
    plate_road = create_road(tech_road, "plate")

    x_uid = "uid1xx"
    x_all_party_cred = "am_cx"
    x_all_party_debt = "am_dx"

    label1_text = "clean"
    texas_text = "texas"
    x1_fact = factunit_shop(label1_text, _agenda_real_id=texas_text)
    arbitrarily_set_fact_attr(
        fact=x1_fact,
        uid=x_uid,
        weight=7,
        begin=1,
        close=2,
        addin=3,
        denom=4,
        numor=5,
        reest=6,
        range_source_road=plate_road,
        numeric_road=bowl_road,
        pledge=True,
        all_party_cred=x_all_party_cred,
        all_party_debt=x_all_party_debt,
        is_expanded=True,
    )

    label2_text = "cook"
    x2_fact = factunit_shop(label2_text, _agenda_real_id=texas_text)
    x2_uid = "uid2xx"
    override_text = "override"
    arbitrarily_set_fact_attr(
        fact=x2_fact,
        uid=x2_uid,
        weight=77,
        begin=11,
        close=22,
        addin=33,
        denom=44,
        numor=55,
        reest=66,
        range_source_road=plate_road,
        numeric_road=bowl_road,
        pledge=True,
        all_party_cred=x_all_party_cred,
        all_party_debt=x_all_party_debt,
        is_expanded=True,
        meld_strategy=override_text,
    )

    # WHEN
    x1_fact.meld(x2_fact)

    # THEN
    assert x1_fact._uid == x2_uid
    assert x1_fact._weight == 77
    assert x1_fact._begin == 11
    assert x1_fact._close == 22
    assert x1_fact._addin == 33
    assert x1_fact._denom == 44
    assert x1_fact._numor == 55
    assert x1_fact._reest == 66
    assert x1_fact._range_source_road == plate_road
    assert x1_fact._numeric_road == bowl_road
    assert x1_fact.pledge == True
    assert x1_fact._all_party_cred == x_all_party_cred
    assert x1_fact._all_party_debt == x_all_party_debt
    assert x1_fact._is_expanded == True
    assert x1_fact._agenda_real_id == texas_text


def test_FactUnit_meld_FailRaisesError_uid():
    x_attr = "_uid"
    x_val = "test_uid1"
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, uid=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)

    # WHEN/THEN
    error_message = f"Meld fail fact={x1_fact.get_road()} {x_attr}:{x_val} with {x2_fact.get_road()} {x_attr}:None"

    huh_text = f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
    print(f"{error_message=}")

    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    print(f"{str(excinfo.value)=}")
    assert str(excinfo.value) == error_message
    assert str(excinfo.value) == huh_text

    # == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"


def test_FactUnit_meld_FailRaisesError_begin():
    x_attr = "_begin"
    x_val = 77
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, begin=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
    )


def test_FactUnit_meld_FailRaisesError_close():
    x_attr = "_close"
    x_val = 77
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, close=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
    )


def test_FactUnit_meld_FailRaisesError_addin():
    x_attr = "_addin"
    x_val = 77
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, addin=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)
    print(f"{x2_fact._addin=}")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
    )


def test_FactUnit_meld_FailRaisesError_denom():
    x_attr = "_denom"
    x_val = 15
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, denom=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
    )


def test_FactUnit_meld_FailRaisesError_numor():
    x_attr = "_numor"
    x_val = 77
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, numor=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
    )


def test_FactUnit_meld_FailRaisesError_reest():
    x_attr = "_reest"
    x_val = 77
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, reest=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
    )


def test_FactUnit_meld_FailRaisesError_range_source_road():
    x_attr = "_range_source_road"
    x_val = "test_range_source_road1"
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, range_source_road=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
    )


def test_FactUnit_meld_FailRaisesError_numeric_road():
    x_attr = "_numeric_road"
    x_val = "test_numeric_road1"
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, numeric_road=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
    )


def test_FactUnit_meld_FailRaisesError_action():
    x_attr = "pledge"
    x_val = True
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, pledge=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road, x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road, x2_fact._label)} {x_attr}:False"
    )


# def test_FactUnit_meld_FailRaisesError_all_party_cred():
# def test_FactUnit_meld_FailRaisesError_all_party_debt():
#     x_attr = "_all_party_cred"
#     x_attr = "_all_party_debt"
#     x_val = "test_all_party_cred1"
#     x_val = "test_all_party_debt1"
#     x1_fact = factunit_shop("clean", _parent_road=casa_text)
#     arbitrarily_set_fact_attr(fact=x1_fact, all_party_cred=x_val)
#     arbitrarily_set_fact_attr(fact=x1_fact, all_party_debt=x_val)
#     x2_fact = factunit_shop("cook", _parent_road=casa_text)

#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         x1_fact.meld(x2_fact)
#     assert (
#         str(excinfo.value)
#         == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:None"
#     )


def test_FactUnit_meld_FailRaisesError_is_expanded():
    x_attr = "_is_expanded"
    x_val = False
    outside_val = True
    casa_text = "casa"
    x1_fact = factunit_shop("clean", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x1_fact, is_expanded=x_val)
    x2_fact = factunit_shop("cook", _parent_road=casa_text)
    arbitrarily_set_fact_attr(fact=x2_fact, is_expanded=outside_val)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_fact.meld(x2_fact)
    assert (
        str(excinfo.value)
        == f"Meld fail fact={create_road(x1_fact._parent_road,x1_fact._label)} {x_attr}:{x_val} with {create_road(x2_fact._parent_road,x2_fact._label)} {x_attr}:True"
    )


def test_FactUnit_meld_CorrectlyCreatesOriginUnitWithOriginLink():
    # GIVEN
    label1_text = "clean"
    x1_fact = factunit_shop(label1_text)

    label2_text = "cook"
    x2_fact = factunit_shop(label2_text)
    assert x1_fact._originunit == originunit_shop()

    # WHEN
    sue_text = "Sue"
    sue_weight = 5
    x1_fact.meld(other_fact=x2_fact, party_id=sue_text, party_weight=sue_weight)

    # THEN
    assert x1_fact._originunit != None
    sue_originunit = originunit_shop()
    sue_originunit.set_originlink(party_id=sue_text, weight=sue_weight)
    assert x1_fact._originunit == sue_originunit


def test_FactUnit_meld_FactMeldingItselfCreatesOriginUnitWithCorrectOriginLink():
    # GIVEN
    label1_text = "clean"
    x1_fact = factunit_shop(label1_text)
    tim_text = "Tim"
    tim_weight = 7
    tim_fact = factunit_shop(tim_text)
    ex_x1_fact_originunit = originunit_shop()
    ex_x1_fact_originunit.set_originlink(party_id=tim_text, weight=tim_weight)
    x1_fact.meld(other_fact=tim_fact, party_id=tim_text, party_weight=tim_weight)
    assert x1_fact._originunit == ex_x1_fact_originunit

    sue_text = "Sue"
    sue_weight = 5
    ex_x1_fact_originunit.set_originlink(party_id=sue_text, weight=sue_weight)
    assert x1_fact._originunit != ex_x1_fact_originunit

    x1_fact_copy = deepcopy(x1_fact)

    # WHEN
    x1_fact.meld(other_fact=x1_fact, party_id=sue_text, party_weight=sue_weight)
    assert x1_fact._originunit == ex_x1_fact_originunit

    # THEN
    assert x1_fact._originunit != x1_fact_copy._originunit

    x1_fact_originunit_link_sue = x1_fact._originunit._links.get(sue_text)
    x1_fact_originunit_link_tim = x1_fact._originunit._links.get(tim_text)
    assert x1_fact_originunit_link_sue != None
    assert x1_fact_originunit_link_sue != x1_fact_copy._originunit._links.get(sue_text)
    assert x1_fact_originunit_link_tim == x1_fact_copy._originunit._links.get(tim_text)
    # assert x1_fact == x1_fact_copy #Uncomment to see differences
