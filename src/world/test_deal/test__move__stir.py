from src.agenda.party import partyunit_shop
from src.world.move import (
    moveunit_shop,
    StirUnit,
    stirunit_shop,
    stir_insert,
    stir_delete,
    stir_update,
    category_ref,
    is_category_ref,
    get_stir_config_dict,
    get_mog,
    set_mog,
)
from src.world.examples.example_deals import (
    get_sue_personroad,
    get_sue_moveunit_example1,
)


def test_category_ref_ReturnsCorrectObj():
    idea_text = "idea"
    assert category_ref() == {
        "AgendaUnit_weight",
        "_max_tree_traverse",
        "_party_creditor_pool",
        "_party_debtor_pool",
        "_auto_output_to_forum",
        "_meld_strategy",
        "partyunit",
        "groupunit",
        "groupunit_partylink",
        idea_text,
        f"{idea_text}_balancelink",
        f"{idea_text}_reasonunit",
        f"{idea_text}_reasonunit_premiseunit",
        f"{idea_text}_suffgroup",
        f"{idea_text}_beliefunit",
    }
    assert "partyunit" in category_ref()
    assert is_category_ref(idea_text)
    assert is_category_ref("idearoot") == False


def every_crud_text_has_stir_order(stir_config_dict, stir_order_text):
    for category, category_dict in stir_config_dict.items():
        if category_dict.get(stir_insert()) != None:
            category_insert = category_dict.get(stir_insert())
            if category_insert.get(stir_order_text) is None:
                print(
                    f"{category} {stir_insert()} {category_insert.get(stir_order_text)=}"
                )
                return False

        if category_dict.get(stir_update()) != None:
            category_update = category_dict.get(stir_update())
            if category_update.get(stir_order_text) is None:
                print(
                    f"{category} {stir_update()} {category_update.get(stir_order_text)=}"
                )
                return False

        if category_dict.get(stir_delete()) != None:
            category_delete = category_dict.get(stir_delete())
            if category_delete.get(stir_order_text) is None:
                print(
                    f"{category} {stir_delete()} {category_delete.get(stir_order_text)=}"
                )
                return False
    return True


def test_get_stir_config_dict_EveryCrudOperationHasMoveOrderGroup():
    # GIVEN
    stir_order_text = "stir_order"

    # WHEN / THEN
    assert every_crud_text_has_stir_order(get_stir_config_dict(), stir_order_text)
    mog = stir_order_text
    # Simple script for editing stir_categorys.json
    # set_mog("partyunit", stir_insert(), mog, 0)
    # set_mog("partyunit", stir_update(), mog, 1)
    # set_mog("partyunit", stir_delete(), mog, 2)
    # set_mog("groupunit_partylink", stir_insert(), mog, 3)
    # set_mog("groupunit_partylink", stir_update(), mog, 4)
    # set_mog("groupunit_partylink", stir_delete(), mog, 5)
    # set_mog("groupunit", stir_insert(), mog, 6)
    # set_mog("groupunit", stir_update(), mog, 7)
    # set_mog("groupunit", stir_delete(), mog, 8)
    # set_mog("idea", stir_insert(), mog, 9)
    # set_mog("idea_balancelink", stir_insert(), mog, 10)
    # set_mog("idea_reasonunit_premiseunit", stir_insert(), mog, 11)
    # set_mog("idea_reasonunit", stir_insert(), mog, 12)
    # set_mog("idea_suffgroup", stir_insert(), mog, 13)
    # set_mog("idea_beliefunit", stir_insert(), mog, 14)
    # set_mog("idea", stir_delete(), mog, 15)
    # set_mog("idea_balancelink", stir_delete(), mog, 16)
    # set_mog("idea_reasonunit_premiseunit", stir_delete(), mog, 17)
    # set_mog("idea_reasonunit", stir_delete(), mog, 18)
    # set_mog("idea_suffgroup", stir_delete(), mog, 19)
    # set_mog("idea_beliefunit", stir_delete(), mog, 20)
    # set_mog("idea", stir_update(), mog, 21)
    # set_mog("idea_balancelink", stir_update(), mog, 22)
    # set_mog("idea_reasonunit_premiseunit", stir_update(), mog, 23)
    # set_mog("idea_reasonunit", stir_update(), mog, 24)
    # set_mog("idea_suffgroup", stir_update(), mog, 25)
    # set_mog("idea_beliefunit", stir_update(), mog, 26)
    # set_mog("AgendaUnit_weight", stir_update(), mog, 27)
    # set_mog("_max_tree_traverse", stir_update(), mog, 27)
    # set_mog("_party_creditor_pool", stir_update(), mog, 27)
    # set_mog("_party_debtor_pool", stir_update(), mog, 27)
    # set_mog("_auto_output_to_forum", stir_update(), mog, 27)
    # set_mog("_meld_strategy", stir_update(), mog, 27)

    assert 0 == get_mog("partyunit", stir_insert(), mog, 0)
    assert 1 == get_mog("partyunit", stir_update(), mog, 1)
    assert 2 == get_mog("partyunit", stir_delete(), mog, 2)
    assert 3 == get_mog("groupunit_partylink", stir_insert(), mog, 3)
    assert 4 == get_mog("groupunit_partylink", stir_update(), mog, 4)
    assert 5 == get_mog("groupunit_partylink", stir_delete(), mog, 5)
    assert 6 == get_mog("groupunit", stir_insert(), mog, 6)
    assert 7 == get_mog("groupunit", stir_update(), mog, 7)
    assert 8 == get_mog("groupunit", stir_delete(), mog, 8)
    assert 9 == get_mog("idea", stir_insert(), mog, 9)
    assert 10 == get_mog("idea_balancelink", stir_insert(), mog, 10)
    assert 11 == get_mog("idea_reasonunit_premiseunit", stir_insert(), mog, 11)
    assert 12 == get_mog("idea_reasonunit", stir_insert(), mog, 12)
    assert 13 == get_mog("idea_suffgroup", stir_insert(), mog, 13)
    assert 14 == get_mog("idea_beliefunit", stir_insert(), mog, 14)
    assert 15 == get_mog("idea", stir_delete(), mog, 15)
    assert 16 == get_mog("idea_balancelink", stir_delete(), mog, 16)
    assert 17 == get_mog("idea_reasonunit_premiseunit", stir_delete(), mog, 17)
    assert 18 == get_mog("idea_reasonunit", stir_delete(), mog, 18)
    assert 19 == get_mog("idea_suffgroup", stir_delete(), mog, 19)
    assert 20 == get_mog("idea_beliefunit", stir_delete(), mog, 20)
    assert 21 == get_mog("idea", stir_update(), mog, 21)
    assert 22 == get_mog("idea_balancelink", stir_update(), mog, 22)
    assert 23 == get_mog("idea_reasonunit_premiseunit", stir_update(), mog, 23)
    assert 24 == get_mog("idea_reasonunit", stir_update(), mog, 24)
    assert 26 == get_mog("idea_beliefunit", stir_update(), mog, 26)
    assert 27 == get_mog("AgendaUnit_weight", stir_update(), mog, 27)
    assert 27 == get_mog("_max_tree_traverse", stir_update(), mog, 27)
    assert 27 == get_mog("_party_creditor_pool", stir_update(), mog, 27)
    assert 27 == get_mog("_party_debtor_pool", stir_update(), mog, 27)
    assert 27 == get_mog("_auto_output_to_forum", stir_update(), mog, 27)
    assert 27 == get_mog("_meld_strategy", stir_update(), mog, 27)


def test_StirUnit_exists():
    # GIVEN / WHEN
    x_stirunit = StirUnit()

    # THEN
    x_stirunit.category is None
    x_stirunit.crud_text is None
    x_stirunit.locator is None
    x_stirunit.required_args is None
    x_stirunit.optional_args is None
    x_stirunit.stir_order is None


def test_stirunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    bob_locator_dict = {"party_id": bob_text}
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    cw_text = "_creditor_weight"
    dw_text = "_debtor_weight"
    bob_required_dict = {"party_id": "huh"}
    bob_optional_dict = {cw_text: bob_partyunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)
    partyunit_text = "partyunit"

    # WHEN
    x_stirunit = stirunit_shop(
        category=partyunit_text,
        crud_text=stir_insert(),
        locator=bob_locator_dict,
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )

    # THEN
    print(f"{x_stirunit=}")
    assert x_stirunit.category == partyunit_text
    assert x_stirunit.crud_text == stir_insert()
    assert x_stirunit.locator == bob_locator_dict
    assert x_stirunit.required_args == bob_required_dict
    assert x_stirunit.optional_args == bob_optional_dict


def test_StirUnit_set_required_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_stirunit = stirunit_shop(partyunit_text, stir_insert())
    assert partyunit_stirunit.required_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_stirunit.set_required_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_stirunit.required_args == {party_id_text: bob_text}


def test_StirUnit_set_optional_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_stirunit = stirunit_shop(partyunit_text, stir_insert())
    assert partyunit_stirunit.optional_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_stirunit.set_optional_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_stirunit.optional_args == {party_id_text: bob_text}


def test_StirUnit_set_locator_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_stirunit = stirunit_shop(partyunit_text, stir_insert())
    assert partyunit_stirunit.locator == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_stirunit.set_locator(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_stirunit.locator == {party_id_text: bob_text}


def test_StirUnit_get_locator_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_stirunit = stirunit_shop(partyunit_text, stir_insert())
    party_id_text = "party_id"
    partyunit_stirunit.set_locator(x_key=party_id_text, x_value=bob_text)

    # WHEN / THEN
    assert partyunit_stirunit.get_locator(party_id_text) == bob_text


def test_StirUnit_get_locator_key_ReturnsCorrectObj_single_parameter():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_stirunit = stirunit_shop(partyunit_text, stir_insert())
    party_id_text = "party_id"
    partyunit_stirunit.set_locator(x_key=party_id_text, x_value=bob_text)

    # WHEN / THEN
    assert partyunit_stirunit.get_locator_key() == f"{partyunit_text} {bob_text}"


def test_StirUnit_get_locator_key_ReturnsCorrectObj_double_parameter():
    # GIVEN
    bob_text = "Bob"
    groupunit_partylink_text = "groupunit_partylink"
    gupl_stirunit = stirunit_shop(groupunit_partylink_text)
    party_id_text = "party_id"
    tom_text = "Tom"
    gupl_stirunit.set_locator(party_id_text, bob_text)
    group_id_text = "group_id"
    run_text = "Runners"
    gupl_stirunit.set_locator(group_id_text, run_text)

    # WHEN / THEN
    assert (
        gupl_stirunit.get_locator_key()
        == f"{groupunit_partylink_text} {run_text} {bob_text}"
    )


def test_StirUnit_is_optional_args_valid_ReturnsCorrectBoolean():
    # WHEN
    partyunit_text = "partyunit"
    bob_insert_stirunit = stirunit_shop(partyunit_text, crud_text=stir_insert())
    assert bob_insert_stirunit.is_optional_args_valid()

    # WHEN
    bob_insert_stirunit.set_optional_arg("creditor_weight", 55)
    # THEN
    assert len(bob_insert_stirunit.optional_args) == 1
    assert bob_insert_stirunit.is_optional_args_valid()

    # WHEN
    bob_insert_stirunit.set_optional_arg("debtor_weight", 66)
    # THEN
    assert len(bob_insert_stirunit.optional_args) == 2
    assert bob_insert_stirunit.is_optional_args_valid()

    # WHEN
    bob_insert_stirunit.set_optional_arg("x_x_x", 77)
    # THEN
    assert len(bob_insert_stirunit.optional_args) == 3
    assert bob_insert_stirunit.is_optional_args_valid() == False


def test_StirUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_INSERT():
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "partyunit"

    # WHEN
    bob_insert_stirunit = stirunit_shop(partyunit_text, crud_text=stir_insert())

    # THEN
    assert bob_insert_stirunit.is_locator_valid() == False
    assert bob_insert_stirunit.is_required_args_valid() == False
    assert bob_insert_stirunit.is_optional_args_valid()
    assert bob_insert_stirunit.is_valid() == False

    # WHEN
    party_id_text = "party_id"
    bob_insert_stirunit.set_locator(party_id_text, bob_text)

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_required_args_valid() == False
    assert bob_insert_stirunit.is_optional_args_valid()
    assert bob_insert_stirunit.is_valid() == False

    # WHEN
    bob_insert_stirunit.set_optional_arg("x_x_x", 12)

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_required_args_valid() == False
    assert bob_insert_stirunit.is_optional_args_valid() == False
    assert bob_insert_stirunit.is_valid() == False

    # WHEN
    bob_insert_stirunit.set_required_arg(party_id_text, bob_text)

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_required_args_valid()
    assert bob_insert_stirunit.is_optional_args_valid() == False
    assert bob_insert_stirunit.is_valid() == False

    # WHEN
    bob_insert_stirunit.optional_args = {}
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    bob_insert_stirunit.set_optional_arg(cw_text, bob_partyunit.get_dict().get(cw_text))
    bob_insert_stirunit.set_optional_arg(dw_text, bob_partyunit.get_dict().get(dw_text))

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_required_args_valid()
    assert bob_insert_stirunit.is_optional_args_valid()
    assert bob_insert_stirunit.is_valid()

    # WHEN
    bob_insert_stirunit.crud_text = None

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_required_args_valid() == False
    assert bob_insert_stirunit.is_valid() == False

    # WHEN
    bob_insert_stirunit.crud_text = stir_insert()

    # THEN
    assert bob_insert_stirunit.is_locator_valid()
    assert bob_insert_stirunit.is_required_args_valid()
    assert bob_insert_stirunit.is_valid()


def test_StirUnit_get_value_ReturnsObj():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "partyunit"
    bob_insert_stirunit = stirunit_shop(partyunit_text, stir_insert())
    bob_locator_dict = {"party_id": bob_text}
    bob_insert_stirunit.locator = bob_locator_dict
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    # bob_partyunit_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    # print(f"{bob_partyunit_dict=}")
    bob_insert_stirunit.set_required_arg(party_id_text, bob_text)
    bob_insert_stirunit.set_optional_arg(cw_text, bob_partyunit.get_dict().get(cw_text))
    bob_insert_stirunit.set_optional_arg(dw_text, bob_partyunit.get_dict().get(dw_text))
    assert bob_insert_stirunit.is_valid()

    # WHEN / THEN
    assert bob_insert_stirunit.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_stirunit.get_value(dw_text) == bob_debtor_weight


def test_StirUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_DELETE():
    bob_text = "Bob"
    partyunit_text = "partyunit"
    delete_text = stir_delete()

    # WHEN
    bob_delete_stirunit = stirunit_shop(partyunit_text, crud_text=delete_text)

    # THEN
    assert bob_delete_stirunit.is_locator_valid() == False
    assert bob_delete_stirunit.is_required_args_valid()
    assert bob_delete_stirunit.is_valid() == False

    # WHEN
    bob_locator_dict = {"party_id": bob_text}
    bob_delete_stirunit.locator = bob_locator_dict

    # THEN
    assert bob_delete_stirunit.is_locator_valid()
    assert bob_delete_stirunit.is_required_args_valid()
    assert bob_delete_stirunit.is_valid()


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
    assert sue_moveunit.update_stirs == {}
    assert agenda_weight_stirunit.stir_order is None

    # WHEN
    sue_moveunit.set_stirunit(agenda_weight_stirunit)

    # THEN
    assert len(sue_moveunit.update_stirs) == 1
    x_stirunit = sue_moveunit.update_stirs.get(category)
    assert x_stirunit == agenda_weight_stirunit
    assert agenda_weight_stirunit.stir_order != None


def test_StirUnit_set_stir_order_SetCorrectAttr():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    partyunit_text = "partyunit"
    bob_insert_stirunit = stirunit_shop(partyunit_text, stir_insert())
    party_id_text = "party_id"
    bob_insert_stirunit.set_locator(party_id_text, bob_text)
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    bob_insert_stirunit.set_required_arg(party_id_text, bob_text)
    bob_insert_stirunit.set_optional_arg(cw_text, bob_creditor_weight)
    bob_insert_stirunit.set_optional_arg(dw_text, bob_debtor_weight)
    assert bob_insert_stirunit.is_valid()

    # WHEN / THEN
    assert bob_insert_stirunit.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_stirunit.get_value(dw_text) == bob_debtor_weight


def test_MoveUnit_get_stir_ReturnsCorrectObj():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    w_value = 55
    w_name = "AgendaUnit_weight"
    w_stirunit = stirunit_shop(w_name, stir_update())
    w_stirunit.set_required_arg(x_key=w_name, x_value=w_value)
    sue_moveunit.set_stirunit(w_stirunit)

    # WHEN
    gen_stirunit = sue_moveunit.get_stir(stir_update(), locator_key=w_name)

    # THEN
    assert gen_stirunit == w_stirunit


def test_MoveUnit_add_stirunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    assert sue_moveunit.update_stirs == {}

    # WHEN
    attribute_value = 55
    category = "AgendaUnit_weight"
    required_args = {category: attribute_value}
    sue_moveunit.add_stirunit(category, stir_update(), None, required_args)

    # THEN
    assert len(sue_moveunit.update_stirs) == 1
    x_stirunit = sue_moveunit.update_stirs.get(category)
    assert x_stirunit != None


def test_MoveUnit_add_stirunit_CorrectlySets_AgendaUnit_partyunits():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    assert sue_moveunit.insert_stirs == {}

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
    assert len(sue_moveunit.insert_stirs) == 1
    bob_locator_key = f"{partyunit_text} {bob_text}"
    assert sue_moveunit.insert_stirs.get(bob_locator_key) != None


def test_MoveUnit_add_stirunit_CorrectlySets_AgendaUnit_max_tree_traverse():
    # GIVEN
    sue_moveunit = moveunit_shop(get_sue_personroad())
    assert sue_moveunit.update_stirs == {}

    # WHEN
    weight_value = 55
    weight_name = "AgendaUnit_weight"
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


def test_MoveUnit_get_stir_order_stirunit_dict_ReturnsCorrectObj():
    # GIVEN
    sue_moveunit = get_sue_moveunit_example1()
    assert len(sue_moveunit.update_stirs) == 5
    assert len(sue_moveunit.delete_stirs) == 1
    assert len(sue_moveunit.insert_stirs) == 0

    # WHEN
    sue_stir_order_dict = sue_moveunit.get_stir_order_stirunit_dict()

    # THEN
    assert len(sue_stir_order_dict) == 2
    print(f"{sue_stir_order_dict=}")
    assert len(sue_stir_order_dict[2]) == 1
    assert len(sue_stir_order_dict[27]) == 5
