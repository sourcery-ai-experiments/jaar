from src.system.system import SystemUnit
from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaKid
from src.calendar.group import groupunit_shop
from src.calendar.member import memberlink_shop
from src.system.examples.system_env_kit import (
    get_temp_env_name,
    get_test_systems_dir,
    env_dir_setup_cleanup,
)
from src.system.y_func import get_single_result_back
from src.system.bank_sqlstr import (
    get_db_tables,
    get_table_count_sqlstr,
)


def test_system_create_dirs_if_null_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create system
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())

    # WHEN
    sx.create_dirs_if_null(in_memory_bank=True)

    # THEN
    with sx.get_bank_conn() as bank_conn:
        tables_dict = get_db_tables(bank_conn)

    # row_count = 0
    # for table_name, table_x in tables_dict.items():
    #     row_count += 1
    #     print(f" {table_x=} {row_count}. {table_name=}")

    curr_tables = {
        0: "calendarunits",
        1: "ledger",
        2: "river_tmember",
        3: "river_flow",
        4: "river_bucket",
        5: "idea_catalog",
        6: "acptfact_catalog",
        7: "groupunit_catalog",
    }

    assert tables_dict.get(curr_tables[0]) != None
    assert tables_dict.get(curr_tables[1]) != None
    assert tables_dict.get(curr_tables[2]) != None
    assert tables_dict.get(curr_tables[3]) != None
    assert tables_dict.get(curr_tables[4]) != None
    assert tables_dict.get(curr_tables[5]) != None
    assert tables_dict.get(curr_tables[6]) != None
    assert tables_dict.get(curr_tables[7]) != None
    assert len(tables_dict) == len(curr_tables)


def test_system_refresh_bank_metrics_CorrectlyDeletesOldBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"

    bob = CalendarUnit(_owner=bob_text)
    bob.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    sx.save_public_calendarunit(calendar_x=bob)
    sx.refresh_bank_metrics()
    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 1

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 1


def test_system_refresh_bank_metrics_CorrectlyDeletesOldBankFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=False)

    bob_text = "bob"
    tom_text = "tom"

    bob = CalendarUnit(_owner=bob_text)
    bob.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    sx.save_public_calendarunit(calendar_x=bob)
    sx.refresh_bank_metrics()
    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 1

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 1


def test_system_refresh_bank_metrics_CorrectlyPopulatesLedgerTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example system with 4 Persons, each with 3 Memberunits = 12 ledger rows
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    bob = CalendarUnit(_owner=bob_text)
    bob.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    bob.add_memberunit(name=sal_text, creditor_weight=1, debtor_weight=4)
    bob.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    sx.save_public_calendarunit(calendar_x=bob)

    sal = CalendarUnit(_owner=sal_text)
    sal.add_memberunit(name=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    sal.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    sx.save_public_calendarunit(calendar_x=sal)

    tom = CalendarUnit(_owner=tom_text)
    tom.add_memberunit(name=bob_text, creditor_weight=3, debtor_weight=1)
    tom.add_memberunit(name=sal_text, creditor_weight=1, debtor_weight=4)
    tom.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    sx.save_public_calendarunit(calendar_x=tom)

    elu = CalendarUnit(_owner=elu_text)
    elu.add_memberunit(name=bob_text, creditor_weight=3, debtor_weight=1)
    elu.add_memberunit(name=tom_text, creditor_weight=1, debtor_weight=4)
    elu.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    sx.save_public_calendarunit(calendar_x=elu)

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 12


def test_system_refresh_bank_metrics_CorrectlyPopulatesCalendarTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example system with 4 Persons, each with 3 Memberunits = 12 ledger rows
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    sx.save_public_calendarunit(calendar_x=CalendarUnit(_owner=bob_text))
    sx.save_public_calendarunit(calendar_x=CalendarUnit(_owner=tom_text))
    sx.save_public_calendarunit(calendar_x=CalendarUnit(_owner=sal_text))
    sx.save_public_calendarunit(calendar_x=CalendarUnit(_owner=elu_text))

    sqlstr_count_calendars = get_table_count_sqlstr("calendarunits")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_calendars) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_calendars) == 4


def test_system_refresh_bank_metrics_CorrectlyPopulatesCalendarTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example system with 4 Persons, each with 3 Memberunits = 12 ledger rows
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    sx.save_public_calendarunit(calendar_x=CalendarUnit(_owner=bob_text))
    sx.save_public_calendarunit(calendar_x=CalendarUnit(_owner=tom_text))
    sx.save_public_calendarunit(calendar_x=CalendarUnit(_owner=sal_text))
    sx.save_public_calendarunit(calendar_x=CalendarUnit(_owner=elu_text))

    sqlstr_count_calendars = get_table_count_sqlstr("calendarunits")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_calendars) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_calendars) == 4


def test_system_refresh_bank_metrics_CorrectlyPopulates_groupunit_catalog(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"
    bob_calendar = CalendarUnit(_owner=bob_text)
    tom_calendar = CalendarUnit(_owner=tom_text)
    bob_calendar.add_memberunit(name=tom_text)
    tom_calendar.add_memberunit(name=bob_text)
    tom_calendar.add_memberunit(name=elu_text)
    sx.save_public_calendarunit(calendar_x=bob_calendar)
    sx.save_public_calendarunit(calendar_x=tom_calendar)

    sqlstr = get_table_count_sqlstr("groupunit_catalog")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr) == 0

    # WHEN
    sx.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr) == 3


def test_system_set_calendar_bank_attrs_CorrectlyPopulatesCalendar_Groupunit_Memberlinks(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    # create 4 calendars, 1 with group "swimming expert" linked to 1 member
    # two others have idea f"{root_label()},sports,swimming"
    # run set_bank_metrics
    # assert
    # _memberlinks_set_by_system_road
    # assert group "swimming expert" has 1 member
    # change groupunit "swimming expert" _memberlinks_set_by_system_road ==  "A,sports,swimmer"
    # run set_bank_metrics
    # assert group "swimming expert" has 2 different member

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_calendar = CalendarUnit(_owner=sal_text)
    bob_calendar = CalendarUnit(_owner=bob_text)
    tom_calendar = CalendarUnit(_owner=tom_text)
    ava_calendar = CalendarUnit(_owner=ava_text)

    swim_text = "swimming"
    sports_text = "sports"
    sal_sports_road = f"{sal_calendar._owner},{sports_text}"
    bob_sports_road = f"{bob_calendar._owner},{sports_text}"
    tom_sports_road = f"{tom_calendar._owner},{sports_text}"

    sal_calendar.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=sal_sports_road)
    bob_calendar.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=bob_sports_road)
    tom_calendar.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=tom_sports_road)

    sal_calendar.add_memberunit(name=bob_text, creditor_weight=2, debtor_weight=2)

    swim_group_text = "swimming expert"
    swim_group_unit = groupunit_shop(name=swim_group_text)
    bob_link = memberlink_shop(name=bob_text)
    swim_group_unit.set_memberlink(memberlink=bob_link)
    sal_calendar.set_groupunit(groupunit=swim_group_unit)

    sx.save_public_calendarunit(calendar_x=sal_calendar)
    sx.save_public_calendarunit(calendar_x=bob_calendar)
    sx.save_public_calendarunit(calendar_x=tom_calendar)
    sx.save_public_calendarunit(calendar_x=ava_calendar)

    sx.set_calendar_bank_attrs(calendar_name=sal_text)
    e1_sal_calendar = sx.get_public_calendar(owner=sal_text)
    assert len(e1_sal_calendar._groups.get(swim_group_text)._members) == 1

    # WHEN
    # change groupunit "swimming expert" _memberlinks_set_by_system_road ==  "A,sports,swimmer"
    sal_swim_road = f"{sal_sports_road},{swim_text}"
    swim_group_unit.set_attr(_memberlinks_set_by_system_road=sal_swim_road)
    sal_calendar.set_groupunit(groupunit=swim_group_unit)
    sx.save_public_calendarunit(calendar_x=sal_calendar)
    sx.set_calendar_bank_attrs(calendar_name=sal_text)

    # THEN
    e1_sal_calendar = sx.get_public_calendar(owner=sal_text)
    assert len(e1_sal_calendar._groups.get(swim_group_text)._members) == 2
