from src.world.pain import painunit_shop, fixlink_shop, healerlink_shop


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


def test_healingunit_set_relative_weight_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    assert yao_healerlink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    yao_healerlink.set_relative_weight(x_relative_weight)

    # THEN
    assert yao_healerlink._relative_weight == x_relative_weight


def test_painunit_set_relative_weight_SetsCorrectly():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    assert fear_painunit._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    fear_painunit.set_relative_weight(x_relative_weight)

    # THEN
    assert fear_painunit._relative_weight == x_relative_weight


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


def test_healingunit_set_person_importance_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    assert yao_healerlink._person_importance is None

    # WHEN
    x_person_importance = 0.45
    yao_healerlink.set_person_importance(x_person_importance)

    # THEN
    assert yao_healerlink._person_importance == x_person_importance


def test_painunit_set_person_importance_SetsCorrectly():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    assert fear_painunit._person_importance is None

    # WHEN
    x_person_importance = 0.45
    fear_painunit.set_person_importance(x_person_importance)

    # THEN
    assert fear_painunit._person_importance == x_person_importance


def test_healingunit_set_fixlinks_weight_metrics_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_hl = healerlink_shop(person_name=yao_text)
    yao_hl._person_importance = 0.25
    fight_text = "fight"
    flee_text = "flee"
    nego_text = "negoiate"
    yao_hl.set_fixlink(fixlink_shop(fight_text, weight=10))
    yao_hl.set_fixlink(fixlink_shop(flee_text, weight=7))
    yao_hl.set_fixlink(fixlink_shop(nego_text, weight=3))
    fight_fixlink = yao_hl.get_fixlink(fight_text)
    flee_fixlink = yao_hl.get_fixlink(flee_text)
    nego_fixlink = yao_hl.get_fixlink(nego_text)
    assert fight_fixlink._relative_weight is None
    assert flee_fixlink._relative_weight is None
    assert nego_fixlink._relative_weight is None
    assert fight_fixlink._person_importance is None
    assert flee_fixlink._person_importance is None
    assert nego_fixlink._person_importance is None

    # WHEN
    yao_hl.set_fixlinks_weight_metrics()

    # THEN
    assert fight_fixlink._relative_weight == 0.5
    assert flee_fixlink._relative_weight == 0.35
    assert nego_fixlink._relative_weight == 0.15
    assert fight_fixlink._person_importance == 0.125
    assert flee_fixlink._person_importance == 0.0875
    assert nego_fixlink._person_importance == 0.0375


def test_painunit_set_healerlinks_weight_metrics_SetsCorrectly():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    fear_painunit._person_importance = 0.25

    yao_text = "Yao"
    sue_text = "Sue"
    tim_text = "Tim"

    fear_painunit.set_healerlink(healerlink_shop(yao_text, weight=15))
    fear_painunit.set_healerlink(healerlink_shop(sue_text, weight=3))
    fear_painunit.set_healerlink(healerlink_shop(tim_text, weight=2))

    yao_healerlink = fear_painunit.get_healerlink(yao_text)
    sue_healerlink = fear_painunit.get_healerlink(sue_text)
    tim_healerlink = fear_painunit.get_healerlink(tim_text)
    assert yao_healerlink._relative_weight is None
    assert sue_healerlink._relative_weight is None
    assert tim_healerlink._relative_weight is None
    assert yao_healerlink._person_importance is None
    assert sue_healerlink._person_importance is None
    assert tim_healerlink._person_importance is None

    # WHEN
    fear_painunit.set_healerlinks_weight_metrics()

    # THEN
    assert yao_healerlink._relative_weight == 0.75
    assert sue_healerlink._relative_weight == 0.15
    assert tim_healerlink._relative_weight == 0.10
    assert yao_healerlink._person_importance == 0.1875
    assert sue_healerlink._person_importance == 0.0375
    assert tim_healerlink._person_importance == 0.025
