from src._road.road import (
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src.listen.filehub import filehub_shop
from src.listen.examples.examples import get_agenda_with_4_levels
from src.listen.examples.listen_env import (
    get_texas_filehub,
    get_listen_temp_env_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_FileHub_create_econ_dir_if_missing_CreatesDirectory(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_listen_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    assert os_path_exists(sue_filehub.econ_dir()) is False

    # WHEN
    sue_filehub.create_econ_dir_if_missing()

    # THEN
    assert os_path_exists(sue_filehub.econ_dir())


def test_FileHub_save_role_agenda_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_listen_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert sue_filehub.role_file_exists(bob_text) is False

    # WHEN
    sue_filehub.save_role_agenda(bob_agenda)

    # THEN
    assert sue_filehub.role_file_exists(bob_text)


def test_FileHub_role_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_listen_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert sue_filehub.role_file_exists(bob_text) is False

    # WHEN
    sue_filehub.save_role_agenda(bob_agenda)

    # THEN
    assert sue_filehub.role_file_exists(bob_text)


def test_FileHub_get_role_agenda_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_listen_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    sue_filehub.save_role_agenda(bob_agenda)

    # WHEN / THEN
    assert sue_filehub.get_role_agenda(bob_text).get_dict() == bob_agenda.get_dict()


def test_FileHub_delete_role_file_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    texas_filehub = get_texas_filehub()
    sue_agenda = get_agenda_with_4_levels()
    sue_text = sue_agenda._owner_id
    texas_filehub.save_role_agenda(sue_agenda)
    print(f"{texas_filehub.role_path(sue_text)=}")
    role_path = texas_filehub.role_path(sue_text)
    assert texas_filehub.role_file_exists(sue_text)

    # WHEN
    texas_filehub.delete_role_file(sue_text)

    # THEN
    assert texas_filehub.role_file_exists(sue_text) is False


def test_FileHub_save_job_agenda_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_listen_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert sue_filehub.job_file_exists(bob_text) is False

    # WHEN
    sue_filehub.save_job_agenda(bob_agenda)

    # THEN
    assert sue_filehub.job_file_exists(bob_text)


def test_FileHub_job_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_listen_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert sue_filehub.job_file_exists(bob_text) is False

    # WHEN
    sue_filehub.save_job_agenda(bob_agenda)

    # THEN
    assert sue_filehub.job_file_exists(bob_text)


def test_FileHub_get_job_agenda_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_listen_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    sue_filehub.save_job_agenda(bob_agenda)

    # WHEN / THEN
    assert sue_filehub.get_job_agenda(bob_text).get_dict() == bob_agenda.get_dict()


def test_FileHub_delete_job_file_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    texas_filehub = get_texas_filehub()
    sue_agenda = get_agenda_with_4_levels()
    sue_text = sue_agenda._owner_id
    texas_filehub.save_job_agenda(sue_agenda)
    print(f"{texas_filehub.job_path(sue_text)=}")
    assert texas_filehub.job_file_exists(sue_text)

    # WHEN
    texas_filehub.delete_job_file(sue_text)

    # THEN
    assert texas_filehub.job_file_exists(sue_text) is False


def test_FileHub_delete_treasury_db_file_DeletesFile(env_dir_setup_cleanup):
    # GIVEN
    texas_filehub = get_texas_filehub()
    texas_filehub.create_treasury_db_file()
    assert texas_filehub.treasury_db_file_exists()

    # WHEN
    texas_filehub.delete_treasury_db_file()

    # THEN
    assert texas_filehub.treasury_db_file_exists() is False
