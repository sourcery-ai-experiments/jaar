from src._road.jaar_config import soul_str, dutys_str, jobs_str, being_str
from src._road.finance import default_money_magnitude
from src.listen.hubunit import hubunit_shop, HubUnit
from plotly.graph_objects import (
    Figure as plotly_Figure,
    Scatter as plotly_Scatter,
    Table as plotly_Table,
)
from dataclasses import dataclass


# @dataclass
# class ListenPlotlyShape:
#     x_hubunit: HubUnit
#     base_width: float = None
#     base_h: float = None
#     level: float = None
#     level_width0: float = None
#     level_width1: float = None
#     display_text: str = None
#     color: str = None

#     def set_attrs(self):
#         self.base_width = 0.1
#         self.base_h = 0.2
#         self.level = 0
#         self.level_width0 = 0.1
#         self.level_width1 = 0.9
#         self.display_text = f"{self.x_hubunit.crud_text} {get_normal_table_name(self.x_hubunit.category)} Order: {self.x_hubunit.listen_order}"

#     def set_level(self, x_level, x_width0, x_width1, color=None):
#         self.level = x_level
#         self.level_width0 = x_width0
#         self.level_width1 = x_width1
#         self.color = color


def add_world_rect(fig: plotly_Figure, x0, y0, x1, y1, display_text, x_color=None):
    if x_color is None:
        x_color = "LightSeaGreen"
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_text(fig, x0, y1, display_text)


def add_direc_rect(fig: plotly_Figure, x0, y0, x1, y1, display_text):
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_text(fig, x0, y1, display_text)


def add_econ__rect(
    fig: plotly_Figure, x0, y0, x1, y1, text1=None, text2=None, text3=None, text4=None
):
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_text(fig, x0 + 0.5, y1, text1)
    add_rect_text(fig, x0 + 0.5, y1 - 0.2, text2)
    add_rect_text(fig, x0 + 0.5, y1 - 0.4, text3)
    add_rect_text(fig, x0 + 0.5, y1 - 0.6, text4)


def add_rect_text(fig, x0, y0, text):
    x_margin = 0.2
    fig.add_annotation(
        x=x0 + x_margin, y=y0 - x_margin, text=text, showarrow=False, align="left"
    )


def add_2_curve(fig: plotly_Figure, path: str, color: str):
    fig.add_shape(dict(type="path", path=path, line_color=color))


def add_rect_arrow(fig: plotly_Figure, x0, y0, ax0, ay0, color=None):
    if color is None:
        color = "black"
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
        arrowhead=2,
        arrowsize=1,
        arrowwidth=3,
        arrowcolor=color,
    )


# def add_listen_rect(fig: plotly_Figure, listenplotyshape: ListenPlotlyShape):
#     level_bump = listenplotyshape.level * 0.05
#     home_form_x0 = listenplotyshape.base_width
#     home_form_x1 = 1 - listenplotyshape.base_width
#     home_width = home_form_x1 - home_form_x0
#     shape_x0 = home_form_x0 + (home_width * listenplotyshape.level_width0)
#     shape_x1 = home_form_x0 + (home_width * listenplotyshape.level_width1)
#     shape_y0 = level_bump + listenplotyshape.base_h
#     shape_y1 = level_bump + listenplotyshape.base_h + 0.05
#     x_color = "RoyalBlue"
#     if listenplotyshape.color != None:
#         x_color = listenplotyshape.color
#     fig.add_shape(
#         type="rect",
#         xref="paper",
#         yref="paper",
#         x0=shape_x0,
#         y0=shape_y0,
#         x1=shape_x1,
#         y1=shape_y1,
#         line=dict(
#             color=x_color,
#             width=8,
#         ),
#         fillcolor=None,  # "LightSkyBlue",
#     )
#     text_y = (shape_y0 + shape_y1) / 2
#     text_x = (shape_x0 + shape_x1) / 2
#     add_rect_text(fig, x=text_x, y=text_y, text=listenplotyshape.display_text)


# def add_beliefunits_circle(fig: plotly_Figure):
#     home_form_x0 = 0.2
#     home_form_x1 = 1 - 0.2
#     home_width = home_form_x1 - home_form_x0
#     shape_x0 = home_form_x0 + (home_width * 0.425)
#     shape_x1 = home_form_x0 + (home_width * 0.575)
#     shape_y0 = 0.325
#     shape_y1 = 0.425
#     x_color = "Green"
#     fig.add_shape(
#         type="circle",
#         xref="paper",
#         yref="paper",
#         x0=shape_x0,
#         y0=shape_y0,
#         x1=shape_x1,
#         y1=shape_y1,
#         line=dict(
#             color=x_color,
#             width=8,
#         ),
#         fillcolor=None,  # "LightSkyBlue",
#     )
#     text_y = (shape_y0 + shape_y1) / 2
#     text_x = (shape_x0 + shape_x1) / 2
#     add_rect_text(fig, x=text_x, y=text_y, text="BeliefUnits")


# def add_different_ideas_circle(fig: plotly_Figure):
#     home_form_x0 = 0.2
#     home_form_x1 = 1 - 0.2
#     home_width = home_form_x1 - home_form_x0
#     shape_x0 = home_form_x0
#     shape_x1 = home_form_x0 + home_width
#     shape_y0 = 0.54
#     shape_y1 = 0.75
#     x_color = "Grey"
#     fig.add_shape(
#         type="circle",
#         xref="paper",
#         yref="paper",
#         x0=shape_x0,
#         y0=shape_y0,
#         x1=shape_x1,
#         y1=shape_y1,
#         line=dict(
#             color=x_color,
#             width=3,
#         ),
#         fillcolor=None,  # "LightSkyBlue",
#     )
#     text_y = shape_y1 - 0.01
#     text_x = (shape_x0 + shape_x1) / 2
#     add_rect_text(fig, x=text_x, y=text_y, text="Different Ideas")


def get_hubunit_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 10])
    fig.update_yaxes(range=[0, 10])
    return fig


def get_listening_structures0_fig() -> plotly_Figure:
    fig = get_hubunit_base_fig()
    sue_text = "Sue"
    bob_text = "Bob"
    yao_text = "Yao"
    sue_soul_text = f"{sue_text}.{soul_str()}"
    sue_being_text = f"{sue_text}.{being_str()}"
    yao_being_text = f"{yao_text}.{being_str()}"
    bob_being_text = f"{bob_text}.{being_str()}"
    dir_being_text = f"{being_str()}s directory"
    dir_soul_text = f"{soul_str()}s directory"

    green_text = "Green"
    med_purple = "MediumPurple"
    add_world_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_soul_text, green_text)
    add_direc_rect(fig, 0.7, 6.7, 6.3, 8.3, dir_soul_text)
    add_world_rect(fig, 1.0, 1.0, 2.0, 2.0, sue_being_text, green_text)
    add_world_rect(fig, 3.0, 1.0, 4.0, 2.0, yao_being_text)
    add_world_rect(fig, 5.0, 1.0, 6.0, 2.0, bob_being_text)
    add_direc_rect(fig, 0.7, 0.7, 6.3, 2.3, dir_being_text)
    add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 5,4 5.5,2", color=med_purple)
    add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3,4 3.5,2", color=med_purple)
    add_rect_arrow(fig, 1.75, 2, 1.75, 6.8, green_text)
    add_rect_arrow(fig, 3.43, 2.3, 3.5, 2, med_purple)
    add_rect_arrow(fig, 5.41, 2.3, 5.5, 2, med_purple)

    fig.add_trace(
        plotly_Scatter(
            x=[4.0, 4.0],
            y=[9.0, 8.75],
            text=[
                "Reality World Listening Structures",
                "The soul world listens to other's being worlds and builds a beling world from itself and others",
            ],
            mode="text",
        )
    )

    return fig


def get_listening_structures1_fig() -> plotly_Figure:
    fig = get_hubunit_base_fig()
    sue_text = "Sue"
    bob_text = "Bob"
    sue_soul_text = f"{sue_text}.{soul_str()}"
    dir_soul_text = f"{soul_str()}s dir"

    green_text = "Green"
    blue_text = "blue"
    add_world_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_soul_text, green_text)
    add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_soul_text)
    add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 7.4,5.1 7.5,5", color=blue_text)
    add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 5.4,5.2 5.5,5", color=blue_text)
    add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=blue_text)
    add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, blue_text)

    sue_duty_text = f"{sue_text} duty"
    sue_job_text = f"{sue_text} job"
    d_sue1_p1 = f"Healer = {sue_text} "
    d_sue1_p2 = "Problem = problem1"
    d_sue1_p3 = "Econ = project1"
    d_sue1_p4 = f"Money = {default_money_magnitude()} "
    d_bob1_p1 = f"Healer = {bob_text} "
    d_bob1_p2 = "Problem = problem1"
    d_bob1_p3 = "Econ = project1"
    d_bob1_p4 = f"Money = {default_money_magnitude()} "
    d_sue2_p1 = f"Healer = {sue_text} "
    d_sue2_p2 = "Problem = problem2"
    d_sue2_p3 = "Project = project3"
    d_sue2_p4 = f"Money={default_money_magnitude()} "

    add_world_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_text)
    add_world_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_job_text)
    add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_text)
    add_econ__rect(fig, 2.7, 0.7, 4.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4)
    add_world_rect(fig, 5.0, 4.0, 6.0, 5.0, sue_duty_text)
    add_world_rect(fig, 5.0, 1.0, 6.0, 2.0, sue_job_text)
    add_rect_arrow(fig, 5.7, 2.1, 5.7, 3.9, green_text)
    add_econ__rect(fig, 4.7, 0.7, 6.3, 6.7, d_bob1_p1, d_bob1_p2, d_bob1_p3, d_bob1_p4)
    add_world_rect(fig, 7.0, 4.0, 8.0, 5.0, sue_duty_text)
    add_world_rect(fig, 7.0, 1.0, 8.0, 2.0, sue_job_text)
    add_rect_arrow(fig, 7.7, 2.1, 7.7, 3.9, green_text)
    add_econ__rect(fig, 6.7, 0.7, 8.3, 6.7, d_sue2_p1, d_sue2_p2, d_sue2_p3, d_sue2_p4)

    green_text = "Green"
    fig.add_trace(
        plotly_Scatter(
            x=[2.0],
            y=[13],
            text=["World Listening Structures"],
            mode="text",
        )
    )

    return fig


def get_listening_structures2_fig() -> plotly_Figure:
    fig = get_hubunit_base_fig()
    fig.update_yaxes(range=[-4, 10])
    sue_text = "Sue"
    bob_text = "Bob"
    sue_soul_text = f"{sue_text}.{soul_str()}"
    sue_being_text = f"{sue_text}.{being_str()}"
    dir_being_text = f"{being_str()}s dir"
    dir_soul_text = f"{soul_str()}s dir"

    green_text = "Green"
    blue_text = "blue"
    add_world_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_soul_text, green_text)
    add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_soul_text)
    add_world_rect(fig, 1.0, -2.0, 2.0, -1.0, sue_being_text, green_text)
    add_direc_rect(fig, 0.7, -2.3, 2.3, -0.7, dir_being_text)

    add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 7.4,5.1 7.5,5", color=blue_text)
    add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 5.4,5.2 5.5,5", color=blue_text)
    add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=blue_text)
    add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, blue_text)
    add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 7.4,0.4 7.5,1", color=blue_text)
    add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 5.4,0.4 5.5,1", color=blue_text)
    add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 3.4,0.4 3.5,1", color=blue_text)
    add_rect_arrow(fig, 1.71, -1.0, 1.75, -0.8, blue_text)

    sue_duty_text = f"{sue_text} duty"
    sue_job_text = f"{sue_text} job"
    d_sue1_p1 = f"Healer = {sue_text} "
    d_sue1_p2 = "Problem = problem1"
    d_sue1_p3 = "Econ = project1"
    d_sue1_p4 = f"Money = {default_money_magnitude()} "
    d_bob1_p1 = f"Healer = {bob_text} "
    d_bob1_p2 = "Problem = problem1"
    d_bob1_p3 = "Econ = project1"
    d_bob1_p4 = f"Money = {default_money_magnitude()} "
    d_sue2_p1 = f"Healer = {sue_text} "
    d_sue2_p2 = "Problem = problem2"
    d_sue2_p3 = "Project = project3"
    d_sue2_p4 = f"Money={default_money_magnitude()} "

    add_world_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_text)
    add_world_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_job_text)
    add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_text)
    add_econ__rect(fig, 2.7, 0.7, 4.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4)
    add_world_rect(fig, 5.0, 4.0, 6.0, 5.0, sue_duty_text)
    add_world_rect(fig, 5.0, 1.0, 6.0, 2.0, sue_job_text)
    add_rect_arrow(fig, 5.7, 2.1, 5.7, 3.9, green_text)
    add_econ__rect(fig, 4.7, 0.7, 6.3, 6.7, d_bob1_p1, d_bob1_p2, d_bob1_p3, d_bob1_p4)
    add_world_rect(fig, 7.0, 4.0, 8.0, 5.0, sue_duty_text)
    add_world_rect(fig, 7.0, 1.0, 8.0, 2.0, sue_job_text)
    add_rect_arrow(fig, 7.7, 2.1, 7.7, 3.9, green_text)
    add_econ__rect(fig, 6.7, 0.7, 8.3, 6.7, d_sue2_p1, d_sue2_p2, d_sue2_p3, d_sue2_p4)

    green_text = "Green"
    fig.add_trace(
        plotly_Scatter(
            x=[5, 5, 5],
            y=[9, 8.5, 8.0],
            text=[
                "World Listening Structures",
                "Flow of Worlds to Econs",
                "(Requires justification by problem and with unique name)",
            ],
            mode="text",
        )
    )

    return fig


def get_listening_structures3_fig() -> plotly_Figure:
    fig = get_hubunit_base_fig()
    fig.update_yaxes(range=[-4, 10])
    sue_text = "Sue"
    bob_text = "Bob"
    yao_text = "Yao"
    sue_soul_text = f"{sue_text}.{soul_str()}"
    sue_being_text = f"{sue_text}.{being_str()}"
    dir_being_text = f"{being_str()}s dir"
    dir_soul_text = f"{soul_str()}s dir"

    green_text = "Green"
    blue_text = "blue"
    blue_text = "blue"
    add_world_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_soul_text, green_text)
    add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_soul_text)
    add_world_rect(fig, 1.0, -2.0, 2.0, -1.0, sue_being_text, green_text)
    add_direc_rect(fig, 0.7, -2.3, 2.3, -0.7, dir_being_text)

    add_rect_arrow(fig, 3.85, 3.8, 4, 3.6, blue_text)
    add_2_curve(fig, path="M 4,3.6 C 4.3,3.4 7.4,2.1 7.5,2", color=blue_text)
    add_2_curve(fig, path="M 4,3.6 C 4.3,3.4 5.4,2.2 5.5,2", color=blue_text)
    add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=blue_text)
    add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, blue_text)
    # add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 7.4,0.4 7.5,1", color=blue_text)
    # add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 5.4,0.4 5.5,1", color=blue_text)
    add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 3.4,0.4 3.5,1", color=blue_text)
    add_rect_arrow(fig, 1.71, -1.0, 1.75, -0.8, blue_text)

    sue_duty_text = f"{sue_text} duty"
    sue_job_text = f"{sue_text} job"
    bob_job_text = f"{bob_text} job"
    yao_job_text = f"{yao_text} job"
    d_sue1_p1 = f"Healer = {sue_text} "
    d_sue1_p2 = "Problem = problem1"
    d_sue1_p3 = "Econ = project1"
    d_sue1_p4 = f"Money = {default_money_magnitude()} "

    add_world_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_text)
    add_world_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_job_text)
    add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_text)
    add_econ__rect(fig, 2.7, 0.7, 8.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4)
    add_world_rect(fig, 5.0, 1.0, 6.0, 2.0, yao_job_text)
    add_world_rect(fig, 7.0, 1.0, 8.0, 2.0, bob_job_text)

    green_text = "Green"
    fig.add_trace(
        plotly_Scatter(
            x=[5, 5, 5],
            y=[9, 8.5, 8.0],
            text=[
                "World Listening Structures",
                "Flow of Worlds to Econs",
                "(Requires justification by problem and with unique name)",
            ],
            mode="text",
        )
    )

    return fig
