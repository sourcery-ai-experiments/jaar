from src._road.jaar_config import init_change_id
from src._road.road import RoadUnit
from src.agenda.group import GroupID
from src.agenda.agenda import AgendaUnit
from src.agenda.pledge import create_pledge
from src.change.filehub import filehub_shop, FileHub
from copy import deepcopy as copy_deepcopy


class Invalid_duty_Exception(Exception):
    pass


def initialize_change_duty_files(x_filehub: FileHub):
    x_duty_file_exists = x_filehub.duty_file_exists()
    change_file_exists = x_filehub.change_file_exists(init_change_id())
    if x_duty_file_exists == False and change_file_exists == False:
        x_filehub._create_initial_change_and_duty_files()
    elif x_duty_file_exists == False and change_file_exists:
        x_filehub._create_duty_from_changes()
    elif x_duty_file_exists and change_file_exists == False:
        x_filehub._create_initial_change_files_from_duty()


def append_changes_to_duty_file(x_filehub: FileHub) -> AgendaUnit:
    duty_agenda = x_filehub.get_duty_agenda()
    duty_agenda = x_filehub._merge_any_changes(duty_agenda)
    x_filehub = filehub_shop(
        reals_dir=x_filehub.reals_dir,
        real_id=x_filehub.real_id,
        person_id=x_filehub.person_id,
        econ_road=None,
        road_delimiter=x_filehub.road_delimiter,
        planck=x_filehub.planck,
    )
    x_filehub.save_duty_agenda(duty_agenda)
    return x_filehub.get_duty_agenda()


def add_pledge_change(x_filehub, pledge_road: RoadUnit, x_suffgroup: GroupID = None):
    duty_agenda = x_filehub.get_duty_agenda()
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_changeunit = x_filehub._default_changeunit()
    next_changeunit._bookunit.add_all_different_agendaatoms(
        old_duty_agenda, duty_agenda
    )
    next_changeunit.save_files()
    append_changes_to_duty_file(x_filehub)
