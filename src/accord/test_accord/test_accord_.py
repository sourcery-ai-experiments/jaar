# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import (
    create_road,
    create_economyaddress,
    create_road_from_nodes as roadnodes,
)
from src.accord.topic import topicunit_shop
from src.accord.accord import AccordUnit, accordunit_shop
from src.accord.examples.example_topics import (
    get_cooking_topic,
    get_speedboats_action_topic,
    get_climate_topic,
    get_gasheater_action_topic,
)
from pytest import raises as pytest_raises


def test_AccordUnit_exists():
    # GIVEN / WHEN
    x_accordunit = AccordUnit()

    # THEN
    assert x_accordunit._author_road is None
    assert x_accordunit._reader_road is None
    assert x_accordunit._author_deltaunits is None
    assert x_accordunit._reader_deltaunits is None
    assert x_accordunit._topicunits is None
    assert x_accordunit._dueunits is None


def test_accordunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    hunger_text = "Hunger"
    ohio_text = "Ohio"
    bob_road = roadnodes([bob_text, hunger_text, yao_text, ohio_text, bob_text])
    tim_road = roadnodes([tim_text, hunger_text, yao_text, ohio_text, tim_text])

    # WHEN
    farm_accordunit = accordunit_shop(
        _author_road=bob_road,
        _reader_road=tim_road,
        _author_deltaunits=None,
        _reader_deltaunits=None,
        _topicunits=None,
        _dueunits=None,
    )

    # THEN
    assert farm_accordunit._author_road == bob_road
    assert farm_accordunit._reader_road == tim_road
    assert farm_accordunit._author_deltaunits == {}
    assert farm_accordunit._reader_deltaunits == {}
    assert farm_accordunit._topicunits == {}
    assert farm_accordunit._dueunits == {}


def test_AccordUnit_get_member_attr_CorrectlyRaisesError():
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
    farm_accordunit = accordunit_shop(
        _author_road=bob_road,
        _reader_road=tim_road,
        _author_deltaunits=None,
        _reader_deltaunits=None,
        _topicunits=None,
        _dueunits=None,
    )

    # WHEN / THEN
    person_id_text = "PersonID"
    something_text = "something"
    with pytest_raises(Exception) as excinfo:
        farm_accordunit.get_member_attr(something_text, person_id_text)
    assert (
        str(excinfo.value)
        == f"get_member_attr cannot receive '{something_text}' as member parameter."
    )


def test_AccordUnit_get_member_attr_ReturnCorrectObjs():
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
    farm_accordunit = accordunit_shop(
        _author_road=bob_road,
        _reader_road=tim_road,
        _author_deltaunits=None,
        _reader_deltaunits=None,
        _topicunits=None,
        _dueunits=None,
    )

    # WHEN / THEN
    person_id_text = "PersonID"
    problem_id_text = "ProblemID"
    healer_id_text = "HealerID"
    economy_id_text = "EconomyID"
    author_text = "author"
    reader_text = "reader"

    assert farm_accordunit.get_member_attr(author_text, person_id_text) == bob_text
    assert farm_accordunit.get_member_attr(author_text, problem_id_text) == hunger_text
    assert farm_accordunit.get_member_attr(author_text, healer_id_text) == yao_text
    assert farm_accordunit.get_member_attr(author_text, economy_id_text) == ohio_text
    assert farm_accordunit.get_member_attr(reader_text, person_id_text) == tim_text
    assert farm_accordunit.get_member_attr(reader_text, problem_id_text) == cowboy_text
    assert farm_accordunit.get_member_attr(reader_text, healer_id_text) == sue_text
    assert farm_accordunit.get_member_attr(reader_text, economy_id_text) == iowa_text
