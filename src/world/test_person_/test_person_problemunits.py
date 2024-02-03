from src.world.person import personunit_shop, problembeam_shop
from src.world.problem import problemunit_shop, healerlink_shop, economylink_shop
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    worlds_dir_setup_cleanup,
)


def test_PersonUnit_set_person_metrics_SetsCorrectlyV1(
    worlds_dir_setup_cleanup,
):
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
    assert knee_problemunit._manager_importance == 0.6
    assert bore_problemunit._manager_importance == 0.35
    assert rain_problemunit._manager_importance == 0.05


def test_PersonUnit_set_person_metrics_SetsCorrectlyV2(
    worlds_dir_setup_cleanup,
):
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

    plan1_economy_id = "plan1"
    plan2_economy_id = "plan2"
    plan3_economy_id = "plan3"
    knee_tim_healerlink.set_economylink(economylink_shop(plan1_economy_id, 7))
    bore_sue_healerlink.set_economylink(economylink_shop(plan2_economy_id, 2))
    bore_sue_healerlink.set_economylink(economylink_shop(plan3_economy_id, 23))
    bore_tim_healerlink.set_economylink(economylink_shop(plan3_economy_id, 8))
    rain_ray_healerlink.set_economylink(economylink_shop(plan3_economy_id, 11))

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
    assert z_knee_problemunit._manager_importance == 0.6
    assert z_bore_problemunit._manager_importance == 0.35
    assert z_rain_problemunit._manager_importance == 0.05

    z_knee_tim_healerlink = z_knee_problemunit.get_healerlink(tim_text)
    z_bore_tim_healerlink = z_bore_problemunit.get_healerlink(tim_text)
    z_bore_sue_healerlink = z_bore_problemunit.get_healerlink(sue_text)
    z_rain_ray_healerlink = z_rain_problemunit.get_healerlink(ray_text)

    assert z_knee_tim_healerlink._manager_importance == 0.6
    assert z_bore_tim_healerlink._manager_importance == 0.21
    assert z_bore_sue_healerlink._manager_importance < 0.14
    assert z_bore_sue_healerlink._manager_importance > 0.139999
    assert z_rain_ray_healerlink._manager_importance == 0.05

    knee_tim_plan1_economylink = z_knee_tim_healerlink.get_economylink(plan1_economy_id)
    bore_sue_plan2_economylink = z_bore_sue_healerlink.get_economylink(plan2_economy_id)
    bore_sue_plan3_economylink = z_bore_sue_healerlink.get_economylink(plan3_economy_id)
    bore_tim_plan3_economylink = z_bore_tim_healerlink.get_economylink(plan3_economy_id)
    rain_ray_plan3_economylink = z_rain_ray_healerlink.get_economylink(plan3_economy_id)

    assert knee_tim_plan1_economylink._manager_importance == 0.6
    assert bore_sue_plan2_economylink._manager_importance == 0.0112
    assert bore_sue_plan3_economylink._manager_importance == 0.1288
    assert bore_tim_plan3_economylink._manager_importance == 0.21
    assert rain_ray_plan3_economylink._manager_importance == 0.05


def test_PersonUnit_popup_visualization_CorrectlyPopsUpVisualization(
    worlds_dir_setup_cleanup,
):
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
    knee_tim_healerlink.set_economylink(economylink_shop(plan1_text, 7))
    bore_sue_healerlink.set_economylink(economylink_shop(plan2_text, 2))
    bore_sue_healerlink.set_economylink(economylink_shop(plan3_text, 23))
    bore_tim_healerlink.set_economylink(economylink_shop(plan3_text, 8))
    rain_sue_healerlink.set_economylink(economylink_shop(plan3_text, 11))
    rain_ray_healerlink.set_economylink(economylink_shop(plan3_text, 11))
    rain_tim_healerlink.set_economylink(economylink_shop(plan1_text, 2))
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
    yao_personunit.popup_visualization(economylink_by_problem=True, show_fig=False)

    # THEN
    view_fig_in_test = False
    print(f"{view_fig_in_test=}")
    if view_fig_in_test:
        yao_personunit.popup_visualization(economylink_by_problem=True, show_fig=True)


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
    knee_tim_healerlink.set_economylink(economylink_shop(plan1_text, 7))
    bore_sue_healerlink.set_economylink(economylink_shop(plan2_text, 2))
    bore_sue_healerlink.set_economylink(economylink_shop(plan3_text, 23))
    bore_tim_healerlink.set_economylink(economylink_shop(plan3_text, 8))
    rain_sue_healerlink.set_economylink(economylink_shop(plan3_text, 11))
    rain_ray_healerlink.set_economylink(economylink_shop(plan3_text, 11))
    rain_tim_healerlink.set_economylink(economylink_shop(plan1_text, 2))
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
