from src._instrument.file import save_file, open_file, delete_dir
from src._instrument.sqlite import check_connection
from src._road.jaar_config import treasury_file_name
from src._road.road import default_road_delimiter_if_none
from src.money.money import moneyunit_shop, MoneyUnit
from src.money.examples.econ_env import env_dir_setup_cleanup, get_texas_userhub
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_MoneyUnit_exists():
    # GIVEN
    texas_userhub = get_texas_userhub()

    # WHEN
    x_money = MoneyUnit(userhub=texas_userhub)

    # THEN
    assert x_money.userhub == texas_userhub


def test_moneyunit_shop_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_texas_userhub = get_texas_userhub()
    sue_texas_userhub.owner_id = sue_text

    # WHEN
    texas_money = moneyunit_shop(sue_texas_userhub)

    # THEN
    assert texas_money != None
    assert texas_money.userhub.real_id != None
    assert texas_money._treasury_db != None
    assert texas_money.userhub.owner_id == sue_text
    assert texas_money.userhub.road_delimiter == default_road_delimiter_if_none()
    assert texas_money.userhub == sue_texas_userhub


def test_MoneyUnitcreate_treasury_db_CreatesTreasuryDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    texas_userhub = get_texas_userhub()
    x_money = moneyunit_shop(texas_userhub)
    delete_dir(texas_userhub.treasury_db_path())  # clear out any treasury.db file
    assert os_path_exists(x_money.userhub.treasury_db_path()) is False

    # WHEN
    x_money.create_treasury_db()

    # THEN
    assert os_path_exists(x_money.userhub.treasury_db_path())


def test_MoneyUnitcreate_treasury_db_DoesNotOverWriteDBIfItExists(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    texas_userhub = get_texas_userhub()
    x_money = moneyunit_shop(texas_userhub)
    delete_dir(texas_userhub.treasury_db_path())  # clear out any treasury.db file
    x_money.create_treasury_db()
    assert os_path_exists(x_money.userhub.treasury_db_path())

    # GIVEN
    x_file_text = "Texas Dallas ElPaso"
    db_file = treasury_file_name()
    save_file(
        x_money.userhub.econ_dir(),
        file_name=db_file,
        file_text=x_file_text,
        replace=True,
    )
    assert os_path_exists(x_money.userhub.treasury_db_path())
    assert open_file(x_money.userhub.econ_dir(), file_name=db_file) == x_file_text

    # WHEN
    x_money.create_treasury_db()
    # THEN
    assert open_file(x_money.userhub.econ_dir(), file_name=db_file) == x_file_text

    # # WHEN
    # x_money.create_treasury_db(overwrite=True)
    # # THEN
    # assert open_file(x_money.userhub.econ_dir(), file_name=db_file) != x_file_text


def test_MoneyUnitcreate_treasury_db_CanCreateTreasuryInMemory(env_dir_setup_cleanup):
    # GIVEN create econ
    texas_userhub = get_texas_userhub()
    x_money = moneyunit_shop(texas_userhub)

    x_money._treasury_db = None
    assert x_money._treasury_db is None
    assert os_path_exists(x_money.userhub.treasury_db_path()) is False

    # WHEN
    x_money.create_treasury_db(in_memory=True)

    # THEN
    assert x_money._treasury_db != None
    assert os_path_exists(x_money.userhub.treasury_db_path()) is False


def test_MoneyUnit_refresh_treasury_job_worlds_data_CanConnectToTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    texas_userhub = get_texas_userhub()
    x_money = moneyunit_shop(texas_userhub)
    # x_money.create_treasury_db(in_memory=True)
    assert os_path_exists(x_money.userhub.treasury_db_path()) is False

    # WHEN
    x_money.refresh_treasury_job_worlds_data()

    # THEN
    assert os_path_exists(x_money.userhub.treasury_db_path()) is False


# def test_MoneyUnit_get_treasury_conn_CreatesTreasuryDBIfItDoesNotExist(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN create econ
#     x_money = MoneyUnit(get_texas_userhub())
#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         check_connection(x_money.get_treasury_conn())
#     assert str(excinfo.value) == "unable to open database file"

#     # WHEN
#     x_money.create_treasury_db(in_memory=True)

#     # THEN
#     assert check_connection(x_money.get_treasury_conn())
