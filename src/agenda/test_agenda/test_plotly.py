from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels,
    get_agenda_assignment_laundry_example1,
    get_agenda_with_4_levels_and_2reasons,
    get_agenda_x1_3levels_1reason_1beliefs,
)
from src.agenda.agenda import agendaunit_shop
from src.agenda.graphic import display_ideatree, display_party_graph


def test_display_ideatree_GivenAgenda():
    # a_agenda = get_1node_agenda()
    # a_agenda = get_2node_agenda()
    # a_agenda = get_3node_agenda()
    # a_agenda = get_5nodeHG_agenda()
    # a_agenda = get_7nodeJRoot_agenda()
    a_agenda = get_agenda_with_4_levels()
    # a_agenda = agenda_v001()
    a_agenda.set_agenda_metrics()
    print(f"Agenda {a_agenda._world_id}: Nodes ({len(a_agenda._idea_dict)})")

    # WHEN
    x_fig = display_ideatree(a_agenda)

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
    print(f"Agenda {a_agenda._world_id}: Nodes ({len(a_agenda._idea_dict)})")

    # WHEN
    x_fig = display_ideatree(a_agenda, mode="Task")

    # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_display_party_graph_DisplaysCorrectInfo():
    # GIVEN
    luca_agenda = agendaunit_shop()
    luca_agenda.set_party_creditor_pool(500)
    luca_agenda.set_party_debtor_pool(400)
    todd_text = "Todd"
    todd_creditor_weight = 66
    todd_debtor_weight = 77
    luca_agenda.add_partyunit(todd_text, todd_creditor_weight, todd_debtor_weight)
    sue_text = "Sue"
    sue_creditor_weight = 434
    sue_debtor_weight = 323
    luca_agenda.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)

    # WHEN
    display_party_graph(luca_agenda)

    # THEN
    assert 1 == 2
