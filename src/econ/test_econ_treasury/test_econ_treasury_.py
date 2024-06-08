from src._instrument.file import save_file, open_file, delete_dir
from src._instrument.sqlite import check_connection
from src.econ.econ import econunit_shop, EconUnit, treasury_db_filename
from src.econ.examples.econ_env_kit import env_dir_setup_cleanup, get_texas_agendahub
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_EconUnitcreate_treasury_db_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    texas_agendahub = get_texas_agendahub()
    x_econ = econunit_shop(texas_agendahub)
    delete_dir(texas_agendahub.treasury_db_path())  # clear out any treasury.db file
    assert os_path_exists(x_econ.agendahub.treasury_db_path()) == False

    # WHEN
    x_econ.create_treasury_db()

    # THEN
    assert os_path_exists(x_econ.agendahub.treasury_db_path())


def test_EconUnitcreate_treasury_db_DoesNotOverWriteDBIfItExists(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    texas_agendahub = get_texas_agendahub()
    x_econ = econunit_shop(texas_agendahub)
    delete_dir(texas_agendahub.treasury_db_path())  # clear out any treasury.db file
    x_econ.create_treasury_db()
    assert os_path_exists(x_econ.agendahub.treasury_db_path())

    # GIVEN
    x_file_text = "Texas Dallas ElPaso"
    db_file = treasury_db_filename()
    save_file(
        x_econ.agendahub.econ_dir(),
        file_name=db_file,
        file_text=x_file_text,
        replace=True,
    )
    assert os_path_exists(x_econ.agendahub.treasury_db_path())
    assert open_file(x_econ.agendahub.econ_dir(), file_name=db_file) == x_file_text

    # WHEN
    x_econ.create_treasury_db()
    # THEN
    assert open_file(x_econ.agendahub.econ_dir(), file_name=db_file) == x_file_text

    # # WHEN
    # x_econ.create_treasury_db(overwrite=True)
    # # THEN
    # assert open_file(x_econ.agendahub.econ_dir(), file_name=db_file) != x_file_text


def test_EconUnitcreate_treasury_db_CanCreateTreasuryInMemory(env_dir_setup_cleanup):
    # GIVEN create econ
    texas_agendahub = get_texas_agendahub()
    x_econ = econunit_shop(texas_agendahub)

    x_econ._treasury_db = None
    assert x_econ._treasury_db is None
    assert os_path_exists(x_econ.agendahub.treasury_db_path()) == False

    # WHEN
    x_econ.create_treasury_db(in_memory=True)

    # THEN
    assert x_econ._treasury_db != None
    assert os_path_exists(x_econ.agendahub.treasury_db_path()) == False


def test_EconUnit_refresh_treasury_job_agendas_data_CanConnectToTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    texas_agendahub = get_texas_agendahub()
    x_econ = econunit_shop(texas_agendahub)
    # x_econ.create_treasury_db(in_memory=True)
    assert os_path_exists(x_econ.agendahub.treasury_db_path()) == False

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    assert os_path_exists(x_econ.agendahub.treasury_db_path()) == False


def test_EconUnit_get_treasury_conn_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    x_econ = EconUnit(get_texas_agendahub())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(x_econ.get_treasury_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    x_econ.create_treasury_db(in_memory=True)

    # THEN
    assert check_connection(x_econ.get_treasury_conn())
