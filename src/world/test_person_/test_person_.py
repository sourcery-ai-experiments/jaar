from src.world.person import PersonUnit, personunit_shop


def test_personunit_exists():
    # GIVEN / WHEN
    px = PersonUnit()

    # THEN
    assert px.name is None
    assert px.person_dir is None
    assert px._goals is None


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    px = personunit_shop(name=dallas_text)

    # THEN
    assert px.name == dallas_text
    assert px.person_dir == ""
    assert px._goals == {}


def test_personunit_shop_ReturnsPersonUnitWithCorrectAttrs_v2():
    # GIVEN
    dallas_text = "dallas"
    dallas_dir = ""

    # WHEN
    px = personunit_shop(name=dallas_text, person_dir=dallas_dir)

    # THEN
    assert px.name == dallas_text
    assert px.person_dir == dallas_dir


def test_personunit_create_goal_CorrectlyCreatesAnGoalUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    # WHEN
    home_text = "home"
    xao_person_obj.create_goal(home_text)

    # THEN
    # home_goal = xao_person.get_goal()
    home_goal = xao_person_obj._goals.get(home_text)
    assert home_goal != None
    assert home_goal.tag == home_text
    assert home_goal.goals_dir == f"{xao_person_dir}/goals"


def test_personunit_get_goal_obj_CorrectlyGetsAnGoalUnit():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_person_obj = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    home_text = "home"
    xao_person_obj.create_goal(home_text)

    # WHEN
    home_goal = xao_person_obj.get_goal_obj(home_text)

    # THEN
    assert home_goal != None
    assert home_goal.tag == home_text
    assert home_goal.goals_dir == f"{xao_person_dir}/goals"
