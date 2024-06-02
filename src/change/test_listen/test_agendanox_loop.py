# from src._road.road import (
#     default_road_delimiter_if_none,
#     create_road_from_nodes,
#     create_road,
#     get_default_real_id_roadnode as root_label,
# )
# from src._road.finance import default_planck_if_none
# from src.change.agendanox import usernox_shop, get_econ_path, AgendaNox, agendanox_shop
# from src._road.jaar_config import (
#     get_changes_folder,
#     duty_str,
#     work_str,
#     get_test_reals_dir,
#     get_test_real_id,
#     get_rootpart_of_econ_dir,
# )
# from src.change.examples.change_env import (
#     env_dir_setup_cleanup,
#     get_change_temp_env_dir,
# )
# from pytest import raises as pytest_raises
# from os.path import exists as os_path_exists


# def test_AgendaNox_save_file_role_CorrectlySavesFile(env_dir_setup_cleanup):
#     # GIVEN
#     sue_text = "Sue"
#     nation_text = "nation-state"
#     nation_road = create_road(root_label(), nation_text)
#     usa_text = "USA"
#     usa_road = create_road(nation_road, usa_text)
#     texas_text = "Texas"
#     texas_road = create_road(usa_road, texas_text)
#     sue_agendanox = agendanox_shop(
#         get_change_temp_env_dir(), None, sue_text, texas_road
#     )
#     bob_text = "Bob"
#     assert os_path_exists(sue_agendanox.role_path(bob_text)) == False

#     # WHEN
#     sue_agendanox.save_file_role(bob_text, file_text="fooboo", replace=True)

#     # THEN
#     assert os_path_exists(sue_agendanox.role_path(bob_text))


# def test_AgendaNox_role_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
#     # GIVEN
#     sue_text = "Sue"
#     nation_text = "nation-state"
#     nation_road = create_road(root_label(), nation_text)
#     usa_text = "USA"
#     usa_road = create_road(nation_road, usa_text)
#     texas_text = "Texas"
#     texas_road = create_road(usa_road, texas_text)
#     sue_agendanox = agendanox_shop(
#         get_change_temp_env_dir(), None, sue_text, texas_road
#     )
#     bob_text = "Bob"
#     assert sue_agendanox.role_file_exists(bob_text) == False

#     # WHEN
#     sue_agendanox.save_file_role(bob_text, file_text="fooboo", replace=True)

#     # THEN
#     assert sue_agendanox.role_file_exists(bob_text)


# def test_AgendaNox_open_file_role_OpensFile(env_dir_setup_cleanup):
#     # GIVEN
#     sue_text = "Sue"
#     nation_text = "nation-state"
#     nation_road = create_road(root_label(), nation_text)
#     usa_text = "USA"
#     usa_road = create_road(nation_road, usa_text)
#     texas_text = "Texas"
#     texas_road = create_road(usa_road, texas_text)
#     sue_agendanox = agendanox_shop(
#         get_change_temp_env_dir(), None, sue_text, texas_road
#     )
#     example_text = "fooboo"
#     bob_text = "Bob"
#     sue_agendanox.save_file_role(bob_text, example_text, replace=True)

#     # WHEN / THEN
#     assert sue_agendanox.open_file_role(bob_text) == example_text


# def test_AgendaNox_save_file_job_CorrectlySavesFile(env_dir_setup_cleanup):
#     # GIVEN
#     sue_text = "Sue"
#     nation_text = "nation-state"
#     nation_road = create_road(root_label(), nation_text)
#     usa_text = "USA"
#     usa_road = create_road(nation_road, usa_text)
#     texas_text = "Texas"
#     texas_road = create_road(usa_road, texas_text)
#     sue_agendanox = agendanox_shop(
#         get_change_temp_env_dir(), None, sue_text, texas_road
#     )
#     bob_text = "Bob"
#     assert os_path_exists(sue_agendanox.job_path(bob_text)) == False

#     # WHEN
#     sue_agendanox.save_file_job(bob_text, file_text="fooboo", replace=True)

#     # THEN
#     assert os_path_exists(sue_agendanox.job_path(bob_text))


# def test_AgendaNox_job_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
#     # GIVEN
#     sue_text = "Sue"
#     nation_text = "nation-state"
#     nation_road = create_road(root_label(), nation_text)
#     usa_text = "USA"
#     usa_road = create_road(nation_road, usa_text)
#     texas_text = "Texas"
#     texas_road = create_road(usa_road, texas_text)
#     sue_agendanox = agendanox_shop(
#         get_change_temp_env_dir(), None, sue_text, texas_road
#     )
#     bob_text = "Bob"
#     assert sue_agendanox.job_file_exists(bob_text) == False

#     # WHEN
#     sue_agendanox.save_file_job(bob_text, file_text="fooboo", replace=True)

#     # THEN
#     assert sue_agendanox.job_file_exists(bob_text)


# def test_AgendaNox_open_file_job_OpensFile(env_dir_setup_cleanup):
#     # GIVEN
#     sue_text = "Sue"
#     nation_text = "nation-state"
#     nation_road = create_road(root_label(), nation_text)
#     usa_text = "USA"
#     usa_road = create_road(nation_road, usa_text)
#     texas_text = "Texas"
#     texas_road = create_road(usa_road, texas_text)
#     sue_agendanox = agendanox_shop(
#         get_change_temp_env_dir(), None, sue_text, texas_road
#     )
#     example_text = "fooboo"
#     bob_text = "Bob"
#     sue_agendanox.save_file_job(bob_text, example_text, replace=True)

#     # WHEN / THEN
#     assert sue_agendanox.open_file_job(bob_text) == example_text
