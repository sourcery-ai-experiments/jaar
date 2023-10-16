from src.world.pain import painunit_shop, curelink_shop, healerlink_shop


def test_curelink_get_dict_ReturnsCorrectDict():
    # GIVEN
    home_text = "home"
    home_weight = 5
    home_curelink = curelink_shop(handle=home_text, weight=home_weight)

    # WHEN
    home_dict = home_curelink.get_dict()

    # THEN
    assert home_dict == {"handle": home_text, "weight": home_weight}


def test_healerlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_healerlink = healerlink_shop(person_name=yao_text, weight=yao_weight)
    home_text = "home"
    home_weight = 7
    home_curelink = curelink_shop(handle=home_text, weight=home_weight)
    yao_healerlink.set_curelink(home_curelink)
    home_cure = yao_healerlink.get_curelink(home_text)
    assert home_cure != None
    assert home_cure.handle == home_text

    # WHEN
    yao_dict = yao_healerlink.get_dict()

    # THEN
    assert yao_dict == {
        "person_name": yao_text,
        "weight": yao_weight,
        "_curelinks": {home_text: {"handle": home_text, "weight": home_weight}},
    }


def test_painunit_get_dict_ReturnsCorrectDict():
    # GIVEN
    fear_text = "fear"
    fear_weight = 13
    fear_painunit = painunit_shop(kind=fear_text, weight=fear_weight)

    yao_text = "yao"
    yao_weight = 7
    yao_healerlink = healerlink_shop(person_name=yao_text, weight=yao_weight)

    home_text = "home"
    home_weight = 3
    home_curelink = curelink_shop(handle=home_text, weight=home_weight)
    yao_healerlink.set_curelink(home_curelink)

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
    yao_curelinks_dict = yao_healerlink.get("_curelinks")
    print(f"{yao_curelinks_dict=}")
    assert len(yao_curelinks_dict) == 1
    assert len(fear_dict.get("_healerlinks")) == 1
    assert fear_dict.get("kind") == fear_text
    home_curelink_dict = yao_curelinks_dict.get(home_text)
    assert home_curelink_dict == {"handle": home_text, "weight": home_weight}
    assert yao_curelinks_dict == {
        home_text: {"handle": home_text, "weight": home_weight}
    }

    assert x_healerlinks_dict == {
        yao_text: {
            "person_name": yao_text,
            "weight": yao_weight,
            "_curelinks": {home_text: {"handle": home_text, "weight": home_weight}},
        }
    }
    assert fear_dict == {
        "kind": fear_text,
        "weight": fear_weight,
        "_healerlinks": {
            yao_text: {
                "person_name": yao_text,
                "weight": yao_weight,
                "_curelinks": {home_text: {"handle": home_text, "weight": home_weight}},
            }
        },
    }
