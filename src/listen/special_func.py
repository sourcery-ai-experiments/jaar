from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src._truth.belief import BeliefID
from src._truth.truth import TruthUnit
from src.listen.userhub import UserHub
from copy import deepcopy as copy_deepcopy


def create_pledge(
    x_truth: TruthUnit,
    pledge_road: RoadUnit,
    x_suffbelief: BeliefID = None,
    reason_premise: RoadUnit = None,
):
    if pledge_road is not None and get_terminus_node(pledge_road) != "":
        x_idea = x_truth.get_idea_obj(pledge_road, if_missing_create=True)
        x_idea.pledge = True
        x_idea._assignedunit.set_suffbelief(x_suffbelief)

        if x_truth.get_beliefunit(x_suffbelief) is None:
            x_truth.add_otherunit(x_suffbelief)

        if reason_premise != None:
            if x_truth.idea_exists(reason_premise) is False:
                x_truth.get_idea_obj(reason_premise, if_missing_create=True)
            reason_base = get_parent_road(reason_premise)
            x_truth.edit_reason(pledge_road, reason_base, reason_premise)


def add_same_pledge(
    x_userhub: UserHub,
    pledge_road: RoadUnit,
    x_suffbelief: BeliefID = None,
    reason_premise: RoadUnit = None,
):
    same_truth = x_userhub.get_same_truth()
    old_same_truth = copy_deepcopy(same_truth)
    create_pledge(same_truth, pledge_road, x_suffbelief, reason_premise)
    next_atomunit = x_userhub._default_atomunit()
    next_atomunit._nucunit.add_all_different_quarkunits(old_same_truth, same_truth)
    next_atomunit.save_files()
    x_userhub.append_atoms_to_same_file()


def create_fact(x_truth: TruthUnit, fact_pick: RoadUnit):
    if x_truth.idea_exists(fact_pick) is False:
        x_truth.get_idea_obj(fact_pick, if_missing_create=True)
    fact_base = get_parent_road(fact_pick)
    x_truth.set_fact(fact_base, fact_pick)


def add_same_fact(x_userhub: UserHub, fact_pick: RoadUnit):
    same_truth = x_userhub.get_same_truth()
    old_same_truth = copy_deepcopy(same_truth)
    create_fact(same_truth, fact_pick)
    next_atomunit = x_userhub._default_atomunit()
    next_atomunit._nucunit.add_all_different_quarkunits(old_same_truth, same_truth)
    next_atomunit.save_files()
    x_userhub.append_atoms_to_same_file()
