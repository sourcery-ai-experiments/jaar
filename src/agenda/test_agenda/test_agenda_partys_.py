from src._road.road import RoadUnit
from src.agenda.party import (
    PartyID,
    partylink_shop,
    partyunit_shop,
    PartyUnitExternalMetrics,
)
from src.agenda.belief import (
    BeliefID,
    beliefunit_shop,
    balancelink_shop,
    get_intersection_of_partys,
)
from src.agenda.examples.example_agendas import (
    agenda_v001 as examples_agenda_v001,
    agenda_v001_with_large_intent as examples_agenda_v001_with_large_intent,
)
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.agenda.idea import ideaunit_shop, IdeaUnit
from pytest import raises as pytest_raises
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


def test_AgendaUnit_set_partyunit_SetObjCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_partyunit = partyunit_shop(yao_text)
    deepcopy_yao_partyunit = copy_deepcopy(yao_partyunit)
    slash_text = "/"
    bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_text)

    # WHEN
    bob_agenda.set_partyunit(partyunit=yao_partyunit)

    # THEN
    assert bob_agenda._partys.get(yao_text)._road_delimiter == slash_text
    x_partys = {yao_partyunit.party_id: deepcopy_yao_partyunit}
    assert bob_agenda._partys != x_partys
    deepcopy_yao_partyunit._road_delimiter = bob_agenda._road_delimiter
    assert bob_agenda._partys == x_partys


def test_examples_agenda_v001_has_partys():
    # GIVEN / WHEN
    yao_agenda = examples_agenda_v001()

    # THEN
    assert yao_agenda._partys != None
    assert len(yao_agenda._partys) == 22


def test_AgendaUnit_set_party_CorrectlySets_partys_beliefs():
    # GIVEN
    x_planck = 0.5
    yao_agenda = agendaunit_shop("Yao", _planck=x_planck)
    yao_agenda.calc_agenda_metrics()
    assert len(yao_agenda._partys) == 0
    assert len(yao_agenda._beliefs) == 0

    # WHEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(rico_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(carm_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(patr_text)))

    # THEN
    assert yao_agenda._partys.get(rico_text)._planck == x_planck
    assert len(yao_agenda._partys) == 3
    assert len(yao_agenda._beliefs) == 3
    assert yao_agenda._beliefs["rico"]._party_mirror == True

    # WHEN
    rico_belief = rico_text
    carm_belief = carm_text
    patr_belief = patr_text
    yao_agenda._idearoot.set_balancelink(
        balancelink_shop(rico_belief, credor_weight=10)
    )
    yao_agenda._idearoot.set_balancelink(
        balancelink_shop(carm_belief, credor_weight=10)
    )
    yao_agenda._idearoot.set_balancelink(
        balancelink_shop(patr_belief, credor_weight=10)
    )
    assert len(yao_agenda._idearoot._balancelinks) == 3


def test_AgendaUnit_add_partyunit_CorrectlySets_partys():
    # GIVEN
    x_planck = 0.5
    yao_agenda = agendaunit_shop("Yao", _planck=x_planck)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    # WHEN
    yao_agenda.add_partyunit(rico_text, credor_weight=13, debtor_weight=8)
    yao_agenda.add_partyunit(carm_text, debtor_weight=5)
    yao_agenda.add_partyunit(patr_text, credor_weight=17)

    # THEN
    assert len(yao_agenda._partys) == 3
    assert len(yao_agenda._beliefs) == 3
    assert yao_agenda.get_beliefunit(rico_text)._party_mirror == True
    assert yao_agenda._partys.get(patr_text).credor_weight == 17
    assert yao_agenda._partys.get(carm_text).debtor_weight == 5
    assert yao_agenda._partys.get(patr_text)._planck == x_planck


def test_AgendaUnit_party_exists_ReturnsObj():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    yao_text = "Yao"

    # WHEN / THEN
    assert bob_agenda.party_exists(yao_text) is False

    # GIVEN
    bob_agenda.add_partyunit(yao_text)

    # WHEN / THEN
    assert bob_agenda.party_exists(yao_text)


def test_AgendaUnit_set_party_CorrectlyUpdate_party_mirror_BeliefUnit():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    before_rico_credor = 7
    before_rico_debtor = 17
    yao_agenda.add_partyunit(rico_text, before_rico_credor, before_rico_debtor)
    rico_beliefunit = yao_agenda.get_beliefunit(rico_text)
    rico_partylink = rico_beliefunit.get_partylink(rico_text)
    assert rico_partylink.credor_weight != before_rico_credor
    assert rico_partylink.debtor_weight != before_rico_debtor
    assert rico_partylink.credor_weight == 1
    assert rico_partylink.debtor_weight == 1

    # WHEN
    after_rico_credor = 11
    after_rico_debtor = 13
    yao_agenda.set_partyunit(
        partyunit_shop(rico_text, after_rico_credor, after_rico_debtor)
    )

    # THEN
    assert rico_partylink.credor_weight != after_rico_credor
    assert rico_partylink.debtor_weight != after_rico_debtor
    assert rico_partylink.credor_weight == 1
    assert rico_partylink.debtor_weight == 1


def test_AgendaUnit_edit_party_RaiseExceptionWhenPartyDoesNotExist():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    rico_credor_weight = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_partyunit(rico_text, credor_weight=rico_credor_weight)
    assert str(excinfo.value) == f"PartyUnit '{rico_text}' does not exist."


def test_AgendaUnit_edit_party_CorrectlyUpdatesObj():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    old_rico_credor_weight = 55
    old_rico_debtor_weight = 66
    yao_agenda.set_partyunit(
        partyunit_shop(
            rico_text,
            old_rico_credor_weight,
            old_rico_debtor_weight,
        )
    )
    rico_partyunit = yao_agenda.get_party(rico_text)
    assert rico_partyunit.credor_weight == old_rico_credor_weight
    assert rico_partyunit.debtor_weight == old_rico_debtor_weight

    # WHEN
    new_rico_credor_weight = 22
    new_rico_debtor_weight = 33
    yao_agenda.edit_partyunit(
        party_id=rico_text,
        credor_weight=new_rico_credor_weight,
        debtor_weight=new_rico_debtor_weight,
    )

    # THEN
    assert rico_partyunit.credor_weight == new_rico_credor_weight
    assert rico_partyunit.debtor_weight == new_rico_debtor_weight


def test_AgendaUnit_get_party_ReturnsCorrectObj():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    yao_agenda.add_partyunit(rico_text)
    yao_agenda.add_partyunit(carm_text)

    # WHEN
    rico_party = yao_agenda.get_party(rico_text)
    carm_party = yao_agenda.get_party(carm_text)

    # THEN
    assert rico_party == yao_agenda._partys.get(rico_text)
    assert carm_party == yao_agenda._partys.get(carm_text)


def test_AgendaUnit_calc_agenda_metrics_CorrectlySetsPartyLinkAgendaCredAndDebt():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(rico_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(carm_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_agenda._idearoot.set_balancelink(balancelink=bl_rico)
    yao_agenda._idearoot.set_balancelink(balancelink=bl_carm)
    yao_agenda._idearoot.set_balancelink(balancelink=bl_patr)

    rico_beliefunit = yao_agenda.get_beliefunit(rico_text)
    carm_beliefunit = yao_agenda.get_beliefunit(carm_text)
    patr_beliefunit = yao_agenda.get_beliefunit(patr_text)
    rico_partylink = rico_beliefunit._partys.get(rico_text)
    carm_partylink = carm_beliefunit._partys.get(carm_text)
    patr_partylink = patr_beliefunit._partys.get(patr_text)
    rico_partylink._agenda_cred is None
    rico_partylink._agenda_debt is None
    carm_partylink._agenda_cred is None
    carm_partylink._agenda_debt is None
    patr_partylink._agenda_cred is None
    patr_partylink._agenda_debt is None

    # for belief in yao_agenda._beliefs.values():
    #     for partylink in belief._partys.values():
    #         assert partylink._agenda_cred is None
    #         assert partylink._agenda_debt is None

    yao_agenda.calc_agenda_metrics()

    # for balancelink in yao_agenda._balanceheirs.values():
    #     print(
    #         f"{yao_agenda._agenda_importance=} {balancelink.belief_id=} {balancelink._agenda_cred=} {balancelink._agenda_debt=}"
    #     )

    assert rico_partylink._agenda_cred == 0.5
    assert rico_partylink._agenda_debt == 0.8
    assert carm_partylink._agenda_cred == 0.25
    assert carm_partylink._agenda_debt == 0.1
    assert patr_partylink._agenda_cred == 0.25
    assert patr_partylink._agenda_debt == 0.1

    # partylink_agenda_cred_sum = 0.0
    # partylink_agenda_debt_sum = 0.0
    # for belief in yao_agenda._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._partys=}")

    #     for partylink in belief._partys.values():
    #         assert partylink._agenda_cred != None
    #         assert partylink._agenda_cred in [0.25, 0.5]
    #         assert partylink._agenda_debt != None
    #         assert partylink._agenda_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {partylink._agenda_importance=} {belief._agenda_importance=}"
    #         # )
    #         partylink_agenda_cred_sum += partylink._agenda_cred
    #         partylink_agenda_debt_sum += partylink._agenda_debt

    #         # print(f"{partylink_agenda_importance_sum=}")
    # assert partylink_agenda_cred_sum == 1.0
    # assert partylink_agenda_debt_sum == 1.0

    assert (
        rico_partylink._agenda_cred
        + carm_partylink._agenda_cred
        + patr_partylink._agenda_cred
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
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(selena_text)))
    yao_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            belief_id=BeliefID(selena_text), credor_weight=20, debtor_weight=13
        )
    )
    yao_agenda.calc_agenda_metrics()

    # THEN
    selena_beliefunit = yao_agenda.get_beliefunit(selena_text)
    selena_partylink = selena_beliefunit._partys.get(selena_text)

    assert rico_partylink._agenda_cred != 0.25
    assert rico_partylink._agenda_debt != 0.8
    assert carm_partylink._agenda_cred != 0.25
    assert carm_partylink._agenda_debt != 0.1
    assert patr_partylink._agenda_cred != 0.5
    assert patr_partylink._agenda_debt != 0.1
    assert selena_partylink._agenda_cred != None
    assert selena_partylink._agenda_debt != None

    # partylink_agenda_cred_sum = 0.0
    # partylink_agenda_debt_sum = 0.0

    # for belief in yao_agenda._beliefs.values():
    #     # print(f"{belief.belief_id=} {belief._partys=}")

    #     for partylink in belief._partys.values():
    #         assert partylink._agenda_cred != None
    #         assert partylink._agenda_cred not in [0.25, 0.5]
    #         assert partylink._agenda_debt != None
    #         assert partylink._agenda_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{belief.belief_id=} {partylink._agenda_importance=} {belief._agenda_importance=}"
    #         # )
    #         partylink_agenda_cred_sum += partylink._agenda_cred
    #         partylink_agenda_debt_sum += partylink._agenda_debt

    #         # print(f"{partylink_agenda_importance_sum=}")
    # assert partylink_agenda_cred_sum == 1.0
    # assert partylink_agenda_debt_sum > 0.9999999
    # assert partylink_agenda_debt_sum < 1.00000001

    assert (
        rico_partylink._agenda_cred
        + carm_partylink._agenda_cred
        + patr_partylink._agenda_cred
        + selena_partylink._agenda_cred
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


def test_AgendaUnit_calc_agenda_metrics_CorrectlySetsPartyUnitAgendaImportance():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    swim_text = "swim"
    yao_agenda.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(rico_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(carm_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_rico)
    yao_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_carm)
    yao_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_patr)

    rico_partyunit = yao_agenda._partys.get(rico_text)
    carm_partyunit = yao_agenda._partys.get(carm_text)
    patr_partyunit = yao_agenda._partys.get(patr_text)

    assert rico_partyunit._agenda_cred == 0
    assert rico_partyunit._agenda_debt == 0
    assert carm_partyunit._agenda_cred == 0
    assert carm_partyunit._agenda_debt == 0
    assert patr_partyunit._agenda_cred == 0
    assert patr_partyunit._agenda_debt == 0

    # WHEN
    yao_agenda.calc_agenda_metrics()

    # THEN
    partyunit_agenda_cred_sum = 0.0
    partyunit_agenda_debt_sum = 0.0

    assert rico_partyunit._agenda_cred == 0.5
    assert rico_partyunit._agenda_debt == 0.8
    assert carm_partyunit._agenda_cred == 0.25
    assert carm_partyunit._agenda_debt == 0.1
    assert patr_partyunit._agenda_cred == 0.25
    assert patr_partyunit._agenda_debt == 0.1

    assert (
        rico_partyunit._agenda_cred
        + carm_partyunit._agenda_cred
        + patr_partyunit._agenda_cred
        == 1.0
    )
    assert (
        rico_partyunit._agenda_debt
        + carm_partyunit._agenda_debt
        + patr_partyunit._agenda_debt
        == 1.0
    )

    # for partyunit in yao_agenda._partys.values():
    #     assert partyunit._agenda_cred != None
    #     assert partyunit._agenda_cred in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {partyunit._agenda_credor=} {belief._agenda_credor=}"
    #     # )
    #     print(f"{partyunit.} {partyunit._agenda_cred=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_cred_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_cred_sum += partyunit._agenda_cred
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt

    # assert partyunit_agenda_cred_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001

    # WHEN another action, check metrics are as expected
    selena_text = "selena"
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(selena_text)))
    yao_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(
            belief_id=selena_text, credor_weight=20, debtor_weight=10
        )
    )
    yao_agenda.calc_agenda_metrics()

    # THEN
    selena_partyunit = yao_agenda._partys.get(selena_text)

    assert rico_partyunit._agenda_cred != 0.5
    assert rico_partyunit._agenda_debt != 0.8
    assert carm_partyunit._agenda_cred != 0.25
    assert carm_partyunit._agenda_debt != 0.1
    assert patr_partyunit._agenda_cred != 0.25
    assert patr_partyunit._agenda_debt != 0.1
    assert selena_partyunit._agenda_cred != None
    assert selena_partyunit._agenda_debt != None

    assert (
        rico_partyunit._agenda_cred
        + carm_partyunit._agenda_cred
        + patr_partyunit._agenda_cred
        < 1.0
    )
    assert (
        rico_partyunit._agenda_cred
        + carm_partyunit._agenda_cred
        + patr_partyunit._agenda_cred
        + selena_partyunit._agenda_cred
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

    # partyunit_agenda_cred_sum = 0.0
    # partyunit_agenda_debt_sum = 0.0

    # for partyunit in yao_agenda._partys.values():
    #     assert partyunit._agenda_cred != None
    #     assert partyunit._agenda_cred not in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {partyunit._agenda_credor=} {belief._agenda_credor=}"
    #     # )
    #     print(f"{partyunit.} {partyunit._agenda_cred=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_cred_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_cred_sum += partyunit._agenda_cred
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt

    # assert partyunit_agenda_cred_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def test_AgendaUnit_calc_agenda_metrics_CorrectlySetsPartBeliefedLWPartyUnitAgendaImportance():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    swim_text = "swim"
    yao_agenda.add_l1_idea(ideaunit_shop(swim_text))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(rico_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(carm_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(patr_text)))
    bl_rico = balancelink_shop(belief_id=rico_text, credor_weight=20, debtor_weight=40)
    bl_carm = balancelink_shop(belief_id=carm_text, credor_weight=10, debtor_weight=5)
    bl_patr = balancelink_shop(belief_id=patr_text, credor_weight=10, debtor_weight=5)
    yao_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_rico)
    yao_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_carm)
    yao_agenda._idearoot._kids.get(swim_text).set_balancelink(balancelink=bl_patr)

    # no balancelinks attached to this one
    hunt_text = "hunt"
    yao_agenda.add_l1_idea(ideaunit_shop(hunt_text, _weight=3))

    # WHEN
    yao_agenda.calc_agenda_metrics()

    # THEN
    rico_beliefunit = yao_agenda.get_beliefunit(rico_text)
    carm_beliefunit = yao_agenda.get_beliefunit(carm_text)
    patr_beliefunit = yao_agenda.get_beliefunit(patr_text)
    assert rico_beliefunit._agenda_cred != 0.5
    assert rico_beliefunit._agenda_debt != 0.8
    assert carm_beliefunit._agenda_cred != 0.25
    assert carm_beliefunit._agenda_debt != 0.1
    assert patr_beliefunit._agenda_cred != 0.25
    assert patr_beliefunit._agenda_debt != 0.1
    assert (
        rico_beliefunit._agenda_cred
        + carm_beliefunit._agenda_cred
        + patr_beliefunit._agenda_cred
        == 0.25
    )
    assert (
        rico_beliefunit._agenda_debt
        + carm_beliefunit._agenda_debt
        + patr_beliefunit._agenda_debt
        == 0.25
    )

    # beliefunit_agenda_cred_sum = 0.0
    # beliefunit_agenda_debt_sum = 0.0
    # for beliefunit in yao_agenda._beliefs.values():
    #     assert beliefunit._agenda_cred != None
    #     assert beliefunit._agenda_cred not in [0.25, 0.5]
    #     assert beliefunit._agenda_debt != None
    #     assert beliefunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {beliefunit._agenda_credor=} {belief._agenda_credor=}"
    #     # )
    #     print(f"{beliefunit.belief_id=} {beliefunit._agenda_cred=} {beliefunit._agenda_debt=} ")
    #     # print(f"{beliefunit_agenda_cred_sum=}")
    #     # print(f"{beliefunit_agenda_debt_sum=}")
    #     beliefunit_agenda_cred_sum += beliefunit._agenda_cred
    #     beliefunit_agenda_debt_sum += beliefunit._agenda_debt
    # assert beliefunit_agenda_cred_sum == 0.25
    # assert beliefunit_agenda_debt_sum == 0.25

    rico_partyunit = yao_agenda._partys.get(rico_text)
    carm_partyunit = yao_agenda._partys.get(carm_text)
    patr_partyunit = yao_agenda._partys.get(patr_text)

    assert rico_partyunit._agenda_cred == 0.375
    assert rico_partyunit._agenda_debt == 0.45
    assert carm_partyunit._agenda_cred == 0.3125
    assert carm_partyunit._agenda_debt == 0.275
    assert patr_partyunit._agenda_cred == 0.3125
    assert patr_partyunit._agenda_debt == 0.275

    assert (
        rico_partyunit._agenda_cred
        + carm_partyunit._agenda_cred
        + patr_partyunit._agenda_cred
        == 1.0
    )
    assert (
        rico_partyunit._agenda_debt
        + carm_partyunit._agenda_debt
        + patr_partyunit._agenda_debt
        == 1.0
    )

    # partyunit_agenda_cred_sum = 0.0
    # partyunit_agenda_debt_sum = 0.0
    # for partyunit in yao_agenda._partys.values():
    #     assert partyunit._agenda_cred != None
    #     assert partyunit._agenda_cred not in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {partyunit._agenda_credor=} {belief._agenda_credor=}"
    #     # )
    #     print(f"{partyunit.} {partyunit._agenda_cred=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_cred_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_cred_sum += partyunit._agenda_cred
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt
    # assert partyunit_agenda_cred_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def test_AgendaUnit_calc_agenda_metrics_CorrectlySetsPartyAttrs():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    yao_agenda.add_l1_idea(ideaunit_shop("swim"))
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.set_partyunit(
        partyunit=partyunit_shop(PartyID(rico_text), credor_weight=8)
    )
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(carm_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(patr_text)))
    rico_partyunit = yao_agenda._partys.get(rico_text)
    carm_partyunit = yao_agenda._partys.get(carm_text)
    patr_partyunit = yao_agenda._partys.get(patr_text)
    assert rico_partyunit._agenda_cred == 0
    assert rico_partyunit._agenda_debt == 0
    assert carm_partyunit._agenda_cred == 0
    assert carm_partyunit._agenda_debt == 0
    assert patr_partyunit._agenda_cred == 0
    assert patr_partyunit._agenda_debt == 0

    # WHEN
    yao_agenda.calc_agenda_metrics()

    # THEN
    assert (
        rico_partyunit._agenda_cred
        + carm_partyunit._agenda_cred
        + patr_partyunit._agenda_cred
        == 1.0
    )
    assert (
        rico_partyunit._agenda_debt
        + carm_partyunit._agenda_debt
        + patr_partyunit._agenda_debt
        == 1.0
    )
    # partyunit_agenda_cred_sum = 0.0
    # partyunit_agenda_debt_sum = 0.0
    # for partyunit in yao_agenda._partys.values():
    #     assert partyunit._agenda_cred != None
    #     assert partyunit._agenda_cred not in [0.25, 0.5]
    #     assert partyunit._agenda_debt != None
    #     assert partyunit._agenda_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{belief.belief_id=} {partyunit._agenda_credor=} {belief._agenda_credor=}"
    #     # )
    #     print(f"{partyunit.} {partyunit._agenda_cred=} {partyunit._agenda_debt=} ")
    #     # print(f"{partyunit_agenda_cred_sum=}")
    #     # print(f"{partyunit_agenda_debt_sum=}")
    #     partyunit_agenda_cred_sum += partyunit._agenda_cred
    #     partyunit_agenda_debt_sum += partyunit._agenda_debt
    # assert partyunit_agenda_cred_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def test_AgendaUnit_calc_agenda_metrics_RaisesErrorWhen_is_partyunits_credor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_credor_weight = 20
    carm_credor_weight = 30
    patr_credor_weight = 50
    yao_agenda.set_partyunit(partyunit_shop(rico_text, None, rico_credor_weight))
    yao_agenda.set_partyunit(partyunit_shop(carm_text, None, carm_credor_weight))
    yao_agenda.set_partyunit(partyunit_shop(patr_text, None, patr_credor_weight))
    assert yao_agenda._party_credor_pool is None
    assert yao_agenda.is_partyunits_credor_weight_sum_correct()
    assert yao_agenda.calc_agenda_metrics() is None

    # WHEN
    x_int = 13
    yao_agenda.set_party_credor_pool(x_int)
    assert yao_agenda.is_partyunits_credor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_agenda.calc_agenda_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_partyunits_credor_weight_sum_correct is False. _party_credor_pool={x_int}. partyunits_credor_weight_sum={yao_agenda.get_partyunits_credor_weight_sum()}"
    )

    # WHEN / THEN
    yao_agenda.set_party_credor_pool(yao_agenda.get_partyunits_credor_weight_sum())
    assert yao_agenda.calc_agenda_metrics() is None


def test_AgendaUnit_calc_agenda_metrics_DoesNotRaiseError_party_credor_poolWhenPartySumIsZero():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    assert yao_agenda._party_credor_pool is None
    assert yao_agenda.is_partyunits_credor_weight_sum_correct()
    assert yao_agenda.calc_agenda_metrics() is None

    # WHEN
    x_int = 13
    yao_agenda.set_party_credor_pool(x_int)

    # THEN
    assert yao_agenda.is_partyunits_credor_weight_sum_correct()
    yao_agenda.calc_agenda_metrics()


def test_AgendaUnit_calc_agenda_metrics_RaisesErrorWhen_is_partyunits_debtor_weight_sum_correct_IsFalse():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 40
    yao_agenda.set_partyunit(partyunit_shop(rico_text, None, None, rico_debtor_weight))
    yao_agenda.set_partyunit(partyunit_shop(carm_text, None, None, carm_debtor_weight))
    yao_agenda.set_partyunit(partyunit_shop(patr_text, None, None, patr_debtor_weight))
    assert yao_agenda._party_debtor_pool is None
    assert yao_agenda.is_partyunits_debtor_weight_sum_correct()
    assert yao_agenda.calc_agenda_metrics() is None

    # WHEN
    x_int = 13
    yao_agenda.set_party_debtor_pool(x_int)
    assert yao_agenda.is_partyunits_debtor_weight_sum_correct() is False
    with pytest_raises(Exception) as excinfo:
        yao_agenda.calc_agenda_metrics()
    assert (
        str(excinfo.value)
        == f"'{yao_text}' is_partyunits_debtor_weight_sum_correct is False. _party_debtor_pool={x_int}. partyunits_debtor_weight_sum={yao_agenda.get_partyunits_debtor_weight_sum()}"
    )

    # WHEN / THEN
    yao_agenda.set_party_debtor_pool(yao_agenda.get_partyunits_debtor_weight_sum())
    assert yao_agenda.calc_agenda_metrics() is None


def test_AgendaUnit_calc_agenda_metrics_DoesNotRaiseError_party_debtor_poolWhenPartySumIsZero():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    assert yao_agenda._party_credor_pool is None
    assert yao_agenda.is_partyunits_debtor_weight_sum_correct()
    assert yao_agenda.calc_agenda_metrics() is None

    # WHEN
    x_int = 13
    yao_agenda.set_party_debtor_pool(x_int)

    # THEN
    assert yao_agenda.is_partyunits_debtor_weight_sum_correct()
    yao_agenda.calc_agenda_metrics()


def clear_all_partyunits_beliefunits_agenda_intent_cred_debt(x_agenda: AgendaUnit):
    # DELETE agenda_intent_debt and agenda_intent_cred
    for beliefunit_x in x_agenda._beliefs.values():
        beliefunit_x.reset_agenda_cred_debt()
        # for partylink_x in beliefunit_x._partys.values():
        #     print(f"{beliefunit_x.belief_id=} {partylink_x.credor_weight=}  {partylink_x._agenda_cred:.6f} {partylink_x.debtor_weight=} {partylink_x._agenda_debt:.6f} {partylink_x.} ")

    # DELETE agenda_intent_debt and agenda_intent_cred
    for x_partyunit in x_agenda._partys.values():
        x_partyunit.reset_agenda_cred_debt()


@dataclass
class BeliefIntentMetrics:
    sum_beliefunit_cred: float = 0
    sum_beliefunit_debt: float = 0
    sum_partylink_cred: float = 0
    sum_partylink_debt: float = 0
    partylink_count: int = 0

    def set_sums(self, x_agenda: AgendaUnit):
        for beliefunit_x in x_agenda._beliefs.values():
            self.sum_beliefunit_cred += beliefunit_x._agenda_intent_cred
            self.sum_beliefunit_debt += beliefunit_x._agenda_intent_debt
            for partylink_x in beliefunit_x._partys.values():
                self.sum_partylink_cred += partylink_x._agenda_intent_cred
                self.sum_partylink_debt += partylink_x._agenda_intent_debt
                self.partylink_count += 1


@dataclass
class PartyIntentMetrics:
    sum_intent_cred: float = 0
    sum_intent_debt: float = 0
    sum_intent_ratio_cred: float = 0
    sum_intent_ratio_debt: float = 0

    def set_sums(self, x_agenda: AgendaUnit):
        for partyunit in x_agenda._partys.values():
            self.sum_intent_cred += partyunit._agenda_intent_cred
            self.sum_intent_debt += partyunit._agenda_intent_debt
            self.sum_intent_ratio_cred += partyunit._agenda_intent_ratio_cred
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


def test_AgendaUnit_intent_cred_debt_IsCorrectlySet():
    # GIVEN
    x_agenda = examples_agenda_v001_with_large_intent()
    clear_all_partyunits_beliefunits_agenda_intent_cred_debt(x_agenda=x_agenda)

    # TEST agenda_intent_debt and agenda_intent_cred are empty
    x_beliefintentmetrics = BeliefIntentMetrics()
    x_beliefintentmetrics.set_sums(x_agenda=x_agenda)
    assert x_beliefintentmetrics.sum_beliefunit_cred == 0
    assert x_beliefintentmetrics.sum_beliefunit_debt == 0
    assert x_beliefintentmetrics.sum_partylink_cred == 0
    assert x_beliefintentmetrics.sum_partylink_debt == 0

    # TEST agenda_intent_debt and agenda_intent_cred are empty
    x_partyintentmetrics = PartyIntentMetrics()
    x_partyintentmetrics.set_sums(x_agenda=x_agenda)
    assert x_partyintentmetrics.sum_intent_cred == 0
    assert x_partyintentmetrics.sum_intent_debt == 0
    assert x_partyintentmetrics.sum_intent_ratio_cred == 0
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
    assert x_balanceintentmetrics.intent_yes_agenda_i_sum == 0.0027965049894874455
    assert are_equal(
        x_balanceintentmetrics.intent_no_agenda_i_sum
        + x_balanceintentmetrics.intent_yes_agenda_i_sum,
        x_balanceintentmetrics.sum_agenda_intent_importance,
    )
    assert x_balanceintentmetrics.sum_agenda_intent_importance == 0.006543772991141412

    x_beliefintentmetrics = BeliefIntentMetrics()
    x_beliefintentmetrics.set_sums(x_agenda=x_agenda)
    assert x_beliefintentmetrics.partylink_count == 81
    x_sum = 0.0027965049894874455
    assert are_equal(x_beliefintentmetrics.sum_beliefunit_cred, x_sum)
    assert are_equal(x_beliefintentmetrics.sum_beliefunit_debt, x_sum)
    assert are_equal(x_beliefintentmetrics.sum_partylink_cred, x_sum)
    assert are_equal(x_beliefintentmetrics.sum_partylink_debt, x_sum)
    assert are_equal(
        x_balanceintentmetrics.intent_yes_agenda_i_sum,
        x_beliefintentmetrics.sum_beliefunit_cred,
    )

    assert all_partyunits_have_legitimate_values(x_agenda)

    x_partyintentmetrics = PartyIntentMetrics()
    x_partyintentmetrics.set_sums(x_agenda=x_agenda)
    assert are_equal(
        x_partyintentmetrics.sum_intent_cred,
        x_balanceintentmetrics.sum_agenda_intent_importance,
    )
    assert are_equal(
        x_partyintentmetrics.sum_intent_debt,
        x_balanceintentmetrics.sum_agenda_intent_importance,
    )
    assert are_equal(x_partyintentmetrics.sum_intent_ratio_cred, 1)
    assert are_equal(x_partyintentmetrics.sum_intent_ratio_debt, 1)

    # partyunit_agenda_cred_sum = 0.0
    # partyunit_agenda_debt_sum = 0.0

    # assert partyunit_agenda_cred_sum == 1.0
    # assert partyunit_agenda_debt_sum > 0.9999999
    # assert partyunit_agenda_debt_sum < 1.00000001


def all_partyunits_have_legitimate_values(x_agenda: AgendaUnit):
    return not any(
        (
            partyunit._agenda_cred is None
            or partyunit._agenda_cred in [0.25, 0.5]
            or partyunit._agenda_debt is None
            or partyunit._agenda_debt in [0.8, 0.1]
        )
        for partyunit in x_agenda._partys.values()
    )


def are_equal(x1: float, x2: float):
    e10 = 0.0000000001
    return abs(x1 - x2) < e10


def test_AgendaUnit_intent_ratio_cred_debt_IsCorrectlySetWhenAgendaIsEmpty():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_party = partyunit_shop(rico_text, credor_weight=0.5, debtor_weight=2)
    carm_party = partyunit_shop(carm_text, credor_weight=1.5, debtor_weight=3)
    patr_party = partyunit_shop(patr_text, credor_weight=8, debtor_weight=5)
    noa_agenda.set_partyunit(partyunit=rico_party)
    noa_agenda.set_partyunit(partyunit=carm_party)
    noa_agenda.set_partyunit(partyunit=patr_party)
    noa_agenda_rico_party = noa_agenda._partys.get(rico_text)
    noa_agenda_carm_party = noa_agenda._partys.get(carm_text)
    noa_agenda_patr_party = noa_agenda._partys.get(patr_text)

    assert noa_agenda_rico_party._agenda_intent_cred in [0, None]
    assert noa_agenda_rico_party._agenda_intent_debt in [0, None]
    assert noa_agenda_carm_party._agenda_intent_cred in [0, None]
    assert noa_agenda_carm_party._agenda_intent_debt in [0, None]
    assert noa_agenda_patr_party._agenda_intent_cred in [0, None]
    assert noa_agenda_patr_party._agenda_intent_debt in [0, None]
    assert noa_agenda_rico_party._agenda_intent_ratio_cred != 0.05
    assert noa_agenda_rico_party._agenda_intent_ratio_debt != 0.2
    assert noa_agenda_carm_party._agenda_intent_ratio_cred != 0.15
    assert noa_agenda_carm_party._agenda_intent_ratio_debt != 0.3
    assert noa_agenda_patr_party._agenda_intent_ratio_cred != 0.8
    assert noa_agenda_patr_party._agenda_intent_ratio_debt != 0.5

    # WHEN
    noa_agenda.calc_agenda_metrics()

    # THEN
    assert noa_agenda_rico_party._agenda_intent_cred == 0
    assert noa_agenda_rico_party._agenda_intent_debt == 0
    assert noa_agenda_carm_party._agenda_intent_cred == 0
    assert noa_agenda_carm_party._agenda_intent_debt == 0
    assert noa_agenda_patr_party._agenda_intent_cred == 0
    assert noa_agenda_patr_party._agenda_intent_debt == 0
    assert noa_agenda_rico_party._agenda_intent_ratio_cred == 0.05
    assert noa_agenda_rico_party._agenda_intent_ratio_debt == 0.2
    assert noa_agenda_carm_party._agenda_intent_ratio_cred == 0.15
    assert noa_agenda_carm_party._agenda_intent_ratio_debt == 0.3
    assert noa_agenda_patr_party._agenda_intent_ratio_cred == 0.8
    assert noa_agenda_patr_party._agenda_intent_ratio_debt == 0.5


def test_AgendaUnit_get_party_belief_ids_ReturnsCorrectObj():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(rico_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(carm_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(patr_text)))

    # WHEN / THEN
    assert yao_agenda.get_party_belief_ids(carm_text) == [carm_text]

    # WHEN / THEN
    swimmers = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swimmers)
    swim_belief.set_partylink(partylink_shop(carm_text))
    yao_agenda.set_beliefunit(swim_belief)
    assert yao_agenda.get_party_belief_ids(carm_text) == [carm_text, swimmers]


def test_AgendaUnit_edit_partyunit_party_id_CorrectlyModifiesPartyUnit_party_id():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    yao_agenda.add_partyunit(rico_text, credor_weight=13)
    yao_agenda.add_partyunit("carmen")
    yao_agenda.add_partyunit("patrick", credor_weight=17)
    assert len(yao_agenda._partys) == 3
    assert yao_agenda._partys.get(rico_text) != None
    assert yao_agenda._partys.get(rico_text).credor_weight == 13
    assert len(yao_agenda._beliefs) == 3
    assert yao_agenda.get_beliefunit(rico_text) != None
    assert yao_agenda.get_beliefunit(rico_text)._party_mirror == True

    # WHEN
    beto_text = "beta"
    yao_agenda.edit_partyunit_party_id(
        old_party_id=rico_text,
        new_party_id=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_agenda._partys.get(beto_text) != None
    assert yao_agenda._partys.get(beto_text).credor_weight == 13
    assert yao_agenda._partys.get(rico_text) is None
    assert len(yao_agenda._partys) == 3
    assert len(yao_agenda._beliefs) == 3
    assert yao_agenda.get_beliefunit(rico_text) is None
    assert yao_agenda.get_beliefunit(beto_text) != None
    assert yao_agenda.get_beliefunit(beto_text)._party_mirror == True


def test_AgendaUnit_PartyUnit_raiseErrorNewparty_idPreviouslyExists():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    yao_agenda.add_partyunit(rico_text, credor_weight=13)
    carmen_text = "carmen"
    yao_agenda.add_partyunit(carmen_text)
    yao_agenda.add_partyunit("patrick", credor_weight=17)
    assert len(yao_agenda._partys) == 3
    assert yao_agenda._partys.get(rico_text) != None
    assert yao_agenda._partys.get(rico_text).credor_weight == 13
    assert len(yao_agenda._beliefs) == 3
    assert yao_agenda.get_beliefunit(rico_text) != None
    assert yao_agenda.get_beliefunit(rico_text)._party_mirror == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_partyunit_party_id(
            old_party_id=rico_text,
            new_party_id=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' modify to '{carmen_text}' failed since '{carmen_text}' exists."
    )


def test_AgendaUnit_PartyUnit_CorrectlyModifiesBeliefUnitPartyLinks():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.add_partyunit(rico_text, credor_weight=13)
    yao_agenda.add_partyunit(carm_text)
    yao_agenda.add_partyunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_party_dict = {PartyID(carm_text): partylink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _partys=carmen_party_dict)
    swim_belief.set_partylink(
        partylink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_partylink(
        partylink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_agenda.set_beliefunit(y_beliefunit=swim_belief)

    swim_belief = yao_agenda.get_beliefunit(swim_text)
    assert len(swim_belief._partys) == 2
    assert swim_belief.get_partylink(rico_text) != None
    assert swim_belief.get_partylink(rico_text).credor_weight == 7
    assert swim_belief.get_partylink(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    yao_agenda.edit_partyunit_party_id(
        old_party_id=rico_text,
        new_party_id=beto_text,
        allow_party_overwite=False,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert swim_belief.get_partylink(beto_text) != None
    assert swim_belief.get_partylink(beto_text).credor_weight == 7
    assert swim_belief.get_partylink(beto_text).debtor_weight == 30
    assert swim_belief.get_partylink(rico_text) is None
    assert len(swim_belief._partys) == 2


def test_AgendaUnit_PartyUnit_CorrectlyMergesparty_ids():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.add_partyunit(rico_text, credor_weight=13)
    yao_agenda.add_partyunit(carm_text, credor_weight=3)
    yao_agenda.add_partyunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_party_dict = {PartyID(carm_text): partylink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _partys=carmen_party_dict)
    swim_belief.set_partylink(
        partylink=partylink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_partylink(
        partylink=partylink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_agenda.set_beliefunit(y_beliefunit=swim_belief)

    assert len(yao_agenda._partys) == 3
    assert yao_agenda._partys.get(rico_text) != None
    assert yao_agenda._partys.get(rico_text).credor_weight == 13
    assert yao_agenda._partys.get(carm_text) != None
    assert yao_agenda._partys.get(carm_text).credor_weight == 3

    # WHEN / THEN
    yao_agenda.edit_partyunit_party_id(
        old_party_id=rico_text,
        new_party_id=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert yao_agenda._partys.get(carm_text) != None
    assert yao_agenda._partys.get(carm_text).credor_weight == 16
    assert yao_agenda._partys.get(rico_text) is None
    assert len(yao_agenda._partys) == 2


def test_AgendaUnit_PartyUnit_CorrectlyMergesBeliefUnitPartyLinks():
    # GIVEN
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.add_partyunit(rico_text, credor_weight=13)
    yao_agenda.add_partyunit(carm_text)
    yao_agenda.add_partyunit(patr_text, credor_weight=17)

    swim_text = ",swimmers"
    carmen_party_dict = {PartyID(carm_text): partylink_shop(carm_text)}
    swim_belief = beliefunit_shop(belief_id=swim_text, _partys=carmen_party_dict)
    swim_belief.set_partylink(
        partylink=partylink_shop(carm_text, credor_weight=5, debtor_weight=18)
    )
    swim_belief.set_partylink(
        partylink=partylink_shop(rico_text, credor_weight=7, debtor_weight=30)
    )
    yao_agenda.set_beliefunit(y_beliefunit=swim_belief)

    swim_belief = yao_agenda.get_beliefunit(swim_text)
    assert len(swim_belief._partys) == 2
    assert swim_belief.get_partylink(rico_text) != None
    assert swim_belief.get_partylink(rico_text).credor_weight == 7
    assert swim_belief.get_partylink(rico_text).debtor_weight == 30
    assert swim_belief.get_partylink(carm_text) != None
    assert swim_belief.get_partylink(carm_text).credor_weight == 5
    assert swim_belief.get_partylink(carm_text).debtor_weight == 18

    # WHEN
    yao_agenda.edit_partyunit_party_id(
        old_party_id=rico_text,
        new_party_id=carm_text,
        allow_party_overwite=True,
        allow_nonsingle_belief_overwrite=False,
    )

    # THEN
    assert swim_belief.get_partylink(carm_text) != None
    assert swim_belief.get_partylink(carm_text).credor_weight == 12
    assert swim_belief.get_partylink(carm_text).debtor_weight == 48
    assert swim_belief.get_partylink(rico_text) is None
    assert len(swim_belief._partys) == 1


def test_AgendaUnit_PartyUnit_raiseErrorNewPersonIDBeliefUnitPreviouslyExists():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    yao_agenda.add_partyunit(rico_text, credor_weight=13)
    anna_text = "anna"
    yao_agenda.add_partyunit(anna_text, credor_weight=17)
    carmen_text = ",carmen"
    carmen_belief = beliefunit_shop(belief_id=carmen_text)
    carmen_belief.set_partylink(partylink=partylink_shop(rico_text))
    carmen_belief.set_partylink(partylink=partylink_shop(anna_text))
    yao_agenda.set_beliefunit(y_beliefunit=carmen_belief)
    assert len(yao_agenda._beliefs) == 3
    assert yao_agenda._partys.get(carmen_text) is None
    assert yao_agenda.get_beliefunit(carmen_text)._party_mirror is False
    assert len(yao_agenda.get_beliefunit(carmen_text)._partys) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_agenda.edit_partyunit_party_id(
            old_party_id=rico_text,
            new_party_id=carmen_text,
            allow_party_overwite=False,
            allow_nonsingle_belief_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Party '{rico_text}' modify to '{carmen_text}' failed since non-single belief '{carmen_text}' exists."
    )


# def test_AgendaUnit_PartyUnit_CorrectlyOverwriteNewPersonIDBeliefUnit():
#     # GIVEN
#     yao_agenda = agendaunit_shop("Yao")
#     rico_text = "rico"
#     yao_agenda.add_partyunit(rico_text, credor_weight=13)
#     anna_text = "anna"
#     yao_agenda.add_partyunit(anna_text, credor_weight=17)
#     carmen_text = ",carmen"
#     carmen_belief = beliefunit_shop(belief_id=carmen_text)
#     carmen_belief.set_partylink(
#         partylink=partylink_shop(rico_text, credor_weight=3)
#     )
#     carmen_belief.set_partylink(
#         partylink=partylink_shop(anna_text, credor_weight=5)
#     )
#     yao_agenda.set_beliefunit(y_beliefunit=carmen_belief)
#     assert len(yao_agenda._beliefs) == 3
#     assert yao_agenda._partys.get(rico_text) != None
#     assert yao_agenda._partys.get(carmen_text) is None
#     assert yao_agenda.get_beliefunit(carmen_text)._party_mirror is False
#     assert len(yao_agenda.get_beliefunit(carmen_text)._partys) == 2
#     assert (
#         yao_agenda.get_beliefunit(carmen_text)._partys.get(anna_text).credor_weight
#         == 5
#     )
#     assert (
#         yao_agenda.get_beliefunit(carmen_text)._partys.get(rico_text).credor_weight
#         == 3
#     )

#     # WHEN
#     yao_agenda.edit_partyunit_party_id(
#         old_rico_text,
#         new_carmen_text,
#         allow_party_overwite=False,
#         allow_nonsingle_belief_overwrite=True,
#     )

#     assert len(yao_agenda._beliefs) == 2
#     assert yao_agenda._partys.get(rico_text) is None
#     assert yao_agenda._partys.get(carmen_text) != None
#     assert yao_agenda.get_beliefunit(carmen_text)._party_mirror == True
#     assert len(yao_agenda.get_beliefunit(carmen_text)._partys) == 1
#     assert yao_agenda.get_beliefunit(carmen_text)._partys.get(rico_text) is None
#     assert (
#         yao_agenda.get_beliefunit(carmen_text)._partys.get(carmen_text).credor_weight
#         == 1
#     )


def test_AgendaUnit_get_partyunits_party_id_list_ReturnsListOfPartyUnits():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    noa_agenda.set_partyunit(partyunit=partyunit_shop(sam_text))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(will_text))
    noa_agenda.set_partyunit(partyunit=partyunit_shop(fry_text))
    fun_text = ",fun people"
    fun_belief = beliefunit_shop(belief_id=fun_text)
    fun_belief.set_partylink(partylink=partylink_shop(will_text))
    noa_agenda.set_beliefunit(y_beliefunit=fun_belief)
    assert len(noa_agenda._beliefs) == 4
    assert len(noa_agenda._partys) == 3

    # WHEN
    partyunit_list_x = noa_agenda.get_partyunits_party_id_list()

    # THEN
    assert len(partyunit_list_x) == 4
    assert partyunit_list_x[0] == ""
    assert partyunit_list_x[1] == fry_text
    assert partyunit_list_x[2] == sam_text
    assert partyunit_list_x[3] == will_text


def test_get_intersection_of_partys_ReturnsUnionOfKeysOfTwoDictionarys_scenario1():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text)

    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "Elu"
    bob_agenda.set_partyunit(partyunit=partyunit_shop(bob_text))
    bob_agenda.set_partyunit(partyunit=partyunit_shop(sam_text))
    bob_agenda.set_partyunit(partyunit=partyunit_shop(wil_text))
    bob_agenda.set_partyunit(partyunit=partyunit_shop(fry_text))

    y_agenda = agendaunit_shop()
    y_agenda.set_partyunit(partyunit=partyunit_shop(bob_text))
    y_agenda.set_partyunit(partyunit=partyunit_shop(wil_text))
    y_agenda.set_partyunit(partyunit=partyunit_shop(fry_text))
    y_agenda.set_partyunit(partyunit=partyunit_shop(elu_text))

    # WHEN
    print(f"{len(bob_agenda._partys)=} {len(y_agenda._partys)=}")
    intersection_x = get_intersection_of_partys(bob_agenda._partys, y_agenda._partys)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}


def test_AgendaUnit_clear_output_agenda_meld_orders_CorrectlyClearsAttrs():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(rico_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(carm_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(patr_text)))
    rico_partyunit = yao_agenda.get_party(rico_text)
    carm_partyunit = yao_agenda.get_party(carm_text)
    patr_partyunit = yao_agenda.get_party(patr_text)
    rico_partyunit.set_output_agenda_meld_order(3)
    carm_partyunit.set_output_agenda_meld_order(4)
    patr_partyunit.set_output_agenda_meld_order(5)

    assert rico_partyunit._output_agenda_meld_order != None
    assert carm_partyunit._output_agenda_meld_order != None
    assert patr_partyunit._output_agenda_meld_order != None

    # WHEN
    yao_agenda.clear_partys_output_agenda_meld_order()

    # THEN
    assert rico_partyunit._output_agenda_meld_order is None
    assert carm_partyunit._output_agenda_meld_order is None
    assert patr_partyunit._output_agenda_meld_order is None


def test_AgendaUnit_clear_output_agenda_meld_orders_WithNoArgsCorrectlySetOrder():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(rico_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(carm_text)))
    yao_agenda.set_partyunit(partyunit=partyunit_shop(PartyID(patr_text)))
    rico_partyunit = yao_agenda.get_party(rico_text)
    carm_partyunit = yao_agenda.get_party(carm_text)
    patr_partyunit = yao_agenda.get_party(patr_text)
    assert rico_partyunit._output_agenda_meld_order is None
    assert carm_partyunit._output_agenda_meld_order is None
    assert patr_partyunit._output_agenda_meld_order is None

    # WHEN
    yao_agenda.set_partys_output_agenda_meld_order()

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


def test_AgendaUnit_is_partyunits_credor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_credor_weight = 20
    carm_credor_weight = 30
    patr_credor_weight = 50
    yao_agenda.set_partyunit(partyunit_shop(rico_text, rico_credor_weight))
    yao_agenda.set_partyunit(partyunit_shop(carm_text, carm_credor_weight))
    yao_agenda.set_partyunit(partyunit_shop(patr_text, patr_credor_weight))
    # print(f"{yao_agenda._partys.keys()=}")
    # for x_partyunit in yao_agenda._partys.values():
    #     print(f"{x_partyunit.credor_weight=}")

    # WHEN / THEN
    assert yao_agenda.is_partyunits_credor_weight_sum_correct()
    yao_agenda.set_party_credor_pool(13)
    assert yao_agenda.is_partyunits_credor_weight_sum_correct() is False
    # WHEN / THEN
    yao_party_cred_pool = rico_credor_weight + carm_credor_weight + patr_credor_weight
    yao_agenda.set_party_credor_pool(yao_party_cred_pool)
    assert yao_agenda.is_partyunits_credor_weight_sum_correct()


def test_AgendaUnit_is_partyunits_debtor_weight_sum_correct_ReturnsCorrectBool():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_debtor_weight = 15
    carm_debtor_weight = 25
    patr_debtor_weight = 60
    yao_agenda.set_partyunit(partyunit_shop(rico_text, None, rico_debtor_weight))
    yao_agenda.set_partyunit(partyunit_shop(carm_text, None, carm_debtor_weight))
    yao_agenda.set_partyunit(partyunit_shop(patr_text, None, patr_debtor_weight))

    # WHEN / THEN
    yao_party_debt_pool = rico_debtor_weight + carm_debtor_weight + patr_debtor_weight
    assert yao_agenda.is_partyunits_debtor_weight_sum_correct()
    yao_agenda.set_party_debtor_pool(yao_party_debt_pool + 1)
    assert yao_agenda.is_partyunits_debtor_weight_sum_correct() is False
    # WHEN / THEN
    yao_agenda.set_party_debtor_pool(yao_party_debt_pool)
    assert yao_agenda.is_partyunits_debtor_weight_sum_correct()


def test_AgendaUnit_set_partyunit_external_metrics_SetsAttrs_credor_operational_debtor_operational():
    # GIVEN
    x_agenda = agendaunit_shop("Yao")
    jane_text = "Jane Randolph"
    x_agenda.add_partyunit(jane_text)

    jane_party = x_agenda._partys.get(jane_text)
    print(f"Before Party {jane_party.party_id} {jane_party._debtor_operational=} ")
    assert jane_party._debtor_operational is None
    assert jane_party._credor_operational is None

    assert sum(
        party_x._credor_operational is None for party_x in x_agenda._partys.values()
    ) == len(x_agenda._partys)
    assert sum(
        party_x._debtor_operational is None for party_x in x_agenda._partys.values()
    ) == len(x_agenda._partys)

    # WHEN
    jane_debtor_status = True
    jane_credor_status = True
    jane_metr = PartyUnitExternalMetrics(
        internal_party_id=jane_text,
        debtor_operational=jane_debtor_status,
        credor_operational=jane_credor_status,
    )
    x_agenda.set_partyunit_external_metrics(jane_metr)

    # THEN
    assert jane_party._debtor_operational == jane_debtor_status
    assert jane_party._credor_operational == jane_credor_status

    assert (
        sum(
            party_x._credor_operational is None for party_x in x_agenda._partys.values()
        )
        == len(x_agenda._partys) - 1
    )
    assert (
        sum(
            party_x._debtor_operational is None for party_x in x_agenda._partys.values()
        )
        == len(x_agenda._partys) - 1
    )
    assert (
        sum(
            party_x._credor_operational != None for party_x in x_agenda._partys.values()
        )
        == 1
    )
    assert (
        sum(
            party_x._debtor_operational != None for party_x in x_agenda._partys.values()
        )
        == 1
    )
