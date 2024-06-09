from src._instrument.file import save_file, open_file, delete_dir
from src._instrument.sqlite import check_connection
from src._road.jaar_config import treasury_file_name
from src._road.road import default_road_delimiter_if_none
from src.econ.econ import econunit_shop, EconUnit
from src.econ.examples.econ_env import env_dir_setup_cleanup, get_texas_filehub
from pytest import raises as pytest_raises
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
    sue_text = "Sue"
    sue_texas_filehub = get_texas_filehub()
    sue_texas_filehub.person_id = sue_text

    # WHEN
    texas_econ = econunit_shop(sue_texas_filehub)

    # THEN
    assert texas_econ != None
    assert texas_econ.filehub.real_id != None
    assert texas_econ._treasury_db != None
    assert texas_econ.filehub.person_id == sue_text
    assert texas_econ.filehub.road_delimiter == default_road_delimiter_if_none()
    assert texas_econ.filehub == sue_texas_filehub


def test_EconUnitcreate_treasury_db_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    texas_filehub = get_texas_filehub()
    x_econ = econunit_shop(texas_filehub)
    delete_dir(texas_filehub.treasury_db_path())  # clear out any treasury.db file
    assert os_path_exists(x_econ.filehub.treasury_db_path()) is False

    # WHEN
    x_econ.create_treasury_db()

    # THEN
    assert os_path_exists(x_econ.filehub.treasury_db_path())


def test_EconUnitcreate_treasury_db_DoesNotOverWriteDBIfItExists(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    texas_filehub = get_texas_filehub()
    x_econ = econunit_shop(texas_filehub)
    delete_dir(texas_filehub.treasury_db_path())  # clear out any treasury.db file
    x_econ.create_treasury_db()
    assert os_path_exists(x_econ.filehub.treasury_db_path())

    # GIVEN
    x_file_text = "Texas Dallas ElPaso"
    db_file = treasury_file_name()
    save_file(
        x_econ.filehub.econ_dir(),
        file_name=db_file,
        file_text=x_file_text,
        replace=True,
    )
    assert os_path_exists(x_econ.filehub.treasury_db_path())
    assert open_file(x_econ.filehub.econ_dir(), file_name=db_file) == x_file_text

    # WHEN
    x_econ.create_treasury_db()
    # THEN
    assert open_file(x_econ.filehub.econ_dir(), file_name=db_file) == x_file_text

    # # WHEN
    # x_econ.create_treasury_db(overwrite=True)
    # # THEN
    # assert open_file(x_econ.filehub.econ_dir(), file_name=db_file) != x_file_text


def test_EconUnitcreate_treasury_db_CanCreateTreasuryInMemory(env_dir_setup_cleanup):
    # GIVEN create econ
    texas_filehub = get_texas_filehub()
    x_econ = econunit_shop(texas_filehub)

    x_econ._treasury_db = None
    assert x_econ._treasury_db is None
    assert os_path_exists(x_econ.filehub.treasury_db_path()) is False

    # WHEN
    x_econ.create_treasury_db(in_memory=True)

    # THEN
    assert x_econ._treasury_db != None
    assert os_path_exists(x_econ.filehub.treasury_db_path()) is False


def test_EconUnit_refresh_treasury_job_agendas_data_CanConnectToTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    texas_filehub = get_texas_filehub()
    x_econ = econunit_shop(texas_filehub)
    # x_econ.create_treasury_db(in_memory=True)
    assert os_path_exists(x_econ.filehub.treasury_db_path()) is False

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    assert os_path_exists(x_econ.filehub.treasury_db_path()) is False


def test_EconUnit_get_treasury_conn_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    x_econ = EconUnit(get_texas_filehub())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_econ.get_treasury_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_econ.create_treasury_db(in_memory=True)

    # THEN
    assert check_connection(x_econ.get_treasury_conn())
