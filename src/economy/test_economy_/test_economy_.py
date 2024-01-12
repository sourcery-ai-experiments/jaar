from src._prime.road import (
    get_all_road_nodes,
    default_road_delimiter_if_none,
    create_road,
)
from src.tools.file import delete_dir
from os import path as os_path
from src.economy.economy import EconomyUnit, economyunit_shop
from src.economy.examples.economy_env_kit import (
    get_temp_env_economy_id,
    get_test_economys_dir,
    change_economy_id_example_economy,
    copy_evaluation_economy,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_EconomyUnit_exists():
    # GIVEN
    x_economy_id = "test1"

    # WHEN
    x_economy = EconomyUnit(x_economy_id, economys_dir=get_test_economys_dir())

    # THEN
    assert x_economy.economy_id == x_economy_id
    assert x_economy.economys_dir == get_test_economys_dir()
    assert x_economy._manager_pid is None
    assert x_economy._road_delimiter is None


def test_economyunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    economy_dir = f"src/economy/examples/economys/{x_economy_id}"
    sue_text = "Sue"
    assert os_path.exists(economy_dir) is False

    # WHEN
    x_economy = economyunit_shop(
        x_economy_id, get_test_economys_dir(), _manager_pid=sue_text
    )

    # THEN
    assert x_economy != None
    assert x_economy.economy_id == x_economy_id
    assert os_path.exists(economy_dir)
    assert x_economy._treasury_db != None
    assert x_economy._manager_pid == sue_text
    assert x_economy._clerkunits == {}
    assert x_economy._road_delimiter == default_road_delimiter_if_none()


def test_EconomyUnit_set_road_delimiter_CorrectSetsAttribute(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    economy_dir = f"src/economy/examples/economys/{x_economy_id}"
    sue_text = "Sue"
    x_economy = economyunit_shop(
        x_economy_id, get_test_economys_dir(), _manager_pid=sue_text
    )
    assert x_economy._road_delimiter == default_road_delimiter_if_none()

    # WHEN
    slash_text = "/"
    x_economy.set_road_delimiter(slash_text)

    # THEN
    assert x_economy._road_delimiter == slash_text


def test_economyunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    economy_dir = f"src/economy/examples/economys/{x_economy_id}"
    sue_text = "Sue"
    assert os_path.exists(economy_dir) is False

    # WHEN
    x_economy = economyunit_shop(
        x_economy_id,
        economys_dir=get_test_economys_dir(),
        _manager_pid=sue_text,
    )

    # THEN
    assert x_economy != None
    assert x_economy.economy_id == x_economy_id
    assert os_path.exists(economy_dir)
    assert x_economy._treasury_db != None
    assert x_economy._manager_pid == sue_text
    assert x_economy._clerkunits == {}
    assert x_economy._road_delimiter == default_road_delimiter_if_none()


def test_economy_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create economy
    x_economy_id = get_temp_env_economy_id()
    x_economy = EconomyUnit(x_economy_id, economys_dir=get_test_economys_dir())
    print(f"{get_test_economys_dir()=} {x_economy.economys_dir=}")
    # delete_dir(x_economy.get_object_root_dir())
    print(f"delete {x_economy.get_object_root_dir()=}")
    economy_dir = f"src/economy/examples/economys/{x_economy_id}"
    economy_file_name = "economy.json"
    economy_file_path = f"{economy_dir}/{economy_file_name}"
    agendas_dir = f"{economy_dir}/agendas"
    clerkunits_dir = f"{economy_dir}/clerkunits"
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{economy_dir}/{treasury_file_name}"

    assert os_path.exists(economy_dir) is False
    assert os_path.isdir(economy_dir) is False
    assert os_path.exists(economy_file_path) is False
    assert os_path.exists(agendas_dir) is False
    assert os_path.exists(clerkunits_dir) is False
    assert os_path.exists(treasury_file_path) is False

    # WHEN
    x_economy.create_dirs_if_null(in_memory_treasury=False)

    # THEN check agendas src directory created
    assert os_path.exists(economy_dir)
    assert os_path.isdir(economy_dir)
    assert os_path.exists(economy_file_path)
    assert os_path.exists(agendas_dir)
    assert os_path.exists(clerkunits_dir)
    assert os_path.exists(treasury_file_path)
    assert x_economy.get_object_root_dir() == economy_dir
    assert x_economy.get_public_dir() == agendas_dir
    assert x_economy.get_clerkunits_dir() == clerkunits_dir
    assert x_economy.get_treasury_db_path() == treasury_file_path


def test_change_economy_id_example_economy_CorrectlyChangesDirAndFiles(
    env_dir_setup_cleanup,
):
    # GIVEN create economy
    old_x_economy_id = get_temp_env_economy_id()
    old_economy_dir = f"src/economy/examples/economys/{old_x_economy_id}"
    old_economy_file_name = "economy.json"
    old_economy_file_path = f"{old_economy_dir}/{old_economy_file_name}"
    old_agendas_dir = f"{old_economy_dir}/agendas"
    old_clerkunits_dir = f"{old_economy_dir}/clerkunits"

    new_x_economy_id = "ex_env1"
    new_economy_dir = f"src/economy/examples/economys/{new_x_economy_id}"
    new_economy_file_name = "economy.json"
    new_economy_file_path = f"{new_economy_dir}/{new_economy_file_name}"
    new_agendas_dir = f"{new_economy_dir}/agendas"
    new_clerkunits_dir = f"{new_economy_dir}/clerkunits"
    delete_dir(dir=new_economy_dir)
    print(f"{new_economy_dir=}")

    x_economy = economyunit_shop(
        economy_id=old_x_economy_id, economys_dir=get_test_economys_dir()
    )
    # delete_dir(x_economy.get_object_root_dir())
    # print(f"{x_economy.get_object_root_dir()=}")

    x_economy.create_dirs_if_null(in_memory_treasury=True)

    assert os_path.exists(old_economy_dir)
    assert os_path.isdir(old_economy_dir)
    assert os_path.exists(old_economy_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_economy.get_public_dir() == old_agendas_dir
    assert x_economy.get_clerkunits_dir() == old_clerkunits_dir

    assert os_path.exists(new_economy_dir) is False
    assert os_path.isdir(new_economy_dir) is False
    assert os_path.exists(new_economy_file_path) is False
    assert os_path.exists(new_agendas_dir) is False
    assert os_path.exists(new_clerkunits_dir) is False
    assert x_economy.get_public_dir() != new_agendas_dir
    assert x_economy.get_clerkunits_dir() != new_clerkunits_dir
    assert x_economy.economy_id != new_x_economy_id

    # WHEN
    change_economy_id_example_economy(
        economy_obj=x_economy, new_economy_id=new_x_economy_id
    )

    # THEN check agendas src directory created
    assert os_path.exists(old_economy_dir) is False
    assert os_path.isdir(old_economy_dir) is False
    assert os_path.exists(old_economy_file_path) is False
    assert os_path.exists(old_agendas_dir) is False
    assert os_path.exists(old_clerkunits_dir) is False
    assert x_economy.get_public_dir() != old_agendas_dir
    assert x_economy.get_clerkunits_dir() != old_clerkunits_dir

    assert os_path.exists(new_economy_dir)
    assert os_path.isdir(new_economy_dir)
    assert os_path.exists(new_economy_file_path)
    assert os_path.exists(new_agendas_dir)
    assert os_path.exists(new_clerkunits_dir)
    assert x_economy.get_public_dir() == new_agendas_dir
    assert x_economy.get_clerkunits_dir() == new_clerkunits_dir
    assert x_economy.economy_id == new_x_economy_id

    # Undo change to directory
    # delete_dir(dir=old_economy_dir)
    # print(f"{old_economy_dir=}")
    delete_dir(dir=new_economy_dir)
    print(f"{new_economy_dir=}")


def test_copy_evaluation_economy_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create economy
    old_x_economy_id = get_temp_env_economy_id()
    old_economy_dir = f"src/economy/examples/economys/{old_x_economy_id}"
    old_economy_file_name = "economy.json"
    old_economy_file_path = f"{old_economy_dir}/{old_economy_file_name}"
    old_agendas_dir = f"{old_economy_dir}/agendas"
    old_clerkunits_dir = f"{old_economy_dir}/clerkunits"

    x_economy = economyunit_shop(old_x_economy_id, get_test_economys_dir())
    x_economy.create_dirs_if_null()

    assert os_path.exists(old_economy_dir)
    assert os_path.isdir(old_economy_dir)
    assert os_path.exists(old_economy_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_economy.get_public_dir() == old_agendas_dir
    assert x_economy.get_clerkunits_dir() == old_clerkunits_dir

    new_x_economy_id = "ex_env1"
    new_economy_dir = f"src/economy/examples/economys/{new_x_economy_id}"
    new_economy_file_name = "economy.json"
    new_economy_file_path = f"{new_economy_dir}/{new_economy_file_name}"
    new_agendas_dir = f"{new_economy_dir}/agendas"
    new_clerkunits_dir = f"{new_economy_dir}/clerkunits"

    assert os_path.exists(new_economy_dir) is False
    assert os_path.isdir(new_economy_dir) is False
    assert os_path.exists(new_economy_file_path) is False
    assert os_path.exists(new_agendas_dir) is False
    assert os_path.exists(new_clerkunits_dir) is False
    assert x_economy.get_public_dir() != new_agendas_dir
    assert x_economy.get_clerkunits_dir() != new_clerkunits_dir
    assert x_economy.economy_id != new_x_economy_id

    # WHEN
    copy_evaluation_economy(
        src_economy_id=x_economy.economy_id, dest_economy_id=new_x_economy_id
    )

    # THEN check agendas src directory created
    assert os_path.exists(old_economy_dir)
    assert os_path.isdir(old_economy_dir)
    assert os_path.exists(old_economy_file_path)
    assert os_path.exists(old_agendas_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_economy.get_public_dir() == old_agendas_dir
    assert x_economy.get_clerkunits_dir() == old_clerkunits_dir

    assert os_path.exists(new_economy_dir)
    assert os_path.isdir(new_economy_dir)
    assert os_path.exists(new_economy_file_path)
    assert os_path.exists(new_agendas_dir)
    assert os_path.exists(new_clerkunits_dir)
    assert x_economy.get_public_dir() != new_agendas_dir
    assert x_economy.get_clerkunits_dir() != new_clerkunits_dir
    assert x_economy.economy_id != new_x_economy_id

    # Undo change to directory
    # delete_dir(x_economy.get_object_root_dir())
    # delete_dir(dir=old_economy_dir)
    delete_dir(dir=new_economy_dir)


def test_copy_evaluation_economy_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create economy
    old_x_economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(old_x_economy_id, get_test_economys_dir())
    x_economy.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_economy(
            src_economy_id=x_economy.economy_id, dest_economy_id=old_x_economy_id
        )
    assert (
        str(excinfo.value)
        == f"Cannot copy economy to '{x_economy.get_object_root_dir()}' directory because '{x_economy.get_object_root_dir()}' exists."
    )


def test_economyunit_set_manager_pid_CorrectsSetsData(env_dir_setup_cleanup):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    assert x_economy.economy_id == x_economy_id
    assert x_economy._manager_pid is None

    # WHEN
    zuo_text = "Zuo"
    x_economy.set_manager_pid(zuo_text)

    # THEN
    assert x_economy._manager_pid == zuo_text


def test_economyunit_get_road_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    healer_text = "healer"
    healer_road_with_woot = create_road(x_economy.economy_id, healer_text)
    healer_road_wo_root = healer_text
    # healer_list_wo_root = get_all_road_nodes(healer_road_wo_root)
    bloomers_text = "bloomers"
    bloomers_road_with_root = create_road(healer_road_with_woot, bloomers_text)
    bloomers_road_wo_root = create_road(healer_road_wo_root, bloomers_text)
    # bloomers_list_wo_root = get_all_road_nodes(bloomers_road_wo_root)
    roses_text = "roses"
    roses_road_with_root = create_road(bloomers_road_with_root, roses_text)
    roses_road_wo_root = create_road(bloomers_road_wo_root, roses_text)
    # roses_list_wo_root = get_all_road_nodes(roses_road_wo_root)

    # WHEN / THEN
    assert x_economy.economy_id == x_economy.build_economy_road()
    assert healer_road_with_woot == x_economy.build_economy_road(healer_road_wo_root)
    assert bloomers_road_with_root == x_economy.build_economy_road(
        bloomers_road_wo_root
    )
    assert roses_road_with_root == x_economy.build_economy_road(roses_road_wo_root)
