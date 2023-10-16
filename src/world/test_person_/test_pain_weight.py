from src.world.pain import (
    PainUnit,
    PainKind,
    painunit_shop,
    CureLink,
    curelink_shop,
    HealerLink,
    healerlink_shop,
)


def test_curelink_set_relative_weight_SetsCorrectly():
    # GIVEN
    home_text = "home"
    home_curelink = curelink_shop(handle=home_text)
    assert home_curelink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    home_curelink.set_relative_weight(x_relative_weight)

    # THEN
    assert home_curelink._relative_weight == x_relative_weight


def test_healerunit_set_relative_weight_SetsCorrectly():
    # GIVEN
    yao_text = "yao"
    yao_healerlink = healerlink_shop(person_name=yao_text)
    assert yao_healerlink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    yao_healerlink.set_relative_weight(x_relative_weight)

    # THEN
    assert yao_healerlink._relative_weight == x_relative_weight


def test_painunit_set_relative_weight_SetsCorrectly():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    assert fear_painunit._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    fear_painunit.set_relative_weight(x_relative_weight)

    # THEN
    assert fear_painunit._relative_weight == x_relative_weight
