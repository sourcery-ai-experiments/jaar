from src.agent.examples.example_agents import (
    get_agent_with_4_levels as example_agents_get_agent_with_4_levels,
)
from src.agent.member import MemberName
from src.agent.tool import ToolKid
from src.agent.agent import AgentUnit
from src.agent.group import Groupline, GroupLink
from pytest import raises as pytest_raises


def test_set_agent_metrics_CorrectlyClearsDescendantAttributes():
    agent_x = example_agents_get_agent_with_4_levels()

    # tool "src,weekdays,Sunday"
    # tool "src,weekdays,Monday"
    # tool "src,weekdays,Tuesday"
    # tool "src,weekdays,Wednesday"
    # tool "src,weekdays,Thursday"
    # tool "src,weekdays,Friday"
    # tool "src,weekdays,Saturday"
    # tool "src,weekdays"
    # tool "src,nation-state,USA,Texas"
    # tool "src,nation-state,USA,Oregon"
    # tool "src,nation-state,USA"
    # tool "src,nation-state,France"
    # tool "src,nation-state,Brazil"
    # tool "src,nation-state"
    # tool "work"  # , promise=True)
    # tool "feed cat"  # , promise=True)
    # tool "src"

    # test root init status:
    yrx = agent_x._toolroot
    assert yrx._descendant_promise_count is None
    assert yrx._all_member_credit is None
    assert yrx._all_member_debt is None
    assert yrx._kids["work"]._descendant_promise_count is None
    assert yrx._kids["work"]._all_member_credit is None
    assert yrx._kids["work"]._all_member_debt is None
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count is None
    assert yrx._kids["weekdays"]._kids["Monday"]._all_member_credit is None
    assert yrx._kids["weekdays"]._kids["Monday"]._all_member_debt is None

    yrx._descendant_promise_count = -2
    yrx._all_member_credit = -2
    yrx._all_member_debt = -2
    yrx._kids["work"]._descendant_promise_count = -2
    yrx._kids["work"]._all_member_credit = -2
    yrx._kids["work"]._all_member_debt = -2
    yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count = -2
    yrx._kids["weekdays"]._kids["Monday"]._all_member_credit = -2
    yrx._kids["weekdays"]._kids["Monday"]._all_member_debt = -2

    assert yrx._descendant_promise_count == -2
    assert yrx._all_member_credit == -2
    assert yrx._all_member_debt == -2
    assert yrx._kids["work"]._descendant_promise_count == -2
    assert yrx._kids["work"]._all_member_credit == -2
    assert yrx._kids["work"]._all_member_debt == -2
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count == -2
    assert yrx._kids["weekdays"]._kids["Monday"]._all_member_credit == -2
    assert yrx._kids["weekdays"]._kids["Monday"]._all_member_debt == -2

    agent_x.set_agent_metrics()

    assert yrx._descendant_promise_count == 2
    assert yrx._kids["work"]._descendant_promise_count == 0
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count == 0

    assert yrx._kids["weekdays"]._kids["Monday"]._all_member_credit == True
    assert yrx._kids["weekdays"]._kids["Monday"]._all_member_debt == True
    assert yrx._kids["work"]._all_member_credit == True
    assert yrx._kids["work"]._all_member_debt == True
    assert yrx._all_member_credit == True
    assert yrx._all_member_debt == True


def test_get_tool_kid_CorrectlyReturnsTool():
    lw_x = example_agents_get_agent_with_4_levels()

    brazil = "src,nation-state,Brazil"
    tool_kid = lw_x.get_tool_kid(road=brazil)
    assert tool_kid != None
    assert tool_kid._desc == "Brazil"

    weekdays = "src,weekdays"
    tool_kid = lw_x.get_tool_kid(road=weekdays)
    assert tool_kid != None
    assert tool_kid._desc == "weekdays"

    # src = "src"
    # with pytest.raises(Exception) as excinfo:
    #     lw_x.get_tool_kid(road=src)
    # assert str(excinfo.value) == f"Cannot return root '{src}'"
    src = "src"
    tool_root = lw_x.get_tool_kid(road=src)
    assert tool_root != None
    assert tool_root._desc == src

    wrong_road = "src,bobdylan"
    with pytest_raises(Exception) as excinfo:
        lw_x.get_tool_kid(road=wrong_road)
    assert (
        str(excinfo.value)
        == f"Getting tool_desc='bobdylan' failed no item at '{wrong_road}'"
    )


def test_set_agent_metrics_RootOnlyCorrectlySetsDescendantAttributes():
    lw_x = AgentUnit(_desc="src")
    assert lw_x._toolroot._descendant_promise_count is None
    assert lw_x._toolroot._all_member_credit is None
    assert lw_x._toolroot._all_member_debt is None

    lw_x.set_agent_metrics()
    assert lw_x._toolroot._descendant_promise_count == 0
    assert lw_x._toolroot._all_member_credit == True
    assert lw_x._toolroot._all_member_debt == True


def test_set_agent_metrics_NLevelCorrectlySetsDescendantAttributes_1():
    lw_x = example_agents_get_agent_with_4_levels()
    x_tool = ToolKid(_desc="email", promise=True)
    lw_x.add_tool(tool_kid=x_tool, walk="src,work")

    # tool "src,weekdays,Sunday"
    # tool "src,weekdays,Monday"
    # tool "src,weekdays,Tuesday"
    # tool "src,weekdays,Wednesday"
    # tool "src,weekdays,Thursday"
    # tool "src,weekdays,Friday"
    # tool "src,weekdays,Saturday"
    # tool "src,weekdays"
    # tool "src,nation-state,USA,Texas"
    # tool "src,nation-state,USA,Oregon"
    # tool "src,nation-state,USA"
    # tool "src,nation-state,France"
    # tool "src,nation-state,Brazil"
    # tool "src,nation-state"
    # tool "work"  # , promise=True)
    # tool "feed cat"  # , promise=True)
    # tool "src"

    # test root init status:
    assert lw_x._toolroot._descendant_promise_count is None
    assert lw_x._toolroot._all_member_credit is None
    assert lw_x._toolroot._all_member_debt is None
    assert lw_x._toolroot._kids["work"]._descendant_promise_count is None
    assert lw_x._toolroot._kids["work"]._all_member_credit is None
    assert lw_x._toolroot._kids["work"]._all_member_debt is None
    assert (
        lw_x._toolroot._kids["weekdays"]._kids["Monday"]._descendant_promise_count
        is None
    )
    assert lw_x._toolroot._kids["weekdays"]._kids["Monday"]._all_member_credit is None
    assert lw_x._toolroot._kids["weekdays"]._kids["Monday"]._all_member_debt is None

    lw_x.set_agent_metrics()
    assert lw_x._toolroot._descendant_promise_count == 3
    assert lw_x._toolroot._kids["work"]._descendant_promise_count == 1
    assert lw_x._toolroot._kids["work"]._kids["email"]._descendant_promise_count == 0
    assert (
        lw_x._toolroot._kids["weekdays"]._kids["Monday"]._descendant_promise_count == 0
    )
    assert lw_x._toolroot._all_member_credit == True
    assert lw_x._toolroot._all_member_debt == True
    assert lw_x._toolroot._kids["work"]._all_member_credit == True
    assert lw_x._toolroot._kids["work"]._all_member_debt == True
    assert lw_x._toolroot._kids["weekdays"]._kids["Monday"]._all_member_credit == True
    assert lw_x._toolroot._kids["weekdays"]._kids["Monday"]._all_member_debt == True


def test_set_agent_metrics_NLevelCorrectlySetsDescendantAttributes_2():
    lw_x = example_agents_get_agent_with_4_levels()
    x1_tool = ToolKid(_desc="email", promise=True)
    lw_x.add_tool(tool_kid=x1_tool, walk="src,work")
    x2_tool = ToolKid(_desc="sweep", promise=True)
    lw_x.add_tool(tool_kid=x2_tool, walk="src,work")

    lw_x.add_memberunit(name="sandy")
    x_grouplink = GroupLink(name="sandy")
    lw_x._toolroot._kids["work"]._kids["email"].set_grouplink(grouplink=x_grouplink)
    # print(lw_x._kids["work"]._kids["email"])
    # print(lw_x._kids["work"]._kids["email"]._grouplink)
    lw_x.set_agent_metrics()
    # print(lw_x._kids["work"]._kids["email"])
    # print(lw_x._kids["work"]._kids["email"]._grouplink)

    assert lw_x._toolroot._all_member_credit == False
    assert lw_x._toolroot._all_member_debt == False
    assert lw_x._toolroot._kids["work"]._all_member_credit == False
    assert lw_x._toolroot._kids["work"]._all_member_debt == False
    assert lw_x._toolroot._kids["work"]._kids["email"]._all_member_credit == False
    assert lw_x._toolroot._kids["work"]._kids["email"]._all_member_debt == False
    assert lw_x._toolroot._kids["work"]._kids["sweep"]._all_member_credit == True
    assert lw_x._toolroot._kids["work"]._kids["sweep"]._all_member_debt == True
    assert lw_x._toolroot._kids["weekdays"]._all_member_credit == True
    assert lw_x._toolroot._kids["weekdays"]._all_member_debt == True
    assert lw_x._toolroot._kids["weekdays"]._kids["Monday"]._all_member_credit == True
    assert lw_x._toolroot._kids["weekdays"]._kids["Monday"]._all_member_debt == True
    assert lw_x._toolroot._kids["weekdays"]._kids["Tuesday"]._all_member_credit == True
    assert lw_x._toolroot._kids["weekdays"]._kids["Tuesday"]._all_member_debt == True


def test_TreeTraverseSetsClearsGrouplineestorsCorrectly():
    # sourcery skip: simplify-empty-collection-comparison
    agent_x = example_agents_get_agent_with_4_levels()
    agent_x.set_agent_metrics()
    # tool tree has no grouplinks
    assert agent_x._toolroot._grouplines == {}
    agent_x._toolroot._grouplines = {1: "testtest"}
    assert agent_x._toolroot._grouplines != {}
    agent_x.set_agent_metrics()
    assert agent_x._toolroot._grouplines == {}

    # test for level 1 and level n
    agent_x._toolroot._kids["work"]._grouplines = {1: "testtest"}
    assert agent_x._toolroot._kids["work"]._grouplines != {}
    agent_x.set_agent_metrics()
    assert agent_x._toolroot._kids["work"]._grouplines == {}


def test_TreeTraverseSetsGrouplineestorFromRootCorrectly():
    # GIVEN
    a_x = example_agents_get_agent_with_4_levels()
    a_x.set_agent_metrics()
    # tool tree has no grouplinks
    assert a_x._toolroot._grouplines == {}
    sandy_text = "sandy"
    sandy_grouplink = GroupLink(name=sandy_text)
    a_x.add_memberunit(name=sandy_text)
    a_x._toolroot.set_grouplink(grouplink=sandy_grouplink)
    # tool tree has grouplines
    assert a_x._toolroot._groupheirs.get(sandy_text) is None

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    assert a_x._toolroot._groupheirs.get(sandy_text) != None
    assert a_x._toolroot._groupheirs.get(sandy_text).name == sandy_text
    assert a_x._toolroot._grouplines != {}
    root_tool = a_x.get_tool_kid(road=f"{a_x._toolroot._desc}")
    sandy_groupline = a_x._toolroot._grouplines.get(sandy_text)
    print(f"{sandy_groupline._agent_credit=} {root_tool._agent_importance=} ")
    print(f"  {sandy_groupline._agent_debt=} {root_tool._agent_importance=} ")
    sum_x = 0
    cat_road = "src,feed cat"
    cat_tool = a_x.get_tool_kid(cat_road)
    week_road = "src,weekdays"
    week_tool = a_x.get_tool_kid(week_road)
    work_road = "src,work"
    work_tool = a_x.get_tool_kid(work_road)
    nation_road = "src,nation-state"
    nation_tool = a_x.get_tool_kid(nation_road)
    sum_x = cat_tool._agent_importance
    print(f"{cat_tool._agent_importance=} {sum_x} ")
    sum_x += week_tool._agent_importance
    print(f"{week_tool._agent_importance=} {sum_x} ")
    sum_x += work_tool._agent_importance
    print(f"{work_tool._agent_importance=} {sum_x} ")
    sum_x += nation_tool._agent_importance
    print(f"{nation_tool._agent_importance=} {sum_x} ")
    assert sum_x >= 1.0
    assert sum_x < 1.00000000001

    # for kid_tool in root_tool._kids.values():
    #     sum_x += kid_tool._agent_importance
    #     print(f"  {kid_tool._agent_importance=} {sum_x=} {kid_tool.get_road()=}")
    assert round(sandy_groupline._agent_credit, 15) == 1
    assert round(sandy_groupline._agent_debt, 15) == 1
    x_groupline = Groupline(
        name=sandy_text,
        _agent_credit=0.9999999999999998,
        _agent_debt=0.9999999999999998,
    )
    assert a_x._toolroot._grouplines == {x_groupline.name: x_groupline}


def test_TreeTraverseSetsGrouplineestorFromNonRootCorrectly():
    lw_x = example_agents_get_agent_with_4_levels()
    lw_x.set_agent_metrics()
    # tool tree has no grouplinks
    assert lw_x._toolroot._grouplines == {}
    lw_x.add_memberunit(name="sandy")
    x_grouplink = GroupLink(name="sandy")
    lw_x._toolroot._kids["work"].set_grouplink(grouplink=x_grouplink)

    # tool tree has grouplinks
    lw_x.set_agent_metrics()
    assert lw_x._toolroot._grouplines != {}
    x_groupline = Groupline(
        name="sandy", _agent_credit=0.23076923076923078, _agent_debt=0.23076923076923078
    )
    assert lw_x._toolroot._grouplines == {x_groupline.name: x_groupline}
    assert lw_x._toolroot._kids["work"]._grouplines != {}
    assert lw_x._toolroot._kids["work"]._grouplines == {x_groupline.name: x_groupline}


def test_agent4member_Exists():
    agent_x = example_agents_get_agent_with_4_levels()
    x1_tool = ToolKid(_desc="email", promise=True)
    agent_x.add_tool(tool_kid=x1_tool, walk="src,work")
    x2_tool = ToolKid(_desc="sweep", promise=True)
    agent_x.add_tool(tool_kid=x2_tool, walk="src,work")

    sandy_name = MemberName("sandy")
    agent_x.add_memberunit(name=sandy_name)
    x_grouplink = GroupLink(name=sandy_name)
    yrx = agent_x._toolroot
    yrx._kids["work"]._kids["email"].set_grouplink(grouplink=x_grouplink)
    sandy_agent4member = agent_x.get_agent4member(
        acptfacts=None, member_name=sandy_name
    )
    assert sandy_agent4member
    assert str(type(sandy_agent4member)).find(".agent.AgentUnit'>")
    assert sandy_agent4member._desc == sandy_name


def test_agent4member_hasCorrectLevel1StructureNoGrouplessBranches():
    agent_x = example_agents_get_agent_with_4_levels()
    x1_tool = ToolKid(_desc="email", promise=True)
    agent_x.add_tool(tool_kid=x1_tool, walk="src,work")
    x2_tool = ToolKid(_desc="sweep", promise=True)
    agent_x.add_tool(tool_kid=x2_tool, walk="src,work")

    billy_name = MemberName("billy")
    agent_x.add_memberunit(name=billy_name)
    billy_bl = GroupLink(name=billy_name)
    yrx = agent_x._toolroot
    yrx._kids["weekdays"].set_grouplink(grouplink=billy_bl)
    yrx._kids["feed cat"].set_grouplink(grouplink=billy_bl)
    yrx._kids["nation-state"].set_grouplink(grouplink=billy_bl)

    sandy_name = MemberName("sandy")
    agent_x.add_memberunit(name=sandy_name)
    sandy_bl = GroupLink(name=sandy_name)
    yrx._kids["work"]._kids["email"].set_grouplink(grouplink=sandy_bl)

    sandy_agent4member = agent_x.get_agent4member(
        acptfacts=None, member_name=sandy_name
    )
    assert len(sandy_agent4member._toolroot._kids) > 0
    print(f"{len(sandy_agent4member._toolroot._kids)=}")
    assert (
        str(type(sandy_agent4member._toolroot._kids.get("work"))).find(
            ".tool.ToolKid'>"
        )
        > 0
    )
    assert sandy_agent4member._toolroot._kids.get("feed cat") is None
    assert sandy_agent4member._toolroot._agent_importance == 1
    y4a_work = sandy_agent4member._toolroot._kids.get("work")
    assert y4a_work._agent_importance == yrx._kids["work"]._agent_importance
    assert sandy_agent4member._toolroot._kids.get("__other__") != None
    y4a_others = sandy_agent4member._toolroot._kids.get("__other__")
    others_agent_importance = yrx._kids["weekdays"]._agent_importance
    others_agent_importance += yrx._kids["feed cat"]._agent_importance
    others_agent_importance += yrx._kids["nation-state"]._agent_importance
    print(f"{others_agent_importance=}")
    assert round(y4a_others._agent_importance, 15) == round(others_agent_importance, 15)


def test_agent_get_orderd_node_list_WorksCorrectly():
    lw_x = example_agents_get_agent_with_4_levels()
    assert lw_x.get_tool_tree_ordered_road_list()
    ordered_node_list = lw_x.get_tool_tree_ordered_road_list()
    # for node in ordered_node_list:
    #     print(f"{node}")
    assert len(ordered_node_list) == 17
    assert lw_x.get_tool_tree_ordered_road_list()[0] == "src"
    assert lw_x.get_tool_tree_ordered_road_list()[8] == "src,weekdays"

    lw_y = AgentUnit(_desc="MyAgent")
    assert lw_y.get_tool_tree_ordered_road_list()[0] == "MyAgent"


def test_agent_get_orderd_node_list_CorrectlyFiltersRangedToolRoads():
    src = "src"
    agent_x = AgentUnit(_desc=src)
    time = "timeline"
    agent_x.add_tool(ToolKid(_desc=time, _begin=0, _close=700), walk=src)
    t_road = f"{src},{time}"
    week = "weeks"
    agent_x.add_tool(ToolKid(_desc=week, _denom=7), walk=t_road)

    assert len(agent_x.get_tool_tree_ordered_road_list()) == 3
    assert len(agent_x.get_tool_tree_ordered_road_list(no_range_descendents=True)) == 2


def test_agent_get_heir_road_list_returnsCorrectList():
    lw_x = example_agents_get_agent_with_4_levels()
    weekdays = "src,weekdays"
    assert lw_x.get_heir_road_list(src_road=weekdays)
    heir_node_road_list = lw_x.get_heir_road_list(src_road=weekdays)
    # for node in heir_node_road_list:
    #     print(f"{node}")
    assert len(heir_node_road_list) == 8
    assert heir_node_road_list[0] == weekdays
    assert heir_node_road_list[3] == f"{weekdays},Saturday"
    assert heir_node_road_list[4] == f"{weekdays},Sunday"


# def test_agent4member_hasCorrectLevel1StructureWithGrouplessBranches_2():
#     lw_desc = "src"
#     lw_x = AgentUnit(_desc=lw_desc)
#     lw_x.add_tool(tool_kid=ToolKid(_desc="A", _weight=7), walk="src")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="C", _weight=3), walk="src,A")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="E", _weight=7), walk="src,A,C")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="D", _weight=7), walk="src,A,C")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="B", _weight=13), walk="src")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="F", _weight=23), walk="src")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="G", _weight=57), walk="src")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="I"), walk="src,G")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="H"), walk="src,G")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="J"), walk="src,G,I")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="K"), walk="src,G,I")
#     lw_x.add_tool(tool_kid=ToolKid(_desc="M"), walk="src,G,H")

#     billy_name = MemberName("billy")
#     lw_x.add_memberunit(name=billy_name)
#     billy_bl = GroupLink(name=billy_name)
#     lw_x.edit_tool_attr(road="src,G", grouplink=billy_bl)
#     lw_x.edit_tool_attr(road="src,G,H,M", grouplink=billy_bl)

#     sandy_name = MemberName("sandy")
#     lw_x.add_memberunit(name=sandy_name)
#     sandy_bl = GroupLink(name=sandy_name)
#     lw_x.edit_tool_attr(road="src,A", grouplink=sandy_bl)
#     lw_x.edit_tool_attr(road="src,B", grouplink=sandy_bl)
#     lw_x.edit_tool_attr(road="src,A,C,E", grouplink=sandy_bl)

#     # expected sandy
#     exp_sandy = AgentUnit(_desc=lw_desc)
#     exp_sandy.add_tool(tool_kid=ToolKid(_desc="A", _agent_importance=0.07), walk="src")
#     exp_sandy.add_tool(tool_kid=ToolKid(_desc="C", _agent_importance=0.07), walk="src,A")
#     exp_sandy.add_tool(tool_kid=ToolKid(_desc="E", _agent_importance=0.5), walk="src,A,C")
#     exp_sandy.add_tool(tool_kid=ToolKid(_desc="B", _agent_importance=0.13), walk="src")

#     # generated sandy
#     gen_sandy = lw_x.get_agent4member(acptfacts=None, member_name=sandy_name)

#     # confirm generated sandy is correct
#     assert gen_sandy.get_tool_kid(road="src,A")._agent_importance == 0.07
#     assert gen_sandy.get_tool_kid(road="src,A,C")._agent_importance == 0.07
#     assert gen_sandy.get_tool_kid(road="src,A,C,E")._agent_importance == 0.5
#     assert gen_sandy.get_tool_kid(road="src,B")._agent_importance == 0.13
#     assert (
#         gen_sandy.get_tool_kid(road="src,A")._agent_importance
#         == exp_sandy.get_tool_kid(road="src,A")._agent_importance
#     )
#     assert (
#         gen_sandy.get_tool_kid(road="src,A,C")._agent_importance
#         == exp_sandy.get_tool_kid(road="src,A,C")._agent_importance
#     )
#     assert (
#         gen_sandy.get_tool_kid(road="src,A,C,E")._agent_importance
#         == exp_sandy.get_tool_kid(road="src,A,C,E")._agent_importance
#     )
#     assert (
#         gen_sandy.get_tool_kid(road="src,B")._agent_importance
#         == exp_sandy.get_tool_kid(road="src,B")._agent_importance
#     )
#     gen_sandy_list = gen_sandy.get_tool_list()
#     assert len(gen_sandy_list) == 5
