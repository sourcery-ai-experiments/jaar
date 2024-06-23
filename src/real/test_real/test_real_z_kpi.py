from src.real.real_report import (
    get_real_dutys_others_dataframe,
    get_real_dutys_others_plotly_fig,
    get_real_goals_others_dataframe,
    get_real_goals_others_plotly_fig,
    get_real_dutys_intent_dataframe,
    get_real_dutys_intent_plotly_fig,
    get_real_goals_intent_dataframe,
    get_real_goals_intent_plotly_fig,
)
from src.real.examples.example_reals import (
    create_example_real2,
    create_example_real3,
    create_example_real4,
)
from src.real.examples.real_env import env_dir_setup_cleanup


def test_get_real_dutys_others_dataframe_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real2()

    # WHEN
    x_df = get_real_dutys_others_dataframe(music_real)

    # THEN
    otherunit_colums = {
        "owner_id",
        "other_id",
        "credor_weight",
        "debtor_weight",
        "_agenda_cred",
        "_agenda_debt",
        "_agenda_intent_cred",
        "_agenda_intent_debt",
        "_agenda_intent_ratio_cred",
        "_agenda_intent_ratio_debt",
        "_credor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_agenda_meld_order",
        "_treasury_cred_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == otherunit_colums
    assert x_df.shape[0] == 8


def test_get_real_dutys_others_plotly_fig_DisplaysCorrectInfo(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real2()

    # WHEN
    x_fig = get_real_dutys_others_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2


def test_get_real_goals_others_dataframe_ReturnsCorrectObj(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real2()
    music_real.generate_all_goal_agendas()

    # WHEN
    x_df = get_real_goals_others_dataframe(music_real)

    # THEN
    otherunit_colums = {
        "owner_id",
        "other_id",
        "credor_weight",
        "debtor_weight",
        "_agenda_cred",
        "_agenda_debt",
        "_agenda_intent_cred",
        "_agenda_intent_debt",
        "_agenda_intent_ratio_cred",
        "_agenda_intent_ratio_debt",
        "_credor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_agenda_meld_order",
        "_treasury_cred_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
        "_inallocable_debtor_weight",
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert x_df.shape[0] == 8
    assert set(x_df.columns) == otherunit_colums


def test_get_real_goals_others_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real2()
    music_real.generate_all_goal_agendas()

    # WHEN
    x_fig = get_real_goals_others_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2


def test_get_real_dutys_intent_dataframe_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real3()

    # WHEN
    x_df = get_real_dutys_intent_dataframe(music_real)

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


def test_get_real_dutys_intent_plotly_fig_DisplaysCorrectInfo(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real3()

    # WHEN
    x_fig = get_real_dutys_intent_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_get_real_goals_intent_dataframe_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    music_real = create_example_real4()
    music_real.generate_all_goal_agendas()

    # WHEN
    x_df = get_real_goals_intent_dataframe(music_real)

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


def test_get_real_goals_intent_plotly_fig_DisplaysCorrectInfo(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = create_example_real4()
    music_real.generate_all_goal_agendas()

    # WHEN
    x_fig = get_real_goals_intent_plotly_fig(music_real)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
    # assert 1 == 2
