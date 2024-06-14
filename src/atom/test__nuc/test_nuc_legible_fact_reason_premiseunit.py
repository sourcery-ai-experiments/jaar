from src.atom.quark import quarkunit_shop, quark_update, quark_insert, quark_delete
from src.atom.nuc import nucunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_fact_reason_premiseunit_INSERT_WithOutNumericArgs():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reason_premiseunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_agenda.make_l1_road("casa")
    base_value = sue_agenda.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_agenda.make_road(base_value, "dirty")
    swim_quarkunit = quarkunit_shop(category, quark_insert())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    swim_quarkunit.set_arg(need_text, need_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for fact '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_fact_reason_premiseunit_INSERT_WithNumericArgs():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reason_premiseunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_agenda.make_l1_road("casa")
    base_value = sue_agenda.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_agenda.make_road(base_value, "dirty")
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    divisor_value = 7
    nigh_value = 13
    open_value = 17
    swim_quarkunit = quarkunit_shop(category, quark_insert())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    swim_quarkunit.set_arg(need_text, need_value)
    swim_quarkunit.set_arg(divisor_text, divisor_value)
    swim_quarkunit.set_arg(nigh_text, nigh_value)
    swim_quarkunit.set_arg(open_text, open_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for fact '{road_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_fact_reason_premiseunit_UPDATE_WithOutNumericArgs():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reason_premiseunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_agenda.make_l1_road("casa")
    base_value = sue_agenda.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_agenda.make_road(base_value, "dirty")
    swim_quarkunit = quarkunit_shop(category, quark_update())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    swim_quarkunit.set_arg(need_text, need_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for fact '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_fact_reason_premiseunit_UPDATE_WithNumericArgs():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reason_premiseunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_agenda.make_l1_road("casa")
    base_value = sue_agenda.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_agenda.make_road(base_value, "dirty")
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    divisor_value = 7
    nigh_value = 13
    open_value = 17
    swim_quarkunit = quarkunit_shop(category, quark_update())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    swim_quarkunit.set_arg(need_text, need_value)
    swim_quarkunit.set_arg(divisor_text, divisor_value)
    swim_quarkunit.set_arg(nigh_text, nigh_value)
    swim_quarkunit.set_arg(open_text, open_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for fact '{road_value}'. Open={open_value}. Nigh={nigh_value}. Divisor={divisor_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_fact_reason_premiseunit_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_fact_reason_premiseunit"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    base_text = "base"
    casa_road = sue_agenda.make_l1_road("casa")
    base_value = sue_agenda.make_road(casa_road, "fridge status")
    need_text = "need"
    need_value = sue_agenda.make_road(base_value, "dirty")
    swim_quarkunit = quarkunit_shop(category, quark_delete())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(base_text, base_value)
    swim_quarkunit.set_arg(need_text, need_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"PremiseUnit '{need_value}' deleted from reason '{base_value}' for fact '{road_value}'."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
