from src._prime.road import get_single_roadnode
from src._prime.meld import get_meld_default
from src.agenda.agenda import agendaunit_shop
from src.world.move import (
    MoveUnit,
    moveunit_shop,
    stir_update,
    stir_delete,
    stir_insert,
    stirunit_shop,
)
from src.world.examples.example_deals import get_sue_personroad


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_SimplestScenario():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)

    # WHEN
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
    sue_weight = 55
    before_sue_agendaunit = agendaunit_shop(sue_text, _weight=sue_weight)
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit._weight == sue_weight
    assert after_sue_agendaunit == before_sue_agendaunit


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")

    sue_weight = 44
    before_sue_agendaunit = agendaunit_shop(sue_text, _weight=sue_weight)

    new1_value = 55
    attribute_name = "AgendaUnit._weight"
    x_stirunit = stirunit_shop(attribute_name, stir_update())
    x_stirunit.add_required_arg(attribute_name, new1_value)
    sue_moveunit.set_stirunit(x_stirunit)

    new2_value = 66
    attribute_name = "_max_tree_traverse"
    x_stirunit = stirunit_shop(attribute_name, stir_update())
    x_stirunit.add_required_arg(attribute_name, new2_value)
    sue_moveunit.set_stirunit(x_stirunit)

    new3_value = 77
    attribute_name = "_party_creditor_pool"
    x_stirunit = stirunit_shop(attribute_name, stir_update())
    x_stirunit.add_required_arg(attribute_name, new3_value)
    sue_moveunit.set_stirunit(x_stirunit)

    new4_value = 88
    attribute_name = "_party_debtor_pool"
    x_stirunit = stirunit_shop(attribute_name, stir_update())
    x_stirunit.add_required_arg(attribute_name, new4_value)
    sue_moveunit.set_stirunit(x_stirunit)

    new5_value = "override"
    attribute_name = "_meld_strategy"
    x_stirunit = stirunit_shop(attribute_name, stir_update())
    x_stirunit.add_required_arg(attribute_name, new5_value)
    sue_moveunit.set_stirunit(x_stirunit)

    # WHEN
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    print(f"{sue_moveunit.update_stirs=}")
    assert after_sue_agendaunit._weight == new1_value
    assert after_sue_agendaunit._weight != before_sue_agendaunit._weight
    assert after_sue_agendaunit._max_tree_traverse == new2_value
    assert after_sue_agendaunit._party_creditor_pool == new3_value
    assert after_sue_agendaunit._party_debtor_pool == new4_value
    assert after_sue_agendaunit._meld_strategy == new5_value


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_party():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")

    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_agendaunit.add_partyunit(rico_text)
    before_sue_agendaunit.add_partyunit(carm_text)

    attribute_name = "partyunit"
    x_stirunit = stirunit_shop(attribute_name, stir_delete())
    x_stirunit.add_locator("party_id", carm_text)
    sue_moveunit.set_stirunit(x_stirunit)

    # WHEN
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    print(f"{sue_moveunit.update_stirs=}")
    assert after_sue_agendaunit != before_sue_agendaunit
    assert after_sue_agendaunit.get_party(rico_text) != None
    assert after_sue_agendaunit.get_party(carm_text) is None


# def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_group():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_moveunit = moveunit_shop(sue_road)
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")

#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     rico_text = "Rico"
#     carm_text = "Carmen"
#     before_sue_agendaunit.add_partyunit(rico_text)
#     before_sue_agendaunit.add_partyunit(carm_text)

#     attribute_name = "groupunit"
#     x_stirunit = stirunit_shop(attribute_name, stir_delete())
#     x_stirunit.add_locator("group_id", carm_text)
#     sue_moveunit.set_stirunit(x_stirunit)

#     # WHEN
#     after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     print(f"{sue_moveunit.update_stirs=}")
#     assert after_sue_agendaunit != before_sue_agendaunit
#     assert after_sue_agendaunit.get_party(rico_text) != None
#     assert after_sue_agendaunit.get_party(carm_text) is None
