from src._road.jaar_config import work_str
from src._road.userdir import userdir_shop
from src.agenda.agenda import agendaunit_shop, get_from_json as agendaunit_get_from_json
from src.real.admin_work import (
    work_file_exists,
    save_work_file,
    initialize_work_file,
    get_work_file_agenda,
)
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
    sue_work_file_name = f"{work_str()}.json"
    sue_work_path = f"{sue_person_dir}/{sue_work_file_name}"
    print(f"{sue_work_path=}")
    assert os_path_exists(sue_work_path) == False
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_userdir, sue_agenda)
    assert work_file_exists(sue_userdir)
    delete_dir(sue_userdir._work_path)
    assert os_path_exists(sue_work_path) == False
    assert work_file_exists(sue_userdir) == False

    # WHEN
    save_file(
        dest_dir=sue_userdir.person_dir,
        file_name=sue_userdir._work_file_name,
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_work_path)
    assert work_file_exists(sue_userdir)


def test_save_work_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_userdir, sue_agenda)
    assert work_file_exists(sue_userdir)
    delete_dir(sue_userdir._work_path)
    assert work_file_exists(sue_userdir) == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    save_work_file(sue_userdir, sue_agenda)

    # THEN
    assert work_file_exists(sue_userdir)

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_file_name = f"{work_str()}.json"
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.get_party(bob_text) != None

    # # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    save_work_file(sue_userdir, sue2_agenda)

    # THEN
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.get_party(zia_text) != None


def testsave_work_file_RaisesErrorWhenAgenda_work_id_IsWrong(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        save_work_file(sue_userdir, agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )


def test_initialize_work_file_CorrectlySavesFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_userdir, sue_agenda)
    assert work_file_exists(sue_userdir)
    delete_dir(sue_userdir._work_path)
    assert work_file_exists(sue_userdir) == False

    # WHEN
    initialize_work_file(sue_userdir, sue_agenda)

    # THEN
    work_agenda = get_work_file_agenda(sue_userdir)
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert work_agenda.get_party(bob_text) is None

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    save_work_file(sue_userdir, sue_agenda)
    work_agenda = get_work_file_agenda(sue_userdir)
    assert work_agenda.get_party(bob_text)

    # WHEN
    initialize_work_file(sue_userdir, sue_agenda)

    # THEN
    work_agenda = get_work_file_agenda(sue_userdir)
    assert work_agenda.get_party(bob_text)


def test_initialize_work_file_CorrectlyDoesNotOverwrite(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_planck = 7
    sue_userdir = userdir_shop(None, None, sue_text, None, planck=sue_planck)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id(), _planck=sue_planck)
    initialize_work_file(sue_userdir, sue_agenda)
    assert work_file_exists(sue_userdir)
    delete_dir(sue_userdir._work_path)
    assert work_file_exists(sue_userdir) == False

    # WHEN
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    initialize_work_file(sue_userdir, sue_agenda)

    # THEN
    assert work_file_exists(sue_userdir)

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_file_name = f"{work_str()}.json"
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    assert work_agenda._planck == sue_planck


def test_initialize_work_file_CreatesDirsAndFiles(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    delete_dir(sue_userdir.real_dir)
    assert os_path_exists(sue_userdir._work_path) is False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_userdir, sue_agenda)

    # THEN
    assert os_path_exists(sue_userdir._work_path)
