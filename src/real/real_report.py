from src._truth.report import (
    get_truth_otherunits_dataframe,
    get_truth_agenda_dataframe,
)
from src.real.real import RealUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_real_sames_others_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all person paths
    person_userhubs = x_real.get_person_userhubs()
    # for all persons get same
    same_dfs = []
    for x_userhub in person_userhubs.values():
        same_truth = x_userhub.get_same_truth()
        same_truth.calc_truth_metrics()
        df = get_truth_otherunits_dataframe(same_truth)
        df.insert(0, "owner_id", same_truth._owner_id)
        same_dfs.append(df)
    return pandas_concat(same_dfs, ignore_index=True)


def get_real_sames_others_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "other_id",
        "credor_weight",
        "debtor_weight",
        "_truth_cred",
        "_truth_debt",
        "_truth_agenda_cred",
        "_truth_agenda_debt",
    ]
    df = get_real_sames_others_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.other_id,
                df.credor_weight,
                df.debtor_weight,
                df._truth_cred,
                df._truth_debt,
                df._truth_agenda_cred,
                df._truth_agenda_debt,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', same others metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_lives_others_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all person paths
    person_userhubs = x_real.get_person_userhubs()
    # for all persons get live
    live_dfs = []
    for x_userhub in person_userhubs.values():
        live_truth = x_userhub.get_live_truth()
        live_truth.calc_truth_metrics()
        live_df = get_truth_otherunits_dataframe(live_truth)
        live_df.insert(0, "owner_id", live_truth._owner_id)
        live_dfs.append(live_df)
    return pandas_concat(live_dfs, ignore_index=True)


def get_real_lives_others_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "other_id",
        "credor_weight",
        "debtor_weight",
        "_truth_cred",
        "_truth_debt",
        "_truth_agenda_cred",
        "_truth_agenda_debt",
    ]
    df = get_real_lives_others_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.other_id,
                df.credor_weight,
                df.debtor_weight,
                df._truth_cred,
                df._truth_debt,
                df._truth_agenda_cred,
                df._truth_agenda_debt,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', live others metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_sames_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all person paths
    person_userhubs = x_real.get_person_userhubs()
    # for all persons get same
    same_dfs = []
    for x_userhub in person_userhubs.values():
        same_truth = x_userhub.get_same_truth()
        same_truth.calc_truth_metrics()
        df = get_truth_agenda_dataframe(same_truth)
        same_dfs.append(df)
    return pandas_concat(same_dfs, ignore_index=True)


def get_real_sames_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "truth_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    ]
    df = get_real_sames_agenda_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.truth_importance,
                df._label,
                df._parent_road,
                df._begin,
                df._close,
                df._addin,
                df._denom,
                df._numor,
                df._reest,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', same agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_lives_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all person paths
    person_userhubs = x_real.get_person_userhubs()
    # for all persons get live
    live_dfs = []
    for x_userhub in person_userhubs.values():
        live_truth = x_userhub.get_live_truth()
        live_truth.calc_truth_metrics()
        live_df = get_truth_agenda_dataframe(live_truth)
        live_dfs.append(live_df)
    return pandas_concat(live_dfs, ignore_index=True)


def get_real_lives_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "truth_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    ]
    df = get_real_lives_agenda_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.truth_importance,
                df._label,
                df._parent_road,
                df._begin,
                df._close,
                df._addin,
                df._denom,
                df._numor,
                df._reest,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', live agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
