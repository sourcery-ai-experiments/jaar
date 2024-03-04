from src.agenda.agenda import AgendaUnit
from pandas import DataFrame


def get_agenda_partyunits_dataframe(x_agenda: AgendaUnit) -> DataFrame:
    x_agenda.set_agenda_metrics()
    x_partyunits_list = list(x_agenda.get_partys_dict(all_attrs=True).values())
    return DataFrame(x_partyunits_list)
