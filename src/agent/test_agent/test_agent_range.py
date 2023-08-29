from src.agent.tool import ToolKid
from src.agent.agent import AgentUnit


def test_agentAddingToolWithAddinCorrectlyTransformsRangeScenario1():
    # Given
    src = "src"
    agent_x = AgentUnit(_weight=10, _desc=src)

    l1 = "level1"
    tool_kid_l1 = ToolKid(_weight=30, _desc=l1)
    agent_x.add_tool(walk=src, tool_kid=tool_kid_l1)
    l1_road = f"{src},{l1}"

    rx1 = "range_root_example"
    tool_kid_rx1 = ToolKid(_weight=30, _desc=rx1)
    agent_x.add_tool(walk=l1_road, tool_kid=tool_kid_rx1)
    rx1_road = f"{l1_road},{rx1}"
    agent_x.edit_tool_attr(road=rx1_road, begin=10, close=25)

    y_tool = agent_x.get_tool_kid(road=rx1_road)
    print(f"Add example child tool to road='{rx1_road}'")

    rcA = "range_child_example"
    tool_kid_rcA = ToolKid(_weight=30, _begin=10, _close=25, _desc=rcA)
    agent_x.add_tool(walk=rx1_road, tool_kid=tool_kid_rcA)

    rcA_road = f"{rx1_road},{rcA}"
    x_tool = agent_x.get_tool_kid(road=rcA_road)

    assert x_tool._begin == 10
    assert x_tool._close == 25

    # When
    agent_x.edit_tool_attr(road=rcA_road, addin=7)

    # Then
    assert x_tool._begin == 17
    assert x_tool._close == 32


def test_agentAddingToolWithAddinCorrectlyTransformsRangeScenario2():
    # Given
    src = "src"
    agent_x = AgentUnit(_weight=10, _desc=src)

    l1 = "level1"
    tool_kid_l1 = ToolKid(_weight=30, _desc=l1)
    agent_x.add_tool(walk=src, tool_kid=tool_kid_l1)
    l1_road = f"{src},{l1}"

    rx1 = "range_root_example"
    tool_kid_rx1 = ToolKid(_weight=30, _desc=rx1)
    agent_x.add_tool(walk=l1_road, tool_kid=tool_kid_rx1)
    rx1_road = f"{l1_road},{rx1}"
    agent_x.edit_tool_attr(road=rx1_road, begin=10, close=25)

    y_tool = agent_x.get_tool_kid(road=rx1_road)
    print(f"Add example child tool to road='{rx1_road}'")

    rcA = "range_child_example"
    tool_kid_rcA = ToolKid(_weight=30, _begin=10, _close=25, _desc=rcA)
    agent_x.add_tool(walk=rx1_road, tool_kid=tool_kid_rcA)

    rcA_road = f"{rx1_road},{rcA}"
    x_tool = agent_x.get_tool_kid(road=rcA_road)

    assert x_tool._begin == 10
    assert x_tool._close == 25
    assert x_tool._addin is None

    # When
    agent_x.edit_tool_attr(road=rcA_road, addin=15, denom=5)

    # Then
    assert x_tool._begin == 5
    assert x_tool._close == 8
    assert x_tool._addin == 15
    assert x_tool._denom == 5


def test_get_tool_ranged_kids_CorrectlyReturnsAllChildren():
    # GIVEN
    src_text = "src"
    cx = AgentUnit(_desc=src_text)
    cx.set_time_hreg_tools(c400_count=7)

    # WHEN
    weekunit_road = f"{cx._desc},time,tech,week"
    ranged_tools = cx.get_tool_ranged_kids(tool_road=weekunit_road)

    # # THEN
    assert len(ranged_tools) == 7


def test_get_tool_ranged_kids_CorrectlyReturnsSomeChildrenScen1():
    # GIVEN
    src_text = "src"
    cx = AgentUnit(_desc=src_text)
    cx.set_time_hreg_tools(c400_count=7)

    # WHEN
    weekunit_road = f"{cx._desc},time,tech,week"
    begin_x = 1440
    close_x = 4 * 1440
    ranged_tools = cx.get_tool_ranged_kids(
        tool_road=weekunit_road, begin=begin_x, close=close_x
    )

    # THEN
    # for tool_x in ranged_tools.values():
    #     print(
    #         f"{begin_x=} {close_x=} {tool_x._desc=} {tool_x._begin=} {tool_x._close=} "
    #     )
    assert len(ranged_tools) == 3


def test_get_tool_ranged_kids_CorrectlyReturnsSomeChildrenScen2():
    # GIVEN
    src_text = "src"
    cx = AgentUnit(_desc=src_text)
    cx.set_time_hreg_tools(c400_count=7)

    # WHEN THEN
    week_road = f"{cx._desc},time,tech,week"
    assert len(cx.get_tool_ranged_kids(tool_road=week_road, begin=0, close=1440)) == 1
    assert len(cx.get_tool_ranged_kids(tool_road=week_road, begin=0, close=2000)) == 2
    assert len(cx.get_tool_ranged_kids(tool_road=week_road, begin=0, close=3000)) == 3


def test_get_tool_ranged_kids_CorrectlyReturnsSomeChildrenScen3():
    # GIVEN
    src_text = "src"
    cx = AgentUnit(_desc=src_text)
    cx.set_time_hreg_tools(c400_count=7)

    # WHEN THEN
    week_road = f"{cx._desc},time,tech,week"
    assert len(cx.get_tool_ranged_kids(tool_road=week_road, begin=0)) == 1
    assert len(cx.get_tool_ranged_kids(tool_road=week_road, begin=1440)) == 1
