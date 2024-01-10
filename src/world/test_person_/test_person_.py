from src._prime.road import create_road, default_road_delimiter_if_none
from src.world.person import PersonUnit, personunit_shop
from src.world.problem import problemunit_shop
from pytest import raises as pytest_raises


def test_personunit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.pid is None
    assert x_person.person_dir is None
    assert x_person._economys is None
    assert x_person._problems is None
    assert x_person._road_delimiter is None


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    x_person = personunit_shop(pid=dallas_text)

    # THEN
    assert x_person.pid == dallas_text
    assert x_person.person_dir == ""
    assert x_person._economys == {}
    assert x_person._problems == {}
    assert x_person._road_delimiter == default_road_delimiter_if_none()


def test_personunit_shop_ReturnsPersonUnitWithCorrectAttrs_v2():
    # GIVEN
    dallas_text = "dallas"
    dallas_dir = ""
    slash_text = "/"

    # WHEN
    x_person = personunit_shop(
        pid=dallas_text, person_dir=dallas_dir, _road_delimiter=slash_text
    )

    # THEN
    assert x_person.pid == dallas_text
    assert x_person.person_dir == dallas_dir
    assert x_person._road_delimiter == slash_text


def test_personunit_set_economyunit_CorrectlyCreatesEconomyUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    slash_text = "/"
    xao_person_obj = personunit_shop(
        pid=xao_text, person_dir=xao_person_dir, _road_delimiter=slash_text
    )

    # WHEN
    diet_text = "diet"
    xao_person_obj.set_economyunit(economy_id=diet_text)

    # THEN
    # diet_economy = xao_person.get_economy()
    diet_economy = xao_person_obj._economys.get(diet_text)
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text
    assert diet_economy.economys_dir == f"{xao_person_dir}/economys"
    assert diet_economy._manager_pid == xao_text
    assert diet_economy._road_delimiter == slash_text


def test_personunit_economyunit_exists_ReturnsCorrectObj():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    assert xao_person_obj.economyunit_exists(diet_text) == False

    # WHEN
    xao_person_obj.set_economyunit(economy_id=diet_text)

    # THEN
    assert xao_person_obj.economyunit_exists(diet_text)


def test_personunit_get_economyunit_CorrectlyGetsEconomyUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_person_obj.set_economyunit(diet_text)

    # WHEN
    diet_economy = xao_person_obj.get_economyunit(diet_text)

    # THEN
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text
    assert diet_economy.economys_dir == f"{xao_person_dir}/economys"


def test_personunit_get_economyaddress_ReturnsCorrectObj():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_person_obj.set_economyunit(diet_text)

    # WHEN
    diet_economyaddress = xao_person_obj.get_economyaddress(diet_text)

    # THEN
    assert diet_economyaddress != None
    assert diet_economyaddress == create_road(xao_text, diet_text)


def test_personunit_get_economyaddress_RaisesException():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_person_obj.set_economyunit(diet_text)

    # WHEN/THEN
    texas_text = "Texas"
    with pytest_raises(Exception) as excinfo:
        xao_person_obj.get_economyaddress(texas_text)
    assert (
        str(excinfo.value)
        == f"Cannot get economyaddress for {xao_text} because economy {texas_text} does not exist"
    )


def test_personunit_del_economyunit_CorrectlyDeletesEconomyUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_person_obj.set_economyunit(diet_text)
    before_diet_economy = xao_person_obj.get_economyunit(diet_text)
    assert before_diet_economy != None
    assert before_diet_economy.economy_id == diet_text
    assert before_diet_economy.economys_dir == f"{xao_person_dir}/economys"

    # WHEN
    xao_person_obj.del_economyunit(diet_text)

    # THEN
    after_diet_economy = xao_person_obj.get_economyunit(diet_text)
    assert after_diet_economy is None


def test_personunit_create_problemunit_from_genus_CorrectlyCreatesProblemUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)

    # WHEN
    knee_text = "knee discomfort"
    xao_person_obj.create_problemunit_from_genus(knee_text)

    # THEN
    knee_problem = xao_person_obj._problems.get(knee_text)
    assert knee_problem != None
    assert knee_problem.genus == knee_text


def test_personunit_create_problemunit_from_genus_CorrectlyCreatesProblemUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)

    # WHEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(knee_text)
    xao_person_obj.set_problemunit(knee_problemunit)

    # THEN
    knee_problem = xao_person_obj._problems.get(knee_text)
    assert knee_problem != None
    assert knee_problem.genus == knee_text


def test_personunit_get_problemunit_CorrectlyGetsProblemUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    knee_text = "knee discomfort"
    xao_person_obj.create_problemunit_from_genus(knee_text)

    # WHEN
    knee_problem = xao_person_obj.get_problemunit(knee_text)

    # THEN
    assert knee_problem != None
    assert knee_problem.genus == knee_text


def test_personunit_del_problemunit_CorrectlyDeletesProblemUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    knee_text = "knee discomfort"
    xao_person_obj.create_problemunit_from_genus(knee_text)
    before_knee_problem = xao_person_obj.get_problemunit(knee_text)
    assert before_knee_problem != None
    assert before_knee_problem.genus == knee_text

    # WHEN
    xao_person_obj.del_problemunit(knee_text)

    # THEN
    after_knee_problem = xao_person_obj.get_problemunit(knee_text)
    assert after_knee_problem is None
