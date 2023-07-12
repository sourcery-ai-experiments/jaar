from lib.agent.test_agent.example_agents import (
    get_agent_with_4_levels as example_agents_get_agent_with_4_levels,
)
from lib.agent.ally import AllyName
from lib.agent.idea import IdeaKid
from lib.agent.agent import AgentUnit
from lib.agent.brand import Brandline, BrandLink
from pytest import raises as pytest_raises


def test_set_agent_metrics_CorrectlyClearsDescendantAttributes():
    agent_x = example_agents_get_agent_with_4_levels()

    # idea "src,weekdays,Sunday"
    # idea "src,weekdays,Monday"
    # idea "src,weekdays,Tuesday"
    # idea "src,weekdays,Wednesday"
    # idea "src,weekdays,Thursday"
    # idea "src,weekdays,Friday"
    # idea "src,weekdays,Saturday"
    # idea "src,weekdays"
    # idea "src,nation-state,USA,Texas"
    # idea "src,nation-state,USA,Oregon"
    # idea "src,nation-state,USA"
    # idea "src,nation-state,France"
    # idea "src,nation-state,Brazil"
    # idea "src,nation-state"
    # idea "work"  # , promise=True)
    # idea "feed cat"  # , promise=True)
    # idea "src"

    # test root init status:
    yrx = agent_x._idearoot
    assert yrx._descendant_promise_count is None
    assert yrx._all_ally_credit is None
    assert yrx._all_ally_debt is None
    assert yrx._kids["work"]._descendant_promise_count is None
    assert yrx._kids["work"]._all_ally_credit is None
    assert yrx._kids["work"]._all_ally_debt is None
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count is None
    assert yrx._kids["weekdays"]._kids["Monday"]._all_ally_credit is None
    assert yrx._kids["weekdays"]._kids["Monday"]._all_ally_debt is None

    yrx._descendant_promise_count = -2
    yrx._all_ally_credit = -2
    yrx._all_ally_debt = -2
    yrx._kids["work"]._descendant_promise_count = -2
    yrx._kids["work"]._all_ally_credit = -2
    yrx._kids["work"]._all_ally_debt = -2
    yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count = -2
    yrx._kids["weekdays"]._kids["Monday"]._all_ally_credit = -2
    yrx._kids["weekdays"]._kids["Monday"]._all_ally_debt = -2

    assert yrx._descendant_promise_count == -2
    assert yrx._all_ally_credit == -2
    assert yrx._all_ally_debt == -2
    assert yrx._kids["work"]._descendant_promise_count == -2
    assert yrx._kids["work"]._all_ally_credit == -2
    assert yrx._kids["work"]._all_ally_debt == -2
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count == -2
    assert yrx._kids["weekdays"]._kids["Monday"]._all_ally_credit == -2
    assert yrx._kids["weekdays"]._kids["Monday"]._all_ally_debt == -2

    agent_x.set_agent_metrics()

    assert yrx._descendant_promise_count == 2
    assert yrx._kids["work"]._descendant_promise_count == 0
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count == 0

    assert yrx._kids["weekdays"]._kids["Monday"]._all_ally_credit == True
    assert yrx._kids["weekdays"]._kids["Monday"]._all_ally_debt == True
    assert yrx._kids["work"]._all_ally_credit == True
    assert yrx._kids["work"]._all_ally_debt == True
    assert yrx._all_ally_credit == True
    assert yrx._all_ally_debt == True


def test_get_idea_kid_CorrectlyReturnsIdea():
    lw_x = example_agents_get_agent_with_4_levels()

    brazil = "src,nation-state,Brazil"
    idea_kid = lw_x.get_idea_kid(road=brazil)
    assert idea_kid != None
    assert idea_kid._desc == "Brazil"

    weekdays = "src,weekdays"
    idea_kid = lw_x.get_idea_kid(road=weekdays)
    assert idea_kid != None
    assert idea_kid._desc == "weekdays"

    # src = "src"
    # with pytest.raises(Exception) as excinfo:
    #     lw_x.get_idea_kid(road=src)
    # assert str(excinfo.value) == f"Cannot return root '{src}'"
    src = "src"
    idea_root = lw_x.get_idea_kid(road=src)
    assert idea_root != None
    assert idea_root._desc == src

    wrong_road = "src,bobdylan"
    with pytest_raises(Exception) as excinfo:
        lw_x.get_idea_kid(road=wrong_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_desc='bobdylan' failed no item at '{wrong_road}'"
    )


def test_set_agent_metrics_RootOnlyCorrectlySetsDescendantAttributes():
    lw_x = AgentUnit(_desc="src")
    assert lw_x._idearoot._descendant_promise_count is None
    assert lw_x._idearoot._all_ally_credit is None
    assert lw_x._idearoot._all_ally_debt is None

    lw_x.set_agent_metrics()
    assert lw_x._idearoot._descendant_promise_count == 0
    assert lw_x._idearoot._all_ally_credit == True
    assert lw_x._idearoot._all_ally_debt == True


def test_set_agent_metrics_NLevelCorrectlySetsDescendantAttributes_1():
    lw_x = example_agents_get_agent_with_4_levels()
    x_idea = IdeaKid(_desc="email", promise=True)
    lw_x.add_idea(idea_kid=x_idea, walk="src,work")

    # idea "src,weekdays,Sunday"
    # idea "src,weekdays,Monday"
    # idea "src,weekdays,Tuesday"
    # idea "src,weekdays,Wednesday"
    # idea "src,weekdays,Thursday"
    # idea "src,weekdays,Friday"
    # idea "src,weekdays,Saturday"
    # idea "src,weekdays"
    # idea "src,nation-state,USA,Texas"
    # idea "src,nation-state,USA,Oregon"
    # idea "src,nation-state,USA"
    # idea "src,nation-state,France"
    # idea "src,nation-state,Brazil"
    # idea "src,nation-state"
    # idea "work"  # , promise=True)
    # idea "feed cat"  # , promise=True)
    # idea "src"

    # test root init status:
    assert lw_x._idearoot._descendant_promise_count is None
    assert lw_x._idearoot._all_ally_credit is None
    assert lw_x._idearoot._all_ally_debt is None
    assert lw_x._idearoot._kids["work"]._descendant_promise_count is None
    assert lw_x._idearoot._kids["work"]._all_ally_credit is None
    assert lw_x._idearoot._kids["work"]._all_ally_debt is None
    assert (
        lw_x._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count
        is None
    )
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_ally_credit is None
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_ally_debt is None

    lw_x.set_agent_metrics()
    assert lw_x._idearoot._descendant_promise_count == 3
    assert lw_x._idearoot._kids["work"]._descendant_promise_count == 1
    assert lw_x._idearoot._kids["work"]._kids["email"]._descendant_promise_count == 0
    assert (
        lw_x._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count == 0
    )
    assert lw_x._idearoot._all_ally_credit == True
    assert lw_x._idearoot._all_ally_debt == True
    assert lw_x._idearoot._kids["work"]._all_ally_credit == True
    assert lw_x._idearoot._kids["work"]._all_ally_debt == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_ally_credit == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_ally_debt == True


def test_set_agent_metrics_NLevelCorrectlySetsDescendantAttributes_2():
    lw_x = example_agents_get_agent_with_4_levels()
    x1_idea = IdeaKid(_desc="email", promise=True)
    lw_x.add_idea(idea_kid=x1_idea, walk="src,work")
    x2_idea = IdeaKid(_desc="sweep", promise=True)
    lw_x.add_idea(idea_kid=x2_idea, walk="src,work")

    lw_x.add_allyunit(name="sandy")
    x_brandlink = BrandLink(name="sandy")
    lw_x._idearoot._kids["work"]._kids["email"].set_brandlink(brandlink=x_brandlink)
    # print(lw_x._kids["work"]._kids["email"])
    # print(lw_x._kids["work"]._kids["email"]._brandlink)
    lw_x.set_agent_metrics()
    # print(lw_x._kids["work"]._kids["email"])
    # print(lw_x._kids["work"]._kids["email"]._brandlink)

    assert lw_x._idearoot._all_ally_credit == False
    assert lw_x._idearoot._all_ally_debt == False
    assert lw_x._idearoot._kids["work"]._all_ally_credit == False
    assert lw_x._idearoot._kids["work"]._all_ally_debt == False
    assert lw_x._idearoot._kids["work"]._kids["email"]._all_ally_credit == False
    assert lw_x._idearoot._kids["work"]._kids["email"]._all_ally_debt == False
    assert lw_x._idearoot._kids["work"]._kids["sweep"]._all_ally_credit == True
    assert lw_x._idearoot._kids["work"]._kids["sweep"]._all_ally_debt == True
    assert lw_x._idearoot._kids["weekdays"]._all_ally_credit == True
    assert lw_x._idearoot._kids["weekdays"]._all_ally_debt == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_ally_credit == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_ally_debt == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Tuesday"]._all_ally_credit == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Tuesday"]._all_ally_debt == True


def test_TreeTraverseSetsClearsBrandlineestorsCorrectly():
    # sourcery skip: simplify-empty-collection-comparison
    agent_x = example_agents_get_agent_with_4_levels()
    agent_x.set_agent_metrics()
    # idea tree has no brandlinks
    assert agent_x._idearoot._brandlines == {}
    agent_x._idearoot._brandlines = {1: "testtest"}
    assert agent_x._idearoot._brandlines != {}
    agent_x.set_agent_metrics()
    assert agent_x._idearoot._brandlines == {}

    # test for level 1 and level n
    agent_x._idearoot._kids["work"]._brandlines = {1: "testtest"}
    assert agent_x._idearoot._kids["work"]._brandlines != {}
    agent_x.set_agent_metrics()
    assert agent_x._idearoot._kids["work"]._brandlines == {}


def test_TreeTraverseSetsBrandlineestorFromRootCorrectly():
    # GIVEN
    a_x = example_agents_get_agent_with_4_levels()
    a_x.set_agent_metrics()
    # idea tree has no brandlinks
    assert a_x._idearoot._brandlines == {}
    sandy_text = "sandy"
    sandy_brandlink = BrandLink(name=sandy_text)
    a_x.add_allyunit(name=sandy_text)
    a_x._idearoot.set_brandlink(brandlink=sandy_brandlink)
    # idea tree has brandlines
    assert a_x._idearoot._brandheirs.get(sandy_text) is None

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    assert a_x._idearoot._brandheirs.get(sandy_text) != None
    assert a_x._idearoot._brandheirs.get(sandy_text).name == sandy_text
    assert a_x._idearoot._brandlines != {}
    root_idea = a_x.get_idea_kid(road=f"{a_x._idearoot._desc}")
    sandy_brandline = a_x._idearoot._brandlines.get(sandy_text)
    print(f"{sandy_brandline._agent_credit=} {root_idea._agent_importance=} ")
    print(f"  {sandy_brandline._agent_debt=} {root_idea._agent_importance=} ")
    sum_x = 0
    for kid_idea in root_idea._kids.values():
        sum_x += kid_idea._agent_importance
        print(f"  {kid_idea._agent_importance=} {sum_x=} {kid_idea._desc=}")
    assert round(sandy_brandline._agent_credit, 15) == 1
    assert round(sandy_brandline._agent_debt, 15) == 1
    x_brandline = Brandline(
        name=sandy_text,
        _agent_credit=0.9999999999999998,
        _agent_debt=0.9999999999999998,
    )
    assert a_x._idearoot._brandlines == {x_brandline.name: x_brandline}


def test_TreeTraverseSetsBrandlineestorFromNonRootCorrectly():
    lw_x = example_agents_get_agent_with_4_levels()
    lw_x.set_agent_metrics()
    # idea tree has no brandlinks
    assert lw_x._idearoot._brandlines == {}
    lw_x.add_allyunit(name="sandy")
    x_brandlink = BrandLink(name="sandy")
    lw_x._idearoot._kids["work"].set_brandlink(brandlink=x_brandlink)

    # idea tree has brandlinks
    lw_x.set_agent_metrics()
    assert lw_x._idearoot._brandlines != {}
    x_brandline = Brandline(
        name="sandy", _agent_credit=0.23076923076923078, _agent_debt=0.23076923076923078
    )
    assert lw_x._idearoot._brandlines == {x_brandline.name: x_brandline}
    assert lw_x._idearoot._kids["work"]._brandlines != {}
    assert lw_x._idearoot._kids["work"]._brandlines == {x_brandline.name: x_brandline}


def test_agent4ally_Exists():
    agent_x = example_agents_get_agent_with_4_levels()
    x1_idea = IdeaKid(_desc="email", promise=True)
    agent_x.add_idea(idea_kid=x1_idea, walk="src,work")
    x2_idea = IdeaKid(_desc="sweep", promise=True)
    agent_x.add_idea(idea_kid=x2_idea, walk="src,work")

    sandy_name = AllyName("sandy")
    agent_x.add_allyunit(name=sandy_name)
    x_brandlink = BrandLink(name=sandy_name)
    yrx = agent_x._idearoot
    yrx._kids["work"]._kids["email"].set_brandlink(brandlink=x_brandlink)
    sandy_agent4ally = agent_x.get_agent4ally(acptfacts=None, ally_name=sandy_name)
    assert sandy_agent4ally
    assert str(type(sandy_agent4ally)).find(".agent.AgentUnit'>")
    assert sandy_agent4ally._desc == sandy_name


def test_agent4ally_hasCorrectLevel1StructureNoBrandlessBranches():
    agent_x = example_agents_get_agent_with_4_levels()
    x1_idea = IdeaKid(_desc="email", promise=True)
    agent_x.add_idea(idea_kid=x1_idea, walk="src,work")
    x2_idea = IdeaKid(_desc="sweep", promise=True)
    agent_x.add_idea(idea_kid=x2_idea, walk="src,work")

    billy_name = AllyName("billy")
    agent_x.add_allyunit(name=billy_name)
    billy_bl = BrandLink(name=billy_name)
    yrx = agent_x._idearoot
    yrx._kids["weekdays"].set_brandlink(brandlink=billy_bl)
    yrx._kids["feed cat"].set_brandlink(brandlink=billy_bl)
    yrx._kids["nation-state"].set_brandlink(brandlink=billy_bl)

    sandy_name = AllyName("sandy")
    agent_x.add_allyunit(name=sandy_name)
    sandy_bl = BrandLink(name=sandy_name)
    yrx._kids["work"]._kids["email"].set_brandlink(brandlink=sandy_bl)

    sandy_agent4ally = agent_x.get_agent4ally(acptfacts=None, ally_name=sandy_name)
    assert len(sandy_agent4ally._idearoot._kids) > 0
    print(f"{len(sandy_agent4ally._idearoot._kids)=}")
    assert (
        str(type(sandy_agent4ally._idearoot._kids.get("work"))).find(".idea.IdeaKid'>")
        > 0
    )
    assert sandy_agent4ally._idearoot._kids.get("feed cat") is None
    assert sandy_agent4ally._idearoot._agent_importance == 1
    y4a_work = sandy_agent4ally._idearoot._kids.get("work")
    assert y4a_work._agent_importance == yrx._kids["work"]._agent_importance
    assert sandy_agent4ally._idearoot._kids.get("__other__") != None
    y4a_others = sandy_agent4ally._idearoot._kids.get("__other__")
    others_agent_importance = yrx._kids["weekdays"]._agent_importance
    others_agent_importance += yrx._kids["feed cat"]._agent_importance
    others_agent_importance += yrx._kids["nation-state"]._agent_importance
    print(f"{others_agent_importance=}")
    assert round(y4a_others._agent_importance, 15) == round(others_agent_importance, 15)


def test_agent_get_orderd_node_list_WorksCorrectly():
    lw_x = example_agents_get_agent_with_4_levels()
    assert lw_x.get_idea_tree_ordered_road_list()
    ordered_node_list = lw_x.get_idea_tree_ordered_road_list()
    for node in ordered_node_list:
        print(f"{node}")
    assert len(ordered_node_list) == 17
    assert lw_x.get_idea_tree_ordered_road_list()[0] == "src"
    assert lw_x.get_idea_tree_ordered_road_list()[8] == "src,weekdays"

    lw_y = AgentUnit(_desc="MyAgent")
    assert lw_y.get_idea_tree_ordered_road_list()[0] == "MyAgent"


def test_agent_get_orderd_node_list_CorrectlyFiltersRangedIdeaRoads():
    src = "src"
    agent_x = AgentUnit(_desc=src)
    time = "timeline"
    agent_x.add_idea(IdeaKid(_desc=time, _begin=0, _close=700), walk=src)
    t_road = f"{src},{time}"
    week = "weeks"
    agent_x.add_idea(IdeaKid(_desc=week, _denom=7), walk=t_road)

    assert len(agent_x.get_idea_tree_ordered_road_list()) == 3
    assert len(agent_x.get_idea_tree_ordered_road_list(no_range_descendents=True)) == 2


def test_agent_get_heir_road_list_returnsCorrectList():
    lw_x = example_agents_get_agent_with_4_levels()
    weekdays = "src,weekdays"
    assert lw_x.get_heir_road_list(src_road=weekdays)
    heir_node_road_list = lw_x.get_heir_road_list(src_road=weekdays)
    for node in heir_node_road_list:
        print(f"{node}")
    assert len(heir_node_road_list) == 8
    assert heir_node_road_list[0] == weekdays
    assert heir_node_road_list[3] == f"{weekdays},Saturday"
    assert heir_node_road_list[4] == f"{weekdays},Sunday"


# def test_agent4ally_hasCorrectLevel1StructureWithBrandlessBranches_2():
#     lw_desc = "src"
#     lw_x = AgentUnit(_desc=lw_desc)
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="A", _weight=7), walk="src")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="C", _weight=3), walk="src,A")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="E", _weight=7), walk="src,A,C")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="D", _weight=7), walk="src,A,C")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="B", _weight=13), walk="src")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="F", _weight=23), walk="src")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="G", _weight=57), walk="src")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="I"), walk="src,G")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="H"), walk="src,G")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="J"), walk="src,G,I")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="K"), walk="src,G,I")
#     lw_x.add_idea(idea_kid=IdeaKid(_desc="M"), walk="src,G,H")

#     billy_name = AllyName("billy")
#     lw_x.add_allyunit(name=billy_name)
#     billy_bl = BrandLink(name=billy_name)
#     lw_x.edit_idea_attr(road="src,G", brandlink=billy_bl)
#     lw_x.edit_idea_attr(road="src,G,H,M", brandlink=billy_bl)

#     sandy_name = AllyName("sandy")
#     lw_x.add_allyunit(name=sandy_name)
#     sandy_bl = BrandLink(name=sandy_name)
#     lw_x.edit_idea_attr(road="src,A", brandlink=sandy_bl)
#     lw_x.edit_idea_attr(road="src,B", brandlink=sandy_bl)
#     lw_x.edit_idea_attr(road="src,A,C,E", brandlink=sandy_bl)

#     # expected sandy
#     exp_sandy = AgentUnit(_desc=lw_desc)
#     exp_sandy.add_idea(idea_kid=IdeaKid(_desc="A", _agent_importance=0.07), walk="src")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_desc="C", _agent_importance=0.07), walk="src,A")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_desc="E", _agent_importance=0.5), walk="src,A,C")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_desc="B", _agent_importance=0.13), walk="src")

#     # generated sandy
#     gen_sandy = lw_x.get_agent4ally(acptfacts=None, ally_name=sandy_name)

#     # confirm generated sandy is correct
#     assert gen_sandy.get_idea_kid(road="src,A")._agent_importance == 0.07
#     assert gen_sandy.get_idea_kid(road="src,A,C")._agent_importance == 0.07
#     assert gen_sandy.get_idea_kid(road="src,A,C,E")._agent_importance == 0.5
#     assert gen_sandy.get_idea_kid(road="src,B")._agent_importance == 0.13
#     assert (
#         gen_sandy.get_idea_kid(road="src,A")._agent_importance
#         == exp_sandy.get_idea_kid(road="src,A")._agent_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road="src,A,C")._agent_importance
#         == exp_sandy.get_idea_kid(road="src,A,C")._agent_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road="src,A,C,E")._agent_importance
#         == exp_sandy.get_idea_kid(road="src,A,C,E")._agent_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road="src,B")._agent_importance
#         == exp_sandy.get_idea_kid(road="src,B")._agent_importance
#     )
#     gen_sandy_list = gen_sandy.get_idea_list()
#     assert len(gen_sandy_list) == 5

#     assert 1 == 2
