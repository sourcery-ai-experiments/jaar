from src.agenda.agenda import agendaunit_shop
from src.econ.econ import create_job_file_from_role_file
from src.econ.examples.econ_env_kit import env_dir_setup_cleanup, get_texas_agendanox
from os.path import exists as os_path_exists


def test_get_role_agenda_ReturnsCorrectAgendaWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    texas_agendanox = get_texas_agendanox()
    sue_text = "Sue"
    src_sue_agenda = agendaunit_shop(sue_text)
    texas_agendanox.save_file_role(src_sue_agenda)

    # WHEN
    sue_role = texas_agendanox.get_role_agenda(sue_text)

    # THEN
    print(f"{sue_role}")
    assert src_sue_agenda.get_dict() == sue_role.get_dict()


def test_get_job_agenda_ReturnsCorrectAgendaWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    texas_agendanox = get_texas_agendanox()
    sue_text = "Sue"

    # WHEN / THEN
    assert texas_agendanox.get_role_agenda(sue_text) is None

    # GIVEN
    texas_agendanox.save_file_role(agendaunit_shop(sue_text))
    # WHEN
    sue_job = texas_agendanox.get_role_agenda(sue_text)
    # THEN
    print(f"{sue_job=}")
    assert sue_job.get_dict() == sue_job.get_dict()


def test_create_job_file_from_role_file_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_role = agendaunit_shop(sue_text)
    sue_role.calc_agenda_metrics()
    texas_agendanox = get_texas_agendanox()
    texas_agendanox.save_file_role(sue_role)
    sue_job_file_path = texas_agendanox.job_path(sue_text)
    assert os_path_exists(sue_job_file_path) == False

    # WHEN
    sue_job = create_job_file_from_role_file(texas_agendanox, sue_text)

    # GIVEN
    assert sue_job._owner_id != None
    assert sue_job._owner_id == sue_text
    assert sue_job.get_dict() == sue_role.get_dict()
    assert os_path_exists(sue_job_file_path)
