from src.econ.econ import econunit_shop
from src.econ.examples.example_econ_agendas import (
    get_1node_agenda as example_get_1node_agenda,
    get_1node_agenda as example_get_7nodeJRootWithH_agenda,
    get_agenda_2CleanNodesRandomWeights,
)
from src.econ.examples.econ_env_kit import env_dir_setup_cleanup, get_texas_agendahub
from os.path import exists as os_path_exists


def test_EconUnit_agendahub_save_role_agenda_CreatesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    texas_agendahub = get_texas_agendahub()
    x_econ = econunit_shop(texas_agendahub)
    bob_text = "Bob"
    bob_role = get_agenda_2CleanNodesRandomWeights(bob_text)
    bob_path = f"{x_econ.agendahub.roles_dir()}/{bob_role._owner_id}.json"
    assert os_path_exists(bob_path) == False

    # WHEN
    x_econ.agendahub.save_role_agenda(bob_role)

    # THEN
    print(f"{bob_path=}")
    assert os_path_exists(bob_path)


def test_EconUnit_get_role_agenda_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    texas_agendahub = get_texas_agendahub()
    x_econ = econunit_shop(texas_agendahub)
    y_agenda = example_get_7nodeJRootWithH_agenda()
    x_econ.agendahub.save_role_agenda(y_agenda)

    # WHEN / THEN
    assert x_econ.agendahub.get_role_agenda(y_agenda._owner_id) == y_agenda
