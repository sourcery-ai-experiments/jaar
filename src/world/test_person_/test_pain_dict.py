from src.world.pain import (
    PainUnit,
    PainKind,
    painunit_shop,
    HealLink,
    heallink_shop,
    PersonLink,
    personlink_shop,
)


def test_heallink_get_dict_ReturnsCorrectDict():
    # GIVEN
    home_text = "home"
    home_weight = 5
    home_heallink = heallink_shop(kind=home_text, weight=home_weight)

    # WHEN
    home_dict = home_heallink.get_dict()

    # THEN
    assert home_dict == {"kind": home_text, "weight": home_weight}


def test_personlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_personlink = personlink_shop(person_name=yao_text, weight=yao_weight)

    # WHEN
    yao_dict = yao_personlink.get_dict()

    # THEN
    assert yao_dict == {"person_name": yao_text, "weight": yao_weight}


def test_painunit_get_dict_ReturnsCorrectDict():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)

    home_text = "home"
    home_weight = 3
    home_heallink = heallink_shop(kind=home_text, weight=home_weight)
    fear_painunit.set_heallink(home_heallink)

    yao_text = "yao"
    yao_weight = 7
    yao_personlink = personlink_shop(person_name=yao_text, weight=yao_weight)
    fear_painunit.set_personlink(yao_personlink)

    # WHEN
    fear_dict = fear_painunit.get_dict()

    # THEN
    assert fear_dict == {
        "kind": fear_text,
        "_heallinks": {home_text: {"kind": home_text, "weight": home_weight}},
        "_personlinks": {yao_text: {"person_name": yao_text, "weight": yao_weight}},
    }
