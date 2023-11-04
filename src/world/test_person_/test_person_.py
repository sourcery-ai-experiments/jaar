from src.world.person import PersonUnit, personunit_shop
from src.world.pain import painunit_shop, healerlink_shop, culturelink_shop


def test_personunit_exists():
    # GIVEN / WHEN
    px = PersonUnit()

    # THEN
    assert px.name is None
    assert px.person_dir is None
    assert px._cultures is None
    assert px._pains is None


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    px = personunit_shop(name=dallas_text)

    # THEN
    assert px.name == dallas_text
    assert px.person_dir == ""
    assert px._cultures == {}
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


def test_personunit_set_cultureunit_CorrectlyCreatesCultureUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    diet_text = "diet"
    xao_person_obj.set_cultureunit(culture_title=diet_text)

    # THEN
    # diet_culture = xao_person.get_culture()
    diet_culture = xao_person_obj._cultures.get(diet_text)
    assert diet_culture != None
    assert diet_culture.title == diet_text
    assert diet_culture.cultures_dir == f"{xao_person_dir}/cultures"
    assert diet_culture._manager_name == xao_text


def test_personunit_get_cultureunit_CorrectlyGetsCultureUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_person_obj.set_cultureunit(diet_text)

    # WHEN
    diet_culture = xao_person_obj.get_cultureunit(diet_text)

    # THEN
    assert diet_culture != None
    assert diet_culture.title == diet_text
    assert diet_culture.cultures_dir == f"{xao_person_dir}/cultures"


def test_personunit_del_cultureunit_CorrectlyDeletesCultureUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_person_obj.set_cultureunit(diet_text)
    before_diet_culture = xao_person_obj.get_cultureunit(diet_text)
    assert before_diet_culture != None
    assert before_diet_culture.title == diet_text
    assert before_diet_culture.cultures_dir == f"{xao_person_dir}/cultures"

    # WHEN
    xao_person_obj.del_cultureunit(diet_text)

    # THEN
    after_diet_culture = xao_person_obj.get_cultureunit(diet_text)
    assert after_diet_culture is None


def test_personunit_create_painunit_from_genus_CorrectlyCreatesPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    fear_text = "fear"
    xao_person_obj.create_painunit_from_genus(fear_text)

    # THEN
    fear_pain = xao_person_obj._pains.get(fear_text)
    assert fear_pain != None
    assert fear_pain.genus == fear_text


def test_personunit_create_painunit_from_genus_CorrectlyCreatesPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    fear_text = "fear"
    fear_painunit = painunit_shop(fear_text)
    xao_person_obj.set_painunit(fear_painunit)

    # THEN
    fear_pain = xao_person_obj._pains.get(fear_text)
    assert fear_pain != None
    assert fear_pain.genus == fear_text


def test_personunit_get_painunit_CorrectlyGetsPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    fear_text = "fear"
    xao_person_obj.create_painunit_from_genus(fear_text)

    # WHEN
    fear_pain = xao_person_obj.get_painunit(fear_text)

    # THEN
    assert fear_pain != None
    assert fear_pain.genus == fear_text


def test_personunit_del_painunit_CorrectlyDeletesPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    fear_text = "fear"
    xao_person_obj.create_painunit_from_genus(fear_text)
    before_fear_pain = xao_person_obj.get_painunit(fear_text)
    assert before_fear_pain != None
    assert before_fear_pain.genus == fear_text

    # WHEN
    xao_person_obj.del_painunit(fear_text)

    # THEN
    after_fear_pain = xao_person_obj.get_painunit(fear_text)
    assert after_fear_pain is None
