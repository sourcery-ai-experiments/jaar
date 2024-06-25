from src.gift.atom_config import (
    atom_insert,
    atom_delete,
    atom_update,
    category_ref,
    is_category_ref,
    get_atom_config_dict,
    get_atom_order as q_order,
    set_mog,
    get_flattened_atom_table_build,
    get_normalized_world_table_build,
    required_args_text,
    optional_args_text,
    normal_table_name_text,
    normal_specs_text,
    sqlite_datatype_text,
    python_type_text,
    worldunit_text,
    world_otherunit_text,
    world_beliefunit_text,
    world_belief_otherlink_text,
    world_ideaunit_text,
    world_idea_balancelink_text,
    world_idea_reasonunit_text,
    world_idea_reason_premiseunit_text,
    world_idea_suffbelief_text,
    world_idea_healerhold_text,
    world_idea_factunit_text,
)


def test_worldunit_text_ReturnsObj():
    assert worldunit_text() == "worldunit"


def test_world_otherunit_text_ReturnsObj():
    assert world_otherunit_text() == "world_otherunit"


def test_world_beliefunit_text_ReturnsObj():
    assert world_beliefunit_text() == "world_beliefunit"


def test_world_belief_otherlink_text_ReturnsObj():
    assert world_belief_otherlink_text() == "world_belief_otherlink"


def test_world_ideaunit_text_ReturnsObj():
    assert world_ideaunit_text() == "world_ideaunit"


def test_world_idea_balancelink_text_ReturnsObj():
    assert world_idea_balancelink_text() == "world_idea_balancelink"


def test_world_idea_reasonunit_text_ReturnsObj():
    assert world_idea_reasonunit_text() == "world_idea_reasonunit"


def test_world_idea_reason_premiseunit_text_ReturnsObj():
    assert world_idea_reason_premiseunit_text() == "world_idea_reason_premiseunit"


def test_world_idea_suffbelief_text_ReturnsObj():
    assert world_idea_suffbelief_text() == "world_idea_suffbelief"


def test_world_idea_healerhold_text_ReturnsObj():
    assert world_idea_healerhold_text() == "world_idea_healerhold"


def test_world_idea_factunit_text_ReturnsObj():
    assert world_idea_factunit_text() == "world_idea_factunit"


def test_atom_config_HasCorrect_category():
    assert category_ref() == {
        worldunit_text(),
        world_otherunit_text(),
        world_beliefunit_text(),
        world_belief_otherlink_text(),
        world_ideaunit_text(),
        world_idea_balancelink_text(),
        world_idea_reasonunit_text(),
        world_idea_reason_premiseunit_text(),
        world_idea_suffbelief_text(),
        world_idea_healerhold_text(),
        world_idea_factunit_text(),
    }
    assert world_otherunit_text() in category_ref()
    assert is_category_ref("idearoot") is False


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

        if category_dict.get(normal_specs_text()) is None:
            print(f"{category=} {normal_specs_text()} is missing")
            return False
    return True


def test_get_atom_config_dict_EveryCrudOperationHasChangeOrderBelief():
    # GIVEN
    atom_order_text = "atom_order"

    # WHEN / THEN
    assert check_every_crud_dict_has_element(get_atom_config_dict(), atom_order_text)
    mog = atom_order_text
    # # Simple script for editing atom_config.json
    # set_mog("world_otherunit", atom_insert(), mog, 0)
    # set_mog("world_belief_otherlink", atom_insert(), mog, 1)
    # set_mog("beliefunit", atom_insert(), mog, 2)
    # set_mog("world_ideaunit", atom_insert(), mog, 3)
    # set_mog("world_idea_balancelink", atom_insert(), mog, 4)
    # set_mog("world_idea_suffbelief", atom_insert(), mog, 5)
    # set_mog("world_idea_healerhold", atom_insert(), mog, 6)
    # set_mog("world_idea_factunit", atom_insert(), mog, 7)
    # set_mog("world_idea_reasonunit", atom_insert(), mog, 8)
    # set_mog("world_idea_reason_premiseunit", atom_insert(), mog, 9)
    # set_mog("world_otherunit", atom_update(), mog, 10)
    # set_mog("beliefunit", atom_update(), mog, 11)
    # set_mog("world_belief_otherlink", atom_update(), mog, 12)
    # set_mog("world_ideaunit", atom_update(), mog, 13)
    # set_mog("world_idea_balancelink", atom_update(), mog, 14)
    # set_mog("world_idea_factunit", atom_update(), mog, 15)
    # set_mog("world_idea_reason_premiseunit", atom_update(), mog, 16)
    # set_mog("world_idea_reasonunit", atom_update(), mog, 17)
    # set_mog("world_idea_reason_premiseunit", atom_delete(), mog, 18)
    # set_mog("world_idea_reasonunit", atom_delete(), mog, 19)
    # set_mog("world_idea_factunit", atom_delete(), mog, 20)
    # set_mog("world_idea_suffbelief", atom_delete(), mog, 21)
    # set_mog("world_idea_healerhold", atom_delete(), mog, 22)
    # set_mog("world_idea_balancelink", atom_delete(), mog, 23)
    # set_mog("world_ideaunit", atom_delete(), mog, 24)
    # set_mog("world_belief_otherlink", atom_delete(), mog, 25)
    # set_mog("world_otherunit", atom_delete(), mog, 26)
    # set_mog("beliefunit", atom_delete(), mog, 27)
    # set_mog("worldunit", atom_update(), mog, 28)

    assert 0 == q_order("world_otherunit", atom_insert(), mog, 0)
    assert 1 == q_order("world_belief_otherlink", atom_insert(), mog, 1)
    assert 2 == q_order("world_beliefunit", atom_insert(), mog, 2)
    assert 3 == q_order("world_ideaunit", atom_insert(), mog, 3)
    assert 4 == q_order("world_idea_balancelink", atom_insert(), mog, 4)
    assert 5 == q_order("world_idea_suffbelief", atom_insert(), mog, 5)
    assert 6 == q_order("world_idea_healerhold", atom_insert(), mog, 6)
    assert 7 == q_order("world_idea_factunit", atom_insert(), mog, 7)
    assert 8 == q_order("world_idea_reasonunit", atom_insert(), mog, 8)
    assert 9 == q_order("world_idea_reason_premiseunit", atom_insert(), mog, 9)
    assert 10 == q_order("world_otherunit", atom_update(), mog, 10)
    assert 11 == q_order("world_beliefunit", atom_update(), mog, 11)
    assert 12 == q_order("world_belief_otherlink", atom_update(), mog, 12)
    assert 13 == q_order("world_ideaunit", atom_update(), mog, 13)
    assert 14 == q_order("world_idea_balancelink", atom_update(), mog, 14)
    assert 15 == q_order("world_idea_factunit", atom_update(), mog, 15)
    assert 16 == q_order("world_idea_reason_premiseunit", atom_update(), mog, 16)
    assert 17 == q_order("world_idea_reasonunit", atom_update(), mog, 17)
    assert 18 == q_order("world_idea_reason_premiseunit", atom_delete(), mog, 18)
    assert 19 == q_order("world_idea_reasonunit", atom_delete(), mog, 19)
    assert 20 == q_order("world_idea_factunit", atom_delete(), mog, 20)
    assert 21 == q_order("world_idea_suffbelief", atom_delete(), mog, 21)
    assert 22 == q_order("world_idea_healerhold", atom_delete(), mog, 22)
    assert 23 == q_order("world_idea_balancelink", atom_delete(), mog, 23)
    assert 24 == q_order("world_ideaunit", atom_delete(), mog, 24)
    assert 25 == q_order("world_belief_otherlink", atom_delete(), mog, 25)
    assert 26 == q_order("world_otherunit", atom_delete(), mog, 26)
    assert 27 == q_order("world_beliefunit", atom_delete(), mog, 27)
    assert 28 == q_order("worldunit", atom_update(), mog, 28)


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


def check_every_arg_dict_has_elements(atom_config_dict):
    for category_key, category_dict in atom_config_dict.items():
        print(f"{category_key=}")
        _every_category_dict_has_arg_elements(category_dict)
    return True


def test_atom_config_AllArgsHave_python_type_sqlite_datatype():
    # GIVEN
    # WHEN / THEN
    assert check_every_arg_dict_has_elements(get_atom_config_dict())


def test_get_flattened_atom_table_build_ReturnsCorrectObj():
    # GIVEN / WHEN
    atom_columns = get_flattened_atom_table_build()

    # THEN
    assert len(atom_columns) == 111
    assert atom_columns.get("worldunit_UPDATE__other_credor_pool") == "INTEGER"
    # print(f"{atom_columns.keys()=}")


def test_get_normalized_world_table_build_ReturnsCorrectObj():
    # GIVEN / WHEN
    normalized_world_table_build = get_normalized_world_table_build()
    nx = normalized_world_table_build

    # THEN
    assert len(nx) == 11
    cat_worldunit = nx.get(worldunit_text())
    cat_otherunit = nx.get(world_otherunit_text())
    cat_belief = nx.get(world_beliefunit_text())
    cat_otherlink = nx.get(world_belief_otherlink_text())
    cat_idea = nx.get(world_ideaunit_text())
    cat_balancelink = nx.get(world_idea_balancelink_text())
    cat_reason = nx.get(world_idea_reasonunit_text())
    cat_premise = nx.get(world_idea_reason_premiseunit_text())
    cat_suffbelief = nx.get(world_idea_suffbelief_text())
    cat_healerhold = nx.get(world_idea_healerhold_text())
    cat_fact = nx.get(world_idea_factunit_text())

    assert cat_worldunit != None
    assert cat_otherunit != None
    assert cat_belief != None
    assert cat_otherlink != None
    assert cat_idea != None
    assert cat_balancelink != None
    assert cat_reason != None
    assert cat_premise != None
    assert cat_suffbelief != None
    assert cat_healerhold != None
    assert cat_fact != None

    normal_specs_worldunit = cat_worldunit.get(normal_specs_text())
    normal_specs_otherunit = cat_otherunit.get(normal_specs_text())
    normal_specs_belief = cat_belief.get(normal_specs_text())
    normal_specs_otherlink = cat_otherlink.get(normal_specs_text())
    normal_specs_idea = cat_idea.get(normal_specs_text())
    normal_specs_balancelink = cat_balancelink.get(normal_specs_text())
    normal_specs_reason = cat_reason.get(normal_specs_text())
    normal_specs_premise = cat_premise.get(normal_specs_text())
    normal_specs_suffbelief = cat_suffbelief.get(normal_specs_text())
    normal_specs_healerhold = cat_healerhold.get(normal_specs_text())
    normal_specs_fact = cat_fact.get(normal_specs_text())

    columns_text = "columns"
    print(f"{cat_worldunit.keys()=}")
    print(f"{normal_specs_text()=}")
    assert normal_specs_worldunit != None
    assert normal_specs_otherunit != None
    assert normal_specs_belief != None
    assert normal_specs_otherlink != None
    assert normal_specs_idea != None
    assert normal_specs_balancelink != None
    assert normal_specs_reason != None
    assert normal_specs_premise != None
    assert normal_specs_suffbelief != None
    assert normal_specs_healerhold != None
    assert normal_specs_fact != None

    table_name_worldunit = normal_specs_worldunit.get(normal_table_name_text())
    table_name_otherunit = normal_specs_otherunit.get(normal_table_name_text())
    table_name_belief = normal_specs_belief.get(normal_table_name_text())
    table_name_otherlink = normal_specs_otherlink.get(normal_table_name_text())
    table_name_idea = normal_specs_idea.get(normal_table_name_text())
    table_name_balancelink = normal_specs_balancelink.get(normal_table_name_text())
    table_name_reason = normal_specs_reason.get(normal_table_name_text())
    table_name_premise = normal_specs_premise.get(normal_table_name_text())
    table_name_suffbelief = normal_specs_suffbelief.get(normal_table_name_text())
    table_name_healerhold = normal_specs_healerhold.get(normal_table_name_text())
    table_name_fact = normal_specs_fact.get(normal_table_name_text())

    assert table_name_worldunit == "world"
    assert table_name_otherunit == "otherunit"
    assert table_name_belief == "beliefunit"
    assert table_name_otherlink == "otherlink"
    assert table_name_idea == "idea"
    assert table_name_balancelink == "balancelink"
    assert table_name_reason == "reason"
    assert table_name_premise == "premise"
    assert table_name_suffbelief == "suffbelief"
    assert table_name_healerhold == "healerhold"
    assert table_name_fact == "fact"

    assert len(cat_worldunit) == 2
    assert cat_worldunit.get(columns_text) != None

    worldunit_columns = cat_worldunit.get(columns_text)
    assert len(worldunit_columns) == 9
    assert worldunit_columns.get("uid") != None
    assert worldunit_columns.get("_max_tree_traverse") != None
    assert worldunit_columns.get("_meld_strategy") != None
    assert worldunit_columns.get("_monetary_desc") != None
    assert worldunit_columns.get("_other_credor_pool") != None
    assert worldunit_columns.get("_other_debtor_pool") != None
    assert worldunit_columns.get("_penny") != None
    assert worldunit_columns.get("_pixel") != None
    assert worldunit_columns.get("_weight") != None

    assert len(cat_otherunit) == 2
    otherunit_columns = cat_otherunit.get(columns_text)
    assert len(otherunit_columns) == 4
    assert otherunit_columns.get("uid") != None
    assert otherunit_columns.get("other_id") != None
    assert otherunit_columns.get("credor_weight") != None
    assert otherunit_columns.get("debtor_weight") != None

    other_id_dict = otherunit_columns.get("other_id")
    assert len(other_id_dict) == 2
    assert other_id_dict.get(sqlite_datatype_text()) == "TEXT"
    assert other_id_dict.get("nullable") == False
    debtor_weight_dict = otherunit_columns.get("debtor_weight")
    assert len(other_id_dict) == 2
    assert debtor_weight_dict.get(sqlite_datatype_text()) == "INTEGER"
    assert debtor_weight_dict.get("nullable") == True
