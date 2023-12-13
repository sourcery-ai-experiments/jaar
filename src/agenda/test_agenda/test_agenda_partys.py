from src.agenda.party import PartyPID, partylink_shop, partyunit_shop
from src.agenda.group import GroupBrand, groupunit_shop, balancelink_shop
from src.agenda.examples.example_agendas import (
    agenda_v001 as examples_agenda_v001,
    agenda_v001_with_large_intent as examples_agenda_v001_with_large_intent,
)
from src.agenda.agenda import AgendaUnit, agendaunit_shop, get_intersection_of_partys
from src.agenda.idea import ideacore_shop
from pytest import raises as pytest_raises


def test_agenda_partys_exists():
    # GIVEN / WHEN
    x_agenda = agendaunit_shop()

    # THEN
    assert x_agenda._partys is None

    # GIVEN
    yahri_party = partyunit_shop(pid=PartyPID("yahri"))
    partys_x = {yahri_party.pid: yahri_party}
    x_agenda2 = agendaunit_shop()

    # WHEN
    x_agenda2.set_partyunit(partyunit=yahri_party)

    # THEN
    assert x_agenda2._partys == partys_x


def test_example_has_partys():
    # GIVEN / WHEN
    x_agenda = examples_agenda_v001()

    # THEN
    assert x_agenda._partys != None
    assert len(x_agenda._partys) == 22


def test_agenda_set_party_correctly_sets_partys_1():
    # GIVEN
    x_agenda = agendaunit_shop(_healer="prom")
    x_agenda.set_agenda_metrics()
    assert len(x_agenda._partys) == 0
    assert len(x_agenda._groups) == 0

    # WHEN
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID("rico")))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID("carmen")))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID("patrick")))

    # THEN
    assert len(x_agenda._partys) == 3
    assert len(x_agenda._groups) == 3
    assert x_agenda._groups["rico"]._single_party == True

    # WHEN
    x_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand("rico"), creditor_weight=10)
    )
    x_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand("carmen"), creditor_weight=10)
    )
    x_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand("patrick"), creditor_weight=10)
    )
    assert len(x_agenda._idearoot._balancelinks) == 3


def test_agenda_set_party_correctly_sets_partys_2():
    # GIVEN
    x_agenda = agendaunit_shop(_healer="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    assign_text = "assignment"

    # WHEN
    x_agenda.add_partyunit(pid=rico_text, uid=61, creditor_weight=13, debtor_weight=8)
    x_agenda.add_partyunit(pid=carm_text, uid=5, debtor_weight=5)
    x_agenda.add_partyunit(
        pid=patr_text, creditor_weight=17, depotlink_type=assign_text
    )

    # THEN
    assert len(x_agenda._partys) == 3
    assert len(x_agenda._groups) == 3
    assert x_agenda._groups.get(rico_text)._single_party == True
    assert x_agenda._partys.get(patr_text).creditor_weight == 17
    assert x_agenda._partys.get(carm_text).debtor_weight == 5
    assert x_agenda._partys.get(patr_text).depotlink_type == assign_text


def test_agenda_get_party_CorrectlyGetsParty():
    # GIVEN
    x_agenda = agendaunit_shop(_healer="prom")
    rico_text = "rico"
    carm_text = "carmen"
    x_agenda.add_partyunit(pid=rico_text)
    x_agenda.add_partyunit(pid=carm_text)

    # WHEN
    rico_party = x_agenda.get_party(rico_text)
    carm_party = x_agenda.get_party(carm_text)

    # THEN
    assert rico_party == x_agenda._partys.get(rico_text)
    assert carm_party == x_agenda._partys.get(carm_text)


def test_agenda_get_partys_depotlink_count_GetsCorrectCount():
    # GIVEN
    sue_text = "sue"
    sue_x_agenda = agendaunit_shop(_healer=sue_text)
    assign_text = "assignment"

    # WHEN
    rico_text = "rico"
    carm_text = "carmen"
    sue_x_agenda.add_partyunit(pid=rico_text)
    sue_x_agenda.add_partyunit(pid=carm_text)
    # THEN
    assert len(sue_x_agenda._partys) == 2
    assert sue_x_agenda.get_partys_depotlink_count() == 0

    # WHEN
    patr_text = "patrick"
    sue_x_agenda.add_partyunit(pid=patr_text, depotlink_type=assign_text)
    # THEN
    assert len(sue_x_agenda._partys) == 3
    assert sue_x_agenda.get_partys_depotlink_count() == 1

    # WHEN
    rico_party = sue_x_agenda.get_party(rico_text)
    rico_party.set_depotlink_type(assign_text)
    # THEN
    assert len(sue_x_agenda._partys) == 3
    assert sue_x_agenda.get_partys_depotlink_count() == 2


def test_agenda_get_idea_list_CorrectlySetsPartyLinkAgendaCreditAndDebt():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    bl_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    x_agenda._idearoot.set_balancelink(balancelink=bl_rico)
    x_agenda._idearoot.set_balancelink(balancelink=bl_carm)
    x_agenda._idearoot.set_balancelink(balancelink=bl_patr)

    rico_groupunit = x_agenda._groups.get(rico_text)
    carm_groupunit = x_agenda._groups.get(carm_text)
    patr_groupunit = x_agenda._groups.get(patr_text)
    rico_partylink = rico_groupunit._partys.get(rico_text)
    carm_partylink = carm_groupunit._partys.get(carm_text)
    patr_partylink = patr_groupunit._partys.get(patr_text)
    rico_partylink._agenda_credit is None
    rico_partylink._agenda_debt is None
    carm_partylink._agenda_credit is None
    carm_partylink._agenda_debt is None
    patr_partylink._agenda_credit is None
    patr_partylink._agenda_debt is None

    # for group in x_agenda._groups.values():
    #     for partylink in group._partys.values():
    #         assert partylink._agenda_credit is None
    #         assert partylink._agenda_debt is None

    x_agenda.set_agenda_metrics()

    # for balancelink in x_agenda._balanceheirs.values():
    #     print(
    #         f"{x_agenda._agenda_importance=} {balancelink.brand=} {balancelink._agenda_credit=} {balancelink._agenda_debt=}"
    #     )

    assert rico_partylink._agenda_credit == 0.5
    assert rico_partylink._agenda_debt == 0.8
    assert carm_partylink._agenda_credit == 0.25
    assert carm_partylink._agenda_debt == 0.1
    assert patr_partylink._agenda_credit == 0.25
    assert patr_partylink._agenda_debt == 0.1

    # partylink_agenda_credit_sum = 0.0
    # partylink_agenda_debt_sum = 0.0
    # for group in x_agenda._groups.values():
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

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(selena_text)))
    x_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            brand=GroupBrand(selena_text), creditor_weight=20, debtor_weight=13
        )
    )
    x_agenda.set_agenda_metrics()

    # THEN
    selena_groupunit = x_agenda._groups.get(selena_text)
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

    # for group in x_agenda._groups.values():
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


def test_agenda_get_idea_list_CorrectlySetsPartyUnitAgendaImportance():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(_healer=prom_text)
    swim_text = "swim"
    x_agenda.add_idea(ideacore_shop(_label=swim_text), pad=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    bl_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=bl_rico)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=bl_carm)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=bl_patr)

    rico_partyunit = x_agenda._partys.get(rico_text)
    carm_partyunit = x_agenda._partys.get(carm_text)
    patr_partyunit = x_agenda._partys.get(patr_text)

    assert rico_partyunit._agenda_credit is None
    assert rico_partyunit._agenda_debt is None
    assert carm_partyunit._agenda_credit is None
    assert carm_partyunit._agenda_debt is None
    assert patr_partyunit._agenda_credit is None
    assert patr_partyunit._agenda_debt is None

    # WHEN
    x_agenda.set_agenda_metrics()

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

    # for partyunit in x_agenda._partys.values():
    #     assert partyunit._agenda_credit != None
    #     assert partyunit._agenda_credit in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._agenda_creditor=} {group._agenda_creditor=}"
    #     # )
    #     print(f"{partyunit.pid=} {partyunit._agenda_credit=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_credit_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_credit_sum += partyunit._agenda_credit
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt

    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(selena_text)))
    x_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            brand=selena_text, creditor_weight=20, debtor_weight=10
        )
    )
    x_agenda.set_agenda_metrics()

    # THEN
    selena_partyunit = x_agenda._partys.get(selena_text)

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

    # for partyunit in x_agenda._partys.values():
    #     assert partyunit._agenda_credit != None
    #     assert partyunit._agenda_credit not in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._agenda_creditor=} {group._agenda_creditor=}"
    #     # )
    #     print(f"{partyunit.pid=} {partyunit._agenda_credit=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_credit_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_credit_sum += partyunit._agenda_credit
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt

    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def test_agenda_get_idea_list_CorrectlySetsPartGroupedLWPartyUnitAgendaImportance():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(_healer=prom_text)
    swim_text = "swim"
    x_agenda.add_idea(ideacore_shop(_label=swim_text), pad=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    bl_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(brand=patr_text, creditor_weight=10, debtor_weight=5)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=bl_rico)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=bl_carm)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=bl_patr)

    # no balancelinks attached to this one
    hunt_text = "hunt"
    x_agenda.add_idea(
        idea_kid=ideacore_shop(_label=hunt_text, _weight=3), pad=prom_text
    )

    assert x_agenda._idearoot._balancelinks is None

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    rico_groupunit = x_agenda._groups.get(rico_text)
    carm_groupunit = x_agenda._groups.get(carm_text)
    patr_groupunit = x_agenda._groups.get(patr_text)
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
    # for groupunit in x_agenda._groups.values():
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

    rico_partyunit = x_agenda._partys.get(rico_text)
    carm_partyunit = x_agenda._partys.get(carm_text)
    patr_partyunit = x_agenda._partys.get(patr_text)

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
    # for partyunit in x_agenda._partys.values():
    #     assert partyunit._agenda_credit != None
    #     assert partyunit._agenda_credit not in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._agenda_creditor=} {group._agenda_creditor=}"
    #     # )
    #     print(f"{partyunit.pid=} {partyunit._agenda_credit=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_credit_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_credit_sum += partyunit._agenda_credit
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt
    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def test_agenda_get_idea_list_WithAllPartysWeighted():
    # GIVEN
    x_agenda = agendaunit_shop(_healer="prom")
    x_agenda.add_idea(ideacore_shop(_label="swim"), pad="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(
        partyunit=partyunit_shop(pid=PartyPID(rico_text), creditor_weight=8)
    )
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    rico_partyunit = x_agenda._partys.get(rico_text)
    carm_partyunit = x_agenda._partys.get(carm_text)
    patr_partyunit = x_agenda._partys.get(patr_text)
    assert rico_partyunit._agenda_credit is None
    assert rico_partyunit._agenda_debt is None
    assert carm_partyunit._agenda_credit is None
    assert carm_partyunit._agenda_debt is None
    assert patr_partyunit._agenda_credit is None
    assert patr_partyunit._agenda_debt is None

    # WHEN
    x_agenda.set_agenda_metrics()

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
    # for partyunit in x_agenda._partys.values():
    #     assert partyunit._agenda_credit != None
    #     assert partyunit._agenda_credit not in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.brand=} {partyunit._agenda_creditor=} {group._agenda_creditor=}"
    #     # )
    #     print(f"{partyunit.pid=} {partyunit._agenda_credit=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_credit_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_credit_sum += partyunit._agenda_credit
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt
    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def clear_all_partyunits_groupunits_agenda_intent_credit_debt(x_agenda: AgendaUnit):
    # DELETE agenda_intent_debt and agenda_intent_credit
    for groupunit_x in x_agenda._groups.values():
        groupunit_x.reset_agenda_credit_debt()
        # for partylink_x in groupunit_x._partys.values():
        #     print(f"{groupunit_x.brand=} {partylink_x.creditor_weight=}  {partylink_x._agenda_credit:.6f} {partylink_x.debtor_weight=} {partylink_x._agenda_debt:.6f} {partylink_x.pid=} ")

    # DELETE agenda_intent_debt and agenda_intent_credit
    for x_partyunit in x_agenda._partys.values():
        x_partyunit.reset_agenda_credit_debt()


# sourcery skip: no-loop-in-tests
# sourcery skip: no-conditionals-in-tests
def test_agenda_intent_credit_debt_IsCorrectlySet():
    # GIVEN
    x_agenda = examples_agenda_v001_with_large_intent()
    clear_all_partyunits_groupunits_agenda_intent_credit_debt(x_agenda=x_agenda)

    # TEST agenda_intent_debt and agenda_intent_credit are empty
    sum_groupunit_agenda_intent_credit = 0
    sum_groupunit_agenda_intent_debt = 0
    sum_partylink_agenda_intent_credit = 0
    sum_partylink_agenda_intent_debt = 0
    for groupunit_x in x_agenda._groups.values():
        # print(f"{partyunit.pid=}")
        sum_groupunit_agenda_intent_credit += groupunit_x._agenda_intent_credit
        sum_groupunit_agenda_intent_debt += groupunit_x._agenda_intent_debt
        for partylink_x in groupunit_x._partys.values():
            sum_partylink_agenda_intent_credit += partylink_x._agenda_intent_credit
            sum_partylink_agenda_intent_debt += partylink_x._agenda_intent_debt

    assert sum_groupunit_agenda_intent_credit == 0
    assert sum_groupunit_agenda_intent_debt == 0
    assert sum_partylink_agenda_intent_credit == 0
    assert sum_partylink_agenda_intent_debt == 0

    # TEST agenda_intent_debt and agenda_intent_credit are empty
    sum_partyunit_agenda_intent_credit = 0
    sum_partyunit_agenda_intent_debt = 0
    sum_partyunit_agenda_intent_ratio_credit = 0
    sum_partyunit_agenda_intent_ratio_debt = 0
    for partyunit in x_agenda._partys.values():
        # print(f"{partyunit.pid=}")
        sum_partyunit_agenda_intent_credit += partyunit._agenda_intent_credit
        sum_partyunit_agenda_intent_debt += partyunit._agenda_intent_debt
        sum_partyunit_agenda_intent_ratio_credit += (
            partyunit._agenda_intent_ratio_credit
        )
        sum_partyunit_agenda_intent_ratio_debt += partyunit._agenda_intent_ratio_debt

    assert sum_partyunit_agenda_intent_credit == 0
    assert sum_partyunit_agenda_intent_debt == 0
    assert sum_partyunit_agenda_intent_ratio_credit == 0
    assert sum_partyunit_agenda_intent_ratio_debt == 0

    # WHEN
    intent_list = x_agenda.get_intent_items()

    # THEN
    assert len(intent_list) == 68
    sum_agenda_intent_importance = 0
    intent_no_balancelines_count = 0
    intent_yes_balancelines_count = 0
    intent_no_balancelines_agenda_i_sum = 0
    intent_yes_balancelines_agenda_i_sum = 0
    for intent_item in intent_list:
        sum_agenda_intent_importance += intent_item._agenda_importance
        if intent_item._balancelines == {}:
            intent_no_balancelines_count += 1
            intent_no_balancelines_agenda_i_sum += intent_item._agenda_importance
        else:
            intent_yes_balancelines_count += 1
            intent_yes_balancelines_agenda_i_sum += intent_item._agenda_importance
        # print(f"idea importance: {intent_item._agenda_importance:.7f} {sum_agenda_intent_importance:.5f} {intent_item._label=} ")
        # print(f"{intent_item.get_road()}")
    print(f"{sum_agenda_intent_importance=}")
    assert intent_no_balancelines_count == 20
    assert intent_yes_balancelines_count == 48
    assert intent_no_balancelines_agenda_i_sum == 0.00447826215370075
    assert intent_yes_balancelines_agenda_i_sum == 0.0027152834170378025
    x2 = intent_no_balancelines_agenda_i_sum + intent_yes_balancelines_agenda_i_sum
    e10 = 0.0000000001
    assert abs(x2 - sum_agenda_intent_importance) < e10

    assert sum_agenda_intent_importance == 0.007193545570738553

    sum_groupunit_agenda_intent_credit = 0
    sum_groupunit_agenda_intent_debt = 0
    sum_partylink_agenda_intent_credit = 0
    sum_partylink_agenda_intent_debt = 0
    partylink_count = 0
    for groupunit_x in x_agenda._groups.values():
        # print(f"{partyunit.pid=}")
        sum_groupunit_agenda_intent_credit += groupunit_x._agenda_intent_credit
        sum_groupunit_agenda_intent_debt += groupunit_x._agenda_intent_debt
        for partylink_x in groupunit_x._partys.values():
            sum_partylink_agenda_intent_credit += partylink_x._agenda_intent_credit
            sum_partylink_agenda_intent_debt += partylink_x._agenda_intent_debt
            partylink_count += 1

    assert partylink_count == 81
    x_sum = 0.0027152834170378025
    assert sum_groupunit_agenda_intent_credit == x_sum
    assert sum_groupunit_agenda_intent_debt == x_sum
    assert sum_partylink_agenda_intent_credit == x_sum
    assert sum_partylink_agenda_intent_debt == x_sum
    assert (
        abs(intent_yes_balancelines_agenda_i_sum - sum_groupunit_agenda_intent_credit)
        < e10
    )

    sum_partyunit_agenda_intent_credit = 0
    sum_partyunit_agenda_intent_debt = 0
    sum_partyunit_agenda_intent_ratio_credit = 0
    sum_partyunit_agenda_intent_ratio_debt = 0
    for partyunit in x_agenda._partys.values():
        assert partyunit._agenda_credit != None
        assert partyunit._agenda_credit not in [0.25, 0.5]
        assert partyunit._agenda_debt != None
        assert partyunit._agenda_debt not in [
            0.8,
            0.1,
        ]  # print(f"{partyunit.pid=}")
        sum_partyunit_agenda_intent_credit += partyunit._agenda_intent_credit
        sum_partyunit_agenda_intent_debt += partyunit._agenda_intent_debt
        sum_partyunit_agenda_intent_ratio_credit += (
            partyunit._agenda_intent_ratio_credit
        )
        sum_partyunit_agenda_intent_ratio_debt += partyunit._agenda_intent_ratio_debt

    assert abs(sum_partyunit_agenda_intent_credit - sum_agenda_intent_importance) < e10
    assert abs(sum_partyunit_agenda_intent_debt - sum_agenda_intent_importance) < e10
    assert abs(sum_partyunit_agenda_intent_ratio_credit - 1) < e10
    assert abs(sum_partyunit_agenda_intent_ratio_debt - 1) < e10

    # partyunit_agenda_credit_sum = 0.0
    # partyunit_agenda_debt_sum = 0.0

    # assert partyunit_agenda_credit_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def test_agenda_intent_ratio_credit_debt_IsCorrectlySetWhenAgendaIsEmpty():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_party = partyunit_shop(pid=rico_text, creditor_weight=0.5, debtor_weight=2)
    carm_party = partyunit_shop(pid=carm_text, creditor_weight=1.5, debtor_weight=3)
    patr_party = partyunit_shop(pid=patr_text, creditor_weight=8, debtor_weight=5)
    x_agenda.set_partyunit(partyunit=rico_party)
    x_agenda.set_partyunit(partyunit=carm_party)
    x_agenda.set_partyunit(partyunit=patr_party)
    x_agenda_rico_party = x_agenda._partys.get(rico_text)
    x_agenda_carm_party = x_agenda._partys.get(carm_text)
    x_agenda_patr_party = x_agenda._partys.get(patr_text)

    assert x_agenda_rico_party._agenda_intent_credit in [0, None]
    assert x_agenda_rico_party._agenda_intent_debt in [0, None]
    assert x_agenda_carm_party._agenda_intent_credit in [0, None]
    assert x_agenda_carm_party._agenda_intent_debt in [0, None]
    assert x_agenda_patr_party._agenda_intent_credit in [0, None]
    assert x_agenda_patr_party._agenda_intent_debt in [0, None]
    assert x_agenda_rico_party._agenda_intent_ratio_credit != 0.05
    assert x_agenda_rico_party._agenda_intent_ratio_debt != 0.2
    assert x_agenda_carm_party._agenda_intent_ratio_credit != 0.15
    assert x_agenda_carm_party._agenda_intent_ratio_debt != 0.3
    assert x_agenda_patr_party._agenda_intent_ratio_credit != 0.8
    assert x_agenda_patr_party._agenda_intent_ratio_debt != 0.5

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert x_agenda_rico_party._agenda_intent_credit == 0
    assert x_agenda_rico_party._agenda_intent_debt == 0
    assert x_agenda_carm_party._agenda_intent_credit == 0
    assert x_agenda_carm_party._agenda_intent_debt == 0
    assert x_agenda_patr_party._agenda_intent_credit == 0
    assert x_agenda_patr_party._agenda_intent_debt == 0
    assert x_agenda_rico_party._agenda_intent_ratio_credit == 0.05
    assert x_agenda_rico_party._agenda_intent_ratio_debt == 0.2
    assert x_agenda_carm_party._agenda_intent_ratio_credit == 0.15
    assert x_agenda_carm_party._agenda_intent_ratio_debt == 0.3
    assert x_agenda_patr_party._agenda_intent_ratio_credit == 0.8
    assert x_agenda_patr_party._agenda_intent_ratio_debt == 0.5


def test_agenda_get_party_groups_returnsCorrectData():
    x_agenda = agendaunit_shop(_healer="prom")
    x_agenda.add_idea(ideacore_shop(_label="swim"), pad="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))

    carmen_group_list = x_agenda.get_party_groups(party_pid=carm_text)
    assert carmen_group_list == [carm_text]

    swimmers = "swimmers"
    carmen_party_dict = {PartyPID(carm_text): partylink_shop(pid=carm_text)}
    swim_group = groupunit_shop(brand=swimmers, _partys=carmen_party_dict)
    x_agenda._groups[swim_group.brand] = swim_group
    carmen_group_list = x_agenda.get_party_groups(party_pid=carm_text)
    assert carmen_group_list == [carm_text, swimmers]


def test_agenda_PartyUnit_CorrectlyCreatesNewPID():
    # GIVEN
    x_agenda = agendaunit_shop(_healer="prom")
    rico_text = "rico"
    x_agenda.add_partyunit(pid=rico_text, uid=61, creditor_weight=13)
    x_agenda.add_partyunit(pid="carmen", uid=5)
    x_agenda.add_partyunit(pid="patrick", creditor_weight=17)
    assert len(x_agenda._partys) == 3
    assert x_agenda._partys.get(rico_text) != None
    assert x_agenda._partys.get(rico_text).creditor_weight == 13
    assert len(x_agenda._groups) == 3
    assert x_agenda._groups.get(rico_text) != None
    assert x_agenda._groups.get(rico_text)._single_party == True

    # WHEN
    beto_text = "beta"
    x_agenda.edit_partyunit_pid(
        old_pid=rico_text,
        new_pid=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert x_agenda._partys.get(beto_text) != None
    assert x_agenda._partys.get(beto_text).creditor_weight == 13
    assert x_agenda._partys.get(rico_text) is None
    assert len(x_agenda._partys) == 3
    assert len(x_agenda._groups) == 3
    assert x_agenda._groups.get(rico_text) is None
    assert x_agenda._groups.get(beto_text) != None
    assert x_agenda._groups.get(beto_text)._single_party == True


def test_agenda_PartyUnit_raiseErrorNewPIDPreviouslyExists():
    # GIVEN
    x_agenda = agendaunit_shop(_healer="prom")
    rico_text = "rico"
    x_agenda.add_partyunit(pid=rico_text, uid=61, creditor_weight=13)
    carmen_text = "carmen"
    x_agenda.add_partyunit(pid=carmen_text, uid=5)
    x_agenda.add_partyunit(pid="patrick", creditor_weight=17)
    assert len(x_agenda._partys) == 3
    assert x_agenda._partys.get(rico_text) != None
    assert x_agenda._partys.get(rico_text).creditor_weight == 13
    assert len(x_agenda._groups) == 3
    assert x_agenda._groups.get(rico_text) != None
    assert x_agenda._groups.get(rico_text)._single_party == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_partyunit_pid(
            old_pid=rico_text,
            new_pid=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' change to '{carmen_text}' failed since '{carmen_text}' exists."
    )


def test_agenda_PartyUnit_CorrectlyChangesGroupUnitPartyLinks():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.add_partyunit(pid=rico_text, uid=61, creditor_weight=13)
    x_agenda.add_partyunit(pid=carm_text, uid=5)
    x_agenda.add_partyunit(pid=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyPID(carm_text): partylink_shop(pid=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(pid=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(pid=rico_text, creditor_weight=7, debtor_weight=30)
    )
    x_agenda.set_groupunit(groupunit=swim_group)

    swim_group = x_agenda._groups.get(swim_text)
    assert len(swim_group._partys) == 2
    assert swim_group._partys.get(rico_text) != None
    assert swim_group._partys.get(rico_text).creditor_weight == 7
    assert swim_group._partys.get(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    x_agenda.edit_partyunit_pid(
        old_pid=rico_text,
        new_pid=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._partys.get(beto_text) != None
    assert swim_group._partys.get(beto_text).creditor_weight == 7
    assert swim_group._partys.get(beto_text).debtor_weight == 30
    assert swim_group._partys.get(rico_text) is None
    assert len(swim_group._partys) == 2


def test_agenda_PartyUnit_CorrectlyMergesPIDs():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.add_partyunit(pid=rico_text, uid=61, creditor_weight=13)
    x_agenda.add_partyunit(pid=carm_text, uid=5, creditor_weight=3)
    x_agenda.add_partyunit(pid=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyPID(carm_text): partylink_shop(pid=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(pid=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(pid=rico_text, creditor_weight=7, debtor_weight=30)
    )
    x_agenda.set_groupunit(groupunit=swim_group)

    assert len(x_agenda._partys) == 3
    assert x_agenda._partys.get(rico_text) != None
    assert x_agenda._partys.get(rico_text).creditor_weight == 13
    assert x_agenda._partys.get(carm_text) != None
    assert x_agenda._partys.get(carm_text).creditor_weight == 3

    # WHEN / THEN
    x_agenda.edit_partyunit_pid(
        old_pid=rico_text,
        new_pid=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert x_agenda._partys.get(carm_text) != None
    assert x_agenda._partys.get(carm_text).creditor_weight == 16
    assert x_agenda._partys.get(rico_text) is None
    assert len(x_agenda._partys) == 2


def test_agenda_PartyUnit_CorrectlyMergesGroupUnitPartyLinks():
    # GIVEN
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.add_partyunit(pid=rico_text, uid=61, creditor_weight=13)
    x_agenda.add_partyunit(pid=carm_text, uid=5)
    x_agenda.add_partyunit(pid=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_party_dict = {PartyPID(carm_text): partylink_shop(pid=carm_text)}
    swim_group = groupunit_shop(brand=swim_text, _partys=carmen_party_dict)
    swim_group.set_partylink(
        partylink=partylink_shop(pid=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_partylink(
        partylink=partylink_shop(pid=rico_text, creditor_weight=7, debtor_weight=30)
    )
    x_agenda.set_groupunit(groupunit=swim_group)

    swim_group = x_agenda._groups.get(swim_text)
    assert len(swim_group._partys) == 2
    assert swim_group._partys.get(rico_text) != None
    assert swim_group._partys.get(rico_text).creditor_weight == 7
    assert swim_group._partys.get(rico_text).debtor_weight == 30
    assert swim_group._partys.get(carm_text) != None
    assert swim_group._partys.get(carm_text).creditor_weight == 5
    assert swim_group._partys.get(carm_text).debtor_weight == 18

    # WHEN
    x_agenda.edit_partyunit_pid(
        old_pid=rico_text,
        new_pid=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._partys.get(carm_text) != None
    assert swim_group._partys.get(carm_text).creditor_weight == 12
    assert swim_group._partys.get(carm_text).debtor_weight == 48
    assert swim_group._partys.get(rico_text) is None
    assert len(swim_group._partys) == 1


def test_agenda_PartyUnit_raiseErrorNewPIDGroupUnitPreviouslyExists():
    # GIVEN
    x_agenda = agendaunit_shop(_healer="prom")
    rico_text = "rico"
    x_agenda.add_partyunit(pid=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    x_agenda.add_partyunit(pid=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(brand=carmen_text)
    carmen_group.set_partylink(partylink=partylink_shop(pid=rico_text))
    carmen_group.set_partylink(partylink=partylink_shop(pid=anna_text))
    x_agenda.set_groupunit(groupunit=carmen_group)
    assert len(x_agenda._groups) == 3
    assert x_agenda._partys.get(carmen_text) is None
    assert x_agenda._groups.get(carmen_text)._single_party == False
    assert len(x_agenda._groups.get(carmen_text)._partys) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_partyunit_pid(
            old_pid=rico_text,
            new_pid=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' change to '{carmen_text}' failed since non-single group '{carmen_text}' exists."
    )


def test_agenda_PartyUnit_CorrectlyOverwriteNewPIDGroupUnit():
    # GIVEN
    x_agenda = agendaunit_shop(_healer="prom")
    rico_text = "rico"
    x_agenda.add_partyunit(pid=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    x_agenda.add_partyunit(pid=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(brand=carmen_text)
    carmen_group.set_partylink(
        partylink=partylink_shop(pid=rico_text, creditor_weight=3)
    )
    carmen_group.set_partylink(
        partylink=partylink_shop(pid=anna_text, creditor_weight=5)
    )
    x_agenda.set_groupunit(groupunit=carmen_group)
    assert len(x_agenda._groups) == 3
    assert x_agenda._partys.get(rico_text) != None
    assert x_agenda._partys.get(carmen_text) is None
    assert x_agenda._groups.get(carmen_text)._single_party == False
    assert len(x_agenda._groups.get(carmen_text)._partys) == 2
    assert x_agenda._groups.get(carmen_text)._partys.get(anna_text).creditor_weight == 5
    assert x_agenda._groups.get(carmen_text)._partys.get(rico_text).creditor_weight == 3

    # WHEN
    x_agenda.edit_partyunit_pid(
        old_pid=rico_text,
        new_pid=carmen_text,
        allow_party_overwite=False,
        allow_nonsingle_group_overwrite=True,
    )

    assert len(x_agenda._groups) == 2
    assert x_agenda._partys.get(rico_text) is None
    assert x_agenda._partys.get(carmen_text) != None
    assert x_agenda._groups.get(carmen_text)._single_party == True
    assert len(x_agenda._groups.get(carmen_text)._partys) == 1
    assert x_agenda._groups.get(carmen_text)._partys.get(rico_text) is None
    assert (
        x_agenda._groups.get(carmen_text)._partys.get(carmen_text).creditor_weight == 1
    )


def test_agenda_set_all_partyunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=swim_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=pad_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=fly_text))
    assert x_agenda._partys[swim_text].uid is None
    assert x_agenda._partys[pad_text].uid is None
    assert x_agenda._partys[fly_text].uid is None

    # WHEN
    x_agenda.set_all_partyunits_uids_unique()

    # THEN
    assert x_agenda._partys[swim_text].uid != None
    assert x_agenda._partys[pad_text].uid != None
    assert x_agenda._partys[fly_text].uid != None


def test_agenda_set_all_partyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=swim_text, uid=3))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=pad_text, uid=3))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=fly_text))
    assert x_agenda._partys[swim_text].uid == 3
    assert x_agenda._partys[pad_text].uid == 3
    assert x_agenda._partys[fly_text].uid is None

    # WHEN
    x_agenda.set_all_partyunits_uids_unique()

    # THEN
    print(f"{x_agenda._partys[swim_text].uid=}")
    print(f"{x_agenda._partys[pad_text].uid=}")
    assert x_agenda._partys[swim_text].uid != x_agenda._partys[pad_text].uid
    assert x_agenda._partys[pad_text].uid != 3
    assert x_agenda._partys[pad_text].uid != 3
    assert x_agenda._partys[fly_text].uid != None


def test_agenda_set_all_partyunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=swim_text, uid=3))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=pad_text, uid=3))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=fly_text))
    assert x_agenda._partys[swim_text].uid == 3
    assert x_agenda._partys[pad_text].uid == 3
    assert x_agenda._partys[fly_text].uid is None

    # WHEN
    x_agenda.set_all_partyunits_uids_unique()

    # THEN
    print(f"{x_agenda._partys[swim_text].uid=}")
    print(f"{x_agenda._partys[pad_text].uid=}")
    assert x_agenda._partys[swim_text].uid != x_agenda._partys[pad_text].uid
    assert x_agenda._partys[pad_text].uid != 3
    assert x_agenda._partys[pad_text].uid != 3
    assert x_agenda._partys[fly_text].uid != None


def test_agenda_all_partyunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=swim_text, uid=3))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=pad_text, uid=3))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=fly_text))
    assert x_agenda._partys[swim_text].uid == 3
    assert x_agenda._partys[pad_text].uid == 3
    assert x_agenda._partys[fly_text].uid is None

    # WHEN1 / THEN
    assert x_agenda.all_partyunits_uids_are_unique() == False

    # WHEN2
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=swim_text, uid=4))

    # THEN
    assert x_agenda.all_partyunits_uids_are_unique() == False

    # WHEN3
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=fly_text, uid=5))

    # THEN
    assert x_agenda.all_partyunits_uids_are_unique()


def test_agenda_get_partyunits_pid_list_CorrectlyReturnsListOfPartyUnits():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_partys_empty_if_null()
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=sam_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=will_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=fry_text))
    fun_text = "fun people"
    fun_group = groupunit_shop(brand=fun_text)
    fun_group.set_partylink(partylink=partylink_shop(pid=will_text))
    x_agenda.set_groupunit(groupunit=fun_group)
    assert len(x_agenda._groups) == 4
    assert len(x_agenda._partys) == 3

    # WHEN
    partyunit_list_x = x_agenda.get_partyunits_pid_list()

    # THEN
    assert len(partyunit_list_x) == 4
    assert partyunit_list_x[0] == ""
    assert partyunit_list_x[1] == fry_text
    assert partyunit_list_x[2] == sam_text
    assert partyunit_list_x[3] == will_text


def test_get_intersection_of_partys_CorrectlyReturnsUnionOfKeysOfTwoDictionarys_scenario1():
    # GIVEN
    bob_text = "bob"
    x_agenda = agendaunit_shop(_healer=bob_text)
    x_agenda.set_partys_empty_if_null()

    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=bob_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=sam_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=wil_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=fry_text))

    y_agenda = agendaunit_shop()
    y_agenda.set_partys_empty_if_null()

    y_agenda.set_partyunit(partyunit=partyunit_shop(pid=bob_text))
    y_agenda.set_partyunit(partyunit=partyunit_shop(pid=wil_text))
    y_agenda.set_partyunit(partyunit=partyunit_shop(pid=fry_text))
    y_agenda.set_partyunit(partyunit=partyunit_shop(pid=elu_text))

    # WHEN
    print(f"{len(x_agenda._partys)=} {len(y_agenda._partys)=}")
    intersection_x = get_intersection_of_partys(x_agenda._partys, y_agenda._partys)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}


def test_agenda_clear_output_agenda_meld_orders_CorrectlyClearsAttrs():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    rico_partyunit = x_agenda.get_party(rico_text)
    carm_partyunit = x_agenda.get_party(carm_text)
    patr_partyunit = x_agenda.get_party(patr_text)
    rico_partyunit.set_output_agenda_meld_order(3)
    carm_partyunit.set_output_agenda_meld_order(4)
    patr_partyunit.set_output_agenda_meld_order(5)

    assert rico_partyunit._output_agenda_meld_order != None
    assert carm_partyunit._output_agenda_meld_order != None
    assert patr_partyunit._output_agenda_meld_order != None

    # WHEN
    x_agenda.clear_partys_output_agenda_meld_order()

    # THEN
    assert rico_partyunit._output_agenda_meld_order is None
    assert carm_partyunit._output_agenda_meld_order is None
    assert patr_partyunit._output_agenda_meld_order is None


def test_agenda_clear_output_agenda_meld_orders_WithNoArgsCorrectlySetOrder():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    rico_partyunit = x_agenda.get_party(rico_text)
    carm_partyunit = x_agenda.get_party(carm_text)
    patr_partyunit = x_agenda.get_party(patr_text)
    assert rico_partyunit._output_agenda_meld_order is None
    assert carm_partyunit._output_agenda_meld_order is None
    assert patr_partyunit._output_agenda_meld_order is None

    # WHEN
    x_agenda.set_partys_output_agenda_meld_order()

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
