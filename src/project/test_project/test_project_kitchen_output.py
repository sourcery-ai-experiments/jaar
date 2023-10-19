from src.deal.examples.example_deals import (
    deal_v002 as ex_deal_v002,
)
from src.project.project import projectunit_shop
from src.project.examples.example_kitchens import (
    get_6node_deal as example_healers_get_6node_deal,
    get_deal_2CleanNodesRandomWeights,
    get_deal_3CleanNodesRandomWeights,
)
from src.project.examples.project_env_kit import (
    get_temp_env_handle,
    get_test_projects_dir,
    env_dir_setup_cleanup,
)


def test_project_get_output_deal_ReturnsCorrectDealObjScenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_project = projectunit_shop(get_temp_env_handle(), get_test_projects_dir())
    x_project.create_dirs_if_null(in_memory_bank=True)
    input_deal = example_healers_get_6node_deal()
    x_project.save_public_deal(input_deal)
    # x_project.save_public_deal(ex_cxs_get_deal_1Task_1CE0MinutesRequired_1AcptFact())
    # x_project.save_public_deal(ex_cxs_deal_v001())
    xia_text = "Xia"
    x_project.create_new_kitchenunit(kitchen_title=xia_text)
    x_project.set_healer_depotlink(
        xia_text, input_deal._healer, depotlink_type="blind_trust"
    )
    x_project.save_kitchenunit_file(kitchen_title=xia_text)
    xia_healer = x_project.get_kitchenunit(title=xia_text)
    # print(f"{xia_healer._seed._partys.keys()=}")

    # WHEN
    output_deal = x_project.get_output_deal(kitchen_title=xia_text)
    # input deal must be melded to itself to create originunits
    input_deal.meld(input_deal)
    input_deal.set_healer(new_healer=xia_text)
    input_deal._originunit.set_originlink(title=xia_text, weight=1)

    # THEN
    a_text = "A"
    c_text = "C"
    c_road = f"{input_deal._project_handle},{c_text}"
    d_text = "D"
    d_road = f"{c_road},{d_text}"
    print(f"{output_deal._healer=}")
    print(f"{output_deal._idea_dict.keys()=}")
    output_deal_d_idea = output_deal.get_idea_kid(d_road)
    # print(f" {output_deal_d_idea._weight=} {len(input_deal._idearoot._kids)=} ")
    assert output_deal != None
    assert len(input_deal._idearoot._kids) == 2
    # idea_a = output_deal.get_idea_kid(road="A")
    # idea_b = output_deal.get_idea_kid(road="B")
    # for idea_kid_x1 in input_deal._idearoot._kids.values():
    #     print(f"{idea_kid_x1._label=}")
    #     output_deal_counterpart_x1 = output_deal._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_deal_counterpart_x2 = output_deal_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_deal_counterpart_x2._weight=}"
    #         )
    #         # assert output_deal_counterpart_x2 == idea_kid_x2
    #         assert output_deal_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_deal_counterpart_x1._weight=}"
    #     )
    #     assert output_deal_counterpart_x1._label == idea_kid_x1._label
    # assert output_deal._idearoot._kids == input_deal._idearoot._kids
    assert output_deal._idearoot._acptfactunits == {}
    assert output_deal._idearoot._acptfactunits == input_deal._idearoot._acptfactunits
    assert list(output_deal._partys.keys()) == [xia_text, a_text]
    assert output_deal._partys != input_deal._partys
    assert list(output_deal._groups.keys()) == [xia_text, a_text]
    assert output_deal._groups != input_deal._groups
    print(f"{output_deal._originunit=}")
    print(f"{input_deal._originunit=}")
    assert output_deal._originunit == input_deal._originunit

    b_text = "B"
    print(f"{output_deal._idearoot._kids.get(b_text)._originunit=}")
    print(f"{input_deal._idearoot._kids.get(b_text)._originunit=}")
    assert output_deal._idearoot == input_deal._idearoot


def test_project_get_output_deal_ReturnsCorrectDealObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_project = projectunit_shop(get_temp_env_handle(), get_test_projects_dir())
    x_project.create_dirs_if_null(in_memory_bank=True)
    x1_deal = example_healers_get_6node_deal()
    x2_deal = ex_deal_v002()

    x_project.save_public_deal(x1_deal)
    x_project.save_public_deal(x2_deal)
    # x_project.save_public_deal(ex_cxs_get_deal_1Task_1CE0MinutesRequired_1AcptFact())
    # x_project.save_public_deal(ex_cxs_deal_v001())
    xia_text = "Xia"
    x_project.create_new_kitchenunit(kitchen_title=xia_text)
    x_project.set_healer_depotlink(xia_text, x1_deal._healer, "blind_trust")
    x_project.set_healer_depotlink(xia_text, x2_deal._healer, "blind_trust")
    x_project.save_kitchenunit_file(kitchen_title=xia_text)
    xia_healer = x_project.get_kitchenunit(title=xia_text)
    print(f"{xia_healer._seed._partys.keys()=}")

    # WHEN
    output_deal = x_project.get_output_deal(kitchen_title=xia_text)

    # THEN
    output_deal_d_road = f"{output_deal._project_handle},C,D"
    output_deal_d_idea = output_deal.get_idea_kid(output_deal_d_road)
    print(f" {output_deal_d_idea._weight=} ")
    assert output_deal != None
    # for idea_kid_x1 in x1_deal._idearoot._kids.values():
    #     output_deal_counterpart_x1 = output_deal._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_deal_counterpart_x2 = output_deal_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_deal_counterpart_x2._weight=}"
    #         )
    #         # assert output_deal_counterpart_x2 == idea_kid_x2
    #         assert output_deal_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_deal_counterpart_x1._weight=}"
    #     )
    #     assert output_deal_counterpart_x1._label == idea_kid_x1._label
    # assert output_deal._idearoot._kids == x1_deal._idearoot._kids
    assert len(output_deal._idearoot._acptfactunits) == 9
    assert len(output_deal._idearoot._acptfactunits) == len(
        x2_deal._idearoot._acptfactunits
    )
    assert len(output_deal._partys) == 25
    assert len(output_deal._partys) == len(x2_deal._partys) + 2 + 1
    assert len(output_deal._groups) == 37
    assert len(output_deal._groups) == len(x2_deal._groups) + 2 + 1
    assert output_deal._idearoot != x1_deal._idearoot
    assert output_deal._idearoot != x2_deal._idearoot


def test_kitchenunit_refresh_depotlinks_CorrectlyPullsAllPublicDeals(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_test_projects_dir()
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(handle=project_handle, projects_dir=env_dir)
    x_project.create_dirs_if_null(in_memory_bank=True)
    # ux = kitchenunit_shop(title=healer1_text, env_dir=env_dir)

    ernie_text = "ernie"
    jessi_text = "jessi"
    steve_text = "steve"
    ernie_deal = get_deal_2CleanNodesRandomWeights(_healer=ernie_text)
    jessi_deal = get_deal_2CleanNodesRandomWeights(_healer=jessi_text)
    old_steve_deal = get_deal_2CleanNodesRandomWeights(_healer=steve_text)
    x_project.save_public_deal(x_deal=ernie_deal)
    x_project.save_public_deal(x_deal=jessi_deal)
    x_project.save_public_deal(x_deal=old_steve_deal)
    x_project.create_new_kitchenunit(kitchen_title=ernie_text)
    x_project.create_new_kitchenunit(kitchen_title=jessi_text)
    # x_project.create_new_kitchenunit(kitchen_title=steve_text)
    ux_ernie = x_project.get_kitchenunit(title=ernie_text)
    ux_jessi = x_project.get_kitchenunit(title=jessi_text)
    # ux_steve = x_project.get_kitchenunit(title=steve_text)
    ux_ernie.set_depot_deal(x_deal=jessi_deal, depotlink_type="blind_trust")
    ux_ernie.set_depot_deal(x_deal=old_steve_deal, depotlink_type="blind_trust")
    ux_jessi.set_depot_deal(x_deal=ernie_deal, depotlink_type="blind_trust")
    ux_jessi.set_depot_deal(x_deal=old_steve_deal, depotlink_type="blind_trust")
    # ux_steve.set_depot_deal(x_deal=ernie_deal, depotlink_type="blind_trust")
    # ux_steve.set_depot_deal(x_deal=jessi_deal, depotlink_type="blind_trust")
    assert len(ux_ernie._admin.get_remelded_output_deal().get_idea_list()) == 4
    assert len(ux_jessi._admin.get_remelded_output_deal().get_idea_list()) == 4
    # assert len(ux_steve._admin.get_remelded_output_deal().get_idea_list()) == 4
    new_steve_deal = get_deal_3CleanNodesRandomWeights(_healer="steve")
    x_project.save_public_deal(x_deal=new_steve_deal)
    # print(f"{env_dir=} {ux._admin._deals_public_dir=}")
    # for file_title in x_func_dir_files(dir_path=env_dir):
    #     print(f"{ux._admin._deals_public_dir=} {file_title=}")

    # for file_title in x_func_dir_files(dir_path=ux._admin._deals_public_dir):
    #     print(f"{ux._admin._deals_public_dir=} {file_title=}")

    # WHEN
    x_project.reload_all_kitchenunits_src_dealunits()

    # THEN
    assert len(ux_ernie._admin.get_remelded_output_deal().get_idea_list()) == 5
    assert len(ux_jessi._admin.get_remelded_output_deal().get_idea_list()) == 5
