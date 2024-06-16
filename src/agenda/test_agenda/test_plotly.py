from src.agenda.examples.example_agendas import (
    agenda_v001_with_large_intent,
    get_agenda_with_4_levels,
    get_agenda_assignment_laundry_example1,
    get_agenda_with_4_levels_and_2reasons,
    get_agenda_x1_3levels_1reason_1facts,
)
from src.agenda.agenda import agendaunit_shop
from src.agenda.graphic import (
    display_ideatree,
    get_agenda_guys_plotly_fig,
    get_agenda_intent_plotly_fig,
)


def test_display_ideatree_GivenAgenda():
    # a_agenda = get_1node_agenda()
    # a_agenda = get_2node_agenda()
    # a_agenda = get_3node_agenda()
    # a_agenda = get_5nodeHG_agenda()
    # a_agenda = get_7nodeJRoot_agenda()
    a_agenda = get_agenda_with_4_levels()
    # a_agenda = agenda_v001()
    a_agenda.calc_agenda_metrics()
    print(f"Agenda {a_agenda._real_id}: Nodes ({len(a_agenda._idea_dict)})")

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
    a_agenda.calc_agenda_metrics()
    print(f"Agenda {a_agenda._real_id}: Nodes ({len(a_agenda._idea_dict)})")

    # WHEN
    x_fig = display_ideatree(a_agenda, mode="Task")

    # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_get_agenda_guys_plotly_fig_DisplaysCorrectInfo():
    # GIVEN
    luca_agenda = agendaunit_shop()
    luca_agenda.set_guy_credor_pool(500)
    luca_agenda.set_guy_debtor_pool(400)
    todd_text = "Todd"
    todd_credor_weight = 66
    todd_debtor_weight = 77
    luca_agenda.add_guyunit(todd_text, todd_credor_weight, todd_debtor_weight)
    sue_text = "Sue"
    sue_credor_weight = 434
    sue_debtor_weight = 323
    luca_agenda.add_guyunit(sue_text, sue_credor_weight, sue_debtor_weight)

    # WHEN
    x_fig = get_agenda_guys_plotly_fig(luca_agenda)

    # THEN
    # show_figure = True
    # if show_figure:
    #   x_fig.show()


def test_get_agenda_intent_plotly_fig_DisplaysCorrectInfo():
    # GIVEN
    yao_agenda = agenda_v001_with_large_intent()
    week_text = "weekdays"
    week_road = yao_agenda.make_l1_road(week_text)
    assert len(yao_agenda.get_intent_dict()) == 63

    # WHEN
    x_fig = get_agenda_intent_plotly_fig(yao_agenda)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
