from src._instrument.file import delete_dir
from src._road.road import default_road_delimiter_if_none, create_road
from src._road.worlddir import econdir_shop
from src.econ.econ import (
    EconUnit,
    econunit_shop,
    temp_person_id,
    temp_real_id,
)
from src.econ.examples.econ_env_kit import (
    temp_reals_dir,
    temp_reals_dir,
    copy_evaluation_econ,
    env_dir_setup_cleanup,
    get_texas_road,
    get_texas_econdir,
)
from pytest import raises as pytest_raises
from os import path as os_path


def test_EconUnit_exists():
    # GIVEN
    x_real_id = "test1"

    # WHEN
    x_econ = EconUnit(x_real_id, econ_dir=temp_reals_dir())

    # THEN
    assert x_econ.real_id == x_real_id
    assert x_econ.econ_dir == temp_reals_dir()
    assert x_econ._manager_person_id is None
    assert x_econ._road_delimiter is None


def test_EconUnit_set_real_id_CorrectlySetsAttr():
    # GIVEN
    x_econunit = EconUnit()
    assert x_econunit.real_id is None

    # WHEN
    texas_text = "texas"
    x_econunit.set_real_id(texas_text)

    # THEN
    assert x_econunit.real_id == texas_text


def test_econunit_shop_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_real_id = temp_real_id()
    sue_text = "Sue"
    sue_texas_econdir = get_texas_econdir()
    sue_texas_econdir.person_id = sue_text

    # WHEN
    texas_econ = econunit_shop(sue_texas_econdir)

    # THEN
    assert texas_econ != None
    assert texas_econ.real_id == x_real_id
    assert os_path.exists(sue_texas_econdir.econ_dir())
    assert texas_econ._treasury_db != None
    assert texas_econ._manager_person_id == sue_text
    assert texas_econ._road_delimiter == default_road_delimiter_if_none()


def test_econunit_shop_ReturnsObj_WithTempNames(env_dir_setup_cleanup):
    # GIVEN
    x_real_id = temp_real_id()
    # assert os_path.exists(econ_dir) is False

    # WHEN
    texas_econ = econunit_shop(get_texas_econdir())

    # THEN
    assert texas_econ != None
    assert texas_econ.real_id == x_real_id
    # assert os_path.exists(econ_dir)
    assert texas_econ._treasury_db != None
    assert texas_econ._manager_person_id == temp_person_id()
    assert texas_econ._road_delimiter == default_road_delimiter_if_none()


def test_econunit_shop_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"
    texas_econdir = get_texas_econdir()
    texas_econdir.real_id = texas_text
    texas_econdir._road_delimiter = slash_text

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        econunit_shop(texas_econdir)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_EconUnit_set_road_delimiter_CorrectSetsAttribute(
    env_dir_setup_cleanup,
):
    # GIVEN
    texas_econdir = get_texas_econdir()
    texas_econ = econunit_shop(texas_econdir)
    assert texas_econ._road_delimiter == default_road_delimiter_if_none()

    # WHEN
    slash_text = "/"
    texas_econ.set_road_delimiter(slash_text)

    # THEN
    assert texas_econ._road_delimiter == slash_text


def test_EconUnit_get_jobs_dir_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN create econ
    x_real_id = temp_real_id()
    x_econ = EconUnit(x_real_id, econ_dir=temp_reals_dir())

    # WHEN / THEN
    jobs_text = "jobs"
    assert x_econ.get_jobs_dir() == f"{x_econ.get_object_root_dir()}/{jobs_text}"


def test_EconUnit_get_roles_dir_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN create econ
    x_real_id = temp_real_id()
    x_econ = EconUnit(x_real_id, econ_dir=temp_reals_dir())

    # WHEN / THEN
    roles_text = "roles"
    assert x_econ.get_roles_dir() == f"{x_econ.get_object_root_dir()}/{roles_text}"


def test_EconUnit_set_econ_dirs_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create econ
    x_real_id = temp_real_id()
    x_econ = EconUnit(x_real_id, econ_dir=temp_reals_dir())
    texas_econdir = get_texas_econdir()
    print(f"{temp_reals_dir()=} {x_econ.econ_dir=}")
    # delete_dir(x_econ.get_object_root_dir())
    print(f"delete {x_econ.get_object_root_dir()=}")
    delete_dir(texas_econdir.reals_dir)
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{texas_econdir.reals_dir}/{treasury_file_name}"

    assert os_path.exists(texas_econdir.reals_dir) is False
    assert os_path.isdir(texas_econdir.reals_dir) is False
    assert os_path.exists(x_econ.get_jobs_dir()) is False
    assert os_path.exists(x_econ.get_roles_dir()) is False
    assert os_path.exists(treasury_file_path) is False

    # WHEN
    x_econ.set_econ_dirs(in_memory_treasury=False)

    # THEN check agendas src directory created
    assert os_path.exists(texas_econdir.reals_dir)
    assert os_path.isdir(texas_econdir.reals_dir)
    assert os_path.exists(x_econ.get_jobs_dir())
    assert os_path.exists(x_econ.get_roles_dir())
    assert os_path.exists(treasury_file_path)
    assert x_econ.get_object_root_dir() == texas_econdir.reals_dir
    assert x_econ.get_jobs_dir() == x_econ.get_jobs_dir()
    assert x_econ.get_roles_dir() == x_econ.get_roles_dir()
    assert x_econ.get_treasury_db_path() == treasury_file_path


# def test_modify_real_id_example_econ_CorrectlyModifiesDirAndFiles(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN create econ
#     texas_econdir = get_texas_econdir()
#     old_x_real_id = texas_econdir.real_id
#     old_econ_dir = texas_econdir.econ_dir()
#     old_jobs_dir = texas_econdir.jobs_dir()
#     old_roles_dir = texas_econdir.roles_dir()
#     print(f"{texas_econdir.econ_road=}")

#     new_econdir = get_texas_econdir()
#     new_econdir.real_id = "music"
#     new_x_real_id = new_econdir.real_id
#     new_econ_dir = new_econdir.econ_dir()
#     new_jobs_dir = new_econdir.jobs_dir()
#     new_roles_dir = new_econdir.roles_dir()
#     delete_dir(dir=new_econ_dir)
#     print(f"{new_econ_dir=}")

#     texas_econ = econunit_shop(texas_econdir)

#     texas_econ.set_econ_dirs(in_memory_treasury=True)

#     assert os_path.exists(old_econ_dir)
#     assert os_path.isdir(old_econ_dir)
#     assert os_path.exists(old_jobs_dir)
#     assert os_path.exists(old_roles_dir)
#     assert texas_econ.get_jobs_dir() == old_jobs_dir
#     assert texas_econ.get_roles_dir() == old_roles_dir

#     assert os_path.exists(new_econ_dir) is False
#     assert os_path.isdir(new_econ_dir) is False
#     assert os_path.exists(new_jobs_dir) is False
#     assert os_path.exists(new_roles_dir) is False
#     assert texas_econ.get_jobs_dir() != new_jobs_dir
#     assert texas_econ.get_roles_dir() != new_roles_dir
#     assert texas_econ.real_id != new_x_real_id

#     # WHEN
#     print(f"{new_x_real_id=} {old_x_real_id=}")
#     print(f"{old_econ_dir=}")
#     assert os_path.exists(old_econ_dir)
#     texas_econdir.save_file_job("sue", "fooboo", True)
#     modify_real_id_example_econ(
#         econ_obj=texas_econ,
#         src_econdir=texas_econdir,
#         dst_econdir=new_econdir,
#         new_real_id=new_x_real_id,
#     )

#     # THEN check agendas src directory created
#     assert os_path.exists(old_econ_dir) is False
#     assert os_path.isdir(old_econ_dir) is False
#     assert os_path.exists(old_jobs_dir) is False
#     assert os_path.exists(old_roles_dir) is False
#     assert texas_econ.real_id == new_x_real_id
#     print(f"{texas_econ.get_jobs_dir()=}")
#     print(f"           {old_jobs_dir=}")
#     assert texas_econ.get_jobs_dir() != old_jobs_dir
#     assert texas_econ.get_roles_dir() != old_roles_dir

#     assert os_path.exists(new_econ_dir)
#     assert os_path.isdir(new_econ_dir)
#     assert os_path.exists(new_jobs_dir)
#     assert os_path.exists(new_roles_dir)
#     assert texas_econ.get_jobs_dir() == new_jobs_dir
#     assert texas_econ.get_roles_dir() == new_roles_dir

#     # Undo modification to directory
#     # delete_dir(dir=old_econ_dir)
#     # print(f"{old_econ_dir=}")
#     delete_dir(dir=new_econ_dir)
#     print(f"{new_econ_dir=}")


# def test_copy_evaluation_econ_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
#     # GIVEN create econ
#     old_x_real_id = temp_real_id()
#     old_econ_dir = f"src/econ/examples/econs/{old_x_real_id}"
#     jobs_text = "jobs"
#     old_jobs_dir = f"{old_econ_dir}/{jobs_text}"
#     roles_text = "roles"
#     old_roles_dir = f"{old_econ_dir}/{roles_text}"
#     texas_econdir = get_texas_econdir()

#     x_econ = econunit_shop(old_x_real_id, temp_reals_dir())
#     x_econ.set_econ_dirs()

#     assert os_path.exists(old_econ_dir)
#     assert os_path.isdir(old_econ_dir)
#     assert os_path.exists(old_jobs_dir)
#     assert os_path.exists(old_roles_dir)
#     assert x_econ.get_jobs_dir() == old_jobs_dir
#     assert x_econ.get_roles_dir() == old_roles_dir

#     new_x_real_id = "ex_env1"
#     new_econ_dir = f"src/econ/examples/econs/{new_x_real_id}"
#     new_jobs_dir = f"{new_econ_dir}/{jobs_text}"
#     new_roles_dir = f"{new_econ_dir}/{roles_text}"

#     assert os_path.exists(new_econ_dir) is False
#     assert os_path.isdir(new_econ_dir) is False
#     assert os_path.exists(new_jobs_dir) is False
#     assert os_path.exists(new_roles_dir) is False
#     assert x_econ.get_jobs_dir() != new_jobs_dir
#     assert x_econ.get_roles_dir() != new_roles_dir
#     assert x_econ.real_id != new_x_real_id

#     # WHEN
#     copy_evaluation_econ(src_real_id=x_econ.real_id, dest_real_id=new_x_real_id)

#     # THEN check agendas src directory created
#     assert os_path.exists(old_econ_dir)
#     assert os_path.isdir(old_econ_dir)
#     assert os_path.exists(old_jobs_dir)
#     assert os_path.exists(old_roles_dir)
#     assert x_econ.get_jobs_dir() == old_jobs_dir
#     assert x_econ.get_roles_dir() == old_roles_dir

#     assert os_path.exists(new_econ_dir)
#     assert os_path.isdir(new_econ_dir)
#     assert os_path.exists(new_jobs_dir)
#     assert os_path.exists(new_roles_dir)
#     assert x_econ.get_jobs_dir() != new_jobs_dir
#     assert x_econ.get_roles_dir() != new_roles_dir
#     assert x_econ.real_id != new_x_real_id

#     # Undo modification to directory
#     # delete_dir(x_econ.get_object_root_dir())
#     # delete_dir(dir=old_econ_dir)
#     delete_dir(dir=new_econ_dir)


# def test_copy_evaluation_econ_CorrectlyRaisesError(env_dir_setup_cleanup):
#     # GIVEN create econ
#     old_x_real_id = temp_real_id()
#     x_econ = econunit_shop(old_x_real_id, temp_reals_dir())
#     x_econ.set_econ_dirs()

#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         copy_evaluation_econ(src_real_id=x_econ.real_id, dest_real_id=old_x_real_id)
#     assert (
#         str(excinfo.value)
#         == f"Cannot copy econ to '{x_econ.get_object_root_dir()}' directory because '{x_econ.get_object_root_dir()}' exists."
#     )
