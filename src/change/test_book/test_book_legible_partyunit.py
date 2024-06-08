from src.change.atom import agendaatom_shop, atom_update, atom_insert, atom_delete
from src.change.book import bookunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_partyunit_INSERT():
    # GIVEN
    category = "agenda_partyunit"
    party_id_text = "party_id"
    creditor_weight_text = "creditor_weight"
    debtor_weight_text = "debtor_weight"
    creditor_weight_value = 81
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_insert())
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} was added with {creditor_weight_value} {sue_agenda._monetary_desc} credit and {debtor_weight_value} {sue_agenda._monetary_desc} debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partyunit_INSERT_monetary_desc_IsNone():
    # GIVEN
    category = "agenda_partyunit"
    party_id_text = "party_id"
    creditor_weight_text = "creditor_weight"
    debtor_weight_text = "debtor_weight"
    creditor_weight_value = 81
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_insert())
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} was added with {creditor_weight_value} monetary_desc credit and {debtor_weight_value} monetary_desc debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partyunit_UPDATE_creditor_weight_debtor_weight():
    # GIVEN
    category = "agenda_partyunit"
    party_id_text = "party_id"
    creditor_weight_text = "creditor_weight"
    debtor_weight_text = "debtor_weight"
    creditor_weight_value = 81
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_update())
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} now has {creditor_weight_value} {sue_agenda._monetary_desc} credit and {debtor_weight_value} {sue_agenda._monetary_desc} debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partyunit_UPDATE_creditor_weight():
    # GIVEN
    category = "agenda_partyunit"
    party_id_text = "party_id"
    creditor_weight_text = "creditor_weight"
    creditor_weight_value = 81
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_update())
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} now has {creditor_weight_value} {sue_agenda._monetary_desc} credit."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partyunit_UPDATE_debtor_weight():
    # GIVEN
    category = "agenda_partyunit"
    party_id_text = "party_id"
    debtor_weight_text = "debtor_weight"
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_update())
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = (
        f"{rico_text} now has {debtor_weight_value} {sue_agenda._monetary_desc} debt."
    )
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partyunit_DELETE():
    # GIVEN
    category = "agenda_partyunit"
    party_id_text = "party_id"
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_delete())
    rico_agendaatom.set_arg(party_id_text, rico_text)
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} was removed from {sue_agenda._monetary_desc} partys."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
