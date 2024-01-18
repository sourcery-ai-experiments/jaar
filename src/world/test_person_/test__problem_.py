from src.world.problem import (
    ProblemUnit,
    problemunit_shop,
    economylink_shop,
    healerlink_shop,
)


def test_problemunit_exists():
    # GIVEN
    knee_text = "knee"
    knee_weight = 13

    # WHEN
    knee_problemunit = ProblemUnit(problem_id=knee_text, weight=knee_weight)

    # THEN
    assert knee_problemunit.problem_id == knee_text
    assert knee_problemunit.weight == knee_weight
    assert knee_problemunit._healerlinks is None
    assert knee_problemunit._relative_weight is None
    assert knee_problemunit._manager_importance is None


def test_problemunit_shop_ReturnsNoneProblemUnitWithCorrectAttrs_v1():
    # GIVEN
    knee_text = "knee"

    # WHEN
    knee_problemunit = problemunit_shop(problem_id=knee_text)

    # THEN
    assert knee_problemunit.problem_id == knee_text
    assert knee_problemunit.weight == 1
    assert knee_problemunit._healerlinks == {}
    assert knee_problemunit._relative_weight is None
    assert knee_problemunit._manager_importance is None
