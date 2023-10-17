from src.contract.contract import ContractUnit
from src.contract.idea import IdeaKid
from src.contract.required_idea import RequiredUnit
from src.contract.party import partyunit_shop, partylink_shop
from src.contract.group import groupunit_shop
from src.contract.examples.example_contracts import (
    get_contract_with_4_levels as example_contracts_get_contract_with_4_levels,
    get_contract_with7amCleanTableRequired as example_contracts_get_contract_with7amCleanTableRequired,
    get_assignment_contract_example1 as example_contract_get_assignment_contract_example1,
)
from src.cure.examples.example_healers import (
    get_contract_assignment_laundry_example1,
)


def test_contractunit_get_assignment_ReturnsContract():
    # GIVEN
    jes_text = "jessi"
    jes1_cx = ContractUnit(_healer=jes_text)
    jes1_cx.set_groupunits_empty_if_null()

    # WHEN
    bob_text = "bob"
    contract_x = ContractUnit(_healer=jes_text)
    contract_x.set_groupunits_empty_if_null()
    assignor_known_partys_x = {}
    cx_assignment = jes1_cx.get_assignment(
        contract_x=contract_x,
        assignor_partys=assignor_known_partys_x,
        assignor_title=bob_text,
    )

    # THEN
    assert str(type(cx_assignment)) == "<class 'src.contract.contract.ContractUnit'>"
    assert cx_assignment == contract_x


def test_contractunit_get_assignment_ReturnsEmptyBecauseAssignorIsNotInPartys():
    # GIVEN
    noa_text = "Noa"
    noa_cx = example_contracts_get_contract_with_4_levels()
    noa_cx.set_partyunit(partyunit_shop(title=noa_text))
    zia_text = "Zia"
    yao_text = "Yao"
    noa_cx.set_partyunit(partyunit_shop(title=zia_text))
    noa_cx.set_partyunit(partyunit_shop(title=yao_text))

    # WHEN
    bob_text = "bob"
    cx = ContractUnit(_healer=noa_text)
    tx = ContractUnit()
    tx.set_partys_empty_if_null()
    tx.set_partyunit(partyunit=partyunit_shop(title=zia_text))
    tx.set_partyunit(partyunit=partyunit_shop(title=noa_text))

    cx_assignment = noa_cx.get_assignment(cx, tx._partys, bob_text)

    # THEN
    assert len(noa_cx._partys) == 3
    assert len(cx_assignment._partys) == 0


def test_contractunit_get_assignment_ReturnsCorrectPartys():
    # GIVEN
    jes_text = "Jessi"
    jes_cx = ContractUnit(_healer=jes_text)
    jes_cx.set_partyunit(partyunit_shop(title=jes_text))
    bob_text = "Bob"
    zia_text = "Zia"
    noa_text = "Noa"
    yao_text = "Yao"
    jes_cx.set_partyunit(partyunit_shop(title=bob_text))
    jes_cx.set_partyunit(partyunit_shop(title=zia_text))
    jes_cx.set_partyunit(partyunit_shop(title=noa_text))
    jes_cx.set_partyunit(partyunit_shop(title=yao_text))

    # WHEN
    tx = ContractUnit()
    tx.set_partys_empty_if_null()
    tx.set_partyunit(partyunit=partyunit_shop(title=bob_text))
    tx.set_partyunit(partyunit=partyunit_shop(title=zia_text))
    tx.set_partyunit(partyunit=partyunit_shop(title=noa_text))

    empty_cx = ContractUnit(_healer=jes_text)
    cx_assignment = jes_cx.get_assignment(empty_cx, tx._partys, bob_text)

    # THEN
    assert len(cx_assignment._partys) == 3
    assert cx_assignment._partys.get(bob_text) != None
    assert cx_assignment._partys.get(zia_text) != None
    assert cx_assignment._partys.get(noa_text) != None
    assert cx_assignment._partys.get(yao_text) is None


def test_contractunit_get_assignment_ReturnsCorrectGroups_Scenario1():
    # GIVEN
    jes_text = "Jessi"
    jes_cx = ContractUnit(_healer=jes_text)
    jes_cx.set_partyunit(partyunit_shop(title=jes_text))
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_cx.set_partyunit(partyunit_shop(title=bob_text))
    jes_cx.set_partyunit(partyunit_shop(title=noa_text))
    jes_cx.set_partyunit(partyunit_shop(title=eli_text))
    swim_text = "swimmers"
    jes_cx.set_groupunit(groupunit_shop(brand=swim_text))
    swim_group = jes_cx._groups.get(swim_text)
    swim_group.set_partylink(partylink_shop(bob_text))

    hike_text = "hikers"
    jes_cx.set_groupunit(groupunit_shop(brand=hike_text))
    hike_group = jes_cx._groups.get(hike_text)
    hike_group.set_partylink(partylink_shop(bob_text))
    hike_group.set_partylink(partylink_shop(noa_text))

    hunt_text = "hunters"
    jes_cx.set_groupunit(groupunit_shop(brand=hunt_text))
    hike_group = jes_cx._groups.get(hunt_text)
    hike_group.set_partylink(partylink_shop(noa_text))
    hike_group.set_partylink(partylink_shop(eli_text))

    # WHEN
    tx = ContractUnit()
    tx.set_partys_empty_if_null()
    zia_text = "Zia"
    yao_text = "Yao"
    tx.set_partyunit(partyunit=partyunit_shop(title=bob_text))
    tx.set_partyunit(partyunit=partyunit_shop(title=zia_text))
    tx.set_partyunit(partyunit=partyunit_shop(title=noa_text))

    empty_cx = ContractUnit(_healer=jes_text)
    cx_assignment = jes_cx.get_assignment(empty_cx, tx._partys, bob_text)

    # THEN
    assert len(cx_assignment._groups) == 5
    assert cx_assignment._groups.get(bob_text) != None
    assert cx_assignment._groups.get(noa_text) != None
    assert cx_assignment._groups.get(zia_text) is None
    assert cx_assignment._groups.get(yao_text) is None
    assert cx_assignment._groups.get(swim_text) != None
    assert cx_assignment._groups.get(hike_text) != None
    assert cx_assignment._groups.get(hunt_text) != None
    hunt_group = cx_assignment._groups.get(hunt_text)
    assert hunt_group._partys.get(noa_text) != None
    assert len(hunt_group._partys) == 1


def test_contract__get_assignor_promise_ideas_ReturnsCorrectIdeaRoads():
    # GIVEN
    cx = example_contracts_get_contract_with7amCleanTableRequired()
    cx.set_contract_metrics()

    # WHEN
    assignor_promises = cx._get_assignor_promise_ideas(cx, "any")

    # THEN
    print(f"{assignor_promises=}")
    x_dict = {
        f"{cx._cure_handle},work": -1,
        f"{cx._cure_handle},housework,clean table": -1,
        f"{cx._cure_handle},housework,clean table,remove dishs": -1,
        f"{cx._cure_handle},housework,clean table,get soap": -1,
        f"{cx._cure_handle},housework,clean table,get soap,grab soap": -1,
        f"{cx._cure_handle},feed cat": -1,
    }
    assert assignor_promises == x_dict


def test_contract__get_relevant_roads_EmptyRoadReturnsEmpty():
    # GIVEN
    cx = example_contracts_get_contract_with_4_levels()
    cx.set_contract_metrics()

    # WHEN
    relevant_roads = cx._get_relevant_roads({})

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 0
    assert relevant_roads == {}


def test_contract__get_relevant_roads_RootRoadReturnsOnlyItself():
    # GIVEN
    cx = example_contracts_get_contract_with_4_levels()
    cx.set_contract_metrics()

    # WHEN
    root_dict = {cx._cure_handle: -1}
    relevant_roads = cx._get_relevant_roads(root_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 1
    assert relevant_roads == {cx._cure_handle: -1}


def test_contract__get_relevant_roads_SimpleReturnsOnlyAncestors():
    # GIVEN
    cx = example_contracts_get_contract_with_4_levels()
    cx.set_contract_metrics()

    # WHEN
    week_text = "weekdays"
    week_road = f"{cx._cure_handle},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"
    sun_dict = {sun_road}
    relevant_roads = cx._get_relevant_roads(sun_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert relevant_roads == {cx._cure_handle: -1, sun_road: -1, week_road: -1}


def test_contract__get_relevant_roads_ReturnsSimpleRequiredUnitBase():
    # GIVEN
    healer_text = "Neo"
    cx = ContractUnit(_healer=healer_text)
    casa_text = "casa"
    casa_road = f"{cx._cure_handle},{casa_text}"
    floor_text = "mop floor"
    floor_road = f"{casa_road},{floor_text}"
    floor_idea = IdeaKid(_label=floor_text)
    cx.add_idea(idea_kid=floor_idea, pad=casa_road)

    unim_text = "unimportant"
    unim_road = f"{cx._cure_handle},{unim_text}"
    unim_idea = IdeaKid(_label=unim_text)
    cx.add_idea(idea_kid=unim_idea, pad=cx._cure_handle)

    status_text = "cleaniness status"
    status_road = f"{casa_road},{status_text}"
    status_idea = IdeaKid(_label=status_text)
    cx.add_idea(idea_kid=status_idea, pad=casa_road)
    floor_required = RequiredUnit(base=status_road, sufffacts={})
    floor_required.set_sufffact(sufffact=status_road)
    cx.edit_idea_attr(road=floor_road, required=floor_required)

    # WHEN
    cx.set_contract_metrics()
    floor_dict = {floor_road}
    relevant_roads = cx._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads == {
        cx._cure_handle: -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


def test_contract__get_relevant_roads_ReturnsRequiredUnitBaseAndDescendents():
    # GIVEN
    cx = example_contract_get_assignment_contract_example1()
    casa_text = "casa"
    casa_road = f"{cx._cure_handle},{casa_text}"
    floor_text = "mop floor"
    floor_road = f"{casa_road},{floor_text}"

    unim_text = "unimportant"
    unim_road = f"{cx._cure_handle},{unim_text}"

    status_text = "cleaniness status"
    status_road = f"{casa_road},{status_text}"

    clean_text = "clean"
    clean_road = f"{status_road},{clean_text}"

    very_much_text = "very_much"
    very_much_road = f"{clean_road},{very_much_text}"

    moderately_text = "moderately"
    moderately_road = f"{clean_road},{moderately_text}"

    dirty_text = "dirty"
    dirty_road = f"{status_road},{dirty_text}"

    # WHEN
    cx.set_contract_metrics()
    floor_dict = {floor_road}
    relevant_roads = cx._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 8
    assert relevant_roads.get(clean_road) != None
    assert relevant_roads.get(dirty_road) != None
    assert relevant_roads.get(moderately_road) != None
    assert relevant_roads.get(very_much_road) != None
    assert relevant_roads == {
        cx._cure_handle: -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
        clean_road: -1,
        dirty_road: -1,
        very_much_road: -1,
        moderately_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


# def test_contract__get_relevant_roads_ReturnsRequiredUnitBaseRecursively():
#     pass


def test_contract__get_relevant_roads_numeric_road_ReturnSimple():
    # GIVEN
    healer_text = "Yao"
    cx = ContractUnit(_healer=healer_text)
    work_text = "work"
    work_road = f"{cx._cure_handle},{work_text}"
    cx.add_idea(IdeaKid(_label=work_text), pad=cx._cure_handle)
    work_idea = cx.get_idea_kid(road=work_road)
    day_text = "day_range"
    day_road = f"{cx._cure_handle},{day_text}"
    day_idea = IdeaKid(_label=day_text, _begin=44, _close=110)
    cx.add_idea(day_idea, pad=cx._cure_handle)
    cx.edit_idea_attr(road=work_road, denom=11, numeric_road=day_road)
    assert work_idea._begin == 4
    print(f"{work_idea._label=} {work_idea._begin=} {work_idea._close=}")

    # WHEN
    cx.set_contract_metrics()
    roads_dict = {work_road}
    relevant_roads = cx._get_relevant_roads(roads_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert relevant_roads.get(work_road) != None
    assert relevant_roads.get(day_road) != None
    assert relevant_roads == {
        cx._cure_handle: -1,
        work_road: -1,
        day_road: -1,
    }


def test_contract__get_relevant_roads_range_source_road_ReturnSimple():
    # GIVEN
    healer_text = "Yao"
    cx = ContractUnit(_healer=healer_text)
    min_range_text = "a_minute_range"
    min_range_road = f"{cx._cure_handle},{min_range_text}"
    min_range_idea = IdeaKid(_label=min_range_text, _begin=0, _close=2880)
    cx.add_idea(min_range_idea, pad=cx._cure_handle)

    day_len_text = "day_length"
    day_len_road = f"{cx._cure_handle},{day_len_text}"
    day_len_idea = IdeaKid(_label=day_len_text, _begin=0, _close=1440)
    cx.add_idea(day_len_idea, pad=cx._cure_handle)

    min_days_text = "days in minute_range"
    min_days_road = f"{min_range_road},{min_days_text}"
    min_days_idea = IdeaKid(_label=min_days_text, _range_source_road=day_len_road)
    cx.add_idea(min_days_idea, pad=min_range_road)

    # WHEN
    cx.set_contract_metrics()
    print(f"{cx._idea_dict.keys()}")
    roads_dict = {min_days_road}
    relevant_roads = cx._get_relevant_roads(roads_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads.get(min_range_road) != None
    assert relevant_roads.get(day_len_road) != None
    assert relevant_roads.get(min_days_road) != None
    assert relevant_roads.get(cx._cure_handle) != None
    # min_days_idea = cx.get_idea_kid(road=min_days_road)
    # print(f"{min_days_idea=}")
    # assert 1 == 2


# def test_contract__get_relevant_roads_numeric_road_range_source_road_ReturnEntireRangeTree():
#
def test_contract__set_assignment_ideas_ReturnsCorrectIdeas():
    # GIVEN
    yao_text = "Yao"
    yao_cx = ContractUnit(_healer=yao_text)
    casa_text = "casa"
    casa_road = f"{yao_cx._cure_handle},{casa_text}"
    yao_cx.add_idea(IdeaKid(_label=casa_text), pad=yao_cx._cure_handle)
    yao_cx.set_contract_metrics()

    # WHEN
    bob_text = "Bob"
    bob_contract = ContractUnit(_healer=bob_text)
    relevant_roads = {
        yao_cx._cure_handle: "descendant",
        casa_road: "requirementunit_base",
    }
    yao_cx._set_assignment_ideas(contract_x=bob_contract, relevant_roads=relevant_roads)

    # THEN
    bob_contract.set_contract_metrics()
    print(f"{bob_contract._idea_dict.keys()=}")
    assert len(bob_contract._idea_dict) == 2
    assert bob_contract.get_idea_kid(casa_road) != None


def test_contract__set_assignment_ideas_ReturnsCorrectIdeaRoot_acptfacts():
    # GIVEN
    yao_text = "Yao"
    yao_cx = ContractUnit(_healer=yao_text)

    casa_text = "casa"
    casa_road = f"{yao_cx._cure_handle},{casa_text}"
    yao_cx.add_idea(IdeaKid(_label=casa_text), pad=yao_cx._cure_handle)

    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    yao_cx.add_idea(IdeaKid(basket_text), pad=casa_road)
    yao_cx.set_acptfact(base=basket_road, pick=basket_road)
    # print(f"{list(yao_cx._idearoot._acptfactunits.keys())=}")

    room_text = "room status"
    room_road = f"{casa_road},{room_text}"
    yao_cx.add_idea(IdeaKid(room_text), pad=casa_road)
    yao_cx.set_acptfact(base=room_road, pick=room_road)
    print(f"{list(yao_cx._idearoot._acptfactunits.keys())=}")

    bob_text = "Bob"
    bob_cx = ContractUnit(_healer=bob_text)

    yao_cx.set_contract_metrics()
    bob_cx.set_contract_metrics()
    assert list(yao_cx._idearoot._acptfactunits.keys()) == [basket_road, room_road]
    assert not list(bob_cx._idearoot._acptfactunits.keys())

    # WHEN
    relevant_roads = {
        yao_cx._cure_handle: "descendant",
        casa_road: "requirementunit_base",
        basket_road: "assigned",
    }
    yao_cx._set_assignment_ideas(contract_x=bob_cx, relevant_roads=relevant_roads)

    # THEN
    bob_cx.set_contract_metrics()
    assert bob_cx._idearoot._acptfactunits.get(room_road) is None
    assert list(bob_cx._idearoot._acptfactunits.keys()) == [basket_road]


def test_contract_get_assignment_getsCorrectIdeas_scenario1():
    # GIVEN
    cx = example_contract_get_assignment_contract_example1()
    casa_text = "casa"
    casa_road = f"{cx._cure_handle},{casa_text}"
    floor_text = "mop floor"
    floor_road = f"{casa_road},{floor_text}"
    unim_text = "unimportant"
    unim_road = f"{cx._cure_handle},{unim_text}"
    status_text = "cleaniness status"
    status_road = f"{casa_road},{status_text}"
    clean_text = "clean"
    clean_road = f"{status_road},{clean_text}"
    very_much_text = "very_much"
    very_much_road = f"{clean_road},{very_much_text}"
    moderately_text = "moderately"
    moderately_road = f"{clean_road},{moderately_text}"
    dirty_text = "dirty"
    dirty_road = f"{status_road},{dirty_text}"
    bob_text = "Bob"
    cx.add_partyunit(title=bob_text)

    # WHEN
    assignment_x = cx.get_assignment(
        contract_x=ContractUnit(_healer=bob_text),
        assignor_partys={bob_text: -1},
        assignor_title=bob_text,
    )

    # THEN
    assignment_x.set_contract_metrics()
    print(f"{assignment_x._idea_dict.keys()=}")
    assert len(assignment_x._idea_dict) == 8
    assert assignment_x._idea_dict.get(clean_road) != None
    assert assignment_x._idea_dict.get(dirty_road) != None
    assert assignment_x._idea_dict.get(moderately_road) != None
    assert assignment_x._idea_dict.get(very_much_road) != None
    assert assignment_x._idea_dict.get(unim_road) is None


def test_contract_get_assignment_CorrectlyCreatesAssignmentFile_v1():
    # GIVEN
    america_cx = get_contract_assignment_laundry_example1()
    cure_handle_text = "tiger_econ"
    print(f"{america_cx._cure_handle=} {america_cx._idea_dict.keys()=}")
    america_cx.set_cure_handle(cure_handle_text)
    print(f"{america_cx._cure_handle=} {america_cx._idea_dict.keys()=}")
    do_laundery_idea = america_cx.get_idea_kid("tiger_econ,casa,do_laundry")
    print(f"{do_laundery_idea._requiredunits.keys()=}")

    # WHEN
    joachim_text = "Joachim"
    joachim_contract = ContractUnit(_healer=joachim_text)
    joachim_contract.set_cure_handle(cure_handle_text)
    print(f"{joachim_contract._cure_handle=} {joachim_contract._idea_dict.keys()=}")
    joachim_assignment = america_cx.get_assignment(
        contract_x=joachim_contract,
        assignor_partys={joachim_text: -1, america_cx._healer: -1},
        assignor_title=joachim_text,
    )

    # THEN
    assert joachim_assignment != None
    joachim_assignment.set_contract_metrics()
    assert len(joachim_assignment._idea_dict.keys()) == 9

    # for road_x in joachim_assignment._idea_dict.keys():
    #     print(f"{road_x=}")
    # road_x='A'
    # road_x='A,casa'
    # road_x='A,casa,laundry basket status'
    # road_x='A,casa,laundry basket status,smelly'
    # road_x='A,casa,laundry basket status,half full'
    # road_x='A,casa,laundry basket status,full'
    # road_x='A,casa,laundry basket status,fine'
    # road_x='A,casa,laundry basket status,bare'
    # road_x='A,casa,do_laundry'
    casa_text = "casa"
    casa_road = f"{america_cx._cure_handle},{casa_text}"
    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    b_smel_text = "smelly"
    b_smel_road = f"{basket_road},{b_smel_text}"
    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    b_fine_text = "fine"
    b_fine_road = f"{basket_road},{b_fine_text}"
    b_half_text = "half full"
    b_half_road = f"{basket_road},{b_half_text}"
    laundry_task_text = "do_laundry"
    laundry_task_road = f"{casa_road},{laundry_task_text}"

    assert joachim_assignment._idea_dict.get(casa_road) != None
    assert joachim_assignment._idea_dict.get(basket_road) != None
    assert joachim_assignment._idea_dict.get(b_full_road) != None
    assert joachim_assignment._idea_dict.get(b_smel_road) != None
    assert joachim_assignment._idea_dict.get(b_bare_road) != None
    assert joachim_assignment._idea_dict.get(b_fine_road) != None
    assert joachim_assignment._idea_dict.get(b_half_road) != None
    assert joachim_assignment._idea_dict.get(laundry_task_road) != None

    laundry_do_idea = joachim_assignment.get_idea_kid(laundry_task_road)
    print(f"{laundry_do_idea.promise=}")
    print(f"{laundry_do_idea._requiredunits.keys()=}")
    print(f"{laundry_do_idea._requiredunits.get(basket_road).sufffacts.keys()=}")
    print(f"{laundry_do_idea._acptfactheirs=}")
    print(f"{laundry_do_idea._assignedunit=}")

    assert laundry_do_idea.promise == True
    assert list(laundry_do_idea._requiredunits.keys()) == [basket_road]
    laundry_do_sufffacts = laundry_do_idea._requiredunits.get(basket_road).sufffacts
    assert list(laundry_do_sufffacts.keys()) == [b_full_road, b_smel_road]
    assert list(laundry_do_idea._assignedunit._suffgroups.keys()) == [joachim_text]
    assert list(laundry_do_idea._acptfactheirs.keys()) == [basket_road]

    assert laundry_do_idea._acptfactheirs.get(basket_road).pick == b_full_road

    # print(f"{laundry_do_idea=}")

    assert len(joachim_assignment.get_agenda_items()) == 1
    assert joachim_assignment.get_agenda_items()[0]._label == "do_laundry"
