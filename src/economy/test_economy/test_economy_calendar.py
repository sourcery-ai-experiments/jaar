from src.economy.economy import economyunit_shop
from src.calendar.calendar import CalendarUnit
from src.calendar.examples.example_calendars import (
    get_calendar_1Task_1CE0MinutesRequired_1AcptFact as example_calendars_get_calendar_1Task_1CE0MinutesRequired_1AcptFact,
    calendar_v001 as example_calendars_calendar_v001,
)
import src.economy.examples.example_actors as example_actors
from os import path as os_path
from src.economy.examples.economy_env_kit import (
    get_temp_env_name,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_economy_set_calendar_CreatesCalendarFile(env_dir_setup_cleanup):
    # GIVEN
    economy_name = get_temp_env_name()
    sx = economyunit_shop(name=economy_name, economys_dir=get_test_economys_dir())
    sx.create_dirs_if_null()
    sx1_obj = example_actors.get_1node_calendar()
    sx1_path = f"{sx.get_public_dir()}/{sx1_obj._owner}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    sx.save_public_calendar(calendar_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_economy_get_calendar_currentlyGetsCalendar(env_dir_setup_cleanup):
    # GIVEN
    economy_name = get_temp_env_name()
    e5 = economyunit_shop(name=economy_name, economys_dir=get_test_economys_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_actors.get_7nodeJRootWithH_calendar()
    e5.save_public_calendar(calendar_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_public_calendar(owner=sx5_obj._owner) == sx5_obj


def test_economy_rename_public_calendar_ChangesCalendarName(
    env_dir_setup_cleanup,
):
    # GIVEN
    economy_name = get_temp_env_name()
    e5 = economyunit_shop(name=economy_name, economys_dir=get_test_economys_dir())
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
