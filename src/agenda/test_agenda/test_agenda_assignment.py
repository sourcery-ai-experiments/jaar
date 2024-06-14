from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.reason_idea import reasonunit_shop
from src.agenda.party import partyunit_shop, partylink_shop
from src.agenda.belief import beliefunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_with7amCleanTableReason as example_agendas_get_agenda_with7amCleanTableReason,
    get_assignment_agenda_example1 as example_agenda_get_assignment_agenda_example1,
    get_agenda_assignment_laundry_example1,
)


def test_agendaunit_get_assignment_ReturnsAgenda():
    # GIVEN
    jes_text = "jessi"
    jes1_agenda = agendaunit_shop(_owner_id=jes_text)

    # WHEN
    bob_text = "Bob"
    agenda_x = agendaunit_shop(_owner_id=jes_text)
    assignor_known_partys_x = {}
    x_assignment_agenda = jes1_agenda.get_assignment(
        agenda_x=agenda_x,
        assignor_partys=assignor_known_partys_x,
        assignor_party_id=bob_text,
    )

    # THEN
    assert str(type(x_assignment_agenda)) == "<class 'src.agenda.agenda.AgendaUnit'>"
    assert x_assignment_agenda == agenda_x


def test_agendaunit_get_assignment_ReturnsEmptyBecauseAssignorIsNotInPartys():
    # GIVEN
    noa_text = "Noa"
    noa_agenda = example_agendas_get_agenda_with_4_levels()
    noa_agenda.set_partyunit(partyunit_shop(party_id=noa_text))
    zia_text = "Zia"
    yao_text = "Yao"
    noa_agenda.set_partyunit(partyunit_shop(party_id=zia_text))
    noa_agenda.set_partyunit(partyunit_shop(party_id=yao_text))

    # WHEN
    bob_text = "Bob"
    y_agenda = agendaunit_shop(_owner_id=noa_text)
    x_agenda = agendaunit_shop()
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=zia_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=noa_text))

    x_assignment_agenda = noa_agenda.get_assignment(
        y_agenda, x_agenda._partys, bob_text
    )

    # THEN
    assert len(noa_agenda._partys) == 3
    assert len(x_assignment_agenda._partys) == 0


def test_agendaunit_get_assignment_ReturnsCorrectPartys():
    # GIVEN
    jes_text = "Jessi"
    jes_agenda = agendaunit_shop(_owner_id=jes_text)
    jes_agenda.set_partyunit(partyunit_shop(party_id=jes_text))
    bob_text = "Bob"
    zia_text = "Zia"
    noa_text = "Noa"
    yao_text = "Yao"
    jes_agenda.set_partyunit(partyunit_shop(party_id=bob_text))
    jes_agenda.set_partyunit(partyunit_shop(party_id=zia_text))
    jes_agenda.set_partyunit(partyunit_shop(party_id=noa_text))
    jes_agenda.set_partyunit(partyunit_shop(party_id=yao_text))

    # WHEN
    tx = agendaunit_shop()
    tx.set_partyunit(partyunit=partyunit_shop(party_id=bob_text))
    tx.set_partyunit(partyunit=partyunit_shop(party_id=zia_text))
    tx.set_partyunit(partyunit=partyunit_shop(party_id=noa_text))

    x_agenda = agendaunit_shop(jes_text)
    x_assignment_agenda = jes_agenda.get_assignment(x_agenda, tx._partys, bob_text)

    # THEN
    assert len(x_assignment_agenda._partys) == 3
    assert x_assignment_agenda._partys.get(bob_text) != None
    assert x_assignment_agenda._partys.get(zia_text) != None
    assert x_assignment_agenda._partys.get(noa_text) != None
    assert x_assignment_agenda._partys.get(yao_text) is None


def test_agendaunit_get_assignment_ReturnsCorrectBeliefs_Scenario1():
    # GIVEN
    jes_text = "Jessi"
    jes_agenda = agendaunit_shop(_owner_id=jes_text)
    jes_agenda.set_partyunit(partyunit_shop(party_id=jes_text))
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_agenda.set_partyunit(partyunit_shop(party_id=bob_text))
    jes_agenda.set_partyunit(partyunit_shop(party_id=noa_text))
    jes_agenda.set_partyunit(partyunit_shop(party_id=eli_text))
    swim_text = ",swimmers"
    jes_agenda.set_beliefunit(beliefunit_shop(belief_id=swim_text))
    swim_belief = jes_agenda._beliefs.get(swim_text)
    swim_belief.set_partylink(partylink_shop(bob_text))

    hike_text = ",hikers"
    jes_agenda.set_beliefunit(beliefunit_shop(belief_id=hike_text))
    hike_belief = jes_agenda._beliefs.get(hike_text)
    hike_belief.set_partylink(partylink_shop(bob_text))
    hike_belief.set_partylink(partylink_shop(noa_text))

    hunt_text = ",hunters"
    jes_agenda.set_beliefunit(beliefunit_shop(belief_id=hunt_text))
    hike_belief = jes_agenda._beliefs.get(hunt_text)
    hike_belief.set_partylink(partylink_shop(noa_text))
    hike_belief.set_partylink(partylink_shop(eli_text))

    # WHEN
    tx = agendaunit_shop()
    zia_text = "Zia"
    yao_text = "Yao"
    tx.set_partyunit(partyunit=partyunit_shop(party_id=bob_text))
    tx.set_partyunit(partyunit=partyunit_shop(party_id=zia_text))
    tx.set_partyunit(partyunit=partyunit_shop(party_id=noa_text))

    valueless_agenda = agendaunit_shop(_owner_id=jes_text)
    x_assignment_agenda = jes_agenda.get_assignment(
        valueless_agenda, tx._partys, bob_text
    )

    # THEN
    assert len(x_assignment_agenda._beliefs) == 5
    assert x_assignment_agenda._beliefs.get(bob_text) != None
    assert x_assignment_agenda._beliefs.get(noa_text) != None
    assert x_assignment_agenda._beliefs.get(zia_text) is None
    assert x_assignment_agenda._beliefs.get(yao_text) is None
    assert x_assignment_agenda._beliefs.get(swim_text) != None
    assert x_assignment_agenda._beliefs.get(hike_text) != None
    assert x_assignment_agenda._beliefs.get(hunt_text) != None
    hunt_belief = x_assignment_agenda._beliefs.get(hunt_text)
    assert hunt_belief._partys.get(noa_text) != None
    assert len(hunt_belief._partys) == 1


def test_AgendaUnit_get_assignor_pledge_ideas_ReturnsCorrectIdeaRoadUnits():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with7amCleanTableReason()
    x_agenda.calc_agenda_metrics()

    # WHEN
    assignor_pledges = x_agenda._get_assignor_pledge_ideas(x_agenda, "any")

    # THEN
    print(f"{assignor_pledges=}")
    casa_road = x_agenda.make_l1_road("casa")
    house_road = x_agenda.make_l1_road("housemanagement")
    table_road = x_agenda.make_road(house_road, "clean table")
    dish_road = x_agenda.make_road(table_road, "remove dishs")
    soap_road = x_agenda.make_road(table_road, "get soap")
    grab_road = x_agenda.make_road(soap_road, "grab soap")
    feed_road = x_agenda.make_l1_road("feed cat")

    x_dict = {
        casa_road: -1,
        table_road: -1,
        dish_road: -1,
        soap_road: -1,
        grab_road: -1,
        feed_road: -1,
    }
    assert assignor_pledges == x_dict


def test_AgendaUnit_get_relevant_roads_EmptyRoadUnitReturnsEmpty():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.calc_agenda_metrics()

    # WHEN
    relevant_roads = x_agenda._get_relevant_roads({})

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 0
    assert relevant_roads == {}


def test_AgendaUnit_get_relevant_roads_RootRoadUnitReturnsOnlyItself():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.calc_agenda_metrics()

    # WHEN
    root_dict = {x_agenda._real_id: -1}
    relevant_roads = x_agenda._get_relevant_roads(root_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 1
    assert relevant_roads == {x_agenda._real_id: -1}


def test_AgendaUnit_get_relevant_roads_SimpleReturnsOnlyAncestors():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.calc_agenda_metrics()

    # WHEN
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = x_agenda.make_road(week_road, sun_text)
    sun_dict = {sun_road}
    relevant_roads = x_agenda._get_relevant_roads(sun_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert relevant_roads == {x_agenda._real_id: -1, sun_road: -1, week_road: -1}


def test_AgendaUnit_get_relevant_roads_ReturnsSimpleReasonUnitBase():
    # GIVEN
    neo_agenda = agendaunit_shop(_owner_id="Neo")
    casa_text = "casa"
    casa_road = neo_agenda.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = neo_agenda.make_road(casa_road, floor_text)
    floor_idea = ideaunit_shop(floor_text)
    neo_agenda.add_idea(floor_idea, parent_road=casa_road)

    unim_text = "unimportant"
    unim_road = neo_agenda.make_l1_road(unim_text)
    unim_idea = ideaunit_shop(unim_text)
    neo_agenda.add_idea(unim_idea, parent_road=neo_agenda._real_id)

    status_text = "cleaniness status"
    status_road = neo_agenda.make_road(casa_road, status_text)
    status_idea = ideaunit_shop(status_text)
    neo_agenda.add_idea(status_idea, parent_road=casa_road)
    floor_reason = reasonunit_shop(base=status_road)
    floor_reason.set_premise(premise=status_road)
    neo_agenda.edit_idea_attr(road=floor_road, reason=floor_reason)

    # WHEN
    neo_agenda.calc_agenda_metrics()
    floor_dict = {floor_road}
    relevant_roads = neo_agenda._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads == {
        neo_agenda._real_id: -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


def test_AgendaUnit_get_relevant_roads_ReturnsReasonUnitBaseAndDescendents():
    # GIVEN
    x_agenda = example_agenda_get_assignment_agenda_example1()
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = x_agenda.make_road(casa_road, floor_text)

    unim_text = "unimportant"
    unim_road = x_agenda.make_l1_road(unim_text)

    status_text = "cleaniness status"
    status_road = x_agenda.make_road(casa_road, status_text)

    clean_text = "clean"
    clean_road = x_agenda.make_road(status_road, clean_text)

    very_much_text = "very_much"
    very_much_road = x_agenda.make_road(clean_road, very_much_text)

    moderately_text = "moderately"
    moderately_road = x_agenda.make_road(clean_road, moderately_text)

    dirty_text = "dirty"
    dirty_road = x_agenda.make_road(status_road, dirty_text)

    # WHEN
    x_agenda.calc_agenda_metrics()
    floor_dict = {floor_road}
    relevant_roads = x_agenda._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 8
    assert relevant_roads.get(clean_road) != None
    assert relevant_roads.get(dirty_road) != None
    assert relevant_roads.get(moderately_road) != None
    assert relevant_roads.get(very_much_road) != None
    assert relevant_roads == {
        x_agenda._real_id: -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
        clean_road: -1,
        dirty_road: -1,
        very_much_road: -1,
        moderately_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


# def test_AgendaUnit_get_relevant_roads_ReturnsReasonUnitBaseRecursively():
#     pass


def test_AgendaUnit_get_relevant_roads_numeric_road_ReturnSimple():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(_owner_id=yao_text)
    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    yao_agenda.add_l1_idea(ideaunit_shop(casa_text))
    casa_idea = yao_agenda.get_idea_obj(casa_road)
    day_text = "day_range"
    day_road = yao_agenda.make_l1_road(day_text)
    day_idea = ideaunit_shop(day_text, _begin=44, _close=110)
    yao_agenda.add_l1_idea(day_idea)
    yao_agenda.edit_idea_attr(road=casa_road, denom=11, numeric_road=day_road)
    assert casa_idea._begin == 4
    print(f"{casa_idea._label=} {casa_idea._begin=} {casa_idea._close=}")

    # WHEN
    yao_agenda.calc_agenda_metrics()
    roads_dict = {casa_road}
    relevant_roads = yao_agenda._get_relevant_roads(roads_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert relevant_roads.get(casa_road) != None
    assert relevant_roads.get(day_road) != None
    assert relevant_roads == {
        yao_agenda._real_id: -1,
        casa_road: -1,
        day_road: -1,
    }


def test_AgendaUnit_get_relevant_roads_range_source_road_ReturnSimple():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(_owner_id=yao_text)
    min_range_text = "a_minute_range"
    min_range_road = yao_agenda.make_l1_road(min_range_text)
    min_range_idea = ideaunit_shop(min_range_text, _begin=0, _close=2880)
    yao_agenda.add_l1_idea(min_range_idea)

    day_len_text = "day_length"
    day_len_road = yao_agenda.make_l1_road(day_len_text)
    day_len_idea = ideaunit_shop(day_len_text, _begin=0, _close=1440)
    yao_agenda.add_l1_idea(day_len_idea)

    min_days_text = "days in minute_range"
    min_days_road = yao_agenda.make_road(min_range_road, min_days_text)
    min_days_idea = ideaunit_shop(min_days_text, _range_source_road=day_len_road)
    yao_agenda.add_idea(min_days_idea, parent_road=min_range_road)

    # WHEN
    yao_agenda.calc_agenda_metrics()
    print(f"{yao_agenda._idea_dict.keys()}")
    roads_dict = {min_days_road}
    relevant_roads = yao_agenda._get_relevant_roads(roads_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads.get(min_range_road) != None
    assert relevant_roads.get(day_len_road) != None
    assert relevant_roads.get(min_days_road) != None
    assert relevant_roads.get(yao_agenda._real_id) != None
    # min_days_idea = yao_agenda.get_idea_obj(min_days_road)


# def test_AgendaUnit_get_relevant_roads_numeric_road_range_source_road_ReturnEntireRangeTree():
def test_AgendaUnit_set_assignment_ideas_ReturnsCorrectIdeas():
    # TODO figure out if this test is necessary
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(_owner_id=yao_text)
    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    yao_agenda.add_l1_idea(ideaunit_shop(casa_text))
    yao_agenda.calc_agenda_metrics()

    # WHEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    relevant_roads = {
        yao_agenda._real_id: "descendant",
        casa_road: "An ex",
    }
    yao_agenda._set_assignment_ideas(x_agenda=bob_agenda, relevant_roads=relevant_roads)

    # THEN
    bob_agenda.calc_agenda_metrics()
    print(f"{bob_agenda._idea_dict.keys()=}")
    assert len(bob_agenda._idea_dict) == 2
    assert bob_agenda.get_idea_obj(casa_road) != None


def test_AgendaUnit_set_assignment_ideas_ReturnsCorrect_idearoot_facts():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(_owner_id=yao_text)

    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    yao_agenda.add_l1_idea(ideaunit_shop(casa_text))

    basket_text = "laundry basket status"
    basket_road = yao_agenda.make_road(casa_road, basket_text)
    yao_agenda.add_idea(ideaunit_shop(basket_text), parent_road=casa_road)
    yao_agenda.set_fact(base=basket_road, pick=basket_road)
    # print(f"{list(yao_agenda._idearoot._factunits.keys())=}")

    room_text = "room status"
    room_road = yao_agenda.make_road(casa_road, room_text)
    yao_agenda.add_idea(ideaunit_shop(room_text), parent_road=casa_road)
    yao_agenda.set_fact(base=room_road, pick=room_road)
    print(f"{list(yao_agenda._idearoot._factunits.keys())=}")

    bob_text = "Bob"
    bob_agenda = agendaunit_shop(_owner_id=bob_text)

    yao_agenda.calc_agenda_metrics()
    bob_agenda.calc_agenda_metrics()
    assert list(yao_agenda._idearoot._factunits.keys()) == [basket_road, room_road]
    assert not list(bob_agenda._idearoot._factunits.keys())

    # WHEN
    relevant_roads = {
        yao_agenda._real_id: "descendant",
        casa_road: "not the casa_road",
        basket_road: "assigned",
    }
    yao_agenda._set_assignment_ideas(x_agenda=bob_agenda, relevant_roads=relevant_roads)

    # THEN
    bob_agenda.calc_agenda_metrics()
    assert bob_agenda._idearoot._factunits.get(room_road) is None
    assert list(bob_agenda._idearoot._factunits.keys()) == [basket_road]


def test_AgendaUnit_get_assignment_getsCorrectIdeas_scenario1():
    # GIVEN
    x_agenda = example_agenda_get_assignment_agenda_example1()
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = x_agenda.make_road(casa_road, floor_text)
    unim_text = "unimportant"
    unim_road = x_agenda.make_l1_road(unim_text)
    status_text = "cleaniness status"
    status_road = x_agenda.make_road(casa_road, status_text)
    clean_text = "clean"
    clean_road = x_agenda.make_road(status_road, clean_text)
    very_much_text = "very_much"
    very_much_road = x_agenda.make_road(clean_road, very_much_text)
    moderately_text = "moderately"
    moderately_road = x_agenda.make_road(clean_road, moderately_text)
    dirty_text = "dirty"
    dirty_road = x_agenda.make_road(status_road, dirty_text)
    bob_text = "Bob"
    x_agenda.add_partyunit(party_id=bob_text)

    # WHEN
    assignment_x = x_agenda.get_assignment(
        agenda_x=agendaunit_shop(_owner_id=bob_text),
        assignor_partys={bob_text: -1},
        assignor_party_id=bob_text,
    )

    # THEN
    assignment_x.calc_agenda_metrics()
    print(f"{assignment_x._idea_dict.keys()=}")
    assert len(assignment_x._idea_dict) == 8
    assert assignment_x._idea_dict.get(clean_road) != None
    assert assignment_x._idea_dict.get(dirty_road) != None
    assert assignment_x._idea_dict.get(moderately_road) != None
    assert assignment_x._idea_dict.get(very_much_road) != None
    assert assignment_x._idea_dict.get(unim_road) is None


def test_AgendaUnit_get_assignment_CorrectlyCreatesAssignmentAgendaUnit_v1():
    # GIVEN
    amer_agenda = get_agenda_assignment_laundry_example1()
    real_id_text = "tiger"
    print(f"{amer_agenda._real_id=} {amer_agenda._idea_dict.keys()=}")
    amer_agenda.set_real_id(real_id_text)
    print(f"{amer_agenda._real_id=} {amer_agenda._idea_dict.keys()=}")
    casa_text = "casa"
    casa_road = amer_agenda.make_l1_road(casa_text)
    laundry_task_road_text = "do_laundry"
    laundry_task_road_road = amer_agenda.make_road(casa_road, laundry_task_road_text)
    do_laundry_idea = amer_agenda.get_idea_obj(laundry_task_road_road)
    print(f"{do_laundry_idea._reasonunits.keys()=}")

    # WHEN
    cali_text = "Cali"
    cali_agenda = agendaunit_shop(_owner_id=cali_text)
    cali_agenda.set_real_id(real_id_text)
    print(f"{cali_agenda._real_id=} {cali_agenda._idea_dict.keys()=}")
    cali_assignment = amer_agenda.get_assignment(
        agenda_x=cali_agenda,
        assignor_partys={cali_text: -1, amer_agenda._owner_id: -1},
        assignor_party_id=cali_text,
    )

    # THEN
    assert cali_assignment != None
    cali_assignment.calc_agenda_metrics()
    assert len(cali_assignment._idea_dict.keys()) == 9

    # for road_x in cali_assignment._idea_dict.keys():
    #     print(f"{road_x=}")
    # road_x='A'
    # road_x='A,casa'
    # road_x='A,casa,laundry basket status'
    # road_x='A,casa,laundry basket status,smelly'
    # road_x='A,casa,laundry basket status,half full'
    # road_x='A,casa,laundry basket status,full'
    # road_x='A,casa,laundry basket status,fine'
    # road_x='A,casa,laundry basket status,bare'
    # road_x='A,casa,laundry_task_road'
    casa_text = "casa"
    casa_road = amer_agenda.make_l1_road(casa_text)
    basket_text = "laundry basket status"
    basket_road = amer_agenda.make_road(casa_road, basket_text)
    b_full_text = "full"
    b_full_road = amer_agenda.make_road(basket_road, b_full_text)
    b_smel_text = "smelly"
    b_smel_road = amer_agenda.make_road(basket_road, b_smel_text)
    b_bare_text = "bare"
    b_bare_road = amer_agenda.make_road(basket_road, b_bare_text)
    b_fine_text = "fine"
    b_fine_road = amer_agenda.make_road(basket_road, b_fine_text)
    b_half_text = "half full"
    b_half_road = amer_agenda.make_road(basket_road, b_half_text)

    assert cali_assignment._idea_dict.get(casa_road) != None
    assert cali_assignment._idea_dict.get(basket_road) != None
    assert cali_assignment._idea_dict.get(b_full_road) != None
    assert cali_assignment._idea_dict.get(b_smel_road) != None
    assert cali_assignment._idea_dict.get(b_bare_road) != None
    assert cali_assignment._idea_dict.get(b_fine_road) != None
    assert cali_assignment._idea_dict.get(b_half_road) != None
    assert cali_assignment._idea_dict.get(laundry_task_road_road) != None

    laundry_do_idea = cali_assignment.get_idea_obj(laundry_task_road_road)
    print(f"{laundry_do_idea.pledge=}")
    print(f"{laundry_do_idea._reasonunits.keys()=}")
    print(f"{laundry_do_idea._reasonunits.get(basket_road).premises.keys()=}")
    print(f"{laundry_do_idea._factheirs=}")
    print(f"{laundry_do_idea._assignedunit=}")

    assert laundry_do_idea.pledge == True
    assert list(laundry_do_idea._reasonunits.keys()) == [basket_road]
    laundry_do_premises = laundry_do_idea._reasonunits.get(basket_road).premises
    assert list(laundry_do_premises.keys()) == [b_full_road, b_smel_road]
    assert list(laundry_do_idea._assignedunit._suffbeliefs.keys()) == [cali_text]
    assert list(laundry_do_idea._factheirs.keys()) == [basket_road]

    assert laundry_do_idea._factheirs.get(basket_road).pick == b_full_road

    # print(f"{laundry_do_idea=}")

    assert len(cali_assignment.get_intent_dict()) == 1
    print(f"{cali_assignment.get_intent_dict().keys()=}")
    assert (
        cali_assignment.get_intent_dict().get(laundry_task_road_road)._label
        == laundry_task_road_text
    )
