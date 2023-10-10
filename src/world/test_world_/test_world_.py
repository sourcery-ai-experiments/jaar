# from src.economy.economy import EconomyUnit, economyunit_shop
# from src.contract.x_func import delete_dir as x_func_delete_dir
# from os import path as os_path
# from src.economy.examples.economy_env_kit import (
#     get_temp_env_mark,
#     get_test_economys_dir,
#     rename_example_economy,
#     copy_evaluation_economy,
#     env_dir_setup_cleanup,
# )
# from pytest import raises as pytest_raises
from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import get_test_worlds_dir
from src.world.person import personunit_shop


def test_worldunit_exists():
    dallas_text = "dallas"
    wx = WorldUnit(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert wx.mark == dallas_text
    assert wx.worlds_dir == get_test_worlds_dir()
    assert wx._persons_dir is None


def test_worldunit_shop_ReturnsWorldUnit():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())

    # THEN
    assert wx.mark == dallas_text
    assert wx.worlds_dir == get_test_worlds_dir()
    assert wx._persons_obj == {}


def test_worldunit__set_world_dirs_SetsPersonDir():
    # GIVEN
    dallas_text = "dallas"
    wx = WorldUnit(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert wx._persons_dir is None

    # WHEN
    wx._set_world_dirs()

    # THEN
    assert wx._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert wx._persons_dir == f"{get_test_worlds_dir()}/{dallas_text}/persons"


def test_worldunit_shop_SetsWorldsDirs():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())

    # THEN
    assert wx.mark == dallas_text
    assert wx._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert wx._persons_dir == f"{wx._world_dir}/persons"


def test_worldunit__set_person_in_memory_CorrectlySetsPerson():
    # GIVEN
    dallas_text = "dallas"
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert wx._persons_obj == {}

    # WHEN
    luca_text = "Luca"
    luca_person = personunit_shop(name=luca_text)
    wx._set_person_in_memory(personunit=luca_person)

    # THEN
    assert wx._persons_obj != {}
    assert len(wx._persons_obj) == 1
    assert wx._persons_obj[luca_text] == luca_person
    assert wx._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert wx._persons_dir == f"{wx._world_dir}/persons"


def test_worldunit__create_person_from_name_CorrectlySetsPerson():
    # GIVEN
    dallas_text = "dallas"
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{wx._persons_dir},{luca_text}"
    luca_person_obj = personunit_shop(name=luca_text, person_dir=luca_person_dir)

    # WHEN
    wx._create_person_from_name(luca_text)

    # THEN
    assert wx._persons_obj[luca_text] != None
    assert wx._persons_obj[luca_text].person_dir == luca_person_dir
    assert wx._persons_obj[luca_text] == luca_person_obj


def test_worldunit_get_personunit_from_memory_CorrectlyReturnsPerson():
    # GIVEN
    dallas_text = "dallas"
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{wx._persons_dir},{luca_text}"
    luca_person_obj = personunit_shop(name=luca_text, person_dir=luca_person_dir)
    wx._create_person_from_name(luca_text)

    # WHEN
    luca_gotten_obj = wx.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj != None
    assert luca_gotten_obj.person_dir == luca_person_dir
    assert luca_gotten_obj == luca_person_obj


def test_worldunit_get_personunit_from_memory_CorrectlyReturnsNone():
    # GIVEN
    dallas_text = "dallas"
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"

    # WHEN
    luca_gotten_obj = wx.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj is None


# def test_world_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
#     # GIVEN create world
#     dallas_text = get_temp_env_mark()
#     wx = EconomyUnit(mark=dallas_text, worlds_dir=get_test_economys_dir())
#     print(f"{get_test_economys_dir()=} {wx.economys_dir=}")
#     # x_func_delete_dir(wx.get_object_root_dir())
#     print(f"delete {wx.get_object_root_dir()=}")
#     economy_dir = f"src/economy/examples/economys/{economy_mark}"
#     economy_file_title = "economy.json"
#     economy_file_path = f"{economy_dir}/{economy_file_title}"
#     contracts_dir = f"{economy_dir}/contracts"
#     owners_dir = f"{economy_dir}/owners"
#     bank_file_title = "bank.db"
#     bank_file_path = f"{economy_dir}/{bank_file_title}"

#     assert os_path.exists(economy_dir) is False
#     assert os_path.isdir(economy_dir) is False
#     assert os_path.exists(economy_file_path) is False
#     assert os_path.exists(contracts_dir) is False
#     assert os_path.exists(owners_dir) is False
#     assert os_path.exists(bank_file_path) is False

#     # WHEN
#     wx.create_dirs_if_null(in_memory_bank=False)

#     # THEN check contracts src directory created
#     assert os_path.exists(economy_dir)
#     assert os_path.isdir(economy_dir)
#     assert os_path.exists(economy_file_path)
#     assert os_path.exists(contracts_dir)
#     assert os_path.exists(owners_dir)
#     assert os_path.exists(bank_file_path)
#     assert wx.get_object_root_dir() == economy_dir
#     assert wx.get_public_dir() == contracts_dir
#     assert wx.get_owners_dir() == owners_dir
#     assert wx.get_bank_db_path() == bank_file_path


# def test_rename_example_economy_CorrectlyRenamesDirAndFiles(env_dir_setup_cleanup):
#     # GIVEN create economy
#     old_economy_mark = get_temp_env_mark()
#     old_economy_dir = f"src/economy/examples/economys/{old_economy_mark}"
#     old_economy_file_title = "economy.json"
#     old_economy_file_path = f"{old_economy_dir}/{old_economy_file_title}"
#     old_contracts_dir = f"{old_economy_dir}/contracts"
#     old_owners_dir = f"{old_economy_dir}/owners"

#     new_economy_mark = "ex_env1"
#     new_economy_dir = f"src/economy/examples/economys/{new_economy_mark}"
#     new_economy_file_title = "economy.json"
#     new_economy_file_path = f"{new_economy_dir}/{new_economy_file_title}"
#     new_contracts_dir = f"{new_economy_dir}/contracts"
#     new_owners_dir = f"{new_economy_dir}/owners"
#     x_func_delete_dir(dir=new_economy_dir)
#     print(f"{new_economy_dir=}")

#     wx = economyunit_shop(mark=old_economy_mark, economys_dir=get_test_economys_dir())
#     # x_func_delete_dir(wx.get_object_root_dir())
#     # print(f"{wx.get_object_root_dir()=}")

#     wx.create_dirs_if_null(in_memory_bank=True)

#     assert os_path.exists(old_economy_dir)
#     assert os_path.isdir(old_economy_dir)
#     assert os_path.exists(old_economy_file_path)
#     assert os_path.exists(old_contracts_dir)
#     assert os_path.exists(old_owners_dir)
#     assert wx.get_public_dir() == old_contracts_dir
#     assert wx.get_owners_dir() == old_owners_dir

#     assert os_path.exists(new_economy_dir) is False
#     assert os_path.isdir(new_economy_dir) is False
#     assert os_path.exists(new_economy_file_path) is False
#     assert os_path.exists(new_contracts_dir) is False
#     assert os_path.exists(new_owners_dir) is False
#     assert wx.get_public_dir() != new_contracts_dir
#     assert wx.get_owners_dir() != new_owners_dir
#     assert wx.mark != new_economy_mark

#     # WHEN
#     rename_example_economy(economy_obj=wx, new_title=new_economy_mark)

#     # THEN check contracts src directory created
#     assert os_path.exists(old_economy_dir) is False
#     assert os_path.isdir(old_economy_dir) is False
#     assert os_path.exists(old_economy_file_path) is False
#     assert os_path.exists(old_contracts_dir) is False
#     assert os_path.exists(old_owners_dir) is False
#     assert wx.get_public_dir() != old_contracts_dir
#     assert wx.get_owners_dir() != old_owners_dir

#     assert os_path.exists(new_economy_dir)
#     assert os_path.isdir(new_economy_dir)
#     assert os_path.exists(new_economy_file_path)
#     assert os_path.exists(new_contracts_dir)
#     assert os_path.exists(new_owners_dir)
#     assert wx.get_public_dir() == new_contracts_dir
#     assert wx.get_owners_dir() == new_owners_dir
#     assert wx.mark == new_economy_mark

#     # Undo change to directory
#     # x_func_delete_dir(dir=old_economy_dir)
#     # print(f"{old_economy_dir=}")
#     x_func_delete_dir(dir=new_economy_dir)
#     print(f"{new_economy_dir=}")


# def test_copy_evaluation_economy_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
#     # GIVEN create economy
#     old_economy_mark = get_temp_env_mark()
#     old_economy_dir = f"src/economy/examples/economys/{old_economy_mark}"
#     old_economy_file_title = "economy.json"
#     old_economy_file_path = f"{old_economy_dir}/{old_economy_file_title}"
#     old_contracts_dir = f"{old_economy_dir}/contracts"
#     old_owners_dir = f"{old_economy_dir}/owners"

#     wx = economyunit_shop(mark=old_economy_mark, economys_dir=get_test_economys_dir())
#     wx.create_dirs_if_null()

#     assert os_path.exists(old_economy_dir)
#     assert os_path.isdir(old_economy_dir)
#     assert os_path.exists(old_economy_file_path)
#     assert os_path.exists(old_contracts_dir)
#     assert os_path.exists(old_owners_dir)
#     assert wx.get_public_dir() == old_contracts_dir
#     assert wx.get_owners_dir() == old_owners_dir

#     new_economy_mark = "ex_env1"
#     new_economy_dir = f"src/economy/examples/economys/{new_economy_mark}"
#     new_economy_file_title = "economy.json"
#     new_economy_file_path = f"{new_economy_dir}/{new_economy_file_title}"
#     new_contracts_dir = f"{new_economy_dir}/contracts"
#     new_owners_dir = f"{new_economy_dir}/owners"

#     assert os_path.exists(new_economy_dir) is False
#     assert os_path.isdir(new_economy_dir) is False
#     assert os_path.exists(new_economy_file_path) is False
#     assert os_path.exists(new_contracts_dir) is False
#     assert os_path.exists(new_owners_dir) is False
#     assert wx.get_public_dir() != new_contracts_dir
#     assert wx.get_owners_dir() != new_owners_dir
#     assert wx.mark != new_economy_mark

#     # WHEN
#     copy_evaluation_economy(src_mark=wx.mark, dest_mark=new_economy_mark)

#     # THEN check contracts src directory created
#     assert os_path.exists(old_economy_dir)
#     assert os_path.isdir(old_economy_dir)
#     assert os_path.exists(old_economy_file_path)
#     assert os_path.exists(old_contracts_dir)
#     assert os_path.exists(old_owners_dir)
#     assert wx.get_public_dir() == old_contracts_dir
#     assert wx.get_owners_dir() == old_owners_dir

#     assert os_path.exists(new_economy_dir)
#     assert os_path.isdir(new_economy_dir)
#     assert os_path.exists(new_economy_file_path)
#     assert os_path.exists(new_contracts_dir)
#     assert os_path.exists(new_owners_dir)
#     assert wx.get_public_dir() != new_contracts_dir
#     assert wx.get_owners_dir() != new_owners_dir
#     assert wx.mark != new_economy_mark

#     # Undo change to directory
#     # x_func_delete_dir(wx.get_object_root_dir())
#     # x_func_delete_dir(dir=old_economy_dir)
#     x_func_delete_dir(dir=new_economy_dir)


# def test_copy_evaluation_economy_CorrectlyRaisesError(env_dir_setup_cleanup):
#     # GIVEN create economy
#     old_economy_mark = get_temp_env_mark()
#     wx = economyunit_shop(mark=old_economy_mark, economys_dir=get_test_economys_dir())
#     wx.create_dirs_if_null()

#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         copy_evaluation_economy(src_mark=wx.mark, dest_mark=old_economy_mark)
#     assert (
#         str(excinfo.value)
#         == f"Cannot copy economy to '{wx.get_object_root_dir()}' directory because '{wx.get_object_root_dir()}' exists."
#     )


# def test_economyunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
#     # GIVEN
#     park_text = get_temp_env_mark()
#     economy_dir = f"src/economy/examples/economys/{park_text}"
#     assert os_path.exists(economy_dir) is False

#     # WHEN
#     wx = economyunit_shop(mark=park_text, economys_dir=get_test_economys_dir())

#     # THEN
#     assert wx != None
#     assert wx.mark == park_text
#     assert os_path.exists(economy_dir)
#     assert wx._bank_db != None
