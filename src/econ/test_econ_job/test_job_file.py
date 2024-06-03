from src._road.worldnox import get_file_name
from src.econ.econ import econunit_shop, create_job_file_from_role_file
from src.econ.examples.example_econ_agendas import (
    get_1node_agenda as example_get_1node_agenda,
    get_1node_agenda as example_get_7nodeJRootWithH_agenda,
    get_agenda_2CleanNodesRandomWeights,
)
from src.econ.examples.econ_env_kit import env_dir_setup_cleanup, get_texas_agendanox
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_EconUnit_save_job_file_CreatesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_texas_agendanox())
    a_agenda = example_get_1node_agenda()
    a_path = f"{x_econ.agendanox.jobs_dir()}/{a_agenda._owner_id}.json"
    assert os_path_exists(a_path) == False

    # WHEN
    x_econ.agendanox.save_file_job(a_agenda)

    # THEN
    print(f"{a_path=}")
    assert os_path_exists(a_path)


def test_EconUnit_get_job_agenda_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_texas_agendanox())
    y_agenda = example_get_7nodeJRootWithH_agenda()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_econ.agendanox.get_job_agenda(y_agenda._owner_id)
    assert (
        str(excinfo.value)
        == "Could not load file src/econ/examples/reals/ex_econ04/persons/ex_person04/econs/nation-state/usa/texas/jobs/A.json (2, 'No such file or directory')"
    )

    # WHEN
    x_econ.agendanox.save_file_job(y_agenda)

    # THEN
    assert x_econ.agendanox.get_job_agenda(y_agenda._owner_id) == y_agenda


def test_EconUnit_delete_job_file_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_texas_agendanox())
    a_agenda = example_get_1node_agenda()
    a_path = f"{x_econ.agendanox.jobs_dir()}/{get_file_name(a_agenda._owner_id)}"
    x_econ.agendanox.save_file_job(a_agenda)
    print(f"{a_path=}")
    assert os_path_exists(a_path)

    # WHEN
    x_econ.agendanox.delete_job_file(a_agenda._owner_id)

    # THEN
    assert os_path_exists(a_path) == False


def test_create_job_file_from_role_file_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_texas_agendanox())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    bob_text = "Bob"
    bob_role = get_agenda_2CleanNodesRandomWeights(bob_text)
    x_econ.agendanox.save_file_role(bob_role)

    # WHEN
    bob_job = create_job_file_from_role_file(x_econ.agendanox, bob_text)

    # THEN
    assert bob_job != None
    assert x_econ.agendanox.get_job_agenda(bob_text) != None
