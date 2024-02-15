from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesReason_1Belief,
    get_agenda_with_tuesday_cleaning_task,
)
from src.market.market import marketunit_shop
from src.market.examples.market_env_kit import (
    get_temp_env_market_id,
    get_test_market_dir,
    env_dir_setup_cleanup,
)
from src.market.bank_sqlstr import (
    get_table_count_sqlstr,
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
    CalendarIntentUnit,
    CalendarReport,
)
from src.instrument.sqlite import get_single_result
from pytest import raises as pytest_raises


def test_CalendarReport_Exists():
    # GIVEN
    bob_text = "Bob"
    x_time_road = "A,time,jajatime"
    x_date_range_start = 1000000600
    x_interval_count = 20
    x_interval_length = 15
    x_intent_max_count_task = 11
    x_intent_max_count_state = 7

    # WHEN
    x_calendarreport = CalendarReport(
        agent_id=bob_text,
        time_road=x_time_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )

    # THEN
    assert x_calendarreport.time_road == x_time_road
    assert x_calendarreport.date_range_start == x_date_range_start
    assert x_calendarreport.interval_count == x_interval_count
    assert x_calendarreport.interval_length == x_interval_length
    assert x_calendarreport.intent_max_count_task == x_intent_max_count_task
    assert x_calendarreport.intent_max_count_state == x_intent_max_count_state


def test_CalendarReport_CalculationMethodsReturnCorrectObj():
    # GIVEN
    bob_text = "Bob"
    x_time_road = "A,time,jajatime"
    x_date_range_start = 1000000600
    x_interval_count = 20
    x_interval_length = 15
    x_intent_max_count_task = 11
    x_intent_max_count_state = 7
    x_calendarreport = CalendarReport(
        agent_id=bob_text,
        time_road=x_time_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )

    # WHEN / THEN
    assert x_calendarreport.get_date_range_cease() == 1000000900
    assert x_calendarreport.get_date_range_length() == 300
    assert x_calendarreport.get_interval_begin(interval_num=0) == 1000000600
    assert x_calendarreport.get_interval_begin(interval_num=2) == 1000000630
    assert x_calendarreport.get_interval_begin(interval_num=3) == 1000000645
    assert x_calendarreport.get_interval_close(interval_num=0) == 1000000615
    assert x_calendarreport.get_interval_close(interval_num=2) == 1000000645
    assert x_calendarreport.get_interval_close(interval_num=3) == 1000000660


def test_CalendarIntentUnit_exists():
    # GIVEN
    bob_text = "Bob"
    x_time_road = "A,time,jajatime"
    x_date_range_start = 1000000600
    # x_date_range_cease = 1000000900
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
        agent_id=bob_text,
        time_road=x_time_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )

    # WHEN
    x_calendarintentunit = CalendarIntentUnit(
        calendarreport=x_calendarreport,
        time_begin=x_time_begin,
        time_close=x_time_close,
        intent_idea_road=x_intent_idea_road,
        intent_weight=x_intent_weight,
        task=x_task,
    )

    # THEN
    assert x_calendarintentunit.calendarreport == x_calendarreport
    assert x_calendarintentunit.time_begin == x_time_begin
    assert x_calendarintentunit.time_close == x_time_close
    assert x_calendarintentunit.intent_idea_road == x_intent_idea_road
    assert x_calendarintentunit.intent_weight == x_intent_weight
    assert x_calendarintentunit.task == x_task


def test_market_bank_get_calendar_table_crud_sqlstr_CorrectlyManagesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    market_id = get_temp_env_market_id()
    x_market = marketunit_shop(market_id, get_test_market_dir())
    x_market.set_market_dirs(in_memory_bank=True)
    x_market.refresh_bank_forum_agendas_data()
    calendar_count_sqlstr = get_table_count_sqlstr("calendar")
    assert get_single_result(x_market.get_bank_conn(), calendar_count_sqlstr) == 0
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

    # WHEN
    x_calendarreport = CalendarReport(
        agent_id=bob_text,
        time_road=x_time_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )
    bob_calendarintentunit = CalendarIntentUnit(
        calendarreport=x_calendarreport,
        time_begin=x_time_begin,
        time_close=x_time_close,
        intent_idea_road=x_intent_idea_road,
        intent_weight=x_intent_weight,
        task=x_task,
    )

    # WHEN
    calendar_insert_sqlstr = get_calendar_table_insert_sqlstr(bob_calendarintentunit)
    print(f"{calendar_insert_sqlstr}")
    market_conn = x_market.get_bank_conn()
    market_conn.execute(calendar_insert_sqlstr)

    # THEN
    assert get_single_result(x_market.get_bank_conn(), calendar_count_sqlstr) == 1

    # WHEN
    calendar_delete_sqlstr = get_calendar_table_delete_sqlstr(bob_text)
    print(f"{calendar_delete_sqlstr}")
    market_conn = x_market.get_bank_conn()
    market_conn.execute(calendar_delete_sqlstr)

    # THEN
    assert get_single_result(x_market.get_bank_conn(), calendar_count_sqlstr) == 0


def test_market_bank_insert_intent_into_bank_RaisesBaseDoesNotExistError():
    # GIVEN
    # A agenda that has 1 intent item
    market_id = get_temp_env_market_id()
    x_market = marketunit_shop(market_id, get_test_market_dir())
    x_market.set_market_dirs(in_memory_bank=True)
    x_market.refresh_bank_forum_agendas_data()

    amos_agenda = get_agenda_1Task_1CE0MinutesReason_1Belief()

    calendar_count_sqlstr = get_table_count_sqlstr("calendar")
    assert get_single_result(x_market.get_bank_conn(), calendar_count_sqlstr) == 0

    # WHEN
    bob_text = "Bob"
    bad_road = amos_agenda.make_l1_road("jajatime")
    x_calendarreport = CalendarReport(bob_text, bad_road, 10, 19, 15, 11, 7)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        x_market.insert_intent_into_bank(amos_agenda, x_calendarreport)
    assert (
        str(excinfo.value)
        == f"Intent base cannot be '{bad_road}' because it does not exist in agenda '{amos_agenda._agent_id}'."
    )


def test_market_bank_insert_intent_into_bank_CorrectlyPopulatesBank():
    # GIVEN
    # A agenda that has 1 intent item
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_market_dir())
    x_market.set_market_dirs(in_memory_bank=True)
    x_market.refresh_bank_forum_agendas_data()
    calendar_count_sqlstr = get_table_count_sqlstr("calendar")
    assert get_single_result(x_market.get_bank_conn(), calendar_count_sqlstr) == 0

    # WHEN
    bob_agenda = get_agenda_with_tuesday_cleaning_task()
    jajatime_road = bob_agenda.make_road(bob_agenda.make_l1_road("time"), "jajatime")
    print(f"{jajatime_road=}")
    x_date_range_start = 1064131200
    x_interval_count = 5
    x_interval_length = 15
    x_intent_max_count_task = 11
    x_intent_max_count_state = 7
    # WHEN
    x_calendarreport = CalendarReport(
        agent_id=bob_agenda._agent_id,
        time_road=jajatime_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )
    x_market.insert_intent_into_bank(bob_agenda, x_calendarreport)

    # THEN
    assert get_single_result(x_market.get_bank_conn(), calendar_count_sqlstr) == 6

    # GIVEN
    new_interval_count = 3
    # WHEN
    x_calendarreport = CalendarReport(
        agent_id=bob_agenda._agent_id,
        time_road=jajatime_road,
        date_range_start=x_date_range_start,
        interval_count=new_interval_count,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )
    x_market.insert_intent_into_bank(bob_agenda, x_calendarreport)
    # THEN
    assert get_single_result(x_market.get_bank_conn(), calendar_count_sqlstr) == 4
