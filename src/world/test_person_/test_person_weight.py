from src.world.person import personunit_shop
from src.world.pain import painunit_shop, healerlink_shop, fixlink_shop
from src.world.examples.world_env_kit import (
    get_temp_env_dir,
    get_temp_env_handle,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)


def test_personunit_set_painunits_weight_metrics_SetsCorrectly(env_dir_setup_cleanup):
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"{get_temp_env_dir}/persons/{xao_text}"
    xao_personunit = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    fear_text = "fear"
    bore_text = "bore"
    rain_text = "rain"

    xao_personunit.set_painunit(painunit_shop(kind=fear_text, weight=60))
    xao_personunit.set_painunit(painunit_shop(kind=bore_text, weight=35))
    xao_personunit.set_painunit(painunit_shop(kind=rain_text, weight=5))

    fear_painunit = xao_personunit.get_painunit(fear_text)
    bore_painunit = xao_personunit.get_painunit(bore_text)
    rain_painunit = xao_personunit.get_painunit(rain_text)

    assert fear_painunit._relative_weight is None
    assert bore_painunit._relative_weight is None
    assert rain_painunit._relative_weight is None

    # WHEN
    xao_personunit.set_painunits_weight_metrics()

    # THEN
    assert fear_painunit._relative_weight == 0.6
    assert bore_painunit._relative_weight == 0.35
    assert rain_painunit._relative_weight == 0.05
    assert fear_painunit._person_importance == 0.6
    assert bore_painunit._person_importance == 0.35
    assert rain_painunit._person_importance == 0.05


def test_personunit_set_painunits_weight_metrics_SetsCorrectly(env_dir_setup_cleanup):
    # GIVEN
    xao_name = "Xao"
    xao_person_dir = f"{get_temp_env_dir}/persons/{xao_name}"
    xao_personunit = personunit_shop(name=xao_name, person_dir=xao_person_dir)

    fear_kind = "fear"
    bore_kind = "bore"
    rain_kind = "rain"

    x_fear_painunit = painunit_shop(fear_kind, 60)
    x_bore_painunit = painunit_shop(bore_kind, 35)
    x_rain_painunit = painunit_shop(rain_kind, 5)

    tim_text = "Tim"
    sue_text = "Sue"
    ray_text = "Ray"
    fear_tim_healerlink = healerlink_shop(tim_text, weight=10)
    bore_sue_healerlink = healerlink_shop(sue_text, weight=2)
    bore_tim_healerlink = healerlink_shop(tim_text, weight=3)
    rain_ray_healerlink = healerlink_shop(ray_text, weight=5)

    plan1_handle = "plan1"
    plan2_handle = "plan2"
    plan3_handle = "plan3"
    fear_tim_healerlink.set_fixlink(fixlink_shop(plan1_handle, 7))
    bore_sue_healerlink.set_fixlink(fixlink_shop(plan2_handle, 2))
    bore_sue_healerlink.set_fixlink(fixlink_shop(plan3_handle, 23))
    bore_tim_healerlink.set_fixlink(fixlink_shop(plan3_handle, 8))
    rain_ray_healerlink.set_fixlink(fixlink_shop(plan3_handle, 11))

    x_fear_painunit.set_healerlink(fear_tim_healerlink)
    x_bore_painunit.set_healerlink(bore_sue_healerlink)
    x_bore_painunit.set_healerlink(bore_tim_healerlink)
    x_rain_painunit.set_healerlink(rain_ray_healerlink)

    xao_personunit.set_painunit(x_fear_painunit)
    xao_personunit.set_painunit(x_bore_painunit)
    xao_personunit.set_painunit(x_rain_painunit)

    # WHEN
    xao_personunit.set_painunits_weight_metrics()

    # THEN
    z_fear_painunit = xao_personunit.get_painunit(fear_kind)
    z_bore_painunit = xao_personunit.get_painunit(bore_kind)
    z_rain_painunit = xao_personunit.get_painunit(rain_kind)
    assert z_fear_painunit._relative_weight == 0.6
    assert z_bore_painunit._relative_weight == 0.35
    assert z_rain_painunit._relative_weight == 0.05
    assert z_fear_painunit._person_importance == 0.6
    assert z_bore_painunit._person_importance == 0.35
    assert z_rain_painunit._person_importance == 0.05

    z_fear_tim_healerlink = z_fear_painunit.get_healerlink(tim_text)
    z_bore_tim_healerlink = z_bore_painunit.get_healerlink(tim_text)
    z_bore_sue_healerlink = z_bore_painunit.get_healerlink(sue_text)
    z_rain_ray_healerlink = z_rain_painunit.get_healerlink(ray_text)

    assert z_fear_tim_healerlink._person_importance == 0.6
    assert z_bore_tim_healerlink._person_importance == 0.21
    assert z_bore_sue_healerlink._person_importance < 0.14
    assert z_bore_sue_healerlink._person_importance > 0.139999
    assert z_rain_ray_healerlink._person_importance == 0.05

    fear_tim_plan1_fixlink = z_fear_tim_healerlink.get_fixlink(plan1_handle)
    bore_sue_plan2_fixlink = z_bore_sue_healerlink.get_fixlink(plan2_handle)
    bore_sue_plan3_fixlink = z_bore_sue_healerlink.get_fixlink(plan3_handle)
    bore_tim_plan3_fixlink = z_bore_tim_healerlink.get_fixlink(plan3_handle)
    rain_ray_plan3_fixlink = z_rain_ray_healerlink.get_fixlink(plan3_handle)

    assert fear_tim_plan1_fixlink._person_importance == 0.6
    assert bore_sue_plan2_fixlink._person_importance == 0.0112
    assert bore_sue_plan3_fixlink._person_importance == 0.1288
    assert bore_tim_plan3_fixlink._person_importance == 0.21
    assert rain_ray_plan3_fixlink._person_importance == 0.05


def test_personunit_set_fixunits_weight_metrics_SetsCorrectly(env_dir_setup_cleanup):
    # GIVEN
    xao_name = "Xao"
    xao_person_dir = f"{get_temp_env_dir()}/persons/{xao_name}"
    xao_personunit = personunit_shop(name=xao_name, person_dir=xao_person_dir)

    fear_kind = "fear"
    bore_kind = "bore"
    rain_kind = "rain"

    x_fear_painunit = painunit_shop(fear_kind, 60)
    x_bore_painunit = painunit_shop(bore_kind, 35)
    x_rain_painunit = painunit_shop(rain_kind, 5)

    tim_text = "Tim"
    sue_text = "Sue"
    ray_text = "Ray"
    x_fear_tim_healerlink = healerlink_shop(tim_text, weight=10)
    x_bore_sue_healerlink = healerlink_shop(sue_text, weight=2)
    x_bore_tim_healerlink = healerlink_shop(tim_text, weight=3)
    x_rain_ray_healerlink = healerlink_shop(ray_text, weight=5)

    plan1_handle = "plan1"
    plan2_handle = "plan2"
    plan3_handle = "plan3"
    plan4_handle = "plan4"
    x_fear_tim_healerlink.set_fixlink(fixlink_shop(plan1_handle, 7))
    x_bore_sue_healerlink.set_fixlink(fixlink_shop(plan2_handle, 2))
    x_bore_sue_healerlink.set_fixlink(fixlink_shop(plan3_handle, 23))
    x_bore_tim_healerlink.set_fixlink(fixlink_shop(plan3_handle, 8))
    x_rain_ray_healerlink.set_fixlink(fixlink_shop(plan3_handle, 11))

    x_fear_painunit.set_healerlink(x_fear_tim_healerlink)
    x_bore_painunit.set_healerlink(x_bore_sue_healerlink)
    x_bore_painunit.set_healerlink(x_bore_tim_healerlink)
    x_rain_painunit.set_healerlink(x_rain_ray_healerlink)

    xao_personunit.set_painunit(x_fear_painunit)
    xao_personunit.set_painunit(x_bore_painunit)
    xao_personunit.set_painunit(x_rain_painunit)

    xao_personunit.set_fixunit(plan1_handle)
    xao_personunit.set_fixunit(plan2_handle)
    xao_personunit.set_fixunit(plan3_handle)
    xao_personunit.set_fixunit(plan4_handle)

    plan1_fixunit = xao_personunit.get_fixunit(plan1_handle)
    plan2_fixunit = xao_personunit.get_fixunit(plan2_handle)
    plan3_fixunit = xao_personunit.get_fixunit(plan3_handle)
    plan4_fixunit = xao_personunit.get_fixunit(plan4_handle)

    assert plan1_fixunit._person_importance is None
    assert plan2_fixunit._person_importance is None
    assert plan3_fixunit._person_importance is None
    assert plan4_fixunit._person_importance is None

    # WHEN
    xao_personunit.set_fixunits_weight_metrics()

    # THEN
    # z_fear_painunit = xao_personunit.get_painunit(fear_kind)
    # z_bore_painunit = xao_personunit.get_painunit(bore_kind)
    # z_rain_painunit = xao_personunit.get_painunit(rain_kind)
    # z_fear_tim_healerlink = z_fear_painunit.get_healerlink(tim_text)
    # z_bore_tim_healerlink = z_bore_painunit.get_healerlink(tim_text)
    # z_bore_sue_healerlink = z_bore_painunit.get_healerlink(sue_text)
    # z_rain_ray_healerlink = z_rain_painunit.get_healerlink(ray_text)
    # fear_tim_plan1_fixlink = z_fear_tim_healerlink.get_fixlink(plan1_handle)
    # bore_sue_plan2_fixlink = z_bore_sue_healerlink.get_fixlink(plan2_handle)
    # bore_sue_plan3_fixlink = z_bore_sue_healerlink.get_fixlink(plan3_handle)
    # bore_tim_plan3_fixlink = z_bore_tim_healerlink.get_fixlink(plan3_handle)
    # rain_ray_plan3_fixlink = z_rain_ray_healerlink.get_fixlink(plan3_handle)
    # assert fear_tim_plan1_fixlink._person_importance == 0.6
    # assert bore_sue_plan2_fixlink._person_importance == 0.0112
    # assert bore_sue_plan3_fixlink._person_importance == 0.1288
    # assert bore_tim_plan3_fixlink._person_importance == 0.21
    # assert rain_ray_plan3_fixlink._person_importance == 0.05

    assert plan1_fixunit._person_importance == 0.6
    assert plan2_fixunit._person_importance == 0.0112
    assert plan3_fixunit._person_importance == 0.3888
    assert plan4_fixunit._person_importance == 0
