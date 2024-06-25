from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src._world.belief import BeliefID
from src._world.world import WorldUnit
from src.listen.userhub import UserHub
from copy import deepcopy as copy_deepcopy


def create_pledge(
    x_world: WorldUnit,
    pledge_road: RoadUnit,
    x_suffbelief: BeliefID = None,
    reason_premise: RoadUnit = None,
):
    if pledge_road is not None and get_terminus_node(pledge_road) != "":
        x_idea = x_world.get_idea_obj(pledge_road, if_missing_create=True)
        x_idea.pledge = True
        x_idea._assignedunit.set_suffbelief(x_suffbelief)

        if x_world.get_beliefunit(x_suffbelief) is None:
            x_world.add_otherunit(x_suffbelief)

        if reason_premise != None:
            if x_world.idea_exists(reason_premise) is False:
                x_world.get_idea_obj(reason_premise, if_missing_create=True)
            reason_base = get_parent_road(reason_premise)
            x_world.edit_reason(pledge_road, reason_base, reason_premise)


def add_same_pledge(
    x_userhub: UserHub,
    pledge_road: RoadUnit,
    x_suffbelief: BeliefID = None,
    reason_premise: RoadUnit = None,
):
    same_world = x_userhub.get_same_world()
    old_same_world = copy_deepcopy(same_world)
    create_pledge(same_world, pledge_road, x_suffbelief, reason_premise)
    next_giftunit = x_userhub._default_giftunit()
    next_giftunit._changeunit.add_all_different_atomunits(old_same_world, same_world)
    next_giftunit.save_files()
    x_userhub.append_gifts_to_same_file()


def create_fact(x_world: WorldUnit, fact_pick: RoadUnit):
    if x_world.idea_exists(fact_pick) is False:
        x_world.get_idea_obj(fact_pick, if_missing_create=True)
    fact_base = get_parent_road(fact_pick)
    x_world.set_fact(fact_base, fact_pick)


def add_same_fact(x_userhub: UserHub, fact_pick: RoadUnit):
    same_world = x_userhub.get_same_world()
    old_same_world = copy_deepcopy(same_world)
    create_fact(same_world, fact_pick)
    next_giftunit = x_userhub._default_giftunit()
    next_giftunit._changeunit.add_all_different_atomunits(old_same_world, same_world)
    next_giftunit.save_files()
    x_userhub.append_gifts_to_same_file()
