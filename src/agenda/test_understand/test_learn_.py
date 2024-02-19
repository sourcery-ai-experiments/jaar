from src.agenda.party import partyunit_shop
from src.agenda.understand import (
    LearnUnit,
    learnunit_shop,
    learn_insert,
    learn_delete,
    learn_update,
    category_ref,
    is_category_ref,
    get_learn_config_dict,
    get_mog,
    set_mog,
)


def test_category_ref_ReturnsCorrectObj():
    assert category_ref() == {
        "agendaunit",
        "partyunit",
        "groupunit",
        "partylink",
        "ideaunit",
        "idea_balancelink",
        "idea_reasonunit",
        "idea_reason_premiseunit",
        "idea_suffgroup",
        "idea_healerhold",
        "idea_beliefunit",
    }
    assert "partyunit" in category_ref()
    assert is_category_ref("idearoot") == False


def check_every_crud_dict_has_element(learn_config_dict, learn_order_text):
    for category, category_dict in learn_config_dict.items():
        if category_dict.get(learn_insert()) != None:
            category_insert = category_dict.get(learn_insert())
            if category_insert.get(learn_order_text) is None:
                print(
                    f"Missing from {category} {learn_insert()} {category_insert.get(learn_order_text)=}"
                )
                return False

        if category_dict.get(learn_update()) != None:
            category_update = category_dict.get(learn_update())
            if category_update.get(learn_order_text) is None:
                print(
                    f"Missing from {category} {learn_update()} {category_update.get(learn_order_text)=}"
                )
                return False

        if category_dict.get(learn_delete()) != None:
            category_delete = category_dict.get(learn_delete())
            if category_delete.get(learn_order_text) is None:
                print(
                    f"Missing from {category} {learn_delete()} {category_delete.get(learn_order_text)=}"
                )
                return False
    return True


def test_get_learn_config_dict_EveryCrudOperationHasUnderstandOrderGroup():
    # GIVEN
    learn_order_text = "learn_order"
    description_elements_text = "description_elements"

    # WHEN / THEN
    assert check_every_crud_dict_has_element(get_learn_config_dict(), learn_order_text)
    assert check_every_crud_dict_has_element(
        get_learn_config_dict(), description_elements_text
    )
    mog = learn_order_text
    # # Simple script for editing understand_learn_config.json
    # set_mog("partyunit", learn_insert(), mog, 0)
    # set_mog("partylink", learn_insert(), mog, 1)
    # set_mog("groupunit", learn_insert(), mog, 2)
    # set_mog("ideaunit", learn_insert(), mog, 3)
    # set_mog("idea_balancelink", learn_insert(), mog, 4)
    # set_mog("idea_suffgroup", learn_insert(), mog, 5)
    # set_mog("idea_healerhold", learn_insert(), mog, 6)
    # set_mog("idea_beliefunit", learn_insert(), mog, 7)
    # set_mog("idea_reasonunit", learn_insert(), mog, 8)
    # set_mog("idea_reason_premiseunit", learn_insert(), mog, 9)
    # set_mog("partyunit", learn_update(), mog, 10)
    # set_mog("groupunit", learn_update(), mog, 11)
    # set_mog("partylink", learn_update(), mog, 12)
    # set_mog("ideaunit", learn_update(), mog, 13)
    # set_mog("idea_balancelink", learn_update(), mog, 14)
    # set_mog("idea_beliefunit", learn_update(), mog, 15)
    # set_mog("idea_reason_premiseunit", learn_update(), mog, 16)
    # set_mog("idea_reasonunit", learn_update(), mog, 17)
    # set_mog("idea_reason_premiseunit", learn_delete(), mog, 18)
    # set_mog("idea_reasonunit", learn_delete(), mog, 19)
    # set_mog("idea_beliefunit", learn_delete(), mog, 20)
    # set_mog("idea_suffgroup", learn_delete(), mog, 21)
    # set_mog("idea_healerhold", learn_delete(), mog, 22)
    # set_mog("idea_balancelink", learn_delete(), mog, 23)
    # set_mog("ideaunit", learn_delete(), mog, 24)
    # set_mog("partylink", learn_delete(), mog, 25)
    # set_mog("partyunit", learn_delete(), mog, 26)
    # set_mog("groupunit", learn_delete(), mog, 27)
    # set_mog("agendaunit", learn_update(), mog, 28)

    assert 0 == get_mog("partyunit", learn_insert(), mog, 0)
    assert 1 == get_mog("partylink", learn_insert(), mog, 1)
    assert 2 == get_mog("groupunit", learn_insert(), mog, 2)
    assert 3 == get_mog("ideaunit", learn_insert(), mog, 3)
    assert 4 == get_mog("idea_balancelink", learn_insert(), mog, 4)
    assert 5 == get_mog("idea_suffgroup", learn_insert(), mog, 5)
    assert 6 == get_mog("idea_healerhold", learn_insert(), mog, 6)
    assert 7 == get_mog("idea_beliefunit", learn_insert(), mog, 7)
    assert 8 == get_mog("idea_reasonunit", learn_insert(), mog, 8)
    assert 9 == get_mog("idea_reason_premiseunit", learn_insert(), mog, 9)
    assert 10 == get_mog("partyunit", learn_update(), mog, 10)
    assert 11 == get_mog("groupunit", learn_update(), mog, 11)
    assert 12 == get_mog("partylink", learn_update(), mog, 12)
    assert 13 == get_mog("ideaunit", learn_update(), mog, 13)
    assert 14 == get_mog("idea_balancelink", learn_update(), mog, 14)
    assert 15 == get_mog("idea_beliefunit", learn_update(), mog, 15)
    assert 16 == get_mog("idea_reason_premiseunit", learn_update(), mog, 16)
    assert 17 == get_mog("idea_reasonunit", learn_update(), mog, 17)
    assert 18 == get_mog("idea_reason_premiseunit", learn_delete(), mog, 18)
    assert 19 == get_mog("idea_reasonunit", learn_delete(), mog, 19)
    assert 20 == get_mog("idea_beliefunit", learn_delete(), mog, 20)
    assert 21 == get_mog("idea_suffgroup", learn_delete(), mog, 21)
    assert 22 == get_mog("idea_healerhold", learn_delete(), mog, 22)
    assert 23 == get_mog("idea_balancelink", learn_delete(), mog, 23)
    assert 24 == get_mog("ideaunit", learn_delete(), mog, 24)
    assert 25 == get_mog("partylink", learn_delete(), mog, 25)
    assert 26 == get_mog("partyunit", learn_delete(), mog, 26)
    assert 27 == get_mog("groupunit", learn_delete(), mog, 27)
    assert 28 == get_mog("agendaunit", learn_update(), mog, 28)


def test_LearnUnit_exists():
    # GIVEN / WHEN
    x_learnunit = LearnUnit()

    # THEN
    x_learnunit.category is None
    x_learnunit.crud_text is None
    x_learnunit.locator is None
    x_learnunit.required_args is None
    x_learnunit.optional_args is None
    x_learnunit.learn_order is None


def test_learnunit_shop_ReturnsCorrectObj():
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
    x_learnunit = learnunit_shop(
        category=partyunit_text,
        crud_text=learn_insert(),
        locator=bob_locator_dict,
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )

    # THEN
    print(f"{x_learnunit=}")
    assert x_learnunit.category == partyunit_text
    assert x_learnunit.crud_text == learn_insert()
    assert x_learnunit.locator == bob_locator_dict
    assert x_learnunit.required_args == bob_required_dict
    assert x_learnunit.optional_args == bob_optional_dict


def test_LearnUnit_set_required_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_learnunit = learnunit_shop(partyunit_text, learn_insert())
    assert partyunit_learnunit.required_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_learnunit.set_required_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_learnunit.required_args == {party_id_text: bob_text}


def test_LearnUnit_set_optional_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_learnunit = learnunit_shop(partyunit_text, learn_insert())
    assert partyunit_learnunit.optional_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_learnunit.set_optional_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_learnunit.optional_args == {party_id_text: bob_text}


def test_LearnUnit_set_locator_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_learnunit = learnunit_shop(partyunit_text, learn_insert())
    assert partyunit_learnunit.locator == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_learnunit.set_locator(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_learnunit.locator == {party_id_text: bob_text}


def test_LearnUnit_get_locator_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "partyunit"
    partyunit_learnunit = learnunit_shop(partyunit_text, learn_insert())
    party_id_text = "party_id"
    partyunit_learnunit.set_locator(x_key=party_id_text, x_value=bob_text)

    # WHEN / THEN
    assert partyunit_learnunit.get_locator(party_id_text) == bob_text


# def test_LearnUnit_get_locator_key_ReturnsCorrectObj_single_parameter():
#     # GIVEN
#     bob_text = "Bob"
#     partyunit_text = "partyunit"
#     partyunit_learnunit = learnunit_shop(partyunit_text, learn_insert())
#     party_id_text = "party_id"
#     partyunit_learnunit.set_locator(x_key=party_id_text, x_value=bob_text)

#     # WHEN / THEN
#     assert partyunit_learnunit.get_locator_key() == f"{partyunit_text} {bob_text}"


# def test_LearnUnit_get_locator_key_ReturnsCorrectObj_double_parameter():
#     # GIVEN
#     bob_text = "Bob"
#     partylink_text = "partylink"
#     gupl_learnunit = learnunit_shop(partylink_text)
#     party_id_text = "party_id"
#     tom_text = "Tom"
#     gupl_learnunit.set_locator(party_id_text, bob_text)
#     group_id_text = "group_id"
#     run_text = "Runners"
#     gupl_learnunit.set_locator(group_id_text, run_text)

#     # WHEN / THEN
#     assert (
#         gupl_learnunit.get_locator_key()
#         == f"{partylink_text} {run_text} {bob_text}"
#     )


def test_LearnUnit_is_optional_args_valid_ReturnsCorrectBoolean():
    # WHEN
    partyunit_text = "partyunit"
    bob_insert_learnunit = learnunit_shop(partyunit_text, crud_text=learn_insert())
    assert bob_insert_learnunit.is_optional_args_valid()

    # WHEN
    bob_insert_learnunit.set_optional_arg("creditor_weight", 55)
    # THEN
    assert len(bob_insert_learnunit.optional_args) == 1
    assert bob_insert_learnunit.is_optional_args_valid()

    # WHEN
    bob_insert_learnunit.set_optional_arg("debtor_weight", 66)
    # THEN
    assert len(bob_insert_learnunit.optional_args) == 2
    assert bob_insert_learnunit.is_optional_args_valid()

    # WHEN
    bob_insert_learnunit.set_optional_arg("x_x_x", 77)
    # THEN
    assert len(bob_insert_learnunit.optional_args) == 3
    assert bob_insert_learnunit.is_optional_args_valid() == False


def test_LearnUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_INSERT():
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "partyunit"

    # WHEN
    bob_insert_learnunit = learnunit_shop(partyunit_text, crud_text=learn_insert())

    # THEN
    assert bob_insert_learnunit.is_locator_valid() == False
    assert bob_insert_learnunit.is_required_args_valid() == False
    assert bob_insert_learnunit.is_optional_args_valid()
    assert bob_insert_learnunit.is_valid() == False

    # WHEN
    party_id_text = "party_id"
    bob_insert_learnunit.set_locator(party_id_text, bob_text)

    # THEN
    assert bob_insert_learnunit.is_locator_valid()
    assert bob_insert_learnunit.is_required_args_valid() == False
    assert bob_insert_learnunit.is_optional_args_valid()
    assert bob_insert_learnunit.is_valid() == False

    # WHEN
    bob_insert_learnunit.set_optional_arg("x_x_x", 12)

    # THEN
    assert bob_insert_learnunit.is_locator_valid()
    assert bob_insert_learnunit.is_required_args_valid() == False
    assert bob_insert_learnunit.is_optional_args_valid() == False
    assert bob_insert_learnunit.is_valid() == False

    # WHEN
    bob_insert_learnunit.set_required_arg(party_id_text, bob_text)

    # THEN
    assert bob_insert_learnunit.is_locator_valid()
    assert bob_insert_learnunit.is_required_args_valid()
    assert bob_insert_learnunit.is_optional_args_valid() == False
    assert bob_insert_learnunit.is_valid() == False

    # WHEN
    bob_insert_learnunit.optional_args = {}
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    bob_insert_learnunit.set_optional_arg(
        cw_text, bob_partyunit.get_dict().get(cw_text)
    )
    bob_insert_learnunit.set_optional_arg(
        dw_text, bob_partyunit.get_dict().get(dw_text)
    )

    # THEN
    assert bob_insert_learnunit.is_locator_valid()
    assert bob_insert_learnunit.is_required_args_valid()
    assert bob_insert_learnunit.is_optional_args_valid()
    assert bob_insert_learnunit.is_valid()

    # WHEN
    bob_insert_learnunit.crud_text = None

    # THEN
    assert bob_insert_learnunit.is_locator_valid()
    assert bob_insert_learnunit.is_required_args_valid() == False
    assert bob_insert_learnunit.is_valid() == False

    # WHEN
    bob_insert_learnunit.crud_text = learn_insert()

    # THEN
    assert bob_insert_learnunit.is_locator_valid()
    assert bob_insert_learnunit.is_required_args_valid()
    assert bob_insert_learnunit.is_valid()


def test_LearnUnit_get_value_ReturnsObj():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "partyunit"
    bob_insert_learnunit = learnunit_shop(partyunit_text, learn_insert())
    bob_locator_dict = {"party_id": bob_text}
    bob_insert_learnunit.locator = bob_locator_dict
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    # bob_partyunit_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    # print(f"{bob_partyunit_dict=}")
    bob_insert_learnunit.set_required_arg(party_id_text, bob_text)
    bob_insert_learnunit.set_optional_arg(
        cw_text, bob_partyunit.get_dict().get(cw_text)
    )
    bob_insert_learnunit.set_optional_arg(
        dw_text, bob_partyunit.get_dict().get(dw_text)
    )
    assert bob_insert_learnunit.is_valid()

    # WHEN / THEN
    assert bob_insert_learnunit.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_learnunit.get_value(dw_text) == bob_debtor_weight


def test_LearnUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_DELETE():
    bob_text = "Bob"
    partyunit_text = "partyunit"
    delete_text = learn_delete()

    # WHEN
    bob_delete_learnunit = learnunit_shop(partyunit_text, crud_text=delete_text)

    # THEN
    assert bob_delete_learnunit.is_locator_valid() == False
    assert bob_delete_learnunit.is_required_args_valid() == False
    assert bob_delete_learnunit.is_valid() == False

    # WHEN
    bob_delete_learnunit.set_locator("party_id", bob_text)

    # THEN
    assert bob_delete_learnunit.is_locator_valid()
    assert bob_delete_learnunit.is_required_args_valid() == False
    assert bob_delete_learnunit.is_valid() == False

    # WHEN
    bob_delete_learnunit.set_required_arg("party_id", bob_text)

    # THEN
    assert bob_delete_learnunit.is_locator_valid()
    assert bob_delete_learnunit.is_required_args_valid()
    assert bob_delete_learnunit.is_valid()


def test_LearnUnit_set_learn_order_SetCorrectAttr():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    partyunit_text = "partyunit"
    bob_insert_learnunit = learnunit_shop(partyunit_text, learn_insert())
    party_id_text = "party_id"
    bob_insert_learnunit.set_locator(party_id_text, bob_text)
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    bob_insert_learnunit.set_required_arg(party_id_text, bob_text)
    bob_insert_learnunit.set_optional_arg(cw_text, bob_creditor_weight)
    bob_insert_learnunit.set_optional_arg(dw_text, bob_debtor_weight)
    assert bob_insert_learnunit.is_valid()

    # WHEN / THEN
    assert bob_insert_learnunit.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_learnunit.get_value(dw_text) == bob_debtor_weight
