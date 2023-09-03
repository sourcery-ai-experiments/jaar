from src.system.calendarlink import (
    calendarlink_shop,
    get_calendar_from_calendars_dirlink_from_dict,
)
from pytest import raises as pytest_raises


def test_calendarlink_exists():
    # GIVEN
    calendar_text = "test1"
    blind_text = "blind_trust"
    weight_float = 42
    # WHEN
    slx = calendarlink_shop(
        calendar_owner=calendar_text, link_type=blind_text, weight=weight_float
    )
    # THEN
    assert slx != None
    assert slx.calendar_owner == calendar_text
    assert slx.link_type == blind_text
    assert slx.weight == weight_float


def test_calendarlink_shop_ifAttrNoneAutoFill():
    # GIVEN
    calendar_text = "test1"
    blind_text = "blind_trust"

    # WHEN
    slx = calendarlink_shop(calendar_owner=calendar_text, link_type=None, weight=None)

    # THEN
    assert slx != None
    assert slx.calendar_owner == calendar_text
    assert slx.link_type == blind_text
    assert slx.weight == 1


def test_calendarlink_shop_checkAllowed_link_types():
    # GIVEN / WHEN
    calendar_text = "test1"
    blind_trust_text = "blind_trust"
    bond_filter_text = "bond_filter"
    tributary_text = "tributary"
    ignore_text = "ignore"

    link_types = {
        blind_trust_text: None,
        bond_filter_text: None,
        tributary_text: None,
        ignore_text: None,
    }

    # THEN
    # for link_type_x in link_types:
    #     print(f"{link_type_x=} assert attempted.")
    #     assert calendarlink_shop(calendar_text, link_type_x).link_type == link_type_x
    #     print(f"{link_type_x=} assert succeeded.")
    # assert calendarlink_shop(calendar_text, link_type_x).link_type == link_type_x

    calendarlink_blind_trust = calendarlink_shop(calendar_text, blind_trust_text)
    assert calendarlink_blind_trust.link_type == blind_trust_text

    calendarlink_bond_filter = calendarlink_shop(calendar_text, bond_filter_text)
    assert calendarlink_bond_filter.link_type == bond_filter_text

    calendarlink_tributary = calendarlink_shop(calendar_text, tributary_text)
    assert calendarlink_tributary.link_type == tributary_text

    calendarlink_ignore = calendarlink_shop(calendar_text, ignore_text)
    assert calendarlink_ignore.link_type == ignore_text


def test_calendarlink_shop_raisesErrorIfByTypeIsEntered():
    # GIVEN
    calendar_text = "test1"
    bad_type_text = "bad"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        calendarlink_shop(calendar_owner=calendar_text, link_type=bad_type_text)
    assert (
        str(excinfo.value)
        == f"Calendarlink '{calendar_text}' cannot have type '{bad_type_text}'."
    )


def test_calendarlink_get_dict_ReturnsDictObject():
    # GIVEN
    calendar_text = "test1"
    blind_text = "blind_trust"
    weight_float = 29
    clx = calendarlink_shop(
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


def test_get_calendar_from_calendars_dirlink_from_dict_ReturnsCalendarLinkObject():
    # GIVEN
    calendar_owner_title = "calendar_owner"
    link_type_title = "link_type"
    weight_title = "weight"

    test1_desc_text = "test1"
    test1_link_text = "blind_trust"
    test1_weight_float = 12.4

    calendarlink_dict = {
        calendar_owner_title: test1_desc_text,
        link_type_title: test1_link_text,
        weight_title: test1_weight_float,
    }

    # WHEN
    x_obj = get_calendar_from_calendars_dirlink_from_dict(x_dict=calendarlink_dict)

    # THEN
    assert x_obj.calendar_owner == test1_desc_text
    assert x_obj.link_type == test1_link_text
    assert x_obj.weight == test1_weight_float
