from src._road.road import (
    get_ancestor_roads,
    RoadUnit,
    get_root_node_from_road,
    PersonID,
)
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit, GuyUnit
from src.listen.basis_agendas import create_empty_agenda, create_listen_basis
from src.listen.userhub import UserHub, userhub_shop
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class Missing_guy_debtor_poolException(Exception):
    pass


def generate_perspective_intent(perspective_agenda: AgendaUnit) -> list[IdeaUnit]:
    for x_factunit in perspective_agenda._idearoot._factunits.values():
        x_factunit.set_pick_to_base()
    return list(perspective_agenda.get_intent_dict().values())


def _ingest_perspective_intent(
    listener: AgendaUnit, intent: list[IdeaUnit]
) -> AgendaUnit:
    debtor_amount = listener._guy_debtor_pool
    ingest_list = generate_ingest_list(intent, debtor_amount, listener._planck)
    for ingest_ideaunit in ingest_list:
        _ingest_single_ideaunit(listener, ingest_ideaunit)
    return listener


def _allocate_irrational_debtor_weight(
    listener: AgendaUnit, speaker_owner_id: PersonID
):
    speaker_guyunit = listener.get_guy(speaker_owner_id)
    speaker_debtor_weight = speaker_guyunit.debtor_weight
    speaker_guyunit.add_irrational_debtor_weight(speaker_debtor_weight)
    return listener


def _allocate_inallocable_debtor_weight(
    listener: AgendaUnit, speaker_owner_id: PersonID
):
    speaker_guyunit = listener.get_guy(speaker_owner_id)
    speaker_guyunit.add_inallocable_debtor_weight(speaker_guyunit.debtor_weight)
    return listener


def get_speaker_perspective(speaker: AgendaUnit, listener_owner_id: PersonID):
    listener_userhub = userhub_shop("", "", listener_owner_id)
    return listener_userhub.get_perspective_agenda(speaker)


def _get_planck_scaled_weight(
    x_agenda_importance: float, debtor_amount: float, planck: float
) -> float:
    x_ingest_weight = x_agenda_importance * debtor_amount
    return int(x_ingest_weight / planck) * planck


def _allot_ingest(x_list: list[IdeaUnit], nonallocated_ingest: float, planck: float):
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
    _allot_ingest(x_list, nonallocated_ingest, planck)
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


def get_debtors_roll(x_role: AgendaUnit) -> list[GuyUnit]:
    return [
        x_guyunit for x_guyunit in x_role._guys.values() if x_guyunit.debtor_weight != 0
    ]


def get_ordered_debtors_roll(x_agenda: AgendaUnit) -> list[GuyUnit]:
    guys_ordered_list = get_debtors_roll(x_agenda)
    guys_ordered_list.sort(key=lambda x: (x.debtor_weight, x.guy_id), reverse=True)
    return guys_ordered_list


def migrate_all_facts(src_listener: AgendaUnit, dst_listener: AgendaUnit):
    for x_factunit in src_listener._idearoot._factunits.values():
        base_road = x_factunit.base
        pick_road = x_factunit.pick
        if dst_listener.idea_exists(base_road) is False:
            base_idea = src_listener.get_idea_obj(base_road)
            dst_listener.add_idea(base_idea, base_idea._parent_road)
        if dst_listener.idea_exists(pick_road) is False:
            pick_idea = src_listener.get_idea_obj(pick_road)
            dst_listener.add_idea(pick_idea, pick_idea._parent_road)
        dst_listener.set_fact(base_road, pick_road)


def listen_to_speaker_fact(
    listener: AgendaUnit,
    speaker: AgendaUnit,
    missing_fact_bases: list[RoadUnit] = None,
) -> AgendaUnit:
    if missing_fact_bases is None:
        missing_fact_bases = list(listener.get_missing_fact_bases())
    for missing_fact_base in missing_fact_bases:
        x_factunit = speaker.get_fact(missing_fact_base)
        if x_factunit != None:
            listener.set_fact(
                base=x_factunit.base,
                pick=x_factunit.pick,
                open=x_factunit.open,
                nigh=x_factunit.nigh,
                create_missing_ideas=True,
            )


def listen_to_speaker_intent(listener: AgendaUnit, speaker: AgendaUnit) -> AgendaUnit:
    if listener.guy_exists(speaker._owner_id) is False:
        raise Missing_guy_debtor_poolException(
            f"listener '{listener._owner_id}' agenda is assumed to have {speaker._owner_id} guyunit."
        )
    perspective_agenda = get_speaker_perspective(speaker, listener._owner_id)
    if perspective_agenda._rational is False:
        return _allocate_irrational_debtor_weight(listener, speaker._owner_id)
    if listener._guy_debtor_pool is None:
        return _allocate_inallocable_debtor_weight(listener, speaker._owner_id)
    if listener._owner_id != speaker._owner_id:
        intent = generate_perspective_intent(perspective_agenda)
    else:
        intent = list(perspective_agenda.get_all_pledges().values())
    if len(intent) == 0:
        return _allocate_inallocable_debtor_weight(listener, speaker._owner_id)
    return _ingest_perspective_intent(listener, intent)


def listen_to_intents_duty_work(listener_work: AgendaUnit, listener_userhub: UserHub):
    for x_guyunit in get_ordered_debtors_roll(listener_work):
        if x_guyunit.guy_id == listener_work._owner_id:
            listen_to_speaker_intent(listener_work, listener_userhub.get_duty_agenda())
        else:
            speaker_id = x_guyunit.guy_id
            speaker_work = listener_userhub.dw_speaker_agenda(speaker_id)
            if speaker_work is None:
                speaker_work = create_empty_agenda(listener_work, speaker_id)
            listen_to_speaker_intent(listener_work, speaker_work)


def listen_to_intents_role_job(listener_job: AgendaUnit, healer_userhub: UserHub):
    listener_id = listener_job._owner_id
    for x_guyunit in get_ordered_debtors_roll(listener_job):
        if x_guyunit.guy_id == listener_id:
            listener_role = healer_userhub.get_role_agenda(listener_id)
            listen_to_speaker_intent(listener_job, listener_role)
        else:
            speaker_id = x_guyunit.guy_id
            healer_id = healer_userhub.person_id
            speaker_job = healer_userhub.rj_speaker_agenda(healer_id, speaker_id)
            if speaker_job is None:
                speaker_job = create_empty_agenda(listener_job, speaker_id)
            listen_to_speaker_intent(listener_job, speaker_job)


def listen_to_facts_role_job(new_job: AgendaUnit, healer_userhub: UserHub):
    role = healer_userhub.get_role_agenda(new_job._owner_id)
    migrate_all_facts(role, new_job)
    for x_guyunit in get_ordered_debtors_roll(new_job):
        if x_guyunit.guy_id != new_job._owner_id:
            speaker_job = healer_userhub.get_job_agenda(x_guyunit.guy_id)
            if speaker_job != None:
                listen_to_speaker_fact(new_job, speaker_job)


def listen_to_facts_duty_work(new_work: AgendaUnit, listener_userhub: UserHub):
    migrate_all_facts(listener_userhub.get_duty_agenda(), new_work)
    for x_guyunit in get_ordered_debtors_roll(new_work):
        speaker_id = x_guyunit.guy_id
        if speaker_id != new_work._owner_id:
            speaker_work = listener_userhub.dw_speaker_agenda(speaker_id)
            if speaker_work != None:
                listen_to_speaker_fact(new_work, speaker_work)


def listen_to_debtors_roll_duty_work(listener_userhub: UserHub) -> AgendaUnit:
    duty = listener_userhub.get_duty_agenda()
    new_agenda = create_listen_basis(duty)
    if duty._guy_debtor_pool is None:
        return new_agenda
    listen_to_intents_duty_work(new_agenda, listener_userhub)
    listen_to_facts_duty_work(new_agenda, listener_userhub)
    return new_agenda


def listen_to_debtors_roll_role_job(
    healer_userhub: UserHub, listener_id: PersonID
) -> AgendaUnit:
    role = healer_userhub.get_role_agenda(listener_id)
    new_role = create_listen_basis(role)
    if role._guy_debtor_pool is None:
        return new_role
    listen_to_intents_role_job(new_role, healer_userhub)
    listen_to_facts_role_job(new_role, healer_userhub)
    return new_role


def listen_to_person_jobs(listener_userhub: UserHub) -> None:
    duty = listener_userhub.get_duty_agenda()
    new_work = create_listen_basis(duty)
    pre_work_dict = new_work.get_dict()
    duty.calc_agenda_metrics()
    new_work.calc_agenda_metrics()

    for x_healer_id, econ_dict in duty._healers_dict.items():
        listener_id = listener_userhub.person_id
        healer_userhub = copy_deepcopy(listener_userhub)
        healer_userhub.person_id = x_healer_id
        _pick_econ_jobs_and_listen(listener_id, econ_dict, healer_userhub, new_work)

    if new_work.get_dict() == pre_work_dict:
        intent = list(duty.get_intent_dict().values())
        _ingest_perspective_intent(new_work, intent)
        listen_to_speaker_fact(new_work, duty)

    listener_userhub.save_work_agenda(new_work)


def _pick_econ_jobs_and_listen(
    listener_id: PersonID,
    econ_dict: dict[RoadUnit],
    healer_userhub: UserHub,
    new_work: AgendaUnit,
):
    for econ_path in econ_dict:
        healer_userhub.econ_road = econ_path
        pick_econ_job_and_listen(listener_id, healer_userhub, new_work)


def pick_econ_job_and_listen(
    listener_person_id: PersonID, healer_userhub: UserHub, new_work: AgendaUnit
):
    listener_id = listener_person_id
    if healer_userhub.job_file_exists(listener_id):
        econ_job = healer_userhub.get_job_agenda(listener_id)
    else:
        econ_job = create_empty_agenda(new_work, new_work._owner_id)
    listen_to_job_intent(new_work, econ_job)


def listen_to_job_intent(listener: AgendaUnit, job: AgendaUnit):
    for x_idea in job._idea_dict.values():
        if listener.idea_exists(x_idea.get_road()) is False:
            listener.add_idea(x_idea, x_idea._parent_road)
        if listener.get_fact(x_idea.get_road()) is False:
            listener.add_idea(x_idea, x_idea._parent_road)
    for x_fact_road, x_fact_unit in job._idearoot._factunits.items():
        listener._idearoot.set_factunit(x_fact_unit)
    listener.calc_agenda_metrics()


def create_job_file_from_role_file(healer_userhub: UserHub, person_id: PersonID):
    x_job = listen_to_debtors_roll_role_job(healer_userhub, listener_id=person_id)
    healer_userhub.save_job_agenda(x_job)


def create_work_file_from_duty_file(userhub: UserHub):
    x_work = listen_to_debtors_roll_duty_work(userhub)
    userhub.save_work_agenda(x_work)
