from src.economy.actor import actorunit_shop
from src.contract.contract import ContractUnit
from src.contract.idea import IdeaRoot
import src.economy.examples.example_actors as example_actors
from src.economy.examples.actor_env_kit import (
    actor_dir_setup_cleanup,
    get_temp_actor_dir,
    get_temp_economy_title,
    create_contract_file,
)
from os import path as os_path, scandir as os_scandir
from pytest import raises as pytest_raises
from src.contract.x_func import (
    count_files as x_func_count_files,
    open_file as x_func_open_file,
    delete_dir as x_func_delete_dir,
)


def test_actorunit_exists(actor_dir_setup_cleanup):
    # GIVEN
    actor_text = "test1"

    # WHEN
    ux = actorunit_shop(
        name=actor_text,
        env_dir=get_temp_actor_dir(),
        economy_title=get_temp_economy_title(),
    )

    # GIVEN
    assert ux._admin._actor_name != None
    assert ux._admin._economy_title != None
    assert ux._admin._economy_title == get_temp_economy_title()
    assert ux._isol is None


def test_actorunit_auto_output_to_public_SavesContractToPublicDirWhenTrue(
    actor_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_actor_dir()
    economy_title = get_temp_economy_title()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_actor_dir()}/contracts/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/economy/examples/ex_env/contracts/{public_file_name}"
    ux = actorunit_shop(tim_text, env_dir, economy_title, _auto_output_to_public=True)
    ux.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    tim_contract = ContractUnit(_owner=tim_text)
    tim_contract.set_economy_title(economy_title)
    ux.set_depot_contract(tim_contract, "blind_trust")

    # THEN
    assert os_path.exists(public_file_path)


def test_actorunit_auto_output_to_public_DoesNotSaveContractToPublicDirWhenFalse(
    actor_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_actor_dir()
    economy_title = get_temp_economy_title()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_actor_dir()}/contracts/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/economy/examples/ex_env/contracts/{public_file_name}"
    ux = actorunit_shop(tim_text, env_dir, economy_title, _auto_output_to_public=False)
    ux.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    ux.set_depot_contract(ContractUnit(_owner=tim_text), depotlink_type="blind_trust")

    # THEN
    assert os_path.exists(public_file_path) is False


def test_actorunit_get_isol_createsEmptyContractWhenFileDoesNotExist(
    actor_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = actorunit_shop(tim_text, get_temp_actor_dir(), get_temp_economy_title())
    tim_ux.create_core_dir_and_files()
    assert os_path.exists(tim_ux._admin._isol_file_path)
    x_func_delete_dir(dir=tim_ux._admin._isol_file_path)
    assert os_path.exists(tim_ux._admin._isol_file_path) is False
    assert tim_ux._isol is None

    # WHEN
    cx_isol = tim_ux.get_isol()

    # THEN
    assert os_path.exists(tim_ux._admin._isol_file_path)
    assert tim_ux._isol != None


def test_actorunit_get_isol_getsMemoryContractIfExists(
    actor_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = actorunit_shop(tim_text, get_temp_actor_dir(), get_temp_economy_title())
    tim_ux.create_core_dir_and_files()
    isol_file_path = f"{tim_ux._admin._actor_dir}/{tim_ux._admin._isol_file_name}"
    cx_isol1 = tim_ux.get_isol()
    assert os_path.exists(isol_file_path)
    assert tim_ux._isol != None

    # WHEN
    ray_text = "Ray"
    tim_ux._isol = ContractUnit(_owner=ray_text)
    cx_isol2 = tim_ux.get_isol()

    # THEN
    assert cx_isol2._owner == ray_text
    assert cx_isol2 != cx_isol1

    # WHEN
    tim_ux._isol = None
    cx_isol3 = tim_ux.get_isol()

    # THEN
    assert cx_isol3._owner != ray_text
    assert cx_isol3 == cx_isol1


def test_actorunit_set_isol_savesIsolContractSet_isol_None(
    actor_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = actorunit_shop(tim_text, get_temp_actor_dir(), get_temp_economy_title())
    tim_ux.create_core_dir_and_files()
    isol_file_path = f"{tim_ux._admin._actor_dir}/{tim_ux._admin._isol_file_name}"
    cx_isol1 = tim_ux.get_isol()
    assert os_path.exists(isol_file_path)
    assert tim_ux._isol != None

    # WHEN
    uid_text = "Not a real uid"
    tim_ux._isol._idearoot._uid = uid_text
    tim_ux.set_isol()

    # THEN
    assert os_path.exists(isol_file_path)
    assert tim_ux._isol is None
    cx_isol2 = tim_ux.get_isol()
    assert cx_isol2._idearoot._uid == uid_text


def test_actorunit_set_isol_savesGivenContractSet_isol_None(
    actor_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    ux = actorunit_shop(tim_text, get_temp_actor_dir(), get_temp_economy_title())
    ux.create_core_dir_and_files()
    isol_file_path = f"{ux._admin._actor_dir}/{ux._admin._isol_file_name}"
    cx_isol1 = ux.get_isol()
    assert os_path.exists(isol_file_path)
    assert ux._isol != None

    # WHEN
    isol_uid_text = "this is ._isol uid"
    ux._isol._idearoot._uid = isol_uid_text

    new_cx = ContractUnit(_owner=tim_text)
    new_cx_uid_text = "this is pulled ContractUnit uid"
    new_cx._idearoot._uid = new_cx_uid_text

    ux.set_isol(new_cx)

    # THEN
    assert os_path.exists(isol_file_path)
    assert ux._isol is None
    assert ux.get_isol()._idearoot._uid != isol_uid_text
    assert ux.get_isol()._idearoot._uid == new_cx_uid_text

    # GIVEN
    ux.set_isol(new_cx)
    assert os_path.exists(isol_file_path)
    assert ux._isol is None

    # WHEN
    ux.set_isol_if_empty()

    # THEN
    assert ux._isol != None
    assert os_path.exists(isol_file_path)

    # WHEN
    isol_uid_text = "this is ._isol uid"
    ux._isol._idearoot._uid = isol_uid_text


def test_actorunit_set_isol_if_emtpy_DoesNotReplace_isol(
    actor_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    ux = actorunit_shop(tim_text, get_temp_actor_dir(), get_temp_economy_title())
    ux.create_core_dir_and_files()
    saved_cx = ContractUnit(_owner=tim_text)
    saved_cx_uid_text = "this is pulled ContractUnit uid"
    saved_cx._idearoot._uid = saved_cx_uid_text
    ux.set_isol(saved_cx)
    ux.get_isol()
    assert ux._isol != None

    # WHEN
    isol_uid_text = "this is ._isol uid"
    ux._isol._idearoot._uid = isol_uid_text
    ux.set_isol_if_empty()

    # THEN
    assert ux._isol != None
    assert ux._isol._idearoot._uid == isol_uid_text
    assert ux._isol._idearoot._uid != saved_cx_uid_text
