from src.listen.userhub import userhub_shop
from src._truth.truth import truthunit_shop
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import get_texas_userhub, env_dir_setup_cleanup
from src.money.treasury_sqlstr import get_truthtreasuryunits_dict


def test_MoneyUnit_treasury_get_truthunits_ReturnsCorrectEmptyObj(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)
    x_money.refresh_treasury_job_truths_data()

    # WHEN
    x_truthtreasuryunits = get_truthtreasuryunits_dict(x_money.get_treasury_conn())

    # THEN
    assert len(x_truthtreasuryunits) == 0


def test_MoneyUnit_treasury_get_truthunits_ReturnsCorrectNoneObj(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)
    x_money.refresh_treasury_job_truths_data()
    assert len(get_truthtreasuryunits_dict(x_money.get_treasury_conn())) == 0

    # WHEN
    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"
    x_money.userhub.save_job_truth(truthunit_shop(_owner_id=sal_text))
    x_money.userhub.save_job_truth(truthunit_shop(_owner_id=bob_text))
    x_money.userhub.save_job_truth(truthunit_shop(_owner_id=tom_text))
    x_money.userhub.save_job_truth(truthunit_shop(_owner_id=ava_text))
    x_money.userhub.save_job_truth(truthunit_shop(_owner_id=elu_text))
    x_money.refresh_treasury_job_truths_data()
    x_truthtreasuryunits = get_truthtreasuryunits_dict(x_money.get_treasury_conn())

    # THEN
    assert len(x_truthtreasuryunits) == 5
    assert x_truthtreasuryunits.get(sal_text) != None
    assert x_truthtreasuryunits.get(bob_text) != None
    assert x_truthtreasuryunits.get(tom_text) != None
    assert x_truthtreasuryunits.get(ava_text) != None
    assert x_truthtreasuryunits.get(elu_text) != None
    assert x_truthtreasuryunits.get(sal_text).owner_id == sal_text
    assert x_truthtreasuryunits.get(bob_text).owner_id == bob_text
    assert x_truthtreasuryunits.get(tom_text).owner_id == tom_text
    assert x_truthtreasuryunits.get(ava_text).owner_id == ava_text
    assert x_truthtreasuryunits.get(elu_text).owner_id == elu_text
    print(f"{x_truthtreasuryunits.get(sal_text)=}")
    print(f"{x_truthtreasuryunits.get(bob_text)=}")
    print(f"{x_truthtreasuryunits.get(tom_text)=}")
    print(f"{x_truthtreasuryunits.get(ava_text)=}")
    print(f"{x_truthtreasuryunits.get(elu_text)=}")
    assert x_truthtreasuryunits.get(sal_text).rational is None
    assert x_truthtreasuryunits.get(bob_text).rational is None
    assert x_truthtreasuryunits.get(tom_text).rational is None
    assert x_truthtreasuryunits.get(ava_text).rational is None
    assert x_truthtreasuryunits.get(elu_text).rational is None


def test_MoneyUnit_treasury_treasury_set_truthunit_attrs_CorrectlyUpdatesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)
    x_money.refresh_treasury_job_truths_data()
    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"
    sal_truth = truthunit_shop(_owner_id=sal_text)
    bob_truth = truthunit_shop(_owner_id=bob_text)
    tom_truth = truthunit_shop(_owner_id=tom_text)
    ava_truth = truthunit_shop(_owner_id=ava_text)
    elu_truth = truthunit_shop(_owner_id=elu_text)
    x_money.userhub.save_job_truth(sal_truth)
    x_money.userhub.save_job_truth(bob_truth)
    x_money.userhub.save_job_truth(tom_truth)
    x_money.userhub.save_job_truth(ava_truth)
    x_money.userhub.save_job_truth(elu_truth)
    x_money.refresh_treasury_job_truths_data()
    x_truthtreasuryunits = get_truthtreasuryunits_dict(x_money.get_treasury_conn())
    assert x_truthtreasuryunits.get(sal_text).rational is None
    assert x_truthtreasuryunits.get(bob_text).rational is None

    # WHEN
    sal_truth.calc_truth_metrics()
    bob_rational = False
    bob_truth._rational = bob_rational
    x_money._treasury_set_truthunit_attrs(sal_truth)
    x_money._treasury_set_truthunit_attrs(bob_truth)

    # THEN
    x_truthtreasuryunits = get_truthtreasuryunits_dict(x_money.get_treasury_conn())
    print(f"{x_truthtreasuryunits.get(sal_text)=}")
    print(f"{x_truthtreasuryunits.get(bob_text)=}")
    print(f"{x_truthtreasuryunits.get(tom_text)=}")
    print(f"{x_truthtreasuryunits.get(ava_text)=}")
    print(f"{x_truthtreasuryunits.get(elu_text)=}")
    assert x_truthtreasuryunits.get(sal_text).rational
    assert x_truthtreasuryunits.get(bob_text).rational == bob_rational
