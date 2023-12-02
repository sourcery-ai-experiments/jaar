from src.world.person import personunit_shop


def test_personunit_get_dict_CorrectlyGetsDict():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(pid=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_personunit.add_cultureunit(diet_text)

    knee_text = "knee discomfort"
    xao_personunit.create_painunit_from_genus(knee_text)

    # WHEN
    xao_personunit_get_dict = xao_personunit.get_dict()

    # THEN
    knee_painunit = xao_personunit.get_painunit(knee_text)
    xao_personunit_x_dict = {
        "pid": xao_text,
        "_cultures": {diet_text: None},
        "_pains": {knee_text: knee_painunit.get_dict()},
    }
    assert xao_personunit_x_dict == xao_personunit_get_dict
