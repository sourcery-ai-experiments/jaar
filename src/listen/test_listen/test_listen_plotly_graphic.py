# from src._world.examples.example_worlds import (
#     world_v001_with_large_agenda,
#     get_world_with_4_levels,
#     get_world_with_4_levels_and_2reasons,
#     get_world_x1_3levels_1reason_1facts,
# )
# from src._world.world import worldunit_shop
from src.listen.listen_graphic import (
    get_listening_structures0_fig,
    get_listening_structures1_fig,
    get_listening_structures2_fig,
    get_listening_structures3_fig,
)


def test_atomunit_periodic_table0_ShowsExplanation0Graph():
    # GIVEN / WHEN
    listening_structures0_fig = get_listening_structures0_fig()
    listening_structures1_fig = get_listening_structures1_fig()
    listening_structures2_fig = get_listening_structures2_fig()
    listening_structures3_fig = get_listening_structures3_fig()

    # # THEN
    # show_figure = True
    # if show_figure:
    #     # listening_structures0_fig.show()
    #     # listening_structures1_fig.show()
    #     # listening_structures2_fig.show()
    #     listening_structures3_fig.show()

    # assert 1 == 2

    # # a_world = get_1node_world()
    # # a_world = get_2node_world()
    # # a_world = get_3node_world()
    # # a_world = get_5nodeHG_world()
    # # a_world = get_7nodeJRoot_world()
    # a_world = get_world_with_4_levels()
    # # a_world = world_v001()
    # a_world.calc_world_metrics()
    # print(f"World {a_world._real_id}: Nodes ({len(a_world._idea_dict)})")

    # # WHEN
    # x_fig = concept_world_level0(a_world)

    # # THEN
    # show_figure = True
    # if show_figure:
    #     x_fig.show()
