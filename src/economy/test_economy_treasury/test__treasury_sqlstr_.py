from src.agenda.agenda import agendaunit_shop
from src.economy.treasury_sqlstr import (
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
    get_agenda_partyunit_table_create_sqlstr,
    get_agenda_partyunit_table_update_treasury_tax_paid_sqlstr,
    get_agenda_partyunit_table_update_credit_score_sqlstr,
    get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr,
    get_river_reach_table_touch_select_sqlstr,
    get_river_reach_table_final_select_sqlstr,
    get_river_reach_table_create_sqlstr,
    get_river_reach_table_insert_sqlstr,
    get_river_score_select_sqlstr,
)
from src.tools.sqlite import sqlite_text


def test_get_agendaunit_update_sqlstr_ReturnsCorrectStr():
    # GIVEN
    bob_agent_id = "Bob"
    bob_rational = False
    bob_agenda = agendaunit_shop(_agent_id=bob_agent_id)
    bob_agenda._rational = bob_rational

    # WHEN
    gen_sqlstr = get_agendaunit_update_sqlstr(agenda=bob_agenda)

    # THEN
    example_sqlstr = f"""
UPDATE agendaunit
SET rational = {sqlite_text(bob_rational)}
WHERE agent_id = '{bob_agent_id}'
;
"""
    assert gen_sqlstr == example_sqlstr


def test_get_agendaunits_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_agendaunits_select_sqlstr()

    # THEN
    example_sqlstr = """
SELECT 
  agent_id
, rational
FROM agendaunit
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_partyunit_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    bob_text = "bob"
    generated_sqlstr = get_agenda_partyunit_table_update_treasury_tax_paid_sqlstr(
        bob_text
    )

    # THEN
    example_sqlstr = f"""
UPDATE agenda_partyunit
SET _treasury_tax_paid = (
    SELECT SUM(block.currency_close-block.currency_start) 
    FROM river_block block
    WHERE block.currency_master='{bob_text}' 
        AND block.dst_agent_id=block.currency_master
        AND block.src_agent_id = agenda_partyunit.party_id
    )
WHERE EXISTS (
    SELECT block.currency_close
    FROM river_block block
    WHERE agenda_partyunit.agent_id='{bob_text}' 
        AND agenda_partyunit.party_id = block.dst_agent_id
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_reach_table_touch_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    bob_text = "bob"
    generated_sqlstr = get_river_reach_table_touch_select_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
    SELECT 
    block.currency_master
    , block.src_agent_id src
    , block.dst_agent_id dst
    , CASE 
        WHEN block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_start
            AND block.currency_close <= circle.curr_close
            THEN circle.curr_start --'leftside' 
        WHEN block.currency_start >= circle.curr_start 
            AND block.currency_start < circle.curr_close
            AND block.currency_close > circle.curr_close
            THEN block.currency_start --'rightside' 
        WHEN block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_close
            THEN circle.curr_start --'outside' 
        WHEN block.currency_start >= circle.curr_start 
            AND block.currency_close <= circle.curr_close
            THEN block.currency_start --'inside' 
            END reach_start
    , CASE 
        WHEN block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_start
            AND block.currency_close <= circle.curr_close
            THEN block.currency_close --'leftside' 
        WHEN block.currency_start >= circle.curr_start 
            AND block.currency_start < circle.curr_close
            AND block.currency_close > circle.curr_close
            THEN circle.curr_close --'rightside' 
        WHEN block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_close
            THEN circle.curr_close --'outside' 
        WHEN block.currency_start >= circle.curr_start 
            AND block.currency_close <= circle.curr_close
            THEN block.currency_close --'inside' 
            END reach_close
    FROM river_block block
    JOIN river_circle circle on 
            (block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_close)
        OR     (block.currency_start >= circle.curr_start 
            AND block.currency_close <= circle.curr_close)
        OR     (block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_start
            AND block.currency_close <= circle.curr_close)
        OR     (block.currency_start >= circle.curr_start 
            AND block.currency_start < circle.curr_close
            AND block.currency_close > circle.curr_close)
    WHERE block.currency_master = '{bob_text}'
        AND block.src_agent_id != block.currency_master
    ORDER BY 
    block.src_agent_id
    , block.dst_agent_id
    , block.currency_start
    , block.currency_close
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_reach_table_final_select_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    bob_text = "bob"
    generated_sqlstr = get_river_reach_table_final_select_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
WITH reach_inter(curr_mstr, src, dst, reach_start, reach_close) AS (
{get_river_reach_table_touch_select_sqlstr(bob_text)}
),
reach_order(
  curr_mstr
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
    reach_inter.curr_mstr
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
  curr_mstr
, src
, prev_src
, src_step
, range_step
, change_step
, prev_start
, prev_close
, reach_start
, reach_close
) AS (
    SELECT
    curr_mstr
    , src
    , prev_src
    , src_step
    , range_step
    , CASE 
        WHEN src_step =1 AND range_step =1 
        THEN 1
        ELSE src_step + range_step
        END change_step
    , prev_start
    , prev_close
    , reach_start
    , reach_close
    FROM reach_order
)
, reach_sets_num (  
  curr_mstr
, src
, set_num
, prev_start
, prev_close
, reach_start
, reach_close
) AS (
    SELECT
      curr_mstr
    , src
    , SUM(change_step) OVER (ORDER BY src, reach_start, reach_close) set_num
    , prev_start
    , prev_close
    , reach_start
    , reach_close
    FROM reach_step
)
SELECT 
  curr_mstr
, src
, set_num 
, MIN(reach_start) reach_start
, MAX(reach_close) reach_close
FROM reach_sets_num
GROUP BY curr_mstr, src, set_num
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_reach_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_river_reach_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS river_reach (
  currency_master VARCHAR(255) NOT NULL
, src_agent_id VARCHAR(255) NOT NULL
, set_num INT NOT NULL
, reach_curr_start FLOAT NOT NULL
, reach_curr_close FLOAT NOT NULL
, FOREIGN KEY(currency_master) REFERENCES agendaunit(agent_id)
, FOREIGN KEY(src_agent_id) REFERENCES agendaunit(agent_id)
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_river_reach_table_insert_sqlstr_ReturnsCorrectStr():
    # GIVEN
    select_example_sqlstr = """
SELECT 
  'Yao' currency_master
, 'Sue' src_agent_id
, 4 set_num
, 0.78 reach_curr_start
, 0.89 reach_curr_close
"""

    # WHEN
    generated_sqlstr = get_river_reach_table_insert_sqlstr(select_example_sqlstr)

    # THEN
    example_sqlstr = f"""
INSERT INTO river_reach (currency_master, src_agent_id, set_num, reach_curr_start, reach_curr_close)
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
  currency_master
, src_agent_id
, SUM(reach_curr_close - reach_curr_start) range_sum
FROM river_reach
WHERE currency_master = '{yao_text}'
GROUP BY currency_master, src_agent_id
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
  agent_id VARCHAR(255) NOT NULL 
, party_id VARCHAR(255) NOT NULL
, _agenda_credit FLOAT
, _agenda_debt FLOAT
, _agenda_intent_credit FLOAT
, _agenda_intent_debt FLOAT
, _agenda_intent_ratio_credit FLOAT
, _agenda_intent_ratio_debt FLOAT
, _creditor_live INT
, _debtor_live INT
, _treasury_tax_paid FLOAT
, _treasury_tax_diff FLOAT
, _treasury_credit_score FLOAT
, _treasury_voice_rank INT
, _treasury_voice_hx_lowest_rank INT
, FOREIGN KEY(agent_id) REFERENCES agendaunit(agent_id)
, FOREIGN KEY(party_id) REFERENCES agendaunit(agent_id)
, UNIQUE(agent_id, party_id)
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_agenda_partyunit_table_update_credit_score_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    yao_text = "Yao"
    generated_sqlstr = get_agenda_partyunit_table_update_credit_score_sqlstr(yao_text)

    # THEN
    example_sqlstr = f"""
UPDATE agenda_partyunit
SET _treasury_credit_score = (
    SELECT SUM(reach_curr_close - reach_curr_start) range_sum
    FROM river_reach reach
    WHERE reach.currency_master = agenda_partyunit.agent_id
        AND reach.src_agent_id = agenda_partyunit.party_id
    )
WHERE agenda_partyunit.agent_id = '{yao_text}'
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
        , row_number() over (order by p2._treasury_credit_score DESC) rn
        FROM agenda_partyunit p2
        WHERE p2.agent_id = '{yao_text}'
    ) p3
    WHERE p3.party_id = agenda_partyunit.party_id AND agenda_partyunit.agent_id = '{yao_text}'
    )
WHERE agenda_partyunit.agent_id = '{yao_text}'
;
"""
    assert generated_sqlstr == example_sqlstr
