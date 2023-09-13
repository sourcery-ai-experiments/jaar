from src.system.system import SystemUnit
from src.system.person import personunit_shop
from src.system.examples.system_env_kit import (
    get_temp_env_dir,
    get_temp_env_name,
    env_dir_setup_cleanup,
    get_test_systems_dir,
    create_person_file_for_systems,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_system_set_person_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    sx = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    print(f"create env '{system_name}' directories.")
    sx.create_dirs_if_null(in_memory_bank=True)
    timmy_text = "timmy"
    wx_path = f"{sx.get_persons_dir()}/{timmy_text}"
    print(f"{wx_path=}")
    assert os_path.exists(wx_path) == False

    # WHEN
    sx.create_new_personunit(person_name=timmy_text)

    # THEN
    print(f"{wx_path=}")
    assert os_path.exists(wx_path)


def test_system_load_personunit_RaisesErrorWhenPersonDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    system_name = get_temp_env_name()
    sx = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())

    # WHEN / THEN
    bobs_text = "bobs wurld"
    with pytest_raises(Exception) as excinfo:
        sx.load_personunit(name=bobs_text)
    assert (
        str(excinfo.value)
        == f"Could not load file {sx.get_persons_dir()}/{bobs_text}/isol_calendar.json (2, 'No such file or directory')"
    )


def test_system_env_kit_create_person_file_for_systems_WorksCorrectly(
    env_dir_setup_cleanup,
):
    # GIVEN
    system_name = get_temp_env_name()
    sx = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    sx.set_personunits_empty_if_null()
    bobs_text = "bobs wurld"
    create_person_file_for_systems(
        system_dir=sx.get_object_root_dir(), person_name=bobs_text
    )
    assert sx._personunits.get(bobs_text) is None

    # WHEN
    sx.load_personunit(name=bobs_text)

    # THEN
    assert sx._personunits.get(bobs_text) != None
    bobs_person = sx._personunits[bobs_text]
    assert bobs_person._admin._person_name == bobs_text


def test_system_rename_personunit_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    e5 = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{e5.get_persons_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/isol_calendar.json"
    wx5_obj = personunit_shop(name=old_bob_text, env_dir=e5.get_object_root_dir())
    e5.set_personunits_empty_if_null()
    e5.set_personunit_to_system(person=wx5_obj)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{e5.get_persons_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/isol_calendar.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_person_x = e5.sys_get_person_obj(name=old_bob_text)
    assert e5.sys_get_person_obj(name=new_bob_text) is None
    assert old_person_x._admin._person_dir == old_bob_dir
    assert old_person_x._admin._person_dir != new_bob_dir

    # WHEN
    e5.rename_personunit(old_name=old_bob_text, new_name=new_bob_text)

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    # assert e5.get_calendar_obj_from_file(name=old_bob_text) is None
    assert e5.sys_get_person_obj(name=old_bob_text) is None
    new_person_x = e5.sys_get_person_obj(name=new_bob_text)
    assert new_person_x._admin._person_dir != old_bob_dir
    assert new_person_x._admin._person_dir == new_bob_dir


def test_system_del_person_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    sx = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    xia_text = "Xia"
    xia_dir = f"{sx.get_persons_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/isol_calendar.json"
    sx.create_new_personunit(person_name=xia_text)
    sx.save_person_file(person_name=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    sx.del_person_dir(person_name=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False
