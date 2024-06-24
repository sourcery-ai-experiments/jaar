from src._truth.examples.example_truths import (
    truth_v001_with_large_intent,
    get_truth_with_4_levels,
    get_truth_assignment_laundry_example1,
    get_truth_with_4_levels_and_2reasons,
    get_truth_x1_3levels_1reason_1facts,
)
from src._truth.truth import truthunit_shop
from src._truth.graphic import (
    display_ideatree,
    get_truth_others_plotly_fig,
    get_truth_intent_plotly_fig,
)


def test_display_ideatree_GivenTruth():
    # a_truth = get_1node_truth()
    # a_truth = get_2node_truth()
    # a_truth = get_3node_truth()
    # a_truth = get_5nodeHG_truth()
    # a_truth = get_7nodeJRoot_truth()
    a_truth = get_truth_with_4_levels()
    # a_truth = truth_v001()
    a_truth.calc_truth_metrics()
    print(f"Truth {a_truth._real_id}: Nodes ({len(a_truth._idea_dict)})")

    # WHEN
    x_fig = display_ideatree(a_truth)

    # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_display_ideatree_GivenTruth_shows_Tasks():
    # a_truth = get_1node_truth()
    # a_truth = get_2node_truth()
    # a_truth = get_3node_truth()
    # a_truth = get_5nodeHG_truth()
    # a_truth = get_7nodeJRoot_truth()
    a_truth = get_truth_assignment_laundry_example1()
    # a_truth = truth_v001()
    a_truth.calc_truth_metrics()
    print(f"Truth {a_truth._real_id}: Nodes ({len(a_truth._idea_dict)})")

    # WHEN
    x_fig = display_ideatree(a_truth, mode="Task")

    # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()


def test_get_truth_others_plotly_fig_DisplaysCorrectInfo():
    # GIVEN
    luca_truth = truthunit_shop()
    luca_truth.set_other_credor_pool(500)
    luca_truth.set_other_debtor_pool(400)
    todd_text = "Todd"
    todd_credor_weight = 66
    todd_debtor_weight = 77
    luca_truth.add_otherunit(todd_text, todd_credor_weight, todd_debtor_weight)
    sue_text = "Sue"
    sue_credor_weight = 434
    sue_debtor_weight = 323
    luca_truth.add_otherunit(sue_text, sue_credor_weight, sue_debtor_weight)

    # WHEN
    x_fig = get_truth_others_plotly_fig(luca_truth)

    # THEN
    # show_figure = True
    # if show_figure:
    #   x_fig.show()


def test_get_truth_intent_plotly_fig_DisplaysCorrectInfo():
    # GIVEN
    yao_truth = truth_v001_with_large_intent()
    week_text = "weekdays"
    week_road = yao_truth.make_l1_road(week_text)
    assert len(yao_truth.get_intent_dict()) == 63

    # WHEN
    x_fig = get_truth_intent_plotly_fig(yao_truth)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
