from src.agenda.atom import agendaatom_shop, atom_update, atom_insert, atom_delete
from src.agenda.book import bookunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_group_partylink_INSERT():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_group_partylink"
    group_id_text = "group_id"
    party_id_text = "party_id"
    creditor_weight_text = "creditor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    creditor_weight_value = 81
    debtor_weight_value = 43
    rico_agendaatom = agendaatom_shop(category, atom_insert())
    rico_agendaatom.set_arg(group_id_text, swim_text)
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Group '{swim_text}' has new member {rico_text} with group_credit={creditor_weight_value} and group_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_group_partylink_UPDATE_creditor_weight_debtor_weight():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_group_partylink"
    group_id_text = "group_id"
    party_id_text = "party_id"
    creditor_weight_text = "creditor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    creditor_weight_value = 81
    debtor_weight_value = 43
    rico_agendaatom = agendaatom_shop(category, atom_update())
    rico_agendaatom.set_arg(group_id_text, swim_text)
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Group '{swim_text}' member {rico_text} has new group_credit={creditor_weight_value} and group_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_group_partylink_UPDATE_creditor_weight():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_group_partylink"
    group_id_text = "group_id"
    party_id_text = "party_id"
    creditor_weight_text = "creditor_weight"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    creditor_weight_value = 81
    rico_agendaatom = agendaatom_shop(category, atom_update())
    rico_agendaatom.set_arg(group_id_text, swim_text)
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Group '{swim_text}' member {rico_text} has new group_credit={creditor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_group_partylink_UPDATE_debtor_weight():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_group_partylink"
    group_id_text = "group_id"
    party_id_text = "party_id"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    debtor_weight_value = 43
    rico_agendaatom = agendaatom_shop(category, atom_update())
    rico_agendaatom.set_arg(group_id_text, swim_text)
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Group '{swim_text}' member {rico_text} has new group_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_group_partylink_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_group_partylink"
    group_id_text = "group_id"
    party_id_text = "party_id"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_delete())
    rico_agendaatom.set_arg(group_id_text, swim_text)
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Group '{swim_text}' no longer has member {rico_text}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_group_partylink_INSERT_money_desc_IsNone():
#     # GIVEN
#     category = "agenda_group_partylink"
#     party_id_text = "party_id"
#     creditor_weight_text = "creditor_weight"
#     debtor_weight_text = "debtor_weight"
#     creditor_weight_value = 81
#     debtor_weight_value = 43
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_insert())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
#     rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = f"{rico_text} was added with {creditor_weight_value} money credit and {debtor_weight_value} money debt"
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_group_partylink_UPDATE_creditor_weight_debtor_weight():
#     # GIVEN
#     category = "agenda_group_partylink"
#     party_id_text = "party_id"
#     creditor_weight_text = "creditor_weight"
#     debtor_weight_text = "debtor_weight"
#     creditor_weight_value = 81
#     debtor_weight_value = 43
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_update())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
#     rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")
#     sue_money_desc = "dragon coins"
#     sue_agenda.set_money_desc(sue_money_desc)

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = f"{rico_text} now has {creditor_weight_value} {sue_agenda._money_desc} credit and {debtor_weight_value} {sue_agenda._money_desc} debt."
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_group_partylink_UPDATE_creditor_weight():
#     # GIVEN
#     category = "agenda_group_partylink"
#     party_id_text = "party_id"
#     creditor_weight_text = "creditor_weight"
#     creditor_weight_value = 81
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_update())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")
#     sue_money_desc = "dragon coins"
#     sue_agenda.set_money_desc(sue_money_desc)

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = (
#         f"{rico_text} now has {creditor_weight_value} {sue_agenda._money_desc} credit."
#     )
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_group_partylink_UPDATE_debtor_weight():
#     # GIVEN
#     category = "agenda_group_partylink"
#     party_id_text = "party_id"
#     debtor_weight_text = "debtor_weight"
#     debtor_weight_value = 43
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_update())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")
#     sue_money_desc = "dragon coins"
#     sue_agenda.set_money_desc(sue_money_desc)

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = f"{rico_text} now has {debtor_weight_value} {sue_agenda._money_desc} debt."
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_group_partylink_DELETE():
#     # GIVEN
#     category = "agenda_group_partylink"
#     party_id_text = "party_id"
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_delete())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")
#     sue_money_desc = "dragon coins"
#     sue_agenda.set_money_desc(sue_money_desc)

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = f"{rico_text} was removed from {sue_agenda._money_desc} partys."
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str
