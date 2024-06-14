from src._road.jaar_config import get_test_real_id
from src._road.road import RealID
from src.atom.quark import (
    QuarkUnit,
    quark_delete,
    quark_update,
    quark_insert,
    quarkunit_shop,
)
from src.atom.nuc import NucUnit, nucunit_shop


def get_quark_example_oathunit_sports(real_id: RealID = None) -> QuarkUnit:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    x_category = "agenda_oathunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_oathunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_oathunit_quarkunit.set_required_arg(label_text, sports_text)
    insert_oathunit_quarkunit.set_required_arg(parent_road_text, real_id)
    return insert_oathunit_quarkunit


def get_nucunit_carm_example() -> NucUnit:
    sue_nucunit = nucunit_shop()

    agendaunit_text = "agendaunit"
    pool_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    pool_attribute = "_party_credor_pool"
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
    x_attribute = "_party_credor_pool"
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


def get_nucunit_example2() -> NucUnit:
    sue_nucunit = nucunit_shop()

    agendaunit_text = "agendaunit"
    x_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    x_attribute = "_party_credor_pool"
    x_quarkunit.set_optional_arg(x_attribute, 77)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    x_quarkunit = quarkunit_shop(category, quark_delete())
    x_quarkunit.set_required_arg("party_id", carm_text)
    sue_nucunit.set_quarkunit(x_quarkunit)
    return sue_nucunit
