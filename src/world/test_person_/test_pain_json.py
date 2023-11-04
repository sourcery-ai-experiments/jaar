from src.world.pain import painunit_shop, culturelink_shop, healerlink_shop


def test_culturelink_get_dict_ReturnsCorrectDict():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5
    diet_culturelink = culturelink_shop(title=diet_text, weight=diet_weight)

    # WHEN
    diet_dict = diet_culturelink.get_dict()

    # THEN
    assert diet_dict == {"title": diet_text, "weight": diet_weight}


def test_healerlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_healerlink = healerlink_shop(person_name=yao_text, weight=yao_weight)
    diet_text = "diet"
    diet_weight = 7
    diet_culturelink = culturelink_shop(title=diet_text, weight=diet_weight)
    yao_healerlink.set_culturelink(diet_culturelink)
    diet_culture = yao_healerlink.get_culturelink(diet_text)
    assert diet_culture != None
    assert diet_culture.title == diet_text

    # WHEN
    yao_dict = yao_healerlink.get_dict()

    # THEN
    assert yao_dict == {
        "person_name": yao_text,
        "weight": yao_weight,
        "_culturelinks": {diet_text: {"title": diet_text, "weight": diet_weight}},
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
    diet_culturelink = culturelink_shop(title=diet_text, weight=diet_weight)
    yao_healerlink.set_culturelink(diet_culturelink)

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
    yao_culturelinks_dict = yao_healerlink.get("_culturelinks")
    print(f"{yao_culturelinks_dict=}")
    assert len(yao_culturelinks_dict) == 1
    assert len(fear_dict.get("_healerlinks")) == 1
    assert fear_dict.get("genus") == fear_text
    diet_culturelink_dict = yao_culturelinks_dict.get(diet_text)
    assert diet_culturelink_dict == {"title": diet_text, "weight": diet_weight}
    assert yao_culturelinks_dict == {
        diet_text: {"title": diet_text, "weight": diet_weight}
    }

    assert x_healerlinks_dict == {
        yao_text: {
            "person_name": yao_text,
            "weight": yao_weight,
            "_culturelinks": {diet_text: {"title": diet_text, "weight": diet_weight}},
        }
    }
    assert fear_dict == {
        "genus": fear_text,
        "weight": fear_weight,
        "_healerlinks": {
            yao_text: {
                "person_name": yao_text,
                "weight": yao_weight,
                "_culturelinks": {
                    diet_text: {"title": diet_text, "weight": diet_weight}
                },
            }
        },
    }
