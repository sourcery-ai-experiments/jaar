from src.world.problem import problemunit_shop, healerlink_shop


def test_problemunit_set_healerlink_CorrectlySetsHealerLink():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)

    # WHEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_id=yao_text)
    knee_problemunit.set_healerlink(yao_healerlink)

    # THEN
    # yao_person = xao_problem.get_person()
    yao_person = knee_problemunit._healerlinks.get(yao_text)
    assert yao_person != None
    assert yao_person.person_id == yao_text


def test_problemunit_get_healerlink_CorrectlyGetsObj():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_id=yao_text)
    knee_problemunit.set_healerlink(yao_healerlink)

    # WHEN
    yao_person = knee_problemunit.get_healerlink(yao_text)

    # THEN
    assert yao_person != None
    assert yao_person.person_id == yao_text


def test_problemunit_del_healerlink_CorrectlyDeletesObj():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_id=yao_text)
    knee_problemunit.set_healerlink(yao_healerlink)
    before_yao_person = knee_problemunit.get_healerlink(yao_text)
    assert before_yao_person != None
    assert before_yao_person.person_id == yao_text

    # WHEN
    knee_problemunit.del_healerlink(person_id=yao_text)

    # THEN
    after_yao_person = knee_problemunit.get_healerlink(yao_text)
    assert after_yao_person is None
