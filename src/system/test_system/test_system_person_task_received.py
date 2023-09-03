from src.system.system import SystemUnit
from src.system.person import personunit_shop
from src.system.examples.env_kit import (
    get_temp_env_dir,
    get_temp_env_name,
    env_dir_setup_cleanup,
    get_test_systems_dir,
    create_person_file_for_systems,
)
from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaKid
from os import path as os_path
from pytest import raises as pytest_raises


def test_system_person1_set_laundry_fact_create_person2_laundry_task(
    env_dir_setup_cleanup,
):
    # GIVEN
    # Create person1
    # Create person1 task:
    #   what: do the laundry
    #   why: because laundry is full: alternatives: laundry is not full
    #   who: group "person2"
    #   who optional: "who are members of this group"

    # Create person2
    # Create person2 ListenUnit: all task for me from person1

    # person1 sets acptfact such as "laundry is not full"
    # person2 listens
    # person2 has empty agenda

    # WHEN
    # person1 changes acptfact such as "laundry is full"
    # person2 "listens"

    # THEN
    # person2 has new agenda item "do laundry"

    system_name = get_temp_env_name()
    ex = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    ex.create_dirs_if_null(in_memory_bank=True)

    # Create two persons
    america_text = "America"
    joachim_text = "Joachim"
    ex.create_new_personunit(person_name=america_text)
    ex.create_new_personunit(person_name=joachim_text)
    america_calendar = CalendarUnit(_owner=america_text)
    joachim_calendar = CalendarUnit(_owner=joachim_text)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=america_calendar)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=joachim_calendar)

    # wx_path = f"{e1.get_persons_dir()}/{timmy_text}"

    # person1 has necessary ideas for laundry basket full != True or Not True

    # Have person2 receive laundry idea and status from person1

    # confirm person1 laundry_full == False
    # confirm person2 agenda is empty

    # WHEN
    # person1 laundry_full == True

    # THEN
    # confirm person2 agenda has task "Do the laundry"

    # e1.create_new_personunit(person_name=timmy_text)

    # # THEN
    # print(f"{wx_path=}")
    # assert os_path.exists(wx_path)

    assert 1 == 2
