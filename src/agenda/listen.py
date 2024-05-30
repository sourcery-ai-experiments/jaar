from src._road.road import (
    get_ancestor_roads,
    RoadUnit,
    get_root_node_from_road,
    PersonID,
)
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit, agendaunit_shop, PartyUnit
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class Missing_party_debtor_poolException(Exception):
    pass


def listen_to_speaker_intent(listener: AgendaUnit, speaker: AgendaUnit) -> AgendaUnit:
    if listener.party_exists(speaker._owner_id) == False:
        raise Missing_party_debtor_poolException(
            f"listener '{listener._owner_id}' agenda is assumed to have {speaker._owner_id} partyunit."
        )
    perspective_agenda = get_speaker_perspective(speaker, listener._owner_id)
    if perspective_agenda._rational == False:
        return _allocate_irrational_debtor_weight(listener, speaker._owner_id)

    if listener._party_debtor_pool is None:
        return _allocate_missing_job_debtor_weight(listener, speaker._owner_id)
    intent = generate_perspective_intent(perspective_agenda)
    if len(intent) == 0:
        return _allocate_missing_job_debtor_weight(listener, speaker._owner_id)
    return _ingest_perspective_intent(listener, intent)


def generate_perspective_intent(perspective_agenda: AgendaUnit) -> list[IdeaUnit]:
    for x_beliefunit in perspective_agenda._idearoot._beliefunits.values():
        x_beliefunit.set_pick_to_base()
    return list(perspective_agenda.get_intent_dict().values())


def _ingest_perspective_intent(
    listener: AgendaUnit, intent: list[IdeaUnit]
) -> AgendaUnit:
    debtor_amount = listener._party_debtor_pool
    ingest_list = generate_ingest_list(intent, debtor_amount, listener._planck)
    for ingest_ideaunit in ingest_list:
        _ingest_single_ideaunit(listener, ingest_ideaunit)
    return listener


def _allocate_irrational_debtor_weight(
    listener: AgendaUnit, speaker_owner_id: PersonID
):
    speaker_partyunit = listener.get_party(speaker_owner_id)
    speaker_debtor_weight = speaker_partyunit.debtor_weight
    speaker_partyunit.add_irrational_debtor_weight(speaker_debtor_weight)
    return listener


def _allocate_missing_job_debtor_weight(
    listener: AgendaUnit, speaker_owner_id: PersonID
):
    speaker_partyunit = listener.get_party(speaker_owner_id)
    speaker_partyunit.add_missing_job_debtor_weight(speaker_partyunit.debtor_weight)
    return listener


def get_speaker_perspective(speaker: AgendaUnit, listener_owner_id: PersonID):
    perspective_agenda = copy_deepcopy(speaker)
    perspective_agenda.set_owner_id(listener_owner_id)
    perspective_agenda.calc_agenda_metrics()
    return perspective_agenda


def _is_empty_agenda(x_agenda: AgendaUnit) -> bool:
    empty_agenda = create_empty_agenda(x_agenda)
    return x_agenda.get_dict() == empty_agenda.get_dict()


def create_empty_agenda(
    ref_agenda: AgendaUnit, x_owner_id: PersonID = None
) -> AgendaUnit:
    if x_owner_id is None:
        x_owner_id = ref_agenda._owner_id
    x_road_delimiter = ref_agenda._road_delimiter
    x_planck = ref_agenda._planck
    return agendaunit_shop(x_owner_id, ref_agenda._real_id, x_road_delimiter, x_planck)


def create_listen_basis(x_role: AgendaUnit) -> AgendaUnit:
    x_listen = create_empty_agenda(x_role, x_owner_id=x_role._owner_id)
    x_listen._partys = x_role._partys
    x_listen._groups = x_role._groups
    x_listen.set_money_desc(x_role._money_desc)
    x_listen.set_max_tree_traverse(x_role._max_tree_traverse)
    if x_role._party_creditor_pool != None:
        x_listen.set_party_creditor_pool(x_role._party_creditor_pool)
    if x_role._party_debtor_pool != None:
        x_listen.set_party_debtor_pool(x_role._party_debtor_pool)
    for x_partyunit in x_listen._partys.values():
        x_partyunit.reset_listen_calculated_attrs()
    return x_listen


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


def _ingest_single_ideaunit(listener: AgendaUnit, ingest_ideaunit: IdeaUnit):
    weight_data = _create_weight_data(listener, ingest_ideaunit.get_road())

    if listener.idea_exists(ingest_ideaunit.get_road()) == False:
        x_parent_road = ingest_ideaunit._parent_road
        listener.add_idea(ingest_ideaunit, x_parent_road, create_missing_ideas=True)

    _add_and_replace_ideaunit_weights(
        listener=listener,
        replace_weight_list=weight_data.replace_weight_list,
        add_to_weight_list=weight_data.add_to_weight_list,
        x_weight=ingest_ideaunit._weight,
    )


@dataclass
class WeightReplaceOrAddData:
    add_to_weight_list: list = None
    replace_weight_list: list = None


def _create_weight_data(listener: AgendaUnit, x_road: RoadUnit) -> list:
    weight_data = WeightReplaceOrAddData()
    weight_data.add_to_weight_list = []
    weight_data.replace_weight_list = []
    ancestor_roads = get_ancestor_roads(x_road)
    root_road = get_root_node_from_road(x_road)
    for ancestor_road in ancestor_roads:
        if ancestor_road != root_road:
            if listener.idea_exists(ancestor_road):
                weight_data.add_to_weight_list.append(ancestor_road)
            else:
                weight_data.replace_weight_list.append(ancestor_road)
    return weight_data


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


def get_debtor_weight_ordered_partys(x_agenda: AgendaUnit) -> list[PartyUnit]:
    partys_ordered_list = list(x_agenda._partys.values())
    partys_ordered_list.sort(key=lambda x: (x.debtor_weight, x.party_id), reverse=True)
    return partys_ordered_list


def listen_to_speaker_beliefs(
    listener: AgendaUnit,
    speaker: AgendaUnit,
    missing_belief_bases: list[RoadUnit] = None,
) -> AgendaUnit:
    if missing_belief_bases is None:
        missing_belief_bases = list(listener.get_missing_belief_bases())

    for missing_belief_base in missing_belief_bases:
        x_beliefunit = speaker.get_belief(missing_belief_base)
        if x_beliefunit != None:
            listener.set_belief(
                base=x_beliefunit.base,
                pick=x_beliefunit.pick,
                open=x_beliefunit.open,
                nigh=x_beliefunit.nigh,
                create_missing_ideas=True,
            )
