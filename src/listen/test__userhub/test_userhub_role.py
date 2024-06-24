from src._road.road import (
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src.listen.userhub import userhub_shop
from src.listen.examples.example_listen_truths import get_truth_with_4_levels
from src.listen.examples.listen_env import (
    get_texas_userhub,
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_UserHub_create_econ_dir_if_missing_CreatesDirectory(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    assert os_path_exists(sue_userhub.econ_dir()) is False

    # WHEN
    sue_userhub.create_econ_dir_if_missing()

    # THEN
    assert os_path_exists(sue_userhub.econ_dir())


def test_UserHub_save_role_truth_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_truth = get_truth_with_4_levels()
    bob_truth.set_owner_id(bob_text)
    assert sue_userhub.role_file_exists(bob_text) is False

    # WHEN
    sue_userhub.save_role_truth(bob_truth)

    # THEN
    assert sue_userhub.role_file_exists(bob_text)


def test_UserHub_role_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_truth = get_truth_with_4_levels()
    bob_truth.set_owner_id(bob_text)
    assert sue_userhub.role_file_exists(bob_text) is False

    # WHEN
    sue_userhub.save_role_truth(bob_truth)

    # THEN
    assert sue_userhub.role_file_exists(bob_text)


def test_UserHub_get_role_truth_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_truth = get_truth_with_4_levels()
    bob_truth.set_owner_id(bob_text)
    sue_userhub.save_role_truth(bob_truth)

    # WHEN / THEN
    assert sue_userhub.get_role_truth(bob_text).get_dict() == bob_truth.get_dict()


def test_UserHub_delete_role_file_DeletesTruthFile(env_dir_setup_cleanup):
    # GIVEN
    texas_userhub = get_texas_userhub()
    sue_truth = get_truth_with_4_levels()
    sue_text = sue_truth._owner_id
    texas_userhub.save_role_truth(sue_truth)
    print(f"{texas_userhub.role_path(sue_text)=}")
    role_path = texas_userhub.role_path(sue_text)
    assert texas_userhub.role_file_exists(sue_text)

    # WHEN
    texas_userhub.delete_role_file(sue_text)

    # THEN
    assert texas_userhub.role_file_exists(sue_text) is False


def test_UserHub_save_job_truth_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_truth = get_truth_with_4_levels()
    bob_truth.set_owner_id(bob_text)
    assert sue_userhub.job_file_exists(bob_text) is False

    # WHEN
    sue_userhub.save_job_truth(bob_truth)

    # THEN
    assert sue_userhub.job_file_exists(bob_text)


def test_UserHub_job_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_truth = get_truth_with_4_levels()
    bob_truth.set_owner_id(bob_text)
    assert sue_userhub.job_file_exists(bob_text) is False

    # WHEN
    sue_userhub.save_job_truth(bob_truth)

    # THEN
    assert sue_userhub.job_file_exists(bob_text)


def test_UserHub_get_job_truth_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"
    bob_truth = get_truth_with_4_levels()
    bob_truth.set_owner_id(bob_text)
    sue_userhub.save_job_truth(bob_truth)

    # WHEN / THEN
    assert sue_userhub.get_job_truth(bob_text).get_dict() == bob_truth.get_dict()


def test_UserHub_get_job_truth_ReturnsNoneIfFileDoesNotExist(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_userhub = userhub_shop(env_dir(), None, sue_text, texas_road)
    bob_text = "Bob"

    # WHEN / THEN
    assert sue_userhub.get_job_truth(bob_text) is None


def test_UserHub_delete_job_file_DeletesTruthFile(env_dir_setup_cleanup):
    # GIVEN
    texas_userhub = get_texas_userhub()
    sue_truth = get_truth_with_4_levels()
    sue_text = sue_truth._owner_id
    texas_userhub.save_job_truth(sue_truth)
    print(f"{texas_userhub.job_path(sue_text)=}")
    assert texas_userhub.job_file_exists(sue_text)

    # WHEN
    texas_userhub.delete_job_file(sue_text)

    # THEN
    assert texas_userhub.job_file_exists(sue_text) is False


def test_UserHub_delete_treasury_db_file_DeletesFile(env_dir_setup_cleanup):
    # GIVEN
    texas_userhub = get_texas_userhub()
    texas_userhub.create_treasury_db_file()
    assert texas_userhub.treasury_db_file_exists()

    # WHEN
    texas_userhub.delete_treasury_db_file()

    # THEN
    assert texas_userhub.treasury_db_file_exists() is False
