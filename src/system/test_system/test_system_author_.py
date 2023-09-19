from src.system.system import systemunit_shop
from src.system.author import authorunit_shop
from src.system.examples.system_env_kit import (
    get_temp_env_dir,
    get_temp_env_name,
    env_dir_setup_cleanup,
    get_test_systems_dir,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_system_set_author_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    print(f"create env '{system_name}' directories.")
    sx.create_dirs_if_null(in_memory_bank=True)
    timmy_text = "timmy"
    wx_path = f"{sx.get_authors_dir()}/{timmy_text}"
    print(f"{wx_path=}")
    assert os_path.exists(wx_path) == False

    # WHEN
    sx.create_new_authorunit(author_name=timmy_text)

    # THEN
    print(f"{wx_path=}")
    assert os_path.exists(wx_path)


def test_system_create_authorunit_from_public_RaisesErrorWhenAuthorDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())

    # WHEN / THEN
    bobs_text = "bobs wurld"
    with pytest_raises(Exception) as excinfo:
        sx.create_authorunit_from_public(name=bobs_text)
    assert (
        str(excinfo.value)
        == f"Could not load file {sx.get_public_dir()}/{bobs_text}.json (2, 'No such file or directory')"
    )


def test_system_rename_authorunit_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    e5 = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{e5.get_authors_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/isol_calendar.json"
    wx5_obj = authorunit_shop(name=old_bob_text, env_dir=e5.get_object_root_dir())
    e5.set_authorunits_empty_if_null()
    e5.set_authorunit_to_system(author=wx5_obj)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{e5.get_authors_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/isol_calendar.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_author_x = e5.get_author_obj(name=old_bob_text)
    assert e5.get_author_obj(name=new_bob_text) is None
    assert old_author_x._admin._author_dir == old_bob_dir
    assert old_author_x._admin._author_dir != new_bob_dir

    # WHEN
    e5.rename_authorunit(old_name=old_bob_text, new_name=new_bob_text)

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    assert e5.get_author_obj(name=old_bob_text) is None
    new_author_x = e5.get_author_obj(name=new_bob_text)
    assert new_author_x._admin._author_dir != old_bob_dir
    assert new_author_x._admin._author_dir == new_bob_dir


def test_system_del_author_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    sx = systemunit_shop(name=system_name, systems_dir=get_test_systems_dir())
    xia_text = "Xia"
    xia_dir = f"{sx.get_authors_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/isol_calendar.json"
    sx.create_new_authorunit(author_name=xia_text)
    sx.save_author_file(author_name=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    sx.del_author_dir(author_name=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False
