from src.world.person import PersonUnit, personunit_shop
from src.world.pain import painunit_shop, healerlink_shop, curelink_shop


def test_personunit_exists():
    # GIVEN / WHEN
    px = PersonUnit()

    # THEN
    assert px.name is None
    assert px.person_dir is None
    assert px._cures is None
    assert px._pains is None


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    px = personunit_shop(name=dallas_text)

    # THEN
    assert px.name == dallas_text
    assert px.person_dir == ""
    assert px._cures == {}
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


def test_personunit_set_cureunit_CorrectlyCreatesCureUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    home_text = "home"
    xao_person_obj.set_cureunit(cure_handle=home_text)

    # THEN
    # home_cure = xao_person.get_cure()
    home_cure = xao_person_obj._cures.get(home_text)
    assert home_cure != None
    assert home_cure.handle == home_text
    assert home_cure.cures_dir == f"{xao_person_dir}/cures"


def test_personunit_get_cureunit_CorrectlyGetsCureUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    home_text = "home"
    xao_person_obj.set_cureunit(home_text)

    # WHEN
    home_cure = xao_person_obj.get_cureunit(home_text)

    # THEN
    assert home_cure != None
    assert home_cure.handle == home_text
    assert home_cure.cures_dir == f"{xao_person_dir}/cures"


def test_personunit_del_cureunit_CorrectlyDeletesCureUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    home_text = "home"
    xao_person_obj.set_cureunit(home_text)
    before_home_cure = xao_person_obj.get_cureunit(home_text)
    assert before_home_cure != None
    assert before_home_cure.handle == home_text
    assert before_home_cure.cures_dir == f"{xao_person_dir}/cures"

    # WHEN
    xao_person_obj.del_cureunit(home_text)

    # THEN
    after_home_cure = xao_person_obj.get_cureunit(home_text)
    assert after_home_cure is None


def test_personunit_create_painunit_from_kind_CorrectlyCreatesPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    fear_text = "fear"
    xao_person_obj.create_painunit_from_kind(fear_text)

    # THEN
    fear_pain = xao_person_obj._pains.get(fear_text)
    assert fear_pain != None
    assert fear_pain.kind == fear_text


def test_personunit_create_painunit_from_kind_CorrectlyCreatesPainUnit():
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
    assert fear_pain.kind == fear_text


def test_personunit_get_painunit_CorrectlyGetsPainUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    fear_text = "fear"
    xao_person_obj.create_painunit_from_kind(fear_text)

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
    xao_person_obj.create_painunit_from_kind(fear_text)
    before_fear_pain = xao_person_obj.get_painunit(fear_text)
    assert before_fear_pain != None
    assert before_fear_pain.kind == fear_text

    # WHEN
    xao_person_obj.del_painunit(fear_text)

    # THEN
    after_fear_pain = xao_person_obj.get_painunit(fear_text)
    assert after_fear_pain is None


def test_personunit_set_painunits_relative_weight_SetsCorrectly():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    fear_text = "fear"
    bore_text = "bore"
    rain_text = "rain"

    xao_person_obj.set_painunit(painunit_shop(kind=fear_text, weight=60))
    xao_person_obj.set_painunit(painunit_shop(kind=bore_text, weight=35))
    xao_person_obj.set_painunit(painunit_shop(kind=rain_text, weight=5))

    fear_painunit = xao_person_obj.get_painunit(fear_text)
    bore_painunit = xao_person_obj.get_painunit(bore_text)
    rain_painunit = xao_person_obj.get_painunit(rain_text)

    assert fear_painunit._relative_weight is None
    assert bore_painunit._relative_weight is None
    assert rain_painunit._relative_weight is None

    # WHEN
    xao_person_obj.set_painunits_relative_weight()

    # THEN
    assert fear_painunit._relative_weight == 0.6
    assert bore_painunit._relative_weight == 0.35
    assert rain_painunit._relative_weight == 0.05
