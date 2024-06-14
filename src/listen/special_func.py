from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src.agenda.idea import IdeaID
from src.agenda.agenda import AgendaUnit
from src.listen.userhub import UserHub
from copy import deepcopy as copy_deepcopy


def create_pledge(
    x_agenda: AgendaUnit,
    pledge_road: RoadUnit,
    x_suffidea: IdeaID = None,
    reason_premise: RoadUnit = None,
):
    if pledge_road is not None and get_terminus_node(pledge_road) != "":
        x_fact = x_agenda.get_fact_obj(pledge_road, if_missing_create=True)
        x_fact.pledge = True
        x_fact._assignedunit.set_suffidea(x_suffidea)

        if x_agenda.get_ideaunit(x_suffidea) is None:
            x_agenda.add_partyunit(x_suffidea)

        if reason_premise != None:
            if x_agenda.fact_exists(reason_premise) is False:
                x_agenda.get_fact_obj(reason_premise, if_missing_create=True)
            reason_base = get_parent_road(reason_premise)
            x_agenda.edit_reason(pledge_road, reason_base, reason_premise)


def add_duty_pledge(
    x_userhub: UserHub,
    pledge_road: RoadUnit,
    x_suffidea: IdeaID = None,
    reason_premise: RoadUnit = None,
):
    duty_agenda = x_userhub.get_duty_agenda()
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffidea, reason_premise)
    next_atomunit = x_userhub._default_atomunit()
    next_atomunit._nucunit.add_all_different_quarkunits(old_duty_agenda, duty_agenda)
    next_atomunit.save_files()
    x_userhub.append_atoms_to_duty_file()


def create_belief(x_agenda: AgendaUnit, belief_pick: RoadUnit):
    if x_agenda.fact_exists(belief_pick) is False:
        x_agenda.get_fact_obj(belief_pick, if_missing_create=True)
    belief_base = get_parent_road(belief_pick)
    x_agenda.set_belief(belief_base, belief_pick)


def add_duty_belief(x_userhub: UserHub, belief_pick: RoadUnit):
    duty_agenda = x_userhub.get_duty_agenda()
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_belief(duty_agenda, belief_pick)
    next_atomunit = x_userhub._default_atomunit()
    next_atomunit._nucunit.add_all_different_quarkunits(old_duty_agenda, duty_agenda)
    next_atomunit.save_files()
    x_userhub.append_atoms_to_duty_file()
