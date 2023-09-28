from src.contract.examples.example_contracts import (
    get_contract_with_4_levels as example_contracts_get_contract_with_4_levels,
)
from src.contract.member import MemberName
from src.contract.idea import IdeaKid
from src.contract.contract import ContractUnit
from src.contract.group import Groupline, GroupLink
from pytest import raises as pytest_raises


def test_set_contract_metrics_CorrectlyClearsDescendantAttributes():
    cx = example_contracts_get_contract_with_4_levels()

    # idea ",weekdays,Sunday"
    # idea ",weekdays,Monday"
    # idea ",weekdays,Tuesday"
    # idea ",weekdays,Wednesday"
    # idea ",weekdays,Thursday"
    # idea ",weekdays,Friday"
    # idea ",weekdays,Saturday"
    # idea ",weekdays"
    # idea ",nation-state,USA,Texas"
    # idea ",nation-state,USA,Oregon"
    # idea ",nation-state,USA"
    # idea ",nation-state,France"
    # idea ",nation-state,Brazil"
    # idea ",nation-state"
    # idea "work"  # , promise=True)
    # idea "feed cat"  # , promise=True)

    # test root init status:
    yrx = cx._idearoot
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

    cx.set_contract_metrics()

    assert yrx._descendant_promise_count == 2
    assert yrx._kids["work"]._descendant_promise_count == 0
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count == 0

    assert yrx._kids["weekdays"]._kids["Monday"]._all_member_credit == True
    assert yrx._kids["weekdays"]._kids["Monday"]._all_member_debt == True
    assert yrx._kids["work"]._all_member_credit == True
    assert yrx._kids["work"]._all_member_debt == True
    assert yrx._all_member_credit == True
    assert yrx._all_member_debt == True


def test_get_idea_kid_CorrectlyReturnsIdea():
    cx = example_contracts_get_contract_with_4_levels()

    brazil = f"{cx._economy_title},nation-state,Brazil"
    idea_kid = cx.get_idea_kid(road=brazil)
    assert idea_kid != None
    assert idea_kid._label == "Brazil"

    weekdays = f"{cx._economy_title},weekdays"
    idea_kid = cx.get_idea_kid(road=weekdays)
    assert idea_kid != None
    assert idea_kid._label == "weekdays"

    # with pytest.raises(Exception) as excinfo:
    #     cx.get_idea_kid(road=cx._economy_title)
    # assert str(excinfo.value) == f"Cannot return root '{cx._economy_title}'"
    idea_root = cx.get_idea_kid(road=cx._economy_title)
    assert idea_root != None
    assert idea_root._label == cx._economy_title

    wrong_road = f"{cx._economy_title},bobdylan"
    with pytest_raises(Exception) as excinfo:
        cx.get_idea_kid(road=wrong_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='bobdylan' failed no item at '{wrong_road}'"
    )


def test_set_contract_metrics_RootOnlyCorrectlySetsDescendantAttributes():
    owner_text = "Tim"
    cx = ContractUnit(_owner=owner_text)
    assert cx._idearoot._descendant_promise_count is None
    assert cx._idearoot._all_member_credit is None
    assert cx._idearoot._all_member_debt is None

    cx.set_contract_metrics()
    assert cx._idearoot._descendant_promise_count == 0
    assert cx._idearoot._all_member_credit == True
    assert cx._idearoot._all_member_debt == True


def test_set_contract_metrics_NLevelCorrectlySetsDescendantAttributes_1():
    cx = example_contracts_get_contract_with_4_levels()
    x_idea = IdeaKid(_label="email", promise=True)
    cx.add_idea(idea_kid=x_idea, walk=f"{cx._economy_title},work")

    # idea ",weekdays,Sunday"
    # idea ",weekdays,Monday"
    # idea ",weekdays,Tuesday"
    # idea ",weekdays,Wednesday"
    # idea ",weekdays,Thursday"
    # idea ",weekdays,Friday"
    # idea ",weekdays,Saturday"
    # idea ",weekdays"
    # idea ",nation-state,USA,Texas"
    # idea ",nation-state,USA,Oregon"
    # idea ",nation-state,USA"
    # idea ",nation-state,France"
    # idea ",nation-state,Brazil"
    # idea ",nation-state"
    # idea "work"  # , promise=True)
    # idea "feed cat"  # , promise=True)
    # idea "

    # test root init status:
    assert cx._idearoot._descendant_promise_count is None
    assert cx._idearoot._all_member_credit is None
    assert cx._idearoot._all_member_debt is None
    assert cx._idearoot._kids["work"]._descendant_promise_count is None
    assert cx._idearoot._kids["work"]._all_member_credit is None
    assert cx._idearoot._kids["work"]._all_member_debt is None
    assert (
        cx._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count is None
    )
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_member_credit is None
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_member_debt is None

    cx.set_contract_metrics()
    assert cx._idearoot._descendant_promise_count == 3
    assert cx._idearoot._kids["work"]._descendant_promise_count == 1
    assert cx._idearoot._kids["work"]._kids["email"]._descendant_promise_count == 0
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count == 0
    assert cx._idearoot._all_member_credit == True
    assert cx._idearoot._all_member_debt == True
    assert cx._idearoot._kids["work"]._all_member_credit == True
    assert cx._idearoot._kids["work"]._all_member_debt == True
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_member_credit == True
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_member_debt == True


def test_set_contract_metrics_NLevelCorrectlySetsDescendantAttributes_2():
    cx = example_contracts_get_contract_with_4_levels()
    x1_idea = IdeaKid(_label="email", promise=True)
    cx.add_idea(idea_kid=x1_idea, walk=f"{cx._economy_title},work")
    x2_idea = IdeaKid(_label="sweep", promise=True)
    cx.add_idea(idea_kid=x2_idea, walk=f"{cx._economy_title},work")

    cx.add_memberunit(name="sandy")
    x_grouplink = GroupLink(name="sandy")
    cx._idearoot._kids["work"]._kids["email"].set_grouplink(grouplink=x_grouplink)
    # print(cx._kids["work"]._kids["email"])
    # print(cx._kids["work"]._kids["email"]._grouplink)
    cx.set_contract_metrics()
    # print(cx._kids["work"]._kids["email"])
    # print(cx._kids["work"]._kids["email"]._grouplink)

    assert cx._idearoot._all_member_credit == False
    assert cx._idearoot._all_member_debt == False
    assert cx._idearoot._kids["work"]._all_member_credit == False
    assert cx._idearoot._kids["work"]._all_member_debt == False
    assert cx._idearoot._kids["work"]._kids["email"]._all_member_credit == False
    assert cx._idearoot._kids["work"]._kids["email"]._all_member_debt == False
    assert cx._idearoot._kids["work"]._kids["sweep"]._all_member_credit == True
    assert cx._idearoot._kids["work"]._kids["sweep"]._all_member_debt == True
    assert cx._idearoot._kids["weekdays"]._all_member_credit == True
    assert cx._idearoot._kids["weekdays"]._all_member_debt == True
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_member_credit == True
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_member_debt == True
    assert cx._idearoot._kids["weekdays"]._kids["Tuesday"]._all_member_credit == True
    assert cx._idearoot._kids["weekdays"]._kids["Tuesday"]._all_member_debt == True


def test_TreeTraverseSetsClearsGrouplineestorsCorrectly():
    # sourcery skip: simplify-empty-collection-comparison
    cx = example_contracts_get_contract_with_4_levels()
    cx.set_contract_metrics()
    # idea tree has no grouplinks
    assert cx._idearoot._grouplines == {}
    cx._idearoot._grouplines = {1: "testtest"}
    assert cx._idearoot._grouplines != {}
    cx.set_contract_metrics()
    assert cx._idearoot._grouplines == {}

    # test for level 1 and level n
    cx._idearoot._kids["work"]._grouplines = {1: "testtest"}
    assert cx._idearoot._kids["work"]._grouplines != {}
    cx.set_contract_metrics()
    assert cx._idearoot._kids["work"]._grouplines == {}


def test_TreeTraverseSetsGrouplineestorFromRootCorrectly():
    # GIVEN
    cx = example_contracts_get_contract_with_4_levels()
    cx.set_contract_metrics()
    # idea tree has no grouplinks
    assert cx._idearoot._grouplines == {}
    sandy_text = "sandy"
    sandy_grouplink = GroupLink(name=sandy_text)
    cx.add_memberunit(name=sandy_text)
    cx._idearoot.set_grouplink(grouplink=sandy_grouplink)
    # idea tree has grouplines
    assert cx._idearoot._groupheirs.get(sandy_text) is None

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assert cx._idearoot._groupheirs.get(sandy_text) != None
    assert cx._idearoot._groupheirs.get(sandy_text).name == sandy_text
    assert cx._idearoot._grouplines != {}
    root_idea = cx.get_idea_kid(road=f"{cx._idearoot._label}")
    sandy_groupline = cx._idearoot._grouplines.get(sandy_text)
    print(f"{sandy_groupline._contract_credit=} {root_idea._contract_importance=} ")
    print(f"  {sandy_groupline._contract_debt=} {root_idea._contract_importance=} ")
    sum_x = 0
    cat_road = f"{cx._economy_title},feed cat"
    cat_idea = cx.get_idea_kid(cat_road)
    week_road = f"{cx._economy_title},weekdays"
    week_idea = cx.get_idea_kid(week_road)
    work_road = f"{cx._economy_title},work"
    work_idea = cx.get_idea_kid(work_road)
    nation_road = f"{cx._economy_title},nation-state"
    nation_idea = cx.get_idea_kid(nation_road)
    sum_x = cat_idea._contract_importance
    print(f"{cat_idea._contract_importance=} {sum_x} ")
    sum_x += week_idea._contract_importance
    print(f"{week_idea._contract_importance=} {sum_x} ")
    sum_x += work_idea._contract_importance
    print(f"{work_idea._contract_importance=} {sum_x} ")
    sum_x += nation_idea._contract_importance
    print(f"{nation_idea._contract_importance=} {sum_x} ")
    assert sum_x >= 1.0
    assert sum_x < 1.00000000001

    # for kid_idea in root_idea._kids.values():
    #     sum_x += kid_idea._contract_importance
    #     print(f"  {kid_idea._contract_importance=} {sum_x=} {kid_idea.get_road()=}")
    assert round(sandy_groupline._contract_credit, 15) == 1
    assert round(sandy_groupline._contract_debt, 15) == 1
    x_groupline = Groupline(
        name=sandy_text,
        _contract_credit=0.9999999999999998,
        _contract_debt=0.9999999999999998,
    )
    assert cx._idearoot._grouplines == {x_groupline.name: x_groupline}


def test_TreeTraverseSetsGrouplineestorFromNonRootCorrectly():
    cx = example_contracts_get_contract_with_4_levels()
    cx.set_contract_metrics()
    # idea tree has no grouplinks
    assert cx._idearoot._grouplines == {}
    cx.add_memberunit(name="sandy")
    x_grouplink = GroupLink(name="sandy")
    cx._idearoot._kids["work"].set_grouplink(grouplink=x_grouplink)

    # idea tree has grouplinks
    cx.set_contract_metrics()
    assert cx._idearoot._grouplines != {}
    x_groupline = Groupline(
        name="sandy",
        _contract_credit=0.23076923076923078,
        _contract_debt=0.23076923076923078,
    )
    assert cx._idearoot._grouplines == {x_groupline.name: x_groupline}
    assert cx._idearoot._kids["work"]._grouplines != {}
    assert cx._idearoot._kids["work"]._grouplines == {x_groupline.name: x_groupline}


def test_contract4member_Exists():
    cx = example_contracts_get_contract_with_4_levels()
    x1_idea = IdeaKid(_label="email", promise=True)
    cx.add_idea(idea_kid=x1_idea, walk=f"{cx._economy_title},work")
    x2_idea = IdeaKid(_label="sweep", promise=True)
    cx.add_idea(idea_kid=x2_idea, walk=f"{cx._economy_title},work")

    sandy_name = MemberName("sandy")
    cx.add_memberunit(name=sandy_name)
    x_grouplink = GroupLink(name=sandy_name)
    yrx = cx._idearoot
    yrx._kids["work"]._kids["email"].set_grouplink(grouplink=x_grouplink)
    sandy_contract4member = cx.get_contract4member(
        acptfacts=None, member_name=sandy_name
    )
    assert sandy_contract4member
    assert str(type(sandy_contract4member)).find(".contract.ContractUnit'>")
    assert sandy_contract4member._owner == sandy_name


def test_contract4member_hasCorrectLevel1StructureNoGrouplessBranches():
    cx = example_contracts_get_contract_with_4_levels()
    x1_idea = IdeaKid(_label="email", promise=True)
    cx.add_idea(idea_kid=x1_idea, walk=f"{cx._economy_title},work")
    x2_idea = IdeaKid(_label="sweep", promise=True)
    cx.add_idea(idea_kid=x2_idea, walk=f"{cx._economy_title},work")

    billy_name = MemberName("billy")
    cx.add_memberunit(name=billy_name)
    billy_bl = GroupLink(name=billy_name)
    yrx = cx._idearoot
    yrx._kids["weekdays"].set_grouplink(grouplink=billy_bl)
    yrx._kids["feed cat"].set_grouplink(grouplink=billy_bl)
    yrx._kids["nation-state"].set_grouplink(grouplink=billy_bl)

    sandy_name = MemberName("sandy")
    cx.add_memberunit(name=sandy_name)
    sandy_bl = GroupLink(name=sandy_name)
    yrx._kids["work"]._kids["email"].set_grouplink(grouplink=sandy_bl)

    sandy_contract4member = cx.get_contract4member(
        acptfacts=None, member_name=sandy_name
    )
    assert len(sandy_contract4member._idearoot._kids) > 0
    print(f"{len(sandy_contract4member._idearoot._kids)=}")
    assert (
        str(type(sandy_contract4member._idearoot._kids.get("work"))).find(
            ".idea.IdeaKid'>"
        )
        > 0
    )
    assert sandy_contract4member._idearoot._kids.get("feed cat") is None
    assert sandy_contract4member._idearoot._contract_importance == 1
    y4a_work = sandy_contract4member._idearoot._kids.get("work")
    assert y4a_work._contract_importance == yrx._kids["work"]._contract_importance
    assert sandy_contract4member._idearoot._kids.get("__other__") != None
    y4a_others = sandy_contract4member._idearoot._kids.get("__other__")
    others_contract_importance = yrx._kids["weekdays"]._contract_importance
    others_contract_importance += yrx._kids["feed cat"]._contract_importance
    others_contract_importance += yrx._kids["nation-state"]._contract_importance
    print(f"{others_contract_importance=}")
    assert round(y4a_others._contract_importance, 15) == round(
        others_contract_importance, 15
    )


def test_contract_get_orderd_node_list_WorksCorrectly():
    cx = example_contracts_get_contract_with_4_levels()
    assert cx.get_idea_tree_ordered_road_list()
    ordered_node_list = cx.get_idea_tree_ordered_road_list()
    # for node in ordered_node_list:
    #     print(f"{node}")
    assert len(ordered_node_list) == 17
    assert cx.get_idea_tree_ordered_road_list()[0] == f"{cx._economy_title}"
    assert cx.get_idea_tree_ordered_road_list()[8] == f"{cx._economy_title},weekdays"

    lw_y = ContractUnit(_owner="MyContract")
    assert lw_y.get_idea_tree_ordered_road_list()[0] == cx._economy_title


def test_contract_get_orderd_node_list_CorrectlyFiltersRangedIdeaRoads():
    owner_text = "Tim"
    cx = ContractUnit(_owner=owner_text)
    time = "timeline"
    cx.add_idea(IdeaKid(_label=time, _begin=0, _close=700), walk=cx._economy_title)
    t_road = f"{cx._economy_title},{time}"
    week = "weeks"
    cx.add_idea(IdeaKid(_label=week, _denom=7), walk=t_road)

    assert len(cx.get_idea_tree_ordered_road_list()) == 3
    assert len(cx.get_idea_tree_ordered_road_list(no_range_descendants=True)) == 2


def test_contract_get_heir_road_list_returnsCorrectList():
    cx = example_contracts_get_contract_with_4_levels()
    weekdays = f"{cx._economy_title},weekdays"
    assert cx.get_heir_road_list(road_x=weekdays)
    heir_node_road_list = cx.get_heir_road_list(road_x=weekdays)
    # for node in heir_node_road_list:
    #     print(f"{node}")
    assert len(heir_node_road_list) == 8
    assert heir_node_road_list[0] == weekdays
    assert heir_node_road_list[3] == f"{weekdays},Saturday"
    assert heir_node_road_list[4] == f"{weekdays},Sunday"


# def test_contract4member_hasCorrectLevel1StructureWithGrouplessBranches_2():
#     cx = ContractUnit(_owner=owner_text)
#     cx.add_idea(idea_kid=IdeaKid(_label="A", _weight=7), walk="blahblah")
#     cx.add_idea(idea_kid=IdeaKid(_label="C", _weight=3), walk=f"{cx._economy_title},A")
#     cx.add_idea(idea_kid=IdeaKid(_label="E", _weight=7), walk=f"{cx._economy_title},A,C")
#     cx.add_idea(idea_kid=IdeaKid(_label="D", _weight=7), walk=f"{cx._economy_title},A,C")
#     cx.add_idea(idea_kid=IdeaKid(_label="B", _weight=13), walk="blahblah")
#     cx.add_idea(idea_kid=IdeaKid(_label="F", _weight=23), walk="blahblah")
#     cx.add_idea(idea_kid=IdeaKid(_label="G", _weight=57), walk="blahblah")
#     cx.add_idea(idea_kid=IdeaKid(_label="I"), walk=f"{cx._economy_title},G")
#     cx.add_idea(idea_kid=IdeaKid(_label="H"), walk=f"{cx._economy_title},G")
#     cx.add_idea(idea_kid=IdeaKid(_label="J"), walk=f"{cx._economy_title},G,I")
#     cx.add_idea(idea_kid=IdeaKid(_label="K"), walk=f"{cx._economy_title},G,I")
#     cx.add_idea(idea_kid=IdeaKid(_label="M"), walk=f"{cx._economy_title},G,H")

#     billy_name = MemberName("billy")
#     cx.add_memberunit(name=billy_name)
#     billy_bl = GroupLink(name=billy_name)
#     cx.edit_idea_attr(road=f"{cx._economy_title},G", grouplink=billy_bl)
#     cx.edit_idea_attr(road=f"{cx._economy_title},G,H,M", grouplink=billy_bl)

#     sandy_name = MemberName("sandy")
#     cx.add_memberunit(name=sandy_name)
#     sandy_bl = GroupLink(name=sandy_name)
#     cx.edit_idea_attr(road=f"{cx._economy_title},A", grouplink=sandy_bl)
#     cx.edit_idea_attr(road=f"{cx._economy_title},B", grouplink=sandy_bl)
#     cx.edit_idea_attr(road=f"{cx._economy_title},A,C,E", grouplink=sandy_bl)

#     # expected sandy
#     exp_sandy = ContractUnit(_owner=owner_text)
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="A", _contract_importance=0.07), walk="blahblah")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="C", _contract_importance=0.07), walk=f"{cx._economy_title},A")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="E", _contract_importance=0.5), walk=f"{cx._economy_title},A,C")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="B", _contract_importance=0.13), walk="blahblah")

#     # generated sandy
#     gen_sandy = cx.get_contract4member(acptfacts=None, member_name=sandy_name)

#     # check generated sandy is correct
#     assert gen_sandy.get_idea_kid(road=f"{cx._economy_title},A")._contract_importance == 0.07
#     assert gen_sandy.get_idea_kid(road=f"{cx._economy_title},A,C")._contract_importance == 0.07
#     assert gen_sandy.get_idea_kid(road=f"{cx._economy_title},A,C,E")._contract_importance == 0.5
#     assert gen_sandy.get_idea_kid(road=f"{cx._economy_title},B")._contract_importance == 0.13
#     assert (
#         gen_sandy.get_idea_kid(road=f"{cx._economy_title},A")._contract_importance
#         == exp_sandy.get_idea_kid(road=f"{cx._economy_title},A")._contract_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road=f"{cx._economy_title},A,C")._contract_importance
#         == exp_sandy.get_idea_kid(road=f"{cx._economy_title},A,C")._contract_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road=f"{cx._economy_title},A,C,E")._contract_importance
#         == exp_sandy.get_idea_kid(road=f"{cx._economy_title},A,C,E")._contract_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road=f"{cx._economy_title},B")._contract_importance
#         == exp_sandy.get_idea_kid(road=f"{cx._economy_title},B")._contract_importance
#     )
#     gen_sandy_list = gen_sandy.get_idea_list()
#     assert len(gen_sandy_list) == 5
