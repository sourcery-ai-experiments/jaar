from src._prime.road import (
    create_road,
    create_economyaddress,
    PersonRoad,
    create_road_from_nodes as roadnodes,
)
from src.world.move import (
    MoveUnit,
    stirunit_shop,
    moveunit_shop,
    stir_update,
    stir_delete,
)
from src.world.deal import dealunit_shop, DealUnit, vowunit_shop
from src.world.examples.example_topics import get_no_topiclinks_vowunit


def get_bob_personroad() -> PersonRoad:
    bob_text = "Bob"
    food_text = "Hunger"
    yao_text = "Yao"
    ohio_text = "Ohio"
    return roadnodes([bob_text, food_text, yao_text, ohio_text])


def get_sue_personroad() -> PersonRoad:
    sue_text = "Sue"
    food_text = "Hunger"
    yao_text = "Yao"
    ohio_text = "Ohio"
    return roadnodes([sue_text, food_text, yao_text, ohio_text])


def get_yao_personroad() -> PersonRoad:
    yao_text = "Yao"
    food_text = "Hunger"
    ohio_text = "Ohio"
    return roadnodes([yao_text, food_text, yao_text, ohio_text])


def get_no_topiclinks_yao_sue_dealunit() -> DealUnit:
    yao_sue_dealunit = dealunit_shop(get_yao_personroad(), get_sue_personroad())
    yao_sue_dealunit.set_vowunit(vowunit_shop(1, author_weight=12, reader_weight=7))
    yao_sue_dealunit.set_vowunit(vowunit_shop(1, author_weight=28, reader_weight=28))
    return yao_sue_dealunit


def get_sue_moveunit_example1() -> MoveUnit:
    sue_moveunit = moveunit_shop(get_sue_personroad())

    weight_name = "AgendaUnit_weight"
    weight_stirunit = stirunit_shop(weight_name, stir_update())
    weight_stirunit.add_required_arg(weight_name, 55)
    sue_moveunit.set_stirunit(weight_stirunit)

    x_attribute = "_max_tree_traverse"
    x_stirunit = stirunit_shop(x_attribute, stir_update())
    x_stirunit.add_required_arg(x_attribute, 66)
    sue_moveunit.set_stirunit(x_stirunit)

    x_attribute = "_party_creditor_pool"
    x_stirunit = stirunit_shop(x_attribute, stir_update())
    x_stirunit.add_required_arg(x_attribute, 77)
    sue_moveunit.set_stirunit(x_stirunit)

    x_attribute = "_party_debtor_pool"
    x_stirunit = stirunit_shop(x_attribute, stir_update())
    x_stirunit.add_required_arg(x_attribute, 88)
    sue_moveunit.set_stirunit(x_stirunit)

    x_attribute = "_meld_strategy"
    x_stirunit = stirunit_shop(x_attribute, stir_update())
    x_stirunit.add_required_arg(x_attribute, "override")
    sue_moveunit.set_stirunit(x_stirunit)

    category = "partyunit"
    carm_text = "Carmen"
    x_stirunit = stirunit_shop(category, stir_delete())
    x_stirunit.add_locator("party_id", carm_text)
    sue_moveunit.set_stirunit(x_stirunit)
    return sue_moveunit
