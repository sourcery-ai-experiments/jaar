from src.system.system import systemunit_shop
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
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_system_set_calendar_CreatesCalendarFile(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null()
    sx1_obj = example_persons.get_1node_calendar()
    sx1_path = f"{sx.get_public_dir()}/{sx1_obj._owner}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    sx.save_public_calendar(calendar_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_system_get_calendar_currentlyGetsCalendar(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    e5 = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_persons.get_7nodeJRootWithH_calendar()
    e5.save_public_calendar(calendar_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_public_calendar(owner=sx5_obj._owner) == sx5_obj


def test_system_rename_public_calendar_ChangesCalendarName(
    env_dir_setup_cleanup,
):
    # GIVEN
    system_name = get_temp_env_name()
    e5 = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_calendar_owner = "old1"
    sx5_obj = CalendarUnit(_owner=old_calendar_owner)
    old_sx5_path = f"{e5.get_public_dir()}/{old_calendar_owner}.json"
    e5.save_public_calendar(calendar_x=sx5_obj)
    print(f"{old_sx5_path=}")

    # WHEN
    new_calendar_owner = "new1"
    new_sx5_path = f"{e5.get_public_dir()}/{new_calendar_owner}.json"
    assert os_path.exists(new_sx5_path) == False
    assert os_path.exists(old_sx5_path)
    e5.rename_public_calendar(
        old_owner=old_calendar_owner, new_owner=new_calendar_owner
    )

    # THEN
    assert os_path.exists(old_sx5_path) == False
    assert os_path.exists(new_sx5_path)
