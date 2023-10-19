from src.world.pain import ProjectLink, projectlink_shop


def test_projectlink_exists():
    # GIVEN
    diet_text = "diet"
    diet_weight = 3

    # WHEN
    diet_projectlink = ProjectLink(handle=diet_text, weight=diet_weight)

    # THEN
    assert diet_projectlink.handle == diet_text
    assert diet_projectlink.weight == diet_weight
    assert diet_projectlink._relative_weight is None
    assert diet_projectlink._person_importance is None


def test_projectlink_shop_ReturnsCorrectObj():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5

    # WHEN
    diet_projectlink = projectlink_shop(handle=diet_text, weight=diet_weight)

    # THEN
    assert diet_projectlink.handle == diet_text
    assert diet_projectlink.weight == diet_weight
    assert diet_projectlink._relative_weight is None
    assert diet_projectlink._person_importance is None


def test_projectlink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    project_text = "diet"

    # WHEN
    diet_projectlink = projectlink_shop(handle=project_text)

    # THEN
    assert diet_projectlink.handle == project_text
    assert diet_projectlink.weight == 1
    assert diet_projectlink._relative_weight is None
    assert diet_projectlink._person_importance is None


def test_projectlink_set_relative_weight_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_projectlink = projectlink_shop(handle=diet_text)
    assert diet_projectlink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    diet_projectlink.set_relative_weight(x_relative_weight)

    # THEN
    assert diet_projectlink._relative_weight == x_relative_weight


def test_projectlink_set_person_importance_SetsCorrectly():
    # GIVEN
    diet_text = "diet"
    diet_projectlink = projectlink_shop(handle=diet_text)
    assert diet_projectlink._person_importance is None

    # WHEN
    x_person_importance = 0.45
    diet_projectlink.set_person_importance(x_person_importance)

    # THEN
    assert diet_projectlink._person_importance == x_person_importance
