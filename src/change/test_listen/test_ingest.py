from src.agenda.group import groupunit_shop
from src.agenda.party import partylink_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.change.listen import (
    generate_ingest_list,
    create_empty_agenda,
    create_listen_basis,
    _allocate_irrational_debtor_weight,
    generate_perspective_intent,
)


def test_create_empty_agenda_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    slash_text = "/"
    yao_duty = agendaunit_shop(yao_text, _road_delimiter=slash_text)
    yao_duty.add_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_creditor_pool = 87
    zia_debtor_pool = 81
    yao_duty.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_missing_job_debtor_weight = 22
    role_zia_partyunit = yao_duty.get_party(zia_text)
    role_zia_partyunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    role_zia_partyunit.add_missing_job_debtor_weight(zia_missing_job_debtor_weight)
    swim_group = groupunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_group.set_partylink(partylink_shop(zia_text))
    yao_duty.set_groupunit(swim_group)
    yao_duty.set_party_creditor_pool(zia_creditor_pool, True)
    yao_duty.set_party_debtor_pool(zia_debtor_pool, True)

    # WHEN
    yao_empty_job = create_empty_agenda(yao_duty, x_owner_id=zia_text)

    # THEN
    assert yao_empty_job._owner_id != yao_duty._owner_id
    assert yao_empty_job._owner_id == zia_text
    assert yao_empty_job._real_id == yao_duty._real_id
    assert yao_empty_job._last_change_id is None
    assert yao_empty_job.get_groupunits_dict() == {}
    assert yao_empty_job._road_delimiter == yao_duty._road_delimiter
    assert yao_empty_job._planck == yao_duty._planck
    assert yao_empty_job._monetary_desc is None
    assert yao_empty_job._party_creditor_pool != yao_duty._party_creditor_pool
    assert yao_empty_job._party_creditor_pool is None
    assert yao_empty_job._party_debtor_pool != yao_duty._party_debtor_pool
    assert yao_empty_job._party_debtor_pool is None
    yao_empty_job.calc_agenda_metrics()
    assert yao_empty_job._partys == {}


def test_create_listen_basis_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    slash_text = "/"
    yao_role = agendaunit_shop(yao_text, _road_delimiter=slash_text)
    yao_role.add_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_creditor_pool = 87
    zia_debtor_pool = 81
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_missing_job_debtor_weight = 22
    role_zia_partyunit = yao_role.get_party(zia_text)
    role_zia_partyunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    role_zia_partyunit.add_missing_job_debtor_weight(zia_missing_job_debtor_weight)
    swim_group = groupunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_group.set_partylink(partylink_shop(zia_text))
    yao_role.set_groupunit(swim_group)
    yao_role.set_party_creditor_pool(zia_creditor_pool, True)
    yao_role.set_party_debtor_pool(zia_debtor_pool, True)

    # WHEN
    yao_basis_job = create_listen_basis(yao_role)

    # THEN
    assert yao_basis_job._owner_id == yao_role._owner_id
    assert yao_basis_job._real_id == yao_role._real_id
    assert yao_basis_job._last_change_id == yao_role._last_change_id
    assert yao_basis_job.get_groupunits_dict() == yao_role.get_groupunits_dict()
    assert yao_basis_job._road_delimiter == yao_role._road_delimiter
    assert yao_basis_job._planck == yao_role._planck
    assert yao_basis_job._monetary_desc == yao_role._monetary_desc
    assert yao_basis_job._party_creditor_pool == yao_role._party_creditor_pool
    assert yao_basis_job._party_debtor_pool == yao_role._party_debtor_pool
    yao_basis_job.calc_agenda_metrics()
    assert len(yao_basis_job._idea_dict) != len(yao_role._idea_dict)
    assert len(yao_basis_job._idea_dict) == 1
    job_zia_partyunit = yao_basis_job.get_party(zia_text)
    assert yao_basis_job.get_partys_dict().keys() == yao_role.get_partys_dict().keys()
    assert job_zia_partyunit._irrational_debtor_weight == 0
    assert job_zia_partyunit._missing_job_debtor_weight == 0


# def test_create_ingest_idea_ReturnsCorrectIdea():
#     clean_text = "clean"
#     old_ideaunit = ideaunit_shop(clean_text, _weight=14)
#     old_ideaunit.set_agenda_importance(0.5)
#     swimmers_text = ",swimmers"
#     old_ideaunit._assignedunit.set_suffgroup(swimmers_text)
#     print(f"{old_ideaunit._weight=}")
#     assert old_ideaunit._assignedunit.suffgroup_exists(swimmers_text)

#     # WHEN
#     yao_text = "Yao"
#     new_ideaunit = create_ingest_idea(old_ideaunit, 6, 0.25, listener=yao_text)

#     # THEN
#     assert new_ideaunit._assignedunit.suffgroup_exists(swimmers_text) == False
#     assert new_ideaunit._assignedunit.suffgroup_exists(yao_text)
#     assert new_ideaunit._weight == 99


def test_allocate_irrational_debtor_weight_CorrectlySetsAgendaAttr():
    yao_text = "Yao"
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    zia_partyunit = yao_agenda.get_party(zia_text)
    assert zia_partyunit._irrational_debtor_weight == 0

    # WHEN
    _allocate_irrational_debtor_weight(yao_agenda, zia_text)

    # THEN
    assert zia_partyunit._irrational_debtor_weight == zia_debtor_weight


def test_generate_perspective_intent_CorrectlyGrabsIntentTasks():
    # GIVEN
    yao_text = "Yao"
    yao_speaker = agendaunit_shop(yao_text)
    yao_speaker.add_partyunit(yao_text)
    yao_speaker.set_party_pool(20)
    casa_text = "casa"
    casa_road = yao_speaker.make_l1_road(casa_text)
    status_text = "status"
    status_road = yao_speaker.make_road(casa_road, status_text)
    clean_text = "clean"
    clean_road = yao_speaker.make_road(status_road, clean_text)
    dirty_text = "dirty"
    dirty_road = yao_speaker.make_road(status_road, dirty_text)
    sweep_text = "sweep"
    sweep_road = yao_speaker.make_road(casa_road, sweep_text)
    yao_speaker.add_idea(ideaunit_shop(clean_text), status_road)
    yao_speaker.add_idea(ideaunit_shop(dirty_text), status_road)
    yao_speaker.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
    yao_speaker.edit_idea_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    yao_speaker.set_belief(status_road, clean_road)
    assert len(yao_speaker.get_intent_dict()) == 0

    # WHEN
    intent_list = generate_perspective_intent(yao_speaker)

    # THEN
    assert len(intent_list) == 1


def test_generate_ingest_list_ReturnsCorrectList_v1():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_debtor_pool = 78
    zia_planck = 2
    assert len(zia_agendaunit.get_intent_dict()) == 1

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_agendaunit.get_intent_dict().values()),
        debtor_amount=zia_debtor_pool,
        planck=zia_planck,
    )

    # THEN
    # clean_road = zia_agendaunit.make_l1_road(clean_text)
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    assert ingested_list[0] == clean_ideaunit
    assert ingested_list[0]._weight == zia_debtor_pool


def test_generate_ingest_list_ReturnsCorrectList_v2():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, pledge=True))
    zia_debtor_pool = 32
    zia_planck = 2
    assert len(zia_agendaunit.get_intent_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_agendaunit.get_intent_dict().values()),
        debtor_amount=zia_debtor_pool,
        planck=zia_planck,
    )

    # THEN
    # clean_road = zia_agendaunit.make_l1_road(clean_text)
    assert len(ingested_list) == 2
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    cook_road = zia_agendaunit.make_l1_road(cook_text)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road)
    assert ingested_list[0] == cook_ideaunit
    assert ingested_list[0]._weight == 16.0
    assert ingested_list == [cook_ideaunit, clean_ideaunit]


def test_generate_ingest_list_ReturnsCorrectList_v3():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=3, pledge=True))
    zia_debtor_pool = 32
    zia_planck = 2
    assert len(zia_agendaunit.get_intent_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_agendaunit.get_intent_dict().values()),
        debtor_amount=zia_debtor_pool,
        planck=zia_planck,
    )

    # THEN
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    cook_road = zia_agendaunit.make_l1_road(cook_text)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road)
    assert ingested_list == [cook_ideaunit, clean_ideaunit]
    assert ingested_list[0]._weight == 24.0
    assert ingested_list[1]._weight == 8.0


def test_generate_ingest_list_ReturnsCorrectList_v4():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=2, pledge=True))
    zia_debtor_pool = 32
    zia_planck = 2
    assert len(zia_agendaunit.get_intent_dict()) == 2

    # WHEN
    ingested_list = generate_ingest_list(
        item_list=list(zia_agendaunit.get_intent_dict().values()),
        debtor_amount=zia_debtor_pool,
        planck=zia_planck,
    )

    # THEN
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    cook_road = zia_agendaunit.make_l1_road(cook_text)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road)
    assert ingested_list[0]._weight == 22
    assert ingested_list[1]._weight == 10
    assert ingested_list == [cook_ideaunit, clean_ideaunit]
