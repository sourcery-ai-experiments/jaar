from src.x_econ.problem import MarketLink, marketlink_shop


def test_marketlink_exists():
    # GIVEN
    diet_text = "diet"
    diet_weight = 3

    # WHEN
    diet_marketlink = MarketLink(market_id=diet_text, weight=diet_weight)

    # THEN
    assert diet_marketlink.market_id == diet_text
    assert diet_marketlink.weight == diet_weight
    assert diet_marketlink._relative_weight is None
    assert diet_marketlink._person_clout is None


def test_marketlink_shop_ReturnsCorrectObj():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5

    # WHEN
    diet_marketlink = marketlink_shop(market_id=diet_text, weight=diet_weight)

    # THEN
    assert diet_marketlink.market_id == diet_text
    assert diet_marketlink.weight == diet_weight
    assert diet_marketlink._relative_weight is None
    assert diet_marketlink._person_clout is None


def test_marketlink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    market_text = "diet"

    # WHEN
    diet_marketlink = marketlink_shop(market_id=market_text)

    # THEN
    assert diet_marketlink.market_id == market_text
    assert diet_marketlink.weight == 1
    assert diet_marketlink._relative_weight is None
    assert diet_marketlink._person_clout is None


def test_marketlink_set_relative_weight_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_marketlink = marketlink_shop(market_id=diet_text)
    assert diet_marketlink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    diet_marketlink.set_relative_weight(x_relative_weight)

    # THEN
    assert diet_marketlink._relative_weight == x_relative_weight


def test_marketlink_set_person_clout_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_marketlink = marketlink_shop(market_id=diet_text)
    assert diet_marketlink._person_clout is None

    # WHEN
    x_person_clout = 0.45
    diet_marketlink.set_person_clout(x_person_clout)

    # THEN
    assert diet_marketlink._person_clout == x_person_clout
