from src.agenda.report import (
    get_agenda_partyunits_dataframe,
    get_agenda_intent_dataframe,
)
from src.real.real import RealUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table


def get_real_dutys_partys_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all person paths
    person_filehubs = x_real.get_person_filehubs()
    # for all persons get duty
    duty_dfs = []
    for x_filehub in person_filehubs.values():
        duty_agenda = x_filehub.get_duty_agenda()
        duty_agenda.calc_agenda_metrics()
        df = get_agenda_partyunits_dataframe(duty_agenda)
        df.insert(0, "owner_id", duty_agenda._owner_id)
        duty_dfs.append(df)
    return pandas_concat(duty_dfs, ignore_index=True)


def get_real_dutys_partys_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "party_id",
        "creditor_weight",
        "debtor_weight",
        "_agenda_credit",
        "_agenda_debt",
        "_agenda_intent_credit",
        "_agenda_intent_debt",
    ]
    df = get_real_dutys_partys_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.party_id,
                df.creditor_weight,
                df.debtor_weight,
                df._agenda_credit,
                df._agenda_debt,
                df._agenda_intent_credit,
                df._agenda_intent_debt,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', duty partys metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_works_partys_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all person paths
    person_filehubs = x_real.get_person_filehubs()
    # for all persons get work
    work_dfs = []
    for x_filehub in person_filehubs.values():
        work_agenda = x_filehub.get_work_agenda()
        work_agenda.calc_agenda_metrics()
        work_df = get_agenda_partyunits_dataframe(work_agenda)
        work_df.insert(0, "owner_id", work_agenda._owner_id)
        work_dfs.append(work_df)
    return pandas_concat(work_dfs, ignore_index=True)


def get_real_works_partys_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
        "owner_id",
        "party_id",
        "creditor_weight",
        "debtor_weight",
        "_agenda_credit",
        "_agenda_debt",
        "_agenda_intent_credit",
        "_agenda_intent_debt",
    ]
    df = get_real_works_partys_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.party_id,
                df.creditor_weight,
                df.debtor_weight,
                df._agenda_credit,
                df._agenda_debt,
                df._agenda_intent_credit,
                df._agenda_intent_debt,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_title = f"Real '{x_real.real_id}', work partys metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_dutys_intent_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all person paths
    person_filehubs = x_real.get_person_filehubs()
    # for all persons get duty
    duty_dfs = []
    for x_filehub in person_filehubs.values():
        duty_agenda = x_filehub.get_duty_agenda()
        duty_agenda.calc_agenda_metrics()
        df = get_agenda_intent_dataframe(duty_agenda)
        duty_dfs.append(df)
    return pandas_concat(duty_dfs, ignore_index=True)


def get_real_dutys_intent_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
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
    ]
    df = get_real_dutys_intent_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.agenda_importance,
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
    fig_title = f"Real '{x_real.real_id}', duty intent metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig


def get_real_works_intent_dataframe(x_real: RealUnit) -> DataFrame:
    # get list of all person paths
    person_filehubs = x_real.get_person_filehubs()
    # for all persons get work
    work_dfs = []
    for x_filehub in person_filehubs.values():
        work_agenda = x_filehub.get_work_agenda()
        work_agenda.calc_agenda_metrics()
        work_df = get_agenda_intent_dataframe(work_agenda)
        work_dfs.append(work_df)
    return pandas_concat(work_dfs, ignore_index=True)


def get_real_works_intent_plotly_fig(x_real: RealUnit) -> plotly_Figure:
    column_header_list = [
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
    ]
    df = get_real_works_intent_dataframe(x_real)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.owner_id,
                df.agenda_importance,
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
    fig_title = f"Real '{x_real.real_id}', work intent metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
