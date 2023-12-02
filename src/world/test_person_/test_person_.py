from src.world.person import PersonUnit, personunit_shop
from src.world.pain import painunit_shop, healerlink_shop, culturelink_shop


def test_personunit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.pid is None
    assert x_person.person_dir is None
    assert x_person._cultures is None
    assert x_person._pains is None


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    x_person = personunit_shop(pid=dallas_text)

    # THEN
    assert x_person.pid == dallas_text
    assert x_person.person_dir == ""
    assert x_person._cultures == {}
    assert x_person._pains == {}


def test_personunit_shop_ReturnsPersonUnitWithCorrectAttrs_v2():
    # GIVEN
    dallas_text = "dallas"
    dallas_dir = ""

    # WHEN
    x_person = personunit_shop(pid=dallas_text, person_dir=dallas_dir)

    # THEN
    assert x_person.pid == dallas_text
    assert x_person.person_dir == dallas_dir


def test_personunit_add_cultureunit_CorrectlyCreatesCultureUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)

    # WHEN
    diet_text = "diet"
    xao_person_obj.add_cultureunit(culture_qid=diet_text)

    # THEN
    # diet_culture = xao_person.get_culture()
    diet_culture = xao_person_obj._cultures.get(diet_text)
    assert diet_culture != None
    assert diet_culture.qid == diet_text
    assert diet_culture.cultures_dir == f"{xao_person_dir}/cultures"
    assert diet_culture._manager_pid == xao_text


def test_personunit_cultureunit_exists_ReturnsCorrectObj():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    assert xao_person_obj.cultureunit_exists(diet_text) == False

    # WHEN
    xao_person_obj.add_cultureunit(culture_qid=diet_text)

    # THEN
    assert xao_person_obj.cultureunit_exists(diet_text)


def test_personunit_get_cultureunit_CorrectlyGetsCultureUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_person_obj.add_cultureunit(diet_text)

    # WHEN
    diet_culture = xao_person_obj.get_cultureunit(diet_text)

    # THEN
    assert diet_culture != None
    assert diet_culture.qid == diet_text
    assert diet_culture.cultures_dir == f"{xao_person_dir}/cultures"


def test_personunit_del_cultureunit_CorrectlyDeletesCultureUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_person_obj.add_cultureunit(diet_text)
    before_diet_culture = xao_person_obj.get_cultureunit(diet_text)
    assert before_diet_culture != None
    assert before_diet_culture.qid == diet_text
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
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)

    # WHEN
    knee_text = "knee discomfort"
    xao_person_obj.create_painunit_from_genus(knee_text)

    # THEN
    knee_pain = xao_person_obj._pains.get(knee_text)
    assert knee_pain != None
    assert knee_pain.genus == knee_text


def test_personunit_create_painunit_from_genus_CorrectlyCreatesPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)

    # WHEN
    knee_text = "knee discomfort"
    knee_painunit = painunit_shop(knee_text)
    xao_person_obj.set_painunit(knee_painunit)

    # THEN
    knee_pain = xao_person_obj._pains.get(knee_text)
    assert knee_pain != None
    assert knee_pain.genus == knee_text


def test_personunit_get_painunit_CorrectlyGetsPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    knee_text = "knee discomfort"
    xao_person_obj.create_painunit_from_genus(knee_text)

    # WHEN
    knee_pain = xao_person_obj.get_painunit(knee_text)

    # THEN
    assert knee_pain != None
    assert knee_pain.genus == knee_text


def test_personunit_del_painunit_CorrectlyDeletesPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    knee_text = "knee discomfort"
    xao_person_obj.create_painunit_from_genus(knee_text)
    before_knee_pain = xao_person_obj.get_painunit(knee_text)
    assert before_knee_pain != None
    assert before_knee_pain.genus == knee_text

    # WHEN
    xao_person_obj.del_painunit(knee_text)

    # THEN
    after_knee_pain = xao_person_obj.get_painunit(knee_text)
    assert after_knee_pain is None
