from src.economy.treasury_sqlstr import (
    get_calendar_table_create_sqlstr,
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
)


def test_get_calendar_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_calendar_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS calendar (
  healer VARCHAR(255) NOT NULL
, time_road VARCHAR(10000) NOT NULL
, report_date_range_start INT NOT NULL
, report_date_range_cease INT NOT NULL
, report_interval_length INT NOT NULL
, report_interval_intent_task_count INT NOT NULL
, report_interval_intent_state_count INT NOT NULL
, time_begin INT NOT NULL
, time_close INT NOT NULL
, intent_idea_road VARCHAR(255) NOT NULL
, intent_weight INT NOT NULL
, task INT NOT NULL
, FOREIGN KEY(healer) REFERENCES agendaunit(healer)
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_calendar_table_insert_sqlstr_ReturnsCorrectStr():
    # GIVEN
    select_example_sqlstr = """
SELECT 
  'Yao' healer
, 'A,time,jajatime' time_road
, 1000000600 report_date_range_start
, 1000000900 report_date_range_cease
, 15 report_interval_length
, 11 report_interval_intent_task_count
, 7 report_interval_intent_state_count
, 1000000615 time_begin
, 1000000630 time_close
, 'A,casa,cleaning,clean fridge' intent_idea_road
, 0.5 intent_weight
, 1 task
"""

    # WHEN
    generated_sqlstr = get_calendar_table_insert_sqlstr(select_example_sqlstr)

    # THEN
    example_sqlstr = f"""
INSERT INTO calendar (
  healer
, time_road
, report_date_range_start
, report_date_range_cease
, report_interval_length
, report_interval_intent_task_count
, report_interval_intent_state_count
, time_begin
, time_close
, intent_idea_road
, intent_weight
, task)
{select_example_sqlstr}
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_calendar_table_insert_sqlstr_ReturnsCorrectStr():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    generated_sqlstr = get_calendar_table_delete_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
DELETE FROM calendar
WHERE healer = '{bob_text}' 
;
"""
    assert generated_sqlstr == example_sqlstr
