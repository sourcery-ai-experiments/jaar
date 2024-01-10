from src._prime.road import (
    create_road,
    create_economyaddress,
)
from src._prime.topic import topicunit_shop, factunit_shop, TopicUnit


def get_cooking_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    cook_road = create_road(yao_economyaddress, "cooking")
    cook_topic = topicunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    fresh_road = create_road(cook_road, "farm fresh")
    resin_road = create_road(cook_road, "plastic pots")
    metal_road = create_road(cook_road, "metal pots")
    fresh_fact = factunit_shop(fresh_road, affect=3)
    cheap_fact = factunit_shop(cheap_road, affect=-2)
    metal_fact = factunit_shop(metal_road, affect=7)
    resin_fact = factunit_shop(resin_road, affect=-5)
    cook_topic.set_factunit(cheap_fact)
    cook_topic.set_factunit(fresh_fact)
    cook_topic.set_factunit(resin_fact)
    cook_topic.set_factunit(metal_fact)
    return cook_topic


def get_climate_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    climate_road = create_road(yao_economyaddress, "climate")
    climate_topic = topicunit_shop(climate_road)

    crazy_road = create_road(climate_road, "crazy weather")
    usual_road = create_road(climate_road, "usual weather")
    crazy_fact = factunit_shop(crazy_road, affect=-2)
    usual_fact = factunit_shop(usual_road, affect=3)
    climate_topic.set_factunit(crazy_fact)
    climate_topic.set_factunit(usual_fact)
    return climate_topic


def get_speedboats_action_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    climate_road = create_road(yao_economyaddress, "speedboats")
    climate_topic = topicunit_shop(climate_road, action=True)

    stop_road = create_road(climate_road, "stop using")
    keep_road = create_road(climate_road, "keep using")
    stop_fact = factunit_shop(stop_road, affect=3)
    keep_fact = factunit_shop(keep_road, affect=-5)
    climate_topic.set_factunit(stop_fact)
    climate_topic.set_factunit(keep_fact)
    return climate_topic


def get_gasheater_action_topic() -> TopicUnit:
    """is_meaningful=False"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    gasheater_road = create_road(yao_economyaddress, "home gas heaters")
    gasheater_topic = topicunit_shop(gasheater_road, action=True)

    keep_road = create_road(gasheater_road, "keep using")
    keep_fact = factunit_shop(keep_road, affect=3)
    gasheater_topic.set_factunit(keep_fact)
    return gasheater_topic


def get_childcare_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    family_road = create_road(yao_economyaddress, "family")
    childcare_road = create_road(family_road, "childcare")
    childcare_topic = topicunit_shop(childcare_road)

    school_road = create_road(childcare_road, "school most beneficial for kids")
    home_road = create_road(childcare_road, "home most beneficial for kids")
    school_fact = factunit_shop(school_road, affect=3)
    home_fact = factunit_shop(home_road, affect=-4)
    childcare_topic.set_factunit(school_fact)
    childcare_topic.set_factunit(home_fact)
    return childcare_topic


def get_helen_action_topic() -> TopicUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Aubri", "Oregon")
    psu_road = create_road(yao_economyaddress, "PSU")
    helen_road = create_road(psu_road, "Helen Gordon")
    helen_topic = topicunit_shop(helen_road, action=True)

    in_school_road = create_road(helen_road, "kids in school")
    no_school_road = create_road(helen_road, "kids not in school")
    in_school_fact = factunit_shop(in_school_road, affect=3)
    no_school_fact = factunit_shop(no_school_road, affect=-4)
    helen_topic.set_factunit(in_school_fact)
    helen_topic.set_factunit(no_school_fact)
    return helen_topic
