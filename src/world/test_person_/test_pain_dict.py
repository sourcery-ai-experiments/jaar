from src.world.pain import (
    PainUnit,
    PainKind,
    painunit_shop,
    HealingLink,
    healinglink_shop,
    HealerLink,
    healerlink_shop,
)


def test_healinglink_get_dict_ReturnsCorrectDict():
    # GIVEN
    home_text = "home"
    home_weight = 5
    home_healinglink = healinglink_shop(kind=home_text, weight=home_weight)

    # WHEN
    home_dict = home_healinglink.get_dict()

    # THEN
    assert home_dict == {"kind": home_text, "weight": home_weight}


def test_healerlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_healerlink = healerlink_shop(person_name=yao_text, weight=yao_weight)

    # WHEN
    yao_dict = yao_healerlink.get_dict()

    # THEN
    assert yao_dict == {"person_name": yao_text, "weight": yao_weight}


def test_painunit_get_dict_ReturnsCorrectDict():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)

    home_text = "home"
    home_weight = 3
    home_healinglink = healinglink_shop(kind=home_text, weight=home_weight)
    fear_painunit.set_healinglink(home_healinglink)

    yao_text = "yao"
    yao_weight = 7
    yao_healerlink = healerlink_shop(person_name=yao_text, weight=yao_weight)
    fear_painunit.set_healerlink(yao_healerlink)

    # WHEN
    fear_dict = fear_painunit.get_dict()

    # THEN
    assert fear_dict == {
        "kind": fear_text,
        "_healinglinks": {home_text: {"kind": home_text, "weight": home_weight}},
        "_healerlinks": {yao_text: {"person_name": yao_text, "weight": yao_weight}},
    }
