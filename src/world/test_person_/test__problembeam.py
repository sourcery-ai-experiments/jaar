from src._prime.road import create_proad, default_road_delimiter_if_none
from src.world.person import ProblemBeam, problembeam_shop


def test_ProblemBeam_Exists():
    # GIVEN / WHEN
    diet_problembeam = ProblemBeam()

    # THEN
    assert diet_problembeam.person_id is None
    assert diet_problembeam.problem_id is None
    assert diet_problembeam.problem_weight is None
    assert diet_problembeam.problem_relative_weight is None
    assert diet_problembeam.problem_person_importance is None
    assert diet_problembeam.healer_id is None
    assert diet_problembeam.healer_weight is None
    assert diet_problembeam.healer_relative_weight is None
    assert diet_problembeam.healer_person_importance is None
    assert diet_problembeam.economy_id is None
    assert diet_problembeam.economy_weight is None
    assert diet_problembeam.economy_relative_weight is None
    assert diet_problembeam.economy_person_importance is None
    assert diet_problembeam._road_delimiter is None
    assert diet_problembeam._proad is None


def test_ProblemBeam_AcceptsArgs():
    # GIVEN
    sue_text = "Sue"
    leg_text = "leg"
    leg_weight = 33
    leg_relative_weight = 0.33
    leg_person_importance = 0.233
    yao_text = "Yao"
    yao_weight = 44
    yao_relative_weight = 0.44
    yao_person_importance = 0.244
    diet_text = "diet"
    diet_weight = 55
    diet_relative_weight = 0.55
    diet_person_importance = 0.255
    slash_text = "/"

    # WHEN
    diet_problembeam = ProblemBeam(
        person_id=sue_text,
        healer_id=yao_text,
        healer_weight=yao_weight,
        healer_relative_weight=yao_relative_weight,
        healer_person_importance=yao_person_importance,
        problem_id=leg_text,
        problem_weight=leg_weight,
        problem_relative_weight=leg_relative_weight,
        problem_person_importance=leg_person_importance,
        economy_id=diet_text,
        economy_weight=diet_weight,
        economy_relative_weight=diet_relative_weight,
        economy_person_importance=diet_person_importance,
        _road_delimiter=slash_text,
    )

    # THEN
    assert diet_problembeam.person_id == sue_text
    assert diet_problembeam.healer_id == yao_text
    assert diet_problembeam.healer_weight == yao_weight
    assert diet_problembeam.healer_relative_weight == yao_relative_weight
    assert diet_problembeam.healer_person_importance == yao_person_importance
    assert diet_problembeam.problem_id == leg_text
    assert diet_problembeam.problem_weight == leg_weight
    assert diet_problembeam.problem_relative_weight == leg_relative_weight
    assert diet_problembeam.problem_person_importance == leg_person_importance
    assert diet_problembeam.economy_id == diet_text
    assert diet_problembeam.economy_weight == diet_weight
    assert diet_problembeam.economy_relative_weight == diet_relative_weight
    assert diet_problembeam.economy_person_importance == diet_person_importance
    assert diet_problembeam._road_delimiter == slash_text
    assert diet_problembeam._proad is None


def test_problembeam_shop_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    leg_text = "leg"
    leg_weight = 33
    leg_relative_weight = 0.33
    leg_person_importance = 0.233
    yao_text = "Yao"
    yao_weight = 44
    yao_relative_weight = 0.44
    yao_person_importance = 0.244
    diet_text = "diet"
    diet_weight = 55
    diet_relative_weight = 0.55
    diet_person_importance = 0.255
    slash_text = "/"

    # WHEN
    diet_problembeam = problembeam_shop(
        person_id=sue_text,
        healer_id=yao_text,
        healer_weight=yao_weight,
        healer_relative_weight=yao_relative_weight,
        healer_person_importance=yao_person_importance,
        problem_id=leg_text,
        problem_weight=leg_weight,
        problem_relative_weight=leg_relative_weight,
        problem_person_importance=leg_person_importance,
        economy_id=diet_text,
        economy_weight=diet_weight,
        economy_relative_weight=diet_relative_weight,
        economy_person_importance=diet_person_importance,
        _road_delimiter=slash_text,
    )

    # THEN
    assert diet_problembeam.person_id == sue_text
    assert diet_problembeam.healer_id == yao_text
    assert diet_problembeam.healer_weight == yao_weight
    assert diet_problembeam.healer_relative_weight == yao_relative_weight
    assert diet_problembeam.healer_person_importance == yao_person_importance
    assert diet_problembeam.problem_id == leg_text
    assert diet_problembeam.problem_weight == leg_weight
    assert diet_problembeam.problem_relative_weight == leg_relative_weight
    assert diet_problembeam.problem_person_importance == leg_person_importance
    assert diet_problembeam.economy_id == diet_text
    assert diet_problembeam.economy_weight == diet_weight
    assert diet_problembeam.economy_relative_weight == diet_relative_weight
    assert diet_problembeam.economy_person_importance == diet_person_importance
    assert diet_problembeam._road_delimiter == slash_text
    diet_proad = create_proad(
        person_id=sue_text,
        problem_id=leg_text,
        healer_id=yao_text,
        economy_id=diet_text,
        delimiter=slash_text,
    )
    print(f"{diet_proad=}")
    assert diet_problembeam._proad == diet_proad


def test_problembeam_shop_ReturnsCorrectObj_EmptyAttr():
    # GIVEN
    sue_text = "Sue"
    leg_text = "leg"
    yao_text = "Yao"
    diet_text = "diet"

    # WHEN
    diet_problembeam = problembeam_shop(
        person_id=sue_text,
        healer_id=yao_text,
        problem_id=leg_text,
        economy_id=diet_text,
    )

    # THEN
    assert diet_problembeam.person_id == sue_text
    assert diet_problembeam.healer_id == yao_text
    assert diet_problembeam.healer_weight is None
    assert diet_problembeam.healer_relative_weight is None
    assert diet_problembeam.healer_person_importance is None
    assert diet_problembeam.problem_id == leg_text
    assert diet_problembeam.problem_weight is None
    assert diet_problembeam.problem_relative_weight is None
    assert diet_problembeam.problem_person_importance is None
    assert diet_problembeam.economy_id == diet_text
    assert diet_problembeam.economy_weight is None
    assert diet_problembeam.economy_relative_weight is None
    assert diet_problembeam.economy_person_importance is None
    assert diet_problembeam._road_delimiter == default_road_delimiter_if_none()
    diet_proad = create_proad(
        person_id=sue_text,
        problem_id=leg_text,
        healer_id=yao_text,
        economy_id=diet_text,
    )
    print(f"{diet_proad=}")
    assert diet_problembeam._proad == diet_proad
