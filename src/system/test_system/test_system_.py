from src.system.system import SystemUnit
from src.agent.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.system.examples.env_kit import (
    get_temp_env_name,
    get_test_systems_dir,
    rename_example_system,
    copy_test_system,
    env_dir_setup_cleanup,
)


def test_system_exists():
    system_name = "test1"
    ex = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    assert ex.name == system_name
    assert ex.systems_dir == get_test_systems_dir()


def test_system_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create system
    system_name = get_temp_env_name()
    e1 = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    print(f"{get_test_systems_dir()=} {e1.systems_dir=}")
    # x_func_delete_dir(e1.get_object_root_dir())
    print(f"delete {e1.get_object_root_dir()=}")
    system_dir = f"src/system/examples/systems/{system_name}"
    system_file_name = "system.json"
    system_file_path = f"{system_dir}/{system_file_name}"
    agents_dir = f"{system_dir}/agents"
    persons_dir = f"{system_dir}/persons"
    bank_file_name = "bank.db"
    bank_file_path = f"{system_dir}/{bank_file_name}"

    assert os_path.exists(system_dir) is False
    assert os_path.isdir(system_dir) is False
    assert os_path.exists(system_file_path) is False
    assert os_path.exists(agents_dir) is False
    assert os_path.exists(persons_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    e1.create_dirs_if_null(in_memory_bank=False)

    # THEN confirm agents src directory created
    assert os_path.exists(system_dir)
    assert os_path.isdir(system_dir)
    assert os_path.exists(system_file_path)
    assert os_path.exists(agents_dir)
    assert os_path.exists(persons_dir)
    assert os_path.exists(bank_file_path)
    assert e1.get_object_root_dir() == system_dir
    assert e1.get_agents_dir() == agents_dir
    assert e1.get_persons_dir() == persons_dir
    assert e1.get_bank_db_path() == bank_file_path


def test_rename_example_system_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create system
    old_system_name = get_temp_env_name()
    old_system_dir = f"src/system/examples/systems/{old_system_name}"
    old_system_file_name = "system.json"
    old_system_file_path = f"{old_system_dir}/{old_system_file_name}"
    old_agents_dir = f"{old_system_dir}/agents"
    old_persons_dir = f"{old_system_dir}/persons"

    new_system_name = "ex_env1"
    new_system_dir = f"src/system/examples/systems/{new_system_name}"
    new_system_file_name = "system.json"
    new_system_file_path = f"{new_system_dir}/{new_system_file_name}"
    new_agents_dir = f"{new_system_dir}/agents"
    new_persons_dir = f"{new_system_dir}/persons"
    x_func_delete_dir(dir=new_system_dir)
    print(f"{new_system_dir=}")

    e1 = SystemUnit(name=old_system_name, systems_dir=get_test_systems_dir())
    # x_func_delete_dir(e1.get_object_root_dir())
    # print(f"{e1.get_object_root_dir()=}")

    e1.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_system_dir)
    assert os_path.isdir(old_system_dir)
    assert os_path.exists(old_system_file_path)
    assert os_path.exists(old_agents_dir)
    assert os_path.exists(old_persons_dir)
    assert e1.get_agents_dir() == old_agents_dir
    assert e1.get_persons_dir() == old_persons_dir

    assert os_path.exists(new_system_dir) is False
    assert os_path.isdir(new_system_dir) is False
    assert os_path.exists(new_system_file_path) is False
    assert os_path.exists(new_agents_dir) is False
    assert os_path.exists(new_persons_dir) is False
    assert e1.get_agents_dir() != new_agents_dir
    assert e1.get_persons_dir() != new_persons_dir
    assert e1.name != new_system_name

    # WHEN
    rename_example_system(system_obj=e1, new_name=new_system_name)

    # THEN confirm agents src directory created
    assert os_path.exists(old_system_dir) is False
    assert os_path.isdir(old_system_dir) is False
    assert os_path.exists(old_system_file_path) is False
    assert os_path.exists(old_agents_dir) is False
    assert os_path.exists(old_persons_dir) is False
    assert e1.get_agents_dir() != old_agents_dir
    assert e1.get_persons_dir() != old_persons_dir

    assert os_path.exists(new_system_dir)
    assert os_path.isdir(new_system_dir)
    assert os_path.exists(new_system_file_path)
    assert os_path.exists(new_agents_dir)
    assert os_path.exists(new_persons_dir)
    assert e1.get_agents_dir() == new_agents_dir
    assert e1.get_persons_dir() == new_persons_dir
    assert e1.name == new_system_name

    # Undo change to directory
    # x_func_delete_dir(dir=old_system_dir)
    # print(f"{old_system_dir=}")
    x_func_delete_dir(dir=new_system_dir)
    print(f"{new_system_dir=}")


def test_copy_test_system_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create system
    old_system_name = get_temp_env_name()
    old_system_dir = f"src/system/examples/systems/{old_system_name}"
    old_system_file_name = "system.json"
    old_system_file_path = f"{old_system_dir}/{old_system_file_name}"
    old_agents_dir = f"{old_system_dir}/agents"
    old_persons_dir = f"{old_system_dir}/persons"

    e1 = SystemUnit(name=old_system_name, systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null()

    assert os_path.exists(old_system_dir)
    assert os_path.isdir(old_system_dir)
    assert os_path.exists(old_system_file_path)
    assert os_path.exists(old_agents_dir)
    assert os_path.exists(old_persons_dir)
    assert e1.get_agents_dir() == old_agents_dir
    assert e1.get_persons_dir() == old_persons_dir

    new_system_name = "ex_env1"
    new_system_dir = f"src/system/examples/systems/{new_system_name}"
    new_system_file_name = "system.json"
    new_system_file_path = f"{new_system_dir}/{new_system_file_name}"
    new_agents_dir = f"{new_system_dir}/agents"
    new_persons_dir = f"{new_system_dir}/persons"

    assert os_path.exists(new_system_dir) is False
    assert os_path.isdir(new_system_dir) is False
    assert os_path.exists(new_system_file_path) is False
    assert os_path.exists(new_agents_dir) is False
    assert os_path.exists(new_persons_dir) is False
    assert e1.get_agents_dir() != new_agents_dir
    assert e1.get_persons_dir() != new_persons_dir
    assert e1.name != new_system_name

    # WHEN
    copy_test_system(src_name=e1.name, dest_name=new_system_name)

    # THEN confirm agents src directory created
    assert os_path.exists(old_system_dir)
    assert os_path.isdir(old_system_dir)
    assert os_path.exists(old_system_file_path)
    assert os_path.exists(old_agents_dir)
    assert os_path.exists(old_persons_dir)
    assert e1.get_agents_dir() == old_agents_dir
    assert e1.get_persons_dir() == old_persons_dir

    assert os_path.exists(new_system_dir)
    assert os_path.isdir(new_system_dir)
    assert os_path.exists(new_system_file_path)
    assert os_path.exists(new_agents_dir)
    assert os_path.exists(new_persons_dir)
    assert e1.get_agents_dir() != new_agents_dir
    assert e1.get_persons_dir() != new_persons_dir
    assert e1.name != new_system_name

    # Undo change to directory
    # x_func_delete_dir(e1.get_object_root_dir())
    # x_func_delete_dir(dir=old_system_dir)
    x_func_delete_dir(dir=new_system_dir)
