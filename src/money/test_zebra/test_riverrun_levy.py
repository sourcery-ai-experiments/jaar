from src.money.examples.example_credorledgers import (
    example_yao_bob_zia_credorledgers,
    example_yao_bob_zia_tax_dues,
    example_yao_userhub,
)
from src.money.river_cycle import RiverRun, riverrun_shop


def test_RiverRun_levy_tax_dues_CorrectChanges_cycleledger_Scenario01():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_tax_due = 222
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_other_tax_due(yao_text, yao_tax_due)

    yao_paid = 500
    x_cycleledger = {yao_text: yao_paid}
    assert x_riverrun.get_other_tax_due(yao_text) == yao_tax_due
    assert x_cycleledger.get(yao_text) == yao_paid

    # WHEN
    x_riverrun.levy_tax_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_other_tax_due(yao_text) == 0
    assert x_cycleledger.get(yao_text) == yao_paid - yao_tax_due


def test_RiverRun_levy_tax_dues_CorrectChanges_cycleledger_Scenario02():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    bob_text = "Bob"
    yao_tax_due = 222
    bob_tax_due = 127
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_other_tax_due(yao_text, yao_tax_due)
    x_riverrun.set_other_tax_due(bob_text, bob_tax_due)

    yao_paid = 500
    bob_paid = 100
    x_cycleledger = {yao_text: yao_paid, bob_text: bob_paid}
    assert x_riverrun.get_other_tax_due(yao_text) == yao_tax_due
    assert x_riverrun.get_other_tax_due(bob_text) == bob_tax_due
    assert x_cycleledger.get(yao_text) == yao_paid
    assert x_cycleledger.get(bob_text) == bob_paid

    # WHEN
    x_riverrun.levy_tax_dues(x_cycleledger)

    # THEN
    assert x_riverrun.get_other_tax_due(yao_text) == 0
    assert x_riverrun.get_other_tax_due(bob_text) == 27
    assert x_cycleledger.get(yao_text) == yao_paid - yao_tax_due
    assert x_cycleledger.get(bob_text) is None
