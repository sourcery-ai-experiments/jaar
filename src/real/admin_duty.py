from src._instrument.file import set_dir
from src._road.jaar_config import init_change_id
from src._road.road import RoadUnit
from src.agenda.group import GroupID
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
)
from src.agenda.pledge import create_pledge
from src.change.filehub import filehub_shop, FileHub
from src.change.change import changeunit_shop, get_init_change_id_if_None
from src.real.admin_change import (
    _merge_changes_into_agenda,
    _create_new_changeunit,
)
from copy import deepcopy as copy_deepcopy


class Invalid_duty_Exception(Exception):
    pass


def _create_initial_change_from_duty(x_filehub: FileHub):
    x_changeunit = changeunit_shop(
        _giver=x_filehub.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_filehub.changes_dir(),
        _atoms_dir=x_filehub.atoms_dir(),
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_filehub),
        after_agenda=get_duty_file_agenda(x_filehub),
    )
    x_changeunit.save_files()


def get_duty_file_agenda(x_filehub: FileHub) -> AgendaUnit:
    x_filehub = filehub_shop(
        reals_dir=x_filehub.reals_dir,
        real_id=x_filehub.real_id,
        person_id=x_filehub.person_id,
        econ_road=None,
        road_delimiter=x_filehub.road_delimiter,
        planck=x_filehub.planck,
    )
    if x_filehub.duty_file_exists() == False:
        x_filehub.save_duty_agenda(get_default_duty_agenda(x_filehub))
    duty_json = x_filehub.open_file_duty()
    return agendaunit_get_from_json(duty_json)


def _create_duty_from_changes(x_filehub):
    x_agenda = _merge_changes_into_agenda(x_filehub, get_default_duty_agenda(x_filehub))
    x_filehub = filehub_shop(
        reals_dir=x_filehub.reals_dir,
        real_id=x_filehub.real_id,
        person_id=x_filehub.person_id,
        econ_road=None,
        road_delimiter=x_filehub.road_delimiter,
        planck=x_filehub.planck,
    )
    x_filehub.save_duty_agenda(x_agenda)


def get_default_duty_agenda(x_filehub: FileHub) -> AgendaUnit:
    x_agendaunit = agendaunit_shop(
        x_filehub.person_id,
        x_filehub.real_id,
        x_filehub.road_delimiter,
        x_filehub.planck,
    )
    x_agendaunit._last_change_id = init_change_id()
    return x_agendaunit


def initialize_change_duty_files(x_filehub: FileHub):
    set_dir(x_filehub.real_dir())
    set_dir(x_filehub.persons_dir())
    set_dir(x_filehub.person_dir())
    set_dir(x_filehub.atoms_dir())
    set_dir(x_filehub.changes_dir())
    x_duty_file_exists = x_filehub.duty_file_exists()
    change_file_exists = x_filehub.change_file_exists(init_change_id())
    if x_duty_file_exists == False and change_file_exists == False:
        _create_initial_change_and_duty_files(x_filehub)
    elif x_duty_file_exists == False and change_file_exists:
        _create_duty_from_changes(x_filehub)
    elif x_duty_file_exists and change_file_exists == False:
        _create_initial_change_from_duty(x_filehub)


def append_changes_to_duty_file(x_filehub: FileHub) -> AgendaUnit:
    duty_agenda = get_duty_file_agenda(x_filehub)
    duty_agenda = _merge_changes_into_agenda(x_filehub, duty_agenda)
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


def _create_initial_change_and_duty_files(x_filehub: FileHub):
    x_changeunit = changeunit_shop(
        _giver=x_filehub.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_filehub.changes_dir(),
        _atoms_dir=x_filehub.atoms_dir(),
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_filehub),
        after_agenda=get_default_duty_agenda(x_filehub),
    )
    x_changeunit.save_files()
    _create_duty_from_changes(x_filehub)


def add_pledge_change(x_filehub, pledge_road: RoadUnit, x_suffgroup: GroupID = None):
    duty_agenda = get_duty_file_agenda(x_filehub)
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_changeunit = _create_new_changeunit(x_filehub)
    next_changeunit._bookunit.add_all_different_agendaatoms(
        old_duty_agenda, duty_agenda
    )
    next_changeunit.save_files()
    append_changes_to_duty_file(x_filehub)
