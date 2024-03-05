from src.world.report import (
    get_world_guts_partys_dataframe,
    get_world_guts_partys_plotly_fig,
    get_world_lifes_partys_dataframe,
    get_world_lifes_partys_plotly_fig,
)
from src.world.examples.example_worlds import create_example_world2
from src.world.examples.world_env_kit import worlds_dir_setup_cleanup


def test_get_world_guts_partys_dataframe_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    music_world = create_example_world2()

    # WHEN
    x_df = get_world_guts_partys_dataframe(music_world)

    # THEN
    partyunit_colums = {
        "worker_id",
        "party_id",
        "creditor_weight",
        "debtor_weight",
        "_agenda_credit",
        "_agenda_debt",
        "_agenda_intent_credit",
        "_agenda_intent_debt",
        "_agenda_intent_ratio_credit",
        "_agenda_intent_ratio_debt",
        "_creditor_live",
        "_debtor_live",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_agenda_meld_order",
        "_treasury_credit_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
        "depotlink_type",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == partyunit_colums
    assert x_df.shape[0] == 8


def test_get_world_guts_partys_plotly_fig_DisplaysCorrectInfo(worlds_dir_setup_cleanup):
    # GIVEN
    music_world = create_example_world2()

    # WHEN
    x_fig = get_world_guts_partys_plotly_fig(music_world)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2


def test_get_world_lifes_partys_dataframe_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    music_world = create_example_world2()
    music_world.generate_all_life_agendas()

    # WHEN
    x_df = get_world_lifes_partys_dataframe(music_world)

    # THEN
    partyunit_colums = {
        "worker_id",
        "party_id",
        "creditor_weight",
        "debtor_weight",
        "_agenda_credit",
        "_agenda_debt",
        "_agenda_intent_credit",
        "_agenda_intent_debt",
        "_agenda_intent_ratio_credit",
        "_agenda_intent_ratio_debt",
        "_creditor_live",
        "_debtor_live",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_agenda_meld_order",
        "_treasury_credit_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
        "depotlink_type",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == partyunit_colums
    assert x_df.shape[0] == 8


def test_get_world_lifes_partys_plotly_fig_DisplaysCorrectInfo(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_world = create_example_world2()

    # WHEN
    x_fig = get_world_lifes_partys_plotly_fig(music_world)

    # THEN
    show_figure = True
    if show_figure:
        x_fig.show()
    assert 1 == 2
