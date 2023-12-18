from src.agenda.road import get_road, get_all_road_nodes, get_node_delimiter
from src.agenda.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.culture.culture import CultureUnit, cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_culture_id,
    get_test_cultures_dir,
    change_culture_id_example_culture,
    copy_evaluation_culture,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_CultureUnit_exists():
    # GIVEN
    x_culture_id = "test1"

    # WHEN
    x_culture = CultureUnit(x_culture_id, cultures_dir=get_test_cultures_dir())

    # THEN
    assert x_culture.culture_id == x_culture_id
    assert x_culture.cultures_dir == get_test_cultures_dir()
    assert x_culture._manager_pid is None
    assert x_culture._road_node_delimiter is None


def test_cultureunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_culture_id = get_temp_env_culture_id()
    culture_dir = f"src/culture/examples/cultures/{x_culture_id}"
    sue_text = "Sue"
    assert os_path.exists(culture_dir) is False

    # WHEN
    x_culture = cultureunit_shop(
        x_culture_id, get_test_cultures_dir(), _manager_pid=sue_text
    )

    # THEN
    assert x_culture != None
    assert x_culture.culture_id == x_culture_id
    assert os_path.exists(culture_dir)
    assert x_culture._treasury_db != None
    assert x_culture._manager_pid == sue_text
    assert x_culture._councilunits == {}
    assert x_culture._road_node_delimiter == get_node_delimiter()


def test_CultureUnit_set_road_node_delimiter_CorrectSetsAttribute(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture_id = get_temp_env_culture_id()
    culture_dir = f"src/culture/examples/cultures/{x_culture_id}"
    sue_text = "Sue"
    x_culture = cultureunit_shop(
        x_culture_id, get_test_cultures_dir(), _manager_pid=sue_text
    )
    assert x_culture._road_node_delimiter == get_node_delimiter()

    # WHEN
    slash_text = "/"
    x_culture.set_road_node_delimiter(slash_text)

    # THEN
    assert x_culture._road_node_delimiter == slash_text


def test_cultureunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_culture_id = get_temp_env_culture_id()
    culture_dir = f"src/culture/examples/cultures/{x_culture_id}"
    sue_text = "Sue"
    assert os_path.exists(culture_dir) is False

    # WHEN
    x_culture = cultureunit_shop(
        x_culture_id,
        cultures_dir=get_test_cultures_dir(),
        _manager_pid=sue_text,
    )

    # THEN
    assert x_culture != None
    assert x_culture.culture_id == x_culture_id
    assert os_path.exists(culture_dir)
    assert x_culture._treasury_db != None
    assert x_culture._manager_pid == sue_text
    assert x_culture._councilunits == {}
    assert x_culture._road_node_delimiter == get_node_delimiter()


def test_culture_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create culture
    x_culture_id = get_temp_env_culture_id()
    x_culture = CultureUnit(x_culture_id, cultures_dir=get_test_cultures_dir())
    print(f"{get_test_cultures_dir()=} {x_culture.cultures_dir=}")
    # x_func_delete_dir(x_culture.get_object_root_dir())
    print(f"delete {x_culture.get_object_root_dir()=}")
    culture_dir = f"src/culture/examples/cultures/{x_culture_id}"
    culture_file_name = "culture.json"
    culture_file_path = f"{culture_dir}/{culture_file_name}"
    agendas_dir = f"{culture_dir}/agendas"
    councilunits_dir = f"{culture_dir}/councilunits"
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{culture_dir}/{treasury_file_name}"

    assert os_path.exists(culture_dir) is False
    assert os_path.isdir(culture_dir) is False
    assert os_path.exists(culture_file_path) is False
    assert os_path.exists(agendas_dir) is False
    assert os_path.exists(councilunits_dir) is False
    assert os_path.exists(treasury_file_path) is False

    # WHEN
    x_culture.create_dirs_if_null(in_memory_treasury=False)

    # THEN check agendas src directory created
    assert os_path.exists(culture_dir)
    assert os_path.isdir(culture_dir)
    assert os_path.exists(culture_file_path)
    assert os_path.exists(agendas_dir)
    assert os_path.exists(councilunits_dir)
    assert os_path.exists(treasury_file_path)
    assert x_culture.get_object_root_dir() == culture_dir
    assert x_culture.get_public_dir() == agendas_dir
    assert x_culture.get_councilunits_dir() == councilunits_dir
    assert x_culture.get_treasury_db_path() == treasury_file_path


def test_change_culture_id_example_culture_CorrectlyChangesDirAndFiles(
    env_dir_setup_cleanup,
):
    # GIVEN create culture
    old_x_culture_id = get_temp_env_culture_id()
    old_culture_dir = f"src/culture/examples/cultures/{old_x_culture_id}"
    old_culture_file_name = "culture.json"
    old_culture_file_path = f"{old_culture_dir}/{old_culture_file_name}"
    old_agendas_dir = f"{old_culture_dir}/agendas"
    old_councilunits_dir = f"{old_culture_dir}/councilunits"

    new_x_culture_id = "ex_env1"
    new_culture_dir = f"src/culture/examples/cultures/{new_x_culture_id}"
    new_culture_file_name = "culture.json"
    new_culture_file_path = f"{new_culture_dir}/{new_culture_file_name}"
    new_agendas_dir = f"{new_culture_dir}/agendas"
    new_councilunits_dir = f"{new_culture_dir}/councilunits"
    x_func_delete_dir(dir=new_culture_dir)
    print(f"{new_culture_dir=}")

    x_culture = cultureunit_shop(
        culture_id=old_x_culture_id, cultures_dir=get_test_cultures_dir()
    )
    # x_func_delete_dir(x_culture.get_object_root_dir())
    # print(f"{x_culture.get_object_root_dir()=}")

    x_culture.create_dirs_if_null(in_memory_treasury=True)

    assert os_path.exists(old_culture_dir)
    assert os_path.isdir(old_culture_dir)
    assert os_path.exists(old_culture_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_councilunits_dir)
    assert x_culture.get_public_dir() == old_agendas_dir
    assert x_culture.get_councilunits_dir() == old_councilunits_dir

    assert os_path.exists(new_culture_dir) is False
    assert os_path.isdir(new_culture_dir) is False
    assert os_path.exists(new_culture_file_path) is False
    assert os_path.exists(new_agendas_dir) is False
    assert os_path.exists(new_councilunits_dir) is False
    assert x_culture.get_public_dir() != new_agendas_dir
    assert x_culture.get_councilunits_dir() != new_councilunits_dir
    assert x_culture.culture_id != new_x_culture_id

    # WHEN
    change_culture_id_example_culture(
        culture_obj=x_culture, new_culture_id=new_x_culture_id
    )

    # THEN check agendas src directory created
    assert os_path.exists(old_culture_dir) is False
    assert os_path.isdir(old_culture_dir) is False
    assert os_path.exists(old_culture_file_path) is False
    assert os_path.exists(old_agendas_dir) is False
    assert os_path.exists(old_councilunits_dir) is False
    assert x_culture.get_public_dir() != old_agendas_dir
    assert x_culture.get_councilunits_dir() != old_councilunits_dir

    assert os_path.exists(new_culture_dir)
    assert os_path.isdir(new_culture_dir)
    assert os_path.exists(new_culture_file_path)
    assert os_path.exists(new_agendas_dir)
    assert os_path.exists(new_councilunits_dir)
    assert x_culture.get_public_dir() == new_agendas_dir
    assert x_culture.get_councilunits_dir() == new_councilunits_dir
    assert x_culture.culture_id == new_x_culture_id

    # Undo change to directory
    # x_func_delete_dir(dir=old_culture_dir)
    # print(f"{old_culture_dir=}")
    x_func_delete_dir(dir=new_culture_dir)
    print(f"{new_culture_dir=}")


def test_copy_evaluation_culture_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create culture
    old_x_culture_id = get_temp_env_culture_id()
    old_culture_dir = f"src/culture/examples/cultures/{old_x_culture_id}"
    old_culture_file_name = "culture.json"
    old_culture_file_path = f"{old_culture_dir}/{old_culture_file_name}"
    old_agendas_dir = f"{old_culture_dir}/agendas"
    old_councilunits_dir = f"{old_culture_dir}/councilunits"

    x_culture = cultureunit_shop(old_x_culture_id, get_test_cultures_dir())
    x_culture.create_dirs_if_null()

    assert os_path.exists(old_culture_dir)
    assert os_path.isdir(old_culture_dir)
    assert os_path.exists(old_culture_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_councilunits_dir)
    assert x_culture.get_public_dir() == old_agendas_dir
    assert x_culture.get_councilunits_dir() == old_councilunits_dir

    new_x_culture_id = "ex_env1"
    new_culture_dir = f"src/culture/examples/cultures/{new_x_culture_id}"
    new_culture_file_name = "culture.json"
    new_culture_file_path = f"{new_culture_dir}/{new_culture_file_name}"
    new_agendas_dir = f"{new_culture_dir}/agendas"
    new_councilunits_dir = f"{new_culture_dir}/councilunits"

    assert os_path.exists(new_culture_dir) is False
    assert os_path.isdir(new_culture_dir) is False
    assert os_path.exists(new_culture_file_path) is False
    assert os_path.exists(new_agendas_dir) is False
    assert os_path.exists(new_councilunits_dir) is False
    assert x_culture.get_public_dir() != new_agendas_dir
    assert x_culture.get_councilunits_dir() != new_councilunits_dir
    assert x_culture.culture_id != new_x_culture_id

    # WHEN
    copy_evaluation_culture(
        src_culture_id=x_culture.culture_id, dest_culture_id=new_x_culture_id
    )

    # THEN check agendas src directory created
    assert os_path.exists(old_culture_dir)
    assert os_path.isdir(old_culture_dir)
    assert os_path.exists(old_culture_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_councilunits_dir)
    assert x_culture.get_public_dir() == old_agendas_dir
    assert x_culture.get_councilunits_dir() == old_councilunits_dir

    assert os_path.exists(new_culture_dir)
    assert os_path.isdir(new_culture_dir)
    assert os_path.exists(new_culture_file_path)
    assert os_path.exists(new_agendas_dir)
    assert os_path.exists(new_councilunits_dir)
    assert x_culture.get_public_dir() != new_agendas_dir
    assert x_culture.get_councilunits_dir() != new_councilunits_dir
    assert x_culture.culture_id != new_x_culture_id

    # Undo change to directory
    # x_func_delete_dir(x_culture.get_object_root_dir())
    # x_func_delete_dir(dir=old_culture_dir)
    x_func_delete_dir(dir=new_culture_dir)


def test_copy_evaluation_culture_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create culture
    old_x_culture_id = get_temp_env_culture_id()
    x_culture = cultureunit_shop(old_x_culture_id, get_test_cultures_dir())
    x_culture.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_culture(
            src_culture_id=x_culture.culture_id, dest_culture_id=old_x_culture_id
        )
    assert (
        str(excinfo.value)
        == f"Cannot copy culture to '{x_culture.get_object_root_dir()}' directory because '{x_culture.get_object_root_dir()}' exists."
    )


def test_cultureunit_set_manager_pid_CorrectsSetsData(env_dir_setup_cleanup):
    # GIVEN
    x_culture_id = get_temp_env_culture_id()
    x_culture = cultureunit_shop(x_culture_id, cultures_dir=get_test_cultures_dir())
    assert x_culture.culture_id == x_culture_id
    assert x_culture._manager_pid is None

    # WHEN
    zuo_text = "Zuo"
    x_culture.set_manager_pid(zuo_text)

    # THEN
    assert x_culture._manager_pid == zuo_text


def test_cultureunit_get_road_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_culture_id = get_temp_env_culture_id()
    x_culture = cultureunit_shop(x_culture_id, cultures_dir=get_test_cultures_dir())
    healer_text = "healer"
    healer_road_with_woot = get_road(x_culture.culture_id, healer_text)
    healer_road_wo_root = healer_text
    healer_list_wo_root = get_all_road_nodes(healer_road_wo_root)
    bloomers_text = "bloomers"
    bloomers_road_with_root = get_road(healer_road_with_woot, bloomers_text)
    bloomers_road_wo_root = get_road(healer_road_wo_root, bloomers_text)
    bloomers_list_wo_root = get_all_road_nodes(bloomers_road_wo_root)
    roses_text = "roses"
    roses_road_with_root = get_road(bloomers_road_with_root, roses_text)
    roses_road_wo_root = get_road(bloomers_road_wo_root, roses_text)
    roses_list_wo_root = get_all_road_nodes(roses_road_wo_root)

    # WHEN / THEN
    assert x_culture.culture_id == x_culture.build_culture_road()
    assert healer_road_with_woot == x_culture.build_culture_road(healer_road_wo_root)
    assert bloomers_road_with_root == x_culture.build_culture_road(
        bloomers_road_wo_root
    )
    assert roses_road_with_root == x_culture.build_culture_road(roses_road_wo_root)
