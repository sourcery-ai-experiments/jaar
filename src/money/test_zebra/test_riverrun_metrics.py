from src.money.examples.example_credorledgers import example_yao_userhub
from src.money.riverrun import riverrun_shop


def test_RiverRun_calc_metrics_SetsAttrsScenario01():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_credor_weight = 500
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, yao_credor_weight)
    assert x_riverrun.get_person_tax_due(yao_text) == 0

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._debtor_count == 0
    assert x_riverrun._credor_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_text)
    assert yao_rivergrade != None
    assert yao_rivergrade.userhub == yao_userhub
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.grant_amount == yao_userhub.econ_money_magnitude
    assert yao_rivergrade.tax_bill_amount == 0
    assert yao_rivergrade.tax_paid_amount == 0
    assert yao_rivergrade.tax_paid_bool
    # assert yao_rivergrade.tax_paid_rank_num == 1
    # assert yao_rivergrade.tax_paid_rank_percent == 1.0
    # assert yao_rivergrade.debtor_rank_num is None
    # assert yao_rivergrade.credor_rank_num == 1
    # assert yao_rivergrade.debtor_rank_percent == 1.0
    # assert yao_rivergrade.debtor_count == 0
    # assert yao_rivergrade.credor_count == 1
    # assert yao_rivergrade.credor_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500


def test_RiverRun_calc_metrics_SetsAttrsScenario02():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_credor_weight = 500
    bob_text = "Bob"
    bob_debtor_weight = 350
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, yao_credor_weight)
    x_riverrun.set_tax_dues({bob_text: bob_debtor_weight})
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    econ_money_amount = x_riverrun.userhub.econ_money_magnitude
    assert x_riverrun.get_person_tax_due(bob_text) == econ_money_amount

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    assert x_riverrun.get_person_tax_due(bob_text) == econ_money_amount
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._debtor_count == 1
    assert x_riverrun._credor_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_text)
    assert yao_rivergrade != None
    assert yao_rivergrade.userhub == yao_userhub
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.grant_amount == yao_userhub.econ_money_magnitude
    assert yao_rivergrade.tax_bill_amount == 0
    assert yao_rivergrade.tax_paid_amount == 0
    assert yao_rivergrade.tax_paid_bool
    # assert yao_rivergrade.tax_paid_rank_num == 1
    # assert yao_rivergrade.tax_paid_rank_percent == 1.0
    # assert yao_rivergrade.debtor_rank_num is None
    # assert yao_rivergrade.credor_rank_num == 1
    # assert yao_rivergrade.debtor_rank_percent == 1.0
    # assert yao_rivergrade.debtor_count == 0
    # assert yao_rivergrade.credor_count == 1
    # assert yao_rivergrade.credor_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500
    # assert 1 == 2


def test_RiverRun_calc_metrics_SetsAttrsScenario03():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_credor_weight = 500
    bob_text = "Bob"
    bob_debtor_weight = 25
    sue_text = "Sue"
    sue_debtor_weight = 75
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, yao_credor_weight)
    debtorledger = {bob_text: bob_debtor_weight, sue_text: sue_debtor_weight}
    x_riverrun.set_tax_dues(debtorledger)
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    econ_money_amount = x_riverrun.userhub.econ_money_magnitude
    assert x_riverrun.get_person_tax_due(bob_text) == econ_money_amount * 0.25
    assert x_riverrun.get_person_tax_due(sue_text) == econ_money_amount * 0.75

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    assert x_riverrun.get_person_tax_due(bob_text) == econ_money_amount * 0.25
    assert x_riverrun.get_person_tax_due(sue_text) == econ_money_amount * 0.75
    assert x_riverrun._cycle_count == 1
    assert x_riverrun._debtor_count == 2
    assert x_riverrun._credor_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_text)
    assert yao_rivergrade != None
    assert yao_rivergrade.userhub == yao_userhub
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.grant_amount == yao_userhub.econ_money_magnitude
    assert yao_rivergrade.tax_bill_amount == 0
    assert yao_rivergrade.tax_paid_amount == 0
    assert yao_rivergrade.tax_paid_bool
    # assert yao_rivergrade.tax_paid_rank_num == 1
    # assert yao_rivergrade.tax_paid_rank_percent == 1.0
    # assert yao_rivergrade.debtor_rank_num is None
    # assert yao_rivergrade.credor_rank_num == 1
    # assert yao_rivergrade.debtor_rank_percent == 1.0
    # assert yao_rivergrade.debtor_count == 0
    # assert yao_rivergrade.credor_count == 1
    # assert yao_rivergrade.credor_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500
    # assert 1 == 2


def test_RiverRun_calc_metrics_SetsAttrsScenario04():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_yao_credor_weight = 500
    yao_sue_credor_weight = 2000
    bob_text = "Bob"
    bob_debtor_weight = 25
    sue_text = "Sue"
    sue_debtor_weight = 75
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, yao_yao_credor_weight)
    x_riverrun.set_econ_credorledger(yao_text, sue_text, yao_sue_credor_weight)
    debtorledger = {bob_text: bob_debtor_weight, sue_text: sue_debtor_weight}
    x_riverrun.set_tax_dues(debtorledger)
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    econ_money_amount = x_riverrun.userhub.econ_money_magnitude
    assert x_riverrun.get_person_tax_due(bob_text) == econ_money_amount * 0.25
    assert x_riverrun.get_person_tax_due(sue_text) == econ_money_amount * 0.75

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    assert x_riverrun.get_person_tax_due(bob_text) == econ_money_amount * 0.25
    assert x_riverrun.get_person_tax_due(sue_text) == 0
    assert x_riverrun.get_person_tax_yield(sue_text) == econ_money_amount * 0.75
    assert x_riverrun._cycle_count == 2
    assert x_riverrun._debtor_count == 2
    assert x_riverrun._credor_count == 2
    yao_rivergrade = x_riverrun.get_rivergrade(yao_text)
    sue_rivergrade = x_riverrun.get_rivergrade(sue_text)
    assert yao_rivergrade.grant_amount == yao_userhub.econ_money_magnitude * 0.2
    assert sue_rivergrade.grant_amount == yao_userhub.econ_money_magnitude * 0.8
    assert yao_rivergrade.tax_bill_amount == 0
    assert yao_rivergrade.tax_paid_amount == 0
    assert yao_rivergrade.tax_paid_bool
    # assert yao_rivergrade.tax_paid_rank_num == 1
    # assert yao_rivergrade.tax_paid_rank_percent == 1.0
    # assert yao_rivergrade.debtor_rank_num is None
    # assert yao_rivergrade.credor_rank_num == 1
    # assert yao_rivergrade.debtor_rank_percent == 1.0
    # assert yao_rivergrade.debtor_count == 0
    # assert yao_rivergrade.credor_count == 1
    # assert yao_rivergrade.credor_rank_percent == 1.0
    # assert yao_rivergrade.rewards_count == 1
    # assert yao_rivergrade.rewards_magnitude == 500
    # assert 1 == 2


def test_RiverRun_calc_metrics_SetsAttrsScenario05():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_credor_weight = 500
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, yao_credor_weight)
    x_riverrun.set_tax_dues({yao_text: 1})
    econ_money_amount = yao_userhub.econ_money_magnitude
    assert x_riverrun.get_person_tax_due(yao_text) == econ_money_amount
    assert x_riverrun.get_person_tax_yield(yao_text) == 0

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    assert x_riverrun.get_person_tax_yield(yao_text) == econ_money_amount
    assert x_riverrun._cycle_count == 2
    assert x_riverrun._debtor_count == 1
    assert x_riverrun._credor_count == 1
    yao_rivergrade = x_riverrun.get_rivergrade(yao_text)
    assert yao_rivergrade != None
    assert yao_rivergrade.userhub == yao_userhub
    assert yao_rivergrade.number == 0
    assert yao_rivergrade.grant_amount == econ_money_amount
    assert yao_rivergrade.tax_bill_amount == econ_money_amount
    assert yao_rivergrade.tax_paid_amount == econ_money_amount
    assert yao_rivergrade.tax_paid_bool


def test_RiverRun_calc_metrics_EachTimeResets_tax_yield():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_credor_weight = 500
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, yao_credor_weight)
    x_riverrun.set_tax_dues({yao_text: 1})
    econ_money_amount = yao_userhub.econ_money_magnitude
    x_riverrun.calc_metrics()
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    assert x_riverrun.get_person_tax_yield(yao_text) == econ_money_amount

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    assert x_riverrun.get_person_tax_yield(yao_text) == econ_money_amount


def test_RiverRun_calc_metrics_EndsRiverCycleLoopIfNoDifferencesBetweenCycles():
    # GIVEN / WHEN
    x_riverrun = riverrun_shop(example_yao_userhub())
    yao_text = "Yao"
    bob_text = "Bob"
    x_riverrun.set_econ_credorledger(yao_text, yao_text, 1)
    x_riverrun.set_tax_dues({bob_text: 1})
    econ_money_amount = x_riverrun.userhub.econ_money_magnitude
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    assert x_riverrun.get_person_tax_due(bob_text) == econ_money_amount
    assert x_riverrun._cycle_count == 0
    assert x_riverrun._cycle_payees_prev == set()
    assert x_riverrun._cycle_payees_curr == set()

    # WHEN
    x_riverrun.calc_metrics()

    # THEN
    assert x_riverrun._cycle_payees_prev == {yao_text}
    assert x_riverrun._cycle_payees_curr == {yao_text}
    assert x_riverrun.get_person_tax_due(yao_text) == 0
    assert x_riverrun.get_person_tax_due(bob_text) == econ_money_amount
    assert x_riverrun._cycle_count == 1
