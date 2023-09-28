from src.economy.actor import ActorAdmin, actoradmin_shop
import src.economy.examples.example_actors as example_actors
from src.economy.examples.actor_env_kit import (
    get_temp_actor_dir,
    get_temp_economy_title,
    actor_dir_setup_cleanup,
)
from os import path as os_path
from src.contract.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)


def test_admin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_actor_dir()

    # WHEN
    pdx = ActorAdmin(bob_text, env_dir, get_temp_economy_title())

    # THEN
    assert pdx._actor_name != None
    assert pdx._env_dir != None
    assert pdx._economy_title != None
    assert pdx._actor_dir is None
    assert pdx._isol_file_name is None
    assert pdx._isol_file_path is None
    assert pdx._contract_output_file_name is None
    assert pdx._contract_output_file_path is None
    assert pdx._public_file_name is None
    assert pdx._contracts_public_dir is None
    assert pdx._contracts_depot_dir is None
    assert pdx._contracts_ignore_dir is None
    assert pdx._contracts_bond_dir is None
    assert pdx._contracts_digest_dir is None


def test_ActorAdmin_set_dir_CorrectSetsActorAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_actor_dir()
    pdx = ActorAdmin(bob_text, env_dir, get_temp_economy_title())
    assert pdx._actor_dir is None
    assert pdx._contract_output_file_name is None
    assert pdx._contract_output_file_path is None
    assert pdx._public_file_name is None
    assert pdx._contracts_public_dir is None
    assert pdx._contracts_depot_dir is None
    assert pdx._contracts_ignore_dir is None
    assert pdx._contracts_digest_dir is None
    assert pdx._contracts_bond_dir is None
    assert pdx._isol_file_name is None
    assert pdx._isol_file_path is None
    # WHEN
    pdx.set_dirs()

    # THEN
    assert pdx._actor_dir != None
    assert pdx._contract_output_file_name != None
    assert pdx._contract_output_file_path != None
    assert pdx._public_file_name != None
    assert pdx._contracts_public_dir != None
    assert pdx._contracts_depot_dir != None
    assert pdx._contracts_ignore_dir != None
    assert pdx._contracts_digest_dir != None
    assert pdx._contracts_bond_dir != None
    assert pdx._isol_file_name != None
    assert pdx._isol_file_path != None

    actors_drectory_name = "actors"
    x_actors_dir = f"{env_dir}/{actors_drectory_name}"
    x_actor_dir = f"{x_actors_dir}/{bob_text}"
    x_public_file_name = f"{bob_text}.json"
    x_isol_file_name = "isol_contract.json"
    x_isol_file_path = f"{x_actor_dir}/{x_isol_file_name}"
    x_contract_output_file_name = "output_contract.json"
    x_contract_output_file_path = f"{x_actor_dir}/{x_contract_output_file_name}"
    contracts_str = "contracts"
    x_contracts_depot_dir = f"{x_actor_dir}/{contracts_str}"
    x_contracts_ignore_dir = f"{x_actor_dir}/ignores"
    x_contracts_bond_dir = f"{x_actor_dir}/bonds"
    x_contracts_digest_dir = f"{x_actor_dir}/digests"
    x_contracts_public_dir = f"{env_dir}/{contracts_str}"
    assert pdx._actors_dir == x_actors_dir
    assert pdx._actor_dir == x_actor_dir
    assert pdx._isol_file_name == x_isol_file_name
    assert pdx._isol_file_path == x_isol_file_path
    assert pdx._contract_output_file_name == x_contract_output_file_name
    assert pdx._contract_output_file_path == x_contract_output_file_path
    assert pdx._contracts_depot_dir == x_contracts_depot_dir
    assert pdx._contracts_ignore_dir == x_contracts_ignore_dir
    assert pdx._contracts_bond_dir == x_contracts_bond_dir
    assert pdx._contracts_digest_dir == x_contracts_digest_dir
    assert pdx._public_file_name == x_public_file_name
    assert pdx._contracts_public_dir == x_contracts_public_dir


def test_ActorAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    actor_dir_setup_cleanup,
):
    # GIVEN create actor
    jul_text = "julian"
    env_dir = get_temp_actor_dir()
    pdx = ActorAdmin(jul_text, env_dir, get_temp_economy_title())
    pdx.set_dirs()
    assert os_path.exists(pdx._actors_dir) is False
    assert os_path.exists(pdx._actor_dir) is False
    assert os_path.exists(pdx._isol_file_path) is False
    assert os_path.isdir(pdx._actor_dir) is False
    assert os_path.exists(pdx._contracts_depot_dir) is False
    assert os_path.exists(pdx._contracts_digest_dir) is False
    assert os_path.exists(pdx._contracts_ignore_dir) is False
    assert os_path.exists(pdx._contracts_bond_dir) is False

    # WHEN
    contract_x = example_actors.get_7nodeJRootWithH_contract()
    pdx.create_core_dir_and_files(contract_x)

    # THEN check contracts src directory created
    print(f"Checking {pdx._actors_dir=}")
    print(f"Checking {pdx._actor_dir=}")
    assert os_path.exists(pdx._actors_dir)
    assert os_path.exists(pdx._actor_dir)
    assert os_path.exists(pdx._isol_file_path)
    assert os_path.isdir(pdx._actor_dir)
    assert os_path.exists(pdx._contracts_depot_dir)
    assert os_path.exists(pdx._contracts_digest_dir)
    assert os_path.exists(pdx._contracts_ignore_dir)
    assert os_path.exists(pdx._contracts_bond_dir)


def test_ActorAdmin_create_core_dir_and_files_DoesNotOverWriteIsolContract(
    actor_dir_setup_cleanup,
):
    # GIVEN create actor
    jul_text = "julian"
    env_dir = get_temp_actor_dir()
    jul_pdx = ActorAdmin(jul_text, env_dir, get_temp_economy_title())
    jul_pdx.set_dirs()
    contract_x = example_actors.get_7nodeJRootWithH_contract()
    jul_pdx.create_core_dir_and_files(contract_x)
    assert os_path.exists(jul_pdx._isol_file_path)
    # jul_cx = contract_get_from_json(x_func_open_file(jul_pdx._isol_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_pdx._actor_dir,
        file_name=jul_pdx._isol_file_name,
        file_text=ex1,
    )
    assert x_func_open_file(jul_pdx._actor_dir, jul_pdx._isol_file_name) == ex1

    # WHEN
    jul_pdx.create_core_dir_and_files(contract_x)

    # THEN
    assert x_func_open_file(jul_pdx._actor_dir, jul_pdx._isol_file_name) == ex1


def test_ActorAdmin_set_actor_name_WorksCorrectly(actor_dir_setup_cleanup):
    # GIVEN create actor
    env_dir = get_temp_actor_dir()

    old_actor_text = "bob"
    pdx = ActorAdmin(old_actor_text, env_dir, get_temp_economy_title())
    contract_x = example_actors.get_7nodeJRootWithH_contract()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(contract_x)
    old_actor_dir = pdx._actor_dir
    # old_actor_dir = f"{env_dir}/actors/{old_actor_text}"
    print(f"{pdx._actor_dir}")
    print(f"{env_dir}/actors/{old_actor_text}")
    isol_file_name = "isol_contract.json"
    old_isol_file_path = f"{old_actor_dir}/{isol_file_name}"

    assert os_path.exists(old_actor_dir)
    assert os_path.isdir(old_actor_dir)
    assert os_path.exists(old_isol_file_path)

    new_actor_text = "tim"
    new_actor_dir = f"{env_dir}/actors/{new_actor_text}"
    new_isol_file_path = f"{new_actor_dir}/{isol_file_name}"
    assert os_path.exists(new_actor_dir) == False
    assert os_path.isdir(new_actor_dir) == False
    assert os_path.exists(new_isol_file_path) == False

    # WHEN
    pdx.set_actor_name(new_name=new_actor_text)

    # THEN
    assert os_path.exists(old_actor_dir) == False
    assert os_path.isdir(old_actor_dir) == False
    assert os_path.exists(old_isol_file_path) == False
    assert os_path.exists(new_actor_dir)
    assert os_path.isdir(new_actor_dir)
    assert os_path.exists(new_isol_file_path)


def test_actorunit_auto_output_to_public_SavesContractToPublicDir(
    actor_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = actoradmin_shop(bob_text, get_temp_actor_dir(), get_temp_economy_title())
    contract_x = example_actors.get_6node_contract()
    contract_x.set_owner(new_owner=bob_text)
    pdx.create_core_dir_and_files(contract_x)

    public_file_path = f"{pdx._contracts_public_dir}/{pdx._public_file_name}"
    print(f"{public_file_path=}")
    assert os_path.exists(public_file_path) is False

    # WHEN
    pdx.save_contract_to_public(contract_x=contract_x)

    # THEN
    assert os_path.exists(public_file_path)
