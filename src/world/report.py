from src.agenda.agenda import get_from_json as agenda_get_from_json
from src.agenda.report import get_agenda_partyunits_dataframe
from src.instrument.file import open_file
from src.world.world import WorldUnit
from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import (
    Figure as plotly_Figure,
    Scatter as plotly_Scatter,
    Table as plotly_Table,
)


def get_world_guts_partys_dataframe(x_world: WorldUnit) -> DataFrame:
    # get list of all person paths
    person_paths = x_world.get_person_paths()
    # for all persons get gut
    gut_dfs = []
    for person_path in person_paths:
        gut_agenda = agenda_get_from_json(open_file(person_path, "gut.json"))
        gut_agenda.set_agenda_metrics()
        df = get_agenda_partyunits_dataframe(gut_agenda)
        df.insert(0, "worker_id", gut_agenda._worker_id)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_world_guts_partys_plotly_fig(x_world: WorldUnit) -> plotly_Figure:
    column_header_list = [
        "worker_id",
        "party_id",
        "creditor_weight",
        "debtor_weight",
        "_agenda_credit",
        "_agenda_debt",
        "_agenda_intent_credit",
        "_agenda_intent_debt",
    ]
    df = get_world_guts_partys_dataframe(x_world)
    header_dict = dict(
        values=column_header_list, fill_color="paleturquoise", align="left"
    )
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.worker_id,
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
    fig_title = f"World '{x_world.world_id}', gut partys metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    return fig
