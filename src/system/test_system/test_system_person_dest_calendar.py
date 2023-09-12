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
from src.system.examples.system_env_kit import (
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
    input_cx = example_persons_get_6node_calendar()
    ex.save_public_calendarunit(input_cx)
    # ex.save_public_calendarunit(ex_cxs_get_calendar_1Task_1CE0MinutesRequired_1AcptFact())
    # ex.save_public_calendarunit(ex_cxs_calendar_v001())
    xia_text = "Xia"
    ex.create_new_personunit(person_name=xia_text)
    ex.set_person_depotlink(xia_text, input_cx._owner, depotlink_type="blind_trust")
    ex.save_person_file(person_name=xia_text)
    xia_person = ex.sys_get_person_obj(name=xia_text)
    # print(f"{xia_person._isol._members.keys()=}")

    # WHEN
    output_cx = ex.get_person_output_calendar(person_name=xia_text)
    # input calendar must be melded to itself to create originunits
    input_cx.meld(input_cx)
    input_cx.set_owner(new_owner=xia_text)
    input_cx._originunit.set_originlink(name=xia_text, weight=1)

    # THEN
    a_text = "A"
    c_text = "C"
    c_road = f"{a_text},{c_text}"
    d_text = "D"
    d_road = f"{c_road},{d_text}"
    print(f"{output_cx._owner=}")
    print(f"{output_cx._idea_dict.keys()=}")
    output_cx_d_idea = output_cx.get_idea_kid(d_road)
    # print(f" {output_cx_d_idea._weight=} {len(input_cx._idearoot._kids)=} ")
    assert output_cx != None
    assert len(input_cx._idearoot._kids) == 2
    # idea_a = output_cx.get_idea_kid(road="A")
    # idea_b = output_cx.get_idea_kid(road="B")
    # for idea_kid_x1 in input_cx._idearoot._kids.values():
    #     print(f"{idea_kid_x1._label=}")
    #     output_cx_counterpart_x1 = output_cx._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_cx_counterpart_x2 = output_cx_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_cx_counterpart_x2._weight=}"
    #         )
    #         # assert output_cx_counterpart_x2 == idea_kid_x2
    #         assert output_cx_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_cx_counterpart_x1._weight=}"
    #     )
    #     assert output_cx_counterpart_x1._label == idea_kid_x1._label
    # assert output_cx._idearoot._kids == input_cx._idearoot._kids
    assert output_cx._idearoot._acptfactunits == {}
    assert output_cx._idearoot._acptfactunits == input_cx._idearoot._acptfactunits
    assert list(output_cx._members.keys()) == [a_text]
    assert output_cx._members != input_cx._members
    assert list(output_cx._groups.keys()) == [a_text]
    assert output_cx._groups != input_cx._groups
    print(f"{output_cx._originunit=}")
    print(f"{input_cx._originunit=}")
    assert output_cx._originunit == input_cx._originunit

    b_text = "B"
    print(f"{output_cx._idearoot._kids.get(b_text)._originunit=}")
    print(f"{input_cx._idearoot._kids.get(b_text)._originunit=}")
    assert output_cx._idearoot == input_cx._idearoot


def test_system_get_person_output_calendar_ReturnsCorrectCalendarObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    ex = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    cx1 = example_persons_get_6node_calendar()
    cx2 = ex_cxs_calendar_v002()

    ex.save_public_calendarunit(cx1)
    ex.save_public_calendarunit(cx2)
    # ex.save_public_calendarunit(ex_cxs_get_calendar_1Task_1CE0MinutesRequired_1AcptFact())
    # ex.save_public_calendarunit(ex_cxs_calendar_v001())
    xia_text = "Xia"
    ex.create_new_personunit(person_name=xia_text)
    ex.set_person_depotlink(xia_text, cx1._owner, depotlink_type="blind_trust")
    ex.set_person_depotlink(xia_text, cx2._owner, depotlink_type="blind_trust")
    ex.save_person_file(person_name=xia_text)
    xia_person = ex.sys_get_person_obj(name=xia_text)
    print(f"{xia_person._isol._members.keys()=}")

    # WHEN
    output_cx = ex.get_person_output_calendar(person_name=xia_text)

    # THEN
    output_cx_d_idea = output_cx.get_idea_kid(road="A,C,D")
    print(f" {output_cx_d_idea._weight=} ")
    assert output_cx != None
    # for idea_kid_x1 in cx1._idearoot._kids.values():
    #     output_cx_counterpart_x1 = output_cx._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_cx_counterpart_x2 = output_cx_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_cx_counterpart_x2._weight=}"
    #         )
    #         # assert output_cx_counterpart_x2 == idea_kid_x2
    #         assert output_cx_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_cx_counterpart_x1._weight=}"
    #     )
    #     assert output_cx_counterpart_x1._label == idea_kid_x1._label
    # assert output_cx._idearoot._kids == cx1._idearoot._kids
    assert len(output_cx._idearoot._acptfactunits) == 9
    assert len(output_cx._idearoot._acptfactunits) == len(cx2._idearoot._acptfactunits)
    assert len(output_cx._members) == 24
    assert len(output_cx._members) == len(cx2._members) + 2
    assert len(output_cx._groups) == 36
    assert len(output_cx._groups) == len(cx2._groups) + 2
    assert output_cx._idearoot != cx1._idearoot
    assert output_cx._idearoot != cx2._idearoot
