from src._instrument.python import get_empty_set_if_none
from src._road.road import RoadUnit
from src.agenda.agenda import AgendaUnit
from src.listen.filehub import FileHub
from src.money.money import MoneyUnit, moneyunit_shop


class PersonCreateMoneyUnitsException(Exception):
    pass


def init_treasury_db_file(x_filehub: FileHub, econ_road: RoadUnit) -> MoneyUnit:
    x_filehub.econ_road = econ_road
    return moneyunit_shop(x_filehub, in_memory_treasury=False)


def get_econ_roads(x_filehub: FileHub) -> set[RoadUnit]:
    x_duty_agenda = x_filehub.get_duty_agenda()
    x_duty_agenda.calc_agenda_metrics()
    if x_duty_agenda._econs_justified is False:
        x_str = f"Cannot set '{x_filehub.person_id}' duty agenda moneyunits because 'AgendaUnit._econs_justified' is False."
        raise PersonCreateMoneyUnitsException(x_str)
    if x_duty_agenda._econs_buildable is False:
        x_str = f"Cannot set '{x_filehub.person_id}' duty agenda moneyunits because 'AgendaUnit._econs_buildable' is False."
        raise PersonCreateMoneyUnitsException(x_str)
    person_healer_dict = x_duty_agenda._healers_dict.get(x_filehub.person_id)
    if person_healer_dict is None:
        return get_empty_set_if_none(None)
    econ_roads = x_duty_agenda._healers_dict.get(x_filehub.person_id).keys()
    return get_empty_set_if_none(econ_roads)


def create_duty_treasury_db_files(x_filehub: FileHub):
    for x_econ_road in get_econ_roads(x_filehub):
        init_treasury_db_file(x_filehub, x_econ_road)


def set_all_role_files(x_filehub: FileHub, role: AgendaUnit):
    for x_econ_road in get_econ_roads(x_filehub):
        x_filehub.econ_road = x_econ_road
        x_filehub.save_role_agenda(role)


def set_person_moneyunits_role(x_filehub: FileHub):
    set_all_role_files(x_filehub, x_filehub.get_duty_agenda())
