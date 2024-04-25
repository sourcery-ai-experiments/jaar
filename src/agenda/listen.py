from src._road.road import get_ancestor_roads
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit
from copy import deepcopy as copy_deepcopy


class Missing_party_debtor_poolException(Exception):
    pass


def get_ingested_action_items(
    item_list: list[IdeaUnit], debtor_amount: float, planck: float
) -> list[IdeaUnit]:
    x_list = []
    for x_ideaunit in item_list:
        x_ingest_weight = x_ideaunit._agenda_importance * debtor_amount
        x_ingest_scaled = int(x_ingest_weight / planck) * planck
        x_ideaunit._weight = x_ingest_scaled
        x_list.append(x_ideaunit)

    sum_scaled_ingest = sum(x_ideaunit._weight for x_ideaunit in item_list)

    if x_list:
        x_count = 0
        while sum_scaled_ingest < debtor_amount:
            x_ideaunit = x_list[x_count]
            x_ideaunit._weight += planck
            sum_scaled_ingest += planck
            x_count += 1

    return x_list


def listen_to_agendaunit(listener: AgendaUnit, listened: AgendaUnit) -> AgendaUnit:
    if listener._party_debtor_pool is None:
        raise Missing_party_debtor_poolException(
            "Listening process is not possible without debtor pool."
        )
    listened_agendaunit = copy_deepcopy(listened)
    listened_agendaunit.set_owner_id(listener._owner_id)
    intent_list = list(listened_agendaunit.get_intent_dict().values())
    ingest_list = get_ingested_action_items(
        item_list=intent_list,
        debtor_amount=listener._party_debtor_pool,
        planck=listener._planck,
    )

    for ingested_ideaunit in ingest_list:
        replace_weight_list = []
        add_to_weight_list = []
        ancestor_roads = get_ancestor_roads(ingested_ideaunit._parent_road)
        for ancestor_road in ancestor_roads:
            if ancestor_road != ingested_ideaunit._agenda_world_id:
                try:
                    listener.get_idea_obj(ancestor_road)
                    add_to_weight_list.append(ancestor_road)
                except Exception:
                    replace_weight_list.append(ancestor_road)

        listener.add_idea(
            idea_kid=ingested_ideaunit,
            parent_road=ingested_ideaunit._parent_road,
            create_missing_ideas_and_groups=True,
            create_missing_ancestors=True,
        )

        for idea_road in replace_weight_list:
            listener.edit_idea_attr(idea_road, weight=ingested_ideaunit._weight)
        for idea_road in add_to_weight_list:
            x_ideaunit = listener.get_idea_obj(idea_road)
            x_ideaunit._weight += ingested_ideaunit._weight

    return listener
