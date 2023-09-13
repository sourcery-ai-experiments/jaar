from src.system.system import SystemUnit
from src.calendar.calendar import CalendarUnit
from src.calendar.examples.example_calendars import (
    get_calendar_1Task_1CE0MinutesRequired_1AcptFact as example_calendars_get_calendar_1Task_1CE0MinutesRequired_1AcptFact,
    calendar_v001 as example_calendars_calendar_v001,
)
import src.system.examples.example_persons as example_persons
from os import path as os_path
from src.system.examples.system_env_kit import (
    get_temp_env_name,
    get_test_systems_dir,
    create_person_file_for_systems,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_system_set_calendar_CreatesCalendarFile(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    e1 = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null()
    sx1_obj = example_persons.get_1node_calendar()
    sx1_path = f"{e1.get_calendars_dir()}/{sx1_obj._owner}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    e1.save_public_calendarunit(calendar_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_system_get_calendars_dir_list_of_obj_CreatesCalendarFilesList(
    env_dir_setup_cleanup,
):
    # GIVEN
    system_name = get_temp_env_name()
    ex = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    assert ex.get_calendars_dir_file_names_list() == []
    assert ex.get_calendars_dir_list_of_obj() == []

    # WHEN
    sx1_obj = example_persons.get_1node_calendar()
    sx2_obj = example_calendars_get_calendar_1Task_1CE0MinutesRequired_1AcptFact()
    sx3_obj = example_calendars_calendar_v001()
    print(f"{sx1_obj._owner=}")
    print(f"{sx2_obj._owner=}")
    print(f"{sx3_obj._owner=}")
    ex.save_public_calendarunit(calendar_x=sx1_obj)
    ex.save_public_calendarunit(calendar_x=sx2_obj)
    ex.save_public_calendarunit(calendar_x=sx3_obj)

    sx1_path = f"{ex.get_calendars_dir()}/{sx1_obj._owner}.json"
    sx2_path = f"{ex.get_calendars_dir()}/{sx2_obj._owner}.json"
    sx3_path = f"{ex.get_calendars_dir()}/{sx3_obj._owner}.json"
    assert os_path.exists(sx1_path)
    assert os_path.exists(sx2_path)
    assert os_path.exists(sx3_path)

    # THEN
    assert len(ex.get_calendars_dir_file_names_list()) == 3
    assert ex.get_calendars_dir_file_names_list()[0] == f"{sx1_obj._owner}.json"
    assert ex.get_calendars_dir_list_of_obj()[0]._owner == sx1_obj._owner
    assert ex.get_calendars_dir_list_of_obj()[0] == sx1_obj
    assert ex.get_calendars_dir_list_of_obj()[1]._idearoot == sx2_obj._idearoot
    assert ex.get_calendars_dir_list_of_obj()[1] == sx2_obj
    assert ex.get_calendars_dir_list_of_obj()[2] == sx3_obj


def test_system_get_calendar_currentlyGetsCalendar(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    e5 = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_persons.get_7nodeJRootWithH_calendar()
    e5.save_public_calendarunit(calendar_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_public_calendar(owner=sx5_obj._owner) == sx5_obj


def test_system_rename_calendar_in_calendars_dir_ChangesCalendarName(
    env_dir_setup_cleanup,
):
    # GIVEN
    system_name = get_temp_env_name()
    e5 = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_calendar_owner = "old1"
    sx5_obj = CalendarUnit(_owner=old_calendar_owner)
    old_sx5_path = f"{e5.get_calendars_dir()}/{old_calendar_owner}.json"
    e5.save_public_calendarunit(calendar_x=sx5_obj)
    print(f"{old_sx5_path=}")

    # WHEN
    new_calendar_owner = "new1"
    new_sx5_path = f"{e5.get_calendars_dir()}/{new_calendar_owner}.json"
    assert os_path.exists(new_sx5_path) == False
    assert os_path.exists(old_sx5_path)
    e5.rename_calendar_in_calendars_dir(
        old_owner=old_calendar_owner, new_owner=new_calendar_owner
    )

    # THEN
    assert os_path.exists(old_sx5_path) == False
    assert os_path.exists(new_sx5_path)
