from src.world.problem import problemunit_shop, marketlink_shop, healerlink_shop


def test_marketlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5
    diet_marketlink = marketlink_shop(market_id=diet_text, weight=diet_weight)

    # WHEN
    diet_dict = diet_marketlink.get_dict()

    # THEN
    assert diet_dict == {"market_id": diet_text, "weight": diet_weight}


def test_healerlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_healerlink = healerlink_shop(healer_id=yao_text, weight=yao_weight)
    diet_text = "diet"
    diet_weight = 7
    diet_marketlink = marketlink_shop(market_id=diet_text, weight=diet_weight)
    yao_healerlink.set_marketlink(diet_marketlink)
    diet_market = yao_healerlink.get_marketlink(diet_text)
    assert diet_market != None
    assert diet_market.market_id == diet_text

    # WHEN
    yao_dict = yao_healerlink.get_dict()

    # THEN
    assert yao_dict == {
        "healer_id": yao_text,
        "weight": yao_weight,
        "_marketlinks": {diet_text: {"market_id": diet_text, "weight": diet_weight}},
    }


def test_problemunit_get_dict_ReturnsCorrectDict():
    # GIVEN
    knee_text = "knee discomfort"
    knee_weight = 13
    knee_problemunit = problemunit_shop(problem_id=knee_text, weight=knee_weight)

    yao_text = "yao"
    yao_weight = 7
    yao_healerlink = healerlink_shop(healer_id=yao_text, weight=yao_weight)

    diet_text = "diet"
    diet_weight = 3
    diet_marketlink = marketlink_shop(market_id=diet_text, weight=diet_weight)
    yao_healerlink.set_marketlink(diet_marketlink)

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
    yao_marketlinks_dict = yao_healerlink.get("_marketlinks")
    print(f"{yao_marketlinks_dict=}")
    assert len(yao_marketlinks_dict) == 1
    assert len(knee_dict.get("_healerlinks")) == 1
    assert knee_dict.get("problem_id") == knee_text
    diet_marketlink_dict = yao_marketlinks_dict.get(diet_text)
    assert diet_marketlink_dict == {"market_id": diet_text, "weight": diet_weight}
    assert yao_marketlinks_dict == {
        diet_text: {"market_id": diet_text, "weight": diet_weight}
    }

    assert x_healerlinks_dict == {
        yao_text: {
            "healer_id": yao_text,
            "weight": yao_weight,
            "_marketlinks": {
                diet_text: {"market_id": diet_text, "weight": diet_weight}
            },
        }
    }
    assert knee_dict == {
        "problem_id": knee_text,
        "weight": knee_weight,
        "_healerlinks": {
            yao_text: {
                "healer_id": yao_text,
                "weight": yao_weight,
                "_marketlinks": {
                    diet_text: {"market_id": diet_text, "weight": diet_weight}
                },
            }
        },
    }
