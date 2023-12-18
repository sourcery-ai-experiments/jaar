from src.agenda.examples.example_agendas import (
    agenda_v002 as ex_agenda_v002,
)
from src.culture.culture import cultureunit_shop
from src.culture.examples.example_councils import (
    get_6node_agenda as example_healers_get_6node_agenda,
    get_agenda_2CleanNodesRandomWeights,
    get_agenda_3CleanNodesRandomWeights,
)
from src.culture.examples.culture_env_kit import (
    get_temp_env_culture_id,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)


def test_culture_get_output_agenda_ReturnsCorrectAgendaObjScenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_culture_id(), get_test_cultures_dir())
    input_agenda = example_healers_get_6node_agenda()
    x_culture.save_public_agenda(input_agenda)
    # x_culture.save_public_agenda(ex_cxs_get_agenda_1Task_1CE0MinutesRequired_1AcptFact())
    # x_culture.save_public_agenda(ex_cxs_agenda_v001())
    xia_text = "Xia"
    x_culture.create_new_councilunit(council_cid=xia_text)
    x_culture.set_healer_depotlink(
        xia_text, input_agenda._healer, depotlink_type="blind_trust"
    )
    x_culture.save_councilunit_file(council_cid=xia_text)
    xia_healer = x_culture.get_councilunit(cid=xia_text)
    # print(f"{xia_healer._seed._partys.keys()=}")

    # WHEN
    output_agenda = x_culture.get_output_agenda(council_cid=xia_text)
    # input agenda must be melded to itself to create originunits
    input_agenda.meld(input_agenda)
    input_agenda.set_healer(new_healer=xia_text)
    input_agenda._originunit.set_originlink(pid=xia_text, weight=1)

    # THEN
    a_text = "A"
    c_text = "C"
    c_road = f"{input_agenda._culture_id},{c_text}"
    d_text = "D"
    d_road = f"{c_road},{d_text}"
    print(f"{output_agenda._healer=}")
    print(f"{output_agenda._idea_dict.keys()=}")
    output_agenda_d_idea = output_agenda.get_idea_kid(d_road)
    # print(f" {output_agenda_d_idea._weight=} {len(input_agenda._idearoot._kids)=} ")
    assert output_agenda != None
    assert len(input_agenda._idearoot._kids) == 2
    # idea_a = output_agenda.get_idea_kid("A")
    # idea_b = output_agenda.get_idea_kid("B")
    # for idea_kid_x1 in input_agenda._idearoot._kids.values():
    #     print(f"{idea_kid_x1._label=}")
    #     output_agenda_counterpart_x1 = output_agenda._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_agenda_counterpart_x2 = output_agenda_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_agenda_counterpart_x2._weight=}"
    #         )
    #         # assert output_agenda_counterpart_x2 == idea_kid_x2
    #         assert output_agenda_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_agenda_counterpart_x1._weight=}"
    #     )
    #     assert output_agenda_counterpart_x1._label == idea_kid_x1._label
    # assert output_agenda._idearoot._kids == input_agenda._idearoot._kids
    assert output_agenda._idearoot._acptfactunits == {}
    assert (
        output_agenda._idearoot._acptfactunits == input_agenda._idearoot._acptfactunits
    )
    assert list(output_agenda._partys.keys()) == [xia_text, a_text]
    assert output_agenda._partys != input_agenda._partys
    assert list(output_agenda._groups.keys()) == [xia_text, a_text]
    assert output_agenda._groups != input_agenda._groups
    print(f"{output_agenda._originunit=}")
    print(f"{input_agenda._originunit=}")
    assert output_agenda._originunit == input_agenda._originunit

    b_text = "B"
    print(f"{output_agenda._idearoot._kids.get(b_text)._originunit=}")
    print(f"{input_agenda._idearoot._kids.get(b_text)._originunit=}")
    assert output_agenda._idearoot == input_agenda._idearoot


def test_culture_get_output_agenda_ReturnsCorrectAgendaObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_culture_id(), get_test_cultures_dir())
    x1_agenda = example_healers_get_6node_agenda()
    x2_agenda = ex_agenda_v002()

    x_culture.save_public_agenda(x1_agenda)
    x_culture.save_public_agenda(x2_agenda)
    # x_culture.save_public_agenda(ex_cxs_get_agenda_1Task_1CE0MinutesRequired_1AcptFact())
    # x_culture.save_public_agenda(ex_cxs_agenda_v001())
    xia_text = "Xia"
    x_culture.create_new_councilunit(council_cid=xia_text)
    x_culture.set_healer_depotlink(xia_text, x1_agenda._healer, "blind_trust")
    x_culture.set_healer_depotlink(xia_text, x2_agenda._healer, "blind_trust")
    x_culture.save_councilunit_file(council_cid=xia_text)
    xia_healer = x_culture.get_councilunit(cid=xia_text)
    print(f"{xia_healer._seed._partys.keys()=}")

    # WHEN
    output_agenda = x_culture.get_output_agenda(council_cid=xia_text)

    # THEN
    output_agenda_d_road = f"{output_agenda._culture_id},C,D"
    output_agenda_d_idea = output_agenda.get_idea_kid(output_agenda_d_road)
    print(f" {output_agenda_d_idea._weight=} ")
    assert output_agenda != None
    # for idea_kid_x1 in x1_agenda._idearoot._kids.values():
    #     output_agenda_counterpart_x1 = output_agenda._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_agenda_counterpart_x2 = output_agenda_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_agenda_counterpart_x2._weight=}"
    #         )
    #         # assert output_agenda_counterpart_x2 == idea_kid_x2
    #         assert output_agenda_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_agenda_counterpart_x1._weight=}"
    #     )
    #     assert output_agenda_counterpart_x1._label == idea_kid_x1._label
    # assert output_agenda._idearoot._kids == x1_agenda._idearoot._kids
    assert len(output_agenda._idearoot._acptfactunits) == 9
    assert len(output_agenda._idearoot._acptfactunits) == len(
        x2_agenda._idearoot._acptfactunits
    )
    assert len(output_agenda._partys) == 25
    assert len(output_agenda._partys) == len(x2_agenda._partys) + 2 + 1
    assert len(output_agenda._groups) == 37
    assert len(output_agenda._groups) == len(x2_agenda._groups) + 2 + 1
    assert output_agenda._idearoot != x1_agenda._idearoot
    assert output_agenda._idearoot != x2_agenda._idearoot


def test_councilunit_refresh_depotlinks_CorrectlyPullsAllPublicAgendas(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_test_cultures_dir()
    culture_id = get_temp_env_culture_id()
    x_culture = cultureunit_shop(culture_id=culture_id, cultures_dir=env_dir)
    x_culture.create_dirs_if_null(in_memory_treasury=True)
    # ux = councilunit_shop(pid=healer1_text, env_dir=env_dir)

    ernie_text = "ernie"
    jessi_text = "jessi"
    steve_text = "steve"
    ernie_agenda = get_agenda_2CleanNodesRandomWeights(_healer=ernie_text)
    jessi_agenda = get_agenda_2CleanNodesRandomWeights(_healer=jessi_text)
    old_steve_agenda = get_agenda_2CleanNodesRandomWeights(_healer=steve_text)
    x_culture.save_public_agenda(ernie_agenda)
    x_culture.save_public_agenda(jessi_agenda)
    x_culture.save_public_agenda(old_steve_agenda)
    x_culture.create_new_councilunit(council_cid=ernie_text)
    x_culture.create_new_councilunit(council_cid=jessi_text)
    # x_culture.create_new_councilunit(council_cid=steve_text)
    ux_ernie = x_culture.get_councilunit(cid=ernie_text)
    ux_jessi = x_culture.get_councilunit(cid=jessi_text)
    # ux_steve = x_culture.get_councilunit(cid=steve_text)
    ux_ernie.set_depot_agenda(x_agenda=jessi_agenda, depotlink_type="blind_trust")
    ux_ernie.set_depot_agenda(x_agenda=old_steve_agenda, depotlink_type="blind_trust")
    ux_jessi.set_depot_agenda(x_agenda=ernie_agenda, depotlink_type="blind_trust")
    ux_jessi.set_depot_agenda(x_agenda=old_steve_agenda, depotlink_type="blind_trust")
    # ux_steve.set_depot_agenda(x_agenda=ernie_agenda, depotlink_type="blind_trust")
    # ux_steve.set_depot_agenda(x_agenda=jessi_agenda, depotlink_type="blind_trust")
    assert len(ux_ernie.get_remelded_output_agenda().get_idea_list()) == 4
    assert len(ux_jessi.get_remelded_output_agenda().get_idea_list()) == 4
    # assert len(ux_steve.get_remelded_output_agenda().get_idea_list()) == 4
    new_steve_agenda = get_agenda_3CleanNodesRandomWeights(_healer="steve")
    x_culture.save_public_agenda(new_steve_agenda)
    # print(f"{env_dir=} {ux._agendas_public_dir=}")
    # for file_name in x_func_dir_files(dir_path=env_dir):
    #     print(f"{ux._agendas_public_dir=} {file_name=}")

    # for file_name in x_func_dir_files(dir_path=ux._agendas_public_dir):
    #     print(f"{ux._agendas_public_dir=} {file_name=}")

    # WHEN
    x_culture.reload_all_councilunits_src_agendaunits()

    # THEN
    assert len(ux_ernie.get_remelded_output_agenda().get_idea_list()) == 5
    assert len(ux_jessi.get_remelded_output_agenda().get_idea_list()) == 5
