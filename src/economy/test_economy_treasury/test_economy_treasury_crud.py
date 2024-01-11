from src.agenda.agenda import agendaunit_shop
from src.economy.economy import economyunit_shop
from src.economy.examples.economy_env_kit import (
    get_temp_env_economy_id,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from src.economy.treasury_sqlstr import (
    get_agendaunits_select_sqlstr,
    get_agendatreasuryunits_dict,
    get_table_count_sqlstr,
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
)
from src.tools.sqlite import get_single_result


def test_economy_treasury_get_agendaunits_ReturnsCorrectEmptyObj(env_dir_setup_cleanup):
    # GIVEN
    economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(economy_id, get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    x_economy.refresh_treasury_public_agendas_data()

    # WHEN
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_economy.get_treasury_conn())

    # THEN
    assert len(x_agendatreasuryunits) == 0


def test_economy_treasury_get_agendaunits_ReturnsCorrectNoneObj(env_dir_setup_cleanup):
    # GIVEN
    economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(economy_id, get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    x_economy.refresh_treasury_public_agendas_data()
    assert len(get_agendatreasuryunits_dict(x_economy.get_treasury_conn())) == 0

    # WHEN
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
    x_economy.save_public_agenda(agendaunit_shop(_healer=sal_text))
    x_economy.save_public_agenda(agendaunit_shop(_healer=bob_text))
    x_economy.save_public_agenda(agendaunit_shop(_healer=tom_text))
    x_economy.save_public_agenda(agendaunit_shop(_healer=ava_text))
    x_economy.save_public_agenda(agendaunit_shop(_healer=elu_text))
    x_economy.refresh_treasury_public_agendas_data()
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_economy.get_treasury_conn())

    # THEN
    assert len(x_agendatreasuryunits) == 5
    assert x_agendatreasuryunits.get(sal_text) != None
    assert x_agendatreasuryunits.get(bob_text) != None
    assert x_agendatreasuryunits.get(tom_text) != None
    assert x_agendatreasuryunits.get(ava_text) != None
    assert x_agendatreasuryunits.get(elu_text) != None
    assert x_agendatreasuryunits.get(sal_text).healer == sal_text
    assert x_agendatreasuryunits.get(bob_text).healer == bob_text
    assert x_agendatreasuryunits.get(tom_text).healer == tom_text
    assert x_agendatreasuryunits.get(ava_text).healer == ava_text
    assert x_agendatreasuryunits.get(elu_text).healer == elu_text
    print(f"{x_agendatreasuryunits.get(sal_text)=}")
    print(f"{x_agendatreasuryunits.get(bob_text)=}")
    print(f"{x_agendatreasuryunits.get(tom_text)=}")
    print(f"{x_agendatreasuryunits.get(ava_text)=}")
    print(f"{x_agendatreasuryunits.get(elu_text)=}")
    assert x_agendatreasuryunits.get(sal_text).rational is None
    assert x_agendatreasuryunits.get(bob_text).rational is None
    assert x_agendatreasuryunits.get(tom_text).rational is None
    assert x_agendatreasuryunits.get(ava_text).rational is None
    assert x_agendatreasuryunits.get(elu_text).rational is None


def test_economy_treasury_treasury_set_agendaunit_attrs_CorrectlyUpdatesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(economy_id, get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    x_economy.refresh_treasury_public_agendas_data()
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
    sal_agenda = agendaunit_shop(_healer=sal_text)
    bob_agenda = agendaunit_shop(_healer=bob_text)
    tom_agenda = agendaunit_shop(_healer=tom_text)
    ava_agenda = agendaunit_shop(_healer=ava_text)
    elu_agenda = agendaunit_shop(_healer=elu_text)
    x_economy.save_public_agenda(sal_agenda)
    x_economy.save_public_agenda(bob_agenda)
    x_economy.save_public_agenda(tom_agenda)
    x_economy.save_public_agenda(ava_agenda)
    x_economy.save_public_agenda(elu_agenda)
    x_economy.refresh_treasury_public_agendas_data()
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_economy.get_treasury_conn())
    assert x_agendatreasuryunits.get(sal_text).rational is None
    assert x_agendatreasuryunits.get(bob_text).rational is None

    # WHEN
    sal_agenda.set_agenda_metrics()
    bob_rational = False
    bob_agenda._rational = bob_rational
    x_economy._treasury_set_agendaunit_attrs(sal_agenda)
    x_economy._treasury_set_agendaunit_attrs(bob_agenda)

    # THEN
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_economy.get_treasury_conn())
    print(f"{x_agendatreasuryunits.get(sal_text)=}")
    print(f"{x_agendatreasuryunits.get(bob_text)=}")
    print(f"{x_agendatreasuryunits.get(tom_text)=}")
    print(f"{x_agendatreasuryunits.get(ava_text)=}")
    print(f"{x_agendatreasuryunits.get(elu_text)=}")
    assert x_agendatreasuryunits.get(sal_text).rational
    assert x_agendatreasuryunits.get(bob_text).rational == bob_rational


def test_economy_treasury_get_calendar_table_insert_sqlstr_CorrectlyInsertsRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(economy_id, get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    x_economy.refresh_treasury_public_agendas_data()
    calendar_count_sqlstr = get_table_count_sqlstr("calendar")
    assert get_single_result(x_economy.get_treasury_conn(), calendar_count_sqlstr) == 0

    # WHEN
    yao_text = "Yao"
    calendar_select_sqlstr = f"""
SELECT 
  '{yao_text}' healer
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
    calendar_insert_sqlstr = get_calendar_table_insert_sqlstr(calendar_select_sqlstr)
    print(f"{calendar_insert_sqlstr}")
    econonmy_conn = x_economy.get_treasury_conn()
    econonmy_conn.execute(calendar_insert_sqlstr)

    # THEN
    assert get_single_result(x_economy.get_treasury_conn(), calendar_count_sqlstr) == 1

    # WHEN
    calendar_delete_sqlstr = get_calendar_table_delete_sqlstr(yao_text)
    print(f"{calendar_delete_sqlstr}")
    econonmy_conn = x_economy.get_treasury_conn()
    econonmy_conn.execute(calendar_delete_sqlstr)

    # THEN
    assert get_single_result(x_economy.get_treasury_conn(), calendar_count_sqlstr) == 0
