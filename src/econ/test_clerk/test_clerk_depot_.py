# from src.agenda.agenda import agendaunit_shop, get_from_json as agenda_get_from_json
# from src.instrument.file import count_files, open_file
# from src.econ.clerk import clerkunit_shop

# from src.econ.examples.example_clerks import (
#     get_2node_agenda,
#     get_clerkunit_2agenda,
#     get_agenda_2CleanNodesRandomWeights as get_cal2nodes,
#     get_agenda_3CleanNodesRandomWeights as get_cal3nodes,
#     get_agenda_assignment_laundry_example1 as get_amer_assign_ex,
# )
# from src.econ.examples.clerk_env_kit import (
#     clerk_dir_setup_cleanup,
#     get_temp_clerkunit_dir,
#     get_temp_econ_id,
#     create_agenda_file,
# )
# from src.econ.examples.econ_env_kit import get_temp_env_econ_id
# from src.econ.econ import econunit_shop
# from os import path as os_path
# from os.path import exists as os_path_exists
# from pytest import raises as pytest_raises


# def test_clerkunit__set_depot_agenda_SetsCorrectInfo(clerk_dir_setup_cleanup):
#     # GIVEN
#     x_clerk = get_clerkunit_2agenda(get_temp_clerkunit_dir(), get_temp_econ_id())
#     a_text = "A"
#     j_text = "J"
#     xio_text = "Xio"
#     yao_text = "yoa"
#     zia_text = "Zia"
#     print(f"{x_clerk._role._partys.keys()=}")
#     assert len(x_clerk._role._partys) == 3
#     assert x_clerk._role._partys.get(xio_text) != None
#     assert x_clerk._role._partys.get(a_text) != None
#     assert x_clerk._role._partys.get(j_text) != None
#     a_filepath = f"{x_clerk._agendas_depot_dir}/{a_text}.json"
#     j_filepath = f"{x_clerk._agendas_depot_dir}/{j_text}.json"
#     xio_filepath = f"{x_clerk._agendas_depot_dir}/{xio_text}.json"
#     yao_filepath = f"{x_clerk._agendas_depot_dir}/{yao_text}.json"
#     zia_filepath = f"{x_clerk._agendas_depot_dir}/{zia_text}.json"
#     assert os_path_exists(a_filepath)
#     assert os_path_exists(j_filepath)
#     assert os_path_exists(xio_filepath) == False
#     assert os_path_exists(yao_filepath) == False
#     assert os_path_exists(zia_filepath) == False

#     # WHEN
#     x_clerk._set_depot_agenda(agendaunit_shop(zia_text))
#     x_clerk._set_depot_agenda(agendaunit_shop(yao_text))

#     # THEN
#     print(f"{x_clerk._role._partys.keys()=}")
#     assert len(x_clerk._role._partys) == 3
#     assert x_clerk._role._partys.get(xio_text) != None
#     assert x_clerk._role._partys.get(a_text) != None
#     assert x_clerk._role._partys.get(j_text) != None
#     assert os_path_exists(a_filepath)
#     assert os_path_exists(j_filepath)
#     assert os_path_exists(xio_filepath) == False
#     assert os_path_exists(yao_filepath)
#     assert os_path_exists(zia_filepath)


# def test_clerkunit_create_digested_item_from_depot_item_RaisesErrorWhenAgendaDoesNotExist(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     sue_text = "Sue"
#     env_dir = get_temp_clerkunit_dir()
#     sue_clerkunit = clerkunit_shop(sue_text, env_dir, get_temp_econ_id())
#     sue_clerkunit.set_role_if_empty()
#     tim_text = "Tim"
#     assert list(sue_clerkunit._role._partys.keys()) == [sue_text]

#     # WHEN / THEN
#     file_path_x = f"{sue_clerkunit._agendas_depot_dir}/{tim_text}.json"
#     print(f"{file_path_x=}")
#     with pytest_raises(Exception) as excinfo:
#         sue_clerkunit._create_digested_item_from_depot_item(outer_owner_id=tim_text)
#     assert (
#         str(excinfo.value)
#         == f"owner_id {sue_text} cannot find agenda {tim_text} in {file_path_x}"
#     )


# def test_clerkunit_create_digested_item_from_depot_item_CorrectlySetsAssignment(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     amer_agenda = get_amer_assign_ex()
#     print(f"{len(amer_agenda._idea_dict)=}")
#     cali_text = "Cali"
#     cali_clerkunit = clerkunit_shop(
#         cali_text, get_temp_clerkunit_dir(), get_temp_econ_id()
#     )
#     cali_clerkunit.create_core_dir_aand_files()
#     cali_clerkunit.set_role_if_empty()
#     cali_clerkunit._save_agenda_to_depot(amer_agenda)
#     assert cali_clerkunit.get_role().get_party(amer_agenda._owner_id) is None
#     amer_digest_path = (
#         f"{cali_clerkunit._agendas_digest_dir}/{amer_agenda._owner_id}.json"
#     )
#     assert os_path.exists(amer_digest_path) is False

#     # WHEN
#     print("next set depot_item")
#     cali_clerkunit._create_digested_item_from_depot_item(amer_agenda._owner_id)
#     print("after set depot_item")

#     # THEN
#     assert os_path.exists(amer_digest_path)
#     digest_agenda = agenda_get_from_json(
#         open_file(
#             dest_dir=cali_clerkunit._agendas_digest_dir,
#             file_name=f"{amer_agenda._owner_id}.json",
#         )
#     )
#     print(f"{digest_agenda._owner_id=}")
#     print(f"{len(digest_agenda._idea_dict)=}")
#     digest_agenda.set_agenda_metrics()
#     assert len(digest_agenda._idea_dict) == 9
#     assert digest_agenda._owner_id == cali_text


# def test_clerkunit_del_depot_agenda_CorrectlyDeletesObj(clerk_dir_setup_cleanup):
#     # GIVEN
#     bob_text = "Bob"
#     env_dir = get_temp_clerkunit_dir()
#     bob_clerkunit = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
#     yao_text = "Yao"
#     create_agenda_file(bob_clerkunit._agendas_depot_dir, yao_text)
#     yao_depot_agenda_path = f"{bob_clerkunit._agendas_depot_dir}/{yao_text}.json"
#     bob_clerkunit._create_digested_item_from_depot_item(yao_text)
#     assert list(bob_clerkunit._role._partys.keys()) == [bob_text, yao_text]

#     # WHEN
#     bob_clerkunit.del_depot_agenda(owner_id=yao_text)

#     # THEN
#     assert list(bob_clerkunit._role._partys.keys()) == [bob_text, yao_text]


# def test_clerkunit_del_depot_agenda_CorrectlyDeletesBlindTrustFile(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     bob_text = "Bob"
#     env_dir = get_temp_clerkunit_dir()
#     bob_clerkunit = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
#     lai_text = "Lai"
#     create_agenda_file(bob_clerkunit._agendas_depot_dir, lai_text)
#     bob_clerkunit.set_role_if_empty()
#     bob_clerkunit._create_digested_item_from_depot_item(lai_text)
#     assert count_files(dir_path=bob_clerkunit._agendas_depot_dir) == 1
#     assert count_files(dir_path=bob_clerkunit._agendas_digest_dir) == 1

#     # WHEN
#     bob_clerkunit.del_depot_agenda(owner_id=lai_text)

#     # THEN
#     assert count_files(dir_path=bob_clerkunit._agendas_depot_dir) == 0
#     assert count_files(dir_path=bob_clerkunit._agendas_digest_dir) == 0


# def test_clerkunit__set_depot_agenda_SavesFileCorrectly(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     bob_text = "Bob"
#     env_dir = get_temp_clerkunit_dir()
#     bob_clerkunit = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
#     cal1 = get_2node_agenda()
#     assert count_files(bob_clerkunit._agendas_depot_dir) is None  # dir does not exist

#     # WHEN
#     bob_clerkunit.set_role_if_empty()
#     bob_clerkunit._set_depot_agenda(x_agenda=cal1)

#     # THEN
#     print(f"Saving to {bob_clerkunit._agendas_depot_dir=}")
#     # for path_x in os_scandir(ux._agendas_depot_dir):
#     #     print(f"{path_x=}")
#     assert count_files(bob_clerkunit._agendas_depot_dir) == 1


# def test_clerkunit_delete_ignore_depot_item_CorrectlyDeletesObj(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     bob_text = "Bob"
#     env_dir = get_temp_clerkunit_dir()
#     bob_clerkunit = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
#     yao_text = "Yao"
#     create_agenda_file(bob_clerkunit._agendas_depot_dir, yao_text)
#     bob_clerkunit.set_role_if_empty()
#     bob_clerkunit._create_digested_item_from_depot_item(yao_text)
#     assert list(bob_clerkunit._role._partys.keys()) == [bob_text, yao_text]

#     # WHEN
#     bob_clerkunit.del_depot_agenda(owner_id=yao_text)

#     # THEN
#     assert list(bob_clerkunit._role._partys.keys()) == [bob_text, yao_text]
#     assert 1 == 2


# def test_clerkunit_del_depot_agenda_CorrectlyDoesNotDeletesIgnoreFile(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     bob_text = "Bob"
#     env_dir = get_temp_clerkunit_dir()
#     bob_clerkunit = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
#     zia_text = "Zia"
#     create_agenda_file(bob_clerkunit._agendas_depot_dir, zia_text)
#     bob_clerkunit.set_role_if_empty()
#     bob_clerkunit._create_digested_item_from_depot_item(zia_text)
#     assert count_files(dir_path=bob_clerkunit._agendas_depot_dir) == 1
#     assert count_files(dir_path=bob_clerkunit._agendas_digest_dir) == 1

#     # WHEN
#     bob_clerkunit.del_depot_agenda(owner_id=zia_text)

#     # THEN
#     assert count_files(dir_path=bob_clerkunit._agendas_depot_dir) == 0
#     assert count_files(dir_path=bob_clerkunit._agendas_digest_dir) == 0


# def test_clerkunit_refresh_depotlinks_CorrectlyPullsAlljobsAgendas(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     env_dir = get_temp_clerkunit_dir()
#     econ_id = get_temp_env_econ_id()
#     sx = econunit_shop(econ_id=econ_id, econ_dir=env_dir)
#     yao_text = "Yao"
#     sx.create_clerkunit(clerk_id=yao_text)
#     yao_agenda = sx.get_clerkunit(clerk_id=yao_text)
#     assert len(yao_agenda.get_remelded_output_agenda().get_idea_dict()) == 1

#     ernie_text = "ernie"
#     ernie_agenda = get_cal2nodes(_owner_id=ernie_text)
#     steve_text = "steve"
#     old_steve_agenda = get_cal2nodes(_owner_id=steve_text)
#     sx.save_file_to_jobs(ernie_agenda)
#     sx.save_file_to_jobs(old_steve_agenda)
#     yao_agenda._set_depot_agenda(x_agenda=ernie_agenda)
#     yao_agenda._set_depot_agenda(x_agenda=old_steve_agenda)

#     assert len(yao_agenda.get_remelded_output_agenda().get_idea_dict()) == 4
#     new_steve_agenda = get_cal3nodes(_owner_id=steve_text)
#     sx.save_file_to_jobs(new_steve_agenda)
#     print(f"{env_dir=} {yao_agenda._jobs_dir=}")
#     # for file_name in dir_files(dir_path=env_dir):
#     #     print(f"{bob_clerkunit._jobs_dir=} {file_name=}")

#     # for file_name in dir_files(dir_path=bob_clerkunit._jobs_dir):
#     #     print(f"{bob_clerkunit._jobs_dir=} {file_name=}")

#     # WHEN
#     yao_agenda.refresh_depot_agendas()

#     # THEN
#     assert len(yao_agenda.get_remelded_output_agenda().get_idea_dict()) == 5
#     assert 1 == 2
