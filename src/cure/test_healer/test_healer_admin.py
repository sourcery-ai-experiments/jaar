from src.pact.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.cure.healer import HealerAdmin, healeradmin_shop
from src.cure.examples.example_healers import (
    get_6node_pact as example_healers_get_6node_pact,
    get_6node_pact as example_healers_get_7nodeJRootWithH_pact,
)
from src.cure.examples.healer_env_kit import (
    get_temp_healer_dir,
    get_temp_cure_handle,
    healer_dir_setup_cleanup,
)
from os import path as os_path


def test_admin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healer_dir()

    # WHEN
    pdx = HealerAdmin(bob_text, env_dir, get_temp_cure_handle())

    # THEN
    assert pdx._healer_title != None
    assert pdx._env_dir != None
    assert pdx._cure_handle != None
    assert pdx._healer_dir is None
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


def test_HealerAdmin_set_dir_CorrectSetsHealerAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healer_dir()
    pdx = HealerAdmin(bob_text, env_dir, get_temp_cure_handle())
    assert pdx._healer_dir is None
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
    assert pdx._healer_dir != None
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

    healers_drectory_title = "healers"
    x_healers_dir = f"{env_dir}/{healers_drectory_title}"
    x_healer_dir = f"{x_healers_dir}/{bob_text}"
    x_public_file_title = f"{bob_text}.json"
    x_isol_file_title = "isol_pact.json"
    x_isol_file_path = f"{x_healer_dir}/{x_isol_file_title}"
    x_pact_output_file_title = "output_pact.json"
    x_pact_output_file_path = f"{x_healer_dir}/{x_pact_output_file_title}"
    pacts_str = "pacts"
    x_pacts_depot_dir = f"{x_healer_dir}/{pacts_str}"
    x_pacts_ignore_dir = f"{x_healer_dir}/ignores"
    x_pacts_bond_dir = f"{x_healer_dir}/bonds"
    x_pacts_digest_dir = f"{x_healer_dir}/digests"
    x_pacts_public_dir = f"{env_dir}/{pacts_str}"
    assert pdx._healers_dir == x_healers_dir
    assert pdx._healer_dir == x_healer_dir
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


def test_HealerAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    healer_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_healer_dir()
    pdx = HealerAdmin(jul_text, env_dir, get_temp_cure_handle())
    pdx.set_dirs()
    assert os_path.exists(pdx._healers_dir) is False
    assert os_path.exists(pdx._healer_dir) is False
    assert os_path.exists(pdx._isol_file_path) is False
    assert os_path.isdir(pdx._healer_dir) is False
    assert os_path.exists(pdx._pacts_depot_dir) is False
    assert os_path.exists(pdx._pacts_digest_dir) is False
    assert os_path.exists(pdx._pacts_ignore_dir) is False
    assert os_path.exists(pdx._pacts_bond_dir) is False

    # WHEN
    pact_x = example_healers_get_7nodeJRootWithH_pact()
    pdx.create_core_dir_and_files(pact_x)

    # THEN check pacts src directory created
    print(f"Checking {pdx._healers_dir=}")
    print(f"Checking {pdx._healer_dir=}")
    assert os_path.exists(pdx._healers_dir)
    assert os_path.exists(pdx._healer_dir)
    assert os_path.exists(pdx._isol_file_path)
    assert os_path.isdir(pdx._healer_dir)
    assert os_path.exists(pdx._pacts_depot_dir)
    assert os_path.exists(pdx._pacts_digest_dir)
    assert os_path.exists(pdx._pacts_ignore_dir)
    assert os_path.exists(pdx._pacts_bond_dir)


def test_HealerAdmin_create_core_dir_and_files_DoesNotOverWriteIsolContract(
    healer_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_healer_dir()
    jul_pdx = HealerAdmin(jul_text, env_dir, get_temp_cure_handle())
    jul_pdx.set_dirs()
    pact_x = example_healers_get_7nodeJRootWithH_pact()
    jul_pdx.create_core_dir_and_files(pact_x)
    assert os_path.exists(jul_pdx._isol_file_path)
    # jul_cx = pact_get_from_json(x_func_open_file(jul_pdx._isol_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_pdx._healer_dir,
        file_title=jul_pdx._isol_file_title,
        file_text=ex1,
    )
    assert x_func_open_file(jul_pdx._healer_dir, jul_pdx._isol_file_title) == ex1

    # WHEN
    jul_pdx.create_core_dir_and_files(pact_x)

    # THEN
    assert x_func_open_file(jul_pdx._healer_dir, jul_pdx._isol_file_title) == ex1


def test_HealerAdmin_set_healer_title_WorksCorrectly(healer_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_healer_dir()

    old_healer_text = "bob"
    pdx = HealerAdmin(old_healer_text, env_dir, get_temp_cure_handle())
    pact_x = example_healers_get_7nodeJRootWithH_pact()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(pact_x)
    old_healer_dir = pdx._healer_dir
    # old_healer_dir = f"{env_dir}/healers/{old_healer_text}"
    print(f"{pdx._healer_dir}")
    print(f"{env_dir}/healers/{old_healer_text}")
    isol_file_title = "isol_pact.json"
    old_isol_file_path = f"{old_healer_dir}/{isol_file_title}"

    assert os_path.exists(old_healer_dir)
    assert os_path.isdir(old_healer_dir)
    assert os_path.exists(old_isol_file_path)

    new_healer_text = "tim"
    new_healer_dir = f"{env_dir}/healers/{new_healer_text}"
    new_isol_file_path = f"{new_healer_dir}/{isol_file_title}"
    assert os_path.exists(new_healer_dir) == False
    assert os_path.isdir(new_healer_dir) == False
    assert os_path.exists(new_isol_file_path) == False

    # WHEN
    pdx.set_healer_title(new_title=new_healer_text)

    # THEN
    assert os_path.exists(old_healer_dir) == False
    assert os_path.isdir(old_healer_dir) == False
    assert os_path.exists(old_isol_file_path) == False
    assert os_path.exists(new_healer_dir)
    assert os_path.isdir(new_healer_dir)
    assert os_path.exists(new_isol_file_path)


def test_healerunit_auto_output_to_public_SavesContractToPublicDir(
    healer_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = healeradmin_shop(bob_text, get_temp_healer_dir(), get_temp_cure_handle())
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
