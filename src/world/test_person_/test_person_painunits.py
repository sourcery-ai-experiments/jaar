from src.world.person import personunit_shop
from src.world.pain import painunit_shop, healerlink_shop, culturelink_shop
from src.world.examples.world_env_kit import (
    get_temp_env_dir,
    get_temp_env_title,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)


def test_personunit_set_painunits_weight_metrics_SetsCorrectly(env_dir_setup_cleanup):
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"{get_temp_env_dir}/persons/{xao_text}"
    xao_personunit = personunit_shop(name=xao_text, person_dir=xao_person_dir)

    knee_text = "knee discomfort"
    bore_text = "bore"
    rain_text = "rain"

    xao_personunit.set_painunit(painunit_shop(genus=knee_text, weight=60))
    xao_personunit.set_painunit(painunit_shop(genus=bore_text, weight=35))
    xao_personunit.set_painunit(painunit_shop(genus=rain_text, weight=5))

    knee_painunit = xao_personunit.get_painunit(knee_text)
    bore_painunit = xao_personunit.get_painunit(bore_text)
    rain_painunit = xao_personunit.get_painunit(rain_text)

    assert knee_painunit._relative_weight is None
    assert bore_painunit._relative_weight is None
    assert rain_painunit._relative_weight is None

    # WHEN
    xao_personunit.set_painunits_weight_metrics()

    # THEN
    assert knee_painunit._relative_weight == 0.6
    assert bore_painunit._relative_weight == 0.35
    assert rain_painunit._relative_weight == 0.05
    assert knee_painunit._manager_importance == 0.6
    assert bore_painunit._manager_importance == 0.35
    assert rain_painunit._manager_importance == 0.05


def test_personunit_set_painunits_weight_metrics_SetsCorrectly(env_dir_setup_cleanup):
    # GIVEN
    xao_name = "Xao"
    xao_person_dir = f"{get_temp_env_dir}/persons/{xao_name}"
    xao_personunit = personunit_shop(name=xao_name, person_dir=xao_person_dir)

    knee_genus = "knee"
    bore_genus = "bore"
    rain_genus = "rain"

    x_knee_painunit = painunit_shop(knee_genus, 60)
    x_bore_painunit = painunit_shop(bore_genus, 35)
    x_rain_painunit = painunit_shop(rain_genus, 5)

    tim_text = "Tim"
    sue_text = "Sue"
    ray_text = "Ray"
    knee_tim_healerlink = healerlink_shop(tim_text, weight=10)
    bore_sue_healerlink = healerlink_shop(sue_text, weight=2)
    bore_tim_healerlink = healerlink_shop(tim_text, weight=3)
    rain_ray_healerlink = healerlink_shop(ray_text, weight=5)

    plan1_title = "plan1"
    plan2_title = "plan2"
    plan3_title = "plan3"
    knee_tim_healerlink.set_culturelink(culturelink_shop(plan1_title, 7))
    bore_sue_healerlink.set_culturelink(culturelink_shop(plan2_title, 2))
    bore_sue_healerlink.set_culturelink(culturelink_shop(plan3_title, 23))
    bore_tim_healerlink.set_culturelink(culturelink_shop(plan3_title, 8))
    rain_ray_healerlink.set_culturelink(culturelink_shop(plan3_title, 11))

    x_knee_painunit.set_healerlink(knee_tim_healerlink)
    x_bore_painunit.set_healerlink(bore_sue_healerlink)
    x_bore_painunit.set_healerlink(bore_tim_healerlink)
    x_rain_painunit.set_healerlink(rain_ray_healerlink)

    xao_personunit.set_painunit(x_knee_painunit)
    xao_personunit.set_painunit(x_bore_painunit)
    xao_personunit.set_painunit(x_rain_painunit)

    # WHEN
    xao_personunit.set_painunits_weight_metrics()

    # THEN
    z_knee_painunit = xao_personunit.get_painunit(knee_genus)
    z_bore_painunit = xao_personunit.get_painunit(bore_genus)
    z_rain_painunit = xao_personunit.get_painunit(rain_genus)
    assert z_knee_painunit._relative_weight == 0.6
    assert z_bore_painunit._relative_weight == 0.35
    assert z_rain_painunit._relative_weight == 0.05
    assert z_knee_painunit._manager_importance == 0.6
    assert z_bore_painunit._manager_importance == 0.35
    assert z_rain_painunit._manager_importance == 0.05

    z_knee_tim_healerlink = z_knee_painunit.get_healerlink(tim_text)
    z_bore_tim_healerlink = z_bore_painunit.get_healerlink(tim_text)
    z_bore_sue_healerlink = z_bore_painunit.get_healerlink(sue_text)
    z_rain_ray_healerlink = z_rain_painunit.get_healerlink(ray_text)

    assert z_knee_tim_healerlink._manager_importance == 0.6
    assert z_bore_tim_healerlink._manager_importance == 0.21
    assert z_bore_sue_healerlink._manager_importance < 0.14
    assert z_bore_sue_healerlink._manager_importance > 0.139999
    assert z_rain_ray_healerlink._manager_importance == 0.05

    knee_tim_plan1_culturelink = z_knee_tim_healerlink.get_culturelink(plan1_title)
    bore_sue_plan2_culturelink = z_bore_sue_healerlink.get_culturelink(plan2_title)
    bore_sue_plan3_culturelink = z_bore_sue_healerlink.get_culturelink(plan3_title)
    bore_tim_plan3_culturelink = z_bore_tim_healerlink.get_culturelink(plan3_title)
    rain_ray_plan3_culturelink = z_rain_ray_healerlink.get_culturelink(plan3_title)

    assert knee_tim_plan1_culturelink._manager_importance == 0.6
    assert bore_sue_plan2_culturelink._manager_importance == 0.0112
    assert bore_sue_plan3_culturelink._manager_importance == 0.1288
    assert bore_tim_plan3_culturelink._manager_importance == 0.21
    assert rain_ray_plan3_culturelink._manager_importance == 0.05

    # FROM CULTUREUNIT
    # def set_cultureunits_weight_metrics(self):
    #     self.set_painunits_weight_metrics()
    #     cultureunit_titles = {
    #         x_cultureunit.title: 0 for x_cultureunit in self._cultures.values()
    #     }

    #     for x_painunit in self._pains.values():
    #         for x_healerlink in x_painunit._healerlinks.values():
    #             for x_culturelink in x_healerlink._culturelinks.values():
    #                 cultureunit_titles[
    #                     x_culturelink.title
    #                 ] += x_culturelink._manager_importance


# def test_personunit_set_cultureunits_weight_metrics_SetsCorrectly(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     xao_name = "Xao"
#     xao_person_dir = f"{get_temp_env_dir()}/persons/{xao_name}"
#     xao_personunit = personunit_shop(name=xao_name, person_dir=xao_person_dir)

#     knee_genus = "knee"
#     bore_genus = "bore"
#     rain_genus = "rain"

#     x_knee_painunit = painunit_shop(knee_genus, 60)
#     x_bore_painunit = painunit_shop(bore_genus, 35)
#     x_rain_painunit = painunit_shop(rain_genus, 5)

#     tim_text = "Tim"
#     sue_text = "Sue"
#     ray_text = "Ray"
#     x_knee_tim_healerlink = healerlink_shop(tim_text, weight=10)
#     x_bore_sue_healerlink = healerlink_shop(sue_text, weight=2)
#     x_bore_tim_healerlink = healerlink_shop(tim_text, weight=3)
#     x_rain_ray_healerlink = healerlink_shop(ray_text, weight=5)

#     plan1_title = "plan1"
#     plan2_title = "plan2"
#     plan3_title = "plan3"
#     plan4_title = "plan4"
#     x_knee_tim_healerlink.set_culturelink(culturelink_shop(plan1_title, 7))
#     x_bore_sue_healerlink.set_culturelink(culturelink_shop(plan2_title, 2))
#     x_bore_sue_healerlink.set_culturelink(culturelink_shop(plan3_title, 23))
#     x_bore_tim_healerlink.set_culturelink(culturelink_shop(plan3_title, 8))
#     x_rain_ray_healerlink.set_culturelink(culturelink_shop(plan3_title, 11))

#     x_knee_painunit.set_healerlink(x_knee_tim_healerlink)
#     x_bore_painunit.set_healerlink(x_bore_sue_healerlink)
#     x_bore_painunit.set_healerlink(x_bore_tim_healerlink)
#     x_rain_painunit.set_healerlink(x_rain_ray_healerlink)

#     xao_personunit.set_painunit(x_knee_painunit)
#     xao_personunit.set_painunit(x_bore_painunit)
#     xao_personunit.set_painunit(x_rain_painunit)

#     xao_personunit.set_cultureunit(plan1_title)
#     xao_personunit.set_cultureunit(plan2_title)
#     xao_personunit.set_cultureunit(plan3_title)
#     xao_personunit.set_cultureunit(plan4_title)

#     plan1_cultureunit = xao_personunit.get_cultureunit(plan1_title)
#     plan2_cultureunit = xao_personunit.get_cultureunit(plan2_title)
#     plan3_cultureunit = xao_personunit.get_cultureunit(plan3_title)
#     plan4_cultureunit = xao_personunit.get_cultureunit(plan4_title)

#     assert plan1_cultureunit._manager_importance is None
#     assert plan2_cultureunit._manager_importance is None
#     assert plan3_cultureunit._manager_importance is None
#     assert plan4_cultureunit._manager_importance is None

#     # WHEN
#     xao_personunit.set_cultureunits_weight_metrics()

#     # THEN
#     # z_knee_painunit = xao_personunit.get_painunit(knee_genus)
#     # z_bore_painunit = xao_personunit.get_painunit(bore_genus)
#     # z_rain_painunit = xao_personunit.get_painunit(rain_genus)
#     # z_knee_tim_healerlink = z_knee_painunit.get_healerlink(tim_text)
#     # z_bore_tim_healerlink = z_bore_painunit.get_healerlink(tim_text)
#     # z_bore_sue_healerlink = z_bore_painunit.get_healerlink(sue_text)
#     # z_rain_ray_healerlink = z_rain_painunit.get_healerlink(ray_text)
#     # knee_tim_plan1_culturelink = z_knee_tim_healerlink.get_culturelink(plan1_title)
#     # bore_sue_plan2_culturelink = z_bore_sue_healerlink.get_culturelink(plan2_title)
#     # bore_sue_plan3_culturelink = z_bore_sue_healerlink.get_culturelink(plan3_title)
#     # bore_tim_plan3_culturelink = z_bore_tim_healerlink.get_culturelink(plan3_title)
#     # rain_ray_plan3_culturelink = z_rain_ray_healerlink.get_culturelink(plan3_title)
#     # assert knee_tim_plan1_culturelink._manager_importance == 0.6
#     # assert bore_sue_plan2_culturelink._manager_importance == 0.0112
#     # assert bore_sue_plan3_culturelink._manager_importance == 0.1288
#     # assert bore_tim_plan3_culturelink._manager_importance == 0.21
#     # assert rain_ray_plan3_culturelink._manager_importance == 0.05

#     assert plan1_cultureunit._manager_importance == 0.6
#     assert plan2_cultureunit._manager_importance == 0.0112
#     assert plan3_cultureunit._manager_importance == 0.3888
#     assert plan4_cultureunit._manager_importance == 0
