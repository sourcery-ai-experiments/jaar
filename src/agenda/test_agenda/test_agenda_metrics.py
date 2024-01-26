from src.agenda.examples.example_agendas import (
    agenda_v001 as example_agendas_agenda_v001,
)
from src.agenda.party import partyunit_shop
from src.agenda.group import GroupBrand, balancelink_shop
from src.agenda.agenda import agendaunit_shop


def test_AgendaUnit_get_tree_metrics_TracksReasonsThatHaveNoBeliefBases():
    yao_agenda = example_agendas_agenda_v001()
    yao_agenda_metrics = yao_agenda.get_tree_metrics()

    print(f"{yao_agenda_metrics.level_count=}")
    print(f"{yao_agenda_metrics.reason_bases=}")
    assert yao_agenda_metrics != None
    reason_bases_x = yao_agenda_metrics.reason_bases
    assert reason_bases_x != None
    assert len(reason_bases_x) > 0


def test_AgendaUnit_get_missing_belief_bases_ReturnsAllBasesNotCoveredByBeliefs():
    yao_agenda = example_agendas_agenda_v001()
    missing_bases = yao_agenda.get_missing_belief_bases()
    assert missing_bases != None
    print(f"{missing_bases=}")
    print(f"{len(missing_bases)=}")
    assert len(missing_bases) == 11

    yao_agenda.set_belief(
        base=yao_agenda.make_l1_road("day_minute"),
        pick=yao_agenda.make_l1_road("day_minute"),
        open=0,
        nigh=1439,
    )
    missing_bases = yao_agenda.get_missing_belief_bases()

    assert len(missing_bases) == 11


def test_AgendaUnit_3AdvocatesNoideaunit_shop():
    # GIVEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    yue_agenda = agendaunit_shop("Yue")
    au_rico = partyunit_shop(party_id=rico_text)
    au_carm = partyunit_shop(party_id=carm_text)
    au_patr = partyunit_shop(party_id=patr_text)
    # print(f"{rico=}")
    yue_agenda.set_partyunit(partyunit=au_rico)
    yue_agenda.set_partyunit(partyunit=au_carm)
    yue_agenda.set_partyunit(partyunit=au_patr)
    yue_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand(rico_text), creditor_weight=10)
    )
    yue_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand(carm_text), creditor_weight=10)
    )
    yue_agenda._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand(patr_text), creditor_weight=10)
    )

    # WHEN
    assert yue_agenda.get_partys_metrics() != None
    partys_metrics = yue_agenda.get_partys_metrics()

    # THEN
    balancelink_rico = partys_metrics[rico_text]
    balancelink_carm = partys_metrics[carm_text]
    balancelink_patr = partys_metrics[patr_text]
    assert balancelink_rico.brand != None
    assert balancelink_carm.brand != None
    assert balancelink_patr.brand != None
    assert balancelink_rico.brand == rico_text
    assert balancelink_carm.brand == carm_text
    assert balancelink_patr.brand == patr_text
    all_groups = yue_agenda._groups
    groupunit_rico = all_groups[rico_text]
    groupunit_carm = all_groups[carm_text]
    groupunit_patr = all_groups[patr_text]
    assert groupunit_rico._party_mirrow == True
    assert groupunit_carm._party_mirrow == True
    assert groupunit_patr._party_mirrow == True
