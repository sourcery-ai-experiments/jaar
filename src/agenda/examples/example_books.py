from src._road.road import PersonRoad, create_road_from_nodes as roadnodes
from src.agenda.book import (
    BookUnit,
    bookunit_shop,
    learn_delete,
    learn_update,
    learnunit_shop,
)


def get_yao_example_roadunit() -> PersonRoad:
    yao_text = "Yao"
    food_text = "Hunger"
    ohio_text = "Ohio"
    sports_text = "sports"
    run_text = "running"
    return roadnodes([yao_text, food_text, yao_text, ohio_text, sports_text, run_text])


def get_sue_bookunit_example1() -> BookUnit:
    sue_bookunit = bookunit_shop()

    agendaunit_text = "agendaunit"
    weight_name = "_weight"
    x_learnunit = learnunit_shop(agendaunit_text, learn_update())
    x_learnunit.set_optional_arg(weight_name, 55)
    x_attribute = "_max_tree_traverse"
    x_learnunit.set_optional_arg(x_attribute, 66)
    x_attribute = "_party_creditor_pool"
    x_learnunit.set_optional_arg(x_attribute, 77)
    x_attribute = "_party_debtor_pool"
    x_learnunit.set_optional_arg(x_attribute, 88)
    x_attribute = "_meld_strategy"
    x_learnunit.set_optional_arg(x_attribute, "override")
    sue_bookunit.set_learnunit(x_learnunit)

    category = "partyunit"
    carm_text = "Carmen"
    x_learnunit = learnunit_shop(category, learn_delete())
    x_learnunit.set_locator("party_id", carm_text)
    x_learnunit.set_required_arg("party_id", carm_text)
    sue_bookunit.set_learnunit(x_learnunit)
    return sue_bookunit
