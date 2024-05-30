from src._instrument.file import set_dir
from src._road.road import RoadUnit
from src.agenda.group import GroupID
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
)
from src.agenda.pledge import create_pledge
from src.agenda.change import (
    changeunit_shop,
    init_change_id,
    get_init_change_id_if_None,
)
from src.real.admin_change import (
    changeunit_file_exists,
    _merge_changes_into_agenda,
    _create_new_changeunit,
)
from src._road.userdir import UserDir
from copy import deepcopy as copy_deepcopy


class Invalid_duty_Exception(Exception):
    pass


def _create_initial_change_from_duty(x_userdir: UserDir):
    x_changeunit = changeunit_shop(
        _giver=x_userdir.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_userdir.changes_dir(),
        _atoms_dir=x_userdir.atoms_dir(),
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_userdir),
        after_agenda=get_duty_file_agenda(x_userdir),
    )
    x_changeunit.save_files()


def save_duty_file(x_userdir: UserDir, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_userdir.person_id:
        raise Invalid_duty_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_userdir.person_id}''s duty agenda."
        )
    if replace in {True, False}:
        x_userdir.save_file_duty(x_agenda.get_json(), replace)


def get_duty_file_agenda(x_userdir: UserDir) -> AgendaUnit:
    if x_userdir.duty_file_exists() == False:
        save_duty_file(x_userdir, get_default_duty_agenda(x_userdir))
    duty_json = x_userdir.open_file_duty()
    return agendaunit_get_from_json(duty_json)


def _create_duty_from_changes(x_userdir):
    x_agenda = _merge_changes_into_agenda(x_userdir, get_default_duty_agenda(x_userdir))
    save_duty_file(x_userdir, x_agenda)


def get_default_duty_agenda(x_userdir: UserDir) -> AgendaUnit:
    x_agendaunit = agendaunit_shop(
        x_userdir.person_id,
        x_userdir.real_id,
        x_userdir._road_delimiter,
        x_userdir._planck,
    )
    x_agendaunit._last_change_id = init_change_id()
    return x_agendaunit


def initialize_change_duty_files(x_userdir: UserDir):
    set_dir(x_userdir.real_dir())
    set_dir(x_userdir.persons_dir())
    set_dir(x_userdir.person_dir())
    set_dir(x_userdir.atoms_dir())
    set_dir(x_userdir.changes_dir())
    x_duty_file_exists = x_userdir.duty_file_exists()
    change_file_exists = changeunit_file_exists(x_userdir, init_change_id())
    if x_duty_file_exists == False and change_file_exists == False:
        _create_initial_change_and_duty_files(x_userdir)
    elif x_duty_file_exists == False and change_file_exists:
        _create_duty_from_changes(x_userdir)
    elif x_duty_file_exists and change_file_exists == False:
        _create_initial_change_from_duty(x_userdir)


def append_changes_to_duty_file(x_userdir: UserDir) -> AgendaUnit:
    duty_agenda = get_duty_file_agenda(x_userdir)
    duty_agenda = _merge_changes_into_agenda(x_userdir, duty_agenda)
    save_duty_file(x_userdir, duty_agenda)
    return get_duty_file_agenda(x_userdir)


def _create_initial_change_and_duty_files(x_userdir: UserDir):
    x_changeunit = changeunit_shop(
        _giver=x_userdir.person_id,
        _change_id=get_init_change_id_if_None(),
        _changes_dir=x_userdir.changes_dir(),
        _atoms_dir=x_userdir.atoms_dir(),
    )
    x_changeunit._bookunit.add_all_different_agendaatoms(
        before_agenda=get_default_duty_agenda(x_userdir),
        after_agenda=get_default_duty_agenda(x_userdir),
    )
    x_changeunit.save_files()
    _create_duty_from_changes(x_userdir)


def add_pledge_change(x_userdir, pledge_road: RoadUnit, x_suffgroup: GroupID = None):
    duty_agenda = get_duty_file_agenda(x_userdir)
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_changeunit = _create_new_changeunit(x_userdir)
    next_changeunit._bookunit.add_all_different_agendaatoms(
        old_duty_agenda, duty_agenda
    )
    next_changeunit.save_files()
    append_changes_to_duty_file(x_userdir)
