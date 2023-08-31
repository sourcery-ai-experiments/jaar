from src.system.system import SystemUnit
from src.calendar.calendar import CalendarUnit
from src.calendar.examples.example_calendars import (
    get_calendar_1Task_1CE0MinutesRequired_1AcptFact as ex_cxs_get_calendar_1Task_1CE0MinutesRequired_1AcptFact,
    calendar_v001 as ex_cxs_calendar_v001,
    calendar_v002 as ex_cxs_calendar_v002,
)
from src.system.examples.example_persons import (
    get_1node_calendar as example_persons_get_1node_calendar,
    get_6node_calendar as example_persons_get_6node_calendar,
)
from os import path as os_path
from src.system.examples.env_kit import (
    get_temp_env_name,
    get_test_systems_dir,
    create_person_file_for_systems,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_system_get_person_dest_calendar_from_digest_calendar_files_ReturnsCorrectCalendarObjScenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    ex = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    input_calendar = example_persons_get_6node_calendar()
    ex.save_calendarunit_obj_to_calendars_dir(input_calendar)
    # ex.save_calendarunit_obj_to_calendars_dir(ex_cxs_get_calendar_1Task_1CE0MinutesRequired_1AcptFact())
    # ex.save_calendarunit_obj_to_calendars_dir(ex_cxs_calendar_v001())
    px_name = "test_person1"
    ex.create_new_personunit(person_name=px_name)
    ex.create_calendarlink_to_saved_calendar(
        person_name=px_name, calendar_desc=input_calendar._desc
    )
    ex.save_person_file(person_name=px_name)
    person_x_obj = ex.get_person_obj_from_system(name=px_name)
    print(f"{person_x_obj._src_calendarlinks=}")

    # WHEN
    dest_calendar = ex.get_person_dest_calendar_from_digest_calendar_files(
        person_name=px_name
    )

    # THEN
    # print(f"Before meldable= {person_x_obj._src_calendarlinks} ")
    input_calendar.make_meldable(person_x_obj.get_starting_digest_calendar())
    # print(f"After meldable= {person_x_obj._src_calendarlinks} ")

    dest_calendar_d_idea = dest_calendar.get_idea_kid(road="A,C,D")
    print(f" {dest_calendar_d_idea._weight=} {len(input_calendar._idearoot._kids)=} ")
    assert dest_calendar != None
    assert len(input_calendar._idearoot._kids) == 2
    # idea_a = dest_calendar.get_idea_kid(road="A")
    # idea_b = dest_calendar.get_idea_kid(road="B")
    # for idea_kid_x1 in input_calendar._idearoot._kids.values():
    #     print(f"{idea_kid_x1._desc=}")
    #     dest_calendar_counterpart_x1 = dest_calendar._idearoot._kids.get(idea_kid_x1._desc)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         dest_calendar_counterpart_x2 = dest_calendar_counterpart_x1._kids.get(
    #             idea_kid_x2._desc
    #         )
    #         print(
    #             f"{idea_kid_x2._desc=} {idea_kid_x2._weight=} {dest_calendar_counterpart_x2._weight=}"
    #         )
    #         # assert dest_calendar_counterpart_x2 == idea_kid_x2
    #         assert dest_calendar_counterpart_x2._desc == idea_kid_x2._desc

    #     print(
    #         f"{idea_kid_x1._desc=} {idea_kid_x1._weight=} {dest_calendar_counterpart_x1._weight=}"
    #     )
    #     assert dest_calendar_counterpart_x1._desc == idea_kid_x1._desc
    # assert dest_calendar._idearoot._kids == input_calendar._idearoot._kids
    assert dest_calendar._idearoot._acptfactunits == {}
    assert (
        dest_calendar._idearoot._acptfactunits
        == input_calendar._idearoot._acptfactunits
    )
    assert dest_calendar._members == {}
    assert dest_calendar._members == input_calendar._members
    assert dest_calendar._groups == {}
    assert dest_calendar._groups == input_calendar._groups
    assert dest_calendar._idearoot == input_calendar._idearoot


def test_system_get_person_dest_calendar_from_digest_calendar_files_ReturnsCorrectCalendarObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    ex = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    calendar1 = example_persons_get_6node_calendar()
    calendar2 = ex_cxs_calendar_v002()

    ex.save_calendarunit_obj_to_calendars_dir(calendar1)
    ex.save_calendarunit_obj_to_calendars_dir(calendar2)
    # ex.save_calendarunit_obj_to_calendars_dir(ex_cxs_get_calendar_1Task_1CE0MinutesRequired_1AcptFact())
    # ex.save_calendarunit_obj_to_calendars_dir(ex_cxs_calendar_v001())
    px_name = "test_person1"
    ex.create_new_personunit(person_name=px_name)
    ex.create_calendarlink_to_saved_calendar(px_name, calendar1._desc)
    ex.create_calendarlink_to_saved_calendar(px_name, calendar2._desc)
    ex.save_person_file(person_name=px_name)
    person_x_obj = ex.get_person_obj_from_system(name=px_name)
    print(f"{person_x_obj._src_calendarlinks=}")

    # WHEN
    dest_calendar = ex.get_person_dest_calendar_from_digest_calendar_files(
        person_name=px_name
    )

    # THEN
    # print(f"Before meldable= {person_x_obj._src_calendarlinks} ")
    calendar1.make_meldable(person_x_obj.get_starting_digest_calendar())
    # print(f"After meldable= {person_x_obj._src_calendarlinks} ")

    dest_calendar_d_idea = dest_calendar.get_idea_kid(road="A,C,D")
    print(f" {dest_calendar_d_idea._weight=} ")
    assert dest_calendar != None
    # for idea_kid_x1 in calendar1._idearoot._kids.values():
    #     dest_calendar_counterpart_x1 = dest_calendar._idearoot._kids.get(idea_kid_x1._desc)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         dest_calendar_counterpart_x2 = dest_calendar_counterpart_x1._kids.get(
    #             idea_kid_x2._desc
    #         )
    #         print(
    #             f"{idea_kid_x2._desc=} {idea_kid_x2._weight=} {dest_calendar_counterpart_x2._weight=}"
    #         )
    #         # assert dest_calendar_counterpart_x2 == idea_kid_x2
    #         assert dest_calendar_counterpart_x2._desc == idea_kid_x2._desc

    #     print(
    #         f"{idea_kid_x1._desc=} {idea_kid_x1._weight=} {dest_calendar_counterpart_x1._weight=}"
    #     )
    #     assert dest_calendar_counterpart_x1._desc == idea_kid_x1._desc
    # assert dest_calendar._idearoot._kids == calendar1._idearoot._kids
    assert len(dest_calendar._idearoot._acptfactunits) == 9
    assert len(dest_calendar._idearoot._acptfactunits) == len(
        calendar2._idearoot._acptfactunits
    )
    assert len(dest_calendar._members) == 22
    assert len(dest_calendar._members) == len(calendar2._members)
    assert len(dest_calendar._groups) == 34
    assert len(dest_calendar._groups) == len(calendar2._groups)
    assert dest_calendar._idearoot != calendar1._idearoot
    assert dest_calendar._idearoot != calendar2._idearoot
