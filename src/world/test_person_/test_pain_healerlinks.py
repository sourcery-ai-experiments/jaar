from src.world.pain import painunit_shop, healerlink_shop


def test_painunit_set_healerlink_CorrectlySetsHealerLink():
    # GIVEN
    knee_text = "knee discomfort"
    knee_painunit = painunit_shop(genus=knee_text)

    # WHEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_pid=yao_text)
    knee_painunit.set_healerlink(yao_healerlink)

    # THEN
    # yao_person = xao_pain.get_person()
    yao_person = knee_painunit._healerlinks.get(yao_text)
    assert yao_person != None
    assert yao_person.person_pid == yao_text


def test_painunit_get_healerlink_CorrectlyGetsObj():
    # GIVEN
    knee_text = "knee discomfort"
    knee_painunit = painunit_shop(genus=knee_text)
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_pid=yao_text)
    knee_painunit.set_healerlink(yao_healerlink)

    # WHEN
    yao_person = knee_painunit.get_healerlink(yao_text)

    # THEN
    assert yao_person != None
    assert yao_person.person_pid == yao_text


def test_painunit_del_healerlink_CorrectlyDeletesObj():
    # GIVEN
    knee_text = "knee discomfort"
    knee_painunit = painunit_shop(genus=knee_text)
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_pid=yao_text)
    knee_painunit.set_healerlink(yao_healerlink)
    before_yao_person = knee_painunit.get_healerlink(yao_text)
    assert before_yao_person != None
    assert before_yao_person.person_pid == yao_text

    # WHEN
    knee_painunit.del_healerlink(person_pid=yao_text)

    # THEN
    after_yao_person = knee_painunit.get_healerlink(yao_text)
    assert after_yao_person is None
