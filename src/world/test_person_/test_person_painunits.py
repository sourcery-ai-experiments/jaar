from src.world.person import personunit_shop
from src.world.pain import painunit_shop, healerlink_shop, economylink_shop
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    worlds_dir_setup_cleanup,
)


def test_personunit_set_painunits_weight_metrics_SetsCorrectlyV1(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"{get_temp_world_dir()}/persons/{xao_text}"
    xao_personunit = personunit_shop(pid=xao_text, person_dir=xao_person_dir)

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


def test_personunit_set_painunits_weight_metrics_SetsCorrectlyV2(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    xao_text = "Xao"
    xao_person_dir = f"{get_temp_world_dir()}/persons/{xao_text}"
    xao_personunit = personunit_shop(pid=xao_text, person_dir=xao_person_dir)

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

    plan1_economy_id = "plan1"
    plan2_economy_id = "plan2"
    plan3_economy_id = "plan3"
    knee_tim_healerlink.set_economylink(economylink_shop(plan1_economy_id, 7))
    bore_sue_healerlink.set_economylink(economylink_shop(plan2_economy_id, 2))
    bore_sue_healerlink.set_economylink(economylink_shop(plan3_economy_id, 23))
    bore_tim_healerlink.set_economylink(economylink_shop(plan3_economy_id, 8))
    rain_ray_healerlink.set_economylink(economylink_shop(plan3_economy_id, 11))

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

    # FROM ECONOMYUNIT
    # def set_economyunits_weight_metrics(self):
    #     self.set_painunits_weight_metrics()
    #     economyunit_economy_ids = {
    #         x_economyunit.economy_id: 0 for x_economyunit in self._economys.values()
    #     }

    #     for x_painunit in self._pains.values():
    #         for x_healerlink in x_painunit._healerlinks.values():
    #             for x_economylink in x_healerlink._economylinks.values():
    #                 economyunit_economy_ids[
    #                     x_economylink.economy_id
    #                 ] += x_economylink._manager_importance


# def test_personunit_set_economyunits_weight_metrics_SetsCorrectly(
#     worlds_dir_setup_cleanup,
# ):
#     # GIVEN
#     xao_text = "Xao"
#     xao_person_dir = f"{get_temp_world_dir()}/persons/{xao_text}"
#     xao_personunit = personunit_shop(pid=xao_text, person_dir=xao_person_dir)

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

#     plan1_economy_id = "plan1"
#     plan2_economy_id = "plan2"
#     plan3_economy_id = "plan3"
#     plan4_economy_id = "plan4"
#     x_knee_tim_healerlink.set_economylink(economylink_shop(plan1_economy_id, 7))
#     x_bore_sue_healerlink.set_economylink(economylink_shop(plan2_economy_id, 2))
#     x_bore_sue_healerlink.set_economylink(economylink_shop(plan3_economy_id, 23))
#     x_bore_tim_healerlink.set_economylink(economylink_shop(plan3_economy_id, 8))
#     x_rain_ray_healerlink.set_economylink(economylink_shop(plan3_economy_id, 11))

#     x_knee_painunit.set_healerlink(x_knee_tim_healerlink)
#     x_bore_painunit.set_healerlink(x_bore_sue_healerlink)
#     x_bore_painunit.set_healerlink(x_bore_tim_healerlink)
#     x_rain_painunit.set_healerlink(x_rain_ray_healerlink)

#     xao_personunit.set_painunit(x_knee_painunit)
#     xao_personunit.set_painunit(x_bore_painunit)
#     xao_personunit.set_painunit(x_rain_painunit)

#     xao_personunit.set_economyunit(plan1_economy_id)
#     xao_personunit.set_economyunit(plan2_economy_id)
#     xao_personunit.set_economyunit(plan3_economy_id)
#     xao_personunit.set_economyunit(plan4_economy_id)

#     plan1_economyunit = xao_personunit.get_economyunit(plan1_economy_id)
#     plan2_economyunit = xao_personunit.get_economyunit(plan2_economy_id)
#     plan3_economyunit = xao_personunit.get_economyunit(plan3_economy_id)
#     plan4_economyunit = xao_personunit.get_economyunit(plan4_economy_id)

#     assert plan1_economyunit._manager_importance is None
#     assert plan2_economyunit._manager_importance is None
#     assert plan3_economyunit._manager_importance is None
#     assert plan4_economyunit._manager_importance is None

#     # WHEN
#     xao_personunit.set_economyunits_weight_metrics()

#     # THEN
#     # z_knee_painunit = xao_personunit.get_painunit(knee_genus)
#     # z_bore_painunit = xao_personunit.get_painunit(bore_genus)
#     # z_rain_painunit = xao_personunit.get_painunit(rain_genus)
#     # z_knee_tim_healerlink = z_knee_painunit.get_healerlink(tim_text)
#     # z_bore_tim_healerlink = z_bore_painunit.get_healerlink(tim_text)
#     # z_bore_sue_healerlink = z_bore_painunit.get_healerlink(sue_text)
#     # z_rain_ray_healerlink = z_rain_painunit.get_healerlink(ray_text)
#     # knee_tim_plan1_economylink = z_knee_tim_healerlink.get_economylink(plan1_economy_id)
#     # bore_sue_plan2_economylink = z_bore_sue_healerlink.get_economylink(plan2_economy_id)
#     # bore_sue_plan3_economylink = z_bore_sue_healerlink.get_economylink(plan3_economy_id)
#     # bore_tim_plan3_economylink = z_bore_tim_healerlink.get_economylink(plan3_economy_id)
#     # rain_ray_plan3_economylink = z_rain_ray_healerlink.get_economylink(plan3_economy_id)
#     # assert knee_tim_plan1_economylink._manager_importance == 0.6
#     # assert bore_sue_plan2_economylink._manager_importance == 0.0112
#     # assert bore_sue_plan3_economylink._manager_importance == 0.1288
#     # assert bore_tim_plan3_economylink._manager_importance == 0.21
#     # assert rain_ray_plan3_economylink._manager_importance == 0.05

#     assert plan1_economyunit._manager_importance == 0.6
#     assert plan2_economyunit._manager_importance == 0.0112
#     assert plan3_economyunit._manager_importance == 0.3888
#     assert plan4_economyunit._manager_importance == 0
