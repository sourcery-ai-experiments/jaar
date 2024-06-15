from src.atom.quark_config import (
    quark_insert,
    quark_delete,
    quark_update,
    category_ref,
    is_category_ref,
    get_quark_config_dict,
    get_quark_order as q_order,
    set_mog,
    get_flattened_quark_table_build,
    get_normalized_agenda_table_build,
    required_args_text,
    optional_args_text,
    normal_table_name_text,
    sqlite_datatype_text,
    python_type_text,
    agendaunit_text,
    agenda_partyunit_text,
    agenda_beliefunit_text,
    agenda_belief_partylink_text,
    agenda_ideaunit_text,
    agenda_idea_balancelink_text,
    agenda_idea_reasonunit_text,
    agenda_idea_reason_premiseunit_text,
    agenda_idea_suffbelief_text,
    agenda_idea_healerhold_text,
    agenda_idea_factunit_text,
)


def test_agendaunit_text_ReturnsObj():
    assert agendaunit_text() == "agendaunit"


def test_agenda_partyunit_text_ReturnsObj():
    assert agenda_partyunit_text() == "agenda_partyunit"


def test_agenda_beliefunit_text_ReturnsObj():
    assert agenda_beliefunit_text() == "agenda_beliefunit"


def test_agenda_belief_partylink_text_ReturnsObj():
    assert agenda_belief_partylink_text() == "agenda_belief_partylink"


def test_agenda_ideaunit_text_ReturnsObj():
    assert agenda_ideaunit_text() == "agenda_ideaunit"


def test_agenda_idea_balancelink_text_ReturnsObj():
    assert agenda_idea_balancelink_text() == "agenda_idea_balancelink"


def test_agenda_idea_reasonunit_text_ReturnsObj():
    assert agenda_idea_reasonunit_text() == "agenda_idea_reasonunit"


def test_agenda_idea_reason_premiseunit_text_ReturnsObj():
    assert agenda_idea_reason_premiseunit_text() == "agenda_idea_reason_premiseunit"


def test_agenda_idea_suffbelief_text_ReturnsObj():
    assert agenda_idea_suffbelief_text() == "agenda_idea_suffbelief"


def test_agenda_idea_healerhold_text_ReturnsObj():
    assert agenda_idea_healerhold_text() == "agenda_idea_healerhold"


def test_agenda_idea_factunit_text_ReturnsObj():
    assert agenda_idea_factunit_text() == "agenda_idea_factunit"


def test_quark_config_HasCorrect_category():
    assert category_ref() == {
        agendaunit_text(),
        agenda_partyunit_text(),
        agenda_beliefunit_text(),
        agenda_belief_partylink_text(),
        agenda_ideaunit_text(),
        agenda_idea_balancelink_text(),
        agenda_idea_reasonunit_text(),
        agenda_idea_reason_premiseunit_text(),
        agenda_idea_suffbelief_text(),
        agenda_idea_healerhold_text(),
        agenda_idea_factunit_text(),
    }
    assert agenda_partyunit_text() in category_ref()
    assert is_category_ref("idearoot") is False


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

        if category_dict.get(normal_table_name_text()) is None:
            print(f"{category=} {normal_table_name_text()} is missing")
            return False
    return True


def test_get_quark_config_dict_EveryCrudOperationHasNucOrderBelief():
    # GIVEN
    quark_order_text = "quark_order"

    # WHEN / THEN
    assert check_every_crud_dict_has_element(get_quark_config_dict(), quark_order_text)
    mog = quark_order_text
    # # Simple script for editing quark_config.json
    # set_mog("agenda_partyunit", quark_insert(), mog, 0)
    # set_mog("agenda_belief_partylink", quark_insert(), mog, 1)
    # set_mog("beliefunit", quark_insert(), mog, 2)
    # set_mog("agenda_ideaunit", quark_insert(), mog, 3)
    # set_mog("agenda_idea_balancelink", quark_insert(), mog, 4)
    # set_mog("agenda_idea_suffbelief", quark_insert(), mog, 5)
    # set_mog("agenda_idea_healerhold", quark_insert(), mog, 6)
    # set_mog("agenda_idea_factunit", quark_insert(), mog, 7)
    # set_mog("agenda_idea_reasonunit", quark_insert(), mog, 8)
    # set_mog("agenda_idea_reason_premiseunit", quark_insert(), mog, 9)
    # set_mog("agenda_partyunit", quark_update(), mog, 10)
    # set_mog("beliefunit", quark_update(), mog, 11)
    # set_mog("agenda_belief_partylink", quark_update(), mog, 12)
    # set_mog("agenda_ideaunit", quark_update(), mog, 13)
    # set_mog("agenda_idea_balancelink", quark_update(), mog, 14)
    # set_mog("agenda_idea_factunit", quark_update(), mog, 15)
    # set_mog("agenda_idea_reason_premiseunit", quark_update(), mog, 16)
    # set_mog("agenda_idea_reasonunit", quark_update(), mog, 17)
    # set_mog("agenda_idea_reason_premiseunit", quark_delete(), mog, 18)
    # set_mog("agenda_idea_reasonunit", quark_delete(), mog, 19)
    # set_mog("agenda_idea_factunit", quark_delete(), mog, 20)
    # set_mog("agenda_idea_suffbelief", quark_delete(), mog, 21)
    # set_mog("agenda_idea_healerhold", quark_delete(), mog, 22)
    # set_mog("agenda_idea_balancelink", quark_delete(), mog, 23)
    # set_mog("agenda_ideaunit", quark_delete(), mog, 24)
    # set_mog("agenda_belief_partylink", quark_delete(), mog, 25)
    # set_mog("agenda_partyunit", quark_delete(), mog, 26)
    # set_mog("beliefunit", quark_delete(), mog, 27)
    # set_mog("agendaunit", quark_update(), mog, 28)

    assert 0 == q_order("agenda_partyunit", quark_insert(), mog, 0)
    assert 1 == q_order("agenda_belief_partylink", quark_insert(), mog, 1)
    assert 2 == q_order("agenda_beliefunit", quark_insert(), mog, 2)
    assert 3 == q_order("agenda_ideaunit", quark_insert(), mog, 3)
    assert 4 == q_order("agenda_idea_balancelink", quark_insert(), mog, 4)
    assert 5 == q_order("agenda_idea_suffbelief", quark_insert(), mog, 5)
    assert 6 == q_order("agenda_idea_healerhold", quark_insert(), mog, 6)
    assert 7 == q_order("agenda_idea_factunit", quark_insert(), mog, 7)
    assert 8 == q_order("agenda_idea_reasonunit", quark_insert(), mog, 8)
    assert 9 == q_order("agenda_idea_reason_premiseunit", quark_insert(), mog, 9)
    assert 10 == q_order("agenda_partyunit", quark_update(), mog, 10)
    assert 11 == q_order("agenda_beliefunit", quark_update(), mog, 11)
    assert 12 == q_order("agenda_belief_partylink", quark_update(), mog, 12)
    assert 13 == q_order("agenda_ideaunit", quark_update(), mog, 13)
    assert 14 == q_order("agenda_idea_balancelink", quark_update(), mog, 14)
    assert 15 == q_order("agenda_idea_factunit", quark_update(), mog, 15)
    assert 16 == q_order("agenda_idea_reason_premiseunit", quark_update(), mog, 16)
    assert 17 == q_order("agenda_idea_reasonunit", quark_update(), mog, 17)
    assert 18 == q_order("agenda_idea_reason_premiseunit", quark_delete(), mog, 18)
    assert 19 == q_order("agenda_idea_reasonunit", quark_delete(), mog, 19)
    assert 20 == q_order("agenda_idea_factunit", quark_delete(), mog, 20)
    assert 21 == q_order("agenda_idea_suffbelief", quark_delete(), mog, 21)
    assert 22 == q_order("agenda_idea_healerhold", quark_delete(), mog, 22)
    assert 23 == q_order("agenda_idea_balancelink", quark_delete(), mog, 23)
    assert 24 == q_order("agenda_ideaunit", quark_delete(), mog, 24)
    assert 25 == q_order("agenda_belief_partylink", quark_delete(), mog, 25)
    assert 26 == q_order("agenda_partyunit", quark_delete(), mog, 26)
    assert 27 == q_order("agenda_beliefunit", quark_delete(), mog, 27)
    assert 28 == q_order("agendaunit", quark_update(), mog, 28)


def _every_category_dict_has_arg_elements(category_dict: dict) -> bool:
    for required_arg, x_dict in category_dict.get(required_args_text()).items():
        if x_dict.get(python_type_text()) is None:
            print(f"python_type_text failed for {required_arg=}")
            return False
        if x_dict.get(sqlite_datatype_text()) is None:
            print(f"sqlite_datatype_text failed for {required_arg=}")
            return False
    if category_dict.get(optional_args_text()) != None:
        for optional_arg, x_dict in category_dict.get(optional_args_text()).items():
            if x_dict.get(python_type_text()) is None:
                print(f"python_type_text failed for {optional_arg=}")
                return False
            if x_dict.get(sqlite_datatype_text()) is None:
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


def test_get_flattened_quark_table_build_ReturnsCorrectObj():
    # GIVEN / WHEN
    quark_columns = get_flattened_quark_table_build()

    # THEN
    assert len(quark_columns) == 111
    assert quark_columns.get("agendaunit_UPDATE__party_credor_pool") == "INTEGER"
    # print(f"{quark_columns.keys()=}")


def test_get_normalized_agenda_table_build_ReturnsCorrectObj():
    # GIVEN / WHEN
    normalized_agenda_table_build = get_normalized_agenda_table_build()
    nx = normalized_agenda_table_build

    # THEN
    assert len(nx) == 11
    assert nx.get(agendaunit_text()) != None
    assert nx.get(agenda_partyunit_text()) != None
    assert nx.get(agenda_beliefunit_text()) != None
    assert nx.get(agenda_belief_partylink_text()) != None
    assert nx.get(agenda_ideaunit_text()) != None
    assert nx.get(agenda_idea_balancelink_text()) != None
    assert nx.get(agenda_idea_reasonunit_text()) != None
    assert nx.get(agenda_idea_reason_premiseunit_text()) != None
    assert nx.get(agenda_idea_suffbelief_text()) != None
    assert nx.get(agenda_idea_healerhold_text()) != None
    assert nx.get(agenda_idea_factunit_text()) != None
    agendaunit_cat = nx.get(agendaunit_text())
    partyunit_cat = nx.get(agenda_partyunit_text())
    belief_cat = nx.get(agenda_beliefunit_text())
    partylink_cat = nx.get(agenda_belief_partylink_text())
    idea_cat = nx.get(agenda_ideaunit_text())
    balancelink_cat = nx.get(agenda_idea_balancelink_text())
    reason_cat = nx.get(agenda_idea_reasonunit_text())
    premise_cat = nx.get(agenda_idea_reason_premiseunit_text())
    suffbelief_cat = nx.get(agenda_idea_suffbelief_text())
    healerhold_cat = nx.get(agenda_idea_healerhold_text())
    fact_cat = nx.get(agenda_idea_factunit_text())

    columns_text = "columns"
    print(f"{agendaunit_cat=}")
    assert agendaunit_cat.get(normal_table_name_text()) == "agenda"
    assert partyunit_cat.get(normal_table_name_text()) == "partyunit"
    assert belief_cat.get(normal_table_name_text()) == "beliefunit"
    assert partylink_cat.get(normal_table_name_text()) == "partylink"
    assert idea_cat.get(normal_table_name_text()) == "idea"
    assert balancelink_cat.get(normal_table_name_text()) == "balancelink"
    assert reason_cat.get(normal_table_name_text()) == "reason"
    assert premise_cat.get(normal_table_name_text()) == "premise"
    assert suffbelief_cat.get(normal_table_name_text()) == "suffbelief"
    assert healerhold_cat.get(normal_table_name_text()) == "healerhold"
    assert fact_cat.get(normal_table_name_text()) == "fact"

    assert len(agendaunit_cat) == 2
    assert agendaunit_cat.get(columns_text) != None

    agendaunit_columns = agendaunit_cat.get(columns_text)
    assert len(agendaunit_columns) == 9
    assert agendaunit_columns.get("uid") != None
    assert agendaunit_columns.get("_max_tree_traverse") != None
    assert agendaunit_columns.get("_meld_strategy") != None
    assert agendaunit_columns.get("_monetary_desc") != None
    assert agendaunit_columns.get("_party_credor_pool") != None
    assert agendaunit_columns.get("_party_debtor_pool") != None
    assert agendaunit_columns.get("_penny") != None
    assert agendaunit_columns.get("_planck") != None
    assert agendaunit_columns.get("_weight") != None

    assert len(partyunit_cat) == 2
    partyunit_columns = partyunit_cat.get(columns_text)
    assert len(partyunit_columns) == 4
    assert partyunit_columns.get("uid") != None
    assert partyunit_columns.get("party_id") != None
    assert partyunit_columns.get("credor_weight") != None
    assert partyunit_columns.get("debtor_weight") != None

    party_id_dict = partyunit_columns.get("party_id")
    assert len(party_id_dict) == 2
    assert party_id_dict.get(sqlite_datatype_text()) == "TEXT"
    assert party_id_dict.get("nullable") == False
    debtor_weight_dict = partyunit_columns.get("debtor_weight")
    assert len(party_id_dict) == 2
    assert debtor_weight_dict.get(sqlite_datatype_text()) == "INTEGER"
    assert debtor_weight_dict.get("nullable") == True
