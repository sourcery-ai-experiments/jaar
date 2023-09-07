from src.system.depotlink import (
    depotlink_shop,
    get_depotlink_from_dict,
)
from pytest import raises as pytest_raises


def test_depotlink_exists():
    # GIVEN
    calendar_text = "test1"
    blind_text = "blind_trust"
    weight_float = 42
    # WHEN
    slx = depotlink_shop(
        calendar_owner=calendar_text, link_type=blind_text, weight=weight_float
    )
    # THEN
    assert slx != None
    assert slx.calendar_owner == calendar_text
    assert slx.link_type == blind_text
    assert slx.weight == weight_float


def test_depotlink_shop_ifAttrNoneAutoFill():
    # GIVEN
    calendar_text = "test1"
    blind_text = "blind_trust"

    # WHEN
    slx = depotlink_shop(calendar_owner=calendar_text, link_type=None, weight=None)

    # THEN
    assert slx != None
    assert slx.calendar_owner == calendar_text
    assert slx.link_type == blind_text
    assert slx.weight == 1


def test_depotlink_shop_checkAllowed_depotlink_types():
    # GIVEN / WHEN
    calendar_text = "test1"
    blind_trust_text = "blind_trust"
    bond_filter_text = "bond_filter"
    tributary_text = "tributary"
    ignore_text = "ignore"

    # depotlink_types = {
    #     blind_trust_text: None,
    #     bond_filter_text: None,
    #     tributary_text: None,
    #     ignore_text: None,
    # }

    # THEN
    # for depotlink_type_x in depotlink_types:
    #     print(f"{depotlink_type_x=} assert attempted.")
    #     assert depotlink_shop(calendar_text, depotlink_type_x).depotlink_type == depotlink_type_x
    #     print(f"{depotlink_type_x=} assert succeeded.")
    # assert depotlink_shop(calendar_text, depotlink_type_x).depotlink_type == depotlink_type_x

    depotlink_blind_trust = depotlink_shop(calendar_text, blind_trust_text)
    assert depotlink_blind_trust.link_type == blind_trust_text

    depotlink_bond_filter = depotlink_shop(calendar_text, bond_filter_text)
    assert depotlink_bond_filter.link_type == bond_filter_text

    depotlink_tributary = depotlink_shop(calendar_text, tributary_text)
    assert depotlink_tributary.link_type == tributary_text

    depotlink_ignore = depotlink_shop(calendar_text, ignore_text)
    assert depotlink_ignore.link_type == ignore_text


def test_depotlink_shop_raisesErrorIfByTypeIsEntered():
    # GIVEN
    calendar_text = "test1"
    bad_type_text = "bad"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        depotlink_shop(calendar_owner=calendar_text, link_type=bad_type_text)
    assert (
        str(excinfo.value)
        == f"Calendarlink '{calendar_text}' cannot have type '{bad_type_text}'."
    )


def test_depotlink_get_dict_ReturnsDictObject():
    # GIVEN
    calendar_text = "test1"
    blind_text = "blind_trust"
    weight_float = 29
    clx = depotlink_shop(
        calendar_owner=calendar_text, link_type=blind_text, weight=weight_float
    )

    # WHEN
    x_dict = clx.get_dict()

    # THEN
    assert x_dict == {
        "calendar_owner": calendar_text,
        "link_type": blind_text,
        "weight": weight_float,
    }


def test_get_depotlink_from_dict_ReturnsCalendarLinkObject():
    # GIVEN
    calendar_owner_text = "calendar_owner"
    link_type_text = "link_type"
    weight_text = "weight"

    test1_label_text = "test1"
    test1_link_text = "blind_trust"
    test1_weight_float = 12.4

    depotlink_dict = {
        calendar_owner_text: test1_label_text,
        link_type_text: test1_link_text,
        weight_text: test1_weight_float,
    }

    # WHEN
    x_obj = get_depotlink_from_dict(x_dict=depotlink_dict)

    # THEN
    assert x_obj.calendar_owner == test1_label_text
    assert x_obj.link_type == test1_link_text
    assert x_obj.weight == test1_weight_float
