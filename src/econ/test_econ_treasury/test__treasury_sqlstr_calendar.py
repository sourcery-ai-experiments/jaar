from src.econ.treasury_sqlstr import (
    get_calendar_table_create_sqlstr,
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
    CalendarIntentUnit,
    CalendarReport,
)
from src.instrument.sqlite import sqlite_bool


def test_get_calendar_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_calendar_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS calendar (
  owner_id VARCHAR(255) NOT NULL
, report_time_road VARCHAR(10000) NOT NULL
, report_date_range_start INT NOT NULL
, report_date_range_cease INT NOT NULL
, report_interval_length INT NOT NULL
, report_interval_intent_task_max_count INT NOT NULL
, report_interval_intent_state_max_count INT NOT NULL
, time_begin INT NOT NULL
, time_close INT NOT NULL
, intent_idea_road VARCHAR(255) NOT NULL
, intent_weight INT NOT NULL
, task INT NOT NULL
, FOREIGN KEY(owner_id) REFERENCES agendaunit(owner_id)
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_calendar_table_insert_sqlstr_ReturnsCorrectStr():
    # GIVEN
    bob_text = "Bob"
    x_time_road = "A,time,jajatime"
    x_date_range_start = 1000000600
    x_interval_count = 20
    x_interval_length = 15
    x_intent_max_count_task = 11
    x_intent_max_count_state = 7
    x_time_begin = 1000000615
    x_time_close = 1000000630
    x_intent_idea_road = "A,casa,cleaning,clean fridge"
    x_intent_weight = 0.5
    x_task = True
    x_calendarreport = CalendarReport(
        owner_id=bob_text,
        time_road=x_time_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )

    # WHEN
    bob_calendarintentunit = CalendarIntentUnit(
        calendarreport=x_calendarreport,
        time_begin=x_time_begin,
        time_close=x_time_close,
        intent_idea_road=x_intent_idea_road,
        intent_weight=x_intent_weight,
        task=x_task,
    )

    # WHEN
    generated_sqlstr = get_calendar_table_insert_sqlstr(bob_calendarintentunit)

    # THEN
    example_sqlstr = f"""
INSERT INTO calendar (
  owner_id
, report_time_road
, report_date_range_start
, report_date_range_cease
, report_interval_length
, report_interval_intent_task_max_count
, report_interval_intent_state_max_count
, time_begin
, time_close
, intent_idea_road
, intent_weight
, task)
VALUES (
  '{bob_text}'
, '{x_time_road}'
, {x_date_range_start}
, {x_calendarreport.get_date_range_cease()}
, {x_interval_length}
, {x_intent_max_count_task}
, {x_intent_max_count_state}
, {x_time_begin}
, {x_time_close}
, '{x_intent_idea_road}'
, {x_intent_weight}
, {sqlite_bool(x_task)}
)
;
"""
    print(f"{example_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_calendar_table_delete_sqlstr_ReturnsCorrectStr():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    generated_sqlstr = get_calendar_table_delete_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
DELETE FROM calendar
WHERE owner_id = '{bob_text}' 
;
"""
    assert generated_sqlstr == example_sqlstr
