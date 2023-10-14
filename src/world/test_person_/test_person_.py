from src.world.person import PersonUnit, personunit_shop


def test_personunit_exists():
    # GIVEN / WHEN
    px = PersonUnit()

    # THEN
    assert px.name is None
    assert px.person_dir is None
    assert px._heals is None
    assert px._pains is None


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    px = personunit_shop(name=dallas_text)

    # THEN
    assert px.name == dallas_text
    assert px.person_dir == ""
    assert px._heals == {}
    assert px._pains == {}


def test_personunit_shop_ReturnsPersonUnitWithCorrectAttrs_v2():
    # GIVEN
    dallas_text = "dallas"
    dallas_dir = ""

    # WHEN
    px = personunit_shop(name=dallas_text, person_dir=dallas_dir)

    # THEN
    assert px.name == dallas_text
    assert px.person_dir == dallas_dir


def test_personunit_set_healunit_CorrectlyCreatesHealUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    home_text = "home"
    xao_person_obj.set_healunit(home_text)

    # THEN
    # home_heal = xao_person.get_heal()
    home_heal = xao_person_obj._heals.get(home_text)
    assert home_heal != None
    assert home_heal.kind == home_text
    assert home_heal.heals_dir == f"{xao_person_dir}/heals"


def test_personunit_get_healunit_CorrectlyGetsHealUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    home_text = "home"
    xao_person_obj.set_healunit(home_text)

    # WHEN
    home_heal = xao_person_obj.get_healunit(home_text)

    # THEN
    assert home_heal != None
    assert home_heal.kind == home_text
    assert home_heal.heals_dir == f"{xao_person_dir}/heals"


def test_personunit_get_healunit_CorrectlyGetsHealUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    home_text = "home"
    xao_person_obj.set_healunit(home_text)

    # WHEN
    home_heal = xao_person_obj.get_healunit(home_text)

    # THEN
    assert home_heal != None
    assert home_heal.kind == home_text
    assert home_heal.heals_dir == f"{xao_person_dir}/heals"


def test_personunit_get_healunit_CorrectlyGetsHealUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    home_text = "home"
    xao_person_obj.set_healunit(home_text)
    before_home_heal = xao_person_obj.get_healunit(home_text)
    assert before_home_heal != None
    assert before_home_heal.kind == home_text
    assert before_home_heal.heals_dir == f"{xao_person_dir}/heals"

    # WHEN
    xao_person_obj.del_healunit(home_text)

    # THEN
    before_home_heal = xao_person_obj.get_healunit(home_text)
    assert before_home_heal is None


def test_personunit_set_painunit_CorrectlyCreatesPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    fear_text = "fear"
    xao_person_obj.set_painunit(fear_text)

    # THEN
    fear_pain = xao_person_obj._pains.get(fear_text)
    assert fear_pain != None
    assert fear_pain.kind == fear_text


def test_personunit_get_painunit_CorrectlyGetsPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    fear_text = "fear"
    xao_person_obj.set_painunit(fear_text)

    # WHEN
    fear_pain = xao_person_obj.get_painunit(fear_text)

    # THEN
    assert fear_pain != None
    assert fear_pain.kind == fear_text


def test_personunit_del_painunit_CorrectlyDeletesPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    fear_text = "fear"
    xao_person_obj.set_painunit(fear_text)
    before_fear_pain = xao_person_obj.get_painunit(fear_text)
    assert before_fear_pain != None
    assert before_fear_pain.kind == fear_text

    # WHEN
    xao_person_obj.del_painunit(fear_text)

    # THEN
    after_fear_pain = xao_person_obj.get_painunit(fear_text)
    assert after_fear_pain is None
