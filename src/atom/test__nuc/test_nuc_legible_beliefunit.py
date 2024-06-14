from src.atom.quark import quarkunit_shop, quark_update, quark_insert, quark_delete
from src.atom.nuc import nucunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_beliefunit_INSERT():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    category = "agenda_beliefunit"
    belief_id_text = "belief_id"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    swim_quarkunit = quarkunit_shop(category, quark_insert())
    swim_quarkunit.set_arg(belief_id_text, swim_text)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"The belief '{swim_text}' was created."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_beliefunit_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")

    category = "agenda_beliefunit"
    belief_id_text = "belief_id"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    swim_quarkunit = quarkunit_shop(category, quark_delete())
    swim_quarkunit.set_arg(belief_id_text, swim_text)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"The belief '{swim_text}' was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_belief_partylink_INSERT():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_belief_partylink"
    belief_id_text = "belief_id"
    party_id_text = "party_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_quarkunit = quarkunit_shop(category, quark_insert())
    rico_quarkunit.set_arg(belief_id_text, swim_text)
    rico_quarkunit.set_arg(party_id_text, rico_text)
    rico_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    rico_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"Belief '{swim_text}' has new member {rico_text} with belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_belief_partylink_UPDATE_credor_weight_debtor_weight():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_belief_partylink"
    belief_id_text = "belief_id"
    party_id_text = "party_id"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    credor_weight_value = 81
    debtor_weight_value = 43
    rico_quarkunit = quarkunit_shop(category, quark_update())
    rico_quarkunit.set_arg(belief_id_text, swim_text)
    rico_quarkunit.set_arg(party_id_text, rico_text)
    rico_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    rico_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"Belief '{swim_text}' member {rico_text} has new belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_belief_partylink_UPDATE_credor_weight():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_belief_partylink"
    belief_id_text = "belief_id"
    party_id_text = "party_id"
    credor_weight_text = "credor_weight"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    credor_weight_value = 81
    rico_quarkunit = quarkunit_shop(category, quark_update())
    rico_quarkunit.set_arg(belief_id_text, swim_text)
    rico_quarkunit.set_arg(party_id_text, rico_text)
    rico_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"Belief '{swim_text}' member {rico_text} has new belief_cred={credor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_belief_partylink_UPDATE_debtor_weight():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_belief_partylink"
    belief_id_text = "belief_id"
    party_id_text = "party_id"
    debtor_weight_text = "debtor_weight"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    debtor_weight_value = 43
    rico_quarkunit = quarkunit_shop(category, quark_update())
    rico_quarkunit.set_arg(belief_id_text, swim_text)
    rico_quarkunit.set_arg(party_id_text, rico_text)
    rico_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"Belief '{swim_text}' member {rico_text} has new belief_debt={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_belief_partylink_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_belief_partylink"
    belief_id_text = "belief_id"
    party_id_text = "party_id"
    swim_text = f"{sue_agenda._road_delimiter}Swimmers"
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_delete())
    rico_quarkunit.set_arg(belief_id_text, swim_text)
    rico_quarkunit.set_arg(party_id_text, rico_text)
    # print(f"{rico_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(rico_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"Belief '{swim_text}' no longer has member {rico_text}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
