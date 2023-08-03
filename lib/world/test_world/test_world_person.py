from lib.world.world import WorldUnit
from lib.world.person import personunit_shop
from lib.world.examples.env_tools import (
    get_temp_env_dir,
    get_temp_env_name,
    env_dir_setup_cleanup,
    get_test_worlds_dir,
    create_person_file_for_worlds,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_world_set_person_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    print(f"create env '{world_name}' directories.")
    e1.create_dirs_if_null(in_memory_bank=True)
    timmy_text = "timmy"
    wx_path = f"{e1.get_persons_dir()}/{timmy_text}"
    print(f"{wx_path=}")
    assert os_path.exists(wx_path) == False

    # WHEN
    e1.create_new_personunit(person_name=timmy_text)

    # THEN
    print(f"{wx_path=}")
    assert os_path.exists(wx_path)


def test_world_load_personunit_RaisesErrorWhenPersonDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())

    # WHEN / THEN
    bobs_text = "bobs wurld"
    with pytest_raises(Exception) as excinfo:
        e1.load_personunit(name=bobs_text)
    assert (
        str(excinfo.value)
        == f"Could not load file {e1.get_persons_dir()}/{bobs_text}/{bobs_text}.json (2, 'No such file or directory')"
    )


def test_world_env_tools_create_person_file_for_worlds_WorksCorrectly(
    env_dir_setup_cleanup,
):
    # GIVEN
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.set_personunits_empty_if_null()
    bobs_text = "bobs wurld"
    create_person_file_for_worlds(
        world_dir=e1.get_object_root_dir(), person_name=bobs_text
    )
    assert e1._personunits.get(bobs_text) is None

    # WHEN
    e1.load_personunit(name=bobs_text)

    # THEN
    assert e1._personunits.get(bobs_text) != None
    bobs_person = e1._personunits[bobs_text]
    assert bobs_person.name == bobs_text


def test_world_rename_personunit_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    world_name = get_temp_env_name()
    e5 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_person_name = "old1"
    old_wx_dir = f"{e5.get_persons_dir()}/{old_person_name}"
    old_wx_file_path = f"{old_wx_dir}/{old_person_name}.json"
    wx5_obj = personunit_shop(name=old_person_name, env_dir=e5.get_object_root_dir())
    e5.set_personunits_empty_if_null()
    e5.set_personunit_to_world(person=wx5_obj)
    print(f"{old_wx_dir=}")

    new_person_name = "new1"
    new_wx_dir = f"{e5.get_persons_dir()}/{new_person_name}"
    new_wx_file_path = f"{new_wx_dir}/{new_person_name}.json"
    assert os_path.exists(new_wx_dir) == False
    assert os_path.exists(old_wx_dir)
    assert os_path.exists(new_wx_file_path) == False
    assert os_path.exists(old_wx_file_path)
    old_person_x = e5.get_person_obj_from_world(name=old_person_name)
    assert e5.get_person_obj_from_world(name=new_person_name) is None
    assert old_person_x._person_dir == old_wx_dir
    assert old_person_x._person_dir != new_wx_dir

    # WHEN
    e5.rename_personunit(old_name=old_person_name, new_name=new_person_name)

    # THEN
    assert os_path.exists(new_wx_dir)
    assert os_path.exists(old_wx_dir) == False
    print(f"{new_wx_file_path=}")
    assert os_path.exists(new_wx_file_path)
    assert os_path.exists(old_wx_file_path) == False
    # assert e5.get_person_obj_from_file(name=old_person_name) is None
    assert e5.get_person_obj_from_world(name=old_person_name) is None
    new_person_x = e5.get_person_obj_from_world(name=new_person_name)
    assert new_person_x._person_dir != old_wx_dir
    assert new_person_x._person_dir == new_wx_dir


def test_world_del_person_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    wx_name = "test_person1"
    wx_dir = f"{e1.get_persons_dir()}/{wx_name}"
    wx_file_path = f"{wx_dir}/{wx_name}.json"
    e1.create_new_personunit(person_name=wx_name)
    e1.save_person_file(person_name=wx_name)
    print(f"{wx_file_path=}")
    assert os_path.exists(wx_dir)
    assert os_path.exists(wx_file_path)

    # WHEN
    e1.del_person_dir(person_name=wx_name)

    # THEN
    assert os_path.exists(wx_file_path) == False
    assert os_path.exists(wx_dir) == False
