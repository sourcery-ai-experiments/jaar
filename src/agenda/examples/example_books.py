from src._road.jaar_config import get_test_real_id
from src._road.road import RealID
from src.agenda.atom import (
    AgendaAtom,
    atom_delete,
    atom_update,
    atom_insert,
    agendaatom_shop,
)
from src.agenda.book import BookUnit, bookunit_shop


def get_atom_example_ideaunit_sports(real_id: RealID = None) -> AgendaAtom:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    x_category = "agenda_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_ideaunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    insert_ideaunit_agendaatom.set_required_arg(label_text, sports_text)
    insert_ideaunit_agendaatom.set_required_arg(parent_road_text, real_id)
    return insert_ideaunit_agendaatom


def get_bookunit_carm_example() -> BookUnit:
    sue_bookunit = bookunit_shop()

    agendaunit_text = "agendaunit"
    pool_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    pool_attribute = "_party_creditor_pool"
    pool_agendaatom.set_optional_arg(pool_attribute, 77)
    sue_bookunit.set_agendaatom(pool_agendaatom)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_agendaatom = agendaatom_shop(category, atom_delete())
    carm_agendaatom.set_required_arg("party_id", carm_text)
    sue_bookunit.set_agendaatom(carm_agendaatom)
    return sue_bookunit


def get_bookunit_example1() -> BookUnit:
    sue_bookunit = bookunit_shop()

    agendaunit_text = "agendaunit"
    weight_name = "_weight"
    x_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    x_agendaatom.set_optional_arg(weight_name, 55)
    x_attribute = "_max_tree_traverse"
    x_agendaatom.set_optional_arg(x_attribute, 66)
    x_attribute = "_party_creditor_pool"
    x_agendaatom.set_optional_arg(x_attribute, 77)
    x_attribute = "_party_debtor_pool"
    x_agendaatom.set_optional_arg(x_attribute, 88)
    x_attribute = "_meld_strategy"
    x_agendaatom.set_optional_arg(x_attribute, "override")
    sue_bookunit.set_agendaatom(x_agendaatom)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    x_agendaatom = agendaatom_shop(category, atom_delete())
    x_agendaatom.set_required_arg("party_id", carm_text)
    sue_bookunit.set_agendaatom(x_agendaatom)
    return sue_bookunit


def get_bookunit_example2() -> BookUnit:
    sue_bookunit = bookunit_shop()

    agendaunit_text = "agendaunit"
    x_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    x_attribute = "_party_creditor_pool"
    x_agendaatom.set_optional_arg(x_attribute, 77)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    x_agendaatom = agendaatom_shop(category, atom_delete())
    x_agendaatom.set_required_arg("party_id", carm_text)
    sue_bookunit.set_agendaatom(x_agendaatom)
    return sue_bookunit
