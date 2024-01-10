from src.world.problem import HealerLink, healerlink_shop


def test_healerlink_exists():
    # GIVEN
    yao_text = "yao"
    yao_weight = 3
    yao_in_tribe = True

    # WHEN
    yao_healerlink = HealerLink(person_id=yao_text, weight=3, in_tribe=yao_in_tribe)

    # THEN
    assert yao_healerlink.person_id == yao_text
    assert yao_healerlink.weight == yao_weight
    assert yao_healerlink.in_tribe == yao_in_tribe
    assert yao_healerlink._economylinks is None
    assert yao_healerlink._relative_weight is None
    assert yao_healerlink._manager_importance is None


def test_healerlink_shop_ReturnsCorrectObj():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_in_tribe = False

    # WHEN
    yao_healerlink = healerlink_shop(
        person_id=yao_text, weight=yao_weight, in_tribe=yao_in_tribe
    )

    # THEN
    assert yao_healerlink.person_id == yao_text
    assert yao_healerlink.weight == yao_weight
    assert yao_healerlink.in_tribe == yao_in_tribe
    assert yao_healerlink._economylinks == {}
    assert yao_healerlink._relative_weight is None
    assert yao_healerlink._manager_importance is None


def test_healerlink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    yao_text = "yao"

    # WHEN
    yao_healerlink = healerlink_shop(person_id=yao_text)

    # THEN
    assert yao_healerlink.person_id == yao_text
    assert yao_healerlink.weight == 1
    assert yao_healerlink.in_tribe is None
    assert yao_healerlink._economylinks == {}
    assert yao_healerlink._relative_weight is None
    assert yao_healerlink._manager_importance is None


def test_healerlink_set_relative_weight_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_healerlink = healerlink_shop(person_id=yao_text)
    assert yao_healerlink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    yao_healerlink.set_relative_weight(x_relative_weight)

    # THEN
    assert yao_healerlink._relative_weight == x_relative_weight


def test_healerlink_set_manager_importance_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_healerlink = healerlink_shop(person_id=yao_text)
    assert yao_healerlink._manager_importance is None

    # WHEN
    x_manager_importance = 0.45
    yao_healerlink.set_manager_importance(x_manager_importance)

    # THEN
    assert yao_healerlink._manager_importance == x_manager_importance
