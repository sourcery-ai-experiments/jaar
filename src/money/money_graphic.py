from src._road.jaar_config import soul_str, dutys_str, jobs_str, being_str
from src._road.finance import default_money_magnitude
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from dataclasses import dataclass


def green_str():
    return "green"


def blue_str():
    return "blue"


def red_str():
    return "red"


def black_str():
    return "black"


def bob_str() -> str:
    return "Bob"


def buz_str() -> str:
    return "Buz"


def car_str() -> str:
    return "Carl"


def joc_str() -> str:
    return "Joc"


def luc_str() -> str:
    return "Luca"


def mar_str() -> str:
    return "Martin"


def ric_str() -> str:
    return "Rico"


def sue_str() -> str:
    return "Sue"


def xio_str() -> str:
    return "Xio"


def yao_str() -> str:
    return "Yao"


def zia_str() -> str:
    return "Zia"


def add_river_rect(
    fig: plotly_Figure, x0, y0, x1, y1, display_text, x_color=None, money_supply=None
):
    if x_color is None:
        x_color = "LightSeaGreen"
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_text(fig, x0, y1, display_text)
    if money_supply != None:
        money_percent = f"{int(((x1 - x0) * 12.5))}%"
        add_rect_text(fig, x0, y1 - 0.2, str(money_percent))
        money_amt = round((((x1 - x0) * 12.5) / 100) * money_supply)
        add_rect_text(fig, x0, y1 - 0.4, str(money_amt))


def add_column_rect(
    fig: plotly_Figure, x0, y0, x1, y1, display_text, x_color=None, money_supply=None
):
    if x_color is None:
        x_color = "Purple"
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    if money_supply is None:
        add_rect_text(fig, x0, y0, display_text)
    if money_supply != None:
        money_percent = f"{display_text} {int(((y0 - y1) * 12.5))}%"
        add_rect_text(fig, x0, y0, str(money_percent))
        money_amt = round((((y0 - y1) * 12.5) / 100) * money_supply)
        add_rect_text(fig, x0, y0 - 0.2, str(money_amt))


def add_river_row(fig, grants_dict: dict, money_amt, y0, color=None):
    row_x0 = 1
    row_x1 = 9
    row_len = row_x1 - row_x0
    grants_sum = sum(grants_dict.values())
    ratio_dict = {grantee: wx / grants_sum for grantee, wx in grants_dict.items()}
    for grantee in grants_dict:
        new_x1 = row_x0 + row_len * ratio_dict.get(grantee)
        add_river_rect(fig, row_x0, y0, new_x1, y0 + 1, grantee, color, money_amt)
        row_x0 = new_x1


def add_river_col(fig, num_dict: dict, money_amt, x0, y0, c_len):
    row_y0 = y0
    row_y1 = row_y0 - c_len
    row_len = row_y1 - row_y0
    num_sum = sum(num_dict.values())
    ratio_dict = {char_id: wx / num_sum for char_id, wx in num_dict.items()}
    for grantee in num_dict:
        new_y1 = row_y0 + row_len * ratio_dict.get(grantee)
        add_column_rect(fig, x0, row_y0, x0 + 1, new_y1, grantee, None, money_amt)
        row_y0 = new_y1


def add_grants_top(fig, grants_dict: dict, t_y0: int, healer_id, money_amt):
    grants_text = f"{healer_id} Grants"
    dy0 = t_y0 - 1.2
    dy1 = t_y0 - 1.6
    dy2 = t_y0 - 2.2
    dy3 = t_y0 - 3
    ey0 = t_y0 - 0.8
    ey1 = t_y0 - 1.2
    add_river_rect(fig, 1.0, t_y0 - 1, 2.0, t_y0, grants_text, green_str())
    add_river_row(fig, grants_dict, money_amt=money_amt, y0=t_y0 - 4)
    add_2_curve(fig, path=f"M 1.75,{dy0} C 2,{dy1} 7.4,{dy2} 9,{dy3}", color=blue_str())
    add_2_curve(fig, path=f"M 1.75,{dy0} C 2,{dy1} 1.2,{dy2} 1,{dy3}", color=blue_str())
    add_rect_arrow(fig, 1.75, ey1, 1.5, ey0, blue_str())


def add_taxs_bottom(fig, taxs_dict, b_y0: int, healer_id: str, money_amt: int):
    taxs_text = f"{healer_id} Taxs"
    cy0 = b_y0 + 1.2
    cy1 = b_y0 + 1.6
    cy2 = b_y0 + 2.2
    cy3 = b_y0 + 3
    ay0 = b_y0 + 0.8
    ay1 = b_y0 + 1.2
    add_river_rect(fig, 1.0, b_y0, 2.0, b_y0 + 1, taxs_text, green_str())
    add_river_row(fig, taxs_dict, money_amt=money_amt, y0=b_y0 + 3)
    add_2_curve(fig, path=f"M 1.75,{cy0} C 2,{cy1} 7.4,{cy2} 9,{cy3}", color=red_str())
    add_2_curve(fig, path=f"M 1.75,{cy0} C 2,{cy1} 1.2,{cy2} 1,{cy3}", color=red_str())
    add_rect_arrow(fig, 1.5, ay0, 1.75, ay1, red_str())


def add_taxs_column(
    fig, taxs_dict, b_x0: int, b_y0: int, healer_id: str, money_amt: int, c_len: float
):
    taxs_text = f"{healer_id} Taxs"
    cx0 = b_x0 - 0.2
    cx1 = b_x0 - 0.8
    cx2 = b_x0 - 0.4
    cy0 = b_y0 - 4
    cy1 = cy0 - c_len
    cy2 = cy1 + 2
    cy4 = b_y0 - 1
    ax0 = b_x0 + 0.05
    ax1 = b_x0 - 0.2
    ay0 = b_y0 - 0.7
    ay1 = cy4
    add_river_rect(fig, b_x0, b_y0 - 1, b_x0 + 1, b_y0, taxs_text, green_str())
    add_river_col(fig, taxs_dict, money_amt=money_amt, x0=b_x0, y0=cy0, c_len=c_len)
    z1_path = f"M {cx0},5 C {cx2},4 {cx2},2.2 {b_x0},{cy0}"
    z2_path = f"M {cx0},5 C {cx1},4 {cx1},{cy2} {b_x0},{cy1}"
    add_2_curve(fig, path=z1_path, color=red_str())
    add_2_curve(fig, path=z2_path, color=red_str())
    add_rect_arrow(fig, ax0, ay0, ax1, ay1, red_str())
    print(f"columns: {b_x0=} {b_y0=}")


def add_rivercycle(fig: plotly_Figure, x0, y0, x1, y1, display_text):
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_text(fig, x0, y1, display_text)


def add_econ__rect(
    fig: plotly_Figure, x0, y0, x1, y1, text1=None, text2=None, text3=None, text4=None
):
    y0 -= 0.3
    y1 += 0.3
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_text(fig, x0 + 4, y1, text1)
    add_rect_text(fig, x0 + 4, y1 - 0.2, text2)
    add_rect_text(fig, x0 + 4, y1 - 0.4, text3)
    add_rect_text(fig, x0 + 4, y1 - 0.6, text4)


def add_rect_text(fig, x0, y0, text):
    x_margin = 0.3
    fig.add_annotation(
        x=x0 + x_margin, y=y0 - x_margin, text=text, showarrow=False, align="left"
    )


def add_2_curve(fig: plotly_Figure, path: str, color: str):
    fig.add_shape(dict(type="path", path=path, line_color=color))


def add_rect_arrow(fig: plotly_Figure, x0, y0, ax0, ay0, color=None, width=None):
    if color is None:
        color = "black"
    if width is None:
        width = 3
    fig.add_annotation(
        x=x0,  # arrows' head
        y=y0,  # arrows' head
        ax=ax0,  # arrows' tail
        ay=ay0,  # arrows' tail
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",  # if you want only the arrow
        showarrow=True,
        arrowhead=width,
        arrowsize=1,
        arrowwidth=width,
        arrowcolor=color,
    )


def get_money_graphic_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 10])
    fig.update_yaxes(range=[0, 10])
    return fig


def grants1_dict() -> dict:
    return {
        bob_str(): 2.2 - 1.0,
        buz_str(): 3.0 - 2.2,
        car_str(): 4.6 - 3.0,
        ric_str(): 5.2 - 4.6,
        sue_str(): 6.6 - 5.2,
        xio_str(): 7.2 - 6.6,
        yao_str(): 8.0 - 7.2,
        zia_str(): 9.0 - 8.0,
    }


def taxs1_dict() -> dict:
    return {
        joc_str(): 100,
        luc_str(): 100,
        mar_str(): 55,
        ric_str(): 60,
        sue_str(): 76,
        xio_str(): 130,
        yao_str(): 100,
        zia_str(): 100,
    }


def rivercycle1_dict() -> dict:
    return {
        bob_str(): 60,
        joc_str(): 200,
        luc_str(): 55,
        mar_str(): 66,
        sue_str(): 76,
        xio_str(): 130,
        yao_str(): 50,
        zia_str(): 70,
    }


def get_money_structures0_fig() -> plotly_Figure:
    fig = get_money_graphic_base_fig()

    mm = default_money_magnitude()
    sue1_p1 = f"Healer = {sue_str()} "
    sue1_p2 = "Problem = problem1"
    sue1_p3 = "Econ = project1"
    sue1_p4 = f"Money = {mm} "

    m_y0 = 8
    m_y1 = -3
    add_grants_top(fig, grants1_dict(), t_y0=m_y0, healer_id=sue_str(), money_amt=mm)
    add_taxs_bottom(fig, taxs1_dict(), m_y1, healer_id=sue_str(), money_amt=mm)
    add_econ__rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
    fig.update_yaxes(range=[m_y1 - 1, m_y0 + 3])
    fig.add_trace(
        plotly_Scatter(
            x=[5.0, 5.0, 5.0],
            y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
            text=[
                "Econ Money Structure",
                "Flow of Money to Chars",
                "Money starts as grants from Healer. Taxs are money coming back to healer.",
            ],
            mode="text",
        )
    )

    return fig


def get_money_structures1_fig() -> plotly_Figure:
    fig = get_money_graphic_base_fig()

    mm = default_money_magnitude()
    sue1_p1 = f"Healer = {sue_str()} "
    sue1_p2 = "Problem = problem1"
    sue1_p3 = "Econ = project1"
    sue1_p4 = f"Money = {mm} "

    m_y0 = 8
    m_y1 = -5
    add_grants_top(fig, grants1_dict(), t_y0=m_y0, healer_id=sue_str(), money_amt=mm)
    add_taxs_bottom(fig, taxs1_dict(), m_y1, healer_id=sue_str(), money_amt=mm)

    y_mid = m_y1 + (m_y0 - m_y1) / 2
    add_rect_arrow(fig, 4.8, y_mid + 0.3, 2, y_mid + 1.3, green_str())
    add_rect_arrow(fig, 5, y_mid + 0.3, 5, y_mid + 1.3, green_str())
    add_rect_arrow(fig, 5.2, y_mid + 0.3, 8.2, y_mid + 1.3, green_str())

    add_econ__rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
    fig.update_yaxes(range=[m_y1 - 1, m_y0 + 3])
    fig.add_trace(
        plotly_Scatter(
            x=[5.0, 5.0, 5.0],
            y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
            text=[
                "Econ Money Structure",
                "Flow of Money to Chars",
                "Money starts as grants from Healer. Taxs are money coming back to healer.",
            ],
            mode="text",
        )
    )

    return fig


def get_money_structures2_fig() -> plotly_Figure:
    fig = get_money_graphic_base_fig()

    mm = default_money_magnitude()
    sue1_p1 = f"Healer = {sue_str()} "
    sue1_p2 = "Problem = problem1"
    sue1_p3 = "Econ = project1"
    sue1_p4 = f"Money = {mm} "

    m_y0 = 8
    m_y1 = -7
    add_grants_top(fig, grants1_dict(), t_y0=m_y0, healer_id=sue_str(), money_amt=mm)
    add_taxs_column(fig, taxs1_dict(), -1, 6, sue_str(), mm, c_len=9)
    add_river_row(fig, rivercycle1_dict(), mm, 0, black_str())

    ay0 = 3.88
    ay1 = ay0 - 2.6
    bob_src = 2
    buz_src = 2.75
    car_src = 3.25
    ric_src = 4.75
    sue_src = 5.5
    xio_src = 6.7
    yao_src = 7.3
    zia_src = 8.5
    bob_dst = 1.3
    joc_dst = 2.5
    luc_dst = 4.25
    mar_dst = 4.75
    sue_dst = 5.6
    xio_dst = 6.7
    yao_dst = 7.3
    zia_dst = 8.5
    add_rect_arrow(fig, bob_dst, ay1, bob_src, ay0, green_str(), 2)
    add_rect_arrow(fig, luc_dst, ay1, bob_src, ay0, green_str(), 2)
    add_rect_arrow(fig, sue_dst, ay1, bob_src, ay0, green_str(), 2)
    add_rect_arrow(fig, joc_dst, ay1, buz_src, ay0, green_str(), 1)
    add_rect_arrow(fig, luc_dst, ay1, buz_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, car_src, ay0, green_str(), 1)
    add_rect_arrow(fig, mar_dst, ay1, car_src, ay0, green_str(), 1)
    add_rect_arrow(fig, luc_dst, ay1, car_src, ay0, green_str(), 1)
    add_rect_arrow(fig, mar_dst, ay1, ric_src, ay0, green_str(), 1)
    add_rect_arrow(fig, mar_dst, ay1, ric_src, ay0, green_str(), 1)
    add_rect_arrow(fig, luc_dst, ay1, sue_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, sue_src, ay0, green_str(), 1)
    add_rect_arrow(fig, yao_dst, ay1, sue_src, ay0, green_str(), 1)
    add_rect_arrow(fig, zia_dst, ay1, sue_src, ay0, green_str(), 1)
    add_rect_arrow(fig, luc_dst, ay1, xio_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, xio_src, ay0, green_str(), 1)
    add_rect_arrow(fig, xio_dst, ay1, yao_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, yao_src, ay0, green_str(), 1)
    add_rect_arrow(fig, xio_dst, ay1, zia_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, zia_src, ay0, green_str(), 1)
    add_rect_arrow(fig, zia_src, ay1, zia_src, ay0, green_str(), 1)
    # add_rect_arrow(fig, 5, y_mid + 0.3, 5, y_mid + 1.3, green_str())
    # add_rect_arrow(fig, 5.2, y_mid + 0.3, 8.2, y_mid + 1.3, green_str())

    add_econ__rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
    # fig.update_yaxes(range=[m_y1 - 1, m_y0 + 3])
    fig.update_yaxes(range=[-8, 10])
    fig.update_xaxes(range=[-3, 10])
    fig.add_trace(
        plotly_Scatter(
            x=[5.0, 5.0, 5.0],
            y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
            text=[
                "Econ Money Structure",
                "Flow of Money to Chars",
                "Money starts as grants from Healer. Taxs are money coming back to healer.",
            ],
            mode="text",
        )
    )

    return fig


def get_money_structures3_fig() -> plotly_Figure:
    fig = get_money_graphic_base_fig()

    mm = default_money_magnitude()
    sue1_p1 = f"Healer = {sue_str()} "
    sue1_p2 = "Problem = problem1"
    sue1_p3 = "Econ = project1"
    sue1_p4 = f"Money = {mm} "

    m_y0 = 8
    m_y1 = -7
    add_grants_top(fig, grants1_dict(), t_y0=m_y0, healer_id=sue_str(), money_amt=mm)
    add_taxs_column(fig, taxs1_dict(), -1, 6, sue_str(), mm, c_len=9)
    add_river_row(fig, rivercycle1_dict(), mm, 0, black_str())

    ay0 = 3.88
    ay1 = ay0 - 2.6
    bob_src = 2
    buz_src = 2.75
    car_src = 3.25
    ric_src = 4.75
    sue_src = 5.5
    xio_src = 6.7
    yao_src = 7.3
    zia_src = 8.5
    bob_dst = 1.3
    joc_dst = 2.5
    luc_dst = 4.25
    mar_dst = 4.75
    sue_dst = 5.6
    xio_dst = 6.7
    yao_dst = 7.3
    zia_dst = 8.5
    add_rect_arrow(fig, bob_dst, ay1, bob_src, ay0, green_str(), 2)
    add_rect_arrow(fig, luc_dst, ay1, bob_src, ay0, green_str(), 2)
    add_rect_arrow(fig, sue_dst, ay1, bob_src, ay0, green_str(), 2)
    add_rect_arrow(fig, joc_dst, ay1, buz_src, ay0, green_str(), 1)
    add_rect_arrow(fig, luc_dst, ay1, buz_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, car_src, ay0, green_str(), 1)
    add_rect_arrow(fig, mar_dst, ay1, car_src, ay0, green_str(), 1)
    add_rect_arrow(fig, luc_dst, ay1, car_src, ay0, green_str(), 1)
    add_rect_arrow(fig, mar_dst, ay1, ric_src, ay0, green_str(), 1)
    add_rect_arrow(fig, mar_dst, ay1, ric_src, ay0, green_str(), 1)
    add_rect_arrow(fig, luc_dst, ay1, sue_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, sue_src, ay0, green_str(), 1)
    add_rect_arrow(fig, yao_dst, ay1, sue_src, ay0, green_str(), 1)
    add_rect_arrow(fig, zia_dst, ay1, sue_src, ay0, green_str(), 1)
    add_rect_arrow(fig, luc_dst, ay1, xio_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, xio_src, ay0, green_str(), 1)
    add_rect_arrow(fig, xio_dst, ay1, yao_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, yao_src, ay0, green_str(), 1)
    add_rect_arrow(fig, xio_dst, ay1, zia_src, ay0, green_str(), 1)
    add_rect_arrow(fig, joc_dst, ay1, zia_src, ay0, green_str(), 1)
    add_rect_arrow(fig, zia_src, ay1, zia_src, ay0, green_str(), 1)
    # add_rect_arrow(fig, 5, y_mid + 0.3, 5, y_mid + 1.3, green_str())
    # add_rect_arrow(fig, 5.2, y_mid + 0.3, 8.2, y_mid + 1.3, green_str())

    add_econ__rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
    # fig.update_yaxes(range=[m_y1 - 1, m_y0 + 3])
    fig.update_yaxes(range=[-8, 10])
    fig.update_xaxes(range=[-3, 10])
    fig.add_trace(
        plotly_Scatter(
            x=[5.0, 5.0, 5.0],
            y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
            text=[
                "Econ Money Structure",
                "Flow of Money to Chars",
                "Money starts as grants from Healer. Taxs are money coming back to healer.",
            ],
            mode="text",
        )
    )

    return fig
