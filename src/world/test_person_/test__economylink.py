from src.world.problem import EconomyLink, economylink_shop


def test_economylink_exists():
    # GIVEN
    diet_text = "diet"
    diet_weight = 3

    # WHEN
    diet_economylink = EconomyLink(economy_id=diet_text, weight=diet_weight)

    # THEN
    assert diet_economylink.economy_id == diet_text
    assert diet_economylink.weight == diet_weight
    assert diet_economylink._relative_weight is None
    assert diet_economylink._person_clout is None


def test_economylink_shop_ReturnsCorrectObj():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5

    # WHEN
    diet_economylink = economylink_shop(economy_id=diet_text, weight=diet_weight)

    # THEN
    assert diet_economylink.economy_id == diet_text
    assert diet_economylink.weight == diet_weight
    assert diet_economylink._relative_weight is None
    assert diet_economylink._person_clout is None


def test_economylink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    economy_text = "diet"

    # WHEN
    diet_economylink = economylink_shop(economy_id=economy_text)

    # THEN
    assert diet_economylink.economy_id == economy_text
    assert diet_economylink.weight == 1
    assert diet_economylink._relative_weight is None
    assert diet_economylink._person_clout is None


def test_economylink_set_relative_weight_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_economylink = economylink_shop(economy_id=diet_text)
    assert diet_economylink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    diet_economylink.set_relative_weight(x_relative_weight)

    # THEN
    assert diet_economylink._relative_weight == x_relative_weight


def test_economylink_set_person_clout_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_economylink = economylink_shop(economy_id=diet_text)
    assert diet_economylink._person_clout is None

    # WHEN
    x_person_clout = 0.45
    diet_economylink.set_person_clout(x_person_clout)

    # THEN
    assert diet_economylink._person_clout == x_person_clout
