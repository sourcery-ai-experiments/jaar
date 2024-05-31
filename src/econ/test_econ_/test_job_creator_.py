from src.agenda.agenda import agendaunit_shop
from src.econ.econ import (
    save_role_file_agenda,
    save_job_file,
    get_job_file,
    get_role_file_agenda,
    create_job_file_from_role_file,
)
from src.econ.examples.econ_env_kit import env_dir_setup_cleanup, get_texas_econnox
from os.path import exists as os_path_exists


def test_get_role_file_agenda_ReturnsCorrectAgendaWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    src_yao_agenda = agendaunit_shop(yao_text)
    texas_econnox = get_texas_econnox()
    save_role_file_agenda(texas_econnox, src_yao_agenda)

    # WHEN
    yao_role = get_role_file_agenda(texas_econnox, yao_text)

    # THEN
    assert src_yao_agenda.get_dict() == yao_role.get_dict()


def test_get_job_file_ReturnsCorrectAgendaWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    texas_econnox = get_texas_econnox()

    # WHEN / THEN
    assert get_job_file(texas_econnox, yao_text) is None

    # GIVEN
    save_job_file(texas_econnox, agendaunit_shop(yao_text))
    # WHEN
    yao_job = get_job_file(texas_econnox, yao_text)
    # THEN
    assert yao_job.get_dict() == yao_job.get_dict()


def test_create_job_file_from_role_file_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    yao_role.calc_agenda_metrics()
    texas_econnox = get_texas_econnox()
    save_role_file_agenda(texas_econnox, yao_role)
    yao_job_file_path = texas_econnox.job_path(yao_text)
    assert os_path_exists(yao_job_file_path) == False

    # WHEN
    yao_job = create_job_file_from_role_file(texas_econnox, yao_text)

    # GIVEN
    assert yao_job._owner_id != None
    assert yao_job._owner_id == yao_text
    assert yao_job.get_dict() == yao_role.get_dict()
    assert os_path_exists(yao_job_file_path)
