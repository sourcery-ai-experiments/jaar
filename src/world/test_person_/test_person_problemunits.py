from src.world.person import personunit_shop, problembeam_shop
from src.world.problem import problemunit_shop, healerlink_shop, marketlink_shop
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    worlds_dir_setup_cleanup,
)


def test_PersonUnit_set_person_metrics_SetsCorrectlyV1():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"{get_temp_world_dir()}/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)

    knee_text = "knee discomfort"
    bore_text = "bore"
    rain_text = "rain"

    yao_personunit.set_problemunit(problemunit_shop(problem_id=knee_text, weight=60))
    yao_personunit.set_problemunit(problemunit_shop(problem_id=bore_text, weight=35))
    yao_personunit.set_problemunit(problemunit_shop(problem_id=rain_text, weight=5))

    knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    bore_problemunit = yao_personunit.get_problem_obj(bore_text)
    rain_problemunit = yao_personunit.get_problem_obj(rain_text)

    assert knee_problemunit._relative_weight is None
    assert bore_problemunit._relative_weight is None
    assert rain_problemunit._relative_weight is None

    # WHEN
    yao_personunit.set_person_metrics()

    # THEN
    assert knee_problemunit._relative_weight == 0.6
    assert bore_problemunit._relative_weight == 0.35
    assert rain_problemunit._relative_weight == 0.05
    assert knee_problemunit._person_clout == 0.6
    assert bore_problemunit._person_clout == 0.35
    assert rain_problemunit._person_clout == 0.05


def test_PersonUnit_set_person_metrics_SetsCorrectlyV2():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"{get_temp_world_dir()}/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)

    knee_text = "knee"
    bore_problem_id = "bore"
    rain_problem_id = "rain"

    x_knee_problemunit = problemunit_shop(knee_text, 60)
    x_bore_problemunit = problemunit_shop(bore_problem_id, 35)
    x_rain_problemunit = problemunit_shop(rain_problem_id, 5)

    tim_text = "Tim"
    sue_text = "Sue"
    ray_text = "Ray"
    knee_tim_healerlink = healerlink_shop(tim_text, weight=10)
    bore_sue_healerlink = healerlink_shop(sue_text, weight=2)
    bore_tim_healerlink = healerlink_shop(tim_text, weight=3)
    rain_ray_healerlink = healerlink_shop(ray_text, weight=5)

    plan1_market_id = "plan1"
    plan2_market_id = "plan2"
    plan3_market_id = "plan3"
    knee_tim_healerlink.set_marketlink(marketlink_shop(plan1_market_id, 7))
    bore_sue_healerlink.set_marketlink(marketlink_shop(plan2_market_id, 2))
    bore_sue_healerlink.set_marketlink(marketlink_shop(plan3_market_id, 23))
    bore_tim_healerlink.set_marketlink(marketlink_shop(plan3_market_id, 8))
    rain_ray_healerlink.set_marketlink(marketlink_shop(plan3_market_id, 11))

    x_knee_problemunit.set_healerlink(knee_tim_healerlink)
    x_bore_problemunit.set_healerlink(bore_sue_healerlink)
    x_bore_problemunit.set_healerlink(bore_tim_healerlink)
    x_rain_problemunit.set_healerlink(rain_ray_healerlink)

    yao_personunit.set_problemunit(x_knee_problemunit)
    yao_personunit.set_problemunit(x_bore_problemunit)
    yao_personunit.set_problemunit(x_rain_problemunit)

    # WHEN
    yao_personunit.set_person_metrics()

    # THEN
    z_knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    z_bore_problemunit = yao_personunit.get_problem_obj(bore_problem_id)
    z_rain_problemunit = yao_personunit.get_problem_obj(rain_problem_id)
    assert z_knee_problemunit._relative_weight == 0.6
    assert z_bore_problemunit._relative_weight == 0.35
    assert z_rain_problemunit._relative_weight == 0.05
    assert z_knee_problemunit._person_clout == 0.6
    assert z_bore_problemunit._person_clout == 0.35
    assert z_rain_problemunit._person_clout == 0.05

    z_knee_tim_healerlink = z_knee_problemunit.get_healerlink(tim_text)
    z_bore_tim_healerlink = z_bore_problemunit.get_healerlink(tim_text)
    z_bore_sue_healerlink = z_bore_problemunit.get_healerlink(sue_text)
    z_rain_ray_healerlink = z_rain_problemunit.get_healerlink(ray_text)

    assert z_knee_tim_healerlink._person_clout == 0.6
    assert z_bore_tim_healerlink._person_clout == 0.21
    assert z_bore_sue_healerlink._person_clout < 0.14
    assert z_bore_sue_healerlink._person_clout > 0.139999
    assert z_rain_ray_healerlink._person_clout == 0.05

    knee_tim_plan1_marketlink = z_knee_tim_healerlink.get_marketlink(plan1_market_id)
    bore_sue_plan2_marketlink = z_bore_sue_healerlink.get_marketlink(plan2_market_id)
    bore_sue_plan3_marketlink = z_bore_sue_healerlink.get_marketlink(plan3_market_id)
    bore_tim_plan3_marketlink = z_bore_tim_healerlink.get_marketlink(plan3_market_id)
    rain_ray_plan3_marketlink = z_rain_ray_healerlink.get_marketlink(plan3_market_id)

    assert knee_tim_plan1_marketlink._person_clout == 0.6
    assert bore_sue_plan2_marketlink._person_clout == 0.0112
    assert bore_sue_plan3_marketlink._person_clout == 0.1288
    assert bore_tim_plan3_marketlink._person_clout == 0.21
    assert rain_ray_plan3_marketlink._person_clout == 0.05


def test_PersonUnit_popup_visualization_CorrectlyPopsUpVisualization():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(yao_text)
    knee_text = "knee"
    bore_text = "bore"
    rain_text = "rain"
    x_knee_problemunit = problemunit_shop(knee_text, 60)
    x_bore_problemunit = problemunit_shop(bore_text, 35)
    x_rain_problemunit = problemunit_shop(rain_text, 5)
    tim_text = "Tim"
    sue_text = "Sue"
    ray_text = "Ray"
    knee_tim_healerlink = healerlink_shop(tim_text, weight=10)
    bore_sue_healerlink = healerlink_shop(sue_text, weight=2)
    bore_tim_healerlink = healerlink_shop(tim_text, weight=3)
    rain_sue_healerlink = healerlink_shop(sue_text, weight=7)
    rain_tim_healerlink = healerlink_shop(tim_text, weight=15)
    rain_ray_healerlink = healerlink_shop(ray_text, weight=5)
    plan1_text = "plan1"
    plan2_text = "plan2"
    plan3_text = "plan3"
    knee_tim_healerlink.set_marketlink(marketlink_shop(plan1_text, 7))
    bore_sue_healerlink.set_marketlink(marketlink_shop(plan2_text, 2))
    bore_sue_healerlink.set_marketlink(marketlink_shop(plan3_text, 23))
    bore_tim_healerlink.set_marketlink(marketlink_shop(plan3_text, 8))
    rain_sue_healerlink.set_marketlink(marketlink_shop(plan3_text, 11))
    rain_ray_healerlink.set_marketlink(marketlink_shop(plan3_text, 11))
    rain_tim_healerlink.set_marketlink(marketlink_shop(plan1_text, 2))
    x_knee_problemunit.set_healerlink(knee_tim_healerlink)
    x_bore_problemunit.set_healerlink(bore_sue_healerlink)
    x_bore_problemunit.set_healerlink(bore_tim_healerlink)
    x_rain_problemunit.set_healerlink(rain_sue_healerlink)
    x_rain_problemunit.set_healerlink(rain_ray_healerlink)
    x_rain_problemunit.set_healerlink(rain_tim_healerlink)
    yao_personunit.set_problemunit(x_knee_problemunit)
    yao_personunit.set_problemunit(x_bore_problemunit)
    yao_personunit.set_problemunit(x_rain_problemunit)

    # WHEN
    yao_personunit.popup_visualization(marketlink_by_problem=True, show_fig=False)

    # THEN
    view_fig_in_test = False
    print(f"{view_fig_in_test=}")
    if view_fig_in_test:
        yao_personunit.popup_visualization(marketlink_by_problem=True, show_fig=True)


def test_PersonUnit_set_person_metrics_CorrectlySets_problembeams():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(yao_text)
    knee_text = "knee"
    bore_text = "bore"
    rain_text = "rain"
    x_knee_problemunit = problemunit_shop(knee_text, 60)
    x_bore_problemunit = problemunit_shop(bore_text, 35)
    x_rain_problemunit = problemunit_shop(rain_text, 5)
    tim_text = "Tim"
    sue_text = "Sue"
    ray_text = "Ray"
    knee_tim_healerlink = healerlink_shop(tim_text, weight=10)
    bore_sue_healerlink = healerlink_shop(sue_text, weight=2)
    bore_tim_healerlink = healerlink_shop(tim_text, weight=3)
    rain_sue_healerlink = healerlink_shop(sue_text, weight=7)
    rain_tim_healerlink = healerlink_shop(tim_text, weight=15)
    rain_ray_healerlink = healerlink_shop(ray_text, weight=5)
    plan1_text = "plan1"
    plan2_text = "plan2"
    plan3_text = "plan3"
    knee_tim_healerlink.set_marketlink(marketlink_shop(plan1_text, 7))
    bore_sue_healerlink.set_marketlink(marketlink_shop(plan2_text, 2))
    bore_sue_healerlink.set_marketlink(marketlink_shop(plan3_text, 23))
    bore_tim_healerlink.set_marketlink(marketlink_shop(plan3_text, 8))
    rain_sue_healerlink.set_marketlink(marketlink_shop(plan3_text, 11))
    rain_ray_healerlink.set_marketlink(marketlink_shop(plan3_text, 11))
    rain_tim_healerlink.set_marketlink(marketlink_shop(plan1_text, 2))
    x_knee_problemunit.set_healerlink(knee_tim_healerlink)
    x_bore_problemunit.set_healerlink(bore_sue_healerlink)
    x_bore_problemunit.set_healerlink(bore_tim_healerlink)
    x_rain_problemunit.set_healerlink(rain_sue_healerlink)
    x_rain_problemunit.set_healerlink(rain_ray_healerlink)
    x_rain_problemunit.set_healerlink(rain_tim_healerlink)
    yao_personunit.set_problemunit(x_knee_problemunit)
    yao_personunit.set_problemunit(x_bore_problemunit)
    yao_personunit.set_problemunit(x_rain_problemunit)
    assert yao_personunit._problembeams == {}

    # WHEN
    yao_personunit.set_person_metrics()

    # THEN
    assert len(yao_personunit._problembeams) == 7
    # x_yao_knee_tim_plan1_problembeam = problembeam_shop(person_id=)

    # Confirm problembeams do not accumulate
    # WHEN
    yao_personunit.del_problemunit(knee_text)

    # THEN
    yao_personunit.set_person_metrics()
    assert len(yao_personunit._problembeams) != 7
    assert len(yao_personunit._problembeams) == 6


def test_PersonUnit_set_person_metrics_CorrectlySets_marketmetrics():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(yao_text)
    knee_text = "knee"
    bore_text = "bore"
    rain_text = "rain"
    x_knee_problemunit = problemunit_shop(knee_text, 60)
    x_bore_problemunit = problemunit_shop(bore_text, 35)
    x_rain_problemunit = problemunit_shop(rain_text, 5)
    tim_text = "Tim"
    sue_text = "Sue"
    ray_text = "Ray"
    knee_tim_healerlink = healerlink_shop(tim_text, weight=10)
    bore_sue_healerlink = healerlink_shop(sue_text, weight=2)
    bore_tim_healerlink = healerlink_shop(tim_text, weight=3)
    rain_sue_healerlink = healerlink_shop(sue_text, weight=7)
    rain_tim_healerlink = healerlink_shop(tim_text, weight=15)
    rain_ray_healerlink = healerlink_shop(ray_text, weight=5)
    plan1_text = "plan1"
    plan2_text = "plan2"
    plan3_text = "plan3"
    knee_tim_healerlink.set_marketlink(marketlink_shop(plan1_text, 7))
    bore_sue_healerlink.set_marketlink(marketlink_shop(plan2_text, 2))
    bore_sue_healerlink.set_marketlink(marketlink_shop(plan3_text, 23))
    bore_tim_healerlink.set_marketlink(marketlink_shop(plan3_text, 8))
    rain_sue_healerlink.set_marketlink(marketlink_shop(plan3_text, 11))
    rain_ray_healerlink.set_marketlink(marketlink_shop(plan3_text, 11))
    rain_tim_healerlink.set_marketlink(marketlink_shop(plan1_text, 2))
    x_knee_problemunit.set_healerlink(knee_tim_healerlink)
    x_bore_problemunit.set_healerlink(bore_sue_healerlink)
    x_bore_problemunit.set_healerlink(bore_tim_healerlink)
    x_rain_problemunit.set_healerlink(rain_sue_healerlink)
    x_rain_problemunit.set_healerlink(rain_ray_healerlink)
    x_rain_problemunit.set_healerlink(rain_tim_healerlink)
    yao_personunit.set_problemunit(x_knee_problemunit)
    yao_personunit.set_problemunit(x_bore_problemunit)
    yao_personunit.set_problemunit(x_rain_problemunit)
    assert yao_personunit._market_metrics == {}

    # WHEN
    yao_personunit.set_person_metrics()

    # THEN
    # for x_problembeam in yao_personunit._problembeams.values():
    #     print(
    #         f"{x_problembeam._proad=} {x_problembeam.market_id=} {x_problembeam.market_person_clout=}"
    #     )

    assert len(yao_personunit._problembeams) == 7
    assert yao_personunit._market_metrics != {}
    assert len(yao_personunit._market_metrics) == 3
    # for x_marketmetric in yao_personunit._market_metrics.values():
    #     print(f"{x_marketmetric.market_id=} {x_marketmetric._person_clout}")

    # Confirm problembeams do not accumulate
    # WHEN
    yao_personunit.del_problemunit(bore_text)

    # THEN
    yao_personunit.set_person_metrics()
    assert len(yao_personunit._problembeams) == 4
    # for x_problembeam in yao_personunit._problembeams.values():
    #     print(
    #         f"{x_problembeam._proad=} {x_problembeam.market_id=} {x_problembeam.market_person_clout=}"
    #     )
    # yao_knee_tim_plan1_proad = yao_personunit.make_proad(
    #     knee_text, tim_text, plan1_text
    # )
    # yao_rain_sue_plan3_proad = yao_personunit.make_proad(
    #     rain_text, sue_text, plan3_text
    # )
    assert yao_personunit._market_metrics != {}
    assert len(yao_personunit._market_metrics) == 3
    plan1_marketmetric = yao_personunit._market_metrics.get(plan1_text)
    plan2_marketmetric = yao_personunit._market_metrics.get(plan2_text)
    plan3_marketmetric = yao_personunit._market_metrics.get(plan3_text)
    assert 1 == (
        plan1_marketmetric._person_clout
        + plan2_marketmetric._person_clout
        + plan3_marketmetric._person_clout
    )

    print(f"{plan1_marketmetric=}")
    print(f"{plan2_marketmetric=}")
    print(f"{plan3_marketmetric=}")
