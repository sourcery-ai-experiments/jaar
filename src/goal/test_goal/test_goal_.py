from src.contract.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.goal.goal import GoalUnit, goalunit_shop
from src.goal.examples.goal_env_kit import (
    get_temp_env_tag,
    get_test_goals_dir,
    rename_example_goal,
    copy_evaluation_goal,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_goal_exists():
    goal_tag = "test1"
    sx = GoalUnit(tag=goal_tag, goals_dir=get_test_goals_dir())
    assert sx.tag == goal_tag
    assert sx.goals_dir == get_test_goals_dir()


def test_goal_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create goal
    goal_tag = get_temp_env_tag()
    sx = GoalUnit(tag=goal_tag, goals_dir=get_test_goals_dir())
    print(f"{get_test_goals_dir()=} {sx.goals_dir=}")
    # x_func_delete_dir(sx.get_object_root_dir())
    print(f"delete {sx.get_object_root_dir()=}")
    goal_dir = f"src/goal/examples/goals/{goal_tag}"
    goal_file_title = "goal.json"
    goal_file_path = f"{goal_dir}/{goal_file_title}"
    contracts_dir = f"{goal_dir}/contracts"
    owners_dir = f"{goal_dir}/owners"
    bank_file_title = "bank.db"
    bank_file_path = f"{goal_dir}/{bank_file_title}"

    assert os_path.exists(goal_dir) is False
    assert os_path.isdir(goal_dir) is False
    assert os_path.exists(goal_file_path) is False
    assert os_path.exists(contracts_dir) is False
    assert os_path.exists(owners_dir) is False
    assert os_path.exists(bank_file_path) is False

    # WHEN
    sx.create_dirs_if_null(in_memory_bank=False)

    # THEN check contracts src directory created
    assert os_path.exists(goal_dir)
    assert os_path.isdir(goal_dir)
    assert os_path.exists(goal_file_path)
    assert os_path.exists(contracts_dir)
    assert os_path.exists(owners_dir)
    assert os_path.exists(bank_file_path)
    assert sx.get_object_root_dir() == goal_dir
    assert sx.get_public_dir() == contracts_dir
    assert sx.get_owners_dir() == owners_dir
    assert sx.get_bank_db_path() == bank_file_path


def test_rename_example_goal_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create goal
    old_goal_tag = get_temp_env_tag()
    old_goal_dir = f"src/goal/examples/goals/{old_goal_tag}"
    old_goal_file_title = "goal.json"
    old_goal_file_path = f"{old_goal_dir}/{old_goal_file_title}"
    old_contracts_dir = f"{old_goal_dir}/contracts"
    old_owners_dir = f"{old_goal_dir}/owners"

    new_goal_tag = "ex_env1"
    new_goal_dir = f"src/goal/examples/goals/{new_goal_tag}"
    new_goal_file_title = "goal.json"
    new_goal_file_path = f"{new_goal_dir}/{new_goal_file_title}"
    new_contracts_dir = f"{new_goal_dir}/contracts"
    new_owners_dir = f"{new_goal_dir}/owners"
    x_func_delete_dir(dir=new_goal_dir)
    print(f"{new_goal_dir=}")

    sx = goalunit_shop(tag=old_goal_tag, goals_dir=get_test_goals_dir())
    # x_func_delete_dir(sx.get_object_root_dir())
    # print(f"{sx.get_object_root_dir()=}")

    sx.create_dirs_if_null(in_memory_bank=True)

    assert os_path.exists(old_goal_dir)
    assert os_path.isdir(old_goal_dir)
    assert os_path.exists(old_goal_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_owners_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_owners_dir() == old_owners_dir

    assert os_path.exists(new_goal_dir) is False
    assert os_path.isdir(new_goal_dir) is False
    assert os_path.exists(new_goal_file_path) is False
    assert os_path.exists(new_contracts_dir) is False
    assert os_path.exists(new_owners_dir) is False
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_owners_dir() != new_owners_dir
    assert sx.tag != new_goal_tag

    # WHEN
    rename_example_goal(goal_obj=sx, new_title=new_goal_tag)

    # THEN check contracts src directory created
    assert os_path.exists(old_goal_dir) is False
    assert os_path.isdir(old_goal_dir) is False
    assert os_path.exists(old_goal_file_path) is False
    assert os_path.exists(old_contracts_dir) is False
    assert os_path.exists(old_owners_dir) is False
    assert sx.get_public_dir() != old_contracts_dir
    assert sx.get_owners_dir() != old_owners_dir

    assert os_path.exists(new_goal_dir)
    assert os_path.isdir(new_goal_dir)
    assert os_path.exists(new_goal_file_path)
    assert os_path.exists(new_contracts_dir)
    assert os_path.exists(new_owners_dir)
    assert sx.get_public_dir() == new_contracts_dir
    assert sx.get_owners_dir() == new_owners_dir
    assert sx.tag == new_goal_tag

    # Undo change to directory
    # x_func_delete_dir(dir=old_goal_dir)
    # print(f"{old_goal_dir=}")
    x_func_delete_dir(dir=new_goal_dir)
    print(f"{new_goal_dir=}")


def test_copy_evaluation_goal_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create goal
    old_goal_tag = get_temp_env_tag()
    old_goal_dir = f"src/goal/examples/goals/{old_goal_tag}"
    old_goal_file_title = "goal.json"
    old_goal_file_path = f"{old_goal_dir}/{old_goal_file_title}"
    old_contracts_dir = f"{old_goal_dir}/contracts"
    old_owners_dir = f"{old_goal_dir}/owners"

    sx = goalunit_shop(tag=old_goal_tag, goals_dir=get_test_goals_dir())
    sx.create_dirs_if_null()

    assert os_path.exists(old_goal_dir)
    assert os_path.isdir(old_goal_dir)
    assert os_path.exists(old_goal_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_owners_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_owners_dir() == old_owners_dir

    new_goal_tag = "ex_env1"
    new_goal_dir = f"src/goal/examples/goals/{new_goal_tag}"
    new_goal_file_title = "goal.json"
    new_goal_file_path = f"{new_goal_dir}/{new_goal_file_title}"
    new_contracts_dir = f"{new_goal_dir}/contracts"
    new_owners_dir = f"{new_goal_dir}/owners"

    assert os_path.exists(new_goal_dir) is False
    assert os_path.isdir(new_goal_dir) is False
    assert os_path.exists(new_goal_file_path) is False
    assert os_path.exists(new_contracts_dir) is False
    assert os_path.exists(new_owners_dir) is False
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_owners_dir() != new_owners_dir
    assert sx.tag != new_goal_tag

    # WHEN
    copy_evaluation_goal(src_tag=sx.tag, dest_tag=new_goal_tag)

    # THEN check contracts src directory created
    assert os_path.exists(old_goal_dir)
    assert os_path.isdir(old_goal_dir)
    assert os_path.exists(old_goal_file_path)
    assert os_path.exists(old_contracts_dir)
    assert os_path.exists(old_owners_dir)
    assert sx.get_public_dir() == old_contracts_dir
    assert sx.get_owners_dir() == old_owners_dir

    assert os_path.exists(new_goal_dir)
    assert os_path.isdir(new_goal_dir)
    assert os_path.exists(new_goal_file_path)
    assert os_path.exists(new_contracts_dir)
    assert os_path.exists(new_owners_dir)
    assert sx.get_public_dir() != new_contracts_dir
    assert sx.get_owners_dir() != new_owners_dir
    assert sx.tag != new_goal_tag

    # Undo change to directory
    # x_func_delete_dir(sx.get_object_root_dir())
    # x_func_delete_dir(dir=old_goal_dir)
    x_func_delete_dir(dir=new_goal_dir)


def test_copy_evaluation_goal_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create goal
    old_goal_tag = get_temp_env_tag()
    sx = goalunit_shop(tag=old_goal_tag, goals_dir=get_test_goals_dir())
    sx.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_goal(src_tag=sx.tag, dest_tag=old_goal_tag)
    assert (
        str(excinfo.value)
        == f"Cannot copy goal to '{sx.get_object_root_dir()}' directory because '{sx.get_object_root_dir()}' exists."
    )


def test_goalunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    park_text = get_temp_env_tag()
    goal_dir = f"src/goal/examples/goals/{park_text}"
    assert os_path.exists(goal_dir) is False

    # WHEN
    sx = goalunit_shop(tag=park_text, goals_dir=get_test_goals_dir())

    # THEN
    assert sx != None
    assert sx.tag == park_text
    assert os_path.exists(goal_dir)
    assert sx._bank_db != None
