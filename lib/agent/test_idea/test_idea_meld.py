from lib.agent.idea import IdeaCore
from lib.agent.brand import BrandLink, BrandName, brandlink_shop
from lib.agent.required import RequiredUnit, acptfactunit_shop as c_acptfactunit, Road
from pytest import raises as pytest_raises


def custom_set_idea_attr(
    idea: IdeaCore,
    weight: int = None,
    uid: int = None,
    required: RequiredUnit = None,  # delete/replace RequiredUnit
    required_base: Road = None,
    required_sufffact: Road = None,
    required_sufffact_open: float = None,
    required_sufffact_nigh: float = None,
    required_sufffact_divisor: int = None,
    required_del_sufffact_base: Road = None,
    required_del_sufffact_need: Road = None,
    required_suff_idea_active_status: str = None,
    begin: float = None,
    close: float = None,
    addin: int = None,
    numor: int = None,
    denom: int = None,
    reest: bool = None,
    numeric_road: Road = None,
    special_road: float = None,
    descendant_promise_count: int = None,
    all_ally_credit: bool = None,
    all_ally_debt: bool = None,
    brandlink: BrandLink = None,
    brandlink_del: BrandName = None,
    is_expanded: bool = None,
    promise: bool = None,
    problem_bool: bool = None,
    on_meld_weight_action: str = None,
):
    idea._set_idea_attr(
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
        special_road=special_road,
        descendant_promise_count=descendant_promise_count,
        all_ally_credit=all_ally_credit,
        all_ally_debt=all_ally_debt,
        brandlink=brandlink,
        brandlink_del=brandlink_del,
        is_expanded=is_expanded,
        promise=promise,
        problem_bool=problem_bool,
        on_meld_weight_action=on_meld_weight_action,
    )


def test_idea_required_meld_BaseScenarioWorks():
    # GIVEN
    required_base_x1 = "src,ball,run"
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(
        idea=yx1,
        required_base=required_base_x1,
        required_sufffact=required_base_x1,
    )

    yx2 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(
        idea=yx2,
        required_base=required_base_x1,
        required_sufffact=required_base_x1,
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    lu_x = RequiredUnit(base=required_base_x1, sufffacts={})
    lu_x.set_sufffact(sufffact=required_base_x1)
    requiredunits_x = {lu_x.base: lu_x}
    assert yx1._requiredunits == requiredunits_x
    print(f"{yx1._on_meld_weight_action=}")
    assert yx1._weight == 1


def test_idea_required_meld_TwoRequiredsScenarioWorks():
    # GIVEN
    required_base_x1 = "src,ball,run"
    required_base_x2 = "src,ball,swim"
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(
        idea=yx1,
        required_base=required_base_x1,
        required_sufffact=required_base_x1,
    )

    yx2 = IdeaCore(_desc="spirit")
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
    required_base_x1 = "src,ball,run"
    required_base_x2 = "src,ball,swim"
    yx1 = IdeaCore(_desc="spirit")
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

    yx2 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(
        idea=yx2,
        required_base=required_base_x2,
        required_sufffact=required_base_x2,
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    # lu_x = RequiredUnit(base=required_base_x1, sufffacts={})
    # lu_x.set_sufffact(sufffact=required_base_x1)
    # lu_x.set_sufffact(sufffact=required_base_x2)
    # requiredunits_x = {lu_x.base: lu_x}
    assert len(yx1._requiredunits) == 2
    assert yx1._requiredunits[required_base_x1] != None
    assert yx1._requiredunits[required_base_x2] != None


def test_idea_brandlink_meld_BaseScenarioWorks_on_meld_weight_actionEquals_default():
    # GIVEN
    yx1 = IdeaCore(_desc="spirit")
    br1 = "Running"
    custom_set_idea_attr(idea=yx1, on_meld_weight_action="default")
    custom_set_idea_attr(
        idea=yx1, brandlink=brandlink_shop(name=br1, creditor_weight=2)
    )
    yx2 = IdeaCore(_desc="Rocking")
    custom_set_idea_attr(idea=yx2, on_meld_weight_action="default")
    custom_set_idea_attr(
        idea=yx2, brandlink=brandlink_shop(name=br1, creditor_weight=3)
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    bl_x = brandlink_shop(name=br1, creditor_weight=2)
    assert yx1._brandlinks[br1] == bl_x


def test_idea_brandlink_meld_BaseScenarioWorks_on_meld_weight_actionEquals_sum():
    # GIVEN
    yx1 = IdeaCore(_desc="spirit")
    br1 = "Running"
    custom_set_idea_attr(idea=yx1, on_meld_weight_action="sum")
    custom_set_idea_attr(
        idea=yx1, brandlink=brandlink_shop(name=br1, creditor_weight=2, debtor_weight=3)
    )
    yx2 = IdeaCore(_desc="Rocking")
    custom_set_idea_attr(idea=yx2, on_meld_weight_action="sum")
    custom_set_idea_attr(
        idea=yx2, brandlink=brandlink_shop(name=br1, creditor_weight=2, debtor_weight=3)
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    lu_x = brandlink_shop(name=br1, creditor_weight=4, debtor_weight=6)
    assert yx1._brandlinks[br1] == lu_x


def test_idea_brandlink_meld_TwoBrandsScenarioWorks():
    # GIVEN
    yx1 = IdeaCore(_desc="spirit")
    br1 = "Running"
    custom_set_idea_attr(idea=yx1, on_meld_weight_action="sum")
    custom_set_idea_attr(
        idea=yx1, brandlink=brandlink_shop(name=br1, creditor_weight=2)
    )

    br2 = "Bears"
    yx2 = IdeaCore(_desc="Rocking")
    custom_set_idea_attr(idea=yx1, on_meld_weight_action="sum")
    custom_set_idea_attr(
        idea=yx2, brandlink=brandlink_shop(name=br2, creditor_weight=2)
    )

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    lu_x1 = brandlink_shop(name=br1, creditor_weight=2)
    lu_x2 = brandlink_shop(name=br2, creditor_weight=2)
    assert yx1._brandlinks[br1] == lu_x1
    assert yx1._brandlinks[br2] == lu_x2


def test_idea_acptfactunits_meld_BaseScenarioWorks():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    hc_1 = c_acptfactunit(base=tech_road, pick=bowl_road)
    yx1 = IdeaCore(_desc="spirit")
    yx1.set_acptfactunits_empty_if_null()
    yx1.set_acptfactunit(acptfactunit=hc_1)

    hc_2 = c_acptfactunit(base=tech_road, pick=bowl_road)
    yx2 = IdeaCore(_desc="fun")
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
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    plate_text = "plate"
    plate_road = f"{src},{tech_text},{plate_text}"

    hc_1 = c_acptfactunit(base=tech_road, pick=bowl_road)
    yx1 = IdeaCore(_desc="spirit")
    yx1.set_acptfactunit(acptfactunit=hc_1)

    hc_2 = c_acptfactunit(base=plate_road, pick=plate_road)
    yx2 = IdeaCore(_desc="fun")
    yx2.set_acptfactunit(acptfactunit=hc_2)

    # WHEN
    yx1.meld(other_idea=yx2)

    # THEN
    assert len(yx1._acptfactunits) == 2
    assert len(yx1._acptfactunits) == len(yx2._acptfactunits) + 1
    assert yx1._acptfactunits != yx2._acptfactunits


def test_idea_attributes_meld_Works():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    plate_text = "plate"
    plate_road = f"{src},{tech_text},{plate_text}"

    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(
        idea=yx1,
        uid="test_uid1",
        weight=7,
        begin=1,
        close=2,
        addin=3,
        denom=4,
        numor=5,
        reest=6,
        special_road=plate_road,
        numeric_road=bowl_road,
        promise=True,
        all_ally_credit="testbrand1",
        all_ally_debt="testbrand1",
        is_expanded=True,
    )

    yx2 = IdeaCore(_desc="fun")
    custom_set_idea_attr(
        idea=yx2,
        uid="test_uid1",
        weight=7,
        begin=1,
        close=2,
        addin=3,
        denom=4,
        numor=5,
        reest=6,
        special_road=plate_road,
        numeric_road=bowl_road,
        promise=True,
        all_ally_credit="testbrand1",
        all_ally_debt="testbrand1",
        is_expanded=True,
    )

    # WHEN
    yx1.meld(yx2)

    # THEN
    assert yx1._uid == "test_uid1"
    assert yx1._weight == 7
    assert yx1._begin == 1
    assert yx1._close == 2
    assert yx1._addin == 3
    assert yx1._denom == 4
    assert yx1._numor == 5
    assert yx1._reest == 6
    assert yx1._special_road == plate_road
    assert yx1._numeric_road == bowl_road
    assert yx1.promise == True
    assert yx1._all_ally_credit == "testbrand1"
    assert yx1._all_ally_debt == "testbrand1"
    assert yx1._is_expanded == True


def test_idea_attributes_meld_FailRaisesError_uid():
    x_name = "_uid"
    x_val = "test_uid1"
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, uid=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
    )


def test_idea_attributes_meld_FailRaisesError_begin():
    x_name = "_begin"
    x_val = 77
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, begin=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
    )


def test_idea_attributes_meld_FailRaisesError_close():
    x_name = "_close"
    x_val = 77
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, close=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
    )


def test_idea_attributes_meld_FailRaisesError_addin():
    x_name = "_addin"
    x_val = 77
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, addin=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
    )


def test_idea_attributes_meld_FailRaisesError_denom():
    x_name = "_denom"
    x_val = 15
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, denom=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
    )


def test_idea_attributes_meld_FailRaisesError_numor():
    x_name = "_numor"
    x_val = 77
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, numor=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
    )


def test_idea_attributes_meld_FailRaisesError_reest():
    x_name = "_reest"
    x_val = 77
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, reest=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
    )


def test_idea_attributes_meld_FailRaisesError_special_road():
    x_name = "_special_road"
    x_val = "test_special_road1"
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, special_road=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
    )


def test_idea_attributes_meld_FailRaisesError_numeric_road():
    x_name = "_numeric_road"
    x_val = "test_numeric_road1"
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, numeric_road=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
    )


def test_idea_attributes_meld_FailRaisesError_action():
    x_name = "promise"
    x_val = True
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, promise=x_val)
    yx2 = IdeaCore(_desc="fun")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:False"
    )


# def test_idea_attributes_meld_FailRaisesError_all_ally_credit():
# def test_idea_attributes_meld_FailRaisesError_all_ally_debt():
#     x_name = "_all_ally_credit"
#     x_name = "_all_ally_debt"
#     x_val = "test_all_ally_credit1"
#     x_val = "test_all_ally_debt1"
#     yx1 = IdeaCore(_desc="spirit")
#     custom_set_idea_attr(idea=yx1, all_ally_credit=x_val)
#     custom_set_idea_attr(idea=yx1, all_ally_debt=x_val)
#     yx2 = IdeaCore(_desc="fun")

#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         yx1.meld(yx2)
#     assert (
#         str(excinfo.value)
#         == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:None"
#     )


def test_idea_attributes_meld_FailRaisesError_is_expanded():
    x_name = "_is_expanded"
    x_val = False
    other_val = True
    yx1 = IdeaCore(_desc="spirit")
    custom_set_idea_attr(idea=yx1, is_expanded=x_val)
    yx2 = IdeaCore(_desc="fun")
    custom_set_idea_attr(idea=yx2, is_expanded=other_val)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        yx1.meld(yx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={yx1._walk},{yx1._desc} {x_name}:{x_val} with {yx2._walk},{yx2._desc} {x_name}:True"
    )
