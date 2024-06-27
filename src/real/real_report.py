from src._world.report import (
    get_world_charunits_dataframe,
    get_world_agenda_dataframe,
)
from src.real.real import RealUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_real_souls_chars_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_userhubs = x_real.get_owner_userhubs()
    # for all owners get soul
    soul_dfs = []
    for x_userhub in owner_userhubs.values():
        soul_world = x_userhub.get_soul_world()
        soul_world.calc_world_metrics()
        df = get_world_charunits_dataframe(soul_world)
        df.insert(0, "owner_id", soul_world._owner_id)
        soul_dfs.append(df)
    return pandas_concat(soul_dfs, ignore_index=True)


def get_real_souls_chars_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
    ]
    df = get_real_souls_chars_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.char_id,
                df.credor_weight,
                df.debtor_weight,
                df._world_cred,
                df._world_debt,
                df._world_agenda_cred,
                df._world_agenda_debt,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', soul chars metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_homes_chars_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_userhubs = x_real.get_owner_userhubs()
    # for all owners get home
    home_dfs = []
    for x_userhub in owner_userhubs.values():
        home_world = x_userhub.get_home_world()
        home_world.calc_world_metrics()
        home_df = get_world_charunits_dataframe(home_world)
        home_df.insert(0, "owner_id", home_world._owner_id)
        home_dfs.append(home_df)
    return pandas_concat(home_dfs, ignore_index=True)


def get_real_homes_chars_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "char_id",
        "credor_weight",
        "debtor_weight",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
    ]
    df = get_real_homes_chars_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.char_id,
                df.credor_weight,
                df.debtor_weight,
                df._world_cred,
                df._world_debt,
                df._world_agenda_cred,
                df._world_agenda_debt,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', home chars metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_souls_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_userhubs = x_real.get_owner_userhubs()
    # for all owners get soul
    soul_dfs = []
    for x_userhub in owner_userhubs.values():
        soul_world = x_userhub.get_soul_world()
        soul_world.calc_world_metrics()
        df = get_world_agenda_dataframe(soul_world)
        soul_dfs.append(df)
    return pandas_concat(soul_dfs, ignore_index=True)


def get_real_souls_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "world_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    ]
    df = get_real_souls_agenda_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.world_importance,
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
    fig_title = f"Real '{x_real.real_id}', soul agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_homes_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_userhubs = x_real.get_owner_userhubs()
    # for all owners get home
    home_dfs = []
    for x_userhub in owner_userhubs.values():
        home_world = x_userhub.get_home_world()
        home_world.calc_world_metrics()
        home_df = get_world_agenda_dataframe(home_world)
        home_dfs.append(home_df)
    return pandas_concat(home_dfs, ignore_index=True)


def get_real_homes_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "world_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    ]
    df = get_real_homes_agenda_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.world_importance,
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
    fig_title = f"Real '{x_real.real_id}', home agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
