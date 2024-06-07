from src._road.jaar_config import work_str
from src.agenda.agenda import agendaunit_shop, get_from_json as agendaunit_get_from_json
from src.change.agendahub import agendahub_shop
from src.change.listen import listen_to_person_jobs
from src.real.admin_work import initialize_work_file
from src.real.real import realunit_shop
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)

from pytest import raises as pytest_raises
from os.path import exists as os_path_exists
from src._instrument.file import open_file, save_file, delete_dir


def test_work_file_exists_ReturnsCorrectBool(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_dir = f"{sue_person_dir}/work"
    sue_work_file_name = f"{sue_text}.json"
    sue_work_path = f"{sue_work_dir}/{sue_work_file_name}"
    print(f"{sue_work_path=}")
    assert os_path_exists(sue_work_path) == False
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_agendahub, sue_agenda)
    assert sue_agendahub.work_file_exists()
    delete_dir(sue_agendahub.work_path())
    assert os_path_exists(sue_work_path) == False
    assert sue_agendahub.work_file_exists() == False

    # WHEN
    save_file(
        dest_dir=sue_agendahub.work_dir(),
        file_name=sue_agendahub.work_file_name(),
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_work_path)
    assert sue_agendahub.work_file_exists()


def test_save_work_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_agendahub, sue_agenda)
    assert sue_agendahub.work_file_exists()
    delete_dir(sue_agendahub.work_path())
    assert sue_agendahub.work_file_exists() == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_agendahub.save_work_agenda(sue_agenda)

    # THEN
    assert sue_agendahub.work_file_exists()

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_dir = f"{sue_person_dir}/work"
    sue_work_file_name = f"{sue_text}.json"
    work_file_text = open_file(dest_dir=sue_work_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.party_exists(bob_text)

    # # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    sue_agendahub.save_work_agenda(sue2_agenda)

    # THEN
    work_file_text = open_file(dest_dir=sue_work_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.party_exists(zia_text)


def test_save_work_file_RaisesErrorWhenAgenda_work_id_IsWrong(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_agendahub.save_work_agenda(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )


def test_initialize_work_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_agendahub, sue_agenda)
    assert sue_agendahub.work_file_exists()
    delete_dir(sue_agendahub.work_path())
    assert sue_agendahub.work_file_exists() == False

    # WHEN
    initialize_work_file(sue_agendahub, sue_agenda)

    # THEN
    work_agenda = sue_agendahub.get_work_agenda()
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert work_agenda.party_exists(bob_text) == False

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    sue_agendahub.save_work_agenda(sue_agenda)
    work_agenda = sue_agendahub.get_work_agenda()
    assert work_agenda.get_party(bob_text)

    # WHEN
    initialize_work_file(sue_agendahub, sue_agenda)

    # THEN
    work_agenda = sue_agendahub.get_work_agenda()
    assert work_agenda.get_party(bob_text)


def test_initialize_work_file_CorrectlyDoesNotOverwrite(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_planck = 7
    sue_agendahub = agendahub_shop(None, None, sue_text, None, planck=sue_planck)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id(), _planck=sue_planck)
    initialize_work_file(sue_agendahub, sue_agenda)
    assert sue_agendahub.work_file_exists()
    delete_dir(sue_agendahub.work_path())
    assert sue_agendahub.work_file_exists() == False

    # WHEN
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    initialize_work_file(sue_agendahub, sue_agenda)

    # THEN
    assert sue_agendahub.work_file_exists()

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_dir = f"{sue_person_dir}/work"
    sue_work_file_name = f"{sue_text}.json"
    work_file_text = open_file(dest_dir=sue_work_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    assert work_agenda._planck == sue_planck


def test_initialize_work_file_CreatesDirsAndFiles(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    delete_dir(sue_agendahub.real_dir())
    assert os_path_exists(sue_agendahub.work_path()) is False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_agendahub, sue_agenda)

    # THEN
    assert os_path_exists(sue_agendahub.work_path())
