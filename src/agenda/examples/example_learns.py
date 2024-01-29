from src._prime.road import PersonRoad, create_road_from_nodes as roadnodes
from src.agenda.learn import (
    LearnUnit,
    learnunit_shop,
    grain_delete,
    grain_update,
    grainunit_shop,
)


def get_sue_personroad() -> PersonRoad:
    sue_text = "Sue"
    food_text = "Hunger"
    yao_text = "Yao"
    ohio_text = "Ohio"
    return roadnodes([sue_text, food_text, yao_text, ohio_text])


def get_yao_example_roadunit() -> PersonRoad:
    yao_text = "Yao"
    food_text = "Hunger"
    ohio_text = "Ohio"
    sports_text = "sports"
    run_text = "running"
    return roadnodes([yao_text, food_text, yao_text, ohio_text, sports_text, run_text])


def get_sue_learnunit_example1() -> LearnUnit:
    sue_learnunit = learnunit_shop(get_sue_personroad())

    weight_name = "AgendaUnit_weight"
    weight_grainunit = grainunit_shop(weight_name, grain_update())
    weight_grainunit.set_required_arg(weight_name, 55)
    sue_learnunit.set_grainunit(weight_grainunit)

    x_attribute = "_max_tree_traverse"
    x_grainunit = grainunit_shop(x_attribute, grain_update())
    x_grainunit.set_required_arg(x_attribute, 66)
    sue_learnunit.set_grainunit(x_grainunit)

    x_attribute = "_party_creditor_pool"
    x_grainunit = grainunit_shop(x_attribute, grain_update())
    x_grainunit.set_required_arg(x_attribute, 77)
    sue_learnunit.set_grainunit(x_grainunit)

    x_attribute = "_party_debtor_pool"
    x_grainunit = grainunit_shop(x_attribute, grain_update())
    x_grainunit.set_required_arg(x_attribute, 88)
    sue_learnunit.set_grainunit(x_grainunit)

    x_attribute = "_meld_strategy"
    x_grainunit = grainunit_shop(x_attribute, grain_update())
    x_grainunit.set_required_arg(x_attribute, "override")
    sue_learnunit.set_grainunit(x_grainunit)

    category = "partyunit"
    carm_text = "Carmen"
    x_grainunit = grainunit_shop(category, grain_delete())
    x_grainunit.set_locator("party_id", carm_text)
    sue_learnunit.set_grainunit(x_grainunit)
    return sue_learnunit
