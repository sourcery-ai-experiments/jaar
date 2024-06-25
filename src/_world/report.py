from src._road.road import RoadUnit
from src._world.world import WorldUnit
from pandas import DataFrame


def get_world_personunits_dataframe(x_world: WorldUnit) -> DataFrame:
    if x_world._persons == {}:
        return DataFrame(
            columns=[
                "person_id",
                "credor_weight",
                "debtor_weight",
                "_world_cred",
                "_world_debt",
                "_world_agenda_cred",
                "_world_agenda_debt",
                "_world_agenda_ratio_cred",
                "_world_agenda_ratio_debt",
                "_credor_operational",
                "_debtor_operational",
                "_treasury_due_paid",
                "_treasury_due_diff",
                "_output_world_meld_order",
                "_treasury_cred_score",
                "_treasury_voice_rank",
                "_treasury_voice_hx_lowest_rank",
            ]
        )
    x_personunits_list = list(x_world.get_persons_dict(all_attrs=True).values())
    return DataFrame(x_personunits_list)


def get_world_agenda_dataframe(x_world: WorldUnit, base: RoadUnit = None) -> DataFrame:
    agenda_dict = x_world.get_agenda_dict(base=base)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "owner_id",
                "world_importance",
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
            "owner_id": x_world._owner_id,
            "world_importance": x_idea._world_importance,
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
