from src.econ.econ import econunit_shop
from src.econ.clerk import clerkunit_shop
from src.econ.examples.econ_env_kit import (
    get_test_econ_dir,
    get_temp_env_econ_id,
    env_dir_setup_cleanup,
    get_test_econ_dir,
)
from os import path as os_path


def test_EconUnit_create_new_clerkunit_SetsAttrCorrecty(env_dir_setup_cleanup):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(x_econ_id, econ_dir=get_test_econ_dir())
    print(f"create env '{x_econ_id}' directories.")
    x_econ.set_econ_dirs(in_memory_treasury=True)
    timmy_text = "timmy"
    timmy_dir = f"{x_econ.get_clerkunits_dir()}/{timmy_text}"
    print(f"{timmy_dir=}")
    assert os_path.exists(timmy_dir) == False

    # WHEN
    x_econ.create_new_clerkunit(clerk_id=timmy_text)

    # THEN
    print(f"{timmy_dir=}")
    assert os_path.exists(timmy_dir)


def test_EconUnit_change_clerkunit_clerk_id_SetsAttrsCorrectly(env_dir_setup_cleanup):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(x_econ_id, econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    old_bob_text = "old Bob"
    old_bob_dir = f"{x_econ.get_clerkunits_dir()}/{old_bob_text}"
    old_bob_file_path = f"{old_bob_dir}/role_agenda.json"
    bob_clerkunit = clerkunit_shop(
        old_bob_text, x_econ.get_object_root_dir(), get_temp_env_econ_id()
    )
    x_econ.set_clerkunit(bob_clerkunit)
    print(f"{old_bob_dir=}")

    new_bob_text = "new Bob"
    new_bob_dir = f"{x_econ.get_clerkunits_dir()}/{new_bob_text}"
    new_bob_file_path = f"{new_bob_dir}/role_agenda.json"
    assert os_path.exists(new_bob_dir) == False
    assert os_path.exists(old_bob_dir)
    assert os_path.exists(new_bob_file_path) == False
    assert os_path.exists(old_bob_file_path)
    old_bob_clerkunit = x_econ.get_clerkunit(clerk_id=old_bob_text)
    assert x_econ.get_clerkunit(clerk_id=new_bob_text) is None
    assert old_bob_clerkunit._clerkunit_dir == old_bob_dir
    assert old_bob_clerkunit._clerkunit_dir != new_bob_dir

    # WHEN
    x_econ.change_clerkunit_clerk_id(
        old_clerk_id=old_bob_text, new_clerk_id=new_bob_text
    )

    # THEN
    assert os_path.exists(new_bob_dir)
    assert os_path.exists(old_bob_dir) == False
    print(f"{new_bob_file_path=}")
    assert os_path.exists(new_bob_file_path)
    assert os_path.exists(old_bob_file_path) == False
    assert x_econ.get_clerkunit(clerk_id=old_bob_text) is None
    new_bob_clerkunit = x_econ.get_clerkunit(clerk_id=new_bob_text)
    assert new_bob_clerkunit._clerkunit_dir != old_bob_dir
    assert new_bob_clerkunit._clerkunit_dir == new_bob_dir


def test_EconUnit_del_clerkunit_dir_DeletesAttr(env_dir_setup_cleanup):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(x_econ_id, econ_dir=get_test_econ_dir())
    xia_text = "Xia"
    xia_dir = f"{x_econ.get_clerkunits_dir()}/{xia_text}"
    xia_file_path = f"{xia_dir}/role_agenda.json"
    x_econ.create_new_clerkunit(clerk_id=xia_text)
    x_econ.save_clerkunit_file(clerk_id=xia_text)
    print(f"{xia_file_path=}")
    assert os_path.exists(xia_dir)
    assert os_path.exists(xia_file_path)

    # WHEN
    x_econ.del_clerkunit_dir(clerk_id=xia_text)

    # THEN
    assert os_path.exists(xia_file_path) == False
    assert os_path.exists(xia_dir) == False


def test_EconUnit_add_clerkunit_SetsAttr(env_dir_setup_cleanup):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(x_econ_id, econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    bob_text = "Bob"
    bob_dir = f"{x_econ.get_clerkunits_dir()}/{bob_text}"
    bob_file_path = f"{bob_dir}/role_agenda.json"
    assert os_path.exists(bob_dir) == False
    assert os_path.exists(bob_file_path) == False
    assert x_econ.get_clerkunit(clerk_id=bob_text) is None

    # WHEN
    x_econ.add_clerkunit(worker_id=bob_text)

    # THEN
    assert x_econ._clerkunits != {}
    print(f"{bob_file_path=}")
    bob_static_clerkunit = clerkunit_shop(
        worker_id=bob_text,
        env_dir=get_test_econ_dir(),
        econ_id=get_temp_env_econ_id(),
    )
    bob_gen_clerkunit = x_econ.get_clerkunit(bob_text)
    assert bob_gen_clerkunit._env_dir == bob_static_clerkunit._env_dir
    assert bob_gen_clerkunit._role != None
    assert bob_static_clerkunit._role != None
    assert bob_gen_clerkunit == bob_static_clerkunit
    print(f"{   bob_gen_clerkunit._role._worker_id=}")
    print(f"{bob_static_clerkunit._role._worker_id=}")
    assert bob_gen_clerkunit._role == bob_static_clerkunit._role
    assert os_path.exists(bob_dir)
    assert os_path.exists(bob_file_path)


def test_EconUnit_clerkunit_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    x_econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(x_econ_id, econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    bob_text = "Bob"

    # WHEN / THEN
    assert x_econ.clerkunit_exists(clerk_id=bob_text) == False

    # WHEN / THEN
    x_econ.add_clerkunit(worker_id=bob_text)
    assert x_econ.clerkunit_exists(clerk_id=bob_text)
