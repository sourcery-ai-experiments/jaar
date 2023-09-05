from src.calendar.origin import OriginLink, originlink_shop, OriginUnit, originunit_shop
from src.calendar.member import MemberName
from pytest import raises as pytest_raises


def test_OriginLink_exists():
    # GIVEN
    roy_text = "Roy"
    roy_weight = 4

    # WHEN
    originlink_x = OriginLink(name=roy_text, weight=roy_weight)

    # THEN
    assert originlink_x.name == roy_text
    assert originlink_x.weight == roy_weight


def test_originlink_shop_ReturnsCorrectObj():
    # GIVEN
    roy_text = "Roy"
    roy_weight = 4

    # WHEN
    originlink_x = originlink_shop(name=roy_text, weight=roy_weight)

    # THEN
    assert originlink_x.name == roy_text
    assert originlink_x.weight == roy_weight


def test_originlink_shop_WeightIsNotRequired():
    # GIVEN
    roy_text = "Roy"
    # roy_name = MemberName(roy_text)

    # WHEN
    originlink_x = originlink_shop(name=roy_text)

    # THEN
    assert originlink_x.name == roy_text
    assert originlink_x.weight == 1


def test_OriginUnit_exists():
    # GIVEN / WHEN
    originunit_x = OriginUnit()

    # THEN
    assert originunit_x
    assert originunit_x._links is None


def test_originunit_ReturnsCorrectObj():
    # GIVEN / WHEN
    originunit_x = originunit_shop()

    # THEN
    assert originunit_x._links == {}


def test_originunit__set_originlinks_empty_if_null_CorrectlySetsAttribute():
    # GIVEN
    originunit_x = originunit_shop()
    originunit_x._links = None
    assert originunit_x._links is None

    # WHEN
    originunit_x._set_originlinks_empty_if_null()

    # THEN
    assert originunit_x._links == {}


def test_originunit_set_originlink_CorrectlySetsOriginLink():
    # GIVEN
    originunit_x = originunit_shop()

    # WHEN
    tim_text = "tim"
    tim_weight = 3
    originunit_x.set_originlink(name=tim_text, weight=tim_weight)

    # THEN
    assert originunit_x._links.get(tim_text) != None
    assert originunit_x._links.get(tim_text).name == tim_text
    assert originunit_x._links.get(tim_text).weight == tim_weight


def test_originunit_del_originlink_CorrectlyDeletesOriginLink():
    # GIVEN
    originunit_x = originunit_shop()
    tim_text = "tim"
    tim_weight = 3
    originunit_x.set_originlink(name=tim_text, weight=tim_weight)
    assert originunit_x._links.get(tim_text) != None
    assert originunit_x._links.get(tim_text).name == tim_text

    # WHEN
    originunit_x.del_originlink(name=tim_text)

    # THEN
    assert originunit_x._links.get(tim_text) is None
