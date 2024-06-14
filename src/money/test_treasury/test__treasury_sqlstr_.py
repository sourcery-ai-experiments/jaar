from src.agenda.agenda import agendaunit_shop
from src.money.treasury_sqlstr import (
    get_agendaunit_table_create_sqlstr,
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
    get_agenda_partyunit_table_create_sqlstr,
    get_agenda_partyunit_table_update_treasury_due_paid_sqlstr,
    get_agenda_partyunit_table_update_cred_score_sqlstr,
    get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr,
    get_river_reach_table_touch_select_sqlstr,
    get_river_reach_table_final_select_sqlstr,
    get_river_reach_table_create_sqlstr,
    get_river_reach_table_insert_sqlstr,
    get_river_score_select_sqlstr,
)
from src._instrument.sqlite import sqlite_text


def test_get_agendaunit_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN /  WHEN
    gen_sqlstr = get_agendaunit_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS agendaunit (
  owner_id VARCHAR(255) PRIMARY KEY ASC
, real_id VARCHAR(255) NOT NULL
, rational INT NULL
, UNIQUE(owner_id)
)
;
"""
    assert gen_sqlstr == example_sqlstr


def test_get_agendaunit_update_sqlstr_ReturnsCorrectStr():
    # GIVEN
    bob_owner_id = "Bob"
    bob_rational = False
    bob_agenda = agendaunit_shop(_owner_id=bob_owner_id)
    bob_agenda._rational = bob_rational

    # WHEN
    gen_sqlstr = get_agendaunit_update_sqlstr(agenda=bob_agenda)

    # THEN
    example_sqlstr = f"""
UPDATE agendaunit
SET rational = {sqlite_text(bob_rational)}
WHERE owner_id = '{bob_owner_id}'
;
"""
    assert gen_sqlstr == example_sqlstr


def test_get_agendaunits_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_agendaunits_select_sqlstr()

    # THEN
    example_sqlstr = """
SELECT 
  owner_id
, rational
FROM agendaunit
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_partyunit_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    bob_text = "Bob"
    generated_sqlstr = get_agenda_partyunit_table_update_treasury_due_paid_sqlstr(
        bob_text
    )

    # THEN
    example_sqlstr = f"""
UPDATE agenda_partyunit
SET _treasury_due_paid = (
    SELECT SUM(block.cash_close-block.cash_start) 
    FROM river_block block
    WHERE block.cash_master='{bob_text}' 
        AND block.dst_owner_id=block.cash_master
        AND block.src_owner_id = agenda_partyunit.party_id
    )
WHERE EXISTS (
    SELECT block.cash_close
    FROM river_block block
    WHERE agenda_partyunit.owner_id='{bob_text}' 
        AND agenda_partyunit.party_id = block.dst_owner_id
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_reach_table_touch_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    bob_text = "Bob"
    generated_sqlstr = get_river_reach_table_touch_select_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
    SELECT 
    block.cash_master
    , block.src_owner_id src
    , block.dst_owner_id dst
    , CASE 
        WHEN block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_start
            AND block.cash_close <= circle.coin_close
            THEN circle.coin_start --'leftside' 
        WHEN block.cash_start >= circle.coin_start 
            AND block.cash_start < circle.coin_close
            AND block.cash_close > circle.coin_close
            THEN block.cash_start --'rightside' 
        WHEN block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_close
            THEN circle.coin_start --'outside' 
        WHEN block.cash_start >= circle.coin_start 
            AND block.cash_close <= circle.coin_close
            THEN block.cash_start --'inside' 
            END reach_start
    , CASE 
        WHEN block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_start
            AND block.cash_close <= circle.coin_close
            THEN block.cash_close --'leftside' 
        WHEN block.cash_start >= circle.coin_start 
            AND block.cash_start < circle.coin_close
            AND block.cash_close > circle.coin_close
            THEN circle.coin_close --'rightside' 
        WHEN block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_close
            THEN circle.coin_close --'outside' 
        WHEN block.cash_start >= circle.coin_start 
            AND block.cash_close <= circle.coin_close
            THEN block.cash_close --'inside' 
            END reach_close
    FROM river_block block
    JOIN river_circle circle on 
            (block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_close)
        OR     (block.cash_start >= circle.coin_start 
            AND block.cash_close <= circle.coin_close)
        OR     (block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_start
            AND block.cash_close <= circle.coin_close)
        OR     (block.cash_start >= circle.coin_start 
            AND block.cash_start < circle.coin_close
            AND block.cash_close > circle.coin_close)
    WHERE block.cash_master = '{bob_text}'
        AND block.src_owner_id != block.cash_master
    ORDER BY 
    block.src_owner_id
    , block.dst_owner_id
    , block.cash_start
    , block.cash_close
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_reach_table_final_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    bob_text = "Bob"
    generated_sqlstr = get_river_reach_table_final_select_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
WITH reach_inter(coin_mstr, src, dst, reach_start, reach_close) AS (
{get_river_reach_table_touch_select_sqlstr(bob_text)}
),
reach_order(
  coin_mstr
, src
, prev_src
, src_step
, reach_start
, prev_start
, range_step
, reach_close
, prev_close
) AS (
    SELECT 
    reach_inter.coin_mstr
    , reach_inter.src
    , IFNULL(
        LAG(reach_inter.src, 1) OVER(ORDER BY 
        reach_inter.src
        , reach_inter.dst
        , reach_inter.reach_start
        , reach_inter.reach_close
        )
      , reach_inter.src) prev_src
    , CASE 
        WHEN 
          IFNULL(
            LAG(reach_inter.src, 1) OVER(ORDER BY 
            reach_inter.src
            , reach_inter.dst
            , reach_inter.reach_start
            , reach_inter.reach_close
            )
          , reach_inter.src) 
          = reach_inter.src
        THEN 0
        ELSE 1
        END src_step
    , reach_inter.reach_start
    , IFNULL(
        LAG(reach_start, 1) OVER(ORDER BY 
        reach_inter.src
        , reach_inter.dst
        , reach_inter.reach_start
        , reach_inter.reach_close
        ) 
      , reach_start) prev_start
    , CASE
      WHEN
        IFNULL(
        LAG(reach_close, 1) OVER(ORDER BY 
        reach_inter.src
        , reach_inter.dst
        , reach_inter.reach_start
        , reach_inter.reach_close
        ) 
      , reach_close) < reach_inter.reach_start
      THEN 1
      ELSE 0
      END range_step
    , reach_inter.reach_close
    , IFNULL(
        LAG(reach_close, 1) OVER(ORDER BY 
        reach_inter.src
        , reach_inter.dst
        , reach_inter.reach_start
        , reach_inter.reach_close
        ) 
      , reach_close) prev_close
    FROM reach_inter
) 
, reach_step (  
  coin_mstr
, src
, prev_src
, src_step
, range_step
, delta_step
, prev_start
, prev_close
, reach_start
, reach_close
) AS (
    SELECT
    coin_mstr
    , src
    , prev_src
    , src_step
    , range_step
    , CASE 
        WHEN src_step =1 AND range_step =1 
        THEN 1
        ELSE src_step + range_step
        END delta_step
    , prev_start
    , prev_close
    , reach_start
    , reach_close
    FROM reach_order
)
, reach_sets_num (  
  coin_mstr
, src
, set_num
, prev_start
, prev_close
, reach_start
, reach_close
) AS (
    SELECT
      coin_mstr
    , src
    , SUM(delta_step) OVER (ORDER BY src, reach_start, reach_close) set_num
    , prev_start
    , prev_close
    , reach_start
    , reach_close
    FROM reach_step
)
SELECT 
  coin_mstr
, src
, set_num 
, MIN(reach_start) reach_start
, MAX(reach_close) reach_close
FROM reach_sets_num
GROUP BY coin_mstr, src, set_num
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_reach_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_river_reach_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS river_reach (
  cash_master VARCHAR(255) NOT NULL
, src_owner_id VARCHAR(255) NOT NULL
, set_num INT NOT NULL
, reach_coin_start FLOAT NOT NULL
, reach_coin_close FLOAT NOT NULL
, FOREIGN KEY(cash_master) REFERENCES agendaunit(owner_id)
, FOREIGN KEY(src_owner_id) REFERENCES agendaunit(owner_id)
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_reach_table_insert_sqlstr_ReturnsCorrectStr():
    # GIVEN
    select_example_sqlstr = """
SELECT 
  'Yao' cash_master
, 'Sue' src_owner_id
, 4 set_num
, 0.78 reach_coin_start
, 0.89 reach_coin_close
"""

    # WHEN
    generated_sqlstr = get_river_reach_table_insert_sqlstr(select_example_sqlstr)

    # THEN
    example_sqlstr = f"""
INSERT INTO river_reach (cash_master, src_owner_id, set_num, reach_coin_start, reach_coin_close)
{select_example_sqlstr}
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_score_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    yao_text = "Yao"
    generated_sqlstr = get_river_score_select_sqlstr(yao_text)

    # THEN
    example_sqlstr = f"""
SELECT 
  cash_master
, src_owner_id
, SUM(reach_coin_close - reach_coin_start) range_sum
FROM river_reach
WHERE cash_master = '{yao_text}'
GROUP BY cash_master, src_owner_id
ORDER BY range_sum DESC
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_agenda_partyunit_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_agenda_partyunit_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS agenda_partyunit (
  owner_id VARCHAR(255) NOT NULL 
, party_id VARCHAR(255) NOT NULL
, _agenda_cred FLOAT
, _agenda_debt FLOAT
, _agenda_intent_cred FLOAT
, _agenda_intent_debt FLOAT
, _agenda_intent_ratio_cred FLOAT
, _agenda_intent_ratio_debt FLOAT
, _credor_operational INT
, _debtor_operational INT
, _treasury_due_paid FLOAT
, _treasury_due_diff FLOAT
, _treasury_cred_score FLOAT
, _treasury_voice_rank INT
, _treasury_voice_hx_lowest_rank INT
, FOREIGN KEY(owner_id) REFERENCES agendaunit(owner_id)
, FOREIGN KEY(party_id) REFERENCES agendaunit(owner_id)
, UNIQUE(owner_id, party_id)
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_agenda_partyunit_table_update_cred_score_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    yao_text = "Yao"
    generated_sqlstr = get_agenda_partyunit_table_update_cred_score_sqlstr(yao_text)

    # THEN
    example_sqlstr = f"""
UPDATE agenda_partyunit
SET _treasury_cred_score = (
    SELECT SUM(reach_coin_close - reach_coin_start) range_sum
    FROM river_reach reach
    WHERE reach.cash_master = agenda_partyunit.owner_id
        AND reach.src_owner_id = agenda_partyunit.party_id
    )
WHERE agenda_partyunit.owner_id = '{yao_text}'
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    yao_text = "Yao"
    generated_sqlstr = get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr(
        yao_text
    )

    # THEN
    example_sqlstr = f"""
UPDATE agenda_partyunit
SET _treasury_voice_rank = 
    (
    SELECT rn
    FROM (
        SELECT p2.party_id
        , row_number() over (order by p2._treasury_cred_score DESC) rn
        FROM agenda_partyunit p2
        WHERE p2.owner_id = '{yao_text}'
    ) p3
    WHERE p3.party_id = agenda_partyunit.party_id AND agenda_partyunit.owner_id = '{yao_text}'
    )
WHERE agenda_partyunit.owner_id = '{yao_text}'
;
"""
    assert generated_sqlstr == example_sqlstr
