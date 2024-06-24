from src._road.road import RoadUnit
from src._truth.truth import TruthUnit
from pandas import DataFrame


def get_truth_otherunits_dataframe(x_truth: TruthUnit) -> DataFrame:
    if x_truth._others == {}:
        return DataFrame(
            columns=[
                "other_id",
                "credor_weight",
                "debtor_weight",
                "_truth_cred",
                "_truth_debt",
                "_truth_agenda_cred",
                "_truth_agenda_debt",
                "_truth_agenda_ratio_cred",
                "_truth_agenda_ratio_debt",
                "_credor_operational",
                "_debtor_operational",
                "_treasury_due_paid",
                "_treasury_due_diff",
                "_output_truth_meld_order",
                "_treasury_cred_score",
                "_treasury_voice_rank",
                "_treasury_voice_hx_lowest_rank",
            ]
        )
    x_otherunits_list = list(x_truth.get_others_dict(all_attrs=True).values())
    return DataFrame(x_otherunits_list)


def get_truth_agenda_dataframe(x_truth: TruthUnit, base: RoadUnit = None) -> DataFrame:
    agenda_dict = x_truth.get_agenda_dict(base=base)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "owner_id",
                "truth_importance",
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
    for x_idea in agenda_dict.values():
        idea_dict = {
            "owner_id": x_truth._owner_id,
            "truth_importance": x_idea._truth_importance,
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
