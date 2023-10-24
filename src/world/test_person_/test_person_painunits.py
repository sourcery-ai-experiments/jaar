from src.world.person import personunit_shop
from src.world.pain import painunit_shop, healerlink_shop, culturelink_shop
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

    xao_personunit.set_painunit(painunit_shop(genus=fear_text, weight=60))
    xao_personunit.set_painunit(painunit_shop(genus=bore_text, weight=35))
    xao_personunit.set_painunit(painunit_shop(genus=rain_text, weight=5))

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
    assert fear_painunit._manager_importance == 0.6
    assert bore_painunit._manager_importance == 0.35
    assert rain_painunit._manager_importance == 0.05


def test_personunit_set_painunits_weight_metrics_SetsCorrectly(env_dir_setup_cleanup):
    # GIVEN
    xao_name = "Xao"
    xao_person_dir = f"{get_temp_env_dir}/persons/{xao_name}"
    xao_personunit = personunit_shop(name=xao_name, person_dir=xao_person_dir)

    fear_genus = "fear"
    bore_genus = "bore"
    rain_genus = "rain"

    x_fear_painunit = painunit_shop(fear_genus, 60)
    x_bore_painunit = painunit_shop(bore_genus, 35)
    x_rain_painunit = painunit_shop(rain_genus, 5)

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
    fear_tim_healerlink.set_culturelink(culturelink_shop(plan1_handle, 7))
    bore_sue_healerlink.set_culturelink(culturelink_shop(plan2_handle, 2))
    bore_sue_healerlink.set_culturelink(culturelink_shop(plan3_handle, 23))
    bore_tim_healerlink.set_culturelink(culturelink_shop(plan3_handle, 8))
    rain_ray_healerlink.set_culturelink(culturelink_shop(plan3_handle, 11))

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
    z_fear_painunit = xao_personunit.get_painunit(fear_genus)
    z_bore_painunit = xao_personunit.get_painunit(bore_genus)
    z_rain_painunit = xao_personunit.get_painunit(rain_genus)
    assert z_fear_painunit._relative_weight == 0.6
    assert z_bore_painunit._relative_weight == 0.35
    assert z_rain_painunit._relative_weight == 0.05
    assert z_fear_painunit._manager_importance == 0.6
    assert z_bore_painunit._manager_importance == 0.35
    assert z_rain_painunit._manager_importance == 0.05

    z_fear_tim_healerlink = z_fear_painunit.get_healerlink(tim_text)
    z_bore_tim_healerlink = z_bore_painunit.get_healerlink(tim_text)
    z_bore_sue_healerlink = z_bore_painunit.get_healerlink(sue_text)
    z_rain_ray_healerlink = z_rain_painunit.get_healerlink(ray_text)

    assert z_fear_tim_healerlink._manager_importance == 0.6
    assert z_bore_tim_healerlink._manager_importance == 0.21
    assert z_bore_sue_healerlink._manager_importance < 0.14
    assert z_bore_sue_healerlink._manager_importance > 0.139999
    assert z_rain_ray_healerlink._manager_importance == 0.05

    fear_tim_plan1_culturelink = z_fear_tim_healerlink.get_culturelink(plan1_handle)
    bore_sue_plan2_culturelink = z_bore_sue_healerlink.get_culturelink(plan2_handle)
    bore_sue_plan3_culturelink = z_bore_sue_healerlink.get_culturelink(plan3_handle)
    bore_tim_plan3_culturelink = z_bore_tim_healerlink.get_culturelink(plan3_handle)
    rain_ray_plan3_culturelink = z_rain_ray_healerlink.get_culturelink(plan3_handle)

    assert fear_tim_plan1_culturelink._manager_importance == 0.6
    assert bore_sue_plan2_culturelink._manager_importance == 0.0112
    assert bore_sue_plan3_culturelink._manager_importance == 0.1288
    assert bore_tim_plan3_culturelink._manager_importance == 0.21
    assert rain_ray_plan3_culturelink._manager_importance == 0.05

    # FROM CULTUREUNIT
    # def set_cultureunits_weight_metrics(self):
    #     self.set_painunits_weight_metrics()
    #     cultureunit_handles = {
    #         x_cultureunit.handle: 0 for x_cultureunit in self._cultures.values()
    #     }

    #     for x_painunit in self._pains.values():
    #         for x_healerlink in x_painunit._healerlinks.values():
    #             for x_culturelink in x_healerlink._culturelinks.values():
    #                 cultureunit_handles[
    #                     x_culturelink.handle
    #                 ] += x_culturelink._manager_importance


# def test_personunit_set_cultureunits_weight_metrics_SetsCorrectly(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     xao_name = "Xao"
#     xao_person_dir = f"{get_temp_env_dir()}/persons/{xao_name}"
#     xao_personunit = personunit_shop(name=xao_name, person_dir=xao_person_dir)

#     fear_genus = "fear"
#     bore_genus = "bore"
#     rain_genus = "rain"

#     x_fear_painunit = painunit_shop(fear_genus, 60)
#     x_bore_painunit = painunit_shop(bore_genus, 35)
#     x_rain_painunit = painunit_shop(rain_genus, 5)

#     tim_text = "Tim"
#     sue_text = "Sue"
#     ray_text = "Ray"
#     x_fear_tim_healerlink = healerlink_shop(tim_text, weight=10)
#     x_bore_sue_healerlink = healerlink_shop(sue_text, weight=2)
#     x_bore_tim_healerlink = healerlink_shop(tim_text, weight=3)
#     x_rain_ray_healerlink = healerlink_shop(ray_text, weight=5)

#     plan1_handle = "plan1"
#     plan2_handle = "plan2"
#     plan3_handle = "plan3"
#     plan4_handle = "plan4"
#     x_fear_tim_healerlink.set_culturelink(culturelink_shop(plan1_handle, 7))
#     x_bore_sue_healerlink.set_culturelink(culturelink_shop(plan2_handle, 2))
#     x_bore_sue_healerlink.set_culturelink(culturelink_shop(plan3_handle, 23))
#     x_bore_tim_healerlink.set_culturelink(culturelink_shop(plan3_handle, 8))
#     x_rain_ray_healerlink.set_culturelink(culturelink_shop(plan3_handle, 11))

#     x_fear_painunit.set_healerlink(x_fear_tim_healerlink)
#     x_bore_painunit.set_healerlink(x_bore_sue_healerlink)
#     x_bore_painunit.set_healerlink(x_bore_tim_healerlink)
#     x_rain_painunit.set_healerlink(x_rain_ray_healerlink)

#     xao_personunit.set_painunit(x_fear_painunit)
#     xao_personunit.set_painunit(x_bore_painunit)
#     xao_personunit.set_painunit(x_rain_painunit)

#     xao_personunit.set_cultureunit(plan1_handle)
#     xao_personunit.set_cultureunit(plan2_handle)
#     xao_personunit.set_cultureunit(plan3_handle)
#     xao_personunit.set_cultureunit(plan4_handle)

#     plan1_cultureunit = xao_personunit.get_cultureunit(plan1_handle)
#     plan2_cultureunit = xao_personunit.get_cultureunit(plan2_handle)
#     plan3_cultureunit = xao_personunit.get_cultureunit(plan3_handle)
#     plan4_cultureunit = xao_personunit.get_cultureunit(plan4_handle)

#     assert plan1_cultureunit._manager_importance is None
#     assert plan2_cultureunit._manager_importance is None
#     assert plan3_cultureunit._manager_importance is None
#     assert plan4_cultureunit._manager_importance is None

#     # WHEN
#     xao_personunit.set_cultureunits_weight_metrics()

#     # THEN
#     # z_fear_painunit = xao_personunit.get_painunit(fear_genus)
#     # z_bore_painunit = xao_personunit.get_painunit(bore_genus)
#     # z_rain_painunit = xao_personunit.get_painunit(rain_genus)
#     # z_fear_tim_healerlink = z_fear_painunit.get_healerlink(tim_text)
#     # z_bore_tim_healerlink = z_bore_painunit.get_healerlink(tim_text)
#     # z_bore_sue_healerlink = z_bore_painunit.get_healerlink(sue_text)
#     # z_rain_ray_healerlink = z_rain_painunit.get_healerlink(ray_text)
#     # fear_tim_plan1_culturelink = z_fear_tim_healerlink.get_culturelink(plan1_handle)
#     # bore_sue_plan2_culturelink = z_bore_sue_healerlink.get_culturelink(plan2_handle)
#     # bore_sue_plan3_culturelink = z_bore_sue_healerlink.get_culturelink(plan3_handle)
#     # bore_tim_plan3_culturelink = z_bore_tim_healerlink.get_culturelink(plan3_handle)
#     # rain_ray_plan3_culturelink = z_rain_ray_healerlink.get_culturelink(plan3_handle)
#     # assert fear_tim_plan1_culturelink._manager_importance == 0.6
#     # assert bore_sue_plan2_culturelink._manager_importance == 0.0112
#     # assert bore_sue_plan3_culturelink._manager_importance == 0.1288
#     # assert bore_tim_plan3_culturelink._manager_importance == 0.21
#     # assert rain_ray_plan3_culturelink._manager_importance == 0.05

#     assert plan1_cultureunit._manager_importance == 0.6
#     assert plan2_cultureunit._manager_importance == 0.0112
#     assert plan3_cultureunit._manager_importance == 0.3888
#     assert plan4_cultureunit._manager_importance == 0
