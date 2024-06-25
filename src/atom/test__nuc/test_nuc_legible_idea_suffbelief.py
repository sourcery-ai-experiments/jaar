from src.atom.quark import quarkunit_shop, quark_insert, quark_delete
from src.atom.nuc import nucunit_shop, create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_idea_suffbelief_INSERT():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_suffbelief"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_world._road_delimiter}Swimmers"
    swim_quarkunit = quarkunit_shop(category, quark_insert())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(belief_id_text, belief_id_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_world)

    # THEN
    x_str = f"Suffbelief '{belief_id_value}' created for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_suffbelief_DELETE():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_suffbelief"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_world._road_delimiter}Swimmers"
    swim_quarkunit = quarkunit_shop(category, quark_delete())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(belief_id_text, belief_id_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_world)

    # THEN
    x_str = f"Suffbelief '{belief_id_value}' deleted for idea '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
