from src._road.road import default_road_delimiter_if_none
from src.agenda.agenda import agendaunit_shop
from src.econ.econ import econunit_shop, EconUnit, create_job_file_from_role_file
from src.econ.examples.econ_env_kit import (
    env_dir_setup_cleanup,
    temp_reals_dir,
    temp_reals_dir,
    temp_real_id,
    get_texas_filehub,
)
from src.econ.examples.example_econ_agendas import (
    get_agenda_2CleanNodesRandomWeights,
)
from os.path import exists as os_path_exists


def test_EconUnit_exists():
    # GIVEN
    texas_filehub = get_texas_filehub()

    # WHEN
    x_econ = EconUnit(filehub=texas_filehub)

    # THEN
    assert x_econ.filehub == texas_filehub


def test_econunit_shop_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_real_id = temp_real_id()
    sue_text = "Sue"
    sue_texas_filehub = get_texas_filehub()
    sue_texas_filehub.person_id = sue_text

    # WHEN
    texas_econ = econunit_shop(sue_texas_filehub)

    # THEN
    assert texas_econ != None
    assert texas_econ.filehub.real_id == x_real_id
    assert texas_econ._treasury_db != None
    assert texas_econ.filehub.person_id == sue_text
    assert texas_econ.filehub.road_delimiter == default_road_delimiter_if_none()


def test_econunit_shop_ReturnsObj_WithTempNames(env_dir_setup_cleanup):
    # GIVEN / WHEN
    texas_econ = econunit_shop(get_texas_filehub())

    # THEN
    assert texas_econ != None
    assert texas_econ.filehub == get_texas_filehub()
    # assert os_path_exists(econ_dir)
    assert texas_econ._treasury_db != None


def test_EconUnit_create_treasury_db_CreatesDatabaseFile(env_dir_setup_cleanup):
    # GIVEN create econ
    texas_filehub = get_texas_filehub()
    x_econ = EconUnit(texas_filehub)
    print(f"{temp_reals_dir()=} {x_econ.filehub.econ_dir()=}")
    print(f"delete {x_econ.filehub.econ_dir()=}")
    treasury_file_path = texas_filehub.treasury_db_path()

    assert os_path_exists(treasury_file_path) is False

    # WHEN
    x_econ.create_treasury_db(in_memory=False)

    # THEN check agendas src directory created
    assert os_path_exists(treasury_file_path)


def test_create_job_file_from_role_file_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_role = agendaunit_shop(sue_text)
    sue_role.calc_agenda_metrics()
    texas_filehub = get_texas_filehub()
    texas_filehub.save_role_agenda(sue_role)
    sue_job_file_path = texas_filehub.job_path(sue_text)
    assert os_path_exists(sue_job_file_path) == False

    # WHEN
    sue_job = create_job_file_from_role_file(texas_filehub, sue_text)

    # GIVEN
    assert sue_job._owner_id != None
    assert sue_job._owner_id == sue_text
    assert sue_job.get_dict() == sue_role.get_dict()
    assert os_path_exists(sue_job_file_path)
