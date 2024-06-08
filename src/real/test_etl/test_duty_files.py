from src._instrument.file import open_file, delete_dir
from src._road.jaar_config import init_change_id
from src.agenda.agenda import agendaunit_shop, get_from_json as agendaunit_get_from_json
from src.change.filehub import filehub_shop
from src.real.admin_duty import initialize_change_duty_files
from src.real.examples.real_env_kit import get_test_real_id, reals_dir_setup_cleanup
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_initialize_change_duty_files_CorrectlySavesDutyFileAndChangeFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(None, None, sue_text, None, planck=seven_int)
    assert sue_filehub.duty_file_exists() == False
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    delete_dir(sue_filehub.changes_dir())
    assert os_path_exists(init_change_file_path) == False

    # WHEN
    initialize_change_duty_files(sue_filehub)

    # THEN
    duty_agenda = sue_filehub.get_duty_agenda()
    assert duty_agenda._real_id == get_test_real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_change_file_path)


def test_initialize_change_duty_files_CorrectlySavesOnlyDutyFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(None, None, sue_text, None, planck=seven_int)
    initialize_change_duty_files(sue_filehub)
    assert sue_filehub.duty_file_exists()
    sue_filehub.delete_duty_file()
    assert sue_filehub.duty_file_exists() == False
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    assert os_path_exists(init_change_file_path)

    # WHEN
    initialize_change_duty_files(sue_filehub)

    # THEN
    duty_agenda = sue_filehub.get_duty_agenda()
    assert duty_agenda._real_id == get_test_real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_change_file_path)


def test_initialize_change_duty_files_CorrectlySavesOnlychangeFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_filehub = filehub_shop(None, None, sue_text, None, planck=seven_int)
    initialize_change_duty_files(sue_filehub)
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    sue_filehub.save_duty_agenda(sue_duty_agenda)
    assert sue_filehub.duty_file_exists()
    init_change_file_path = f"{sue_filehub.changes_dir()}/{init_change_id()}.json"
    delete_dir(sue_filehub.changes_dir())
    assert os_path_exists(init_change_file_path) == False

    # WHEN
    initialize_change_duty_files(sue_filehub)

    # THEN
    assert sue_duty_agenda._real_id == get_test_real_id()
    assert sue_duty_agenda._owner_id == sue_text
    assert sue_duty_agenda._planck == seven_int
    assert sue_duty_agenda.party_exists(bob_text)
    assert os_path_exists(init_change_file_path)
