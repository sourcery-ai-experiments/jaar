from src.world.pain import culturelink_shop, healerlink_shop


def test_healerlink_set_culturelink_CorrectlySetsObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_id=yao_text)

    # WHEN
    diet_text = "diet"
    diet_culturelink = culturelink_shop(culture_id=diet_text)
    yao_healerlink.set_culturelink(diet_culturelink)

    # THEN
    # diet_culture = xao_pain.get_culture()
    diet_culture = yao_healerlink._culturelinks.get(diet_text)
    assert diet_culture != None
    assert diet_culture.culture_id == diet_text


def test_healerlink_get_cultureunit_CorrectlyGetsObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_id=yao_text)
    diet_text = "diet"
    diet_culturelink = culturelink_shop(culture_id=diet_text)
    yao_healerlink.set_culturelink(diet_culturelink)

    # WHEN
    diet_culture = yao_healerlink.get_culturelink(diet_text)

    # THEN
    assert diet_culture != None
    assert diet_culture.culture_id == diet_text


def test_healerlink_del_cultureunit_CorrectlyDeletesObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_id=yao_text)
    diet_text = "diet"
    diet_culturelink = culturelink_shop(culture_id=diet_text)
    yao_healerlink.set_culturelink(diet_culturelink)
    diet_culture = yao_healerlink.get_culturelink(diet_text)
    assert diet_culture != None
    assert diet_culture.culture_id == diet_text

    # WHEN
    yao_healerlink.del_culturelink(cultureculture_id=diet_text)

    # THEN
    after_diet_culture = yao_healerlink.get_culturelink(diet_text)
    assert after_diet_culture is None


def test_healerlink_set_culturelinks_weight_metrics_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_hl = healerlink_shop(person_id=yao_text)
    yao_hl._manager_importance = 0.25
    fight_text = "fight"
    flee_text = "flee"
    nego_text = "negoiate"
    yao_hl.set_culturelink(culturelink_shop(fight_text, weight=10))
    yao_hl.set_culturelink(culturelink_shop(flee_text, weight=7))
    yao_hl.set_culturelink(culturelink_shop(nego_text, weight=3))
    fight_culturelink = yao_hl.get_culturelink(fight_text)
    flee_culturelink = yao_hl.get_culturelink(flee_text)
    nego_culturelink = yao_hl.get_culturelink(nego_text)
    assert fight_culturelink._relative_weight is None
    assert flee_culturelink._relative_weight is None
    assert nego_culturelink._relative_weight is None
    assert fight_culturelink._manager_importance is None
    assert flee_culturelink._manager_importance is None
    assert nego_culturelink._manager_importance is None

    # WHEN
    yao_hl.set_culturelinks_weight_metrics()

    # THEN
    assert fight_culturelink._relative_weight == 0.5
    assert flee_culturelink._relative_weight == 0.35
    assert nego_culturelink._relative_weight == 0.15
    assert fight_culturelink._manager_importance == 0.125
    assert flee_culturelink._manager_importance == 0.0875
    assert nego_culturelink._manager_importance == 0.0375
