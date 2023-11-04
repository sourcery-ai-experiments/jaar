from src.world.pain import CultureLink, culturelink_shop


def test_culturelink_exists():
    # GIVEN
    diet_text = "diet"
    diet_weight = 3

    # WHEN
    diet_culturelink = CultureLink(title=diet_text, weight=diet_weight)

    # THEN
    assert diet_culturelink.title == diet_text
    assert diet_culturelink.weight == diet_weight
    assert diet_culturelink._relative_weight is None
    assert diet_culturelink._manager_importance is None


def test_culturelink_shop_ReturnsCorrectObj():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5

    # WHEN
    diet_culturelink = culturelink_shop(title=diet_text, weight=diet_weight)

    # THEN
    assert diet_culturelink.title == diet_text
    assert diet_culturelink.weight == diet_weight
    assert diet_culturelink._relative_weight is None
    assert diet_culturelink._manager_importance is None


def test_culturelink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    culture_text = "diet"

    # WHEN
    diet_culturelink = culturelink_shop(title=culture_text)

    # THEN
    assert diet_culturelink.title == culture_text
    assert diet_culturelink.weight == 1
    assert diet_culturelink._relative_weight is None
    assert diet_culturelink._manager_importance is None


def test_culturelink_set_relative_weight_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_culturelink = culturelink_shop(title=diet_text)
    assert diet_culturelink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    diet_culturelink.set_relative_weight(x_relative_weight)

    # THEN
    assert diet_culturelink._relative_weight == x_relative_weight


def test_culturelink_set_manager_importance_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_culturelink = culturelink_shop(title=diet_text)
    assert diet_culturelink._manager_importance is None

    # WHEN
    x_manager_importance = 0.45
    diet_culturelink.set_manager_importance(x_manager_importance)

    # THEN
    assert diet_culturelink._manager_importance == x_manager_importance
