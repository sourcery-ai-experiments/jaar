from src.world.world import WorldUnit
from src.agent.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.world.examples.env_tools import (
    get_temp_env_name,
    get_test_worlds_dir,
    rename_test_world,
    copy_test_world,
    env_dir_setup_cleanup,
)


def test_world_exists():
    world_name = "test1"
    ex = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    assert ex.name == world_name
    assert ex.worlds_dir == get_test_worlds_dir()


def test_world_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create world
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    print(f"{get_test_worlds_dir()=} {e1.worlds_dir=}")
    # x_func_delete_dir(e1.get_object_root_dir())
    print(f"delete {e1.get_object_root_dir()=}")
    world_dir = f"lib/world/examples/worlds/{world_name}"
    world_file_name = "world.json"
    world_file_path = f"{world_dir}/{world_file_name}"
    agents_dir = f"{world_dir}/agents"
    persons_dir = f"{world_dir}/persons"
    bank_file_name = "bank.db"
    bank_file_path = f"{world_dir}/{bank_file_name}"

    assert os_path.exists(world_dir) is False
    assert os_path.isdir(world_dir) is False
    assert os_path.exists(world_file_path) is False
    assert os_path.exists(agents_dir) is False
    assert os_path.exists(persons_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    e1.create_dirs_if_null(in_memory_bank=False)

    # THEN confirm agents src directory created
    assert os_path.exists(world_dir)
    assert os_path.isdir(world_dir)
    assert os_path.exists(world_file_path)
    assert os_path.exists(agents_dir)
    assert os_path.exists(persons_dir)
    assert os_path.exists(bank_file_path)
    assert e1.get_object_root_dir() == world_dir
    assert e1.get_agents_dir() == agents_dir
    assert e1.get_persons_dir() == persons_dir
    assert e1.get_bank_db_path() == bank_file_path


def test_rename_test_world_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create world
    old_world_name = get_temp_env_name()
    old_world_dir = f"lib/world/examples/worlds/{old_world_name}"
    old_world_file_name = "world.json"
    old_world_file_path = f"{old_world_dir}/{old_world_file_name}"
    old_agents_dir = f"{old_world_dir}/agents"
    old_persons_dir = f"{old_world_dir}/persons"

    new_world_name = "ex_env1"
    new_world_dir = f"lib/world/examples/worlds/{new_world_name}"
    new_world_file_name = "world.json"
    new_world_file_path = f"{new_world_dir}/{new_world_file_name}"
    new_agents_dir = f"{new_world_dir}/agents"
    new_persons_dir = f"{new_world_dir}/persons"
    x_func_delete_dir(dir=new_world_dir)
    print(f"{new_world_dir=}")

    e1 = WorldUnit(name=old_world_name, worlds_dir=get_test_worlds_dir())
    # x_func_delete_dir(e1.get_object_root_dir())
    # print(f"{e1.get_object_root_dir()=}")

    e1.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_world_dir)
    assert os_path.isdir(old_world_dir)
    assert os_path.exists(old_world_file_path)
    assert os_path.exists(old_agents_dir)
    assert os_path.exists(old_persons_dir)
    assert e1.get_agents_dir() == old_agents_dir
    assert e1.get_persons_dir() == old_persons_dir

    assert os_path.exists(new_world_dir) is False
    assert os_path.isdir(new_world_dir) is False
    assert os_path.exists(new_world_file_path) is False
    assert os_path.exists(new_agents_dir) is False
    assert os_path.exists(new_persons_dir) is False
    assert e1.get_agents_dir() != new_agents_dir
    assert e1.get_persons_dir() != new_persons_dir
    assert e1.name != new_world_name

    # WHEN
    rename_test_world(world_obj=e1, new_name=new_world_name)

    # THEN confirm agents src directory created
    assert os_path.exists(old_world_dir) is False
    assert os_path.isdir(old_world_dir) is False
    assert os_path.exists(old_world_file_path) is False
    assert os_path.exists(old_agents_dir) is False
    assert os_path.exists(old_persons_dir) is False
    assert e1.get_agents_dir() != old_agents_dir
    assert e1.get_persons_dir() != old_persons_dir

    assert os_path.exists(new_world_dir)
    assert os_path.isdir(new_world_dir)
    assert os_path.exists(new_world_file_path)
    assert os_path.exists(new_agents_dir)
    assert os_path.exists(new_persons_dir)
    assert e1.get_agents_dir() == new_agents_dir
    assert e1.get_persons_dir() == new_persons_dir
    assert e1.name == new_world_name

    # Undo change to directory
    # x_func_delete_dir(dir=old_world_dir)
    # print(f"{old_world_dir=}")
    x_func_delete_dir(dir=new_world_dir)
    print(f"{new_world_dir=}")


def test_copy_test_world_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create world
    old_world_name = get_temp_env_name()
    old_world_dir = f"lib/world/examples/worlds/{old_world_name}"
    old_world_file_name = "world.json"
    old_world_file_path = f"{old_world_dir}/{old_world_file_name}"
    old_agents_dir = f"{old_world_dir}/agents"
    old_persons_dir = f"{old_world_dir}/persons"

    e1 = WorldUnit(name=old_world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null()

    assert os_path.exists(old_world_dir)
    assert os_path.isdir(old_world_dir)
    assert os_path.exists(old_world_file_path)
    assert os_path.exists(old_agents_dir)
    assert os_path.exists(old_persons_dir)
    assert e1.get_agents_dir() == old_agents_dir
    assert e1.get_persons_dir() == old_persons_dir

    new_world_name = "ex_env1"
    new_world_dir = f"lib/world/examples/worlds/{new_world_name}"
    new_world_file_name = "world.json"
    new_world_file_path = f"{new_world_dir}/{new_world_file_name}"
    new_agents_dir = f"{new_world_dir}/agents"
    new_persons_dir = f"{new_world_dir}/persons"

    assert os_path.exists(new_world_dir) is False
    assert os_path.isdir(new_world_dir) is False
    assert os_path.exists(new_world_file_path) is False
    assert os_path.exists(new_agents_dir) is False
    assert os_path.exists(new_persons_dir) is False
    assert e1.get_agents_dir() != new_agents_dir
    assert e1.get_persons_dir() != new_persons_dir
    assert e1.name != new_world_name

    # WHEN
    copy_test_world(src_name=e1.name, dest_name=new_world_name)

    # THEN confirm agents src directory created
    assert os_path.exists(old_world_dir)
    assert os_path.isdir(old_world_dir)
    assert os_path.exists(old_world_file_path)
    assert os_path.exists(old_agents_dir)
    assert os_path.exists(old_persons_dir)
    assert e1.get_agents_dir() == old_agents_dir
    assert e1.get_persons_dir() == old_persons_dir

    assert os_path.exists(new_world_dir)
    assert os_path.isdir(new_world_dir)
    assert os_path.exists(new_world_file_path)
    assert os_path.exists(new_agents_dir)
    assert os_path.exists(new_persons_dir)
    assert e1.get_agents_dir() != new_agents_dir
    assert e1.get_persons_dir() != new_persons_dir
    assert e1.name != new_world_name

    # Undo change to directory
    # x_func_delete_dir(e1.get_object_root_dir())
    # x_func_delete_dir(dir=old_world_dir)
    x_func_delete_dir(dir=new_world_dir)
