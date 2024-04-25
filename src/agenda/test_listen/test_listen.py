from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.listen import listen_to_jefe, get_ingested_action_items
from copy import deepcopy as copy_deepcopy
from pytest import raises as pytest_raises


def test_get_ingested_action_items_ReturnsCorrectList_v1():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, promise=True))
    zia_debtor_pool = 78
    zia_planck = 2
    assert len(zia_agendaunit.get_intent_dict()) == 1

    # WHEN
    ingested_list = get_ingested_action_items(
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


def test_get_ingested_action_items_ReturnsCorrectList_v2():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, promise=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, promise=True))
    zia_debtor_pool = 32
    zia_planck = 2
    assert len(zia_agendaunit.get_intent_dict()) == 2

    # WHEN
    ingested_list = get_ingested_action_items(
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


def test_get_ingested_action_items_ReturnsCorrectList_v3():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, promise=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=3, promise=True))
    zia_debtor_pool = 32
    zia_planck = 2
    assert len(zia_agendaunit.get_intent_dict()) == 2

    # WHEN
    ingested_list = get_ingested_action_items(
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


def test_get_ingested_action_items_ReturnsCorrectList_v4():
    # GIVEN
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, promise=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=2, promise=True))
    zia_debtor_pool = 32
    zia_planck = 2
    assert len(zia_agendaunit.get_intent_dict()) == 2

    # WHEN
    ingested_list = get_ingested_action_items(
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


def test_listen_to_jefe_ReturnsUnchangedAgenda():
    # GIVEN
    yao_text = "Yao"
    yao_agendaunit = agendaunit_shop(yao_text)
    yao_agendaunit.set_party_pool(100)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)

    # WHEN
    after_yao_agendaunit = listen_to_jefe(yao_agendaunit, zia_agendaunit)

    # THEN
    assert after_yao_agendaunit == yao_agendaunit


def test_listen_to_jefe_RaisesErrorIfPoolIsNotSet():
    # GIVEN
    yao_text = "Yao"
    yao_agendaunit = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        listen_to_jefe(yao_agendaunit, zia_agendaunit)
    assert (
        str(excinfo.value) == "Listening process is not possible without debtor pool."
    )


def test_listen_to_jefe_ReturnsSingleTaskAgenda():
    # GIVEN
    yao_text = "Yao"
    before_yao_agendaunit = agendaunit_shop(yao_text)
    yao_debtor_weight = 77
    before_yao_agendaunit.set_party_pool(yao_debtor_weight)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_partyunit(yao_text)
    clean_text = "clean"
    yao_clean_ideaunit = ideaunit_shop(clean_text, promise=True)
    yao_clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    zia_agendaunit.add_l1_idea(yao_clean_ideaunit)
    assert len(zia_agendaunit.get_intent_dict()) == 0
    zia_yao_agendaunit = copy_deepcopy(zia_agendaunit)
    zia_yao_agendaunit.set_owner_id(yao_text)
    assert len(zia_yao_agendaunit.get_intent_dict()) == 1
    print(f"{zia_yao_agendaunit.get_intent_dict()=}")

    # WHEN
    after_yao_agendaunit = listen_to_jefe(before_yao_agendaunit, zia_agendaunit)

    # THEN
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    x_clean_ideaunit = after_yao_agendaunit.get_idea_obj(clean_road)
    print(f"{x_clean_ideaunit._weight=}")
    assert x_clean_ideaunit._weight != yao_clean_ideaunit._weight
    assert x_clean_ideaunit._weight == yao_debtor_weight
    assert after_yao_agendaunit == before_yao_agendaunit
    assert len(after_yao_agendaunit.get_intent_dict()) == 1


def test_listen_to_jefe_ReturnsLevel2TaskAgenda():
    # GIVEN
    yao_text = "Yao"
    before_yao_agendaunit = agendaunit_shop(yao_text)
    yao_debtor_weight = 77
    before_yao_agendaunit.set_party_pool(yao_debtor_weight)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_partyunit(yao_text)
    clean_text = "clean"
    yao_clean_ideaunit = ideaunit_shop(clean_text, promise=True)
    yao_clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    casa_road = zia_agendaunit.make_l1_road("casa")
    zia_agendaunit.add_idea(yao_clean_ideaunit, casa_road)
    assert len(zia_agendaunit.get_intent_dict()) == 0
    zia_yao_agendaunit = copy_deepcopy(zia_agendaunit)
    zia_yao_agendaunit.set_owner_id(yao_text)
    assert len(zia_yao_agendaunit.get_intent_dict()) == 1
    print(f"{zia_yao_agendaunit.get_intent_dict()=}")

    # WHEN
    after_yao_agendaunit = listen_to_jefe(before_yao_agendaunit, zia_agendaunit)

    # THEN
    clean_road = zia_agendaunit.make_road(casa_road, clean_text)
    x_clean_ideaunit = after_yao_agendaunit.get_idea_obj(clean_road)
    print(f"{x_clean_ideaunit._weight=}")
    assert x_clean_ideaunit._weight != yao_clean_ideaunit._weight
    assert x_clean_ideaunit._weight == yao_debtor_weight
    after_casa_ideaunit = after_yao_agendaunit.get_idea_obj(casa_road)
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == yao_debtor_weight
    assert after_yao_agendaunit == before_yao_agendaunit
    assert len(after_yao_agendaunit.get_intent_dict()) == 1


def test_listen_to_jefe_Returns2IntentIdeasLevel2TaskAgenda():
    # GIVEN
    yao_text = "Yao"
    before_yao_agendaunit = agendaunit_shop(yao_text)
    yao_debtor_weight = 55
    before_yao_agendaunit.set_party_pool(yao_debtor_weight)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_partyunit(yao_text)
    clean_text = "clean"
    cook_text = "cook"
    fly_text = "fly"
    yao_clean_ideaunit = ideaunit_shop(clean_text, promise=True)
    yao_clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_cook_ideaunit = ideaunit_shop(cook_text, promise=True)
    yao_cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_fly_ideaunit = ideaunit_shop(fly_text, promise=True)
    yao_fly_ideaunit._assignedunit.set_suffgroup(yao_text)
    casa_road = zia_agendaunit.make_l1_road("casa")
    fly_road = zia_agendaunit.make_l1_road(fly_text)
    zia_agendaunit.add_idea(yao_clean_ideaunit, casa_road)
    zia_agendaunit.add_idea(yao_cook_ideaunit, casa_road)
    zia_agendaunit.add_l1_idea(yao_fly_ideaunit)
    assert len(zia_agendaunit.get_intent_dict()) == 0
    zia_yao_agendaunit = copy_deepcopy(zia_agendaunit)
    zia_yao_agendaunit.set_owner_id(yao_text)
    assert len(zia_yao_agendaunit.get_intent_dict()) == 3

    # WHEN
    after_yao_agendaunit = listen_to_jefe(before_yao_agendaunit, zia_agendaunit)

    # THEN
    clean_road = zia_agendaunit.make_road(casa_road, clean_text)
    cook_road = zia_agendaunit.make_road(casa_road, cook_text)
    after_cook_ideaunit = after_yao_agendaunit.get_idea_obj(cook_road)
    after_clean_ideaunit = after_yao_agendaunit.get_idea_obj(clean_road)
    after_casa_ideaunit = after_yao_agendaunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_agendaunit.get_idea_obj(fly_road)
    print(f"{after_clean_ideaunit._weight=}")
    assert after_clean_ideaunit._weight != yao_clean_ideaunit._weight
    assert after_clean_ideaunit._weight == 13
    print(f"{after_cook_ideaunit._weight=}")
    assert after_cook_ideaunit._weight != yao_cook_ideaunit._weight
    assert after_cook_ideaunit._weight == 14
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == 27
    assert after_yao_agendaunit == before_yao_agendaunit
    assert len(after_yao_agendaunit.get_intent_dict()) == 3
    assert after_fly_ideaunit._weight != 1
    assert after_fly_ideaunit._weight == 28


def test_listen_to_jefe_Returns2IntentIdeasLevel2TaskAgendaWhereAnIdeaUnitAlreadyExists():
    # GIVEN
    yao_text = "Yao"
    before_yao_agendaunit = agendaunit_shop(yao_text)
    yao_debtor_weight = 55
    before_yao_agendaunit.set_party_pool(yao_debtor_weight)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_partyunit(yao_text)
    dish_text = "dish"
    cook_text = "cook"
    fly_text = "fly"
    yao_dish_ideaunit = ideaunit_shop(dish_text, promise=True)
    yao_dish_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_cook_ideaunit = ideaunit_shop(cook_text, promise=True)
    yao_cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_fly_ideaunit = ideaunit_shop(fly_text, promise=True)
    yao_fly_ideaunit._assignedunit.set_suffgroup(yao_text)
    casa_road = zia_agendaunit.make_l1_road("casa")
    dish_road = zia_agendaunit.make_road(casa_road, dish_text)
    fly_road = zia_agendaunit.make_l1_road(fly_text)
    before_yao_agendaunit.add_idea(yao_dish_ideaunit, casa_road)
    # before_yao_agendaunit.edit_idea_attr(dish_road, weight=999)
    zia_agendaunit.add_idea(yao_dish_ideaunit, casa_road)
    zia_agendaunit.add_idea(yao_cook_ideaunit, casa_road)
    zia_agendaunit.add_l1_idea(yao_fly_ideaunit)
    assert len(zia_agendaunit.get_intent_dict()) == 1
    zia_yao_agendaunit = copy_deepcopy(zia_agendaunit)
    zia_yao_agendaunit.set_owner_id(yao_text)
    assert len(zia_yao_agendaunit.get_intent_dict()) == 3

    # WHEN
    after_yao_agendaunit = listen_to_jefe(before_yao_agendaunit, zia_agendaunit)

    # THEN
    cook_road = zia_agendaunit.make_road(casa_road, cook_text)
    after_cook_ideaunit = after_yao_agendaunit.get_idea_obj(cook_road)
    after_dish_ideaunit = after_yao_agendaunit.get_idea_obj(dish_road)
    after_casa_ideaunit = after_yao_agendaunit.get_idea_obj(casa_road)
    after_fly_ideaunit = after_yao_agendaunit.get_idea_obj(fly_road)
    print(f"{after_dish_ideaunit._weight=}")
    assert after_dish_ideaunit._weight != yao_dish_ideaunit._weight
    assert after_dish_ideaunit._weight == 28
    print(f"{after_cook_ideaunit._weight=}")
    assert after_cook_ideaunit._weight != yao_cook_ideaunit._weight
    assert after_cook_ideaunit._weight == 13
    print(f"{after_casa_ideaunit._weight=}")
    assert after_casa_ideaunit._weight != 1
    assert after_casa_ideaunit._weight == 28
    assert after_yao_agendaunit == before_yao_agendaunit
    assert len(after_yao_agendaunit.get_intent_dict()) == 3
    assert after_fly_ideaunit._weight != 1
    assert after_fly_ideaunit._weight == 28
