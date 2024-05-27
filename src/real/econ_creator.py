from src._instrument.python import get_empty_dict_if_none
from src._instrument.file import (
    set_dir,
    get_directory_path,
    get_all_dirs_with_file,
    get_parts_dir,
    delete_dir,
)
from src._road.road import (
    RoadUnit,
    RoadNode,
    get_all_road_nodes,
    change_road,
    create_road_from_nodes,
)
from src.agenda.agenda import AgendaUnit
from src.econ.econ import (
    EconUnit,
    econunit_shop,
    treasury_db_filename,
    get_rootpart_of_econ_dir,
)
from src.real.nook import NookUnit, get_duty_file_agenda


class InvalidEconException(Exception):
    pass


class PersonCreateEconUnitsException(Exception):
    pass


def _get_econs_roads(x_nookunit: NookUnit) -> dict[RoadUnit:EconUnit]:
    x_duty_agenda = get_duty_file_agenda(x_nookunit)
    x_duty_agenda.calc_agenda_metrics()
    if x_duty_agenda._econs_justified == False:
        x_str = f"Cannot set '{x_nookunit.person_id}' duty agenda econunits because 'AgendaUnit._econs_justified' is False."
        raise PersonCreateEconUnitsException(x_str)
    if x_duty_agenda._econs_buildable == False:
        x_str = f"Cannot set '{x_nookunit.person_id}' duty agenda econunits because 'AgendaUnit._econs_buildable' is False."
        raise PersonCreateEconUnitsException(x_str)

    x_person_econs = x_duty_agenda._healers_dict.get(x_nookunit.person_id)
    return get_empty_dict_if_none(x_person_econs)


def get_econ_path(x_nookunit: NookUnit, x_road: RoadNode) -> str:
    # econ_root = get_rootpart_of_econ_dir()
    # x_road = change_road(x_road, x_nookunit.real_id, econ_root)
    x_list = get_all_road_nodes(x_road, x_nookunit._road_delimiter)
    return f"{x_nookunit._econs_dir}{get_directory_path(x_list=[*x_list])}"


def create_econ_dir(x_nookunit: NookUnit, x_road: RoadUnit) -> str:
    x_econ_path = get_econ_path(x_nookunit, x_road)
    set_dir(x_econ_path)
    return x_econ_path


def init_econunit(x_nookunit: NookUnit, econ_road: RoadUnit) -> EconUnit:
    x_econ_path = create_econ_dir(x_nookunit, econ_road)
    x_econunit = econunit_shop(
        real_id=x_nookunit.real_id,
        econ_dir=x_econ_path,
        _manager_person_id=x_nookunit.person_id,
        _road_delimiter=x_nookunit._road_delimiter,
    )
    x_econunit.set_econ_dirs()
    return x_econunit


def create_person_econunits(x_nookunit: NookUnit):
    x_person_econs = _get_econs_roads(x_nookunit)
    for econ_idea in x_person_econs.values():
        init_econunit(x_nookunit, econ_idea.get_road())

    db_filename = treasury_db_filename()
    econs_dir = x_nookunit._econs_dir
    root_dir = get_rootpart_of_econ_dir()
    for treasury_dir in get_all_dirs_with_file(db_filename, econs_dir):
        treasury_road = create_road_from_nodes(get_parts_dir(treasury_dir))
        treasury_road = change_road(treasury_road, root_dir, x_nookunit.real_id)
        if x_person_econs.get(treasury_road) is None:
            dir_to_delete = f"{x_nookunit._econs_dir}/{treasury_dir}"
            delete_dir(dir_to_delete)


def get_econunit(x_nookunit: NookUnit, econ_road: RoadUnit) -> EconUnit:
    return init_econunit(x_nookunit, econ_road)


def set_econunit_role(x_nookunit: NookUnit, econ_road: RoadUnit, role: AgendaUnit):
    x_econ = get_econunit(x_nookunit, econ_road)
    x_econ.save_role_file(role)


def set_econunits_role(x_nookunit: NookUnit, role: AgendaUnit):
    for x_econ_road in _get_econs_roads(x_nookunit).keys():
        set_econunit_role(x_nookunit, x_econ_road, role)


def set_person_econunits_role(x_nookunit: NookUnit):
    set_econunits_role(x_nookunit, get_duty_file_agenda(x_nookunit))
