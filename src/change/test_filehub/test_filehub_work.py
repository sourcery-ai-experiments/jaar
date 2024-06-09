from src._instrument.file import open_file, save_file, delete_dir
from src._road.road import get_default_real_id_roadnode as root_label
from src.agenda.agenda import agendaunit_shop, get_from_json as agendaunit_get_from_json
from src.change.filehub import filehub_shop
from src.change.examples.change_env import (
    env_dir_setup_cleanup,
    get_change_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_FileHub_work_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text, None)
    assert os_path_exists(sue_filehub.work_path()) is False
    assert sue_filehub.work_file_exists() is False

    # WHEN
    save_file(
        dest_dir=sue_filehub.work_dir(),
        file_name=sue_filehub.work_file_name(),
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_filehub.work_path())
    assert sue_filehub.work_file_exists()


def test_FileHub_save_work_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text, None)
    assert sue_filehub.work_file_exists() is False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_filehub.save_work_agenda(sue_agenda)

    # THEN
    assert sue_filehub.work_file_exists()

    work_file_text = open_file(sue_filehub.work_dir(), sue_filehub.work_file_name())
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.party_exists(bob_text)

    # # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    sue_filehub.save_work_agenda(sue2_agenda)

    # THEN
    work_file_text = open_file(sue_filehub.work_dir(), sue_filehub.work_file_name())
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.party_exists(zia_text)


def test_FileHub_save_work_file_RaisesErrorWhenAgenda_work_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_filehub.save_work_agenda(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )


def test_FileHub_initialize_work_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text, None)
    sue_agenda = agendaunit_shop(sue_text, root_label())
    assert sue_filehub.work_file_exists() is False

    # WHEN
    sue_filehub.initialize_work_file(sue_agenda)

    # THEN
    work_agenda = sue_filehub.get_work_agenda()
    assert work_agenda._real_id == root_label()
    assert work_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert work_agenda.party_exists(bob_text) is False

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    sue_filehub.save_work_agenda(sue_agenda)
    work_agenda = sue_filehub.get_work_agenda()
    assert work_agenda.get_party(bob_text)

    # WHEN
    sue_filehub.initialize_work_file(sue_agenda)

    # THEN
    work_agenda = sue_filehub.get_work_agenda()
    assert work_agenda.get_party(bob_text)


def test_FileHub_initialize_work_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_planck = 7
    sue_filehub = filehub_shop(
        env_dir(), root_label(), sue_text, None, planck=sue_planck
    )
    sue_agenda = agendaunit_shop(sue_text, root_label(), _planck=sue_planck)
    sue_filehub.initialize_work_file(sue_agenda)
    assert sue_filehub.work_file_exists()
    delete_dir(sue_filehub.work_path())
    assert sue_filehub.work_file_exists() is False

    # WHEN
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_filehub.initialize_work_file(sue_agenda)

    # THEN
    assert sue_filehub.work_file_exists()

    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_dir = f"{sue_person_dir}/work"
    sue_work_file_name = f"{sue_text}.json"
    work_file_text = open_file(dest_dir=sue_work_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda._real_id == root_label()
    assert work_agenda._owner_id == sue_text
    assert work_agenda._planck == sue_planck


def test_FileHub_initialize_work_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text, None)
    delete_dir(sue_filehub.real_dir())
    assert os_path_exists(sue_filehub.work_path()) is False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text, root_label())
    sue_filehub.initialize_work_file(sue_agenda)

    # THEN
    assert os_path_exists(sue_filehub.work_path())
