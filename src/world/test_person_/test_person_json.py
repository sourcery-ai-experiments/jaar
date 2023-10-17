from src.world.person import personunit_shop


def test_personunit_get_dict_CorrectlyGetsDict():
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"/persons/{xao_text}"
    xao_personunit = personunit_shop(name=xao_text, person_dir=xao_person_dir)
    diet_text = "diet"
    xao_personunit.set_cureunit(diet_text)

    fear_text = "fear"
    xao_personunit.create_painunit_from_kind(fear_text)

    # WHEN
    xao_personunit_get_dict = xao_personunit.get_dict()

    # THEN
    fear_painunit = xao_personunit.get_painunit(fear_text)
    xao_personunit_x_dict = {
        "name": xao_text,
        "_cures": {diet_text: None},
        "_pains": {fear_text: fear_painunit.get_dict()},
    }
    assert xao_personunit_x_dict == xao_personunit_get_dict
