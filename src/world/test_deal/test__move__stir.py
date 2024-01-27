from src.agenda.party import partyunit_shop
from src.world.move import (
    moveunit_shop,
    StirUnit,
    stirunit_shop,
    stir_insert,
    stir_delete,
    stir_update,
    attribute_ref,
    is_attribute_ref,
)
from src.world.examples.example_deals import get_sue_personroad


def test_attribute_ref_ReturnsCorrectObj():
    idea_text = "idea"
    assert attribute_ref() == {
        "AgendaUnit._weight",
        "_max_tree_traverse",
        "_party_creditor_pool",
        "_party_debtor_pool",
        "_auto_output_to_forum",
        "_meld_strategy",
        "partyunit",
        "groupunit",
        "groupunit_partylink",
        idea_text,
    }
    assert "partyunit" in attribute_ref()
    assert is_attribute_ref(idea_text)
    assert is_attribute_ref("idearoot") == False


def test_StirUnit_exists():
    # GIVEN / WHEN
    x_stirunit = StirUnit()

    # THEN
    x_stirunit.attribute_name is None
    x_stirunit.crud_command is None
    x_stirunit.locator is None
    x_stirunit.required_args is None
    x_stirunit.optional_args is None


def test_stirunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_party_id = "Bob"
    bob_locator_dict = {"party_id": bob_party_id}
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_party_id, bob_creditor_weight, bob_debtor_weight)
    cw_text = "_creditor_weight"
    dw_text = "_debtor_weight"
    bob_partyunit_dict = {cw_text: bob_partyunit.get_dict().get(cw_text)}
    bob_partyunit_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)

    partyunit_text = "partyunit"

    # WHEN
    x_stirunit = stirunit_shop(
        attribute_name=partyunit_text,
        crud_command=stir_insert(),
        locator=bob_locator_dict,
        required_args=bob_partyunit_dict,
        optional_args=None,
    )

    # THEN
    print(f"{x_stirunit=}")
    assert x_stirunit.attribute_name == partyunit_text
    assert x_stirunit.crud_command == stir_insert()
    assert x_stirunit.locator == bob_locator_dict
    assert x_stirunit.required_args == bob_partyunit_dict
    assert x_stirunit.optional_args == {}


def test_StirUnit_add_required_arg_CorrectlySetsAttr():
    # GIVEN
    bob_party_id = "Bob"
    partyunit_text = "partyunit"
    partyunit_stirunit = stirunit_shop(partyunit_text, stir_insert())
    assert partyunit_stirunit.required_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_stirunit.add_required_arg(x_key=party_id_text, x_value=bob_party_id)

    # THEN
    assert partyunit_stirunit.required_args == {party_id_text: bob_party_id}


def test_StirUnit_add_locator_CorrectlySetsAttr():
    # GIVEN
    bob_party_id = "Bob"
    partyunit_text = "partyunit"
    partyunit_stirunit = stirunit_shop(partyunit_text, stir_insert())
    assert partyunit_stirunit.locator == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_stirunit.add_locator(x_key=party_id_text, x_value=bob_party_id)

    # THEN
    assert partyunit_stirunit.locator == {party_id_text: bob_party_id}


def test_StirUnit_get_locator_ReturnsCorrectObj():
    # GIVEN
    bob_party_id = "Bob"
    partyunit_text = "partyunit"
    partyunit_stirunit = stirunit_shop(partyunit_text, stir_insert())
    party_id_text = "party_id"
    partyunit_stirunit.add_locator(x_key=party_id_text, x_value=bob_party_id)

    # WHEN / THEN
    assert partyunit_stirunit.get_locator(party_id_text) == bob_party_id


def test_StirUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_INSERT():
    bob_party_id = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_party_id, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "partyunit"

    # WHEN
    bob_insert_stirunit = stirunit_shop(partyunit_text, crud_command=stir_insert())

    # THEN
    assert bob_insert_stirunit.is_locator_valid() == False
    assert bob_insert_stirunit.is_args_valid() == False
    assert bob_insert_stirunit.is_valid() == False

    # WHEN
    party_id_text = "party_id"
    bob_locator_dict = {party_id_text: bob_party_id}
    bob_insert_stirunit.locator = bob_locator_dict

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_args_valid() == False
    assert bob_insert_stirunit.is_valid() == False

    # WHEN
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    bob_partyunit_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    bob_partyunit_dict[cw_text] = bob_partyunit.get_dict().get(cw_text)
    bob_partyunit_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)
    bob_insert_stirunit.required_args = bob_partyunit_dict

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_args_valid()
    assert bob_insert_stirunit.is_valid()

    # WHEN
    bob_insert_stirunit.crud_command = None

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_args_valid() == False
    assert bob_insert_stirunit.is_valid() == False

    # WHEN
    bob_insert_stirunit.crud_command = stir_insert()

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_args_valid()
    assert bob_insert_stirunit.is_valid()


def test_StirUnit_get_value_ReturnsObj():
    # GIVEN
    bob_party_id = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_party_id, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "partyunit"
    bob_insert_stirunit = stirunit_shop(partyunit_text, stir_insert())
    bob_locator_dict = {"party_id": bob_party_id}
    bob_insert_stirunit.locator = bob_locator_dict
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    bob_partyunit_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    bob_partyunit_dict[cw_text] = bob_partyunit.get_dict().get(cw_text)
    bob_partyunit_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)
    print(f"{bob_partyunit_dict=}")
    bob_insert_stirunit.required_args = bob_partyunit_dict
    assert bob_insert_stirunit.is_valid()

    # WHEN / THEN
    assert bob_insert_stirunit.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_stirunit.get_value(dw_text) == bob_debtor_weight


def test_StirUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_DELETE():
    bob_party_id = "Bob"
    partyunit_text = "partyunit"
    delete_text = stir_delete()

    # WHEN
    bob_delete_stirunit = stirunit_shop(partyunit_text, crud_command=delete_text)

    # THEN
    assert bob_delete_stirunit.is_locator_valid() == False
    assert bob_delete_stirunit.is_args_valid()
    assert bob_delete_stirunit.is_valid() == False

    # WHEN
    bob_locator_dict = {"party_id": bob_party_id}
    bob_delete_stirunit.locator = bob_locator_dict

    # THEN
    assert bob_delete_stirunit.is_locator_valid()
    assert bob_delete_stirunit.is_args_valid()
    assert bob_delete_stirunit.is_valid()


def test_MoveUnit_set_stirunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    assert sue_moveunit.update_stirs == {}

    # WHEN
    attribute_value = 55
    attribute_name = "AgendaUnit._weight"
    required_args = {attribute_name: attribute_value}
    agenda_weight_stirunit = stirunit_shop(
        attribute_name, stir_update(), required_args=required_args
    )
    sue_moveunit.set_stirunit(agenda_weight_stirunit)

    # THEN
    assert len(sue_moveunit.update_stirs) == 1
    x_stirunit = sue_moveunit.update_stirs.get(attribute_name)
    assert x_stirunit == agenda_weight_stirunit


def test_MoveUnit_get_stir_ReturnsCorrectObj():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    w_value = 55
    w_name = "AgendaUnit._weight"
    w_stirunit = stirunit_shop(w_name, stir_update())
    w_stirunit.add_required_arg(x_key=w_name, x_value=w_value)
    sue_moveunit.set_stirunit(w_stirunit)

    # WHEN
    gen_stirunit = sue_moveunit.get_stir(stir_update(), attribute_name=w_name)

    # THEN
    assert gen_stirunit == w_stirunit


def test_MoveUnit_add_stirunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    assert sue_moveunit.update_stirs == {}

    # WHEN
    attribute_value = 55
    attribute_name = "AgendaUnit._weight"
    required_args = {attribute_name: attribute_value}
    sue_moveunit.add_stirunit(attribute_name, stir_update(), None, required_args)

    # THEN
    assert len(sue_moveunit.update_stirs) == 1
    x_stirunit = sue_moveunit.update_stirs.get(attribute_name)
    assert x_stirunit != None


def test_MoveUnit_add_stirunit_CorrectlySets_AgendaUnit_partyunits():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    assert sue_moveunit.insert_stirs == {}

    # WHEN
    party_id_text = "party_id"
    bob_party_id = "Bob"
    bob_locator_dict = {party_id_text: bob_party_id}
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(
        bob_party_id,
        bob_creditor_weight,
        bob_debtor_weight,
        depotlink_type="assignment",
    )
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    bob_required_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    bob_required_dict[cw_text] = bob_partyunit.get_dict().get(cw_text)
    bob_required_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)
    print(f"{bob_required_dict=}")
    partyunit_text = "partyunit"
    sue_moveunit.add_stirunit(
        attribute_name=partyunit_text,
        stir_crud=stir_insert(),
        locator=bob_locator_dict,
        required_args=bob_required_dict,
    )
    # THEN
    assert len(sue_moveunit.insert_stirs) == 1
    assert sue_moveunit.insert_stirs.get(partyunit_text) != None

    # Delete RecordLocator="party_id"
    # Update RecordLocator="party_id", "creditor_weight", "debtor_weight"


def test_MoveUnit_add_stirunit_CorrectlySets_AgendaUnit_max_tree_traverse():
    # GIVEN
    sue_moveunit = moveunit_shop(get_sue_personroad())
    assert sue_moveunit.update_stirs == {}

    # WHEN
    weight_value = 55
    weight_name = "AgendaUnit._weight"
    required_args = {weight_name: weight_value}
    weight_stirunit = stirunit_shop(weight_name, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(weight_stirunit)
    # THEN
    assert len(sue_moveunit.update_stirs) == 1
    assert weight_stirunit == sue_moveunit.update_stirs.get(weight_name)

    # WHEN
    new2_value = 66
    x_attribute = "_max_tree_traverse"
    required_args = {x_attribute: new2_value}
    x_stirunit = stirunit_shop(x_attribute, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(x_stirunit)
    # THEN
    assert len(sue_moveunit.update_stirs) == 2
    assert x_stirunit == sue_moveunit.update_stirs.get(x_attribute)

    # WHEN
    new3_value = 77
    x_attribute = "_party_creditor_pool"
    required_args = {x_attribute: new3_value}
    x_stirunit = stirunit_shop(x_attribute, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(x_stirunit)
    # THEN
    assert len(sue_moveunit.update_stirs) == 3
    assert x_stirunit == sue_moveunit.update_stirs.get(x_attribute)

    # WHEN
    new4_value = 88
    x_attribute = "_party_debtor_pool"
    required_args = {x_attribute: new4_value}
    x_stirunit = stirunit_shop(x_attribute, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(x_stirunit)
    # THEN
    assert len(sue_moveunit.update_stirs) == 4
    assert x_stirunit == sue_moveunit.update_stirs.get(x_attribute)

    # WHEN
    new5_value = "override"
    x_attribute = "_meld_strategy"
    required_args = {x_attribute: new5_value}
    x_stirunit = stirunit_shop(x_attribute, stir_update(), None, required_args)
    sue_moveunit.set_stirunit(x_stirunit)
    # THEN
    assert len(sue_moveunit.update_stirs) == 5
    assert x_stirunit == sue_moveunit.update_stirs.get(x_attribute)
