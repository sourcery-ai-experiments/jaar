from src.world.pain import fixlink_shop, healerlink_shop


def test_healerlink_set_fixlink_CorrectlySetsFixLink():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)

    # WHEN
    diet_text = "diet"
    diet_fixlink = fixlink_shop(handle=diet_text)
    yao_healerlink.set_fixlink(diet_fixlink)

    # THEN
    # diet_fix = xao_pain.get_fix()
    diet_fix = yao_healerlink._fixlinks.get(diet_text)
    assert diet_fix != None
    assert diet_fix.handle == diet_text


def test_healerlink_get_fixunit_CorrectlyGetsAnFixUnit():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    diet_text = "diet"
    diet_fixlink = fixlink_shop(handle=diet_text)
    yao_healerlink.set_fixlink(diet_fixlink)

    # WHEN
    diet_fix = yao_healerlink.get_fixlink(diet_text)

    # THEN
    assert diet_fix != None
    assert diet_fix.handle == diet_text


def test_healerlink_del_fixunit_CorrectlyDeletesFixUnit():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    diet_text = "diet"
    diet_fixlink = fixlink_shop(handle=diet_text)
    yao_healerlink.set_fixlink(diet_fixlink)
    diet_fix = yao_healerlink.get_fixlink(diet_text)
    assert diet_fix != None
    assert diet_fix.handle == diet_text

    # WHEN
    yao_healerlink.del_fixlink(fixhandle=diet_text)

    # THEN
    after_diet_fix = yao_healerlink.get_fixlink(diet_text)
    assert after_diet_fix is None


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
