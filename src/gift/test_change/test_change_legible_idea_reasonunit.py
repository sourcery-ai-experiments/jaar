from src.gift.atom import atomunit_shop, atom_update, atom_insert, atom_delete
from src.gift.change import changeunit_shop, create_legible_list
from src._world.world import worldunit_shop


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_With_base_idea_active_requisite():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reasonunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_world._road_delimiter}Swimmers"
    base_idea_active_requisite_text = "base_idea_active_requisite"
    base_idea_active_requisite_value = True
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(
        base_idea_active_requisite_text, base_idea_active_requisite_value
    )
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"ReasonUnit created for idea '{road_value}' with base '{base_value}'. base_idea_active_requisite={base_idea_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_Without_base_idea_active_requisite():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reasonunit"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_world._road_delimiter}Swimmers"
    swim_atomunit = atomunit_shop(category, atom_insert())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"ReasonUnit created for idea '{road_value}' with base '{base_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_base_idea_active_requisite_IsTrue():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reasonunit"
    base_text = "base"
    base_value = f"{sue_world._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    base_idea_active_requisite_text = "base_idea_active_requisite"
    base_idea_active_requisite_value = True
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    swim_atomunit.set_arg(
        base_idea_active_requisite_text, base_idea_active_requisite_value
    )
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' transited with base_idea_active_requisite={base_idea_active_requisite_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_base_idea_active_requisite_IsNone():
    # GIVEN
    sue_world = worldunit_shop("Sue")
    category = "world_idea_reasonunit"
    base_text = "base"
    base_value = f"{sue_world._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_world.make_l1_road("casa")
    road_value = sue_world.make_road(casa_road, "clean fridge")
    swim_atomunit = atomunit_shop(category, atom_update())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

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
    swim_atomunit = atomunit_shop(category, atom_delete())
    swim_atomunit.set_arg(road_text, road_value)
    swim_atomunit.set_arg(base_text, base_value)
    # print(f"{swim_atomunit=}")
    x_changeunit = changeunit_shop()
    x_changeunit.set_atomunit(swim_atomunit)

    # WHEN
    legible_list = create_legible_list(x_changeunit, sue_world)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
