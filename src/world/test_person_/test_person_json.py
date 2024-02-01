from src.world.person import personunit_shop


def test_personunit_get_dict_CorrectlyGetsDict():
    # GIVEN
    yao_text = "Yao"
    yao_artbitarydirectory = f"/artbitarydirectory/persons/{yao_text}"
    yao_personunit = personunit_shop(
        person_id=yao_text, person_dir=yao_artbitarydirectory
    )
    diet_text = "diet"
    knee_text = "knee discomfort"
    yao_personunit.set_economyunit(diet_text, x_problem_id=knee_text)

    # WHEN
    yao_personunit_get_dict = yao_personunit.get_dict()

    # THEN
    knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    knee_proad = yao_personunit.make_proad(knee_text, yao_text, diet_text)
    print(f"{knee_proad=}")
    yao_personunit_x_dict = {
        "person_id": yao_text,
        "person_dir": yao_artbitarydirectory,
        "_economys": {diet_text: None},
        "_problems": {knee_text: knee_problemunit.get_dict()},
        "_primary_contract_road": knee_proad,
        "_primary_contract_active": True,
    }
    assert yao_personunit_x_dict == yao_personunit_get_dict
