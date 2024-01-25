from src._prime.road import RoadUnit
from src.agenda.party import PartyID, partylink_shop, partyunit_shop
from src.agenda.group import GroupBrand, groupunit_shop, balancelink_shop
from src.agenda.examples.example_agendas import (
    agenda_v001 as examples_agenda_v001,
    agenda_v001_with_large_intent as examples_agenda_v001_with_large_intent,
)
from src.agenda.agenda import AgendaUnit, agendaunit_shop, get_intersection_of_partys
from src.agenda.idea import ideaunit_shop, IdeaUnit
from pytest import raises as pytest_raises
from dataclasses import dataclass


def test_AgendaUnit_set_partyunit_SetObjCorrectly():
    # GIVEN
    yahri_party = partyunit_shop(party_id=PartyID("yahri"))
    partys_x = {yahri_party.party_id: yahri_party}
    bob_agenda = agendaunit_shop("Bob")

    # WHEN
    bob_agenda.set_partyunit(partyunit=yahri_party)

    # THEN
    assert bob_agenda._partys == partys_x


def test_examples_agenda_v001_has_partys():
    # GIVEN / WHEN
    yao_agenda = examples_agenda_v001()

    # THEN
    assert yao_agenda._partys != None
    assert len(yao_agenda._partys) == 22


def test_AgendaUnit_set_party_CorrectlySetsPartys_v1():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    yue_agenda.set_agenda_metrics()
    assert len(yue_agenda._partys) == 0
    assert len(yue_agenda._groups) == 0

    # WHEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))

    # THEN
    assert len(yue_agenda._partys) == 3
    assert len(yue_agenda._groups) == 3
    assert yue_agenda._groups["rico"]._single_party == True

    # WHEN
    rico_group = rico_text
    carm_group = carm_text
    patr_group = patr_text
    yue_agenda._idearoot.set_balancelink(
        balancelink_shop(rico_group, creditor_weight=10)
    )
    yue_agenda._idearoot.set_balancelink(
        balancelink_shop(carm_group, creditor_weight=10)
    )
    yue_agenda._idearoot.set_balancelink(
        balancelink_shop(patr_group, creditor_weight=10)
    )
    assert len(yue_agenda._idearoot._balancelinks) == 3


def test_AgendaUnit_set_party_CorrectlySetsPartys_v2():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    assign_text = "assignment"

    # WHEN
    yue_agenda.add_partyunit(
        party_id=rico_text, uid=61, creditor_weight=13, debtor_weight=8
    )
    yue_agenda.add_partyunit(party_id=carm_text, uid=5, debtor_weight=5)
    yue_agenda.add_partyunit(
        party_id=patr_text, creditor_weight=17, depotlink_type=assign_text
    )

    # THEN
    assert len(yue_agenda._partys) == 3
    assert len(yue_agenda._groups) == 3
    assert yue_agenda.get_groupunit(rico_text)._single_party == True
    assert yue_agenda._partys.get(patr_text).creditor_weight == 17
    assert yue_agenda._partys.get(carm_text).debtor_weight == 5
    assert yue_agenda._partys.get(patr_text).depotlink_type == assign_text


def test_AgendaUnit_get_party_ReturnsCorrectObj():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    yue_agenda.add_partyunit(party_id=rico_text)
    yue_agenda.add_partyunit(party_id=carm_text)

    # WHEN
    rico_party = yue_agenda.get_party(rico_text)
    carm_party = yue_agenda.get_party(carm_text)

    # THEN
    assert rico_party == yue_agenda._partys.get(rico_text)
    assert carm_party == yue_agenda._partys.get(carm_text)


def test_AgendaUnit_get_partys_depotlink_count_GetsCorrectCount():
    # GIVEN
    sue_text = "sue"
    sue_agenda = agendaunit_shop(_agent_id=sue_text)
    assign_text = "assignment"

    # WHEN
    rico_text = "rico"
    carm_text = "carmen"
    sue_agenda.add_partyunit(party_id=rico_text)
    sue_agenda.add_partyunit(party_id=carm_text)
    # THEN
    assert len(sue_agenda._partys) == 2
    assert sue_agenda.get_partys_depotlink_count() == 0

    # WHEN
    patr_text = "patrick"
    sue_agenda.add_partyunit(party_id=patr_text, depotlink_type=assign_text)
    # THEN
    assert len(sue_agenda._partys) == 3
    assert sue_agenda.get_partys_depotlink_count() == 1

    # WHEN
    rico_party = sue_agenda.get_party(rico_text)
    rico_party.set_depotlink_type(assign_text)
    # THEN
    assert len(sue_agenda._partys) == 3
    assert sue_agenda.get_partys_depotlink_count() == 2


def test_AgendaUnit_get_idea_list_CorrectlySetsPartyLinkAgendaCreditAndDebt():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    bl_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    yue_agenda._idearoot.set_balancelink(balancelink=bl_rico)
    yue_agenda._idearoot.set_balancelink(balancelink=bl_carm)
    yue_agenda._idearoot.set_balancelink(balancelink=bl_patr)

    rico_groupunit = yue_agenda.get_groupunit(rico_text)
    carm_groupunit = yue_agenda.get_groupunit(carm_text)
    patr_groupunit = yue_agenda.get_groupunit(patr_text)
    rico_partylink = rico_groupunit._partys.get(rico_text)
    carm_partylink = carm_groupunit._partys.get(carm_text)
    patr_partylink = patr_groupunit._partys.get(patr_text)
    rico_partylink._agenda_credit is None
    rico_partylink._agenda_debt is None
    carm_partylink._agenda_credit is None
    carm_partylink._agenda_debt is None
    patr_partylink._agenda_credit is None
    patr_partylink._agenda_debt is None

    # for group in yue_agenda._groups.values():
    #     for partylink in group._partys.values():
    #         assert partylink._agenda_credit is None
    #         assert partylink._agenda_debt is None

    yue_agenda.set_agenda_metrics()

    # for balancelink in yue_agenda._balanceheirs.values():
    #     print(
    #         f"{yue_agenda._agenda_importance=} {balancelink.brand=} {balancelink._agenda_credit=} {balancelink._agenda_debt=}"
    #     )

    assert rico_partylink._agenda_credit == 0.5
    assert rico_partylink._agenda_debt == 0.8
    assert carm_partylink._agenda_credit == 0.25
    assert carm_partylink._agenda_debt == 0.1
    assert patr_partylink._agenda_credit == 0.25
    assert patr_partylink._agenda_debt == 0.1

    # partylink_agenda_credit_sum = 0.0
    # partylink_agenda_debt_sum = 0.0
    # for group in yue_agenda._groups.values():
    #     # print(f"{group.brand=} {group._partys=}")

    #     for partylink in group._partys.values():
    #         assert partylink._agenda_credit != None
    #         assert partylink._agenda_credit in [0.25, 0.5]
    #         assert partylink._agenda_debt != None
    #         assert partylink._agenda_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{group.brand=} {partylink._agenda_importance=} {group._agenda_importance=}"
    #         # )
    #         partylink_agenda_credit_sum += partylink._agenda_credit
    #         partylink_agenda_debt_sum += partylink._agenda_debt

    #         # print(f"{partylink_agenda_importance_sum=}")
    # assert partylink_agenda_credit_sum == 1.0
    # assert partylink_agenda_debt_sum == 1.0

    assert (
        rico_partylink._agenda_credit
        + carm_partylink._agenda_credit
        + patr_partylink._agenda_credit
        == 1.0
    )
    assert (
        rico_partylink._agenda_debt
        + carm_partylink._agenda_debt
        + patr_partylink._agenda_debt
        == 1.0
    )

    # WHEN another action, check metrics are as expected
    selena_text = "selena"
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(selena_text)))
    yue_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            brand=GroupBrand(selena_text), creditor_weight=20, debtor_weight=13
        )
    )
    yue_agenda.set_agenda_metrics()

    # THEN
    selena_groupunit = yue_agenda.get_groupunit(selena_text)
    selena_partylink = selena_groupunit._partys.get(selena_text)

    assert rico_partylink._agenda_credit != 0.25
    assert rico_partylink._agenda_debt != 0.8
    assert carm_partylink._agenda_credit != 0.25
    assert carm_partylink._agenda_debt != 0.1
    assert patr_partylink._agenda_credit != 0.5
    assert patr_partylink._agenda_debt != 0.1
    assert selena_partylink._agenda_credit != None
    assert selena_partylink._agenda_debt != None

    # partylink_agenda_credit_sum = 0.0
    # partylink_agenda_debt_sum = 0.0

    # for group in yue_agenda._groups.values():
    #     # print(f"{group.brand=} {group._partys=}")

    #     for partylink in group._partys.values():
    #         assert partylink._agenda_credit != None
    #         assert partylink._agenda_credit not in [0.25, 0.5]
    #         assert partylink._agenda_debt != None
    #         assert partylink._agenda_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{group.brand=} {partylink._agenda_importance=} {group._agenda_importance=}"
    #         # )
    #         partylink_agenda_credit_sum += partylink._agenda_credit
    #         partylink_agenda_debt_sum += partylink._agenda_debt

    #         # print(f"{partylink_agenda_importance_sum=}")
    # assert partylink_agenda_credit_sum == 1.0
    # assert partylink_agenda_debt_sum > 0.9999999
    # assert partylink_agenda_debt_sum < 1.00000001

    assert (
        rico_partylink._agenda_credit
        + carm_partylink._agenda_credit
        + patr_partylink._agenda_credit
        + selena_partylink._agenda_credit
        == 1.0
    )
    assert (
        rico_partylink._agenda_debt
        + carm_partylink._agenda_debt
        + patr_partylink._agenda_debt
        + selena_partylink._agenda_debt
        > 0.9999999
    )
    assert (
        rico_partylink._agenda_debt
        + carm_partylink._agenda_debt
        + patr_partylink._agenda_debt
        + selena_partylink._agenda_debt
        < 1.0
    )


def test_AgendaUnit_get_idea_list_CorrectlySetsPartyUnitAgendaImportance():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    swim_text = "swim"
    yue_agenda.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    bl_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    yue_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_rico)
    yue_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_carm)
    yue_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_patr)

    rico_partyunit = yue_agenda._partys.get(rico_text)
    carm_partyunit = yue_agenda._partys.get(carm_text)
    patr_partyunit = yue_agenda._partys.get(patr_text)

    assert rico_partyunit._agenda_credit == 0
    assert rico_partyunit._agenda_debt == 0
    assert carm_partyunit._agenda_credit == 0
    assert carm_partyunit._agenda_debt == 0
    assert patr_partyunit._agenda_credit == 0
    assert patr_partyunit._agenda_debt == 0

    # WHEN
    yue_agenda.set_agenda_metrics()

    # THEN
    partyunit_agenda_credit_sum = 0.0
    partyunit_agenda_debt_sum = 0.0

    assert rico_partyunit._agenda_credit == 0.5
    assert rico_partyunit._agenda_debt == 0.8
    assert carm_partyunit._agenda_credit == 0.25
    assert carm_partyunit._agenda_debt == 0.1
    assert patr_partyunit._agenda_credit == 0.25
    assert patr_partyunit._agenda_debt == 0.1

    assert (
        rico_partyunit._agenda_credit
        + carm_partyunit._agenda_credit
        + patr_partyunit._agenda_credit
        == 1.0
    )
    assert (
        rico_partyunit._agenda_debt
        + carm_partyunit._agenda_debt
        + patr_partyunit._agenda_debt
        == 1.0
    )

    # for partyunit in yue_agenda._partys.values():
    #     assert partyunit._agenda_credit != None
    #     assert partyunit._agenda_credit in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._agenda_creditor=} {group._agenda_creditor=}"
    #     # )
    #     print(f"{partyunit.party_id=} {partyunit._agenda_credit=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_credit_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_credit_sum += partyunit._agenda_credit
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt

    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001

    # WHEN another action, check metrics are as expected
    selena_text = "selena"
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(selena_text)))
    yue_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            brand=selena_text, creditor_weight=20, debtor_weight=10
        )
    )
    yue_agenda.set_agenda_metrics()

    # THEN
    selena_partyunit = yue_agenda._partys.get(selena_text)

    assert rico_partyunit._agenda_credit != 0.5
    assert rico_partyunit._agenda_debt != 0.8
    assert carm_partyunit._agenda_credit != 0.25
    assert carm_partyunit._agenda_debt != 0.1
    assert patr_partyunit._agenda_credit != 0.25
    assert patr_partyunit._agenda_debt != 0.1
    assert selena_partyunit._agenda_credit != None
    assert selena_partyunit._agenda_debt != None

    assert (
        rico_partyunit._agenda_credit
        + carm_partyunit._agenda_credit
        + patr_partyunit._agenda_credit
        < 1.0
    )
    assert (
        rico_partyunit._agenda_credit
        + carm_partyunit._agenda_credit
        + patr_partyunit._agenda_credit
        + selena_partyunit._agenda_credit
        == 1.0
    )
    assert (
        rico_partyunit._agenda_debt
        + carm_partyunit._agenda_debt
        + patr_partyunit._agenda_debt
        < 1.0
    )
    assert (
        rico_partyunit._agenda_debt
        + carm_partyunit._agenda_debt
        + patr_partyunit._agenda_debt
        + selena_partyunit._agenda_debt
        == 1.0
    )

    # partyunit_agenda_credit_sum = 0.0
    # partyunit_agenda_debt_sum = 0.0

    # for partyunit in yue_agenda._partys.values():
    #     assert partyunit._agenda_credit != None
    #     assert partyunit._agenda_credit not in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._agenda_creditor=} {group._agenda_creditor=}"
    #     # )
    #     print(f"{partyunit.party_id=} {partyunit._agenda_credit=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_credit_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_credit_sum += partyunit._agenda_credit
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt

    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def test_AgendaUnit_get_idea_list_CorrectlySetsPartGroupedLWPartyUnitAgendaImportance():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    swim_text = "swim"
    yue_agenda.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    bl_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    yue_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_rico)
    yue_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_carm)
    yue_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_patr)

    # no balancelinks attached to this one
    hunt_text = "hunt"
    yue_agenda.add_l1_idea(ideaunit_shop(hunt_text, _weight=3))

    # WHEN
    yue_agenda.set_agenda_metrics()

    # THEN
    rico_groupunit = yue_agenda.get_groupunit(rico_text)
    carm_groupunit = yue_agenda.get_groupunit(carm_text)
    patr_groupunit = yue_agenda.get_groupunit(patr_text)
    assert rico_groupunit._agenda_credit != 0.5
    assert rico_groupunit._agenda_debt != 0.8
    assert carm_groupunit._agenda_credit != 0.25
    assert carm_groupunit._agenda_debt != 0.1
    assert patr_groupunit._agenda_credit != 0.25
    assert patr_groupunit._agenda_debt != 0.1
    assert (
        rico_groupunit._agenda_credit
        + carm_groupunit._agenda_credit
        + patr_groupunit._agenda_credit
        == 0.25
    )
    assert (
        rico_groupunit._agenda_debt
        + carm_groupunit._agenda_debt
        + patr_groupunit._agenda_debt
        == 0.25
    )

    # groupunit_agenda_credit_sum = 0.0
    # groupunit_agenda_debt_sum = 0.0
    # for groupunit in yue_agenda._groups.values():
    #     assert groupunit._agenda_credit != None
    #     assert groupunit._agenda_credit not in [0.25, 0.5]
    #     assert groupunit._agenda_debt != None
    #     assert groupunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {groupunit._agenda_creditor=} {group._agenda_creditor=}"
    #     # )
    #     print(f"{groupunit.brand=} {groupunit._agenda_credit=} {groupunit._agenda_debt=} ")
    #     # print(f"{groupunit_agenda_credit_sum=}")
    #     # print(f"{groupunit_agenda_debt_sum=}")
    #     groupunit_agenda_credit_sum += groupunit._agenda_credit
    #     groupunit_agenda_debt_sum += groupunit._agenda_debt
    # assert groupunit_agenda_credit_sum == 0.25
    # assert groupunit_agenda_debt_sum == 0.25

    rico_partyunit = yue_agenda._partys.get(rico_text)
    carm_partyunit = yue_agenda._partys.get(carm_text)
    patr_partyunit = yue_agenda._partys.get(patr_text)

    assert rico_partyunit._agenda_credit == 0.375
    assert rico_partyunit._agenda_debt == 0.45
    assert carm_partyunit._agenda_credit == 0.3125
    assert carm_partyunit._agenda_debt == 0.275
    assert patr_partyunit._agenda_credit == 0.3125
    assert patr_partyunit._agenda_debt == 0.275

    assert (
        rico_partyunit._agenda_credit
        + carm_partyunit._agenda_credit
        + patr_partyunit._agenda_credit
        == 1.0
    )
    assert (
        rico_partyunit._agenda_debt
        + carm_partyunit._agenda_debt
        + patr_partyunit._agenda_debt
        == 1.0
    )

    # partyunit_agenda_credit_sum = 0.0
    # partyunit_agenda_debt_sum = 0.0
    # for partyunit in yue_agenda._partys.values():
    #     assert partyunit._agenda_credit != None
    #     assert partyunit._agenda_credit not in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._agenda_creditor=} {group._agenda_creditor=}"
    #     # )
    #     print(f"{partyunit.party_id=} {partyunit._agenda_credit=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_credit_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_credit_sum += partyunit._agenda_credit
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt
    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def test_AgendaUnit_set_agenda_metrics_CorrectlySetsPartyAttrs():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    yue_agenda.add_l1_idea(ideaunit_shop("swim"))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.set_partyunit(
        partyunit=partyunit_shop(party_id=PartyID(rico_text), creditor_weight=8)
    )
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    rico_partyunit = yue_agenda._partys.get(rico_text)
    carm_partyunit = yue_agenda._partys.get(carm_text)
    patr_partyunit = yue_agenda._partys.get(patr_text)
    assert rico_partyunit._agenda_credit == 0
    assert rico_partyunit._agenda_debt == 0
    assert carm_partyunit._agenda_credit == 0
    assert carm_partyunit._agenda_debt == 0
    assert patr_partyunit._agenda_credit == 0
    assert patr_partyunit._agenda_debt == 0

    # WHEN
    yue_agenda.set_agenda_metrics()

    # THEN
    assert (
        rico_partyunit._agenda_credit
        + carm_partyunit._agenda_credit
        + patr_partyunit._agenda_credit
        == 1.0
    )
    assert (
        rico_partyunit._agenda_debt
        + carm_partyunit._agenda_debt
        + patr_partyunit._agenda_debt
        == 1.0
    )
    # partyunit_agenda_credit_sum = 0.0
    # partyunit_agenda_debt_sum = 0.0
    # for partyunit in yue_agenda._partys.values():
    #     assert partyunit._agenda_credit != None
    #     assert partyunit._agenda_credit not in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._agenda_creditor=} {group._agenda_creditor=}"
    #     # )
    #     print(f"{partyunit.party_id=} {partyunit._agenda_credit=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_credit_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_credit_sum += partyunit._agenda_credit
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt
    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def test_AgendaUnit_set_agenda_metrics_RaisesErrorWhen_is_partyunits_creditor_weight_sum_correct_IsFalse():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_creditor_weight = 20
    carm_creditor_weight = 30
    patr_creditor_weight = 50
    yue_agenda.set_partyunit(partyunit_shop(rico_text, None, rico_creditor_weight))
    yue_agenda.set_partyunit(partyunit_shop(carm_text, None, carm_creditor_weight))
    yue_agenda.set_partyunit(partyunit_shop(patr_text, None, patr_creditor_weight))
    assert yue_agenda._party_creditor_pool is None
    assert yue_agenda.is_partyunits_creditor_weight_sum_correct()
    assert yue_agenda.set_agenda_metrics() is None

    # WHEN
    x_int = 13
    yue_agenda.set_party_creditor_pool(x_int)
    assert yue_agenda.is_partyunits_creditor_weight_sum_correct() == False
    with pytest_raises(Exception) as excinfo:
        yue_agenda.set_agenda_metrics()
    assert (
        str(excinfo.value)
        == f"is_partyunits_creditor_weight_sum_correct is False. _party_creditor_pool={x_int}. partyunits_creditor_weight_sum={yue_agenda.get_partyunits_creditor_weight_sum()}"
    )

    # WHEN / THEN
    yue_agenda.set_party_creditor_pool(yue_agenda.get_partyunits_creditor_weight_sum())
    assert yue_agenda.set_agenda_metrics() is None


def test_AgendaUnit_set_agenda_metrics_RaisesErrorWhen_is_partyunits_debtor_weight_sum_correct_IsFalse():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 40
    yue_agenda.set_partyunit(partyunit_shop(rico_text, None, None, rico_debtor_weight))
    yue_agenda.set_partyunit(partyunit_shop(carm_text, None, None, carm_debtor_weight))
    yue_agenda.set_partyunit(partyunit_shop(patr_text, None, None, patr_debtor_weight))
    assert yue_agenda._party_debtor_pool is None
    assert yue_agenda.is_partyunits_debtor_weight_sum_correct()
    assert yue_agenda.set_agenda_metrics() is None

    # WHEN
    x_int = 13
    yue_agenda.set_party_debtor_pool(x_int)
    assert yue_agenda.is_partyunits_debtor_weight_sum_correct() == False
    with pytest_raises(Exception) as excinfo:
        yue_agenda.set_agenda_metrics()
    assert (
        str(excinfo.value)
        == f"is_partyunits_debtor_weight_sum_correct is False. _party_debtor_pool={x_int}. partyunits_debtor_weight_sum={yue_agenda.get_partyunits_debtor_weight_sum()}"
    )

    # WHEN / THEN
    yue_agenda.set_party_debtor_pool(yue_agenda.get_partyunits_debtor_weight_sum())
    assert yue_agenda.set_agenda_metrics() is None


def clear_all_partyunits_groupunits_agenda_intent_credit_debt(x_agenda: AgendaUnit):
    # DELETE agenda_intent_debt and agenda_intent_credit
    for groupunit_x in x_agenda._groups.values():
        groupunit_x.reset_agenda_credit_debt()
        # for partylink_x in groupunit_x._partys.values():
        #     print(f"{groupunit_x.brand=} {partylink_x.creditor_weight=}  {partylink_x._agenda_credit:.6f} {partylink_x.debtor_weight=} {partylink_x._agenda_debt:.6f} {partylink_x.party_id=} ")

    # DELETE agenda_intent_debt and agenda_intent_credit
    for x_partyunit in x_agenda._partys.values():
        x_partyunit.reset_agenda_credit_debt()


@dataclass
class GroupIntentMetrics:
    sum_groupunit_credit: float = 0
    sum_groupunit_debt: float = 0
    sum_partylink_credit: float = 0
    sum_partylink_debt: float = 0
    partylink_count: int = 0

    def set_sums(self, x_agenda: AgendaUnit):
        for groupunit_x in x_agenda._groups.values():
            self.sum_groupunit_credit += groupunit_x._agenda_intent_credit
            self.sum_groupunit_debt += groupunit_x._agenda_intent_debt
            for partylink_x in groupunit_x._partys.values():
                self.sum_partylink_credit += partylink_x._agenda_intent_credit
                self.sum_partylink_debt += partylink_x._agenda_intent_debt
                self.partylink_count += 1


@dataclass
class PartyIntentMetrics:
    sum_intent_credit: float = 0
    sum_intent_debt: float = 0
    sum_intent_ratio_credit: float = 0
    sum_intent_ratio_debt: float = 0

    def set_sums(self, x_agenda: AgendaUnit):
        for partyunit in x_agenda._partys.values():
            self.sum_intent_credit += partyunit._agenda_intent_credit
            self.sum_intent_debt += partyunit._agenda_intent_debt
            self.sum_intent_ratio_credit += partyunit._agenda_intent_ratio_credit
            self.sum_intent_ratio_debt += partyunit._agenda_intent_ratio_debt


@dataclass
class BalanceIntentMetrics:
    sum_agenda_intent_importance = 0
    intent_no_count = 0
    intent_yes_count = 0
    intent_no_agenda_i_sum = 0
    intent_yes_agenda_i_sum = 0

    def set_sums(self, intent_dict: dict[RoadUnit:IdeaUnit]):
        for intent_item in intent_dict.values():
            self.sum_agenda_intent_importance += intent_item._agenda_importance
            if intent_item._balancelines == {}:
                self.intent_no_count += 1
                self.intent_no_agenda_i_sum += intent_item._agenda_importance
            else:
                self.intent_yes_count += 1
                self.intent_yes_agenda_i_sum += intent_item._agenda_importance


def test_AgendaUnit_intent_credit_debt_IsCorrectlySet():
    # GIVEN
    x_agenda = examples_agenda_v001_with_large_intent()
    clear_all_partyunits_groupunits_agenda_intent_credit_debt(x_agenda=x_agenda)

    # TEST agenda_intent_debt and agenda_intent_credit are empty
    x_groupintentmetrics = GroupIntentMetrics()
    x_groupintentmetrics.set_sums(x_agenda=x_agenda)
    assert x_groupintentmetrics.sum_groupunit_credit == 0
    assert x_groupintentmetrics.sum_groupunit_debt == 0
    assert x_groupintentmetrics.sum_partylink_credit == 0
    assert x_groupintentmetrics.sum_partylink_debt == 0

    # TEST agenda_intent_debt and agenda_intent_credit are empty
    x_partyintentmetrics = PartyIntentMetrics()
    x_partyintentmetrics.set_sums(x_agenda=x_agenda)
    assert x_partyintentmetrics.sum_intent_credit == 0
    assert x_partyintentmetrics.sum_intent_debt == 0
    assert x_partyintentmetrics.sum_intent_ratio_credit == 0
    assert x_partyintentmetrics.sum_intent_ratio_debt == 0

    # WHEN
    intent_dict = x_agenda.get_intent_dict()

    # THEN
    assert len(intent_dict) == 63
    x_balanceintentmetrics = BalanceIntentMetrics()
    x_balanceintentmetrics.set_sums(intent_dict=intent_dict)
    # print(f"{sum_agenda_intent_importance=}")
    assert x_balanceintentmetrics.intent_no_count == 14
    assert x_balanceintentmetrics.intent_yes_count == 49
    assert x_balanceintentmetrics.intent_no_agenda_i_sum == 0.0037472680016539662
    assert x_balanceintentmetrics.intent_yes_agenda_i_sum == 0.002796504989487445
    assert are_equal(
        x_balanceintentmetrics.intent_no_agenda_i_sum
        + x_balanceintentmetrics.intent_yes_agenda_i_sum,
        x_balanceintentmetrics.sum_agenda_intent_importance,
    )
    assert x_balanceintentmetrics.sum_agenda_intent_importance == 0.006543772991141412

    x_groupintentmetrics = GroupIntentMetrics()
    x_groupintentmetrics.set_sums(x_agenda=x_agenda)
    assert x_groupintentmetrics.partylink_count == 81
    x_sum = 0.002796504989487445
    assert x_groupintentmetrics.sum_groupunit_credit == x_sum
    assert x_groupintentmetrics.sum_groupunit_debt == x_sum
    assert x_groupintentmetrics.sum_partylink_credit == x_sum
    assert x_groupintentmetrics.sum_partylink_debt == x_sum
    assert are_equal(
        x_balanceintentmetrics.intent_yes_agenda_i_sum,
        x_groupintentmetrics.sum_groupunit_credit,
    )

    assert all_partyunits_have_legitimate_values(x_agenda)

    x_partyintentmetrics = PartyIntentMetrics()
    x_partyintentmetrics.set_sums(x_agenda=x_agenda)
    assert are_equal(
        x_partyintentmetrics.sum_intent_credit,
        x_balanceintentmetrics.sum_agenda_intent_importance,
    )
    assert are_equal(
        x_partyintentmetrics.sum_intent_debt,
        x_balanceintentmetrics.sum_agenda_intent_importance,
    )
    assert are_equal(x_partyintentmetrics.sum_intent_ratio_credit, 1)
    assert are_equal(x_partyintentmetrics.sum_intent_ratio_debt, 1)

    # partyunit_agenda_credit_sum = 0.0
    # partyunit_agenda_debt_sum = 0.0

    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def all_partyunits_have_legitimate_values(x_agenda: AgendaUnit):
    return not any(
        (
            partyunit._agenda_credit is None
            or partyunit._agenda_credit in [0.25, 0.5]
            or partyunit._agenda_debt is None
            or partyunit._agenda_debt in [0.8, 0.1]
        )
        for partyunit in x_agenda._partys.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000000001
    return abs(x1 - x2) < e10


def test_AgendaUnit_intent_ratio_credit_debt_IsCorrectlySetWhenAgendaIsEmpty():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_party = partyunit_shop(
        party_id=rico_text, creditor_weight=0.5, debtor_weight=2
    )
    carm_party = partyunit_shop(
        party_id=carm_text, creditor_weight=1.5, debtor_weight=3
    )
    patr_party = partyunit_shop(party_id=patr_text, creditor_weight=8, debtor_weight=5)
    noa_agenda.set_partyunit(partyunit=rico_party)
    noa_agenda.set_partyunit(partyunit=carm_party)
    noa_agenda.set_partyunit(partyunit=patr_party)
    noa_agenda_rico_party = noa_agenda._partys.get(rico_text)
    noa_agenda_carm_party = noa_agenda._partys.get(carm_text)
    noa_agenda_patr_party = noa_agenda._partys.get(patr_text)

    assert noa_agenda_rico_party._agenda_intent_credit in [0, None]
    assert noa_agenda_rico_party._agenda_intent_debt in [0, None]
    assert noa_agenda_carm_party._agenda_intent_credit in [0, None]
    assert noa_agenda_carm_party._agenda_intent_debt in [0, None]
    assert noa_agenda_patr_party._agenda_intent_credit in [0, None]
    assert noa_agenda_patr_party._agenda_intent_debt in [0, None]
    assert noa_agenda_rico_party._agenda_intent_ratio_credit != 0.05
    assert noa_agenda_rico_party._agenda_intent_ratio_debt != 0.2
    assert noa_agenda_carm_party._agenda_intent_ratio_credit != 0.15
    assert noa_agenda_carm_party._agenda_intent_ratio_debt != 0.3
    assert noa_agenda_patr_party._agenda_intent_ratio_credit != 0.8
    assert noa_agenda_patr_party._agenda_intent_ratio_debt != 0.5

    # WHEN
    noa_agenda.set_agenda_metrics()

    # THEN
    assert noa_agenda_rico_party._agenda_intent_credit == 0
    assert noa_agenda_rico_party._agenda_intent_debt == 0
    assert noa_agenda_carm_party._agenda_intent_credit == 0
    assert noa_agenda_carm_party._agenda_intent_debt == 0
    assert noa_agenda_patr_party._agenda_intent_credit == 0
    assert noa_agenda_patr_party._agenda_intent_debt == 0
    assert noa_agenda_rico_party._agenda_intent_ratio_credit == 0.05
    assert noa_agenda_rico_party._agenda_intent_ratio_debt == 0.2
    assert noa_agenda_carm_party._agenda_intent_ratio_credit == 0.15
    assert noa_agenda_carm_party._agenda_intent_ratio_debt == 0.3
    assert noa_agenda_patr_party._agenda_intent_ratio_credit == 0.8
    assert noa_agenda_patr_party._agenda_intent_ratio_debt == 0.5


def test_AgendaUnit_get_party_groupbrands_ReturnsCorrectObj():
    # GIVEN
    yao_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))

    # WHEN / THEN
    assert yao_agenda.get_party_groupbrands(party_id=carm_text) == [carm_text]

    # WHEN / THEN
    swimmers = "swimmers"
    swim_group = groupunit_shop(brand=swimmers)
    swim_group.set_partylink(partylink_shop(carm_text))
    yao_agenda.set_groupunit(swim_group)
    assert yao_agenda.get_party_groupbrands(party_id=carm_text) == [carm_text, swimmers]


def test_AgendaUnit_edit_partyunit_party_id_CorrectlyChangesPartyUnit_party_id():
    # GIVEN
    yao_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    yao_agenda.add_partyunit(party_id=rico_text, uid=61, creditor_weight=13)
    yao_agenda.add_partyunit(party_id="carmen", uid=5)
    yao_agenda.add_partyunit(party_id="patrick", creditor_weight=17)
    assert len(yao_agenda._partys) == 3
    assert yao_agenda._partys.get(rico_text) != None
    assert yao_agenda._partys.get(rico_text).creditor_weight == 13
    assert len(yao_agenda._groups) == 3
    assert yao_agenda.get_groupunit(rico_text) != None
    assert yao_agenda.get_groupunit(rico_text)._single_party == True

    # WHEN
    beto_text = "beta"
    yao_agenda.edit_partyunit_party_id(
        old_party_id=rico_text,
        new_party_id=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert yao_agenda._partys.get(beto_text) != None
    assert yao_agenda._partys.get(beto_text).creditor_weight == 13
    assert yao_agenda._partys.get(rico_text) is None
    assert len(yao_agenda._partys) == 3
    assert len(yao_agenda._groups) == 3
    assert yao_agenda.get_groupunit(rico_text) is None
    assert yao_agenda.get_groupunit(beto_text) != None
    assert yao_agenda.get_groupunit(beto_text)._single_party == True


def test_AgendaUnit_PartyUnit_raiseErrorNewparty_idPreviouslyExists():
    # GIVEN
    yao_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    yao_agenda.add_partyunit(party_id=rico_text, uid=61, creditor_weight=13)
    carmen_text = "carmen"
    yao_agenda.add_partyunit(party_id=carmen_text, uid=5)
    yao_agenda.add_partyunit(party_id="patrick", creditor_weight=17)
    assert len(yao_agenda._partys) == 3
    assert yao_agenda._partys.get(rico_text) != None
    assert yao_agenda._partys.get(rico_text).creditor_weight == 13
    assert len(yao_agenda._groups) == 3
    assert yao_agenda.get_groupunit(rico_text) != None
    assert yao_agenda.get_groupunit(rico_text)._single_party == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_partyunit_party_id(
            old_party_id=rico_text,
            new_party_id=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' change to '{carmen_text}' failed since '{carmen_text}' exists."
    )


def test_AgendaUnit_PartyUnit_CorrectlyChangesGroupUnitPartyLinks():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.add_partyunit(party_id=rico_text, uid=61, creditor_weight=13)
    yue_agenda.add_partyunit(party_id=carm_text, uid=5)
    yue_agenda.add_partyunit(party_id=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyID(carm_text): partylink_shop(party_id=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink_shop(carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink_shop(rico_text, creditor_weight=7, debtor_weight=30)
    )
    yue_agenda.set_groupunit(y_groupunit=swim_group)

    swim_group = yue_agenda.get_groupunit(swim_text)
    assert len(swim_group._partys) == 2
    assert swim_group.get_partylink(rico_text) != None
    assert swim_group.get_partylink(rico_text).creditor_weight == 7
    assert swim_group.get_partylink(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    yue_agenda.edit_partyunit_party_id(
        old_party_id=rico_text,
        new_party_id=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group.get_partylink(beto_text) != None
    assert swim_group.get_partylink(beto_text).creditor_weight == 7
    assert swim_group.get_partylink(beto_text).debtor_weight == 30
    assert swim_group.get_partylink(rico_text) is None
    assert len(swim_group._partys) == 2


def test_AgendaUnit_PartyUnit_CorrectlyMergesparty_ids():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.add_partyunit(party_id=rico_text, uid=61, creditor_weight=13)
    yue_agenda.add_partyunit(party_id=carm_text, uid=5, creditor_weight=3)
    yue_agenda.add_partyunit(party_id=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyID(carm_text): partylink_shop(party_id=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(rico_text, creditor_weight=7, debtor_weight=30)
    )
    yue_agenda.set_groupunit(y_groupunit=swim_group)

    assert len(yue_agenda._partys) == 3
    assert yue_agenda._partys.get(rico_text) != None
    assert yue_agenda._partys.get(rico_text).creditor_weight == 13
    assert yue_agenda._partys.get(carm_text) != None
    assert yue_agenda._partys.get(carm_text).creditor_weight == 3

    # WHEN / THEN
    yue_agenda.edit_partyunit_party_id(
        old_party_id=rico_text,
        new_party_id=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert yue_agenda._partys.get(carm_text) != None
    assert yue_agenda._partys.get(carm_text).creditor_weight == 16
    assert yue_agenda._partys.get(rico_text) is None
    assert len(yue_agenda._partys) == 2


def test_AgendaUnit_PartyUnit_CorrectlyMergesGroupUnitPartyLinks():
    # GIVEN
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.add_partyunit(party_id=rico_text, uid=61, creditor_weight=13)
    yue_agenda.add_partyunit(party_id=carm_text, uid=5)
    yue_agenda.add_partyunit(party_id=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyID(carm_text): partylink_shop(party_id=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(rico_text, creditor_weight=7, debtor_weight=30)
    )
    yue_agenda.set_groupunit(y_groupunit=swim_group)

    swim_group = yue_agenda.get_groupunit(swim_text)
    assert len(swim_group._partys) == 2
    assert swim_group.get_partylink(rico_text) != None
    assert swim_group.get_partylink(rico_text).creditor_weight == 7
    assert swim_group.get_partylink(rico_text).debtor_weight == 30
    assert swim_group.get_partylink(carm_text) != None
    assert swim_group.get_partylink(carm_text).creditor_weight == 5
    assert swim_group.get_partylink(carm_text).debtor_weight == 18

    # WHEN
    yue_agenda.edit_partyunit_party_id(
        old_party_id=rico_text,
        new_party_id=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group.get_partylink(carm_text) != None
    assert swim_group.get_partylink(carm_text).creditor_weight == 12
    assert swim_group.get_partylink(carm_text).debtor_weight == 48
    assert swim_group.get_partylink(rico_text) is None
    assert len(swim_group._partys) == 1


def test_AgendaUnit_PartyUnit_raiseErrorNewPIDGroupUnitPreviouslyExists():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    yue_agenda.add_partyunit(party_id=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    yue_agenda.add_partyunit(party_id=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(brand=carmen_text)
    carmen_group.set_partylink(partylink=partylink_shop(party_id=rico_text))
    carmen_group.set_partylink(partylink=partylink_shop(party_id=anna_text))
    yue_agenda.set_groupunit(y_groupunit=carmen_group)
    assert len(yue_agenda._groups) == 3
    assert yue_agenda._partys.get(carmen_text) is None
    assert yue_agenda.get_groupunit(carmen_text)._single_party == False
    assert len(yue_agenda.get_groupunit(carmen_text)._partys) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yue_agenda.edit_partyunit_party_id(
            old_party_id=rico_text,
            new_party_id=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' change to '{carmen_text}' failed since non-single group '{carmen_text}' exists."
    )


def test_AgendaUnit_PartyUnit_CorrectlyOverwriteNewPIDGroupUnit():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    yue_agenda.add_partyunit(party_id=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    yue_agenda.add_partyunit(party_id=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(brand=carmen_text)
    carmen_group.set_partylink(
        partylink=partylink_shop(party_id=rico_text, creditor_weight=3)
    )
    carmen_group.set_partylink(
        partylink=partylink_shop(party_id=anna_text, creditor_weight=5)
    )
    yue_agenda.set_groupunit(y_groupunit=carmen_group)
    assert len(yue_agenda._groups) == 3
    assert yue_agenda._partys.get(rico_text) != None
    assert yue_agenda._partys.get(carmen_text) is None
    assert yue_agenda.get_groupunit(carmen_text)._single_party == False
    assert len(yue_agenda.get_groupunit(carmen_text)._partys) == 2
    assert (
        yue_agenda.get_groupunit(carmen_text)._partys.get(anna_text).creditor_weight
        == 5
    )
    assert (
        yue_agenda.get_groupunit(carmen_text)._partys.get(rico_text).creditor_weight
        == 3
    )

    # WHEN
    yue_agenda.edit_partyunit_party_id(
        old_party_id=rico_text,
        new_party_id=carmen_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=True,
    )

    assert len(yue_agenda._groups) == 2
    assert yue_agenda._partys.get(rico_text) is None
    assert yue_agenda._partys.get(carmen_text) != None
    assert yue_agenda.get_groupunit(carmen_text)._single_party == True
    assert len(yue_agenda.get_groupunit(carmen_text)._partys) == 1
    assert yue_agenda.get_groupunit(carmen_text)._partys.get(rico_text) is None
    assert (
        yue_agenda.get_groupunit(carmen_text)._partys.get(carmen_text).creditor_weight
        == 1
    )


def test_AgendaUnit_set_all_partyunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    swim_text = "swim"
    run_text = "run"
    fly_text = "fly"
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=swim_text))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=run_text))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=fly_text))
    assert noa_agenda._partys[swim_text].uid is None
    assert noa_agenda._partys[run_text].uid is None
    assert noa_agenda._partys[fly_text].uid is None

    # WHEN
    noa_agenda.set_all_partyunits_uids_unique()

    # THEN
    assert noa_agenda._partys[swim_text].uid != None
    assert noa_agenda._partys[run_text].uid != None
    assert noa_agenda._partys[fly_text].uid != None


def test_AgendaUnit_set_all_partyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    swim_text = "swim"
    run_text = "run"
    fly_text = "fly"
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=swim_text, uid=3))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=run_text, uid=3))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=fly_text))
    assert noa_agenda._partys[swim_text].uid == 3
    assert noa_agenda._partys[run_text].uid == 3
    assert noa_agenda._partys[fly_text].uid is None

    # WHEN
    noa_agenda.set_all_partyunits_uids_unique()

    # THEN
    print(f"{noa_agenda._partys[swim_text].uid=}")
    print(f"{noa_agenda._partys[run_text].uid=}")
    assert noa_agenda._partys[swim_text].uid != noa_agenda._partys[run_text].uid
    assert noa_agenda._partys[run_text].uid != 3
    assert noa_agenda._partys[run_text].uid != 3
    assert noa_agenda._partys[fly_text].uid != None


def test_AgendaUnit_set_all_partyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    swim_text = "swim"
    run_text = "run"
    fly_text = "fly"
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=swim_text, uid=3))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=run_text, uid=3))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=fly_text))
    assert noa_agenda._partys[swim_text].uid == 3
    assert noa_agenda._partys[run_text].uid == 3
    assert noa_agenda._partys[fly_text].uid is None

    # WHEN
    noa_agenda.set_all_partyunits_uids_unique()

    # THEN
    print(f"{noa_agenda._partys[swim_text].uid=}")
    print(f"{noa_agenda._partys[run_text].uid=}")
    assert noa_agenda._partys[swim_text].uid != noa_agenda._partys[run_text].uid
    assert noa_agenda._partys[run_text].uid != 3
    assert noa_agenda._partys[run_text].uid != 3
    assert noa_agenda._partys[fly_text].uid != None


def test_AgendaUnit_all_partyunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    swim_text = "swim"
    run_text = "run"
    fly_text = "fly"
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=swim_text, uid=3))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=run_text, uid=3))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=fly_text))
    assert noa_agenda._partys[swim_text].uid == 3
    assert noa_agenda._partys[run_text].uid == 3
    assert noa_agenda._partys[fly_text].uid is None

    # WHEN1 / THEN
    assert noa_agenda.all_partyunits_uids_are_unique() == False

    # WHEN2
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=swim_text, uid=4))

    # THEN
    assert noa_agenda.all_partyunits_uids_are_unique() == False

    # WHEN3
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=fly_text, uid=5))

    # THEN
    assert noa_agenda.all_partyunits_uids_are_unique()


def test_AgendaUnit_get_partyunits_party_id_list_CorrectlyReturnsListOfPartyUnits():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=sam_text))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=will_text))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(party_id=fry_text))
    fun_text = "fun people"
    fun_group = groupunit_shop(brand=fun_text)
    fun_group.set_partylink(partylink=partylink_shop(party_id=will_text))
    noa_agenda.set_groupunit(y_groupunit=fun_group)
    assert len(noa_agenda._groups) == 4
    assert len(noa_agenda._partys) == 3

    # WHEN
    partyunit_list_x = noa_agenda.get_partyunits_party_id_list()

    # THEN
    assert len(partyunit_list_x) == 4
    assert partyunit_list_x[0] == ""
    assert partyunit_list_x[1] == fry_text
    assert partyunit_list_x[2] == sam_text
    assert partyunit_list_x[3] == will_text


def test_get_intersection_of_partys_CorrectlyReturnsUnionOfKeysOfTwoDictionarys_scenario1():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text)

    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    bob_agenda.set_partyunit(partyunit=partyunit_shop(party_id=bob_text))
    bob_agenda.set_partyunit(partyunit=partyunit_shop(party_id=sam_text))
    bob_agenda.set_partyunit(partyunit=partyunit_shop(party_id=wil_text))
    bob_agenda.set_partyunit(partyunit=partyunit_shop(party_id=fry_text))

    y_agenda = agendaunit_shop()
    y_agenda.set_partyunit(partyunit=partyunit_shop(party_id=bob_text))
    y_agenda.set_partyunit(partyunit=partyunit_shop(party_id=wil_text))
    y_agenda.set_partyunit(partyunit=partyunit_shop(party_id=fry_text))
    y_agenda.set_partyunit(partyunit=partyunit_shop(party_id=elu_text))

    # WHEN
    print(f"{len(bob_agenda._partys)=} {len(y_agenda._partys)=}")
    intersection_x = get_intersection_of_partys(bob_agenda._partys, y_agenda._partys)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}


def test_AgendaUnit_clear_output_agenda_meld_orders_CorrectlyClearsAttrs():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    rico_partyunit = yue_agenda.get_party(rico_text)
    carm_partyunit = yue_agenda.get_party(carm_text)
    patr_partyunit = yue_agenda.get_party(patr_text)
    rico_partyunit.set_output_agenda_meld_order(3)
    carm_partyunit.set_output_agenda_meld_order(4)
    patr_partyunit.set_output_agenda_meld_order(5)

    assert rico_partyunit._output_agenda_meld_order != None
    assert carm_partyunit._output_agenda_meld_order != None
    assert patr_partyunit._output_agenda_meld_order != None

    # WHEN
    yue_agenda.clear_partys_output_agenda_meld_order()

    # THEN
    assert rico_partyunit._output_agenda_meld_order is None
    assert carm_partyunit._output_agenda_meld_order is None
    assert patr_partyunit._output_agenda_meld_order is None


def test_AgendaUnit_clear_output_agenda_meld_orders_WithNoArgsCorrectlySetOrder():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    yue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    rico_partyunit = yue_agenda.get_party(rico_text)
    carm_partyunit = yue_agenda.get_party(carm_text)
    patr_partyunit = yue_agenda.get_party(patr_text)
    assert rico_partyunit._output_agenda_meld_order is None
    assert carm_partyunit._output_agenda_meld_order is None
    assert patr_partyunit._output_agenda_meld_order is None

    # WHEN
    yue_agenda.set_partys_output_agenda_meld_order()

    # THEN
    assert rico_partyunit._output_agenda_meld_order != None
    assert carm_partyunit._output_agenda_meld_order != None
    assert patr_partyunit._output_agenda_meld_order != None
    print(f"{rico_partyunit._output_agenda_meld_order=}")
    print(f"{carm_partyunit._output_agenda_meld_order=}")
    print(f"{patr_partyunit._output_agenda_meld_order=}")
    assert rico_partyunit._output_agenda_meld_order == 2
    assert carm_partyunit._output_agenda_meld_order == 0
    assert patr_partyunit._output_agenda_meld_order == 1


def test_AgendaUnit_is_partyunits_creditor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_creditor_weight = 20
    carm_creditor_weight = 30
    patr_creditor_weight = 50
    yue_agenda.set_partyunit(partyunit_shop(rico_text, None, rico_creditor_weight))
    yue_agenda.set_partyunit(partyunit_shop(carm_text, None, carm_creditor_weight))
    yue_agenda.set_partyunit(partyunit_shop(patr_text, None, patr_creditor_weight))

    # WHEN / THEN
    assert yue_agenda.is_partyunits_creditor_weight_sum_correct()
    yue_agenda.set_party_creditor_pool(13)
    assert yue_agenda.is_partyunits_creditor_weight_sum_correct() == False
    # WHEN / THEN
    yue_party_credit_pool = (
        rico_creditor_weight + carm_creditor_weight + patr_creditor_weight
    )
    yue_agenda.set_party_creditor_pool(yue_party_credit_pool)
    assert yue_agenda.is_partyunits_creditor_weight_sum_correct()


def test_AgendaUnit_is_partyunits_debtor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yue_agenda = agendaunit_shop("Yue")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 60
    yue_agenda.set_partyunit(partyunit_shop(rico_text, None, None, rico_debtor_weight))
    yue_agenda.set_partyunit(partyunit_shop(carm_text, None, None, carm_debtor_weight))
    yue_agenda.set_partyunit(partyunit_shop(patr_text, None, None, patr_debtor_weight))

    # WHEN / THEN
    yue_party_debt_pool = rico_debtor_weight + carm_debtor_weight + patr_debtor_weight
    assert yue_agenda.is_partyunits_debtor_weight_sum_correct()
    yue_agenda.set_party_debtor_pool(yue_party_debt_pool + 1)
    assert yue_agenda.is_partyunits_debtor_weight_sum_correct() == False
    # WHEN / THEN
    yue_agenda.set_party_debtor_pool(yue_party_debt_pool)
    assert yue_agenda.is_partyunits_debtor_weight_sum_correct()
