from src.world.person import personunit_shop


def test_personunit_get_dict_CorrectlyGetsDict():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    diet_text = "diet"
    knee_text = "knee discomfort"
    yao_personunit.set_economyunit(diet_text, x_problem_id=knee_text)

    # WHEN
    yao_personunit_get_dict = yao_personunit.get_dict()

    # THEN
    knee_problemunit = yao_personunit.get_problemunit(knee_text)
    yao_personunit_x_dict = {
        "person_id": yao_text,
        "_economys": {diet_text: None},
        "_problems": {knee_text: knee_problemunit.get_dict()},
    }
    assert yao_personunit_x_dict == yao_personunit_get_dict
