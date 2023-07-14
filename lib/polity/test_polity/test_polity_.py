from lib.polity.polity import PolityUnit
from lib.agent.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from lib.polity.examples.env_tools import (
    get_temp_env_name,
    get_test_politys_dir,
    rename_test_polity,
    copy_test_polity,
    env_dir_setup_cleanup,
)


def test_polity_exists():
    polity_name = "test1"
    ex = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    assert ex.name == polity_name
    assert ex.politys_dir == get_test_politys_dir()


def test_polity_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create polity
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    print(f"{get_test_politys_dir()=} {e1.politys_dir=}")
    # x_func_delete_dir(e1.get_object_root_dir())
    print(f"delete {e1.get_object_root_dir()=}")
    polity_dir = f"lib/polity/examples/politys/{polity_name}"
    polity_file_name = "polity.json"
    polity_file_path = f"{polity_dir}/{polity_file_name}"
    agents_dir = f"{polity_dir}/agents"
    persons_dir = f"{polity_dir}/persons"
    bank_file_name = "bank.db"
    bank_file_path = f"{polity_dir}/{bank_file_name}"

    assert os_path.exists(polity_dir) is False
    assert os_path.isdir(polity_dir) is False
    assert os_path.exists(polity_file_path) is False
    assert os_path.exists(agents_dir) is False
    assert os_path.exists(persons_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    e1.create_dirs_if_null(in_memory_bank=False)

    # THEN confirm agents src directory created
    assert os_path.exists(polity_dir)
    assert os_path.isdir(polity_dir)
    assert os_path.exists(polity_file_path)
    assert os_path.exists(agents_dir)
    assert os_path.exists(persons_dir)
    assert os_path.exists(bank_file_path)
    assert e1.get_object_root_dir() == polity_dir
    assert e1.get_agents_dir() == agents_dir
    assert e1.get_persons_dir() == persons_dir
    assert e1.get_bank_db_path() == bank_file_path


def test_rename_test_polity_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create polity
    old_polity_name = get_temp_env_name()
    old_polity_dir = f"lib/polity/examples/politys/{old_polity_name}"
    old_polity_file_name = "polity.json"
    old_polity_file_path = f"{old_polity_dir}/{old_polity_file_name}"
    old_agents_dir = f"{old_polity_dir}/agents"
    old_persons_dir = f"{old_polity_dir}/persons"

    new_polity_name = "ex_env1"
    new_polity_dir = f"lib/polity/examples/politys/{new_polity_name}"
    new_polity_file_name = "polity.json"
    new_polity_file_path = f"{new_polity_dir}/{new_polity_file_name}"
    new_agents_dir = f"{new_polity_dir}/agents"
    new_persons_dir = f"{new_polity_dir}/persons"
    x_func_delete_dir(dir=new_polity_dir)
    print(f"{new_polity_dir=}")

    e1 = PolityUnit(name=old_polity_name, politys_dir=get_test_politys_dir())
    # x_func_delete_dir(e1.get_object_root_dir())
    # print(f"{e1.get_object_root_dir()=}")

    e1.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_polity_dir)
    assert os_path.isdir(old_polity_dir)
    assert os_path.exists(old_polity_file_path)
    assert os_path.exists(old_agents_dir)
    assert os_path.exists(old_persons_dir)
    assert e1.get_agents_dir() == old_agents_dir
    assert e1.get_persons_dir() == old_persons_dir

    assert os_path.exists(new_polity_dir) is False
    assert os_path.isdir(new_polity_dir) is False
    assert os_path.exists(new_polity_file_path) is False
    assert os_path.exists(new_agents_dir) is False
    assert os_path.exists(new_persons_dir) is False
    assert e1.get_agents_dir() != new_agents_dir
    assert e1.get_persons_dir() != new_persons_dir
    assert e1.name != new_polity_name

    # WHEN
    rename_test_polity(polity_obj=e1, new_name=new_polity_name)

    # THEN confirm agents src directory created
    assert os_path.exists(old_polity_dir) is False
    assert os_path.isdir(old_polity_dir) is False
    assert os_path.exists(old_polity_file_path) is False
    assert os_path.exists(old_agents_dir) is False
    assert os_path.exists(old_persons_dir) is False
    assert e1.get_agents_dir() != old_agents_dir
    assert e1.get_persons_dir() != old_persons_dir

    assert os_path.exists(new_polity_dir)
    assert os_path.isdir(new_polity_dir)
    assert os_path.exists(new_polity_file_path)
    assert os_path.exists(new_agents_dir)
    assert os_path.exists(new_persons_dir)
    assert e1.get_agents_dir() == new_agents_dir
    assert e1.get_persons_dir() == new_persons_dir
    assert e1.name == new_polity_name

    # Undo change to directory
    # x_func_delete_dir(dir=old_polity_dir)
    # print(f"{old_polity_dir=}")
    x_func_delete_dir(dir=new_polity_dir)
    print(f"{new_polity_dir=}")


def test_copy_test_polity_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create polity
    old_polity_name = get_temp_env_name()
    old_polity_dir = f"lib/polity/examples/politys/{old_polity_name}"
    old_polity_file_name = "polity.json"
    old_polity_file_path = f"{old_polity_dir}/{old_polity_file_name}"
    old_agents_dir = f"{old_polity_dir}/agents"
    old_persons_dir = f"{old_polity_dir}/persons"

    e1 = PolityUnit(name=old_polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null()

    assert os_path.exists(old_polity_dir)
    assert os_path.isdir(old_polity_dir)
    assert os_path.exists(old_polity_file_path)
    assert os_path.exists(old_agents_dir)
    assert os_path.exists(old_persons_dir)
    assert e1.get_agents_dir() == old_agents_dir
    assert e1.get_persons_dir() == old_persons_dir

    new_polity_name = "ex_env1"
    new_polity_dir = f"lib/polity/examples/politys/{new_polity_name}"
    new_polity_file_name = "polity.json"
    new_polity_file_path = f"{new_polity_dir}/{new_polity_file_name}"
    new_agents_dir = f"{new_polity_dir}/agents"
    new_persons_dir = f"{new_polity_dir}/persons"

    assert os_path.exists(new_polity_dir) is False
    assert os_path.isdir(new_polity_dir) is False
    assert os_path.exists(new_polity_file_path) is False
    assert os_path.exists(new_agents_dir) is False
    assert os_path.exists(new_persons_dir) is False
    assert e1.get_agents_dir() != new_agents_dir
    assert e1.get_persons_dir() != new_persons_dir
    assert e1.name != new_polity_name

    # WHEN
    copy_test_polity(src_name=e1.name, dest_name=new_polity_name)

    # THEN confirm agents src directory created
    assert os_path.exists(old_polity_dir)
    assert os_path.isdir(old_polity_dir)
    assert os_path.exists(old_polity_file_path)
    assert os_path.exists(old_agents_dir)
    assert os_path.exists(old_persons_dir)
    assert e1.get_agents_dir() == old_agents_dir
    assert e1.get_persons_dir() == old_persons_dir

    assert os_path.exists(new_polity_dir)
    assert os_path.isdir(new_polity_dir)
    assert os_path.exists(new_polity_file_path)
    assert os_path.exists(new_agents_dir)
    assert os_path.exists(new_persons_dir)
    assert e1.get_agents_dir() != new_agents_dir
    assert e1.get_persons_dir() != new_persons_dir
    assert e1.name != new_polity_name

    # Undo change to directory
    # x_func_delete_dir(e1.get_object_root_dir())
    # x_func_delete_dir(dir=old_polity_dir)
    x_func_delete_dir(dir=new_polity_dir)
