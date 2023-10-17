from src.world.pain import FixLink, fixlink_shop


def test_fixlink_exists():
    # GIVEN
    diet_text = "diet"
    diet_weight = 3

    # WHEN
    diet_fixlink = FixLink(handle=diet_text, weight=diet_weight)

    # THEN
    assert diet_fixlink.handle == diet_text
    assert diet_fixlink.weight == diet_weight
    assert diet_fixlink._relative_weight is None
    assert diet_fixlink._person_importance is None


def test_fixlink_shop_ReturnsCorrectObj():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5

    # WHEN
    diet_fixlink = fixlink_shop(handle=diet_text, weight=diet_weight)

    # THEN
    assert diet_fixlink.handle == diet_text
    assert diet_fixlink.weight == diet_weight
    assert diet_fixlink._relative_weight is None
    assert diet_fixlink._person_importance is None


def test_fixlink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    fix_text = "diet"

    # WHEN
    diet_fixlink = fixlink_shop(handle=fix_text)

    # THEN
    assert diet_fixlink.handle == fix_text
    assert diet_fixlink.weight == 1
    assert diet_fixlink._relative_weight is None
    assert diet_fixlink._person_importance is None


def test_fixlink_set_relative_weight_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_fixlink = fixlink_shop(handle=diet_text)
    assert diet_fixlink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    diet_fixlink.set_relative_weight(x_relative_weight)

    # THEN
    assert diet_fixlink._relative_weight == x_relative_weight


def test_fixlink_set_person_importance_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_fixlink = fixlink_shop(handle=diet_text)
    assert diet_fixlink._person_importance is None

    # WHEN
    x_person_importance = 0.45
    diet_fixlink.set_person_importance(x_person_importance)

    # THEN
    assert diet_fixlink._person_importance == x_person_importance
