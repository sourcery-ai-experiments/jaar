from src._truth.other import otherunit_shop
from src.atom.quark import QuarkUnit, quarkunit_shop, quark_insert, quark_delete


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
    bob_otherunit = otherunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    cw_text = "_credor_weight"
    dw_text = "_debtor_weight"
    bob_required_dict = {"other_id": "huh"}
    bob_optional_dict = {cw_text: bob_otherunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_otherunit.get_dict().get(dw_text)
    otherunit_text = "truth_otherunit"

    # WHEN
    x_quarkunit = quarkunit_shop(
        category=otherunit_text,
        crud_text=quark_insert(),
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )

    # THEN
    print(f"{x_quarkunit=}")
    assert x_quarkunit.category == otherunit_text
    assert x_quarkunit.crud_text == quark_insert()
    assert x_quarkunit.required_args == bob_required_dict
    assert x_quarkunit.optional_args == bob_optional_dict


def test_QuarkUnit_set_required_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    otherunit_text = "truth_otherunit"
    otherunit_quarkunit = quarkunit_shop(otherunit_text, quark_insert())
    assert otherunit_quarkunit.required_args == {}

    # WHEN
    other_id_text = "other_id"
    otherunit_quarkunit.set_required_arg(x_key=other_id_text, x_value=bob_text)

    # THEN
    assert otherunit_quarkunit.required_args == {other_id_text: bob_text}


def test_QuarkUnit_set_optional_arg_CorrectlySetsAttr():
    # GIVEN
    bob_text = "Bob"
    otherunit_text = "truth_otherunit"
    otherunit_quarkunit = quarkunit_shop(otherunit_text, quark_insert())
    assert otherunit_quarkunit.optional_args == {}

    # WHEN
    other_id_text = "other_id"
    otherunit_quarkunit.set_optional_arg(x_key=other_id_text, x_value=bob_text)

    # THEN
    assert otherunit_quarkunit.optional_args == {other_id_text: bob_text}


def test_QuarkUnit_get_value_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    otherunit_text = "truth_otherunit"
    otherunit_quarkunit = quarkunit_shop(otherunit_text, quark_insert())
    other_id_text = "other_id"
    otherunit_quarkunit.set_required_arg(x_key=other_id_text, x_value=bob_text)

    # WHEN / THEN
    assert otherunit_quarkunit.get_value(other_id_text) == bob_text


def test_QuarkUnit_is_optional_args_valid_ReturnsCorrectBoolean():
    # WHEN
    otherunit_text = "truth_otherunit"
    bob_insert_quarkunit = quarkunit_shop(otherunit_text, crud_text=quark_insert())
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


def test_QuarkUnit_is_valid_ReturnsCorrectBoolean_OtherUnit_INSERT():
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    bob_otherunit = otherunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    otherunit_text = "truth_otherunit"

    # WHEN
    bob_insert_quarkunit = quarkunit_shop(otherunit_text, crud_text=quark_insert())

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
    other_id_text = "other_id"
    bob_insert_quarkunit.set_required_arg(other_id_text, bob_text)

    # THEN
    assert bob_insert_quarkunit.is_required_args_valid()
    assert bob_insert_quarkunit.is_optional_args_valid() is False
    assert bob_insert_quarkunit.is_valid() is False

    # WHEN
    bob_insert_quarkunit.optional_args = {}
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    bob_insert_quarkunit.set_optional_arg(
        cw_text, bob_otherunit.get_dict().get(cw_text)
    )
    bob_insert_quarkunit.set_optional_arg(
        dw_text, bob_otherunit.get_dict().get(dw_text)
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
    bob_otherunit = otherunit_shop(bob_text, bob_credor_weight, bob_debtor_weight)
    otherunit_text = "truth_otherunit"
    bob_insert_quarkunit = quarkunit_shop(otherunit_text, quark_insert())
    other_id_text = "other_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_otherunit.get_dict()=}")
    # bob_otherunit_dict = {other_id_text: bob_otherunit.get_dict().get(other_id_text)}
    # print(f"{bob_otherunit_dict=}")
    bob_insert_quarkunit.set_required_arg(other_id_text, bob_text)
    bob_insert_quarkunit.set_optional_arg(
        cw_text, bob_otherunit.get_dict().get(cw_text)
    )
    bob_insert_quarkunit.set_optional_arg(
        dw_text, bob_otherunit.get_dict().get(dw_text)
    )
    assert bob_insert_quarkunit.is_valid()

    # WHEN / THEN
    assert bob_insert_quarkunit.get_value(cw_text) == bob_credor_weight
    assert bob_insert_quarkunit.get_value(dw_text) == bob_debtor_weight


def test_QuarkUnit_is_valid_ReturnsCorrectBoolean_OtherUnit_DELETE():
    bob_text = "Bob"
    otherunit_text = "truth_otherunit"
    delete_text = quark_delete()

    # WHEN
    bob_delete_quarkunit = quarkunit_shop(otherunit_text, crud_text=delete_text)

    # THEN
    assert bob_delete_quarkunit.is_required_args_valid() is False
    assert bob_delete_quarkunit.is_valid() is False

    # WHEN
    bob_delete_quarkunit.set_required_arg("other_id", bob_text)

    # THEN
    assert bob_delete_quarkunit.is_required_args_valid()
    assert bob_delete_quarkunit.is_valid()


def test_QuarkUnit_set_quark_order_SetCorrectAttr():
    # GIVEN
    bob_text = "Bob"
    bob_credor_weight = 55
    bob_debtor_weight = 66
    otherunit_text = "truth_otherunit"
    bob_insert_quarkunit = quarkunit_shop(otherunit_text, quark_insert())
    other_id_text = "other_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"
    bob_insert_quarkunit.set_required_arg(other_id_text, bob_text)
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
    otherunit_text = "truth_otherunit"
    bob_insert_quarkunit = quarkunit_shop(otherunit_text, quark_insert())
    other_id_text = "other_id"
    cw_text = "credor_weight"
    dw_text = "debtor_weight"

    # WHEN
    bob_insert_quarkunit.set_arg(other_id_text, bob_text)
    bob_insert_quarkunit.set_arg(cw_text, bob_credor_weight)
    bob_insert_quarkunit.set_arg(dw_text, bob_debtor_weight)

    # THEN
    assert bob_insert_quarkunit.get_value(other_id_text) == bob_text
    assert bob_insert_quarkunit.get_value(cw_text) == bob_credor_weight
    assert bob_insert_quarkunit.get_value(dw_text) == bob_debtor_weight
    assert bob_insert_quarkunit.get_value(other_id_text) == bob_text
    assert bob_insert_quarkunit.is_valid()
