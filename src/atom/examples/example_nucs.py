from src.atom.quark import quark_delete, quark_update, quarkunit_shop
from src.atom.nuc import NucUnit, nucunit_shop


def get_nucunit_carm_example() -> NucUnit:
    sue_nucunit = nucunit_shop()

    agendaunit_text = "agendaunit"
    pool_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    pool_attribute = "_party_creditor_pool"
    pool_quarkunit.set_optional_arg(pool_attribute, 77)
    sue_nucunit.set_quarkunit(pool_quarkunit)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_quarkunit = quarkunit_shop(category, quark_delete())
    carm_quarkunit.set_required_arg("party_id", carm_text)
    sue_nucunit.set_quarkunit(carm_quarkunit)
    return sue_nucunit


def get_nucunit_example1() -> NucUnit:
    sue_nucunit = nucunit_shop()

    agendaunit_text = "agendaunit"
    weight_name = "_weight"
    x_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    x_quarkunit.set_optional_arg(weight_name, 55)
    x_attribute = "_max_tree_traverse"
    x_quarkunit.set_optional_arg(x_attribute, 66)
    x_attribute = "_party_creditor_pool"
    x_quarkunit.set_optional_arg(x_attribute, 77)
    x_attribute = "_party_debtor_pool"
    x_quarkunit.set_optional_arg(x_attribute, 88)
    x_attribute = "_meld_strategy"
    x_quarkunit.set_optional_arg(x_attribute, "override")
    sue_nucunit.set_quarkunit(x_quarkunit)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    x_quarkunit = quarkunit_shop(category, quark_delete())
    x_quarkunit.set_required_arg("party_id", carm_text)
    sue_nucunit.set_quarkunit(x_quarkunit)
    return sue_nucunit
