from src.world.pain import (
    PainUnit,
    painunit_shop,
    economylink_shop,
    healerlink_shop,
)


def test_painunit_exists():
    # GIVEN
    knee_text = "knee"
    knee_weight = 13

    # WHEN
    knee_painunit = PainUnit(genus=knee_text, weight=knee_weight)

    # THEN
    assert knee_painunit.genus == knee_text
    assert knee_painunit.weight == knee_weight
    assert knee_painunit._healerlinks is None
    assert knee_painunit._relative_weight is None
    assert knee_painunit._manager_importance is None


def test_painunit_shop_ReturnsNonePainUnitWithCorrectAttrs_v1():
    # GIVEN
    knee_text = "knee"

    # WHEN
    knee_painunit = painunit_shop(genus=knee_text)

    # THEN
    assert knee_painunit.genus == knee_text
    assert knee_painunit.weight == 1
    assert knee_painunit._healerlinks == {}
    assert knee_painunit._relative_weight is None
    assert knee_painunit._manager_importance is None
