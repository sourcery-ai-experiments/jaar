from src.agenda.agenda import agendaunit_shop
from src.listen.userhub import userhub_shop
from src.money.river_cycle import (
    get_credorledger,
    get_debtorledger,
    RiverRun,
    riverrun_shop,
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


def test_RiverRun_Exists():
    # GIVEN / WHEN
    riverrun = RiverRun()

    # THEN
    assert riverrun.userhub is None
    assert riverrun.taxledger is None


def test_riverrun_shop_ReturnsCorrectWhenEmpty():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 88
    bob_penny = 11
    bob_userhub = userhub_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )

    # WHEN
    bob_riverrun = riverrun_shop(bob_userhub)

    # THEN
    assert bob_riverrun.userhub == bob_userhub
    assert bob_riverrun.taxledger == {}


def test_RiverRun_set_other_tax_due_SetsAttr():
    # GIVEN
    bob_text = "Bob"
    bob_userhub = userhub_shop(None, None, bob_text)
    bob_riverrun = riverrun_shop(bob_userhub)
    yao_text = "Yao"
    assert bob_riverrun.taxledger.get(yao_text) is None

    # WHEN
    yao_tax_due = 7
    bob_riverrun.set_other_tax_due(yao_text, yao_tax_due)

    # THEN
    assert bob_riverrun.taxledger.get(yao_text) == yao_tax_due


def test_RiverRun_riverrun_is_empty_ReturnsObj():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 88
    bob_penny = 11
    bob_userhub = userhub_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_userhub)
    assert bob_riverrun.taxledger_is_empty()

    # WHEN
    bob_riverrun.set_other_tax_due("Yao", 5)

    # THEN
    assert bob_riverrun.taxledger_is_empty() == False


def test_RiverRun_reset_taxledger_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_userhub = userhub_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_userhub)
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
    assert bob_riverrun.taxledger_is_empty()

    # WHEN
    bob_riverrun.reset_taxledger(bob_debtorledger)

    # THEN
    assert bob_riverrun.taxledger_is_empty() == False
    bob_riverrun = bob_riverrun.taxledger
    assert bob_riverrun.get(bob_text) == 380
    assert bob_riverrun.get(sue_text) == 560
    assert bob_riverrun.get(yao_text) == 60


def test_RiverRun_other_has_tax_due_ReturnsCorrectBool():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_userhub = userhub_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_userhub)
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
    assert bob_riverrun.other_has_tax_due(bob_text) == False
    assert bob_riverrun.other_has_tax_due(sue_text) == False
    assert bob_riverrun.other_has_tax_due(yao_text) == False
    assert bob_riverrun.other_has_tax_due(zia_text) == False

    # WHEN
    bob_riverrun.reset_taxledger(bob_debtorledger)

    # THEN
    assert bob_riverrun.other_has_tax_due(bob_text)
    assert bob_riverrun.other_has_tax_due(sue_text)
    assert bob_riverrun.other_has_tax_due(yao_text)
    assert bob_riverrun.other_has_tax_due(zia_text) == False


def test_RiverRun_delete_tax_due_SetsAttr():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 88
    bob_penny = 11
    bob_userhub = userhub_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_userhub)
    yao_text = "Yao"
    bob_riverrun.set_other_tax_due(yao_text, 5)
    assert bob_riverrun.other_has_tax_due(yao_text)

    # WHEN
    bob_riverrun.delete_tax_due(yao_text)

    # THEN
    assert bob_riverrun.other_has_tax_due(yao_text) == False


def test_RiverRun_get_other_tax_due_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_userhub = userhub_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_userhub)
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
    assert bob_riverrun.other_has_tax_due(bob_text) == False
    assert bob_riverrun.get_other_tax_due(bob_text) == 0
    assert bob_riverrun.other_has_tax_due(zia_text) == False
    assert bob_riverrun.get_other_tax_due(zia_text) == 0

    # WHEN
    bob_riverrun.reset_taxledger(bob_debtorledger)

    # THEN
    assert bob_riverrun.other_has_tax_due(bob_text)
    assert bob_riverrun.get_other_tax_due(bob_text) == 380
    assert bob_riverrun.other_has_tax_due(zia_text) == False
    assert bob_riverrun.get_other_tax_due(zia_text) == 0


def test_RiverRun_levy_tax_due_SetsAttr():
    # GIVEN
    bob_text = "Bob"
    bob_money_amount = 1000
    bob_penny = 1
    bob_userhub = userhub_shop(
        None, None, bob_text, penny=bob_penny, econ_money_magnitude=bob_money_amount
    )
    bob_riverrun = riverrun_shop(bob_userhub)
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
    bob_riverrun.reset_taxledger(bob_debtorledger)
    assert bob_riverrun.get_other_tax_due(bob_text) == 380

    # WHEN / THEN
    excess_payer_money = bob_riverrun.levy_tax_due(bob_text, 5)
    assert excess_payer_money == 0
    assert bob_riverrun.get_other_tax_due(bob_text) == 375

    # WHEN /THEN
    excess_payer_money = bob_riverrun.levy_tax_due(bob_text, 375)
    assert excess_payer_money == 0
    assert bob_riverrun.get_other_tax_due(bob_text) == 0
    assert bob_riverrun.other_has_tax_due(bob_text) == False

    # WHEN / THEN
    assert bob_riverrun.get_other_tax_due(sue_text) == 560
    excess_payer_money = bob_riverrun.levy_tax_due(sue_text, 1000)
    assert excess_payer_money == 440
    assert bob_riverrun.get_other_tax_due(sue_text) == 0
    assert bob_riverrun.taxledger.get(sue_text) is None

    # WHEN / THEN
    zia_text = "Zia"
    excess_payer_money = bob_riverrun.get_other_tax_due(zia_text)
    assert excess_payer_money == 0
    assert bob_riverrun.levy_tax_due(zia_text, 1000) == 1000

    # WHEN / THEN
    assert bob_riverrun.get_other_tax_due(yao_text) == 60
    assert bob_riverrun.levy_tax_due(yao_text, 81) == 21
