from src._road.road import default_road_delimiter_if_none, create_road
from src.instrument.file import delete_dir
from os import path as os_path
from src.econ.econ import (
    EconUnit,
    econunit_shop,
    get_temp_env_person_id,
    get_temp_env_problem_id,
    get_temp_env_healer_id,
    get_temp_env_world_id,
)
from src.econ.examples.econ_env_kit import (
    get_test_econ_dir,
    change_world_id_example_econ,
    copy_evaluation_econ,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_EconUnit_exists():
    # GIVEN
    x_world_id = "test1"

    # WHEN
    x_econ = EconUnit(x_world_id, econ_dir=get_test_econ_dir())

    # THEN
    assert x_econ.world_id == x_world_id
    assert x_econ.econ_dir == get_test_econ_dir()
    assert x_econ._manager_person_id is None
    assert x_econ._road_delimiter is None


def test_EconUnit_set_world_id_CorrectlySetsAttr():
    # GIVEN
    x_econunit = EconUnit()
    assert x_econunit.world_id is None

    # WHEN
    texas_text = "texas"
    x_econunit.set_world_id(texas_text)

    # THEN
    assert x_econunit.world_id == texas_text


def test_econunit_shop_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_world_id = get_temp_env_world_id()
    econ_dir = f"src/econ/examples/econs/{x_world_id}"
    sue_text = "Sue"
    assert os_path.exists(econ_dir) is False

    # WHEN
    x_econ = econunit_shop(
        world_id=x_world_id,
        econ_dir=get_test_econ_dir(),
        _manager_person_id=sue_text,
    )

    # THEN
    assert x_econ != None
    assert x_econ.world_id == x_world_id
    assert os_path.exists(econ_dir)
    assert x_econ._treasury_db != None
    assert x_econ._manager_person_id == sue_text
    assert x_econ._clerkunits == {}
    assert x_econ._road_delimiter == default_road_delimiter_if_none()


def test_econunit_shop_ReturnsObj_WithTempNames(env_dir_setup_cleanup):
    # GIVEN
    x_world_id = get_temp_env_world_id()
    # assert os_path.exists(econ_dir) is False

    # WHEN
    x_econ = econunit_shop(world_id=x_world_id, econ_dir=get_test_econ_dir())

    # THEN
    assert x_econ != None
    assert x_econ.world_id == x_world_id
    # assert os_path.exists(econ_dir)
    assert x_econ._treasury_db != None
    assert x_econ._manager_person_id == get_temp_env_person_id()
    assert x_econ._clerkunits == {}
    assert x_econ._road_delimiter == default_road_delimiter_if_none()


def test_econunit_shop_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        econunit_shop(world_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_EconUnit_set_road_delimiter_CorrectSetsAttribute(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_world_id = get_temp_env_world_id()
    econ_dir = f"src/econ/examples/econs/{x_world_id}"
    sue_text = "Sue"
    x_econ = econunit_shop(x_world_id, get_test_econ_dir(), _manager_person_id=sue_text)
    assert x_econ._road_delimiter == default_road_delimiter_if_none()

    # WHEN
    slash_text = "/"
    x_econ.set_road_delimiter(slash_text)

    # THEN
    assert x_econ._road_delimiter == slash_text


def test_EconUnit_get_jobs_dir_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN create econ
    x_world_id = get_temp_env_world_id()
    x_econ = EconUnit(x_world_id, econ_dir=get_test_econ_dir())

    # WHEN / THEN
    jobs_text = "jobs"
    assert x_econ.get_jobs_dir() == f"{x_econ.get_object_root_dir()}/{jobs_text}"


def test_EconUnit_get_roles_dir_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN create econ
    x_world_id = get_temp_env_world_id()
    x_econ = EconUnit(x_world_id, econ_dir=get_test_econ_dir())

    # WHEN / THEN
    roles_text = "roles"
    assert x_econ.get_roles_dir() == f"{x_econ.get_object_root_dir()}/{roles_text}"


def test_EconUnit_set_econ_dirs_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create econ
    x_world_id = get_temp_env_world_id()
    x_econ = EconUnit(x_world_id, econ_dir=get_test_econ_dir())
    print(f"{get_test_econ_dir()=} {x_econ.econ_dir=}")
    # delete_dir(x_econ.get_object_root_dir())
    print(f"delete {x_econ.get_object_root_dir()=}")
    econ_dir = f"src/econ/examples/econs/{x_world_id}"
    econ_file_name = "econ.json"
    econ_file_path = f"{econ_dir}/{econ_file_name}"
    clerkunits_dir = f"{econ_dir}/clerkunits"
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{econ_dir}/{treasury_file_name}"

    assert os_path.exists(econ_dir) is False
    assert os_path.isdir(econ_dir) is False
    assert os_path.exists(econ_file_path) is False
    assert os_path.exists(x_econ.get_jobs_dir()) is False
    assert os_path.exists(x_econ.get_roles_dir()) is False
    assert os_path.exists(clerkunits_dir) is False
    assert os_path.exists(treasury_file_path) is False

    # WHEN
    x_econ.set_econ_dirs(in_memory_treasury=False)

    # THEN check agendas src directory created
    assert os_path.exists(econ_dir)
    assert os_path.isdir(econ_dir)
    assert os_path.exists(econ_file_path)
    assert os_path.exists(x_econ.get_jobs_dir())
    assert os_path.exists(x_econ.get_roles_dir())
    assert os_path.exists(clerkunits_dir)
    assert os_path.exists(treasury_file_path)
    assert x_econ.get_object_root_dir() == econ_dir
    assert x_econ.get_jobs_dir() == x_econ.get_jobs_dir()
    assert x_econ.get_roles_dir() == x_econ.get_roles_dir()
    assert x_econ.get_clerkunits_dir() == clerkunits_dir
    assert x_econ.get_treasury_db_path() == treasury_file_path


def test_change_world_id_example_econ_CorrectlyChangesDirAndFiles(
    env_dir_setup_cleanup,
):
    # GIVEN create econ
    old_x_world_id = get_temp_env_world_id()
    old_econ_dir = f"src/econ/examples/econs/{old_x_world_id}"
    old_econ_file_name = "econ.json"
    old_econ_file_path = f"{old_econ_dir}/{old_econ_file_name}"
    jobs_text = "jobs"
    old_jobs_dir = f"{old_econ_dir}/{jobs_text}"
    roles_text = "roles"
    old_roles_dir = f"{old_econ_dir}/{roles_text}"
    old_clerkunits_dir = f"{old_econ_dir}/clerkunits"

    new_x_world_id = "ex_env1"
    new_econ_dir = f"src/econ/examples/econs/{new_x_world_id}"
    new_econ_file_name = "econ.json"
    new_econ_file_path = f"{new_econ_dir}/{new_econ_file_name}"
    new_jobs_dir = f"{new_econ_dir}/{jobs_text}"
    new_roles_dir = f"{new_econ_dir}/{roles_text}"
    new_clerkunits_dir = f"{new_econ_dir}/clerkunits"
    delete_dir(dir=new_econ_dir)
    print(f"{new_econ_dir=}")

    x_econ = econunit_shop(world_id=old_x_world_id, econ_dir=get_test_econ_dir())
    # delete_dir(x_econ.get_object_root_dir())
    # print(f"{x_econ.get_object_root_dir()=}")

    x_econ.set_econ_dirs(in_memory_treasury=True)

    assert os_path.exists(old_econ_dir)
    assert os_path.isdir(old_econ_dir)
    assert os_path.exists(old_econ_file_path)
    assert os_path.exists(old_jobs_dir)
    assert os_path.exists(old_roles_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_econ.get_jobs_dir() == old_jobs_dir
    assert x_econ.get_roles_dir() == old_roles_dir
    assert x_econ.get_clerkunits_dir() == old_clerkunits_dir

    assert os_path.exists(new_econ_dir) is False
    assert os_path.isdir(new_econ_dir) is False
    assert os_path.exists(new_econ_file_path) is False
    assert os_path.exists(new_jobs_dir) is False
    assert os_path.exists(new_roles_dir) is False
    assert os_path.exists(new_clerkunits_dir) is False
    assert x_econ.get_jobs_dir() != new_jobs_dir
    assert x_econ.get_roles_dir() != new_roles_dir
    assert x_econ.get_clerkunits_dir() != new_clerkunits_dir
    assert x_econ.world_id != new_x_world_id

    # WHEN
    print(f"{new_x_world_id=} {old_x_world_id=}")
    change_world_id_example_econ(econ_obj=x_econ, new_world_id=new_x_world_id)

    # THEN check agendas src directory created
    assert os_path.exists(old_econ_dir) is False
    assert os_path.isdir(old_econ_dir) is False
    assert os_path.exists(old_econ_file_path) is False
    assert os_path.exists(old_jobs_dir) is False
    assert os_path.exists(old_roles_dir) is False
    assert os_path.exists(old_clerkunits_dir) is False
    assert x_econ.world_id == new_x_world_id
    print(f"{x_econ.get_jobs_dir()=}")
    print(f"           {old_jobs_dir=}")
    assert x_econ.get_jobs_dir() != old_jobs_dir
    assert x_econ.get_roles_dir() != old_roles_dir
    assert x_econ.get_clerkunits_dir() != old_clerkunits_dir

    assert os_path.exists(new_econ_dir)
    assert os_path.isdir(new_econ_dir)
    assert os_path.exists(new_econ_file_path)
    assert os_path.exists(new_jobs_dir)
    assert os_path.exists(new_roles_dir)
    assert os_path.exists(new_clerkunits_dir)
    assert x_econ.get_jobs_dir() == new_jobs_dir
    assert x_econ.get_roles_dir() == new_roles_dir
    assert x_econ.get_clerkunits_dir() == new_clerkunits_dir

    # Undo change to directory
    # delete_dir(dir=old_econ_dir)
    # print(f"{old_econ_dir=}")
    delete_dir(dir=new_econ_dir)
    print(f"{new_econ_dir=}")


def test_copy_evaluation_econ_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create econ
    old_x_world_id = get_temp_env_world_id()
    old_econ_dir = f"src/econ/examples/econs/{old_x_world_id}"
    old_econ_file_name = "econ.json"
    old_econ_file_path = f"{old_econ_dir}/{old_econ_file_name}"
    jobs_text = "jobs"
    old_jobs_dir = f"{old_econ_dir}/{jobs_text}"
    roles_text = "roles"
    old_roles_dir = f"{old_econ_dir}/{roles_text}"
    old_clerkunits_dir = f"{old_econ_dir}/clerkunits"

    x_econ = econunit_shop(old_x_world_id, get_test_econ_dir())
    x_econ.set_econ_dirs()

    assert os_path.exists(old_econ_dir)
    assert os_path.isdir(old_econ_dir)
    assert os_path.exists(old_econ_file_path)
    assert os_path.exists(old_jobs_dir)
    assert os_path.exists(old_roles_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_econ.get_jobs_dir() == old_jobs_dir
    assert x_econ.get_roles_dir() == old_roles_dir
    assert x_econ.get_clerkunits_dir() == old_clerkunits_dir

    new_x_world_id = "ex_env1"
    new_econ_dir = f"src/econ/examples/econs/{new_x_world_id}"
    new_econ_file_name = "econ.json"
    new_econ_file_path = f"{new_econ_dir}/{new_econ_file_name}"
    new_jobs_dir = f"{new_econ_dir}/{jobs_text}"
    new_roles_dir = f"{new_econ_dir}/{roles_text}"
    new_clerkunits_dir = f"{new_econ_dir}/clerkunits"

    assert os_path.exists(new_econ_dir) is False
    assert os_path.isdir(new_econ_dir) is False
    assert os_path.exists(new_econ_file_path) is False
    assert os_path.exists(new_jobs_dir) is False
    assert os_path.exists(new_roles_dir) is False
    assert os_path.exists(new_clerkunits_dir) is False
    assert x_econ.get_jobs_dir() != new_jobs_dir
    assert x_econ.get_roles_dir() != new_roles_dir
    assert x_econ.get_clerkunits_dir() != new_clerkunits_dir
    assert x_econ.world_id != new_x_world_id

    # WHEN
    copy_evaluation_econ(src_world_id=x_econ.world_id, dest_world_id=new_x_world_id)

    # THEN check agendas src directory created
    assert os_path.exists(old_econ_dir)
    assert os_path.isdir(old_econ_dir)
    assert os_path.exists(old_econ_file_path)
    assert os_path.exists(old_jobs_dir)
    assert os_path.exists(old_roles_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_econ.get_jobs_dir() == old_jobs_dir
    assert x_econ.get_roles_dir() == old_roles_dir
    assert x_econ.get_clerkunits_dir() == old_clerkunits_dir

    assert os_path.exists(new_econ_dir)
    assert os_path.isdir(new_econ_dir)
    assert os_path.exists(new_econ_file_path)
    assert os_path.exists(new_jobs_dir)
    assert os_path.exists(new_roles_dir)
    assert os_path.exists(new_clerkunits_dir)
    assert x_econ.get_jobs_dir() != new_jobs_dir
    assert x_econ.get_roles_dir() != new_roles_dir
    assert x_econ.get_clerkunits_dir() != new_clerkunits_dir
    assert x_econ.world_id != new_x_world_id

    # Undo change to directory
    # delete_dir(x_econ.get_object_root_dir())
    # delete_dir(dir=old_econ_dir)
    delete_dir(dir=new_econ_dir)


def test_copy_evaluation_econ_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create econ
    old_x_world_id = get_temp_env_world_id()
    x_econ = econunit_shop(old_x_world_id, get_test_econ_dir())
    x_econ.set_econ_dirs()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_econ(src_world_id=x_econ.world_id, dest_world_id=old_x_world_id)
    assert (
        str(excinfo.value)
        == f"Cannot copy econ to '{x_econ.get_object_root_dir()}' directory because '{x_econ.get_object_root_dir()}' exists."
    )


def test_EconUnit_get_road_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_world_id = get_temp_env_world_id()
    x_econ = econunit_shop(x_world_id, econ_dir=get_test_econ_dir())
    bob_text = "Bob"
    econ_road_with_root = create_road(x_econ.world_id, bob_text)
    econ_road_wo_root = bob_text
    # healer_list_wo_root = get_all_road_nodes(econ_road_wo_root)
    bloomers_text = "bloomers"
    bloomers_road_with_root = create_road(econ_road_with_root, bloomers_text)
    bloomers_road_wo_root = create_road(econ_road_wo_root, bloomers_text)
    # bloomers_list_wo_root = get_all_road_nodes(bloomers_road_wo_root)
    roses_text = "roses"
    roses_road_with_root = create_road(bloomers_road_with_root, roses_text)
    roses_road_wo_root = create_road(bloomers_road_wo_root, roses_text)
    # roses_list_wo_root = get_all_road_nodes(roses_road_wo_root)

    # WHEN / THEN
    assert x_econ.world_id == x_econ.build_econ_road()
    assert econ_road_with_root == x_econ.build_econ_road(econ_road_wo_root)
    assert bloomers_road_with_root == x_econ.build_econ_road(bloomers_road_wo_root)
    assert roses_road_with_root == x_econ.build_econ_road(roses_road_wo_root)
