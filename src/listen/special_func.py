from src._road.road import RoadUnit, get_terminus_node
from src.agenda.group import GroupID
from src.agenda.agenda import AgendaUnit
from src.listen.userhub import UserHub
from copy import deepcopy as copy_deepcopy


def create_pledge(
    x_agenda: AgendaUnit, pledge_road: RoadUnit, x_suffgroup: GroupID = None
):
    if pledge_road is not None and get_terminus_node(pledge_road) != "":
        x_idea = x_agenda.get_idea_obj(pledge_road, if_missing_create=True)
        x_idea.pledge = True
        x_idea._assignedunit.set_suffgroup(x_suffgroup)

        if x_agenda.get_groupunit(x_suffgroup) is None:
            x_agenda.add_partyunit(x_suffgroup)


def add_pledge_atom(
    x_userhub: UserHub, pledge_road: RoadUnit, x_suffgroup: GroupID = None
):
    duty_agenda = x_userhub.get_duty_agenda()
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_atomunit = x_userhub._default_atomunit()
    next_atomunit._nucunit.add_all_different_quarkunits(old_duty_agenda, duty_agenda)
    next_atomunit.save_files()
    x_userhub.append_atoms_to_duty_file()
