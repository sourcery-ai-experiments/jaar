from src._road.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
)
from src._road.belief import beliefunit_shop, opinionunit_shop


def get_cooking_beliefunit():
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
