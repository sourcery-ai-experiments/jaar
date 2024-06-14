from src._road.road import RoadUnit
from src.agenda.agenda import AgendaUnit
from pandas import DataFrame


def get_agenda_partyunits_dataframe(x_agenda: AgendaUnit) -> DataFrame:
    if x_agenda._partys == {}:
        return DataFrame(
            columns=[
                "party_id",
                "credor_weight",
                "debtor_weight",
                "_agenda_cred",
                "_agenda_debt",
                "_agenda_intent_cred",
                "_agenda_intent_debt",
                "_agenda_intent_ratio_cred",
                "_agenda_intent_ratio_debt",
                "_credor_operational",
                "_debtor_operational",
                "_treasury_due_paid",
                "_treasury_due_diff",
                "_output_agenda_meld_order",
                "_treasury_cred_score",
                "_treasury_voice_rank",
                "_treasury_voice_hx_lowest_rank",
            ]
        )
    x_partyunits_list = list(x_agenda.get_partys_dict(all_attrs=True).values())
    return DataFrame(x_partyunits_list)


def get_agenda_intent_dataframe(
    x_agenda: AgendaUnit, base: RoadUnit = None
) -> DataFrame:
    intent_dict = x_agenda.get_intent_dict(base=base)
    if intent_dict == {}:
        return DataFrame(
            columns=[
                "owner_id",
                "agenda_importance",
                "_label",
                "_parent_road",
                "_begin",
                "_close",
                "_addin",
                "_denom",
                "_numor",
                "_reest",
            ]
        )
    x_oath_list = []
    for x_oath in intent_dict.values():
        oath_dict = {
            "owner_id": x_agenda._owner_id,
            "agenda_importance": x_oath._agenda_importance,
            "_label": x_oath._label,
            "_parent_road": x_oath._parent_road,
            "_begin": x_oath._begin,
            "_close": x_oath._close,
            "_addin": x_oath._addin,
            "_denom": x_oath._denom,
            "_numor": x_oath._numor,
            "_reest": x_oath._reest,
        }
        x_oath_list.append(oath_dict)
    return DataFrame(x_oath_list)
