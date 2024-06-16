from src.atom.quark import quarkunit_shop, quark_update, quark_insert, quark_delete
from src.atom.nuc import nucunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_guyunit_INSERT():
    # GIVEN
    category = "agenda_guyunit"
    guy_id_text = "guy_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_insert())
    rico_quarkunit.set_arg(guy_id_text, rico_text)
    rico_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    rico_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} was added with {credor_weight_value} {sue_agenda._monetary_desc} cred and {debtor_weight_value} {sue_agenda._monetary_desc} debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_guyunit_INSERT_monetary_desc_IsNone():
    # GIVEN
    category = "agenda_guyunit"
    guy_id_text = "guy_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_insert())
    rico_quarkunit.set_arg(guy_id_text, rico_text)
    rico_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    rico_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} was added with {credor_weight_value} monetary_desc cred and {debtor_weight_value} monetary_desc debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_guyunit_UPDATE_credor_weight_debtor_weight():
    # GIVEN
    category = "agenda_guyunit"
    guy_id_text = "guy_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_update())
    rico_quarkunit.set_arg(guy_id_text, rico_text)
    rico_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    rico_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} now has {credor_weight_value} {sue_agenda._monetary_desc} cred and {debtor_weight_value} {sue_agenda._monetary_desc} debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_guyunit_UPDATE_credor_weight():
    # GIVEN
    category = "agenda_guyunit"
    guy_id_text = "guy_id"
    credor_weight_text = "credor_weight"
    credor_weight_value = 81
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_update())
    rico_quarkunit.set_arg(guy_id_text, rico_text)
    rico_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = (
        f"{rico_text} now has {credor_weight_value} {sue_agenda._monetary_desc} cred."
    )
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_guyunit_UPDATE_debtor_weight():
    # GIVEN
    category = "agenda_guyunit"
    guy_id_text = "guy_id"
    debtor_weight_text = "debtor_weight"
    debtor_weight_value = 43
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_update())
    rico_quarkunit.set_arg(guy_id_text, rico_text)
    rico_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = (
        f"{rico_text} now has {debtor_weight_value} {sue_agenda._monetary_desc} debt."
    )
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_guyunit_DELETE():
    # GIVEN
    category = "agenda_guyunit"
    guy_id_text = "guy_id"
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_delete())
    rico_quarkunit.set_arg(guy_id_text, rico_text)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} was removed from {sue_agenda._monetary_desc} guys."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
