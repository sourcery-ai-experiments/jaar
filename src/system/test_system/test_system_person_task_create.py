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
from src.calendar.road import (
    road_validate,
    get_global_root_label as root_label,
    get_road_from_nodes,
)
from os import path as os_path
from pytest import raises as pytest_raises


# def test_system_person1_set_laundry_fact_create_person2_laundry_task(
#     env_dir_setup_cleanup,
# ):
#     ex = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
#     ex.create_dirs_if_null(in_memory_bank=True)

#     # GIVEN
#     # Create person1
#     america_text = "America"
#     ex.create_new_personunit(person_name=america_text)
#     america_person = ex.sys_get_person_obj(name=america_text)
#     america_person.save_output_calendar_to_public()

#     # Create person2
#     joachim_text = "Joachim"
#     ex.create_new_personunit(person_name=joachim_text)
#     old_joa_person = ex.sys_get_person_obj(name=joachim_text)
#     old_joa_person._set_depotlink(america_text, depotlink_type="blind_trust")
#     old_joa_person.save_output_calendar_to_public()
#     old_joa_dest_c = ex.get_public_calendar(joachim_text)
#     old_joa_agenda = old_joa_dest_c.get_agenda_items()
#     assert len(old_joa_agenda) == 0

#     # Create person1 task:
#     #  create joachim member in America calendar
#     america_person._set_depotlink(owner=joachim_text)

#     casa_text = "casa"
#     casa_road = f"{root_label()},{casa_text}"
#     task_text = "do_laundry"
#     task_road = f"{casa_road},{task_text}"
#     req_base_text = "laundry basket status"
#     req_base_road = f"{casa_road},{req_base_text}"
#     req_pick_full_text = "full"
#     req_pick_full_road = f"{req_base_road},{req_pick_full_text}"
#     req_pick_smel_text = "smelly"
#     req_pick_smel_road = f"{req_base_road},{req_pick_smel_text}"
#     req_picks = {req_pick_full_road: -1, req_pick_smel_road: -1}
#     req_pick_bare_text = "bare"
#     req_pick_bare_road = f"{req_base_road},{req_pick_bare_text}"
#     req_pick_fine_text = "fine"
#     req_pick_fine_road = f"{req_base_road},{req_pick_fine_text}"
#     req_pick_half_text = "half full"
#     req_pick_half_road = f"{req_base_road},{req_pick_half_text}"
#     req_not_picks = {
#         req_pick_bare_road: -1,
#         req_pick_fine_road: -1,
#         req_pick_half_road: -1,
#     }
#     for_group_x = {america_text: -1, joachim_text: -1}
#     assigned_group_x = {joachim_text: -1}
#     america_person.create_task(
#         task_road=task_road,
#         required_base=req_base_road,
#         required_picks=req_picks,
#         required_not_picks=req_not_picks,
#         for_groups=for_group_x,
#         assigned_group=assigned_group_x,
#         create_missing_ideas=True,
#     )

#     # WHEN
#     america_person.save_output_calendar_to_public()
#     new_joa_person = ex.sys_get_person_obj(name=joachim_text)
#     new_joa_person.save_output_calendar_to_public()
#     new_joa_dest_c = ex.get_public_calendar(joachim_text)
#     new_joa_agenda = new_joa_dest_c.get_agenda_items()
#     assert len(new_joa_agenda) == 1
#     print(f"{new_joa_agenda[0]._label=}")
#     assert new_joa_agenda[0]._label == task_text

#     assert 1 == 2
