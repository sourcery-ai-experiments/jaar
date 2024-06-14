from src.atom.quark import quarkunit_shop, quark_update, quark_insert, quark_delete
from src.atom.nuc import nucunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_fact_reasonunit_INSERT_With_suff_fact_active():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reasonunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    suff_fact_active_text = "suff_fact_active"
    suff_fact_active_value = True
    swim_quarkunit = quarkunit_shop(category, quark_insert())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    swim_quarkunit.set_arg(suff_fact_active_text, suff_fact_active_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit created for fact '{road_value}' with base '{base_value}'. suff_fact_active={suff_fact_active_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_fact_reasonunit_INSERT_Without_suff_fact_active():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reasonunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    swim_quarkunit = quarkunit_shop(category, quark_insert())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit created for fact '{road_value}' with base '{base_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_fact_reasonunit_UPDATE_suff_fact_active_IsTrue():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reasonunit"
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    suff_fact_active_text = "suff_fact_active"
    suff_fact_active_value = True
    swim_quarkunit = quarkunit_shop(category, quark_update())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    swim_quarkunit.set_arg(suff_fact_active_text, suff_fact_active_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for fact '{road_value}' transited with suff_fact_active={suff_fact_active_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_fact_reasonunit_UPDATE_suff_fact_active_IsNone():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reasonunit"
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    swim_quarkunit = quarkunit_shop(category, quark_update())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for fact '{road_value}' and no longer checks base active mode."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_fact_reasonunit_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reasonunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    base_value = f"{sue_agenda._road_delimiter}Swimmers"
    swim_quarkunit = quarkunit_shop(category, quark_delete())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"ReasonUnit base='{base_value}' for fact '{road_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
