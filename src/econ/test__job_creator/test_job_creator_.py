from src._road.road import create_road, get_default_real_id_roadnode as root_label
from src._road.worlddir import econdir_shop, get_econ_jobs_dir
from src.agenda.party import partylink_shop
from src.agenda.group import groupunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.change import get_init_change_id_if_None
from src.econ.job_creator import (
    save_role_file,
    save_job_file,
    get_file_name,
    get_job_file,
    create_listen_basis,
    get_role_file,
    listen_to_debtors_roll,
    create_job_file_from_role_file,
)
from src.econ.examples.econ_env_kit import env_dir_setup_cleanup, get_test_econ_dir
from os.path import exists as os_path_exists


def test_get_role_file_ReturnsCorrectAgendaWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    src_yao_agenda = agendaunit_shop(yao_text)
    save_role_file(get_test_econ_dir(), src_yao_agenda)

    # WHEN
    yao_role = get_role_file(get_test_econ_dir(), yao_text)

    # THEN
    assert src_yao_agenda.get_dict() == yao_role.get_dict()


def test_get_job_file_ReturnsCorrectAgendaWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"

    # WHEN / THEN
    assert get_job_file(get_test_econ_dir(), yao_text) is None

    # GIVEN
    save_job_file(get_test_econ_dir(), agendaunit_shop(yao_text))
    # WHEN
    yao_job = get_job_file(get_test_econ_dir(), yao_text)
    # THEN
    assert yao_job.get_dict() == yao_job.get_dict()


def test_create_job_file_from_role_file_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    yao_role.calc_agenda_metrics()
    save_role_file(get_test_econ_dir(), yao_role)
    yao_job_file_path = f"{get_test_econ_dir()}/jobs/{get_file_name(yao_text)}"
    assert os_path_exists(yao_job_file_path) == False

    # WHEN
    yao_job = create_job_file_from_role_file(get_test_econ_dir(), yao_text)

    # GIVEN
    assert yao_job._owner_id != None
    assert yao_job._owner_id == yao_text
    assert yao_job.get_dict() == yao_role.get_dict()
    assert os_path_exists(yao_job_file_path)
