from src._road.road import create_road
from src.agenda.examples.example_agendas import get_agenda_assignment_laundry_example1
from src.econ.econ import EconUnit


# def get_econ_WithLaundryTaskMeldFromOneClerkToAnother(x_econ: EconUnit):
#     yao_text = "Yao"
#     x_econ.create_clerkunit(clerk_id=yao_text)
#     yao_clerk = x_econ.get_clerkunit(clerk_id=yao_text)
#     laundry_agenda = get_agenda_assignment_laundry_example1()
#     laundry_agenda.set_real_id(x_econ.real_id)
#     print(f"{laundry_agenda._owner_id=}")
#     yao_clerk.set_role(laundry_agenda)

#     casa_text = "casa"
#     basket_text = "laundry basket status"
#     casa_road = x_econ.build_econ_road(casa_text)
#     basket_road = laundry_agenda.make_road(casa_road, basket_text)
#     # print(f"{x1_casa_road=} {basket_road=}")
#     # print(f"{x1_casa_road=} {x1_basket_road=}")
#     b_full_text = "full"
#     b_full_road = create_road(basket_road, b_full_text)
#     b_bare_text = "bare"
#     b_bare_road = create_road({basket_road}, {b_bare_text})
#     # set basket status to "bare"
#     role_x = yao_clerk.get_role().set_belief(base=basket_road, pick=b_bare_road)
#     yao_clerk.set_role(role_x)
#     # save belief change to jobs
#     yao_clerk.save_refreshed_job_to_jobs()
#     # print(f"{x_econ.get_file_in_jobs(yao_text)._idearoot._beliefunits.keys()=}")
#     yao_output = x_econ.get_file_in_jobs(yao_text)

#     # create assignment for Cali
#     cali_text = "Cali"
#     x_econ.create_clerkunit(clerk_id=cali_text)
#     cali_clerk = x_econ.get_clerkunit(clerk_id=cali_text)
#     cali_clerk.set_depot_agenda(yao_output, "assignment")
#     old_cali_agenda = x_econ.get_job_agenda(cali_text)
#     # print(f"{old_cali_agenda._partys.keys()=}")
#     # print(f"{old_cali_agenda._idearoot._beliefunits.keys()=}")
#     # basket_belief = old_cali_agenda._idearoot._beliefunits.get(basket_road)
#     # print(f"Cali: {basket_belief.base=} {basket_belief.pick=}")
#     assert len(old_cali_agenda.get_intent_dict()) == 0

#     # WHEN
#     # set basket status to "full"
#     yao_clerk.get_role().set_belief(base=basket_road, pick=b_full_road)
#     yao_clerk.set_role()
#     yao_clerk.save_refreshed_job_to_jobs()

#     cali_clerk.refresh_depot_agendas()
#     new_cali_agenda = cali_clerk.get_remelded_output_agenda()

#     # new_jobs_yao = x_econ.get_file_in_jobs(yao_text)
#     # a_basket_belief = new_jobs_yao._idearoot._beliefunits.get(basket_road)
#     # print(f"Yao after when {a_basket_belief.base=} {a_basket_belief.pick=}")

#     # THEN
#     # print(f"{new_cali_agenda._partys.keys()=}")
#     # basket_belief = new_cali_agenda._idearoot._beliefunits.get(basket_road)
#     # print(f"{basket_belief.base=} {basket_belief.pick=}")
#     # print(f"{len(new_cali_agenda._idearoot._beliefunits.keys())=}")
#     assert len(new_cali_agenda.get_intent_dict()) == 1
#     laundry_task_text = "do_laundry"
#     casa_road = x_econ.build_econ_road(casa_text)
#     laundry_task_road = create_road(casa_road, laundry_task_text)
#     assert new_cali_agenda.get_intent_dict()[0].get_road() == laundry_task_road
