from src._instrument.file import delete_dir
from src._road.jaar_config import init_change_id, get_test_real_id as real_id
from src.listen.filehub import filehub_shop
from src.listen.examples.example_listen_changes import sue_2atomunits_changeunit
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_FileHub_default_duty_agenda_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"
    point_five_float = 0.5
    sue_filehub = filehub_shop(
        env_dir(),
        real_id(),
        sue_text,
        econ_road=None,
        nox_type=None,
        road_delimiter=slash_text,
        planck=point_five_float,
    )

    # WHEN
    sue_default_duty = sue_filehub.default_duty_agenda()

    # THEN
    assert sue_default_duty._real_id == sue_filehub.real_id
    assert sue_default_duty._owner_id == sue_filehub.person_id
    assert sue_default_duty._road_delimiter == sue_filehub.road_delimiter
    assert sue_default_duty._planck == sue_filehub.planck


def test_FileHub_delete_duty_file_DeletesDutyFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), real_id(), sue_text)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    assert sue_filehub.duty_file_exists()

    # WHEN
    sue_filehub.delete_duty_file()

    # THEN
    assert sue_filehub.duty_file_exists() is False


def test_FileHub_create_initial_change_files_from_default_CorrectlySavesChangeUnitFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    init_change_file_name = sue_filehub.change_file_name(init_change_id())
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_file_name}"
    assert os_path_exists(init_change_file_path) is False
    assert sue_filehub.duty_file_exists() is False

    # WHEN
    sue_filehub._create_initial_change_files_from_default()

    # THEN
    assert os_path_exists(init_change_file_path)
    assert sue_filehub.duty_file_exists() is False


def test_FileHub_create_duty_from_changes_CreatesDutyFileFromChangeFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    init_change_file_name = sue_filehub.change_file_name(init_change_id())
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_file_name}"
    sue_filehub._create_initial_change_files_from_default()
    assert os_path_exists(init_change_file_path)
    assert sue_filehub.duty_file_exists() is False

    # WHEN
    sue_filehub._create_duty_from_changes()

    # THEN
    assert sue_filehub.duty_file_exists()
    static_sue_duty = sue_filehub._merge_any_changes(sue_filehub.default_duty_agenda())
    assert sue_filehub.get_duty_agenda().get_dict() == static_sue_duty.get_dict()


def test_FileHub_create_initial_change_and_duty_files_CreatesChangeFilesAndDutyFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    init_change_file_name = sue_filehub.change_file_name(init_change_id())
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_file_name}"
    assert os_path_exists(init_change_file_path) is False
    assert sue_filehub.duty_file_exists() is False

    # WHEN
    sue_filehub._create_initial_change_and_duty_files()

    # THEN
    assert os_path_exists(init_change_file_path)
    assert sue_filehub.duty_file_exists()
    static_sue_duty = sue_filehub._merge_any_changes(sue_filehub.default_duty_agenda())
    assert sue_filehub.get_duty_agenda().get_dict() == static_sue_duty.get_dict()


def test_FileHub_create_initial_change_files_from_duty_SavesOnlyChangeFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    sue_duty_agenda = sue_filehub.default_duty_agenda()
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    assert sue_filehub.duty_file_exists() is False
    sue_filehub.save_duty_agenda(sue_duty_agenda)
    assert sue_filehub.duty_file_exists()
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    assert os_path_exists(init_change_file_path) is False

    # WHEN
    sue_filehub._create_initial_change_files_from_duty()

    # THEN
    assert os_path_exists(init_change_file_path)


def test_FileHub_initialize_change_duty_files_CorrectlySavesDutyFileAndChangeFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    assert sue_filehub.duty_file_exists() is False
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    delete_dir(sue_filehub.changes_dir())
    assert os_path_exists(init_change_file_path) is False

    # WHEN
    sue_filehub.initialize_change_duty_files()

    # THEN
    duty_agenda = sue_filehub.get_duty_agenda()
    assert duty_agenda._real_id == real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_change_file_path)


def test_FileHub_initialize_change_duty_files_CorrectlySavesOnlyDutyFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    sue_filehub.initialize_change_duty_files()
    assert sue_filehub.duty_file_exists()
    sue_filehub.delete_duty_file()
    assert sue_filehub.duty_file_exists() is False
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    assert os_path_exists(init_change_file_path)

    # WHEN
    sue_filehub.initialize_change_duty_files()

    # THEN
    duty_agenda = sue_filehub.get_duty_agenda()
    assert duty_agenda._real_id == real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_change_file_path)


def test_FileHub_initialize_change_duty_files_CorrectlySavesOnlychangeFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    sue_filehub.initialize_change_duty_files()
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    sue_filehub.save_duty_agenda(sue_duty_agenda)
    assert sue_filehub.duty_file_exists()
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    delete_dir(sue_filehub.changes_dir())
    assert os_path_exists(init_change_file_path) is False

    # WHEN
    sue_filehub.initialize_change_duty_files()

    # THEN
    assert sue_duty_agenda._real_id == real_id()
    assert sue_duty_agenda._owner_id == sue_text
    assert sue_duty_agenda._planck == seven_int
    assert sue_duty_agenda.party_exists(bob_text)
    assert os_path_exists(init_change_file_path)


def test_FileHub_append_changes_to_duty_file_AddschangesToDutyFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), real_id(), sue_text)
    sue_filehub.initialize_change_duty_files()
    sue_filehub.save_change_file(sue_2atomunits_changeunit())
    duty_agenda = sue_filehub.get_duty_agenda()
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) is False
    assert duty_agenda.idea_exists(knee_road) is False

    # WHEN
    new_agenda = sue_filehub.append_changes_to_duty_file()

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)
