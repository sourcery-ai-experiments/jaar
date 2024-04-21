# from src._road.road import create_road
# from src.econ.econ import econunit_shop
# from src.econ.examples.econ_env_kit import (
#     get_temp_env_econ_id,
#     env_dir_setup_cleanup,
#     get_test_econ_dir,
# )
# from src.econ.examples.example_clerks import (
#     get_agenda_assignment_laundry_example1,
# )


# def test_EconUnit_ChangingOneHealersBeliefChangesAnotherAgenda(env_dir_setup_cleanup):
#     # GIVEN
#     x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
#     amer_text = "Amer"
#     x_econ.create_clerkunit(clerk_id=amer_text)
#     amer_clerk = x_econ.get_clerkunit(clerk_id=amer_text)
#     laundry_agenda = get_agenda_assignment_laundry_example1()
#     laundry_agenda.set_world_id(x_econ.econ_id)
#     amer_clerk.set_role(laundry_agenda)

#     casa_text = "casa"
#     basket_text = "laundry basket status"
#     casa_road = x_econ.build_econ_road(casa_text)
#     basket_road = create_road(casa_road, basket_text)
#     # print(f"{x1_casa_road=} {basket_road=}")
#     # print(f"{x1_casa_road=} {x1_basket_road=}")
#     b_full_text = "full"
#     b_full_road = create_road(basket_road, b_full_text)
#     b_bare_text = "bare"
#     b_bare_road = create_road({basket_road}, {b_bare_text})
#     # set basket status to "bare"
#     role_x = amer_clerk.get_role().set_belief(base=basket_road, pick=b_bare_road)
#     amer_clerk.set_role(role_x)
#     # save belief change to jobs
#     amer_clerk.save_refreshed_job_to_jobs()
#     # print(f"{x_econ.get_refreshed_job(amer_text)._idearoot._beliefunits.keys()=}")
#     amer_output = x_econ.get_refreshed_job(amer_text)

#     # create assignment for Cali
#     cali_text = "Cali"
#     x_econ.create_clerkunit(clerk_id=cali_text)
#     cali_clerk = x_econ.get_clerkunit(clerk_id=cali_text)
#     cali_clerk.set_depot_agenda(amer_output)
#     old_cali_agenda = x_econ.get_refreshed_job(cali_text)
#     # print(f"{old_cali_agenda._partys.keys()=}")
#     # print(f"{old_cali_agenda._idearoot._beliefunits.keys()=}")
#     # basket_belief = old_cali_agenda._idearoot._beliefunits.get(basket_road)
#     # print(f"Cali: {basket_belief.base=} {basket_belief.pick=}")
#     assert len(old_cali_agenda.get_intent_dict()) == 0

#     # WHEN
#     # set basket status to "full"
#     amer_clerk.get_role().set_belief(base=basket_road, pick=b_full_road)
#     amer_clerk.set_role()
#     amer_clerk.save_refreshed_job_to_jobs()

#     cali_clerk.refresh_depot_agendas()
#     new_cali_agenda = cali_clerk.get_remelded_output_agenda()

#     # new_jobs_amer = x_econ.get_refreshed_job(amer_text)
#     # a_basket_belief = new_jobs_amer._idearoot._beliefunits.get(basket_road)
#     # print(f"Amer after when {a_basket_belief.base=} {a_basket_belief.pick=}")

#     # THEN
#     # print(f"{new_cali_agenda._partys.keys()=}")
#     # basket_belief = new_cali_agenda._idearoot._beliefunits.get(basket_road)
#     # print(f"{basket_belief.base=} {basket_belief.pick=}")
#     # print(f"{len(new_cali_agenda._idearoot._beliefunits.keys())=}")
#     assert len(new_cali_agenda.get_intent_dict()) == 1
#     laundry_task_text = "do_laundry"
#     casa_road = x_econ.build_econ_road(casa_text)
#     laundry_task_road = create_road(casa_road, laundry_task_text)
#     assert laundry_task_road in new_cali_agenda.get_intent_dict().keys()


# def test_EconUnit_clerk_MeldOrderChangesOutputBelief(env_dir_setup_cleanup):
#     # GIVEN
#     x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
#     amer_text = "Amer"
#     beto_text = "Beto"
#     x_econ.create_clerkunit(clerk_id=amer_text)
#     x_econ.create_clerkunit(clerk_id=beto_text)
#     amer_clerk = x_econ.get_clerkunit(clerk_id=amer_text)
#     beto_clerk = x_econ.get_clerkunit(clerk_id=beto_text)
#     # print(f"{beto_clerk=}")
#     laundry_agenda = get_agenda_assignment_laundry_example1()
#     laundry_agenda.set_world_id(x_econ.econ_id)
#     amer_clerk.set_role(laundry_agenda)
#     beto_clerk.set_role(laundry_agenda)

#     casa_text = "casa"
#     casa_road = create_road(x_econ.econ_id, casa_text)
#     basket_text = "laundry basket status"
#     basket_road = create_road(casa_road, basket_text)
#     b_full_text = "full"
#     b_full_road = create_road(basket_road, b_full_text)
#     b_bare_text = "bare"
#     b_bare_road = create_road(basket_road, b_bare_text)

#     # amer jobs laundry belief as "full"
#     amer_role_x = amer_clerk.get_role().set_belief(basket_road, b_full_road)
#     beto_role_x = beto_clerk.get_role().set_belief(basket_road, b_bare_road)

#     amer_clerk.set_role(amer_role_x)
#     beto_clerk.set_role(beto_role_x)
#     amer_clerk.save_refreshed_job_to_jobs()
#     beto_clerk.save_refreshed_job_to_jobs()
#     amer_output = x_econ.get_refreshed_job(amer_text)
#     beto_output = x_econ.get_refreshed_job(beto_text)

#     cali_text = "Cali"
#     x_econ.create_clerkunit(cali_text)
#     cali_kichen = x_econ.get_clerkunit(cali_text)
#     cali_kichen.set_depot_agenda(beto_output)
#     cali_kichen.set_depot_agenda(amer_output)

#     # WHEN
#     cali_kichen.save_refreshed_job_to_jobs()

#     # THEN
#     old_cali_output = x_econ.get_refreshed_job(cali_text)
#     assert len(old_cali_output.get_intent_dict()) == 0
#     old_cali_beliefs = old_cali_output._idearoot._beliefunits
#     # print(f"{old_cali_output._idearoot._beliefunits=}")
#     assert old_cali_beliefs.get(basket_road) != None
#     old_cali_basket_belief = old_cali_beliefs.get(basket_road)
#     # print(f"{old_cali_basket_belief.base=}")
#     # print(f"{old_cali_basket_belief.pick=}")
#     # print(f"{old_cali_basket_belief.open=}")
#     # print(f"{old_cali_basket_belief.nigh=}")
#     assert old_cali_basket_belief.pick == b_bare_road

#     # WHEN voice_rank is changed
#     cali_role = cali_kichen.get_role()
#     cali_amer_party = cali_role.get_party(amer_text)
#     cali_beto_party = cali_role.get_party(beto_text)
#     amer_voice_rank = 45
#     beto_voice_rank = 100
#     cali_amer_party.set_treasurying_data(None, None, None, voice_rank=amer_voice_rank)
#     cali_beto_party.set_treasurying_data(None, None, None, voice_rank=beto_voice_rank)
#     # print(f"{cali_amer_party._treasury_voice_rank=} {amer_voice_rank=}")
#     # print(f"{cali_beto_party._treasury_voice_rank=} {beto_voice_rank=}")

#     cali_kichen.set_role(cali_role)

#     print("get new role...")
#     # new_cali_role = cali_kichen.get_role()
#     # new_cali_amer_party = new_cali_role.get_party(amer_text)
#     # new_cali_beto_party = new_cali_role.get_party(beto_text)
#     # print(f"{new_cali_amer_party._treasury_voice_rank=} ")
#     # print(f"{new_cali_beto_party._treasury_voice_rank=} ")

#     cali_kichen.save_refreshed_job_to_jobs()

#     # THEN final belief changed
#     new_cali_output = x_econ.get_refreshed_job(cali_text)
#     assert len(new_cali_output.get_intent_dict()) == 1
#     new_cali_beliefs = new_cali_output._idearoot._beliefunits
#     # print(f"{new_cali_output._idearoot._beliefunits=}")
#     assert new_cali_beliefs.get(basket_road) != None
#     new_cali_basket_belief = new_cali_beliefs.get(basket_road)
#     print(f"{new_cali_basket_belief.base=}")
#     print(f"{new_cali_basket_belief.pick=}")
#     print(f"{new_cali_basket_belief.open=}")
#     print(f"{new_cali_basket_belief.nigh=}")
#     assert new_cali_basket_belief.pick == b_full_road
