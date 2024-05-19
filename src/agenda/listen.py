from src._road.road import get_ancestor_roads, RoadUnit, get_root_node_from_road
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit
from copy import deepcopy as copy_deepcopy


class Missing_party_debtor_poolException(Exception):
    pass


def _get_planck_scaled_weight(
    x_agenda_importance: float, debtor_amount: float, planck: float
) -> float:
    x_ingest_weight = x_agenda_importance * debtor_amount
    return int(x_ingest_weight / planck) * planck


def _distribute_ingest(
    x_list: list[IdeaUnit], nonallocated_ingest: float, planck: float
):
    # TODO very slow needs to be optimized
    if x_list:
        x_count = 0
        while nonallocated_ingest > 0:
            x_ideaunit = x_list[x_count]
            x_ideaunit._weight += planck
            nonallocated_ingest -= planck
            x_count += 1
            if x_count == len(x_list):
                x_count = 0


def _get_ingested_ideaunit_list(
    item_list: list[IdeaUnit], debtor_amount: float, planck: float
) -> list[IdeaUnit]:
    x_list = []
    for x_ideaunit in item_list:
        x_ideaunit._weight = _get_planck_scaled_weight(
            x_agenda_importance=x_ideaunit._agenda_importance,
            debtor_amount=debtor_amount,
            planck=planck,
        )
        x_list.append(x_ideaunit)
    sum_scaled_ingest = sum(x_ideaunit._weight for x_ideaunit in item_list)
    nonallocated_ingest = debtor_amount - sum_scaled_ingest
    _distribute_ingest(x_list, nonallocated_ingest, planck)
    return x_list


def listen_to_speaker(listener: AgendaUnit, speaker: AgendaUnit) -> AgendaUnit:
    if listener._party_debtor_pool is None:
        raise Missing_party_debtor_poolException(
            "Listening process is not possible without debtor pool."
        )
    if speaker._rational:
        perspective_agendaunit = copy_deepcopy(speaker)
        # look at things from speaker's prespective
        perspective_agendaunit.set_owner_id(listener._owner_id)
        intent_list = list(perspective_agendaunit.get_intent_dict().values())
        ingest_list = _get_ingested_ideaunit_list(
            item_list=intent_list,
            debtor_amount=listener._party_debtor_pool,
            planck=listener._planck,
        )

        for ingested_ideaunit in ingest_list:
            replace_weight_list, add_to_weight_list = (
                _create_weight_replace_and_add_lists(
                    listener, ingested_ideaunit.get_road()
                )
            )

            if listener.idea_exists(ingested_ideaunit.get_road()) == False:
                listener.add_idea(
                    idea_kid=ingested_ideaunit,
                    parent_road=ingested_ideaunit._parent_road,
                    create_missing_ideas=True,
                    create_missing_ancestors=True,
                )

            _add_and_replace_ideaunit_weights(
                listener,
                replace_weight_list,
                add_to_weight_list,
                ingested_ideaunit._weight,
            )

    return listener


def _create_weight_replace_and_add_lists(
    listener: AgendaUnit, x_road: RoadUnit
) -> list:
    replace_weight_list = []
    add_to_weight_list = []
    ancestor_roads = get_ancestor_roads(x_road)
    root_road = get_root_node_from_road(x_road)
    for ancestor_road in ancestor_roads:
        if ancestor_road != root_road:
            try:
                listener.get_idea_obj(ancestor_road)
                add_to_weight_list.append(ancestor_road)
            except Exception:
                replace_weight_list.append(ancestor_road)

    return replace_weight_list, add_to_weight_list


def _add_and_replace_ideaunit_weights(
    listener: AgendaUnit,
    replace_weight_list: list[RoadUnit],
    add_to_weight_list: list[RoadUnit],
    x_weight: float,
):
    for idea_road in replace_weight_list:
        listener.edit_idea_attr(idea_road, weight=x_weight)
    for idea_road in add_to_weight_list:
        x_ideaunit = listener.get_idea_obj(idea_road)
        x_ideaunit._weight += x_weight
