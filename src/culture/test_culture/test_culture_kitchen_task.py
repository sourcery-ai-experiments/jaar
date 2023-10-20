from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    env_dir_setup_cleanup,
    get_test_cultures_dir,
)
from src.culture.examples.example_kitchens import (
    get_agenda_assignment_laundry_example1,
)


def test_culture_ChangingOneHealersFactChangesAnotherAgenda(env_dir_setup_cleanup):
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    # GIVEN
    america_text = "America"
    x_culture.create_new_kitchenunit(kitchen_title=america_text)
    america_ux = x_culture.get_kitchenunit(title=america_text)
    laundry_agenda = get_agenda_assignment_laundry_example1()
    laundry_agenda.set_culture_handle(x_culture.handle)
    america_ux.set_seed(laundry_agenda)

    casa_text = "casa"
    casa_road = f"{x_culture.handle},{casa_text}"
    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    # set basket status to "bare"
    seed_x = america_ux.get_seed().set_acptfact(base=basket_road, pick=b_bare_road)
    america_ux.set_seed(seed_x)
    # save fact change to public
    america_ux._admin.save_refreshed_output_to_public()
    # print(f"{x_culture.get_public_agenda(america_text)._idearoot._acptfactunits.keys()=}")
    america_output = x_culture.get_public_agenda(america_text)

    # create assignment for Joachim
    joachim_text = "Joachim"
    x_culture.create_new_kitchenunit(kitchen_title=joachim_text)
    joachim_ux = x_culture.get_kitchenunit(title=joachim_text)
    joachim_ux.set_depot_agenda(america_output, "assignment")
    old_joachim_cx = x_culture.get_output_agenda(joachim_text)
    # print(f"{old_joachim_cx._partys.keys()=}")
    # print(f"{old_joachim_cx._idearoot._acptfactunits.keys()=}")
    basket_acptfact = old_joachim_cx._idearoot._acptfactunits.get(basket_road)
    # print(f"Joachim: {basket_acptfact.base=} {basket_acptfact.pick=}")
    assert len(old_joachim_cx.get_goal_items()) == 0

    # WHEN
    # set basket status to "full"
    america_ux.get_seed().set_acptfact(base=basket_road, pick=b_full_road)
    america_ux.set_seed()
    america_ux._admin.save_refreshed_output_to_public()

    joachim_ux.refresh_depot_agendas()
    new_joachim_cx = joachim_ux._admin.get_remelded_output_agenda()

    # new_public_america = x_culture.get_public_agenda(america_text)
    # a_basket_acptfact = new_public_america._idearoot._acptfactunits.get(basket_road)
    # print(f"America after when {a_basket_acptfact.base=} {a_basket_acptfact.pick=}")

    # THEN
    # print(f"{new_joachim_cx._partys.keys()=}")
    # basket_acptfact = new_joachim_cx._idearoot._acptfactunits.get(basket_road)
    # print(f"{basket_acptfact.base=} {basket_acptfact.pick=}")
    # print(f"{len(new_joachim_cx._idearoot._acptfactunits.keys())=}")
    assert len(new_joachim_cx.get_goal_items()) == 1
    laundry_task_text = "do_laundry"
    laundry_task_road = f"{casa_road},{laundry_task_text}"
    assert new_joachim_cx.get_goal_items()[0].get_road() == laundry_task_road


# def test_culture_create_task_CorrectlyCreatesTask(env_dir_setup_cleanup):
#     x_culture = cultureunit_shop(
#         handle=get_temp_env_handle(), cultures_dir=get_test_cultures_dir()
#     )
#     x_culture.create_dirs_if_null(in_memory_bank=True)

#     america_text = "America"
#     joachim_text = "Joachim"
#     casa_text = "casa"
#     casa_road = f"{root_label()},{casa_text}"
#     do_laundry_text = "do_laundry"
#     do_laundry_road = f"{casa_road},{do_laundry_text}"
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
#     x_culture.create_task(
#         from_healer=america_text,
#         to_group=joachim_text,
#         group_partys={joachim_text},
#         task_road=do_laundry_road,
#         required_base=req_base_road,
#         required_picks=req_picks,
#         required_not_picks=req_not_picks,
#         for_groups=for_group_x,
#         assigned_group=assigned_group_x,
#         create_missing_ideas=True,
#     )

#     # # WHEN
#     # america_healer.save_output_agenda_to_public()
#     # new_joa_healer = x_culture.get_kitchenunit(title=joachim_text)
#     # new_joa_healer.save_output_agenda_to_public()
#     # new_joa_dest_c = x_culture.get_public_agenda(joachim_text)
#     # new_joa_goal = new_joa_dest_c.get_goal_items()
#     # assert len(new_joa_goal) == 1
#     # print(f"{new_joa_goal[0]._label=}")
#     # assert new_joa_goal[0]._label == task_text
#     joachim_cx = x_culture.get_public_agenda(joachim_text)

#     assert len(joachim_cx.get_goal_items()) == 1
#     assert joachim_cx.get_goal_items()[0].get_road() == do_laundry_road

#     # x_culture.create_new_kitchenunit(kitchen_title=america_text)
#     # america_healer = x_culture.get_kitchenunit(title=america_text)
#     # america_healer.save_output_agenda_to_public()
#     # assert x_culture.get_public_agenda(america_text) != None

#     # # Create healer2

#     # x_culture.create_new_kitchenunit(kitchen_title=joachim_text)
#     # old_joa_healer = x_culture.get_kitchenunit(title=joachim_text)
#     # old_joa_healer._set_depotlink(america_cx._healert, depotlink_type="blind_trust")
#     # old_joa_healer.save_output_agenda_to_public()
#     # old_joa_dest_c = x_culture.get_public_agenda(joachim_text)
#     # old_joa_goal = old_joa_dest_c.get_goal_items()
#     # # assert len(old_joa_goal) == 0

#     # # # Create healer1 task:
#     # # #  create joachim party in America agenda
#     # america_healer._set_depotlink(joachim_text)
