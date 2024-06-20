from src.agenda.agenda import agendaunit_shop
from src.money.river_cycle import get_credorledger, get_debtorledger


def test_get_credorledger_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    yao_credor_weight = 8
    bob_credor_weight = 48
    sue_credor_weight = 66
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(bob_text, yao_credor_weight)
    yao_agenda.add_otherunit(sue_text, bob_credor_weight)
    yao_agenda.add_otherunit(yao_text, sue_credor_weight)

    # WHEN
    yao_credorledger = get_credorledger(yao_agenda)

    # THEN
    assert len(yao_credorledger) == 3
    assert yao_credorledger.get(bob_text) == yao_credor_weight
    assert yao_credorledger.get(sue_text) == bob_credor_weight
    assert yao_credorledger.get(yao_text) == sue_credor_weight


def test_get_debtorledger_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    yao_debtor_weight = 8
    bob_debtor_weight = 48
    sue_debtor_weight = 66
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(bob_text, 2, yao_debtor_weight)
    yao_agenda.add_otherunit(sue_text, 2, bob_debtor_weight)
    yao_agenda.add_otherunit(yao_text, 2, sue_debtor_weight)

    # WHEN
    yao_debtorledger = get_debtorledger(yao_agenda)

    # THEN
    assert len(yao_debtorledger) == 3
    assert yao_debtorledger.get(bob_text) == yao_debtor_weight
    assert yao_debtorledger.get(sue_text) == bob_debtor_weight
    assert yao_debtorledger.get(yao_text) == sue_debtor_weight
