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
    home_curelink = CureLink(handle=home_text, weight=home_weight)

    # THEN
    assert home_curelink.handle == home_text
    assert home_curelink.weight == home_weight


def test_curelink_shop_ReturnsCorrectObj():
    # GIVEN
    home_text = "home"
    home_weight = 5

    # WHEN
    home_curelink = curelink_shop(handle=home_text, weight=home_weight)

    # THEN
    assert home_curelink.handle == home_text
    assert home_curelink.weight == home_weight


def test_curelink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    cure_text = "home"

    # WHEN
    home_curelink = curelink_shop(handle=cure_text)

    # THEN
    assert home_curelink.handle == cure_text
    assert home_curelink.weight == 1


def test_healerlink_exists():
    # GIVEN
    yao_text = "yao"
    yao_weight = 3
    yao_in_tribe = True

    # WHEN
    yao_healerlink = HealerLink(person_name=yao_text, weight=3, in_tribe=yao_in_tribe)

    # THEN
    assert yao_healerlink.person_name == yao_text
    assert yao_healerlink.weight == yao_weight
    assert yao_healerlink.in_tribe == yao_in_tribe
    assert yao_healerlink._curelinks is None


def test_healerlink_shop_ReturnsCorrectObj():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_in_tribe = False

    # WHEN
    yao_healerlink = healerlink_shop(
        person_name=yao_text, weight=yao_weight, in_tribe=yao_in_tribe
    )

    # THEN
    assert yao_healerlink.person_name == yao_text
    assert yao_healerlink.weight == yao_weight
    assert yao_healerlink.in_tribe == yao_in_tribe
    assert yao_healerlink._curelinks == {}


def test_healerlink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    yao_text = "yao"

    # WHEN
    yao_healerlink = healerlink_shop(person_name=yao_text)

    # THEN
    assert yao_healerlink.person_name == yao_text
    assert yao_healerlink.weight == 1
    assert yao_healerlink.in_tribe is None
    assert yao_healerlink._curelinks == {}


def test_healerunit_set_curelink_CorrectlySetsCureLink():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)

    # WHEN
    home_text = "home"
    home_curelink = curelink_shop(handle=home_text)
    yao_healerlink.set_curelink(home_curelink)

    # THEN
    # home_cure = xao_pain.get_cure()
    home_cure = yao_healerlink._curelinks.get(home_text)
    assert home_cure != None
    assert home_cure.handle == home_text


def test_healerunit_get_cureunit_CorrectlyGetsAnCureUnit():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    home_text = "home"
    home_curelink = curelink_shop(handle=home_text)
    yao_healerlink.set_curelink(home_curelink)

    # WHEN
    home_cure = yao_healerlink.get_curelink(home_text)

    # THEN
    assert home_cure != None
    assert home_cure.handle == home_text


def test_healerunit_del_cureunit_CorrectlyDeletesCureUnit():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    home_text = "home"
    home_curelink = curelink_shop(handle=home_text)
    yao_healerlink.set_curelink(home_curelink)
    home_cure = yao_healerlink.get_curelink(home_text)
    assert home_cure != None
    assert home_cure.handle == home_text

    # WHEN
    yao_healerlink.del_curelink(curehandle=home_text)

    # THEN
    after_home_cure = yao_healerlink.get_curelink(home_text)
    assert after_home_cure is None


def test_painunit_exists():
    # GIVEN
    fear_text = "dallas"

    # WHEN
    fear_painunit = PainUnit(kind=fear_text)

    # THEN
    assert fear_painunit.kind == fear_text
    assert fear_painunit._healerlinks is None


def test_healerunit_shop_ReturnsNonePainUnitWithCorrectAttrs_v1():
    # GIVEN
    fear_text = "dallas"

    # WHEN
    fear_painunit = painunit_shop(kind=fear_text)

    # THEN
    assert fear_painunit.kind == fear_text
    assert fear_painunit._healerlinks == {}


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
