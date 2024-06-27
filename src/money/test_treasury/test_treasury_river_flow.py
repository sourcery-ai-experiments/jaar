from src._world.world import worldunit_shop
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import env_dir_setup_cleanup, get_texas_userhub
from src._instrument.sqlite import get_single_result, get_row_count_sqlstr
from src.money.treasury_sqlstr import (
    get_chartreasuryunit_dict,
    get_river_block_dict,
)


def get_world_charunit_table_treasurying_attr_set_count_sqlstr():
    # def get_world_charunit_table_treasurying_attr_set_count_sqlstr(cash_master:):
    #     return f"""
    # SELECT COUNT(*)
    # FROM world_charunit
    # WHERE _treasury_due_paid IS NOT NULL
    #     AND owner_id = {cash_master}
    # """
    return """
SELECT COUNT(*) 
FROM world_charunit
WHERE _treasury_due_paid IS NOT NULL
;
"""


def test_MoneyUnit_set_cred_flow_for_world_CorrectlyPopulateschartreasuryunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"

    sal_worldunit = worldunit_shop(_owner_id=sal_text)
    sal_worldunit.add_charunit(char_id=bob_text, credor_weight=1)
    sal_worldunit.add_charunit(char_id=tom_text, credor_weight=3)
    x_money.userhub.save_job_world(sal_worldunit)

    bob_worldunit = worldunit_shop(_owner_id=bob_text)
    bob_worldunit.add_charunit(char_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_worldunit)

    tom_worldunit = worldunit_shop(_owner_id=tom_text)
    tom_worldunit.add_charunit(char_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_world(tom_worldunit)

    x_money.refresh_treasury_job_worlds_data()
    charunit_count_sqlstr = get_row_count_sqlstr("world_charunit")
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 4

    chartreasuryunit_count_sqlstr = (
        get_world_charunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_world(owner_id=sal_text)

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 4
    with x_money.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)

    block_0 = river_blocks.get(0)
    block_1 = river_blocks.get(1)
    assert block_1.src_owner_id == sal_text and block_1.dst_owner_id == tom_text
    assert block_1.river_tree_level == 1
    assert block_1.cash_start == 0.25
    assert block_1.cash_close == 1
    assert block_1.parent_block_num is None
    block_2 = river_blocks.get(2)
    block_3 = river_blocks.get(3)
    assert block_3.src_owner_id == tom_text and block_3.dst_owner_id == sal_text
    assert block_3.river_tree_level == 2
    assert block_3.parent_block_num == 1

    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        chartreasuryunits = get_chartreasuryunit_dict(treasury_conn, sal_text)
    assert len(chartreasuryunits) == 2
    river_sal_due_bob = chartreasuryunits.get(bob_text)
    river_sal_due_tom = chartreasuryunits.get(tom_text)

    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")

    assert river_sal_due_bob.due_total == 0.25
    assert river_sal_due_tom.due_total == 0.75


def test_MoneyUnit_set_cred_flow_for_world_CorrectlyPopulateschartreasuryunitTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 worlds, 85% of river blocks to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"

    sal_world = worldunit_shop(_owner_id=sal_text)
    sal_world.add_charunit(char_id=bob_text, credor_weight=2)
    sal_world.add_charunit(char_id=tom_text, credor_weight=7)
    sal_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(sal_world)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_charunit(char_id=sal_text, credor_weight=3)
    bob_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    tom_world = worldunit_shop(_owner_id=tom_text)
    tom_world.add_charunit(char_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_world(tom_world)

    ava_world = worldunit_shop(_owner_id=ava_text)
    x_money.userhub.save_job_world(ava_world)
    x_money.refresh_treasury_job_worlds_data()

    charunit_count_sqlstr = get_row_count_sqlstr("world_charunit")
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 6

    chartreasuryunit_count_sqlstr = (
        get_world_charunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_world(owner_id=sal_text)

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 6
    with x_money.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        chartreasuryunits = get_chartreasuryunit_dict(treasury_conn, sal_text)
    assert len(chartreasuryunits) == 2
    assert chartreasuryunits.get(bob_text) != None
    assert chartreasuryunits.get(tom_text) != None
    assert chartreasuryunits.get(ava_text) is None

    river_sal_due_bob = chartreasuryunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = chartreasuryunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_MoneyUnit_set_cred_flow_for_world_CorrectlyPopulateschartreasuryunitTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 worlds, 85% of river blocks to sal, left over %15 goes on endless loop
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_world = worldunit_shop(_owner_id=sal_text)
    sal_world.add_charunit(char_id=bob_text, credor_weight=2)
    sal_world.add_charunit(char_id=tom_text, credor_weight=7)
    sal_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(sal_world)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_charunit(char_id=sal_text, credor_weight=3)
    bob_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    tom_world = worldunit_shop(_owner_id=tom_text)
    tom_world.add_charunit(char_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_world(tom_world)

    ava_world = worldunit_shop(_owner_id=ava_text)
    ava_world.add_charunit(char_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_world(ava_world)

    elu_world = worldunit_shop(_owner_id=elu_text)
    elu_world.add_charunit(char_id=ava_text, credor_weight=2)
    x_money.userhub.save_job_world(elu_world)

    x_money.refresh_treasury_job_worlds_data()

    charunit_count_sqlstr = get_row_count_sqlstr("world_charunit")
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 8

    chartreasuryunit_count_sqlstr = (
        get_world_charunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_world(owner_id=sal_text)

    # THEN
    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    # with x_money.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        chartreasuryunits = get_chartreasuryunit_dict(treasury_conn, sal_text)
    assert len(chartreasuryunits) == 2
    assert chartreasuryunits.get(bob_text) != None
    assert chartreasuryunits.get(tom_text) != None
    assert chartreasuryunits.get(ava_text) is None

    river_sal_due_bob = chartreasuryunits.get(bob_text)
    print(f"{river_sal_due_bob=}")
    river_sal_due_tom = chartreasuryunits.get(tom_text)
    print(f"{river_sal_due_tom=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert river_sal_due_tom.due_total == 0.7


def test_MoneyUnit_set_cred_flow_for_world_CorrectlyPopulateschartreasuryunitTable05_v1(
    env_dir_setup_cleanup,
):
    # GIVEN 5 worlds, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_world = worldunit_shop(_owner_id=sal_text)
    sal_world.add_charunit(char_id=bob_text, credor_weight=2)
    sal_world.add_charunit(char_id=tom_text, credor_weight=7)
    sal_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(sal_world)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_charunit(char_id=sal_text, credor_weight=3)
    bob_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    tom_world = worldunit_shop(_owner_id=tom_text)
    tom_world.add_charunit(char_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_world(tom_world)

    ava_world = worldunit_shop(_owner_id=ava_text)
    ava_world.add_charunit(char_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_world(ava_world)

    elu_world = worldunit_shop(_owner_id=elu_text)
    elu_world.add_charunit(char_id=ava_text, credor_weight=19)
    elu_world.add_charunit(char_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_world(elu_world)

    x_money.refresh_treasury_job_worlds_data()

    charunit_count_sqlstr = get_row_count_sqlstr("world_charunit")
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 9

    chartreasuryunit_count_sqlstr = (
        get_world_charunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_world(owner_id=sal_text)

    # THEN
    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    # with x_money.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        chartreasuryunits = get_chartreasuryunit_dict(treasury_conn, sal_text)
    assert len(chartreasuryunits) == 2
    assert chartreasuryunits.get(bob_text) != None
    assert chartreasuryunits.get(tom_text) != None
    assert chartreasuryunits.get(elu_text) is None
    assert chartreasuryunits.get(ava_text) is None

    river_sal_due_bob = chartreasuryunits.get(bob_text)
    river_sal_due_tom = chartreasuryunits.get(tom_text)
    river_sal_due_elu = chartreasuryunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_MoneyUnit_set_cred_flow_for_world_CorrectlyUsesMaxblocksCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 worlds, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_world = worldunit_shop(_owner_id=sal_text)
    sal_world.add_charunit(char_id=bob_text, credor_weight=2)
    sal_world.add_charunit(char_id=tom_text, credor_weight=7)
    sal_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(sal_world)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_charunit(char_id=sal_text, credor_weight=3)
    bob_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    tom_world = worldunit_shop(_owner_id=tom_text)
    tom_world.add_charunit(char_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_world(tom_world)

    ava_world = worldunit_shop(_owner_id=ava_text)
    ava_world.add_charunit(char_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_world(ava_world)

    elu_world = worldunit_shop(_owner_id=elu_text)
    elu_world.add_charunit(char_id=ava_text, credor_weight=19)
    elu_world.add_charunit(char_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_world(elu_world)

    x_money.refresh_treasury_job_worlds_data()

    charunit_count_sqlstr = get_row_count_sqlstr("world_charunit")
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 9

    chartreasuryunit_count_sqlstr = (
        get_world_charunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    mbc = 13
    x_money.set_cred_flow_for_world(owner_id=sal_text, max_blocks_count=mbc)

    # THEN
    # with x_money.get_treasury_conn() as treasury_conn:
    #     river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == mbc
    )


def test_MoneyUnit_set_cred_flow_for_world_CorrectlyPopulateschartreasuryunitTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 worlds, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_world = worldunit_shop(_owner_id=sal_text)
    sal_world.add_charunit(char_id=bob_text, credor_weight=2)
    sal_world.add_charunit(char_id=tom_text, credor_weight=7)
    sal_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(sal_world)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_charunit(char_id=sal_text, credor_weight=3)
    bob_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    tom_world = worldunit_shop(_owner_id=tom_text)
    tom_world.add_charunit(char_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_world(tom_world)

    ava_world = worldunit_shop(_owner_id=ava_text)
    ava_world.add_charunit(char_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_world(ava_world)

    elu_world = worldunit_shop(_owner_id=elu_text)
    elu_world.add_charunit(char_id=ava_text, credor_weight=19)
    elu_world.add_charunit(char_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_world(elu_world)

    x_money.refresh_treasury_job_worlds_data()

    charunit_count_sqlstr = get_row_count_sqlstr("world_charunit")
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 9

    chartreasuryunit_count_sqlstr = (
        get_world_charunit_table_treasurying_attr_set_count_sqlstr()
    )
    river_block_count_sqlstr = get_row_count_sqlstr("river_block")
    assert get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 0
    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 0
    )

    # WHEN
    x_money.set_cred_flow_for_world(owner_id=sal_text)

    # THEN
    assert (
        get_single_result(x_money.get_treasury_conn(), river_block_count_sqlstr) == 40
    )
    with x_money.get_treasury_conn() as treasury_conn:
        river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result(x_money.get_treasury_conn(), chartreasuryunit_count_sqlstr)
        == 2
    )

    with x_money.get_treasury_conn() as treasury_conn:
        chartreasuryunits = get_chartreasuryunit_dict(treasury_conn, sal_text)
    chartreasuryunits = x_money.get_chartreasuryunits(sal_text)
    assert len(chartreasuryunits) == 2
    assert chartreasuryunits.get(bob_text) != None
    assert chartreasuryunits.get(tom_text) != None
    assert chartreasuryunits.get(elu_text) is None
    assert chartreasuryunits.get(ava_text) is None

    river_sal_due_bob = chartreasuryunits.get(bob_text)
    river_sal_due_tom = chartreasuryunits.get(tom_text)
    river_sal_due_elu = chartreasuryunits.get(elu_text)
    print(f"{river_sal_due_bob=}")
    print(f"{river_sal_due_tom=}")
    print(f"{river_sal_due_elu=}")

    assert round(river_sal_due_bob.due_total, 15) == 0.15
    assert round(river_sal_due_tom.due_total, 15) == 0.7


def test_MoneyUnit_set_cred_flow_for_world_CorrectlyBuildsASingle_ContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 worlds, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_world = worldunit_shop(_owner_id=sal_text)
    sal_world.add_charunit(char_id=bob_text, credor_weight=2)
    sal_world.add_charunit(char_id=tom_text, credor_weight=7)
    sal_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(sal_world)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_charunit(char_id=sal_text, credor_weight=3)
    bob_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    tom_world = worldunit_shop(_owner_id=tom_text)
    tom_world.add_charunit(char_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_world(tom_world)

    ava_world = worldunit_shop(_owner_id=ava_text)
    ava_world.add_charunit(char_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_world(ava_world)

    elu_world = worldunit_shop(_owner_id=elu_text)
    elu_world.add_charunit(char_id=ava_text, credor_weight=19)
    elu_world.add_charunit(char_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_world(elu_world)

    x_money.refresh_treasury_job_worlds_data()

    # WHEN
    x_money.set_cred_flow_for_world(owner_id=sal_text, max_blocks_count=100)

    # THEN
    count_range_fails_sql = """
    SELECT COUNT(*)
    FROM (
        SELECT 
            rt1.cash_start x_row_start
        , lag(cash_close) OVER (ORDER BY cash_start, cash_close) AS prev_close
        , lag(cash_close) OVER (ORDER BY cash_start, cash_close) - rt1.cash_start prev_diff
        , rt1.block_num or_block_num
        , lag(block_num) OVER (ORDER BY cash_start, cash_close) AS prev_block_num
        , rt1.parent_block_num or_parent_block_num
        , lag(parent_block_num) OVER (ORDER BY cash_start, cash_close) AS prev_parent_block_num
        , river_tree_level
        , lag(river_tree_level) OVER (ORDER BY cash_start, cash_close) AS prev_parent_river_tree_level
        FROM river_block rt1
        --  WHERE dst_owner_id = 'sal' and cash_master = dst_owner_id
        ORDER BY rt1.cash_start, rt1.cash_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_single_result(treasury_conn, count_range_fails_sql) == 0


def test_MoneyUnit_set_cred_flow_for_world_CorrectlyUpatesWorldCharUnits(
    env_dir_setup_cleanup,
):
    """GIVEN 5 worlds, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal"""
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_world_src = worldunit_shop(_owner_id=sal_text)
    sal_world_src.add_charunit(char_id=bob_text, credor_weight=2, debtor_weight=2)
    sal_world_src.add_charunit(char_id=tom_text, credor_weight=2, debtor_weight=1)
    sal_world_src.add_charunit(char_id=ava_text, credor_weight=2, debtor_weight=2)
    x_money.userhub.save_job_world(sal_world_src)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_charunit(char_id=sal_text, credor_weight=3)
    bob_world.add_charunit(char_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    tom_world = worldunit_shop(_owner_id=tom_text)
    tom_world.add_charunit(char_id=sal_text)
    x_money.userhub.save_job_world(tom_world)

    ava_world = worldunit_shop(_owner_id=ava_text)
    ava_world.add_charunit(char_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_world(ava_world)

    elu_world = worldunit_shop(_owner_id=elu_text)
    elu_world.add_charunit(char_id=ava_text, credor_weight=8)
    elu_world.add_charunit(char_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_world(elu_world)

    x_money.refresh_treasury_job_worlds_data()
    sal_world_before = x_money.userhub.get_job_world(owner_id=sal_text)

    x_money.set_cred_flow_for_world(owner_id=sal_text, max_blocks_count=100)
    assert len(sal_world_before._chars) == 3
    print(f"{len(sal_world_before._chars)=}")
    bob_char = sal_world_before._chars.get(bob_text)
    tom_char = sal_world_before._chars.get(tom_text)
    ava_char = sal_world_before._chars.get(ava_text)
    assert bob_char._treasury_due_paid is None
    assert tom_char._treasury_due_paid is None
    assert ava_char._treasury_due_paid is None
    assert bob_char._treasury_due_diff is None
    assert tom_char._treasury_due_diff is None
    assert ava_char._treasury_due_diff is None
    assert bob_char._treasury_voice_rank is None
    assert tom_char._treasury_voice_rank is None
    assert ava_char._treasury_voice_rank is None
    assert bob_char._treasury_voice_hx_lowest_rank is None
    assert tom_char._treasury_voice_hx_lowest_rank is None
    assert ava_char._treasury_voice_hx_lowest_rank is None

    # WHEN
    x_money.set_cred_flow_for_world(owner_id=sal_text)

    # THEN
    sal_chartreasuryunits = x_money.get_chartreasuryunits(owner_id=sal_text)
    assert len(sal_chartreasuryunits) == 2
    bob_chartreasury = sal_chartreasuryunits.get(bob_text)
    tom_chartreasury = sal_chartreasuryunits.get(tom_text)
    assert bob_chartreasury.due_owner_id == bob_text
    assert tom_chartreasury.due_owner_id == tom_text
    assert bob_chartreasury.cash_master == sal_text
    assert tom_chartreasury.cash_master == sal_text

    sal_world_after = x_money.userhub.get_job_world(owner_id=sal_text)
    bob_char = sal_world_after._chars.get(bob_text)
    tom_char = sal_world_after._chars.get(tom_text)
    ava_char = sal_world_after._chars.get(ava_text)
    elu_char = sal_world_after._chars.get(elu_text)

    assert bob_chartreasury.due_total == bob_char._treasury_due_paid
    assert bob_chartreasury.due_diff == bob_char._treasury_due_diff
    assert tom_chartreasury.due_total == tom_char._treasury_due_paid
    assert tom_chartreasury.due_diff == tom_char._treasury_due_diff
    assert elu_char is None

    # for chartreasury_uid, sal_chartreasuryunit in sal_chartreasuryunits.items():
    #     print(f"{chartreasury_uid=} {sal_chartreasuryunit=}")
    #     assert sal_chartreasuryunit.cash_master == sal_text
    #     assert sal_chartreasuryunit.due_owner_id in [bob_text, tom_text, elu_text]
    #     x_charunit = sal_world_after._chars.get(sal_chartreasuryunit.due_owner_id)
    #     if x_charunit != None:
    #         # print(
    #         #     f"{sal_chartreasuryunit.cash_master=} {sal_chartreasuryunit.due_owner_id=} {x_charunit.char_id=} due_total: {sal_chartreasuryunit.due_total} _Due_ Paid: {x_charunit._treasury_due_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_chartreasuryunit.cash_master=} {sal_chartreasuryunit.due_owner_id=} {x_charunit.char_id=} due_diff:  {sal_chartreasuryunit.due_diff} _Due_ Paid: {x_charunit._treasury_due_diff}"
    #         # )
    #         assert sal_chartreasuryunit.due_total == x_charunit._treasury_due_paid
    #         assert sal_chartreasuryunit.due_diff == x_charunit._treasury_due_diff

    assert sal_chartreasuryunits.get(ava_text) is None
    assert ava_char._treasury_due_paid is None
    assert ava_char._treasury_due_diff is None

    # for x_charunit in sal_world_after._chars.values():
    #     print(f"sal_world_after {x_charunit.char_id=} {x_charunit._treasury_due_paid=}")
    #     chartreasuryunit_x = sal_chartreasuryunits.get(x_charunit.char_id)
    #     if chartreasuryunit_x is None:
    #         assert x_charunit._treasury_due_paid is None
    #         assert x_charunit._treasury_due_diff is None
    #     else:
    #         assert x_charunit._treasury_due_paid != None
    #         assert x_charunit._treasury_due_diff != None
    # assert sal_world_after != sal_world_before
