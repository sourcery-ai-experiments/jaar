from src.agenda.road import get_road_from_nodes, get_all_road_nodes, get_road
from src.agenda.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.culture.culture import CultureUnit, cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_qid,
    get_test_cultures_dir,
    reqid_example_culture,
    copy_evaluation_culture,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_culture_exists():
    # GIVEN
    x_qid = "test1"

    # WHEN
    x_culture = CultureUnit(qid=x_qid, cultures_dir=get_test_cultures_dir())

    # THEN
    assert x_culture.qid == x_qid
    assert x_culture.cultures_dir == get_test_cultures_dir()
    assert x_culture._manager_pid is None


def test_culture_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create culture
    x_qid = get_temp_env_qid()
    x_culture = CultureUnit(qid=x_qid, cultures_dir=get_test_cultures_dir())
    print(f"{get_test_cultures_dir()=} {x_culture.cultures_dir=}")
    # x_func_delete_dir(x_culture.get_object_root_dir())
    print(f"delete {x_culture.get_object_root_dir()=}")
    culture_dir = f"src/culture/examples/cultures/{x_qid}"
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


def test_reqid_example_culture_CorrectlyChangesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create culture
    old_x_qid = get_temp_env_qid()
    old_culture_dir = f"src/culture/examples/cultures/{old_x_qid}"
    old_culture_file_name = "culture.json"
    old_culture_file_path = f"{old_culture_dir}/{old_culture_file_name}"
    old_agendas_dir = f"{old_culture_dir}/agendas"
    old_councilunits_dir = f"{old_culture_dir}/councilunits"

    new_x_qid = "ex_env1"
    new_culture_dir = f"src/culture/examples/cultures/{new_x_qid}"
    new_culture_file_name = "culture.json"
    new_culture_file_path = f"{new_culture_dir}/{new_culture_file_name}"
    new_agendas_dir = f"{new_culture_dir}/agendas"
    new_councilunits_dir = f"{new_culture_dir}/councilunits"
    x_func_delete_dir(dir=new_culture_dir)
    print(f"{new_culture_dir=}")

    x_culture = cultureunit_shop(qid=old_x_qid, cultures_dir=get_test_cultures_dir())
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
    assert x_culture.qid != new_x_qid

    # WHEN
    reqid_example_culture(culture_obj=x_culture, new_qid=new_x_qid)

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
    assert x_culture.qid == new_x_qid

    # Undo change to directory
    # x_func_delete_dir(dir=old_culture_dir)
    # print(f"{old_culture_dir=}")
    x_func_delete_dir(dir=new_culture_dir)
    print(f"{new_culture_dir=}")


def test_copy_evaluation_culture_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create culture
    old_x_qid = get_temp_env_qid()
    old_culture_dir = f"src/culture/examples/cultures/{old_x_qid}"
    old_culture_file_name = "culture.json"
    old_culture_file_path = f"{old_culture_dir}/{old_culture_file_name}"
    old_agendas_dir = f"{old_culture_dir}/agendas"
    old_councilunits_dir = f"{old_culture_dir}/councilunits"

    x_culture = cultureunit_shop(old_x_qid, get_test_cultures_dir())
    x_culture.create_dirs_if_null()

    assert os_path.exists(old_culture_dir)
    assert os_path.isdir(old_culture_dir)
    assert os_path.exists(old_culture_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_councilunits_dir)
    assert x_culture.get_public_dir() == old_agendas_dir
    assert x_culture.get_councilunits_dir() == old_councilunits_dir

    new_x_qid = "ex_env1"
    new_culture_dir = f"src/culture/examples/cultures/{new_x_qid}"
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
    assert x_culture.qid != new_x_qid

    # WHEN
    copy_evaluation_culture(src_qid=x_culture.qid, dest_qid=new_x_qid)

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
    assert x_culture.qid != new_x_qid

    # Undo change to directory
    # x_func_delete_dir(x_culture.get_object_root_dir())
    # x_func_delete_dir(dir=old_culture_dir)
    x_func_delete_dir(dir=new_culture_dir)


def test_copy_evaluation_culture_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create culture
    old_x_qid = get_temp_env_qid()
    x_culture = cultureunit_shop(old_x_qid, get_test_cultures_dir())
    x_culture.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_culture(src_qid=x_culture.qid, dest_qid=old_x_qid)
    assert (
        str(excinfo.value)
        == f"Cannot copy culture to '{x_culture.get_object_root_dir()}' directory because '{x_culture.get_object_root_dir()}' exists."
    )


def test_cultureunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_qid = get_temp_env_qid()
    culture_dir = f"src/culture/examples/cultures/{x_qid}"
    sue_text = "Sue"
    assert os_path.exists(culture_dir) is False

    # WHEN
    x_culture = cultureunit_shop(
        qid=x_qid, cultures_dir=get_test_cultures_dir(), _manager_pid=sue_text
    )

    # THEN
    assert x_culture != None
    assert x_culture.qid == x_qid
    assert os_path.exists(culture_dir)
    assert x_culture._treasury_db != None
    assert x_culture._manager_pid == sue_text
    assert x_culture._councilunits == {}


def test_cultureunit_set_manager_pid_CorrectsSetsData(env_dir_setup_cleanup):
    # GIVEN
    x_qid = get_temp_env_qid()
    x_culture = cultureunit_shop(qid=x_qid, cultures_dir=get_test_cultures_dir())
    assert x_culture.qid == x_qid
    assert x_culture._manager_pid is None

    # WHEN
    zuo_text = "Zuo"
    x_culture.set_manager_pid(zuo_text)

    # THEN
    assert x_culture._manager_pid == zuo_text


def test_cultureunit_get_road_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_qid = get_temp_env_qid()
    x_culture = cultureunit_shop(qid=x_qid, cultures_dir=get_test_cultures_dir())
    healer_text = "healer"
    healer_road_with_woot = get_road(x_culture.qid, healer_text)
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
    assert x_culture.qid == x_culture.build_road()
    assert healer_road_with_woot == x_culture.build_road(healer_road_wo_root)
    assert bloomers_road_with_root == x_culture.build_road(bloomers_road_wo_root)
    assert roses_road_with_root == x_culture.build_road(roses_road_wo_root)
