from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesReason_1Belief,
    get_agenda_with_tuesday_cleaning_task,
)
from src.economy.economy import economyunit_shop
from src.economy.examples.economy_env_kit import (
    get_temp_env_economy_id,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from src.economy.treasury_sqlstr import (
    get_table_count_sqlstr,
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
    CalendarIntentUnit,
    CalendarReportUnit,
)
from src.tools.sqlite import get_single_result
from pytest import raises as pytest_raises


def test_CalendarReportUnit_exists():
    # GIVEN
    bob_text = "Bob"
    x_time_road = "A,time,jajatime"
    x_date_range_start = 1000000600
    x_date_range_cease = 1000000900
    x_interval_length = 15
    x_intent_max_count_task = 11
    x_intent_max_count_state = 7

    # WHEN
    x_calendarreportunit = CalendarReportUnit(
        healer=bob_text,
        time_road=x_time_road,
        date_range_start=x_date_range_start,
        date_range_cease=x_date_range_cease,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )

    # THEN
    assert x_calendarreportunit.time_road == x_time_road
    assert x_calendarreportunit.date_range_start == x_date_range_start
    assert x_calendarreportunit.date_range_cease == x_date_range_cease
    assert x_calendarreportunit.interval_length == x_interval_length
    assert x_calendarreportunit.intent_max_count_task == x_intent_max_count_task
    assert x_calendarreportunit.intent_max_count_state == x_intent_max_count_state


def test_CalendarIntentUnit_exists():
    # GIVEN
    bob_text = "Bob"
    x_time_road = "A,time,jajatime"
    x_date_range_start = 1000000600
    x_date_range_cease = 1000000900
    x_interval_length = 15
    x_intent_max_count_task = 11
    x_intent_max_count_state = 7
    x_time_begin = 1000000615
    x_time_close = 1000000630
    x_intent_idea_road = "A,casa,cleaning,clean fridge"
    x_intent_weight = 0.5
    x_task = True
    x_calendarreportunit = CalendarReportUnit(
        healer=bob_text,
        time_road=x_time_road,
        date_range_start=x_date_range_start,
        date_range_cease=x_date_range_cease,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )

    # WHEN
    x_calendarintentunit = CalendarIntentUnit(
        calendarreportunit=x_calendarreportunit,
        time_begin=x_time_begin,
        time_close=x_time_close,
        intent_idea_road=x_intent_idea_road,
        intent_weight=x_intent_weight,
        task=x_task,
    )

    # THEN
    assert x_calendarintentunit.calendarreportunit == x_calendarreportunit
    assert x_calendarintentunit.time_begin == x_time_begin
    assert x_calendarintentunit.time_close == x_time_close
    assert x_calendarintentunit.intent_idea_road == x_intent_idea_road
    assert x_calendarintentunit.intent_weight == x_intent_weight
    assert x_calendarintentunit.task == x_task


def test_economy_treasury_get_calendar_table_crud_sqlstr_CorrectlyManagesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(economy_id, get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    x_economy.refresh_treasury_public_agendas_data()
    calendar_count_sqlstr = get_table_count_sqlstr("calendar")
    assert get_single_result(x_economy.get_treasury_conn(), calendar_count_sqlstr) == 0
    bob_text = "Bob"
    x_time_road = "A,time,jajatime"
    x_date_range_start = 1000000600
    x_date_range_cease = 1000000900
    x_interval_length = 15
    x_intent_max_count_task = 11
    x_intent_max_count_state = 7
    x_time_begin = 1000000615
    x_time_close = 1000000630
    x_intent_idea_road = "A,casa,cleaning,clean fridge"
    x_intent_weight = 0.5
    x_task = True

    # WHEN
    x_calendarreportunit = CalendarReportUnit(
        healer=bob_text,
        time_road=x_time_road,
        date_range_start=x_date_range_start,
        date_range_cease=x_date_range_cease,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )
    bob_calendarintentunit = CalendarIntentUnit(
        calendarreportunit=x_calendarreportunit,
        time_begin=x_time_begin,
        time_close=x_time_close,
        intent_idea_road=x_intent_idea_road,
        intent_weight=x_intent_weight,
        task=x_task,
    )

    # WHEN
    calendar_insert_sqlstr = get_calendar_table_insert_sqlstr(bob_calendarintentunit)
    print(f"{calendar_insert_sqlstr}")
    econonmy_conn = x_economy.get_treasury_conn()
    econonmy_conn.execute(calendar_insert_sqlstr)

    # THEN
    assert get_single_result(x_economy.get_treasury_conn(), calendar_count_sqlstr) == 1

    # WHEN
    calendar_delete_sqlstr = get_calendar_table_delete_sqlstr(bob_text)
    print(f"{calendar_delete_sqlstr}")
    econonmy_conn = x_economy.get_treasury_conn()
    econonmy_conn.execute(calendar_delete_sqlstr)

    # THEN
    assert get_single_result(x_economy.get_treasury_conn(), calendar_count_sqlstr) == 0


def test_economy_treasury_insert_intent_into_treasury_db_RaisesBaseDoesNotExistError():
    # GIVEN
    # A agenda that has 1 intent item
    economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(economy_id, get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    x_economy.refresh_treasury_public_agendas_data()

    amos_agenda = get_agenda_1Task_1CE0MinutesReason_1Belief()

    calendar_count_sqlstr = get_table_count_sqlstr("calendar")
    assert get_single_result(x_economy.get_treasury_conn(), calendar_count_sqlstr) == 0

    # WHEN
    bob_text = "Bob"
    bad_road = amos_agenda.make_l1_road("jajatime")
    x_calendarreportunit = CalendarReportUnit(bob_text, bad_road, 10, 19, 15, 11, 7)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        x_economy.insert_intent_into_treasury_db(amos_agenda, x_calendarreportunit)
    assert (
        str(excinfo.value)
        == f"Intent base cannot be '{bad_road}' because it does not exist in agenda '{amos_agenda._healer}'."
    )


def test_economy_treasury_insert_intent_into_treasury_db_CorrectlyPopulatesDB():
    # GIVEN
    # A agenda that has 1 intent item
    economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(economy_id, get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    x_economy.refresh_treasury_public_agendas_data()

    amos_agenda = get_agenda_with_tuesday_cleaning_task()

    calendar_count_sqlstr = get_table_count_sqlstr("calendar")
    assert get_single_result(x_economy.get_treasury_conn(), calendar_count_sqlstr) == 0

    # WHEN
    bob_text = "Bob"
    time_road = amos_agenda.make_l1_road("time")
    jajatime_road = amos_agenda.make_road(time_road, "jajatime")
    print(f"{jajatime_road=}")
    x_date_range_start = 1000000600
    x_date_range_cease = 1000000900
    x_interval_length = 15
    x_intent_max_count_task = 11
    x_intent_max_count_state = 7
    # WHEN
    x_calendarreportunit = CalendarReportUnit(
        healer=bob_text,
        time_road=jajatime_road,
        date_range_start=x_date_range_start,
        date_range_cease=x_date_range_cease,
        interval_length=x_interval_length,
        intent_max_count_task=x_intent_max_count_task,
        intent_max_count_state=x_intent_max_count_state,
    )
    x_economy.insert_intent_into_treasury_db(amos_agenda, x_calendarreportunit)

    # THEN
    assert get_single_result(x_economy.get_treasury_conn(), calendar_count_sqlstr) == 20
