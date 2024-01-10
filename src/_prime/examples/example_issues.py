from src._prime.road import (
    create_road,
    create_economyaddress,
)
from src._prime.issue import issueunit_shop, factunit_shop, IssueUnit


def get_cooking_issue() -> IssueUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    cook_road = create_road(yao_economyaddress, "cooking")
    cook_issue = issueunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    fresh_road = create_road(cook_road, "farm fresh")
    resin_road = create_road(cook_road, "plastic pots")
    metal_road = create_road(cook_road, "metal pots")
    fresh_fact = factunit_shop(fresh_road, affect=3)
    cheap_fact = factunit_shop(cheap_road, affect=-2)
    metal_fact = factunit_shop(metal_road, affect=7)
    resin_fact = factunit_shop(resin_road, affect=-5)
    cook_issue.set_factunit(cheap_fact)
    cook_issue.set_factunit(fresh_fact)
    cook_issue.set_factunit(resin_fact)
    cook_issue.set_factunit(metal_fact)
    return cook_issue


def get_climate_issue() -> IssueUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    climate_road = create_road(yao_economyaddress, "climate")
    climate_issue = issueunit_shop(climate_road)

    crazy_road = create_road(climate_road, "crazy weather")
    usual_road = create_road(climate_road, "usual weather")
    crazy_fact = factunit_shop(crazy_road, affect=-2)
    usual_fact = factunit_shop(usual_road, affect=3)
    climate_issue.set_factunit(crazy_fact)
    climate_issue.set_factunit(usual_fact)
    return climate_issue


def get_speedboats_action_issue() -> IssueUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    climate_road = create_road(yao_economyaddress, "speedboats")
    climate_issue = issueunit_shop(climate_road, action=True)

    stop_road = create_road(climate_road, "stop using")
    keep_road = create_road(climate_road, "keep using")
    stop_fact = factunit_shop(stop_road, affect=3)
    keep_fact = factunit_shop(keep_road, affect=-5)
    climate_issue.set_factunit(stop_fact)
    climate_issue.set_factunit(keep_fact)
    return climate_issue


def get_gasheater_action_issue() -> IssueUnit:
    """is_meaningful=False"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    gasheater_road = create_road(yao_economyaddress, "home gas heaters")
    gasheater_issue = issueunit_shop(gasheater_road, action=True)

    keep_road = create_road(gasheater_road, "keep using")
    keep_fact = factunit_shop(keep_road, affect=3)
    gasheater_issue.set_factunit(keep_fact)
    return gasheater_issue


def get_childcare_issue() -> IssueUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Yao", "Texas")
    family_road = create_road(yao_economyaddress, "family")
    childcare_road = create_road(family_road, "childcare")
    childcare_issue = issueunit_shop(childcare_road)

    school_road = create_road(childcare_road, "school most beneficial for kids")
    home_road = create_road(childcare_road, "home most beneficial for kids")
    school_fact = factunit_shop(school_road, affect=3)
    home_fact = factunit_shop(home_road, affect=-4)
    childcare_issue.set_factunit(school_fact)
    childcare_issue.set_factunit(home_fact)
    return childcare_issue


def get_helen_action_issue() -> IssueUnit:
    """is_meaningful=True"""
    yao_economyaddress = create_economyaddress("Aubri", "Oregon")
    psu_road = create_road(yao_economyaddress, "PSU")
    helen_road = create_road(psu_road, "Helen Gordon")
    helen_issue = issueunit_shop(helen_road, action=True)

    in_school_road = create_road(helen_road, "kids in school")
    no_school_road = create_road(helen_road, "kids not in school")
    in_school_fact = factunit_shop(in_school_road, affect=3)
    no_school_fact = factunit_shop(no_school_road, affect=-4)
    helen_issue.set_factunit(in_school_fact)
    helen_issue.set_factunit(no_school_fact)
    return helen_issue
