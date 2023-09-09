from src.calendar.calendar import (
    CalendarUnit,
    get_from_json as calendar_get_from_json,
    get_meld_of_calendar_files,
)
from src.calendar.examples.get_calendar_examples_dir import get_calendar_examples_dir
from src.calendar.idea import IdeaCore, IdeaKid
from src.calendar.road import Road
from src.calendar.required_idea import RequiredUnit
from src.calendar.member import memberunit_shop, memberlink_shop
from src.calendar.group import groupunit_shop, grouplink_shop
from src.calendar.road import get_global_root_label as root_label
from src.calendar.examples.example_calendars import (
    get_calendar_with_4_levels as example_calendars_get_calendar_with_4_levels,
    get_calendar_with_4_levels_and_2requireds as example_calendars_get_calendar_with_4_levels_and_2requireds,
    get_calendar_with7amCleanTableRequired as example_calendars_get_calendar_with7amCleanTableRequired,
    get_calendar_with_4_levels_and_2requireds_2acptfacts as example_calendars_get_calendar_with_4_levels_and_2requireds_2acptfacts,
    calendar_v001 as example_calendars_calendar_v001,
)
from src.calendar.x_func import (
    dir_files as x_func_dir_files,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from src.system.examples.env_kit import env_dir_setup_cleanup, get_temp_env_dir
from pytest import raises as pytest_raises


def test_calendarunit_get_assignment_ReturnsCalendar():
    # GIVEN
    jes_text = "jessi"
    jes1_cx = CalendarUnit(_owner=jes_text)
    jes1_cx.set_groupunits_empty_if_null()

    # WHEN
    bob_text = "bob"
    empty_calendar_x = CalendarUnit(_owner=jes_text)
    empty_calendar_x.set_groupunits_empty_if_null()
    assignor_known_members_x = {}
    cx_assignment = jes1_cx.get_assignment(
        empty_calendar=empty_calendar_x,
        assignor_members=assignor_known_members_x,
        assignor_name=bob_text,
    )

    # THEN
    assert str(type(cx_assignment)) == "<class 'src.calendar.calendar.CalendarUnit'>"
    assert cx_assignment == empty_calendar_x


def test_calendarunit_get_assignment_ReturnsEmptyBecauseAssignorIsNotInMembers():
    # GIVEN
    noa_text = "Noa"
    noa_cx = example_calendars_get_calendar_with_4_levels()
    noa_cx.set_memberunit(memberunit_shop(name=noa_text))
    zia_text = "Zia"
    yao_text = "Yao"
    noa_cx.set_memberunit(memberunit_shop(name=zia_text))
    noa_cx.set_memberunit(memberunit_shop(name=yao_text))

    # WHEN
    bob_text = "bob"
    cx = CalendarUnit(_owner=noa_text)
    tx = CalendarUnit()
    tx.set_members_empty_if_null()
    tx.set_memberunit(memberunit=memberunit_shop(name=zia_text))
    tx.set_memberunit(memberunit=memberunit_shop(name=noa_text))

    cx_assignment = noa_cx.get_assignment(cx, tx._members, bob_text)

    # THEN
    assert len(noa_cx._members) == 3
    assert len(cx_assignment._members) == 0


def test_calendarunit_get_assignment_ReturnsCorrectMembers():
    # GIVEN
    jes_text = "Jessi"
    jes_cx = CalendarUnit(_owner=jes_text)
    jes_cx.set_memberunit(memberunit_shop(name=jes_text))
    bob_text = "Bob"
    zia_text = "Zia"
    noa_text = "Noa"
    yao_text = "Yao"
    jes_cx.set_memberunit(memberunit_shop(name=bob_text))
    jes_cx.set_memberunit(memberunit_shop(name=zia_text))
    jes_cx.set_memberunit(memberunit_shop(name=noa_text))
    jes_cx.set_memberunit(memberunit_shop(name=yao_text))

    # WHEN
    tx = CalendarUnit()
    tx.set_members_empty_if_null()
    tx.set_memberunit(memberunit=memberunit_shop(name=bob_text))
    tx.set_memberunit(memberunit=memberunit_shop(name=zia_text))
    tx.set_memberunit(memberunit=memberunit_shop(name=noa_text))

    empty_cx = CalendarUnit(_owner=jes_text)
    cx_assignment = jes_cx.get_assignment(empty_cx, tx._members, bob_text)

    # THEN
    assert len(cx_assignment._members) == 3
    assert cx_assignment._members.get(bob_text) != None
    assert cx_assignment._members.get(zia_text) != None
    assert cx_assignment._members.get(noa_text) != None
    assert cx_assignment._members.get(yao_text) is None


def test_calendarunit_get_assignment_ReturnsCorrectGroups_Scenario1():
    # GIVEN
    jes_text = "Jessi"
    jes_cx = CalendarUnit(_owner=jes_text)
    jes_cx.set_memberunit(memberunit_shop(name=jes_text))
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_cx.set_memberunit(memberunit_shop(name=bob_text))
    jes_cx.set_memberunit(memberunit_shop(name=noa_text))
    jes_cx.set_memberunit(memberunit_shop(name=eli_text))
    swim_text = "swimmers"
    jes_cx.set_groupunit(groupunit_shop(name=swim_text))
    swim_group = jes_cx._groups.get(swim_text)
    swim_group.set_memberlink(memberlink_shop(bob_text))

    hike_text = "hikers"
    jes_cx.set_groupunit(groupunit_shop(name=hike_text))
    hike_group = jes_cx._groups.get(hike_text)
    hike_group.set_memberlink(memberlink_shop(bob_text))
    hike_group.set_memberlink(memberlink_shop(noa_text))

    hunt_text = "hunters"
    jes_cx.set_groupunit(groupunit_shop(name=hunt_text))
    hike_group = jes_cx._groups.get(hunt_text)
    hike_group.set_memberlink(memberlink_shop(noa_text))
    hike_group.set_memberlink(memberlink_shop(eli_text))

    # WHEN
    tx = CalendarUnit()
    tx.set_members_empty_if_null()
    zia_text = "Zia"
    yao_text = "Yao"
    tx.set_memberunit(memberunit=memberunit_shop(name=bob_text))
    tx.set_memberunit(memberunit=memberunit_shop(name=zia_text))
    tx.set_memberunit(memberunit=memberunit_shop(name=noa_text))

    empty_cx = CalendarUnit(_owner=jes_text)
    cx_assignment = jes_cx.get_assignment(empty_cx, tx._members, bob_text)

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
    assert hunt_group._members.get(noa_text) != None
    assert len(hunt_group._members) == 1


def test_calendar__get_assignor_promise_ideas_ReturnsCorrectIdeaRoads():
    # GIVEN
    cx = example_calendars_get_calendar_with7amCleanTableRequired()
    cx.set_calendar_metrics()

    # WHEN
    assignor_promises = cx._get_assignor_promise_ideas(cx, "any")

    # THEN
    print(f"{assignor_promises=}")
    x_dict = {
        "A,work": -1,
        "A,housework,clean table": -1,
        "A,housework,clean table,remove dishs": -1,
        "A,housework,clean table,get soap": -1,
        "A,housework,clean table,get soap,grab soap": -1,
        "A,feed cat": -1,
    }
    assert assignor_promises == x_dict


def test_calendar__get_relevant_roads_EmptyRoadReturnsEmpty():
    # GIVEN
    cx = example_calendars_get_calendar_with_4_levels()
    cx.set_calendar_metrics()

    # WHEN
    relevant_roads = cx._get_relevant_roads({})

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 0
    assert relevant_roads == {}


def test_calendar__get_relevant_roads_RootRoadReturnsOnlyItself():
    # GIVEN
    cx = example_calendars_get_calendar_with_4_levels()
    cx.set_calendar_metrics()

    # WHEN
    root_dict = {root_label(): -1}
    relevant_roads = cx._get_relevant_roads(root_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 1
    assert relevant_roads == {root_label(): -1}


def test_calendar__get_relevant_roads_SimpleReturnsOnlyAncestors():
    # GIVEN
    cx = example_calendars_get_calendar_with_4_levels()
    cx.set_calendar_metrics()

    # WHEN
    week_text = "weekdays"
    week_road = f"{root_label()},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"
    sun_dict = {sun_road}
    relevant_roads = cx._get_relevant_roads(sun_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 3
    assert relevant_roads == {root_label(): -1, sun_road: -1, week_road: -1}


def test_calendar__get_relevant_roads_ReturnsSimpleRequiredUnitBase():
    # GIVEN
    owner_text = "Neo"
    cx = CalendarUnit(_owner=owner_text)
    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    floor_text = "mop floor"
    floor_road = f"{casa_road},{floor_text}"
    floor_idea = IdeaKid(_label=floor_text)
    cx.add_idea(idea_kid=floor_idea, walk=casa_road)

    unim_text = "unimportant"
    unim_road = f"{root_label()},{unim_text}"
    unim_idea = IdeaKid(_label=unim_text)
    cx.add_idea(idea_kid=unim_idea, walk=root_label())

    status_text = "cleaniness status"
    status_road = f"{casa_road},{status_text}"
    status_idea = IdeaKid(_label=status_text)
    cx.add_idea(idea_kid=status_idea, walk=casa_road)
    floor_required = RequiredUnit(base=status_road, sufffacts={})
    floor_required.set_sufffact(sufffact=status_road)
    cx.edit_idea_attr(road=floor_road, required=floor_required)

    # WHEN
    cx.set_calendar_metrics()
    floor_dict = {floor_road}
    relevant_roads = cx._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 4
    assert relevant_roads == {
        root_label(): -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


def test_calendar__get_relevant_roads_ReturnsRequiredUnitBaseAndDescendents():
    # GIVEN
    owner_text = "Neo"
    cx = CalendarUnit(_owner=owner_text)
    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    floor_text = "mop floor"
    floor_road = f"{casa_road},{floor_text}"
    floor_idea = IdeaKid(_label=floor_text)
    cx.add_idea(idea_kid=floor_idea, walk=casa_road)

    unim_text = "unimportant"
    unim_road = f"{root_label()},{unim_text}"
    unim_idea = IdeaKid(_label=unim_text)
    cx.add_idea(idea_kid=unim_idea, walk=root_label())

    status_text = "cleaniness status"
    status_road = f"{casa_road},{status_text}"
    status_idea = IdeaKid(_label=status_text)
    cx.add_idea(idea_kid=status_idea, walk=casa_road)

    clean_text = "clean"
    clean_road = f"{status_road},{clean_text}"
    clean_idea = IdeaKid(_label=clean_text)
    cx.add_idea(idea_kid=clean_idea, walk=clean_road)

    dirty_text = "dirty"
    dirty_road = f"{status_road},{dirty_text}"
    dirty_idea = IdeaKid(_label=dirty_text)
    cx.add_idea(idea_kid=dirty_idea, walk=dirty_road)

    floor_required = RequiredUnit(base=status_road, sufffacts={})
    floor_required.set_sufffact(sufffact=status_road)
    cx.edit_idea_attr(road=floor_road, required=floor_required)

    # WHEN
    cx.set_calendar_metrics()
    floor_dict = {floor_road}
    relevant_roads = cx._get_relevant_roads(floor_dict)

    # THEN
    print(f"{relevant_roads=}")
    assert len(relevant_roads) == 6
    assert relevant_roads == {
        root_label(): -1,
        casa_road: -1,
        status_road: -1,
        floor_road: -1,
        clean_road: -1,
        dirty_road: -1,
    }
    assert relevant_roads.get(unim_road) is None


def test_calendar__get_relevant_roads_ReturnsRequiredUnitBaseRecursively():
    pass


def test_calendar__get_relevant_roads_numeric_road_special_road_ReturnSimple():
    pass


def test_calendar__get_relevant_roads_numeric_road_special_road_ReturnEntireRangeTree():
    pass
