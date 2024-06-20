from src.agenda.agenda import agendaunit_shop
from src.money.river_cycle import (
    get_credorledger,
    get_debtorledger,
    TaxDueLedger,
    taxdueledger_shop,
)


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


def test_TaxDueLedger_Exists():
    # GIVEN / WHEN
    x_riverrun = TaxDueLedger()

    # THEN
    assert x_riverrun.healer_id is None
    assert x_riverrun.tax_due_ledger is None
    assert x_riverrun.money_amount is None
    assert x_riverrun.penny is None


def test_taxdueledger_shop_ReturnsCorrectWhenEmpty():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 88
    bob_penny = 11

    # WHEN
    bob_taxdueledger = taxdueledger_shop(bob_text, bob_money_amount, bob_penny)

    # THEN
    assert bob_taxdueledger.healer_id == bob_text
    assert bob_taxdueledger.tax_due_ledger == {}
    assert bob_taxdueledger.money_amount == bob_money_amount
    assert bob_taxdueledger.penny == bob_penny


def test_TaxDueLedger_set_other_tax_due_SetsAttr():
    # GIVEN
    bob_text = "Bob"
    bob_taxdueledger = taxdueledger_shop(bob_text)
    yao_text = "Yao"
    assert bob_taxdueledger.tax_due_ledger.get(yao_text) is None

    # WHEN
    yao_tax_due = 7
    bob_taxdueledger.set_other_tax_due(yao_text, yao_tax_due)

    # THEN
    assert bob_taxdueledger.tax_due_ledger.get(yao_text) == yao_tax_due


def test_TaxDueLedger_tax_due_ledger_is_empty_ReturnsObj():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 88
    bob_penny = 11
    bob_taxdueledger = taxdueledger_shop(bob_text, bob_money_amount, bob_penny)
    assert bob_taxdueledger.tax_due_ledger_is_empty()

    # WHEN
    bob_taxdueledger.set_other_tax_due("Yao", 5)

    # THEN
    assert bob_taxdueledger.tax_due_ledger_is_empty() == False


def test_TaxDueLedger_reset_tax_due_ledger_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_taxdueledger = taxdueledger_shop(bob_text, bob_money_amount, bob_penny)
    sue_text = "Sue"
    yao_text = "Yao"
    bob_debtor_weight = 38
    sue_debtor_weight = 56
    yao_debtor_weight = 6
    bob_agenda = agendaunit_shop(bob_text)
    bob_agenda.add_otherunit(bob_text, 2, bob_debtor_weight)
    bob_agenda.add_otherunit(sue_text, 2, sue_debtor_weight)
    bob_agenda.add_otherunit(yao_text, 2, yao_debtor_weight)
    bob_debtorledger = get_debtorledger(bob_agenda)
    assert bob_taxdueledger.tax_due_ledger_is_empty()

    # WHEN
    bob_taxdueledger.reset_tax_due_ledger(bob_debtorledger)

    # THEN
    assert bob_taxdueledger.tax_due_ledger_is_empty() == False
    bob_tax_due_ledger = bob_taxdueledger.tax_due_ledger
    assert bob_tax_due_ledger.get(bob_text) == 380
    assert bob_tax_due_ledger.get(sue_text) == 560
    assert bob_tax_due_ledger.get(yao_text) == 60


def test_TaxDueLedger_other_has_tax_due_ReturnsCorrectBool():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_taxdueledger = taxdueledger_shop(bob_text, bob_money_amount, bob_penny)
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    yao_debtor_weight = 6
    bob_debtor_weight = 38
    sue_debtor_weight = 56
    bob_agenda = agendaunit_shop(bob_text)
    bob_agenda.add_otherunit(bob_text, 2, bob_debtor_weight)
    bob_agenda.add_otherunit(sue_text, 2, sue_debtor_weight)
    bob_agenda.add_otherunit(yao_text, 2, yao_debtor_weight)
    bob_debtorledger = get_debtorledger(bob_agenda)
    assert bob_taxdueledger.other_has_tax_due(bob_text) == False
    assert bob_taxdueledger.other_has_tax_due(sue_text) == False
    assert bob_taxdueledger.other_has_tax_due(yao_text) == False
    assert bob_taxdueledger.other_has_tax_due(zia_text) == False

    # WHEN
    bob_taxdueledger.reset_tax_due_ledger(bob_debtorledger)

    # THEN
    assert bob_taxdueledger.other_has_tax_due(bob_text)
    assert bob_taxdueledger.other_has_tax_due(sue_text)
    assert bob_taxdueledger.other_has_tax_due(yao_text)
    assert bob_taxdueledger.other_has_tax_due(zia_text) == False


def test_TaxDueLedger_delete_tax_due_SetsAttr():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 88
    bob_penny = 11
    bob_taxdueledger = taxdueledger_shop(bob_text, bob_money_amount, bob_penny)
    yao_text = "Yao"
    bob_taxdueledger.set_other_tax_due(yao_text, 5)
    assert bob_taxdueledger.other_has_tax_due(yao_text)

    # WHEN
    bob_taxdueledger.delete_tax_due(yao_text)

    # THEN
    assert bob_taxdueledger.other_has_tax_due(yao_text) == False


def test_TaxDueLedger_get_other_tax_due_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_taxdueledger = taxdueledger_shop(bob_text, bob_money_amount, bob_penny)
    sue_text = "Sue"
    yao_text = "Yao"
    zia_text = "Zia"
    bob_debtor_weight = 38
    sue_debtor_weight = 56
    yao_debtor_weight = 6
    bob_agenda = agendaunit_shop(bob_text)
    bob_agenda.add_otherunit(bob_text, 2, bob_debtor_weight)
    bob_agenda.add_otherunit(sue_text, 2, sue_debtor_weight)
    bob_agenda.add_otherunit(yao_text, 2, yao_debtor_weight)
    bob_debtorledger = get_debtorledger(bob_agenda)
    assert bob_taxdueledger.other_has_tax_due(bob_text) == False
    assert bob_taxdueledger.get_other_tax_due(bob_text) == 0
    assert bob_taxdueledger.other_has_tax_due(zia_text) == False
    assert bob_taxdueledger.get_other_tax_due(zia_text) == 0

    # WHEN
    bob_taxdueledger.reset_tax_due_ledger(bob_debtorledger)

    # THEN
    assert bob_taxdueledger.other_has_tax_due(bob_text)
    assert bob_taxdueledger.get_other_tax_due(bob_text) == 380
    assert bob_taxdueledger.other_has_tax_due(zia_text) == False
    assert bob_taxdueledger.get_other_tax_due(zia_text) == 0


def test_TaxDueLedgerpay_any_tax_due_SetsAttr():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_taxdueledger = taxdueledger_shop(bob_text, bob_money_amount, bob_penny)
    sue_text = "Sue"
    yao_text = "Yao"
    bob_debtor_weight = 38
    sue_debtor_weight = 56
    yao_debtor_weight = 6
    bob_agenda = agendaunit_shop(bob_text)
    bob_agenda.add_otherunit(bob_text, 2, bob_debtor_weight)
    bob_agenda.add_otherunit(sue_text, 2, sue_debtor_weight)
    bob_agenda.add_otherunit(yao_text, 2, yao_debtor_weight)
    bob_debtorledger = get_debtorledger(bob_agenda)
    bob_taxdueledger.reset_tax_due_ledger(bob_debtorledger)
    assert bob_taxdueledger.get_other_tax_due(bob_text) == 380

    # WHEN / THEN
    bob_taxdueledger.pay_any_tax_due(bob_text, 5)
    assert bob_taxdueledger.get_other_tax_due(bob_text) == 375

    # WHEN /THEN
    bob_taxdueledger.pay_any_tax_due(bob_text, 375)
    assert bob_taxdueledger.get_other_tax_due(bob_text) == 0
    assert bob_taxdueledger.other_has_tax_due(bob_text) == False

    # WHEN / THEN
    assert bob_taxdueledger.get_other_tax_due(sue_text) == 560
    bob_taxdueledger.pay_any_tax_due(sue_text, 1000)
    assert bob_taxdueledger.get_other_tax_due(sue_text) == 0
    assert bob_taxdueledger.tax_due_ledger.get(sue_text) is None

    # WHEN / THEN
    zia_text = "Zia"
    assert bob_taxdueledger.get_other_tax_due(zia_text) == 0
    assert bob_taxdueledger.pay_any_tax_due(zia_text, 1000) == 1000

    # WHEN / THEN
    assert bob_taxdueledger.get_other_tax_due(yao_text) == 60
    assert bob_taxdueledger.pay_any_tax_due(yao_text, 81) == 21
