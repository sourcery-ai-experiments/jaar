from src._prime.road import get_parent_road_from_road, RoadUnit, is_sub_road
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit
from plotly.graph_objects import Figure, Scatter


def _get_dot_diameter(x_ratio: float):
    return ((x_ratio**0.4)) * 100


def _get_parent_y(x_idea: IdeaUnit, ideaunit_y_coordinate_dict: dict) -> RoadUnit:
    parent_road = get_parent_road_from_road(x_idea.get_road())
    return ideaunit_y_coordinate_dict.get(parent_road)


def _get_color_for_ideaunit_trace(x_ideaunit: IdeaUnit, mode: str) -> str:
    if mode is None:
        if x_ideaunit._level == 0:
            return "Red"
        elif x_ideaunit._level == 1:
            return "Pink"
        elif x_ideaunit._level == 2:
            return "Green"
        elif x_ideaunit._level == 3:
            return "Blue"
        elif x_ideaunit._level == 4:
            return "Purple"
        elif x_ideaunit._level == 5:
            return "Gold"
        else:
            return "Black"
    elif mode == "Task":
        return "Red" if x_ideaunit.promise else "Pink"
    elif mode == "Market":
        if x_ideaunit._problem_bool and x_ideaunit._healerhold.any_group_id_exists():
            return "Purple"
        elif x_ideaunit._healerhold.any_group_id_exists():
            return "Blue"
        elif x_ideaunit._problem_bool:
            return "Red"
        else:
            return "Pink"


def _add_individual_trace(
    trace_list: list,
    anno_list: list,
    parent_y,
    current_y,
    kid_idea: IdeaUnit,
    mode: str,
):
    trace_list.append(
        Scatter(
            x=[kid_idea._level - 1, kid_idea._level],
            y=[parent_y, current_y],
            marker_size=_get_dot_diameter(kid_idea._agenda_importance),
            name=kid_idea._label,
            marker_color=_get_color_for_ideaunit_trace(kid_idea, mode=mode),
        )
    )
    anno_list.append(
        dict(
            x=kid_idea._level,
            y=current_y
            + (_get_dot_diameter(kid_idea._agenda_importance) / 150)
            + 0.002,
            text=kid_idea._label,
            showarrow=False,
        )
    )


def _add_ideaunit_traces(
    trace_list, anno_list, x_agenda: AgendaUnit, current_y: float, mode: str
):
    ideas = [x_agenda._idearoot]
    y_ideaunit_y_coordinate_dict = {None: 0}
    prev_road = x_agenda._idearoot.get_road()
    current_y = 0
    while ideas != []:
        x_idea = ideas.pop(-1)
        if is_sub_road(x_idea.get_road(), prev_road) == False:
            current_y -= 1
        _add_individual_trace(
            trace_list=trace_list,
            anno_list=anno_list,
            parent_y=_get_parent_y(x_idea, y_ideaunit_y_coordinate_dict),
            current_y=current_y,
            kid_idea=x_idea,
            mode=mode,
        )
        ideas.extend(iter(x_idea._kids.values()))
        y_ideaunit_y_coordinate_dict[x_idea.get_road()] = current_y
        prev_road = x_idea.get_road()


def _update_layout_fig(x_fig: Figure, mode: str, x_agenda: AgendaUnit):
    x_title = "Tree with lines Layout"
    if mode == "Task":
        x_title = "Idea Tree with task ideas in Red."
    x_title += f" (Items: {len(x_agenda._idea_dict)})"
    x_title += f" (_sum_healerhold_importance: {x_agenda._sum_healerhold_importance})"
    x_title += f" (_markets_justified: {x_agenda._markets_justified})"
    x_fig.update_layout(
        title_text=x_title,
        font_size=12,
    )


def display_agenda(x_agenda: AgendaUnit, mode: str = None) -> Figure:
    """Mode can be None, Task, Market"""

    x_fig = Figure()
    current_y = 0
    trace_list = []
    anno_list = []
    _add_ideaunit_traces(trace_list, anno_list, x_agenda, current_y, mode=mode)
    _update_layout_fig(x_fig, mode, x_agenda=x_agenda)
    while trace_list:
        x_trace = trace_list.pop(-1)
        x_fig.add_trace(x_trace)
        x_anno = anno_list.pop(-1)
        x_fig.add_annotation(
            x=x_anno.get("x"),
            y=x_anno.get("y"),
            text=x_anno.get("text"),
            font_size=20,
            showarrow=False,
        )

    return x_fig
