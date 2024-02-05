from src._prime.road import default_road_delimiter_if_none
from src.x_econ.problem import ProblemUnit, problemunit_shop
from pytest import raises as pytest_raises


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
    assert knee_problemunit._person_clout is None
    assert knee_problemunit._road_delimiter is None


def test_ProblemUnit_set_problem_id_CorrectlySetsAttr():
    # GIVEN
    x_problemunit = ProblemUnit()
    assert x_problemunit.problem_id is None

    # WHEN
    knee_text = "knee"
    x_problemunit.set_problem_id(knee_text)

    # THEN
    assert x_problemunit.problem_id == knee_text


def test_ProblemUnit_set_problem_id_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    knee_text = f"knee{slash_text}shin"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        problemunit_shop(knee_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{knee_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


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
    assert knee_problemunit._person_clout is None
    assert knee_problemunit._road_delimiter == default_road_delimiter_if_none()
