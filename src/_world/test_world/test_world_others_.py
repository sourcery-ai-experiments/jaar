from src._road.road import RoadUnit
from src._world.other import (
    OtherID,
    otherlink_shop,
    otherunit_shop,
    OtherUnitExternalMetrics,
)
from src._world.belief import (
    BeliefID,
    beliefunit_shop,
    balancelink_shop,
    get_intersection_of_others,
)
from src._world.examples.example_worlds import (
    world_v001 as examples_world_v001,
    world_v001_with_large_agenda as examples_world_v001_with_large_agenda,
)
from src._world.world import WorldUnit, worldunit_shop
from src._world.idea import ideaunit_shop, IdeaUnit
from pytest import raises as pytest_raises
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


def test_WorldUnit_set_otherunit_SetObjCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_otherunit = otherunit_shop(yao_text)
    deepcopy_yao_otherunit = copy_deepcopy(yao_otherunit)
    slash_text = "/"
    bob_world = worldunit_shop("Bob", _road_delimiter=slash_text)

    # WHEN
    bob_world.set_otherunit(otherunit=yao_otherunit)

    # THEN
    assert bob_world._others.get(yao_text)._road_delimiter == slash_text
    x_others = {yao_otherunit.other_id: deepcopy_yao_otherunit}
    assert bob_world._others != x_others
    deepcopy_yao_otherunit._road_delimiter = bob_world._road_delimiter
    assert bob_world._others == x_others


def test_examples_world_v001_has_others():
    # GIVEN / WHEN
    yao_world = examples_world_v001()

    # THEN
    assert yao_world._others != None
    assert len(yao_world._others) == 22


def test_WorldUnit_set_other_CorrectlySets_others_beliefs():
    # GIVEN
    x_pixel = 0.5
    yao_world = worldunit_shop("Yao", _pixel=x_pixel)
    yao_world.calc_world_metrics()
    assert len(yao_world._others) == 0
    assert len(yao_world._beliefs) == 0

    # WHEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))

    # THEN
    assert yao_world._others.get(rico_text)._pixel == x_pixel
    assert len(yao_world._others) == 3
    assert len(yao_world._beliefs) == 3
    assert yao_world._beliefs["rico"]._other_mirror == True

    # WHEN
    rico_belief = rico_text
    carm_belief = carm_text
    patr_belief = patr_text
    yao_world._idearoot.set_balancelink(balancelink_shop(rico_belief, credor_weight=10))
    yao_world._idearoot.set_balancelink(balancelink_shop(carm_belief, credor_weight=10))
    yao_world._idearoot.set_balancelink(balancelink_shop(patr_belief, credor_weight=10))
    assert len(yao_world._idearoot._balancelinks) == 3


def test_WorldUnit_add_otherunit_CorrectlySets_others():
    # GIVEN
    x_pixel = 0.5
    yao_world = worldunit_shop("Yao", _pixel=x_pixel)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    # WHEN
    yao_world.add_otherunit(rico_text, credor_weight=13, debtor_weight=8)
    yao_world.add_otherunit(carm_text, debtor_weight=5)
    yao_world.add_otherunit(patr_text, credor_weight=17)

    # THEN
    assert len(yao_world._others) == 3
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefunit(rico_text)._other_mirror == True
    assert yao_world._others.get(patr_text).credor_weight == 17
    assert yao_world._others.get(carm_text).debtor_weight == 5
    assert yao_world._others.get(patr_text)._pixel == x_pixel


def test_WorldUnit_other_exists_ReturnsObj():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    yao_text = "Yao"

    # WHEN / THEN
    assert bob_world.other_exists(yao_text) is False

    # GIVEN
    bob_world.add_otherunit(yao_text)

    # WHEN / THEN
    assert bob_world.other_exists(yao_text)


def test_WorldUnit_set_other_CorrectlyUpdate_other_mirror_BeliefUnit():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    before_rico_credor = 7
    before_rico_debtor = 17
    yao_world.add_otherunit(rico_text, before_rico_credor, before_rico_debtor)
    rico_beliefunit = yao_world.get_beliefunit(rico_text)
    rico_otherlink = rico_beliefunit.get_otherlink(rico_text)
    assert rico_otherlink.credor_weight != before_rico_credor
    assert rico_otherlink.debtor_weight != before_rico_debtor
    assert rico_otherlink.credor_weight == 1
    assert rico_otherlink.debtor_weight == 1

    # WHEN
    after_rico_credor = 11
    after_rico_debtor = 13
    yao_world.set_otherunit(
        otherunit_shop(rico_text, after_rico_credor, after_rico_debtor)
    )

    # THEN
    assert rico_otherlink.credor_weight != after_rico_credor
    assert rico_otherlink.debtor_weight != after_rico_debtor
    assert rico_otherlink.credor_weight == 1
    assert rico_otherlink.debtor_weight == 1


def test_WorldUnit_edit_other_RaiseExceptionWhenOtherDoesNotExist():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    rico_credor_weight = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_otherunit(rico_text, credor_weight=rico_credor_weight)
    assert str(excinfo.value) == f"OtherUnit '{rico_text}' does not exist."


def test_WorldUnit_edit_other_CorrectlyUpdatesObj():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    old_rico_credor_weight = 55
    old_rico_debtor_weight = 66
    yao_world.set_otherunit(
        otherunit_shop(
            rico_text,
            old_rico_credor_weight,
            old_rico_debtor_weight,
        )
    )
    rico_otherunit = yao_world.get_other(rico_text)
    assert rico_otherunit.credor_weight == old_rico_credor_weight
    assert rico_otherunit.debtor_weight == old_rico_debtor_weight

    # WHEN
    new_rico_credor_weight = 22
    new_rico_debtor_weight = 33
    yao_world.edit_otherunit(
        other_id=rico_text,
        credor_weight=new_rico_credor_weight,
        debtor_weight=new_rico_debtor_weight,
    )

    # THEN
    assert rico_otherunit.credor_weight == new_rico_credor_weight
    assert rico_otherunit.debtor_weight == new_rico_debtor_weight


def test_WorldUnit_get_other_ReturnsCorrectObj():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    yao_world.add_otherunit(rico_text)
    yao_world.add_otherunit(carm_text)

    # WHEN
    rico_other = yao_world.get_other(rico_text)
    carm_other = yao_world.get_other(carm_text)

    # THEN
    assert rico_other == yao_world._others.get(rico_text)
    assert carm_other == yao_world._others.get(carm_text)


def test_WorldUnit_calc_world_metrics_CorrectlySetsOtherLinkWorldCredAndDebt():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_world._idearoot.set_balancelink(balancelink=bl_rico)
    yao_world._idearoot.set_balancelink(balancelink=bl_carm)
    yao_world._idearoot.set_balancelink(balancelink=bl_patr)

    rico_beliefunit = yao_world.get_beliefunit(rico_text)
    carm_beliefunit = yao_world.get_beliefunit(carm_text)
    patr_beliefunit = yao_world.get_beliefunit(patr_text)
    rico_otherlink = rico_beliefunit._others.get(rico_text)
    carm_otherlink = carm_beliefunit._others.get(carm_text)
    patr_otherlink = patr_beliefunit._others.get(patr_text)
    rico_otherlink._world_cred is None
    rico_otherlink._world_debt is None
    carm_otherlink._world_cred is None
    carm_otherlink._world_debt is None
    patr_otherlink._world_cred is None
    patr_otherlink._world_debt is None

    # for belief in yao_world._beliefs.values():
    #     for otherlink in belief._others.values():
    #         assert otherlink._world_cred is None
    #         assert otherlink._world_debt is None

    yao_world.calc_world_metrics()

    # for balancelink in yao_world._balanceheirs.values():
    #     print(
    #         f"{yao_world._world_importance=} {balancelink.belief_id=} {balancelink._world_cred=} {balancelink._world_debt=}"
    #     )

    assert rico_otherlink._world_cred == 0.5
    assert rico_otherlink._world_debt == 0.8
    assert carm_otherlink._world_cred == 0.25
    assert carm_otherlink._world_debt == 0.1
    assert patr_otherlink._world_cred == 0.25
    assert patr_otherlink._world_debt == 0.1

    # otherlink_world_cred_sum = 0.0
    # otherlink_world_debt_sum = 0.0
    # for belief in yao_world._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._others=}")

    #     for otherlink in belief._others.values():
    #         assert otherlink._world_cred != None
    #         assert otherlink._world_cred in [0.25, 0.5]
    #         assert otherlink._world_debt != None
    #         assert otherlink._world_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {otherlink._world_importance=} {belief._world_importance=}"
    #         # )
    #         otherlink_world_cred_sum += otherlink._world_cred
    #         otherlink_world_debt_sum += otherlink._world_debt

    #         # print(f"{otherlink_world_importance_sum=}")
    # assert otherlink_world_cred_sum == 1.0
    # assert otherlink_world_debt_sum == 1.0

    assert (
        rico_otherlink._world_cred
        + carm_otherlink._world_cred
        + patr_otherlink._world_cred
        == 1.0
    )
    assert (
        rico_otherlink._world_debt
        + carm_otherlink._world_debt
        + patr_otherlink._world_debt
        == 1.0
    )

    # WHEN anothher pledge, check metrics are as expected
    selena_text = "selena"
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(selena_text)))
    yao_world._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            belief_id=BeliefID(selena_text), credor_weight=20, debtor_weight=13
        )
    )
    yao_world.calc_world_metrics()

    # THEN
    selena_beliefunit = yao_world.get_beliefunit(selena_text)
    selena_otherlink = selena_beliefunit._others.get(selena_text)

    assert rico_otherlink._world_cred != 0.25
    assert rico_otherlink._world_debt != 0.8
    assert carm_otherlink._world_cred != 0.25
    assert carm_otherlink._world_debt != 0.1
    assert patr_otherlink._world_cred != 0.5
    assert patr_otherlink._world_debt != 0.1
    assert selena_otherlink._world_cred != None
    assert selena_otherlink._world_debt != None

    # otherlink_world_cred_sum = 0.0
    # otherlink_world_debt_sum = 0.0

    # for belief in yao_world._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._others=}")

    #     for otherlink in belief._others.values():
    #         assert otherlink._world_cred != None
    #         assert otherlink._world_cred not in [0.25, 0.5]
    #         assert otherlink._world_debt != None
    #         assert otherlink._world_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {otherlink._world_importance=} {belief._world_importance=}"
    #         # )
    #         otherlink_world_cred_sum += otherlink._world_cred
    #         otherlink_world_debt_sum += otherlink._world_debt

    #         # print(f"{otherlink_world_importance_sum=}")
    # assert otherlink_world_cred_sum == 1.0
    # assert otherlink_world_debt_sum > 0.9999999
    # assert otherlink_world_debt_sum < 1.00000001

    assert (
        rico_otherlink._world_cred
        + carm_otherlink._world_cred
        + patr_otherlink._world_cred
        + selena_otherlink._world_cred
        == 1.0
    )
    assert (
        rico_otherlink._world_debt
        + carm_otherlink._world_debt
        + patr_otherlink._world_debt
        + selena_otherlink._world_debt
        > 0.9999999
    )
    assert (
        rico_otherlink._world_debt
        + carm_otherlink._world_debt
        + patr_otherlink._world_debt
        + selena_otherlink._world_debt
        < 1.0
    )


def test_WorldUnit_calc_world_metrics_CorrectlySetsOtherUnitWorldImportance():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    swim_text = "swim"
    yao_world.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_world._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_rico)
    yao_world._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_carm)
    yao_world._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_patr)

    rico_otherunit = yao_world._others.get(rico_text)
    carm_otherunit = yao_world._others.get(carm_text)
    patr_otherunit = yao_world._others.get(patr_text)

    assert rico_otherunit._world_cred == 0
    assert rico_otherunit._world_debt == 0
    assert carm_otherunit._world_cred == 0
    assert carm_otherunit._world_debt == 0
    assert patr_otherunit._world_cred == 0
    assert patr_otherunit._world_debt == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    otherunit_world_cred_sum = 0.0
    otherunit_world_debt_sum = 0.0

    assert rico_otherunit._world_cred == 0.5
    assert rico_otherunit._world_debt == 0.8
    assert carm_otherunit._world_cred == 0.25
    assert carm_otherunit._world_debt == 0.1
    assert patr_otherunit._world_cred == 0.25
    assert patr_otherunit._world_debt == 0.1

    assert (
        rico_otherunit._world_cred
        + carm_otherunit._world_cred
        + patr_otherunit._world_cred
        == 1.0
    )
    assert (
        rico_otherunit._world_debt
        + carm_otherunit._world_debt
        + patr_otherunit._world_debt
        == 1.0
    )

    # for otherunit in yao_world._others.values():
    #     assert otherunit._world_cred != None
    #     assert otherunit._world_cred in [0.25, 0.5]
    #     assert otherunit._world_debt != None
    #     assert otherunit._world_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {otherunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{otherunit.} {otherunit._world_cred=} {otherunit._world_debt=} ")
    #     # print(f"{otherunit_world_cred_sum=}")
    #     # print(f"{otherunit_world_debt_sum=}")
    #     otherunit_world_cred_sum += otherunit._world_cred
    #     otherunit_world_debt_sum += otherunit._world_debt

    # assert otherunit_world_cred_sum == 1.0
    # assert otherunit_world_debt_sum > 0.9999999
    # assert otherunit_world_debt_sum < 1.00000001

    # WHEN anothher pledge, check metrics are as expected
    selena_text = "selena"
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(selena_text)))
    yao_world._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            belief_id=selena_text, credor_weight=20, debtor_weight=10
        )
    )
    yao_world.calc_world_metrics()

    # THEN
    selena_otherunit = yao_world._others.get(selena_text)

    assert rico_otherunit._world_cred != 0.5
    assert rico_otherunit._world_debt != 0.8
    assert carm_otherunit._world_cred != 0.25
    assert carm_otherunit._world_debt != 0.1
    assert patr_otherunit._world_cred != 0.25
    assert patr_otherunit._world_debt != 0.1
    assert selena_otherunit._world_cred != None
    assert selena_otherunit._world_debt != None

    assert (
        rico_otherunit._world_cred
        + carm_otherunit._world_cred
        + patr_otherunit._world_cred
        < 1.0
    )
    assert (
        rico_otherunit._world_cred
        + carm_otherunit._world_cred
        + patr_otherunit._world_cred
        + selena_otherunit._world_cred
        == 1.0
    )
    assert (
        rico_otherunit._world_debt
        + carm_otherunit._world_debt
        + patr_otherunit._world_debt
        < 1.0
    )
    assert (
        rico_otherunit._world_debt
        + carm_otherunit._world_debt
        + patr_otherunit._world_debt
        + selena_otherunit._world_debt
        == 1.0
    )

    # otherunit_world_cred_sum = 0.0
    # otherunit_world_debt_sum = 0.0

    # for otherunit in yao_world._others.values():
    #     assert otherunit._world_cred != None
    #     assert otherunit._world_cred not in [0.25, 0.5]
    #     assert otherunit._world_debt != None
    #     assert otherunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {otherunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{otherunit.} {otherunit._world_cred=} {otherunit._world_debt=} ")
    #     # print(f"{otherunit_world_cred_sum=}")
    #     # print(f"{otherunit_world_debt_sum=}")
    #     otherunit_world_cred_sum += otherunit._world_cred
    #     otherunit_world_debt_sum += otherunit._world_debt

    # assert otherunit_world_cred_sum == 1.0
    # assert otherunit_world_debt_sum > 0.9999999
    # assert otherunit_world_debt_sum < 1.00000001


def test_WorldUnit_calc_world_metrics_CorrectlySetsPartBeliefedLWOtherUnitWorldImportance():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    swim_text = "swim"
    yao_world.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_world._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_rico)
    yao_world._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_carm)
    yao_world._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_patr)

    # no balancelinks attached to this one
    hunt_text = "hunt"
    yao_world.add_l1_idea(ideaunit_shop(hunt_text, _weight=3))

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    rico_beliefunit = yao_world.get_beliefunit(rico_text)
    carm_beliefunit = yao_world.get_beliefunit(carm_text)
    patr_beliefunit = yao_world.get_beliefunit(patr_text)
    assert rico_beliefunit._world_cred != 0.5
    assert rico_beliefunit._world_debt != 0.8
    assert carm_beliefunit._world_cred != 0.25
    assert carm_beliefunit._world_debt != 0.1
    assert patr_beliefunit._world_cred != 0.25
    assert patr_beliefunit._world_debt != 0.1
    assert (
        rico_beliefunit._world_cred
        + carm_beliefunit._world_cred
        + patr_beliefunit._world_cred
        == 0.25
    )
    assert (
        rico_beliefunit._world_debt
        + carm_beliefunit._world_debt
        + patr_beliefunit._world_debt
        == 0.25
    )

    # beliefunit_world_cred_sum = 0.0
    # beliefunit_world_debt_sum = 0.0
    # for beliefunit in yao_world._beliefs.values():
    #     assert beliefunit._world_cred != None
    #     assert beliefunit._world_cred not in [0.25, 0.5]
    #     assert beliefunit._world_debt != None
    #     assert beliefunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {beliefunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{beliefunit.belief_id=} {beliefunit._world_cred=} {beliefunit._world_debt=} ")
    #     # print(f"{beliefunit_world_cred_sum=}")
    #     # print(f"{beliefunit_world_debt_sum=}")
    #     beliefunit_world_cred_sum += beliefunit._world_cred
    #     beliefunit_world_debt_sum += beliefunit._world_debt
    # assert beliefunit_world_cred_sum == 0.25
    # assert beliefunit_world_debt_sum == 0.25

    rico_otherunit = yao_world._others.get(rico_text)
    carm_otherunit = yao_world._others.get(carm_text)
    patr_otherunit = yao_world._others.get(patr_text)

    assert rico_otherunit._world_cred == 0.375
    assert rico_otherunit._world_debt == 0.45
    assert carm_otherunit._world_cred == 0.3125
    assert carm_otherunit._world_debt == 0.275
    assert patr_otherunit._world_cred == 0.3125
    assert patr_otherunit._world_debt == 0.275

    assert (
        rico_otherunit._world_cred
        + carm_otherunit._world_cred
        + patr_otherunit._world_cred
        == 1.0
    )
    assert (
        rico_otherunit._world_debt
        + carm_otherunit._world_debt
        + patr_otherunit._world_debt
        == 1.0
    )

    # otherunit_world_cred_sum = 0.0
    # otherunit_world_debt_sum = 0.0
    # for otherunit in yao_world._others.values():
    #     assert otherunit._world_cred != None
    #     assert otherunit._world_cred not in [0.25, 0.5]
    #     assert otherunit._world_debt != None
    #     assert otherunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {otherunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{otherunit.} {otherunit._world_cred=} {otherunit._world_debt=} ")
    #     # print(f"{otherunit_world_cred_sum=}")
    #     # print(f"{otherunit_world_debt_sum=}")
    #     otherunit_world_cred_sum += otherunit._world_cred
    #     otherunit_world_debt_sum += otherunit._world_debt
    # assert otherunit_world_cred_sum == 1.0
    # assert otherunit_world_debt_sum > 0.9999999
    # assert otherunit_world_debt_sum < 1.00000001


def test_WorldUnit_calc_world_metrics_CorrectlySetsOtherAttrs():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    yao_world.add_l1_idea(ideaunit_shop("swim"))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_otherunit(
        otherunit=otherunit_shop(OtherID(rico_text), credor_weight=8)
    )
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    rico_otherunit = yao_world._others.get(rico_text)
    carm_otherunit = yao_world._others.get(carm_text)
    patr_otherunit = yao_world._others.get(patr_text)
    assert rico_otherunit._world_cred == 0
    assert rico_otherunit._world_debt == 0
    assert carm_otherunit._world_cred == 0
    assert carm_otherunit._world_debt == 0
    assert patr_otherunit._world_cred == 0
    assert patr_otherunit._world_debt == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    assert (
        rico_otherunit._world_cred
        + carm_otherunit._world_cred
        + patr_otherunit._world_cred
        == 1.0
    )
    assert (
        rico_otherunit._world_debt
        + carm_otherunit._world_debt
        + patr_otherunit._world_debt
        == 1.0
    )
    # otherunit_world_cred_sum = 0.0
    # otherunit_world_debt_sum = 0.0
    # for otherunit in yao_world._others.values():
    #     assert otherunit._world_cred != None
    #     assert otherunit._world_cred not in [0.25, 0.5]
    #     assert otherunit._world_debt != None
    #     assert otherunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {otherunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{otherunit.} {otherunit._world_cred=} {otherunit._world_debt=} ")
    #     # print(f"{otherunit_world_cred_sum=}")
    #     # print(f"{otherunit_world_debt_sum=}")
    #     otherunit_world_cred_sum += otherunit._world_cred
    #     otherunit_world_debt_sum += otherunit._world_debt
    # assert otherunit_world_cred_sum == 1.0
    # assert otherunit_world_debt_sum > 0.9999999
    # assert otherunit_world_debt_sum < 1.00000001


def test_WorldUnit_calc_world_metrics_RaisesErrorWhen_is_otherunits_credor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_world = worldunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_credor_weight = 20
    carm_credor_weight = 30
    patr_credor_weight = 50
    yao_world.set_otherunit(otherunit_shop(rico_text, None, rico_credor_weight))
    yao_world.set_otherunit(otherunit_shop(carm_text, None, carm_credor_weight))
    yao_world.set_otherunit(otherunit_shop(patr_text, None, patr_credor_weight))
    assert yao_world._other_credor_pool is None
    assert yao_world.is_otherunits_credor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_other_credor_pool(x_int)
    assert yao_world.is_otherunits_credor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_world.calc_world_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_otherunits_credor_weight_sum_correct is False. _other_credor_pool={x_int}. otherunits_credor_weight_sum={yao_world.get_otherunits_credor_weight_sum()}"
    )

    # WHEN / THEN
    yao_world.set_other_credor_pool(yao_world.get_otherunits_credor_weight_sum())
    assert yao_world.calc_world_metrics() is None


def test_WorldUnit_calc_world_metrics_DoesNotRaiseError_other_credor_poolWhenOtherSumIsZero():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    assert yao_world._other_credor_pool is None
    assert yao_world.is_otherunits_credor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_other_credor_pool(x_int)

    # THEN
    assert yao_world.is_otherunits_credor_weight_sum_correct()
    yao_world.calc_world_metrics()


def test_WorldUnit_calc_world_metrics_RaisesErrorWhen_is_otherunits_debtor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_world = worldunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 40
    yao_world.set_otherunit(otherunit_shop(rico_text, None, None, rico_debtor_weight))
    yao_world.set_otherunit(otherunit_shop(carm_text, None, None, carm_debtor_weight))
    yao_world.set_otherunit(otherunit_shop(patr_text, None, None, patr_debtor_weight))
    assert yao_world._other_debtor_pool is None
    assert yao_world.is_otherunits_debtor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_other_debtor_pool(x_int)
    assert yao_world.is_otherunits_debtor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_world.calc_world_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_otherunits_debtor_weight_sum_correct is False. _other_debtor_pool={x_int}. otherunits_debtor_weight_sum={yao_world.get_otherunits_debtor_weight_sum()}"
    )

    # WHEN / THEN
    yao_world.set_other_debtor_pool(yao_world.get_otherunits_debtor_weight_sum())
    assert yao_world.calc_world_metrics() is None


def test_WorldUnit_calc_world_metrics_DoesNotRaiseError_other_debtor_poolWhenOtherSumIsZero():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    assert yao_world._other_credor_pool is None
    assert yao_world.is_otherunits_debtor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_other_debtor_pool(x_int)

    # THEN
    assert yao_world.is_otherunits_debtor_weight_sum_correct()
    yao_world.calc_world_metrics()


def clear_all_otherunits_beliefunits_world_agenda_cred_debt(x_world: WorldUnit):
    # DELETE world_agenda_debt and world_agenda_cred
    for beliefunit_x in x_world._beliefs.values():
        beliefunit_x.reset_world_cred_debt()
        # for otherlink_x in beliefunit_x._others.values():
        #     print(f"{beliefunit_x.belief_id=} {otherlink_x.credor_weight=}  {otherlink_x._world_cred:.6f} {otherlink_x.debtor_weight=} {otherlink_x._world_debt:.6f} {otherlink_x.} ")

    # DELETE world_agenda_debt and world_agenda_cred
    for x_otherunit in x_world._others.values():
        x_otherunit.reset_world_cred_debt()


@dataclass
class BeliefAgendaMetrics:
    sum_beliefunit_cred: float = 0
    sum_beliefunit_debt: float = 0
    sum_otherlink_cred: float = 0
    sum_otherlink_debt: float = 0
    otherlink_count: int = 0

    def set_sums(self, x_world: WorldUnit):
        for beliefunit_x in x_world._beliefs.values():
            self.sum_beliefunit_cred += beliefunit_x._world_agenda_cred
            self.sum_beliefunit_debt += beliefunit_x._world_agenda_debt
            for otherlink_x in beliefunit_x._others.values():
                self.sum_otherlink_cred += otherlink_x._world_agenda_cred
                self.sum_otherlink_debt += otherlink_x._world_agenda_debt
                self.otherlink_count += 1


@dataclass
class OtherAgendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_sums(self, x_world: WorldUnit):
        for otherunit in x_world._others.values():
            self.sum_agenda_cred += otherunit._world_agenda_cred
            self.sum_agenda_debt += otherunit._world_agenda_debt
            self.sum_agenda_ratio_cred += otherunit._world_agenda_ratio_cred
            self.sum_agenda_ratio_debt += otherunit._world_agenda_ratio_debt


@dataclass
class BalanceAgendaMetrics:
    sum_world_agenda_importance = 0
    agenda_no_count = 0
    agenda_yes_count = 0
    agenda_no_world_i_sum = 0
    agenda_yes_world_i_sum = 0

    def set_sums(self, agenda_dict: dict[RoadUnit:IdeaUnit]):
        for agenda_item in agenda_dict.values():
            self.sum_world_agenda_importance += agenda_item._world_importance
            if agenda_item._balancelines == {}:
                self.agenda_no_count += 1
                self.agenda_no_world_i_sum += agenda_item._world_importance
            else:
                self.agenda_yes_count += 1
                self.agenda_yes_world_i_sum += agenda_item._world_importance


def test_WorldUnit_agenda_cred_debt_IsCorrectlySet():
    # GIVEN
    x_world = examples_world_v001_with_large_agenda()
    clear_all_otherunits_beliefunits_world_agenda_cred_debt(x_world=x_world)

    # TEST world_agenda_debt and world_agenda_cred are empty
    x_beliefagendametrics = BeliefAgendaMetrics()
    x_beliefagendametrics.set_sums(x_world=x_world)
    assert x_beliefagendametrics.sum_beliefunit_cred == 0
    assert x_beliefagendametrics.sum_beliefunit_debt == 0
    assert x_beliefagendametrics.sum_otherlink_cred == 0
    assert x_beliefagendametrics.sum_otherlink_debt == 0

    # TEST world_agenda_debt and world_agenda_cred are empty
    x_otheragendametrics = OtherAgendaMetrics()
    x_otheragendametrics.set_sums(x_world=x_world)
    assert x_otheragendametrics.sum_agenda_cred == 0
    assert x_otheragendametrics.sum_agenda_debt == 0
    assert x_otheragendametrics.sum_agenda_ratio_cred == 0
    assert x_otheragendametrics.sum_agenda_ratio_debt == 0

    # WHEN
    agenda_dict = x_world.get_agenda_dict()

    # THEN
    assert len(agenda_dict) == 63
    x_balanceagendametrics = BalanceAgendaMetrics()
    x_balanceagendametrics.set_sums(agenda_dict=agenda_dict)
    # print(f"{sum_world_agenda_importance=}")
    assert x_balanceagendametrics.agenda_no_count == 14
    assert x_balanceagendametrics.agenda_yes_count == 49
    assert x_balanceagendametrics.agenda_no_world_i_sum == 0.0037472680016539662
    assert x_balanceagendametrics.agenda_yes_world_i_sum == 0.0027965049894874455
    assert are_equal(
        x_balanceagendametrics.agenda_no_world_i_sum
        + x_balanceagendametrics.agenda_yes_world_i_sum,
        x_balanceagendametrics.sum_world_agenda_importance,
    )
    assert x_balanceagendametrics.sum_world_agenda_importance == 0.006543772991141412

    x_beliefagendametrics = BeliefAgendaMetrics()
    x_beliefagendametrics.set_sums(x_world=x_world)
    assert x_beliefagendametrics.otherlink_count == 81
    x_sum = 0.0027965049894874455
    assert are_equal(x_beliefagendametrics.sum_beliefunit_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_beliefunit_debt, x_sum)
    assert are_equal(x_beliefagendametrics.sum_otherlink_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_otherlink_debt, x_sum)
    assert are_equal(
        x_balanceagendametrics.agenda_yes_world_i_sum,
        x_beliefagendametrics.sum_beliefunit_cred,
    )

    assert all_otherunits_have_legitimate_values(x_world)

    x_otheragendametrics = OtherAgendaMetrics()
    x_otheragendametrics.set_sums(x_world=x_world)
    assert are_equal(
        x_otheragendametrics.sum_agenda_cred,
        x_balanceagendametrics.sum_world_agenda_importance,
    )
    assert are_equal(
        x_otheragendametrics.sum_agenda_debt,
        x_balanceagendametrics.sum_world_agenda_importance,
    )
    assert are_equal(x_otheragendametrics.sum_agenda_ratio_cred, 1)
    assert are_equal(x_otheragendametrics.sum_agenda_ratio_debt, 1)

    # otherunit_world_cred_sum = 0.0
    # otherunit_world_debt_sum = 0.0

    # assert otherunit_world_cred_sum == 1.0
    # assert otherunit_world_debt_sum > 0.9999999
    # assert otherunit_world_debt_sum < 1.00000001


def all_otherunits_have_legitimate_values(x_world: WorldUnit):
    return not any(
        (
            otherunit._world_cred is None
            or otherunit._world_cred in [0.25, 0.5]
            or otherunit._world_debt is None
            or otherunit._world_debt in [0.8, 0.1]
        )
        for otherunit in x_world._others.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000000001
    return abs(x1 - x2) < e10


def test_WorldUnit_agenda_ratio_cred_debt_IsCorrectlySetWhenWorldIsEmpty():
    # GIVEN
    noa_world = worldunit_shop("Noa")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_other = otherunit_shop(rico_text, credor_weight=0.5, debtor_weight=2)
    carm_other = otherunit_shop(carm_text, credor_weight=1.5, debtor_weight=3)
    patr_other = otherunit_shop(patr_text, credor_weight=8, debtor_weight=5)
    noa_world.set_otherunit(otherunit=rico_other)
    noa_world.set_otherunit(otherunit=carm_other)
    noa_world.set_otherunit(otherunit=patr_other)
    noa_world_rico_other = noa_world._others.get(rico_text)
    noa_world_carm_other = noa_world._others.get(carm_text)
    noa_world_patr_other = noa_world._others.get(patr_text)

    assert noa_world_rico_other._world_agenda_cred in [0, None]
    assert noa_world_rico_other._world_agenda_debt in [0, None]
    assert noa_world_carm_other._world_agenda_cred in [0, None]
    assert noa_world_carm_other._world_agenda_debt in [0, None]
    assert noa_world_patr_other._world_agenda_cred in [0, None]
    assert noa_world_patr_other._world_agenda_debt in [0, None]
    assert noa_world_rico_other._world_agenda_ratio_cred != 0.05
    assert noa_world_rico_other._world_agenda_ratio_debt != 0.2
    assert noa_world_carm_other._world_agenda_ratio_cred != 0.15
    assert noa_world_carm_other._world_agenda_ratio_debt != 0.3
    assert noa_world_patr_other._world_agenda_ratio_cred != 0.8
    assert noa_world_patr_other._world_agenda_ratio_debt != 0.5

    # WHEN
    noa_world.calc_world_metrics()

    # THEN
    assert noa_world_rico_other._world_agenda_cred == 0
    assert noa_world_rico_other._world_agenda_debt == 0
    assert noa_world_carm_other._world_agenda_cred == 0
    assert noa_world_carm_other._world_agenda_debt == 0
    assert noa_world_patr_other._world_agenda_cred == 0
    assert noa_world_patr_other._world_agenda_debt == 0
    assert noa_world_rico_other._world_agenda_ratio_cred == 0.05
    assert noa_world_rico_other._world_agenda_ratio_debt == 0.2
    assert noa_world_carm_other._world_agenda_ratio_cred == 0.15
    assert noa_world_carm_other._world_agenda_ratio_debt == 0.3
    assert noa_world_patr_other._world_agenda_ratio_cred == 0.8
    assert noa_world_patr_other._world_agenda_ratio_debt == 0.5


def test_WorldUnit_get_other_belief_ids_ReturnsCorrectObj():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))

    # WHEN / THEN
    assert yao_world.get_other_belief_ids(carm_text) == [carm_text]

    # WHEN / THEN
    swimmers = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swimmers)
    swim_belief.set_otherlink(otherlink_shop(carm_text))
    yao_world.set_beliefunit(swim_belief)
    assert yao_world.get_other_belief_ids(carm_text) == [carm_text, swimmers]


def test_WorldUnit_edit_otherunit_other_id_CorrectlyModifiesOtherUnit_other_id():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    yao_world.add_otherunit(rico_text, credor_weight=13)
    yao_world.add_otherunit("carmen")
    yao_world.add_otherunit("patrick", credor_weight=17)
    assert len(yao_world._others) == 3
    assert yao_world._others.get(rico_text) != None
    assert yao_world._others.get(rico_text).credor_weight == 13
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefunit(rico_text) != None
    assert yao_world.get_beliefunit(rico_text)._other_mirror == True

    # WHEN
    beto_text = "beta"
    yao_world.edit_otherunit_other_id(
        old_other_id=rico_text,
        new_other_id=beto_text,
        allow_other_overwite=False,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_world._others.get(beto_text) != None
    assert yao_world._others.get(beto_text).credor_weight == 13
    assert yao_world._others.get(rico_text) is None
    assert len(yao_world._others) == 3
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefunit(rico_text) is None
    assert yao_world.get_beliefunit(beto_text) != None
    assert yao_world.get_beliefunit(beto_text)._other_mirror == True


def test_WorldUnit_OtherUnit_raiseErrorNewother_idPreviouslyExists():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    yao_world.add_otherunit(rico_text, credor_weight=13)
    carmen_text = "carmen"
    yao_world.add_otherunit(carmen_text)
    yao_world.add_otherunit("patrick", credor_weight=17)
    assert len(yao_world._others) == 3
    assert yao_world._others.get(rico_text) != None
    assert yao_world._others.get(rico_text).credor_weight == 13
    assert len(yao_world._beliefs) == 3
    assert yao_world.get_beliefunit(rico_text) != None
    assert yao_world.get_beliefunit(rico_text)._other_mirror == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_otherunit_other_id(
            old_other_id=rico_text,
            new_other_id=carmen_text,
            allow_other_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Other '{rico_text}' modify to '{carmen_text}' failed since '{carmen_text}' exists."
    )


def test_WorldUnit_OtherUnit_CorrectlyModifiesBeliefUnitOtherLinks():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.add_otherunit(rico_text, credor_weight=13)
    yao_world.add_otherunit(carm_text)
    yao_world.add_otherunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_other_dict = {OtherID(carm_text): otherlink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _others=carmen_other_dict)
    swim_belief.set_otherlink(
        otherlink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_otherlink(
        otherlink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_world.set_beliefunit(y_beliefunit=swim_belief)

    swim_belief = yao_world.get_beliefunit(swim_text)
    assert len(swim_belief._others) == 2
    assert swim_belief.get_otherlink(rico_text) != None
    assert swim_belief.get_otherlink(rico_text).credor_weight == 7
    assert swim_belief.get_otherlink(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    yao_world.edit_otherunit_other_id(
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


def test_WorldUnit_OtherUnit_CorrectlyMergesother_ids():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.add_otherunit(rico_text, credor_weight=13)
    yao_world.add_otherunit(carm_text, credor_weight=3)
    yao_world.add_otherunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_other_dict = {OtherID(carm_text): otherlink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _others=carmen_other_dict)
    swim_belief.set_otherlink(
        otherlink=otherlink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_otherlink(
        otherlink=otherlink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_world.set_beliefunit(y_beliefunit=swim_belief)

    assert len(yao_world._others) == 3
    assert yao_world._others.get(rico_text) != None
    assert yao_world._others.get(rico_text).credor_weight == 13
    assert yao_world._others.get(carm_text) != None
    assert yao_world._others.get(carm_text).credor_weight == 3

    # WHEN / THEN
    yao_world.edit_otherunit_other_id(
        old_other_id=rico_text,
        new_other_id=carm_text,
        allow_other_overwite=True,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_world._others.get(carm_text) != None
    assert yao_world._others.get(carm_text).credor_weight == 16
    assert yao_world._others.get(rico_text) is None
    assert len(yao_world._others) == 2


def test_WorldUnit_OtherUnit_CorrectlyMergesBeliefUnitOtherLinks():
    # GIVEN
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.add_otherunit(rico_text, credor_weight=13)
    yao_world.add_otherunit(carm_text)
    yao_world.add_otherunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_other_dict = {OtherID(carm_text): otherlink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _others=carmen_other_dict)
    swim_belief.set_otherlink(
        otherlink=otherlink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_otherlink(
        otherlink=otherlink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_world.set_beliefunit(y_beliefunit=swim_belief)

    swim_belief = yao_world.get_beliefunit(swim_text)
    assert len(swim_belief._others) == 2
    assert swim_belief.get_otherlink(rico_text) != None
    assert swim_belief.get_otherlink(rico_text).credor_weight == 7
    assert swim_belief.get_otherlink(rico_text).debtor_weight == 30
    assert swim_belief.get_otherlink(carm_text) != None
    assert swim_belief.get_otherlink(carm_text).credor_weight == 5
    assert swim_belief.get_otherlink(carm_text).debtor_weight == 18

    # WHEN
    yao_world.edit_otherunit_other_id(
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


def test_WorldUnit_OtherUnit_raiseErrorNewOtherIDBeliefUnitPreviouslyExists():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    yao_world.add_otherunit(rico_text, credor_weight=13)
    anna_text = "anna"
    yao_world.add_otherunit(anna_text, credor_weight=17)
    carmen_text = ",carmen"
    carmen_belief = beliefunit_shop(belief_id=carmen_text)
    carmen_belief.set_otherlink(otherlink=otherlink_shop(rico_text))
    carmen_belief.set_otherlink(otherlink=otherlink_shop(anna_text))
    yao_world.set_beliefunit(y_beliefunit=carmen_belief)
    assert len(yao_world._beliefs) == 3
    assert yao_world._others.get(carmen_text) is None
    assert yao_world.get_beliefunit(carmen_text)._other_mirror is False
    assert len(yao_world.get_beliefunit(carmen_text)._others) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_world.edit_otherunit_other_id(
            old_other_id=rico_text,
            new_other_id=carmen_text,
            allow_other_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Other '{rico_text}' modify to '{carmen_text}' failed since non-single belief '{carmen_text}' exists."
    )


# def test_WorldUnit_OtherUnit_CorrectlyOverwriteNewOtherIDBeliefUnit():
#     # GIVEN
#     yao_world = worldunit_shop("Yao")
#     rico_text = "rico"
#     yao_world.add_otherunit(rico_text, credor_weight=13)
#     anna_text = "anna"
#     yao_world.add_otherunit(anna_text, credor_weight=17)
#     carmen_text = ",carmen"
#     carmen_belief = beliefunit_shop(belief_id=carmen_text)
#     carmen_belief.set_otherlink(
#         otherlink=otherlink_shop(rico_text, credor_weight=3)
#     )
#     carmen_belief.set_otherlink(
#         otherlink=otherlink_shop(anna_text, credor_weight=5)
#     )
#     yao_world.set_beliefunit(y_beliefunit=carmen_belief)
#     assert len(yao_world._beliefs) == 3
#     assert yao_world._others.get(rico_text) != None
#     assert yao_world._others.get(carmen_text) is None
#     assert yao_world.get_beliefunit(carmen_text)._other_mirror is False
#     assert len(yao_world.get_beliefunit(carmen_text)._others) == 2
#     assert (
#         yao_world.get_beliefunit(carmen_text)._others.get(anna_text).credor_weight
#         == 5
#     )
#     assert (
#         yao_world.get_beliefunit(carmen_text)._others.get(rico_text).credor_weight
#         == 3
#     )

#     # WHEN
#     yao_world.edit_otherunit_other_id(
#         old_rico_text,
#         new_carmen_text,
#         allow_other_overwite=False,
#         allow_nonsingle_belief_overwrite=True,
#     )

#     assert len(yao_world._beliefs) == 2
#     assert yao_world._others.get(rico_text) is None
#     assert yao_world._others.get(carmen_text) != None
#     assert yao_world.get_beliefunit(carmen_text)._other_mirror == True
#     assert len(yao_world.get_beliefunit(carmen_text)._others) == 1
#     assert yao_world.get_beliefunit(carmen_text)._others.get(rico_text) is None
#     assert (
#         yao_world.get_beliefunit(carmen_text)._others.get(carmen_text).credor_weight
#         == 1
#     )


def test_WorldUnit_get_otherunits_other_id_list_ReturnsListOfOtherUnits():
    # GIVEN
    noa_world = worldunit_shop("Noa")
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    noa_world.set_otherunit(otherunit=otherunit_shop(sam_text))
    noa_world.set_otherunit(otherunit=otherunit_shop(will_text))
    noa_world.set_otherunit(otherunit=otherunit_shop(fry_text))
    fun_text = ",fun people"
    fun_belief = beliefunit_shop(belief_id=fun_text)
    fun_belief.set_otherlink(otherlink=otherlink_shop(will_text))
    noa_world.set_beliefunit(y_beliefunit=fun_belief)
    assert len(noa_world._beliefs) == 4
    assert len(noa_world._others) == 3

    # WHEN
    otherunit_list_x = noa_world.get_otherunits_other_id_list()

    # THEN
    assert len(otherunit_list_x) == 4
    assert otherunit_list_x[0] == ""
    assert otherunit_list_x[1] == fry_text
    assert otherunit_list_x[2] == sam_text
    assert otherunit_list_x[3] == will_text


def test_get_intersection_of_others_ReturnsUnionOfKeysOfTwoDictionarys_scenario1():
    # GIVEN
    bob_text = "Bob"
    bob_world = worldunit_shop(bob_text)

    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "Elu"
    bob_world.set_otherunit(otherunit=otherunit_shop(bob_text))
    bob_world.set_otherunit(otherunit=otherunit_shop(sam_text))
    bob_world.set_otherunit(otherunit=otherunit_shop(wil_text))
    bob_world.set_otherunit(otherunit=otherunit_shop(fry_text))

    y_world = worldunit_shop()
    y_world.set_otherunit(otherunit=otherunit_shop(bob_text))
    y_world.set_otherunit(otherunit=otherunit_shop(wil_text))
    y_world.set_otherunit(otherunit=otherunit_shop(fry_text))
    y_world.set_otherunit(otherunit=otherunit_shop(elu_text))

    # WHEN
    print(f"{len(bob_world._others)=} {len(y_world._others)=}")
    intersection_x = get_intersection_of_others(bob_world._others, y_world._others)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}


def test_WorldUnit_clear_output_world_meld_orders_CorrectlyClearsAttrs():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    rico_otherunit = yao_world.get_other(rico_text)
    carm_otherunit = yao_world.get_other(carm_text)
    patr_otherunit = yao_world.get_other(patr_text)
    rico_otherunit.set_output_world_meld_order(3)
    carm_otherunit.set_output_world_meld_order(4)
    patr_otherunit.set_output_world_meld_order(5)

    assert rico_otherunit._output_world_meld_order != None
    assert carm_otherunit._output_world_meld_order != None
    assert patr_otherunit._output_world_meld_order != None

    # WHEN
    yao_world.clear_others_output_world_meld_order()

    # THEN
    assert rico_otherunit._output_world_meld_order is None
    assert carm_otherunit._output_world_meld_order is None
    assert patr_otherunit._output_world_meld_order is None


def test_WorldUnit_clear_output_world_meld_orders_WithNoArgsCorrectlySetOrder():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(rico_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(carm_text)))
    yao_world.set_otherunit(otherunit=otherunit_shop(OtherID(patr_text)))
    rico_otherunit = yao_world.get_other(rico_text)
    carm_otherunit = yao_world.get_other(carm_text)
    patr_otherunit = yao_world.get_other(patr_text)
    assert rico_otherunit._output_world_meld_order is None
    assert carm_otherunit._output_world_meld_order is None
    assert patr_otherunit._output_world_meld_order is None

    # WHEN
    yao_world.set_others_output_world_meld_order()

    # THEN
    assert rico_otherunit._output_world_meld_order != None
    assert carm_otherunit._output_world_meld_order != None
    assert patr_otherunit._output_world_meld_order != None
    print(f"{rico_otherunit._output_world_meld_order=}")
    print(f"{carm_otherunit._output_world_meld_order=}")
    print(f"{patr_otherunit._output_world_meld_order=}")
    assert rico_otherunit._output_world_meld_order == 2
    assert carm_otherunit._output_world_meld_order == 0
    assert patr_otherunit._output_world_meld_order == 1


def test_WorldUnit_is_otherunits_credor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_credor_weight = 20
    carm_credor_weight = 30
    patr_credor_weight = 50
    yao_world.set_otherunit(otherunit_shop(rico_text, rico_credor_weight))
    yao_world.set_otherunit(otherunit_shop(carm_text, carm_credor_weight))
    yao_world.set_otherunit(otherunit_shop(patr_text, patr_credor_weight))
    # print(f"{yao_world._others.keys()=}")
    # for x_otherunit in yao_world._others.values():
    #     print(f"{x_otherunit.credor_weight=}")

    # WHEN / THEN
    assert yao_world.is_otherunits_credor_weight_sum_correct()
    yao_world.set_other_credor_pool(13)
    assert yao_world.is_otherunits_credor_weight_sum_correct() is False
    # WHEN / THEN
    yao_other_cred_pool = rico_credor_weight + carm_credor_weight + patr_credor_weight
    yao_world.set_other_credor_pool(yao_other_cred_pool)
    assert yao_world.is_otherunits_credor_weight_sum_correct()


def test_WorldUnit_is_otherunits_debtor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 60
    yao_world.set_otherunit(otherunit_shop(rico_text, None, rico_debtor_weight))
    yao_world.set_otherunit(otherunit_shop(carm_text, None, carm_debtor_weight))
    yao_world.set_otherunit(otherunit_shop(patr_text, None, patr_debtor_weight))

    # WHEN / THEN
    yao_other_debt_pool = rico_debtor_weight + carm_debtor_weight + patr_debtor_weight
    assert yao_world.is_otherunits_debtor_weight_sum_correct()
    yao_world.set_other_debtor_pool(yao_other_debt_pool + 1)
    assert yao_world.is_otherunits_debtor_weight_sum_correct() is False
    # WHEN / THEN
    yao_world.set_other_debtor_pool(yao_other_debt_pool)
    assert yao_world.is_otherunits_debtor_weight_sum_correct()


def test_WorldUnit_set_otherunit_external_metrics_SetsAttrs_credor_operational_debtor_operational():
    # GIVEN
    x_world = worldunit_shop("Yao")
    jane_text = "Jane Randolph"
    x_world.add_otherunit(jane_text)

    jane_other = x_world._others.get(jane_text)
    print(f"Before Other {jane_other.other_id} {jane_other._debtor_operational=} ")
    assert jane_other._debtor_operational is None
    assert jane_other._credor_operational is None

    assert sum(
        other_x._credor_operational is None for other_x in x_world._others.values()
    ) == len(x_world._others)
    assert sum(
        other_x._debtor_operational is None for other_x in x_world._others.values()
    ) == len(x_world._others)

    # WHEN
    jane_debtor_status = True
    jane_credor_status = True
    jane_metr = OtherUnitExternalMetrics(
        internal_other_id=jane_text,
        debtor_operational=jane_debtor_status,
        credor_operational=jane_credor_status,
    )
    x_world.set_otherunit_external_metrics(jane_metr)

    # THEN
    assert jane_other._debtor_operational == jane_debtor_status
    assert jane_other._credor_operational == jane_credor_status

    assert (
        sum(other_x._credor_operational is None for other_x in x_world._others.values())
        == len(x_world._others) - 1
    )
    assert (
        sum(other_x._debtor_operational is None for other_x in x_world._others.values())
        == len(x_world._others) - 1
    )
    assert (
        sum(other_x._credor_operational != None for other_x in x_world._others.values())
        == 1
    )
    assert (
        sum(other_x._debtor_operational != None for other_x in x_world._others.values())
        == 1
    )
