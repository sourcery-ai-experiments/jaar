from src.world.pain import painunit_shop, healerlink_shop


def test_painunit_set_relative_weight_SetsCorrectly():
    # GIVEN
    knee_text = "knee discomfort"
    knee_painunit = painunit_shop(genus=knee_text)
    assert knee_painunit._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    knee_painunit.set_relative_weight(x_relative_weight)

    # THEN
    assert knee_painunit._relative_weight == x_relative_weight


def test_painunit_set_manager_importance_SetsCorrectly():
    # GIVEN
    knee_text = "knee discomfort"
    knee_painunit = painunit_shop(genus=knee_text)
    assert knee_painunit._manager_importance is None

    # WHEN
    x_manager_importance = 0.45
    knee_painunit.set_manager_importance(x_manager_importance)

    # THEN
    assert knee_painunit._manager_importance == x_manager_importance


def test_painunit_set_healerlinks_weight_metrics_SetsCorrectly():
    # GIVEN
    knee_text = "knee discomfort"
    knee_painunit = painunit_shop(genus=knee_text)
    knee_painunit._manager_importance = 0.25

    yao_text = "Yao"
    sue_text = "Sue"
    tim_text = "Tim"

    knee_painunit.set_healerlink(healerlink_shop(yao_text, weight=15))
    knee_painunit.set_healerlink(healerlink_shop(sue_text, weight=3))
    knee_painunit.set_healerlink(healerlink_shop(tim_text, weight=2))

    yao_healerlink = knee_painunit.get_healerlink(yao_text)
    sue_healerlink = knee_painunit.get_healerlink(sue_text)
    tim_healerlink = knee_painunit.get_healerlink(tim_text)
    assert yao_healerlink._relative_weight is None
    assert sue_healerlink._relative_weight is None
    assert tim_healerlink._relative_weight is None
    assert yao_healerlink._manager_importance is None
    assert sue_healerlink._manager_importance is None
    assert tim_healerlink._manager_importance is None

    # WHEN
    knee_painunit.set_healerlinks_weight_metrics()

    # THEN
    assert yao_healerlink._relative_weight == 0.75
    assert sue_healerlink._relative_weight == 0.15
    assert tim_healerlink._relative_weight == 0.10
    assert yao_healerlink._manager_importance == 0.1875
    assert sue_healerlink._manager_importance == 0.0375
    assert tim_healerlink._manager_importance == 0.025
