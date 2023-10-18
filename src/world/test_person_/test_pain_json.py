from src.world.pain import painunit_shop, projectlink_shop, healerlink_shop


def test_projectlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5
    diet_projectlink = projectlink_shop(handle=diet_text, weight=diet_weight)

    # WHEN
    diet_dict = diet_projectlink.get_dict()

    # THEN
    assert diet_dict == {"handle": diet_text, "weight": diet_weight}


def test_healerlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_healerlink = healerlink_shop(person_name=yao_text, weight=yao_weight)
    diet_text = "diet"
    diet_weight = 7
    diet_projectlink = projectlink_shop(handle=diet_text, weight=diet_weight)
    yao_healerlink.set_projectlink(diet_projectlink)
    diet_project = yao_healerlink.get_projectlink(diet_text)
    assert diet_project != None
    assert diet_project.handle == diet_text

    # WHEN
    yao_dict = yao_healerlink.get_dict()

    # THEN
    assert yao_dict == {
        "person_name": yao_text,
        "weight": yao_weight,
        "_projectlinks": {diet_text: {"handle": diet_text, "weight": diet_weight}},
    }


def test_painunit_get_dict_ReturnsCorrectDict():
    # GIVEN
    fear_text = "fear"
    fear_weight = 13
    fear_painunit = painunit_shop(genus=fear_text, weight=fear_weight)

    yao_text = "yao"
    yao_weight = 7
    yao_healerlink = healerlink_shop(person_name=yao_text, weight=yao_weight)

    diet_text = "diet"
    diet_weight = 3
    diet_projectlink = projectlink_shop(handle=diet_text, weight=diet_weight)
    yao_healerlink.set_projectlink(diet_projectlink)

    fear_painunit.set_healerlink(yao_healerlink)

    # WHEN
    fear_dict = fear_painunit.get_dict()

    # THEN
    print(f"{fear_dict.keys()=}")
    assert len(fear_dict) == 3
    x_healerlinks_dict = fear_dict.get("_healerlinks")
    print(f"{x_healerlinks_dict=}")
    assert len(x_healerlinks_dict) == 1
    yao_healerlink = x_healerlinks_dict.get(yao_text)
    yao_projectlinks_dict = yao_healerlink.get("_projectlinks")
    print(f"{yao_projectlinks_dict=}")
    assert len(yao_projectlinks_dict) == 1
    assert len(fear_dict.get("_healerlinks")) == 1
    assert fear_dict.get("genus") == fear_text
    diet_projectlink_dict = yao_projectlinks_dict.get(diet_text)
    assert diet_projectlink_dict == {"handle": diet_text, "weight": diet_weight}
    assert yao_projectlinks_dict == {
        diet_text: {"handle": diet_text, "weight": diet_weight}
    }

    assert x_healerlinks_dict == {
        yao_text: {
            "person_name": yao_text,
            "weight": yao_weight,
            "_projectlinks": {diet_text: {"handle": diet_text, "weight": diet_weight}},
        }
    }
    assert fear_dict == {
        "genus": fear_text,
        "weight": fear_weight,
        "_healerlinks": {
            yao_text: {
                "person_name": yao_text,
                "weight": yao_weight,
                "_projectlinks": {
                    diet_text: {"handle": diet_text, "weight": diet_weight}
                },
            }
        },
    }
