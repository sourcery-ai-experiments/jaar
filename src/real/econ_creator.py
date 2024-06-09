from src._instrument.python import get_empty_dict_if_none
from src._road.road import RoadUnit
from src.agenda.agenda import AgendaUnit, IdeaUnit
from src.change.filehub import filehub_shop, FileHub
from src.econ.econ import EconUnit, econunit_shop


class InvalidEconException(Exception):
    pass


class PersonCreateEconUnitsException(Exception):
    pass


def _get_econs_ideas(x_filehub: FileHub) -> dict[RoadUnit:IdeaUnit]:
    x_duty_agenda = x_filehub.get_duty_agenda()
    x_duty_agenda.calc_agenda_metrics()
    if x_duty_agenda._econs_justified is False:
        x_str = f"Cannot set '{x_filehub.person_id}' duty agenda econunits because 'AgendaUnit._econs_justified' is False."
        raise PersonCreateEconUnitsException(x_str)
    if x_duty_agenda._econs_buildable is False:
        x_str = f"Cannot set '{x_filehub.person_id}' duty agenda econunits because 'AgendaUnit._econs_buildable' is False."
        raise PersonCreateEconUnitsException(x_str)

    x_person_econs = x_duty_agenda._healers_dict.get(x_filehub.person_id)
    return get_empty_dict_if_none(x_person_econs)


def init_econunit(x_filehub: FileHub, econ_road: RoadUnit) -> EconUnit:
    x_filehub.econ_road = econ_road
    return econunit_shop(x_filehub, in_memory_treasury=False)


def create_person_econunits(x_filehub: FileHub):
    x_person_econs = _get_econs_ideas(x_filehub)
    for econ_idea in x_person_econs.values():
        init_econunit(x_filehub, econ_idea.get_road())


def get_econunit(x_filehub: FileHub, econ_road: RoadUnit) -> EconUnit:
    return init_econunit(x_filehub, econ_road)


def set_econunit_role(x_filehub: FileHub, econ_road: RoadUnit, role: AgendaUnit):
    x_filehub.econ_road = econ_road
    x_filehub.save_role_agenda(role)


def set_econunits_role(x_filehub: FileHub, role: AgendaUnit):
    for x_econ_road in _get_econs_ideas(x_filehub).keys():
        set_econunit_role(x_filehub, x_econ_road, role)


def set_person_econunits_role(x_filehub: FileHub):
    set_econunits_role(x_filehub, x_filehub.get_duty_agenda())
