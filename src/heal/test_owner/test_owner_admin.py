from src.contract.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.heal.owner import OwnerAdmin, owneradmin_shop
from src.heal.examples.example_owners import (
    get_6node_contract as example_owners_get_6node_contract,
    get_6node_contract as example_owners_get_7nodeJRootWithH_contract,
)
from src.heal.examples.owner_env_kit import (
    get_temp_owner_dir,
    get_temp_heal_kind,
    owner_dir_setup_cleanup,
)
from os import path as os_path


def test_admin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_owner_dir()

    # WHEN
    pdx = OwnerAdmin(bob_text, env_dir, get_temp_heal_kind())

    # THEN
    assert pdx._owner_title != None
    assert pdx._env_dir != None
    assert pdx._heal_kind != None
    assert pdx._owner_dir is None
    assert pdx._isol_file_title is None
    assert pdx._isol_file_path is None
    assert pdx._contract_output_file_title is None
    assert pdx._contract_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._contracts_public_dir is None
    assert pdx._contracts_depot_dir is None
    assert pdx._contracts_ignore_dir is None
    assert pdx._contracts_bond_dir is None
    assert pdx._contracts_digest_dir is None


def test_OwnerAdmin_set_dir_CorrectSetsOwnerAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_owner_dir()
    pdx = OwnerAdmin(bob_text, env_dir, get_temp_heal_kind())
    assert pdx._owner_dir is None
    assert pdx._contract_output_file_title is None
    assert pdx._contract_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._contracts_public_dir is None
    assert pdx._contracts_depot_dir is None
    assert pdx._contracts_ignore_dir is None
    assert pdx._contracts_digest_dir is None
    assert pdx._contracts_bond_dir is None
    assert pdx._isol_file_title is None
    assert pdx._isol_file_path is None
    # WHEN
    pdx.set_dirs()

    # THEN
    assert pdx._owner_dir != None
    assert pdx._contract_output_file_title != None
    assert pdx._contract_output_file_path != None
    assert pdx._public_file_title != None
    assert pdx._contracts_public_dir != None
    assert pdx._contracts_depot_dir != None
    assert pdx._contracts_ignore_dir != None
    assert pdx._contracts_digest_dir != None
    assert pdx._contracts_bond_dir != None
    assert pdx._isol_file_title != None
    assert pdx._isol_file_path != None

    owners_drectory_title = "owners"
    x_owners_dir = f"{env_dir}/{owners_drectory_title}"
    x_owner_dir = f"{x_owners_dir}/{bob_text}"
    x_public_file_title = f"{bob_text}.json"
    x_isol_file_title = "isol_contract.json"
    x_isol_file_path = f"{x_owner_dir}/{x_isol_file_title}"
    x_contract_output_file_title = "output_contract.json"
    x_contract_output_file_path = f"{x_owner_dir}/{x_contract_output_file_title}"
    contracts_str = "contracts"
    x_contracts_depot_dir = f"{x_owner_dir}/{contracts_str}"
    x_contracts_ignore_dir = f"{x_owner_dir}/ignores"
    x_contracts_bond_dir = f"{x_owner_dir}/bonds"
    x_contracts_digest_dir = f"{x_owner_dir}/digests"
    x_contracts_public_dir = f"{env_dir}/{contracts_str}"
    assert pdx._owners_dir == x_owners_dir
    assert pdx._owner_dir == x_owner_dir
    assert pdx._isol_file_title == x_isol_file_title
    assert pdx._isol_file_path == x_isol_file_path
    assert pdx._contract_output_file_title == x_contract_output_file_title
    assert pdx._contract_output_file_path == x_contract_output_file_path
    assert pdx._contracts_depot_dir == x_contracts_depot_dir
    assert pdx._contracts_ignore_dir == x_contracts_ignore_dir
    assert pdx._contracts_bond_dir == x_contracts_bond_dir
    assert pdx._contracts_digest_dir == x_contracts_digest_dir
    assert pdx._public_file_title == x_public_file_title
    assert pdx._contracts_public_dir == x_contracts_public_dir


def test_OwnerAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    owner_dir_setup_cleanup,
):
    # GIVEN create owner
    jul_text = "julian"
    env_dir = get_temp_owner_dir()
    pdx = OwnerAdmin(jul_text, env_dir, get_temp_heal_kind())
    pdx.set_dirs()
    assert os_path.exists(pdx._owners_dir) is False
    assert os_path.exists(pdx._owner_dir) is False
    assert os_path.exists(pdx._isol_file_path) is False
    assert os_path.isdir(pdx._owner_dir) is False
    assert os_path.exists(pdx._contracts_depot_dir) is False
    assert os_path.exists(pdx._contracts_digest_dir) is False
    assert os_path.exists(pdx._contracts_ignore_dir) is False
    assert os_path.exists(pdx._contracts_bond_dir) is False

    # WHEN
    contract_x = example_owners_get_7nodeJRootWithH_contract()
    pdx.create_core_dir_and_files(contract_x)

    # THEN check contracts src directory created
    print(f"Checking {pdx._owners_dir=}")
    print(f"Checking {pdx._owner_dir=}")
    assert os_path.exists(pdx._owners_dir)
    assert os_path.exists(pdx._owner_dir)
    assert os_path.exists(pdx._isol_file_path)
    assert os_path.isdir(pdx._owner_dir)
    assert os_path.exists(pdx._contracts_depot_dir)
    assert os_path.exists(pdx._contracts_digest_dir)
    assert os_path.exists(pdx._contracts_ignore_dir)
    assert os_path.exists(pdx._contracts_bond_dir)


def test_OwnerAdmin_create_core_dir_and_files_DoesNotOverWriteIsolContract(
    owner_dir_setup_cleanup,
):
    # GIVEN create owner
    jul_text = "julian"
    env_dir = get_temp_owner_dir()
    jul_pdx = OwnerAdmin(jul_text, env_dir, get_temp_heal_kind())
    jul_pdx.set_dirs()
    contract_x = example_owners_get_7nodeJRootWithH_contract()
    jul_pdx.create_core_dir_and_files(contract_x)
    assert os_path.exists(jul_pdx._isol_file_path)
    # jul_cx = contract_get_from_json(x_func_open_file(jul_pdx._isol_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_pdx._owner_dir,
        file_title=jul_pdx._isol_file_title,
        file_text=ex1,
    )
    assert x_func_open_file(jul_pdx._owner_dir, jul_pdx._isol_file_title) == ex1

    # WHEN
    jul_pdx.create_core_dir_and_files(contract_x)

    # THEN
    assert x_func_open_file(jul_pdx._owner_dir, jul_pdx._isol_file_title) == ex1


def test_OwnerAdmin_set_owner_title_WorksCorrectly(owner_dir_setup_cleanup):
    # GIVEN create owner
    env_dir = get_temp_owner_dir()

    old_owner_text = "bob"
    pdx = OwnerAdmin(old_owner_text, env_dir, get_temp_heal_kind())
    contract_x = example_owners_get_7nodeJRootWithH_contract()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(contract_x)
    old_owner_dir = pdx._owner_dir
    # old_owner_dir = f"{env_dir}/owners/{old_owner_text}"
    print(f"{pdx._owner_dir}")
    print(f"{env_dir}/owners/{old_owner_text}")
    isol_file_title = "isol_contract.json"
    old_isol_file_path = f"{old_owner_dir}/{isol_file_title}"

    assert os_path.exists(old_owner_dir)
    assert os_path.isdir(old_owner_dir)
    assert os_path.exists(old_isol_file_path)

    new_owner_text = "tim"
    new_owner_dir = f"{env_dir}/owners/{new_owner_text}"
    new_isol_file_path = f"{new_owner_dir}/{isol_file_title}"
    assert os_path.exists(new_owner_dir) == False
    assert os_path.isdir(new_owner_dir) == False
    assert os_path.exists(new_isol_file_path) == False

    # WHEN
    pdx.set_owner_title(new_title=new_owner_text)

    # THEN
    assert os_path.exists(old_owner_dir) == False
    assert os_path.isdir(old_owner_dir) == False
    assert os_path.exists(old_isol_file_path) == False
    assert os_path.exists(new_owner_dir)
    assert os_path.isdir(new_owner_dir)
    assert os_path.exists(new_isol_file_path)


def test_ownerunit_auto_output_to_public_SavesContractToPublicDir(
    owner_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = owneradmin_shop(bob_text, get_temp_owner_dir(), get_temp_heal_kind())
    contract_x = example_owners_get_6node_contract()
    contract_x.set_owner(new_owner=bob_text)
    pdx.create_core_dir_and_files(contract_x)

    public_file_path = f"{pdx._contracts_public_dir}/{pdx._public_file_title}"
    print(f"{public_file_path=}")
    assert os_path.exists(public_file_path) is False

    # WHEN
    pdx.save_contract_to_public(contract_x=contract_x)

    # THEN
    assert os_path.exists(public_file_path)
