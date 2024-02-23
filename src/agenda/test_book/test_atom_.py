from src.agenda.party import partyunit_shop
from src.agenda.atom import (
    AgendaAtom,
    agendaatom_shop,
    atom_insert,
    atom_delete,
    atom_update,
    category_ref,
    is_category_ref,
    get_atom_config_dict,
    get_mog,
    set_mog,
    get_atom_columns_build,
)


def test_atom_config_HasCorrect_category():
    assert category_ref() == {
        "agendaunit",
        "agenda_partyunit",
        "agenda_groupunit",
        "agenda_group_partylink",
        "agenda_ideaunit",
        "agenda_idea_balancelink",
        "agenda_idea_reasonunit",
        "agenda_idea_reason_premiseunit",
        "agenda_idea_suffgroup",
        "agenda_idea_healerhold",
        "agenda_idea_beliefunit",
    }
    assert "agenda_partyunit" in category_ref()
    assert is_category_ref("idearoot") == False


def check_every_crud_dict_has_element(atom_config_dict, atom_order_text):
    for category, category_dict in atom_config_dict.items():
        if category_dict.get(atom_insert()) != None:
            category_insert = category_dict.get(atom_insert())
            if category_insert.get(atom_order_text) is None:
                print(
                    f"Missing from {category} {atom_insert()} {category_insert.get(atom_order_text)=}"
                )
                return False

        if category_dict.get(atom_update()) != None:
            category_update = category_dict.get(atom_update())
            if category_update.get(atom_order_text) is None:
                print(
                    f"Missing from {category} {atom_update()} {category_update.get(atom_order_text)=}"
                )
                return False

        if category_dict.get(atom_delete()) != None:
            category_delete = category_dict.get(atom_delete())
            if category_delete.get(atom_order_text) is None:
                print(
                    f"Missing from {category} {atom_delete()} {category_delete.get(atom_order_text)=}"
                )
                return False
    return True


def test_get_atom_config_dict_EveryCrudOperationHasBookOrderGroup():
    # GIVEN
    atom_order_text = "atom_order"
    description_elements_text = "description_elements"

    # WHEN / THEN
    assert check_every_crud_dict_has_element(get_atom_config_dict(), atom_order_text)
    assert check_every_crud_dict_has_element(
        get_atom_config_dict(), description_elements_text
    )
    mog = atom_order_text
    # # Simple script for editing atom_config.json
    # set_mog("agenda_partyunit", atom_insert(), mog, 0)
    # set_mog("agenda_group_partylink", atom_insert(), mog, 1)
    # set_mog("groupunit", atom_insert(), mog, 2)
    # set_mog("agenda_ideaunit", atom_insert(), mog, 3)
    # set_mog("agenda_idea_balancelink", atom_insert(), mog, 4)
    # set_mog("agenda_idea_suffgroup", atom_insert(), mog, 5)
    # set_mog("agenda_idea_healerhold", atom_insert(), mog, 6)
    # set_mog("agenda_idea_beliefunit", atom_insert(), mog, 7)
    # set_mog("agenda_idea_reasonunit", atom_insert(), mog, 8)
    # set_mog("agenda_idea_reason_premiseunit", atom_insert(), mog, 9)
    # set_mog("agenda_partyunit", atom_update(), mog, 10)
    # set_mog("groupunit", atom_update(), mog, 11)
    # set_mog("agenda_group_partylink", atom_update(), mog, 12)
    # set_mog("agenda_ideaunit", atom_update(), mog, 13)
    # set_mog("agenda_idea_balancelink", atom_update(), mog, 14)
    # set_mog("agenda_idea_beliefunit", atom_update(), mog, 15)
    # set_mog("agenda_idea_reason_premiseunit", atom_update(), mog, 16)
    # set_mog("agenda_idea_reasonunit", atom_update(), mog, 17)
    # set_mog("agenda_idea_reason_premiseunit", atom_delete(), mog, 18)
    # set_mog("agenda_idea_reasonunit", atom_delete(), mog, 19)
    # set_mog("agenda_idea_beliefunit", atom_delete(), mog, 20)
    # set_mog("agenda_idea_suffgroup", atom_delete(), mog, 21)
    # set_mog("agenda_idea_healerhold", atom_delete(), mog, 22)
    # set_mog("agenda_idea_balancelink", atom_delete(), mog, 23)
    # set_mog("agenda_ideaunit", atom_delete(), mog, 24)
    # set_mog("agenda_group_partylink", atom_delete(), mog, 25)
    # set_mog("agenda_partyunit", atom_delete(), mog, 26)
    # set_mog("groupunit", atom_delete(), mog, 27)
    # set_mog("agendaunit", atom_update(), mog, 28)

    assert 0 == get_mog("agenda_partyunit", atom_insert(), mog, 0)
    assert 1 == get_mog("agenda_group_partylink", atom_insert(), mog, 1)
    assert 2 == get_mog("agenda_groupunit", atom_insert(), mog, 2)
    assert 3 == get_mog("agenda_ideaunit", atom_insert(), mog, 3)
    assert 4 == get_mog("agenda_idea_balancelink", atom_insert(), mog, 4)
    assert 5 == get_mog("agenda_idea_suffgroup", atom_insert(), mog, 5)
    assert 6 == get_mog("agenda_idea_healerhold", atom_insert(), mog, 6)
    assert 7 == get_mog("agenda_idea_beliefunit", atom_insert(), mog, 7)
    assert 8 == get_mog("agenda_idea_reasonunit", atom_insert(), mog, 8)
    assert 9 == get_mog("agenda_idea_reason_premiseunit", atom_insert(), mog, 9)
    assert 10 == get_mog("agenda_partyunit", atom_update(), mog, 10)
    assert 11 == get_mog("agenda_groupunit", atom_update(), mog, 11)
    assert 12 == get_mog("agenda_group_partylink", atom_update(), mog, 12)
    assert 13 == get_mog("agenda_ideaunit", atom_update(), mog, 13)
    assert 14 == get_mog("agenda_idea_balancelink", atom_update(), mog, 14)
    assert 15 == get_mog("agenda_idea_beliefunit", atom_update(), mog, 15)
    assert 16 == get_mog("agenda_idea_reason_premiseunit", atom_update(), mog, 16)
    assert 17 == get_mog("agenda_idea_reasonunit", atom_update(), mog, 17)
    assert 18 == get_mog("agenda_idea_reason_premiseunit", atom_delete(), mog, 18)
    assert 19 == get_mog("agenda_idea_reasonunit", atom_delete(), mog, 19)
    assert 20 == get_mog("agenda_idea_beliefunit", atom_delete(), mog, 20)
    assert 21 == get_mog("agenda_idea_suffgroup", atom_delete(), mog, 21)
    assert 22 == get_mog("agenda_idea_healerhold", atom_delete(), mog, 22)
    assert 23 == get_mog("agenda_idea_balancelink", atom_delete(), mog, 23)
    assert 24 == get_mog("agenda_ideaunit", atom_delete(), mog, 24)
    assert 25 == get_mog("agenda_group_partylink", atom_delete(), mog, 25)
    assert 26 == get_mog("agenda_partyunit", atom_delete(), mog, 26)
    assert 27 == get_mog("agenda_groupunit", atom_delete(), mog, 27)
    assert 28 == get_mog("agendaunit", atom_update(), mog, 28)


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


def check_every_arg_dict_has_elements(atom_config_dict):
    for category_key, category_dict in atom_config_dict.items():
        print(f"{category_key=}")
        _every_category_dict_has_arg_elements(category_dict)
    return True


def test_atom_config_AllArgsHave_python_type_sqlite_datatype():
    # GIVEN
    # WHEN / THEN
    assert check_every_arg_dict_has_elements(get_atom_config_dict())


def test_get_atom_columns_build_ReturnsCorrectObj():
    # GIVEN / WHEN
    atom_columns = get_atom_columns_build()

    # THEN
    assert len(atom_columns) == 113
    assert atom_columns.get("agendaunit_UPDATE__auto_output_job_to_forum") == "INTEGER"
    # print(f"{atom_columns.keys()=}")


def test_AgendaAtom_exists():
    # GIVEN / WHEN
    x_agendaatom = AgendaAtom()

    # THEN
    x_agendaatom.category is None
    x_agendaatom.crud_text is None
    x_agendaatom.required_args is None
    x_agendaatom.optional_args is None
    x_agendaatom.atom_order is None


def test_agendaatom_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    cw_text = "_creditor_weight"
    dw_text = "_debtor_weight"
    bob_required_dict = {"party_id": "huh"}
    bob_optional_dict = {cw_text: bob_partyunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)
    partyunit_text = "agenda_partyunit"

    # WHEN
    x_agendaatom = agendaatom_shop(
        category=partyunit_text,
        crud_text=atom_insert(),
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )

    # THEN
    print(f"{x_agendaatom=}")
    assert x_agendaatom.category == partyunit_text
    assert x_agendaatom.crud_text == atom_insert()
    assert x_agendaatom.required_args == bob_required_dict
    assert x_agendaatom.optional_args == bob_optional_dict


def test_AgendaAtom_set_required_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "agenda_partyunit"
    partyunit_agendaatom = agendaatom_shop(partyunit_text, atom_insert())
    assert partyunit_agendaatom.required_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_agendaatom.set_required_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_agendaatom.required_args == {party_id_text: bob_text}


def test_AgendaAtom_set_optional_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "agenda_partyunit"
    partyunit_agendaatom = agendaatom_shop(partyunit_text, atom_insert())
    assert partyunit_agendaatom.optional_args == {}

    # WHEN
    party_id_text = "party_id"
    partyunit_agendaatom.set_optional_arg(x_key=party_id_text, x_value=bob_text)

    # THEN
    assert partyunit_agendaatom.optional_args == {party_id_text: bob_text}


def test_AgendaAtom_get_value_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    partyunit_text = "agenda_partyunit"
    partyunit_agendaatom = agendaatom_shop(partyunit_text, atom_insert())
    party_id_text = "party_id"
    partyunit_agendaatom.set_required_arg(x_key=party_id_text, x_value=bob_text)

    # WHEN / THEN
    assert partyunit_agendaatom.get_value(party_id_text) == bob_text


def test_AgendaAtom_is_optional_args_valid_ReturnsCorrectBoolean():
    # WHEN
    partyunit_text = "agenda_partyunit"
    bob_insert_agendaatom = agendaatom_shop(partyunit_text, crud_text=atom_insert())
    assert bob_insert_agendaatom.is_optional_args_valid()

    # WHEN
    bob_insert_agendaatom.set_optional_arg("creditor_weight", 55)
    # THEN
    assert len(bob_insert_agendaatom.optional_args) == 1
    assert bob_insert_agendaatom.is_optional_args_valid()

    # WHEN
    bob_insert_agendaatom.set_optional_arg("debtor_weight", 66)
    # THEN
    assert len(bob_insert_agendaatom.optional_args) == 2
    assert bob_insert_agendaatom.is_optional_args_valid()

    # WHEN
    bob_insert_agendaatom.set_optional_arg("x_x_x", 77)
    # THEN
    assert len(bob_insert_agendaatom.optional_args) == 3
    assert bob_insert_agendaatom.is_optional_args_valid() == False


def test_AgendaAtom_is_valid_ReturnsCorrectBoolean_PartyUnit_INSERT():
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "agenda_partyunit"

    # WHEN
    bob_insert_agendaatom = agendaatom_shop(partyunit_text, crud_text=atom_insert())

    # THEN
    assert bob_insert_agendaatom.is_required_args_valid() == False
    assert bob_insert_agendaatom.is_optional_args_valid()
    assert bob_insert_agendaatom.is_valid() == False

    # WHEN
    bob_insert_agendaatom.set_optional_arg("x_x_x", 12)

    # THEN
    assert bob_insert_agendaatom.is_required_args_valid() == False
    assert bob_insert_agendaatom.is_optional_args_valid() == False
    assert bob_insert_agendaatom.is_valid() == False

    # WHEN
    party_id_text = "party_id"
    bob_insert_agendaatom.set_required_arg(party_id_text, bob_text)

    # THEN
    assert bob_insert_agendaatom.is_required_args_valid()
    assert bob_insert_agendaatom.is_optional_args_valid() == False
    assert bob_insert_agendaatom.is_valid() == False

    # WHEN
    bob_insert_agendaatom.optional_args = {}
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    bob_insert_agendaatom.set_optional_arg(
        cw_text, bob_partyunit.get_dict().get(cw_text)
    )
    bob_insert_agendaatom.set_optional_arg(
        dw_text, bob_partyunit.get_dict().get(dw_text)
    )

    # THEN
    assert bob_insert_agendaatom.is_required_args_valid()
    assert bob_insert_agendaatom.is_optional_args_valid()
    assert bob_insert_agendaatom.is_valid()

    # WHEN
    bob_insert_agendaatom.crud_text = None

    # THEN
    assert bob_insert_agendaatom.is_required_args_valid() == False
    assert bob_insert_agendaatom.is_valid() == False

    # WHEN
    bob_insert_agendaatom.crud_text = atom_insert()

    # THEN
    assert bob_insert_agendaatom.is_required_args_valid()
    assert bob_insert_agendaatom.is_valid()


def test_AgendaAtom_get_value_ReturnsObj():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
    partyunit_text = "agenda_partyunit"
    bob_insert_agendaatom = agendaatom_shop(partyunit_text, atom_insert())
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    # bob_partyunit_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    # print(f"{bob_partyunit_dict=}")
    bob_insert_agendaatom.set_required_arg(party_id_text, bob_text)
    bob_insert_agendaatom.set_optional_arg(
        cw_text, bob_partyunit.get_dict().get(cw_text)
    )
    bob_insert_agendaatom.set_optional_arg(
        dw_text, bob_partyunit.get_dict().get(dw_text)
    )
    assert bob_insert_agendaatom.is_valid()

    # WHEN / THEN
    assert bob_insert_agendaatom.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_agendaatom.get_value(dw_text) == bob_debtor_weight


def test_AgendaAtom_is_valid_ReturnsCorrectBoolean_PartyUnit_DELETE():
    bob_text = "Bob"
    partyunit_text = "agenda_partyunit"
    delete_text = atom_delete()

    # WHEN
    bob_delete_agendaatom = agendaatom_shop(partyunit_text, crud_text=delete_text)

    # THEN
    assert bob_delete_agendaatom.is_required_args_valid() == False
    assert bob_delete_agendaatom.is_valid() == False

    # WHEN
    bob_delete_agendaatom.set_required_arg("party_id", bob_text)

    # THEN
    assert bob_delete_agendaatom.is_required_args_valid()
    assert bob_delete_agendaatom.is_valid()


def test_AgendaAtom_set_atom_order_SetCorrectAttr():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    partyunit_text = "agenda_partyunit"
    bob_insert_agendaatom = agendaatom_shop(partyunit_text, atom_insert())
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    bob_insert_agendaatom.set_required_arg(party_id_text, bob_text)
    bob_insert_agendaatom.set_optional_arg(cw_text, bob_creditor_weight)
    bob_insert_agendaatom.set_optional_arg(dw_text, bob_debtor_weight)
    assert bob_insert_agendaatom.is_valid()

    # WHEN / THEN
    assert bob_insert_agendaatom.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_agendaatom.get_value(dw_text) == bob_debtor_weight


def test_AgendaAtom_set_arg_SetsAny_required_arg_optional_arg():
    # GIVEN
    bob_text = "Bob"
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    partyunit_text = "agenda_partyunit"
    bob_insert_agendaatom = agendaatom_shop(partyunit_text, atom_insert())
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"

    # WHEN
    bob_insert_agendaatom.set_arg(party_id_text, bob_text)
    bob_insert_agendaatom.set_arg(cw_text, bob_creditor_weight)
    bob_insert_agendaatom.set_arg(dw_text, bob_debtor_weight)

    # THEN
    assert bob_insert_agendaatom.get_value(party_id_text) == bob_text
    assert bob_insert_agendaatom.get_value(cw_text) == bob_creditor_weight
    assert bob_insert_agendaatom.get_value(dw_text) == bob_debtor_weight
    assert bob_insert_agendaatom.get_value(party_id_text) == bob_text
    assert bob_insert_agendaatom.is_valid()
