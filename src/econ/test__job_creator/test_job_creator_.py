from src.agenda.agenda import agendaunit_shop
from src.econ.job_creator import (
    save_role_file,
    save_job_file,
    get_file_name,
    get_job_file,
    get_role_file,
    create_job_file_from_role_file,
)
from src.econ.examples.econ_env_kit import env_dir_setup_cleanup, temp_reals_dir
from os.path import exists as os_path_exists


def test_get_role_file_ReturnsCorrectAgendaWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    src_yao_agenda = agendaunit_shop(yao_text)
    save_role_file(temp_reals_dir(), src_yao_agenda)

    # WHEN
    yao_role = get_role_file(temp_reals_dir(), yao_text)

    # THEN
    assert src_yao_agenda.get_dict() == yao_role.get_dict()


def test_get_job_file_ReturnsCorrectAgendaWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"

    # WHEN / THEN
    assert get_job_file(temp_reals_dir(), yao_text) is None

    # GIVEN
    save_job_file(temp_reals_dir(), agendaunit_shop(yao_text))
    # WHEN
    yao_job = get_job_file(temp_reals_dir(), yao_text)
    # THEN
    assert yao_job.get_dict() == yao_job.get_dict()


def test_create_job_file_from_role_file_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    yao_role.calc_agenda_metrics()
    save_role_file(temp_reals_dir(), yao_role)
    yao_job_file_path = f"{temp_reals_dir()}/jobs/{get_file_name(yao_text)}"
    assert os_path_exists(yao_job_file_path) == False

    # WHEN
    yao_job = create_job_file_from_role_file(temp_reals_dir(), yao_text)

    # GIVEN
    assert yao_job._owner_id != None
    assert yao_job._owner_id == yao_text
    assert yao_job.get_dict() == yao_role.get_dict()
    assert os_path_exists(yao_job_file_path)
