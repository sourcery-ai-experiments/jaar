from src.atom.quark import quarkunit_shop, quark_update
from src.atom.nuc import nucunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObjGivenEmptyNuc():
    # GIVEN / WHEN
    x_nucunit = nucunit_shop()
    sue_agenda = agendaunit_shop("Sue")

    # THEN
    assert create_legible_list(x_nucunit, sue_agenda) == []


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_weight():
    # GIVEN
    category = "agendaunit"
    weight_text = "_weight"
    weight_int = 55
    weight_quarkunit = quarkunit_shop(category, quark_update())
    weight_quarkunit.set_arg(weight_text, weight_int)
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(weight_quarkunit)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{sue_agenda._owner_id}'s agenda weight was transited to {weight_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_monetary_desc():
    # GIVEN
    category = "agendaunit"
    _monetary_desc_text = "_monetary_desc"
    sue_monetary_desc = "dragon funds"
    _monetary_desc_quarkunit = quarkunit_shop(category, quark_update())
    _monetary_desc_quarkunit.set_arg(_monetary_desc_text, sue_monetary_desc)
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(_monetary_desc_quarkunit)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = (
        f"{sue_agenda._owner_id}'s monetary_desc is now called '{sue_monetary_desc}'"
    )
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_party_credor_pool():
    # GIVEN
    category = "agendaunit"
    party_credor_pool_text = "_party_credor_pool"
    party_credor_pool_int = 71
    party_credor_pool_quarkunit = quarkunit_shop(category, quark_update())
    party_credor_pool_quarkunit.set_arg(party_credor_pool_text, party_credor_pool_int)

    print(f"{party_credor_pool_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(party_credor_pool_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{sue_monetary_desc} credor pool is now {party_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_party_credor_pool_With_monetary_desc_None():
    # GIVEN
    category = "agendaunit"
    party_credor_pool_text = "_party_credor_pool"
    party_credor_pool_int = 71
    party_credor_pool_quarkunit = quarkunit_shop(category, quark_update())
    party_credor_pool_quarkunit.set_arg(party_credor_pool_text, party_credor_pool_int)

    print(f"{party_credor_pool_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(party_credor_pool_quarkunit)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{sue_agenda._owner_id}'s monetary_desc credor pool is now {party_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_party_debtor_pool():
    # GIVEN
    category = "agendaunit"
    party_debtor_pool_text = "_party_debtor_pool"
    party_debtor_pool_int = 78
    party_debtor_pool_quarkunit = quarkunit_shop(category, quark_update())
    party_debtor_pool_quarkunit.set_arg(party_debtor_pool_text, party_debtor_pool_int)

    print(f"{party_debtor_pool_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(party_debtor_pool_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{sue_monetary_desc} debtor pool is now {party_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_party_credor_pool_Equal_party_debtor_pool():
    # GIVEN
    x_nucunit = nucunit_shop()
    category = "agendaunit"
    party_credor_pool_text = "_party_credor_pool"
    party_debtor_pool_text = "_party_debtor_pool"
    party_pool_int = 83
    agendaunit_quarkunit = quarkunit_shop(category, quark_update())
    agendaunit_quarkunit.set_arg(party_credor_pool_text, party_pool_int)
    agendaunit_quarkunit.set_arg(party_debtor_pool_text, party_pool_int)
    x_nucunit.set_quarkunit(agendaunit_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_agenda.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{sue_monetary_desc} total pool is now {party_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_max_tree_traverse():
    # GIVEN
    category = "agendaunit"
    max_tree_traverse_text = "_max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_quarkunit = quarkunit_shop(category, quark_update())
    max_tree_traverse_quarkunit.set_arg(max_tree_traverse_text, max_tree_traverse_int)

    print(f"{max_tree_traverse_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(max_tree_traverse_quarkunit)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = f"{sue_agenda._owner_id}'s maximum number of Agenda output evaluations transited to {max_tree_traverse_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_meld_strategy():
    # GIVEN
    category = "agendaunit"
    meld_strategy_text = "_meld_strategy"
    meld_strategy_value = "override"
    meld_strategy_quarkunit = quarkunit_shop(category, quark_update())
    meld_strategy_quarkunit.set_arg(meld_strategy_text, meld_strategy_value)

    print(f"{meld_strategy_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(meld_strategy_quarkunit)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_agenda)

    # THEN
    x_str = (
        f"{sue_agenda._owner_id}'s Meld strategy transited to '{meld_strategy_value}'"
    )
    assert legible_list[0] == x_str
