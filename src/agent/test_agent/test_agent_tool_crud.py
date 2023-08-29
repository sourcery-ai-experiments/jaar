from src.agent.examples.example_agents import get_agent_with_4_levels
from src.agent.tool import ToolKid
from src.agent.required import RequiredUnit, acptfactunit_shop
from src.agent.agent import AgentUnit
from src.agent.group import grouplink_shop
from pytest import raises as pytest_raises
from src.agent.road import Road


def test_root_has_kids():
    # GIVEN
    agent_x = AgentUnit(_desc="prom")
    toolroot_x = agent_x._toolroot
    tool1 = ToolKid(_weight=30, _desc="work")
    tool2 = ToolKid(_weight=40, _desc="ulty")

    # WHEN
    agent_x.add_tool(tool_kid=tool1, walk=agent_x._desc)
    agent_x.add_tool(tool_kid=tool2, walk=agent_x._desc)

    # THEN
    assert toolroot_x._weight == 1
    assert toolroot_x._kids
    assert len(toolroot_x._kids) == 2


def test_kid_can_have_kids():
    # GIVEN/WHEN
    agent_x = get_agent_with_4_levels()

    # THEN
    assert agent_x._weight == 10
    assert agent_x._toolroot._kids
    print(f"{len(agent_x._toolroot._kids)=} {agent_x._toolroot._walk=}")
    assert agent_x.get_level_count(level=0) == 1
    weekdays_kids = agent_x._toolroot._kids["weekdays"]._kids
    weekdays_len = len(weekdays_kids)
    print(f"{weekdays_len=} {agent_x._toolroot._walk=}")
    # for tool in weekdays_kids.values():
    #     print(f"{tool._desc=}")
    assert agent_x.get_node_count() == 17
    assert agent_x.get_level_count(level=1) == 4
    assert agent_x.get_level_count(level=2) == 10
    assert agent_x.get_level_count(level=3) == 2


def test_agent_add_tool_CanAddKidToRootTool():
    # GIVEN
    agent_x = get_agent_with_4_levels()
    assert agent_x.get_node_count() == 17
    assert agent_x.get_level_count(level=1) == 4

    new_tool_parent_road = agent_x._desc
    new_tool = ToolKid(_weight=40, _desc="new_tool")

    # WHEN
    agent_x.add_tool(tool_kid=new_tool, walk=new_tool_parent_road)

    # THEN
    print(f"{(agent_x._desc == new_tool_parent_road[0])=}")
    print(f"{(len(new_tool_parent_road) == 1)=}")
    assert agent_x.get_node_count() == 18
    assert agent_x.get_level_count(level=1) == 5


def test_agent_add_tool_CanAddKidToKidTool():
    # GIVEN
    agent_x = get_agent_with_4_levels()
    assert agent_x.get_node_count() == 17
    assert agent_x.get_level_count(level=2) == 10

    new_tool_parent_road = f"{agent_x._desc},work"
    new_tool = ToolKid(_weight=40, _desc="new_york")

    # WHEN
    agent_x.add_tool(tool_kid=new_tool, walk=new_tool_parent_road)

    # THEN
    # print(f"{(agent_x._desc == new_tool_parent_road[0])=}")
    # print(agent_x._toolroot._kids["work"])
    # print(f"{(len(new_tool_parent_road) == 1)=}")
    assert agent_x.get_node_count() == 18
    assert agent_x.get_level_count(level=2) == 11
    assert (
        agent_x._toolroot._kids["work"]._kids["new_york"]._walk
        == f"{agent_x._desc},work"
    )
    agent_x._toolroot._kids["work"]._kids["new_york"].set_road(parent_road="testing")
    assert agent_x._toolroot._kids["work"]._kids["new_york"]._walk == "testing"
    assert agent_x.get_agenda_items


def test_agent_add_tool_CanAddKidToGrandkidTool():
    # GIVEN
    agent_x = get_agent_with_4_levels()
    assert agent_x.get_node_count() == 17
    assert agent_x.get_level_count(level=3) == 2
    new_tool_parent_road = f"{agent_x._desc},weekdays,Wednesday"
    new_tool = ToolKid(_weight=40, _desc="new_tool")

    # WHEN
    agent_x.add_tool(tool_kid=new_tool, walk=new_tool_parent_road)

    # THEN
    print(f"{(agent_x._desc == new_tool_parent_road[0])=}")
    print(agent_x._toolroot._kids["work"])
    print(f"{(len(new_tool_parent_road) == 1)=}")
    assert agent_x.get_node_count() == 18
    assert agent_x.get_level_count(level=3) == 3


def test_agent_add_tool_CanCreateRoadToGrandkidTool():
    # GIVEN
    agent_x = get_agent_with_4_levels()
    assert agent_x.get_node_count() == 17
    assert agent_x.get_level_count(level=3) == 2
    new_tool_parent_road = f"{agent_x._desc},ww2,battles,coralsea"
    new_tool = ToolKid(_weight=40, _desc="USS Saratoga")

    # WHEN
    agent_x.add_tool(tool_kid=new_tool, walk=new_tool_parent_road)

    # THEN
    print(agent_x._toolroot._kids["ww2"])
    print(f"{(len(new_tool_parent_road) == 1)=}")
    assert agent_x._toolroot._kids["ww2"]._desc == "ww2"
    assert agent_x._toolroot._kids["ww2"]._kids["battles"]._desc == "battles"
    assert agent_x.get_node_count() == 21
    assert agent_x.get_level_count(level=3) == 3


def test_agent_add_tool_creates_requireds_tools():
    # GIVEN
    agent_x = get_agent_with_4_levels()
    assert agent_x.get_node_count() == 17
    assert agent_x.get_level_count(level=3) == 2
    src_text = agent_x._toolroot._desc
    new_tool_parent_road = f"{src_text},work,cleaning"
    clean_cookery_text = "clean_cookery"
    clean_cookery_tool = ToolKid(_weight=40, _desc=clean_cookery_text, promise=True)

    buildings_text = "buildings"
    buildings_road = Road(f"{src_text},{buildings_text}")
    cookery_room_text = "cookery"
    cookery_room_road = Road(f"{src_text},{buildings_text},{cookery_room_text}")
    cookery_dirty_text = "dirty"
    cookery_dirty_road = Road(f"{cookery_room_road},{cookery_dirty_text}")
    required_x = RequiredUnit(base=cookery_room_road, sufffacts={})
    required_x.set_sufffact(sufffact=cookery_dirty_road)
    clean_cookery_tool.set_required_unit(required=required_x)

    assert agent_x._toolroot._kids.get(buildings_text) is None

    # WHEN
    agent_x.add_tool(
        tool_kid=clean_cookery_tool,
        walk=new_tool_parent_road,
        create_missing_tools_groups=True,
    )

    # THEN
    print(f"{(len(new_tool_parent_road) == 1)=}")
    # for tool_kid in agent_x._toolroot._kids.values():
    #     print(f"{tool_kid._desc=}")
    assert agent_x._toolroot._kids.get(buildings_text) != None
    assert agent_x.get_tool_kid(road=buildings_road) != None
    assert agent_x.get_tool_kid(road=cookery_dirty_road) != None
    assert agent_x.get_node_count() == 22
    assert agent_x.get_level_count(level=3) == 4


def test_agent_toolroot_is_heir_CorrectlyChecksLineage():
    agent_x = get_agent_with_4_levels()
    sunday_road = f"{agent_x._desc},weekdays,Sunday"
    weekday_road = f"{agent_x._desc},weekdays"
    assert agent_x._toolroot.is_heir(src=weekday_road, heir=weekday_road)
    assert agent_x._toolroot.is_heir(src=weekday_road, heir=sunday_road)
    assert agent_x._toolroot.is_heir(src=sunday_road, heir=weekday_road) == False


def test_agent_del_tool_kid_ToolLevel0CannotBeDeleted():
    # Given
    agent_x = get_agent_with_4_levels()
    root_road = f"{agent_x._desc}"

    # When/Then
    with pytest_raises(Exception) as excinfo:
        agent_x.del_tool_kid(road=root_road)
    assert str(excinfo.value) == "Object cannot delete itself"


def test_agent_del_tool_kid_ToolLevel1CanBeDeleted_ChildrenDeleted():
    # Given
    agent_x = get_agent_with_4_levels()
    weekdays_road = f"{agent_x._desc},weekdays"
    sunday_road = f"{agent_x._desc},weekdays,Sunday"
    assert agent_x.get_tool_kid(road=weekdays_road)
    assert agent_x.get_tool_kid(road=sunday_road)

    # When
    agent_x.del_tool_kid(road=weekdays_road)

    # Then
    with pytest_raises(Exception) as excinfo:
        agent_x.get_tool_kid(road=weekdays_road)
    assert (
        str(excinfo.value)
        == f"Getting tool_desc='weekdays' failed no item at '{weekdays_road}'"
    )
    new_sunday_road = f"{agent_x._desc},Sunday"
    with pytest_raises(Exception) as excinfo:
        agent_x.get_tool_kid(road=new_sunday_road)
    assert (
        str(excinfo.value)
        == f"Getting tool_desc='Sunday' failed no item at '{new_sunday_road}'"
    )


def test_agent_del_tool_kid_ToolLevel1CanBeDeleted_ChildrenInherited():
    # Given
    agent_x = get_agent_with_4_levels()
    weekdays_road = f"{agent_x._desc},weekdays"
    old_sunday_road = f"{agent_x._desc},weekdays,Sunday"
    assert agent_x.get_tool_kid(road=old_sunday_road)

    # When
    agent_x.del_tool_kid(road=weekdays_road, del_children=False)

    # Then
    with pytest_raises(Exception) as excinfo:
        agent_x.get_tool_kid(road=old_sunday_road)
    assert (
        str(excinfo.value)
        == f"Getting tool_desc='Sunday' failed no item at '{old_sunday_road}'"
    )
    new_sunday_road = f"{agent_x._desc},Sunday"
    assert agent_x.get_tool_kid(road=new_sunday_road)
    new_sunday_tool = agent_x.get_tool_kid(road=new_sunday_road)
    assert new_sunday_tool._walk == f"{agent_x._desc}"


def test_agent_del_tool_kid_ToolLevel2CanBeDeleted_ChildrenDeleted():
    # Given
    agent_x = get_agent_with_4_levels()
    monday_road = f"{agent_x._desc},weekdays,Monday"
    assert agent_x.get_tool_kid(road=monday_road)

    # When
    agent_x.del_tool_kid(road=monday_road)

    # Then
    with pytest_raises(Exception) as excinfo:
        agent_x.get_tool_kid(road=monday_road)
    assert (
        str(excinfo.value)
        == f"Getting tool_desc='Monday' failed no item at '{monday_road}'"
    )


def test_agent_del_tool_kid_ToolLevelNCanBeDeleted_ChildrenDeleted():
    # Given
    agent_x = get_agent_with_4_levels()
    states = "nation-state"
    USA = "USA"
    Texas = "Texas"
    texas_road = f"{agent_x._desc},{states},{USA},{Texas}"
    assert agent_x.get_tool_kid(road=texas_road)

    # When
    agent_x.del_tool_kid(road=texas_road)

    # Then
    with pytest_raises(Exception) as excinfo:
        agent_x.get_tool_kid(road=texas_road)
    assert (
        str(excinfo.value)
        == f"Getting tool_desc='Texas' failed no item at '{texas_road}'"
    )


def test_agent_edit_tool_attr_IsAbleToEditAnyAncestor_Tool():
    agent_x = get_agent_with_4_levels()
    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"
    print(f"{work_road=}")
    current_weight = agent_x._toolroot._kids[work_text]._weight
    assert current_weight == 30
    agent_x.edit_tool_attr(road=work_road, weight=23)
    new_weight = agent_x._toolroot._kids[work_text]._weight
    assert new_weight == 23

    # uid: int = None,
    agent_x._toolroot._kids[work_text]._uid = 34
    uid_curr = agent_x._toolroot._kids[work_text]._uid
    assert uid_curr == 34
    agent_x.edit_tool_attr(road=work_road, uid=23)
    uid_new = agent_x._toolroot._kids[work_text]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    agent_x._toolroot._kids[work_text]._begin = 39
    begin_curr = agent_x._toolroot._kids[work_text]._begin
    assert begin_curr == 39
    agent_x._toolroot._kids[work_text]._close = 43
    close_curr = agent_x._toolroot._kids[work_text]._close
    assert close_curr == 43
    agent_x.edit_tool_attr(road=work_road, begin=25, close=29)
    assert agent_x._toolroot._kids[work_text]._begin == 25
    assert agent_x._toolroot._kids[work_text]._close == 29

    # acptfactunit: acptfactunit_shop = None,
    # agent_x._toolroot._kids[work_text]._acptfactunits = None
    assert agent_x._toolroot._kids[work_text]._acptfactunits is None
    acptfact_road = "src,weekdays,Sunday"
    acptfactunit_x = acptfactunit_shop(base=acptfact_road, pick=acptfact_road)

    work_acptfactunits = agent_x._toolroot._kids[work_text]._acptfactunits
    print(f"{work_acptfactunits=}")
    agent_x.edit_tool_attr(road=work_road, acptfactunit=acptfactunit_x)
    work_acptfactunits = agent_x._toolroot._kids[work_text]._acptfactunits
    print(f"{work_acptfactunits=}")
    assert agent_x._toolroot._kids[work_text]._acptfactunits == {
        acptfactunit_x.base: acptfactunit_x
    }

    # _descendant_promise_count: int = None,
    agent_x._toolroot._kids[work_text]._descendant_promise_count = 81
    _descendant_promise_count_curr = agent_x._toolroot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_curr == 81
    agent_x.edit_tool_attr(road=work_road, descendant_promise_count=67)
    _descendant_promise_count_new = agent_x._toolroot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_new == 67

    # _all_member_credit: bool = None,
    agent_x._toolroot._kids[work_text]._all_member_credit = 74
    _all_member_credit_curr = agent_x._toolroot._kids[work_text]._all_member_credit
    assert _all_member_credit_curr == 74
    agent_x.edit_tool_attr(road=work_road, all_member_credit=59)
    _all_member_credit_new = agent_x._toolroot._kids[work_text]._all_member_credit
    assert _all_member_credit_new == 59

    # _all_member_debt: bool = None,
    agent_x._toolroot._kids[work_text]._all_member_debt = 74
    _all_member_debt_curr = agent_x._toolroot._kids[work_text]._all_member_debt
    assert _all_member_debt_curr == 74
    agent_x.edit_tool_attr(road=work_road, all_member_debt=59)
    _all_member_debt_new = agent_x._toolroot._kids[work_text]._all_member_debt
    assert _all_member_debt_new == 59

    # _grouplink: dict = None,
    agent_x._toolroot._kids[work_text]._grouplinks = {
        "fun": grouplink_shop(name="fun", creditor_weight=1, debtor_weight=7)
    }
    _grouplinks = agent_x._toolroot._kids[work_text]._grouplinks
    assert _grouplinks == {
        "fun": grouplink_shop(name="fun", creditor_weight=1, debtor_weight=7)
    }
    agent_x.edit_tool_attr(
        road=work_road,
        grouplink=grouplink_shop(name="fun", creditor_weight=4, debtor_weight=8),
    )
    assert agent_x._toolroot._kids[work_text]._grouplinks == {
        "fun": grouplink_shop(name="fun", creditor_weight=4, debtor_weight=8)
    }

    # _is_expanded: dict = None,
    agent_x._toolroot._kids[work_text]._is_expanded = "what"
    _is_expanded = agent_x._toolroot._kids[work_text]._is_expanded
    assert _is_expanded == "what"
    agent_x.edit_tool_attr(road=work_road, is_expanded=True)
    assert agent_x._toolroot._kids[work_text]._is_expanded == True

    # promise: dict = None,
    agent_x._toolroot._kids[work_text].promise = "funfun3"
    action = agent_x._toolroot._kids[work_text].promise
    assert action == "funfun3"
    agent_x.edit_tool_attr(road=work_road, promise=True)
    assert agent_x._toolroot._kids[work_text].promise == True

    # _problem_bool
    agent_x._toolroot._kids[work_text]._problem_bool = "heat2"
    _problem_bool = agent_x._toolroot._kids[work_text]._problem_bool
    assert _problem_bool == "heat2"
    agent_x.edit_tool_attr(road=work_road, problem_bool=True)
    assert agent_x._toolroot._kids[work_text]._problem_bool == True

    # _special_road: dict = None,
    agent_x._toolroot._kids[work_text]._special_road = "fun3rol"
    special_road = agent_x._toolroot._kids[work_text]._special_road
    assert special_road == "fun3rol"
    agent_x.edit_tool_attr(road=work_road, special_road="my,work,end")
    assert agent_x._toolroot._kids[work_text]._special_road == "my,work,end"


def test_agent_edit_tool_attr_agentIsAbleToEdit_on_meld_weight_action_AnyToolIfInvaildThrowsError():
    agent_x = get_agent_with_4_levels()
    work_road = f"{agent_x._desc},work"

    # When/Then
    with pytest_raises(Exception) as excinfo:
        agent_x.edit_tool_attr(road=work_road, on_meld_weight_action="yahoo9")
    assert (
        str(excinfo.value)
        == "ToolCore unit 'work' cannot have on_meld_weight_action 'yahoo9'."
    )


def test_agent_edit_tool_attr_agentIsAbleToEditDenomAnyToolIfInvaildDenomThrowsError():
    src = "src"
    agent_x = AgentUnit(_desc=src)
    # When/Then
    with pytest_raises(Exception) as excinfo:
        agent_x.edit_tool_attr(road="", denom=46)
    assert str(excinfo.value) == "Root Tool cannot have numor denom reest."

    work = "work"
    w_road = f"{src},{work}"
    work_tool = ToolKid(_desc=work)
    agent_x.add_tool(work_tool, walk=src)
    clean = "clean"
    clean_tool = ToolKid(_desc=clean)
    c_road = f"{w_road},{clean}"
    agent_x.add_tool(clean_tool, walk=w_road)

    # When/Then
    with pytest_raises(Exception) as excinfo:
        agent_x.edit_tool_attr(road=c_road, denom=46)
    assert (
        str(excinfo.value)
        == "Tool cannot edit numor=1/denom/reest of 'src,work,clean' if parent 'src,work' or toolcore._numeric_road does not have begin/close range"
    )

    # Given
    agent_x.edit_tool_attr(road=w_road, begin=44, close=110)
    agent_x.edit_tool_attr(road=c_road, denom=11)
    clean_tool = agent_x.get_tool_kid(road=c_road)
    assert clean_tool._begin == 4
    assert clean_tool._close == 10


def test_agent_edit_tool_attr_agentIsAbleToEditDenomAnyToolInvaildDenomThrowsError():
    # Given
    src = "src"
    agent_x = AgentUnit(_desc=src)
    work = "work"
    w_road = f"{src},{work}"
    work_tool = ToolKid(_desc=work, _begin=8, _close=14)
    agent_x.add_tool(work_tool, walk=src)

    clean = "clean"
    clean_tool = ToolKid(_desc=clean, _denom=1)
    c_road = f"{w_road},{clean}"
    agent_x.add_tool(clean_tool, walk=w_road)

    clean_tool = agent_x.get_tool_kid(road=c_road)

    day = "day_range"
    day_tool = ToolKid(_desc=day, _begin=44, _close=110)
    day_road = f"{src},{day}"
    agent_x.add_tool(day_tool, walk=src)

    # When/Then
    with pytest_raises(Exception) as excinfo:
        agent_x.edit_tool_attr(road=c_road, numeric_road=day_road)
    assert (
        str(excinfo.value)
        == "Tool has begin-close range parent, cannot have numeric_road"
    )

    agent_x.edit_tool_attr(road=w_road, numeric_road=day_road)


def test_agent_edit_tool_attr_agentWhenParentAndNumeric_roadBothHaveRangeThrowError():
    # Given
    src = "src"
    agent_x = AgentUnit(_desc=src)
    work = "work"
    w_road = f"{src},{work}"
    work_tool = ToolKid(_desc=work)
    agent_x.add_tool(work_tool, walk=src)
    day = "day_range"
    day_tool = ToolKid(_desc=day, _begin=44, _close=110)
    day_road = f"{src},{day}"
    agent_x.add_tool(day_tool, walk=src)

    work_tool2 = agent_x.get_tool_kid(road=w_road)
    assert work_tool2._begin is None
    assert work_tool2._close is None

    with pytest_raises(Exception) as excinfo:
        agent_x.edit_tool_attr(road=w_road, denom=11)
    assert (
        str(excinfo.value)
        == "Tool cannot edit numor=1/denom/reest of 'src,work' if parent 'src' or toolcore._numeric_road does not have begin/close range"
    )

    # When
    agent_x.edit_tool_attr(road=w_road, numeric_road=day_road)

    # Then
    work_tool3 = agent_x.get_tool_kid(road=w_road)
    assert work_tool3._addin is None
    assert work_tool3._numor is None
    assert work_tool3._denom is None
    assert work_tool3._reest is None
    assert work_tool3._begin == 44
    assert work_tool3._close == 110
    agent_x.edit_tool_attr(road=w_road, denom=11, numeric_road=day_road)
    assert work_tool3._begin == 4
    assert work_tool3._close == 10
    assert work_tool3._numor == 1
    assert work_tool3._denom == 11
    assert work_tool3._reest == False
    assert work_tool3._addin == 0


def test_agent_add_tool_MustReorderKidsDictToBeAlphabetical():
    # Given
    src_text = "src"
    ax = AgentUnit(_desc=src_text)
    work_text = "work"
    ax.add_tool(ToolKid(_desc=work_text), walk=src_text)
    swim_text = "swim"
    ax.add_tool(ToolKid(_desc=swim_text), walk=src_text)

    # WHEN
    tool_list = list(ax._toolroot._kids.values())

    # THEN
    assert tool_list[0]._desc == swim_text
