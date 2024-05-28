from src._road.road import get_default_real_id_roadnode as root_label
from src.agenda.agenda import agendaunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesReason_1Belief as example_agendas_get_agenda_1Task_1CE0MinutesReason_1Belief,
)
from src.econ.econ import econunit_shop, get_owner_file_name
from src.econ.examples.example_econ_agendas import (
    get_1node_agenda as example_get_1node_agenda,
    get_1node_agenda as example_get_7nodeJRootWithH_agenda,
    get_agenda_2CleanNodesRandomWeights,
)
from src.econ.examples.econ_env_kit import (
    get_temp_env_real_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os import path as os_path


def test_EconUnit_save_job_file_CreatesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    a_agenda = example_get_1node_agenda()
    a_path = f"{x_econ.get_jobs_dir()}/{a_agenda._owner_id}.json"
    assert os_path.exists(a_path) == False

    # WHEN
    x_econ.save_job_file(a_agenda)

    # THEN
    print(f"{a_path=}")
    assert os_path.exists(a_path)


def test_EconUnit_get_job_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    y_agenda = example_get_7nodeJRootWithH_agenda()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_econ.get_job_file(y_agenda._owner_id)
    assert (
        str(excinfo.value)
        == "Could not load file src/econ/examples/econs/ex_econ04/jobs/A.json (2, 'No such file or directory')"
    )

    # WHEN
    x_econ.save_job_file(y_agenda)

    # THEN
    assert x_econ.get_job_file(y_agenda._owner_id) == y_agenda


def test_EconUnit_delete_job_file_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    a_agenda = example_get_1node_agenda()
    a_path = f"{x_econ.get_jobs_dir()}/{get_owner_file_name(a_agenda._owner_id)}"
    x_econ.save_job_file(a_agenda)
    print(f"{a_path=}")
    assert os_path.exists(a_path)

    # WHEN
    x_econ.delete_job_file(a_agenda._owner_id)

    # THEN
    assert os_path.exists(a_path) == False


def test_EconUnit_modify_job_owner_id_ModifysFileName(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    yao_owner_id = "yao"
    y_agenda = agendaunit_shop(_owner_id=yao_owner_id)
    yao_agenda_path = f"{x_econ.get_jobs_dir()}/{yao_owner_id}.json"
    x_econ.save_job_file(y_agenda)
    print(f"{yao_agenda_path=}")

    # WHEN
    zia_owner_id = "new1"
    zia_agenda_path = f"{x_econ.get_jobs_dir()}/{zia_owner_id}.json"
    assert os_path.exists(zia_agenda_path) == False
    assert os_path.exists(yao_agenda_path)
    x_econ.modify_job_owner_id(old_owner_id=yao_owner_id, new_owner_id=zia_owner_id)

    # THEN
    assert os_path.exists(yao_agenda_path) == False
    assert os_path.exists(zia_agenda_path)


def test_EconUnit_save_job_file_ModifysFile_idearoot(env_dir_setup_cleanup):
    # GIVEN
    x_real_id = get_temp_env_real_id()
    x_econ = econunit_shop(x_real_id, econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    old_x_agenda = example_agendas_get_agenda_1Task_1CE0MinutesReason_1Belief()
    assert old_x_agenda._idearoot._label == root_label()
    assert old_x_agenda._idearoot._label != x_real_id

    # WHEN
    x_econ.save_job_file(old_x_agenda)

    # THEN
    new_x_agenda = x_econ.get_job_file(old_x_agenda._owner_id)
    assert new_x_agenda._idearoot._label != root_label()
    assert new_x_agenda._idearoot._label == x_real_id


def test_EconUnit_create_job_file_from_role_file_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_real_id = get_temp_env_real_id()
    x_econ = econunit_shop(x_real_id, econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    bob_text = "Bob"
    bob_role = get_agenda_2CleanNodesRandomWeights(bob_text)
    x_econ.save_role_file(bob_role)

    # WHEN
    bob_job = x_econ.create_job_file_from_role_file(bob_text)

    # THEN
    assert bob_job != None
    assert x_econ.get_job_file(bob_text) != None
