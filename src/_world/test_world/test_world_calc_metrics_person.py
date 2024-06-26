from src._road.road import RoadUnit
from src._world.person import (
    PersonID,
    personlink_shop,
    personunit_shop,
    PersonUnitExternalMetrics,
)
from src._world.beliefunit import (
    BeliefID,
    beliefunit_shop,
    balancelink_shop,
    get_intersection_of_persons,
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


def test_WorldUnit_calc_world_metrics_CorrectlySetsPersonLinkWorldCredAndDebt():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_personunit(personunit=personunit_shop(PersonID(rico_text)))
    yao_world.set_personunit(personunit=personunit_shop(PersonID(carm_text)))
    yao_world.set_personunit(personunit=personunit_shop(PersonID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_world._idearoot.set_balancelink(balancelink=bl_rico)
    yao_world._idearoot.set_balancelink(balancelink=bl_carm)
    yao_world._idearoot.set_balancelink(balancelink=bl_patr)

    rico_beliefunit = yao_world.get_beliefunit(rico_text)
    carm_beliefunit = yao_world.get_beliefunit(carm_text)
    patr_beliefunit = yao_world.get_beliefunit(patr_text)
    rico_personlink = rico_beliefunit._persons.get(rico_text)
    carm_personlink = carm_beliefunit._persons.get(carm_text)
    patr_personlink = patr_beliefunit._persons.get(patr_text)
    rico_personlink._world_cred is None
    rico_personlink._world_debt is None
    carm_personlink._world_cred is None
    carm_personlink._world_debt is None
    patr_personlink._world_cred is None
    patr_personlink._world_debt is None

    # for belief in yao_world._beliefs.values():
    #     for personlink in belief._persons.values():
    #         assert personlink._world_cred is None
    #         assert personlink._world_debt is None

    yao_world.calc_world_metrics()

    # for balancelink in yao_world._balanceheirs.values():
    #     print(
    #         f"{yao_world._world_importance=} {balancelink.belief_id=} {balancelink._world_cred=} {balancelink._world_debt=}"
    #     )

    assert rico_personlink._world_cred == 0.5
    assert rico_personlink._world_debt == 0.8
    assert carm_personlink._world_cred == 0.25
    assert carm_personlink._world_debt == 0.1
    assert patr_personlink._world_cred == 0.25
    assert patr_personlink._world_debt == 0.1

    # personlink_world_cred_sum = 0.0
    # personlink_world_debt_sum = 0.0
    # for belief in yao_world._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._persons=}")

    #     for personlink in belief._persons.values():
    #         assert personlink._world_cred != None
    #         assert personlink._world_cred in [0.25, 0.5]
    #         assert personlink._world_debt != None
    #         assert personlink._world_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {personlink._world_importance=} {belief._world_importance=}"
    #         # )
    #         personlink_world_cred_sum += personlink._world_cred
    #         personlink_world_debt_sum += personlink._world_debt

    #         # print(f"{personlink_world_importance_sum=}")
    # assert personlink_world_cred_sum == 1.0
    # assert personlink_world_debt_sum == 1.0

    assert (
        rico_personlink._world_cred
        + carm_personlink._world_cred
        + patr_personlink._world_cred
        == 1.0
    )
    assert (
        rico_personlink._world_debt
        + carm_personlink._world_debt
        + patr_personlink._world_debt
        == 1.0
    )

    # WHEN anothher pledge, check metrics are as expected
    selena_text = "selena"
    yao_world.set_personunit(personunit=personunit_shop(PersonID(selena_text)))
    yao_world._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            belief_id=BeliefID(selena_text), credor_weight=20, debtor_weight=13
        )
    )
    yao_world.calc_world_metrics()

    # THEN
    selena_beliefunit = yao_world.get_beliefunit(selena_text)
    selena_personlink = selena_beliefunit._persons.get(selena_text)

    assert rico_personlink._world_cred != 0.25
    assert rico_personlink._world_debt != 0.8
    assert carm_personlink._world_cred != 0.25
    assert carm_personlink._world_debt != 0.1
    assert patr_personlink._world_cred != 0.5
    assert patr_personlink._world_debt != 0.1
    assert selena_personlink._world_cred != None
    assert selena_personlink._world_debt != None

    # personlink_world_cred_sum = 0.0
    # personlink_world_debt_sum = 0.0

    # for belief in yao_world._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._persons=}")

    #     for personlink in belief._persons.values():
    #         assert personlink._world_cred != None
    #         assert personlink._world_cred not in [0.25, 0.5]
    #         assert personlink._world_debt != None
    #         assert personlink._world_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {personlink._world_importance=} {belief._world_importance=}"
    #         # )
    #         personlink_world_cred_sum += personlink._world_cred
    #         personlink_world_debt_sum += personlink._world_debt

    #         # print(f"{personlink_world_importance_sum=}")
    # assert personlink_world_cred_sum == 1.0
    # assert personlink_world_debt_sum > 0.9999999
    # assert personlink_world_debt_sum < 1.00000001

    assert (
        rico_personlink._world_cred
        + carm_personlink._world_cred
        + patr_personlink._world_cred
        + selena_personlink._world_cred
        == 1.0
    )
    assert (
        rico_personlink._world_debt
        + carm_personlink._world_debt
        + patr_personlink._world_debt
        + selena_personlink._world_debt
        > 0.9999999
    )
    assert (
        rico_personlink._world_debt
        + carm_personlink._world_debt
        + patr_personlink._world_debt
        + selena_personlink._world_debt
        < 1.0
    )


def test_WorldUnit_calc_world_metrics_CorrectlySetsPersonUnitWorldImportance():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    swim_text = "swim"
    yao_world.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_personunit(personunit=personunit_shop(PersonID(rico_text)))
    yao_world.set_personunit(personunit=personunit_shop(PersonID(carm_text)))
    yao_world.set_personunit(personunit=personunit_shop(PersonID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_world._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_rico)
    yao_world._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_carm)
    yao_world._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_patr)

    rico_personunit = yao_world._persons.get(rico_text)
    carm_personunit = yao_world._persons.get(carm_text)
    patr_personunit = yao_world._persons.get(patr_text)

    assert rico_personunit._world_cred == 0
    assert rico_personunit._world_debt == 0
    assert carm_personunit._world_cred == 0
    assert carm_personunit._world_debt == 0
    assert patr_personunit._world_cred == 0
    assert patr_personunit._world_debt == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    personunit_world_cred_sum = 0.0
    personunit_world_debt_sum = 0.0

    assert rico_personunit._world_cred == 0.5
    assert rico_personunit._world_debt == 0.8
    assert carm_personunit._world_cred == 0.25
    assert carm_personunit._world_debt == 0.1
    assert patr_personunit._world_cred == 0.25
    assert patr_personunit._world_debt == 0.1

    assert (
        rico_personunit._world_cred
        + carm_personunit._world_cred
        + patr_personunit._world_cred
        == 1.0
    )
    assert (
        rico_personunit._world_debt
        + carm_personunit._world_debt
        + patr_personunit._world_debt
        == 1.0
    )

    # for personunit in yao_world._persons.values():
    #     assert personunit._world_cred != None
    #     assert personunit._world_cred in [0.25, 0.5]
    #     assert personunit._world_debt != None
    #     assert personunit._world_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {personunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{personunit.} {personunit._world_cred=} {personunit._world_debt=} ")
    #     # print(f"{personunit_world_cred_sum=}")
    #     # print(f"{personunit_world_debt_sum=}")
    #     personunit_world_cred_sum += personunit._world_cred
    #     personunit_world_debt_sum += personunit._world_debt

    # assert personunit_world_cred_sum == 1.0
    # assert personunit_world_debt_sum > 0.9999999
    # assert personunit_world_debt_sum < 1.00000001

    # WHEN anothher pledge, check metrics are as expected
    selena_text = "selena"
    yao_world.set_personunit(personunit=personunit_shop(PersonID(selena_text)))
    yao_world._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            belief_id=selena_text, credor_weight=20, debtor_weight=10
        )
    )
    yao_world.calc_world_metrics()

    # THEN
    selena_personunit = yao_world._persons.get(selena_text)

    assert rico_personunit._world_cred != 0.5
    assert rico_personunit._world_debt != 0.8
    assert carm_personunit._world_cred != 0.25
    assert carm_personunit._world_debt != 0.1
    assert patr_personunit._world_cred != 0.25
    assert patr_personunit._world_debt != 0.1
    assert selena_personunit._world_cred != None
    assert selena_personunit._world_debt != None

    assert (
        rico_personunit._world_cred
        + carm_personunit._world_cred
        + patr_personunit._world_cred
        < 1.0
    )
    assert (
        rico_personunit._world_cred
        + carm_personunit._world_cred
        + patr_personunit._world_cred
        + selena_personunit._world_cred
        == 1.0
    )
    assert (
        rico_personunit._world_debt
        + carm_personunit._world_debt
        + patr_personunit._world_debt
        < 1.0
    )
    assert (
        rico_personunit._world_debt
        + carm_personunit._world_debt
        + patr_personunit._world_debt
        + selena_personunit._world_debt
        == 1.0
    )

    # personunit_world_cred_sum = 0.0
    # personunit_world_debt_sum = 0.0

    # for personunit in yao_world._persons.values():
    #     assert personunit._world_cred != None
    #     assert personunit._world_cred not in [0.25, 0.5]
    #     assert personunit._world_debt != None
    #     assert personunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {personunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{personunit.} {personunit._world_cred=} {personunit._world_debt=} ")
    #     # print(f"{personunit_world_cred_sum=}")
    #     # print(f"{personunit_world_debt_sum=}")
    #     personunit_world_cred_sum += personunit._world_cred
    #     personunit_world_debt_sum += personunit._world_debt

    # assert personunit_world_cred_sum == 1.0
    # assert personunit_world_debt_sum > 0.9999999
    # assert personunit_world_debt_sum < 1.00000001


def test_WorldUnit_calc_world_metrics_CorrectlySetsPartBeliefedLWPersonUnitWorldImportance():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    swim_text = "swim"
    yao_world.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_personunit(personunit=personunit_shop(PersonID(rico_text)))
    yao_world.set_personunit(personunit=personunit_shop(PersonID(carm_text)))
    yao_world.set_personunit(personunit=personunit_shop(PersonID(patr_text)))
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

    rico_personunit = yao_world._persons.get(rico_text)
    carm_personunit = yao_world._persons.get(carm_text)
    patr_personunit = yao_world._persons.get(patr_text)

    assert rico_personunit._world_cred == 0.375
    assert rico_personunit._world_debt == 0.45
    assert carm_personunit._world_cred == 0.3125
    assert carm_personunit._world_debt == 0.275
    assert patr_personunit._world_cred == 0.3125
    assert patr_personunit._world_debt == 0.275

    assert (
        rico_personunit._world_cred
        + carm_personunit._world_cred
        + patr_personunit._world_cred
        == 1.0
    )
    assert (
        rico_personunit._world_debt
        + carm_personunit._world_debt
        + patr_personunit._world_debt
        == 1.0
    )

    # personunit_world_cred_sum = 0.0
    # personunit_world_debt_sum = 0.0
    # for personunit in yao_world._persons.values():
    #     assert personunit._world_cred != None
    #     assert personunit._world_cred not in [0.25, 0.5]
    #     assert personunit._world_debt != None
    #     assert personunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {personunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{personunit.} {personunit._world_cred=} {personunit._world_debt=} ")
    #     # print(f"{personunit_world_cred_sum=}")
    #     # print(f"{personunit_world_debt_sum=}")
    #     personunit_world_cred_sum += personunit._world_cred
    #     personunit_world_debt_sum += personunit._world_debt
    # assert personunit_world_cred_sum == 1.0
    # assert personunit_world_debt_sum > 0.9999999
    # assert personunit_world_debt_sum < 1.00000001


def test_WorldUnit_calc_world_metrics_CorrectlySetsPersonAttrs():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    yao_world.add_l1_idea(ideaunit_shop("swim"))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_world.set_personunit(
        personunit=personunit_shop(PersonID(rico_text), credor_weight=8)
    )
    yao_world.set_personunit(personunit=personunit_shop(PersonID(carm_text)))
    yao_world.set_personunit(personunit=personunit_shop(PersonID(patr_text)))
    rico_personunit = yao_world._persons.get(rico_text)
    carm_personunit = yao_world._persons.get(carm_text)
    patr_personunit = yao_world._persons.get(patr_text)
    assert rico_personunit._world_cred == 0
    assert rico_personunit._world_debt == 0
    assert carm_personunit._world_cred == 0
    assert carm_personunit._world_debt == 0
    assert patr_personunit._world_cred == 0
    assert patr_personunit._world_debt == 0

    # WHEN
    yao_world.calc_world_metrics()

    # THEN
    assert (
        rico_personunit._world_cred
        + carm_personunit._world_cred
        + patr_personunit._world_cred
        == 1.0
    )
    assert (
        rico_personunit._world_debt
        + carm_personunit._world_debt
        + patr_personunit._world_debt
        == 1.0
    )
    # personunit_world_cred_sum = 0.0
    # personunit_world_debt_sum = 0.0
    # for personunit in yao_world._persons.values():
    #     assert personunit._world_cred != None
    #     assert personunit._world_cred not in [0.25, 0.5]
    #     assert personunit._world_debt != None
    #     assert personunit._world_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {personunit._world_credor=} {belief._world_credor=}"
    #     # )
    #     print(f"{personunit.} {personunit._world_cred=} {personunit._world_debt=} ")
    #     # print(f"{personunit_world_cred_sum=}")
    #     # print(f"{personunit_world_debt_sum=}")
    #     personunit_world_cred_sum += personunit._world_cred
    #     personunit_world_debt_sum += personunit._world_debt
    # assert personunit_world_cred_sum == 1.0
    # assert personunit_world_debt_sum > 0.9999999
    # assert personunit_world_debt_sum < 1.00000001


def test_WorldUnit_calc_world_metrics_RaisesErrorWhen_is_personunits_credor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_world = worldunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_credor_weight = 20
    carm_credor_weight = 30
    patr_credor_weight = 50
    yao_world.set_personunit(personunit_shop(rico_text, None, rico_credor_weight))
    yao_world.set_personunit(personunit_shop(carm_text, None, carm_credor_weight))
    yao_world.set_personunit(personunit_shop(patr_text, None, patr_credor_weight))
    assert yao_world._person_credor_pool is None
    assert yao_world.is_personunits_credor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_person_credor_pool(x_int)
    assert yao_world.is_personunits_credor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_world.calc_world_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_personunits_credor_weight_sum_correct is False. _person_credor_pool={x_int}. personunits_credor_weight_sum={yao_world.get_personunits_credor_weight_sum()}"
    )

    # WHEN / THEN
    yao_world.set_person_credor_pool(yao_world.get_personunits_credor_weight_sum())
    assert yao_world.calc_world_metrics() is None


def test_WorldUnit_calc_world_metrics_DoesNotRaiseError_person_credor_poolWhenPersonSumIsZero():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    assert yao_world._person_credor_pool is None
    assert yao_world.is_personunits_credor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_person_credor_pool(x_int)

    # THEN
    assert yao_world.is_personunits_credor_weight_sum_correct()
    yao_world.calc_world_metrics()


def test_WorldUnit_calc_world_metrics_RaisesErrorWhen_is_personunits_debtor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_world = worldunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 40
    yao_world.set_personunit(personunit_shop(rico_text, None, None, rico_debtor_weight))
    yao_world.set_personunit(personunit_shop(carm_text, None, None, carm_debtor_weight))
    yao_world.set_personunit(personunit_shop(patr_text, None, None, patr_debtor_weight))
    assert yao_world._person_debtor_pool is None
    assert yao_world.is_personunits_debtor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_person_debtor_pool(x_int)
    assert yao_world.is_personunits_debtor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_world.calc_world_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_personunits_debtor_weight_sum_correct is False. _person_debtor_pool={x_int}. personunits_debtor_weight_sum={yao_world.get_personunits_debtor_weight_sum()}"
    )

    # WHEN / THEN
    yao_world.set_person_debtor_pool(yao_world.get_personunits_debtor_weight_sum())
    assert yao_world.calc_world_metrics() is None


def test_WorldUnit_calc_world_metrics_DoesNotRaiseError_person_debtor_poolWhenPersonSumIsZero():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    assert yao_world._person_credor_pool is None
    assert yao_world.is_personunits_debtor_weight_sum_correct()
    assert yao_world.calc_world_metrics() is None

    # WHEN
    x_int = 13
    yao_world.set_person_debtor_pool(x_int)

    # THEN
    assert yao_world.is_personunits_debtor_weight_sum_correct()
    yao_world.calc_world_metrics()


def clear_all_personunits_beliefunits_world_agenda_cred_debt(x_world: WorldUnit):
    # DELETE world_agenda_debt and world_agenda_cred
    for beliefunit_x in x_world._beliefs.values():
        beliefunit_x.reset_world_cred_debt()
        # for personlink_x in beliefunit_x._persons.values():
        #     print(f"{beliefunit_x.belief_id=} {personlink_x.credor_weight=}  {personlink_x._world_cred:.6f} {personlink_x.debtor_weight=} {personlink_x._world_debt:.6f} {personlink_x.} ")

    # DELETE world_agenda_debt and world_agenda_cred
    for x_personunit in x_world._persons.values():
        x_personunit.reset_world_cred_debt()


@dataclass
class BeliefAgendaMetrics:
    sum_beliefunit_cred: float = 0
    sum_beliefunit_debt: float = 0
    sum_personlink_cred: float = 0
    sum_personlink_debt: float = 0
    personlink_count: int = 0

    def set_sums(self, x_world: WorldUnit):
        for beliefunit_x in x_world._beliefs.values():
            self.sum_beliefunit_cred += beliefunit_x._world_agenda_cred
            self.sum_beliefunit_debt += beliefunit_x._world_agenda_debt
            for personlink_x in beliefunit_x._persons.values():
                self.sum_personlink_cred += personlink_x._world_agenda_cred
                self.sum_personlink_debt += personlink_x._world_agenda_debt
                self.personlink_count += 1


@dataclass
class PersonAgendaMetrics:
    sum_agenda_cred: float = 0
    sum_agenda_debt: float = 0
    sum_agenda_ratio_cred: float = 0
    sum_agenda_ratio_debt: float = 0

    def set_sums(self, x_world: WorldUnit):
        for personunit in x_world._persons.values():
            self.sum_agenda_cred += personunit._world_agenda_cred
            self.sum_agenda_debt += personunit._world_agenda_debt
            self.sum_agenda_ratio_cred += personunit._world_agenda_ratio_cred
            self.sum_agenda_ratio_debt += personunit._world_agenda_ratio_debt


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
    clear_all_personunits_beliefunits_world_agenda_cred_debt(x_world=x_world)

    # TEST world_agenda_debt and world_agenda_cred are empty
    x_beliefagendametrics = BeliefAgendaMetrics()
    x_beliefagendametrics.set_sums(x_world=x_world)
    assert x_beliefagendametrics.sum_beliefunit_cred == 0
    assert x_beliefagendametrics.sum_beliefunit_debt == 0
    assert x_beliefagendametrics.sum_personlink_cred == 0
    assert x_beliefagendametrics.sum_personlink_debt == 0

    # TEST world_agenda_debt and world_agenda_cred are empty
    x_personagendametrics = PersonAgendaMetrics()
    x_personagendametrics.set_sums(x_world=x_world)
    assert x_personagendametrics.sum_agenda_cred == 0
    assert x_personagendametrics.sum_agenda_debt == 0
    assert x_personagendametrics.sum_agenda_ratio_cred == 0
    assert x_personagendametrics.sum_agenda_ratio_debt == 0

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
    assert x_beliefagendametrics.personlink_count == 81
    x_sum = 0.0027965049894874455
    assert are_equal(x_beliefagendametrics.sum_beliefunit_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_beliefunit_debt, x_sum)
    assert are_equal(x_beliefagendametrics.sum_personlink_cred, x_sum)
    assert are_equal(x_beliefagendametrics.sum_personlink_debt, x_sum)
    assert are_equal(
        x_balanceagendametrics.agenda_yes_world_i_sum,
        x_beliefagendametrics.sum_beliefunit_cred,
    )

    assert all_personunits_have_legitimate_values(x_world)

    x_personagendametrics = PersonAgendaMetrics()
    x_personagendametrics.set_sums(x_world=x_world)
    assert are_equal(
        x_personagendametrics.sum_agenda_cred,
        x_balanceagendametrics.sum_world_agenda_importance,
    )
    assert are_equal(
        x_personagendametrics.sum_agenda_debt,
        x_balanceagendametrics.sum_world_agenda_importance,
    )
    assert are_equal(x_personagendametrics.sum_agenda_ratio_cred, 1)
    assert are_equal(x_personagendametrics.sum_agenda_ratio_debt, 1)

    # personunit_world_cred_sum = 0.0
    # personunit_world_debt_sum = 0.0

    # assert personunit_world_cred_sum == 1.0
    # assert personunit_world_debt_sum > 0.9999999
    # assert personunit_world_debt_sum < 1.00000001


def all_personunits_have_legitimate_values(x_world: WorldUnit):
    return not any(
        (
            personunit._world_cred is None
            or personunit._world_cred in [0.25, 0.5]
            or personunit._world_debt is None
            or personunit._world_debt in [0.8, 0.1]
        )
        for personunit in x_world._persons.values()
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
    rico_person = personunit_shop(rico_text, credor_weight=0.5, debtor_weight=2)
    carm_person = personunit_shop(carm_text, credor_weight=1.5, debtor_weight=3)
    patr_person = personunit_shop(patr_text, credor_weight=8, debtor_weight=5)
    noa_world.set_personunit(personunit=rico_person)
    noa_world.set_personunit(personunit=carm_person)
    noa_world.set_personunit(personunit=patr_person)
    noa_world_rico_person = noa_world._persons.get(rico_text)
    noa_world_carm_person = noa_world._persons.get(carm_text)
    noa_world_patr_person = noa_world._persons.get(patr_text)

    assert noa_world_rico_person._world_agenda_cred in [0, None]
    assert noa_world_rico_person._world_agenda_debt in [0, None]
    assert noa_world_carm_person._world_agenda_cred in [0, None]
    assert noa_world_carm_person._world_agenda_debt in [0, None]
    assert noa_world_patr_person._world_agenda_cred in [0, None]
    assert noa_world_patr_person._world_agenda_debt in [0, None]
    assert noa_world_rico_person._world_agenda_ratio_cred != 0.05
    assert noa_world_rico_person._world_agenda_ratio_debt != 0.2
    assert noa_world_carm_person._world_agenda_ratio_cred != 0.15
    assert noa_world_carm_person._world_agenda_ratio_debt != 0.3
    assert noa_world_patr_person._world_agenda_ratio_cred != 0.8
    assert noa_world_patr_person._world_agenda_ratio_debt != 0.5

    # WHEN
    noa_world.calc_world_metrics()

    # THEN
    assert noa_world_rico_person._world_agenda_cred == 0
    assert noa_world_rico_person._world_agenda_debt == 0
    assert noa_world_carm_person._world_agenda_cred == 0
    assert noa_world_carm_person._world_agenda_debt == 0
    assert noa_world_patr_person._world_agenda_cred == 0
    assert noa_world_patr_person._world_agenda_debt == 0
    assert noa_world_rico_person._world_agenda_ratio_cred == 0.05
    assert noa_world_rico_person._world_agenda_ratio_debt == 0.2
    assert noa_world_carm_person._world_agenda_ratio_cred == 0.15
    assert noa_world_carm_person._world_agenda_ratio_debt == 0.3
    assert noa_world_patr_person._world_agenda_ratio_cred == 0.8
    assert noa_world_patr_person._world_agenda_ratio_debt == 0.5
