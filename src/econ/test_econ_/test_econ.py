from src._road.road import default_road_delimiter_if_none
from src.econ.econ import econunit_shop, EconUnit
from src.econ.examples.econ_env_kit import (
    env_dir_setup_cleanup,
    temp_reals_dir,
    temp_reals_dir,
    temp_real_id,
    get_texas_filehub,
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
    assert texas_econ.filehub == sue_texas_filehub


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
