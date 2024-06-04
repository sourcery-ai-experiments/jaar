from src._road.jaar_config import duty_str, init_change_id
from src.agenda.agenda import agendaunit_shop, get_from_json as agendaunit_get_from_json
from src.change.agendahub import agendahub_shop
from src.real.admin_duty import (
    get_duty_file_agenda,
    initialize_change_duty_files,
    get_default_duty_agenda,
)
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists
from src._instrument.file import open_file, delete_dir


def test_get_duty_file_agenda_IfFileMissingCreatesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    delete_dir(sue_agendahub.real_dir())
    assert os_path_exists(sue_agendahub.duty_path()) is False

    # WHEN
    sue_duty = get_duty_file_agenda(sue_agendahub)

    # THEN
    assert os_path_exists(sue_agendahub.duty_path())
    default_duty = get_default_duty_agenda(sue_agendahub)
    default_duty.calc_agenda_metrics()
    assert sue_duty == default_duty


def test_save_duty_agenda_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_duty_file_name = f"{duty_str()}.json"
    sue_duty_path = f"{sue_person_dir}/{sue_duty_file_name}"

    # WHEN
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    initialize_change_duty_files(sue_agendahub)

    # THEN
    assert sue_agendahub.duty_file_exists()

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    delete_dir(sue_duty_path)
    assert sue_agendahub.duty_file_exists() == False

    # WHEN
    sue_agendahub.save_duty_agenda(sue_agenda)

    # THEN
    assert sue_agendahub.duty_file_exists()

    # GIVEN
    duty_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_duty_file_name)
    print(f"{duty_file_text=}")
    duty_agenda = agendaunit_get_from_json(duty_file_text)
    assert duty_agenda.party_exists(bob_text)

    # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    sue_agendahub.save_duty_agenda(sue2_agenda)

    # THEN
    duty_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_duty_file_name)
    print(f"{duty_file_text=}")
    duty_agenda = agendaunit_get_from_json(duty_file_text)
    assert duty_agenda.party_exists(zia_text)


def test_save_duty_agenda_RaisesErrorWhenAgenda_work_id_IsWrong(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_agendahub.save_duty_agenda(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s duty agenda."
    )


def test_initialize_change_duty_files_CorrectlySavesDutyFileAndchangeFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_agendahub = agendahub_shop(None, None, sue_text, None, planck=seven_int)
    initialize_change_duty_files(sue_agendahub)
    assert sue_agendahub.duty_file_exists()
    delete_dir(sue_agendahub.duty_path())
    assert sue_agendahub.duty_file_exists() == False
    init_change_file_path = f"{sue_agendahub.changes_dir()}/{init_change_id()}.json"
    delete_dir(sue_agendahub.changes_dir())
    assert os_path_exists(init_change_file_path) == False

    # WHEN
    initialize_change_duty_files(sue_agendahub)

    # THEN
    duty_agenda = get_duty_file_agenda(sue_agendahub)
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
    sue_agendahub = agendahub_shop(None, None, sue_text, None, planck=seven_int)
    initialize_change_duty_files(sue_agendahub)
    assert sue_agendahub.duty_file_exists()
    delete_dir(sue_agendahub.duty_path())
    assert sue_agendahub.duty_file_exists() == False
    init_change_file_path = f"{sue_agendahub.changes_dir()}/{init_change_id()}.json"
    assert os_path_exists(init_change_file_path)

    # WHEN
    initialize_change_duty_files(sue_agendahub)

    # THEN
    duty_agenda = get_duty_file_agenda(sue_agendahub)
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
    sue_agendahub = agendahub_shop(None, None, sue_text, None, planck=seven_int)
    initialize_change_duty_files(sue_agendahub)
    sue_duty_agenda = get_duty_file_agenda(sue_agendahub)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    sue_agendahub.save_duty_agenda(sue_duty_agenda)
    assert sue_agendahub.duty_file_exists()
    init_change_file_path = f"{sue_agendahub.changes_dir()}/{init_change_id()}.json"
    delete_dir(sue_agendahub.changes_dir())
    assert os_path_exists(init_change_file_path) == False

    # WHEN
    initialize_change_duty_files(sue_agendahub)

    # THEN
    assert sue_duty_agenda._real_id == get_test_real_id()
    assert sue_duty_agenda._owner_id == sue_text
    assert sue_duty_agenda._planck == seven_int
    assert sue_duty_agenda.party_exists(bob_text)
    assert os_path_exists(init_change_file_path)
