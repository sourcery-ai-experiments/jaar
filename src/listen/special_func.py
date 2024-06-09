from src._road.road import RoadUnit
from src.agenda.group import GroupID
from src.agenda.pledge import create_pledge
from src.listen.filehub import FileHub
from copy import deepcopy as copy_deepcopy


def add_pledge_atom(
    x_filehub: FileHub, pledge_road: RoadUnit, x_suffgroup: GroupID = None
):
    duty_agenda = x_filehub.get_duty_agenda()
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_atomunit = x_filehub._default_atomunit()
    next_atomunit._nucunit.add_all_different_quarkunits(old_duty_agenda, duty_agenda)
    next_atomunit.save_files()
    x_filehub.append_atoms_to_duty_file()
