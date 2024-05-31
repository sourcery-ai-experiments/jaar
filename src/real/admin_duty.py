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
from src.agenda.change import changeunit_shop, get_init_change_id_if_None
from src.real.admin_change import (
    changeunit_file_exists,
    _merge_changes_into_agenda,
    _create_new_changeunit,
)
from src._road.worldnox import UserNox
from copy import deepcopy as copy_deepcopy


class Invalid_duty_Exception(Exception):
    pass


def _create_initial_change_from_duty(x_usernox: UserNox):
    x_changeunit = changeunit_shop(
        _giver=x_usernox.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_usernox.changes_dir(),
        _atoms_dir=x_usernox.atoms_dir(),
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_usernox),
        after_agenda=get_duty_file_agenda(x_usernox),
    )
    x_changeunit.save_files()


def save_duty_file(x_usernox: UserNox, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_usernox.person_id:
        raise Invalid_duty_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_usernox.person_id}''s duty agenda."
        )
    if replace in {True, False}:
        x_usernox.save_file_duty(x_agenda.get_json(), replace)


def get_duty_file_agenda(x_usernox: UserNox) -> AgendaUnit:
    if x_usernox.duty_file_exists() == False:
        save_duty_file(x_usernox, get_default_duty_agenda(x_usernox))
    duty_json = x_usernox.open_file_duty()
    return agendaunit_get_from_json(duty_json)


def _create_duty_from_changes(x_usernox):
    x_agenda = _merge_changes_into_agenda(x_usernox, get_default_duty_agenda(x_usernox))
    save_duty_file(x_usernox, x_agenda)


def get_default_duty_agenda(x_usernox: UserNox) -> AgendaUnit:
    x_agendaunit = agendaunit_shop(
        x_usernox.person_id,
        x_usernox.real_id,
        x_usernox._road_delimiter,
        x_usernox._planck,
    )
    x_agendaunit._last_change_id = init_change_id()
    return x_agendaunit


def initialize_change_duty_files(x_usernox: UserNox):
    set_dir(x_usernox.real_dir())
    set_dir(x_usernox.persons_dir())
    set_dir(x_usernox.person_dir())
    set_dir(x_usernox.atoms_dir())
    set_dir(x_usernox.changes_dir())
    x_duty_file_exists = x_usernox.duty_file_exists()
    change_file_exists = changeunit_file_exists(x_usernox, init_change_id())
    if x_duty_file_exists == False and change_file_exists == False:
        _create_initial_change_and_duty_files(x_usernox)
    elif x_duty_file_exists == False and change_file_exists:
        _create_duty_from_changes(x_usernox)
    elif x_duty_file_exists and change_file_exists == False:
        _create_initial_change_from_duty(x_usernox)


def append_changes_to_duty_file(x_usernox: UserNox) -> AgendaUnit:
    duty_agenda = get_duty_file_agenda(x_usernox)
    duty_agenda = _merge_changes_into_agenda(x_usernox, duty_agenda)
    save_duty_file(x_usernox, duty_agenda)
    return get_duty_file_agenda(x_usernox)


def _create_initial_change_and_duty_files(x_usernox: UserNox):
    x_changeunit = changeunit_shop(
        _giver=x_usernox.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_usernox.changes_dir(),
        _atoms_dir=x_usernox.atoms_dir(),
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_usernox),
        after_agenda=get_default_duty_agenda(x_usernox),
    )
    x_changeunit.save_files()
    _create_duty_from_changes(x_usernox)


def add_pledge_change(x_usernox, pledge_road: RoadUnit, x_suffgroup: GroupID = None):
    duty_agenda = get_duty_file_agenda(x_usernox)
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_changeunit = _create_new_changeunit(x_usernox)
    next_changeunit._bookunit.add_all_different_agendaatoms(
        old_duty_agenda, duty_agenda
    )
    next_changeunit.save_files()
    append_changes_to_duty_file(x_usernox)
