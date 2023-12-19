from src.agenda.idea import ideacore_shop, IdeaAttrHolder, IdeaCore
from src.agenda.group import BalanceLink, GroupBrand, balancelink_shop
from src.agenda.required_idea import (
    requiredunit_shop,
    RequiredUnit,
    acptfactunit_shop as c_acptfactunit,
    RoadPath,
)
from src.agenda.road import get_default_economy_root_label as root_label, get_road
from src.agenda.origin import originunit_shop
from pytest import raises as pytest_raises
from copy import deepcopy


def custom_set_idea_attr(
    idea: IdeaCore,
    weight: int = None,
    uid: int = None,
    required: RequiredUnit = None,  # delete/replace RequiredUnit
    required_base: RoadPath = None,
    required_sufffact: RoadPath = None,
    required_sufffact_open: float = None,
    required_sufffact_nigh: float = None,
    required_sufffact_divisor: int = None,
    required_del_sufffact_base: RoadPath = None,
    required_del_sufffact_need: RoadPath = None,
    required_suff_idea_active_status: str = None,
    begin: float = None,
    close: float = None,
    addin: int = None,
    numor: int = None,
    denom: int = None,
    reest: bool = None,
    numeric_road: RoadPath = None,
    range_source_road: float = None,
    descendant_promise_count: int = None,
    all_party_credit: bool = None,
    all_party_debt: bool = None,
    balancelink: BalanceLink = None,
    balancelink_del: GroupBrand = None,
    is_expanded: bool = None,
    promise: bool = None,
    problem_bool: bool = None,
    on_meld_weight_action: str = None,
):
    idea_attr = IdeaAttrHolder(
        weight=weight,
        uid=uid,
        required=required,
        required_base=required_base,
        required_sufffact=required_sufffact,
        required_sufffact_open=required_sufffact_open,
        required_sufffact_nigh=required_sufffact_nigh,
        required_sufffact_divisor=required_sufffact_divisor,
        required_del_sufffact_base=required_del_sufffact_base,
        required_del_sufffact_need=required_del_sufffact_need,
        required_suff_idea_active_status=required_suff_idea_active_status,
        begin=begin,
        close=close,
        addin=addin,
        numor=numor,
        denom=denom,
        reest=reest,
        numeric_road=numeric_road,
        range_source_road=range_source_road,
        descendant_promise_count=descendant_promise_count,
        all_party_credit=all_party_credit,
        all_party_debt=all_party_debt,
        balancelink=balancelink,
        balancelink_del=balancelink_del,
        is_expanded=is_expanded,
        promise=promise,
        problem_bool=problem_bool,
        on_meld_weight_action=on_meld_weight_action,
    )

    idea._set_idea_attr(idea_attr=idea_attr)


def test_idea_required_meld_BaseScenarioWorks():
    # GIVEN
    ball_text = "ball"
    ball_road = get_road(root_label(), ball_text)
    run_text = "run"
    run_road = get_road(ball_road, run_text)
    required_base_x1 = run_road

    _label_text = "spirit"
    yx1 = ideacore_shop(_label_text)
    custom_set_idea_attr(
        idea=yx1,
        required_base=required_base_x1,
        required_sufffact=required_base_x1,
    )

    yx2 = ideacore_shop(_label_text)
    custom_set_idea_attr(
        idea=yx2,
        required_base=required_base_x1,
        required_sufffact=required_base_x1,
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    lu_x = requiredunit_shop(base=required_base_x1)
    lu_x.set_sufffact(sufffact=required_base_x1)
    requiredunits_x = {lu_x.base: lu_x}
    assert yx1._requiredunits == requiredunits_x
    print(f"{yx1._on_meld_weight_action=}")
    assert yx1._weight == 1


def test_idea_required_meld_TwoRequiredsScenarioWorks():
    # GIVEN
    ball_text = "ball"
    ball_road = get_road(root_label(), ball_text)
    run_text = "run"
    run_road = get_road(ball_road, run_text)
    swim_text = "swim"
    swim_road = get_road(ball_road, swim_text)
    required_base_x1 = run_road
    required_base_x2 = swim_road

    _label_text = "spirit"
    yx1 = ideacore_shop(_label_text)
    custom_set_idea_attr(
        idea=yx1,
        required_base=required_base_x1,
        required_sufffact=required_base_x1,
    )

    yx2 = ideacore_shop(_label_text)
    custom_set_idea_attr(
        idea=yx2,
        required_base=required_base_x2,
        required_sufffact=required_base_x2,
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    assert len(yx1._requiredunits) == 2
    assert yx1._requiredunits[required_base_x1] != None
    assert yx1._requiredunits[required_base_x2] != None


def test_idea_required_meld_TwoRequiredsMeldScenarioWorks():
    # GIVEN
    ball_text = "ball"
    ball_road = get_road(root_label(), ball_text)
    run_text = "run"
    run_road = get_road(ball_road, run_text)
    swim_text = "swim"
    swim_road = get_road(ball_road, swim_text)
    required_base_x1 = run_road
    required_base_x2 = swim_road

    _label_text = "spirit"
    yx1 = ideacore_shop(_label_text)
    custom_set_idea_attr(
        idea=yx1,
        required_base=required_base_x1,
        required_sufffact=required_base_x1,
    )
    custom_set_idea_attr(
        idea=yx1,
        required_base=required_base_x2,
        required_sufffact=required_base_x2,
    )

    yx2 = ideacore_shop(_label_text)
    custom_set_idea_attr(
        idea=yx2,
        required_base=required_base_x2,
        required_sufffact=required_base_x2,
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    # lu_x = requiredunit_shop(base=required_base_x1)
    # lu_x.set_sufffact(sufffact=required_base_x1)
    # lu_x.set_sufffact(sufffact=required_base_x2)
    # requiredunits_x = {lu_x.base: lu_x}
    assert len(yx1._requiredunits) == 2
    assert yx1._requiredunits[required_base_x1] != None
    assert yx1._requiredunits[required_base_x2] != None


def test_idea_balancelink_meld_BaseScenarioWorks_on_meld_weight_actionEquals_default():
    # GIVEN
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    br1 = "Running"
    default_text = "default"
    custom_set_idea_attr(idea=yx1, on_meld_weight_action=default_text)
    custom_set_idea_attr(
        idea=yx1, balancelink=balancelink_shop(brand=br1, creditor_weight=2)
    )
    yx2 = ideacore_shop("Rocking")
    custom_set_idea_attr(idea=yx2, on_meld_weight_action=default_text)
    custom_set_idea_attr(
        idea=yx2, balancelink=balancelink_shop(brand=br1, creditor_weight=3)
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    bl_x = balancelink_shop(brand=br1, creditor_weight=2)
    assert yx1._balancelinks[br1] == bl_x


def test_idea_balancelink_meld_BaseScenarioWorks_on_meld_weight_actionEquals_sum():
    # GIVEN
    sum_text = "sum"
    casa_text = "casa"

    yx1 = ideacore_shop("spirit", _pad=casa_text)
    br1 = "Running"
    custom_set_idea_attr(idea=yx1, on_meld_weight_action=sum_text)
    custom_set_idea_attr(
        idea=yx1,
        balancelink=balancelink_shop(brand=br1, creditor_weight=2, debtor_weight=3),
    )
    yx2 = ideacore_shop("Rocking")
    custom_set_idea_attr(idea=yx2, on_meld_weight_action=sum_text)
    custom_set_idea_attr(
        idea=yx2,
        balancelink=balancelink_shop(brand=br1, creditor_weight=2, debtor_weight=3),
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    lu_x = balancelink_shop(brand=br1, creditor_weight=4, debtor_weight=6)
    assert yx1._balancelinks[br1] == lu_x


def test_idea_balancelink_meld_TwoGroupsScenarioWorks():
    # GIVEN
    sum_text = "sum"
    casa_text = "casa"

    yx1 = ideacore_shop("spirit", _pad=casa_text)
    br1 = "Running"
    custom_set_idea_attr(idea=yx1, on_meld_weight_action=sum_text)
    custom_set_idea_attr(
        idea=yx1, balancelink=balancelink_shop(brand=br1, creditor_weight=2)
    )

    br2 = "Bears"
    yx2 = ideacore_shop("Rocking")
    custom_set_idea_attr(idea=yx1, on_meld_weight_action=sum_text)
    custom_set_idea_attr(
        idea=yx2, balancelink=balancelink_shop(brand=br2, creditor_weight=2)
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    lu_x1 = balancelink_shop(brand=br1, creditor_weight=2)
    lu_x2 = balancelink_shop(brand=br2, creditor_weight=2)
    assert yx1._balancelinks[br1] == lu_x1
    assert yx1._balancelinks[br2] == lu_x2


def test_idea_acptfactunits_meld_BaseScenarioWorks():
    # GIVEN
    tech_text = "tech"
    tech_road = get_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = get_road(tech_road, bowl_text)
    casa_text = "casa"
    hc_1 = c_acptfactunit(base=tech_road, pick=bowl_road)
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    yx1.set_acptfactunits_empty_if_null()
    yx1.set_acptfactunit(acptfactunit=hc_1)

    hc_2 = c_acptfactunit(base=tech_road, pick=bowl_road)
    yx2 = ideacore_shop("fun", _pad=casa_text)
    yx2.set_acptfactunits_empty_if_null()
    yx2.set_acptfactunit(acptfactunit=hc_2)

    # WHEN
    yx1.meld(yx2)

    # THEN
    assert len(yx1._acptfactunits) == 1
    assert len(yx1._acptfactunits) == len(yx2._acptfactunits)
    assert yx1._acptfactunits == yx2._acptfactunits


def test_idea_acptfactunits_meld_2AcptFactUnitsWorks():
    # GIVEN
    tech_text = "tech"
    tech_road = get_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = get_road(tech_road, bowl_text)
    plate_text = "plate"
    plate_road = get_road(tech_road, plate_text)
    casa_text = "casa"

    hc_1 = c_acptfactunit(base=tech_road, pick=bowl_road)
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    yx1.set_acptfactunit(acptfactunit=hc_1)

    hc_2 = c_acptfactunit(base=plate_road, pick=plate_road)
    yx2 = ideacore_shop("fun", _pad=casa_text)
    yx2.set_acptfactunit(acptfactunit=hc_2)

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    assert len(yx1._acptfactunits) == 2
    assert len(yx1._acptfactunits) == len(yx2._acptfactunits) + 1
    assert yx1._acptfactunits != yx2._acptfactunits


def test_idea_attributes_meld_CorrectlyMeldsIdeas():
    # GIVEN
    tech_text = "tech"
    tech_road = get_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = get_road(tech_road, bowl_text)
    plate_text = "plate"
    plate_road = get_road(tech_road, plate_text)

    uid_x = "uid1xx"
    all_party_credit_x = "am_cx"
    all_party_debt_x = "am_dx"

    label1_text = "spirit"
    yx1 = ideacore_shop(label1_text)
    custom_set_idea_attr(
        idea=yx1,
        uid=uid_x,
        weight=7,
        begin=1,
        close=2,
        addin=3,
        denom=4,
        numor=5,
        reest=6,
        range_source_road=plate_road,
        numeric_road=bowl_road,
        promise=True,
        all_party_credit=all_party_credit_x,
        all_party_debt=all_party_debt_x,
        is_expanded=True,
    )

    label2_text = "fun"
    yx2 = ideacore_shop(label2_text)
    custom_set_idea_attr(
        idea=yx2,
        uid=uid_x,
        weight=7,
        begin=1,
        close=2,
        addin=3,
        denom=4,
        numor=5,
        reest=6,
        range_source_road=plate_road,
        numeric_road=bowl_road,
        promise=True,
        all_party_credit=all_party_credit_x,
        all_party_debt=all_party_debt_x,
        is_expanded=True,
    )

    # WHEN
    yx1.meld(yx2)

    # THEN
    assert yx1._uid == uid_x
    assert yx1._weight == 7
    assert yx1._begin == 1
    assert yx1._close == 2
    assert yx1._addin == 3
    assert yx1._denom == 4
    assert yx1._numor == 5
    assert yx1._reest == 6
    assert yx1._range_source_road == plate_road
    assert yx1._numeric_road == bowl_road
    assert yx1.promise == True
    assert yx1._all_party_credit == all_party_credit_x
    assert yx1._all_party_debt == all_party_debt_x
    assert yx1._is_expanded == True


def test_idea_attributes_meld_FailRaisesError_uid():
    x_pid = "_uid"
    x_val = "test_uid1"
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, uid=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    error_message = f"Meld fail idea={yx1.get_idea_road()} {x_pid}:{x_val} with {yx2.get_idea_road()} {x_pid}:None"

    huh_text = f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
    print(f"{error_message=}")

    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    print(f"{str(excinfo.value)=}")
    assert str(excinfo.value) == error_message
    assert str(excinfo.value) == huh_text

    # == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"


def test_idea_attributes_meld_FailRaisesError_begin():
    x_pid = "_begin"
    x_val = 77
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, begin=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
    )


def test_idea_attributes_meld_FailRaisesError_close():
    x_pid = "_close"
    x_val = 77
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, close=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
    )


def test_idea_attributes_meld_FailRaisesError_addin():
    x_pid = "_addin"
    x_val = 77
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, addin=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
    )


def test_idea_attributes_meld_FailRaisesError_denom():
    x_pid = "_denom"
    x_val = 15
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, denom=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
    )


def test_idea_attributes_meld_FailRaisesError_numor():
    x_pid = "_numor"
    x_val = 77
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, numor=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
    )


def test_idea_attributes_meld_FailRaisesError_reest():
    x_pid = "_reest"
    x_val = 77
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, reest=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
    )


def test_idea_attributes_meld_FailRaisesError_range_source_road():
    x_pid = "_range_source_road"
    x_val = "test_range_source_road1"
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, range_source_road=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
    )


def test_idea_attributes_meld_FailRaisesError_numeric_road():
    x_pid = "_numeric_road"
    x_val = "test_numeric_road1"
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, numeric_road=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
    )


def test_idea_attributes_meld_FailRaisesError_action():
    x_pid = "promise"
    x_val = True
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, promise=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad, yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad, yx2._label)} {x_pid}:False"
    )


# def test_idea_attributes_meld_FailRaisesError_all_party_credit():
# def test_idea_attributes_meld_FailRaisesError_all_party_debt():
#     x_pid = "_all_party_credit"
#     x_pid = "_all_party_debt"
#     x_val = "test_all_party_credit1"
#     x_val = "test_all_party_debt1"
#     yx1 = ideacore_shop("spirit", _pad=casa_text)
#     custom_set_idea_attr(idea=yx1, all_party_credit=x_val)
#     custom_set_idea_attr(idea=yx1, all_party_debt=x_val)
#     yx2 = ideacore_shop("fun", _pad=casa_text)

#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         yx1.meld(yx2)
#     assert (
#         str(excinfo.value)
#         == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:None"
#     )


def test_idea_attributes_meld_FailRaisesError_is_expanded():
    x_pid = "_is_expanded"
    x_val = False
    outside_val = True
    casa_text = "casa"
    yx1 = ideacore_shop("spirit", _pad=casa_text)
    custom_set_idea_attr(idea=yx1, is_expanded=x_val)
    yx2 = ideacore_shop("fun", _pad=casa_text)
    custom_set_idea_attr(idea=yx2, is_expanded=outside_val)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={get_road(yx1._pad,yx1._label)} {x_pid}:{x_val} with {get_road(yx2._pad,yx2._label)} {x_pid}:True"
    )


def test_idea_meld_CorrectlyCreatesOriginUnitWithOriginLink():
    # GIVEN
    label1_text = "spirit"
    yx1 = ideacore_shop(label1_text)

    label2_text = "fun"
    yx2 = ideacore_shop(label2_text)
    assert yx1._originunit is None

    # WHEN
    sue_text = "Sue"
    sue_weight = 5
    yx1.meld(other_idea=yx2, party_pid=sue_text, party_weight=sue_weight)

    # THEN
    assert yx1._originunit != None
    sue_originunit = originunit_shop()
    sue_originunit.set_originlink(pid=sue_text, weight=sue_weight)
    assert yx1._originunit == sue_originunit


def test_idea_meld_IdeaMeldingItselfCreatesOriginUnitWithCorrectOriginLink():
    # GIVEN
    label1_text = "spirit"
    yx1 = ideacore_shop(label1_text)
    tim_text = "Tim"
    tim_weight = 7
    tim_idea = ideacore_shop(tim_text)
    ex_yx1_originunit = originunit_shop()
    ex_yx1_originunit.set_originlink(pid=tim_text, weight=tim_weight)
    yx1.meld(other_idea=tim_idea, party_pid=tim_text, party_weight=tim_weight)
    assert yx1._originunit == ex_yx1_originunit

    sue_text = "Sue"
    sue_weight = 5
    ex_yx1_originunit.set_originlink(pid=sue_text, weight=sue_weight)
    assert yx1._originunit != ex_yx1_originunit

    yx1_copy = deepcopy(yx1)

    # WHEN
    yx1.meld(other_idea=yx1, party_pid=sue_text, party_weight=sue_weight)
    assert yx1._originunit == ex_yx1_originunit

    # THEN
    assert yx1._originunit != yx1_copy._originunit

    yx1_originunit_link_sue = yx1._originunit._links.get(sue_text)
    yx1_originunit_link_tim = yx1._originunit._links.get(tim_text)
    assert yx1_originunit_link_sue != None
    assert yx1_originunit_link_sue != yx1_copy._originunit._links.get(sue_text)
    assert yx1_originunit_link_tim == yx1_copy._originunit._links.get(tim_text)
    # assert yx1 == yx1_copy #Uncomment to see differences
