from src.agent.ally import AllyName, allylink_shop, allyunit_shop
from src.agent.group import GroupName, groupunit_shop, grouplink_shop
from src.agent.examples.example_agents import (
    agent_v001 as examples_agent_v001,
    agent_v001_with_large_agenda as examples_agent_v001_with_large_agenda,
)
from src.agent.agent import AgentUnit
from src.agent.idea import IdeaKid
from pytest import raises as pytest_raises
from src.world.bank_sqlstr import RiverTallyUnit


def test_agent_allys_exists():
    # GIVEN / WHEN
    a_x = AgentUnit()

    # THEN
    assert a_x._allys is None

    # GIVEN
    yahri_ally = allyunit_shop(name=AllyName("yahri"))
    allys_x = {yahri_ally.name: yahri_ally}
    a_x2 = AgentUnit()

    # WHEN
    a_x2.set_allyunit(allyunit=yahri_ally)

    # THEN
    assert a_x2._allys == allys_x


def test_example_has_allys():
    # GIVEN / WHEN
    a_x = examples_agent_v001()

    # THEN
    assert a_x._allys != None
    assert len(a_x._allys) == 22


def test_agent_set_ally_correctly_sets_allys_1():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    a_x.set_agent_metrics()
    assert len(a_x._allys) == 0
    assert len(a_x._groups) == 0

    # WHEN
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName("rico")))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName("carmen")))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName("patrick")))
    # future: if ally is new check group does not already have that name

    # THEN
    assert len(a_x._allys) == 3
    assert len(a_x._groups) == 3
    assert a_x._groups["rico"]._single_ally == True

    # WHEN
    a_x._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=GroupName("rico"), creditor_weight=10)
    )
    a_x._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=GroupName("carmen"), creditor_weight=10)
    )
    a_x._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=GroupName("patrick"), creditor_weight=10)
    )
    assert len(a_x._idearoot._grouplinks) == 3


def test_agent_set_ally_correctly_sets_allys_2():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    # WHEN
    a_x.add_allyunit(name=rico_text, uid=61, creditor_weight=13, debtor_weight=8)
    a_x.add_allyunit(name=carm_text, uid=5, debtor_weight=5)
    a_x.add_allyunit(name=patr_text, creditor_weight=17)
    # future: if ally is new check group does not already have that name

    # THEN
    assert len(a_x._allys) == 3
    assert len(a_x._groups) == 3
    assert a_x._groups[rico_text]._single_ally == True
    assert a_x._allys[patr_text].creditor_weight == 17
    assert a_x._allys[carm_text].debtor_weight == 5


def test_agent_get_idea_list_CorrectlySetsAllyLinkAgentCreditAndDebt():
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    bl_rico = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = grouplink_shop(name=patr_text, creditor_weight=10, debtor_weight=5)
    a_x._idearoot.set_grouplink(grouplink=bl_rico)
    a_x._idearoot.set_grouplink(grouplink=bl_carm)
    a_x._idearoot.set_grouplink(grouplink=bl_patr)

    rico_groupunit = a_x._groups.get(rico_text)
    carm_groupunit = a_x._groups.get(carm_text)
    patr_groupunit = a_x._groups.get(patr_text)
    rico_allylink = rico_groupunit._allys.get(rico_text)
    carm_allylink = carm_groupunit._allys.get(carm_text)
    patr_allylink = patr_groupunit._allys.get(patr_text)
    rico_allylink._agent_credit is None
    rico_allylink._agent_debt is None
    carm_allylink._agent_credit is None
    carm_allylink._agent_debt is None
    patr_allylink._agent_credit is None
    patr_allylink._agent_debt is None

    # for group in a_x._groups.values():
    #     for allylink in group._allys.values():
    #         assert allylink._agent_credit is None
    #         assert allylink._agent_debt is None

    a_x.set_agent_metrics()

    # for grouplink in a_x._groupheirs.values():
    #     print(
    #         f"{a_x._agent_importance=} {grouplink.name=} {grouplink._agent_credit=} {grouplink._agent_debt=}"
    #     )

    assert rico_allylink._agent_credit == 0.5
    assert rico_allylink._agent_debt == 0.8
    assert carm_allylink._agent_credit == 0.25
    assert carm_allylink._agent_debt == 0.1
    assert patr_allylink._agent_credit == 0.25
    assert patr_allylink._agent_debt == 0.1

    # allylink_agent_credit_sum = 0.0
    # allylink_agent_debt_sum = 0.0
    # for group in a_x._groups.values():
    #     # print(f"{group.name=} {group._allys=}")

    #     for allylink in group._allys.values():
    #         assert allylink._agent_credit != None
    #         assert allylink._agent_credit in [0.25, 0.5]
    #         assert allylink._agent_debt != None
    #         assert allylink._agent_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{group.name=} {allylink._agent_importance=} {group._agent_importance=}"
    #         # )
    #         allylink_agent_credit_sum += allylink._agent_credit
    #         allylink_agent_debt_sum += allylink._agent_debt

    #         # print(f"{allylink_agent_importance_sum=}")
    # assert allylink_agent_credit_sum == 1.0
    # assert allylink_agent_debt_sum == 1.0

    assert (
        rico_allylink._agent_credit
        + carm_allylink._agent_credit
        + patr_allylink._agent_credit
        == 1.0
    )
    assert (
        rico_allylink._agent_debt
        + carm_allylink._agent_debt
        + patr_allylink._agent_debt
        == 1.0
    )

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(selena_text)))
    a_x._idearoot.set_grouplink(
        grouplink=grouplink_shop(
            name=GroupName(selena_text), creditor_weight=20, debtor_weight=13
        )
    )
    a_x.set_agent_metrics()

    # THEN
    selena_groupunit = a_x._groups.get(selena_text)
    selena_allylink = selena_groupunit._allys.get(selena_text)

    assert rico_allylink._agent_credit != 0.25
    assert rico_allylink._agent_debt != 0.8
    assert carm_allylink._agent_credit != 0.25
    assert carm_allylink._agent_debt != 0.1
    assert patr_allylink._agent_credit != 0.5
    assert patr_allylink._agent_debt != 0.1
    assert selena_allylink._agent_credit != None
    assert selena_allylink._agent_debt != None

    # allylink_agent_credit_sum = 0.0
    # allylink_agent_debt_sum = 0.0

    # for group in a_x._groups.values():
    #     # print(f"{group.name=} {group._allys=}")

    #     for allylink in group._allys.values():
    #         assert allylink._agent_credit != None
    #         assert allylink._agent_credit not in [0.25, 0.5]
    #         assert allylink._agent_debt != None
    #         assert allylink._agent_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{group.name=} {allylink._agent_importance=} {group._agent_importance=}"
    #         # )
    #         allylink_agent_credit_sum += allylink._agent_credit
    #         allylink_agent_debt_sum += allylink._agent_debt

    #         # print(f"{allylink_agent_importance_sum=}")
    # assert allylink_agent_credit_sum == 1.0
    # assert allylink_agent_debt_sum > 0.9999999
    # assert allylink_agent_debt_sum < 1.00000001

    assert (
        rico_allylink._agent_credit
        + carm_allylink._agent_credit
        + patr_allylink._agent_credit
        + selena_allylink._agent_credit
        == 1.0
    )
    assert (
        rico_allylink._agent_debt
        + carm_allylink._agent_debt
        + patr_allylink._agent_debt
        + selena_allylink._agent_debt
        > 0.9999999
    )
    assert (
        rico_allylink._agent_debt
        + carm_allylink._agent_debt
        + patr_allylink._agent_debt
        + selena_allylink._agent_debt
        < 1.0
    )


def test_agent_get_idea_list_CorrectlySetsAllyUnitAgentImportance():
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    swim_text = "swim"
    a_x.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    bl_rico = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = grouplink_shop(name=patr_text, creditor_weight=10, debtor_weight=5)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=bl_rico)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=bl_carm)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=bl_patr)

    rico_allyunit = a_x._allys.get(rico_text)
    carm_allyunit = a_x._allys.get(carm_text)
    patr_allyunit = a_x._allys.get(patr_text)

    assert rico_allyunit._agent_credit is None
    assert rico_allyunit._agent_debt is None
    assert carm_allyunit._agent_credit is None
    assert carm_allyunit._agent_debt is None
    assert patr_allyunit._agent_credit is None
    assert patr_allyunit._agent_debt is None

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    allyunit_agent_credit_sum = 0.0
    allyunit_agent_debt_sum = 0.0

    assert rico_allyunit._agent_credit == 0.5
    assert rico_allyunit._agent_debt == 0.8
    assert carm_allyunit._agent_credit == 0.25
    assert carm_allyunit._agent_debt == 0.1
    assert patr_allyunit._agent_credit == 0.25
    assert patr_allyunit._agent_debt == 0.1

    assert (
        rico_allyunit._agent_credit
        + carm_allyunit._agent_credit
        + patr_allyunit._agent_credit
        == 1.0
    )
    assert (
        rico_allyunit._agent_debt
        + carm_allyunit._agent_debt
        + patr_allyunit._agent_debt
        == 1.0
    )

    # for allyunit in a_x._allys.values():
    #     assert allyunit._agent_credit != None
    #     assert allyunit._agent_credit in [0.25, 0.5]
    #     assert allyunit._agent_debt != None
    #     assert allyunit._agent_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {allyunit._agent_creditor=} {group._agent_creditor=}"
    #     # )
    #     print(f"{allyunit.name=} {allyunit._agent_credit=} {allyunit._agent_debt=} ")
    #     # print(f"{allyunit_agent_credit_sum=}")
    #     # print(f"{allyunit_agent_debt_sum=}")
    #     allyunit_agent_credit_sum += allyunit._agent_credit
    #     allyunit_agent_debt_sum += allyunit._agent_debt

    # assert allyunit_agent_credit_sum == 1.0
    # assert allyunit_agent_debt_sum > 0.9999999
    # assert allyunit_agent_debt_sum < 1.00000001

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(selena_text)))
    a_x._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=selena_text, creditor_weight=20, debtor_weight=10)
    )
    a_x.set_agent_metrics()

    # THEN
    selena_allyunit = a_x._allys.get(selena_text)

    assert rico_allyunit._agent_credit != 0.5
    assert rico_allyunit._agent_debt != 0.8
    assert carm_allyunit._agent_credit != 0.25
    assert carm_allyunit._agent_debt != 0.1
    assert patr_allyunit._agent_credit != 0.25
    assert patr_allyunit._agent_debt != 0.1
    assert selena_allyunit._agent_credit != None
    assert selena_allyunit._agent_debt != None

    assert (
        rico_allyunit._agent_credit
        + carm_allyunit._agent_credit
        + patr_allyunit._agent_credit
        < 1.0
    )
    assert (
        rico_allyunit._agent_credit
        + carm_allyunit._agent_credit
        + patr_allyunit._agent_credit
        + selena_allyunit._agent_credit
        == 1.0
    )
    assert (
        rico_allyunit._agent_debt
        + carm_allyunit._agent_debt
        + patr_allyunit._agent_debt
        < 1.0
    )
    assert (
        rico_allyunit._agent_debt
        + carm_allyunit._agent_debt
        + patr_allyunit._agent_debt
        + selena_allyunit._agent_debt
        == 1.0
    )

    # allyunit_agent_credit_sum = 0.0
    # allyunit_agent_debt_sum = 0.0

    # for allyunit in a_x._allys.values():
    #     assert allyunit._agent_credit != None
    #     assert allyunit._agent_credit not in [0.25, 0.5]
    #     assert allyunit._agent_debt != None
    #     assert allyunit._agent_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {allyunit._agent_creditor=} {group._agent_creditor=}"
    #     # )
    #     print(f"{allyunit.name=} {allyunit._agent_credit=} {allyunit._agent_debt=} ")
    #     # print(f"{allyunit_agent_credit_sum=}")
    #     # print(f"{allyunit_agent_debt_sum=}")
    #     allyunit_agent_credit_sum += allyunit._agent_credit
    #     allyunit_agent_debt_sum += allyunit._agent_debt

    # assert allyunit_agent_credit_sum == 1.0
    # assert allyunit_agent_debt_sum > 0.9999999
    # assert allyunit_agent_debt_sum < 1.00000001


def test_agent_get_idea_list_CorrectlySetsPartGroupedLWAllyUnitAgentImportance():
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    swim_text = "swim"
    a_x.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    bl_rico = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = grouplink_shop(name=patr_text, creditor_weight=10, debtor_weight=5)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=bl_rico)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=bl_carm)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=bl_patr)

    # no grouplinks attached to this one
    hunt_text = "hunt"
    a_x.add_idea(idea_kid=IdeaKid(_desc=hunt_text, _weight=3), walk=prom_text)

    assert a_x._idearoot._grouplinks is None

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    rico_groupunit = a_x._groups.get(rico_text)
    carm_groupunit = a_x._groups.get(carm_text)
    patr_groupunit = a_x._groups.get(patr_text)
    assert rico_groupunit._agent_credit != 0.5
    assert rico_groupunit._agent_debt != 0.8
    assert carm_groupunit._agent_credit != 0.25
    assert carm_groupunit._agent_debt != 0.1
    assert patr_groupunit._agent_credit != 0.25
    assert patr_groupunit._agent_debt != 0.1
    assert (
        rico_groupunit._agent_credit
        + carm_groupunit._agent_credit
        + patr_groupunit._agent_credit
        == 0.25
    )
    assert (
        rico_groupunit._agent_debt
        + carm_groupunit._agent_debt
        + patr_groupunit._agent_debt
        == 0.25
    )

    # groupunit_agent_credit_sum = 0.0
    # groupunit_agent_debt_sum = 0.0
    # for groupunit in a_x._groups.values():
    #     assert groupunit._agent_credit != None
    #     assert groupunit._agent_credit not in [0.25, 0.5]
    #     assert groupunit._agent_debt != None
    #     assert groupunit._agent_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {groupunit._agent_creditor=} {group._agent_creditor=}"
    #     # )
    #     print(f"{groupunit.name=} {groupunit._agent_credit=} {groupunit._agent_debt=} ")
    #     # print(f"{groupunit_agent_credit_sum=}")
    #     # print(f"{groupunit_agent_debt_sum=}")
    #     groupunit_agent_credit_sum += groupunit._agent_credit
    #     groupunit_agent_debt_sum += groupunit._agent_debt
    # assert groupunit_agent_credit_sum == 0.25
    # assert groupunit_agent_debt_sum == 0.25

    rico_allyunit = a_x._allys.get(rico_text)
    carm_allyunit = a_x._allys.get(carm_text)
    patr_allyunit = a_x._allys.get(patr_text)

    assert rico_allyunit._agent_credit == 0.375
    assert rico_allyunit._agent_debt == 0.45
    assert carm_allyunit._agent_credit == 0.3125
    assert carm_allyunit._agent_debt == 0.275
    assert patr_allyunit._agent_credit == 0.3125
    assert patr_allyunit._agent_debt == 0.275

    assert (
        rico_allyunit._agent_credit
        + carm_allyunit._agent_credit
        + patr_allyunit._agent_credit
        == 1.0
    )
    assert (
        rico_allyunit._agent_debt
        + carm_allyunit._agent_debt
        + patr_allyunit._agent_debt
        == 1.0
    )

    # allyunit_agent_credit_sum = 0.0
    # allyunit_agent_debt_sum = 0.0
    # for allyunit in a_x._allys.values():
    #     assert allyunit._agent_credit != None
    #     assert allyunit._agent_credit not in [0.25, 0.5]
    #     assert allyunit._agent_debt != None
    #     assert allyunit._agent_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {allyunit._agent_creditor=} {group._agent_creditor=}"
    #     # )
    #     print(f"{allyunit.name=} {allyunit._agent_credit=} {allyunit._agent_debt=} ")
    #     # print(f"{allyunit_agent_credit_sum=}")
    #     # print(f"{allyunit_agent_debt_sum=}")
    #     allyunit_agent_credit_sum += allyunit._agent_credit
    #     allyunit_agent_debt_sum += allyunit._agent_debt
    # assert allyunit_agent_credit_sum == 1.0
    # assert allyunit_agent_debt_sum > 0.9999999
    # assert allyunit_agent_debt_sum < 1.00000001


def test_agent_get_idea_list_WithAllAllysWeighted():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    a_x.add_idea(idea_kid=IdeaKid(_desc="swim"), walk="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(
        allyunit=allyunit_shop(name=AllyName(rico_text), creditor_weight=8)
    )
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    rico_allyunit = a_x._allys.get(rico_text)
    carm_allyunit = a_x._allys.get(carm_text)
    patr_allyunit = a_x._allys.get(patr_text)
    assert rico_allyunit._agent_credit is None
    assert rico_allyunit._agent_debt is None
    assert carm_allyunit._agent_credit is None
    assert carm_allyunit._agent_debt is None
    assert patr_allyunit._agent_credit is None
    assert patr_allyunit._agent_debt is None

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    assert (
        rico_allyunit._agent_credit
        + carm_allyunit._agent_credit
        + patr_allyunit._agent_credit
        == 1.0
    )
    assert (
        rico_allyunit._agent_debt
        + carm_allyunit._agent_debt
        + patr_allyunit._agent_debt
        == 1.0
    )
    # allyunit_agent_credit_sum = 0.0
    # allyunit_agent_debt_sum = 0.0
    # for allyunit in a_x._allys.values():
    #     assert allyunit._agent_credit != None
    #     assert allyunit._agent_credit not in [0.25, 0.5]
    #     assert allyunit._agent_debt != None
    #     assert allyunit._agent_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {allyunit._agent_creditor=} {group._agent_creditor=}"
    #     # )
    #     print(f"{allyunit.name=} {allyunit._agent_credit=} {allyunit._agent_debt=} ")
    #     # print(f"{allyunit_agent_credit_sum=}")
    #     # print(f"{allyunit_agent_debt_sum=}")
    #     allyunit_agent_credit_sum += allyunit._agent_credit
    #     allyunit_agent_debt_sum += allyunit._agent_debt
    # assert allyunit_agent_credit_sum == 1.0
    # assert allyunit_agent_debt_sum > 0.9999999
    # assert allyunit_agent_debt_sum < 1.00000001


def clear_all_allyunits_groupunits_agent_agenda_credit_debt(a_x: AgentUnit):
    # DELETE agent_agenda_debt and agent_agenda_credit
    for groupunit_x in a_x._groups.values():
        groupunit_x.reset_agent_credit_debt()
        # for allylink_x in groupunit_x._allys.values():
        #     print(f"{groupunit_x.name=} {allylink_x.creditor_weight=}  {allylink_x._agent_credit:.6f} {allylink_x.debtor_weight=} {allylink_x._agent_debt:.6f} {allylink_x.name=} ")

    # DELETE agent_agenda_debt and agent_agenda_credit
    for allyunit_x in a_x._allys.values():
        allyunit_x.reset_agent_credit_debt()


# sourcery skip: no-loop-in-tests
# sourcery skip: no-conditionals-in-tests
def test_agent_agenda_credit_debt_IsCorrectlySet():
    # GIVEN
    a_x = examples_agent_v001_with_large_agenda()
    clear_all_allyunits_groupunits_agent_agenda_credit_debt(a_x=a_x)

    # TEST agent_agenda_debt and agent_agenda_credit are empty
    sum_groupunit_agent_agenda_credit = 0
    sum_groupunit_agent_agenda_debt = 0
    sum_allylink_agent_agenda_credit = 0
    sum_allylink_agent_agenda_debt = 0
    for groupunit_x in a_x._groups.values():
        # print(f"{allyunit.name=}")
        sum_groupunit_agent_agenda_credit += groupunit_x._agent_agenda_credit
        sum_groupunit_agent_agenda_debt += groupunit_x._agent_agenda_debt
        for allylink_x in groupunit_x._allys.values():
            sum_allylink_agent_agenda_credit += allylink_x._agent_agenda_credit
            sum_allylink_agent_agenda_debt += allylink_x._agent_agenda_debt

    assert sum_groupunit_agent_agenda_credit == 0
    assert sum_groupunit_agent_agenda_debt == 0
    assert sum_allylink_agent_agenda_credit == 0
    assert sum_allylink_agent_agenda_debt == 0

    # TEST agent_agenda_debt and agent_agenda_credit are empty
    sum_allyunit_agent_agenda_credit = 0
    sum_allyunit_agent_agenda_debt = 0
    sum_allyunit_agent_agenda_ratio_credit = 0
    sum_allyunit_agent_agenda_ratio_debt = 0
    for allyunit in a_x._allys.values():
        # print(f"{allyunit.name=}")
        sum_allyunit_agent_agenda_credit += allyunit._agent_agenda_credit
        sum_allyunit_agent_agenda_debt += allyunit._agent_agenda_debt
        sum_allyunit_agent_agenda_ratio_credit += allyunit._agent_agenda_ratio_credit
        sum_allyunit_agent_agenda_ratio_debt += allyunit._agent_agenda_ratio_debt

    assert sum_allyunit_agent_agenda_credit == 0
    assert sum_allyunit_agent_agenda_debt == 0
    assert sum_allyunit_agent_agenda_ratio_credit == 0
    assert sum_allyunit_agent_agenda_ratio_debt == 0

    # WHEN
    agenda_list = a_x.get_agenda_items()

    # THEN
    assert len(agenda_list) == 68
    sum_agent_agenda_importance = 0
    agenda_no_grouplines_count = 0
    agenda_yes_grouplines_count = 0
    agenda_no_grouplines_agent_i_sum = 0
    agenda_yes_grouplines_agent_i_sum = 0
    for agenda_item in agenda_list:
        sum_agent_agenda_importance += agenda_item._agent_importance
        if agenda_item._grouplines == {}:
            agenda_no_grouplines_count += 1
            agenda_no_grouplines_agent_i_sum += agenda_item._agent_importance
        else:
            agenda_yes_grouplines_count += 1
            agenda_yes_grouplines_agent_i_sum += agenda_item._agent_importance
        # print(f"idea importance: {agenda_item._agent_importance:.7f} {sum_agent_agenda_importance:.5f} {agenda_item._desc=} ")
        # print(f"{agenda_item.get_road()}")
    print(f"{sum_agent_agenda_importance=}")
    assert agenda_no_grouplines_count == 20
    assert agenda_yes_grouplines_count == 48
    assert agenda_no_grouplines_agent_i_sum == 0.00447826215370075
    assert agenda_yes_grouplines_agent_i_sum == 0.0027152834170378025
    x2 = agenda_no_grouplines_agent_i_sum + agenda_yes_grouplines_agent_i_sum
    e10 = 0.0000000001
    assert abs(x2 - sum_agent_agenda_importance) < e10

    assert sum_agent_agenda_importance == 0.007193545570738553

    sum_groupunit_agent_agenda_credit = 0
    sum_groupunit_agent_agenda_debt = 0
    sum_allylink_agent_agenda_credit = 0
    sum_allylink_agent_agenda_debt = 0
    allylink_count = 0
    for groupunit_x in a_x._groups.values():
        # print(f"{allyunit.name=}")
        sum_groupunit_agent_agenda_credit += groupunit_x._agent_agenda_credit
        sum_groupunit_agent_agenda_debt += groupunit_x._agent_agenda_debt
        for allylink_x in groupunit_x._allys.values():
            sum_allylink_agent_agenda_credit += allylink_x._agent_agenda_credit
            sum_allylink_agent_agenda_debt += allylink_x._agent_agenda_debt
            allylink_count += 1

    assert allylink_count == 81
    x_sum = 0.0027152834170378025
    assert sum_groupunit_agent_agenda_credit == x_sum
    assert sum_groupunit_agent_agenda_debt == x_sum
    assert sum_allylink_agent_agenda_credit == x_sum
    assert sum_allylink_agent_agenda_debt == x_sum
    assert (
        abs(agenda_yes_grouplines_agent_i_sum - sum_groupunit_agent_agenda_credit) < e10
    )

    sum_allyunit_agent_agenda_credit = 0
    sum_allyunit_agent_agenda_debt = 0
    sum_allyunit_agent_agenda_ratio_credit = 0
    sum_allyunit_agent_agenda_ratio_debt = 0
    for allyunit in a_x._allys.values():
        assert allyunit._agent_credit != None
        assert allyunit._agent_credit not in [0.25, 0.5]
        assert allyunit._agent_debt != None
        assert allyunit._agent_debt not in [0.8, 0.1]  # print(f"{allyunit.name=}")
        sum_allyunit_agent_agenda_credit += allyunit._agent_agenda_credit
        sum_allyunit_agent_agenda_debt += allyunit._agent_agenda_debt
        sum_allyunit_agent_agenda_ratio_credit += allyunit._agent_agenda_ratio_credit
        sum_allyunit_agent_agenda_ratio_debt += allyunit._agent_agenda_ratio_debt

    assert abs(sum_allyunit_agent_agenda_credit - sum_agent_agenda_importance) < e10
    assert abs(sum_allyunit_agent_agenda_debt - sum_agent_agenda_importance) < e10
    assert abs(sum_allyunit_agent_agenda_ratio_credit - 1) < e10
    assert abs(sum_allyunit_agent_agenda_ratio_debt - 1) < e10

    # allyunit_agent_credit_sum = 0.0
    # allyunit_agent_debt_sum = 0.0

    # assert allyunit_agent_credit_sum == 1.0
    # assert allyunit_agent_debt_sum > 0.9999999
    # assert allyunit_agent_debt_sum < 1.00000001


def test_agent_agenda_ratio_credit_debt_IsCorrectlySetWhenAgendaIsEmpty():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_ally = allyunit_shop(name=rico_text, creditor_weight=0.5, debtor_weight=2)
    carm_ally = allyunit_shop(name=carm_text, creditor_weight=1.5, debtor_weight=3)
    patr_ally = allyunit_shop(name=patr_text, creditor_weight=8, debtor_weight=5)
    a_x.set_allyunit(allyunit=rico_ally)
    a_x.set_allyunit(allyunit=carm_ally)
    a_x.set_allyunit(allyunit=patr_ally)
    a_x_rico_ally = a_x._allys.get(rico_text)
    a_x_carm_ally = a_x._allys.get(carm_text)
    a_x_patr_ally = a_x._allys.get(patr_text)

    assert a_x_rico_ally._agent_agenda_credit in [0, None]
    assert a_x_rico_ally._agent_agenda_debt in [0, None]
    assert a_x_carm_ally._agent_agenda_credit in [0, None]
    assert a_x_carm_ally._agent_agenda_debt in [0, None]
    assert a_x_patr_ally._agent_agenda_credit in [0, None]
    assert a_x_patr_ally._agent_agenda_debt in [0, None]
    assert a_x_rico_ally._agent_agenda_ratio_credit != 0.05
    assert a_x_rico_ally._agent_agenda_ratio_debt != 0.2
    assert a_x_carm_ally._agent_agenda_ratio_credit != 0.15
    assert a_x_carm_ally._agent_agenda_ratio_debt != 0.3
    assert a_x_patr_ally._agent_agenda_ratio_credit != 0.8
    assert a_x_patr_ally._agent_agenda_ratio_debt != 0.5

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    assert a_x_rico_ally._agent_agenda_credit == 0
    assert a_x_rico_ally._agent_agenda_debt == 0
    assert a_x_carm_ally._agent_agenda_credit == 0
    assert a_x_carm_ally._agent_agenda_debt == 0
    assert a_x_patr_ally._agent_agenda_credit == 0
    assert a_x_patr_ally._agent_agenda_debt == 0
    assert a_x_rico_ally._agent_agenda_ratio_credit == 0.05
    assert a_x_rico_ally._agent_agenda_ratio_debt == 0.2
    assert a_x_carm_ally._agent_agenda_ratio_credit == 0.15
    assert a_x_carm_ally._agent_agenda_ratio_debt == 0.3
    assert a_x_patr_ally._agent_agenda_ratio_credit == 0.8
    assert a_x_patr_ally._agent_agenda_ratio_debt == 0.5


def test_agent_get_ally_groups_returnsCorrectData():
    a_x = AgentUnit(_desc="prom")
    a_x.add_idea(idea_kid=IdeaKid(_desc="swim"), walk="prom")
    rico = "rico"
    carmen = "carmen"
    patrick = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carmen)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patrick)))

    carmen_group_list = a_x.get_ally_groups(ally_name=carmen)
    assert carmen_group_list == [carmen]

    swimmers = "swimmers"
    carmen_ally_dict = {AllyName(carmen): allylink_shop(name=carmen)}
    swim_group = groupunit_shop(name=swimmers, _allys=carmen_ally_dict)
    a_x._groups[swim_group.name] = swim_group
    carmen_group_list = a_x.get_ally_groups(ally_name=carmen)
    assert carmen_group_list == [carmen, swimmers]


def test_agent_AllyUnit_CorrectlyCreatesNewName():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    a_x.add_allyunit(name=rico_text, uid=61, creditor_weight=13)
    a_x.add_allyunit(name="carmen", uid=5)
    a_x.add_allyunit(name="patrick", creditor_weight=17)
    assert len(a_x._allys) == 3
    assert a_x._allys.get(rico_text) != None
    assert a_x._allys.get(rico_text).creditor_weight == 13
    assert len(a_x._groups) == 3
    assert a_x._groups.get(rico_text) != None
    assert a_x._groups.get(rico_text)._single_ally == True

    # WHEN
    beto_text = "beta"
    a_x.edit_allyunit_name(
        old_name=rico_text,
        new_name=beto_text,
        allow_ally_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert a_x._allys.get(beto_text) != None
    assert a_x._allys.get(beto_text).creditor_weight == 13
    assert a_x._allys.get(rico_text) is None
    assert len(a_x._allys) == 3
    assert len(a_x._groups) == 3
    assert a_x._groups.get(rico_text) is None
    assert a_x._groups.get(beto_text) != None
    assert a_x._groups.get(beto_text)._single_ally == True


def test_agent_AllyUnit_raiseErrorNewNameAlreadyExists():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text, uid=61, creditor_weight=13)
    carmen_text = "carmen"
    sx.add_allyunit(name=carmen_text, uid=5)
    sx.add_allyunit(name="patrick", creditor_weight=17)
    assert len(sx._allys) == 3
    assert sx._allys.get(rico_text) != None
    assert sx._allys.get(rico_text).creditor_weight == 13
    assert len(sx._groups) == 3
    assert sx._groups.get(rico_text) != None
    assert sx._groups.get(rico_text)._single_ally == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_allyunit_name(
            old_name=rico_text,
            new_name=carmen_text,
            allow_ally_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Ally '{rico_text}' change to '{carmen_text}' failed since it already exists."
    )


def test_agent_AllyUnit_CorrectlyChangesGroupUnitAllyLinks():
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.add_allyunit(name=rico_text, uid=61, creditor_weight=13)
    a_x.add_allyunit(name=carm_text, uid=5)
    a_x.add_allyunit(name=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_ally_dict = {AllyName(carm_text): allylink_shop(name=carm_text)}
    swim_group = groupunit_shop(name=swim_text, _allys=carmen_ally_dict)
    swim_group.set_allylink(
        allylink=allylink_shop(name=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_allylink(
        allylink=allylink_shop(name=rico_text, creditor_weight=7, debtor_weight=30)
    )
    a_x.set_groupunit(groupunit=swim_group)

    swim_group = a_x._groups.get(swim_text)
    assert len(swim_group._allys) == 2
    assert swim_group._allys.get(rico_text) != None
    assert swim_group._allys.get(rico_text).creditor_weight == 7
    assert swim_group._allys.get(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    a_x.edit_allyunit_name(
        old_name=rico_text,
        new_name=beto_text,
        allow_ally_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._allys.get(beto_text) != None
    assert swim_group._allys.get(beto_text).creditor_weight == 7
    assert swim_group._allys.get(beto_text).debtor_weight == 30
    assert swim_group._allys.get(rico_text) is None
    assert len(swim_group._allys) == 2


def test_agent_AllyUnit_CorrectlyMergesNames():
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.add_allyunit(name=rico_text, uid=61, creditor_weight=13)
    a_x.add_allyunit(name=carm_text, uid=5, creditor_weight=3)
    a_x.add_allyunit(name=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_ally_dict = {AllyName(carm_text): allylink_shop(name=carm_text)}
    swim_group = groupunit_shop(name=swim_text, _allys=carmen_ally_dict)
    swim_group.set_allylink(
        allylink=allylink_shop(name=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_allylink(
        allylink=allylink_shop(name=rico_text, creditor_weight=7, debtor_weight=30)
    )
    a_x.set_groupunit(groupunit=swim_group)

    assert len(a_x._allys) == 3
    assert a_x._allys.get(rico_text) != None
    assert a_x._allys.get(rico_text).creditor_weight == 13
    assert a_x._allys.get(carm_text) != None
    assert a_x._allys.get(carm_text).creditor_weight == 3

    # WHEN / THEN
    a_x.edit_allyunit_name(
        old_name=rico_text,
        new_name=carm_text,
        allow_ally_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert a_x._allys.get(carm_text) != None
    assert a_x._allys.get(carm_text).creditor_weight == 16
    assert a_x._allys.get(rico_text) is None
    assert len(a_x._allys) == 2


def test_agent_AllyUnit_CorrectlyMergesGroupUnitAllyLinks():
    # GIVEN
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.add_allyunit(name=rico_text, uid=61, creditor_weight=13)
    a_x.add_allyunit(name=carm_text, uid=5)
    a_x.add_allyunit(name=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_ally_dict = {AllyName(carm_text): allylink_shop(name=carm_text)}
    swim_group = groupunit_shop(name=swim_text, _allys=carmen_ally_dict)
    swim_group.set_allylink(
        allylink=allylink_shop(name=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_allylink(
        allylink=allylink_shop(name=rico_text, creditor_weight=7, debtor_weight=30)
    )
    a_x.set_groupunit(groupunit=swim_group)

    swim_group = a_x._groups.get(swim_text)
    assert len(swim_group._allys) == 2
    assert swim_group._allys.get(rico_text) != None
    assert swim_group._allys.get(rico_text).creditor_weight == 7
    assert swim_group._allys.get(rico_text).debtor_weight == 30
    assert swim_group._allys.get(carm_text) != None
    assert swim_group._allys.get(carm_text).creditor_weight == 5
    assert swim_group._allys.get(carm_text).debtor_weight == 18

    # WHEN
    a_x.edit_allyunit_name(
        old_name=rico_text,
        new_name=carm_text,
        allow_ally_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._allys.get(carm_text) != None
    assert swim_group._allys.get(carm_text).creditor_weight == 12
    assert swim_group._allys.get(carm_text).debtor_weight == 48
    assert swim_group._allys.get(rico_text) is None
    assert len(swim_group._allys) == 1


def test_agent_AllyUnit_raiseErrorNewNameGroupUnitAlreadyExists():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    sx.add_allyunit(name=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(name=carmen_text)
    carmen_group.set_allylink(allylink=allylink_shop(name=rico_text))
    carmen_group.set_allylink(allylink=allylink_shop(name=anna_text))
    sx.set_groupunit(groupunit=carmen_group)
    assert len(sx._groups) == 3
    assert sx._allys.get(carmen_text) is None
    assert sx._groups.get(carmen_text)._single_ally == False
    assert len(sx._groups.get(carmen_text)._allys) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_allyunit_name(
            old_name=rico_text,
            new_name=carmen_text,
            allow_ally_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Ally '{rico_text}' change to '{carmen_text}' failed since non-single group '{carmen_text}' already exists."
    )


def test_agent_AllyUnit_CorrectlyOverwriteNewNameGroupUnit():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    sx.add_allyunit(name=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(name=carmen_text)
    carmen_group.set_allylink(allylink=allylink_shop(name=rico_text, creditor_weight=3))
    carmen_group.set_allylink(allylink=allylink_shop(name=anna_text, creditor_weight=5))
    sx.set_groupunit(groupunit=carmen_group)
    assert len(sx._groups) == 3
    assert sx._allys.get(rico_text) != None
    assert sx._allys.get(carmen_text) is None
    assert sx._groups.get(carmen_text)._single_ally == False
    assert len(sx._groups.get(carmen_text)._allys) == 2
    assert sx._groups.get(carmen_text)._allys.get(anna_text).creditor_weight == 5
    assert sx._groups.get(carmen_text)._allys.get(rico_text).creditor_weight == 3

    # WHEN
    sx.edit_allyunit_name(
        old_name=rico_text,
        new_name=carmen_text,
        allow_ally_overwite=False,
        allow_nonsingle_group_overwrite=True,
    )

    assert len(sx._groups) == 2
    assert sx._allys.get(rico_text) is None
    assert sx._allys.get(carmen_text) != None
    assert sx._groups.get(carmen_text)._single_ally == True
    assert len(sx._groups.get(carmen_text)._allys) == 1
    assert sx._groups.get(carmen_text)._allys.get(rico_text) is None
    assert sx._groups.get(carmen_text)._allys.get(carmen_text).creditor_weight == 1


def test_agent_set_all_allyunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_allyunit(allyunit=allyunit_shop(name=swim_text))
    sx.set_allyunit(allyunit=allyunit_shop(name=walk_text))
    sx.set_allyunit(allyunit=allyunit_shop(name=fly_text))
    assert sx._allys[swim_text].uid is None
    assert sx._allys[walk_text].uid is None
    assert sx._allys[fly_text].uid is None

    # WHEN
    sx.set_all_allyunits_uids_unique()

    # THEN
    assert sx._allys[swim_text].uid != None
    assert sx._allys[walk_text].uid != None
    assert sx._allys[fly_text].uid != None


def test_agent_set_all_allyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_allyunit(allyunit=allyunit_shop(name=swim_text, uid=3))
    sx.set_allyunit(allyunit=allyunit_shop(name=walk_text, uid=3))
    sx.set_allyunit(allyunit=allyunit_shop(name=fly_text))
    assert sx._allys[swim_text].uid == 3
    assert sx._allys[walk_text].uid == 3
    assert sx._allys[fly_text].uid is None

    # WHEN
    sx.set_all_allyunits_uids_unique()

    # THEN
    print(f"{sx._allys[swim_text].uid=}")
    print(f"{sx._allys[walk_text].uid=}")
    assert sx._allys[swim_text].uid != sx._allys[walk_text].uid
    assert sx._allys[walk_text].uid != 3
    assert sx._allys[walk_text].uid != 3
    assert sx._allys[fly_text].uid != None


def test_agent_set_all_allyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_allyunit(allyunit=allyunit_shop(name=swim_text, uid=3))
    sx.set_allyunit(allyunit=allyunit_shop(name=walk_text, uid=3))
    sx.set_allyunit(allyunit=allyunit_shop(name=fly_text))
    assert sx._allys[swim_text].uid == 3
    assert sx._allys[walk_text].uid == 3
    assert sx._allys[fly_text].uid is None

    # WHEN
    sx.set_all_allyunits_uids_unique()

    # THEN
    print(f"{sx._allys[swim_text].uid=}")
    print(f"{sx._allys[walk_text].uid=}")
    assert sx._allys[swim_text].uid != sx._allys[walk_text].uid
    assert sx._allys[walk_text].uid != 3
    assert sx._allys[walk_text].uid != 3
    assert sx._allys[fly_text].uid != None


def test_agent_all_allyunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_allyunit(allyunit=allyunit_shop(name=swim_text, uid=3))
    sx.set_allyunit(allyunit=allyunit_shop(name=walk_text, uid=3))
    sx.set_allyunit(allyunit=allyunit_shop(name=fly_text))
    assert sx._allys[swim_text].uid == 3
    assert sx._allys[walk_text].uid == 3
    assert sx._allys[fly_text].uid is None

    # WHEN1 / THEN
    assert sx.all_allyunits_uids_are_unique() == False

    # WHEN2
    sx.set_allyunit(allyunit=allyunit_shop(name=swim_text, uid=4))

    # THEN
    assert sx.all_allyunits_uids_are_unique() == False

    # WHEN3
    sx.set_allyunit(allyunit=allyunit_shop(name=fly_text, uid=5))

    # THEN
    assert sx.all_allyunits_uids_are_unique()


def test_agent_get_allyunits_name_list_CorrectlyReturnsListOfAllyUnits():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    sx.set_allyunit(allyunit=allyunit_shop(name=sam_text))
    sx.set_allyunit(allyunit=allyunit_shop(name=will_text))
    sx.set_allyunit(allyunit=allyunit_shop(name=fry_text))
    fun_text = "fun people"
    fun_group = groupunit_shop(name=fun_text)
    fun_group.set_allylink(allylink=allylink_shop(name=will_text))
    sx.set_groupunit(groupunit=fun_group)
    assert len(sx._groups) == 4
    assert len(sx._allys) == 3

    # WHEN
    allyunit_list_x = sx.get_allyunits_name_list()

    # THEN
    assert len(allyunit_list_x) == 4
    assert allyunit_list_x[0] == ""
    assert allyunit_list_x[1] == fry_text
    assert allyunit_list_x[2] == sam_text
    assert allyunit_list_x[3] == will_text


def test_agent_set_banking_data_allyunits_CorrectlySetsAllyUnitBankingAttr():
    # GIVEN
    bob_text = "bob"
    ax = AgentUnit(_desc=bob_text)
    ax.set_allys_empty_if_null()
    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    ax.set_allyunit(allyunit=allyunit_shop(name=sam_text))
    ax.set_allyunit(allyunit=allyunit_shop(name=wil_text))
    ax.set_allyunit(allyunit=allyunit_shop(name=fry_text))
    assert ax._allys.get(sam_text)._bank_tax_paid is None
    assert ax._allys.get(sam_text)._bank_tax_diff is None
    assert ax._allys.get(wil_text)._bank_tax_paid is None
    assert ax._allys.get(wil_text)._bank_tax_diff is None
    assert ax._allys.get(fry_text)._bank_tax_paid is None
    assert ax._allys.get(fry_text)._bank_tax_diff is None
    elu_allyunit = allyunit_shop(name=elu_text)
    elu_allyunit._bank_tax_paid = 0.003
    elu_allyunit._bank_tax_diff = 0.007
    ax.set_allyunit(allyunit=elu_allyunit)
    assert ax._allys.get(elu_text)._bank_tax_paid == 0.003
    assert ax._allys.get(elu_text)._bank_tax_diff == 0.007

    river_tally_sam = RiverTallyUnit(bob_text, sam_text, 0.209, 0, 0.034)
    river_tally_wil = RiverTallyUnit(bob_text, wil_text, 0.501, 0, 0.024)
    river_tally_fry = RiverTallyUnit(bob_text, fry_text, 0.111, 0, 0.006)
    river_tallys = {
        river_tally_sam.tax_name: river_tally_sam,
        river_tally_wil.tax_name: river_tally_wil,
        river_tally_fry.tax_name: river_tally_fry,
    }
    # WHEN
    ax.set_banking_attr_allyunits(river_tallys=river_tallys)

    # THEN
    assert ax._allys.get(sam_text)._bank_tax_paid == 0.209
    assert ax._allys.get(sam_text)._bank_tax_diff == 0.034
    assert ax._allys.get(wil_text)._bank_tax_paid == 0.501
    assert ax._allys.get(wil_text)._bank_tax_diff == 0.024
    assert ax._allys.get(fry_text)._bank_tax_paid == 0.111
    assert ax._allys.get(fry_text)._bank_tax_diff == 0.006
    assert ax._allys.get(elu_text)._bank_tax_paid is None
    assert ax._allys.get(elu_text)._bank_tax_diff is None
