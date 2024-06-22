from src.money.examples.example_credorledgers import (
    example_yao_bob_zia_credorledgers,
    example_yao_bob_zia_tax_dues,
    example_yao_userhub,
)
from src.money.river_cycle import RiverRun, riverrun_shop


def test_RiverRun_create_metrics_CorrectChanges_cycleledger_Scenario01():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_credor_weight = 500
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, yao_credor_weight)
    assert x_riverrun.get_other_tax_due(yao_text) == 0

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_other_tax_due(yao_text) == 0
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._debtor_count == 0
    assert x_riverrun._credor_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_text)
    assert yao_rivergrade != None
    assert yao_rivergrade.userhub == yao_userhub
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.debtor_count == 0
    assert yao_rivergrade.credor_count == 1
    assert yao_rivergrade.tax_due_amount == 0
    assert yao_rivergrade.grant_amount == 0
    # assert yao_rivergrade.debtor_rank_num == 1
    # assert yao_rivergrade.credor_rank_num == 1
    # assert yao_rivergrade.tax_paid_amount == 0
    # assert yao_rivergrade.tax_paid_bool
    # assert yao_rivergrade.tax_paid_rank_num == 1
    # assert yao_rivergrade.tax_paid_rank_percent == 1.0
    # assert yao_rivergrade.debtor_rank_percent == 1.0
    # assert yao_rivergrade.credor_rank_percent == 1.0
    # assert yao_rivergrade.transactions_count == 1
    # assert yao_rivergrade.transactions_magnitude == 500
    # assert 1 == 2
