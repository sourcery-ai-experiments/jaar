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
from src.world.person import PersonUnit, personunit_shop


def test_personunit_exists():
    # GIVEN / WHEN
    px = PersonUnit()

    # THEN
    assert px.name is None
    assert px.person_dir is None
    assert px._economys is None


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    px = personunit_shop(name=dallas_text)

    # THEN
    assert px.name == dallas_text
    assert px.person_dir == ""
    assert px._economys == {}


def test_personunit_shop_ReturnsPersonUnitWithCorrectAttrs_v2():
    # GIVEN
    dallas_text = "dallas"
    dallas_dir = ""

    # WHEN
    px = personunit_shop(name=dallas_text, person_dir=dallas_dir)

    # THEN
    assert px.name == dallas_text
    assert px.person_dir == dallas_dir


def test_personunit_create_economy_CorrectlyCreatesAnEconomyUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    home_text = "home"
    xao_person_obj.create_economy(home_text)

    # THEN
    # home_economy = xao_person.get_economy()
    home_economy = xao_person_obj._economys.get(home_text)
    assert home_economy != None
    assert home_economy.tag == home_text
    assert home_economy.economys_dir == f"{xao_person_dir}/economys"


def test_personunit_get_economy_obj_CorrectlyGetsAnEconomyUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    home_text = "home"
    xao_person_obj.create_economy(home_text)

    # WHEN
    home_economy = xao_person_obj.get_economy_obj(home_text)

    # THEN
    assert home_economy != None
    assert home_economy.tag == home_text
    assert home_economy.economys_dir == f"{xao_person_dir}/economys"


# def test_personunit__set_persondir_SetsPersonDir():
#     # GIVEN
#     dallas_text = "dallas"
#     px = PersonUnit(mark=dallas_text, _persons_dir=get_test__persons_dir())
#     assert px._persons_dir is None

#     # WHEN
#     px._set_person_dirs()

#     # THEN
#     assert px._persons_dir == f"{get_test__persons_dir()}/persons"


# def test_personunit_shop_SetsPersonsDirs():
#     # GIVEN
#     dallas_text = "dallas"

#     # WHEN
#     px = personunit_shop(mark=dallas_text, _persons_dir=get_test__persons_dir())

#     # THEN
#     assert px.mark == dallas_text
#     assert px._persons_dir == f"{get_test__persons_dir()}/persons"


# def test_person_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
#     # GIVEN create person
#     dallas_text = get_temp_env_mark()
#     px = EconomyUnit(mark=dallas_text, _persons_dir=get_test_economys_dir())
#     print(f"{get_test_economys_dir()=} {px.economys_dir=}")
#     # x_func_delete_dir(px.get_object_root_dir())
#     print(f"delete {px.get_object_root_dir()=}")
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
#     px.create_dirs_if_null(in_memory_bank=False)

#     # THEN check contracts src directory created
#     assert os_path.exists(economy_dir)
#     assert os_path.isdir(economy_dir)
#     assert os_path.exists(economy_file_path)
#     assert os_path.exists(contracts_dir)
#     assert os_path.exists(owners_dir)
#     assert os_path.exists(bank_file_path)
#     assert px.get_object_root_dir() == economy_dir
#     assert px.get_public_dir() == contracts_dir
#     assert px.get_owners_dir() == owners_dir
#     assert px.get_bank_db_path() == bank_file_path


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

#     px = economyunit_shop(mark=old_economy_mark, economys_dir=get_test_economys_dir())
#     # x_func_delete_dir(px.get_object_root_dir())
#     # print(f"{px.get_object_root_dir()=}")

#     px.create_dirs_if_null(in_memory_bank=True)

#     assert os_path.exists(old_economy_dir)
#     assert os_path.isdir(old_economy_dir)
#     assert os_path.exists(old_economy_file_path)
#     assert os_path.exists(old_contracts_dir)
#     assert os_path.exists(old_owners_dir)
#     assert px.get_public_dir() == old_contracts_dir
#     assert px.get_owners_dir() == old_owners_dir

#     assert os_path.exists(new_economy_dir) is False
#     assert os_path.isdir(new_economy_dir) is False
#     assert os_path.exists(new_economy_file_path) is False
#     assert os_path.exists(new_contracts_dir) is False
#     assert os_path.exists(new_owners_dir) is False
#     assert px.get_public_dir() != new_contracts_dir
#     assert px.get_owners_dir() != new_owners_dir
#     assert px.mark != new_economy_mark

#     # WHEN
#     rename_example_economy(economy_obj=px, new_title=new_economy_mark)

#     # THEN check contracts src directory created
#     assert os_path.exists(old_economy_dir) is False
#     assert os_path.isdir(old_economy_dir) is False
#     assert os_path.exists(old_economy_file_path) is False
#     assert os_path.exists(old_contracts_dir) is False
#     assert os_path.exists(old_owners_dir) is False
#     assert px.get_public_dir() != old_contracts_dir
#     assert px.get_owners_dir() != old_owners_dir

#     assert os_path.exists(new_economy_dir)
#     assert os_path.isdir(new_economy_dir)
#     assert os_path.exists(new_economy_file_path)
#     assert os_path.exists(new_contracts_dir)
#     assert os_path.exists(new_owners_dir)
#     assert px.get_public_dir() == new_contracts_dir
#     assert px.get_owners_dir() == new_owners_dir
#     assert px.mark == new_economy_mark

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

#     px = economyunit_shop(mark=old_economy_mark, economys_dir=get_test_economys_dir())
#     px.create_dirs_if_null()

#     assert os_path.exists(old_economy_dir)
#     assert os_path.isdir(old_economy_dir)
#     assert os_path.exists(old_economy_file_path)
#     assert os_path.exists(old_contracts_dir)
#     assert os_path.exists(old_owners_dir)
#     assert px.get_public_dir() == old_contracts_dir
#     assert px.get_owners_dir() == old_owners_dir

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
#     assert px.get_public_dir() != new_contracts_dir
#     assert px.get_owners_dir() != new_owners_dir
#     assert px.mark != new_economy_mark

#     # WHEN
#     copy_evaluation_economy(src_mark=px.mark, dest_mark=new_economy_mark)

#     # THEN check contracts src directory created
#     assert os_path.exists(old_economy_dir)
#     assert os_path.isdir(old_economy_dir)
#     assert os_path.exists(old_economy_file_path)
#     assert os_path.exists(old_contracts_dir)
#     assert os_path.exists(old_owners_dir)
#     assert px.get_public_dir() == old_contracts_dir
#     assert px.get_owners_dir() == old_owners_dir

#     assert os_path.exists(new_economy_dir)
#     assert os_path.isdir(new_economy_dir)
#     assert os_path.exists(new_economy_file_path)
#     assert os_path.exists(new_contracts_dir)
#     assert os_path.exists(new_owners_dir)
#     assert px.get_public_dir() != new_contracts_dir
#     assert px.get_owners_dir() != new_owners_dir
#     assert px.mark != new_economy_mark

#     # Undo change to directory
#     # x_func_delete_dir(px.get_object_root_dir())
#     # x_func_delete_dir(dir=old_economy_dir)
#     x_func_delete_dir(dir=new_economy_dir)


# def test_copy_evaluation_economy_CorrectlyRaisesError(env_dir_setup_cleanup):
#     # GIVEN create economy
#     old_economy_mark = get_temp_env_mark()
#     px = economyunit_shop(mark=old_economy_mark, economys_dir=get_test_economys_dir())
#     px.create_dirs_if_null()

#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         copy_evaluation_economy(src_mark=px.mark, dest_mark=old_economy_mark)
#     assert (
#         str(excinfo.value)
#         == f"Cannot copy economy to '{px.get_object_root_dir()}' directory because '{px.get_object_root_dir()}' exists."
#     )


# def test_economyunit_shop_CorrectlyReturnsObj(env_dir_setup_cleanup):
#     # GIVEN
#     park_text = get_temp_env_mark()
#     economy_dir = f"src/economy/examples/economys/{park_text}"
#     assert os_path.exists(economy_dir) is False

#     # WHEN
#     px = economyunit_shop(mark=park_text, economys_dir=get_test_economys_dir())

#     # THEN
#     assert px != None
#     assert px.mark == park_text
#     assert os_path.exists(economy_dir)
#     assert px._bank_db != None
