from src.agenda.party import partyunit_shop
from src.agenda.atom import agendaatom_shop, atom_update, atom_insert, atom_delete
from src.agenda.book import (
    BookUnit,
    bookunit_shop,
    validate_agenda_build_from_book,
    create_legible_list,
)
from src.agenda.agenda import agendaunit_shop
from src.agenda.examples.example_books import get_bookunit_example1
from src.instrument.python import x_is_json
from pytest import raises as pytest_raises


def test_create_legible_list_ReturnsObjGivenEmptyBook():
    # GIVEN / WHEN
    x_bookunit = bookunit_shop()
    sue_agenda = agendaunit_shop("Sue")

    # THEN
    assert create_legible_list(x_bookunit, sue_agenda) == []


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_weight():
    # GIVEN
    category = "agendaunit"
    weight_text = "_weight"
    weight_int = 55
    weight_agendaatom = agendaatom_shop(category, atom_update())
    weight_agendaatom.set_arg(weight_text, weight_int)
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(weight_agendaatom)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{sue_agenda._worker_id}'s agenda weight was changed to {weight_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_money_desc():
    # GIVEN
    category = "agendaunit"
    _money_desc_text = "_money_desc"
    sue_money_desc = "dragon coins"
    _money_desc_agendaatom = agendaatom_shop(category, atom_update())
    _money_desc_agendaatom.set_arg(_money_desc_text, sue_money_desc)
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(_money_desc_agendaatom)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{sue_agenda._worker_id}'s money is now called '{sue_money_desc}'"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_party_creditor_pool():
    # GIVEN
    category = "agendaunit"
    party_creditor_pool_text = "_party_creditor_pool"
    party_creditor_pool_int = 71
    party_creditor_pool_agendaatom = agendaatom_shop(category, atom_update())
    party_creditor_pool_agendaatom.set_arg(
        party_creditor_pool_text, party_creditor_pool_int
    )

    party_creditor_pool_agendaatom._crud_cache = None
    print(f"{party_creditor_pool_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(party_creditor_pool_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{sue_money_desc} creditor pool is now {party_creditor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_party_creditor_pool_With_money_desc_None():
    # GIVEN
    category = "agendaunit"
    party_creditor_pool_text = "_party_creditor_pool"
    party_creditor_pool_int = 71
    party_creditor_pool_agendaatom = agendaatom_shop(category, atom_update())
    party_creditor_pool_agendaatom.set_arg(
        party_creditor_pool_text, party_creditor_pool_int
    )

    party_creditor_pool_agendaatom._crud_cache = None
    print(f"{party_creditor_pool_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(party_creditor_pool_agendaatom)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{sue_agenda._worker_id}'s money creditor pool is now {party_creditor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_party_debtor_pool():
    # GIVEN
    category = "agendaunit"
    party_debtor_pool_text = "_party_debtor_pool"
    party_debtor_pool_int = 78
    party_debtor_pool_agendaatom = agendaatom_shop(category, atom_update())
    party_debtor_pool_agendaatom.set_arg(party_debtor_pool_text, party_debtor_pool_int)

    party_debtor_pool_agendaatom._crud_cache = None
    print(f"{party_debtor_pool_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(party_debtor_pool_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{sue_money_desc} debtor pool is now {party_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_party_creditor_pool_Equal_party_debtor_pool():
    # GIVEN
    x_bookunit = bookunit_shop()
    category = "agendaunit"
    party_creditor_pool_text = "_party_creditor_pool"
    party_debtor_pool_text = "_party_debtor_pool"
    party_pool_int = 83
    agendaunit_agendaatom = agendaatom_shop(category, atom_update())
    agendaunit_agendaatom.set_arg(party_creditor_pool_text, party_pool_int)
    agendaunit_agendaatom.set_arg(party_debtor_pool_text, party_pool_int)
    x_bookunit.set_agendaatom(agendaunit_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{sue_money_desc} total pool is now {party_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_max_tree_traverse():
    # GIVEN
    category = "agendaunit"
    max_tree_traverse_text = "_max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_agendaatom = agendaatom_shop(category, atom_update())
    max_tree_traverse_agendaatom.set_arg(max_tree_traverse_text, max_tree_traverse_int)

    max_tree_traverse_agendaatom._crud_cache = None
    print(f"{max_tree_traverse_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(max_tree_traverse_agendaatom)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{sue_agenda._worker_id}'s maximum number of Agenda output evaluations changed to {max_tree_traverse_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_meld_strategy():
    # GIVEN
    category = "agendaunit"
    meld_strategy_text = "_meld_strategy"
    meld_strategy_value = "override"
    meld_strategy_agendaatom = agendaatom_shop(category, atom_update())
    meld_strategy_agendaatom.set_arg(meld_strategy_text, meld_strategy_value)

    meld_strategy_agendaatom._crud_cache = None
    print(f"{meld_strategy_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(meld_strategy_agendaatom)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = (
        f"{sue_agenda._worker_id}'s Meld strategy changed to '{meld_strategy_value}'"
    )
    assert legible_list[0] == x_str


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
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} was added with {creditor_weight_value} {sue_agenda._money_desc} credit and {debtor_weight_value} {sue_agenda._money_desc} debt"
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partyunit_INSERT_money_desc_IsNone():
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
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} was added with {creditor_weight_value} money credit and {debtor_weight_value} money debt"
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
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} now has {creditor_weight_value} {sue_agenda._money_desc} credit and {debtor_weight_value} {sue_agenda._money_desc} debt."
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
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = (
        f"{rico_text} now has {creditor_weight_value} {sue_agenda._money_desc} credit."
    )
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
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} now has {debtor_weight_value} {sue_agenda._money_desc} debt."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partyunit_DELETE():
    # GIVEN
    category = "agenda_partyunit"
    party_id_text = "party_id"
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_delete())
    rico_agendaatom.set_arg(party_id_text, rico_text)
    rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(rico_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{rico_text} was removed from {sue_agenda._money_desc} partys."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
