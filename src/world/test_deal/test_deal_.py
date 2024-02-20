from src._road.road import create_road_from_nodes as roadnodes
from src.agenda.atom import bookunit_shop
from src.world.deal import DealUnit, dealunit_shop
from pytest import raises as pytest_raises


def test_DealUnit_exists():
    # GIVEN / WHEN
    x_dealunit = DealUnit()

    # THEN
    assert x_dealunit._author is None
    assert x_dealunit._signers is None
    assert x_dealunit._like is None
    assert x_dealunit._topicunits is None


def test_dealunit_shop_ReturnsCorrectObjGivenEmptyArgs():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    farm_dealunit = dealunit_shop(_author=bob_text)

    # THEN
    assert farm_dealunit._author == bob_text
    assert farm_dealunit._signers == set()
    assert farm_dealunit._like == bookunit_shop()
    assert farm_dealunit._topicunits == {}


def test_dealunit_shop_ReturnsCorrectObjGivenSomeArgs_v1():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    x_signors = {bob_text, tim_text, yao_text}

    # WHEN
    farm_dealunit = dealunit_shop(
        _author=bob_text,
        _signers=x_signors,
        _like=None,
        _topicunits=None,
    )

    # THEN
    assert farm_dealunit._author == bob_text
    assert farm_dealunit._signers == x_signors
    assert farm_dealunit._topicunits == {}


# def test_DealUnit_get_member_attr_CorrectlyRaisesError():
#     # GIVEN
#     bob_text = "Bob"
#     tim_text = "Tim"
#     yao_text = "Yao"
#     sue_text = "Sue"
#     hunger_text = "Hunger"
#     cowboy_text = "Cowboy"
#     ohio_text = "Ohio"
#     iowa_text = "Iowa"
#     farm_dealunit = dealunit_shop(_author=bob_text)

#     # WHEN / THEN
#     person_id_text = "PersonID"
#     something_text = "something"
#     with pytest_raises(Exception) as excinfo:
#         farm_dealunit.get_member_attr(something_text, person_id_text)
#     assert (
#         str(excinfo.value)
#         == f"get_member_attr cannot receive '{something_text}' as member parameter."
#     )
