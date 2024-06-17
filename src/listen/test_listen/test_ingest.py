from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.listen import (
    generate_ingest_list,
    _allocate_irrational_debtor_weight,
    generate_perspective_intent,
)


# def test_create_ingest_idea_ReturnsCorrectIdea():
#     clean_text = "clean"
#     old_ideaunit = ideaunit_shop(clean_text, _weight=14)
#     old_ideaunit.set_agenda_importance(0.5)
#     swimmers_text = ",swimmers"
#     old_ideaunit._assignedunit.set_suffbelief(swimmers_text)
#     print(f"{old_ideaunit._weight=}")
#     assert old_ideaunit._assignedunit.suffbelief_exists(swimmers_text)

#     # WHEN
#     yao_text = "Yao"
#     new_ideaunit = create_ingest_idea(old_ideaunit, 6, 0.25, listener=yao_text)

#     # THEN
#     assert new_ideaunit._assignedunit.suffbelief_exists(swimmers_text) is False
#     assert new_ideaunit._assignedunit.suffbelief_exists(yao_text)
#     assert new_ideaunit._weight == 99


def test_allocate_irrational_debtor_weight_CorrectlySetsAgendaAttr():
    yao_text = "Yao"
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_otherunit = yao_agenda.get_other(zia_text)
    assert zia_otherunit._irrational_debtor_weight == 0

    # WHEN
    _allocate_irrational_debtor_weight(yao_agenda, zia_text)

    # THEN
    assert zia_otherunit._irrational_debtor_weight == zia_debtor_weight


def test_generate_perspective_intent_CorrectlyGrabsIntentTasks():
    # GIVEN
    yao_text = "Yao"
    yao_speaker = agendaunit_shop(yao_text)
    yao_speaker.add_otherunit(yao_text)
    yao_speaker.set_other_pool(20)
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
    yao_speaker.set_fact(status_road, clean_road)
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
