from src._instrument.python import get_empty_dict_if_none
from src._instrument.file import (
    set_dir,
    get_all_dirs_with_file,
    get_parts_dir,
    delete_dir,
)
from src._road.jaar_config import treasury_file_name
from src._road.road import RoadUnit, rebuild_road, create_road_from_nodes
from src._road.worldnox import UserNox, get_rootpart_of_econ_dir
from src.agenda.agenda import AgendaUnit
from src.change.filehub import get_econ_path, filehub_shop
from src.econ.econ import EconUnit, econunit_shop
from src.real.admin_duty import get_duty_file_agenda


class InvalidEconException(Exception):
    pass


class PersonCreateEconUnitsException(Exception):
    pass


def _get_econs_roads(x_usernox: UserNox) -> dict[RoadUnit:EconUnit]:
    x_duty_agenda = get_duty_file_agenda(x_usernox)
    x_duty_agenda.calc_agenda_metrics()
    if x_duty_agenda._econs_justified == False:
        x_str = f"Cannot set '{x_usernox.person_id}' duty agenda econunits because 'AgendaUnit._econs_justified' is False."
        raise PersonCreateEconUnitsException(x_str)
    if x_duty_agenda._econs_buildable == False:
        x_str = f"Cannot set '{x_usernox.person_id}' duty agenda econunits because 'AgendaUnit._econs_buildable' is False."
        raise PersonCreateEconUnitsException(x_str)

    x_person_econs = x_duty_agenda._healers_dict.get(x_usernox.person_id)
    return get_empty_dict_if_none(x_person_econs)


def init_econunit(x_usernox: UserNox, econ_road: RoadUnit) -> EconUnit:
    x_filehub = filehub_shop(
        reals_dir=x_usernox.reals_dir,
        real_id=x_usernox.real_id,
        person_id=x_usernox.person_id,
        econ_road=econ_road,
        road_delimiter=x_usernox._road_delimiter,
        planck=x_usernox._planck,
    )
    return econunit_shop(x_filehub, in_memory_treasury=False)


def create_person_econunits(x_usernox: UserNox):
    x_person_econs = _get_econs_roads(x_usernox)
    for econ_idea in x_person_econs.values():
        init_econunit(x_usernox, econ_idea.get_road())


def get_econunit(x_usernox: UserNox, econ_road: RoadUnit) -> EconUnit:
    return init_econunit(x_usernox, econ_road)


def set_econunit_role(x_usernox: UserNox, econ_road: RoadUnit, role: AgendaUnit):
    x_econ = get_econunit(x_usernox, econ_road)
    x_econ.filehub.save_role_agenda(role)


def set_econunits_role(x_usernox: UserNox, role: AgendaUnit):
    for x_econ_road in _get_econs_roads(x_usernox).keys():
        set_econunit_role(x_usernox, x_econ_road, role)


def set_person_econunits_role(x_usernox: UserNox):
    set_econunits_role(x_usernox, get_duty_file_agenda(x_usernox))
