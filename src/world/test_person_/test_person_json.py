from src.world.person import personunit_shop


def test_personunit_get_dict_CorrectlyGetsDict():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(person_id=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    knee_text = "knee discomfort"
    xao_personunit.set_economyunit(diet_text, x_problem_id=knee_text)

    # WHEN
    xao_personunit_get_dict = xao_personunit.get_dict()

    # THEN
    knee_problemunit = xao_personunit.get_problemunit(knee_text)
    xao_personunit_x_dict = {
        "person_id": xao_text,
        "_economys": {diet_text: None},
        "_problems": {knee_text: knee_problemunit.get_dict()},
    }
    assert xao_personunit_x_dict == xao_personunit_get_dict
