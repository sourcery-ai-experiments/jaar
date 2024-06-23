from src._instrument.file import open_file, save_file, delete_dir
from src._road.road import get_default_real_id_roadnode as root_label
from src.agenda.agenda import agendaunit_shop, get_from_json as agendaunit_get_from_json
from src.listen.userhub import userhub_shop
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_UserHub_work_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    assert os_path_exists(sue_userhub.work_path()) is False
    assert sue_userhub.work_file_exists() is False

    # WHEN
    save_file(
        dest_dir=sue_userhub.work_dir(),
        file_name=sue_userhub.work_file_name(),
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_userhub.work_path())
    assert sue_userhub.work_file_exists()


def test_UserHub_save_work_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    assert sue_userhub.work_file_exists() is False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_otherunit(bob_text)
    sue_userhub.save_work_agenda(sue_agenda)

    # THEN
    assert sue_userhub.work_file_exists()

    work_file_text = open_file(sue_userhub.work_dir(), sue_userhub.work_file_name())
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.other_exists(bob_text)

    # # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_otherunit(zia_text)
    sue_userhub.save_work_agenda(sue2_agenda)

    # THEN
    work_file_text = open_file(sue_userhub.work_dir(), sue_userhub.work_file_name())
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.other_exists(zia_text)


def test_UserHub_save_work_file_RaisesErrorWhenAgenda_work_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_work_agenda(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )


def test_UserHub_initialize_work_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    sue_agenda = agendaunit_shop(sue_text, root_label())
    assert sue_userhub.work_file_exists() is False

    # WHEN
    sue_userhub.initialize_work_file(sue_agenda)

    # THEN
    work_agenda = sue_userhub.get_work_agenda()
    assert work_agenda._real_id == root_label()
    assert work_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert work_agenda.other_exists(bob_text) is False

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_otherunit(bob_text)
    sue_userhub.save_work_agenda(sue_agenda)
    work_agenda = sue_userhub.get_work_agenda()
    assert work_agenda.get_other(bob_text)

    # WHEN
    sue_userhub.initialize_work_file(sue_agenda)

    # THEN
    work_agenda = sue_userhub.get_work_agenda()
    assert work_agenda.get_other(bob_text)


def test_UserHub_initialize_work_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_pixel = 7
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None, pixel=sue_pixel)
    sue_agenda = agendaunit_shop(sue_text, root_label(), _pixel=sue_pixel)
    sue_userhub.initialize_work_file(sue_agenda)
    assert sue_userhub.work_file_exists()
    delete_dir(sue_userhub.work_path())
    assert sue_userhub.work_file_exists() is False

    # WHEN
    bob_text = "Bob"
    sue_agenda.add_otherunit(bob_text)
    sue_userhub.initialize_work_file(sue_agenda)

    # THEN
    assert sue_userhub.work_file_exists()

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
    assert work_agenda._pixel == sue_pixel


def test_UserHub_initialize_work_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    delete_dir(sue_userhub.real_dir())
    assert os_path_exists(sue_userhub.work_path()) is False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text, root_label())
    sue_userhub.initialize_work_file(sue_agenda)

    # THEN
    assert os_path_exists(sue_userhub.work_path())
