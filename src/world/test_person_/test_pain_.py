from src.world.pain import (
    PainUnit,
    painunit_shop,
    fixlink_shop,
    healerlink_shop,
)


def test_painunit_exists():
    # GIVEN
    fear_text = "dallas"
    fear_weight = 13

    # WHEN
    fear_painunit = PainUnit(genus=fear_text, weight=fear_weight)

    # THEN
    assert fear_painunit.genus == fear_text
    assert fear_painunit.weight == fear_weight
    assert fear_painunit._healerlinks is None
    assert fear_painunit._relative_weight is None
    assert fear_painunit._person_importance is None


def test_painunit_shop_ReturnsNonePainUnitWithCorrectAttrs_v1():
    # GIVEN
    fear_text = "dallas"

    # WHEN
    fear_painunit = painunit_shop(genus=fear_text)

    # THEN
    assert fear_painunit.genus == fear_text
    assert fear_painunit.weight == 1
    assert fear_painunit._healerlinks == {}
    assert fear_painunit._relative_weight is None
    assert fear_painunit._person_importance is None
