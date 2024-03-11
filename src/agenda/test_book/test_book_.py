from src.agenda.party import partyunit_shop
from src.agenda.atom import (
    BookUnit,
    bookunit_shop,
    agendaatom_shop,
    atom_update,
    atom_insert,
    atom_delete,
)
from src.agenda.examples.example_books import get_bookunit_example1
from pytest import raises as pytest_raises


def test_BookUnit_exists():
    # GIVEN / WHEN
    x_bookunit = BookUnit()

    # THEN
    assert x_bookunit.agendaatoms is None
    assert x_bookunit._agenda_build_validated is None


def test_bookunit_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    ex1_bookunit = bookunit_shop()

    # THEN
    assert ex1_bookunit.agendaatoms == {}
    assert ex1_bookunit._agenda_build_validated == False


def test_BookUnit_set_agendaatom_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    ex1_bookunit = bookunit_shop()
    attribute_value = 55
    category = "agendaunit"
    opt1_arg = "_weight"
    optional_args = {opt1_arg: attribute_value}
    required_args = {}
    agenda_weight_agendaatom = agendaatom_shop(
        category,
        atom_update(),
        required_args=required_args,
        optional_args=optional_args,
    )
    assert ex1_bookunit.agendaatoms == {}
    assert agenda_weight_agendaatom.atom_order is None

    # WHEN
    ex1_bookunit.set_agendaatom(agenda_weight_agendaatom)

    # THEN
    assert len(ex1_bookunit.agendaatoms) == 1
    x_update_dict = ex1_bookunit.agendaatoms.get(atom_update())
    # print(f"{x_update_dict=}")
    x_category_agendaatom = x_update_dict.get(category)
    print(f"{x_category_agendaatom=}")
    assert x_category_agendaatom == agenda_weight_agendaatom
    assert agenda_weight_agendaatom.atom_order != None


def test_BookUnit_set_agendaatom_RaisesErrorWhen_is_valid_IsFalse():
    # GIVEN
    ex1_bookunit = bookunit_shop()
    x_category = "agenda_groupunit"
    agenda_weight_agendaatom = agendaatom_shop(x_category, atom_update())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_bookunit.set_agendaatom(agenda_weight_agendaatom)
    assert (
        str(excinfo.value)
        == f"""'{x_category}' UPDATE AgendaAtom is invalid
                x_agendaatom.is_required_args_valid()=False
                x_agendaatom.is_optional_args_valid()=True"""
    )


def test_BookUnit_get_atom_ReturnsCorrectObj():
    # GIVEN
    ex1_bookunit = bookunit_shop()
    agendaunit_text = "agendaunit"
    opt_arg1 = "_weight"
    opt_value = 55
    agendaunit_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    agendaunit_agendaatom.set_optional_arg(x_key=opt_arg1, x_value=opt_value)
    ex1_bookunit.set_agendaatom(agendaunit_agendaatom)

    # WHEN
    gen_agendaatom = ex1_bookunit.get_agendaatom(
        atom_update(), category=agendaunit_text, required_args=[]
    )

    # THEN
    assert gen_agendaatom == agendaunit_agendaatom


def test_BookUnit_add_agendaatom_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    ex1_bookunit = bookunit_shop()
    assert ex1_bookunit.agendaatoms == {}

    # WHEN
    op2_arg = "_weight"
    op2_value = 55
    agendaunit_text = "agendaunit"
    required_args = {}
    optional_args = {op2_arg: op2_value}
    ex1_bookunit.add_agendaatom(
        agendaunit_text,
        atom_update(),
        required_args,
        optional_args=optional_args,
    )

    # THEN
    assert len(ex1_bookunit.agendaatoms) == 1
    x_update_dict = ex1_bookunit.agendaatoms.get(atom_update())
    x_agendaatom = x_update_dict.get(agendaunit_text)
    assert x_agendaatom != None
    assert x_agendaatom.category == agendaunit_text


def test_BookUnit_add_agendaatom_CorrectlySets_AgendaUnit_partyunits():
    # GIVEN
    ex1_bookunit = bookunit_shop()
    assert ex1_bookunit.agendaatoms == {}

    # WHEN
    party_id_text = "party_id"
    bob_text = "Bob"
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
    partyunit_text = "agenda_partyunit"
    ex1_bookunit.add_agendaatom(
        category=partyunit_text,
        crud_text=atom_insert(),
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )
    # THEN
    assert len(ex1_bookunit.agendaatoms) == 1
    assert (
        ex1_bookunit.agendaatoms.get(atom_insert()).get(partyunit_text).get(bob_text)
        != None
    )


def test_BookUnit_get_crud_agendaatoms_list_ReturnsCorrectObj():
    # GIVEN
    ex1_bookunit = get_bookunit_example1()
    assert len(ex1_bookunit.agendaatoms.get(atom_update()).keys()) == 1
    assert ex1_bookunit.agendaatoms.get(atom_insert()) is None
    assert len(ex1_bookunit.agendaatoms.get(atom_delete()).keys()) == 1

    # WHEN
    sue_atom_order_dict = ex1_bookunit.get_crud_agendaatoms_list()

    # THEN
    assert len(sue_atom_order_dict) == 2
    print(f"{sue_atom_order_dict.keys()=}")
    # print(f"{sue_atom_order_dict.get(atom_update())=}")
    assert len(sue_atom_order_dict.get(atom_update())) == 1
    assert len(sue_atom_order_dict.get(atom_delete())) == 1
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_BookUnit_get_agendaatoms_list_ReturnsCorrectObj():
    # GIVEN
    ex1_bookunit = get_bookunit_example1()
    update_dict = ex1_bookunit.agendaatoms.get(atom_update())
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_bookunit.agendaatoms.get(atom_insert()) is None
    delete_dict = ex1_bookunit.agendaatoms.get(atom_delete())
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_bookunit.get_agendaatoms_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get("agendaunit")
    z_atom = sue_atoms_list[1]
    z_atom._crud_cache = None
    print(f"{z_atom=}")
    print(delete_dict.get("agenda_partyunit").keys())
    carmen_partyunit_delete = delete_dict.get("agenda_partyunit").get("Carmen")
    assert sue_atoms_list[1] == carmen_partyunit_delete
    # print(f"{sue_atom_order_dict.keys()=}")
    # # print(f"{sue_atom_order_dict.get(atom_update())=}")
    # assert len(sue_atom_order_dict.get(atom_update())) == 1
    # assert len(sue_atom_order_dict.get(atom_delete())) == 1
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


# def test_BookUnit_add_agendaatom_CorrectlySets_AgendaUnit_max_tree_traverse():
#     # GIVEN
#     ex1_bookunit = bookunit_shop(get_sue_road())
#     assert ex1_bookunit.agendaatoms == {}

#     # WHEN
#     opt2_value = 55
#     category = "agendaunit"
#     opt2_arg = "_weight"
#     weight_agendaatom = agendaatom_shop(category, atom_update())
#     weight_agendaatom.set_optional_arg(opt2_arg, opt2_value)
#     ex1_bookunit.set_agendaatom(weight_agendaatom)
#     # THEN
#     assert len(ex1_bookunit.agendaatoms.get(atom_update()).keys()) == 1
#     sue_agendaunit_dict = ex1_bookunit.agendaatoms.get(atom_update())
#     sue_weight_agendaatom = sue_agendaunit_dict.get(category)
#     print(f"{sue_weight_agendaatom=}")
#     assert weight_agendaatom == sue_weight_agendaatom

#     # WHEN
#     new2_value = 66
#     x_attribute = "_max_tree_traverse"
#     required_args = {x_attribute: new2_value}
#     x_agendaatom = agendaatom_shop(x_attribute, atom_update(), None, required_args)
#     ex1_bookunit.set_agendaatom(x_agendaatom)
#     # THEN
#     print(f"{ex1_bookunit.agendaatoms.keys()=}")
#     print(f"{ex1_bookunit.agendaatoms.get(atom_update()).keys()=}")
#     # print(f"{get_all_nondictionary_objs(ex1_bookunit.agendaatoms).get(atom_update())=}")
#     assert len(ex1_bookunit.agendaatoms.get(atom_update()).keys()) == 2
#     assert x_agendaatom == ex1_bookunit.agendaatoms.get(atom_update()).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = "_party_creditor_pool"
#     required_args = {x_attribute: new3_value}
#     x_agendaatom = agendaatom_shop(x_attribute, atom_update(), None, required_args)
#     ex1_bookunit.set_agendaatom(x_agendaatom)
#     # THEN
#     assert len(ex1_bookunit.agendaatoms.get(atom_update()).keys()) == 3
#     assert x_agendaatom == ex1_bookunit.agendaatoms.get(atom_update()).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "_party_debtor_pool"
#     required_args = {x_attribute: new4_value}
#     x_agendaatom = agendaatom_shop(x_attribute, atom_update(), None, required_args)
#     ex1_bookunit.set_agendaatom(x_agendaatom)
#     # THEN
#     assert len(ex1_bookunit.agendaatoms.get(atom_update()).keys()) == 4
#     assert x_agendaatom == ex1_bookunit.agendaatoms.get(atom_update()).get(x_attribute)

#     # WHEN
#     new5_value = "override"
#     x_attribute = "_meld_strategy"
#     required_args = {x_attribute: new5_value}
#     x_agendaatom = agendaatom_shop(x_attribute, atom_update(), None, required_args)
#     ex1_bookunit.set_agendaatom(x_agendaatom)
#     # THEN
#     assert len(ex1_bookunit.agendaatoms.get(atom_update()).keys()) == 5
#     assert x_agendaatom == ex1_bookunit.agendaatoms.get(atom_update()).get(x_attribute)


def test_BookUnit_get_sorted_agendaatoms_ReturnsCorrectObj():
    # GIVEN
    ex1_bookunit = get_bookunit_example1()
    agendaunit_text = "agendaunit"
    agenda_partyunit_text = "agenda_partyunit"
    update_dict = ex1_bookunit.agendaatoms.get(atom_update())
    assert len(update_dict.keys()) == 1
    assert update_dict.get(agendaunit_text) != None
    print(f"atom_order 28 {ex1_bookunit.agendaatoms.get(atom_update()).keys()=}")
    delete_dict = ex1_bookunit.agendaatoms.get(atom_delete())
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(agenda_partyunit_text) != None
    print(f"atom_order 26 {ex1_bookunit.agendaatoms.get(atom_delete()).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_bookunit.get_sorted_agendaatoms()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get("agenda_partyunit").keys())
    carmen_partyunit_delete = delete_dict.get("agenda_partyunit").get("Carmen")
    # for agendaatom in sue_atom_order_list:
    #     print(f"{agendaatom.atom_order=}")
    assert sue_atom_order_list[0] == carmen_partyunit_delete
    assert sue_atom_order_list[1] == update_dict.get(agendaunit_text)
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_BookUnit_agenda_build_validate_CorrectlySetsTrue():
    # GIVEN
    ex1_bookunit = get_bookunit_example1()
    # assert len(ex1_bookunit.agendaatoms.get(atom_update()).keys()) == 1
    # assert ex1_bookunit.agendaatoms.get(atom_insert()) is None
    # assert len(ex1_bookunit.agendaatoms.get(atom_delete()).keys()) == 1

    # # WHEN
    # sue_atom_order_dict = ex1_bookunit.get_sorted_agendaatoms()

    # # THEN
    # assert len(sue_atom_order_dict) == 2
    # print(f"{sue_atom_order_dict.keys()=}")
    # print(f"{sue_atom_order_dict.get(atom_update())=}")
    # assert len(sue_atom_order_dict.get(atom_update())) == 1
    # assert len(sue_atom_order_dict.get(atom_delete())) == 1


def test_BookUnit_agenda_build_validate_CorrectlySetsFalse():
    # GIVEN
    ex1_bookunit = get_bookunit_example1()
    # assert len(ex1_bookunit.agendaatoms.get(atom_update()).keys()) == 1
    # assert ex1_bookunit.agendaatoms.get(atom_insert()) is None
    # assert len(ex1_bookunit.agendaatoms.get(atom_delete()).keys()) == 1

    # # WHEN
    # sue_atom_order_dict = ex1_bookunit.get_sorted_agendaatoms()

    # # THEN
    # assert len(sue_atom_order_dict) == 2
    # print(f"{sue_atom_order_dict.keys()=}")
    # print(f"{sue_atom_order_dict.get(atom_update())=}")
    # assert len(sue_atom_order_dict.get(atom_update())) == 1
    # assert len(sue_atom_order_dict.get(atom_delete())) == 1
