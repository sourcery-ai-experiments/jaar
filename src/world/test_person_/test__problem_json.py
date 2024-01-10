from src.world.problem import problemunit_shop, economylink_shop, healerlink_shop


def test_economylink_get_dict_ReturnsCorrectDict():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5
    diet_economylink = economylink_shop(economy_id=diet_text, weight=diet_weight)

    # WHEN
    diet_dict = diet_economylink.get_dict()

    # THEN
    assert diet_dict == {"economy_id": diet_text, "weight": diet_weight}


def test_healerlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_healerlink = healerlink_shop(person_id=yao_text, weight=yao_weight)
    diet_text = "diet"
    diet_weight = 7
    diet_economylink = economylink_shop(economy_id=diet_text, weight=diet_weight)
    yao_healerlink.set_economylink(diet_economylink)
    diet_economy = yao_healerlink.get_economylink(diet_text)
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text

    # WHEN
    yao_dict = yao_healerlink.get_dict()

    # THEN
    assert yao_dict == {
        "person_id": yao_text,
        "weight": yao_weight,
        "_economylinks": {diet_text: {"economy_id": diet_text, "weight": diet_weight}},
    }


def test_problemunit_get_dict_ReturnsCorrectDict():
    # GIVEN
    knee_text = "knee discomfort"
    knee_weight = 13
    knee_problemunit = problemunit_shop(genus=knee_text, weight=knee_weight)

    yao_text = "yao"
    yao_weight = 7
    yao_healerlink = healerlink_shop(person_id=yao_text, weight=yao_weight)

    diet_text = "diet"
    diet_weight = 3
    diet_economylink = economylink_shop(economy_id=diet_text, weight=diet_weight)
    yao_healerlink.set_economylink(diet_economylink)

    knee_problemunit.set_healerlink(yao_healerlink)

    # WHEN
    knee_dict = knee_problemunit.get_dict()

    # THEN
    print(f"{knee_dict.keys()=}")
    assert len(knee_dict) == 3
    x_healerlinks_dict = knee_dict.get("_healerlinks")
    print(f"{x_healerlinks_dict=}")
    assert len(x_healerlinks_dict) == 1
    yao_healerlink = x_healerlinks_dict.get(yao_text)
    yao_economylinks_dict = yao_healerlink.get("_economylinks")
    print(f"{yao_economylinks_dict=}")
    assert len(yao_economylinks_dict) == 1
    assert len(knee_dict.get("_healerlinks")) == 1
    assert knee_dict.get("genus") == knee_text
    diet_economylink_dict = yao_economylinks_dict.get(diet_text)
    assert diet_economylink_dict == {"economy_id": diet_text, "weight": diet_weight}
    assert yao_economylinks_dict == {
        diet_text: {"economy_id": diet_text, "weight": diet_weight}
    }

    assert x_healerlinks_dict == {
        yao_text: {
            "person_id": yao_text,
            "weight": yao_weight,
            "_economylinks": {
                diet_text: {"economy_id": diet_text, "weight": diet_weight}
            },
        }
    }
    assert knee_dict == {
        "genus": knee_text,
        "weight": knee_weight,
        "_healerlinks": {
            yao_text: {
                "person_id": yao_text,
                "weight": yao_weight,
                "_economylinks": {
                    diet_text: {"economy_id": diet_text, "weight": diet_weight}
                },
            }
        },
    }
