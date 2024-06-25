from src._world.world import worldunit_shop
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import env_dir_setup_cleanup, get_texas_userhub
from src.money.treasury_sqlstr import (
    get_river_circle_table_insert_sqlstr,
    get_river_circle_dict,
    get_river_circle_table_delete_sqlstr,
)


def test_get_river_circle_table_delete_sqlstr_CorrectlyDeletesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 ledger rows
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_world = worldunit_shop(_owner_id=sal_text)
    sal_world.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_world.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_world.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(sal_world)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_world.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    x_money.refresh_treasury_job_worlds_data()
    x_money.set_cred_flow_for_world(owner_id=sal_text)

    with x_money.get_treasury_conn() as treasury_conn:
        assert len(get_river_circle_dict(treasury_conn, sal_text)) > 0

    # WHEN
    sqlstr = get_river_circle_table_delete_sqlstr(sal_text)
    with x_money.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(sqlstr)

    # THEN
    with x_money.get_treasury_conn() as treasury_conn:
        assert len(get_river_circle_dict(treasury_conn, sal_text)) == 0


def test_get_river_circle_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 ledger rows
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_world = worldunit_shop(_owner_id=sal_text)
    sal_world.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_world.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_world.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(sal_world)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_world.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    tom_world = worldunit_shop(_owner_id=tom_text)
    tom_world.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_world(tom_world)

    ava_world = worldunit_shop(_owner_id=ava_text)
    ava_world.add_otherunit(other_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_world(ava_world)

    elu_world = worldunit_shop(_owner_id=elu_text)
    elu_world.add_otherunit(other_id=ava_text, credor_weight=19)
    elu_world.add_otherunit(other_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_world(elu_world)

    x_money.refresh_treasury_job_worlds_data()
    x_money.set_cred_flow_for_world(owner_id=sal_text, max_blocks_count=100)
    with x_money.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(get_river_circle_table_delete_sqlstr(sal_text))
        assert len(get_river_circle_dict(treasury_conn, cash_owner_id=sal_text)) == 0

    # WHEN / THEN
    mstr_sqlstr = get_river_circle_table_insert_sqlstr(cash_owner_id=sal_text)
    with x_money.get_treasury_conn() as treasury_conn:
        print(mstr_sqlstr)
        treasury_conn.execute(mstr_sqlstr)
        # river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
        # for river_block in river_blocks.values():
        #     print(f"{river_block=}")

    # THEN
    with x_money.get_treasury_conn() as treasury_conn:
        river_circles = get_river_circle_dict(treasury_conn, cash_owner_id=sal_text)
        # for river_circle in river_circles.values():
        #     print(f"huh {river_circle=}")

    assert len(river_circles) == 2
    # for river_circle in river_circles:
    #     print(f"{river_circle=}")

    circle_0 = river_circles[0]
    assert circle_0.cash_master == sal_text
    assert circle_0.dst_owner_id == sal_text
    assert circle_0.circle_num == 0
    assert circle_0.coin_start == 0.04401266686517654
    assert circle_0.coin_close == 0.1

    circle_1 = river_circles[1]
    assert circle_1.cash_master == sal_text
    assert circle_1.dst_owner_id == sal_text
    assert circle_1.circle_num == 1
    assert circle_1.coin_start == 0.12316456150798766
    assert circle_1.coin_close == 1.0

    # for value in river_circles.values():
    #     assert value.cash_master == sal_text
    #     assert value.dst_owner_id == sal_text
    #     assert value.circle_num in [0, 1]
    #     assert value.coin_start in [0.12316456150798766, 0.04401266686517654]
    #     assert value.coin_close in [0.1, 1.0]
