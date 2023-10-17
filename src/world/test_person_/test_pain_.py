from src.world.pain import (
    PainUnit,
    PainKind,
    painunit_shop,
    FixLink,
    fixlink_shop,
    HealerLink,
    healerlink_shop,
)


def test_fixlink_exists():
    # GIVEN
    diet_text = "diet"
    diet_weight = 3

    # WHEN
    diet_fixlink = FixLink(handle=diet_text, weight=diet_weight)

    # THEN
    assert diet_fixlink.handle == diet_text
    assert diet_fixlink.weight == diet_weight
    assert diet_fixlink._relative_weight is None
    assert diet_fixlink._person_importance is None


def test_fixlink_shop_ReturnsCorrectObj():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5

    # WHEN
    diet_fixlink = fixlink_shop(handle=diet_text, weight=diet_weight)

    # THEN
    assert diet_fixlink.handle == diet_text
    assert diet_fixlink.weight == diet_weight
    assert diet_fixlink._relative_weight is None
    assert diet_fixlink._person_importance is None


def test_fixlink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    fix_text = "diet"

    # WHEN
    diet_fixlink = fixlink_shop(handle=fix_text)

    # THEN
    assert diet_fixlink.handle == fix_text
    assert diet_fixlink.weight == 1
    assert diet_fixlink._relative_weight is None
    assert diet_fixlink._person_importance is None


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
    assert yao_healerlink._fixlinks is None
    assert yao_healerlink._relative_weight is None
    assert yao_healerlink._person_importance is None


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
    assert yao_healerlink._fixlinks == {}
    assert yao_healerlink._relative_weight is None
    assert yao_healerlink._person_importance is None


def test_healerlink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    yao_text = "yao"

    # WHEN
    yao_healerlink = healerlink_shop(person_name=yao_text)

    # THEN
    assert yao_healerlink.person_name == yao_text
    assert yao_healerlink.weight == 1
    assert yao_healerlink.in_tribe is None
    assert yao_healerlink._fixlinks == {}
    assert yao_healerlink._relative_weight is None
    assert yao_healerlink._person_importance is None


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


def test_painunit_exists():
    # GIVEN
    fear_text = "dallas"
    fear_weight = 13

    # WHEN
    fear_painunit = PainUnit(kind=fear_text, weight=fear_weight)

    # THEN
    assert fear_painunit.kind == fear_text
    assert fear_painunit.weight == fear_weight
    assert fear_painunit._healerlinks is None
    assert fear_painunit._relative_weight is None
    assert fear_painunit._person_importance is None


def test_painunit_shop_ReturnsNonePainUnitWithCorrectAttrs_v1():
    # GIVEN
    fear_text = "dallas"

    # WHEN
    fear_painunit = painunit_shop(kind=fear_text)

    # THEN
    assert fear_painunit.kind == fear_text
    assert fear_painunit.weight == 1
    assert fear_painunit._healerlinks == {}
    assert fear_painunit._relative_weight is None
    assert fear_painunit._person_importance is None


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
