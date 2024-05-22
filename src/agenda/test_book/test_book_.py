from src._road.road import create_road, get_default_world_id_roadnode as root_label
from src.agenda.party import partyunit_shop
from src.agenda.book import (
    BookUnit,
    bookunit_shop,
    validate_agenda_build_from_book,
    agendaatom_shop,
    atom_update,
    atom_insert,
    atom_delete,
)
from src.agenda.agenda import agendaunit_shop
from src.agenda.examples.example_books import get_bookunit_example1
from src._instrument.python import x_is_json
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
    bob_partyunit = partyunit_shop(bob_text, bob_creditor_weight, bob_debtor_weight)
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
    sue_atom_order_dict = ex1_bookunit._get_crud_agendaatoms_list()

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


def test_BookUnit_get_category_sorted_agendaatoms_list_ReturnsCorrectObj():
    # GIVEN
    ex1_bookunit = get_bookunit_example1()
    update_dict = ex1_bookunit.agendaatoms.get(atom_update())
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_bookunit.agendaatoms.get(atom_insert()) is None
    delete_dict = ex1_bookunit.agendaatoms.get(atom_delete())
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_bookunit.get_category_sorted_agendaatoms_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get("agendaunit")
    z_atom = sue_atoms_list[1]
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


def test_BookUnit_get_sorted_agendaatoms_ReturnsCorrectObj_IdeaUnitsSorted():
    # GIVEN
    x_world_id = root_label()
    sports_text = "sports"
    sports_road = create_road(x_world_id, sports_text)
    knee_text = "knee"
    x_category = "agenda_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    sports_insert_ideaunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    sports_insert_ideaunit_agendaatom.set_required_arg(label_text, sports_text)
    sports_insert_ideaunit_agendaatom.set_required_arg(parent_road_text, x_world_id)
    knee_insert_ideaunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    knee_insert_ideaunit_agendaatom.set_required_arg(label_text, knee_text)
    knee_insert_ideaunit_agendaatom.set_required_arg(parent_road_text, sports_road)
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(knee_insert_ideaunit_agendaatom)
    x_bookunit.set_agendaatom(sports_insert_ideaunit_agendaatom)

    # WHEN
    x_atom_order_list = x_bookunit.get_sorted_agendaatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for agendaatom in x_atom_order_list:
    #     print(f"{agendaatom.required_args=}")
    assert x_atom_order_list[0] == sports_insert_ideaunit_agendaatom
    assert x_atom_order_list[1] == knee_insert_ideaunit_agendaatom
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_BookUnit_get_sorted_agendaatoms_ReturnsCorrectObj_Road_Sorted():
    # GIVEN
    x_world_id = root_label()
    sports_text = "sports"
    sports_road = create_road(x_world_id, sports_text)
    knee_text = "knee"
    knee_road = create_road(sports_road, knee_text)
    x_category = "agenda_idea_balancelink"
    road_text = "road"
    group_id_text = "group_id"
    swimmers_text = ",Swimmers"
    sports_balancelink_agendaatom = agendaatom_shop(x_category, atom_insert())
    sports_balancelink_agendaatom.set_required_arg(group_id_text, swimmers_text)
    sports_balancelink_agendaatom.set_required_arg(road_text, sports_road)
    knee_balancelink_agendaatom = agendaatom_shop(x_category, atom_insert())
    knee_balancelink_agendaatom.set_required_arg(group_id_text, swimmers_text)
    knee_balancelink_agendaatom.set_required_arg(road_text, knee_road)
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(knee_balancelink_agendaatom)
    x_bookunit.set_agendaatom(sports_balancelink_agendaatom)

    # WHEN
    x_atom_order_list = x_bookunit.get_sorted_agendaatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for agendaatom in x_atom_order_list:
    #     print(f"{agendaatom.required_args=}")
    assert x_atom_order_list[0] == sports_balancelink_agendaatom
    assert x_atom_order_list[1] == knee_balancelink_agendaatom
    # for crud_text, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.category=}")


def test_validate_agenda_build_from_book_ReturnsCorrectObjGivenNoAgenda():
    # GIVEN
    sue_bookunit = bookunit_shop()

    agendaunit_text = "agendaunit"
    x_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    x_attribute = "_party_creditor_pool"
    x_agendaatom.set_optional_arg(x_attribute, 100)
    sue_bookunit.set_agendaatom(x_agendaatom)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    x_agendaatom = agendaatom_shop(category, atom_insert())
    x_agendaatom.set_arg("party_id", carm_text)
    x_agendaatom.set_arg("creditor_weight", 70)
    sue_bookunit.set_agendaatom(x_agendaatom)

    # WHEN/THEN
    assert validate_agenda_build_from_book(sue_bookunit) == False

    # WHEN
    rico_text = "Rico"
    x_agendaatom = agendaatom_shop(category, atom_insert())
    x_agendaatom.set_arg("party_id", rico_text)
    x_agendaatom.set_arg("creditor_weight", 30)
    sue_bookunit.set_agendaatom(x_agendaatom)

    # THEN
    assert validate_agenda_build_from_book(sue_bookunit)

    # WHEN
    bob_text = "Bob"
    x_agendaatom = agendaatom_shop(category, atom_insert())
    x_agendaatom.set_arg("party_id", bob_text)
    x_agendaatom.set_arg("creditor_weight", 35)
    sue_bookunit.set_agendaatom(x_agendaatom)

    # THEN
    assert validate_agenda_build_from_book(sue_bookunit) == False


def test_validate_agenda_build_from_book_ReturnsCorrectObjGivenAgenda():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_creditor_pool(100)

    sue_bookunit = bookunit_shop()

    category = "agenda_partyunit"
    carm_text = "Carmen"
    x_agendaatom = agendaatom_shop(category, atom_insert())
    x_agendaatom.set_arg("party_id", carm_text)
    x_agendaatom.set_arg("creditor_weight", 70)
    sue_bookunit.set_agendaatom(x_agendaatom)

    # WHEN/THEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_creditor_pool(100)
    assert validate_agenda_build_from_book(sue_bookunit, sue_agenda) == False

    # WHEN
    rico_text = "Rico"
    x_agendaatom = agendaatom_shop(category, atom_insert())
    x_agendaatom.set_arg("party_id", rico_text)
    x_agendaatom.set_arg("creditor_weight", 30)
    sue_bookunit.set_agendaatom(x_agendaatom)

    # THEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_creditor_pool(100)
    assert validate_agenda_build_from_book(sue_bookunit, sue_agenda)

    # WHEN
    bob_text = "Bob"
    x_agendaatom = agendaatom_shop(category, atom_insert())
    x_agendaatom.set_arg("party_id", bob_text)
    x_agendaatom.set_arg("creditor_weight", 35)
    sue_bookunit.set_agendaatom(x_agendaatom)

    # THEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_creditor_pool(100)
    assert validate_agenda_build_from_book(sue_bookunit, sue_agenda) == False


def test_BookUnit_get_ordered_agendaatoms_ReturnsCorrectObj_GivenNoStartingNumber():
    # GIVEN
    sue_bookunit = bookunit_shop()
    agendaunit_text = "agendaunit"
    pool_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    pool_attribute = "_party_creditor_pool"
    pool_agendaatom.set_optional_arg(pool_attribute, 100)
    sue_bookunit.set_agendaatom(pool_agendaatom)
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_agendaatom = agendaatom_shop(category, atom_insert())
    carm_agendaatom.set_arg("party_id", carm_text)
    carm_agendaatom.set_arg("creditor_weight", 70)
    sue_bookunit.set_agendaatom(carm_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_creditor_pool(100)
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_insert())
    rico_agendaatom.set_arg("party_id", rico_text)
    rico_agendaatom.set_arg("creditor_weight", 30)
    sue_bookunit.set_agendaatom(rico_agendaatom)

    sue_agenda = agendaunit_shop("Sue")
    assert validate_agenda_build_from_book(sue_bookunit, sue_agenda)

    # WHEN
    bookunit_dict = sue_bookunit.get_ordered_agendaatoms()

    # THEN
    # book_carm = bookunit_dict.get(0)
    # book_rico = bookunit_dict.get(1)
    # book_pool = bookunit_dict.get(2)
    # assert book_carm == carm_agendaatom
    # assert book_rico == rico_agendaatom
    # assert book_pool == pool_agendaatom
    assert bookunit_dict.get(0) == carm_agendaatom
    assert bookunit_dict.get(1) == rico_agendaatom
    assert bookunit_dict.get(2) == pool_agendaatom


def test_BookUnit_get_ordered_agendaatoms_ReturnsCorrectObj_GivenStartingNumber():
    # GIVEN
    sue_bookunit = bookunit_shop()
    agendaunit_text = "agendaunit"
    pool_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    pool_attribute = "_party_creditor_pool"
    pool_agendaatom.set_optional_arg(pool_attribute, 100)
    sue_bookunit.set_agendaatom(pool_agendaatom)
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_agendaatom = agendaatom_shop(category, atom_insert())
    carm_agendaatom.set_arg("party_id", carm_text)
    carm_agendaatom.set_arg("creditor_weight", 70)
    sue_bookunit.set_agendaatom(carm_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_creditor_pool(100)
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_insert())
    rico_agendaatom.set_arg("party_id", rico_text)
    rico_agendaatom.set_arg("creditor_weight", 30)
    sue_bookunit.set_agendaatom(rico_agendaatom)

    sue_agenda = agendaunit_shop("Sue")
    assert validate_agenda_build_from_book(sue_bookunit, sue_agenda)

    # WHEN
    bookunit_dict = sue_bookunit.get_ordered_agendaatoms(5)

    # THEN
    # book_carm = bookunit_dict.get(0)
    # book_rico = bookunit_dict.get(1)
    # book_pool = bookunit_dict.get(2)
    # assert book_carm == carm_agendaatom
    # assert book_rico == rico_agendaatom
    # assert book_pool == pool_agendaatom
    assert bookunit_dict.get(5) == carm_agendaatom
    assert bookunit_dict.get(6) == rico_agendaatom
    assert bookunit_dict.get(7) == pool_agendaatom


def test_BookUnit_get_ordered_dict_ReturnsCorrectObj_GivenStartingNumber():
    # GIVEN
    sue_bookunit = bookunit_shop()
    agendaunit_text = "agendaunit"
    pool_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    pool_attribute = "_party_creditor_pool"
    pool_agendaatom.set_optional_arg(pool_attribute, 100)
    sue_bookunit.set_agendaatom(pool_agendaatom)
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_agendaatom = agendaatom_shop(category, atom_insert())
    carm_agendaatom.set_arg("party_id", carm_text)
    carm_agendaatom.set_arg("creditor_weight", 70)
    sue_bookunit.set_agendaatom(carm_agendaatom)
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_creditor_pool(100)
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_insert())
    rico_agendaatom.set_arg("party_id", rico_text)
    rico_agendaatom.set_arg("creditor_weight", 30)
    sue_bookunit.set_agendaatom(rico_agendaatom)

    sue_agenda = agendaunit_shop("Sue")
    assert validate_agenda_build_from_book(sue_bookunit, sue_agenda)

    # WHEN
    bookunit_dict = sue_bookunit.get_ordered_dict(5)

    # THEN
    # book_carm = bookunit_dict.get(0)
    # book_rico = bookunit_dict.get(1)
    # book_pool = bookunit_dict.get(2)
    # assert book_carm == carm_agendaatom
    # assert book_rico == rico_agendaatom
    # assert book_pool == pool_agendaatom
    assert bookunit_dict.get(5) == carm_agendaatom.get_dict()
    assert bookunit_dict.get(6) == rico_agendaatom.get_dict()
    assert bookunit_dict.get(7) == pool_agendaatom.get_dict()


def test_BookUnit_get_json_ReturnsCorrectObj():
    # GIVEN
    sue_bookunit = bookunit_shop()
    agendaunit_text = "agendaunit"
    pool_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    pool_attribute = "_party_creditor_pool"
    pool_agendaatom.set_optional_arg(pool_attribute, 100)
    sue_bookunit.set_agendaatom(pool_agendaatom)
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_agendaatom = agendaatom_shop(category, atom_insert())
    carm_agendaatom.set_arg("party_id", carm_text)
    carm_agendaatom.set_arg("creditor_weight", 70)
    sue_bookunit.set_agendaatom(carm_agendaatom)
    rico_text = "Rico"
    rico_agendaatom = agendaatom_shop(category, atom_insert())
    rico_agendaatom.set_arg("party_id", rico_text)
    rico_agendaatom.set_arg("creditor_weight", 30)
    sue_bookunit.set_agendaatom(rico_agendaatom)

    # WHEN
    book_start_int = 5
    bookunit_json = sue_bookunit.get_json(book_start_int)

    # THEN
    assert x_is_json(bookunit_json)


def test_BookUnit_agendaatom_exists_ReturnsCorrectObj():
    # GIVEN
    farm_bookunit = bookunit_shop()

    # WHEN / THEN
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_agendaatom = agendaatom_shop(category, atom_insert())
    carm_agendaatom.set_arg("party_id", carm_text)
    carm_agendaatom.set_arg("creditor_weight", 70)
    assert farm_bookunit.agendaatom_exists(carm_agendaatom) == False

    # WHEN
    farm_bookunit.set_agendaatom(carm_agendaatom)

    # THEN
    assert farm_bookunit.agendaatom_exists(carm_agendaatom)
