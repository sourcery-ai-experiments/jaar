from src.economy.actor import actorunit_shop
from src.contract.contract import ContractUnit
from src.contract.examples.example_contracts import (
    get_contract_with_4_levels as example_contracts_get_contract_with_4_levels,
)
import src.economy.examples.example_actors as example_actors
from src.economy.examples.actor_env_kit import (
    actor_dir_setup_cleanup,
    get_temp_actor_dir,
)
from src.contract.road import get_default_economy_root_label as root_label
from src.contract.origin import originunit_shop
from os import path as os_path
from src.contract.x_func import (
    open_file as x_func_open_file,
    count_files as x_func_count_files,
)
from pytest import raises as pytest_raises


# def test_actor_save_isol_contract_CreateStartingContractFile(
#     actor_dir_setup_cleanup,
# ):
#     # GIVEN
#     lai_name = "Lai"
#     env_dir = get_temp_actor_dir()
#     lai_contract = actorunit_shop(name=lai_name, env_dir=env_dir)
#     lai_isol_file_name = lai_contract._admin._isol_file_name
#     with pytest_raises(Exception) as excinfo:
#         x_func_open_file(lai_contract._admin._actor_dir, lai_isol_file_name)
#     assert (
#         str(excinfo.value)
#         == f"Could not load file {lai_contract._admin._isol_file_path} (2, 'No such file or directory')"
#     )

#     # WHEN
#     lai_contract._admin.save_isol_contract(
#         contract_x=example_contracts_get_contract_with_4_levels()
#     )

#     # THEN
#     assert x_func_open_file(lai_contract._admin._actor_dir, lai_isol_file_name) != None


def test_actoropen_isol_contract_WhenStartingContractFileDoesNotExists(
    actor_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    env_dir = get_temp_actor_dir()
    ux = actorunit_shop(name=tim_text, env_dir=env_dir)

    # WHEN
    assert ux._admin.open_isol_contract() != None
    isol_contract = ux._admin.open_isol_contract()

    # THEN
    x_contract = ContractUnit(_owner=tim_text)
    x_contract.set_contract_metrics()
    # x_idearoot = IdeaRoot(_label=p_name, _walk="")
    # x_idearoot.set_grouplines_empty_if_null()
    # x_idearoot.set_kids_empty_if_null()
    # x_idearoot.set_grouplink_empty_if_null()
    # x_idearoot.set_groupheir_empty_if_null()
    # x_idearoot.set_requiredunits_empty_if_null()
    # x_idearoot.set_requiredheirs_empty_if_null()
    # x_idearoot._contract_importance = 1
    # x_idearoot._level = 0
    # x_idearoot._ancestor_promise_count = 0
    # x_idearoot._descendant_promise_count = 0
    # x_idearoot._all_member_credit = True
    # x_idearoot._all_member_debt = True

    assert isol_contract._idearoot == x_contract._idearoot
    assert isol_contract._idearoot._acptfactunits == {}
    assert list(isol_contract._members.keys()) == [tim_text]
    assert list(isol_contract._groups.keys()) == [tim_text]


def test_actor_save_isol_contract_IsolContractOwnerMustBeActor(
    actor_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_actor_dir()
    ux = actorunit_shop(name=p_name, env_dir=env_dir)
    cx1 = example_contracts_get_contract_with_4_levels()
    assert cx1._owner != p_name

    # WHEN
    ux._admin.save_isol_contract(contract_x=cx1)

    # THEN
    assert ux._admin.open_isol_contract()._owner == ux._admin._actor_name


def test_actor_open_isol_contract_WhenStartingContractFileExists(
    actor_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_actor_dir()
    ux = actorunit_shop(name=p_name, env_dir=env_dir)
    ux._admin.save_isol_contract(
        contract_x=example_contracts_get_contract_with_4_levels()
    )

    # WHEN
    assert ux._admin.open_isol_contract() != None
    isol_contract = ux._admin.open_isol_contract()

    # THEN
    x_contract = example_contracts_get_contract_with_4_levels()
    x_contract.set_owner(new_owner=p_name)
    x_contract.set_contract_metrics()

    assert isol_contract._idearoot._kids == x_contract._idearoot._kids
    assert isol_contract._idearoot == x_contract._idearoot
    assert isol_contract._idearoot._acptfactunits == {}
    assert isol_contract._members == {}
    assert isol_contract._groups == {}
    assert isol_contract._owner == ux._admin._actor_name


def test_actor_erase_isol_contract_file_DeletesFileCorrectly(
    actor_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_actor_dir()
    ux = actorunit_shop(name=p_name, env_dir=env_dir)
    ux._admin.save_isol_contract(example_contracts_get_contract_with_4_levels())
    file_name = ux._admin._isol_file_name
    assert x_func_open_file(ux._admin._actor_dir, file_name) != None

    # WHEN
    ux._admin.erase_isol_contract_file()

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_func_open_file(ux._admin._actor_dir, file_name)
    assert (
        str(excinfo.value)
        == f"Could not load file {ux._admin._actor_dir}/isol_contract.json (2, 'No such file or directory')"
    )


def test_actorunit_save_contract_to_digest_SavesFileCorrectly(
    actor_dir_setup_cleanup,
):
    # GIVEN
    actor_name = "actor1"
    env_dir = get_temp_actor_dir()
    ux = actorunit_shop(name=actor_name, env_dir=env_dir)
    ux.create_core_dir_and_files()
    cx = example_actors.get_2node_contract()
    src_contract_owner = cx._owner
    assert x_func_count_files(ux._admin._contracts_digest_dir) == 0

    # WHEN
    ux._admin.save_contract_to_digest(cx, src_contract_owner=src_contract_owner)

    # THEN
    cx_file_name = f"{cx._owner}.json"
    digest_file_path = f"{ux._admin._contracts_digest_dir}/{cx_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(ux._admin._contracts_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(ux._admin._contracts_digest_dir) == 1
    digest_cx_json = x_func_open_file(
        dest_dir=ux._admin._contracts_digest_dir,
        file_name=f"{src_contract_owner}.json",
    )
    assert digest_cx_json == cx.get_json()


def test_presonunit__set_depotlink_CorrectlySets_blind_trust_DigestContract(
    actor_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_actor_dir()
    sue_cx = actorunit_shop(name=sue_text, env_dir=env_dir)
    sue_cx.create_core_dir_and_files()
    cx = example_actors.get_2node_contract()
    src_contract_owner = cx._owner
    assert x_func_count_files(sue_cx._admin._contracts_digest_dir) == 0

    # WHEN
    sue_cx.set_depot_contract(contract_x=cx, depotlink_type="blind_trust")

    # THEN
    cx_file_name = f"{cx._owner}.json"
    digest_file_path = f"{sue_cx._admin._contracts_digest_dir}/{cx_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(sue_cx._admin._contracts_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(sue_cx._admin._contracts_digest_dir) == 1
    digest_cx_json = x_func_open_file(
        dest_dir=sue_cx._admin._contracts_digest_dir,
        file_name=f"{src_contract_owner}.json",
    )
    assert digest_cx_json == cx.get_json()


def test_actor_get_remelded_output_contract_withEmptyDigestDict(
    actor_dir_setup_cleanup,
):
    # GIVEN
    actor_name_x = "boots3"
    ux = actorunit_shop(name=actor_name_x, env_dir=get_temp_actor_dir())
    ux.create_core_dir_and_files()
    sx_output_before = ux._admin.get_remelded_output_contract()
    assert str(type(sx_output_before)).find(".contract.ContractUnit'>")
    assert sx_output_before._owner == actor_name_x
    assert sx_output_before._idearoot._label == root_label()
    # ux.set_digested_contract(contract_x=ContractUnit(_owner="digested1"))

    # WHEN
    sx_output_after = ux._admin.get_remelded_output_contract()

    # THEN
    actor_contract_x = ContractUnit(_owner=actor_name_x, _weight=0.0)
    actor_contract_x._idearoot._walk = ""
    actor_contract_x.set_contract_metrics()

    assert str(type(sx_output_after)).find(".contract.ContractUnit'>")
    assert sx_output_after._weight == actor_contract_x._weight
    assert sx_output_after._idearoot._walk == actor_contract_x._idearoot._walk
    assert (
        sx_output_after._idearoot._acptfactunits
        == actor_contract_x._idearoot._acptfactunits
    )
    assert sx_output_after._idearoot == actor_contract_x._idearoot


def test_actor_get_remelded_output_contract_with1DigestedContract(
    actor_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_actor_dir()
    ux = actorunit_shop(name=yao_text, env_dir=env_dir)
    ux.create_core_dir_and_files()
    sx_output_old = ux._admin.get_remelded_output_contract()
    assert str(type(sx_output_old)).find(".contract.ContractUnit'>")
    assert sx_output_old._owner == yao_text
    assert sx_output_old._idearoot._label == root_label()
    input_contract = example_actors.get_2node_contract()
    input_contract.meld(input_contract)
    ux.set_depot_contract(contract_x=input_contract, depotlink_type="blind_trust")

    # WHEN
    sx_output_new = ux._admin.get_remelded_output_contract()

    # THEN
    assert str(type(sx_output_new)).find(".contract.ContractUnit'>")

    assert sx_output_new._weight == 0
    assert sx_output_new._weight != input_contract._weight
    sx_idearoot = sx_output_new._idearoot
    input_idearoot = input_contract._idearoot
    assert sx_idearoot._walk == input_idearoot._walk
    assert sx_idearoot._acptfactunits == input_idearoot._acptfactunits
    input_b_idea = input_idearoot._kids.get("B")
    sx_output_new_b_idea = sx_idearoot._kids.get("B")
    assert sx_output_new_b_idea._walk == input_b_idea._walk
    assert sx_output_new._idearoot._kids == input_contract._idearoot._kids
    assert sx_idearoot._kids_total_weight == input_idearoot._kids_total_weight
    assert sx_idearoot == input_idearoot
    assert sx_output_new._owner != input_contract._owner
    assert sx_output_new != input_contract


# def test_actor_set_digested_contract_with2Groups(actor_dir_setup_cleanup):
#     # GIVEN
#     env_dir = get_temp_actor_dir()
#     ux = actorunit_shop(name="test8", env_dir=env_dir)
#     sx_output_old = ux._admin.get_remelded_output_contract()
#     assert str(type(sx_output_old)).find(".contract.ContractUnit'>")
#     assert sx_output_old._groups == {}
#     assert sx_output_old._members == {}
#     assert sx_output_old._acptfacts == {}

#     src1 = "test1"
#     src1_road = Road(f"{src1}")
#     s1 = ContractUnit(_owner=src1)

#     ceci_text = "Ceci"
#     s1.set_memberunit(memberunit=MemberUnit(name=ceci_text))
#     swim_text = "swimmers"
#     swim_group = BraUnit(name=swim_text)
#     swim_group.set_memberlink(memberlink=memberlink_shop(name=ceci_text))
#     s1.set_groupunit(groupunit=swim_group)

#     yaya_text = "yaya"
#     yaya_road = Road(f"{src1},{yaya_text}")
#     s1.add_idea(idea_kid=IdeaKid(_label=yaya_text), walk=src1_road)
#     s1.set_acptfact(base=yaya_road, acptfact=yaya_road)

#     assert s1._groups.get(swim_text).name == swim_text
#     assert s1._members.get(ceci_text).name == ceci_text
#     assert s1._idearoot._label == src1
#     assert s1._acptfacts.get(yaya_road).base == yaya_road

#     # WHEN
#     ux.set_single_digested_contract(_contract_owner="test1", digest_contract_x=s1)
#     sx_output_new = ux._admin.get_remelded_output_contract()

#     # THEN
#     assert str(type(sx_output_new)).find(".contract.ContractUnit'>")
#     assert sx_output_new._acptfacts == s1._acptfacts
#     assert sx_output_new._members == s1._members
#     assert sx_output_new._groups == s1._groups
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._idearoot._walk == s1._idearoot._walk
#     assert sx_output_new._idearoot._acptfactunits == s1._idearoot._acptfactunits
#     assert sx_output_new._idearoot._kids == s1._idearoot._kids
#     assert sx_output_new._idearoot._kids_total_weight == s1._idearoot._kids_total_weight
#     assert sx_output_new._idearoot == s1._idearoot
#     assert sx_output_new._label != s1._label
#     assert sx_output_new != s1


def test_actor_isol_contract_CorrectlysHasOriginLinksWithOwnerAsSource(
    actor_dir_setup_cleanup,
):
    # GIVEN
    # actorunit with isol_contract and no other depot contracts
    yao_text = "Yao"
    isol_origin_weight = 1
    yao_originunit = originunit_shop()
    yao_originunit.set_originlink(name=yao_text, weight=isol_origin_weight)
    isol_contract_x = example_actors.get_7nodeJRoot_contract()
    isol_contract_x.set_owner(yao_text)

    assert isol_contract_x._idearoot._originunit == originunit_shop()
    assert isol_contract_x._idearoot._originunit != yao_originunit

    ux = actorunit_shop(name=yao_text, env_dir=get_temp_actor_dir())
    ux.create_core_dir_and_files()
    ux._admin.save_isol_contract(contract_x=isol_contract_x)

    # WHEN
    output_contract_x = ux._admin.get_remelded_output_contract()

    # THEN
    assert output_contract_x._idearoot._originunit == originunit_shop()
    d_road = "J,A,C,D"
    d_idea = output_contract_x.get_idea_kid(road=d_road)
    assert d_idea._originunit == yao_originunit

    print(f"{output_contract_x._originunit=}")
    assert output_contract_x._originunit == yao_originunit

    output_originlink = output_contract_x._originunit._links.get(yao_text)
    assert output_originlink.name == yao_text
    assert output_originlink.weight == isol_origin_weight
