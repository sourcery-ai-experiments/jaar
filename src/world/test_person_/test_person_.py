from src.world.person import PersonUnit, personunit_shop


def test_personunit_exists():
    # GIVEN / WHEN
    px = PersonUnit()

    # THEN
    assert px.name is None
    assert px.person_dir is None
    assert px._healings is None
    assert px._pains is None


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    px = personunit_shop(name=dallas_text)

    # THEN
    assert px.name == dallas_text
    assert px.person_dir == ""
    assert px._healings == {}
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


def test_personunit_set_healingunit_CorrectlyCreatesHealingUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    home_text = "home"
    xao_person_obj.set_healingunit(healing_handle=home_text)

    # THEN
    # home_healing = xao_person.get_healing()
    home_healing = xao_person_obj._healings.get(home_text)
    assert home_healing != None
    assert home_healing.handle == home_text
    assert home_healing.healings_dir == f"{xao_person_dir}/healings"


def test_personunit_get_healingunit_CorrectlyGetsHealingUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    home_text = "home"
    xao_person_obj.set_healingunit(home_text)

    # WHEN
    home_healing = xao_person_obj.get_healingunit(home_text)

    # THEN
    assert home_healing != None
    assert home_healing.handle == home_text
    assert home_healing.healings_dir == f"{xao_person_dir}/healings"


def test_personunit_del_healingunit_CorrectlyDeletesHealingUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    home_text = "home"
    xao_person_obj.set_healingunit(home_text)
    before_home_healing = xao_person_obj.get_healingunit(home_text)
    assert before_home_healing != None
    assert before_home_healing.handle == home_text
    assert before_home_healing.healings_dir == f"{xao_person_dir}/healings"

    # WHEN
    xao_person_obj.del_healingunit(home_text)

    # THEN
    after_home_healing = xao_person_obj.get_healingunit(home_text)
    assert after_home_healing is None


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
