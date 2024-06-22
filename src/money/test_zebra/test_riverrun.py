from src.money.examples.example_credorledgers import (
    example_yao_bob_zia_credorledgers,
    example_yao_bob_zia_tax_dues,
    example_yao_userhub,
)
from src.money.river_cycle import taxunit_shop, RiverRun, riverrun_shop


def test_RiverRun_Exists():
    # GIVEN / WHEN
    x_riverrun = RiverRun()

    # THEN
    # create RiverRun and
    assert x_riverrun.userhub is None
    assert x_riverrun.number is None
    assert x_riverrun.econ_credorledgers is None
    assert x_riverrun.taxunit is None
    assert x_riverrun.cycle_count is None
    assert x_riverrun.cycle_max is None


def test_riverrun_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    ten_int = 10
    yao_userhub = example_yao_userhub()
    econ_credorledgers = example_yao_bob_zia_credorledgers()
    x_taxunit = example_yao_bob_zia_tax_dues()
    x_cycle_max = 10

    x_riverrun = riverrun_shop(
        userhub=yao_userhub,
        number=ten_int,
        econ_credorledgers=econ_credorledgers,
        taxunit=x_taxunit,
        cycle_max=x_cycle_max,
    )

    # THEN
    # create RiverRun and
    assert x_riverrun.userhub == yao_userhub
    assert x_riverrun.number == ten_int
    assert x_riverrun.econ_credorledgers == econ_credorledgers
    assert x_riverrun.taxunit == x_taxunit
    assert x_riverrun.cycle_count == 0
    assert x_riverrun.cycle_max == x_cycle_max


def test_RiverRun_levy_tax_dues_CorrectChanges_cycleledger_Scenario01():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_tax_due = 222
    b_taxunit = taxunit_shop(yao_userhub)
    b_taxunit.set_other_tax_due(yao_text, yao_tax_due)
    x_riverrun = riverrun_shop(yao_userhub, taxunit=b_taxunit)

    yao_paid = 500
    x_cycleledger = {yao_text: yao_paid}
    x_taxunit = x_riverrun.taxunit
    assert x_taxunit.get_other_tax_due(yao_text) == yao_tax_due
    assert x_cycleledger.get(yao_text) == yao_paid

    # WHEN
    x_riverrun.levy_tax_dues(x_cycleledger)

    # THEN
    assert x_taxunit.get_other_tax_due(yao_text) == 0
    assert x_cycleledger.get(yao_text) == yao_paid - yao_tax_due


def test_RiverRun_levy_tax_dues_CorrectChanges_cycleledger_Scenario02():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    bob_text = "Bob"
    yao_tax_due = 222
    bob_tax_due = 127
    x_taxunit = taxunit_shop(yao_userhub)
    x_taxunit.set_other_tax_due(yao_text, yao_tax_due)
    x_taxunit.set_other_tax_due(bob_text, bob_tax_due)
    x_riverrun = riverrun_shop(yao_userhub, taxunit=x_taxunit)

    yao_paid = 500
    bob_paid = 100
    x_cycleledger = {yao_text: yao_paid, bob_text: bob_paid}
    gen_taxunit = x_riverrun.taxunit
    assert gen_taxunit.get_other_tax_due(yao_text) == yao_tax_due
    assert gen_taxunit.get_other_tax_due(bob_text) == bob_tax_due
    assert x_cycleledger.get(yao_text) == yao_paid
    assert x_cycleledger.get(bob_text) == bob_paid

    # WHEN
    x_riverrun.levy_tax_dues(x_cycleledger)

    # THEN
    assert gen_taxunit.get_other_tax_due(yao_text) == 0
    assert gen_taxunit.get_other_tax_due(bob_text) == 27
    assert x_cycleledger.get(yao_text) == yao_paid - yao_tax_due
    assert x_cycleledger.get(bob_text) is None
