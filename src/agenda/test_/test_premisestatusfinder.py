from src.agenda.reason_idea import (
    PremiseStatusFinder,
    PremiseBeliefSegerateData,
    pbsd_shop,
)
from pytest import raises as pytest_raises
from plotly.graph_objects import Figure as go_figure, Scatter as go_Scatter
from dataclasses import dataclass


def test_premisestatusfinder_belief_nigh_outside_premise_range_correctlyReturnsValue():
    # GIVEN / WHEN
    segr_obj = PremiseStatusFinder(
        belief_open=20000,
        belief_nigh=29000,
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
    )
    print(f"----\n  {segr_obj.belief_open=}  {segr_obj.belief_nigh=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(
        f"  {segr_obj.belief_open=}  {segr_obj.belief_nigh=} \tdifference:{segr_obj.belief_nigh-segr_obj.belief_open}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    # assert segr_obj._belief_range_len == 9000
    assert segr_obj.get_belief_nigh_mod_div() == 200
    assert segr_obj._task_status


def test_premisestatusfinder_correctlyReturnsTaskStatusTrueWhenBeliefRangeGreaterTbeliefivisor():
    # GIVEN / WHEN
    segr_obj = PremiseStatusFinder(
        belief_open=20000,
        belief_nigh=29000,
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
    )
    print(f"----\n  {segr_obj.belief_open=}  {segr_obj.belief_nigh=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(
        f"  {segr_obj.belief_open=}  {segr_obj.belief_nigh=} \tdifference:{segr_obj.belief_nigh-segr_obj.belief_open}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    # assert segr_obj._belief_range_len == 9000
    assert segr_obj._active_status
    assert segr_obj._task_status


def test_premisestatusfinder_correctlyReturnsActiveStatus_Scenario01():
    # GIVEN / WHEN
    segr_obj = PremiseStatusFinder(
        belief_open=1300,
        belief_nigh=1400,
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
    )
    print(f"----\n  {segr_obj.belief_open=}  {segr_obj.belief_nigh=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    assert segr_obj._active_status
    assert segr_obj._task_status


def test_premisestatusfinder_correctlyReturnsActiveStatus_Scenario02():
    # GIVEN / WHEN
    segr_obj = PremiseStatusFinder(
        belief_open=1300,
        belief_nigh=1300,
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
    )
    print(f"----\n  {segr_obj.belief_open=}  {segr_obj.belief_nigh=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    assert segr_obj._active_status == False
    assert segr_obj._task_status == False


# def test_premisestatusfinder_correctlyReturnsActiveStatus_Scenario03():
#     # GIVEN / WHEN
#     segr_obj = PremiseStatusFinder(
#         belief_open=1063998720,
#         belief_nigh=1064130373,
#         premise_open=1305.0,
#         premise_nigh=1305.0,
#         premise_divisor=1440,
#     )
#     print(f"----\n  {segr_obj.belief_open=}  {segr_obj.belief_nigh=}")
#     print(f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}")
#     print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

#     # THEN
#     assert segr_obj._active_status
#     assert segr_obj._task_status


def test_PremiseStatusFinder_Isssue69FindAndFixActiveStatusSettingError():
    # GIVEN / WHEN
    segr_obj = PremiseStatusFinder(
        belief_open=1300,
        belief_nigh=1300,
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
    )
    print(f"----\n  {segr_obj.belief_open=}  {segr_obj.belief_nigh=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    assert segr_obj._active_status == False
    assert segr_obj._task_status == False


def test_PremiseBeliefSegerateData_Exists():
    # GIVEN
    x_premise_open = 1
    x_premise_nigh = 1
    x_premise_divisor = 1
    x_belief_open_full = 1
    x_belief_nigh_full = 1

    # WHEN
    x_pbsd = PremiseBeliefSegerateData(
        x_premise_open,
        x_premise_nigh,
        x_premise_divisor,
        x_belief_open_full,
        x_belief_nigh_full,
    )

    # THEN
    assert x_pbsd.premise_open == x_premise_open
    assert x_pbsd.premise_nigh == x_premise_nigh
    assert x_pbsd.premise_divisor == x_premise_divisor
    assert x_pbsd.belief_open_full == x_belief_open_full
    assert x_pbsd.belief_nigh_full == x_belief_nigh_full


def test_pbsd_shop_ReturnsCorrectObj():
    # GIVEN
    x_premise_open = 1
    x_premise_nigh = 1
    x_premise_divisor = 1
    x_belief_open_full = 1
    x_belief_nigh_full = 1

    # WHEN
    x_pbsd = pbsd_shop(
        x_premise_open,
        x_premise_nigh,
        x_premise_divisor,
        x_belief_open_full,
        x_belief_nigh_full,
    )

    # THEN
    assert x_pbsd.premise_open == x_premise_open
    assert x_pbsd.premise_nigh == x_premise_nigh
    assert x_pbsd.premise_divisor == x_premise_divisor
    assert x_pbsd.belief_open_full == x_belief_open_full
    assert x_pbsd.belief_nigh_full == x_belief_nigh_full


def test_PremiseBeliefSegerateData_check_attr_CorrectlyRaisesError():
    with pytest_raises(Exception) as excinfo_1:
        pbsd_shop(
            premise_open=1,
            premise_nigh=None,
            premise_divisor=1,
            belief_open_full=1,
            belief_nigh_full=1,
        )
    assert str(excinfo_1.value) == "No parameter can be None"

    x_belief_open_full = 2
    x_belief_nigh_full = 1
    with pytest_raises(Exception) as excinfo_2:
        pbsd_shop(
            premise_open=1,
            premise_nigh=1,
            premise_divisor=1,
            belief_open_full=x_belief_open_full,
            belief_nigh_full=x_belief_nigh_full,
        )
    assert (
        str(excinfo_2.value)
        == f"self.belief_open_full={x_belief_open_full} cannot be greater that self.belief_nigh_full={x_belief_nigh_full}"
    )

    x_premise_divisor = -1
    with pytest_raises(Exception) as excinfo_3:
        pbsd_shop(
            premise_open=1,
            premise_nigh=1,
            premise_divisor=x_premise_divisor,
            belief_open_full=1,
            belief_nigh_full=1,
        )
    assert (
        str(excinfo_3.value)
        == f"self.premise_divisor={x_premise_divisor} cannot be less/equal to zero"
    )

    x_premise_divisor = 1
    x_premise_open = -1
    with pytest_raises(Exception) as excinfo_4:
        pbsd_shop(
            premise_open=x_premise_open,
            premise_nigh=1,
            premise_divisor=x_premise_divisor,
            belief_open_full=1,
            belief_nigh_full=1,
        )
    assert (
        str(excinfo_4.value)
        == f"self.premise_open={x_premise_open} cannot be less than zero or greater than self.premise_divisor={x_premise_divisor}"
    )

    x_premise_nigh = 2
    with pytest_raises(Exception) as excinfo_5:
        pbsd_shop(
            premise_open=1,
            premise_nigh=x_premise_nigh,
            premise_divisor=x_premise_divisor,
            belief_open_full=1,
            belief_nigh_full=1,
        )
    assert (
        str(excinfo_5.value)
        == f"self.premise_nigh={x_premise_nigh} cannot be less than zero or greater than self.premise_divisor={x_premise_divisor}"
    )


def test_PremiseBeliefSegerateData_AbbrevationMethodsReturnCorrectObjs():
    # GIVEN
    x_premise_open = 1
    x_premise_nigh = 2
    x_premise_divisor = 3
    x_belief_open_full = 4
    x_belief_nigh_full = 5

    # WHEN
    x_pbsd = pbsd_shop(
        x_premise_open,
        x_premise_nigh,
        x_premise_divisor,
        x_belief_open_full,
        x_belief_nigh_full,
    )

    # THEN
    assert x_pbsd.bo() == x_belief_open_full % x_premise_divisor
    assert x_pbsd.bn() == x_belief_nigh_full % x_premise_divisor
    assert x_pbsd.po() == x_premise_open
    assert x_pbsd.pn() == x_premise_nigh
    assert x_pbsd.pd() == x_premise_divisor


def add_trace(
    fig: go_figure,
    x_int: int,
    x_end: int,
    y_int: int,
    trace_name: str,
    x_color: str = None,
    showlegend: bool = False,
    case_text: str = "",
    wanted_text: str = "",
    premise_divisor: float = 0,
) -> go_figure:
    if x_end is None:
        x_end = x_int
    if x_color is None:
        x_color = "Black"
    x_marker_size = 10
    if x_color == "Blue":
        x_marker_size = 12
    fig.add_trace(
        go_Scatter(
            x=[x_int, x_end],
            y=[y_int, y_int],
            marker_size=x_marker_size,
            name=trace_name,
            marker_color=x_color,
            showlegend=showlegend,
        )
    )
    fig.add_annotation(
        x=premise_divisor + 0.1,
        y=y_int,
        text=wanted_text,
        showarrow=False,
    )
    fig.add_annotation(
        x=-0.1,
        y=y_int,
        text=case_text,
        showarrow=False,
    )


def add_traces(
    fig: go_figure,
    x_pbsd: PremiseBeliefSegerateData,
    y_int: int,
    showlegend: bool = False,
    case_text: str = "",
    wanted_text: str = "",
    premise_divisor: float = 1,
) -> go_figure:
    belief_text = "BeliefUnit Remainder range"
    premise_text = "Premise Range"
    blue_text = "Blue"
    pink_text = "Pink"
    sl = showlegend
    if x_pbsd.po() <= x_pbsd.pn():
        add_trace(fig, x_pbsd.po(), x_pbsd.pn(), y_int, premise_text, blue_text, sl)
    else:
        add_trace(fig, 0, x_pbsd.pn(), y_int, premise_text, blue_text, sl)
        add_trace(fig, x_pbsd.po(), x_pbsd.pd(), y_int, premise_text, blue_text, sl)

    if x_pbsd.bo() <= x_pbsd.bn():
        add_trace(
            fig,
            x_pbsd.bo(),
            x_pbsd.bn(),
            y_int,
            belief_text,
            pink_text,
            sl,
            case_text=case_text,
            wanted_text=wanted_text,
            premise_divisor=premise_divisor,
        )
    else:
        add_trace(
            fig,
            0,
            x_pbsd.bn(),
            y_int,
            belief_text,
            pink_text,
            sl,
            case_text=case_text,
            wanted_text=wanted_text,
            premise_divisor=premise_divisor,
        )
        add_trace(fig, x_pbsd.bo(), x_pbsd.pd(), y_int, belief_text, pink_text, sl)


def show_x(
    x_pbsd: PremiseBeliefSegerateData,
    wanted_active_status: bool,
    fig: go_figure,
    trace_y: float,
    case_text: str,
    showlegend: bool = False,
) -> bool:
    wanted_text = "TRUE" if wanted_active_status else "FALSE"
    add_traces(fig, x_pbsd, trace_y, showlegend, case_text, wanted_text, 1)
    if x_pbsd.get_active_status() != wanted_active_status:
        fig.show()

    return wanted_active_status


def test_PremiseBeliefSegerateData_get_active_status_ReturnsCorrectObj():
    """Check scenarios where PremiseUnit._active_status should used"""
    fig = go_figure()
    pd = 1  # premise_divisor
    add_trace(
        fig,
        0.0,
        pd,
        0.0,
        "Divisor Range",
        None,
        True,
        "Case",
        "Expected",
        pd,
    )
    fig_title = "When Belief.range < Premise_divisor: Premise.Active_status Checks."
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_title, title_font_size=20)

    # Case A
    assert pbsd_shop(0.3, 0.7, 1, 0.1, 1.2).get_active_status()

    # Case B1
    ll = 0
    caseb1_1 = pbsd_shop(0.3, 0.7, pd, 0.5, 0.8)
    caseb1_2 = pbsd_shop(0.3, 0.7, pd, 0.2, 0.5)
    caseb1_3 = pbsd_shop(0.3, 0.7, pd, 0.4, 0.6)
    caseb1_4 = pbsd_shop(0.3, 0.7, pd, 0.2, 0.8)
    caseb1_5 = pbsd_shop(0.3, 0.7, pd, 0.1, 0.3)
    caseb1_6 = pbsd_shop(0.3, 0.7, pd, 0.7, 0.8)
    caseb1_7 = pbsd_shop(0.3, 0.3, pd, 0.3, 0.5)

    ll = -0.1
    assert caseb1_1.get_active_status() == show_x(
        caseb1_1, True, fig, ll, "caseb1_1", True
    )
    ll -= 0.1
    assert caseb1_2.get_active_status() == show_x(caseb1_2, True, fig, ll, "caseb1_2")
    ll -= 0.1
    assert caseb1_3.get_active_status() == show_x(caseb1_3, True, fig, ll, "caseb1_3")
    ll -= 0.1
    assert caseb1_4.get_active_status() == show_x(caseb1_4, True, fig, ll, "caseb1_4")
    ll -= 0.1
    assert caseb1_5.get_active_status() == show_x(caseb1_5, False, fig, ll, "caseb1_5")
    ll -= 0.1
    assert caseb1_6.get_active_status() == show_x(caseb1_6, False, fig, ll, "caseb1_6")
    ll -= 0.1
    assert caseb1_7.get_active_status() == show_x(caseb1_7, True, fig, ll, "caseb1_7")

    # Case B2
    ll -= 0.1
    caseb2_1 = pbsd_shop(0.3, 0.7, pd, 0.8, 1.4)
    caseb2_2 = pbsd_shop(0.3, 0.7, pd, 0.6, 1.2)
    caseb2_3 = pbsd_shop(0.3, 0.7, pd, 0.6, 1.4)
    caseb2_4 = pbsd_shop(0.3, 0.7, pd, 0.9, 1.8)
    caseb2_5 = pbsd_shop(0.3, 0.7, pd, 0.2, 1.1)
    caseb2_6 = pbsd_shop(0.3, 0.7, pd, 0.9, 1.1)
    caseb2_7 = pbsd_shop(0.3, 0.7, pd, 0.7, 1.2)
    caseb2_8 = pbsd_shop(0.7, 0.7, pd, 0.7, 1.2)
    ll -= 0.1
    assert caseb2_1.get_active_status() == show_x(caseb2_1, True, fig, ll, "caseb2_1")
    ll -= 0.1
    assert caseb2_2.get_active_status() == show_x(caseb2_2, True, fig, ll, "caseb2_2")
    ll -= 0.1
    assert caseb2_3.get_active_status() == show_x(caseb2_3, True, fig, ll, "caseb2_3")
    ll -= 0.1
    assert caseb2_4.get_active_status() == show_x(caseb2_4, True, fig, ll, "caseb2_4")
    ll -= 0.1
    assert caseb2_5.get_active_status() == show_x(caseb2_5, True, fig, ll, "caseb2_5")
    ll -= 0.1
    assert caseb2_6.get_active_status() == show_x(caseb2_6, False, fig, ll, "caseb2_6")
    ll -= 0.1
    assert caseb2_7.get_active_status() == show_x(caseb2_7, False, fig, ll, "caseb2_7")
    ll -= 0.1
    assert caseb2_8.get_active_status() == show_x(caseb2_8, True, fig, ll, "caseb2_8")

    # Case B3
    ll -= 0.1
    caseb3_1 = pbsd_shop(0.7, 0.3, pd, 0.2, 0.5)
    caseb3_2 = pbsd_shop(0.7, 0.3, pd, 0.5, 0.8)
    caseb3_3 = pbsd_shop(0.7, 0.3, pd, 0.2, 0.8)
    caseb3_4 = pbsd_shop(0.7, 0.3, pd, 0.1, 0.2)
    caseb3_5 = pbsd_shop(0.7, 0.3, pd, 0.8, 0.9)
    caseb3_6 = pbsd_shop(0.7, 0.3, pd, 0.4, 0.5)
    caseb3_7 = pbsd_shop(0.7, 0.3, pd, 0.3, 0.5)
    ll -= 0.1
    assert caseb3_1.get_active_status() == show_x(caseb3_1, True, fig, ll, "caseb3_1")
    ll -= 0.1
    assert caseb3_2.get_active_status() == show_x(caseb3_2, True, fig, ll, "caseb3_2")
    ll -= 0.1
    assert caseb3_3.get_active_status() == show_x(caseb3_3, True, fig, ll, "caseb3_3")
    ll -= 0.1
    assert caseb3_4.get_active_status() == show_x(caseb3_4, True, fig, ll, "caseb3_4")
    ll -= 0.1
    assert caseb3_5.get_active_status() == show_x(caseb3_5, True, fig, ll, "caseb3_5")
    ll -= 0.1
    assert caseb3_6.get_active_status() == show_x(caseb3_6, False, fig, ll, "caseb3_6")
    ll -= 0.1
    assert caseb3_7.get_active_status() == show_x(caseb3_7, False, fig, ll, "caseb3_7")

    # Case B4
    ll -= 0.1
    caseb4_1 = pbsd_shop(0.7, 0.3, pd, 0.6, 1.2)
    caseb4_2 = pbsd_shop(0.7, 0.3, pd, 0.8, 1.4)
    caseb4_3 = pbsd_shop(0.7, 0.3, pd, 0.6, 1.4)
    caseb4_4 = pbsd_shop(0.7, 0.3, pd, 0.8, 1.2)
    caseb4_5 = pbsd_shop(0.7, 0.3, pd, 0.2, 1.1)
    caseb4_6 = pbsd_shop(0.7, 0.3, pd, 0.9, 1.8)
    ll -= 0.1
    assert caseb4_1.get_active_status() == show_x(caseb4_1, True, fig, ll, "caseb4_1")
    ll -= 0.1
    assert caseb4_2.get_active_status() == show_x(caseb4_2, True, fig, ll, "caseb4_2")
    ll -= 0.1
    assert caseb4_3.get_active_status() == show_x(caseb4_3, True, fig, ll, "caseb4_3")
    ll -= 0.1
    assert caseb4_4.get_active_status() == show_x(caseb4_4, True, fig, ll, "caseb4_4")
    ll -= 0.1
    assert caseb4_5.get_active_status() == show_x(caseb4_5, True, fig, ll, "caseb4_5")
    ll -= 0.1
    assert caseb4_6.get_active_status() == show_x(caseb4_6, True, fig, ll, "caseb4_6")

    # Bottom divisor line
    ll -= 0.1
    ll -= 0.1
    add_trace(fig, 0.0, pd, ll, "Divisor Range", None)

    false_bool = False
    if false_bool == False:
        fig.show()
        assert 1 == 2
