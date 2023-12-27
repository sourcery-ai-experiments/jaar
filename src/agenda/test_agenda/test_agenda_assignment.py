from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideacore_shop
from src.agenda.required_idea import requiredunit_shop
from src.agenda.party import partyunit_shop, partylink_shop
from src.agenda.group import groupunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_with7amCleanTableRequired as example_agendas_get_agenda_with7amCleanTableRequired,
    get_assignment_agenda_example1 as example_agenda_get_assignment_agenda_example1,
    get_agenda_assignment_laundry_example1,
)


def test_agendaunit_get_assignment_ReturnsAgenda():
    # GIVEN
    jes_text = "jessi"
    jes1_agenda = agendaunit_shop(_healer=jes_text)

    # WHEN
    bob_text = "bob"
    agenda_x = agendaunit_shop(_healer=jes_text)
    assignor_known_partys_x = {}
    x_assignment_agenda = jes1_agenda.get_assignment(
        agenda_x=agenda_x,
        assignor_partys=assignor_known_partys_x,
        assignor_pid=bob_text,
    )

    # THEN
    assert str(type(x_assignment_agenda)) == "<class 'src.agenda.agenda.AgendaUnit'>"
    assert x_assignment_agenda == agenda_x


def test_agendaunit_get_assignment_ReturnsEmptyBecauseAssignorIsNotInPartys():
    # GIVEN
    noa_text = "Noa"
    noa_agenda = example_agendas_get_agenda_with_4_levels()
    noa_agenda.set_partyunit(partyunit_shop(pid=noa_text))
    zia_text = "Zia"
    yao_text = "Yao"
    noa_agenda.set_partyunit(partyunit_shop(pid=zia_text))
    noa_agenda.set_partyunit(partyunit_shop(pid=yao_text))

    # WHEN
    bob_text = "bob"
    y_agenda = agendaunit_shop(_healer=noa_text)
    x_agenda = agendaunit_shop()
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=zia_text))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=noa_text))

    x_assignment_agenda = noa_agenda.get_assignment(
        y_agenda, x_agenda._partys, bob_text
    )

    # THEN
    assert len(noa_agenda._partys) == 3
    assert len(x_assignment_agenda._partys) == 0


def test_agendaunit_get_assignment_ReturnsCorrectPartys():
    # GIVEN
    jes_text = "Jessi"
    jes_agenda = agendaunit_shop(_healer=jes_text)
    jes_agenda.set_partyunit(partyunit_shop(pid=jes_text))
    bob_text = "Bob"
    zia_text = "Zia"
    noa_text = "Noa"
    yao_text = "Yao"
    jes_agenda.set_partyunit(partyunit_shop(pid=bob_text))
    jes_agenda.set_partyunit(partyunit_shop(pid=zia_text))
    jes_agenda.set_partyunit(partyunit_shop(pid=noa_text))
    jes_agenda.set_partyunit(partyunit_shop(pid=yao_text))

    # WHEN
    tx = agendaunit_shop()
    tx.set_partyunit(partyunit=partyunit_shop(pid=bob_text))
    tx.set_partyunit(partyunit=partyunit_shop(pid=zia_text))
    tx.set_partyunit(partyunit=partyunit_shop(pid=noa_text))

    empty_agenda = agendaunit_shop(_healer=jes_text)
    x_assignment_agenda = jes_agenda.get_assignment(empty_agenda, tx._partys, bob_text)

    # THEN
    assert len(x_assignment_agenda._partys) == 3
    assert x_assignment_agenda._partys.get(bob_text) != None
    assert x_assignment_agenda._partys.get(zia_text) != None
    assert x_assignment_agenda._partys.get(noa_text) != None
    assert x_assignment_agenda._partys.get(yao_text) is None


def test_agendaunit_get_assignment_ReturnsCorrectGroups_Scenario1():
    # GIVEN
    jes_text = "Jessi"
    jes_agenda = agendaunit_shop(_healer=jes_text)
    jes_agenda.set_partyunit(partyunit_shop(pid=jes_text))
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_agenda.set_partyunit(partyunit_shop(pid=bob_text))
    jes_agenda.set_partyunit(partyunit_shop(pid=noa_text))
    jes_agenda.set_partyunit(partyunit_shop(pid=eli_text))
    swim_text = "swimmers"
    jes_agenda.set_groupunit(groupunit_shop(brand=swim_text))
    swim_group = jes_agenda._groups.get(swim_text)
    swim_group.set_partylink(partylink_shop(bob_text))

    hike_text = "hikers"
    jes_agenda.set_groupunit(groupunit_shop(brand=hike_text))
    hike_group = jes_agenda._groups.get(hike_text)
    hike_group.set_partylink(partylink_shop(bob_text))
    hike_group.set_partylink(partylink_shop(noa_text))

    hunt_text = "hunters"
    jes_agenda.set_groupunit(groupunit_shop(brand=hunt_text))
    hike_group = jes_agenda._groups.get(hunt_text)
    hike_group.set_partylink(partylink_shop(noa_text))
    hike_group.set_partylink(partylink_shop(eli_text))

    # WHEN
    tx = agendaunit_shop()
    zia_text = "Zia"
    yao_text = "Yao"
    tx.set_partyunit(partyunit=partyunit_shop(pid=bob_text))
    tx.set_partyunit(partyunit=partyunit_shop(pid=zia_text))
    tx.set_partyunit(partyunit=partyunit_shop(pid=noa_text))

    empty_agenda = agendaunit_shop(_healer=jes_text)
    x_assignment_agenda = jes_agenda.get_assignment(empty_agenda, tx._partys, bob_text)

    # THEN
    assert len(x_assignment_agenda._groups) == 5
    assert x_assignment_agenda._groups.get(bob_text) != None
    assert x_assignment_agenda._groups.get(noa_text) != None
    assert x_assignment_agenda._groups.get(zia_text) is None
    assert x_assignment_agenda._groups.get(yao_text) is None
    assert x_assignment_agenda._groups.get(swim_text) != None
    assert x_assignment_agenda._groups.get(hike_text) != None
    assert x_assignment_agenda._groups.get(hunt_text) != None
    hunt_group = x_assignment_agenda._groups.get(hunt_text)
    assert hunt_group._partys.get(noa_text) != None
    assert len(hunt_group._partys) == 1


def test_agenda__get_assignor_promise_ideas_ReturnsCorrectIdeaRoadUnits():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with7amCleanTableRequired()
    x_agenda.set_agenda_metrics()

    # WHEN
    assignor_promises = x_agenda._get_assignor_promise_ideas(x_agenda, "any")

    # THEN
    print(f"{assignor_promises=}")
    work_road = x_agenda.make_l1_road("work")
    house_road = x_agenda.make_l1_road("housework")
    table_road = x_agenda.make_road(house_road, "clean table")
    dish_road = x_agenda.make_road(table_road, "remove dishs")
    soap_road = x_agenda.make_road(table_road, "get soap")
    grab_road = x_agenda.make_road(soap_road, "grab soap")
    feed_road = x_agenda.make_l1_road("feed cat")

    x_dict = {
        work_road: -1,
        table_road: -1,
        dish_road: -1,
        soap_road: -1,
        grab_road: -1,
        feed_road: -1,
    }
    assert assignor_promises == x_dict


def test_agenda__get_relevant_roads_EmptyRoadUnitReturnsEmpty():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

    # WHEN
    relevant_roads = x_agenda._get_relevant_roads({})

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 0
    assert relevant_roads == {}


def test_agenda__get_relevant_roads_RootRoadUnitReturnsOnlyItself():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

    # WHEN
    root_dict = {x_agenda._economy_id: -1}
    relevant_roads = x_agenda._get_relevant_roads(root_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 1
    assert relevant_roads == {x_agenda._economy_id: -1}


def test_agenda__get_relevant_roads_SimpleReturnsOnlyAncestors():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

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
    assert relevant_roads == {x_agenda._economy_id: -1, sun_road: -1, week_road: -1}


def test_agenda__get_relevant_roads_ReturnsSimpleRequiredUnitBase():
    # GIVEN
    healer_text = "Neo"
    x_agenda = agendaunit_shop(_healer=healer_text)
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = x_agenda.make_road(casa_road, floor_text)
    floor_idea = ideacore_shop(floor_text)
    x_agenda.add_idea(floor_idea, pad=casa_road)

    unim_text = "unimportant"
    unim_road = x_agenda.make_l1_road(unim_text)
    unim_idea = ideacore_shop(unim_text)
    x_agenda.add_idea(unim_idea, pad=x_agenda._economy_id)

    status_text = "cleaniness status"
    status_road = x_agenda.make_road(casa_road, status_text)
    status_idea = ideacore_shop(status_text)
    x_agenda.add_idea(status_idea, pad=casa_road)
    floor_required = requiredunit_shop(base=status_road)
    floor_required.set_sufffact(sufffact=status_road)
    x_agenda.edit_idea_attr(road=floor_road, required=floor_required)

    # WHEN
    x_agenda.set_agenda_metrics()
    floor_dict = {floor_road}
    relevant_roads = x_agenda._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads == {
        x_agenda._economy_id: -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


def test_agenda__get_relevant_roads_ReturnsRequiredUnitBaseAndDescendents():
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
    x_agenda.set_agenda_metrics()
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
        x_agenda._economy_id: -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
        clean_road: -1,
        dirty_road: -1,
        very_much_road: -1,
        moderately_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


# def test_agenda__get_relevant_roads_ReturnsRequiredUnitBaseRecursively():
#     pass


def test_agenda__get_relevant_roads_numeric_road_ReturnSimple():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(_healer=yao_text)
    work_text = "work"
    work_road = yao_agenda.make_road(yao_agenda._economy_id, work_text)
    yao_agenda.add_idea(ideacore_shop(work_text), pad=yao_agenda._economy_id)
    work_idea = yao_agenda.get_idea_obj(work_road)
    day_text = "day_range"
    day_road = yao_agenda.make_road(yao_agenda._economy_id, day_text)
    day_idea = ideacore_shop(day_text, _begin=44, _close=110)
    yao_agenda.add_idea(day_idea, pad=yao_agenda._economy_id)
    yao_agenda.edit_idea_attr(road=work_road, denom=11, numeric_road=day_road)
    assert work_idea._begin == 4
    print(f"{work_idea._label=} {work_idea._begin=} {work_idea._close=}")

    # WHEN
    yao_agenda.set_agenda_metrics()
    roads_dict = {work_road}
    relevant_roads = yao_agenda._get_relevant_roads(roads_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert relevant_roads.get(work_road) != None
    assert relevant_roads.get(day_road) != None
    assert relevant_roads == {
        yao_agenda._economy_id: -1,
        work_road: -1,
        day_road: -1,
    }


def test_agenda__get_relevant_roads_range_source_road_ReturnSimple():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(_healer=yao_text)
    min_range_text = "a_minute_range"
    min_range_road = yao_agenda.make_road(yao_agenda._economy_id, min_range_text)
    min_range_idea = ideacore_shop(min_range_text, _begin=0, _close=2880)
    yao_agenda.add_idea(min_range_idea, pad=yao_agenda._economy_id)

    day_len_text = "day_length"
    day_len_road = yao_agenda.make_road(yao_agenda._economy_id, day_len_text)
    day_len_idea = ideacore_shop(day_len_text, _begin=0, _close=1440)
    yao_agenda.add_idea(day_len_idea, pad=yao_agenda._economy_id)

    min_days_text = "days in minute_range"
    min_days_road = yao_agenda.make_road(min_range_road, min_days_text)
    min_days_idea = ideacore_shop(min_days_text, _range_source_road=day_len_road)
    yao_agenda.add_idea(min_days_idea, pad=min_range_road)

    # WHEN
    yao_agenda.set_agenda_metrics()
    print(f"{yao_agenda._idea_dict.keys()}")
    roads_dict = {min_days_road}
    relevant_roads = yao_agenda._get_relevant_roads(roads_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads.get(min_range_road) != None
    assert relevant_roads.get(day_len_road) != None
    assert relevant_roads.get(min_days_road) != None
    assert relevant_roads.get(yao_agenda._economy_id) != None
    # min_days_idea = yao_agenda.get_idea_obj(min_days_road)


# def test_agenda__get_relevant_roads_numeric_road_range_source_road_ReturnEntireRangeTree():
#
def test_agenda_set_assignment_ideas_ReturnsCorrectIdeas():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(_healer=yao_text)
    casa_text = "casa"
    casa_road = yao_agenda.make_road(yao_agenda._economy_id, casa_text)
    yao_agenda.add_idea(ideacore_shop(casa_text), pad=yao_agenda._economy_id)
    yao_agenda.set_agenda_metrics()

    # WHEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(_healer=bob_text)
    relevant_roads = {
        yao_agenda._economy_id: "descendant",
        casa_road: "requirementunit_base",
    }
    yao_agenda._set_assignment_ideas(x_agenda=bob_agenda, relevant_roads=relevant_roads)

    # THEN
    bob_agenda.set_agenda_metrics()
    print(f"{bob_agenda._idea_dict.keys()=}")
    assert len(bob_agenda._idea_dict) == 2
    assert bob_agenda.get_idea_obj(casa_road) != None


def test_agenda__set_assignment_ideas_ReturnsCorrectIdeaRoot_acptfacts():
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(_healer=yao_text)

    casa_text = "casa"
    casa_road = yao_agenda.make_road(yao_agenda._economy_id, casa_text)
    yao_agenda.add_idea(ideacore_shop(casa_text), pad=yao_agenda._economy_id)

    basket_text = "laundry basket status"
    basket_road = yao_agenda.make_road(casa_road, basket_text)
    yao_agenda.add_idea(ideacore_shop(basket_text), pad=casa_road)
    yao_agenda.set_acptfact(base=basket_road, pick=basket_road)
    # print(f"{list(yao_agenda._idearoot._acptfactunits.keys())=}")

    room_text = "room status"
    room_road = yao_agenda.make_road(casa_road, room_text)
    yao_agenda.add_idea(ideacore_shop(room_text), pad=casa_road)
    yao_agenda.set_acptfact(base=room_road, pick=room_road)
    print(f"{list(yao_agenda._idearoot._acptfactunits.keys())=}")

    bob_text = "Bob"
    bob_agenda = agendaunit_shop(_healer=bob_text)

    yao_agenda.set_agenda_metrics()
    bob_agenda.set_agenda_metrics()
    assert list(yao_agenda._idearoot._acptfactunits.keys()) == [basket_road, room_road]
    assert not list(bob_agenda._idearoot._acptfactunits.keys())

    # WHEN
    relevant_roads = {
        yao_agenda._economy_id: "descendant",
        casa_road: "requirementunit_base",
        basket_road: "assigned",
    }
    yao_agenda._set_assignment_ideas(x_agenda=bob_agenda, relevant_roads=relevant_roads)

    # THEN
    bob_agenda.set_agenda_metrics()
    assert bob_agenda._idearoot._acptfactunits.get(room_road) is None
    assert list(bob_agenda._idearoot._acptfactunits.keys()) == [basket_road]


def test_agenda_get_assignment_getsCorrectIdeas_scenario1():
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
    x_agenda.add_partyunit(pid=bob_text)

    # WHEN
    assignment_x = x_agenda.get_assignment(
        agenda_x=agendaunit_shop(_healer=bob_text),
        assignor_partys={bob_text: -1},
        assignor_pid=bob_text,
    )

    # THEN
    assignment_x.set_agenda_metrics()
    print(f"{assignment_x._idea_dict.keys()=}")
    assert len(assignment_x._idea_dict) == 8
    assert assignment_x._idea_dict.get(clean_road) != None
    assert assignment_x._idea_dict.get(dirty_road) != None
    assert assignment_x._idea_dict.get(moderately_road) != None
    assert assignment_x._idea_dict.get(very_much_road) != None
    assert assignment_x._idea_dict.get(unim_road) is None


def test_agenda_get_assignment_CorrectlyCreatesAssignmentFile_v1():
    # GIVEN
    amer_agenda = get_agenda_assignment_laundry_example1()
    economy_id_text = "tiger_econ"
    print(f"{amer_agenda._economy_id=} {amer_agenda._idea_dict.keys()=}")
    amer_agenda.set_economy_id(economy_id_text)
    print(f"{amer_agenda._economy_id=} {amer_agenda._idea_dict.keys()=}")
    casa_text = "casa"
    casa_road = amer_agenda.make_road(amer_agenda._economy_id, casa_text)
    laundry_task_road_text = "do_laundry"
    laundry_task_road_road = amer_agenda.make_road(casa_road, laundry_task_road_text)
    do_laundery_idea = amer_agenda.get_idea_obj(laundry_task_road_road)
    print(f"{do_laundery_idea._requiredunits.keys()=}")

    # WHEN
    cali_text = "Cali"
    cali_agenda = agendaunit_shop(_healer=cali_text)
    cali_agenda.set_economy_id(economy_id_text)
    print(f"{cali_agenda._economy_id=} {cali_agenda._idea_dict.keys()=}")
    cali_assignment = amer_agenda.get_assignment(
        agenda_x=cali_agenda,
        assignor_partys={cali_text: -1, amer_agenda._healer: -1},
        assignor_pid=cali_text,
    )

    # THEN
    assert cali_assignment != None
    cali_assignment.set_agenda_metrics()
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
    casa_road = amer_agenda.make_road(amer_agenda._economy_id, casa_text)
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
    print(f"{laundry_do_idea.promise=}")
    print(f"{laundry_do_idea._requiredunits.keys()=}")
    print(f"{laundry_do_idea._requiredunits.get(basket_road).sufffacts.keys()=}")
    print(f"{laundry_do_idea._acptfactheirs=}")
    print(f"{laundry_do_idea._assignedunit=}")

    assert laundry_do_idea.promise == True
    assert list(laundry_do_idea._requiredunits.keys()) == [basket_road]
    laundry_do_sufffacts = laundry_do_idea._requiredunits.get(basket_road).sufffacts
    assert list(laundry_do_sufffacts.keys()) == [b_full_road, b_smel_road]
    assert list(laundry_do_idea._assignedunit._suffgroups.keys()) == [cali_text]
    assert list(laundry_do_idea._acptfactheirs.keys()) == [basket_road]

    assert laundry_do_idea._acptfactheirs.get(basket_road).pick == b_full_road

    # print(f"{laundry_do_idea=}")

    assert len(cali_assignment.get_intent_items()) == 1
    assert cali_assignment.get_intent_items()[0]._label == laundry_task_road_text
