from src._road.road import (
    get_ancestor_roads,
    RoadUnit,
    get_root_node_from_road,
    PersonID,
)
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit, PartyUnit
from src.listen.basis_agendas import create_empty_agenda, create_listen_basis
from src.listen.filehub import FileHub
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class Missing_party_debtor_poolException(Exception):
    pass


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


def create_ingest_idea(
    x_ideaunit: IdeaUnit, debtor_amount: float, planck: float
) -> IdeaUnit:
    x_ideaunit._weight = _get_planck_scaled_weight(
        x_agenda_importance=x_ideaunit._agenda_importance,
        debtor_amount=debtor_amount,
        planck=planck,
    )
    return x_ideaunit


def generate_ingest_list(
    item_list: list[IdeaUnit], debtor_amount: float, planck: float
) -> list[IdeaUnit]:
    x_list = [
        create_ingest_idea(x_ideaunit, debtor_amount, planck)
        for x_ideaunit in item_list
    ]
    sum_scaled_ingest = sum(x_ideaunit._weight for x_ideaunit in item_list)
    nonallocated_ingest = debtor_amount - sum_scaled_ingest
    _distribute_ingest(x_list, nonallocated_ingest, planck)
    return x_list


def _ingest_single_ideaunit(listener: AgendaUnit, ingest_ideaunit: IdeaUnit):
    weight_data = _create_weight_data(listener, ingest_ideaunit.get_road())

    if listener.idea_exists(ingest_ideaunit.get_road()) is False:
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


def get_debtors_roll(x_role: AgendaUnit) -> list[PartyUnit]:
    return [
        x_partyunit
        for x_partyunit in x_role._partys.values()
        if x_partyunit.debtor_weight != 0
    ]


def get_ordered_debtors_roll(x_agenda: AgendaUnit) -> list[PartyUnit]:
    partys_ordered_list = get_debtors_roll(x_agenda)
    partys_ordered_list.sort(key=lambda x: (x.debtor_weight, x.party_id), reverse=True)
    return partys_ordered_list


def listen_to_speaker_belief(
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


def listen_to_speaker_intent(listener: AgendaUnit, speaker: AgendaUnit) -> AgendaUnit:
    if listener.party_exists(speaker._owner_id) is False:
        raise Missing_party_debtor_poolException(
            f"listener '{listener._owner_id}' agenda is assumed to have {speaker._owner_id} partyunit."
        )
    perspective_agenda = get_speaker_perspective(speaker, listener._owner_id)
    if perspective_agenda._rational is False:
        return _allocate_irrational_debtor_weight(listener, speaker._owner_id)

    if listener._party_debtor_pool is None:
        return _allocate_missing_job_debtor_weight(listener, speaker._owner_id)
    intent = generate_perspective_intent(perspective_agenda)
    if len(intent) == 0:
        return _allocate_missing_job_debtor_weight(listener, speaker._owner_id)
    return _ingest_perspective_intent(listener, intent)


def listen_to_speakers_intent(
    new_listener: AgendaUnit, filehub: FileHub, src_listener: AgendaUnit
):
    for x_partyunit in get_ordered_debtors_roll(new_listener):
        if x_partyunit.party_id == new_listener._owner_id:
            listen_to_speaker_intent(new_listener, src_listener)
        else:
            speaker_job = filehub.get_speaker_agenda(x_partyunit.party_id)
            if speaker_job is None:
                speaker_job = create_empty_agenda(new_listener, x_partyunit.party_id)
            listen_to_speaker_intent(new_listener, speaker_job)


def listen_to_speakers_belief(
    new_listener: AgendaUnit, filehub: FileHub, src_listener: AgendaUnit = None
):
    listen_to_speaker_belief(new_listener, src_listener)
    for x_partyunit in get_ordered_debtors_roll(new_listener):
        if x_partyunit.party_id != new_listener._owner_id:
            speaker_job = filehub.get_speaker_agenda(x_partyunit.party_id)
            if speaker_job != None:
                listen_to_speaker_belief(new_listener, speaker_job)


def listen_to_debtors_roll(listener: AgendaUnit, filehub: FileHub) -> AgendaUnit:
    new_agenda = create_listen_basis(listener)
    if listener._party_debtor_pool is None:
        return new_agenda
    listen_to_speakers_intent(new_agenda, filehub, listener)
    listen_to_speakers_belief(new_agenda, filehub, listener)
    return new_agenda


def listen_to_person_jobs(listener_filehub: FileHub) -> None:
    duty = listener_filehub.get_duty_agenda()
    new_work = create_listen_basis(duty)
    pre_work_dict = new_work.get_dict()
    duty.calc_agenda_metrics()
    new_work.calc_agenda_metrics()

    for x_healer_id, econ_dict in duty._healers_dict.items():
        listener_id = listener_filehub.person_id
        healer_filehub = copy_deepcopy(listener_filehub)
        healer_filehub.person_id = x_healer_id
        _pick_econ_jobs_and_listen(listener_id, econ_dict, healer_filehub, new_work)

    if new_work.get_dict() == pre_work_dict:
        intent = list(duty.get_intent_dict().values())
        _ingest_perspective_intent(new_work, intent)
        listen_to_speaker_belief(new_work, duty)

    listener_filehub.save_work_agenda(new_work)


def _pick_econ_jobs_and_listen(
    listener_id: PersonID,
    econ_dict: dict[RoadUnit],
    healer_filehub: FileHub,
    new_work: AgendaUnit,
):
    for econ_path in econ_dict:
        healer_filehub.econ_road = econ_path
        pick_econ_job_and_listen(listener_id, healer_filehub, new_work)


def pick_econ_job_and_listen(
    listener_person_id: PersonID, healer_filehub: FileHub, new_work: AgendaUnit
):
    listener_id = listener_person_id
    if healer_filehub.job_file_exists(listener_id):
        econ_job = healer_filehub.get_job_agenda(listener_id)
    else:
        econ_job = create_empty_agenda(new_work, new_work._owner_id)
    listen_to_job_intent(new_work, econ_job)


def listen_to_job_intent(listener: AgendaUnit, job: AgendaUnit):
    for x_idea in job._idea_dict.values():
        if listener.idea_exists(x_idea.get_road()) is False:
            listener.add_idea(x_idea, x_idea._parent_road)
        if listener.get_belief(x_idea.get_road()) is False:
            listener.add_idea(x_idea, x_idea._parent_road)
    for x_belief_road, x_belief_unit in job._idearoot._beliefunits.items():
        listener._idearoot.set_beliefunit(x_belief_unit)
    listener.calc_agenda_metrics()


def create_job_file_from_role_file(filehub: FileHub, person_id: PersonID):
    x_role = filehub.get_role_agenda(person_id)
    x_job = listen_to_debtors_roll(x_role, filehub)
    filehub.save_job_agenda(x_job)
    return x_job
