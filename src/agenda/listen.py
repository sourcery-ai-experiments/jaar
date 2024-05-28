from src._road.road import (
    get_ancestor_roads,
    RoadUnit,
    get_root_node_from_road,
    PersonID,
)
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from copy import deepcopy as copy_deepcopy


class Missing_party_debtor_poolException(Exception):
    pass


def create_barren_agenda(ref_agenda: AgendaUnit, x_owner_id: PersonID) -> AgendaUnit:
    barren_agenda = agendaunit_shop(
        x_owner_id, ref_agenda._real_id, _road_delimiter=ref_agenda._road_delimiter
    )
    barren_agenda._planck = ref_agenda._planck
    return barren_agenda


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


def generate_ingest_list(
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
    speaker_partyunit = listener.get_party(speaker._owner_id)
    if speaker_partyunit is None:
        raise Missing_party_debtor_poolException(
            f"listener '{listener._owner_id}' agenda is assumed to have {speaker._owner_id} partyunit."
        )

    speaker_debtor_weight = speaker_partyunit.debtor_weight
    if listener._party_debtor_pool is None or speaker == create_barren_agenda(
        speaker, speaker._owner_id
    ):
        speaker_partyunit.add_missing_job_debtor_weight(speaker_debtor_weight)
        return listener

    # look at things from speaker's prespective
    perspective_agendaunit = copy_deepcopy(speaker)
    perspective_agendaunit.set_owner_id(listener._owner_id)
    perspective_agendaunit.calc_agenda_metrics()

    if perspective_agendaunit._rational == False:
        speaker_partyunit = listener.get_party(speaker._owner_id)
        speaker_debtor_weight = speaker_partyunit.debtor_weight
        speaker_partyunit.add_irrational_debtor_weight(speaker_debtor_weight)
        return listener

    intent_list = list(perspective_agendaunit.get_intent_dict().values())
    debtor_amount = listener._party_debtor_pool
    ingest_list = generate_ingest_list(intent_list, debtor_amount, listener._planck)
    for ingest_ideaunit in ingest_list:
        _ingest_single_ideaunit(listener, ingest_ideaunit)
    return listener


def _ingest_single_ideaunit(listener: AgendaUnit, ingest_ideaunit: IdeaUnit):
    replace_weight_list, add_to_weight_list = _create_weight_replace_and_add_lists(
        listener, ingest_ideaunit.get_road()
    )

    if listener.idea_exists(ingest_ideaunit.get_road()) == False:
        x_parent_road = ingest_ideaunit._parent_road
        listener.add_idea(ingest_ideaunit, x_parent_road, create_missing_ideas=True)

    _add_and_replace_ideaunit_weights(
        listener=listener,
        replace_weight_list=replace_weight_list,
        add_to_weight_list=add_to_weight_list,
        x_weight=ingest_ideaunit._weight,
    )


def _create_weight_replace_and_add_lists(
    listener: AgendaUnit, x_road: RoadUnit
) -> list:
    replace_weight_list = []
    add_to_weight_list = []
    ancestor_roads = get_ancestor_roads(x_road)
    root_road = get_root_node_from_road(x_road)
    for ancestor_road in ancestor_roads:
        if ancestor_road != root_road:
            if listener.idea_exists(ancestor_road):
                add_to_weight_list.append(ancestor_road)
            else:
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
