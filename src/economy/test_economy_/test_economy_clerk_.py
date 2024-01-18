from src.economy.economy import economyunit_shop
from src.economy.clerk import clerkunit_shop
from src.economy.examples.economy_env_kit import (
    get_temp_env_dir,
    get_temp_env_economy_id,
    env_dir_setup_cleanup,
    get_test_economys_dir,
)
from os import path as os_path


def test_economyunit_set_healer_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    print(f"create env '{x_economy_id}' directories.")
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    timmy_text = "timmy"
    timmy_dir = f"{x_economy.get_clerkunits_dir()}/{timmy_text}"
    print(f"{timmy_dir=}")
    assert os_path.exists(timmy_dir) == False

    # WHEN
    x_economy.create_new_clerkunit(clerk_cid=timmy_text)

    # THEN
    print(f"{timmy_dir=}")
    assert os_path.exists(timmy_dir)


def test_economyunit_change_clerkunit_cid_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{x_economy.get_clerkunits_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/contract_agenda.json"
    bob_clerkunit = clerkunit_shop(
        old_bob_text, x_economy.get_object_root_dir(), get_temp_env_economy_id()
    )
    x_economy.set_clerkunit(bob_clerkunit)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{x_economy.get_clerkunits_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/contract_agenda.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_bob_clerkunit = x_economy.get_clerkunit(cid=old_bob_text)
    assert x_economy.get_clerkunit(cid=new_bob_text) is None
    assert old_bob_clerkunit._clerkunit_dir == old_bob_dir
    assert old_bob_clerkunit._clerkunit_dir != new_bob_dir

    # WHEN
    x_economy.change_clerkunit_cid(old_cid=old_bob_text, new_cid=new_bob_text)

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    assert x_economy.get_clerkunit(cid=old_bob_text) is None
    new_bob_clerkunit = x_economy.get_clerkunit(cid=new_bob_text)
    assert new_bob_clerkunit._clerkunit_dir != old_bob_dir
    assert new_bob_clerkunit._clerkunit_dir == new_bob_dir


def test_economyunit_del_clerkunit_dir_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    xia_text = "Xia"
    xia_dir = f"{x_economy.get_clerkunits_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/contract_agenda.json"
    x_economy.create_new_clerkunit(clerk_cid=xia_text)
    x_economy.save_clerkunit_file(clerk_cid=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    x_economy.del_clerkunit_dir(clerk_cid=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False


def test_economyunit_add_clerkunit_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    bob_text = "Bob"
    bob_dir = f"{x_economy.get_clerkunits_dir()}/{bob_text}"
    bob_file_path = f"{bob_dir}/contract_agenda.json"
    assert os_path.exists(bob_dir) == False
    assert os_path.exists(bob_file_path) == False
    assert x_economy.get_clerkunit(cid=bob_text) is None

    # WHEN
    x_economy.add_clerkunit(pid=bob_text)

    # THEN
    assert x_economy._clerkunits != {}
    print(f"{bob_file_path=}")
    bob_static_clerkunit = clerkunit_shop(
        pid=bob_text,
        env_dir=get_temp_env_dir(),
        economy_id=get_temp_env_economy_id(),
    )
    bob_gen_clerkunit = x_economy.get_clerkunit(bob_text)
    assert bob_gen_clerkunit._env_dir == bob_static_clerkunit._env_dir
    assert bob_gen_clerkunit._contract != None
    assert bob_static_clerkunit._contract != None
    assert bob_gen_clerkunit == bob_static_clerkunit
    print(f"{   bob_gen_clerkunit._contract._agent_id=}")
    print(f"{bob_static_clerkunit._contract._agent_id=}")
    assert bob_gen_clerkunit._contract == bob_static_clerkunit._contract
    assert os_path.exists(bob_dir)
    assert os_path.exists(bob_file_path)


def test_economyunit_clerkunit_exists_WorksCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_economy_id = get_temp_env_economy_id()
    x_economy = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    bob_text = "Bob"

    # WHEN / THEN
    assert x_economy.clerkunit_exists(cid=bob_text) == False

    # WHEN / THEN
    x_economy.add_clerkunit(pid=bob_text)
    assert x_economy.clerkunit_exists(cid=bob_text)
