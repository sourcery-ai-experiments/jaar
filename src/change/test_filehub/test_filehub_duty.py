from src._instrument.file import open_file, dir_files, delete_dir, set_dir, save_file
from src._road.jaar_config import init_change_id
from src._road.road import get_default_real_id_roadnode as root_label
from src.change.change import changeunit_shop, get_json_filename
from src.change.filehub import filehub_shop
from src.change.examples.example_change_atoms import get_atom_example_ideaunit_knee
from src.change.examples.example_change_changes import (
    get_sue_changeunit,
    sue_1atomunits_changeunit,
    sue_2atomunits_changeunit,
    sue_3atomunits_changeunit,
    sue_4atomunits_changeunit,
)
from src.change.examples.change_env import (
    env_dir_setup_cleanup,
    get_change_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_FileHub_default_duty_agenda_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"
    point_five_float = 0.5
    sue_filehub = filehub_shop(
        env_dir(),
        root_label(),
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
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    assert sue_filehub.duty_file_exists()

    # WHEN
    sue_filehub.delete_duty_file()

    # THEN
    assert sue_filehub.duty_file_exists() == False


def test_FileHub_create_initial_change_files_from_default_CorrectlySavesChangeUnitFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(
        env_dir(), root_label(), sue_text, None, planck=seven_int
    )
    init_change_file_name = sue_filehub.change_file_name(init_change_id())
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_file_name}"
    assert os_path_exists(init_change_file_path) == False
    assert sue_filehub.duty_file_exists() == False

    # WHEN
    sue_filehub._create_initial_change_files_from_default()

    # THEN
    assert os_path_exists(init_change_file_path)
    assert sue_filehub.duty_file_exists() == False


def test_FileHub_create_duty_from_changes_CreatesDutyFileFromChangeFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(
        env_dir(), root_label(), sue_text, None, planck=seven_int
    )
    init_change_file_name = sue_filehub.change_file_name(init_change_id())
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_file_name}"
    sue_filehub._create_initial_change_files_from_default()
    assert os_path_exists(init_change_file_path)
    assert sue_filehub.duty_file_exists() == False

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
    sue_filehub = filehub_shop(
        env_dir(), root_label(), sue_text, None, planck=seven_int
    )
    init_change_file_name = sue_filehub.change_file_name(init_change_id())
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_file_name}"
    assert os_path_exists(init_change_file_path) == False
    assert sue_filehub.duty_file_exists() == False

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
    sue_filehub = filehub_shop(
        env_dir(), root_label(), sue_text, None, planck=seven_int
    )
    sue_duty_agenda = sue_filehub.default_duty_agenda()
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    assert sue_filehub.duty_file_exists() == False
    sue_filehub.save_duty_agenda(sue_duty_agenda)
    assert sue_filehub.duty_file_exists()
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    assert os_path_exists(init_change_file_path) == False

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
    sue_filehub = filehub_shop(
        env_dir(), root_label(), sue_text, None, planck=seven_int
    )
    assert sue_filehub.duty_file_exists() == False
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    delete_dir(sue_filehub.changes_dir())
    assert os_path_exists(init_change_file_path) == False

    # WHEN
    sue_filehub.initialize_change_duty_files()

    # THEN
    duty_agenda = sue_filehub.get_duty_agenda()
    assert duty_agenda._real_id == root_label()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_change_file_path)


def test_FileHub_initialize_change_duty_files_CorrectlySavesOnlyDutyFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(
        env_dir(), root_label(), sue_text, None, planck=seven_int
    )
    sue_filehub.initialize_change_duty_files()
    assert sue_filehub.duty_file_exists()
    sue_filehub.delete_duty_file()
    assert sue_filehub.duty_file_exists() == False
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    assert os_path_exists(init_change_file_path)

    # WHEN
    sue_filehub.initialize_change_duty_files()

    # THEN
    duty_agenda = sue_filehub.get_duty_agenda()
    assert duty_agenda._real_id == root_label()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_change_file_path)


def test_FileHub_initialize_change_duty_files_CorrectlySavesOnlychangeFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(
        env_dir(), root_label(), sue_text, None, planck=seven_int
    )
    sue_filehub.initialize_change_duty_files()
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    sue_filehub.save_duty_agenda(sue_duty_agenda)
    assert sue_filehub.duty_file_exists()
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    delete_dir(sue_filehub.changes_dir())
    assert os_path_exists(init_change_file_path) == False

    # WHEN
    sue_filehub.initialize_change_duty_files()

    # THEN
    assert sue_duty_agenda._real_id == root_label()
    assert sue_duty_agenda._owner_id == sue_text
    assert sue_duty_agenda._planck == seven_int
    assert sue_duty_agenda.party_exists(bob_text)
    assert os_path_exists(init_change_file_path)
