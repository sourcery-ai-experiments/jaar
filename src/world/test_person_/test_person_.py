from src._prime.road import create_road, default_road_delimiter_if_none
from src.world.problem import healerlink_shop, economylink_shop
from src.world.person import PersonUnit, personunit_shop
from src.world.problem import problemunit_shop
from pytest import raises as pytest_raises


def test_PersonUnit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.person_id is None
    assert x_person.person_dir is None
    assert x_person._economys is None
    assert x_person._problems is None
    assert x_person._road_delimiter is None


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    x_person = personunit_shop(person_id=dallas_text)

    # THEN
    assert x_person.person_id == dallas_text
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
        person_id=dallas_text, person_dir=dallas_dir, _road_delimiter=slash_text
    )

    # THEN
    assert x_person.person_id == dallas_text
    assert x_person.person_dir == dallas_dir
    assert x_person._road_delimiter == slash_text


def test_PersonUnit_create_problemunit_from_problem_id_CorrectlyCreatesProblemUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)

    # WHEN
    knee_text = "knee discomfort"
    xao_personunit.create_problemunit_from_problem_id(knee_text)

    # THEN
    knee_problem = xao_personunit._problems.get(knee_text)
    assert knee_problem != None
    assert knee_problem.problem_id == knee_text


def test_PersonUnit_create_problemunit_from_problem_id_CorrectlyCreatesProblemUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)

    # WHEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(knee_text)
    xao_personunit.set_problemunit(knee_problemunit)

    # THEN
    knee_problem = xao_personunit._problems.get(knee_text)
    assert knee_problem != None
    assert knee_problem.problem_id == knee_text


def test_PersonUnit_get_problemunit_CorrectlyGetsProblemUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    knee_text = "knee discomfort"
    xao_personunit.create_problemunit_from_problem_id(knee_text)

    # WHEN
    knee_problem = xao_personunit.get_problemunit(knee_text)

    # THEN
    assert knee_problem != None
    assert knee_problem.problem_id == knee_text


def test_PersonUnit_economylink_exists_ReturnsCorrectObj():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    knee_text = "knee discomfort"
    xao_personunit.create_problemunit_from_problem_id(knee_text)
    texas_text = "Texas"
    knee_problem = xao_personunit.get_problemunit(knee_text)
    knee_problem.set_healerlink(healerlink_shop(xao_text))
    xao_healerlink = knee_problem.get_healerlink(xao_text)
    assert xao_personunit.economylink_exists(texas_text) == False

    # WHEN
    xao_healerlink.set_economylink(economylink_shop(texas_text))

    # THEN
    assert xao_personunit.economylink_exists(texas_text)

    # WHEN
    xao_healerlink.del_economylink(texas_text)


def test_PersonUnit_del_problemunit_CorrectlyDeletesProblemUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    knee_text = "knee discomfort"
    xao_personunit.create_problemunit_from_problem_id(knee_text)
    before_knee_problem = xao_personunit.get_problemunit(knee_text)
    assert before_knee_problem != None
    assert before_knee_problem.problem_id == knee_text

    # WHEN
    xao_personunit.del_problemunit(knee_text)

    # THEN
    after_knee_problem = xao_personunit.get_problemunit(knee_text)
    assert after_knee_problem is None


def test_PersonUnit_set_economyunit_RaisesErrorIfNoAssociatedProblemExists():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)

    # WHEN/THEN
    diet_text = "diet"
    with pytest_raises(Exception) as excinfo:
        xao_personunit.set_economyunit(economy_id=diet_text)
    assert (
        str(excinfo.value)
        == f"Cannot set_economyunit {diet_text} because no justifying problem exists."
    )


def test_PersonUnit_set_economyunit_CorrectlyCreatesEconomyUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    knee_text = "knee discomfort"
    xao_personunit.create_problemunit_from_problem_id(knee_text)
    diet_text = "diet"
    knee_problem = xao_personunit.get_problemunit(knee_text)
    knee_problem.set_healerlink(healerlink_shop(xao_text))
    xao_healerlink = knee_problem.get_healerlink(xao_text)
    xao_healerlink.set_economylink(economylink_shop(diet_text))

    # WHEN
    xao_personunit.set_economyunit(economy_id=diet_text)

    # THEN
    # diet_economy = xao_person.get_economy()
    diet_economy = xao_personunit._economys.get(diet_text)
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text
    assert diet_economy.economys_dir == f"{xao_person_dir}/economys"


def test_PersonUnit_set_economyunit_CorrectlyCreatesEconomyLink():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    assert xao_personunit.economylink_exists(diet_text) == False

    # WHEN
    knee_text = "knee discomfort"
    xao_personunit.set_economyunit(economy_id=diet_text, x_problem_id=knee_text)

    # THEN
    assert xao_personunit.economylink_exists(diet_text)


def test_PersonUnit_economyunit_exists_ReturnsCorrectObj():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    assert xao_personunit.economyunit_exists(diet_text) == False

    # WHEN
    xao_personunit.set_economyunit(economy_id=diet_text, x_problem_id="Knee")

    # THEN
    assert xao_personunit.economyunit_exists(diet_text)


def test_PersonUnit_all_economyunits_linked_to_problem_ReturnsCorrectObj():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    cooking_text = "cooking"
    hunger_text = "Hunger"
    diet_text = "diet"
    knee_text = "knee"
    xao_personunit.set_economyunit(diet_text, x_problem_id="self-image")
    gym_text = "gym"
    xao_personunit.set_economyunit(gym_text, x_problem_id=knee_text)
    xao_personunit.set_economyunit(cooking_text, x_problem_id=hunger_text)
    xao_personunit.del_problemunit(hunger_text)
    assert xao_personunit.all_economyunits_linked_to_problem() == False

    # WHEN
    hunger_problemunit = problemunit_shop(hunger_text)
    hunger_problemunit.set_healerlink(healerlink_shop(xao_text))
    xao_healerlink = hunger_problemunit.get_healerlink(xao_text)
    xao_healerlink.set_economylink(economylink_shop(cooking_text))
    xao_personunit.set_problemunit(hunger_problemunit)

    # THEN
    assert xao_personunit.all_economyunits_linked_to_problem()

    # WHEN
    xao_personunit.del_problemunit(knee_text)
    assert xao_personunit.all_economyunits_linked_to_problem() == False

    # WHEN
    xao_personunit.del_economyunit(gym_text)

    # THEN
    assert xao_personunit.all_economyunits_linked_to_problem()


def test_PersonUnit_get_economyunit_CorrectlyGetsEconomyUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_personunit.set_economyunit(diet_text, x_problem_id="Knee")

    # WHEN
    diet_economy = xao_personunit.get_economyunit(diet_text)

    # THEN
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text
    assert diet_economy.economys_dir == f"{xao_person_dir}/economys"


def test_PersonUnit_get_economyaddress_ReturnsCorrectObj():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_personunit.set_economyunit(diet_text, x_problem_id="Knee")

    # WHEN
    diet_economyaddress = xao_personunit.get_economyaddress(diet_text)

    # THEN
    assert diet_economyaddress != None
    assert diet_economyaddress == create_road(xao_text, diet_text)


def test_PersonUnit_get_economyaddress_RaisesException():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_personunit.set_economyunit(diet_text, x_problem_id="Knee")

    # WHEN/THEN
    texas_text = "Texas"
    with pytest_raises(Exception) as excinfo:
        xao_personunit.get_economyaddress(texas_text)
    assert (
        str(excinfo.value)
        == f"Cannot get economyaddress for {xao_text} because economy {texas_text} does not exist"
    )


def test_PersonUnit_del_economyunit_CorrectlyDeletesEconomyUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_personunit.set_economyunit(diet_text, x_problem_id="Knee")
    before_diet_economy = xao_personunit.get_economyunit(diet_text)
    assert before_diet_economy != None
    assert before_diet_economy.economy_id == diet_text
    assert before_diet_economy.economys_dir == f"{xao_person_dir}/economys"

    # WHEN
    xao_personunit.del_economyunit(diet_text)

    # THEN
    after_diet_economy = xao_personunit.get_economyunit(diet_text)
    assert after_diet_economy is None
