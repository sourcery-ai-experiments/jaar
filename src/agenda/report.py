from src._road.road import RoadUnit
from src.agenda.agenda import AgendaUnit
from pandas import DataFrame


def get_agenda_otherunits_dataframe(x_agenda: AgendaUnit) -> DataFrame:
    if x_agenda._others == {}:
        return DataFrame(
            columns=[
                "other_id",
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
    x_otherunits_list = list(x_agenda.get_others_dict(all_attrs=True).values())
    return DataFrame(x_otherunits_list)


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
    x_idea_list = []
    for x_idea in intent_dict.values():
        idea_dict = {
            "owner_id": x_agenda._owner_id,
            "agenda_importance": x_idea._agenda_importance,
            "_label": x_idea._label,
            "_parent_road": x_idea._parent_road,
            "_begin": x_idea._begin,
            "_close": x_idea._close,
            "_addin": x_idea._addin,
            "_denom": x_idea._denom,
            "_numor": x_idea._numor,
            "_reest": x_idea._reest,
        }
        x_idea_list.append(idea_dict)
    return DataFrame(x_idea_list)
