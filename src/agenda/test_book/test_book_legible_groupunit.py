from src._road.road import create_road
from src.agenda.atom import agendaatom_shop, atom_update, atom_insert, atom_delete
from src.agenda.book import bookunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_groupunit_INSERT_Without_treasury_partylinks():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    category = "agenda_groupunit"
    group_id_text = "group_id"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_insert())
    swim_agendaatom.set_arg(group_id_text, swim_text)
    # swim_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"The group '{swim_text}' was created."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_groupunit_INSERT_With_treasury_partylinks():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    category = "agenda_groupunit"
    group_id_text = "group_id"
    _treasury_partylinks_text = "_treasury_partylinks"
    _treasury_partylinks_road = sue_agenda.make_l1_road("sports")
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_insert())
    swim_agendaatom.set_arg(group_id_text, swim_text)
    swim_agendaatom.set_arg(_treasury_partylinks_text, _treasury_partylinks_road)
    # swim_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"The group '{swim_text}' was created and has {_treasury_partylinks_text}={_treasury_partylinks_road}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_groupunit_UPDATE_With_treasury_partylinks_Populated():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    category = "agenda_groupunit"
    group_id_text = "group_id"
    _treasury_partylinks_text = "_treasury_partylinks"
    _treasury_partylinks_road = sue_agenda.make_l1_road("sports")
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_update())
    swim_agendaatom.set_arg(group_id_text, swim_text)
    swim_agendaatom.set_arg(_treasury_partylinks_text, _treasury_partylinks_road)
    # swim_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"The group '{swim_text}' now has {_treasury_partylinks_text}={_treasury_partylinks_road}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_groupunit_UPDATE_With_treasury_partylinks_Empty():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    category = "agenda_groupunit"
    group_id_text = "group_id"
    _treasury_partylinks_text = "_treasury_partylinks"
    _treasury_partylinks_road = None
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_update())
    swim_agendaatom.set_arg(group_id_text, swim_text)
    swim_agendaatom.set_arg(_treasury_partylinks_text, _treasury_partylinks_road)
    # swim_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"The group '{swim_text}' no longer has {_treasury_partylinks_text}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_groupunit_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    category = "agenda_groupunit"
    group_id_text = "group_id"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    swim_agendaatom = agendaatom_shop(category, atom_delete())
    swim_agendaatom.set_arg(group_id_text, swim_text)
    # swim_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(swim_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"The group '{swim_text}' was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


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
