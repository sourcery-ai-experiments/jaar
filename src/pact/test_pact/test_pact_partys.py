from src.pact.party import PartyTitle, partylink_shop, partyunit_shop
from src.pact.group import GroupBrand, groupunit_shop, balancelink_shop
from src.pact.examples.example_pacts import (
    pact_v001 as examples_pact_v001,
    pact_v001_with_large_agenda as examples_pact_v001_with_large_agenda,
)
from src.pact.pact import PactUnit, get_intersection_of_partys
from src.pact.idea import IdeaKid
from pytest import raises as pytest_raises
from src.cure.bank_sqlstr import RiverTpartyUnit


def test_pact_partys_exists():
    # GIVEN / WHEN
    x_pact = PactUnit()

    # THEN
    assert x_pact._partys is None

    # GIVEN
    yahri_party = partyunit_shop(title=PartyTitle("yahri"))
    partys_x = {yahri_party.title: yahri_party}
    x_pact2 = PactUnit()

    # WHEN
    x_pact2.set_partyunit(partyunit=yahri_party)

    # THEN
    assert x_pact2._partys == partys_x


def test_example_has_partys():
    # GIVEN / WHEN
    x_pact = examples_pact_v001()

    # THEN
    assert x_pact._partys != None
    assert len(x_pact._partys) == 22


def test_pact_set_party_correctly_sets_partys_1():
    # GIVEN
    x_pact = PactUnit(_healer="prom")
    x_pact.set_pact_metrics()
    assert len(x_pact._partys) == 0
    assert len(x_pact._groups) == 0

    # WHEN
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle("rico")))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle("carmen")))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle("patrick")))

    # THEN
    assert len(x_pact._partys) == 3
    assert len(x_pact._groups) == 3
    assert x_pact._groups["rico"]._single_party == True

    # WHEN
    x_pact._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand("rico"), creditor_weight=10)
    )
    x_pact._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand("carmen"), creditor_weight=10)
    )
    x_pact._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand("patrick"), creditor_weight=10)
    )
    assert len(x_pact._idearoot._balancelinks) == 3


def test_pact_set_party_correctly_sets_partys_2():
    # GIVEN
    x_pact = PactUnit(_healer="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    assign_text = "assignment"

    # WHEN
    x_pact.add_partyunit(title=rico_text, uid=61, creditor_weight=13, debtor_weight=8)
    x_pact.add_partyunit(title=carm_text, uid=5, debtor_weight=5)
    x_pact.add_partyunit(
        title=patr_text, creditor_weight=17, depotlink_type=assign_text
    )

    # THEN
    assert len(x_pact._partys) == 3
    assert len(x_pact._groups) == 3
    assert x_pact._groups.get(rico_text)._single_party == True
    assert x_pact._partys.get(patr_text).creditor_weight == 17
    assert x_pact._partys.get(carm_text).debtor_weight == 5
    assert x_pact._partys.get(patr_text).depotlink_type == assign_text


def test_pact_get_party_CorrectlyGetsParty():
    # GIVEN
    x_pact = PactUnit(_healer="prom")
    rico_text = "rico"
    carm_text = "carmen"
    x_pact.add_partyunit(title=rico_text)
    x_pact.add_partyunit(title=carm_text)

    # WHEN
    rico_party = x_pact.get_party(rico_text)
    carm_party = x_pact.get_party(carm_text)

    # THEN
    assert rico_party == x_pact._partys.get(rico_text)
    assert carm_party == x_pact._partys.get(carm_text)


def test_pact_get_partys_depotlink_count_GetsCorrectCount():
    # GIVEN
    sue_text = "sue"
    sue_x_pact = PactUnit(_healer=sue_text)
    assign_text = "assignment"

    # WHEN
    rico_text = "rico"
    carm_text = "carmen"
    sue_x_pact.add_partyunit(title=rico_text)
    sue_x_pact.add_partyunit(title=carm_text)
    # THEN
    assert len(sue_x_pact._partys) == 2
    assert sue_x_pact.get_partys_depotlink_count() == 0

    # WHEN
    patr_text = "patrick"
    sue_x_pact.add_partyunit(title=patr_text, depotlink_type=assign_text)
    # THEN
    assert len(sue_x_pact._partys) == 3
    assert sue_x_pact.get_partys_depotlink_count() == 1

    # WHEN
    rico_party = sue_x_pact.get_party(rico_text)
    rico_party.set_depotlink_type(assign_text)
    # THEN
    assert len(sue_x_pact._partys) == 3
    assert sue_x_pact.get_partys_depotlink_count() == 2


def test_pact_get_idea_list_CorrectlySetsPartyLinkPactCreditAndDebt():
    # GIVEN
    prom_text = "prom"
    x_pact = PactUnit(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))
    bl_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    x_pact._idearoot.set_balancelink(balancelink=bl_rico)
    x_pact._idearoot.set_balancelink(balancelink=bl_carm)
    x_pact._idearoot.set_balancelink(balancelink=bl_patr)

    rico_groupunit = x_pact._groups.get(rico_text)
    carm_groupunit = x_pact._groups.get(carm_text)
    patr_groupunit = x_pact._groups.get(patr_text)
    rico_partylink = rico_groupunit._partys.get(rico_text)
    carm_partylink = carm_groupunit._partys.get(carm_text)
    patr_partylink = patr_groupunit._partys.get(patr_text)
    rico_partylink._pact_credit is None
    rico_partylink._pact_debt is None
    carm_partylink._pact_credit is None
    carm_partylink._pact_debt is None
    patr_partylink._pact_credit is None
    patr_partylink._pact_debt is None

    # for group in x_pact._groups.values():
    #     for partylink in group._partys.values():
    #         assert partylink._pact_credit is None
    #         assert partylink._pact_debt is None

    x_pact.set_pact_metrics()

    # for balancelink in x_pact._balanceheirs.values():
    #     print(
    #         f"{x_pact._pact_importance=} {balancelink.brand=} {balancelink._pact_credit=} {balancelink._pact_debt=}"
    #     )

    assert rico_partylink._pact_credit == 0.5
    assert rico_partylink._pact_debt == 0.8
    assert carm_partylink._pact_credit == 0.25
    assert carm_partylink._pact_debt == 0.1
    assert patr_partylink._pact_credit == 0.25
    assert patr_partylink._pact_debt == 0.1

    # partylink_pact_credit_sum = 0.0
    # partylink_pact_debt_sum = 0.0
    # for group in x_pact._groups.values():
    #     # print(f"{group.brand=} {group._partys=}")

    #     for partylink in group._partys.values():
    #         assert partylink._pact_credit != None
    #         assert partylink._pact_credit in [0.25, 0.5]
    #         assert partylink._pact_debt != None
    #         assert partylink._pact_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{group.brand=} {partylink._pact_importance=} {group._pact_importance=}"
    #         # )
    #         partylink_pact_credit_sum += partylink._pact_credit
    #         partylink_pact_debt_sum += partylink._pact_debt

    #         # print(f"{partylink_pact_importance_sum=}")
    # assert partylink_pact_credit_sum == 1.0
    # assert partylink_pact_debt_sum == 1.0

    assert (
        rico_partylink._pact_credit
        + carm_partylink._pact_credit
        + patr_partylink._pact_credit
        == 1.0
    )
    assert (
        rico_partylink._pact_debt
        + carm_partylink._pact_debt
        + patr_partylink._pact_debt
        == 1.0
    )

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(selena_text)))
    x_pact._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            brand=GroupBrand(selena_text), creditor_weight=20, debtor_weight=13
        )
    )
    x_pact.set_pact_metrics()

    # THEN
    selena_groupunit = x_pact._groups.get(selena_text)
    selena_partylink = selena_groupunit._partys.get(selena_text)

    assert rico_partylink._pact_credit != 0.25
    assert rico_partylink._pact_debt != 0.8
    assert carm_partylink._pact_credit != 0.25
    assert carm_partylink._pact_debt != 0.1
    assert patr_partylink._pact_credit != 0.5
    assert patr_partylink._pact_debt != 0.1
    assert selena_partylink._pact_credit != None
    assert selena_partylink._pact_debt != None

    # partylink_pact_credit_sum = 0.0
    # partylink_pact_debt_sum = 0.0

    # for group in x_pact._groups.values():
    #     # print(f"{group.brand=} {group._partys=}")

    #     for partylink in group._partys.values():
    #         assert partylink._pact_credit != None
    #         assert partylink._pact_credit not in [0.25, 0.5]
    #         assert partylink._pact_debt != None
    #         assert partylink._pact_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{group.brand=} {partylink._pact_importance=} {group._pact_importance=}"
    #         # )
    #         partylink_pact_credit_sum += partylink._pact_credit
    #         partylink_pact_debt_sum += partylink._pact_debt

    #         # print(f"{partylink_pact_importance_sum=}")
    # assert partylink_pact_credit_sum == 1.0
    # assert partylink_pact_debt_sum > 0.9999999
    # assert partylink_pact_debt_sum < 1.00000001

    assert (
        rico_partylink._pact_credit
        + carm_partylink._pact_credit
        + patr_partylink._pact_credit
        + selena_partylink._pact_credit
        == 1.0
    )
    assert (
        rico_partylink._pact_debt
        + carm_partylink._pact_debt
        + patr_partylink._pact_debt
        + selena_partylink._pact_debt
        > 0.9999999
    )
    assert (
        rico_partylink._pact_debt
        + carm_partylink._pact_debt
        + patr_partylink._pact_debt
        + selena_partylink._pact_debt
        < 1.0
    )


def test_pact_get_idea_list_CorrectlySetsPartyUnitPactImportance():
    # GIVEN
    prom_text = "prom"
    x_pact = PactUnit(_healer=prom_text)
    swim_text = "swim"
    x_pact.add_idea(idea_kid=IdeaKid(_label=swim_text), pad=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))
    bl_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    x_pact._idearoot._kids[swim_text].set_balancelink(balancelink=bl_rico)
    x_pact._idearoot._kids[swim_text].set_balancelink(balancelink=bl_carm)
    x_pact._idearoot._kids[swim_text].set_balancelink(balancelink=bl_patr)

    rico_partyunit = x_pact._partys.get(rico_text)
    carm_partyunit = x_pact._partys.get(carm_text)
    patr_partyunit = x_pact._partys.get(patr_text)

    assert rico_partyunit._pact_credit is None
    assert rico_partyunit._pact_debt is None
    assert carm_partyunit._pact_credit is None
    assert carm_partyunit._pact_debt is None
    assert patr_partyunit._pact_credit is None
    assert patr_partyunit._pact_debt is None

    # WHEN
    x_pact.set_pact_metrics()

    # THEN
    partyunit_pact_credit_sum = 0.0
    partyunit_pact_debt_sum = 0.0

    assert rico_partyunit._pact_credit == 0.5
    assert rico_partyunit._pact_debt == 0.8
    assert carm_partyunit._pact_credit == 0.25
    assert carm_partyunit._pact_debt == 0.1
    assert patr_partyunit._pact_credit == 0.25
    assert patr_partyunit._pact_debt == 0.1

    assert (
        rico_partyunit._pact_credit
        + carm_partyunit._pact_credit
        + patr_partyunit._pact_credit
        == 1.0
    )
    assert (
        rico_partyunit._pact_debt
        + carm_partyunit._pact_debt
        + patr_partyunit._pact_debt
        == 1.0
    )

    # for partyunit in x_pact._partys.values():
    #     assert partyunit._pact_credit != None
    #     assert partyunit._pact_credit in [0.25, 0.5]
    #     assert partyunit._pact_debt != None
    #     assert partyunit._pact_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._pact_creditor=} {group._pact_creditor=}"
    #     # )
    #     print(f"{partyunit.title=} {partyunit._pact_credit=} {partyunit._pact_debt=} ")
    #     # print(f"{partyunit_pact_credit_sum=}")
    #     # print(f"{partyunit_pact_debt_sum=}")
    #     partyunit_pact_credit_sum += partyunit._pact_credit
    #     partyunit_pact_debt_sum += partyunit._pact_debt

    # assert partyunit_pact_credit_sum == 1.0
    # assert partyunit_pact_debt_sum > 0.9999999
    # assert partyunit_pact_debt_sum < 1.00000001

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(selena_text)))
    x_pact._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            brand=selena_text, creditor_weight=20, debtor_weight=10
        )
    )
    x_pact.set_pact_metrics()

    # THEN
    selena_partyunit = x_pact._partys.get(selena_text)

    assert rico_partyunit._pact_credit != 0.5
    assert rico_partyunit._pact_debt != 0.8
    assert carm_partyunit._pact_credit != 0.25
    assert carm_partyunit._pact_debt != 0.1
    assert patr_partyunit._pact_credit != 0.25
    assert patr_partyunit._pact_debt != 0.1
    assert selena_partyunit._pact_credit != None
    assert selena_partyunit._pact_debt != None

    assert (
        rico_partyunit._pact_credit
        + carm_partyunit._pact_credit
        + patr_partyunit._pact_credit
        < 1.0
    )
    assert (
        rico_partyunit._pact_credit
        + carm_partyunit._pact_credit
        + patr_partyunit._pact_credit
        + selena_partyunit._pact_credit
        == 1.0
    )
    assert (
        rico_partyunit._pact_debt
        + carm_partyunit._pact_debt
        + patr_partyunit._pact_debt
        < 1.0
    )
    assert (
        rico_partyunit._pact_debt
        + carm_partyunit._pact_debt
        + patr_partyunit._pact_debt
        + selena_partyunit._pact_debt
        == 1.0
    )

    # partyunit_pact_credit_sum = 0.0
    # partyunit_pact_debt_sum = 0.0

    # for partyunit in x_pact._partys.values():
    #     assert partyunit._pact_credit != None
    #     assert partyunit._pact_credit not in [0.25, 0.5]
    #     assert partyunit._pact_debt != None
    #     assert partyunit._pact_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._pact_creditor=} {group._pact_creditor=}"
    #     # )
    #     print(f"{partyunit.title=} {partyunit._pact_credit=} {partyunit._pact_debt=} ")
    #     # print(f"{partyunit_pact_credit_sum=}")
    #     # print(f"{partyunit_pact_debt_sum=}")
    #     partyunit_pact_credit_sum += partyunit._pact_credit
    #     partyunit_pact_debt_sum += partyunit._pact_debt

    # assert partyunit_pact_credit_sum == 1.0
    # assert partyunit_pact_debt_sum > 0.9999999
    # assert partyunit_pact_debt_sum < 1.00000001


def test_pact_get_idea_list_CorrectlySetsPartGroupedLWPartyUnitPactImportance():
    # GIVEN
    prom_text = "prom"
    x_pact = PactUnit(_healer=prom_text)
    swim_text = "swim"
    x_pact.add_idea(idea_kid=IdeaKid(_label=swim_text), pad=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))
    bl_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    x_pact._idearoot._kids[swim_text].set_balancelink(balancelink=bl_rico)
    x_pact._idearoot._kids[swim_text].set_balancelink(balancelink=bl_carm)
    x_pact._idearoot._kids[swim_text].set_balancelink(balancelink=bl_patr)

    # no balancelinks attached to this one
    hunt_text = "hunt"
    x_pact.add_idea(idea_kid=IdeaKid(_label=hunt_text, _weight=3), pad=prom_text)

    assert x_pact._idearoot._balancelinks is None

    # WHEN
    x_pact.set_pact_metrics()

    # THEN
    rico_groupunit = x_pact._groups.get(rico_text)
    carm_groupunit = x_pact._groups.get(carm_text)
    patr_groupunit = x_pact._groups.get(patr_text)
    assert rico_groupunit._pact_credit != 0.5
    assert rico_groupunit._pact_debt != 0.8
    assert carm_groupunit._pact_credit != 0.25
    assert carm_groupunit._pact_debt != 0.1
    assert patr_groupunit._pact_credit != 0.25
    assert patr_groupunit._pact_debt != 0.1
    assert (
        rico_groupunit._pact_credit
        + carm_groupunit._pact_credit
        + patr_groupunit._pact_credit
        == 0.25
    )
    assert (
        rico_groupunit._pact_debt
        + carm_groupunit._pact_debt
        + patr_groupunit._pact_debt
        == 0.25
    )

    # groupunit_pact_credit_sum = 0.0
    # groupunit_pact_debt_sum = 0.0
    # for groupunit in x_pact._groups.values():
    #     assert groupunit._pact_credit != None
    #     assert groupunit._pact_credit not in [0.25, 0.5]
    #     assert groupunit._pact_debt != None
    #     assert groupunit._pact_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {groupunit._pact_creditor=} {group._pact_creditor=}"
    #     # )
    #     print(f"{groupunit.brand=} {groupunit._pact_credit=} {groupunit._pact_debt=} ")
    #     # print(f"{groupunit_pact_credit_sum=}")
    #     # print(f"{groupunit_pact_debt_sum=}")
    #     groupunit_pact_credit_sum += groupunit._pact_credit
    #     groupunit_pact_debt_sum += groupunit._pact_debt
    # assert groupunit_pact_credit_sum == 0.25
    # assert groupunit_pact_debt_sum == 0.25

    rico_partyunit = x_pact._partys.get(rico_text)
    carm_partyunit = x_pact._partys.get(carm_text)
    patr_partyunit = x_pact._partys.get(patr_text)

    assert rico_partyunit._pact_credit == 0.375
    assert rico_partyunit._pact_debt == 0.45
    assert carm_partyunit._pact_credit == 0.3125
    assert carm_partyunit._pact_debt == 0.275
    assert patr_partyunit._pact_credit == 0.3125
    assert patr_partyunit._pact_debt == 0.275

    assert (
        rico_partyunit._pact_credit
        + carm_partyunit._pact_credit
        + patr_partyunit._pact_credit
        == 1.0
    )
    assert (
        rico_partyunit._pact_debt
        + carm_partyunit._pact_debt
        + patr_partyunit._pact_debt
        == 1.0
    )

    # partyunit_pact_credit_sum = 0.0
    # partyunit_pact_debt_sum = 0.0
    # for partyunit in x_pact._partys.values():
    #     assert partyunit._pact_credit != None
    #     assert partyunit._pact_credit not in [0.25, 0.5]
    #     assert partyunit._pact_debt != None
    #     assert partyunit._pact_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._pact_creditor=} {group._pact_creditor=}"
    #     # )
    #     print(f"{partyunit.title=} {partyunit._pact_credit=} {partyunit._pact_debt=} ")
    #     # print(f"{partyunit_pact_credit_sum=}")
    #     # print(f"{partyunit_pact_debt_sum=}")
    #     partyunit_pact_credit_sum += partyunit._pact_credit
    #     partyunit_pact_debt_sum += partyunit._pact_debt
    # assert partyunit_pact_credit_sum == 1.0
    # assert partyunit_pact_debt_sum > 0.9999999
    # assert partyunit_pact_debt_sum < 1.00000001


def test_pact_get_idea_list_WithAllPartysWeighted():
    # GIVEN
    x_pact = PactUnit(_healer="prom")
    x_pact.add_idea(idea_kid=IdeaKid(_label="swim"), pad="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_pact.set_partyunit(
        partyunit=partyunit_shop(title=PartyTitle(rico_text), creditor_weight=8)
    )
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))
    rico_partyunit = x_pact._partys.get(rico_text)
    carm_partyunit = x_pact._partys.get(carm_text)
    patr_partyunit = x_pact._partys.get(patr_text)
    assert rico_partyunit._pact_credit is None
    assert rico_partyunit._pact_debt is None
    assert carm_partyunit._pact_credit is None
    assert carm_partyunit._pact_debt is None
    assert patr_partyunit._pact_credit is None
    assert patr_partyunit._pact_debt is None

    # WHEN
    x_pact.set_pact_metrics()

    # THEN
    assert (
        rico_partyunit._pact_credit
        + carm_partyunit._pact_credit
        + patr_partyunit._pact_credit
        == 1.0
    )
    assert (
        rico_partyunit._pact_debt
        + carm_partyunit._pact_debt
        + patr_partyunit._pact_debt
        == 1.0
    )
    # partyunit_pact_credit_sum = 0.0
    # partyunit_pact_debt_sum = 0.0
    # for partyunit in x_pact._partys.values():
    #     assert partyunit._pact_credit != None
    #     assert partyunit._pact_credit not in [0.25, 0.5]
    #     assert partyunit._pact_debt != None
    #     assert partyunit._pact_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._pact_creditor=} {group._pact_creditor=}"
    #     # )
    #     print(f"{partyunit.title=} {partyunit._pact_credit=} {partyunit._pact_debt=} ")
    #     # print(f"{partyunit_pact_credit_sum=}")
    #     # print(f"{partyunit_pact_debt_sum=}")
    #     partyunit_pact_credit_sum += partyunit._pact_credit
    #     partyunit_pact_debt_sum += partyunit._pact_debt
    # assert partyunit_pact_credit_sum == 1.0
    # assert partyunit_pact_debt_sum > 0.9999999
    # assert partyunit_pact_debt_sum < 1.00000001


def clear_all_partyunits_groupunits_pact_agenda_credit_debt(x_pact: PactUnit):
    # DELETE pact_agenda_debt and pact_agenda_credit
    for groupunit_x in x_pact._groups.values():
        groupunit_x.reset_pact_credit_debt()
        # for partylink_x in groupunit_x._partys.values():
        #     print(f"{groupunit_x.brand=} {partylink_x.creditor_weight=}  {partylink_x._pact_credit:.6f} {partylink_x.debtor_weight=} {partylink_x._pact_debt:.6f} {partylink_x.title=} ")

    # DELETE pact_agenda_debt and pact_agenda_credit
    for partyunit_x in x_pact._partys.values():
        partyunit_x.reset_pact_credit_debt()


# sourcery skip: no-loop-in-tests
# sourcery skip: no-conditionals-in-tests
def test_pact_agenda_credit_debt_IsCorrectlySet():
    # GIVEN
    x_pact = examples_pact_v001_with_large_agenda()
    clear_all_partyunits_groupunits_pact_agenda_credit_debt(x_pact=x_pact)

    # TEST pact_agenda_debt and pact_agenda_credit are empty
    sum_groupunit_pact_agenda_credit = 0
    sum_groupunit_pact_agenda_debt = 0
    sum_partylink_pact_agenda_credit = 0
    sum_partylink_pact_agenda_debt = 0
    for groupunit_x in x_pact._groups.values():
        # print(f"{partyunit.title=}")
        sum_groupunit_pact_agenda_credit += groupunit_x._pact_agenda_credit
        sum_groupunit_pact_agenda_debt += groupunit_x._pact_agenda_debt
        for partylink_x in groupunit_x._partys.values():
            sum_partylink_pact_agenda_credit += partylink_x._pact_agenda_credit
            sum_partylink_pact_agenda_debt += partylink_x._pact_agenda_debt

    assert sum_groupunit_pact_agenda_credit == 0
    assert sum_groupunit_pact_agenda_debt == 0
    assert sum_partylink_pact_agenda_credit == 0
    assert sum_partylink_pact_agenda_debt == 0

    # TEST pact_agenda_debt and pact_agenda_credit are empty
    sum_partyunit_pact_agenda_credit = 0
    sum_partyunit_pact_agenda_debt = 0
    sum_partyunit_pact_agenda_ratio_credit = 0
    sum_partyunit_pact_agenda_ratio_debt = 0
    for partyunit in x_pact._partys.values():
        # print(f"{partyunit.title=}")
        sum_partyunit_pact_agenda_credit += partyunit._pact_agenda_credit
        sum_partyunit_pact_agenda_debt += partyunit._pact_agenda_debt
        sum_partyunit_pact_agenda_ratio_credit += partyunit._pact_agenda_ratio_credit
        sum_partyunit_pact_agenda_ratio_debt += partyunit._pact_agenda_ratio_debt

    assert sum_partyunit_pact_agenda_credit == 0
    assert sum_partyunit_pact_agenda_debt == 0
    assert sum_partyunit_pact_agenda_ratio_credit == 0
    assert sum_partyunit_pact_agenda_ratio_debt == 0

    # WHEN
    agenda_list = x_pact.get_agenda_items()

    # THEN
    assert len(agenda_list) == 68
    sum_pact_agenda_importance = 0
    agenda_no_balancelines_count = 0
    agenda_yes_balancelines_count = 0
    agenda_no_balancelines_pact_i_sum = 0
    agenda_yes_balancelines_pact_i_sum = 0
    for agenda_item in agenda_list:
        sum_pact_agenda_importance += agenda_item._pact_importance
        if agenda_item._balancelines == {}:
            agenda_no_balancelines_count += 1
            agenda_no_balancelines_pact_i_sum += agenda_item._pact_importance
        else:
            agenda_yes_balancelines_count += 1
            agenda_yes_balancelines_pact_i_sum += agenda_item._pact_importance
        # print(f"idea importance: {agenda_item._pact_importance:.7f} {sum_pact_agenda_importance:.5f} {agenda_item._label=} ")
        # print(f"{agenda_item.get_road()}")
    print(f"{sum_pact_agenda_importance=}")
    assert agenda_no_balancelines_count == 20
    assert agenda_yes_balancelines_count == 48
    assert agenda_no_balancelines_pact_i_sum == 0.00447826215370075
    assert agenda_yes_balancelines_pact_i_sum == 0.0027152834170378025
    x2 = agenda_no_balancelines_pact_i_sum + agenda_yes_balancelines_pact_i_sum
    e10 = 0.0000000001
    assert abs(x2 - sum_pact_agenda_importance) < e10

    assert sum_pact_agenda_importance == 0.007193545570738553

    sum_groupunit_pact_agenda_credit = 0
    sum_groupunit_pact_agenda_debt = 0
    sum_partylink_pact_agenda_credit = 0
    sum_partylink_pact_agenda_debt = 0
    partylink_count = 0
    for groupunit_x in x_pact._groups.values():
        # print(f"{partyunit.title=}")
        sum_groupunit_pact_agenda_credit += groupunit_x._pact_agenda_credit
        sum_groupunit_pact_agenda_debt += groupunit_x._pact_agenda_debt
        for partylink_x in groupunit_x._partys.values():
            sum_partylink_pact_agenda_credit += partylink_x._pact_agenda_credit
            sum_partylink_pact_agenda_debt += partylink_x._pact_agenda_debt
            partylink_count += 1

    assert partylink_count == 81
    x_sum = 0.0027152834170378025
    assert sum_groupunit_pact_agenda_credit == x_sum
    assert sum_groupunit_pact_agenda_debt == x_sum
    assert sum_partylink_pact_agenda_credit == x_sum
    assert sum_partylink_pact_agenda_debt == x_sum
    assert (
        abs(agenda_yes_balancelines_pact_i_sum - sum_groupunit_pact_agenda_credit) < e10
    )

    sum_partyunit_pact_agenda_credit = 0
    sum_partyunit_pact_agenda_debt = 0
    sum_partyunit_pact_agenda_ratio_credit = 0
    sum_partyunit_pact_agenda_ratio_debt = 0
    for partyunit in x_pact._partys.values():
        assert partyunit._pact_credit != None
        assert partyunit._pact_credit not in [0.25, 0.5]
        assert partyunit._pact_debt != None
        assert partyunit._pact_debt not in [
            0.8,
            0.1,
        ]  # print(f"{partyunit.title=}")
        sum_partyunit_pact_agenda_credit += partyunit._pact_agenda_credit
        sum_partyunit_pact_agenda_debt += partyunit._pact_agenda_debt
        sum_partyunit_pact_agenda_ratio_credit += partyunit._pact_agenda_ratio_credit
        sum_partyunit_pact_agenda_ratio_debt += partyunit._pact_agenda_ratio_debt

    assert abs(sum_partyunit_pact_agenda_credit - sum_pact_agenda_importance) < e10
    assert abs(sum_partyunit_pact_agenda_debt - sum_pact_agenda_importance) < e10
    assert abs(sum_partyunit_pact_agenda_ratio_credit - 1) < e10
    assert abs(sum_partyunit_pact_agenda_ratio_debt - 1) < e10

    # partyunit_pact_credit_sum = 0.0
    # partyunit_pact_debt_sum = 0.0

    # assert partyunit_pact_credit_sum == 1.0
    # assert partyunit_pact_debt_sum > 0.9999999
    # assert partyunit_pact_debt_sum < 1.00000001


def test_pact_agenda_ratio_credit_debt_IsCorrectlySetWhenAgendaIsEmpty():
    # GIVEN
    healer_text = "Noa"
    x_pact = PactUnit(_healer=healer_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_party = partyunit_shop(title=rico_text, creditor_weight=0.5, debtor_weight=2)
    carm_party = partyunit_shop(title=carm_text, creditor_weight=1.5, debtor_weight=3)
    patr_party = partyunit_shop(title=patr_text, creditor_weight=8, debtor_weight=5)
    x_pact.set_partyunit(partyunit=rico_party)
    x_pact.set_partyunit(partyunit=carm_party)
    x_pact.set_partyunit(partyunit=patr_party)
    x_pact_rico_party = x_pact._partys.get(rico_text)
    x_pact_carm_party = x_pact._partys.get(carm_text)
    x_pact_patr_party = x_pact._partys.get(patr_text)

    assert x_pact_rico_party._pact_agenda_credit in [0, None]
    assert x_pact_rico_party._pact_agenda_debt in [0, None]
    assert x_pact_carm_party._pact_agenda_credit in [0, None]
    assert x_pact_carm_party._pact_agenda_debt in [0, None]
    assert x_pact_patr_party._pact_agenda_credit in [0, None]
    assert x_pact_patr_party._pact_agenda_debt in [0, None]
    assert x_pact_rico_party._pact_agenda_ratio_credit != 0.05
    assert x_pact_rico_party._pact_agenda_ratio_debt != 0.2
    assert x_pact_carm_party._pact_agenda_ratio_credit != 0.15
    assert x_pact_carm_party._pact_agenda_ratio_debt != 0.3
    assert x_pact_patr_party._pact_agenda_ratio_credit != 0.8
    assert x_pact_patr_party._pact_agenda_ratio_debt != 0.5

    # WHEN
    x_pact.set_pact_metrics()

    # THEN
    assert x_pact_rico_party._pact_agenda_credit == 0
    assert x_pact_rico_party._pact_agenda_debt == 0
    assert x_pact_carm_party._pact_agenda_credit == 0
    assert x_pact_carm_party._pact_agenda_debt == 0
    assert x_pact_patr_party._pact_agenda_credit == 0
    assert x_pact_patr_party._pact_agenda_debt == 0
    assert x_pact_rico_party._pact_agenda_ratio_credit == 0.05
    assert x_pact_rico_party._pact_agenda_ratio_debt == 0.2
    assert x_pact_carm_party._pact_agenda_ratio_credit == 0.15
    assert x_pact_carm_party._pact_agenda_ratio_debt == 0.3
    assert x_pact_patr_party._pact_agenda_ratio_credit == 0.8
    assert x_pact_patr_party._pact_agenda_ratio_debt == 0.5


def test_pact_get_party_groups_returnsCorrectData():
    x_pact = PactUnit(_healer="prom")
    x_pact.add_idea(idea_kid=IdeaKid(_label="swim"), pad="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))

    carmen_group_list = x_pact.get_party_groups(party_title=carm_text)
    assert carmen_group_list == [carm_text]

    swimmers = "swimmers"
    carmen_party_dict = {PartyTitle(carm_text): partylink_shop(title=carm_text)}
    swim_group = groupunit_shop(brand=swimmers, _partys=carmen_party_dict)
    x_pact._groups[swim_group.brand] = swim_group
    carmen_group_list = x_pact.get_party_groups(party_title=carm_text)
    assert carmen_group_list == [carm_text, swimmers]


def test_pact_PartyUnit_CorrectlyCreatesNewTitle():
    # GIVEN
    x_pact = PactUnit(_healer="prom")
    rico_text = "rico"
    x_pact.add_partyunit(title=rico_text, uid=61, creditor_weight=13)
    x_pact.add_partyunit(title="carmen", uid=5)
    x_pact.add_partyunit(title="patrick", creditor_weight=17)
    assert len(x_pact._partys) == 3
    assert x_pact._partys.get(rico_text) != None
    assert x_pact._partys.get(rico_text).creditor_weight == 13
    assert len(x_pact._groups) == 3
    assert x_pact._groups.get(rico_text) != None
    assert x_pact._groups.get(rico_text)._single_party == True

    # WHEN
    beto_text = "beta"
    x_pact.edit_partyunit_title(
        old_title=rico_text,
        new_title=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert x_pact._partys.get(beto_text) != None
    assert x_pact._partys.get(beto_text).creditor_weight == 13
    assert x_pact._partys.get(rico_text) is None
    assert len(x_pact._partys) == 3
    assert len(x_pact._groups) == 3
    assert x_pact._groups.get(rico_text) is None
    assert x_pact._groups.get(beto_text) != None
    assert x_pact._groups.get(beto_text)._single_party == True


def test_pact_PartyUnit_raiseErrorNewTitlePreviouslyExists():
    # GIVEN
    x_pact = PactUnit(_healer="prom")
    rico_text = "rico"
    x_pact.add_partyunit(title=rico_text, uid=61, creditor_weight=13)
    carmen_text = "carmen"
    x_pact.add_partyunit(title=carmen_text, uid=5)
    x_pact.add_partyunit(title="patrick", creditor_weight=17)
    assert len(x_pact._partys) == 3
    assert x_pact._partys.get(rico_text) != None
    assert x_pact._partys.get(rico_text).creditor_weight == 13
    assert len(x_pact._groups) == 3
    assert x_pact._groups.get(rico_text) != None
    assert x_pact._groups.get(rico_text)._single_party == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_pact.edit_partyunit_title(
            old_title=rico_text,
            new_title=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' change to '{carmen_text}' failed since '{carmen_text}' exists."
    )


def test_pact_PartyUnit_CorrectlyChangesGroupUnitPartyLinks():
    # GIVEN
    prom_text = "prom"
    x_pact = PactUnit(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_pact.add_partyunit(title=rico_text, uid=61, creditor_weight=13)
    x_pact.add_partyunit(title=carm_text, uid=5)
    x_pact.add_partyunit(title=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyTitle(carm_text): partylink_shop(title=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(title=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(title=rico_text, creditor_weight=7, debtor_weight=30)
    )
    x_pact.set_groupunit(groupunit=swim_group)

    swim_group = x_pact._groups.get(swim_text)
    assert len(swim_group._partys) == 2
    assert swim_group._partys.get(rico_text) != None
    assert swim_group._partys.get(rico_text).creditor_weight == 7
    assert swim_group._partys.get(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    x_pact.edit_partyunit_title(
        old_title=rico_text,
        new_title=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._partys.get(beto_text) != None
    assert swim_group._partys.get(beto_text).creditor_weight == 7
    assert swim_group._partys.get(beto_text).debtor_weight == 30
    assert swim_group._partys.get(rico_text) is None
    assert len(swim_group._partys) == 2


def test_pact_PartyUnit_CorrectlyMergesTitles():
    # GIVEN
    prom_text = "prom"
    x_pact = PactUnit(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_pact.add_partyunit(title=rico_text, uid=61, creditor_weight=13)
    x_pact.add_partyunit(title=carm_text, uid=5, creditor_weight=3)
    x_pact.add_partyunit(title=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyTitle(carm_text): partylink_shop(title=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(title=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(title=rico_text, creditor_weight=7, debtor_weight=30)
    )
    x_pact.set_groupunit(groupunit=swim_group)

    assert len(x_pact._partys) == 3
    assert x_pact._partys.get(rico_text) != None
    assert x_pact._partys.get(rico_text).creditor_weight == 13
    assert x_pact._partys.get(carm_text) != None
    assert x_pact._partys.get(carm_text).creditor_weight == 3

    # WHEN / THEN
    x_pact.edit_partyunit_title(
        old_title=rico_text,
        new_title=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert x_pact._partys.get(carm_text) != None
    assert x_pact._partys.get(carm_text).creditor_weight == 16
    assert x_pact._partys.get(rico_text) is None
    assert len(x_pact._partys) == 2


def test_pact_PartyUnit_CorrectlyMergesGroupUnitPartyLinks():
    # GIVEN
    # GIVEN
    prom_text = "prom"
    x_pact = PactUnit(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_pact.add_partyunit(title=rico_text, uid=61, creditor_weight=13)
    x_pact.add_partyunit(title=carm_text, uid=5)
    x_pact.add_partyunit(title=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyTitle(carm_text): partylink_shop(title=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(title=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(title=rico_text, creditor_weight=7, debtor_weight=30)
    )
    x_pact.set_groupunit(groupunit=swim_group)

    swim_group = x_pact._groups.get(swim_text)
    assert len(swim_group._partys) == 2
    assert swim_group._partys.get(rico_text) != None
    assert swim_group._partys.get(rico_text).creditor_weight == 7
    assert swim_group._partys.get(rico_text).debtor_weight == 30
    assert swim_group._partys.get(carm_text) != None
    assert swim_group._partys.get(carm_text).creditor_weight == 5
    assert swim_group._partys.get(carm_text).debtor_weight == 18

    # WHEN
    x_pact.edit_partyunit_title(
        old_title=rico_text,
        new_title=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._partys.get(carm_text) != None
    assert swim_group._partys.get(carm_text).creditor_weight == 12
    assert swim_group._partys.get(carm_text).debtor_weight == 48
    assert swim_group._partys.get(rico_text) is None
    assert len(swim_group._partys) == 1


def test_pact_PartyUnit_raiseErrorNewTitleGroupUnitPreviouslyExists():
    # GIVEN
    x_pact = PactUnit(_healer="prom")
    rico_text = "rico"
    x_pact.add_partyunit(title=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    x_pact.add_partyunit(title=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(brand=carmen_text)
    carmen_group.set_partylink(partylink=partylink_shop(title=rico_text))
    carmen_group.set_partylink(partylink=partylink_shop(title=anna_text))
    x_pact.set_groupunit(groupunit=carmen_group)
    assert len(x_pact._groups) == 3
    assert x_pact._partys.get(carmen_text) is None
    assert x_pact._groups.get(carmen_text)._single_party == False
    assert len(x_pact._groups.get(carmen_text)._partys) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_pact.edit_partyunit_title(
            old_title=rico_text,
            new_title=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' change to '{carmen_text}' failed since non-single group '{carmen_text}' exists."
    )


def test_pact_PartyUnit_CorrectlyOverwriteNewTitleGroupUnit():
    # GIVEN
    x_pact = PactUnit(_healer="prom")
    rico_text = "rico"
    x_pact.add_partyunit(title=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    x_pact.add_partyunit(title=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(brand=carmen_text)
    carmen_group.set_partylink(
        partylink=partylink_shop(title=rico_text, creditor_weight=3)
    )
    carmen_group.set_partylink(
        partylink=partylink_shop(title=anna_text, creditor_weight=5)
    )
    x_pact.set_groupunit(groupunit=carmen_group)
    assert len(x_pact._groups) == 3
    assert x_pact._partys.get(rico_text) != None
    assert x_pact._partys.get(carmen_text) is None
    assert x_pact._groups.get(carmen_text)._single_party == False
    assert len(x_pact._groups.get(carmen_text)._partys) == 2
    assert x_pact._groups.get(carmen_text)._partys.get(anna_text).creditor_weight == 5
    assert x_pact._groups.get(carmen_text)._partys.get(rico_text).creditor_weight == 3

    # WHEN
    x_pact.edit_partyunit_title(
        old_title=rico_text,
        new_title=carmen_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=True,
    )

    assert len(x_pact._groups) == 2
    assert x_pact._partys.get(rico_text) is None
    assert x_pact._partys.get(carmen_text) != None
    assert x_pact._groups.get(carmen_text)._single_party == True
    assert len(x_pact._groups.get(carmen_text)._partys) == 1
    assert x_pact._groups.get(carmen_text)._partys.get(rico_text) is None
    assert x_pact._groups.get(carmen_text)._partys.get(carmen_text).creditor_weight == 1


def test_pact_set_all_partyunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    healer_text = "Noa"
    x_pact = PactUnit(_healer=healer_text)
    x_pact.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=swim_text))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=pad_text))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=fly_text))
    assert x_pact._partys[swim_text].uid is None
    assert x_pact._partys[pad_text].uid is None
    assert x_pact._partys[fly_text].uid is None

    # WHEN
    x_pact.set_all_partyunits_uids_unique()

    # THEN
    assert x_pact._partys[swim_text].uid != None
    assert x_pact._partys[pad_text].uid != None
    assert x_pact._partys[fly_text].uid != None


def test_pact_set_all_partyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    healer_text = "Noa"
    x_pact = PactUnit(_healer=healer_text)
    x_pact.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=swim_text, uid=3))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=pad_text, uid=3))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=fly_text))
    assert x_pact._partys[swim_text].uid == 3
    assert x_pact._partys[pad_text].uid == 3
    assert x_pact._partys[fly_text].uid is None

    # WHEN
    x_pact.set_all_partyunits_uids_unique()

    # THEN
    print(f"{x_pact._partys[swim_text].uid=}")
    print(f"{x_pact._partys[pad_text].uid=}")
    assert x_pact._partys[swim_text].uid != x_pact._partys[pad_text].uid
    assert x_pact._partys[pad_text].uid != 3
    assert x_pact._partys[pad_text].uid != 3
    assert x_pact._partys[fly_text].uid != None


def test_pact_set_all_partyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    healer_text = "Noa"
    x_pact = PactUnit(_healer=healer_text)
    x_pact.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=swim_text, uid=3))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=pad_text, uid=3))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=fly_text))
    assert x_pact._partys[swim_text].uid == 3
    assert x_pact._partys[pad_text].uid == 3
    assert x_pact._partys[fly_text].uid is None

    # WHEN
    x_pact.set_all_partyunits_uids_unique()

    # THEN
    print(f"{x_pact._partys[swim_text].uid=}")
    print(f"{x_pact._partys[pad_text].uid=}")
    assert x_pact._partys[swim_text].uid != x_pact._partys[pad_text].uid
    assert x_pact._partys[pad_text].uid != 3
    assert x_pact._partys[pad_text].uid != 3
    assert x_pact._partys[fly_text].uid != None


def test_pact_all_partyunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    healer_text = "Noa"
    x_pact = PactUnit(_healer=healer_text)
    x_pact.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=swim_text, uid=3))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=pad_text, uid=3))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=fly_text))
    assert x_pact._partys[swim_text].uid == 3
    assert x_pact._partys[pad_text].uid == 3
    assert x_pact._partys[fly_text].uid is None

    # WHEN1 / THEN
    assert x_pact.all_partyunits_uids_are_unique() == False

    # WHEN2
    x_pact.set_partyunit(partyunit=partyunit_shop(title=swim_text, uid=4))

    # THEN
    assert x_pact.all_partyunits_uids_are_unique() == False

    # WHEN3
    x_pact.set_partyunit(partyunit=partyunit_shop(title=fly_text, uid=5))

    # THEN
    assert x_pact.all_partyunits_uids_are_unique()


def test_pact_get_partyunits_title_list_CorrectlyReturnsListOfPartyUnits():
    # GIVEN
    healer_text = "Noa"
    x_pact = PactUnit(_healer=healer_text)
    x_pact.set_partys_empty_if_null()
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=sam_text))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=will_text))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=fry_text))
    fun_text = "fun people"
    fun_group = groupunit_shop(brand=fun_text)
    fun_group.set_partylink(partylink=partylink_shop(title=will_text))
    x_pact.set_groupunit(groupunit=fun_group)
    assert len(x_pact._groups) == 4
    assert len(x_pact._partys) == 3

    # WHEN
    partyunit_list_x = x_pact.get_partyunits_title_list()

    # THEN
    assert len(partyunit_list_x) == 4
    assert partyunit_list_x[0] == ""
    assert partyunit_list_x[1] == fry_text
    assert partyunit_list_x[2] == sam_text
    assert partyunit_list_x[3] == will_text


def test_pact_set_banking_data_partyunits_CorrectlySetsPartyUnitBankingAttr():
    # GIVEN
    bob_text = "bob"
    x_pact = PactUnit(_healer=bob_text)
    x_pact.set_partys_empty_if_null()
    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=sam_text))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=wil_text))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=fry_text))
    assert x_pact._partys.get(sam_text)._bank_tax_paid is None
    assert x_pact._partys.get(sam_text)._bank_tax_diff is None
    assert x_pact._partys.get(wil_text)._bank_tax_paid is None
    assert x_pact._partys.get(wil_text)._bank_tax_diff is None
    assert x_pact._partys.get(fry_text)._bank_tax_paid is None
    assert x_pact._partys.get(fry_text)._bank_tax_diff is None
    elu_partyunit = partyunit_shop(title=elu_text)
    elu_partyunit._bank_tax_paid = 0.003
    elu_partyunit._bank_tax_diff = 0.007
    x_pact.set_partyunit(partyunit=elu_partyunit)
    assert x_pact._partys.get(elu_text)._bank_tax_paid == 0.003
    assert x_pact._partys.get(elu_text)._bank_tax_diff == 0.007

    river_tparty_sam = RiverTpartyUnit(bob_text, sam_text, 0.209, 0, 0.034)
    river_tparty_wil = RiverTpartyUnit(bob_text, wil_text, 0.501, 0, 0.024)
    river_tparty_fry = RiverTpartyUnit(bob_text, fry_text, 0.111, 0, 0.006)
    river_tpartys = {
        river_tparty_sam.tax_title: river_tparty_sam,
        river_tparty_wil.tax_title: river_tparty_wil,
        river_tparty_fry.tax_title: river_tparty_fry,
    }
    # WHEN
    x_pact.set_banking_attr_partyunits(river_tpartys=river_tpartys)

    # THEN
    assert x_pact._partys.get(sam_text)._bank_tax_paid == 0.209
    assert x_pact._partys.get(sam_text)._bank_tax_diff == 0.034
    assert x_pact._partys.get(wil_text)._bank_tax_paid == 0.501
    assert x_pact._partys.get(wil_text)._bank_tax_diff == 0.024
    assert x_pact._partys.get(fry_text)._bank_tax_paid == 0.111
    assert x_pact._partys.get(fry_text)._bank_tax_diff == 0.006
    assert x_pact._partys.get(elu_text)._bank_tax_paid is None
    assert x_pact._partys.get(elu_text)._bank_tax_diff is None


def test_get_intersection_of_partys_CorrectlyReturnsUnionOfKeysOfTwoDictionarys_scenario1():
    # GIVEN
    bob_text = "bob"
    x_pact = PactUnit(_healer=bob_text)
    x_pact.set_partys_empty_if_null()

    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    x_pact.set_partyunit(partyunit=partyunit_shop(title=bob_text))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=sam_text))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=wil_text))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=fry_text))

    y_pact = PactUnit()
    y_pact.set_partys_empty_if_null()

    y_pact.set_partyunit(partyunit=partyunit_shop(title=bob_text))
    y_pact.set_partyunit(partyunit=partyunit_shop(title=wil_text))
    y_pact.set_partyunit(partyunit=partyunit_shop(title=fry_text))
    y_pact.set_partyunit(partyunit=partyunit_shop(title=elu_text))

    # WHEN
    print(f"{len(x_pact._partys)=} {len(y_pact._partys)=}")
    intersection_x = get_intersection_of_partys(x_pact._partys, y_pact._partys)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}
