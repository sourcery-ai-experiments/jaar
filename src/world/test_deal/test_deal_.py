from src._prime.road import create_road_from_nodes as roadnodes
from src.world.deal import DealUnit, dealunit_shop
from pytest import raises as pytest_raises


def test_DealUnit_exists():
    # GIVEN / WHEN
    x_dealunit = DealUnit()

    # THEN
    assert x_dealunit._author_road is None
    assert x_dealunit._reader_road is None
    assert x_dealunit._topicunits is None
    assert x_dealunit._vowunits is None


def test_dealunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    hunger_text = "Hunger"
    ohio_text = "Ohio"
    bob_road = roadnodes([bob_text, hunger_text, yao_text, ohio_text, bob_text])
    tim_road = roadnodes([tim_text, hunger_text, yao_text, ohio_text, tim_text])

    # WHEN
    farm_dealunit = dealunit_shop(
        _author_road=bob_road,
        _reader_road=tim_road,
        _topicunits=None,
        _vowunits=None,
    )

    # THEN
    assert farm_dealunit._author_road == bob_road
    assert farm_dealunit._reader_road == tim_road
    assert farm_dealunit._topicunits == {}
    assert farm_dealunit._vowunits == {}


def test_DealUnit_get_member_attr_CorrectlyRaisesError():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    sue_text = "Sue"
    hunger_text = "Hunger"
    cowboy_text = "Cowboy"
    ohio_text = "Ohio"
    iowa_text = "Iowa"
    bob_road = roadnodes([bob_text, hunger_text, yao_text, ohio_text, bob_text])
    tim_road = roadnodes([tim_text, cowboy_text, sue_text, iowa_text, tim_text])
    farm_dealunit = dealunit_shop(_author_road=bob_road, _reader_road=tim_road)

    # WHEN / THEN
    person_id_text = "PersonID"
    something_text = "something"
    with pytest_raises(Exception) as excinfo:
        farm_dealunit.get_member_attr(something_text, person_id_text)
    assert (
        str(excinfo.value)
        == f"get_member_attr cannot receive '{something_text}' as member parameter."
    )


def test_DealUnit_get_member_attr_ReturnCorrectObjs():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    sue_text = "Sue"
    hunger_text = "Hunger"
    cowboy_text = "Cowboy"
    ohio_text = "Ohio"
    iowa_text = "Iowa"
    bob_road = roadnodes([bob_text, hunger_text, yao_text, ohio_text, bob_text])
    tim_road = roadnodes([tim_text, cowboy_text, sue_text, iowa_text, tim_text])
    farm_dealunit = dealunit_shop(_author_road=bob_road, _reader_road=tim_road)

    # WHEN / THEN
    person_id_text = "PersonID"
    problem_id_text = "ProblemID"
    healer_id_text = "HealerID"
    market_id_text = "MarketID"
    author_text = "author"
    reader_text = "reader"

    assert farm_dealunit.get_member_attr(author_text, person_id_text) == bob_text
    assert farm_dealunit.get_member_attr(author_text, problem_id_text) == hunger_text
    assert farm_dealunit.get_member_attr(author_text, healer_id_text) == yao_text
    assert farm_dealunit.get_member_attr(author_text, market_id_text) == ohio_text
    assert farm_dealunit.get_member_attr(reader_text, person_id_text) == tim_text
    assert farm_dealunit.get_member_attr(reader_text, problem_id_text) == cowboy_text
    assert farm_dealunit.get_member_attr(reader_text, healer_id_text) == sue_text
    assert farm_dealunit.get_member_attr(reader_text, market_id_text) == iowa_text
