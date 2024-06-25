from src.atom.quark import quarkunit_shop, quark_update, quark_insert, quark_delete
from src.atom.nuc import nucunit_shop, create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_With_suff_idea_active():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reasonunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_world._road_delimiter}Swimmers"
    suff_idea_active_text = "suff_idea_active"
    suff_idea_active_value = True
    swim_quarkunit = quarkunit_shop(category, quark_insert())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    swim_quarkunit.set_arg(suff_idea_active_text, suff_idea_active_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_world)

    # THEN
    x_str = f"ReasonUnit created for idea '{road_value}' with base '{base_value}'. suff_idea_active={suff_idea_active_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_Without_suff_idea_active():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reasonunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_world._road_delimiter}Swimmers"
    swim_quarkunit = quarkunit_shop(category, quark_insert())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_world)

    # THEN
    x_str = f"ReasonUnit created for idea '{road_value}' with base '{base_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_suff_idea_active_IsTrue():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reasonunit"
    base_text = "base"
    base_value = f"{sue_world._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    suff_idea_active_text = "suff_idea_active"
    suff_idea_active_value = True
    swim_quarkunit = quarkunit_shop(category, quark_update())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    swim_quarkunit.set_arg(suff_idea_active_text, suff_idea_active_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_world)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' transited with suff_idea_active={suff_idea_active_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_suff_idea_active_IsNone():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reasonunit"
    base_text = "base"
    base_value = f"{sue_world._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    swim_quarkunit = quarkunit_shop(category, quark_update())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_world)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' and no longer checks base active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_DELETE():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reasonunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_world._road_delimiter}Swimmers"
    swim_quarkunit = quarkunit_shop(category, quark_delete())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_world)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
