from src.world.pain import painunit_shop, curelink_shop, healerlink_shop


def test_curelink_set_relative_weight_SetsCorrectly():
    # GIVEN
    home_text = "home"
    home_curelink = curelink_shop(handle=home_text)
    assert home_curelink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    home_curelink.set_relative_weight(x_relative_weight)

    # THEN
    assert home_curelink._relative_weight == x_relative_weight


def test_healerunit_set_relative_weight_SetsCorrectly():
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


def test_healerunit_set_curelinks_relative_weight_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_hl = healerlink_shop(person_name=yao_text)
    fight_text = "fight"
    flee_text = "flee"
    nego_text = "negoiate"
    yao_hl.set_curelink(curelink_shop(fight_text, weight=10))
    yao_hl.set_curelink(curelink_shop(flee_text, weight=7))
    yao_hl.set_curelink(curelink_shop(nego_text, weight=3))
    fight_curelink = yao_hl.get_curelink(fight_text)
    flee_curelink = yao_hl.get_curelink(flee_text)
    nego_curelink = yao_hl.get_curelink(nego_text)
    assert fight_curelink._relative_weight is None
    assert flee_curelink._relative_weight is None
    assert nego_curelink._relative_weight is None

    # WHEN
    yao_hl.set_curelinks_relative_weight()

    # THEN
    assert fight_curelink._relative_weight == 0.5
    assert flee_curelink._relative_weight == 0.35
    assert nego_curelink._relative_weight == 0.15


def test_painunit_set_healerlinks_relative_weight_SetsCorrectly():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)

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

    # WHEN
    fear_painunit.set_healerlinks_relative_weight()

    # THEN
    assert yao_healerlink._relative_weight == 0.75
    assert sue_healerlink._relative_weight == 0.15
    assert tim_healerlink._relative_weight == 0.10
