from src.economy.economy import economyunit_shop
from src.calendar.examples.example_calendars import (
    calendar_v002 as ex_cxs_calendar_v002,
)
from src.economy.examples.example_actors import (
    get_6node_calendar as example_actors_get_6node_calendar,
    get_calendar_2CleanNodesRandomWeights,
    get_calendar_3CleanNodesRandomWeights,
)
from src.economy.examples.economy_env_kit import (
    get_temp_env_name,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)


def test_economy_get_output_calendar_ReturnsCorrectCalendarObjScenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = economyunit_shop(
        name=get_temp_env_name(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    input_cx = example_actors_get_6node_calendar()
    sx.save_public_calendar(input_cx)
    # sx.save_public_calendar(ex_cxs_get_calendar_1Task_1CE0MinutesRequired_1AcptFact())
    # sx.save_public_calendar(ex_cxs_calendar_v001())
    xia_text = "Xia"
    sx.create_new_actorunit(actor_name=xia_text)
    sx.set_actor_depotlink(xia_text, input_cx._owner, depotlink_type="blind_trust")
    sx.save_actor_file(actor_name=xia_text)
    xia_actor = sx.get_actor_obj(name=xia_text)
    # print(f"{xia_actor._isol._members.keys()=}")

    # WHEN
    output_cx = sx.get_output_calendar(actor_name=xia_text)
    # input calendar must be melded to itself to create originunits
    input_cx.meld(input_cx)
    input_cx.set_owner(new_owner=xia_text)
    input_cx._originunit.set_originlink(name=xia_text, weight=1)

    # THEN
    a_text = "A"
    c_text = "C"
    c_road = f"{a_text},{c_text}"
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
    assert list(output_cx._members.keys()) == [xia_text, a_text]
    assert output_cx._members != input_cx._members
    assert list(output_cx._groups.keys()) == [xia_text, a_text]
    assert output_cx._groups != input_cx._groups
    print(f"{output_cx._originunit=}")
    print(f"{input_cx._originunit=}")
    assert output_cx._originunit == input_cx._originunit

    b_text = "B"
    print(f"{output_cx._idearoot._kids.get(b_text)._originunit=}")
    print(f"{input_cx._idearoot._kids.get(b_text)._originunit=}")
    assert output_cx._idearoot == input_cx._idearoot


def test_economy_get_output_calendar_ReturnsCorrectCalendarObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = economyunit_shop(
        name=get_temp_env_name(), economys_dir=get_test_economys_dir()
    )
    sx.create_dirs_if_null(in_memory_bank=True)
    cx1 = example_actors_get_6node_calendar()
    cx2 = ex_cxs_calendar_v002()

    sx.save_public_calendar(cx1)
    sx.save_public_calendar(cx2)
    # sx.save_public_calendar(ex_cxs_get_calendar_1Task_1CE0MinutesRequired_1AcptFact())
    # sx.save_public_calendar(ex_cxs_calendar_v001())
    xia_text = "Xia"
    sx.create_new_actorunit(actor_name=xia_text)
    sx.set_actor_depotlink(xia_text, cx1._owner, depotlink_type="blind_trust")
    sx.set_actor_depotlink(xia_text, cx2._owner, depotlink_type="blind_trust")
    sx.save_actor_file(actor_name=xia_text)
    xia_actor = sx.get_actor_obj(name=xia_text)
    print(f"{xia_actor._isol._members.keys()=}")

    # WHEN
    output_cx = sx.get_output_calendar(actor_name=xia_text)

    # THEN
    output_cx_d_idea = output_cx.get_idea_kid(road="A,C,D")
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
    assert len(output_cx._members) == 25
    assert len(output_cx._members) == len(cx2._members) + 2 + 1
    assert len(output_cx._groups) == 37
    assert len(output_cx._groups) == len(cx2._groups) + 2 + 1
    assert output_cx._idearoot != cx1._idearoot
    assert output_cx._idearoot != cx2._idearoot


def test_actorunit_refresh_depotlinks_CorrectlyPullsAllPublicCalendars(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_test_economys_dir()
    economy_name = get_temp_env_name()
    sx = economyunit_shop(name=economy_name, economys_dir=env_dir)
    sx.create_dirs_if_null(in_memory_bank=True)
    # ux = actorunit_shop(name=actor1_text, env_dir=env_dir)

    ernie_text = "ernie"
    jessi_text = "jessi"
    steve_text = "steve"
    ernie_calendar = get_calendar_2CleanNodesRandomWeights(_owner=ernie_text)
    jessi_calendar = get_calendar_2CleanNodesRandomWeights(_owner=jessi_text)
    old_steve_cx = get_calendar_2CleanNodesRandomWeights(_owner=steve_text)
    sx.save_public_calendar(calendar_x=ernie_calendar)
    sx.save_public_calendar(calendar_x=jessi_calendar)
    sx.save_public_calendar(calendar_x=old_steve_cx)
    sx.create_new_actorunit(actor_name=ernie_text)
    sx.create_new_actorunit(actor_name=jessi_text)
    # sx.create_new_actorunit(actor_name=steve_text)
    ux_ernie = sx.get_actor_obj(name=ernie_text)
    ux_jessi = sx.get_actor_obj(name=jessi_text)
    # ux_steve = sx.get_actor_obj(name=steve_text)
    ux_ernie.set_depot_calendar(calendar_x=jessi_calendar, depotlink_type="blind_trust")
    ux_ernie.set_depot_calendar(calendar_x=old_steve_cx, depotlink_type="blind_trust")
    ux_jessi.set_depot_calendar(calendar_x=ernie_calendar, depotlink_type="blind_trust")
    ux_jessi.set_depot_calendar(calendar_x=old_steve_cx, depotlink_type="blind_trust")
    # ux_steve.set_depot_calendar(calendar_x=ernie_calendar, depotlink_type="blind_trust")
    # ux_steve.set_depot_calendar(calendar_x=jessi_calendar, depotlink_type="blind_trust")
    assert len(ux_ernie._admin.get_remelded_output_calendar().get_idea_list()) == 4
    assert len(ux_jessi._admin.get_remelded_output_calendar().get_idea_list()) == 4
    # assert len(ux_steve._admin.get_remelded_output_calendar().get_idea_list()) == 4
    new_steve_calendar = get_calendar_3CleanNodesRandomWeights(_owner="steve")
    sx.save_public_calendar(calendar_x=new_steve_calendar)
    # print(f"{env_dir=} {ux._admin._calendars_public_dir=}")
    # for file_name in x_func_dir_files(dir_path=env_dir):
    #     print(f"{ux._admin._calendars_public_dir=} {file_name=}")

    # for file_name in x_func_dir_files(dir_path=ux._admin._calendars_public_dir):
    #     print(f"{ux._admin._calendars_public_dir=} {file_name=}")

    # WHEN
    sx.reload_all_actors_src_calendarunits()

    # THEN
    assert len(ux_ernie._admin.get_remelded_output_calendar().get_idea_list()) == 5
    assert len(ux_jessi._admin.get_remelded_output_calendar().get_idea_list()) == 5
