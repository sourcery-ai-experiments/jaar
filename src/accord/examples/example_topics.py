from src._prime.road import create_road, create_economyaddress
from src.accord.accord import dueunit_shop, DueUnit
from src.accord.topic import (
    topicunit_shop,
    opinionunit_shop,
    TopicUnit,
    topiclink_shop,
)


def get_cooking_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    cook_road = create_road(yao_economyaddress, "cooking")
    cook_topic = topicunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    fresh_road = create_road(cook_road, "farm fresh")
    resin_road = create_road(cook_road, "plastic pots")
    metal_road = create_road(cook_road, "metal pots")
    fresh_opinion = opinionunit_shop(fresh_road, affect=3)
    cheap_opinion = opinionunit_shop(cheap_road, affect=-2)
    metal_opinion = opinionunit_shop(metal_road, affect=7)
    resin_opinion = opinionunit_shop(resin_road, affect=-5)
    cook_topic.set_opinionunit(cheap_opinion)
    cook_topic.set_opinionunit(fresh_opinion)
    cook_topic.set_opinionunit(resin_opinion)
    cook_topic.set_opinionunit(metal_opinion)
    return cook_topic


def get_climate_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    climate_road = create_road(yao_economyaddress, "climate")
    climate_topic = topicunit_shop(climate_road)

    crazy_road = create_road(climate_road, "crazy weather")
    usual_road = create_road(climate_road, "usual weather")
    crazy_opinion = opinionunit_shop(crazy_road, affect=-2)
    usual_opinion = opinionunit_shop(usual_road, affect=3)
    climate_topic.set_opinionunit(crazy_opinion)
    climate_topic.set_opinionunit(usual_opinion)
    return climate_topic


def get_speedboats_action_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    climate_road = create_road(yao_economyaddress, "speedboats")
    climate_topic = topicunit_shop(climate_road, action=True)

    stop_road = create_road(climate_road, "stop using")
    keep_road = create_road(climate_road, "keep using")
    stop_opinion = opinionunit_shop(stop_road, affect=3)
    keep_opinion = opinionunit_shop(keep_road, affect=-5)
    climate_topic.set_opinionunit(stop_opinion)
    climate_topic.set_opinionunit(keep_opinion)
    return climate_topic


def get_gasheater_action_topic() -> TopicUnit:
    """is_meaningful=False"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    gasheater_road = create_road(yao_economyaddress, "home gas heaters")
    gasheater_topic = topicunit_shop(gasheater_road, action=True)

    keep_road = create_road(gasheater_road, "keep using")
    keep_opinion = opinionunit_shop(keep_road, affect=3)
    gasheater_topic.set_opinionunit(keep_opinion)
    return gasheater_topic


def get_childcare_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    family_road = create_road(yao_economyaddress, "family")
    childcare_road = create_road(family_road, "childcare")
    childcare_topic = topicunit_shop(childcare_road)

    school_road = create_road(childcare_road, "school most beneficial for kids")
    home_road = create_road(childcare_road, "home most beneficial for kids")
    school_opinion = opinionunit_shop(school_road, affect=3)
    home_opinion = opinionunit_shop(home_road, affect=-4)
    childcare_topic.set_opinionunit(school_opinion)
    childcare_topic.set_opinionunit(home_opinion)
    return childcare_topic


def get_helen_action_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Aubri", "Oregon")
    psu_road = create_road(yao_economyaddress, "PSU")
    helen_road = create_road(psu_road, "Helen Gordon")
    helen_topic = topicunit_shop(helen_road, action=True)

    in_school_road = create_road(helen_road, "kids in school")
    no_school_road = create_road(helen_road, "kids not in school")
    in_school_opinion = opinionunit_shop(in_school_road, affect=3)
    no_school_opinion = opinionunit_shop(no_school_road, affect=-4)
    helen_topic.set_opinionunit(in_school_opinion)
    helen_topic.set_opinionunit(no_school_opinion)
    return helen_topic


def get_cooking_dueunit() -> DueUnit:
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    cook_road = create_road(yao_economyaddress, "cooking")
    eight_uid = 8
    eight_dueunit = dueunit_shop(uid=eight_uid)
    eight_dueunit.set_topiclink(topiclink_shop(cook_road))
    return eight_dueunit


def get_climate_dueunit() -> DueUnit:
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    climate_road = create_road(yao_economyaddress, "climate")
    six_uid = 6
    six_dueunit = dueunit_shop(uid=six_uid)
    six_dueunit.set_topiclink(topiclink_shop(climate_road))
    return six_dueunit


def get_speedboat_action_dueunit() -> DueUnit:
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    speedboat_road = create_road(yao_economyaddress, "speedboats")
    seven_uid = 7
    seven_dueunit = dueunit_shop(uid=seven_uid)
    seven_dueunit.set_topiclink(topiclink_shop(speedboat_road, action=True))
    return seven_dueunit
