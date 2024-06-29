from src.listen.hubunit import hubunit_shop
from src._world.world import worldunit_shop
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import get_texas_hubunit, env_dir_setup_cleanup
from src.money.treasury_sqlstr import get_worldtreasuryunits_dict


def test_MoneyUnit_treasury_get_worldunits_ReturnsCorrectEmptyObj(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_hubunit())
    x_money.create_treasury_db(in_memory=True)
    x_money.refresh_treasury_job_worlds_data()

    # WHEN
    x_worldtreasuryunits = get_worldtreasuryunits_dict(x_money.get_treasury_conn())

    # THEN
    assert len(x_worldtreasuryunits) == 0


def test_MoneyUnit_treasury_get_worldunits_ReturnsCorrectNoneObj(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_hubunit())
    x_money.create_treasury_db(in_memory=True)
    x_money.refresh_treasury_job_worlds_data()
    assert len(get_worldtreasuryunits_dict(x_money.get_treasury_conn())) == 0

    # WHEN
    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"
    x_money.hubunit.save_job_world(worldunit_shop(_owner_id=sal_text))
    x_money.hubunit.save_job_world(worldunit_shop(_owner_id=bob_text))
    x_money.hubunit.save_job_world(worldunit_shop(_owner_id=tom_text))
    x_money.hubunit.save_job_world(worldunit_shop(_owner_id=ava_text))
    x_money.hubunit.save_job_world(worldunit_shop(_owner_id=elu_text))
    x_money.refresh_treasury_job_worlds_data()
    x_worldtreasuryunits = get_worldtreasuryunits_dict(x_money.get_treasury_conn())

    # THEN
    assert len(x_worldtreasuryunits) == 5
    assert x_worldtreasuryunits.get(sal_text) != None
    assert x_worldtreasuryunits.get(bob_text) != None
    assert x_worldtreasuryunits.get(tom_text) != None
    assert x_worldtreasuryunits.get(ava_text) != None
    assert x_worldtreasuryunits.get(elu_text) != None
    assert x_worldtreasuryunits.get(sal_text).owner_id == sal_text
    assert x_worldtreasuryunits.get(bob_text).owner_id == bob_text
    assert x_worldtreasuryunits.get(tom_text).owner_id == tom_text
    assert x_worldtreasuryunits.get(ava_text).owner_id == ava_text
    assert x_worldtreasuryunits.get(elu_text).owner_id == elu_text
    print(f"{x_worldtreasuryunits.get(sal_text)=}")
    print(f"{x_worldtreasuryunits.get(bob_text)=}")
    print(f"{x_worldtreasuryunits.get(tom_text)=}")
    print(f"{x_worldtreasuryunits.get(ava_text)=}")
    print(f"{x_worldtreasuryunits.get(elu_text)=}")
    assert x_worldtreasuryunits.get(sal_text).rational is None
    assert x_worldtreasuryunits.get(bob_text).rational is None
    assert x_worldtreasuryunits.get(tom_text).rational is None
    assert x_worldtreasuryunits.get(ava_text).rational is None
    assert x_worldtreasuryunits.get(elu_text).rational is None


def test_MoneyUnit_treasury_treasury_set_worldunit_attrs_CorrectlyUpdatesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_hubunit())
    x_money.create_treasury_db(in_memory=True)
    x_money.refresh_treasury_job_worlds_data()
    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"
    sal_world = worldunit_shop(_owner_id=sal_text)
    bob_world = worldunit_shop(_owner_id=bob_text)
    tom_world = worldunit_shop(_owner_id=tom_text)
    ava_world = worldunit_shop(_owner_id=ava_text)
    elu_world = worldunit_shop(_owner_id=elu_text)
    x_money.hubunit.save_job_world(sal_world)
    x_money.hubunit.save_job_world(bob_world)
    x_money.hubunit.save_job_world(tom_world)
    x_money.hubunit.save_job_world(ava_world)
    x_money.hubunit.save_job_world(elu_world)
    x_money.refresh_treasury_job_worlds_data()
    x_worldtreasuryunits = get_worldtreasuryunits_dict(x_money.get_treasury_conn())
    assert x_worldtreasuryunits.get(sal_text).rational is None
    assert x_worldtreasuryunits.get(bob_text).rational is None

    # WHEN
    sal_world.calc_world_metrics()
    bob_rational = False
    bob_world._rational = bob_rational
    x_money._treasury_set_worldunit_attrs(sal_world)
    x_money._treasury_set_worldunit_attrs(bob_world)

    # THEN
    x_worldtreasuryunits = get_worldtreasuryunits_dict(x_money.get_treasury_conn())
    print(f"{x_worldtreasuryunits.get(sal_text)=}")
    print(f"{x_worldtreasuryunits.get(bob_text)=}")
    print(f"{x_worldtreasuryunits.get(tom_text)=}")
    print(f"{x_worldtreasuryunits.get(ava_text)=}")
    print(f"{x_worldtreasuryunits.get(elu_text)=}")
    assert x_worldtreasuryunits.get(sal_text).rational
    assert x_worldtreasuryunits.get(bob_text).rational == bob_rational
