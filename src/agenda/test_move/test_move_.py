from src.agenda.party import partyunit_shop
from src.agenda.move import (
    MoveUnit,
    moveunit_shop,
    stirunit_shop,
    stir_update,
    stir_insert,
    stir_delete,
)
from src.agenda.examples.example_moves import (
    get_sue_personroad,
    get_sue_moveunit_example1,
)


def test_MoveUnit_exists():
    # GIVEN / WHEN
    x_moveunit = MoveUnit()

    # THEN
    assert x_moveunit.agenda_road is None
    assert x_moveunit.stirunits is None


def test_moveunit_shop_ReturnsCorrectObj():
    # GIVEN
    sue_road = get_sue_personroad()

    # WHEN
    sue_moveunit = moveunit_shop(sue_road)

    # THEN
    assert sue_moveunit.agenda_road == sue_road
    assert sue_moveunit.stirunits == {}


def test_MoveUnit_set_stirunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    attribute_value = 55
    category = "AgendaUnit_weight"
    required_args = {category: attribute_value}
    agenda_weight_stirunit = stirunit_shop(
        category, stir_update(), required_args=required_args
    )
    assert sue_moveunit.stirunits == {}
    assert agenda_weight_stirunit.stir_order is None

    # WHEN
    sue_moveunit.set_stirunit(agenda_weight_stirunit)

    # THEN
    assert len(sue_moveunit.stirunits) == 1
    x_update_dict = sue_moveunit.stirunits.get(stir_update())
    # print(f"{x_update_dict=}")
    x_category_stirunit = x_update_dict.get(category)
    print(f"{x_category_stirunit=}")
    assert x_category_stirunit == agenda_weight_stirunit
    assert agenda_weight_stirunit.stir_order != None


def test_MoveUnit_get_stir_ReturnsCorrectObj():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    AgendaUnit_weight_value = 55
    AgendaUnit_weight_text = "AgendaUnit_weight"
    AgendaUnit_weight_stirunit = stirunit_shop(AgendaUnit_weight_text, stir_update())
    AgendaUnit_weight_stirunit.set_required_arg(
        x_key=AgendaUnit_weight_text, x_value=AgendaUnit_weight_value
    )
    sue_moveunit.set_stirunit(AgendaUnit_weight_stirunit)

    # WHEN
    gen_stirunit = sue_moveunit.get_stirunit(
        stir_update(), category=AgendaUnit_weight_text, locator_values=[]
    )

    # THEN
    assert gen_stirunit == AgendaUnit_weight_stirunit


def test_MoveUnit_add_stirunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    assert sue_moveunit.stirunits == {}

    # WHEN
    AgendaUnit_weight_value = 55
    AgendaUnit_weight_text = "AgendaUnit_weight"
    required_args = {AgendaUnit_weight_text: AgendaUnit_weight_value}
    sue_moveunit.add_stirunit(
        AgendaUnit_weight_text, stir_update(), None, required_args
    )

    # THEN
    assert len(sue_moveunit.stirunits) == 1
    x_update_dict = sue_moveunit.stirunits.get(stir_update())
    x_stirunit = x_update_dict.get(AgendaUnit_weight_text)
    assert x_stirunit != None
    assert x_stirunit.category == AgendaUnit_weight_text


def test_MoveUnit_add_stirunit_CorrectlySets_AgendaUnit_partyunits():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    assert sue_moveunit.stirunits == {}

    # WHEN
    party_id_text = "party_id"
    bob_text = "Bob"
    bob_locator_dict = {party_id_text: bob_text}
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(
        bob_text,
        bob_creditor_weight,
        bob_debtor_weight,
        depotlink_type="assignment",
    )
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    bob_required_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    bob_optional_dict = {cw_text: bob_partyunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)
    print(f"{bob_required_dict=}")
    partyunit_text = "partyunit"
    sue_moveunit.add_stirunit(
        category=partyunit_text,
        crud_text=stir_insert(),
        locator=bob_locator_dict,
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )
    # THEN
    assert len(sue_moveunit.stirunits) == 1
    bob_locator_key = f"{partyunit_text} {bob_text}"
    assert (
        sue_moveunit.stirunits.get(stir_insert()).get(partyunit_text).get(bob_text)
        != None
    )


def test_MoveUnit_add_stirunit_CorrectlySets_AgendaUnit_max_tree_traverse():
    # GIVEN
    sue_moveunit = moveunit_shop(get_sue_personroad())
    assert sue_moveunit.stirunits == {}

    # WHEN
    weight_value = 55
    weight_name = "AgendaUnit_weight"
    required_args = {weight_name: weight_value}
    weight_stirunit = stirunit_shop(weight_name, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(weight_stirunit)
    # THEN
    assert len(sue_moveunit.stirunits.get(stir_update()).keys()) == 1
    assert weight_stirunit == sue_moveunit.stirunits.get(stir_update()).get(weight_name)

    # WHEN
    new2_value = 66
    x_attribute = "_max_tree_traverse"
    required_args = {x_attribute: new2_value}
    x_stirunit = stirunit_shop(x_attribute, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(x_stirunit)
    # THEN
    print(f"{sue_moveunit.stirunits.keys()=}")
    print(f"{sue_moveunit.stirunits.get(stir_update()).keys()=}")
    # print(f"{get_all_nondictionary_objs(sue_moveunit.stirunits).get(stir_update())=}")
    assert len(sue_moveunit.stirunits.get(stir_update()).keys()) == 2
    assert x_stirunit == sue_moveunit.stirunits.get(stir_update()).get(x_attribute)

    # WHEN
    new3_value = 77
    x_attribute = "_party_creditor_pool"
    required_args = {x_attribute: new3_value}
    x_stirunit = stirunit_shop(x_attribute, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(x_stirunit)
    # THEN
    assert len(sue_moveunit.stirunits.get(stir_update()).keys()) == 3
    assert x_stirunit == sue_moveunit.stirunits.get(stir_update()).get(x_attribute)

    # WHEN
    new4_value = 88
    x_attribute = "_party_debtor_pool"
    required_args = {x_attribute: new4_value}
    x_stirunit = stirunit_shop(x_attribute, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(x_stirunit)
    # THEN
    assert len(sue_moveunit.stirunits.get(stir_update()).keys()) == 4
    assert x_stirunit == sue_moveunit.stirunits.get(stir_update()).get(x_attribute)

    # WHEN
    new5_value = "override"
    x_attribute = "_meld_strategy"
    required_args = {x_attribute: new5_value}
    x_stirunit = stirunit_shop(x_attribute, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(x_stirunit)
    # THEN
    assert len(sue_moveunit.stirunits.get(stir_update()).keys()) == 5
    assert x_stirunit == sue_moveunit.stirunits.get(stir_update()).get(x_attribute)


def test_MoveUnit_get_stir_order_stirunit_dict_ReturnsCorrectObj():
    # GIVEN
    sue_moveunit = get_sue_moveunit_example1()
    assert len(sue_moveunit.stirunits.get(stir_update()).keys()) == 5
    assert sue_moveunit.stirunits.get(stir_insert()) is None
    assert len(sue_moveunit.stirunits.get(stir_delete()).keys()) == 1

    # WHEN
    sue_stir_order_dict = sue_moveunit.get_stir_order_stirunit_dict()

    # THEN
    assert len(sue_stir_order_dict) == 2
    print(f"{sue_stir_order_dict.keys()=}")
    print(f"{sue_stir_order_dict.get(stir_update())=}")
    assert len(sue_stir_order_dict.get(stir_update())) == 5
    assert len(sue_stir_order_dict.get(stir_delete())) == 1
