from src.pact.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.cure.healing import HealingAdmin, healingadmin_shop
from src.cure.examples.example_healers import (
    get_6node_pact as example_healers_get_6node_pact,
    get_6node_pact as example_healers_get_7nodeJRootWithH_pact,
)
from src.cure.examples.healer_env_kit import (
    get_temp_healingunit_dir,
    get_temp_cure_handle,
    healer_dir_setup_cleanup,
)
from os import path as os_path


def test_admin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healingunit_dir()

    # WHEN
    pdx = HealingAdmin(bob_text, env_dir, get_temp_cure_handle())

    # THEN
    assert pdx._healing_title != None
    assert pdx._env_dir != None
    assert pdx._cure_handle != None
    assert pdx._healingunit_dir is None
    assert pdx._isol_file_title is None
    assert pdx._isol_file_path is None
    assert pdx._pact_output_file_title is None
    assert pdx._pact_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._pacts_public_dir is None
    assert pdx._pacts_depot_dir is None
    assert pdx._pacts_ignore_dir is None
    assert pdx._pacts_bond_dir is None
    assert pdx._pacts_digest_dir is None


def test_HealingAdmin_set_dir_CorrectSetsHealingAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healingunit_dir()
    pdx = HealingAdmin(bob_text, env_dir, get_temp_cure_handle())
    assert pdx._healingunit_dir is None
    assert pdx._pact_output_file_title is None
    assert pdx._pact_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._pacts_public_dir is None
    assert pdx._pacts_depot_dir is None
    assert pdx._pacts_ignore_dir is None
    assert pdx._pacts_digest_dir is None
    assert pdx._pacts_bond_dir is None
    assert pdx._isol_file_title is None
    assert pdx._isol_file_path is None
    # WHEN
    pdx.set_dirs()

    # THEN
    assert pdx._healingunit_dir != None
    assert pdx._pact_output_file_title != None
    assert pdx._pact_output_file_path != None
    assert pdx._public_file_title != None
    assert pdx._pacts_public_dir != None
    assert pdx._pacts_depot_dir != None
    assert pdx._pacts_ignore_dir != None
    assert pdx._pacts_digest_dir != None
    assert pdx._pacts_bond_dir != None
    assert pdx._isol_file_title != None
    assert pdx._isol_file_path != None

    healers_drectory_folder = "healingunits"
    x_healingunits_dir = f"{env_dir}/{healers_drectory_folder}"
    x_healingunit_dir = f"{x_healingunits_dir}/{bob_text}"
    x_public_file_title = f"{bob_text}.json"
    x_isol_file_title = "isol_pact.json"
    x_isol_file_path = f"{x_healingunit_dir}/{x_isol_file_title}"
    x_pact_output_file_title = "output_pact.json"
    x_pact_output_file_path = f"{x_healingunit_dir}/{x_pact_output_file_title}"
    pacts_str = "pacts"
    x_pacts_depot_dir = f"{x_healingunit_dir}/{pacts_str}"
    x_pacts_ignore_dir = f"{x_healingunit_dir}/ignores"
    x_pacts_bond_dir = f"{x_healingunit_dir}/bonds"
    x_pacts_digest_dir = f"{x_healingunit_dir}/digests"
    x_pacts_public_dir = f"{env_dir}/{pacts_str}"
    assert pdx._healingunits_dir == x_healingunits_dir
    assert pdx._healingunit_dir == x_healingunit_dir
    assert pdx._isol_file_title == x_isol_file_title
    assert pdx._isol_file_path == x_isol_file_path
    assert pdx._pact_output_file_title == x_pact_output_file_title
    assert pdx._pact_output_file_path == x_pact_output_file_path
    assert pdx._pacts_depot_dir == x_pacts_depot_dir
    assert pdx._pacts_ignore_dir == x_pacts_ignore_dir
    assert pdx._pacts_bond_dir == x_pacts_bond_dir
    assert pdx._pacts_digest_dir == x_pacts_digest_dir
    assert pdx._public_file_title == x_public_file_title
    assert pdx._pacts_public_dir == x_pacts_public_dir


def test_HealingAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    healer_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_healingunit_dir()
    pdx = HealingAdmin(jul_text, env_dir, get_temp_cure_handle())
    pdx.set_dirs()
    assert os_path.exists(pdx._healingunits_dir) is False
    assert os_path.exists(pdx._healingunit_dir) is False
    assert os_path.exists(pdx._isol_file_path) is False
    assert os_path.isdir(pdx._healingunit_dir) is False
    assert os_path.exists(pdx._pacts_depot_dir) is False
    assert os_path.exists(pdx._pacts_digest_dir) is False
    assert os_path.exists(pdx._pacts_ignore_dir) is False
    assert os_path.exists(pdx._pacts_bond_dir) is False

    # WHEN
    pact_x = example_healers_get_7nodeJRootWithH_pact()
    pdx.create_core_dir_and_files(pact_x)

    # THEN check pacts src directory created
    print(f"Checking {pdx._healingunits_dir=}")
    print(f"Checking {pdx._healingunit_dir=}")
    assert os_path.exists(pdx._healingunits_dir)
    assert os_path.exists(pdx._healingunit_dir)
    assert os_path.exists(pdx._isol_file_path)
    assert os_path.isdir(pdx._healingunit_dir)
    assert os_path.exists(pdx._pacts_depot_dir)
    assert os_path.exists(pdx._pacts_digest_dir)
    assert os_path.exists(pdx._pacts_ignore_dir)
    assert os_path.exists(pdx._pacts_bond_dir)


def test_HealingAdmin_create_core_dir_and_files_DoesNotOverWriteIsolPact(
    healer_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_healingunit_dir()
    jul_pdx = HealingAdmin(jul_text, env_dir, get_temp_cure_handle())
    jul_pdx.set_dirs()
    pact_x = example_healers_get_7nodeJRootWithH_pact()
    jul_pdx.create_core_dir_and_files(pact_x)
    assert os_path.exists(jul_pdx._isol_file_path)
    # jul_cx = pact_get_from_json(x_func_open_file(jul_pdx._isol_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_pdx._healingunit_dir,
        file_title=jul_pdx._isol_file_title,
        file_text=ex1,
    )
    assert x_func_open_file(jul_pdx._healingunit_dir, jul_pdx._isol_file_title) == ex1

    # WHEN
    jul_pdx.create_core_dir_and_files(pact_x)

    # THEN
    assert x_func_open_file(jul_pdx._healingunit_dir, jul_pdx._isol_file_title) == ex1


def test_HealingAdmin_set_healing_title_WorksCorrectly(healer_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_healingunit_dir()

    old_healer_text = "bob"
    pdx = HealingAdmin(old_healer_text, env_dir, get_temp_cure_handle())
    pact_x = example_healers_get_7nodeJRootWithH_pact()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(pact_x)
    old_healingunit_dir = pdx._healingunit_dir
    # old_healingunit_dir = f"{env_dir}/healingunits/{old_healer_text}"
    print(f"{pdx._healingunit_dir}")
    print(f"{env_dir}/healingunits/{old_healer_text}")
    isol_file_title = "isol_pact.json"
    old_isol_file_path = f"{old_healingunit_dir}/{isol_file_title}"

    assert os_path.exists(old_healingunit_dir)
    assert os_path.isdir(old_healingunit_dir)
    assert os_path.exists(old_isol_file_path)

    new_healer_text = "tim"
    new_healingunit_dir = f"{env_dir}/healingunits/{new_healer_text}"
    new_isol_file_path = f"{new_healingunit_dir}/{isol_file_title}"
    assert os_path.exists(new_healingunit_dir) == False
    assert os_path.isdir(new_healingunit_dir) == False
    assert os_path.exists(new_isol_file_path) == False

    # WHEN
    pdx.set_healing_title(new_title=new_healer_text)

    # THEN
    assert os_path.exists(old_healingunit_dir) == False
    assert os_path.isdir(old_healingunit_dir) == False
    assert os_path.exists(old_isol_file_path) == False
    assert os_path.exists(new_healingunit_dir)
    assert os_path.isdir(new_healingunit_dir)
    assert os_path.exists(new_isol_file_path)


def test_healingunit_auto_output_to_public_SavesPactToPublicDir(
    healer_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = healingadmin_shop(
        bob_text, get_temp_healingunit_dir(), get_temp_cure_handle()
    )
    pact_x = example_healers_get_6node_pact()
    pact_x.set_healer(new_healer=bob_text)
    pdx.create_core_dir_and_files(pact_x)

    public_file_path = f"{pdx._pacts_public_dir}/{pdx._public_file_title}"
    print(f"{public_file_path=}")
    assert os_path.exists(public_file_path) is False

    # WHEN
    pdx.save_pact_to_public(pact_x=pact_x)

    # THEN
    assert os_path.exists(public_file_path)
