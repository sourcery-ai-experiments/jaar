from src._road.road import create_road_from_nodes as roadnodes
from src.agenda.atom import bookunit_shop
from src.world.gift import GiftUnit, giftunit_shop
from pytest import raises as pytest_raises


def test_GiftUnit_exists():
    # GIVEN / WHEN
    x_giftunit = GiftUnit()

    # THEN
    assert x_giftunit._author is None
    assert x_giftunit._signers is None
    assert x_giftunit._like is None


def test_giftunit_shop_ReturnsCorrectObjGivenEmptyArgs():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    farm_giftunit = giftunit_shop(_author=bob_text)

    # THEN
    assert farm_giftunit._author == bob_text
    assert farm_giftunit._signers == set()
    assert farm_giftunit._like == bookunit_shop()


def test_giftunit_shop_ReturnsCorrectObjGivenSomeArgs_v1():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    x_signers = {bob_text, tim_text, yao_text}

    # WHEN
    farm_giftunit = giftunit_shop(
        _author=bob_text,
        _signers=x_signers,
        _like=None,
    )

    # THEN
    assert farm_giftunit._author == bob_text
    assert farm_giftunit._signers == x_signers


# def test_GiftUnit_get_member_attr_CorrectlyRaisesError():
#     # GIVEN
#     bob_text = "Bob"
#     tim_text = "Tim"
#     yao_text = "Yao"
#     sue_text = "Sue"
#     hunger_text = "Hunger"
#     cowboy_text = "Cowboy"
#     ohio_text = "Ohio"
#     iowa_text = "Iowa"
#     farm_giftunit = giftunit_shop(_author=bob_text)

#     # WHEN / THEN
#     person_id_text = "PersonID"
#     something_text = "something"
#     with pytest_raises(Exception) as excinfo:
#         farm_giftunit.get_member_attr(something_text, person_id_text)
#     assert (
#         str(excinfo.value)
#         == f"get_member_attr cannot receive '{something_text}' as member parameter."
#     )
