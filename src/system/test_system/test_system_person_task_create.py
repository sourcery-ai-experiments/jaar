from src.system.system import SystemUnit
from src.system.examples.system_env_kit import (
    get_temp_env_name,
    env_dir_setup_cleanup,
    get_test_systems_dir,
)
from src.calendar.road import get_global_root_label as root_label
from src.system.examples.example_persons import get_calendar_assignment_laundry_example1


def test_system_ChangingOnePersonsFactChangesAnotherAgenda(env_dir_setup_cleanup):
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    # GIVEN
    america_text = "America"
    sx.create_new_personunit(person_name=america_text)
    america_px = sx.sys_get_person_obj(name=america_text)
    america_px.set_isol(get_calendar_assignment_laundry_example1())

    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    # set basket status to "bare"
    isol_x = america_px.get_isol().set_acptfact(base=basket_road, pick=b_bare_road)
    america_px.set_isol(isol_x)
    # save fact change to public
    america_px._admin.save_refreshed_output_to_public()
    print(f"{sx.get_public_calendar(america_text)._idearoot._acptfactunits.keys()=}")
    america_output = sx.get_public_calendar(america_text)

    # create assignment for Joachim
    joachim_text = "Joachim"
    sx.create_new_personunit(person_name=joachim_text)
    joachim_per = sx.sys_get_person_obj(name=joachim_text)
    joachim_per.set_depot_calendar(america_output, "assignment")
    old_joachim_cx = sx.get_person_output_calendar(joachim_text)
    print(f"{old_joachim_cx._members.keys()=}")
    print(f"{old_joachim_cx._idearoot._acptfactunits.keys()=}")
    basket_acptfact = old_joachim_cx._idearoot._acptfactunits.get(basket_road)
    print(f"{basket_acptfact.base=} {basket_acptfact.pick=}")
    assert len(old_joachim_cx.get_agenda_items()) == 0

    # WHEN
    # set basket status to "full"
    america_px.get_isol().set_acptfact(base=basket_road, pick=b_full_road)
    america_px._admin.save_refreshed_output_to_public()

    # THEN
    joachim_px = sx.sys_get_person_obj(name=joachim_text)
    new_joachim_cx = joachim_px._admin.get_refreshed_output_calendar()
    print(f"{new_joachim_cx._members.keys()=}")
    print(f"{new_joachim_cx._idearoot._acptfactunits.keys()=}")
    print(f"{len(new_joachim_cx._idearoot._acptfactunits.keys())=}")
    assert len(new_joachim_cx.get_agenda_items()) == 1

    assert 1 == 2

    # joachim_px = sx.sys_get_person_obj(name=joachim_text)
    # joachim_px.set_depot_calendar(america_text, depotlink_type="assignment")
    # old_joachim_cx = joachim_px._admin.get_refreshed_output_calendar()

    # # Create person1 task:
    # #  create joachim member in America calendar
    # america_px._set_depotlink(joachim_text)

    # casa_text = "casa"
    # casa_road = f"{root_label()},{casa_text}"
    # task_text = "do_laundry"
    # task_road = f"{casa_road},{task_text}"
    # req_base_text = "laundry basket status"
    # req_base_road = f"{casa_road},{req_base_text}"
    # req_pick_full_text = "full"
    # req_pick_full_road = f"{req_base_road},{req_pick_full_text}"
    # req_pick_smel_text = "smelly"
    # req_pick_smel_road = f"{req_base_road},{req_pick_smel_text}"
    # req_picks = {req_pick_full_road: -1, req_pick_smel_road: -1}
    # req_pick_bare_text = "bare"
    # req_pick_bare_road = f"{req_base_road},{req_pick_bare_text}"
    # req_pick_fine_text = "fine"
    # req_pick_fine_road = f"{req_base_road},{req_pick_fine_text}"
    # req_pick_half_text = "half full"
    # req_pick_half_road = f"{req_base_road},{req_pick_half_text}"
    # req_not_picks = {
    #     req_pick_bare_road: -1,
    #     req_pick_fine_road: -1,
    #     req_pick_half_road: -1,
    # }
    # for_group_x = {america_text: -1, joachim_text: -1}
    # assigned_group_x = {joachim_text: -1}
    # america_px.create_task(
    #     task_road=task_road,
    #     required_base=req_base_road,
    #     required_picks=req_picks,
    #     required_not_picks=req_not_picks,
    #     for_groups=for_group_x,
    #     assigned_group=assigned_group_x,
    #     create_missing_ideas=True,
    # )

    # # WHEN
    # america_px.save_output_calendar_to_public()
    # new_joa_person = sx.sys_get_person_obj(name=joachim_text)
    # new_joa_person.save_output_calendar_to_public()
    # new_joa_dest_c = sx.get_public_calendar(joachim_text)
    # new_joa_agenda = new_joa_dest_c.get_agenda_items()
    # assert len(new_joa_agenda) == 1
    # print(f"{new_joa_agenda[0]._label=}")
    # assert new_joa_agenda[0]._label == task_text

    # assert 1 == 2
