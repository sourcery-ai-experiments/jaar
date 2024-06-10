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


def create_duty_treasury_db_files(x_filehub: FileHub):
    for x_econ_road in x_filehub.get_econ_roads():
        init_treasury_db_file(x_filehub, x_econ_road)
