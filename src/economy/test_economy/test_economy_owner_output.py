from src.contract.examples.example_contracts import (
    contract_v002 as ex_cxs_contract_v002,
)
from src.economy.economy import economyunit_shop
from src.economy.examples.example_owners import (
    get_6node_contract as example_owners_get_6node_contract,
    get_contract_2CleanNodesRandomWeights,
    get_contract_3CleanNodesRandomWeights,
)
from src.economy.examples.economy_env_kit import (
    get_temp_env_tag,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)


def test_economy_get_output_contract_ReturnsCorrectContractObjScenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = economyunit_shop(tag=get_temp_env_tag(), economys_dir=get_test_economys_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    input_cx = example_owners_get_6node_contract()
    sx.save_public_contract(input_cx)
    # sx.save_public_contract(ex_cxs_get_contract_1Task_1CE0MinutesRequired_1AcptFact())
    # sx.save_public_contract(ex_cxs_contract_v001())
    xia_text = "Xia"
    sx.create_new_ownerunit(owner_name=xia_text)
    sx.set_owner_depotlink(xia_text, input_cx._owner, depotlink_type="blind_trust")
    sx.save_owner_file(owner_name=xia_text)
    xia_owner = sx.get_owner_obj(name=xia_text)
    # print(f"{xia_owner._isol._partys.keys()=}")

    # WHEN
    output_cx = sx.get_output_contract(owner_name=xia_text)
    # input contract must be melded to itself to create originunits
    input_cx.meld(input_cx)
    input_cx.set_owner(new_owner=xia_text)
    input_cx._originunit.set_originlink(name=xia_text, weight=1)

    # THEN
    a_text = "A"
    c_text = "C"
    c_road = f"{input_cx._economy_tag},{c_text}"
    d_text = "D"
    d_road = f"{c_road},{d_text}"
    print(f"{output_cx._owner=}")
    print(f"{output_cx._idea_dict.keys()=}")
    output_cx_d_idea = output_cx.get_idea_kid(d_road)
    # print(f" {output_cx_d_idea._weight=} {len(input_cx._idearoot._kids)=} ")
    assert output_cx != None
    assert len(input_cx._idearoot._kids) == 2
    # idea_a = output_cx.get_idea_kid(road="A")
    # idea_b = output_cx.get_idea_kid(road="B")
    # for idea_kid_x1 in input_cx._idearoot._kids.values():
    #     print(f"{idea_kid_x1._label=}")
    #     output_cx_counterpart_x1 = output_cx._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_cx_counterpart_x2 = output_cx_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_cx_counterpart_x2._weight=}"
    #         )
    #         # assert output_cx_counterpart_x2 == idea_kid_x2
    #         assert output_cx_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_cx_counterpart_x1._weight=}"
    #     )
    #     assert output_cx_counterpart_x1._label == idea_kid_x1._label
    # assert output_cx._idearoot._kids == input_cx._idearoot._kids
    assert output_cx._idearoot._acptfactunits == {}
    assert output_cx._idearoot._acptfactunits == input_cx._idearoot._acptfactunits
    assert list(output_cx._partys.keys()) == [xia_text, a_text]
    assert output_cx._partys != input_cx._partys
    assert list(output_cx._groups.keys()) == [xia_text, a_text]
    assert output_cx._groups != input_cx._groups
    print(f"{output_cx._originunit=}")
    print(f"{input_cx._originunit=}")
    assert output_cx._originunit == input_cx._originunit

    b_text = "B"
    print(f"{output_cx._idearoot._kids.get(b_text)._originunit=}")
    print(f"{input_cx._idearoot._kids.get(b_text)._originunit=}")
    assert output_cx._idearoot == input_cx._idearoot


def test_economy_get_output_contract_ReturnsCorrectContractObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = economyunit_shop(tag=get_temp_env_tag(), economys_dir=get_test_economys_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    cx1 = example_owners_get_6node_contract()
    cx2 = ex_cxs_contract_v002()

    sx.save_public_contract(cx1)
    sx.save_public_contract(cx2)
    # sx.save_public_contract(ex_cxs_get_contract_1Task_1CE0MinutesRequired_1AcptFact())
    # sx.save_public_contract(ex_cxs_contract_v001())
    xia_text = "Xia"
    sx.create_new_ownerunit(owner_name=xia_text)
    sx.set_owner_depotlink(xia_text, cx1._owner, depotlink_type="blind_trust")
    sx.set_owner_depotlink(xia_text, cx2._owner, depotlink_type="blind_trust")
    sx.save_owner_file(owner_name=xia_text)
    xia_owner = sx.get_owner_obj(name=xia_text)
    print(f"{xia_owner._isol._partys.keys()=}")

    # WHEN
    output_cx = sx.get_output_contract(owner_name=xia_text)

    # THEN
    output_cx_d_road = f"{output_cx._economy_tag},C,D"
    output_cx_d_idea = output_cx.get_idea_kid(output_cx_d_road)
    print(f" {output_cx_d_idea._weight=} ")
    assert output_cx != None
    # for idea_kid_x1 in cx1._idearoot._kids.values():
    #     output_cx_counterpart_x1 = output_cx._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_cx_counterpart_x2 = output_cx_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_cx_counterpart_x2._weight=}"
    #         )
    #         # assert output_cx_counterpart_x2 == idea_kid_x2
    #         assert output_cx_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_cx_counterpart_x1._weight=}"
    #     )
    #     assert output_cx_counterpart_x1._label == idea_kid_x1._label
    # assert output_cx._idearoot._kids == cx1._idearoot._kids
    assert len(output_cx._idearoot._acptfactunits) == 9
    assert len(output_cx._idearoot._acptfactunits) == len(cx2._idearoot._acptfactunits)
    assert len(output_cx._partys) == 25
    assert len(output_cx._partys) == len(cx2._partys) + 2 + 1
    assert len(output_cx._groups) == 37
    assert len(output_cx._groups) == len(cx2._groups) + 2 + 1
    assert output_cx._idearoot != cx1._idearoot
    assert output_cx._idearoot != cx2._idearoot


def test_ownerunit_refresh_depotlinks_CorrectlyPullsAllPublicContracts(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_test_economys_dir()
    economy_tag = get_temp_env_tag()
    sx = economyunit_shop(tag=economy_tag, economys_dir=env_dir)
    sx.create_dirs_if_null(in_memory_bank=True)
    # ux = ownerunit_shop(name=owner1_text, env_dir=env_dir)

    ernie_text = "ernie"
    jessi_text = "jessi"
    steve_text = "steve"
    ernie_contract = get_contract_2CleanNodesRandomWeights(_owner=ernie_text)
    jessi_contract = get_contract_2CleanNodesRandomWeights(_owner=jessi_text)
    old_steve_cx = get_contract_2CleanNodesRandomWeights(_owner=steve_text)
    sx.save_public_contract(contract_x=ernie_contract)
    sx.save_public_contract(contract_x=jessi_contract)
    sx.save_public_contract(contract_x=old_steve_cx)
    sx.create_new_ownerunit(owner_name=ernie_text)
    sx.create_new_ownerunit(owner_name=jessi_text)
    # sx.create_new_ownerunit(owner_name=steve_text)
    ux_ernie = sx.get_owner_obj(name=ernie_text)
    ux_jessi = sx.get_owner_obj(name=jessi_text)
    # ux_steve = sx.get_owner_obj(name=steve_text)
    ux_ernie.set_depot_contract(contract_x=jessi_contract, depotlink_type="blind_trust")
    ux_ernie.set_depot_contract(contract_x=old_steve_cx, depotlink_type="blind_trust")
    ux_jessi.set_depot_contract(contract_x=ernie_contract, depotlink_type="blind_trust")
    ux_jessi.set_depot_contract(contract_x=old_steve_cx, depotlink_type="blind_trust")
    # ux_steve.set_depot_contract(contract_x=ernie_contract, depotlink_type="blind_trust")
    # ux_steve.set_depot_contract(contract_x=jessi_contract, depotlink_type="blind_trust")
    assert len(ux_ernie._admin.get_remelded_output_contract().get_idea_list()) == 4
    assert len(ux_jessi._admin.get_remelded_output_contract().get_idea_list()) == 4
    # assert len(ux_steve._admin.get_remelded_output_contract().get_idea_list()) == 4
    new_steve_contract = get_contract_3CleanNodesRandomWeights(_owner="steve")
    sx.save_public_contract(contract_x=new_steve_contract)
    # print(f"{env_dir=} {ux._admin._contracts_public_dir=}")
    # for file_name in x_func_dir_files(dir_path=env_dir):
    #     print(f"{ux._admin._contracts_public_dir=} {file_name=}")

    # for file_name in x_func_dir_files(dir_path=ux._admin._contracts_public_dir):
    #     print(f"{ux._admin._contracts_public_dir=} {file_name=}")

    # WHEN
    sx.reload_all_owners_src_contractunits()

    # THEN
    assert len(ux_ernie._admin.get_remelded_output_contract().get_idea_list()) == 5
    assert len(ux_jessi._admin.get_remelded_output_contract().get_idea_list()) == 5
