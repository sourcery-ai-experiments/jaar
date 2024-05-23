from src.real.real_report import (
    get_real_guts_partys_dataframe,
    get_real_guts_partys_plotly_fig,
    get_real_lives_partys_dataframe,
    get_real_lives_partys_plotly_fig,
    get_real_guts_intent_dataframe,
    get_real_guts_intent_plotly_fig,
    get_real_lives_intent_dataframe,
    get_real_lives_intent_plotly_fig,
)
from src.real.examples.example_reals import (
    create_example_real2,
    create_example_real3,
    create_example_real4,
)
from src.real.examples.real_env_kit import reals_dir_setup_cleanup


def test_get_real_guts_partys_dataframe_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real2()

    # WHEN
    x_df = get_real_guts_partys_dataframe(music_real)

    # THEN
    partyunit_colums = {
        "owner_id",
        "party_id",
        "creditor_weight",
        "debtor_weight",
        "_agenda_credit",
        "_agenda_debt",
        "_agenda_intent_credit",
        "_agenda_intent_debt",
        "_agenda_intent_ratio_credit",
        "_agenda_intent_ratio_debt",
        "_creditor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_agenda_meld_order",
        "_treasury_credit_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == partyunit_colums
    assert x_df.shape[0] == 8


def test_get_real_guts_partys_plotly_fig_DisplaysCorrectInfo(reals_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real2()

    # WHEN
    x_fig = get_real_guts_partys_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2


def test_get_real_lives_partys_dataframe_ReturnsCorrectObj(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real2()
    music_real.generate_all_live_agendas()

    # WHEN
    x_df = get_real_lives_partys_dataframe(music_real)

    # THEN
    partyunit_colums = {
        "owner_id",
        "party_id",
        "creditor_weight",
        "debtor_weight",
        "_agenda_credit",
        "_agenda_debt",
        "_agenda_intent_credit",
        "_agenda_intent_debt",
        "_agenda_intent_ratio_credit",
        "_agenda_intent_ratio_debt",
        "_creditor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_agenda_meld_order",
        "_treasury_credit_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == partyunit_colums
    assert x_df.shape[0] == 8


def test_get_real_lives_partys_plotly_fig_DisplaysCorrectInfo(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real2()
    music_real.generate_all_live_agendas()

    # WHEN
    x_fig = get_real_lives_partys_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2


def test_get_real_guts_intent_dataframe_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real3()

    # WHEN
    x_df = get_real_guts_intent_dataframe(music_real)

    # THEN
    intent_colums = {
        "owner_id",
        "agenda_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == intent_colums
    assert x_df.shape[0] == 8


def test_get_real_guts_intent_plotly_fig_DisplaysCorrectInfo(reals_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real3()

    # WHEN
    x_fig = get_real_guts_intent_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_get_real_lives_intent_dataframe_ReturnsCorrectObj(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real4()
    music_real.generate_all_live_agendas()

    # WHEN
    x_df = get_real_lives_intent_dataframe(music_real)

    # THEN
    intent_colums = {
        "owner_id",
        "agenda_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == intent_colums
    assert x_df.shape[0] in [8, 9]


def test_get_real_lives_intent_plotly_fig_DisplaysCorrectInfo(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real4()
    music_real.generate_all_live_agendas()

    # WHEN
    x_fig = get_real_lives_intent_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2
