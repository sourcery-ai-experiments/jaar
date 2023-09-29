from src.contract.party import PartyName, partylink_shop, partyunit_shop
from src.contract.group import GroupBrand, groupunit_shop, grouplink_shop
from src.contract.examples.example_contracts import (
    contract_v001 as examples_contract_v001,
    contract_v001_with_large_agenda as examples_contract_v001_with_large_agenda,
)
from src.contract.contract import ContractUnit, get_intersection_of_partys
from src.contract.idea import IdeaKid
from pytest import raises as pytest_raises
from src.economy.bank_sqlstr import RiverTpartyUnit


def test_contract_partys_exists():
    # GIVEN / WHEN
    cx = ContractUnit()

    # THEN
    assert cx._partys is None

    # GIVEN
    yahri_party = partyunit_shop(name=PartyName("yahri"))
    partys_x = {yahri_party.name: yahri_party}
    cx2 = ContractUnit()

    # WHEN
    cx2.set_partyunit(partyunit=yahri_party)

    # THEN
    assert cx2._partys == partys_x


def test_example_has_partys():
    # GIVEN / WHEN
    cx = examples_contract_v001()

    # THEN
    assert cx._partys != None
    assert len(cx._partys) == 22


def test_contract_set_party_correctly_sets_partys_1():
    # GIVEN
    cx = ContractUnit(_owner="prom")
    cx.set_contract_metrics()
    assert len(cx._partys) == 0
    assert len(cx._groups) == 0

    # WHEN
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName("rico")))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName("carmen")))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName("patrick")))

    # THEN
    assert len(cx._partys) == 3
    assert len(cx._groups) == 3
    assert cx._groups["rico"]._single_party == True

    # WHEN
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(brand=GroupBrand("rico"), creditor_weight=10)
    )
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(brand=GroupBrand("carmen"), creditor_weight=10)
    )
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(brand=GroupBrand("patrick"), creditor_weight=10)
    )
    assert len(cx._idearoot._grouplinks) == 3


def test_contract_set_party_correctly_sets_partys_2():
    # GIVEN
    cx = ContractUnit(_owner="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    assign_text = "assignment"

    # WHEN
    cx.add_partyunit(name=rico_text, uid=61, creditor_weight=13, debtor_weight=8)
    cx.add_partyunit(name=carm_text, uid=5, debtor_weight=5)
    cx.add_partyunit(name=patr_text, creditor_weight=17, depotlink_type=assign_text)

    # THEN
    assert len(cx._partys) == 3
    assert len(cx._groups) == 3
    assert cx._groups.get(rico_text)._single_party == True
    assert cx._partys.get(patr_text).creditor_weight == 17
    assert cx._partys.get(carm_text).debtor_weight == 5
    assert cx._partys.get(patr_text).depotlink_type == assign_text


def test_contract_get_party_CorrectlyGetsParty():
    # GIVEN
    cx = ContractUnit(_owner="prom")
    rico_text = "rico"
    carm_text = "carmen"
    cx.add_partyunit(name=rico_text)
    cx.add_partyunit(name=carm_text)

    # WHEN
    rico_party = cx.get_party(rico_text)
    carm_party = cx.get_party(carm_text)

    # THEN
    assert rico_party == cx._partys.get(rico_text)
    assert carm_party == cx._partys.get(carm_text)


def test_contract_get_partys_depotlink_count_GetsCorrectCount():
    # GIVEN
    sue_text = "sue"
    sue_cx = ContractUnit(_owner=sue_text)
    assign_text = "assignment"

    # WHEN
    rico_text = "rico"
    carm_text = "carmen"
    sue_cx.add_partyunit(name=rico_text)
    sue_cx.add_partyunit(name=carm_text)
    # THEN
    assert len(sue_cx._partys) == 2
    assert sue_cx.get_partys_depotlink_count() == 0

    # WHEN
    patr_text = "patrick"
    sue_cx.add_partyunit(name=patr_text, depotlink_type=assign_text)
    # THEN
    assert len(sue_cx._partys) == 3
    assert sue_cx.get_partys_depotlink_count() == 1

    # WHEN
    rico_party = sue_cx.get_party(rico_text)
    rico_party.set_depotlink_type(assign_text)
    # THEN
    assert len(sue_cx._partys) == 3
    assert sue_cx.get_partys_depotlink_count() == 2


def test_contract_get_idea_list_CorrectlySetsPartyLinkContractCreditAndDebt():
    # GIVEN
    prom_text = "prom"
    cx = ContractUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))
    bl_rico = grouplink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = grouplink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = grouplink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    cx._idearoot.set_grouplink(grouplink=bl_rico)
    cx._idearoot.set_grouplink(grouplink=bl_carm)
    cx._idearoot.set_grouplink(grouplink=bl_patr)

    rico_groupunit = cx._groups.get(rico_text)
    carm_groupunit = cx._groups.get(carm_text)
    patr_groupunit = cx._groups.get(patr_text)
    rico_partylink = rico_groupunit._partys.get(rico_text)
    carm_partylink = carm_groupunit._partys.get(carm_text)
    patr_partylink = patr_groupunit._partys.get(patr_text)
    rico_partylink._contract_credit is None
    rico_partylink._contract_debt is None
    carm_partylink._contract_credit is None
    carm_partylink._contract_debt is None
    patr_partylink._contract_credit is None
    patr_partylink._contract_debt is None

    # for group in cx._groups.values():
    #     for partylink in group._partys.values():
    #         assert partylink._contract_credit is None
    #         assert partylink._contract_debt is None

    cx.set_contract_metrics()

    # for grouplink in cx._groupheirs.values():
    #     print(
    #         f"{cx._contract_importance=} {grouplink.brand=} {grouplink._contract_credit=} {grouplink._contract_debt=}"
    #     )

    assert rico_partylink._contract_credit == 0.5
    assert rico_partylink._contract_debt == 0.8
    assert carm_partylink._contract_credit == 0.25
    assert carm_partylink._contract_debt == 0.1
    assert patr_partylink._contract_credit == 0.25
    assert patr_partylink._contract_debt == 0.1

    # partylink_contract_credit_sum = 0.0
    # partylink_contract_debt_sum = 0.0
    # for group in cx._groups.values():
    #     # print(f"{group.brand=} {group._partys=}")

    #     for partylink in group._partys.values():
    #         assert partylink._contract_credit != None
    #         assert partylink._contract_credit in [0.25, 0.5]
    #         assert partylink._contract_debt != None
    #         assert partylink._contract_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{group.brand=} {partylink._contract_importance=} {group._contract_importance=}"
    #         # )
    #         partylink_contract_credit_sum += partylink._contract_credit
    #         partylink_contract_debt_sum += partylink._contract_debt

    #         # print(f"{partylink_contract_importance_sum=}")
    # assert partylink_contract_credit_sum == 1.0
    # assert partylink_contract_debt_sum == 1.0

    assert (
        rico_partylink._contract_credit
        + carm_partylink._contract_credit
        + patr_partylink._contract_credit
        == 1.0
    )
    assert (
        rico_partylink._contract_debt
        + carm_partylink._contract_debt
        + patr_partylink._contract_debt
        == 1.0
    )

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(selena_text)))
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(
            brand=GroupBrand(selena_text), creditor_weight=20, debtor_weight=13
        )
    )
    cx.set_contract_metrics()

    # THEN
    selena_groupunit = cx._groups.get(selena_text)
    selena_partylink = selena_groupunit._partys.get(selena_text)

    assert rico_partylink._contract_credit != 0.25
    assert rico_partylink._contract_debt != 0.8
    assert carm_partylink._contract_credit != 0.25
    assert carm_partylink._contract_debt != 0.1
    assert patr_partylink._contract_credit != 0.5
    assert patr_partylink._contract_debt != 0.1
    assert selena_partylink._contract_credit != None
    assert selena_partylink._contract_debt != None

    # partylink_contract_credit_sum = 0.0
    # partylink_contract_debt_sum = 0.0

    # for group in cx._groups.values():
    #     # print(f"{group.brand=} {group._partys=}")

    #     for partylink in group._partys.values():
    #         assert partylink._contract_credit != None
    #         assert partylink._contract_credit not in [0.25, 0.5]
    #         assert partylink._contract_debt != None
    #         assert partylink._contract_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{group.brand=} {partylink._contract_importance=} {group._contract_importance=}"
    #         # )
    #         partylink_contract_credit_sum += partylink._contract_credit
    #         partylink_contract_debt_sum += partylink._contract_debt

    #         # print(f"{partylink_contract_importance_sum=}")
    # assert partylink_contract_credit_sum == 1.0
    # assert partylink_contract_debt_sum > 0.9999999
    # assert partylink_contract_debt_sum < 1.00000001

    assert (
        rico_partylink._contract_credit
        + carm_partylink._contract_credit
        + patr_partylink._contract_credit
        + selena_partylink._contract_credit
        == 1.0
    )
    assert (
        rico_partylink._contract_debt
        + carm_partylink._contract_debt
        + patr_partylink._contract_debt
        + selena_partylink._contract_debt
        > 0.9999999
    )
    assert (
        rico_partylink._contract_debt
        + carm_partylink._contract_debt
        + patr_partylink._contract_debt
        + selena_partylink._contract_debt
        < 1.0
    )


def test_contract_get_idea_list_CorrectlySetsPartyUnitContractImportance():
    # GIVEN
    prom_text = "prom"
    cx = ContractUnit(_owner=prom_text)
    swim_text = "swim"
    cx.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))
    bl_rico = grouplink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = grouplink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = grouplink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_rico)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_carm)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_patr)

    rico_partyunit = cx._partys.get(rico_text)
    carm_partyunit = cx._partys.get(carm_text)
    patr_partyunit = cx._partys.get(patr_text)

    assert rico_partyunit._contract_credit is None
    assert rico_partyunit._contract_debt is None
    assert carm_partyunit._contract_credit is None
    assert carm_partyunit._contract_debt is None
    assert patr_partyunit._contract_credit is None
    assert patr_partyunit._contract_debt is None

    # WHEN
    cx.set_contract_metrics()

    # THEN
    partyunit_contract_credit_sum = 0.0
    partyunit_contract_debt_sum = 0.0

    assert rico_partyunit._contract_credit == 0.5
    assert rico_partyunit._contract_debt == 0.8
    assert carm_partyunit._contract_credit == 0.25
    assert carm_partyunit._contract_debt == 0.1
    assert patr_partyunit._contract_credit == 0.25
    assert patr_partyunit._contract_debt == 0.1

    assert (
        rico_partyunit._contract_credit
        + carm_partyunit._contract_credit
        + patr_partyunit._contract_credit
        == 1.0
    )
    assert (
        rico_partyunit._contract_debt
        + carm_partyunit._contract_debt
        + patr_partyunit._contract_debt
        == 1.0
    )

    # for partyunit in cx._partys.values():
    #     assert partyunit._contract_credit != None
    #     assert partyunit._contract_credit in [0.25, 0.5]
    #     assert partyunit._contract_debt != None
    #     assert partyunit._contract_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._contract_creditor=} {group._contract_creditor=}"
    #     # )
    #     print(f"{partyunit.name=} {partyunit._contract_credit=} {partyunit._contract_debt=} ")
    #     # print(f"{partyunit_contract_credit_sum=}")
    #     # print(f"{partyunit_contract_debt_sum=}")
    #     partyunit_contract_credit_sum += partyunit._contract_credit
    #     partyunit_contract_debt_sum += partyunit._contract_debt

    # assert partyunit_contract_credit_sum == 1.0
    # assert partyunit_contract_debt_sum > 0.9999999
    # assert partyunit_contract_debt_sum < 1.00000001

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(selena_text)))
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(
            brand=selena_text, creditor_weight=20, debtor_weight=10
        )
    )
    cx.set_contract_metrics()

    # THEN
    selena_partyunit = cx._partys.get(selena_text)

    assert rico_partyunit._contract_credit != 0.5
    assert rico_partyunit._contract_debt != 0.8
    assert carm_partyunit._contract_credit != 0.25
    assert carm_partyunit._contract_debt != 0.1
    assert patr_partyunit._contract_credit != 0.25
    assert patr_partyunit._contract_debt != 0.1
    assert selena_partyunit._contract_credit != None
    assert selena_partyunit._contract_debt != None

    assert (
        rico_partyunit._contract_credit
        + carm_partyunit._contract_credit
        + patr_partyunit._contract_credit
        < 1.0
    )
    assert (
        rico_partyunit._contract_credit
        + carm_partyunit._contract_credit
        + patr_partyunit._contract_credit
        + selena_partyunit._contract_credit
        == 1.0
    )
    assert (
        rico_partyunit._contract_debt
        + carm_partyunit._contract_debt
        + patr_partyunit._contract_debt
        < 1.0
    )
    assert (
        rico_partyunit._contract_debt
        + carm_partyunit._contract_debt
        + patr_partyunit._contract_debt
        + selena_partyunit._contract_debt
        == 1.0
    )

    # partyunit_contract_credit_sum = 0.0
    # partyunit_contract_debt_sum = 0.0

    # for partyunit in cx._partys.values():
    #     assert partyunit._contract_credit != None
    #     assert partyunit._contract_credit not in [0.25, 0.5]
    #     assert partyunit._contract_debt != None
    #     assert partyunit._contract_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._contract_creditor=} {group._contract_creditor=}"
    #     # )
    #     print(f"{partyunit.name=} {partyunit._contract_credit=} {partyunit._contract_debt=} ")
    #     # print(f"{partyunit_contract_credit_sum=}")
    #     # print(f"{partyunit_contract_debt_sum=}")
    #     partyunit_contract_credit_sum += partyunit._contract_credit
    #     partyunit_contract_debt_sum += partyunit._contract_debt

    # assert partyunit_contract_credit_sum == 1.0
    # assert partyunit_contract_debt_sum > 0.9999999
    # assert partyunit_contract_debt_sum < 1.00000001


def test_contract_get_idea_list_CorrectlySetsPartGroupedLWPartyUnitContractImportance():
    # GIVEN
    prom_text = "prom"
    cx = ContractUnit(_owner=prom_text)
    swim_text = "swim"
    cx.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))
    bl_rico = grouplink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = grouplink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = grouplink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_rico)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_carm)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_patr)

    # no grouplinks attached to this one
    hunt_text = "hunt"
    cx.add_idea(idea_kid=IdeaKid(_label=hunt_text, _weight=3), walk=prom_text)

    assert cx._idearoot._grouplinks is None

    # WHEN
    cx.set_contract_metrics()

    # THEN
    rico_groupunit = cx._groups.get(rico_text)
    carm_groupunit = cx._groups.get(carm_text)
    patr_groupunit = cx._groups.get(patr_text)
    assert rico_groupunit._contract_credit != 0.5
    assert rico_groupunit._contract_debt != 0.8
    assert carm_groupunit._contract_credit != 0.25
    assert carm_groupunit._contract_debt != 0.1
    assert patr_groupunit._contract_credit != 0.25
    assert patr_groupunit._contract_debt != 0.1
    assert (
        rico_groupunit._contract_credit
        + carm_groupunit._contract_credit
        + patr_groupunit._contract_credit
        == 0.25
    )
    assert (
        rico_groupunit._contract_debt
        + carm_groupunit._contract_debt
        + patr_groupunit._contract_debt
        == 0.25
    )

    # groupunit_contract_credit_sum = 0.0
    # groupunit_contract_debt_sum = 0.0
    # for groupunit in cx._groups.values():
    #     assert groupunit._contract_credit != None
    #     assert groupunit._contract_credit not in [0.25, 0.5]
    #     assert groupunit._contract_debt != None
    #     assert groupunit._contract_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {groupunit._contract_creditor=} {group._contract_creditor=}"
    #     # )
    #     print(f"{groupunit.brand=} {groupunit._contract_credit=} {groupunit._contract_debt=} ")
    #     # print(f"{groupunit_contract_credit_sum=}")
    #     # print(f"{groupunit_contract_debt_sum=}")
    #     groupunit_contract_credit_sum += groupunit._contract_credit
    #     groupunit_contract_debt_sum += groupunit._contract_debt
    # assert groupunit_contract_credit_sum == 0.25
    # assert groupunit_contract_debt_sum == 0.25

    rico_partyunit = cx._partys.get(rico_text)
    carm_partyunit = cx._partys.get(carm_text)
    patr_partyunit = cx._partys.get(patr_text)

    assert rico_partyunit._contract_credit == 0.375
    assert rico_partyunit._contract_debt == 0.45
    assert carm_partyunit._contract_credit == 0.3125
    assert carm_partyunit._contract_debt == 0.275
    assert patr_partyunit._contract_credit == 0.3125
    assert patr_partyunit._contract_debt == 0.275

    assert (
        rico_partyunit._contract_credit
        + carm_partyunit._contract_credit
        + patr_partyunit._contract_credit
        == 1.0
    )
    assert (
        rico_partyunit._contract_debt
        + carm_partyunit._contract_debt
        + patr_partyunit._contract_debt
        == 1.0
    )

    # partyunit_contract_credit_sum = 0.0
    # partyunit_contract_debt_sum = 0.0
    # for partyunit in cx._partys.values():
    #     assert partyunit._contract_credit != None
    #     assert partyunit._contract_credit not in [0.25, 0.5]
    #     assert partyunit._contract_debt != None
    #     assert partyunit._contract_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._contract_creditor=} {group._contract_creditor=}"
    #     # )
    #     print(f"{partyunit.name=} {partyunit._contract_credit=} {partyunit._contract_debt=} ")
    #     # print(f"{partyunit_contract_credit_sum=}")
    #     # print(f"{partyunit_contract_debt_sum=}")
    #     partyunit_contract_credit_sum += partyunit._contract_credit
    #     partyunit_contract_debt_sum += partyunit._contract_debt
    # assert partyunit_contract_credit_sum == 1.0
    # assert partyunit_contract_debt_sum > 0.9999999
    # assert partyunit_contract_debt_sum < 1.00000001


def test_contract_get_idea_list_WithAllPartysWeighted():
    # GIVEN
    cx = ContractUnit(_owner="prom")
    cx.add_idea(idea_kid=IdeaKid(_label="swim"), walk="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_partyunit(
        partyunit=partyunit_shop(name=PartyName(rico_text), creditor_weight=8)
    )
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))
    rico_partyunit = cx._partys.get(rico_text)
    carm_partyunit = cx._partys.get(carm_text)
    patr_partyunit = cx._partys.get(patr_text)
    assert rico_partyunit._contract_credit is None
    assert rico_partyunit._contract_debt is None
    assert carm_partyunit._contract_credit is None
    assert carm_partyunit._contract_debt is None
    assert patr_partyunit._contract_credit is None
    assert patr_partyunit._contract_debt is None

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assert (
        rico_partyunit._contract_credit
        + carm_partyunit._contract_credit
        + patr_partyunit._contract_credit
        == 1.0
    )
    assert (
        rico_partyunit._contract_debt
        + carm_partyunit._contract_debt
        + patr_partyunit._contract_debt
        == 1.0
    )
    # partyunit_contract_credit_sum = 0.0
    # partyunit_contract_debt_sum = 0.0
    # for partyunit in cx._partys.values():
    #     assert partyunit._contract_credit != None
    #     assert partyunit._contract_credit not in [0.25, 0.5]
    #     assert partyunit._contract_debt != None
    #     assert partyunit._contract_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._contract_creditor=} {group._contract_creditor=}"
    #     # )
    #     print(f"{partyunit.name=} {partyunit._contract_credit=} {partyunit._contract_debt=} ")
    #     # print(f"{partyunit_contract_credit_sum=}")
    #     # print(f"{partyunit_contract_debt_sum=}")
    #     partyunit_contract_credit_sum += partyunit._contract_credit
    #     partyunit_contract_debt_sum += partyunit._contract_debt
    # assert partyunit_contract_credit_sum == 1.0
    # assert partyunit_contract_debt_sum > 0.9999999
    # assert partyunit_contract_debt_sum < 1.00000001


def clear_all_partyunits_groupunits_contract_agenda_credit_debt(cx: ContractUnit):
    # DELETE contract_agenda_debt and contract_agenda_credit
    for groupunit_x in cx._groups.values():
        groupunit_x.reset_contract_credit_debt()
        # for partylink_x in groupunit_x._partys.values():
        #     print(f"{groupunit_x.brand=} {partylink_x.creditor_weight=}  {partylink_x._contract_credit:.6f} {partylink_x.debtor_weight=} {partylink_x._contract_debt:.6f} {partylink_x.name=} ")

    # DELETE contract_agenda_debt and contract_agenda_credit
    for partyunit_x in cx._partys.values():
        partyunit_x.reset_contract_credit_debt()


# sourcery skip: no-loop-in-tests
# sourcery skip: no-conditionals-in-tests
def test_contract_agenda_credit_debt_IsCorrectlySet():
    # GIVEN
    cx = examples_contract_v001_with_large_agenda()
    clear_all_partyunits_groupunits_contract_agenda_credit_debt(cx=cx)

    # TEST contract_agenda_debt and contract_agenda_credit are empty
    sum_groupunit_contract_agenda_credit = 0
    sum_groupunit_contract_agenda_debt = 0
    sum_partylink_contract_agenda_credit = 0
    sum_partylink_contract_agenda_debt = 0
    for groupunit_x in cx._groups.values():
        # print(f"{partyunit.name=}")
        sum_groupunit_contract_agenda_credit += groupunit_x._contract_agenda_credit
        sum_groupunit_contract_agenda_debt += groupunit_x._contract_agenda_debt
        for partylink_x in groupunit_x._partys.values():
            sum_partylink_contract_agenda_credit += partylink_x._contract_agenda_credit
            sum_partylink_contract_agenda_debt += partylink_x._contract_agenda_debt

    assert sum_groupunit_contract_agenda_credit == 0
    assert sum_groupunit_contract_agenda_debt == 0
    assert sum_partylink_contract_agenda_credit == 0
    assert sum_partylink_contract_agenda_debt == 0

    # TEST contract_agenda_debt and contract_agenda_credit are empty
    sum_partyunit_contract_agenda_credit = 0
    sum_partyunit_contract_agenda_debt = 0
    sum_partyunit_contract_agenda_ratio_credit = 0
    sum_partyunit_contract_agenda_ratio_debt = 0
    for partyunit in cx._partys.values():
        # print(f"{partyunit.name=}")
        sum_partyunit_contract_agenda_credit += partyunit._contract_agenda_credit
        sum_partyunit_contract_agenda_debt += partyunit._contract_agenda_debt
        sum_partyunit_contract_agenda_ratio_credit += (
            partyunit._contract_agenda_ratio_credit
        )
        sum_partyunit_contract_agenda_ratio_debt += (
            partyunit._contract_agenda_ratio_debt
        )

    assert sum_partyunit_contract_agenda_credit == 0
    assert sum_partyunit_contract_agenda_debt == 0
    assert sum_partyunit_contract_agenda_ratio_credit == 0
    assert sum_partyunit_contract_agenda_ratio_debt == 0

    # WHEN
    agenda_list = cx.get_agenda_items()

    # THEN
    assert len(agenda_list) == 68
    sum_contract_agenda_importance = 0
    agenda_no_grouplines_count = 0
    agenda_yes_grouplines_count = 0
    agenda_no_grouplines_contract_i_sum = 0
    agenda_yes_grouplines_contract_i_sum = 0
    for agenda_item in agenda_list:
        sum_contract_agenda_importance += agenda_item._contract_importance
        if agenda_item._grouplines == {}:
            agenda_no_grouplines_count += 1
            agenda_no_grouplines_contract_i_sum += agenda_item._contract_importance
        else:
            agenda_yes_grouplines_count += 1
            agenda_yes_grouplines_contract_i_sum += agenda_item._contract_importance
        # print(f"idea importance: {agenda_item._contract_importance:.7f} {sum_contract_agenda_importance:.5f} {agenda_item._label=} ")
        # print(f"{agenda_item.get_road()}")
    print(f"{sum_contract_agenda_importance=}")
    assert agenda_no_grouplines_count == 20
    assert agenda_yes_grouplines_count == 48
    assert agenda_no_grouplines_contract_i_sum == 0.00447826215370075
    assert agenda_yes_grouplines_contract_i_sum == 0.0027152834170378025
    x2 = agenda_no_grouplines_contract_i_sum + agenda_yes_grouplines_contract_i_sum
    e10 = 0.0000000001
    assert abs(x2 - sum_contract_agenda_importance) < e10

    assert sum_contract_agenda_importance == 0.007193545570738553

    sum_groupunit_contract_agenda_credit = 0
    sum_groupunit_contract_agenda_debt = 0
    sum_partylink_contract_agenda_credit = 0
    sum_partylink_contract_agenda_debt = 0
    partylink_count = 0
    for groupunit_x in cx._groups.values():
        # print(f"{partyunit.name=}")
        sum_groupunit_contract_agenda_credit += groupunit_x._contract_agenda_credit
        sum_groupunit_contract_agenda_debt += groupunit_x._contract_agenda_debt
        for partylink_x in groupunit_x._partys.values():
            sum_partylink_contract_agenda_credit += partylink_x._contract_agenda_credit
            sum_partylink_contract_agenda_debt += partylink_x._contract_agenda_debt
            partylink_count += 1

    assert partylink_count == 81
    x_sum = 0.0027152834170378025
    assert sum_groupunit_contract_agenda_credit == x_sum
    assert sum_groupunit_contract_agenda_debt == x_sum
    assert sum_partylink_contract_agenda_credit == x_sum
    assert sum_partylink_contract_agenda_debt == x_sum
    assert (
        abs(agenda_yes_grouplines_contract_i_sum - sum_groupunit_contract_agenda_credit)
        < e10
    )

    sum_partyunit_contract_agenda_credit = 0
    sum_partyunit_contract_agenda_debt = 0
    sum_partyunit_contract_agenda_ratio_credit = 0
    sum_partyunit_contract_agenda_ratio_debt = 0
    for partyunit in cx._partys.values():
        assert partyunit._contract_credit != None
        assert partyunit._contract_credit not in [0.25, 0.5]
        assert partyunit._contract_debt != None
        assert partyunit._contract_debt not in [
            0.8,
            0.1,
        ]  # print(f"{partyunit.name=}")
        sum_partyunit_contract_agenda_credit += partyunit._contract_agenda_credit
        sum_partyunit_contract_agenda_debt += partyunit._contract_agenda_debt
        sum_partyunit_contract_agenda_ratio_credit += (
            partyunit._contract_agenda_ratio_credit
        )
        sum_partyunit_contract_agenda_ratio_debt += (
            partyunit._contract_agenda_ratio_debt
        )

    assert (
        abs(sum_partyunit_contract_agenda_credit - sum_contract_agenda_importance) < e10
    )
    assert (
        abs(sum_partyunit_contract_agenda_debt - sum_contract_agenda_importance) < e10
    )
    assert abs(sum_partyunit_contract_agenda_ratio_credit - 1) < e10
    assert abs(sum_partyunit_contract_agenda_ratio_debt - 1) < e10

    # partyunit_contract_credit_sum = 0.0
    # partyunit_contract_debt_sum = 0.0

    # assert partyunit_contract_credit_sum == 1.0
    # assert partyunit_contract_debt_sum > 0.9999999
    # assert partyunit_contract_debt_sum < 1.00000001


def test_contract_agenda_ratio_credit_debt_IsCorrectlySetWhenAgendaIsEmpty():
    # GIVEN
    owner_text = "Noa"
    cx = ContractUnit(_owner=owner_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_party = partyunit_shop(name=rico_text, creditor_weight=0.5, debtor_weight=2)
    carm_party = partyunit_shop(name=carm_text, creditor_weight=1.5, debtor_weight=3)
    patr_party = partyunit_shop(name=patr_text, creditor_weight=8, debtor_weight=5)
    cx.set_partyunit(partyunit=rico_party)
    cx.set_partyunit(partyunit=carm_party)
    cx.set_partyunit(partyunit=patr_party)
    cx_rico_party = cx._partys.get(rico_text)
    cx_carm_party = cx._partys.get(carm_text)
    cx_patr_party = cx._partys.get(patr_text)

    assert cx_rico_party._contract_agenda_credit in [0, None]
    assert cx_rico_party._contract_agenda_debt in [0, None]
    assert cx_carm_party._contract_agenda_credit in [0, None]
    assert cx_carm_party._contract_agenda_debt in [0, None]
    assert cx_patr_party._contract_agenda_credit in [0, None]
    assert cx_patr_party._contract_agenda_debt in [0, None]
    assert cx_rico_party._contract_agenda_ratio_credit != 0.05
    assert cx_rico_party._contract_agenda_ratio_debt != 0.2
    assert cx_carm_party._contract_agenda_ratio_credit != 0.15
    assert cx_carm_party._contract_agenda_ratio_debt != 0.3
    assert cx_patr_party._contract_agenda_ratio_credit != 0.8
    assert cx_patr_party._contract_agenda_ratio_debt != 0.5

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assert cx_rico_party._contract_agenda_credit == 0
    assert cx_rico_party._contract_agenda_debt == 0
    assert cx_carm_party._contract_agenda_credit == 0
    assert cx_carm_party._contract_agenda_debt == 0
    assert cx_patr_party._contract_agenda_credit == 0
    assert cx_patr_party._contract_agenda_debt == 0
    assert cx_rico_party._contract_agenda_ratio_credit == 0.05
    assert cx_rico_party._contract_agenda_ratio_debt == 0.2
    assert cx_carm_party._contract_agenda_ratio_credit == 0.15
    assert cx_carm_party._contract_agenda_ratio_debt == 0.3
    assert cx_patr_party._contract_agenda_ratio_credit == 0.8
    assert cx_patr_party._contract_agenda_ratio_debt == 0.5


def test_contract_get_party_groups_returnsCorrectData():
    cx = ContractUnit(_owner="prom")
    cx.add_idea(idea_kid=IdeaKid(_label="swim"), walk="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))

    carmen_group_list = cx.get_party_groups(party_name=carm_text)
    assert carmen_group_list == [carm_text]

    swimmers = "swimmers"
    carmen_party_dict = {PartyName(carm_text): partylink_shop(name=carm_text)}
    swim_group = groupunit_shop(brand=swimmers, _partys=carmen_party_dict)
    cx._groups[swim_group.brand] = swim_group
    carmen_group_list = cx.get_party_groups(party_name=carm_text)
    assert carmen_group_list == [carm_text, swimmers]


def test_contract_PartyUnit_CorrectlyCreatesNewName():
    # GIVEN
    cx = ContractUnit(_owner="prom")
    rico_text = "rico"
    cx.add_partyunit(name=rico_text, uid=61, creditor_weight=13)
    cx.add_partyunit(name="carmen", uid=5)
    cx.add_partyunit(name="patrick", creditor_weight=17)
    assert len(cx._partys) == 3
    assert cx._partys.get(rico_text) != None
    assert cx._partys.get(rico_text).creditor_weight == 13
    assert len(cx._groups) == 3
    assert cx._groups.get(rico_text) != None
    assert cx._groups.get(rico_text)._single_party == True

    # WHEN
    beto_text = "beta"
    cx.edit_partyunit_name(
        old_name=rico_text,
        new_name=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert cx._partys.get(beto_text) != None
    assert cx._partys.get(beto_text).creditor_weight == 13
    assert cx._partys.get(rico_text) is None
    assert len(cx._partys) == 3
    assert len(cx._groups) == 3
    assert cx._groups.get(rico_text) is None
    assert cx._groups.get(beto_text) != None
    assert cx._groups.get(beto_text)._single_party == True


def test_contract_PartyUnit_raiseErrorNewNamePreviouslyExists():
    # GIVEN
    sx = ContractUnit(_owner="prom")
    rico_text = "rico"
    sx.add_partyunit(name=rico_text, uid=61, creditor_weight=13)
    carmen_text = "carmen"
    sx.add_partyunit(name=carmen_text, uid=5)
    sx.add_partyunit(name="patrick", creditor_weight=17)
    assert len(sx._partys) == 3
    assert sx._partys.get(rico_text) != None
    assert sx._partys.get(rico_text).creditor_weight == 13
    assert len(sx._groups) == 3
    assert sx._groups.get(rico_text) != None
    assert sx._groups.get(rico_text)._single_party == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_partyunit_name(
            old_name=rico_text,
            new_name=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' change to '{carmen_text}' failed since '{carmen_text}' exists."
    )


def test_contract_PartyUnit_CorrectlyChangesGroupUnitPartyLinks():
    # GIVEN
    prom_text = "prom"
    cx = ContractUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.add_partyunit(name=rico_text, uid=61, creditor_weight=13)
    cx.add_partyunit(name=carm_text, uid=5)
    cx.add_partyunit(name=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyName(carm_text): partylink_shop(name=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(name=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(name=rico_text, creditor_weight=7, debtor_weight=30)
    )
    cx.set_groupunit(groupunit=swim_group)

    swim_group = cx._groups.get(swim_text)
    assert len(swim_group._partys) == 2
    assert swim_group._partys.get(rico_text) != None
    assert swim_group._partys.get(rico_text).creditor_weight == 7
    assert swim_group._partys.get(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    cx.edit_partyunit_name(
        old_name=rico_text,
        new_name=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._partys.get(beto_text) != None
    assert swim_group._partys.get(beto_text).creditor_weight == 7
    assert swim_group._partys.get(beto_text).debtor_weight == 30
    assert swim_group._partys.get(rico_text) is None
    assert len(swim_group._partys) == 2


def test_contract_PartyUnit_CorrectlyMergesNames():
    # GIVEN
    prom_text = "prom"
    cx = ContractUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.add_partyunit(name=rico_text, uid=61, creditor_weight=13)
    cx.add_partyunit(name=carm_text, uid=5, creditor_weight=3)
    cx.add_partyunit(name=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyName(carm_text): partylink_shop(name=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(name=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(name=rico_text, creditor_weight=7, debtor_weight=30)
    )
    cx.set_groupunit(groupunit=swim_group)

    assert len(cx._partys) == 3
    assert cx._partys.get(rico_text) != None
    assert cx._partys.get(rico_text).creditor_weight == 13
    assert cx._partys.get(carm_text) != None
    assert cx._partys.get(carm_text).creditor_weight == 3

    # WHEN / THEN
    cx.edit_partyunit_name(
        old_name=rico_text,
        new_name=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert cx._partys.get(carm_text) != None
    assert cx._partys.get(carm_text).creditor_weight == 16
    assert cx._partys.get(rico_text) is None
    assert len(cx._partys) == 2


def test_contract_PartyUnit_CorrectlyMergesGroupUnitPartyLinks():
    # GIVEN
    # GIVEN
    prom_text = "prom"
    cx = ContractUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.add_partyunit(name=rico_text, uid=61, creditor_weight=13)
    cx.add_partyunit(name=carm_text, uid=5)
    cx.add_partyunit(name=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyName(carm_text): partylink_shop(name=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(name=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(name=rico_text, creditor_weight=7, debtor_weight=30)
    )
    cx.set_groupunit(groupunit=swim_group)

    swim_group = cx._groups.get(swim_text)
    assert len(swim_group._partys) == 2
    assert swim_group._partys.get(rico_text) != None
    assert swim_group._partys.get(rico_text).creditor_weight == 7
    assert swim_group._partys.get(rico_text).debtor_weight == 30
    assert swim_group._partys.get(carm_text) != None
    assert swim_group._partys.get(carm_text).creditor_weight == 5
    assert swim_group._partys.get(carm_text).debtor_weight == 18

    # WHEN
    cx.edit_partyunit_name(
        old_name=rico_text,
        new_name=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._partys.get(carm_text) != None
    assert swim_group._partys.get(carm_text).creditor_weight == 12
    assert swim_group._partys.get(carm_text).debtor_weight == 48
    assert swim_group._partys.get(rico_text) is None
    assert len(swim_group._partys) == 1


def test_contract_PartyUnit_raiseErrorNewNameGroupUnitPreviouslyExists():
    # GIVEN
    sx = ContractUnit(_owner="prom")
    rico_text = "rico"
    sx.add_partyunit(name=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    sx.add_partyunit(name=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(brand=carmen_text)
    carmen_group.set_partylink(partylink=partylink_shop(name=rico_text))
    carmen_group.set_partylink(partylink=partylink_shop(name=anna_text))
    sx.set_groupunit(groupunit=carmen_group)
    assert len(sx._groups) == 3
    assert sx._partys.get(carmen_text) is None
    assert sx._groups.get(carmen_text)._single_party == False
    assert len(sx._groups.get(carmen_text)._partys) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_partyunit_name(
            old_name=rico_text,
            new_name=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' change to '{carmen_text}' failed since non-single group '{carmen_text}' exists."
    )


def test_contract_PartyUnit_CorrectlyOverwriteNewNameGroupUnit():
    # GIVEN
    sx = ContractUnit(_owner="prom")
    rico_text = "rico"
    sx.add_partyunit(name=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    sx.add_partyunit(name=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(brand=carmen_text)
    carmen_group.set_partylink(
        partylink=partylink_shop(name=rico_text, creditor_weight=3)
    )
    carmen_group.set_partylink(
        partylink=partylink_shop(name=anna_text, creditor_weight=5)
    )
    sx.set_groupunit(groupunit=carmen_group)
    assert len(sx._groups) == 3
    assert sx._partys.get(rico_text) != None
    assert sx._partys.get(carmen_text) is None
    assert sx._groups.get(carmen_text)._single_party == False
    assert len(sx._groups.get(carmen_text)._partys) == 2
    assert sx._groups.get(carmen_text)._partys.get(anna_text).creditor_weight == 5
    assert sx._groups.get(carmen_text)._partys.get(rico_text).creditor_weight == 3

    # WHEN
    sx.edit_partyunit_name(
        old_name=rico_text,
        new_name=carmen_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=True,
    )

    assert len(sx._groups) == 2
    assert sx._partys.get(rico_text) is None
    assert sx._partys.get(carmen_text) != None
    assert sx._groups.get(carmen_text)._single_party == True
    assert len(sx._groups.get(carmen_text)._partys) == 1
    assert sx._groups.get(carmen_text)._partys.get(rico_text) is None
    assert sx._groups.get(carmen_text)._partys.get(carmen_text).creditor_weight == 1


def test_contract_set_all_partyunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    owner_text = "Noa"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_partyunit(partyunit=partyunit_shop(name=swim_text))
    sx.set_partyunit(partyunit=partyunit_shop(name=walk_text))
    sx.set_partyunit(partyunit=partyunit_shop(name=fly_text))
    assert sx._partys[swim_text].uid is None
    assert sx._partys[walk_text].uid is None
    assert sx._partys[fly_text].uid is None

    # WHEN
    sx.set_all_partyunits_uids_unique()

    # THEN
    assert sx._partys[swim_text].uid != None
    assert sx._partys[walk_text].uid != None
    assert sx._partys[fly_text].uid != None


def test_contract_set_all_partyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    owner_text = "Noa"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_partyunit(partyunit=partyunit_shop(name=swim_text, uid=3))
    sx.set_partyunit(partyunit=partyunit_shop(name=walk_text, uid=3))
    sx.set_partyunit(partyunit=partyunit_shop(name=fly_text))
    assert sx._partys[swim_text].uid == 3
    assert sx._partys[walk_text].uid == 3
    assert sx._partys[fly_text].uid is None

    # WHEN
    sx.set_all_partyunits_uids_unique()

    # THEN
    print(f"{sx._partys[swim_text].uid=}")
    print(f"{sx._partys[walk_text].uid=}")
    assert sx._partys[swim_text].uid != sx._partys[walk_text].uid
    assert sx._partys[walk_text].uid != 3
    assert sx._partys[walk_text].uid != 3
    assert sx._partys[fly_text].uid != None


def test_contract_set_all_partyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    owner_text = "Noa"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_partyunit(partyunit=partyunit_shop(name=swim_text, uid=3))
    sx.set_partyunit(partyunit=partyunit_shop(name=walk_text, uid=3))
    sx.set_partyunit(partyunit=partyunit_shop(name=fly_text))
    assert sx._partys[swim_text].uid == 3
    assert sx._partys[walk_text].uid == 3
    assert sx._partys[fly_text].uid is None

    # WHEN
    sx.set_all_partyunits_uids_unique()

    # THEN
    print(f"{sx._partys[swim_text].uid=}")
    print(f"{sx._partys[walk_text].uid=}")
    assert sx._partys[swim_text].uid != sx._partys[walk_text].uid
    assert sx._partys[walk_text].uid != 3
    assert sx._partys[walk_text].uid != 3
    assert sx._partys[fly_text].uid != None


def test_contract_all_partyunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    owner_text = "Noa"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_partyunit(partyunit=partyunit_shop(name=swim_text, uid=3))
    sx.set_partyunit(partyunit=partyunit_shop(name=walk_text, uid=3))
    sx.set_partyunit(partyunit=partyunit_shop(name=fly_text))
    assert sx._partys[swim_text].uid == 3
    assert sx._partys[walk_text].uid == 3
    assert sx._partys[fly_text].uid is None

    # WHEN1 / THEN
    assert sx.all_partyunits_uids_are_unique() == False

    # WHEN2
    sx.set_partyunit(partyunit=partyunit_shop(name=swim_text, uid=4))

    # THEN
    assert sx.all_partyunits_uids_are_unique() == False

    # WHEN3
    sx.set_partyunit(partyunit=partyunit_shop(name=fly_text, uid=5))

    # THEN
    assert sx.all_partyunits_uids_are_unique()


def test_contract_get_partyunits_name_list_CorrectlyReturnsListOfPartyUnits():
    # GIVEN
    owner_text = "Noa"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    sx.set_partyunit(partyunit=partyunit_shop(name=sam_text))
    sx.set_partyunit(partyunit=partyunit_shop(name=will_text))
    sx.set_partyunit(partyunit=partyunit_shop(name=fry_text))
    fun_text = "fun people"
    fun_group = groupunit_shop(brand=fun_text)
    fun_group.set_partylink(partylink=partylink_shop(name=will_text))
    sx.set_groupunit(groupunit=fun_group)
    assert len(sx._groups) == 4
    assert len(sx._partys) == 3

    # WHEN
    partyunit_list_x = sx.get_partyunits_name_list()

    # THEN
    assert len(partyunit_list_x) == 4
    assert partyunit_list_x[0] == ""
    assert partyunit_list_x[1] == fry_text
    assert partyunit_list_x[2] == sam_text
    assert partyunit_list_x[3] == will_text


def test_contract_set_banking_data_partyunits_CorrectlySetsPartyUnitBankingAttr():
    # GIVEN
    bob_text = "bob"
    cx = ContractUnit(_owner=bob_text)
    cx.set_partys_empty_if_null()
    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    cx.set_partyunit(partyunit=partyunit_shop(name=sam_text))
    cx.set_partyunit(partyunit=partyunit_shop(name=wil_text))
    cx.set_partyunit(partyunit=partyunit_shop(name=fry_text))
    assert cx._partys.get(sam_text)._bank_tax_paid is None
    assert cx._partys.get(sam_text)._bank_tax_diff is None
    assert cx._partys.get(wil_text)._bank_tax_paid is None
    assert cx._partys.get(wil_text)._bank_tax_diff is None
    assert cx._partys.get(fry_text)._bank_tax_paid is None
    assert cx._partys.get(fry_text)._bank_tax_diff is None
    elu_partyunit = partyunit_shop(name=elu_text)
    elu_partyunit._bank_tax_paid = 0.003
    elu_partyunit._bank_tax_diff = 0.007
    cx.set_partyunit(partyunit=elu_partyunit)
    assert cx._partys.get(elu_text)._bank_tax_paid == 0.003
    assert cx._partys.get(elu_text)._bank_tax_diff == 0.007

    river_tparty_sam = RiverTpartyUnit(bob_text, sam_text, 0.209, 0, 0.034)
    river_tparty_wil = RiverTpartyUnit(bob_text, wil_text, 0.501, 0, 0.024)
    river_tparty_fry = RiverTpartyUnit(bob_text, fry_text, 0.111, 0, 0.006)
    river_tpartys = {
        river_tparty_sam.tax_name: river_tparty_sam,
        river_tparty_wil.tax_name: river_tparty_wil,
        river_tparty_fry.tax_name: river_tparty_fry,
    }
    # WHEN
    cx.set_banking_attr_partyunits(river_tpartys=river_tpartys)

    # THEN
    assert cx._partys.get(sam_text)._bank_tax_paid == 0.209
    assert cx._partys.get(sam_text)._bank_tax_diff == 0.034
    assert cx._partys.get(wil_text)._bank_tax_paid == 0.501
    assert cx._partys.get(wil_text)._bank_tax_diff == 0.024
    assert cx._partys.get(fry_text)._bank_tax_paid == 0.111
    assert cx._partys.get(fry_text)._bank_tax_diff == 0.006
    assert cx._partys.get(elu_text)._bank_tax_paid is None
    assert cx._partys.get(elu_text)._bank_tax_diff is None


def test_get_intersection_of_partys_CorrectlyReturnsUnionOfKeysOfTwoDictionarys_scenario1():
    # GIVEN
    bob_text = "bob"
    cx = ContractUnit(_owner=bob_text)
    cx.set_partys_empty_if_null()

    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    cx.set_partyunit(partyunit=partyunit_shop(name=bob_text))
    cx.set_partyunit(partyunit=partyunit_shop(name=sam_text))
    cx.set_partyunit(partyunit=partyunit_shop(name=wil_text))
    cx.set_partyunit(partyunit=partyunit_shop(name=fry_text))

    tx = ContractUnit()
    tx.set_partys_empty_if_null()

    tx.set_partyunit(partyunit=partyunit_shop(name=bob_text))
    tx.set_partyunit(partyunit=partyunit_shop(name=wil_text))
    tx.set_partyunit(partyunit=partyunit_shop(name=fry_text))
    tx.set_partyunit(partyunit=partyunit_shop(name=elu_text))

    # WHEN
    print(f"{len(cx._partys)=} {len(tx._partys)=}")
    intersection_x = get_intersection_of_partys(cx._partys, tx._partys)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}
