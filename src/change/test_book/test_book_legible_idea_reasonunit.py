from src.change.atom import agendaatom_shop, atom_update, atom_insert, atom_delete
from src.change.book import bookunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_With_suff_idea_active():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_reasonunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    suff_idea_active_text = "suff_idea_active"
    suff_idea_active_value = True
    swim_agendaatom = agendaatom_shop(category, atom_insert())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(base_text, base_value)
    swim_agendaatom.set_arg(suff_idea_active_text, suff_idea_active_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit created for idea '{road_value}' with base '{base_value}'. suff_idea_active={suff_idea_active_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_INSERT_Without_suff_idea_active():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_reasonunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_insert())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(base_text, base_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit created for idea '{road_value}' with base '{base_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_suff_idea_active_IsTrue():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_reasonunit"
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    suff_idea_active_text = "suff_idea_active"
    suff_idea_active_value = True
    swim_agendaatom = agendaatom_shop(category, atom_update())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(base_text, base_value)
    swim_agendaatom.set_arg(suff_idea_active_text, suff_idea_active_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' transited with suff_idea_active={suff_idea_active_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_UPDATE_suff_idea_active_IsNone():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_reasonunit"
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    swim_agendaatom = agendaatom_shop(category, atom_update())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(base_text, base_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' and no longer checks base active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_reasonunit_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_reasonunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_delete())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(base_text, base_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
