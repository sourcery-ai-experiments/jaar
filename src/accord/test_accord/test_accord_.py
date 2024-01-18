# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road, create_economyaddress
from src.accord.topic import topicunit_shop
from src.accord.accord import AccordUnit, accordunit_shop
from src.accord.examples.example_topics import (
    get_cooking_topic,
    get_speedboats_action_topic,
    get_climate_topic,
    get_gasheater_action_topic,
)


def test_AccordUnit_exists():
    # GIVEN / WHEN
    x_accordunit = AccordUnit()

    # THEN
    assert x_accordunit._author is None
    assert x_accordunit._reader is None
    assert x_accordunit._author_economyaddress is None
    assert x_accordunit._reader_economyaddress is None
    assert x_accordunit._topicunits is None
    assert x_accordunit._dueunits is None


def test_accordunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    texas_text = "Texas"
    bob_economyaddress = create_economyaddress(yao_text, texas_text)
    tim_economyaddress = create_economyaddress(yao_text, texas_text)

    # WHEN
    farm_accordunit = accordunit_shop(
        _author=bob_text,
        _reader=tim_text,
        _author_economyaddress=bob_economyaddress,
        _reader_economyaddress=tim_economyaddress,
    )

    # THEN
    assert farm_accordunit._author == bob_text
    assert farm_accordunit._reader == tim_text
    assert farm_accordunit._author_economyaddress == bob_economyaddress
    assert farm_accordunit._reader_economyaddress == tim_economyaddress
    assert farm_accordunit._topicunits == {}
    assert farm_accordunit._dueunits == {}
