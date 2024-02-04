from src.world.problem import economylink_shop, healerlink_shop


def test_HealerLink_set_economylink_CorrectlySetsObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)

    # WHEN
    diet_text = "diet"
    diet_economylink = economylink_shop(economy_id=diet_text)
    yao_healerlink.set_economylink(diet_economylink)

    # THEN
    # diet_economy = yao_problem.get_economy()
    diet_economy = yao_healerlink._economylinks.get(diet_text)
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text


def test_HealerLink_get_economyunit_CorrectlyGetsObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    diet_text = "diet"
    diet_economylink = economylink_shop(economy_id=diet_text)
    yao_healerlink.set_economylink(diet_economylink)

    # WHEN
    diet_economy = yao_healerlink.get_economylink(diet_text)

    # THEN
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text


def test_HealerLink_del_economyunit_CorrectlyDeletesObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    diet_text = "diet"
    diet_economylink = economylink_shop(economy_id=diet_text)
    yao_healerlink.set_economylink(diet_economylink)
    diet_economy = yao_healerlink.get_economylink(diet_text)
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text

    # WHEN
    yao_healerlink.del_economylink(economy_id=diet_text)

    # THEN
    after_diet_economy = yao_healerlink.get_economylink(diet_text)
    assert after_diet_economy is None


def test_HealerLink_economylink_exists_ReturnsCorrectObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    ohio_text = "Ohio"
    yao_healerlink.set_economylink(economylink_shop(economy_id=ohio_text))

    # WHEN / THEN
    diet_text = "diet"
    assert len(yao_healerlink._economylinks) != 0
    assert yao_healerlink.economylink_exists(diet_text) == False

    # WHEN / THEN
    yao_healerlink.set_economylink(economylink_shop(economy_id=diet_text))
    assert len(yao_healerlink._economylinks) != 0
    assert yao_healerlink.economylink_exists(diet_text)

    # WHEN / THEN
    yao_healerlink.del_economylink(diet_text)
    assert len(yao_healerlink._economylinks) != 0
    assert yao_healerlink.economylink_exists(diet_text) == False


def test_HealerLink_set_economylinks_weight_metrics_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_hl = healerlink_shop(healer_id=yao_text)
    yao_hl._person_clout = 0.25
    fight_text = "fight"
    flee_text = "flee"
    nego_text = "negoiate"
    yao_hl.set_economylink(economylink_shop(fight_text, weight=10))
    yao_hl.set_economylink(economylink_shop(flee_text, weight=7))
    yao_hl.set_economylink(economylink_shop(nego_text, weight=3))
    fight_economylink = yao_hl.get_economylink(fight_text)
    flee_economylink = yao_hl.get_economylink(flee_text)
    nego_economylink = yao_hl.get_economylink(nego_text)
    assert fight_economylink._relative_weight is None
    assert flee_economylink._relative_weight is None
    assert nego_economylink._relative_weight is None
    assert fight_economylink._person_clout is None
    assert flee_economylink._person_clout is None
    assert nego_economylink._person_clout is None

    # WHEN
    yao_hl.set_economylinks_weight_metrics()

    # THEN
    assert fight_economylink._relative_weight == 0.5
    assert flee_economylink._relative_weight == 0.35
    assert nego_economylink._relative_weight == 0.15
    assert fight_economylink._person_clout == 0.125
    assert flee_economylink._person_clout == 0.0875
    assert nego_economylink._person_clout == 0.0375
