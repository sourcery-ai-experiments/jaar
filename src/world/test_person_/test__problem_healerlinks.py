from src.world.problem import problemunit_shop, healerlink_shop, economylink_shop


def test_ProblemUnit_set_healerlink_CorrectlySetsHealerLink():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)

    # WHEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    knee_problemunit.set_healerlink(yao_healerlink)

    # THEN
    # yao_healerlink = yao_problem.get_person()
    yao_healerlink = knee_problemunit._healerlinks.get(yao_text)
    assert yao_healerlink != None
    assert yao_healerlink.healer_id == yao_text


def test_ProblemUnit_get_healerlink_CorrectlyGetsObj():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    knee_problemunit.set_healerlink(yao_healerlink)

    # WHEN
    yao_healerlink = knee_problemunit.get_healerlink(yao_text)

    # THEN
    assert yao_healerlink != None
    assert yao_healerlink.healer_id == yao_text


def test_ProblemUnit_del_healerlink_CorrectlyDeletesObj():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    knee_problemunit.set_healerlink(yao_healerlink)
    before_yao_healerlink = knee_problemunit.get_healerlink(yao_text)
    assert before_yao_healerlink != None
    assert before_yao_healerlink.healer_id == yao_text

    # WHEN
    knee_problemunit.del_healerlink(healer_id=yao_text)

    # THEN
    after_yao_healerlink = knee_problemunit.get_healerlink(yao_text)
    assert after_yao_healerlink is None


def test_ProblemUnit_economylink_exists_ReturnsCorrectObj():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)
    yao_text = "yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    ohio_text = "Ohio"
    yao_healerlink.set_economylink(economylink_shop(economy_id=ohio_text))
    knee_problemunit.set_healerlink(yao_healerlink)

    # WHEN / THEN
    diet_text = "diet"
    assert knee_problemunit.economylink_exists(diet_text) == False

    # WHEN / THEN
    yao_healerlink.set_economylink(economylink_shop(economy_id=diet_text))
    assert len(yao_healerlink._economylinks) != 0
    assert knee_problemunit.economylink_exists(diet_text)

    # WHEN / THEN
    yao_healerlink.del_economylink(diet_text)
    assert len(yao_healerlink._economylinks) != 0
    assert knee_problemunit.economylink_exists(diet_text) == False
