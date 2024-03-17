from src.agenda.atom import agendaatom_shop, atom_update, atom_insert, atom_delete
from src.agenda.book import bookunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_idea_balancelink_INSERT():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_balancelink"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    group_id_text = "group_id"
    group_id_value = f"{sue_agenda._road_delimiter}Swimmers"
    creditor_weight_text = "creditor_weight"
    debtor_weight_text = "debtor_weight"
    creditor_weight_value = 81
    debtor_weight_value = 43
    swim_agendaatom = agendaatom_shop(category, atom_insert())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(group_id_text, group_id_value)
    swim_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    swim_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Balancelink created for group {group_id_value} for idea '{road_value}' with creditor_weight={creditor_weight_value} and debtor_weight={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_balancelink_UPDATE_creditor_weight_debtor_weight():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    category = "agenda_idea_balancelink"
    group_id_text = "group_id"
    group_id_value = f"{sue_agenda._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    creditor_weight_text = "creditor_weight"
    debtor_weight_text = "debtor_weight"
    creditor_weight_value = 81
    debtor_weight_value = 43
    swim_agendaatom = agendaatom_shop(category, atom_update())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(group_id_text, group_id_value)
    swim_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    swim_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Balancelink has been changed for group {group_id_value} for idea '{road_value}'. Now creditor_weight={creditor_weight_value} and debtor_weight={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_balancelink_UPDATE_creditor_weight():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_balancelink"
    group_id_text = "group_id"
    group_id_value = f"{sue_agenda._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    creditor_weight_text = "creditor_weight"
    creditor_weight_value = 81
    swim_agendaatom = agendaatom_shop(category, atom_update())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(group_id_text, group_id_value)
    swim_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Balancelink has been changed for group {group_id_value} for idea '{road_value}'. Now creditor_weight={creditor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_balancelink_UPDATE_debtor_weight():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_balancelink"
    group_id_text = "group_id"
    group_id_value = f"{sue_agenda._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    debtor_weight_text = "debtor_weight"
    debtor_weight_value = 81
    swim_agendaatom = agendaatom_shop(category, atom_update())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(group_id_text, group_id_value)
    swim_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Balancelink has been changed for group {group_id_value} for idea '{road_value}'. Now debtor_weight={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_balancelink_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_idea_balancelink"
    road_text = "road"
    casa_road = sue_agenda.make_l1_road("casa")
    road_value = sue_agenda.make_road(casa_road, "clean fridge")
    group_id_text = "group_id"
    group_id_value = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_delete())
    swim_agendaatom.set_arg(road_text, road_value)
    swim_agendaatom.set_arg(group_id_text, group_id_value)
    # print(f"{swim_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = (
        f"Balancelink for group {group_id_value}, idea '{road_value}' has been deleted."
    )
    print(f"{x_str=}")
    assert legible_list[0] == x_str
