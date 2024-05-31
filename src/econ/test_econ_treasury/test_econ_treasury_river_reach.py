from src._road.worldnox import econnox_shop
from src.agenda.agenda import agendaunit_shop, partyunit_shop
from src.econ.examples.econ_env_kit import (
    temp_real_id,
    temp_reals_dir,
    env_dir_setup_cleanup,
)
from src._instrument.sqlite import get_single_result
from src.econ.treasury_sqlstr import (
    get_river_reach_table_touch_select_sqlstr,
    get_river_circle_table_create_sqlstr,
    get_river_block_table_create_sqlstr,
    get_river_reach_table_create_sqlstr,
    get_river_reach_table_insert_sqlstr,
    get_river_reach_table_final_insert_sqlstr,
    get_agenda_partyunit_table_create_sqlstr,
    get_agenda_partyunit_table_insert_sqlstr,
    get_agenda_partyunit_table_update_credit_score_sqlstr,
    get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr,
)
from src._instrument.sqlite import get_single_result, get_row_count_sqlstr
from sqlite3 import connect as sqlite3_connect


def test_get_river_reach_table_insert_sqlstr_InsertsWithoutError():
    # GIVEN
    x_db = sqlite3_connect(":memory:")
    reach_text = "river_reach"
    with x_db as x_conn:
        x_conn.execute(get_river_reach_table_create_sqlstr())
        assert 0 == get_single_result(x_conn, get_row_count_sqlstr(reach_text))

    # WHEN
    select_example_sqlstr = """
SELECT 
  'Yao' cash_master
, 'Sue' src_owner_id
, 4 set_num
, 0.78 reach_coin_start
, 0.89 reach_coin_close
"""
    insert_sqlstr = get_river_reach_table_insert_sqlstr(select_example_sqlstr)
    with x_db as x_conn:
        x_conn.execute(insert_sqlstr)
    print(f"{insert_sqlstr=}")

    # THEN
    with x_db as x_conn:
        assert 1 == get_single_result(x_conn, get_row_count_sqlstr(reach_text))


def test_get_agenda_partyunit_table_update_credit_score_sqlstr_UpdatesWithoutError():
    # GIVEN
    x_db = sqlite3_connect(":memory:")
    partyunit_text = "agenda_partyunit"
    reach_text = "river_reach"
    with x_db as x_conn:
        x_conn.execute(get_agenda_partyunit_table_create_sqlstr())
        x_conn.execute(get_river_reach_table_create_sqlstr())
        assert 0 == get_single_result(x_conn, get_row_count_sqlstr(partyunit_text))
        assert 0 == get_single_result(x_conn, get_row_count_sqlstr(reach_text))

    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)

    bob_text = "Bob"
    cal_text = "Cal"
    dee_text = "Dee"
    bob_partyunit = partyunit_shop(bob_text)
    cal_partyunit = partyunit_shop(cal_text)
    dee_partyunit = partyunit_shop(dee_text)
    bob_s = 0.78
    cal_s = 0.1
    dee_s1 = 0.2
    dee_s2 = 0.6
    bob_close = 0.89
    cal_close = 0.33
    dee_close1 = 0.44
    dee_close2 = 0.61

    bob_select_sqlstr = f"SELECT '{yao_text}', '{bob_text}', 4, {bob_s}, {bob_close}"
    cal_select_sqlstr = f"SELECT '{yao_text}', '{cal_text}', 5, {cal_s}, {cal_close}"
    dee_select_sqlstr1 = f"SELECT '{yao_text}', '{dee_text}', 6, {dee_s1}, {dee_close1}"
    dee_select_sqlstr2 = f"SELECT '{yao_text}', '{dee_text}', 7, {dee_s2}, {dee_close2}"

    with x_db as x_conn:
        x_conn.execute(
            get_agenda_partyunit_table_insert_sqlstr(yao_agenda, bob_partyunit)
        )
        x_conn.execute(
            get_agenda_partyunit_table_insert_sqlstr(yao_agenda, cal_partyunit)
        )
        x_conn.execute(
            get_agenda_partyunit_table_insert_sqlstr(yao_agenda, dee_partyunit)
        )
        x_conn.execute(get_river_reach_table_insert_sqlstr(bob_select_sqlstr))
        x_conn.execute(get_river_reach_table_insert_sqlstr(cal_select_sqlstr))
        x_conn.execute(get_river_reach_table_insert_sqlstr(dee_select_sqlstr1))
        x_conn.execute(get_river_reach_table_insert_sqlstr(dee_select_sqlstr2))
        assert 3 == get_single_result(x_conn, get_row_count_sqlstr(partyunit_text))
        assert 4 == get_single_result(x_conn, get_row_count_sqlstr(reach_text))

    partyunit_select_str = f"""
SELECT 
  owner_id
, party_id
, _treasury_credit_score
FROM agenda_partyunit
WHERE owner_id = '{yao_text}'
"""
    with x_db as x_conn:
        results = x_conn.execute(partyunit_select_str)

    x_rows = results.fetchall()
    print(f"{x_rows=}")
    print(f"{x_rows[0]=}")
    print(f"{x_rows[0][0]=}")
    print(f"{x_rows[1]=}")
    print(f"{x_rows[2]=}")
    assert x_rows[0][1] == bob_text
    assert x_rows[1][1] == cal_text
    assert x_rows[2][1] == dee_text
    assert x_rows[0][2] is None
    assert x_rows[1][2] is None
    assert x_rows[2][2] is None

    # WHEN
    with x_db as x_conn:
        x_conn.execute(get_agenda_partyunit_table_update_credit_score_sqlstr(yao_text))

    # THEN
    with x_db as x_conn:
        results = x_conn.execute(partyunit_select_str)

    y_rows = results.fetchall()
    assert y_rows[0][1] == bob_text
    assert y_rows[1][1] == cal_text
    assert y_rows[2][1] == dee_text
    assert y_rows[0][2] != None
    assert y_rows[1][2] != None
    assert y_rows[2][2] != None
    assert y_rows[0][2] == bob_close - bob_s
    assert y_rows[1][2] == cal_close - cal_s
    assert y_rows[2][2] == (dee_close1 - dee_s1) + (dee_close2 - dee_s2)


def test_get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr_UpdatesWithoutError():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    bob_text = "Bob"
    cal_text = "Cal"
    dee_text = "Dee"
    bob_s = 0.78
    cal_s = 0.1
    dee_s1 = 0.2
    dee_s2 = 0.6
    bob_close = 0.89
    cal_close = 0.33
    dee_close1 = 0.44
    dee_close2 = 0.61
    bob_credit_score = bob_close - bob_s
    cal_credit_score = cal_close - cal_s
    dee_credit_score = (dee_close1 - dee_s1) + (dee_close2 - dee_s2)
    print(f"{bob_credit_score=}")
    print(f"{cal_credit_score=}")
    print(f"{dee_credit_score=}")
    bob_partyunit = partyunit_shop(bob_text)
    cal_partyunit = partyunit_shop(cal_text)
    dee_partyunit = partyunit_shop(dee_text)
    bob_partyunit.set_treasurying_data(None, None, bob_credit_score, None)
    cal_partyunit.set_treasurying_data(None, None, cal_credit_score, None)
    dee_partyunit.set_treasurying_data(None, None, dee_credit_score, None)
    print(f"{bob_partyunit._treasury_credit_score=}")
    print(f"{cal_partyunit._treasury_credit_score=}")
    print(f"{dee_partyunit._treasury_credit_score=}")

    partyunit_text = "agenda_partyunit"
    x_db = sqlite3_connect(":memory:")
    with x_db as x_conn:
        x_conn.execute(get_agenda_partyunit_table_create_sqlstr())
        x_conn.execute(
            get_agenda_partyunit_table_insert_sqlstr(yao_agenda, bob_partyunit)
        )
        x_conn.execute(
            get_agenda_partyunit_table_insert_sqlstr(yao_agenda, cal_partyunit)
        )
        x_conn.execute(
            get_agenda_partyunit_table_insert_sqlstr(yao_agenda, dee_partyunit)
        )
        assert 3 == get_single_result(x_conn, get_row_count_sqlstr(partyunit_text))

    partyunit_select_str = f"""
SELECT 
  owner_id
, party_id
, _treasury_credit_score
, _treasury_voice_rank
FROM agenda_partyunit
WHERE owner_id = '{yao_text}'
"""
    with x_db as x_conn:
        results = x_conn.execute(partyunit_select_str)

    x_rows = results.fetchall()
    print(f"{x_rows=}")
    print(f"{x_rows[0]=}")
    print(f"{x_rows[0][0]=}")
    print(f"{x_rows[1]=}")
    print(f"{x_rows[2]=}")
    assert x_rows[0][1] == bob_text
    assert x_rows[1][1] == cal_text
    assert x_rows[2][1] == dee_text
    assert x_rows[0][2] - bob_partyunit._treasury_credit_score < 0.000001
    assert x_rows[1][2] == cal_partyunit._treasury_credit_score
    assert x_rows[2][2] == dee_partyunit._treasury_credit_score
    assert x_rows[0][3] is None
    assert x_rows[1][3] is None
    assert x_rows[2][3] is None

    # WHEN
    with x_db as x_conn:
        x_conn.execute(
            get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr(yao_text)
        )

    # THEN
    with x_db as x_conn:
        results = x_conn.execute(partyunit_select_str)

    y_rows = results.fetchall()
    assert y_rows[0][1] == bob_text
    assert y_rows[1][1] == cal_text
    assert y_rows[2][1] == dee_text
    assert y_rows[0][3] != None
    assert y_rows[1][3] != None
    assert y_rows[2][3] != None
    print(f"{y_rows[0][2]=}")
    print(f"{y_rows[1][2]=}")
    print(f"{y_rows[2][2]=}")
    assert y_rows[0][3] == 3
    assert y_rows[1][3] == 2
    assert y_rows[2][3] == 1


# STEPS TO CALCULATE RIVER_REACH
# 1. from river_blocks select river_reach_touch:
#   all river_blocks that share a cash range with any river_circle
# 2. from river_reach_touch select river_reach_intersection:
#   every row of river_reach_touch with intersection of river_circle and river_block
# 3. from river_reach_intersection select river_reach_ordered:
#   every row of river_reach_intersection ordered by src_owner_id, coin_start, coin_close
# 4. from river_reach_ordered select river_reach_stepped:
#   every row of river_reach_ordered with column identifying sets of src_owner_id/intersecting curr ranges
# 5. from river_reach_stepped select river_reach_final:
#   one row for every river_reach_stepped set with min coin_start and max coin_close


def test_get_river_reach_table_touch_select_sqlstr_QuerySelectsCorrectResults():
    # def test_econ_river_reach_touch_sqlstr_CorrectlySelectsDataSet(
    #     env_dir_setup_cleanup,
    # ):
    #     # GIVEN
    #     ex7_text = "ex7"
    #     x_econ = _delete_and_set_ex6(x_real_id=ex7_text)
    #     sal_text = "Sal"
    #     # x_econ = _delete_and_set_ex6()
    #     # # x_econ.set_road_nodes(sal_text)
    #     # ex6_text = "ex6"
    #     # x_econ = econunit_shop(real_id=ex6_text, econ_dir=temp_reals_dir())
    #     # x_econ.set_road_nodes(sal_text)
    #     # x_econ.set_credit_flow_for_agenda(sal_text, max_blocks_count=100)

    #     # WHEN
    #     reach_sqlstr = get_river_reach_table_touch_select_sqlstr(sal_text)
    #     reach_count_sqlstr = f"""SELECT COUNT(*) FROM ({reach_sqlstr}) x;"""
    #     reach_rows_num = get_single_result(x_econ.get_x_conn(), reach_count_sqlstr)

    #     # THEN
    #     assert reach_rows_num == 94

    # GIVEN
    x_db = sqlite3_connect(":memory:")
    with x_db as x_conn:
        x_conn.execute(get_river_block_table_create_sqlstr())
        x_conn.execute(get_river_circle_table_create_sqlstr())
        x_conn.execute(get_river_reach_table_create_sqlstr())

    block_text = "river_block"
    circle_text = "river_circle"
    reach_text = "river_reach"
    with x_db as x_conn:
        assert 0 == get_single_result(x_conn, get_row_count_sqlstr(block_text))
        assert 0 == get_single_result(x_conn, get_row_count_sqlstr(circle_text))
        assert 0 == get_single_result(x_conn, get_row_count_sqlstr(reach_text))
    insert_block_values_str = """
INSERT INTO river_block (cash_master, src_owner_id, dst_owner_id, cash_start, cash_close, block_num, parent_block_num, river_tree_level)
VALUES ('Sal', 'Sal', 'Ava', 0.0, 0.1, 0, NULL, 1)
,('Sal', 'Sal', 'Bob', 0.1, 0.3, 1, NULL, 1)
,('Sal', 'Sal', 'Tom', 0.3, 1.0, 2, NULL, 1)
,('Sal', 'Ava', 'Elu', 0.0, 0.1, 3, 0, 2)
,('Sal', 'Bob', 'Ava', 0.1, 0.15, 4, 1, 2)
,('Sal', 'Bob', 'Sal', 0.15, 0.3, 5, 1, 2)
,('Sal', 'Tom', 'Sal', 0.3, 1.0, 6, 2, 2)
,('Sal', 'Elu', 'Ava', 0.0, 0.095, 7, 3, 3)
,('Sal', 'Elu', 'Sal', 0.095, 0.1, 8, 3, 3)
,('Sal', 'Ava', 'Elu', 0.1, 0.15, 9, 4, 3)
,('Sal', 'Ava', 'Elu', 0.0, 0.095, 10, 7, 4)
,('Sal', 'Elu', 'Ava', 0.1, 0.1475, 11, 9, 4)
,('Sal', 'Elu', 'Sal', 0.1475, 0.15, 12, 9, 4)
,('Sal', 'Elu', 'Ava', 0.0, 0.09025, 13, 10, 5)
,('Sal', 'Elu', 'Sal', 0.09025, 0.095, 14, 10, 5)
,('Sal', 'Ava', 'Elu', 0.1, 0.1475, 15, 11, 5)
,('Sal', 'Ava', 'Elu', 0.0, 0.09025, 16, 13, 6)
,('Sal', 'Elu', 'Ava', 0.1, 0.145125, 17, 15, 6)
,('Sal', 'Elu', 'Sal', 0.145125, 0.1475, 18, 15, 6)
,('Sal', 'Elu', 'Ava', 0.0, 0.0857375, 19, 16, 7)
,('Sal', 'Elu', 'Sal', 0.0857375, 0.09025, 20, 16, 7)
,('Sal', 'Ava', 'Elu', 0.1, 0.145125, 21, 17, 7)
,('Sal', 'Ava', 'Elu', 0.0, 0.0857375, 22, 19, 8)
,('Sal', 'Elu', 'Ava', 0.1, 0.14286875, 23, 21, 8)
,('Sal', 'Elu', 'Sal', 0.14286875, 0.145125, 24, 21, 8)
,('Sal', 'Elu', 'Ava', 0.0, 0.081450625, 25, 22, 9)
,('Sal', 'Elu', 'Sal', 0.081450625, 0.0857375, 26, 22, 9)
,('Sal', 'Ava', 'Elu', 0.1, 0.14286875, 27, 23, 9)
,('Sal', 'Ava', 'Elu', 0.0, 0.081450625, 28, 25, 10)
,('Sal', 'Elu', 'Ava', 0.1, 0.1407253125, 29, 27, 10)
,('Sal', 'Elu', 'Sal', 0.1407253125, 0.14286875, 30, 27, 10)
,('Sal', 'Elu', 'Ava', 0.0, 0.07737809375, 31, 28, 11)
,('Sal', 'Elu', 'Sal', 0.07737809375, 0.081450625, 32, 28, 11)
,('Sal', 'Ava', 'Elu', 0.1, 0.1407253125, 33, 29, 11)
,('Sal', 'Ava', 'Elu', 0.0, 0.07737809375, 34, 31, 12)
,('Sal', 'Elu', 'Ava', 0.1, 0.138689046875, 35, 33, 12)
,('Sal', 'Elu', 'Sal', 0.138689046875, 0.1407253125, 36, 33, 12)
,('Sal', 'Elu', 'Ava', 0.0, 0.0735091890625, 37, 34, 13)
,('Sal', 'Elu', 'Sal', 0.0735091890625, 0.07737809375, 38, 34, 13)
,('Sal', 'Ava', 'Elu', 0.1, 0.138689046875, 39, 35, 13)
,('Sal', 'Ava', 'Elu', 0.0, 0.0735091890625, 40, 37, 14)
,('Sal', 'Elu', 'Ava', 0.1, 0.13675459453125, 41, 39, 14)
,('Sal', 'Elu', 'Sal', 0.13675459453125, 0.138689046875, 42, 39, 14)
,('Sal', 'Elu', 'Ava', 0.0, 0.069833729609375, 43, 40, 15)
,('Sal', 'Elu', 'Sal', 0.069833729609375, 0.0735091890625, 44, 40, 15)
,('Sal', 'Ava', 'Elu', 0.1, 0.13675459453125, 45, 41, 15)
,('Sal', 'Ava', 'Elu', 0.0, 0.069833729609375, 46, 43, 16)
,('Sal', 'Elu', 'Ava', 0.1, 0.134916864804687, 47, 45, 16)
,('Sal', 'Elu', 'Sal', 0.134916864804687, 0.13675459453125, 48, 45, 16)
,('Sal', 'Elu', 'Ava', 0.0, 0.0663420431289062, 49, 46, 17)
,('Sal', 'Elu', 'Sal', 0.0663420431289062, 0.069833729609375, 50, 46, 17)
,('Sal', 'Ava', 'Elu', 0.1, 0.134916864804687, 51, 47, 17)
,('Sal', 'Ava', 'Elu', 0.0, 0.0663420431289062, 52, 49, 18)
,('Sal', 'Elu', 'Ava', 0.1, 0.133171021564453, 53, 51, 18)
,('Sal', 'Elu', 'Sal', 0.133171021564453, 0.134916864804687, 54, 51, 18)
,('Sal', 'Elu', 'Ava', 0.0, 0.0630249409724609, 55, 52, 19)
,('Sal', 'Elu', 'Sal', 0.0630249409724609, 0.0663420431289062, 56, 52, 19)
,('Sal', 'Ava', 'Elu', 0.1, 0.133171021564453, 57, 53, 19)
,('Sal', 'Ava', 'Elu', 0.0, 0.0630249409724609, 58, 55, 20)
,('Sal', 'Elu', 'Ava', 0.1, 0.13151247048623, 59, 57, 20)
,('Sal', 'Elu', 'Sal', 0.13151247048623, 0.133171021564453, 60, 57, 20)
,('Sal', 'Elu', 'Ava', 0.0, 0.0598736939238379, 61, 58, 21)
,('Sal', 'Elu', 'Sal', 0.0598736939238379, 0.0630249409724609, 62, 58, 21)
,('Sal', 'Ava', 'Elu', 0.1, 0.13151247048623, 63, 59, 21)
,('Sal', 'Ava', 'Elu', 0.0, 0.0598736939238379, 64, 61, 22)
,('Sal', 'Elu', 'Ava', 0.1, 0.129936846961919, 65, 63, 22)
,('Sal', 'Elu', 'Sal', 0.129936846961919, 0.13151247048623, 66, 63, 22)
,('Sal', 'Elu', 'Ava', 0.0, 0.056880009227646, 67, 64, 23)
,('Sal', 'Elu', 'Sal', 0.056880009227646, 0.0598736939238379, 68, 64, 23)
,('Sal', 'Ava', 'Elu', 0.1, 0.129936846961919, 69, 65, 23)
,('Sal', 'Ava', 'Elu', 0.0, 0.056880009227646, 70, 67, 24)
,('Sal', 'Elu', 'Ava', 0.1, 0.128440004613823, 71, 69, 24)
,('Sal', 'Elu', 'Sal', 0.128440004613823, 0.129936846961919, 72, 69, 24)
,('Sal', 'Elu', 'Ava', 0.0, 0.0540360087662637, 73, 70, 25)
,('Sal', 'Elu', 'Sal', 0.0540360087662637, 0.056880009227646, 74, 70, 25)
,('Sal', 'Ava', 'Elu', 0.1, 0.128440004613823, 75, 71, 25)
,('Sal', 'Ava', 'Elu', 0.0, 0.0540360087662637, 76, 73, 26)
,('Sal', 'Elu', 'Ava', 0.1, 0.127018004383132, 77, 75, 26)
,('Sal', 'Elu', 'Sal', 0.127018004383132, 0.128440004613823, 78, 75, 26)
,('Sal', 'Elu', 'Ava', 0.0, 0.0513342083279505, 79, 76, 27)
,('Sal', 'Elu', 'Sal', 0.0513342083279505, 0.0540360087662637, 80, 76, 27)
,('Sal', 'Ava', 'Elu', 0.1, 0.127018004383132, 81, 77, 27)
,('Sal', 'Ava', 'Elu', 0.0, 0.0513342083279505, 82, 79, 28)
,('Sal', 'Elu', 'Ava', 0.1, 0.125667104163975, 83, 81, 28)
,('Sal', 'Elu', 'Sal', 0.125667104163975, 0.127018004383132, 84, 81, 28)
,('Sal', 'Elu', 'Ava', 0.0, 0.048767497911553, 85, 82, 29)
,('Sal', 'Elu', 'Sal', 0.048767497911553, 0.0513342083279505, 86, 82, 29)
,('Sal', 'Ava', 'Elu', 0.1, 0.125667104163975, 87, 83, 29)
,('Sal', 'Ava', 'Elu', 0.0, 0.048767497911553, 88, 85, 30)
,('Sal', 'Elu', 'Ava', 0.1, 0.124383748955776, 89, 87, 30)
,('Sal', 'Elu', 'Sal', 0.124383748955776, 0.125667104163975, 90, 87, 30)
,('Sal', 'Elu', 'Ava', 0.0, 0.0463291230159753, 91, 88, 31)
,('Sal', 'Elu', 'Sal', 0.0463291230159753, 0.048767497911553, 92, 88, 31)
,('Sal', 'Ava', 'Elu', 0.1, 0.124383748955776, 93, 89, 31)
,('Sal', 'Ava', 'Elu', 0.0, 0.0463291230159753, 94, 91, 32)
,('Sal', 'Elu', 'Ava', 0.1, 0.123164561507988, 95, 93, 32)
,('Sal', 'Elu', 'Sal', 0.123164561507988, 0.124383748955776, 96, 93, 32)
,('Sal', 'Elu', 'Ava', 0.0, 0.0440126668651765, 97, 94, 33)
,('Sal', 'Elu', 'Sal', 0.0440126668651765, 0.0463291230159753, 98, 94, 33)
,('Sal', 'Ava', 'Elu', 0.1, 0.123164561507988, 99, 95, 33)
;
"""
    insert_circle_values_str = """
INSERT INTO river_circle (cash_master, dst_owner_id, circle_num, coin_start, coin_close)
VALUES ('Sal', 'Sal', 0, 0.0440126668651765, 0.1)
, ('Sal', 'Sal', 1, 0.123164561507988, 1.0)
;
"""
    with x_db as x_conn:
        x_conn.execute(insert_block_values_str)
        x_conn.execute(insert_circle_values_str)

        assert 100 == get_single_result(x_db, get_row_count_sqlstr(block_text))
        assert 2 == get_single_result(x_db, get_row_count_sqlstr(circle_text))

    # WHEN
    sal_text = "Sal"
    reach_sqlstr = get_river_reach_table_touch_select_sqlstr(sal_text)
    reach_count_sqlstr = f"""SELECT COUNT(*) FROM ({reach_sqlstr}) x;"""
    reach_rows_num = get_single_result(x_db, reach_count_sqlstr)

    # THEN
    assert reach_rows_num == 94

    # WHEN
    reach_insert_sqlstr = get_river_reach_table_final_insert_sqlstr(sal_text)
    with x_db as x_conn:
        x_conn.execute(reach_insert_sqlstr)

    # THEN
    with x_db as x_conn:
        assert 6 == get_single_result(x_conn, get_row_count_sqlstr(reach_text))
