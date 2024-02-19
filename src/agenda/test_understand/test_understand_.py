from src.agenda.party import partyunit_shop
from src.agenda.understand import (
    UnderstandUnit,
    understandunit_shop,
    learnunit_shop,
    learn_update,
    learn_insert,
    learn_delete,
)
from src.agenda.examples.example_understands import get_sue_understandunit_example1
from pytest import raises as pytest_raises


def test_UnderstandUnit_exists():
    # GIVEN / WHEN
    x_understandunit = UnderstandUnit()

    # THEN
    assert x_understandunit.learnunits is None


def test_understandunit_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    sue_understandunit = understandunit_shop()

    # THEN
    assert sue_understandunit.learnunits == {}


def test_UnderstandUnit_set_learnunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_understandunit = understandunit_shop()
    attribute_value = 55
    category = "agendaunit"
    opt1_arg = "_weight"
    optional_args = {opt1_arg: attribute_value}
    required_args = {}
    agenda_weight_learnunit = learnunit_shop(
        category,
        learn_update(),
        required_args=required_args,
        optional_args=optional_args,
    )
    assert sue_understandunit.learnunits == {}
    assert agenda_weight_learnunit.learn_order is None

    # WHEN
    sue_understandunit.set_learnunit(agenda_weight_learnunit)

    # THEN
    assert len(sue_understandunit.learnunits) == 1
    x_update_dict = sue_understandunit.learnunits.get(learn_update())
    # print(f"{x_update_dict=}")
    x_category_learnunit = x_update_dict.get(category)
    print(f"{x_category_learnunit=}")
    assert x_category_learnunit == agenda_weight_learnunit
    assert agenda_weight_learnunit.learn_order != None


def test_UnderstandUnit_set_learnunit_RaisesErrorWhen_is_valid_IsFalse():
    # GIVEN
    sue_understandunit = understandunit_shop()
    x_category = "groupunit"
    agenda_weight_learnunit = learnunit_shop(x_category, learn_update())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_understandunit.set_learnunit(agenda_weight_learnunit)
    assert (
        str(excinfo.value)
        == f"""'{x_category}' UPDATE LearnUnit is invalid
                x_learnunit.is_locator_valid()=False
                x_learnunit.is_required_args_valid()=False
                x_learnunit.is_optional_args_valid()=True"""
    )


def test_UnderstandUnit_get_learn_ReturnsCorrectObj():
    # GIVEN
    sue_understandunit = understandunit_shop()
    agendaunit_text = "agendaunit"
    opt_arg1 = "_weight"
    opt_value = 55
    agendaunit_learnunit = learnunit_shop(agendaunit_text, learn_update())
    agendaunit_learnunit.set_optional_arg(x_key=opt_arg1, x_value=opt_value)
    sue_understandunit.set_learnunit(agendaunit_learnunit)

    # WHEN
    gen_learnunit = sue_understandunit.get_learnunit(
        learn_update(), category=agendaunit_text, locator_values=[]
    )

    # THEN
    assert gen_learnunit == agendaunit_learnunit


def test_UnderstandUnit_add_learnunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_understandunit = understandunit_shop()
    assert sue_understandunit.learnunits == {}

    # WHEN
    op2_arg = "_weight"
    op2_value = 55
    agendaunit_text = "agendaunit"
    required_args = {}
    optional_args = {op2_arg: op2_value}
    sue_understandunit.add_learnunit(
        agendaunit_text,
        learn_update(),
        None,
        required_args,
        optional_args=optional_args,
    )

    # THEN
    assert len(sue_understandunit.learnunits) == 1
    x_update_dict = sue_understandunit.learnunits.get(learn_update())
    x_learnunit = x_update_dict.get(agendaunit_text)
    assert x_learnunit != None
    assert x_learnunit.category == agendaunit_text


def test_UnderstandUnit_add_learnunit_CorrectlySets_AgendaUnit_partyunits():
    # GIVEN
    sue_understandunit = understandunit_shop()
    assert sue_understandunit.learnunits == {}

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
    sue_understandunit.add_learnunit(
        category=partyunit_text,
        crud_text=learn_insert(),
        locator=bob_locator_dict,
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )
    # THEN
    assert len(sue_understandunit.learnunits) == 1
    bob_locator_key = f"{partyunit_text} {bob_text}"
    assert (
        sue_understandunit.learnunits.get(learn_insert())
        .get(partyunit_text)
        .get(bob_text)
        != None
    )


# def test_UnderstandUnit_add_learnunit_CorrectlySets_AgendaUnit_max_tree_traverse():
#     # GIVEN
#     sue_understandunit = understandunit_shop(get_sue_road())
#     assert sue_understandunit.learnunits == {}

#     # WHEN
#     opt2_value = 55
#     category = "agendaunit"
#     opt2_arg = "_weight"
#     weight_learnunit = learnunit_shop(category, learn_update())
#     weight_learnunit.set_optional_arg(opt2_arg, opt2_value)
#     sue_understandunit.set_learnunit(weight_learnunit)
#     # THEN
#     assert len(sue_understandunit.learnunits.get(learn_update()).keys()) == 1
#     sue_agendaunit_dict = sue_understandunit.learnunits.get(learn_update())
#     sue_weight_learnunit = sue_agendaunit_dict.get(category)
#     print(f"{sue_weight_learnunit=}")
#     assert weight_learnunit == sue_weight_learnunit

#     # WHEN
#     new2_value = 66
#     x_attribute = "_max_tree_traverse"
#     required_args = {x_attribute: new2_value}
#     x_learnunit = learnunit_shop(x_attribute, learn_update(), None, required_args)
#     sue_understandunit.set_learnunit(x_learnunit)
#     # THEN
#     print(f"{sue_understandunit.learnunits.keys()=}")
#     print(f"{sue_understandunit.learnunits.get(learn_update()).keys()=}")
#     # print(f"{get_all_nondictionary_objs(sue_understandunit.learnunits).get(learn_update())=}")
#     assert len(sue_understandunit.learnunits.get(learn_update()).keys()) == 2
#     assert x_learnunit == sue_understandunit.learnunits.get(learn_update()).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = "_party_creditor_pool"
#     required_args = {x_attribute: new3_value}
#     x_learnunit = learnunit_shop(x_attribute, learn_update(), None, required_args)
#     sue_understandunit.set_learnunit(x_learnunit)
#     # THEN
#     assert len(sue_understandunit.learnunits.get(learn_update()).keys()) == 3
#     assert x_learnunit == sue_understandunit.learnunits.get(learn_update()).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "_party_debtor_pool"
#     required_args = {x_attribute: new4_value}
#     x_learnunit = learnunit_shop(x_attribute, learn_update(), None, required_args)
#     sue_understandunit.set_learnunit(x_learnunit)
#     # THEN
#     assert len(sue_understandunit.learnunits.get(learn_update()).keys()) == 4
#     assert x_learnunit == sue_understandunit.learnunits.get(learn_update()).get(x_attribute)

#     # WHEN
#     new5_value = "override"
#     x_attribute = "_meld_strategy"
#     required_args = {x_attribute: new5_value}
#     x_learnunit = learnunit_shop(x_attribute, learn_update(), None, required_args)
#     sue_understandunit.set_learnunit(x_learnunit)
#     # THEN
#     assert len(sue_understandunit.learnunits.get(learn_update()).keys()) == 5
#     assert x_learnunit == sue_understandunit.learnunits.get(learn_update()).get(x_attribute)


def test_UnderstandUnit_get_learn_order_learnunit_dict_ReturnsCorrectObj():
    # GIVEN
    sue_understandunit = get_sue_understandunit_example1()
    assert len(sue_understandunit.learnunits.get(learn_update()).keys()) == 1
    assert sue_understandunit.learnunits.get(learn_insert()) is None
    assert len(sue_understandunit.learnunits.get(learn_delete()).keys()) == 1

    # WHEN
    sue_learn_order_dict = sue_understandunit.get_learn_order_learnunit_dict()

    # THEN
    assert len(sue_learn_order_dict) == 2
    print(f"{sue_learn_order_dict.keys()=}")
    print(f"{sue_learn_order_dict.get(learn_update())=}")
    assert len(sue_learn_order_dict.get(learn_update())) == 1
    assert len(sue_learn_order_dict.get(learn_delete())) == 1
