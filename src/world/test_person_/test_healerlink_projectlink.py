from src.world.pain import projectlink_shop, healerlink_shop


def test_healerlink_set_projectlink_CorrectlySetsObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)

    # WHEN
    diet_text = "diet"
    diet_projectlink = projectlink_shop(handle=diet_text)
    yao_healerlink.set_projectlink(diet_projectlink)

    # THEN
    # diet_project = xao_pain.get_project()
    diet_project = yao_healerlink._projectlinks.get(diet_text)
    assert diet_project != None
    assert diet_project.handle == diet_text


def test_healerlink_get_projectunit_CorrectlyGetsObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    diet_text = "diet"
    diet_projectlink = projectlink_shop(handle=diet_text)
    yao_healerlink.set_projectlink(diet_projectlink)

    # WHEN
    diet_project = yao_healerlink.get_projectlink(diet_text)

    # THEN
    assert diet_project != None
    assert diet_project.handle == diet_text


def test_healerlink_del_projectunit_CorrectlyDeletesObj():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    diet_text = "diet"
    diet_projectlink = projectlink_shop(handle=diet_text)
    yao_healerlink.set_projectlink(diet_projectlink)
    diet_project = yao_healerlink.get_projectlink(diet_text)
    assert diet_project != None
    assert diet_project.handle == diet_text

    # WHEN
    yao_healerlink.del_projectlink(projecthandle=diet_text)

    # THEN
    after_diet_project = yao_healerlink.get_projectlink(diet_text)
    assert after_diet_project is None


def test_healerlink_set_projectlinks_weight_metrics_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_hl = healerlink_shop(person_name=yao_text)
    yao_hl._person_importance = 0.25
    fight_text = "fight"
    flee_text = "flee"
    nego_text = "negoiate"
    yao_hl.set_projectlink(projectlink_shop(fight_text, weight=10))
    yao_hl.set_projectlink(projectlink_shop(flee_text, weight=7))
    yao_hl.set_projectlink(projectlink_shop(nego_text, weight=3))
    fight_projectlink = yao_hl.get_projectlink(fight_text)
    flee_projectlink = yao_hl.get_projectlink(flee_text)
    nego_projectlink = yao_hl.get_projectlink(nego_text)
    assert fight_projectlink._relative_weight is None
    assert flee_projectlink._relative_weight is None
    assert nego_projectlink._relative_weight is None
    assert fight_projectlink._person_importance is None
    assert flee_projectlink._person_importance is None
    assert nego_projectlink._person_importance is None

    # WHEN
    yao_hl.set_projectlinks_weight_metrics()

    # THEN
    assert fight_projectlink._relative_weight == 0.5
    assert flee_projectlink._relative_weight == 0.35
    assert nego_projectlink._relative_weight == 0.15
    assert fight_projectlink._person_importance == 0.125
    assert flee_projectlink._person_importance == 0.0875
    assert nego_projectlink._person_importance == 0.0375
