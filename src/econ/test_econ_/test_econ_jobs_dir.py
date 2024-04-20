from src.agenda.agenda import agendaunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesReason_1Belief as example_agendas_get_agenda_1Task_1CE0MinutesReason_1Belief,
)
from src.econ.econ import econunit_shop
from src.econ.examples.example_clerks import (
    get_1node_agenda as example_get_1node_agenda,
    get_1node_agenda as example_get_7nodeJRootWithH_agenda,
)
from src.econ.examples.econ_env_kit import (
    get_temp_env_econ_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_EconUnit_save_file_to_guts_CreatesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    a_agenda = example_get_1node_agenda()
    a_path = f"{x_econ.get_guts_dir()}/{a_agenda._owner_id}.json"
    assert os_path.exists(a_path) == False

    # WHEN
    x_econ.save_file_to_guts(a_agenda)

    # THEN
    print(f"{a_path=}")
    assert os_path.exists(a_path)


def test_EconUnit_get_file_in_guts_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    y_agenda = example_get_7nodeJRootWithH_agenda()
    x_econ.save_file_to_guts(y_agenda)

    # WHEN / THEN
    assert x_econ.get_file_in_guts(owner_id=y_agenda._owner_id) == y_agenda


def test_EconUnit_delete_file_in_guts_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    a_agenda = example_get_1node_agenda()
    a_path = f"{x_econ.get_guts_dir()}/{a_agenda._owner_id}.json"
    x_econ.save_file_to_guts(a_agenda)
    print(f"{a_path=}")
    assert os_path.exists(a_path)

    # WHEN
    x_econ.delete_file_in_guts(a_agenda._owner_id)

    # THEN
    assert os_path.exists(a_path) == False


def test_EconUnit_save_file_to_jobs_CreatesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    a_agenda = example_get_1node_agenda()
    a_path = f"{x_econ.get_jobs_dir()}/{a_agenda._owner_id}.json"
    assert os_path.exists(a_path) == False

    # WHEN
    x_econ.save_file_to_jobs(a_agenda)

    # THEN
    print(f"{a_path=}")
    assert os_path.exists(a_path)


def test_EconUnit_get_file_in_jobs_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    y_agenda = example_get_7nodeJRootWithH_agenda()
    x_econ.save_file_to_jobs(y_agenda)

    # WHEN / THEN
    assert x_econ.get_file_in_jobs(owner_id=y_agenda._owner_id) == y_agenda


def test_EconUnit_delete_file_in_jobs_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    a_agenda = example_get_1node_agenda()
    a_path = f"{x_econ.get_jobs_dir()}/{a_agenda._owner_id}.json"
    x_econ.save_file_to_jobs(a_agenda)
    print(f"{a_path=}")
    assert os_path.exists(a_path)

    # WHEN
    x_econ.delete_file_in_jobs(a_agenda._owner_id)

    # THEN
    assert os_path.exists(a_path) == False


def test_EconUnit_change_job_owner_id_ChangesFileName(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(x_econ_id, get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    old_owner_id = "old1"
    y_agenda = agendaunit_shop(_owner_id=old_owner_id)
    old_y_agenda_path = f"{x_econ.get_jobs_dir()}/{old_owner_id}.json"
    x_econ.save_file_to_jobs(y_agenda)
    print(f"{old_y_agenda_path=}")

    # WHEN
    new_owner_id = "new1"
    new_y_agenda_path = f"{x_econ.get_jobs_dir()}/{new_owner_id}.json"
    assert os_path.exists(new_y_agenda_path) == False
    assert os_path.exists(old_y_agenda_path)
    x_econ.change_job_owner_id(old_owner_id=old_owner_id, new_owner_id=new_owner_id)

    # THEN
    assert os_path.exists(old_y_agenda_path) == False
    assert os_path.exists(new_y_agenda_path)


def test_EconUnit_save_file_to_jobs_ChangesFile_idearoot(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(x_econ_id, econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    old_x_agenda = example_agendas_get_agenda_1Task_1CE0MinutesReason_1Belief()
    assert old_x_agenda._idearoot._label == "A"
    assert old_x_agenda._idearoot._label != x_econ_id

    # WHEN
    x_econ.save_file_to_jobs(old_x_agenda)

    # THEN
    new_x_agenda = x_econ.get_file_in_jobs(old_x_agenda._owner_id)
    assert new_x_agenda._idearoot._label != "A"
    assert new_x_agenda._idearoot._label == x_econ_id
