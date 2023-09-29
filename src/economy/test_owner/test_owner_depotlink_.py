from src.economy.owner import ownerunit_shop
from src.economy.examples.example_owners import (
    get_2node_contract,
    get_contract_2CleanNodesRandomWeights as get_cal2nodes,
    get_contract_3CleanNodesRandomWeights as get_cal3nodes,
    get_contract_assignment_laundry_example1 as get_america_assign_ex,
)
from src.economy.examples.owner_env_kit import (
    owner_dir_setup_cleanup,
    get_temp_owner_dir,
    get_temp_economy_title,
    create_contract_file,
)
from src.economy.examples.economy_env_kit import get_temp_env_title
from src.economy.economy import economyunit_shop
from os import path as os_path
from pytest import raises as pytest_raises
from src.contract.contract import ContractUnit, get_from_json as contract_get_from_json
from src.contract.x_func import (
    count_files as x_func_count_files,
    open_file as x_func_open_file,
)


def test_ownerunit_set_depotlink_RaisesErrorWhenContractDoesNotExist(
    owner_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_owner_dir()
    sue_cx = ownerunit_shop(sue_text, env_dir, get_temp_economy_title())
    sue_cx.set_isol_if_empty()
    tim_text = "Tim"
    assert list(sue_cx._isol._members.keys()) == [sue_text]

    # WHEN / THEN
    file_path_x = f"{sue_cx._admin._contracts_depot_dir}/{tim_text}.json"
    print(f"{file_path_x=}")
    with pytest_raises(Exception) as excinfo:
        sue_cx._set_depotlink(outer_owner=tim_text)
    assert (
        str(excinfo.value)
        == f"Owner {sue_text} cannot find contract {tim_text} in {file_path_x}"
    )


def test_ownerunit_set_depotlink_CorrectlySetsIsolMembers(owner_dir_setup_cleanup):
    # GIVEN
    yao_text = "yao"
    env_dir = get_temp_owner_dir()
    yao_ux = ownerunit_shop(yao_text, env_dir, get_temp_economy_title())
    yao_ux.set_isol_if_empty()
    sue_text = "sue"
    create_contract_file(yao_ux._admin._contracts_depot_dir, sue_text)
    assert list(yao_ux._isol._members.keys()) == [yao_text]

    # WHEN
    yao_ux._set_depotlink(outer_owner=sue_text)

    # THEN
    assert list(yao_ux._isol._members.keys()) == [yao_text, sue_text]
    assert yao_ux._isol.get_member(sue_text).depotlink_type is None


def test_ownerunit_set_depotlink_CorrectlySetsAssignment(owner_dir_setup_cleanup):
    # GIVEN
    america_cx = get_america_assign_ex()
    print(f"{len(america_cx._idea_dict)=}")
    joachim_text = "Joachim"
    joachim_ux = ownerunit_shop(
        joachim_text, get_temp_owner_dir(), get_temp_economy_title()
    )
    joachim_ux.create_core_dir_and_files()
    joachim_ux.set_isol_if_empty()
    joachim_ux._admin.save_contract_to_depot(america_cx)
    assert joachim_ux.get_isol().get_member(america_cx._owner) is None
    america_digest_path = (
        f"{joachim_ux._admin._contracts_digest_dir}/{america_cx._owner}.json"
    )
    assert os_path.exists(america_digest_path) is False

    # WHEN
    assignment_text = "assignment"
    joachim_ux._set_depotlink(america_cx._owner, link_type=assignment_text)

    # THEN
    assert (
        joachim_ux.get_isol().get_member(america_cx._owner).depotlink_type
        == assignment_text
    )
    assert os_path.exists(america_digest_path)
    digest_cx = contract_get_from_json(
        x_func_open_file(
            dest_dir=joachim_ux._admin._contracts_digest_dir,
            file_name=f"{america_cx._owner}.json",
        )
    )
    print(f"{digest_cx._owner=}")
    print(f"{len(digest_cx._idea_dict)=}")
    digest_cx.set_contract_metrics()
    assert len(digest_cx._idea_dict) == 9
    assert digest_cx._owner == joachim_text


def test_ownerunit_del_depot_contract_CorrectlyDeletesObj(owner_dir_setup_cleanup):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_owner_dir()
    bob_cx = ownerunit_shop(bob_text, env_dir, get_temp_economy_title())
    yao_text = "Yao"
    create_contract_file(bob_cx._admin._contracts_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_cx._set_depotlinks_empty_if_null()
    bob_cx._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_cx._isol._members.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_member(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_cx.del_depot_contract(contract_owner=yao_text)

    # THEN
    assert list(bob_cx._isol._members.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_member(yao_text).depotlink_type is None


def test_ownerunit_del_depot_contract_CorrectlyDeletesBlindTrustFile(
    owner_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_owner_dir()
    bob_cx = ownerunit_shop(bob_text, env_dir, get_temp_economy_title())
    lai_text = "Lai"
    create_contract_file(bob_cx._admin._contracts_depot_dir, lai_text)
    bob_cx.set_isol_if_empty()
    bob_cx._set_depotlink(lai_text, link_type="blind_trust")
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_depot_dir) == 1
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_digest_dir) == 1

    # WHEN
    bob_cx.del_depot_contract(contract_owner=lai_text)

    # THEN
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_depot_dir) == 0
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_digest_dir) == 0


def test_ownerunit_set_depot_contract_SavesFileCorrectly(
    owner_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_owner_dir()
    bob_cx = ownerunit_shop(bob_text, env_dir, get_temp_economy_title())
    cal1 = get_2node_contract()
    assert (
        x_func_count_files(bob_cx._admin._contracts_depot_dir) is None
    )  # dir does not exist

    # WHEN
    bob_cx.set_isol_if_empty()
    bob_cx.set_depot_contract(contract_x=cal1, depotlink_type="blind_trust")

    # THEN
    print(f"Saving to {bob_cx._admin._contracts_depot_dir=}")
    # for path_x in os_scandir(ux._admin._contracts_depot_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(bob_cx._admin._contracts_depot_dir) == 1


def test_ownerunit_delete_ignore_depotlink_CorrectlyDeletesObj(
    owner_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_owner_dir()
    bob_cx = ownerunit_shop(bob_text, env_dir, get_temp_economy_title())
    yao_text = "Yao"
    create_contract_file(bob_cx._admin._contracts_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_cx.set_isol_if_empty()
    bob_cx._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_cx._isol._members.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_member(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_cx.del_depot_contract(contract_owner=yao_text)

    # THEN
    assert list(bob_cx._isol._members.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_member(yao_text).depotlink_type is None


def test_ownerunit_del_depot_contract_CorrectlyDoesNotDeletesIgnoreFile(
    owner_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    env_dir = get_temp_owner_dir()
    bob_cx = ownerunit_shop(bob_text, env_dir, get_temp_economy_title())
    zia_text = "Zia"
    create_contract_file(bob_cx._admin._contracts_depot_dir, zia_text)
    bob_cx.set_isol_if_empty()
    bob_cx._set_depotlink(zia_text, link_type="ignore")
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_depot_dir) == 1
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_digest_dir) == 1
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_ignore_dir) == 1

    # WHEN
    bob_cx.del_depot_contract(contract_owner=zia_text)

    # THEN
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_depot_dir) == 0
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_digest_dir) == 0
    assert x_func_count_files(dir_path=bob_cx._admin._contracts_ignore_dir) == 1


def test_ownerunit_set_ignore_contract_file_CorrectlyUpdatesIgnoreFile(
    owner_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_owner_dir()
    bob_ux = ownerunit_shop(bob_text, env_dir, get_temp_economy_title())
    zia_text = "Zia"
    create_contract_file(bob_ux._admin._contracts_depot_dir, zia_text)
    bob_ux.set_isol_if_empty()
    bob_ux._set_depotlink(zia_text, link_type="ignore")
    assert x_func_count_files(dir_path=bob_ux._admin._contracts_ignore_dir) == 1
    cx1 = bob_ux._admin.open_ignore_contract(owner=zia_text)
    assert len(cx1._members) == 0
    cx1.add_memberunit(name="tim")
    assert len(cx1._members) == 1

    # WHEN
    zia_contract = ContractUnit(_owner=zia_text)
    bob_ux.set_ignore_contract_file(zia_contract, src_contract_owner=None)

    # THEN
    cx2 = bob_ux._admin.open_ignore_contract(owner=zia_text)
    assert len(cx2._members) == 0
    assert x_func_count_files(dir_path=bob_ux._admin._contracts_ignore_dir) == 1


def test_ownerunit_refresh_depotlinks_CorrectlyPullsAllPublicContracts(
    owner_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_owner_dir()
    economy_title = get_temp_env_title()
    sx = economyunit_shop(title=economy_title, economys_dir=env_dir)
    yao_text = "Yao"
    sx.create_new_ownerunit(owner_name=yao_text)
    yao_contract = sx.get_owner_obj(name=yao_text)
    assert len(yao_contract._admin.get_remelded_output_contract().get_idea_list()) == 1

    ernie_text = "ernie"
    ernie_contract = get_cal2nodes(_owner=ernie_text)
    steve_text = "steve"
    old_steve_contract = get_cal2nodes(_owner=steve_text)
    sx.save_public_contract(contract_x=ernie_contract)
    sx.save_public_contract(contract_x=old_steve_contract)
    yao_contract.set_depot_contract(
        contract_x=ernie_contract, depotlink_type="blind_trust"
    )
    yao_contract.set_depot_contract(
        contract_x=old_steve_contract, depotlink_type="blind_trust"
    )

    assert len(yao_contract._admin.get_remelded_output_contract().get_idea_list()) == 4
    new_steve_contract = get_cal3nodes(_owner=steve_text)
    sx.save_public_contract(contract_x=new_steve_contract)
    print(f"{env_dir=} {yao_contract._admin._contracts_public_dir=}")
    # for file_name in x_func_dir_files(dir_path=env_dir):
    #     print(f"{bob_cx._admin._contracts_public_dir=} {file_name=}")

    # for file_name in x_func_dir_files(dir_path=bob_cx._admin._contracts_public_dir):
    #     print(f"{bob_cx._admin._contracts_public_dir=} {file_name=}")

    # WHEN
    yao_contract.refresh_depot_contracts()

    # THEN
    assert len(yao_contract._admin.get_remelded_output_contract().get_idea_list()) == 5
