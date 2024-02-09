from src.world.problem import marketlink_shop, healerlink_shop


def test_HealerLink_set_marketlink_CorrectlySetsObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)

    # WHEN
    diet_text = "diet"
    diet_marketlink = marketlink_shop(market_id=diet_text)
    yao_healerlink.set_marketlink(diet_marketlink)

    # THEN
    # diet_market = yao_problem.get_market()
    diet_market = yao_healerlink._marketlinks.get(diet_text)
    assert diet_market != None
    assert diet_market.market_id == diet_text


def test_HealerLink_get_marketunit_CorrectlyGetsObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    diet_text = "diet"
    diet_marketlink = marketlink_shop(market_id=diet_text)
    yao_healerlink.set_marketlink(diet_marketlink)

    # WHEN
    diet_market = yao_healerlink.get_marketlink(diet_text)

    # THEN
    assert diet_market != None
    assert diet_market.market_id == diet_text


def test_HealerLink_del_marketunit_CorrectlyDeletesObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    diet_text = "diet"
    diet_marketlink = marketlink_shop(market_id=diet_text)
    yao_healerlink.set_marketlink(diet_marketlink)
    diet_market = yao_healerlink.get_marketlink(diet_text)
    assert diet_market != None
    assert diet_market.market_id == diet_text

    # WHEN
    yao_healerlink.del_marketlink(market_id=diet_text)

    # THEN
    after_diet_market = yao_healerlink.get_marketlink(diet_text)
    assert after_diet_market is None


def test_HealerLink_marketlink_exists_ReturnsCorrectObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    ohio_text = "Ohio"
    yao_healerlink.set_marketlink(marketlink_shop(market_id=ohio_text))

    # WHEN / THEN
    diet_text = "diet"
    assert len(yao_healerlink._marketlinks) != 0
    assert yao_healerlink.marketlink_exists(diet_text) == False

    # WHEN / THEN
    yao_healerlink.set_marketlink(marketlink_shop(market_id=diet_text))
    assert len(yao_healerlink._marketlinks) != 0
    assert yao_healerlink.marketlink_exists(diet_text)

    # WHEN / THEN
    yao_healerlink.del_marketlink(diet_text)
    assert len(yao_healerlink._marketlinks) != 0
    assert yao_healerlink.marketlink_exists(diet_text) == False


def test_HealerLink_set_marketlinks_weight_metrics_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_hl = healerlink_shop(healer_id=yao_text)
    yao_hl._person_clout = 0.25
    fight_text = "fight"
    flee_text = "flee"
    nego_text = "negoiate"
    yao_hl.set_marketlink(marketlink_shop(fight_text, weight=10))
    yao_hl.set_marketlink(marketlink_shop(flee_text, weight=7))
    yao_hl.set_marketlink(marketlink_shop(nego_text, weight=3))
    fight_marketlink = yao_hl.get_marketlink(fight_text)
    flee_marketlink = yao_hl.get_marketlink(flee_text)
    nego_marketlink = yao_hl.get_marketlink(nego_text)
    assert fight_marketlink._relative_weight is None
    assert flee_marketlink._relative_weight is None
    assert nego_marketlink._relative_weight is None
    assert fight_marketlink._person_clout is None
    assert flee_marketlink._person_clout is None
    assert nego_marketlink._person_clout is None

    # WHEN
    yao_hl.set_marketlinks_weight_metrics()

    # THEN
    assert fight_marketlink._relative_weight == 0.5
    assert flee_marketlink._relative_weight == 0.35
    assert nego_marketlink._relative_weight == 0.15
    assert fight_marketlink._person_clout == 0.125
    assert flee_marketlink._person_clout == 0.0875
    assert nego_marketlink._person_clout == 0.0375
