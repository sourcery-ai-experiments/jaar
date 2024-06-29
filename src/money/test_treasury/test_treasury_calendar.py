from src._instrument.sqlite import get_single_result, get_row_count_sqlstr
from src._road.road import create_road, get_default_real_id_roadnode as root_label
from src._world.examples.example_worlds import (
    get_world_1Task_1CE0MinutesReason_1Fact,
    get_world_with_tuesday_cleaning_task,
)
from src.money.money import moneyunit_shop
from src.money.treasury_sqlstr import (
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
    CalendarAgendaUnit,
    CalendarReport,
)
from src.money.examples.econ_env import (
    temp_real_id,
    temp_reals_dir,
    env_dir_setup_cleanup,
    get_texas_hubunit,
)
from pytest import raises as pytest_raises


def test_CalendarReport_Exists():
    # GIVEN
    bob_text = "Bob"
    time_road = create_road(root_label(), "time")
    jaja_road = create_road(time_road, "jajatime")
    x_date_range_start = 1000000600
    x_interval_count = 20
    x_interval_length = 15
    x_agenda_max_count_task = 11
    x_agenda_max_count_state = 7

    # WHEN
    x_calendarreport = CalendarReport(
        owner_id=bob_text,
        time_road=jaja_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        agenda_max_count_task=x_agenda_max_count_task,
        agenda_max_count_state=x_agenda_max_count_state,
    )

    # THEN
    assert x_calendarreport.time_road == jaja_road
    assert x_calendarreport.date_range_start == x_date_range_start
    assert x_calendarreport.interval_count == x_interval_count
    assert x_calendarreport.interval_length == x_interval_length
    assert x_calendarreport.agenda_max_count_task == x_agenda_max_count_task
    assert x_calendarreport.agenda_max_count_state == x_agenda_max_count_state


def test_CalendarReport_CalculationMethodsReturnCorrectObj():
    # GIVEN
    bob_text = "Bob"
    time_road = create_road(root_label(), "time")
    jaja_road = create_road(time_road, "jajatime")
    x_date_range_start = 1000000600
    x_interval_count = 20
    x_interval_length = 15
    x_agenda_max_count_task = 11
    x_agenda_max_count_state = 7
    x_calendarreport = CalendarReport(
        owner_id=bob_text,
        time_road=jaja_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        agenda_max_count_task=x_agenda_max_count_task,
        agenda_max_count_state=x_agenda_max_count_state,
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


def test_CalendarAgendaUnit_exists():
    # GIVEN
    bob_text = "Bob"
    time_road = create_road(root_label(), "time")
    jaja_road = create_road(time_road, "jajatime")
    x_date_range_start = 1000000600
    # x_date_range_cease = 1000000900
    x_interval_count = 20
    x_interval_length = 15
    x_agenda_max_count_task = 11
    x_agenda_max_count_state = 7
    x_time_begin = 1000000615
    x_time_close = 1000000630
    casa_road = create_road(root_label(), "casa")
    clean_road = create_road(casa_road, "cleaning")
    fridge_road = create_road(clean_road, "clean fridge")
    x_agenda_weight = 0.5
    x_task = True
    x_calendarreport = CalendarReport(
        owner_id=bob_text,
        time_road=jaja_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        agenda_max_count_task=x_agenda_max_count_task,
        agenda_max_count_state=x_agenda_max_count_state,
    )

    # WHEN
    x_calendaragendaunit = CalendarAgendaUnit(
        calendarreport=x_calendarreport,
        time_begin=x_time_begin,
        time_close=x_time_close,
        agenda_idea_road=fridge_road,
        agenda_weight=x_agenda_weight,
        task=x_task,
    )

    # THEN
    assert x_calendaragendaunit.calendarreport == x_calendarreport
    assert x_calendaragendaunit.time_begin == x_time_begin
    assert x_calendaragendaunit.time_close == x_time_close
    assert x_calendaragendaunit.agenda_idea_road == fridge_road
    assert x_calendaragendaunit.agenda_weight == x_agenda_weight
    assert x_calendaragendaunit.task == x_task


def test_MoneyUnit_treasury_get_calendar_table_crud_sqlstr_CorrectlyManagesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    real_id = temp_real_id()
    x_money = moneyunit_shop(get_texas_hubunit())
    x_money.create_treasury_db(in_memory=True)
    x_money.refresh_treasury_job_worlds_data()
    calendar_count_sqlstr = get_row_count_sqlstr("calendar")
    assert get_single_result(x_money.get_treasury_conn(), calendar_count_sqlstr) == 0
    bob_text = "Bob"
    time_road = create_road(root_label(), "time")
    jaja_road = create_road(time_road, "jajatime")
    x_date_range_start = 1000000600
    x_interval_count = 20
    x_interval_length = 15
    x_agenda_max_count_task = 11
    x_agenda_max_count_state = 7
    x_time_begin = 1000000615
    x_time_close = 1000000630
    casa_road = create_road(root_label(), "casa")
    clean_road = create_road(casa_road, "cleaning")
    fridge_road = create_road(clean_road, "clean fridge")
    x_agenda_weight = 0.5
    x_task = True

    # WHEN
    x_calendarreport = CalendarReport(
        owner_id=bob_text,
        time_road=jaja_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        agenda_max_count_task=x_agenda_max_count_task,
        agenda_max_count_state=x_agenda_max_count_state,
    )
    bob_calendaragendaunit = CalendarAgendaUnit(
        calendarreport=x_calendarreport,
        time_begin=x_time_begin,
        time_close=x_time_close,
        agenda_idea_road=fridge_road,
        agenda_weight=x_agenda_weight,
        task=x_task,
    )

    # WHEN
    calendar_insert_sqlstr = get_calendar_table_insert_sqlstr(bob_calendaragendaunit)
    print(f"{calendar_insert_sqlstr}")
    econ_conn = x_money.get_treasury_conn()
    econ_conn.execute(calendar_insert_sqlstr)

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), calendar_count_sqlstr) == 1

    # WHEN
    calendar_delete_sqlstr = get_calendar_table_delete_sqlstr(bob_text)
    print(f"{calendar_delete_sqlstr}")
    econ_conn = x_money.get_treasury_conn()
    econ_conn.execute(calendar_delete_sqlstr)

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), calendar_count_sqlstr) == 0


def test_MoneyUnit_treasury_insert_agenda_into_treasury_RaisesBaseDoesNotExistError():
    # GIVEN
    # A world that has 1 agenda item
    real_id = temp_real_id()
    x_money = moneyunit_shop(get_texas_hubunit())
    x_money.create_treasury_db(in_memory=True)
    x_money.refresh_treasury_job_worlds_data()

    amos_world = get_world_1Task_1CE0MinutesReason_1Fact()

    calendar_count_sqlstr = get_row_count_sqlstr("calendar")
    assert get_single_result(x_money.get_treasury_conn(), calendar_count_sqlstr) == 0

    # WHEN
    bob_text = "Bob"
    incorrect_road = amos_world.make_l1_road("jajatime")
    x_calendarreport = CalendarReport(bob_text, incorrect_road, 10, 19, 15, 11, 7)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        x_money.insert_agenda_into_treasury(amos_world, x_calendarreport)
    assert (
        str(excinfo.value)
        == f"Agenda base cannot be '{incorrect_road}' because it does not exist in world '{amos_world._owner_id}'."
    )


def test_MoneyUnit_treasury_insert_agenda_into_treasury_CorrectlyPopulatesTreasury():
    # GIVEN
    # A world that has 1 agenda item
    x_money = moneyunit_shop(get_texas_hubunit())
    x_money.create_treasury_db(in_memory=True)
    x_money.refresh_treasury_job_worlds_data()
    calendar_count_sqlstr = get_row_count_sqlstr("calendar")
    assert get_single_result(x_money.get_treasury_conn(), calendar_count_sqlstr) == 0

    # WHEN
    bob_world = get_world_with_tuesday_cleaning_task()
    jajatime_road = bob_world.make_road(bob_world.make_l1_road("time"), "jajatime")
    print(f"{jajatime_road=}")
    x_date_range_start = 1064131200
    x_interval_count = 5
    x_interval_length = 15
    x_agenda_max_count_task = 11
    x_agenda_max_count_state = 7
    # WHEN
    x_calendarreport = CalendarReport(
        owner_id=bob_world._owner_id,
        time_road=jajatime_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        agenda_max_count_task=x_agenda_max_count_task,
        agenda_max_count_state=x_agenda_max_count_state,
    )
    x_money.insert_agenda_into_treasury(bob_world, x_calendarreport)

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), calendar_count_sqlstr) == 6

    # GIVEN
    new_interval_count = 3
    # WHEN
    x_calendarreport = CalendarReport(
        owner_id=bob_world._owner_id,
        time_road=jajatime_road,
        date_range_start=x_date_range_start,
        interval_count=new_interval_count,
        interval_length=x_interval_length,
        agenda_max_count_task=x_agenda_max_count_task,
        agenda_max_count_state=x_agenda_max_count_state,
    )
    x_money.insert_agenda_into_treasury(bob_world, x_calendarreport)
    # THEN
    assert get_single_result(x_money.get_treasury_conn(), calendar_count_sqlstr) == 4
