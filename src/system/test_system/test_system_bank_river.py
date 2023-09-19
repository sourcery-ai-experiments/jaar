from src.system.system import systemunit_shop
from src.calendar.calendar import CalendarUnit
from src.system.examples.system_env_kit import (
    get_temp_env_name,
    get_test_systems_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.system.y_func import check_connection, get_single_result_back
from src.system.bank_sqlstr import (
    get_river_tmember_dict,
    get_river_flow_dict,
    get_table_count_sqlstr,
)


def test_system_set_river_sphere_for_calendar_CorrectlyPopulatesriver_tmemberTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example system with 4 Authors, each with 3 Memberunits = 12 ledger rows
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    sal = CalendarUnit(_owner=sal_text)
    sal.add_memberunit(name=bob_text, creditor_weight=1)
    sal.add_memberunit(name=tom_text, creditor_weight=3)
    sx.save_public_calendar(calendar_x=sal)

    bob = CalendarUnit(_owner=bob_text)
    bob.add_memberunit(name=sal_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=bob)

    tom = CalendarUnit(_owner=tom_text)
    tom.add_memberunit(name=sal_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=tom)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 4

    sqlstr_count_river_tmember = get_table_count_sqlstr("river_tmember")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 0

    # WHEN
    sx.set_river_sphere_for_calendar(calendar_name=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 4
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_calendar_name=sal_text)

    flow_0 = river_flows.get(0)
    flow_1 = river_flows.get(1)
    assert flow_1.src_name == "sal" and flow_1.dst_name == "tom"
    assert flow_1.river_tree_level == 1
    assert flow_1.currency_start == 0.25
    assert flow_1.currency_close == 1
    assert flow_1.parent_flow_num is None
    flow_2 = river_flows.get(2)
    flow_3 = river_flows.get(3)
    assert flow_3.src_name == "tom" and flow_3.dst_name == "sal"
    assert flow_3.river_tree_level == 2
    assert flow_3.parent_flow_num == 1

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 2

    with sx.get_bank_conn() as bank_conn:
        river_tmembers = get_river_tmember_dict(bank_conn, sal_text)
    assert len(river_tmembers) == 2
    river_sal_tax_bob = river_tmembers.get(bob_text)
    river_sal_tax_tom = river_tmembers.get(tom_text)

    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")

    assert river_sal_tax_bob.tax_total == 0.25
    assert river_sal_tax_tom.tax_total == 0.75


def test_system_set_river_sphere_for_calendar_CorrectlyPopulatesriver_tmemberTable02(
    env_dir_setup_cleanup,
):
    # GIVEN 4 calendars, 100% of river flows to sal
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = CalendarUnit(_owner=sal_text)
    sal.add_memberunit(name=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    sx.save_public_calendar(calendar_x=sal)

    bob = CalendarUnit(_owner=bob_text)
    bob.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_memberunit(name=tom_text, creditor_weight=1, debtor_weight=1)
    sx.save_public_calendar(calendar_x=bob)

    tom = CalendarUnit(_owner=tom_text)
    tom.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=8)
    sx.save_public_calendar(calendar_x=tom)

    elu = CalendarUnit(_owner=elu_text)
    elu.add_memberunit(name=sal_text, creditor_weight=1, debtor_weight=8)
    sx.save_public_calendar(calendar_x=elu)
    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tmember = get_table_count_sqlstr("river_tmember")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 0

    # WHEN
    sx.set_river_sphere_for_calendar(calendar_name=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 9
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_calendar_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 1

    with sx.get_bank_conn() as bank_conn:
        river_tmembers = get_river_tmember_dict(bank_conn, sal_text)
    assert len(river_tmembers) == 1
    assert river_tmembers.get(bob_text) is None
    assert river_tmembers.get(tom_text) is None
    river_sal_tax_elu = river_tmembers.get(elu_text)

    print(f"{river_sal_tax_elu=}")
    assert river_sal_tax_elu.tax_total == 1.0


def test_system_set_river_sphere_for_calendar_CorrectlyPopulatesriver_tmemberTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 calendars, 85% of river flows to sal
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_calendar = CalendarUnit(_owner=sal_text)
    sal_calendar.add_memberunit(name=bob_text, creditor_weight=2)
    sal_calendar.add_memberunit(name=tom_text, creditor_weight=7)
    sal_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=sal_calendar)

    bob_calendar = CalendarUnit(_owner=bob_text)
    bob_calendar.add_memberunit(name=sal_text, creditor_weight=3)
    bob_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=bob_calendar)

    tom_calendar = CalendarUnit(_owner=tom_text)
    tom_calendar.add_memberunit(name=sal_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=tom_calendar)

    ava_calendar = CalendarUnit(_owner=ava_text)
    sx.save_public_calendar(calendar_x=ava_calendar)
    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tmember = get_table_count_sqlstr("river_tmember")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 0

    # WHEN
    sx.set_river_sphere_for_calendar(calendar_name=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 6
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_calendar_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 2

    with sx.get_bank_conn() as bank_conn:
        river_tmembers = get_river_tmember_dict(bank_conn, sal_text)
    assert len(river_tmembers) == 2
    assert river_tmembers.get(bob_text) != None
    assert river_tmembers.get(tom_text) != None
    assert river_tmembers.get(ava_text) is None

    river_sal_tax_bob = river_tmembers.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = river_tmembers.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_system_set_river_sphere_for_calendar_CorrectlyPopulatesriver_tmemberTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 calendars, 85% of river flows to sal, left over %15 goes on endless loop
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_calendar = CalendarUnit(_owner=sal_text)
    sal_calendar.add_memberunit(name=bob_text, creditor_weight=2)
    sal_calendar.add_memberunit(name=tom_text, creditor_weight=7)
    sal_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=sal_calendar)

    bob_calendar = CalendarUnit(_owner=bob_text)
    bob_calendar.add_memberunit(name=sal_text, creditor_weight=3)
    bob_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=bob_calendar)

    tom_calendar = CalendarUnit(_owner=tom_text)
    tom_calendar.add_memberunit(name=sal_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=tom_calendar)

    ava_calendar = CalendarUnit(_owner=ava_text)
    ava_calendar.add_memberunit(name=elu_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=ava_calendar)

    elu_calendar = CalendarUnit(_owner=elu_text)
    elu_calendar.add_memberunit(name=ava_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=elu_calendar)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 8

    sqlstr_count_river_tmember = get_table_count_sqlstr("river_tmember")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 0

    # WHEN
    sx.set_river_sphere_for_calendar(calendar_name=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 40
    # with sx.get_bank_conn() as bank_conn:
    #     river_flows = get_river_flow_dict(bank_conn, currency_calendar_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 2

    with sx.get_bank_conn() as bank_conn:
        river_tmembers = get_river_tmember_dict(bank_conn, sal_text)
    assert len(river_tmembers) == 2
    assert river_tmembers.get(bob_text) != None
    assert river_tmembers.get(tom_text) != None
    assert river_tmembers.get(ava_text) is None

    river_sal_tax_bob = river_tmembers.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = river_tmembers.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_system_set_river_sphere_for_calendar_CorrectlyPopulatesriver_tmemberTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 calendars, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_calendar = CalendarUnit(_owner=sal_text)
    sal_calendar.add_memberunit(name=bob_text, creditor_weight=2)
    sal_calendar.add_memberunit(name=tom_text, creditor_weight=7)
    sal_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=sal_calendar)

    bob_calendar = CalendarUnit(_owner=bob_text)
    bob_calendar.add_memberunit(name=sal_text, creditor_weight=3)
    bob_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=bob_calendar)

    tom_calendar = CalendarUnit(_owner=tom_text)
    tom_calendar.add_memberunit(name=sal_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=tom_calendar)

    ava_calendar = CalendarUnit(_owner=ava_text)
    ava_calendar.add_memberunit(name=elu_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=ava_calendar)

    elu_calendar = CalendarUnit(_owner=elu_text)
    elu_calendar.add_memberunit(name=ava_text, creditor_weight=19)
    elu_calendar.add_memberunit(name=sal_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=elu_calendar)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tmember = get_table_count_sqlstr("river_tmember")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 0

    # WHEN
    sx.set_river_sphere_for_calendar(calendar_name=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 40
    # with sx.get_bank_conn() as bank_conn:
    #     river_flows = get_river_flow_dict(bank_conn, currency_calendar_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 3

    with sx.get_bank_conn() as bank_conn:
        river_tmembers = get_river_tmember_dict(bank_conn, sal_text)
    assert len(river_tmembers) == 3
    assert river_tmembers.get(bob_text) != None
    assert river_tmembers.get(tom_text) != None
    assert river_tmembers.get(elu_text) != None
    assert river_tmembers.get(ava_text) is None

    river_sal_tax_bob = river_tmembers.get(bob_text)
    river_sal_tax_tom = river_tmembers.get(tom_text)
    river_sal_tax_elu = river_tmembers.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7
    # assert round(river_sal_tax_elu.tax_total, 15) == 0.048741092066406
    assert round(river_sal_tax_elu.tax_total, 15) == 0.0378017640625


def test_system_set_river_sphere_for_calendar_CorrectlyDeletesPreviousRiver(
    env_dir_setup_cleanup,
):
    # GIVEN 4 calendars, 100% of river flows to sal
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = CalendarUnit(_owner=sal_text)
    sal.add_memberunit(name=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    sx.save_public_calendar(calendar_x=sal)

    bob = CalendarUnit(_owner=bob_text)
    bob.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_memberunit(name=tom_text, creditor_weight=1, debtor_weight=1)
    sx.save_public_calendar(calendar_x=bob)

    tom = CalendarUnit(_owner=tom_text)
    tom.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=8)
    sx.save_public_calendar(calendar_x=tom)

    elu = CalendarUnit(_owner=elu_text)
    elu.add_memberunit(name=sal_text, creditor_weight=1, debtor_weight=8)
    sx.save_public_calendar(calendar_x=elu)
    sx.refresh_bank_metrics()

    sx.set_river_sphere_for_calendar(calendar_name=sal_text)
    sx.set_river_sphere_for_calendar(calendar_name=elu_text)

    sqlstr_count_river_tmember = get_table_count_sqlstr("river_tmember")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 16

    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_calendar_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 3

    # WHEN
    # sal.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    # sx.save_public_calendar(calendar_x=sal)
    sx.set_river_sphere_for_calendar(calendar_name=sal_text)

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 16
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_calendar_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 3


def test_system_set_river_sphere_for_calendar_CorrectlyUsesMaxFlowsCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 calendars, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_calendar = CalendarUnit(_owner=sal_text)
    sal_calendar.add_memberunit(name=bob_text, creditor_weight=2)
    sal_calendar.add_memberunit(name=tom_text, creditor_weight=7)
    sal_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=sal_calendar)

    bob_calendar = CalendarUnit(_owner=bob_text)
    bob_calendar.add_memberunit(name=sal_text, creditor_weight=3)
    bob_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=bob_calendar)

    tom_calendar = CalendarUnit(_owner=tom_text)
    tom_calendar.add_memberunit(name=sal_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=tom_calendar)

    ava_calendar = CalendarUnit(_owner=ava_text)
    ava_calendar.add_memberunit(name=elu_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=ava_calendar)

    elu_calendar = CalendarUnit(_owner=elu_text)
    elu_calendar.add_memberunit(name=ava_text, creditor_weight=19)
    elu_calendar.add_memberunit(name=sal_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=elu_calendar)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tmember = get_table_count_sqlstr("river_tmember")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 0

    # WHEN
    mtc = 13
    sx.set_river_sphere_for_calendar(calendar_name=sal_text, max_flows_count=mtc)

    # THEN
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_calendar_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == mtc


def test_system_set_river_sphere_for_calendar_CorrectlyPopulatesriver_tmemberTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 calendars, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_calendar = CalendarUnit(_owner=sal_text)
    sal_calendar.add_memberunit(name=bob_text, creditor_weight=2)
    sal_calendar.add_memberunit(name=tom_text, creditor_weight=7)
    sal_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=sal_calendar)

    bob_calendar = CalendarUnit(_owner=bob_text)
    bob_calendar.add_memberunit(name=sal_text, creditor_weight=3)
    bob_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=bob_calendar)

    tom_calendar = CalendarUnit(_owner=tom_text)
    tom_calendar.add_memberunit(name=sal_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=tom_calendar)

    ava_calendar = CalendarUnit(_owner=ava_text)
    ava_calendar.add_memberunit(name=elu_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=ava_calendar)

    elu_calendar = CalendarUnit(_owner=elu_text)
    elu_calendar.add_memberunit(name=ava_text, creditor_weight=19)
    elu_calendar.add_memberunit(name=sal_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=elu_calendar)

    sx.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tmember = get_table_count_sqlstr("river_tmember")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 0

    # WHEN
    sx.set_river_sphere_for_calendar(calendar_name=sal_text)

    # THEN
    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_flow) == 40
    with sx.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_calendar_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(sx.get_bank_conn(), sqlstr_count_river_tmember) == 3

    with sx.get_bank_conn() as bank_conn:
        river_tmembers = get_river_tmember_dict(bank_conn, sal_text)
    river_tmembers = sx.get_river_tmembers(sal_text)
    assert len(river_tmembers) == 3
    assert river_tmembers.get(bob_text) != None
    assert river_tmembers.get(tom_text) != None
    assert river_tmembers.get(elu_text) != None
    assert river_tmembers.get(ava_text) is None

    river_sal_tax_bob = river_tmembers.get(bob_text)
    river_sal_tax_tom = river_tmembers.get(tom_text)
    river_sal_tax_elu = river_tmembers.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7
    # assert round(river_sal_tax_elu.tax_total, 15) == 0.048741092066406
    assert round(river_sal_tax_elu.tax_total, 15) == 0.0378017640625


def test_system_set_river_sphere_for_calendar_CorrectlyBuildsASingleContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 calendars, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_calendar = CalendarUnit(_owner=sal_text)
    sal_calendar.add_memberunit(name=bob_text, creditor_weight=2)
    sal_calendar.add_memberunit(name=tom_text, creditor_weight=7)
    sal_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=sal_calendar)

    bob_calendar = CalendarUnit(_owner=bob_text)
    bob_calendar.add_memberunit(name=sal_text, creditor_weight=3)
    bob_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=bob_calendar)

    tom_calendar = CalendarUnit(_owner=tom_text)
    tom_calendar.add_memberunit(name=sal_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=tom_calendar)

    ava_calendar = CalendarUnit(_owner=ava_text)
    ava_calendar.add_memberunit(name=elu_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=ava_calendar)

    elu_calendar = CalendarUnit(_owner=elu_text)
    elu_calendar.add_memberunit(name=ava_text, creditor_weight=19)
    elu_calendar.add_memberunit(name=sal_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=elu_calendar)

    sx.refresh_bank_metrics()

    # WHEN
    sx.set_river_sphere_for_calendar(calendar_name=sal_text, max_flows_count=100)

    # THEN
    count_range_fails_sql = """
    SELECT COUNT(*)
    FROM (
        SELECT 
            rt1.currency_start current_row_start
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) AS prev_close
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) - rt1.currency_start prev_diff
        , rt1.flow_num or_flow_num
        , lag(flow_num) OVER (ORDER BY currency_start, currency_close) AS prev_flow_num
        , rt1.parent_flow_num or_parent_flow_num
        , lag(parent_flow_num) OVER (ORDER BY currency_start, currency_close) AS prev_parent_flow_num
        , river_tree_level
        , lag(river_tree_level) OVER (ORDER BY currency_start, currency_close) AS prev_parent_river_tree_level
        FROM river_flow rt1
        --  WHERE dst_name = 'sal' and currency_name = dst_name
        ORDER BY rt1.currency_start, rt1.currency_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with sx.get_bank_conn() as bank_conn:
        assert get_single_result_back(bank_conn, count_range_fails_sql) == 0


def test_system_set_river_sphere_for_calendar_CorrectlyUpatesCalendarMemberUnits(
    env_dir_setup_cleanup,
):
    # GIVEN 5 calendars, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_calendar_src = CalendarUnit(_owner=sal_text)
    sal_calendar_src.add_memberunit(name=bob_text, creditor_weight=2, debtor_weight=2)
    sal_calendar_src.add_memberunit(name=tom_text, creditor_weight=2, debtor_weight=1)
    sal_calendar_src.add_memberunit(name=ava_text, creditor_weight=2, debtor_weight=2)
    sx.save_public_calendar(calendar_x=sal_calendar_src)

    bob_calendar = CalendarUnit(_owner=bob_text)
    bob_calendar.add_memberunit(name=sal_text, creditor_weight=3)
    bob_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    sx.save_public_calendar(calendar_x=bob_calendar)

    tom_calendar = CalendarUnit(_owner=tom_text)
    tom_calendar.add_memberunit(name=sal_text)
    sx.save_public_calendar(calendar_x=tom_calendar)

    ava_calendar = CalendarUnit(_owner=ava_text)
    ava_calendar.add_memberunit(name=elu_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=ava_calendar)

    elu_calendar = CalendarUnit(_owner=elu_text)
    elu_calendar.add_memberunit(name=ava_text, creditor_weight=8)
    elu_calendar.add_memberunit(name=sal_text, creditor_weight=2)
    sx.save_public_calendar(calendar_x=elu_calendar)

    sx.refresh_bank_metrics()
    sal_calendar_before = sx.get_public_calendar(owner=sal_text)

    sx.set_river_sphere_for_calendar(calendar_name=sal_text, max_flows_count=100)
    assert len(sal_calendar_before._members) == 3
    print(f"{len(sal_calendar_before._members)=}")
    bob_member = sal_calendar_before._members.get(bob_text)
    tom_member = sal_calendar_before._members.get(tom_text)
    ava_member = sal_calendar_before._members.get(ava_text)
    assert bob_member._bank_tax_paid is None
    assert bob_member._bank_tax_diff is None
    assert tom_member._bank_tax_paid is None
    assert tom_member._bank_tax_diff is None
    assert ava_member._bank_tax_paid is None
    assert ava_member._bank_tax_diff is None

    # WHEN
    sx.set_river_sphere_for_calendar(calendar_name=sal_text)

    # THEN
    sal_river_tmembers = sx.get_river_tmembers(calendar_name=sal_text)
    assert len(sal_river_tmembers) == 3

    sal_calendar_after = sx.get_public_calendar(owner=sal_text)

    bob_tmember = sal_river_tmembers.get(bob_text)
    tom_tmember = sal_river_tmembers.get(tom_text)
    elu_tmember = sal_river_tmembers.get(elu_text)
    assert bob_tmember.tax_name == bob_text
    assert tom_tmember.tax_name == tom_text
    assert elu_tmember.tax_name == elu_text
    assert bob_tmember.currency_name == sal_text
    assert tom_tmember.currency_name == sal_text
    assert elu_tmember.currency_name == sal_text

    bob_member = sal_calendar_after._members.get(bob_text)
    tom_member = sal_calendar_after._members.get(tom_text)
    ava_member = sal_calendar_after._members.get(ava_text)
    elu_member = sal_calendar_after._members.get(elu_text)

    assert bob_tmember.tax_total == bob_member._bank_tax_paid
    assert bob_tmember.tax_diff == bob_member._bank_tax_diff
    assert tom_tmember.tax_total == tom_member._bank_tax_paid
    assert tom_tmember.tax_diff == tom_member._bank_tax_diff
    assert elu_member is None
    assert elu_tmember.tax_total < 0.31 and elu_tmember.tax_total > 0.3
    assert elu_tmember.tax_diff is None

    # for tmember_uid, sal_river_tmember in sal_river_tmembers.items():
    #     print(f"{tmember_uid=} {sal_river_tmember=}")
    #     assert sal_river_tmember.currency_name == sal_text
    #     assert sal_river_tmember.tax_name in [bob_text, tom_text, elu_text]
    #     memberunit_x = sal_calendar_after._members.get(sal_river_tmember.tax_name)
    #     if memberunit_x != None:
    #         # print(
    #         #     f"{sal_river_tmember.currency_name=} {sal_river_tmember.tax_name=} {memberunit_x.name=} tax_total: {sal_river_tmember.tax_total} Tax Paid: {memberunit_x._bank_tax_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_river_tmember.currency_name=} {sal_river_tmember.tax_name=} {memberunit_x.name=} tax_diff:  {sal_river_tmember.tax_diff} Tax Paid: {memberunit_x._bank_tax_diff}"
    #         # )
    #         assert sal_river_tmember.tax_total == memberunit_x._bank_tax_paid
    #         assert sal_river_tmember.tax_diff == memberunit_x._bank_tax_diff

    assert sal_river_tmembers.get(ava_text) is None
    assert ava_member._bank_tax_paid is None
    assert ava_member._bank_tax_diff is None

    # for memberunit_x in sal_calendar_after._members.values():
    #     print(f"sal_calendar_after {memberunit_x.name=} {memberunit_x._bank_tax_paid=}")
    #     river_tmember_x = sal_river_tmembers.get(memberunit_x.name)
    #     if river_tmember_x is None:
    #         assert memberunit_x._bank_tax_paid is None
    #         assert memberunit_x._bank_tax_diff is None
    #     else:
    #         assert memberunit_x._bank_tax_paid != None
    #         assert memberunit_x._bank_tax_diff != None
    # assert sal_calendar_after != sal_calendar_before
