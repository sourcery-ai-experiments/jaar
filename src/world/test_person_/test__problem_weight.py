from src.world.problem import problemunit_shop, healerlink_shop


def test_problemunit_set_relative_weight_SetsCorrectly():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)
    assert knee_problemunit._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    knee_problemunit.set_relative_weight(x_relative_weight)

    # THEN
    assert knee_problemunit._relative_weight == x_relative_weight


def test_problemunit_set_person_clout_SetsCorrectly():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)
    assert knee_problemunit._person_clout is None

    # WHEN
    x_person_clout = 0.45
    knee_problemunit.set_person_clout(x_person_clout)

    # THEN
    assert knee_problemunit._person_clout == x_person_clout


def test_problemunit_set_healerlinks_weight_metrics_SetsCorrectly():
    # GIVEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(problem_id=knee_text)
    knee_problemunit._person_clout = 0.25

    yao_text = "Yao"
    sue_text = "Sue"
    tim_text = "Tim"

    knee_problemunit.set_healerlink(healerlink_shop(yao_text, weight=15))
    knee_problemunit.set_healerlink(healerlink_shop(sue_text, weight=3))
    knee_problemunit.set_healerlink(healerlink_shop(tim_text, weight=2))

    yao_healerlink = knee_problemunit.get_healerlink(yao_text)
    sue_healerlink = knee_problemunit.get_healerlink(sue_text)
    tim_healerlink = knee_problemunit.get_healerlink(tim_text)
    assert yao_healerlink._relative_weight is None
    assert sue_healerlink._relative_weight is None
    assert tim_healerlink._relative_weight is None
    assert yao_healerlink._person_clout is None
    assert sue_healerlink._person_clout is None
    assert tim_healerlink._person_clout is None

    # WHEN
    knee_problemunit.set_healerlinks_weight_metrics()

    # THEN
    assert yao_healerlink._relative_weight == 0.75
    assert sue_healerlink._relative_weight == 0.15
    assert tim_healerlink._relative_weight == 0.10
    assert yao_healerlink._person_clout == 0.1875
    assert sue_healerlink._person_clout == 0.0375
    assert tim_healerlink._person_clout == 0.025
