from src._road.road import create_road, get_default_real_id_roadnode as root_label
from src.agenda.party import partyunit_shop
from src.atom.nuc import (
    NucUnit,
    nucunit_shop,
    validate_agenda_build_from_nuc,
    quarkunit_shop,
    quark_update,
    quark_insert,
    quark_delete,
)
from src.agenda.agenda import agendaunit_shop
from src.atom.examples.example_nucs import get_nucunit_example1
from src._instrument.python import x_is_json
from pytest import raises as pytest_raises


def test_NucUnit_exists():
    # GIVEN / WHEN
    x_nucunit = NucUnit()

    # THEN
    assert x_nucunit.quarkunits is None
    assert x_nucunit._agenda_build_validated is None


def test_nucunit_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    ex1_nucunit = nucunit_shop()

    # THEN
    assert ex1_nucunit.quarkunits == {}
    assert ex1_nucunit._agenda_build_validated is False


def test_NucUnit_set_quarkunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    ex1_nucunit = nucunit_shop()
    attribute_value = 55
    category = "agendaunit"
    opt1_arg = "_weight"
    optional_args = {opt1_arg: attribute_value}
    required_args = {}
    agenda_weight_quarkunit = quarkunit_shop(
        category,
        quark_update(),
        required_args=required_args,
        optional_args=optional_args,
    )
    assert ex1_nucunit.quarkunits == {}
    assert agenda_weight_quarkunit.quark_order is None

    # WHEN
    ex1_nucunit.set_quarkunit(agenda_weight_quarkunit)

    # THEN
    assert len(ex1_nucunit.quarkunits) == 1
    x_update_dict = ex1_nucunit.quarkunits.get(quark_update())
    # print(f"{x_update_dict=}")
    x_category_quarkunit = x_update_dict.get(category)
    print(f"{x_category_quarkunit=}")
    assert x_category_quarkunit == agenda_weight_quarkunit
    assert agenda_weight_quarkunit.quark_order != None


def test_NucUnit_set_quarkunit_RaisesErrorWhen_is_valid_IsFalse():
    # GIVEN
    ex1_nucunit = nucunit_shop()
    x_category = "agenda_beliefunit"
    agenda_weight_quarkunit = quarkunit_shop(x_category, quark_update())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_nucunit.set_quarkunit(agenda_weight_quarkunit)
    assert (
        str(excinfo.value)
        == f"""'{x_category}' UPDATE QuarkUnit is invalid
                x_quarkunit.is_required_args_valid()=False
                x_quarkunit.is_optional_args_valid()=True"""
    )


def test_NucUnit_get_quark_ReturnsCorrectObj():
    # GIVEN
    ex1_nucunit = nucunit_shop()
    agendaunit_text = "agendaunit"
    opt_arg1 = "_weight"
    opt_value = 55
    agendaunit_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    agendaunit_quarkunit.set_optional_arg(x_key=opt_arg1, x_value=opt_value)
    ex1_nucunit.set_quarkunit(agendaunit_quarkunit)

    # WHEN
    gen_quarkunit = ex1_nucunit.get_quarkunit(
        quark_update(), category=agendaunit_text, required_args=[]
    )

    # THEN
    assert gen_quarkunit == agendaunit_quarkunit


def test_NucUnit_add_quarkunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    ex1_nucunit = nucunit_shop()
    assert ex1_nucunit.quarkunits == {}

    # WHEN
    op2_arg = "_weight"
    op2_value = 55
    agendaunit_text = "agendaunit"
    required_args = {}
    optional_args = {op2_arg: op2_value}
    ex1_nucunit.add_quarkunit(
        agendaunit_text,
        quark_update(),
        required_args,
        optional_args=optional_args,
    )

    # THEN
    assert len(ex1_nucunit.quarkunits) == 1
    x_update_dict = ex1_nucunit.quarkunits.get(quark_update())
    x_quarkunit = x_update_dict.get(agendaunit_text)
    assert x_quarkunit != None
    assert x_quarkunit.category == agendaunit_text


def test_NucUnit_add_quarkunit_CorrectlySets_AgendaUnit_partyunits():
    # GIVEN
    ex1_nucunit = nucunit_shop()
    assert ex1_nucunit.quarkunits == {}

    # WHEN
    party_id_text = "party_id"
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    party_id_text = "party_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    bob_required_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    bob_optional_dict = {cw_text: bob_partyunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)
    print(f"{bob_required_dict=}")
    partyunit_text = "agenda_partyunit"
    ex1_nucunit.add_quarkunit(
        category=partyunit_text,
        crud_text=quark_insert(),
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )
    # THEN
    assert len(ex1_nucunit.quarkunits) == 1
    assert (
        ex1_nucunit.quarkunits.get(quark_insert()).get(partyunit_text).get(bob_text)
        != None
    )


def test_NucUnit_get_crud_quarkunits_list_ReturnsCorrectObj():
    # GIVEN
    ex1_nucunit = get_nucunit_example1()
    assert len(ex1_nucunit.quarkunits.get(quark_update()).keys()) == 1
    assert ex1_nucunit.quarkunits.get(quark_insert()) is None
    assert len(ex1_nucunit.quarkunits.get(quark_delete()).keys()) == 1

    # WHEN
    sue_quark_order_dict = ex1_nucunit._get_crud_quarkunits_list()

    # THEN
    assert len(sue_quark_order_dict) == 2
    print(f"{sue_quark_order_dict.keys()=}")
    # print(f"{sue_quark_order_dict.get(quark_update())=}")
    assert len(sue_quark_order_dict.get(quark_update())) == 1
    assert len(sue_quark_order_dict.get(quark_delete())) == 1
    # for crud_text, quark_list in sue_quark_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(quark_list)=}")
    #     for x_quark in quark_list:
    #         print(f"{x_quark.category=}")


def test_NucUnit_get_category_sorted_quarkunits_list_ReturnsCorrectObj():
    # GIVEN
    ex1_nucunit = get_nucunit_example1()
    update_dict = ex1_nucunit.quarkunits.get(quark_update())
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_nucunit.quarkunits.get(quark_insert()) is None
    delete_dict = ex1_nucunit.quarkunits.get(quark_delete())
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_quarks_list = ex1_nucunit.get_category_sorted_quarkunits_list()

    # THEN
    assert len(sue_quarks_list) == 2
    assert sue_quarks_list[0] == update_dict.get("agendaunit")
    z_quark = sue_quarks_list[1]
    print(f"{z_quark=}")
    print(delete_dict.get("agenda_partyunit").keys())
    carmen_partyunit_delete = delete_dict.get("agenda_partyunit").get("Carmen")
    assert sue_quarks_list[1] == carmen_partyunit_delete
    # print(f"{sue_quark_order_dict.keys()=}")
    # # print(f"{sue_quark_order_dict.get(quark_update())=}")
    # assert len(sue_quark_order_dict.get(quark_update())) == 1
    # assert len(sue_quark_order_dict.get(quark_delete())) == 1
    # for crud_text, quark_list in sue_quark_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(quark_list)=}")
    #     for x_quark in quark_list:
    #         print(f"{x_quark.category=}")


# def test_NucUnit_add_quarkunit_CorrectlySets_AgendaUnit_max_tree_traverse():
#     # GIVEN
#     ex1_nucunit = nucunit_shop(get_sue_road())
#     assert ex1_nucunit.quarkunits == {}

#     # WHEN
#     opt2_value = 55
#     category = "agendaunit"
#     opt2_arg = "_weight"
#     weight_quarkunit = quarkunit_shop(category, quark_update())
#     weight_quarkunit.set_optional_arg(opt2_arg, opt2_value)
#     ex1_nucunit.set_quarkunit(weight_quarkunit)
#     # THEN
#     assert len(ex1_nucunit.quarkunits.get(quark_update()).keys()) == 1
#     sue_agendaunit_dict = ex1_nucunit.quarkunits.get(quark_update())
#     sue_weight_quarkunit = sue_agendaunit_dict.get(category)
#     print(f"{sue_weight_quarkunit=}")
#     assert weight_quarkunit == sue_weight_quarkunit

#     # WHEN
#     new2_value = 66
#     x_attribute = "_max_tree_traverse"
#     required_args = {x_attribute: new2_value}
#     x_quarkunit = quarkunit_shop(x_attribute, quark_update(), None, required_args)
#     ex1_nucunit.set_quarkunit(x_quarkunit)
#     # THEN
#     print(f"{ex1_nucunit.quarkunits.keys()=}")
#     print(f"{ex1_nucunit.quarkunits.get(quark_update()).keys()=}")
#     assert len(ex1_nucunit.quarkunits.get(quark_update()).keys()) == 2
#     assert x_quarkunit == ex1_nucunit.quarkunits.get(quark_update()).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = "_party_credor_pool"
#     required_args = {x_attribute: new3_value}
#     x_quarkunit = quarkunit_shop(x_attribute, quark_update(), None, required_args)
#     ex1_nucunit.set_quarkunit(x_quarkunit)
#     # THEN
#     assert len(ex1_nucunit.quarkunits.get(quark_update()).keys()) == 3
#     assert x_quarkunit == ex1_nucunit.quarkunits.get(quark_update()).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "_party_debtor_pool"
#     required_args = {x_attribute: new4_value}
#     x_quarkunit = quarkunit_shop(x_attribute, quark_update(), None, required_args)
#     ex1_nucunit.set_quarkunit(x_quarkunit)
#     # THEN
#     assert len(ex1_nucunit.quarkunits.get(quark_update()).keys()) == 4
#     assert x_quarkunit == ex1_nucunit.quarkunits.get(quark_update()).get(x_attribute)

#     # WHEN
#     new5_value = "override"
#     x_attribute = "_meld_strategy"
#     required_args = {x_attribute: new5_value}
#     x_quarkunit = quarkunit_shop(x_attribute, quark_update(), None, required_args)
#     ex1_nucunit.set_quarkunit(x_quarkunit)
#     # THEN
#     assert len(ex1_nucunit.quarkunits.get(quark_update()).keys()) == 5
#     assert x_quarkunit == ex1_nucunit.quarkunits.get(quark_update()).get(x_attribute)


def test_NucUnit_get_sorted_quarkunits_ReturnsCorrectObj():
    # GIVEN
    ex1_nucunit = get_nucunit_example1()
    agendaunit_text = "agendaunit"
    agenda_partyunit_text = "agenda_partyunit"
    update_dict = ex1_nucunit.quarkunits.get(quark_update())
    assert len(update_dict.keys()) == 1
    assert update_dict.get(agendaunit_text) != None
    print(f"quark_order 28 {ex1_nucunit.quarkunits.get(quark_update()).keys()=}")
    delete_dict = ex1_nucunit.quarkunits.get(quark_delete())
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(agenda_partyunit_text) != None
    print(f"quark_order 26 {ex1_nucunit.quarkunits.get(quark_delete()).keys()=}")

    # WHEN
    sue_quark_order_list = ex1_nucunit.get_sorted_quarkunits()

    # THEN
    assert len(sue_quark_order_list) == 2
    print(delete_dict.get("agenda_partyunit").keys())
    carmen_partyunit_delete = delete_dict.get("agenda_partyunit").get("Carmen")
    # for quarkunit in sue_quark_order_list:
    #     print(f"{quarkunit.quark_order=}")
    assert sue_quark_order_list[0] == carmen_partyunit_delete
    assert sue_quark_order_list[1] == update_dict.get(agendaunit_text)
    # for crud_text, quark_list in sue_quark_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(quark_list)=}")
    #     for x_quark in quark_list:
    #         print(f"{x_quark.category=}")


def test_NucUnit_get_sorted_quarkunits_ReturnsCorrectObj_IdeaUnitsSorted():
    # GIVEN
    x_real_id = root_label()
    sports_text = "sports"
    sports_road = create_road(x_real_id, sports_text)
    knee_text = "knee"
    x_category = "agenda_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    sports_insert_ideaunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    sports_insert_ideaunit_quarkunit.set_required_arg(label_text, sports_text)
    sports_insert_ideaunit_quarkunit.set_required_arg(parent_road_text, x_real_id)
    knee_insert_ideaunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    knee_insert_ideaunit_quarkunit.set_required_arg(label_text, knee_text)
    knee_insert_ideaunit_quarkunit.set_required_arg(parent_road_text, sports_road)
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(knee_insert_ideaunit_quarkunit)
    x_nucunit.set_quarkunit(sports_insert_ideaunit_quarkunit)

    # WHEN
    x_quark_order_list = x_nucunit.get_sorted_quarkunits()

    # THEN
    assert len(x_quark_order_list) == 2
    # for quarkunit in x_quark_order_list:
    #     print(f"{quarkunit.required_args=}")
    assert x_quark_order_list[0] == sports_insert_ideaunit_quarkunit
    assert x_quark_order_list[1] == knee_insert_ideaunit_quarkunit
    # for crud_text, quark_list in sue_quark_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(quark_list)=}")
    #     for x_quark in quark_list:
    #         print(f"{x_quark.category=}")


def test_NucUnit_get_sorted_quarkunits_ReturnsCorrectObj_Road_Sorted():
    # GIVEN
    x_real_id = root_label()
    sports_text = "sports"
    sports_road = create_road(x_real_id, sports_text)
    knee_text = "knee"
    knee_road = create_road(sports_road, knee_text)
    x_category = "agenda_idea_balancelink"
    road_text = "road"
    belief_id_text = "belief_id"
    swimmers_text = ",Swimmers"
    sports_balancelink_quarkunit = quarkunit_shop(x_category, quark_insert())
    sports_balancelink_quarkunit.set_required_arg(belief_id_text, swimmers_text)
    sports_balancelink_quarkunit.set_required_arg(road_text, sports_road)
    knee_balancelink_quarkunit = quarkunit_shop(x_category, quark_insert())
    knee_balancelink_quarkunit.set_required_arg(belief_id_text, swimmers_text)
    knee_balancelink_quarkunit.set_required_arg(road_text, knee_road)
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(knee_balancelink_quarkunit)
    x_nucunit.set_quarkunit(sports_balancelink_quarkunit)

    # WHEN
    x_quark_order_list = x_nucunit.get_sorted_quarkunits()

    # THEN
    assert len(x_quark_order_list) == 2
    # for quarkunit in x_quark_order_list:
    #     print(f"{quarkunit.required_args=}")
    assert x_quark_order_list[0] == sports_balancelink_quarkunit
    assert x_quark_order_list[1] == knee_balancelink_quarkunit
    # for crud_text, quark_list in sue_quark_order_dict.items():
    #     print(f"{crud_text=}")
    #     print(f"{len(quark_list)=}")
    #     for x_quark in quark_list:
    #         print(f"{x_quark.category=}")


def test_validate_agenda_build_from_nuc_ReturnsCorrectObjGivenNoAgenda():
    # GIVEN
    sue_nucunit = nucunit_shop()

    agendaunit_text = "agendaunit"
    x_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    x_attribute = "_party_credor_pool"
    x_quarkunit.set_optional_arg(x_attribute, 100)
    sue_nucunit.set_quarkunit(x_quarkunit)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    x_quarkunit = quarkunit_shop(category, quark_insert())
    x_quarkunit.set_arg("party_id", carm_text)
    x_quarkunit.set_arg("credor_weight", 70)
    sue_nucunit.set_quarkunit(x_quarkunit)

    # WHEN/THEN
    assert validate_agenda_build_from_nuc(sue_nucunit) is False

    # WHEN
    rico_text = "Rico"
    x_quarkunit = quarkunit_shop(category, quark_insert())
    x_quarkunit.set_arg("party_id", rico_text)
    x_quarkunit.set_arg("credor_weight", 30)
    sue_nucunit.set_quarkunit(x_quarkunit)

    # THEN
    assert validate_agenda_build_from_nuc(sue_nucunit)

    # WHEN
    bob_text = "Bob"
    x_quarkunit = quarkunit_shop(category, quark_insert())
    x_quarkunit.set_arg("party_id", bob_text)
    x_quarkunit.set_arg("credor_weight", 35)
    sue_nucunit.set_quarkunit(x_quarkunit)

    # THEN
    assert validate_agenda_build_from_nuc(sue_nucunit) is False


def test_validate_agenda_build_from_nuc_ReturnsCorrectObjGivenAgenda():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_credor_pool(100)

    sue_nucunit = nucunit_shop()

    category = "agenda_partyunit"
    carm_text = "Carmen"
    x_quarkunit = quarkunit_shop(category, quark_insert())
    x_quarkunit.set_arg("party_id", carm_text)
    x_quarkunit.set_arg("credor_weight", 70)
    sue_nucunit.set_quarkunit(x_quarkunit)

    # WHEN/THEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_credor_pool(100)
    assert validate_agenda_build_from_nuc(sue_nucunit, sue_agenda) is False

    # WHEN
    rico_text = "Rico"
    x_quarkunit = quarkunit_shop(category, quark_insert())
    x_quarkunit.set_arg("party_id", rico_text)
    x_quarkunit.set_arg("credor_weight", 30)
    sue_nucunit.set_quarkunit(x_quarkunit)

    # THEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_credor_pool(100)
    assert validate_agenda_build_from_nuc(sue_nucunit, sue_agenda)

    # WHEN
    bob_text = "Bob"
    x_quarkunit = quarkunit_shop(category, quark_insert())
    x_quarkunit.set_arg("party_id", bob_text)
    x_quarkunit.set_arg("credor_weight", 35)
    sue_nucunit.set_quarkunit(x_quarkunit)

    # THEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_credor_pool(100)
    assert validate_agenda_build_from_nuc(sue_nucunit, sue_agenda) is False


def test_NucUnit_get_ordered_quarkunits_ReturnsCorrectObj_GivenNoStartingNumber():
    # GIVEN
    sue_nucunit = nucunit_shop()
    agendaunit_text = "agendaunit"
    pool_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    pool_attribute = "_party_credor_pool"
    pool_quarkunit.set_optional_arg(pool_attribute, 100)
    sue_nucunit.set_quarkunit(pool_quarkunit)
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_quarkunit = quarkunit_shop(category, quark_insert())
    carm_quarkunit.set_arg("party_id", carm_text)
    carm_quarkunit.set_arg("credor_weight", 70)
    sue_nucunit.set_quarkunit(carm_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_credor_pool(100)
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_insert())
    rico_quarkunit.set_arg("party_id", rico_text)
    rico_quarkunit.set_arg("credor_weight", 30)
    sue_nucunit.set_quarkunit(rico_quarkunit)

    sue_agenda = agendaunit_shop("Sue")
    assert validate_agenda_build_from_nuc(sue_nucunit, sue_agenda)

    # WHEN
    nucunit_dict = sue_nucunit.get_ordered_quarkunits()

    # THEN
    # nuc_carm = nucunit_dict.get(0)
    # nuc_rico = nucunit_dict.get(1)
    # nuc_pool = nucunit_dict.get(2)
    # assert nuc_carm == carm_quarkunit
    # assert nuc_rico == rico_quarkunit
    # assert nuc_pool == pool_quarkunit
    assert nucunit_dict.get(0) == carm_quarkunit
    assert nucunit_dict.get(1) == rico_quarkunit
    assert nucunit_dict.get(2) == pool_quarkunit


def test_NucUnit_get_ordered_quarkunits_ReturnsCorrectObj_GivenStartingNumber():
    # GIVEN
    sue_nucunit = nucunit_shop()
    agendaunit_text = "agendaunit"
    pool_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    pool_attribute = "_party_credor_pool"
    pool_quarkunit.set_optional_arg(pool_attribute, 100)
    sue_nucunit.set_quarkunit(pool_quarkunit)
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_quarkunit = quarkunit_shop(category, quark_insert())
    carm_quarkunit.set_arg("party_id", carm_text)
    carm_quarkunit.set_arg("credor_weight", 70)
    sue_nucunit.set_quarkunit(carm_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_credor_pool(100)
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_insert())
    rico_quarkunit.set_arg("party_id", rico_text)
    rico_quarkunit.set_arg("credor_weight", 30)
    sue_nucunit.set_quarkunit(rico_quarkunit)

    sue_agenda = agendaunit_shop("Sue")
    assert validate_agenda_build_from_nuc(sue_nucunit, sue_agenda)

    # WHEN
    nucunit_dict = sue_nucunit.get_ordered_quarkunits(5)

    # THEN
    # nuc_carm = nucunit_dict.get(0)
    # nuc_rico = nucunit_dict.get(1)
    # nuc_pool = nucunit_dict.get(2)
    # assert nuc_carm == carm_quarkunit
    # assert nuc_rico == rico_quarkunit
    # assert nuc_pool == pool_quarkunit
    assert nucunit_dict.get(5) == carm_quarkunit
    assert nucunit_dict.get(6) == rico_quarkunit
    assert nucunit_dict.get(7) == pool_quarkunit


def test_NucUnit_get_ordered_dict_ReturnsCorrectObj_GivenStartingNumber():
    # GIVEN
    sue_nucunit = nucunit_shop()
    agendaunit_text = "agendaunit"
    pool_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    pool_attribute = "_party_credor_pool"
    pool_quarkunit.set_optional_arg(pool_attribute, 100)
    sue_nucunit.set_quarkunit(pool_quarkunit)
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_quarkunit = quarkunit_shop(category, quark_insert())
    carm_quarkunit.set_arg("party_id", carm_text)
    carm_quarkunit.set_arg("credor_weight", 70)
    sue_nucunit.set_quarkunit(carm_quarkunit)
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.set_party_credor_pool(100)
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_insert())
    rico_quarkunit.set_arg("party_id", rico_text)
    rico_quarkunit.set_arg("credor_weight", 30)
    sue_nucunit.set_quarkunit(rico_quarkunit)

    sue_agenda = agendaunit_shop("Sue")
    assert validate_agenda_build_from_nuc(sue_nucunit, sue_agenda)

    # WHEN
    nucunit_dict = sue_nucunit.get_ordered_dict(5)

    # THEN
    # nuc_carm = nucunit_dict.get(0)
    # nuc_rico = nucunit_dict.get(1)
    # nuc_pool = nucunit_dict.get(2)
    # assert nuc_carm == carm_quarkunit
    # assert nuc_rico == rico_quarkunit
    # assert nuc_pool == pool_quarkunit
    assert nucunit_dict.get(5) == carm_quarkunit.get_dict()
    assert nucunit_dict.get(6) == rico_quarkunit.get_dict()
    assert nucunit_dict.get(7) == pool_quarkunit.get_dict()


def test_NucUnit_get_json_ReturnsCorrectObj():
    # GIVEN
    sue_nucunit = nucunit_shop()
    agendaunit_text = "agendaunit"
    pool_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    pool_attribute = "_party_credor_pool"
    pool_quarkunit.set_optional_arg(pool_attribute, 100)
    sue_nucunit.set_quarkunit(pool_quarkunit)
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_quarkunit = quarkunit_shop(category, quark_insert())
    carm_quarkunit.set_arg("party_id", carm_text)
    carm_quarkunit.set_arg("credor_weight", 70)
    sue_nucunit.set_quarkunit(carm_quarkunit)
    rico_text = "Rico"
    rico_quarkunit = quarkunit_shop(category, quark_insert())
    rico_quarkunit.set_arg("party_id", rico_text)
    rico_quarkunit.set_arg("credor_weight", 30)
    sue_nucunit.set_quarkunit(rico_quarkunit)

    # WHEN
    nuc_start_int = 5
    nucunit_json = sue_nucunit.get_json(nuc_start_int)

    # THEN
    assert x_is_json(nucunit_json)


def test_NucUnit_quarkunit_exists_ReturnsCorrectObj():
    # GIVEN
    farm_nucunit = nucunit_shop()

    # WHEN / THEN
    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_quarkunit = quarkunit_shop(category, quark_insert())
    carm_quarkunit.set_arg("party_id", carm_text)
    carm_quarkunit.set_arg("credor_weight", 70)
    assert farm_nucunit.quarkunit_exists(carm_quarkunit) is False

    # WHEN
    farm_nucunit.set_quarkunit(carm_quarkunit)

    # THEN
    assert farm_nucunit.quarkunit_exists(carm_quarkunit)
