from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
)
from src._prime.belief import beliefunit_shop, opinionunit_shop


def get_cooking_belief():
    cook_road = create_road(root_label(), "cooking")
    cook_belief = beliefunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    fresh_road = create_road(cook_road, "farm fresh")
    resin_road = create_road(cook_road, "plastic pots")
    metal_road = create_road(cook_road, "metal pots")
    fresh_opinion = opinionunit_shop(fresh_road, affect=3)
    cheap_opinion = opinionunit_shop(cheap_road, affect=-2)
    metal_opinion = opinionunit_shop(metal_road, affect=7)
    resin_opinion = opinionunit_shop(resin_road, affect=-5)
    cook_belief.set_opinionunit(cheap_opinion)
    cook_belief.set_opinionunit(fresh_opinion)
    cook_belief.set_opinionunit(resin_opinion)
    cook_belief.set_opinionunit(metal_opinion)
    return cook_belief


def get_climate_belief():
    climate_road = create_road(root_label(), "climate")
    climate_belief = beliefunit_shop(climate_road)
    crazy_road = create_road(climate_road, "crazy weather")
    normal_road = create_road(climate_road, "normal weather")
    crazy_opinion = opinionunit_shop(crazy_road, affect=-2)
    normal_opinion = opinionunit_shop(normal_road, affect=3)
    climate_belief.set_opinionunit(crazy_opinion)
    climate_belief.set_opinionunit(normal_opinion)
    return climate_belief


def get_speedboats_action_belief():
    climate_road = create_road(root_label(), "speedboats")
    climate_belief = beliefunit_shop(climate_road, action=True)
    stop_road = create_road(climate_road, "stop using")
    keep_road = create_road(climate_road, "keep using")
    stop_opinion = opinionunit_shop(stop_road, affect=3)
    keep_opinion = opinionunit_shop(keep_road, affect=-5)
    climate_belief.set_opinionunit(stop_opinion)
    climate_belief.set_opinionunit(keep_opinion)
    return climate_belief
