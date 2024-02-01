from src.agenda.party import partyunit_shop
from src.agenda.learn import (
    GrainUnit,
    grainunit_shop,
    grain_insert,
    grain_delete,
    grain_update,
    category_ref,
    is_category_ref,
    get_grain_config_dict,
    get_mog,
    set_mog,
)


def test_category_ref_ReturnsCorrectObj():
    assert get_grain_config_dict() != None


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


def check_every_crud_dict_has_element(grain_config_dict, grain_order_text):
    for category, category_dict in grain_config_dict.items():
        if category_dict.get(grain_insert()) != None:
            category_insert = category_dict.get(grain_insert())
            if category_insert.get(grain_order_text) is None:
                print(
                    f"Missing from {category} {grain_insert()} {category_insert.get(grain_order_text)=}"
                )
                return False

        if category_dict.get(grain_update()) != None:
            category_update = category_dict.get(grain_update())
            if category_update.get(grain_order_text) is None:
                print(
                    f"Missing from {category} {grain_update()} {category_update.get(grain_order_text)=}"
                )
                return False

        if category_dict.get(grain_delete()) != None:
            category_delete = category_dict.get(grain_delete())
            if category_delete.get(grain_order_text) is None:
                print(
                    f"Missing from {category} {grain_delete()} {category_delete.get(grain_order_text)=}"
                )
                return False
    return True


def test_get_grain_config_dict_EveryCrudOperationHasLearnOrderGroup():
    # GIVEN
    grain_order_text = "grain_order"
    description_elements_text = "description_elements"

    # WHEN / THEN
    assert check_every_crud_dict_has_element(get_grain_config_dict(), grain_order_text)
    assert check_every_crud_dict_has_element(
        get_grain_config_dict(), description_elements_text
    )
    mog = grain_order_text
    # # Simple script for editing learn_grain_config.json
    # set_mog("partyunit", grain_insert(), mog, 0)
    # set_mog("groupunit_partylink", grain_insert(), mog, 1)
    # set_mog("groupunit", grain_insert(), mog, 2)
    # set_mog("idea", grain_insert(), mog, 3)
    # set_mog("idea_balancelink", grain_insert(), mog, 4)
    # set_mog("idea_suffgroup", grain_insert(), mog, 5)
    # set_mog("idea_beliefunit", grain_insert(), mog, 6)
    # set_mog("idea_reasonunit", grain_insert(), mog, 7)
    # set_mog("idea_reasonunit_premiseunit", grain_insert(), mog, 8)
    # set_mog("partyunit", grain_update(), mog, 9)
    # set_mog("groupunit", grain_update(), mog, 10)
    # set_mog("groupunit_partylink", grain_update(), mog, 11)
    # set_mog("idea", grain_update(), mog, 12)
    # set_mog("idea_balancelink", grain_update(), mog, 13)
    # set_mog("idea_beliefunit", grain_update(), mog, 14)
    # set_mog("idea_reasonunit_premiseunit", grain_update(), mog, 15)
    # set_mog("idea_reasonunit", grain_update(), mog, 16)
    # set_mog("idea_reasonunit_premiseunit", grain_delete(), mog, 17)
    # set_mog("idea_reasonunit", grain_delete(), mog, 18)
    # set_mog("idea_beliefunit", grain_delete(), mog, 19)
    # set_mog("idea_suffgroup", grain_delete(), mog, 20)
    # set_mog("idea_balancelink", grain_delete(), mog, 21)
    # set_mog("idea", grain_delete(), mog, 22)
    # set_mog("groupunit_partylink", grain_delete(), mog, 23)
    # set_mog("partyunit", grain_delete(), mog, 24)
    # set_mog("groupunit", grain_delete(), mog, 25)
    # set_mog("AgendaUnit_weight", grain_update(), mog, 26)
    # set_mog("_max_tree_traverse", grain_update(), mog, 26)
    # set_mog("_party_creditor_pool", grain_update(), mog, 26)
    # set_mog("_party_debtor_pool", grain_update(), mog, 26)
    # set_mog("_auto_output_to_forum", grain_update(), mog, 26)
    # set_mog("_meld_strategy", grain_update(), mog, 26)

    assert 0 == get_mog("partyunit", grain_insert(), mog, 0)
    assert 1 == get_mog("groupunit_partylink", grain_insert(), mog, 1)
    assert 2 == get_mog("groupunit", grain_insert(), mog, 2)
    assert 3 == get_mog("idea", grain_insert(), mog, 3)
    assert 4 == get_mog("idea_balancelink", grain_insert(), mog, 4)
    assert 5 == get_mog("idea_suffgroup", grain_insert(), mog, 5)
    assert 6 == get_mog("idea_beliefunit", grain_insert(), mog, 6)
    assert 7 == get_mog("idea_reasonunit", grain_insert(), mog, 7)
    assert 8 == get_mog("idea_reasonunit_premiseunit", grain_insert(), mog, 8)
    assert 9 == get_mog("partyunit", grain_update(), mog, 9)
    assert 10 == get_mog("groupunit", grain_update(), mog, 10)
    assert 11 == get_mog("groupunit_partylink", grain_update(), mog, 11)
    assert 12 == get_mog("idea", grain_update(), mog, 12)
    assert 13 == get_mog("idea_balancelink", grain_update(), mog, 13)
    assert 14 == get_mog("idea_beliefunit", grain_update(), mog, 14)
    assert 15 == get_mog("idea_reasonunit_premiseunit", grain_update(), mog, 15)
    assert 16 == get_mog("idea_reasonunit", grain_update(), mog, 16)
    assert 17 == get_mog("idea_reasonunit_premiseunit", grain_delete(), mog, 17)
    assert 18 == get_mog("idea_reasonunit", grain_delete(), mog, 18)
    assert 19 == get_mog("idea_beliefunit", grain_delete(), mog, 19)
    assert 20 == get_mog("idea_suffgroup", grain_delete(), mog, 20)
    assert 21 == get_mog("idea_balancelink", grain_delete(), mog, 21)
    assert 22 == get_mog("idea", grain_delete(), mog, 22)
    assert 23 == get_mog("groupunit_partylink", grain_delete(), mog, 23)
    assert 24 == get_mog("partyunit", grain_delete(), mog, 24)
    assert 25 == get_mog("groupunit", grain_delete(), mog, 25)
    assert 26 == get_mog("AgendaUnit_weight", grain_update(), mog, 26)
    assert 26 == get_mog("_max_tree_traverse", grain_update(), mog, 26)
    assert 26 == get_mog("_party_creditor_pool", grain_update(), mog, 26)
    assert 26 == get_mog("_party_debtor_pool", grain_update(), mog, 26)
    assert 26 == get_mog("_auto_output_to_forum", grain_update(), mog, 26)
    assert 26 == get_mog("_meld_strategy", grain_update(), mog, 26)


def test_GrainUnit_exists():
    # GIVEN / WHEN
    x_grainunit = GrainUnit()

    # THEN
    x_grainunit.category is None
    x_grainunit.crud_text is None
    x_grainunit.locator is None
    x_grainunit.required_args is None
    x_grainunit.optional_args is None
    x_grainunit.grain_order is None


def test_grainunit_shop_ReturnsCorrectObj():
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
    x_grainunit = grainunit_shop(
        category=partyunit_text,
        crud_text=grain_insert(),
        locator=bob_locator_dict,
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )

    # THEN
    print(f"{x_grainunit=}")
    assert x_grainunit.category == partyunit_text
    assert x_grainunit.crud_text == grain_insert()
    assert x_grainunit.locator == bob_locator_dict
    assert x_grainunit.required_args == bob_required_dict
    assert x_grainunit.optional_args == bob_optional_dict


def test_GrainUnit_set_required_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_grainunit = grainunit_shop(partyunit_text, grain_insert())
    assert partyunit_grainunit.required_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_grainunit.set_required_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_grainunit.required_args == {party_id_text: bob_text}


def test_GrainUnit_set_optional_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_grainunit = grainunit_shop(partyunit_text, grain_insert())
    assert partyunit_grainunit.optional_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_grainunit.set_optional_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_grainunit.optional_args == {party_id_text: bob_text}


def test_GrainUnit_set_locator_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_grainunit = grainunit_shop(partyunit_text, grain_insert())
    assert partyunit_grainunit.locator == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_grainunit.set_locator(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_grainunit.locator == {party_id_text: bob_text}


def test_GrainUnit_get_locator_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_grainunit = grainunit_shop(partyunit_text, grain_insert())
    party_id_text = "party_id"
    partyunit_grainunit.set_locator(x_key=party_id_text, x_value=bob_text)

    # WHEN / THEN
    assert partyunit_grainunit.get_locator(party_id_text) == bob_text


# def test_GrainUnit_get_locator_key_ReturnsCorrectObj_single_parameter():
#     # GIVEN
#     bob_text = "Bob"
#     partyunit_text = "partyunit"
#     partyunit_grainunit = grainunit_shop(partyunit_text, grain_insert())
#     party_id_text = "party_id"
#     partyunit_grainunit.set_locator(x_key=party_id_text, x_value=bob_text)

#     # WHEN / THEN
#     assert partyunit_grainunit.get_locator_key() == f"{partyunit_text} {bob_text}"


# def test_GrainUnit_get_locator_key_ReturnsCorrectObj_double_parameter():
#     # GIVEN
#     bob_text = "Bob"
#     groupunit_partylink_text = "groupunit_partylink"
#     gupl_grainunit = grainunit_shop(groupunit_partylink_text)
#     party_id_text = "party_id"
#     tom_text = "Tom"
#     gupl_grainunit.set_locator(party_id_text, bob_text)
#     group_id_text = "group_id"
#     run_text = "Runners"
#     gupl_grainunit.set_locator(group_id_text, run_text)

#     # WHEN / THEN
#     assert (
#         gupl_grainunit.get_locator_key()
#         == f"{groupunit_partylink_text} {run_text} {bob_text}"
#     )


def test_GrainUnit_is_optional_args_valid_ReturnsCorrectBoolean():
    # WHEN
    partyunit_text = "partyunit"
    bob_insert_grainunit = grainunit_shop(partyunit_text, crud_text=grain_insert())
    assert bob_insert_grainunit.is_optional_args_valid()

    # WHEN
    bob_insert_grainunit.set_optional_arg("creditor_weight", 55)
    # THEN
    assert len(bob_insert_grainunit.optional_args) == 1
    assert bob_insert_grainunit.is_optional_args_valid()

    # WHEN
    bob_insert_grainunit.set_optional_arg("debtor_weight", 66)
    # THEN
    assert len(bob_insert_grainunit.optional_args) == 2
    assert bob_insert_grainunit.is_optional_args_valid()

    # WHEN
    bob_insert_grainunit.set_optional_arg("x_x_x", 77)
    # THEN
    assert len(bob_insert_grainunit.optional_args) == 3
    assert bob_insert_grainunit.is_optional_args_valid() == False


def test_GrainUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_INSERT():
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "partyunit"

    # WHEN
    bob_insert_grainunit = grainunit_shop(partyunit_text, crud_text=grain_insert())

    # THEN
    assert bob_insert_grainunit.is_locator_valid() == False
    assert bob_insert_grainunit.is_required_args_valid() == False
    assert bob_insert_grainunit.is_optional_args_valid()
    assert bob_insert_grainunit.is_valid() == False

    # WHEN
    party_id_text = "party_id"
    bob_insert_grainunit.set_locator(party_id_text, bob_text)

    # THEN
    assert bob_insert_grainunit.is_locator_valid()
    assert bob_insert_grainunit.is_required_args_valid() == False
    assert bob_insert_grainunit.is_optional_args_valid()
    assert bob_insert_grainunit.is_valid() == False

    # WHEN
    bob_insert_grainunit.set_optional_arg("x_x_x", 12)

    # THEN
    assert bob_insert_grainunit.is_locator_valid()
    assert bob_insert_grainunit.is_required_args_valid() == False
    assert bob_insert_grainunit.is_optional_args_valid() == False
    assert bob_insert_grainunit.is_valid() == False

    # WHEN
    bob_insert_grainunit.set_required_arg(party_id_text, bob_text)

    # THEN
    assert bob_insert_grainunit.is_locator_valid()
    assert bob_insert_grainunit.is_required_args_valid()
    assert bob_insert_grainunit.is_optional_args_valid() == False
    assert bob_insert_grainunit.is_valid() == False

    # WHEN
    bob_insert_grainunit.optional_args = {}
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    bob_insert_grainunit.set_optional_arg(
        cw_text, bob_partyunit.get_dict().get(cw_text)
    )
    bob_insert_grainunit.set_optional_arg(
        dw_text, bob_partyunit.get_dict().get(dw_text)
    )

    # THEN
    assert bob_insert_grainunit.is_locator_valid()
    assert bob_insert_grainunit.is_required_args_valid()
    assert bob_insert_grainunit.is_optional_args_valid()
    assert bob_insert_grainunit.is_valid()

    # WHEN
    bob_insert_grainunit.crud_text = None

    # THEN
    assert bob_insert_grainunit.is_locator_valid()
    assert bob_insert_grainunit.is_required_args_valid() == False
    assert bob_insert_grainunit.is_valid() == False

    # WHEN
    bob_insert_grainunit.crud_text = grain_insert()

    # THEN
    assert bob_insert_grainunit.is_locator_valid()
    assert bob_insert_grainunit.is_required_args_valid()
    assert bob_insert_grainunit.is_valid()


def test_GrainUnit_get_value_ReturnsObj():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "partyunit"
    bob_insert_grainunit = grainunit_shop(partyunit_text, grain_insert())
    bob_locator_dict = {"party_id": bob_text}
    bob_insert_grainunit.locator = bob_locator_dict
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    # bob_partyunit_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    # print(f"{bob_partyunit_dict=}")
    bob_insert_grainunit.set_required_arg(party_id_text, bob_text)
    bob_insert_grainunit.set_optional_arg(
        cw_text, bob_partyunit.get_dict().get(cw_text)
    )
    bob_insert_grainunit.set_optional_arg(
        dw_text, bob_partyunit.get_dict().get(dw_text)
    )
    assert bob_insert_grainunit.is_valid()

    # WHEN / THEN
    assert bob_insert_grainunit.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_grainunit.get_value(dw_text) == bob_debtor_weight


def test_GrainUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_DELETE():
    bob_text = "Bob"
    partyunit_text = "partyunit"
    delete_text = grain_delete()

    # WHEN
    bob_delete_grainunit = grainunit_shop(partyunit_text, crud_text=delete_text)

    # THEN
    assert bob_delete_grainunit.is_locator_valid() == False
    assert bob_delete_grainunit.is_required_args_valid() == False
    assert bob_delete_grainunit.is_valid() == False

    # WHEN
    bob_delete_grainunit.set_locator("party_id", bob_text)

    # THEN
    assert bob_delete_grainunit.is_locator_valid()
    assert bob_delete_grainunit.is_required_args_valid() == False
    assert bob_delete_grainunit.is_valid() == False

    # WHEN
    bob_delete_grainunit.set_required_arg("party_id", bob_text)

    # THEN
    assert bob_delete_grainunit.is_locator_valid()
    assert bob_delete_grainunit.is_required_args_valid()
    assert bob_delete_grainunit.is_valid()


def test_GrainUnit_set_grain_order_SetCorrectAttr():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    partyunit_text = "partyunit"
    bob_insert_grainunit = grainunit_shop(partyunit_text, grain_insert())
    party_id_text = "party_id"
    bob_insert_grainunit.set_locator(party_id_text, bob_text)
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    bob_insert_grainunit.set_required_arg(party_id_text, bob_text)
    bob_insert_grainunit.set_optional_arg(cw_text, bob_creditor_weight)
    bob_insert_grainunit.set_optional_arg(dw_text, bob_debtor_weight)
    assert bob_insert_grainunit.is_valid()

    # WHEN / THEN
    assert bob_insert_grainunit.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_grainunit.get_value(dw_text) == bob_debtor_weight
