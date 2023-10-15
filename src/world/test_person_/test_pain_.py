from src.world.pain import (
    PainUnit,
    PainKind,
    painunit_shop,
    CureLink,
    curelink_shop,
    HealerLink,
    healerlink_shop,
)


def test_curelink_exists():
    # GIVEN
    home_text = "home"
    home_weight = 3

    # WHEN
    px = CureLink(kind=home_text, weight=home_weight)

    # THEN
    assert px.kind == home_text
    assert px.weight == home_weight


def test_curelink_shop_ReturnsCorrectObj():
    # GIVEN
    home_text = "home"
    home_weight = 5

    # WHEN
    px = curelink_shop(kind=home_text, weight=home_weight)

    # THEN
    assert px.kind == home_text
    assert px.weight == home_weight


def test_curelink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    cure_text = "home"

    # WHEN
    px = curelink_shop(kind=cure_text)

    # THEN
    assert px.kind == cure_text
    assert px.weight == 1


def test_healerlink_exists():
    # GIVEN
    yao_text = "yao"
    yao_weight = 3
    yao_in_tribe = True

    # WHEN
    px = HealerLink(person_name=yao_text, weight=3, in_tribe=yao_in_tribe)

    # THEN
    assert px.person_name == yao_text
    assert px.weight == yao_weight
    assert px.in_tribe == yao_in_tribe


def test_healerlink_shop_ReturnsCorrectObj():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_in_tribe = False

    # WHEN
    px = healerlink_shop(person_name=yao_text, weight=yao_weight, in_tribe=yao_in_tribe)

    # THEN
    assert px.person_name == yao_text
    assert px.weight == yao_weight
    assert px.in_tribe == yao_in_tribe


def test_healerlink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    yao_text = "yao"

    # WHEN
    px = healerlink_shop(person_name=yao_text)

    # THEN
    assert px.person_name == yao_text
    assert px.weight == 1
    assert px.in_tribe is None


def test_painunit_exists():
    # GIVEN
    fear_text = "dallas"

    # WHEN
    px = PainUnit(kind=fear_text)

    # THEN
    assert px.kind == fear_text
    assert px._curelinks is None
    assert px._healerlinks is None


def test_painunit_shop_ReturnsNonePainUnitWithCorrectAttrs_v1():
    # GIVEN
    fear_text = "dallas"

    # WHEN
    px = painunit_shop(kind=fear_text)

    # THEN
    assert px.kind == fear_text
    assert px._curelinks == {}
    assert px._healerlinks == {}


def test_painunit_set_curelink_CorrectlySetsCureLink():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)

    # WHEN
    home_text = "home"
    home_curelink = curelink_shop(kind=home_text)
    fear_painunit.set_curelink(home_curelink)

    # THEN
    # home_cure = xao_pain.get_cure()
    home_cure = fear_painunit._curelinks.get(home_text)
    assert home_cure != None
    assert home_cure.kind == home_text


def test_painunit_get_cureunit_CorrectlyGetsAnCureUnit():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    home_text = "home"
    home_curelink = curelink_shop(kind=home_text)
    fear_painunit.set_curelink(home_curelink)

    # WHEN
    home_cure = fear_painunit.get_curelink(home_text)

    # THEN
    assert home_cure != None
    assert home_cure.kind == home_text


def test_painunit_del_cureunit_CorrectlyDeletesCureUnit():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    home_text = "home"
    home_curelink = curelink_shop(kind=home_text)
    fear_painunit.set_curelink(home_curelink)
    before_home_cure = fear_painunit.get_curelink(home_text)
    assert before_home_cure != None
    assert before_home_cure.kind == home_text

    # WHEN
    fear_painunit.del_curelink(curehandle=home_text)

    # THEN
    after_home_cure = fear_painunit.get_curelink(home_text)
    assert after_home_cure is None


def test_painunit_set_healerlink_CorrectlySetsHealerLink():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)

    # WHEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    fear_painunit.set_healerlink(yao_healerlink)

    # THEN
    # yao_person = xao_pain.get_person()
    yao_person = fear_painunit._healerlinks.get(yao_text)
    assert yao_person != None
    assert yao_person.person_name == yao_text


def test_painunit_get_personunit_CorrectlyGetsAnPersonUnit():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    fear_painunit.set_healerlink(yao_healerlink)

    # WHEN
    yao_person = fear_painunit.get_healerlink(yao_text)

    # THEN
    assert yao_person != None
    assert yao_person.person_name == yao_text


def test_painunit_del_personunit_CorrectlyDeletesPersonUnit():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    fear_painunit.set_healerlink(yao_healerlink)
    before_yao_person = fear_painunit.get_healerlink(yao_text)
    assert before_yao_person != None
    assert before_yao_person.person_name == yao_text

    # WHEN
    fear_painunit.del_healerlink(person_name=yao_text)

    # THEN
    after_yao_person = fear_painunit.get_healerlink(yao_text)
    assert after_yao_person is None
