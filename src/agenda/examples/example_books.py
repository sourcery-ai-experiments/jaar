from src.agenda.atom import (
    BookUnit,
    bookunit_shop,
    atom_delete,
    atom_update,
    agendaatom_shop,
)


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

    category = "partyunit"
    carm_text = "Carmen"
    x_agendaatom = agendaatom_shop(category, atom_delete())
    x_agendaatom.set_locator("party_id", carm_text)
    x_agendaatom.set_required_arg("party_id", carm_text)
    sue_bookunit.set_agendaatom(x_agendaatom)
    return sue_bookunit
