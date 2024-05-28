from src._instrument.python import get_empty_dict_if_none
from src._instrument.file import (
    set_dir,
    get_all_dirs_with_file,
    get_parts_dir,
    delete_dir,
)
from src._road.road import RoadUnit, rebuild_road, create_road_from_nodes
from src._road.userdir import UserDir, get_rootpart_of_econ_dir, get_econ_path
from src.agenda.agenda import AgendaUnit
from src.econ.econ import EconUnit, econunit_shop, treasury_db_filename
from src.real.admin_duty import get_duty_file_agenda
from src.real.admin_duty import get_duty_file_agenda


class InvalidEconException(Exception):
    pass


class PersonCreateEconUnitsException(Exception):
    pass


def _get_econs_roads(x_userdir: UserDir) -> dict[RoadUnit:EconUnit]:
    x_duty_agenda = get_duty_file_agenda(x_userdir)
    x_duty_agenda.calc_agenda_metrics()
    if x_duty_agenda._econs_justified == False:
        x_str = f"Cannot set '{x_userdir.person_id}' duty agenda econunits because 'AgendaUnit._econs_justified' is False."
        raise PersonCreateEconUnitsException(x_str)
    if x_duty_agenda._econs_buildable == False:
        x_str = f"Cannot set '{x_userdir.person_id}' duty agenda econunits because 'AgendaUnit._econs_buildable' is False."
        raise PersonCreateEconUnitsException(x_str)

    x_person_econs = x_duty_agenda._healers_dict.get(x_userdir.person_id)
    return get_empty_dict_if_none(x_person_econs)


def create_econ_dir(x_userdir: UserDir, x_road: RoadUnit) -> str:
    x_econ_path = get_econ_path(x_userdir, x_road)
    set_dir(x_econ_path)
    return x_econ_path


def init_econunit(x_userdir: UserDir, econ_road: RoadUnit) -> EconUnit:
    x_econ_path = create_econ_dir(x_userdir, econ_road)
    x_econunit = econunit_shop(
        real_id=x_userdir.real_id,
        econ_dir=x_econ_path,
        _manager_person_id=x_userdir.person_id,
        _road_delimiter=x_userdir._road_delimiter,
    )
    x_econunit.set_econ_dirs()
    return x_econunit


def create_person_econunits(x_userdir: UserDir):
    x_person_econs = _get_econs_roads(x_userdir)
    for econ_idea in x_person_econs.values():
        init_econunit(x_userdir, econ_idea.get_road())

    db_filename = treasury_db_filename()
    econs_dir = x_userdir._econs_dir
    root_dir = get_rootpart_of_econ_dir()
    for treasury_dir in get_all_dirs_with_file(db_filename, econs_dir):
        treasury_road = create_road_from_nodes(get_parts_dir(treasury_dir))
        treasury_road = rebuild_road(treasury_road, root_dir, x_userdir.real_id)
        if x_person_econs.get(treasury_road) is None:
            dir_to_delete = f"{x_userdir._econs_dir}/{treasury_dir}"
            delete_dir(dir_to_delete)


def get_econunit(x_userdir: UserDir, econ_road: RoadUnit) -> EconUnit:
    return init_econunit(x_userdir, econ_road)


def set_econunit_role(x_userdir: UserDir, econ_road: RoadUnit, role: AgendaUnit):
    x_econ = get_econunit(x_userdir, econ_road)
    x_econ.save_role_file(role)


def set_econunits_role(x_userdir: UserDir, role: AgendaUnit):
    for x_econ_road in _get_econs_roads(x_userdir).keys():
        set_econunit_role(x_userdir, x_econ_road, role)


def set_person_econunits_role(x_userdir: UserDir):
    set_econunits_role(x_userdir, get_duty_file_agenda(x_userdir))
