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
    agenda_weight_agendaatom = agendaatom_shop(category, atom_update())
    agenda_weight_agendaatom.set_arg(weight_text, weight_int)
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(agenda_weight_agendaatom)
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


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_creditor_weight_pool():
    # GIVEN
    category = "agendaunit"
    party_creditor_pool_text = "_party_creditor_pool"
    party_creditor_pool_int = 71
    agenda_creditor_weight_agendaatom = agendaatom_shop(category, atom_update())
    agenda_creditor_weight_agendaatom.set_arg(
        party_creditor_pool_text, party_creditor_pool_int
    )

    agenda_creditor_weight_agendaatom._crud_cache = None
    print(f"{agenda_creditor_weight_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(agenda_creditor_weight_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{sue_money_desc} creditor pool is now {party_creditor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_debtor_weight_pool():
    # GIVEN
    category = "agendaunit"
    party_debtor_pool_text = "_party_debtor_pool"
    party_debtor_pool_int = 78
    agenda_debtor_weight_agendaatom = agendaatom_shop(category, atom_update())
    agenda_debtor_weight_agendaatom.set_arg(
        party_debtor_pool_text, party_debtor_pool_int
    )

    agenda_debtor_weight_agendaatom._crud_cache = None
    print(f"{agenda_debtor_weight_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(agenda_debtor_weight_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_money_desc = "dragon coins"
    sue_agenda.set_money_desc(sue_money_desc)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"{sue_money_desc} debtor pool is now {party_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenAgendaUpdate_creditor_weight_pool_Equal_debtor_weight_pool():
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
