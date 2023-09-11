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


def test_system_get_person_output_calendar_ReturnsCorrectCalendarObjScenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    ex = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    input_calendar = example_persons_get_6node_calendar()
    ex.save_public_calendarunit(input_calendar)
    # ex.save_public_calendarunit(ex_cxs_get_calendar_1Task_1CE0MinutesRequired_1AcptFact())
    # ex.save_public_calendarunit(ex_cxs_calendar_v001())
    xia_text = "Xia"
    ex.create_new_personunit(person_name=xia_text)
    ex.set_person_depotlink(
        xia_text, input_calendar._owner, depotlink_type="blind_trust"
    )
    ex.save_person_file(person_name=xia_text)
    person_x_obj = ex.sys_get_person_obj(name=xia_text)
    # print(f"{person_x_obj._isol._members.keys()=}")

    # WHEN
    output_calendar = ex.get_person_output_calendar(person_name=xia_text)
    # input calendar must be melded to itself to create originunits
    input_calendar.meld(input_calendar)
    input_calendar.set_owner(new_owner=xia_text)
    input_calendar._originunit.set_originlink(name=xia_text, weight=1)

    # THEN
    d_road = "A,C,D"
    print(f"{output_calendar._owner=}")
    print(f"{output_calendar._idea_dict.keys()=}")
    output_calendar_d_idea = output_calendar.get_idea_kid(d_road)
    # print(f" {output_calendar_d_idea._weight=} {len(input_calendar._idearoot._kids)=} ")
    assert output_calendar != None
    assert len(input_calendar._idearoot._kids) == 2
    # idea_a = output_calendar.get_idea_kid(road="A")
    # idea_b = output_calendar.get_idea_kid(road="B")
    # for idea_kid_x1 in input_calendar._idearoot._kids.values():
    #     print(f"{idea_kid_x1._label=}")
    #     output_calendar_counterpart_x1 = output_calendar._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_calendar_counterpart_x2 = output_calendar_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_calendar_counterpart_x2._weight=}"
    #         )
    #         # assert output_calendar_counterpart_x2 == idea_kid_x2
    #         assert output_calendar_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_calendar_counterpart_x1._weight=}"
    #     )
    #     assert output_calendar_counterpart_x1._label == idea_kid_x1._label
    # assert output_calendar._idearoot._kids == input_calendar._idearoot._kids
    assert output_calendar._idearoot._acptfactunits == {}
    assert (
        output_calendar._idearoot._acptfactunits
        == input_calendar._idearoot._acptfactunits
    )
    assert output_calendar._members == {}
    assert output_calendar._members == input_calendar._members
    assert output_calendar._groups == {}
    assert output_calendar._groups == input_calendar._groups
    print(f"{output_calendar._originunit=}")
    print(f"{input_calendar._originunit=}")
    assert output_calendar._originunit == input_calendar._originunit

    b_text = "B"
    print(f"{output_calendar._idearoot._kids.get(b_text)._originunit=}")
    print(f"{input_calendar._idearoot._kids.get(b_text)._originunit=}")
    assert output_calendar._idearoot == input_calendar._idearoot


def test_system_get_person_output_calendar_ReturnsCorrectCalendarObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    ex = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    calendar1 = example_persons_get_6node_calendar()
    calendar2 = ex_cxs_calendar_v002()

    ex.save_public_calendarunit(calendar1)
    ex.save_public_calendarunit(calendar2)
    # ex.save_public_calendarunit(ex_cxs_get_calendar_1Task_1CE0MinutesRequired_1AcptFact())
    # ex.save_public_calendarunit(ex_cxs_calendar_v001())
    xia_text = "Xia"
    ex.create_new_personunit(person_name=xia_text)
    ex.set_person_depotlink(xia_text, calendar1._owner, depotlink_type="blind_trust")
    ex.set_person_depotlink(xia_text, calendar2._owner, depotlink_type="blind_trust")
    ex.save_person_file(person_name=xia_text)
    person_x_obj = ex.sys_get_person_obj(name=xia_text)
    print(f"{person_x_obj._isol._members.keys()=}")

    # WHEN
    output_calendar = ex.get_person_output_calendar(person_name=xia_text)

    # THEN
    output_calendar_d_idea = output_calendar.get_idea_kid(road="A,C,D")
    print(f" {output_calendar_d_idea._weight=} ")
    assert output_calendar != None
    # for idea_kid_x1 in calendar1._idearoot._kids.values():
    #     output_calendar_counterpart_x1 = output_calendar._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_calendar_counterpart_x2 = output_calendar_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_calendar_counterpart_x2._weight=}"
    #         )
    #         # assert output_calendar_counterpart_x2 == idea_kid_x2
    #         assert output_calendar_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_calendar_counterpart_x1._weight=}"
    #     )
    #     assert output_calendar_counterpart_x1._label == idea_kid_x1._label
    # assert output_calendar._idearoot._kids == calendar1._idearoot._kids
    assert len(output_calendar._idearoot._acptfactunits) == 9
    assert len(output_calendar._idearoot._acptfactunits) == len(
        calendar2._idearoot._acptfactunits
    )
    assert len(output_calendar._members) == 22
    assert len(output_calendar._members) == len(calendar2._members)
    assert len(output_calendar._groups) == 34
    assert len(output_calendar._groups) == len(calendar2._groups)
    assert output_calendar._idearoot != calendar1._idearoot
    assert output_calendar._idearoot != calendar2._idearoot
