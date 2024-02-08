from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels,
    get_agenda_assignment_laundry_example1,
    get_agenda_with_4_levels_and_2reasons,
    get_agenda_x1_3levels_1reason_1beliefs,
)
from src.agenda.graph import display_agenda


def test_display_ideatree_GivenAgenda():
    # a_agenda = get_1node_agenda()
    # a_agenda = get_2node_agenda()
    # a_agenda = get_3node_agenda()
    # a_agenda = get_5nodeHG_agenda()
    # a_agenda = get_7nodeJRoot_agenda()
    a_agenda = get_agenda_with_4_levels()
    # a_agenda = agenda_v001()
    a_agenda.set_agenda_metrics()
    print(f"Agenda {a_agenda._market_id}: Nodes ({len(a_agenda._idea_dict)})")

    # WHEN
    x_fig = display_agenda(a_agenda)

    # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_display_ideatree_GivenAgenda_shows_Tasks():
    # a_agenda = get_1node_agenda()
    # a_agenda = get_2node_agenda()
    # a_agenda = get_3node_agenda()
    # a_agenda = get_5nodeHG_agenda()
    # a_agenda = get_7nodeJRoot_agenda()
    a_agenda = get_agenda_assignment_laundry_example1()
    # a_agenda = agenda_v001()
    a_agenda.set_agenda_metrics()
    print(f"Agenda {a_agenda._market_id}: Nodes ({len(a_agenda._idea_dict)})")

    # WHEN
    x_fig = display_agenda(a_agenda, mode="Task")

    # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
