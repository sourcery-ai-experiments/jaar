from src.economy.economy import economyunit_shop
from src.economy.actor import actorunit_shop
from src.economy.examples.economy_env_kit import (
    get_temp_env_dir,
    get_temp_env_name,
    env_dir_setup_cleanup,
    get_test_economys_dir,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_economy_set_actor_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    economy_name = get_temp_env_name()
    sx = economyunit_shop(name=economy_name, economys_dir=get_test_economys_dir())
    print(f"create env '{economy_name}' directories.")
    sx.create_dirs_if_null(in_memory_bank=True)
    timmy_text = "timmy"
    wx_path = f"{sx.get_actors_dir()}/{timmy_text}"
    print(f"{wx_path=}")
    assert os_path.exists(wx_path) == False

    # WHEN
    sx.create_new_actorunit(actor_name=timmy_text)

    # THEN
    print(f"{wx_path=}")
    assert os_path.exists(wx_path)


def test_economy_create_actorunit_from_public_RaisesErrorWhenActorDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    economy_name = get_temp_env_name()
    sx = economyunit_shop(name=economy_name, economys_dir=get_test_economys_dir())

    # WHEN / THEN
    bobs_text = "bobs wurld"
    with pytest_raises(Exception) as excinfo:
        sx.create_actorunit_from_public(name=bobs_text)
    assert (
        str(excinfo.value)
        == f"Could not load file {sx.get_public_dir()}/{bobs_text}.json (2, 'No such file or directory')"
    )


def test_economy_rename_actorunit_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    economy_name = get_temp_env_name()
    e5 = economyunit_shop(name=economy_name, economys_dir=get_test_economys_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{e5.get_actors_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/isol_calendar.json"
    wx5_obj = actorunit_shop(name=old_bob_text, env_dir=e5.get_object_root_dir())
    e5.set_actorunits_empty_if_null()
    e5.set_actorunit_to_economy(actor=wx5_obj)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{e5.get_actors_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/isol_calendar.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_actor_x = e5.get_actor_obj(name=old_bob_text)
    assert e5.get_actor_obj(name=new_bob_text) is None
    assert old_actor_x._admin._actor_dir == old_bob_dir
    assert old_actor_x._admin._actor_dir != new_bob_dir

    # WHEN
    e5.rename_actorunit(old_name=old_bob_text, new_name=new_bob_text)

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    assert e5.get_actor_obj(name=old_bob_text) is None
    new_actor_x = e5.get_actor_obj(name=new_bob_text)
    assert new_actor_x._admin._actor_dir != old_bob_dir
    assert new_actor_x._admin._actor_dir == new_bob_dir


def test_economy_del_actor_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    economy_name = get_temp_env_name()
    sx = economyunit_shop(name=economy_name, economys_dir=get_test_economys_dir())
    xia_text = "Xia"
    xia_dir = f"{sx.get_actors_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/isol_calendar.json"
    sx.create_new_actorunit(actor_name=xia_text)
    sx.save_actor_file(actor_name=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    sx.del_actor_dir(actor_name=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False
