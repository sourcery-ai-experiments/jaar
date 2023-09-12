from src.system.person import personunit_shop
from src.system.examples.example_persons import get_calendar_assignment_laundry_example1
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
    create_calendar_file_for_person,
)
from src.system.examples.env_kit import get_temp_env_name
from src.system.system import SystemUnit
from os import path as os_path, scandir as os_scandir
from pytest import raises as pytest_raises
from src.calendar.calendar import CalendarUnit
from src.calendar.road import get_global_root_label as root_label
from src.calendar.x_func import (
    count_files as x_func_count_files,
    dir_files as x_func_dir_files,
)


# def test_person_save_calendar_to_depot_assignment_link_CorrectlyCreatesAssignmentFile(
#     person_dir_setup_cleanup,
# ):
#     # create calendar America with Joachim as assignor for laundry task
#     # GIVEN
#     # Create person1
#     america_cx = get_calendar_assignment_laundry_example1()

#     joachim_text = "Joachim"
#     joachim_px = personunit_shop(joachim_text, get_temp_person_dir())
#     assert joachim_px.get_isol()._members == {}

#     # WHEN
#     joachim_px.set_depot_calendar(calendar_x=america_cx, depotlink_type="assignment")
#     joachim_assignment = america_cx.get_assignment(
#         calendar_x=CalendarUnit(_owner=joachim_text),
#         assignor_members={joachim_text: -1, america_cx._owner: -1},
#         assignor_name=joachim_text,
#     )

#     # THEN
#     assert joachim_assignment != None
#     joachim_assignment.set_calendar_metrics()
#     assert len(joachim_assignment._idea_dict.keys()) == 9

#     casa_text = "casa"
#     casa_road = f"{root_label()},{casa_text}"
#     basket_text = "laundry basket status"
#     basket_road = f"{casa_road},{basket_text}"
#     b_full_text = "full"
#     b_full_road = f"{basket_road},{b_full_text}"
#     b_smel_text = "smelly"
#     b_smel_road = f"{basket_road},{b_smel_text}"
#     b_bare_text = "bare"
#     b_bare_road = f"{basket_road},{b_bare_text}"
#     b_fine_text = "fine"
#     b_fine_road = f"{basket_road},{b_fine_text}"
#     b_half_text = "half full"
#     b_half_road = f"{basket_road},{b_half_text}"
#     laundry_task_text = "do_laundry"
#     laundry_task_road = f"{casa_road},{laundry_task_text}"
#     assert joachim_assignment._idea_dict.get(casa_road) != None
#     assert joachim_assignment._idea_dict.get(basket_road) != None
#     assert joachim_assignment._idea_dict.get(b_full_road) != None
#     assert joachim_assignment._idea_dict.get(b_smel_road) != None
#     assert joachim_assignment._idea_dict.get(b_bare_road) != None
#     assert joachim_assignment._idea_dict.get(b_fine_road) != None
#     assert joachim_assignment._idea_dict.get(b_half_road) != None
#     assert joachim_assignment._idea_dict.get(laundry_task_road) != None

#     laundry_do_idea = joachim_assignment.get_idea_kid(laundry_task_road)
#     print(f"{laundry_do_idea.promise=}")
#     print(f"{laundry_do_idea._requiredunits.keys()=}")
#     print(f"{laundry_do_idea._requiredunits.get(basket_road).sufffacts.keys()=}")
#     print(f"{laundry_do_idea._acptfactheirs=}")
#     print(f"{laundry_do_idea._assignedunit=}")

#     assert laundry_do_idea.promise == True
#     assert list(laundry_do_idea._requiredunits.keys()) == [basket_road]
#     laundry_do_sufffacts = laundry_do_idea._requiredunits.get(basket_road).sufffacts
#     assert list(laundry_do_sufffacts.keys()) == [b_full_road, b_smel_road]
#     assert list(laundry_do_idea._assignedunit._suffgroups.keys()) == [joachim_text]
#     assert list(laundry_do_idea._acptfactheirs.keys()) == [basket_road]

#     assert laundry_do_idea._acptfactheirs.get(basket_road).pick == b_full_road

#     # print(f"{laundry_do_idea=}")

#     # 'A'
#     # 'A,casa'
#     # 'A,casa,laundry basket status'
#     # 'A,casa,laundry basket status,smelly'
#     # 'A,casa,laundry baske...ry basket status,full'
#     # 'A,casa,laundry basket status,fine'
#     # 'A,casa,laundry basket status,bare'
#     # 'A,casa,do_laundry'

#     assert len(joachim_assignment.get_agenda_items()) == 1
#     assert joachim_assignment.get_agenda_items()[0]._label == "do_laundry"

#     assert 1 == 2

#     # america_person = ex.sys_get_person_obj(name=america_cx._owner)
#     # america_person.save_output_calendar_to_public()

#     # # Create person2
#     # joachim_text = "Joachim"
#     # ex.create_new_personunit(person_name=joachim_text)
#     # old_joa_person = ex.sys_get_person_obj(name=joachim_text)
#     # old_joa_person._set_depotlink(america_cx._ownert, depotlink_type="blind_trust")
#     # old_joa_person.save_output_calendar_to_public()
#     # old_joa_dest_c = ex.get_public_calendar(joachim_text)
#     # old_joa_agenda = old_joa_dest_c.get_agenda_items()
#     # assert len(old_joa_agenda) == 0

#     # # Create person1 task:
#     # #  create joachim member in America calendar
#     # america_person._set_depotlink(owner=joachim_text)

#     # casa_text = "casa"
#     # casa_road = f"{root_label()},{casa_text}"
#     # task_text = "do_laundry"
#     # task_road = f"{casa_road},{task_text}"
#     # req_base_text = "laundry basket status"
#     # req_base_road = f"{casa_road},{req_base_text}"
#     # req_pick_full_text = "full"
#     # req_pick_full_road = f"{req_base_road},{req_pick_full_text}"
#     # req_pick_smel_text = "smelly"
#     # req_pick_smel_road = f"{req_base_road},{req_pick_smel_text}"
#     # req_picks = {req_pick_full_road: -1, req_pick_smel_road: -1}
#     # req_pick_bare_text = "bare"
#     # req_pick_bare_road = f"{req_base_road},{req_pick_bare_text}"
#     # req_pick_fine_text = "fine"
#     # req_pick_fine_road = f"{req_base_road},{req_pick_fine_text}"
#     # req_pick_half_text = "half full"
#     # req_pick_half_road = f"{req_base_road},{req_pick_half_text}"
#     # req_not_picks = {
#     #     req_pick_bare_road: -1,
#     #     req_pick_fine_road: -1,
#     #     req_pick_half_road: -1,
#     # }
#     # for_group_x = {america_cx._owner: -1, joachim_text: -1}
#     # assigned_group_x = {joachim_text: -1}
#     # america_person.create_task(
#     #     task_road=task_road,
#     #     required_base=req_base_road,
#     #     required_picks=req_picks,
#     #     required_not_picks=req_not_picks,
#     #     for_groups=for_group_x,
#     #     assigned_group=assigned_group_x,
#     #     create_missing_ideas=True,
#     # )

#     # # WHEN
#     # america_person.save_output_calendar_to_public()
#     # new_joa_person = ex.sys_get_person_obj(name=joachim_text)
#     # new_joa_person.save_output_calendar_to_public()
#     # new_joa_dest_c = ex.get_public_calendar(joachim_text)
#     # new_joa_agenda = new_joa_dest_c.get_agenda_items()
#     # assert len(new_joa_agenda) == 1
#     # print(f"{new_joa_agenda[0]._label=}")
#     # assert new_joa_agenda[0]._label == task_text

#     assert 1 == 2
