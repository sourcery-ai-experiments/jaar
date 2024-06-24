from src._road.road import RoadUnit
from src._truth.other import (
    OtherID,
    otherlink_shop,
    otherunit_shop,
    OtherUnitExternalMetrics,
)
from src._truth.belief import (
    BeliefID,
    beliefunit_shop,
    balancelink_shop,
    get_intersection_of_others,
)
from src._truth.examples.example_truths import (
    truth_v001 as examples_truth_v001,
    truth_v001_with_large_intent as examples_truth_v001_with_large_intent,
)
from src._truth.truth import TruthUnit, truthunit_shop
from src._truth.idea import ideaunit_shop, IdeaUnit
from pytest import raises as pytest_raises
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


def test_TruthUnit_set_otherunit_SetObjCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_otherunit = otherunit_shop(yao_text)
    deepcopy_yao_otherunit = copy_deepcopy(yao_otherunit)
    slash_text = "/"
    bob_truth = truthunit_shop("Bob", _road_delimiter=slash_text)

    # WHEN
    bob_truth.set_otherunit(otherunit=yao_otherunit)

    # THEN
    assert bob_truth._others.get(yao_text)._road_delimiter == slash_text
    x_others = {yao_otherunit.other_id: deepcopy_yao_otherunit}
    assert bob_truth._others != x_others
    deepcopy_yao_otherunit._road_delimiter = bob_truth._road_delimiter
    assert bob_truth._others == x_others


def test_examples_truth_v001_has_others():
    # GIVEN / WHEN
    yao_truth = examples_truth_v001()

    # THEN
    assert yao_truth._others != None
    assert len(yao_truth._others) == 22


def test_TruthUnit_set_other_CorrectlySets_others_beliefs():
    # GIVEN
    x_pixel = 0.5
    yao_truth = truthunit_shop("Yao", _pixel=x_pixel)
    yao_truth.calc_truth_metrics()
    assert len(yao_truth._others) == 0
    assert len(yao_truth._beliefs) == 0

    # WHEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))

    # THEN
    assert yao_truth._others.get(rico_text)._pixel == x_pixel
    assert len(yao_truth._others) == 3
    assert len(yao_truth._beliefs) == 3
    assert yao_truth._beliefs["rico"]._other_mirror == True

    # WHEN
    rico_belief = rico_text
    carm_belief = carm_text
    patr_belief = patr_text
    yao_truth._idearoot.set_balancelink(balancelink_shop(rico_belief, credor_weight=10))
    yao_truth._idearoot.set_balancelink(balancelink_shop(carm_belief, credor_weight=10))
    yao_truth._idearoot.set_balancelink(balancelink_shop(patr_belief, credor_weight=10))
    assert len(yao_truth._idearoot._balancelinks) == 3


def test_TruthUnit_add_otherunit_CorrectlySets_others():
    # GIVEN
    x_pixel = 0.5
    yao_truth = truthunit_shop("Yao", _pixel=x_pixel)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    # WHEN
    yao_truth.add_otherunit(rico_text, credor_weight=13, debtor_weight=8)
    yao_truth.add_otherunit(carm_text, debtor_weight=5)
    yao_truth.add_otherunit(patr_text, credor_weight=17)

    # THEN
    assert len(yao_truth._others) == 3
    assert len(yao_truth._beliefs) == 3
    assert yao_truth.get_beliefunit(rico_text)._other_mirror == True
    assert yao_truth._others.get(patr_text).credor_weight == 17
    assert yao_truth._others.get(carm_text).debtor_weight == 5
    assert yao_truth._others.get(patr_text)._pixel == x_pixel


def test_TruthUnit_other_exists_ReturnsObj():
    # GIVEN
    bob_truth = truthunit_shop("Bob")
    yao_text = "Yao"

    # WHEN / THEN
    assert bob_truth.other_exists(yao_text) is False

    # GIVEN
    bob_truth.add_otherunit(yao_text)

    # WHEN / THEN
    assert bob_truth.other_exists(yao_text)


def test_TruthUnit_set_other_CorrectlyUpdate_other_mirror_BeliefUnit():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    before_rico_credor = 7
    before_rico_debtor = 17
    yao_truth.add_otherunit(rico_text, before_rico_credor, before_rico_debtor)
    rico_beliefunit = yao_truth.get_beliefunit(rico_text)
    rico_otherlink = rico_beliefunit.get_otherlink(rico_text)
    assert rico_otherlink.credor_weight != before_rico_credor
    assert rico_otherlink.debtor_weight != before_rico_debtor
    assert rico_otherlink.credor_weight == 1
    assert rico_otherlink.debtor_weight == 1

    # WHEN
    after_rico_credor = 11
    after_rico_debtor = 13
    yao_truth.set_otherunit(
        otherunit_shop(rico_text, after_rico_credor, after_rico_debtor)
    )

    # THEN
    assert rico_otherlink.credor_weight != after_rico_credor
    assert rico_otherlink.debtor_weight != after_rico_debtor
    assert rico_otherlink.credor_weight == 1
    assert rico_otherlink.debtor_weight == 1


def test_TruthUnit_edit_other_RaiseExceptionWhenOtherDoesNotExist():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    rico_credor_weight = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_truth.edit_otherunit(rico_text, credor_weight=rico_credor_weight)
    assert str(excinfo.value) == f"OtherUnit '{rico_text}' does not exist."


def test_TruthUnit_edit_other_CorrectlyUpdatesObj():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    old_rico_credor_weight = 55
    old_rico_debtor_weight = 66
    yao_truth.set_otherunit(
        otherunit_shop(
            rico_text,
            old_rico_credor_weight,
            old_rico_debtor_weight,
        )
    )
    rico_otherunit = yao_truth.get_other(rico_text)
    assert rico_otherunit.credor_weight == old_rico_credor_weight
    assert rico_otherunit.debtor_weight == old_rico_debtor_weight

    # WHEN
    new_rico_credor_weight = 22
    new_rico_debtor_weight = 33
    yao_truth.edit_otherunit(
        other_id=rico_text,
        credor_weight=new_rico_credor_weight,
        debtor_weight=new_rico_debtor_weight,
    )

    # THEN
    assert rico_otherunit.credor_weight == new_rico_credor_weight
    assert rico_otherunit.debtor_weight == new_rico_debtor_weight


def test_TruthUnit_get_other_ReturnsCorrectObj():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    yao_truth.add_otherunit(rico_text)
    yao_truth.add_otherunit(carm_text)

    # WHEN
    rico_other = yao_truth.get_other(rico_text)
    carm_other = yao_truth.get_other(carm_text)

    # THEN
    assert rico_other == yao_truth._others.get(rico_text)
    assert carm_other == yao_truth._others.get(carm_text)


def test_TruthUnit_calc_truth_metrics_CorrectlySetsOtherLinkTruthCredAndDebt():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_truth._idearoot.set_balancelink(balancelink=bl_rico)
    yao_truth._idearoot.set_balancelink(balancelink=bl_carm)
    yao_truth._idearoot.set_balancelink(balancelink=bl_patr)

    rico_beliefunit = yao_truth.get_beliefunit(rico_text)
    carm_beliefunit = yao_truth.get_beliefunit(carm_text)
    patr_beliefunit = yao_truth.get_beliefunit(patr_text)
    rico_otherlink = rico_beliefunit._others.get(rico_text)
    carm_otherlink = carm_beliefunit._others.get(carm_text)
    patr_otherlink = patr_beliefunit._others.get(patr_text)
    rico_otherlink._truth_cred is None
    rico_otherlink._truth_debt is None
    carm_otherlink._truth_cred is None
    carm_otherlink._truth_debt is None
    patr_otherlink._truth_cred is None
    patr_otherlink._truth_debt is None

    # for belief in yao_truth._beliefs.values():
    #     for otherlink in belief._others.values():
    #         assert otherlink._truth_cred is None
    #         assert otherlink._truth_debt is None

    yao_truth.calc_truth_metrics()

    # for balancelink in yao_truth._balanceheirs.values():
    #     print(
    #         f"{yao_truth._truth_importance=} {balancelink.belief_id=} {balancelink._truth_cred=} {balancelink._truth_debt=}"
    #     )

    assert rico_otherlink._truth_cred == 0.5
    assert rico_otherlink._truth_debt == 0.8
    assert carm_otherlink._truth_cred == 0.25
    assert carm_otherlink._truth_debt == 0.1
    assert patr_otherlink._truth_cred == 0.25
    assert patr_otherlink._truth_debt == 0.1

    # otherlink_truth_cred_sum = 0.0
    # otherlink_truth_debt_sum = 0.0
    # for belief in yao_truth._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._others=}")

    #     for otherlink in belief._others.values():
    #         assert otherlink._truth_cred != None
    #         assert otherlink._truth_cred in [0.25, 0.5]
    #         assert otherlink._truth_debt != None
    #         assert otherlink._truth_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {otherlink._truth_importance=} {belief._truth_importance=}"
    #         # )
    #         otherlink_truth_cred_sum += otherlink._truth_cred
    #         otherlink_truth_debt_sum += otherlink._truth_debt

    #         # print(f"{otherlink_truth_importance_sum=}")
    # assert otherlink_truth_cred_sum == 1.0
    # assert otherlink_truth_debt_sum == 1.0

    assert (
        rico_otherlink._truth_cred
        + carm_otherlink._truth_cred
        + patr_otherlink._truth_cred
        == 1.0
    )
    assert (
        rico_otherlink._truth_debt
        + carm_otherlink._truth_debt
        + patr_otherlink._truth_debt
        == 1.0
    )

    # WHEN anothher pledge, check metrics are as expected
    selena_text = "selena"
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(selena_text)))
    yao_truth._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            belief_id=BeliefID(selena_text), credor_weight=20, debtor_weight=13
        )
    )
    yao_truth.calc_truth_metrics()

    # THEN
    selena_beliefunit = yao_truth.get_beliefunit(selena_text)
    selena_otherlink = selena_beliefunit._others.get(selena_text)

    assert rico_otherlink._truth_cred != 0.25
    assert rico_otherlink._truth_debt != 0.8
    assert carm_otherlink._truth_cred != 0.25
    assert carm_otherlink._truth_debt != 0.1
    assert patr_otherlink._truth_cred != 0.5
    assert patr_otherlink._truth_debt != 0.1
    assert selena_otherlink._truth_cred != None
    assert selena_otherlink._truth_debt != None

    # otherlink_truth_cred_sum = 0.0
    # otherlink_truth_debt_sum = 0.0

    # for belief in yao_truth._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._others=}")

    #     for otherlink in belief._others.values():
    #         assert otherlink._truth_cred != None
    #         assert otherlink._truth_cred not in [0.25, 0.5]
    #         assert otherlink._truth_debt != None
    #         assert otherlink._truth_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {otherlink._truth_importance=} {belief._truth_importance=}"
    #         # )
    #         otherlink_truth_cred_sum += otherlink._truth_cred
    #         otherlink_truth_debt_sum += otherlink._truth_debt

    #         # print(f"{otherlink_truth_importance_sum=}")
    # assert otherlink_truth_cred_sum == 1.0
    # assert otherlink_truth_debt_sum > 0.9999999
    # assert otherlink_truth_debt_sum < 1.00000001

    assert (
        rico_otherlink._truth_cred
        + carm_otherlink._truth_cred
        + patr_otherlink._truth_cred
        + selena_otherlink._truth_cred
        == 1.0
    )
    assert (
        rico_otherlink._truth_debt
        + carm_otherlink._truth_debt
        + patr_otherlink._truth_debt
        + selena_otherlink._truth_debt
        > 0.9999999
    )
    assert (
        rico_otherlink._truth_debt
        + carm_otherlink._truth_debt
        + patr_otherlink._truth_debt
        + selena_otherlink._truth_debt
        < 1.0
    )


def test_TruthUnit_calc_truth_metrics_CorrectlySetsOtherUnitTruthImportance():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    swim_text = "swim"
    yao_truth.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_truth._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_rico)
    yao_truth._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_carm)
    yao_truth._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_patr)

    rico_otherunit = yao_truth._others.get(rico_text)
    carm_otherunit = yao_truth._others.get(carm_text)
    patr_otherunit = yao_truth._others.get(patr_text)

    assert rico_otherunit._truth_cred == 0
    assert rico_otherunit._truth_debt == 0
    assert carm_otherunit._truth_cred == 0
    assert carm_otherunit._truth_debt == 0
    assert patr_otherunit._truth_cred == 0
    assert patr_otherunit._truth_debt == 0

    # WHEN
    yao_truth.calc_truth_metrics()

    # THEN
    otherunit_truth_cred_sum = 0.0
    otherunit_truth_debt_sum = 0.0

    assert rico_otherunit._truth_cred == 0.5
    assert rico_otherunit._truth_debt == 0.8
    assert carm_otherunit._truth_cred == 0.25
    assert carm_otherunit._truth_debt == 0.1
    assert patr_otherunit._truth_cred == 0.25
    assert patr_otherunit._truth_debt == 0.1

    assert (
        rico_otherunit._truth_cred
        + carm_otherunit._truth_cred
        + patr_otherunit._truth_cred
        == 1.0
    )
    assert (
        rico_otherunit._truth_debt
        + carm_otherunit._truth_debt
        + patr_otherunit._truth_debt
        == 1.0
    )

    # for otherunit in yao_truth._others.values():
    #     assert otherunit._truth_cred != None
    #     assert otherunit._truth_cred in [0.25, 0.5]
    #     assert otherunit._truth_debt != None
    #     assert otherunit._truth_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {otherunit._truth_credor=} {belief._truth_credor=}"
    #     # )
    #     print(f"{otherunit.} {otherunit._truth_cred=} {otherunit._truth_debt=} ")
    #     # print(f"{otherunit_truth_cred_sum=}")
    #     # print(f"{otherunit_truth_debt_sum=}")
    #     otherunit_truth_cred_sum += otherunit._truth_cred
    #     otherunit_truth_debt_sum += otherunit._truth_debt

    # assert otherunit_truth_cred_sum == 1.0
    # assert otherunit_truth_debt_sum > 0.9999999
    # assert otherunit_truth_debt_sum < 1.00000001

    # WHEN anothher pledge, check metrics are as expected
    selena_text = "selena"
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(selena_text)))
    yao_truth._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            belief_id=selena_text, credor_weight=20, debtor_weight=10
        )
    )
    yao_truth.calc_truth_metrics()

    # THEN
    selena_otherunit = yao_truth._others.get(selena_text)

    assert rico_otherunit._truth_cred != 0.5
    assert rico_otherunit._truth_debt != 0.8
    assert carm_otherunit._truth_cred != 0.25
    assert carm_otherunit._truth_debt != 0.1
    assert patr_otherunit._truth_cred != 0.25
    assert patr_otherunit._truth_debt != 0.1
    assert selena_otherunit._truth_cred != None
    assert selena_otherunit._truth_debt != None

    assert (
        rico_otherunit._truth_cred
        + carm_otherunit._truth_cred
        + patr_otherunit._truth_cred
        < 1.0
    )
    assert (
        rico_otherunit._truth_cred
        + carm_otherunit._truth_cred
        + patr_otherunit._truth_cred
        + selena_otherunit._truth_cred
        == 1.0
    )
    assert (
        rico_otherunit._truth_debt
        + carm_otherunit._truth_debt
        + patr_otherunit._truth_debt
        < 1.0
    )
    assert (
        rico_otherunit._truth_debt
        + carm_otherunit._truth_debt
        + patr_otherunit._truth_debt
        + selena_otherunit._truth_debt
        == 1.0
    )

    # otherunit_truth_cred_sum = 0.0
    # otherunit_truth_debt_sum = 0.0

    # for otherunit in yao_truth._others.values():
    #     assert otherunit._truth_cred != None
    #     assert otherunit._truth_cred not in [0.25, 0.5]
    #     assert otherunit._truth_debt != None
    #     assert otherunit._truth_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {otherunit._truth_credor=} {belief._truth_credor=}"
    #     # )
    #     print(f"{otherunit.} {otherunit._truth_cred=} {otherunit._truth_debt=} ")
    #     # print(f"{otherunit_truth_cred_sum=}")
    #     # print(f"{otherunit_truth_debt_sum=}")
    #     otherunit_truth_cred_sum += otherunit._truth_cred
    #     otherunit_truth_debt_sum += otherunit._truth_debt

    # assert otherunit_truth_cred_sum == 1.0
    # assert otherunit_truth_debt_sum > 0.9999999
    # assert otherunit_truth_debt_sum < 1.00000001


def test_TruthUnit_calc_truth_metrics_CorrectlySetsPartBeliefedLWOtherUnitTruthImportance():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    swim_text = "swim"
    yao_truth.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_truth._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_rico)
    yao_truth._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_carm)
    yao_truth._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_patr)

    # no balancelinks attached to this one
    hunt_text = "hunt"
    yao_truth.add_l1_idea(ideaunit_shop(hunt_text, _weight=3))

    # WHEN
    yao_truth.calc_truth_metrics()

    # THEN
    rico_beliefunit = yao_truth.get_beliefunit(rico_text)
    carm_beliefunit = yao_truth.get_beliefunit(carm_text)
    patr_beliefunit = yao_truth.get_beliefunit(patr_text)
    assert rico_beliefunit._truth_cred != 0.5
    assert rico_beliefunit._truth_debt != 0.8
    assert carm_beliefunit._truth_cred != 0.25
    assert carm_beliefunit._truth_debt != 0.1
    assert patr_beliefunit._truth_cred != 0.25
    assert patr_beliefunit._truth_debt != 0.1
    assert (
        rico_beliefunit._truth_cred
        + carm_beliefunit._truth_cred
        + patr_beliefunit._truth_cred
        == 0.25
    )
    assert (
        rico_beliefunit._truth_debt
        + carm_beliefunit._truth_debt
        + patr_beliefunit._truth_debt
        == 0.25
    )

    # beliefunit_truth_cred_sum = 0.0
    # beliefunit_truth_debt_sum = 0.0
    # for beliefunit in yao_truth._beliefs.values():
    #     assert beliefunit._truth_cred != None
    #     assert beliefunit._truth_cred not in [0.25, 0.5]
    #     assert beliefunit._truth_debt != None
    #     assert beliefunit._truth_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {beliefunit._truth_credor=} {belief._truth_credor=}"
    #     # )
    #     print(f"{beliefunit.belief_id=} {beliefunit._truth_cred=} {beliefunit._truth_debt=} ")
    #     # print(f"{beliefunit_truth_cred_sum=}")
    #     # print(f"{beliefunit_truth_debt_sum=}")
    #     beliefunit_truth_cred_sum += beliefunit._truth_cred
    #     beliefunit_truth_debt_sum += beliefunit._truth_debt
    # assert beliefunit_truth_cred_sum == 0.25
    # assert beliefunit_truth_debt_sum == 0.25

    rico_otherunit = yao_truth._others.get(rico_text)
    carm_otherunit = yao_truth._others.get(carm_text)
    patr_otherunit = yao_truth._others.get(patr_text)

    assert rico_otherunit._truth_cred == 0.375
    assert rico_otherunit._truth_debt == 0.45
    assert carm_otherunit._truth_cred == 0.3125
    assert carm_otherunit._truth_debt == 0.275
    assert patr_otherunit._truth_cred == 0.3125
    assert patr_otherunit._truth_debt == 0.275

    assert (
        rico_otherunit._truth_cred
        + carm_otherunit._truth_cred
        + patr_otherunit._truth_cred
        == 1.0
    )
    assert (
        rico_otherunit._truth_debt
        + carm_otherunit._truth_debt
        + patr_otherunit._truth_debt
        == 1.0
    )

    # otherunit_truth_cred_sum = 0.0
    # otherunit_truth_debt_sum = 0.0
    # for otherunit in yao_truth._others.values():
    #     assert otherunit._truth_cred != None
    #     assert otherunit._truth_cred not in [0.25, 0.5]
    #     assert otherunit._truth_debt != None
    #     assert otherunit._truth_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {otherunit._truth_credor=} {belief._truth_credor=}"
    #     # )
    #     print(f"{otherunit.} {otherunit._truth_cred=} {otherunit._truth_debt=} ")
    #     # print(f"{otherunit_truth_cred_sum=}")
    #     # print(f"{otherunit_truth_debt_sum=}")
    #     otherunit_truth_cred_sum += otherunit._truth_cred
    #     otherunit_truth_debt_sum += otherunit._truth_debt
    # assert otherunit_truth_cred_sum == 1.0
    # assert otherunit_truth_debt_sum > 0.9999999
    # assert otherunit_truth_debt_sum < 1.00000001


def test_TruthUnit_calc_truth_metrics_CorrectlySetsOtherAttrs():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    yao_truth.add_l1_idea(ideaunit_shop("swim"))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.set_otherunit(
        otherunit=otherunit_shop(OtherID(rico_text), credor_weight=8)
    )
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    rico_otherunit = yao_truth._others.get(rico_text)
    carm_otherunit = yao_truth._others.get(carm_text)
    patr_otherunit = yao_truth._others.get(patr_text)
    assert rico_otherunit._truth_cred == 0
    assert rico_otherunit._truth_debt == 0
    assert carm_otherunit._truth_cred == 0
    assert carm_otherunit._truth_debt == 0
    assert patr_otherunit._truth_cred == 0
    assert patr_otherunit._truth_debt == 0

    # WHEN
    yao_truth.calc_truth_metrics()

    # THEN
    assert (
        rico_otherunit._truth_cred
        + carm_otherunit._truth_cred
        + patr_otherunit._truth_cred
        == 1.0
    )
    assert (
        rico_otherunit._truth_debt
        + carm_otherunit._truth_debt
        + patr_otherunit._truth_debt
        == 1.0
    )
    # otherunit_truth_cred_sum = 0.0
    # otherunit_truth_debt_sum = 0.0
    # for otherunit in yao_truth._others.values():
    #     assert otherunit._truth_cred != None
    #     assert otherunit._truth_cred not in [0.25, 0.5]
    #     assert otherunit._truth_debt != None
    #     assert otherunit._truth_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {otherunit._truth_credor=} {belief._truth_credor=}"
    #     # )
    #     print(f"{otherunit.} {otherunit._truth_cred=} {otherunit._truth_debt=} ")
    #     # print(f"{otherunit_truth_cred_sum=}")
    #     # print(f"{otherunit_truth_debt_sum=}")
    #     otherunit_truth_cred_sum += otherunit._truth_cred
    #     otherunit_truth_debt_sum += otherunit._truth_debt
    # assert otherunit_truth_cred_sum == 1.0
    # assert otherunit_truth_debt_sum > 0.9999999
    # assert otherunit_truth_debt_sum < 1.00000001


def test_TruthUnit_calc_truth_metrics_RaisesErrorWhen_is_otherunits_credor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_truth = truthunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_credor_weight = 20
    carm_credor_weight = 30
    patr_credor_weight = 50
    yao_truth.set_otherunit(otherunit_shop(rico_text, None, rico_credor_weight))
    yao_truth.set_otherunit(otherunit_shop(carm_text, None, carm_credor_weight))
    yao_truth.set_otherunit(otherunit_shop(patr_text, None, patr_credor_weight))
    assert yao_truth._other_credor_pool is None
    assert yao_truth.is_otherunits_credor_weight_sum_correct()
    assert yao_truth.calc_truth_metrics() is None

    # WHEN
    x_int = 13
    yao_truth.set_other_credor_pool(x_int)
    assert yao_truth.is_otherunits_credor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_truth.calc_truth_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_otherunits_credor_weight_sum_correct is False. _other_credor_pool={x_int}. otherunits_credor_weight_sum={yao_truth.get_otherunits_credor_weight_sum()}"
    )

    # WHEN / THEN
    yao_truth.set_other_credor_pool(yao_truth.get_otherunits_credor_weight_sum())
    assert yao_truth.calc_truth_metrics() is None


def test_TruthUnit_calc_truth_metrics_DoesNotRaiseError_other_credor_poolWhenOtherSumIsZero():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    assert yao_truth._other_credor_pool is None
    assert yao_truth.is_otherunits_credor_weight_sum_correct()
    assert yao_truth.calc_truth_metrics() is None

    # WHEN
    x_int = 13
    yao_truth.set_other_credor_pool(x_int)

    # THEN
    assert yao_truth.is_otherunits_credor_weight_sum_correct()
    yao_truth.calc_truth_metrics()


def test_TruthUnit_calc_truth_metrics_RaisesErrorWhen_is_otherunits_debtor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_truth = truthunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 40
    yao_truth.set_otherunit(otherunit_shop(rico_text, None, None, rico_debtor_weight))
    yao_truth.set_otherunit(otherunit_shop(carm_text, None, None, carm_debtor_weight))
    yao_truth.set_otherunit(otherunit_shop(patr_text, None, None, patr_debtor_weight))
    assert yao_truth._other_debtor_pool is None
    assert yao_truth.is_otherunits_debtor_weight_sum_correct()
    assert yao_truth.calc_truth_metrics() is None

    # WHEN
    x_int = 13
    yao_truth.set_other_debtor_pool(x_int)
    assert yao_truth.is_otherunits_debtor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_truth.calc_truth_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_otherunits_debtor_weight_sum_correct is False. _other_debtor_pool={x_int}. otherunits_debtor_weight_sum={yao_truth.get_otherunits_debtor_weight_sum()}"
    )

    # WHEN / THEN
    yao_truth.set_other_debtor_pool(yao_truth.get_otherunits_debtor_weight_sum())
    assert yao_truth.calc_truth_metrics() is None


def test_TruthUnit_calc_truth_metrics_DoesNotRaiseError_other_debtor_poolWhenOtherSumIsZero():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    assert yao_truth._other_credor_pool is None
    assert yao_truth.is_otherunits_debtor_weight_sum_correct()
    assert yao_truth.calc_truth_metrics() is None

    # WHEN
    x_int = 13
    yao_truth.set_other_debtor_pool(x_int)

    # THEN
    assert yao_truth.is_otherunits_debtor_weight_sum_correct()
    yao_truth.calc_truth_metrics()


def clear_all_otherunits_beliefunits_truth_intent_cred_debt(x_truth: TruthUnit):
    # DELETE truth_intent_debt and truth_intent_cred
    for beliefunit_x in x_truth._beliefs.values():
        beliefunit_x.reset_truth_cred_debt()
        # for otherlink_x in beliefunit_x._others.values():
        #     print(f"{beliefunit_x.belief_id=} {otherlink_x.credor_weight=}  {otherlink_x._truth_cred:.6f} {otherlink_x.debtor_weight=} {otherlink_x._truth_debt:.6f} {otherlink_x.} ")

    # DELETE truth_intent_debt and truth_intent_cred
    for x_otherunit in x_truth._others.values():
        x_otherunit.reset_truth_cred_debt()


@dataclass
class BeliefIntentMetrics:
    sum_beliefunit_cred: float = 0
    sum_beliefunit_debt: float = 0
    sum_otherlink_cred: float = 0
    sum_otherlink_debt: float = 0
    otherlink_count: int = 0

    def set_sums(self, x_truth: TruthUnit):
        for beliefunit_x in x_truth._beliefs.values():
            self.sum_beliefunit_cred += beliefunit_x._truth_intent_cred
            self.sum_beliefunit_debt += beliefunit_x._truth_intent_debt
            for otherlink_x in beliefunit_x._others.values():
                self.sum_otherlink_cred += otherlink_x._truth_intent_cred
                self.sum_otherlink_debt += otherlink_x._truth_intent_debt
                self.otherlink_count += 1


@dataclass
class OtherIntentMetrics:
    sum_intent_cred: float = 0
    sum_intent_debt: float = 0
    sum_intent_ratio_cred: float = 0
    sum_intent_ratio_debt: float = 0

    def set_sums(self, x_truth: TruthUnit):
        for otherunit in x_truth._others.values():
            self.sum_intent_cred += otherunit._truth_intent_cred
            self.sum_intent_debt += otherunit._truth_intent_debt
            self.sum_intent_ratio_cred += otherunit._truth_intent_ratio_cred
            self.sum_intent_ratio_debt += otherunit._truth_intent_ratio_debt


@dataclass
class BalanceIntentMetrics:
    sum_truth_intent_importance = 0
    intent_no_count = 0
    intent_yes_count = 0
    intent_no_truth_i_sum = 0
    intent_yes_truth_i_sum = 0

    def set_sums(self, intent_dict: dict[RoadUnit:IdeaUnit]):
        for intent_item in intent_dict.values():
            self.sum_truth_intent_importance += intent_item._truth_importance
            if intent_item._balancelines == {}:
                self.intent_no_count += 1
                self.intent_no_truth_i_sum += intent_item._truth_importance
            else:
                self.intent_yes_count += 1
                self.intent_yes_truth_i_sum += intent_item._truth_importance


def test_TruthUnit_intent_cred_debt_IsCorrectlySet():
    # GIVEN
    x_truth = examples_truth_v001_with_large_intent()
    clear_all_otherunits_beliefunits_truth_intent_cred_debt(x_truth=x_truth)

    # TEST truth_intent_debt and truth_intent_cred are empty
    x_beliefintentmetrics = BeliefIntentMetrics()
    x_beliefintentmetrics.set_sums(x_truth=x_truth)
    assert x_beliefintentmetrics.sum_beliefunit_cred == 0
    assert x_beliefintentmetrics.sum_beliefunit_debt == 0
    assert x_beliefintentmetrics.sum_otherlink_cred == 0
    assert x_beliefintentmetrics.sum_otherlink_debt == 0

    # TEST truth_intent_debt and truth_intent_cred are empty
    x_otherintentmetrics = OtherIntentMetrics()
    x_otherintentmetrics.set_sums(x_truth=x_truth)
    assert x_otherintentmetrics.sum_intent_cred == 0
    assert x_otherintentmetrics.sum_intent_debt == 0
    assert x_otherintentmetrics.sum_intent_ratio_cred == 0
    assert x_otherintentmetrics.sum_intent_ratio_debt == 0

    # WHEN
    intent_dict = x_truth.get_intent_dict()

    # THEN
    assert len(intent_dict) == 63
    x_balanceintentmetrics = BalanceIntentMetrics()
    x_balanceintentmetrics.set_sums(intent_dict=intent_dict)
    # print(f"{sum_truth_intent_importance=}")
    assert x_balanceintentmetrics.intent_no_count == 14
    assert x_balanceintentmetrics.intent_yes_count == 49
    assert x_balanceintentmetrics.intent_no_truth_i_sum == 0.0037472680016539662
    assert x_balanceintentmetrics.intent_yes_truth_i_sum == 0.0027965049894874455
    assert are_equal(
        x_balanceintentmetrics.intent_no_truth_i_sum
        + x_balanceintentmetrics.intent_yes_truth_i_sum,
        x_balanceintentmetrics.sum_truth_intent_importance,
    )
    assert x_balanceintentmetrics.sum_truth_intent_importance == 0.006543772991141412

    x_beliefintentmetrics = BeliefIntentMetrics()
    x_beliefintentmetrics.set_sums(x_truth=x_truth)
    assert x_beliefintentmetrics.otherlink_count == 81
    x_sum = 0.0027965049894874455
    assert are_equal(x_beliefintentmetrics.sum_beliefunit_cred, x_sum)
    assert are_equal(x_beliefintentmetrics.sum_beliefunit_debt, x_sum)
    assert are_equal(x_beliefintentmetrics.sum_otherlink_cred, x_sum)
    assert are_equal(x_beliefintentmetrics.sum_otherlink_debt, x_sum)
    assert are_equal(
        x_balanceintentmetrics.intent_yes_truth_i_sum,
        x_beliefintentmetrics.sum_beliefunit_cred,
    )

    assert all_otherunits_have_legitimate_values(x_truth)

    x_otherintentmetrics = OtherIntentMetrics()
    x_otherintentmetrics.set_sums(x_truth=x_truth)
    assert are_equal(
        x_otherintentmetrics.sum_intent_cred,
        x_balanceintentmetrics.sum_truth_intent_importance,
    )
    assert are_equal(
        x_otherintentmetrics.sum_intent_debt,
        x_balanceintentmetrics.sum_truth_intent_importance,
    )
    assert are_equal(x_otherintentmetrics.sum_intent_ratio_cred, 1)
    assert are_equal(x_otherintentmetrics.sum_intent_ratio_debt, 1)

    # otherunit_truth_cred_sum = 0.0
    # otherunit_truth_debt_sum = 0.0

    # assert otherunit_truth_cred_sum == 1.0
    # assert otherunit_truth_debt_sum > 0.9999999
    # assert otherunit_truth_debt_sum < 1.00000001


def all_otherunits_have_legitimate_values(x_truth: TruthUnit):
    return not any(
        (
            otherunit._truth_cred is None
            or otherunit._truth_cred in [0.25, 0.5]
            or otherunit._truth_debt is None
            or otherunit._truth_debt in [0.8, 0.1]
        )
        for otherunit in x_truth._others.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000000001
    return abs(x1 - x2) < e10


def test_TruthUnit_intent_ratio_cred_debt_IsCorrectlySetWhenTruthIsEmpty():
    # GIVEN
    noa_truth = truthunit_shop("Noa")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_other = otherunit_shop(rico_text, credor_weight=0.5, debtor_weight=2)
    carm_other = otherunit_shop(carm_text, credor_weight=1.5, debtor_weight=3)
    patr_other = otherunit_shop(patr_text, credor_weight=8, debtor_weight=5)
    noa_truth.set_otherunit(otherunit=rico_other)
    noa_truth.set_otherunit(otherunit=carm_other)
    noa_truth.set_otherunit(otherunit=patr_other)
    noa_truth_rico_other = noa_truth._others.get(rico_text)
    noa_truth_carm_other = noa_truth._others.get(carm_text)
    noa_truth_patr_other = noa_truth._others.get(patr_text)

    assert noa_truth_rico_other._truth_intent_cred in [0, None]
    assert noa_truth_rico_other._truth_intent_debt in [0, None]
    assert noa_truth_carm_other._truth_intent_cred in [0, None]
    assert noa_truth_carm_other._truth_intent_debt in [0, None]
    assert noa_truth_patr_other._truth_intent_cred in [0, None]
    assert noa_truth_patr_other._truth_intent_debt in [0, None]
    assert noa_truth_rico_other._truth_intent_ratio_cred != 0.05
    assert noa_truth_rico_other._truth_intent_ratio_debt != 0.2
    assert noa_truth_carm_other._truth_intent_ratio_cred != 0.15
    assert noa_truth_carm_other._truth_intent_ratio_debt != 0.3
    assert noa_truth_patr_other._truth_intent_ratio_cred != 0.8
    assert noa_truth_patr_other._truth_intent_ratio_debt != 0.5

    # WHEN
    noa_truth.calc_truth_metrics()

    # THEN
    assert noa_truth_rico_other._truth_intent_cred == 0
    assert noa_truth_rico_other._truth_intent_debt == 0
    assert noa_truth_carm_other._truth_intent_cred == 0
    assert noa_truth_carm_other._truth_intent_debt == 0
    assert noa_truth_patr_other._truth_intent_cred == 0
    assert noa_truth_patr_other._truth_intent_debt == 0
    assert noa_truth_rico_other._truth_intent_ratio_cred == 0.05
    assert noa_truth_rico_other._truth_intent_ratio_debt == 0.2
    assert noa_truth_carm_other._truth_intent_ratio_cred == 0.15
    assert noa_truth_carm_other._truth_intent_ratio_debt == 0.3
    assert noa_truth_patr_other._truth_intent_ratio_cred == 0.8
    assert noa_truth_patr_other._truth_intent_ratio_debt == 0.5


def test_TruthUnit_get_other_belief_ids_ReturnsCorrectObj():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))

    # WHEN / THEN
    assert yao_truth.get_other_belief_ids(carm_text) == [carm_text]

    # WHEN / THEN
    swimmers = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swimmers)
    swim_belief.set_otherlink(otherlink_shop(carm_text))
    yao_truth.set_beliefunit(swim_belief)
    assert yao_truth.get_other_belief_ids(carm_text) == [carm_text, swimmers]


def test_TruthUnit_edit_otherunit_other_id_CorrectlyModifiesOtherUnit_other_id():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    yao_truth.add_otherunit(rico_text, credor_weight=13)
    yao_truth.add_otherunit("carmen")
    yao_truth.add_otherunit("patrick", credor_weight=17)
    assert len(yao_truth._others) == 3
    assert yao_truth._others.get(rico_text) != None
    assert yao_truth._others.get(rico_text).credor_weight == 13
    assert len(yao_truth._beliefs) == 3
    assert yao_truth.get_beliefunit(rico_text) != None
    assert yao_truth.get_beliefunit(rico_text)._other_mirror == True

    # WHEN
    beto_text = "beta"
    yao_truth.edit_otherunit_other_id(
        old_other_id=rico_text,
        new_other_id=beto_text,
        allow_other_overwite=False,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_truth._others.get(beto_text) != None
    assert yao_truth._others.get(beto_text).credor_weight == 13
    assert yao_truth._others.get(rico_text) is None
    assert len(yao_truth._others) == 3
    assert len(yao_truth._beliefs) == 3
    assert yao_truth.get_beliefunit(rico_text) is None
    assert yao_truth.get_beliefunit(beto_text) != None
    assert yao_truth.get_beliefunit(beto_text)._other_mirror == True


def test_TruthUnit_OtherUnit_raiseErrorNewother_idPreviouslyExists():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    yao_truth.add_otherunit(rico_text, credor_weight=13)
    carmen_text = "carmen"
    yao_truth.add_otherunit(carmen_text)
    yao_truth.add_otherunit("patrick", credor_weight=17)
    assert len(yao_truth._others) == 3
    assert yao_truth._others.get(rico_text) != None
    assert yao_truth._others.get(rico_text).credor_weight == 13
    assert len(yao_truth._beliefs) == 3
    assert yao_truth.get_beliefunit(rico_text) != None
    assert yao_truth.get_beliefunit(rico_text)._other_mirror == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_truth.edit_otherunit_other_id(
            old_other_id=rico_text,
            new_other_id=carmen_text,
            allow_other_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Other '{rico_text}' modify to '{carmen_text}' failed since '{carmen_text}' exists."
    )


def test_TruthUnit_OtherUnit_CorrectlyModifiesBeliefUnitOtherLinks():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.add_otherunit(rico_text, credor_weight=13)
    yao_truth.add_otherunit(carm_text)
    yao_truth.add_otherunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_other_dict = {OtherID(carm_text): otherlink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _others=carmen_other_dict)
    swim_belief.set_otherlink(
        otherlink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_otherlink(
        otherlink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_truth.set_beliefunit(y_beliefunit=swim_belief)

    swim_belief = yao_truth.get_beliefunit(swim_text)
    assert len(swim_belief._others) == 2
    assert swim_belief.get_otherlink(rico_text) != None
    assert swim_belief.get_otherlink(rico_text).credor_weight == 7
    assert swim_belief.get_otherlink(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    yao_truth.edit_otherunit_other_id(
        old_other_id=rico_text,
        new_other_id=beto_text,
        allow_other_overwite=False,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert swim_belief.get_otherlink(beto_text) != None
    assert swim_belief.get_otherlink(beto_text).credor_weight == 7
    assert swim_belief.get_otherlink(beto_text).debtor_weight == 30
    assert swim_belief.get_otherlink(rico_text) is None
    assert len(swim_belief._others) == 2


def test_TruthUnit_OtherUnit_CorrectlyMergesother_ids():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.add_otherunit(rico_text, credor_weight=13)
    yao_truth.add_otherunit(carm_text, credor_weight=3)
    yao_truth.add_otherunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_other_dict = {OtherID(carm_text): otherlink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _others=carmen_other_dict)
    swim_belief.set_otherlink(
        otherlink=otherlink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_otherlink(
        otherlink=otherlink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_truth.set_beliefunit(y_beliefunit=swim_belief)

    assert len(yao_truth._others) == 3
    assert yao_truth._others.get(rico_text) != None
    assert yao_truth._others.get(rico_text).credor_weight == 13
    assert yao_truth._others.get(carm_text) != None
    assert yao_truth._others.get(carm_text).credor_weight == 3

    # WHEN / THEN
    yao_truth.edit_otherunit_other_id(
        old_other_id=rico_text,
        new_other_id=carm_text,
        allow_other_overwite=True,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_truth._others.get(carm_text) != None
    assert yao_truth._others.get(carm_text).credor_weight == 16
    assert yao_truth._others.get(rico_text) is None
    assert len(yao_truth._others) == 2


def test_TruthUnit_OtherUnit_CorrectlyMergesBeliefUnitOtherLinks():
    # GIVEN
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.add_otherunit(rico_text, credor_weight=13)
    yao_truth.add_otherunit(carm_text)
    yao_truth.add_otherunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_other_dict = {OtherID(carm_text): otherlink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _others=carmen_other_dict)
    swim_belief.set_otherlink(
        otherlink=otherlink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_otherlink(
        otherlink=otherlink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_truth.set_beliefunit(y_beliefunit=swim_belief)

    swim_belief = yao_truth.get_beliefunit(swim_text)
    assert len(swim_belief._others) == 2
    assert swim_belief.get_otherlink(rico_text) != None
    assert swim_belief.get_otherlink(rico_text).credor_weight == 7
    assert swim_belief.get_otherlink(rico_text).debtor_weight == 30
    assert swim_belief.get_otherlink(carm_text) != None
    assert swim_belief.get_otherlink(carm_text).credor_weight == 5
    assert swim_belief.get_otherlink(carm_text).debtor_weight == 18

    # WHEN
    yao_truth.edit_otherunit_other_id(
        old_other_id=rico_text,
        new_other_id=carm_text,
        allow_other_overwite=True,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert swim_belief.get_otherlink(carm_text) != None
    assert swim_belief.get_otherlink(carm_text).credor_weight == 12
    assert swim_belief.get_otherlink(carm_text).debtor_weight == 48
    assert swim_belief.get_otherlink(rico_text) is None
    assert len(swim_belief._others) == 1


def test_TruthUnit_OtherUnit_raiseErrorNewPersonIDBeliefUnitPreviouslyExists():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    yao_truth.add_otherunit(rico_text, credor_weight=13)
    anna_text = "anna"
    yao_truth.add_otherunit(anna_text, credor_weight=17)
    carmen_text = ",carmen"
    carmen_belief = beliefunit_shop(belief_id=carmen_text)
    carmen_belief.set_otherlink(otherlink=otherlink_shop(rico_text))
    carmen_belief.set_otherlink(otherlink=otherlink_shop(anna_text))
    yao_truth.set_beliefunit(y_beliefunit=carmen_belief)
    assert len(yao_truth._beliefs) == 3
    assert yao_truth._others.get(carmen_text) is None
    assert yao_truth.get_beliefunit(carmen_text)._other_mirror is False
    assert len(yao_truth.get_beliefunit(carmen_text)._others) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_truth.edit_otherunit_other_id(
            old_other_id=rico_text,
            new_other_id=carmen_text,
            allow_other_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Other '{rico_text}' modify to '{carmen_text}' failed since non-single belief '{carmen_text}' exists."
    )


# def test_TruthUnit_OtherUnit_CorrectlyOverwriteNewPersonIDBeliefUnit():
#     # GIVEN
#     yao_truth = truthunit_shop("Yao")
#     rico_text = "rico"
#     yao_truth.add_otherunit(rico_text, credor_weight=13)
#     anna_text = "anna"
#     yao_truth.add_otherunit(anna_text, credor_weight=17)
#     carmen_text = ",carmen"
#     carmen_belief = beliefunit_shop(belief_id=carmen_text)
#     carmen_belief.set_otherlink(
#         otherlink=otherlink_shop(rico_text, credor_weight=3)
#     )
#     carmen_belief.set_otherlink(
#         otherlink=otherlink_shop(anna_text, credor_weight=5)
#     )
#     yao_truth.set_beliefunit(y_beliefunit=carmen_belief)
#     assert len(yao_truth._beliefs) == 3
#     assert yao_truth._others.get(rico_text) != None
#     assert yao_truth._others.get(carmen_text) is None
#     assert yao_truth.get_beliefunit(carmen_text)._other_mirror is False
#     assert len(yao_truth.get_beliefunit(carmen_text)._others) == 2
#     assert (
#         yao_truth.get_beliefunit(carmen_text)._others.get(anna_text).credor_weight
#         == 5
#     )
#     assert (
#         yao_truth.get_beliefunit(carmen_text)._others.get(rico_text).credor_weight
#         == 3
#     )

#     # WHEN
#     yao_truth.edit_otherunit_other_id(
#         old_rico_text,
#         new_carmen_text,
#         allow_other_overwite=False,
#         allow_nonsingle_belief_overwrite=True,
#     )

#     assert len(yao_truth._beliefs) == 2
#     assert yao_truth._others.get(rico_text) is None
#     assert yao_truth._others.get(carmen_text) != None
#     assert yao_truth.get_beliefunit(carmen_text)._other_mirror == True
#     assert len(yao_truth.get_beliefunit(carmen_text)._others) == 1
#     assert yao_truth.get_beliefunit(carmen_text)._others.get(rico_text) is None
#     assert (
#         yao_truth.get_beliefunit(carmen_text)._others.get(carmen_text).credor_weight
#         == 1
#     )


def test_TruthUnit_get_otherunits_other_id_list_ReturnsListOfOtherUnits():
    # GIVEN
    noa_truth = truthunit_shop("Noa")
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    noa_truth.set_otherunit(otherunit=otherunit_shop(sam_text))
    noa_truth.set_otherunit(otherunit=otherunit_shop(will_text))
    noa_truth.set_otherunit(otherunit=otherunit_shop(fry_text))
    fun_text = ",fun people"
    fun_belief = beliefunit_shop(belief_id=fun_text)
    fun_belief.set_otherlink(otherlink=otherlink_shop(will_text))
    noa_truth.set_beliefunit(y_beliefunit=fun_belief)
    assert len(noa_truth._beliefs) == 4
    assert len(noa_truth._others) == 3

    # WHEN
    otherunit_list_x = noa_truth.get_otherunits_other_id_list()

    # THEN
    assert len(otherunit_list_x) == 4
    assert otherunit_list_x[0] == ""
    assert otherunit_list_x[1] == fry_text
    assert otherunit_list_x[2] == sam_text
    assert otherunit_list_x[3] == will_text


def test_get_intersection_of_others_ReturnsUnionOfKeysOfTwoDictionarys_scenario1():
    # GIVEN
    bob_text = "Bob"
    bob_truth = truthunit_shop(bob_text)

    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "Elu"
    bob_truth.set_otherunit(otherunit=otherunit_shop(bob_text))
    bob_truth.set_otherunit(otherunit=otherunit_shop(sam_text))
    bob_truth.set_otherunit(otherunit=otherunit_shop(wil_text))
    bob_truth.set_otherunit(otherunit=otherunit_shop(fry_text))

    y_truth = truthunit_shop()
    y_truth.set_otherunit(otherunit=otherunit_shop(bob_text))
    y_truth.set_otherunit(otherunit=otherunit_shop(wil_text))
    y_truth.set_otherunit(otherunit=otherunit_shop(fry_text))
    y_truth.set_otherunit(otherunit=otherunit_shop(elu_text))

    # WHEN
    print(f"{len(bob_truth._others)=} {len(y_truth._others)=}")
    intersection_x = get_intersection_of_others(bob_truth._others, y_truth._others)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}


def test_TruthUnit_clear_output_truth_meld_orders_CorrectlyClearsAttrs():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    rico_otherunit = yao_truth.get_other(rico_text)
    carm_otherunit = yao_truth.get_other(carm_text)
    patr_otherunit = yao_truth.get_other(patr_text)
    rico_otherunit.set_output_truth_meld_order(3)
    carm_otherunit.set_output_truth_meld_order(4)
    patr_otherunit.set_output_truth_meld_order(5)

    assert rico_otherunit._output_truth_meld_order != None
    assert carm_otherunit._output_truth_meld_order != None
    assert patr_otherunit._output_truth_meld_order != None

    # WHEN
    yao_truth.clear_others_output_truth_meld_order()

    # THEN
    assert rico_otherunit._output_truth_meld_order is None
    assert carm_otherunit._output_truth_meld_order is None
    assert patr_otherunit._output_truth_meld_order is None


def test_TruthUnit_clear_output_truth_meld_orders_WithNoArgsCorrectlySetOrder():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_truth.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    rico_otherunit = yao_truth.get_other(rico_text)
    carm_otherunit = yao_truth.get_other(carm_text)
    patr_otherunit = yao_truth.get_other(patr_text)
    assert rico_otherunit._output_truth_meld_order is None
    assert carm_otherunit._output_truth_meld_order is None
    assert patr_otherunit._output_truth_meld_order is None

    # WHEN
    yao_truth.set_others_output_truth_meld_order()

    # THEN
    assert rico_otherunit._output_truth_meld_order != None
    assert carm_otherunit._output_truth_meld_order != None
    assert patr_otherunit._output_truth_meld_order != None
    print(f"{rico_otherunit._output_truth_meld_order=}")
    print(f"{carm_otherunit._output_truth_meld_order=}")
    print(f"{patr_otherunit._output_truth_meld_order=}")
    assert rico_otherunit._output_truth_meld_order == 2
    assert carm_otherunit._output_truth_meld_order == 0
    assert patr_otherunit._output_truth_meld_order == 1


def test_TruthUnit_is_otherunits_credor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_credor_weight = 20
    carm_credor_weight = 30
    patr_credor_weight = 50
    yao_truth.set_otherunit(otherunit_shop(rico_text, rico_credor_weight))
    yao_truth.set_otherunit(otherunit_shop(carm_text, carm_credor_weight))
    yao_truth.set_otherunit(otherunit_shop(patr_text, patr_credor_weight))
    # print(f"{yao_truth._others.keys()=}")
    # for x_otherunit in yao_truth._others.values():
    #     print(f"{x_otherunit.credor_weight=}")

    # WHEN / THEN
    assert yao_truth.is_otherunits_credor_weight_sum_correct()
    yao_truth.set_other_credor_pool(13)
    assert yao_truth.is_otherunits_credor_weight_sum_correct() is False
    # WHEN / THEN
    yao_other_cred_pool = rico_credor_weight + carm_credor_weight + patr_credor_weight
    yao_truth.set_other_credor_pool(yao_other_cred_pool)
    assert yao_truth.is_otherunits_credor_weight_sum_correct()


def test_TruthUnit_is_otherunits_debtor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 60
    yao_truth.set_otherunit(otherunit_shop(rico_text, None, rico_debtor_weight))
    yao_truth.set_otherunit(otherunit_shop(carm_text, None, carm_debtor_weight))
    yao_truth.set_otherunit(otherunit_shop(patr_text, None, patr_debtor_weight))

    # WHEN / THEN
    yao_other_debt_pool = rico_debtor_weight + carm_debtor_weight + patr_debtor_weight
    assert yao_truth.is_otherunits_debtor_weight_sum_correct()
    yao_truth.set_other_debtor_pool(yao_other_debt_pool + 1)
    assert yao_truth.is_otherunits_debtor_weight_sum_correct() is False
    # WHEN / THEN
    yao_truth.set_other_debtor_pool(yao_other_debt_pool)
    assert yao_truth.is_otherunits_debtor_weight_sum_correct()


def test_TruthUnit_set_otherunit_external_metrics_SetsAttrs_credor_operational_debtor_operational():
    # GIVEN
    x_truth = truthunit_shop("Yao")
    jane_text = "Jane Randolph"
    x_truth.add_otherunit(jane_text)

    jane_other = x_truth._others.get(jane_text)
    print(f"Before Other {jane_other.other_id} {jane_other._debtor_operational=} ")
    assert jane_other._debtor_operational is None
    assert jane_other._credor_operational is None

    assert sum(
        other_x._credor_operational is None for other_x in x_truth._others.values()
    ) == len(x_truth._others)
    assert sum(
        other_x._debtor_operational is None for other_x in x_truth._others.values()
    ) == len(x_truth._others)

    # WHEN
    jane_debtor_status = True
    jane_credor_status = True
    jane_metr = OtherUnitExternalMetrics(
        internal_other_id=jane_text,
        debtor_operational=jane_debtor_status,
        credor_operational=jane_credor_status,
    )
    x_truth.set_otherunit_external_metrics(jane_metr)

    # THEN
    assert jane_other._debtor_operational == jane_debtor_status
    assert jane_other._credor_operational == jane_credor_status

    assert (
        sum(other_x._credor_operational is None for other_x in x_truth._others.values())
        == len(x_truth._others) - 1
    )
    assert (
        sum(other_x._debtor_operational is None for other_x in x_truth._others.values())
        == len(x_truth._others) - 1
    )
    assert (
        sum(other_x._credor_operational != None for other_x in x_truth._others.values())
        == 1
    )
    assert (
        sum(other_x._debtor_operational != None for other_x in x_truth._others.values())
        == 1
    )
