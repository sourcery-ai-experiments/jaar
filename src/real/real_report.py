from src._world.report import (
    get_world_personunits_dataframe,
    get_world_agenda_dataframe,
)
from src.real.real import RealUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_real_sames_persons_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_userhubs = x_real.get_owner_userhubs()
    # for all owners get same
    same_dfs = []
    for x_userhub in owner_userhubs.values():
        same_world = x_userhub.get_same_world()
        same_world.calc_world_metrics()
        df = get_world_personunits_dataframe(same_world)
        df.insert(0, "owner_id", same_world._owner_id)
        same_dfs.append(df)
    return pandas_concat(same_dfs, ignore_index=True)


def get_real_sames_persons_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "person_id",
        "credor_weight",
        "debtor_weight",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
    ]
    df = get_real_sames_persons_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.person_id,
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
    fig_title = f"Real '{x_real.real_id}', same persons metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_lives_persons_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_userhubs = x_real.get_owner_userhubs()
    # for all owners get live
    live_dfs = []
    for x_userhub in owner_userhubs.values():
        live_world = x_userhub.get_live_world()
        live_world.calc_world_metrics()
        live_df = get_world_personunits_dataframe(live_world)
        live_df.insert(0, "owner_id", live_world._owner_id)
        live_dfs.append(live_df)
    return pandas_concat(live_dfs, ignore_index=True)


def get_real_lives_persons_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "person_id",
        "credor_weight",
        "debtor_weight",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
    ]
    df = get_real_lives_persons_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.person_id,
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
    fig_title = f"Real '{x_real.real_id}', live persons metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_sames_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_userhubs = x_real.get_owner_userhubs()
    # for all owners get same
    same_dfs = []
    for x_userhub in owner_userhubs.values():
        same_world = x_userhub.get_same_world()
        same_world.calc_world_metrics()
        df = get_world_agenda_dataframe(same_world)
        same_dfs.append(df)
    return pandas_concat(same_dfs, ignore_index=True)


def get_real_sames_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
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
    df = get_real_sames_agenda_dataframe(x_real)
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
    fig_title = f"Real '{x_real.real_id}', same agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_lives_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_userhubs = x_real.get_owner_userhubs()
    # for all owners get live
    live_dfs = []
    for x_userhub in owner_userhubs.values():
        live_world = x_userhub.get_live_world()
        live_world.calc_world_metrics()
        live_df = get_world_agenda_dataframe(live_world)
        live_dfs.append(live_df)
    return pandas_concat(live_dfs, ignore_index=True)


def get_real_lives_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
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
    df = get_real_lives_agenda_dataframe(x_real)
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
    fig_title = f"Real '{x_real.real_id}', live agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
