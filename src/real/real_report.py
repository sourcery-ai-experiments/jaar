from src._world.report import (
    get_world_charunits_dataframe,
    get_world_agenda_dataframe,
)
from src.real.real import RealUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_real_minds_chars_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get mind
    mind_dfs = []
    for x_hubunit in owner_hubunits.values():
        mind_world = x_hubunit.get_mind_world()
        mind_world.calc_world_metrics()
        df = get_world_charunits_dataframe(mind_world)
        df.insert(0, "owner_id", mind_world._owner_id)
        mind_dfs.append(df)
    return pandas_concat(mind_dfs, ignore_index=True)


def get_real_minds_chars_plotly_fig(x_real: RealUnit) -> plotly_Figure:
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
    df = get_real_minds_chars_dataframe(x_real)
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
    fig_title = f"Real '{x_real.real_id}', mind chars metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_beings_chars_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get being
    being_dfs = []
    for x_hubunit in owner_hubunits.values():
        being_world = x_hubunit.get_being_world()
        being_world.calc_world_metrics()
        being_df = get_world_charunits_dataframe(being_world)
        being_df.insert(0, "owner_id", being_world._owner_id)
        being_dfs.append(being_df)
    return pandas_concat(being_dfs, ignore_index=True)


def get_real_beings_chars_plotly_fig(x_real: RealUnit) -> plotly_Figure:
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
    df = get_real_beings_chars_dataframe(x_real)
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
    fig_title = f"Real '{x_real.real_id}', being chars metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_minds_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get mind
    mind_dfs = []
    for x_hubunit in owner_hubunits.values():
        mind_world = x_hubunit.get_mind_world()
        mind_world.calc_world_metrics()
        df = get_world_agenda_dataframe(mind_world)
        mind_dfs.append(df)
    return pandas_concat(mind_dfs, ignore_index=True)


def get_real_minds_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
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
    df = get_real_minds_agenda_dataframe(x_real)
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
    fig_title = f"Real '{x_real.real_id}', mind agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_beings_agenda_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all owner paths
    owner_hubunits = x_real.get_owner_hubunits()
    # for all owners get being
    being_dfs = []
    for x_hubunit in owner_hubunits.values():
        being_world = x_hubunit.get_being_world()
        being_world.calc_world_metrics()
        being_df = get_world_agenda_dataframe(being_world)
        being_dfs.append(being_df)
    return pandas_concat(being_dfs, ignore_index=True)


def get_real_beings_agenda_plotly_fig(x_real: RealUnit) -> plotly_Figure:
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
    df = get_real_beings_agenda_dataframe(x_real)
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
    fig_title = f"Real '{x_real.real_id}', being agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
