from src.world.pain import (
    PainUnit,
    PainKind,
    painunit_shop,
    HealLink,
    heallink_shop,
    PersonLink,
    personlink_shop,
)


def test_heallink_exists():
    # GIVEN
    heal_text = "home"
    x_weight = 3

    # WHEN
    px = HealLink(kind=heal_text, weight=3)

    # THEN
    assert px.kind == heal_text
    assert px.weight == x_weight


def test_heallink_shop_ReturnsCorrectObj():
    # GIVEN
    heal_text = "home"
    x_weight = 5

    # WHEN
    px = heallink_shop(kind=heal_text, weight=x_weight)

    # THEN
    assert px.kind == heal_text
    assert px.weight == x_weight


def test_heallink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    heal_text = "home"

    # WHEN
    px = heallink_shop(kind=heal_text)

    # THEN
    assert px.kind == heal_text
    assert px.weight == 1


def test_personlink_exists():
    # GIVEN
    yao_text = "yao"
    x_weight = 3

    # WHEN
    px = PersonLink(person_name=yao_text, weight=3)

    # THEN
    assert px.person_name == yao_text
    assert px.weight == x_weight


def test_personlink_shop_ReturnsCorrectObj():
    # GIVEN
    yao_text = "yao"
    x_weight = 5

    # WHEN
    px = personlink_shop(person_name=yao_text, weight=x_weight)

    # THEN
    assert px.person_name == yao_text
    assert px.weight == x_weight


def test_personlink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    yao_text = "yao"

    # WHEN
    px = personlink_shop(person_name=yao_text)

    # THEN
    assert px.person_name == yao_text
    assert px.weight == 1


def test_painunit_exists():
    # GIVEN
    fear_text = "dallas"

    # WHEN
    px = PainUnit(kind=fear_text)

    # THEN
    assert px.kind == fear_text
    assert px._heallinks is None
    assert px._personlinks is None


def test_painunit_shop_ReturnsNonePainUnitWithCorrectAttrs_v1():
    # GIVEN
    fear_text = "dallas"

    # WHEN
    px = painunit_shop(kind=fear_text)

    # THEN
    assert px.kind == fear_text
    assert px._heallinks == {}
    assert px._personlinks == {}


def test_painunit_set_heallink_CorrectlySetsHealLink():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)

    # WHEN
    home_text = "home"
    home_heallink = heallink_shop(kind=home_text)
    fear_painunit.set_heallink(home_heallink)

    # THEN
    # home_heal = xao_pain.get_heal()
    home_heal = fear_painunit._heallinks.get(home_text)
    assert home_heal != None
    assert home_heal.kind == home_text


def test_painunit_get_healunit_CorrectlyGetsAnHealUnit():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    home_text = "home"
    home_heallink = heallink_shop(kind=home_text)
    fear_painunit.set_heallink(home_heallink)

    # WHEN
    home_heal = fear_painunit.get_heallink(home_text)

    # THEN
    assert home_heal != None
    assert home_heal.kind == home_text


def test_painunit_del_healunit_CorrectlyDeletesHealUnit():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    home_text = "home"
    home_heallink = heallink_shop(kind=home_text)
    fear_painunit.set_heallink(home_heallink)
    before_home_heal = fear_painunit.get_heallink(home_text)
    assert before_home_heal != None
    assert before_home_heal.kind == home_text

    # WHEN
    fear_painunit.del_heallink(healkind=home_text)

    # THEN
    after_home_heal = fear_painunit.get_heallink(home_text)
    assert after_home_heal is None


def test_painunit_set_personlink_CorrectlySetsPersonLink():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)

    # WHEN
    yao_text = "yao"
    yao_personlink = personlink_shop(person_name=yao_text)
    fear_painunit.set_personlink(yao_personlink)

    # THEN
    # yao_person = xao_pain.get_person()
    yao_person = fear_painunit._personlinks.get(yao_text)
    assert yao_person != None
    assert yao_person.person_name == yao_text


def test_painunit_get_personunit_CorrectlyGetsAnPersonUnit():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    yao_text = "yao"
    yao_personlink = personlink_shop(person_name=yao_text)
    fear_painunit.set_personlink(yao_personlink)

    # WHEN
    yao_person = fear_painunit.get_personlink(yao_text)

    # THEN
    assert yao_person != None
    assert yao_person.person_name == yao_text


def test_painunit_del_personunit_CorrectlyDeletesPersonUnit():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    yao_text = "yao"
    yao_personlink = personlink_shop(person_name=yao_text)
    fear_painunit.set_personlink(yao_personlink)
    before_yao_person = fear_painunit.get_personlink(yao_text)
    assert before_yao_person != None
    assert before_yao_person.person_name == yao_text

    # WHEN
    fear_painunit.del_personlink(person_name=yao_text)

    # THEN
    after_yao_person = fear_painunit.get_personlink(yao_text)
    assert after_yao_person is None
