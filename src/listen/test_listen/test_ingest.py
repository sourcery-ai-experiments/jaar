from src.agenda.fact import factunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.listen import (
    generate_ingest_list,
    _allocate_irrational_debtor_weight,
    generate_perspective_intent,
)


# def test_create_ingest_fact_ReturnsCorrectFact():
#     clean_text = "clean"
#     old_factunit = factunit_shop(clean_text, _weight=14)
#     old_factunit.set_agenda_importance(0.5)
#     swimmers_text = ",swimmers"
#     old_factunit._assignedunit.set_suffidea(swimmers_text)
#     print(f"{old_factunit._weight=}")
#     assert old_factunit._assignedunit.suffidea_exists(swimmers_text)

#     # WHEN
#     yao_text = "Yao"
#     new_factunit = create_ingest_fact(old_factunit, 6, 0.25, listener=yao_text)

#     # THEN
#     assert new_factunit._assignedunit.suffidea_exists(swimmers_text) is False
#     assert new_factunit._assignedunit.suffidea_exists(yao_text)
#     assert new_factunit._weight == 99


def test_allocate_irrational_debtor_weight_CorrectlySetsAgendaAttr():
    yao_text = "Yao"
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_partyunit(zia_text, zia_credor_weight, zia_debtor_weight)
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
    yao_speaker.add_fact(factunit_shop(clean_text), status_road)
    yao_speaker.add_fact(factunit_shop(dirty_text), status_road)
    yao_speaker.add_fact(factunit_shop(sweep_text, pledge=True), casa_road)
    yao_speaker.edit_fact_attr(
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
    zia_agendaunit.add_l1_fact(factunit_shop(clean_text, pledge=True))
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
    clean_factunit = zia_agendaunit.get_fact_obj(clean_road)
    assert ingested_list[0] == clean_factunit
    assert ingested_list[0]._weight == zia_debtor_pool


def test_generate_ingest_list_ReturnsCorrectList_v2():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_agendaunit.add_l1_fact(factunit_shop(clean_text, pledge=True))
    zia_agendaunit.add_l1_fact(factunit_shop(cook_text, pledge=True))
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
    clean_factunit = zia_agendaunit.get_fact_obj(clean_road)
    cook_factunit = zia_agendaunit.get_fact_obj(cook_road)
    assert ingested_list[0] == cook_factunit
    assert ingested_list[0]._weight == 16.0
    assert ingested_list == [cook_factunit, clean_factunit]


def test_generate_ingest_list_ReturnsCorrectList_v3():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_agendaunit.add_l1_fact(factunit_shop(clean_text, pledge=True))
    zia_agendaunit.add_l1_fact(factunit_shop(cook_text, _weight=3, pledge=True))
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
    clean_factunit = zia_agendaunit.get_fact_obj(clean_road)
    cook_factunit = zia_agendaunit.get_fact_obj(cook_road)
    assert ingested_list == [cook_factunit, clean_factunit]
    assert ingested_list[0]._weight == 24.0
    assert ingested_list[1]._weight == 8.0


def test_generate_ingest_list_ReturnsCorrectList_v4():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_agendaunit.add_l1_fact(factunit_shop(clean_text, pledge=True))
    zia_agendaunit.add_l1_fact(factunit_shop(cook_text, _weight=2, pledge=True))
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
    clean_factunit = zia_agendaunit.get_fact_obj(clean_road)
    cook_factunit = zia_agendaunit.get_fact_obj(cook_road)
    assert ingested_list[0]._weight == 22
    assert ingested_list[1]._weight == 10
    assert ingested_list == [cook_factunit, clean_factunit]
