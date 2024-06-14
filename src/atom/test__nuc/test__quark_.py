from src.agenda.party import partyunit_shop
from src.atom.quark import (
    QuarkUnit,
    quarkunit_shop,
    quark_insert,
    quark_delete,
    quark_update,
    category_ref,
    is_category_ref,
    get_quark_config_dict,
    get_quark_order as q_order,
    set_mog,
    get_quark_columns_build,
)


def test_quark_config_HasCorrect_category():
    assert category_ref() == {
        "agendaunit",
        "agenda_partyunit",
        "agenda_ideaunit",
        "agenda_idea_partylink",
        "agenda_factunit",
        "agenda_fact_balancelink",
        "agenda_fact_reasonunit",
        "agenda_fact_reason_premiseunit",
        "agenda_fact_suffidea",
        "agenda_fact_healerhold",
        "agenda_fact_beliefunit",
    }
    assert "agenda_partyunit" in category_ref()
    assert is_category_ref("factroot") is False


def check_every_crud_dict_has_element(quark_config_dict, quark_order_text):
    for category, category_dict in quark_config_dict.items():
        if category_dict.get(quark_insert()) != None:
            category_insert = category_dict.get(quark_insert())
            if category_insert.get(quark_order_text) is None:
                print(
                    f"Missing from {category} {quark_insert()} {category_insert.get(quark_order_text)=}"
                )
                return False

        if category_dict.get(quark_update()) != None:
            category_update = category_dict.get(quark_update())
            if category_update.get(quark_order_text) is None:
                print(
                    f"Missing from {category} {quark_update()} {category_update.get(quark_order_text)=}"
                )
                return False

        if category_dict.get(quark_delete()) != None:
            category_delete = category_dict.get(quark_delete())
            if category_delete.get(quark_order_text) is None:
                print(
                    f"Missing from {category} {quark_delete()} {category_delete.get(quark_order_text)=}"
                )
                return False

        treasury_only_text = "treasury_only"
        if category_dict.get(treasury_only_text) is None:
            print(f"{category=} missing {treasury_only_text}")
            return False

        print(f"{category_dict.get(treasury_only_text)=}")
        if category_dict.get(treasury_only_text) not in [True, False]:
            print(
                f"{category=} {treasury_only_text} value '{category_dict.get(treasury_only_text)}' not acceptable"
            )
            return False

        if category_dict.get(treasury_only_text) is None:
            print(f"{category=} missing {treasury_only_text}")
            return False

        calculated_attrs_text = "calculated_attrs"
        if category_dict.get(calculated_attrs_text) is None:
            print(f"{category=} {calculated_attrs_text} is missing")
            return False
    return True


def test_get_quark_config_dict_EveryCrudOperationHasNucOrderIdea():
    # GIVEN
    quark_order_text = "quark_order"
    description_elements_text = "description_elements"

    # WHEN / THEN
    assert check_every_crud_dict_has_element(get_quark_config_dict(), quark_order_text)
    # assert check_every_crud_dict_has_element(
    #     get_quark_config_dict(), description_elements_text
    # )
    mog = quark_order_text
    # # Simple script for editing quark_config.json
    # set_mog("agenda_partyunit", quark_insert(), mog, 0)
    # set_mog("agenda_idea_partylink", quark_insert(), mog, 1)
    # set_mog("ideaunit", quark_insert(), mog, 2)
    # set_mog("agenda_factunit", quark_insert(), mog, 3)
    # set_mog("agenda_fact_balancelink", quark_insert(), mog, 4)
    # set_mog("agenda_fact_suffidea", quark_insert(), mog, 5)
    # set_mog("agenda_fact_healerhold", quark_insert(), mog, 6)
    # set_mog("agenda_fact_beliefunit", quark_insert(), mog, 7)
    # set_mog("agenda_fact_reasonunit", quark_insert(), mog, 8)
    # set_mog("agenda_fact_reason_premiseunit", quark_insert(), mog, 9)
    # set_mog("agenda_partyunit", quark_update(), mog, 10)
    # set_mog("ideaunit", quark_update(), mog, 11)
    # set_mog("agenda_idea_partylink", quark_update(), mog, 12)
    # set_mog("agenda_factunit", quark_update(), mog, 13)
    # set_mog("agenda_fact_balancelink", quark_update(), mog, 14)
    # set_mog("agenda_fact_beliefunit", quark_update(), mog, 15)
    # set_mog("agenda_fact_reason_premiseunit", quark_update(), mog, 16)
    # set_mog("agenda_fact_reasonunit", quark_update(), mog, 17)
    # set_mog("agenda_fact_reason_premiseunit", quark_delete(), mog, 18)
    # set_mog("agenda_fact_reasonunit", quark_delete(), mog, 19)
    # set_mog("agenda_fact_beliefunit", quark_delete(), mog, 20)
    # set_mog("agenda_fact_suffidea", quark_delete(), mog, 21)
    # set_mog("agenda_fact_healerhold", quark_delete(), mog, 22)
    # set_mog("agenda_fact_balancelink", quark_delete(), mog, 23)
    # set_mog("agenda_factunit", quark_delete(), mog, 24)
    # set_mog("agenda_idea_partylink", quark_delete(), mog, 25)
    # set_mog("agenda_partyunit", quark_delete(), mog, 26)
    # set_mog("ideaunit", quark_delete(), mog, 27)
    # set_mog("agendaunit", quark_update(), mog, 28)

    assert 0 == q_order("agenda_partyunit", quark_insert(), mog, 0)
    assert 1 == q_order("agenda_idea_partylink", quark_insert(), mog, 1)
    assert 2 == q_order("agenda_ideaunit", quark_insert(), mog, 2)
    assert 3 == q_order("agenda_factunit", quark_insert(), mog, 3)
    assert 4 == q_order("agenda_fact_balancelink", quark_insert(), mog, 4)
    assert 5 == q_order("agenda_fact_suffidea", quark_insert(), mog, 5)
    assert 6 == q_order("agenda_fact_healerhold", quark_insert(), mog, 6)
    assert 7 == q_order("agenda_fact_beliefunit", quark_insert(), mog, 7)
    assert 8 == q_order("agenda_fact_reasonunit", quark_insert(), mog, 8)
    assert 9 == q_order("agenda_fact_reason_premiseunit", quark_insert(), mog, 9)
    assert 10 == q_order("agenda_partyunit", quark_update(), mog, 10)
    assert 11 == q_order("agenda_ideaunit", quark_update(), mog, 11)
    assert 12 == q_order("agenda_idea_partylink", quark_update(), mog, 12)
    assert 13 == q_order("agenda_factunit", quark_update(), mog, 13)
    assert 14 == q_order("agenda_fact_balancelink", quark_update(), mog, 14)
    assert 15 == q_order("agenda_fact_beliefunit", quark_update(), mog, 15)
    assert 16 == q_order("agenda_fact_reason_premiseunit", quark_update(), mog, 16)
    assert 17 == q_order("agenda_fact_reasonunit", quark_update(), mog, 17)
    assert 18 == q_order("agenda_fact_reason_premiseunit", quark_delete(), mog, 18)
    assert 19 == q_order("agenda_fact_reasonunit", quark_delete(), mog, 19)
    assert 20 == q_order("agenda_fact_beliefunit", quark_delete(), mog, 20)
    assert 21 == q_order("agenda_fact_suffidea", quark_delete(), mog, 21)
    assert 22 == q_order("agenda_fact_healerhold", quark_delete(), mog, 22)
    assert 23 == q_order("agenda_fact_balancelink", quark_delete(), mog, 23)
    assert 24 == q_order("agenda_factunit", quark_delete(), mog, 24)
    assert 25 == q_order("agenda_idea_partylink", quark_delete(), mog, 25)
    assert 26 == q_order("agenda_partyunit", quark_delete(), mog, 26)
    assert 27 == q_order("agenda_ideaunit", quark_delete(), mog, 27)
    assert 28 == q_order("agendaunit", quark_update(), mog, 28)


def _every_category_dict_has_arg_elements(category_dict: dict) -> bool:
    required_args_text = "required_args"
    optional_args_text = "optional_args"
    python_type_text = "python_type"
    sqlite_datatype_text = "sqlite_datatype"
    for required_arg, x_dict in category_dict.get(required_args_text).items():
        if x_dict.get(python_type_text) is None:
            print(f"python_type_text failed for {required_arg=}")
            return False
        if x_dict.get(sqlite_datatype_text) is None:
            print(f"sqlite_datatype_text failed for {required_arg=}")
            return False
    if category_dict.get(optional_args_text) != None:
        for optional_arg, x_dict in category_dict.get(optional_args_text).items():
            if x_dict.get(python_type_text) is None:
                print(f"python_type_text failed for {optional_arg=}")
                return False
            if x_dict.get(sqlite_datatype_text) is None:
                print(f"sqlite_datatype_text failed for {optional_arg=}")
                return False


def check_every_arg_dict_has_elements(quark_config_dict):
    for category_key, category_dict in quark_config_dict.items():
        print(f"{category_key=}")
        _every_category_dict_has_arg_elements(category_dict)
    return True


def test_quark_config_AllArgsHave_python_type_sqlite_datatype():
    # GIVEN
    # WHEN / THEN
    assert check_every_arg_dict_has_elements(get_quark_config_dict())


def test_get_quark_columns_build_ReturnsCorrectObj():
    # GIVEN / WHEN
    quark_columns = get_quark_columns_build()

    # THEN
    assert len(quark_columns) == 111
    assert quark_columns.get("agendaunit_UPDATE__party_credor_pool") == "INTEGER"
    # print(f"{quark_columns.keys()=}")


def test_QuarkUnit_exists():
    # GIVEN / WHEN
    x_quarkunit = QuarkUnit()

    # THEN
    assert x_quarkunit.category is None
    assert x_quarkunit.crud_text is None
    assert x_quarkunit.required_args is None
    assert x_quarkunit.optional_args is None
    assert x_quarkunit.quark_order is None


def test_quarkunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    cw_text = "_credor_weight"
    dw_text = "_debtor_weight"
    bob_required_dict = {"party_id": "huh"}
    bob_optional_dict = {cw_text: bob_partyunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)
    partyunit_text = "agenda_partyunit"

    # WHEN
    x_quarkunit = quarkunit_shop(
        category=partyunit_text,
        crud_text=quark_insert(),
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )

    # THEN
    print(f"{x_quarkunit=}")
    assert x_quarkunit.category == partyunit_text
    assert x_quarkunit.crud_text == quark_insert()
    assert x_quarkunit.required_args == bob_required_dict
    assert x_quarkunit.optional_args == bob_optional_dict


def test_QuarkUnit_set_required_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "agenda_partyunit"
    partyunit_quarkunit = quarkunit_shop(partyunit_text, quark_insert())
    assert partyunit_quarkunit.required_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_quarkunit.set_required_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_quarkunit.required_args == {party_id_text: bob_text}


def test_QuarkUnit_set_optional_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "agenda_partyunit"
    partyunit_quarkunit = quarkunit_shop(partyunit_text, quark_insert())
    assert partyunit_quarkunit.optional_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_quarkunit.set_optional_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_quarkunit.optional_args == {party_id_text: bob_text}


def test_QuarkUnit_get_value_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "agenda_partyunit"
    partyunit_quarkunit = quarkunit_shop(partyunit_text, quark_insert())
    party_id_text = "party_id"
    partyunit_quarkunit.set_required_arg(x_key=party_id_text, x_value=bob_text)

    # WHEN / THEN
    assert partyunit_quarkunit.get_value(party_id_text) == bob_text


def test_QuarkUnit_is_optional_args_valid_ReturnsCorrectBoolean():
    # WHEN
    partyunit_text = "agenda_partyunit"
    bob_insert_quarkunit = quarkunit_shop(partyunit_text, crud_text=quark_insert())
    assert bob_insert_quarkunit.is_optional_args_valid()

    # WHEN
    bob_insert_quarkunit.set_optional_arg("credor_weight", 55)
    # THEN
    assert len(bob_insert_quarkunit.optional_args) == 1
    assert bob_insert_quarkunit.is_optional_args_valid()

    # WHEN
    bob_insert_quarkunit.set_optional_arg("debtor_weight", 66)
    # THEN
    assert len(bob_insert_quarkunit.optional_args) == 2
    assert bob_insert_quarkunit.is_optional_args_valid()

    # WHEN
    bob_insert_quarkunit.set_optional_arg("x_x_x", 77)
    # THEN
    assert len(bob_insert_quarkunit.optional_args) == 3
    assert bob_insert_quarkunit.is_optional_args_valid() is False


def test_QuarkUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_INSERT():
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    partyunit_text = "agenda_partyunit"

    # WHEN
    bob_insert_quarkunit = quarkunit_shop(partyunit_text, crud_text=quark_insert())

    # THEN
    assert bob_insert_quarkunit.is_required_args_valid() is False
    assert bob_insert_quarkunit.is_optional_args_valid()
    assert bob_insert_quarkunit.is_valid() is False

    # WHEN
    bob_insert_quarkunit.set_optional_arg("x_x_x", 12)

    # THEN
    assert bob_insert_quarkunit.is_required_args_valid() is False
    assert bob_insert_quarkunit.is_optional_args_valid() is False
    assert bob_insert_quarkunit.is_valid() is False

    # WHEN
    party_id_text = "party_id"
    bob_insert_quarkunit.set_required_arg(party_id_text, bob_text)

    # THEN
    assert bob_insert_quarkunit.is_required_args_valid()
    assert bob_insert_quarkunit.is_optional_args_valid() is False
    assert bob_insert_quarkunit.is_valid() is False

    # WHEN
    bob_insert_quarkunit.optional_args = {}
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    bob_insert_quarkunit.set_optional_arg(
        cw_text, bob_partyunit.get_dict().get(cw_text)
    )
    bob_insert_quarkunit.set_optional_arg(
        dw_text, bob_partyunit.get_dict().get(dw_text)
    )

    # THEN
    assert bob_insert_quarkunit.is_required_args_valid()
    assert bob_insert_quarkunit.is_optional_args_valid()
    assert bob_insert_quarkunit.is_valid()

    # WHEN
    bob_insert_quarkunit.crud_text = None

    # THEN
    assert bob_insert_quarkunit.is_required_args_valid() is False
    assert bob_insert_quarkunit.is_valid() is False

    # WHEN
    bob_insert_quarkunit.crud_text = quark_insert()

    # THEN
    assert bob_insert_quarkunit.is_required_args_valid()
    assert bob_insert_quarkunit.is_valid()


def test_QuarkUnit_get_value_ReturnsObj():
    # GIVEN
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    partyunit_text = "agenda_partyunit"
    bob_insert_quarkunit = quarkunit_shop(partyunit_text, quark_insert())
    party_id_text = "party_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    # bob_partyunit_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    # print(f"{bob_partyunit_dict=}")
    bob_insert_quarkunit.set_required_arg(party_id_text, bob_text)
    bob_insert_quarkunit.set_optional_arg(
        cw_text, bob_partyunit.get_dict().get(cw_text)
    )
    bob_insert_quarkunit.set_optional_arg(
        dw_text, bob_partyunit.get_dict().get(dw_text)
    )
    assert bob_insert_quarkunit.is_valid()

    # WHEN / THEN
    assert bob_insert_quarkunit.get_value(cw_text) == bob_credor_weight
    assert bob_insert_quarkunit.get_value(dw_text) == bob_debtor_weight


def test_QuarkUnit_is_valid_ReturnsCorrectBoolean_PartyUnit_DELETE():
    bob_text = "Bob"
    partyunit_text = "agenda_partyunit"
    delete_text = quark_delete()

    # WHEN
    bob_delete_quarkunit = quarkunit_shop(partyunit_text, crud_text=delete_text)

    # THEN
    assert bob_delete_quarkunit.is_required_args_valid() is False
    assert bob_delete_quarkunit.is_valid() is False

    # WHEN
    bob_delete_quarkunit.set_required_arg("party_id", bob_text)

    # THEN
    assert bob_delete_quarkunit.is_required_args_valid()
    assert bob_delete_quarkunit.is_valid()


def test_QuarkUnit_set_quark_order_SetCorrectAttr():
    # GIVEN
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    partyunit_text = "agenda_partyunit"
    bob_insert_quarkunit = quarkunit_shop(partyunit_text, quark_insert())
    party_id_text = "party_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    bob_insert_quarkunit.set_required_arg(party_id_text, bob_text)
    bob_insert_quarkunit.set_optional_arg(cw_text, bob_credor_weight)
    bob_insert_quarkunit.set_optional_arg(dw_text, bob_debtor_weight)
    assert bob_insert_quarkunit.is_valid()

    # WHEN / THEN
    assert bob_insert_quarkunit.get_value(cw_text) == bob_credor_weight
    assert bob_insert_quarkunit.get_value(dw_text) == bob_debtor_weight


def test_QuarkUnit_set_arg_SetsAny_required_arg_optional_arg():
    # GIVEN
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    partyunit_text = "agenda_partyunit"
    bob_insert_quarkunit = quarkunit_shop(partyunit_text, quark_insert())
    party_id_text = "party_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"

    # WHEN
    bob_insert_quarkunit.set_arg(party_id_text, bob_text)
    bob_insert_quarkunit.set_arg(cw_text, bob_credor_weight)
    bob_insert_quarkunit.set_arg(dw_text, bob_debtor_weight)

    # THEN
    assert bob_insert_quarkunit.get_value(party_id_text) == bob_text
    assert bob_insert_quarkunit.get_value(cw_text) == bob_credor_weight
    assert bob_insert_quarkunit.get_value(dw_text) == bob_debtor_weight
    assert bob_insert_quarkunit.get_value(party_id_text) == bob_text
    assert bob_insert_quarkunit.is_valid()
