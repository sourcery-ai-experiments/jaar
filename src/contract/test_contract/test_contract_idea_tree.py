from src.contract.examples.example_contracts import (
    get_contract_with_4_levels as example_contracts_get_contract_with_4_levels,
)
from src.contract.party import PartyName
from src.contract.idea import IdeaKid
from src.contract.contract import ContractUnit
from src.contract.group import Balanceline, Balancelink
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
    assert yrx._all_party_credit is None
    assert yrx._all_party_debt is None
    assert yrx._kids["work"]._descendant_promise_count is None
    assert yrx._kids["work"]._all_party_credit is None
    assert yrx._kids["work"]._all_party_debt is None
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count is None
    assert yrx._kids["weekdays"]._kids["Monday"]._all_party_credit is None
    assert yrx._kids["weekdays"]._kids["Monday"]._all_party_debt is None

    yrx._descendant_promise_count = -2
    yrx._all_party_credit = -2
    yrx._all_party_debt = -2
    yrx._kids["work"]._descendant_promise_count = -2
    yrx._kids["work"]._all_party_credit = -2
    yrx._kids["work"]._all_party_debt = -2
    yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count = -2
    yrx._kids["weekdays"]._kids["Monday"]._all_party_credit = -2
    yrx._kids["weekdays"]._kids["Monday"]._all_party_debt = -2

    assert yrx._descendant_promise_count == -2
    assert yrx._all_party_credit == -2
    assert yrx._all_party_debt == -2
    assert yrx._kids["work"]._descendant_promise_count == -2
    assert yrx._kids["work"]._all_party_credit == -2
    assert yrx._kids["work"]._all_party_debt == -2
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count == -2
    assert yrx._kids["weekdays"]._kids["Monday"]._all_party_credit == -2
    assert yrx._kids["weekdays"]._kids["Monday"]._all_party_debt == -2

    cx.set_contract_metrics()

    assert yrx._descendant_promise_count == 2
    assert yrx._kids["work"]._descendant_promise_count == 0
    assert yrx._kids["weekdays"]._kids["Monday"]._descendant_promise_count == 0

    assert yrx._kids["weekdays"]._kids["Monday"]._all_party_credit == True
    assert yrx._kids["weekdays"]._kids["Monday"]._all_party_debt == True
    assert yrx._kids["work"]._all_party_credit == True
    assert yrx._kids["work"]._all_party_debt == True
    assert yrx._all_party_credit == True
    assert yrx._all_party_debt == True


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
    assert cx._idearoot._all_party_credit is None
    assert cx._idearoot._all_party_debt is None

    cx.set_contract_metrics()
    assert cx._idearoot._descendant_promise_count == 0
    assert cx._idearoot._all_party_credit == True
    assert cx._idearoot._all_party_debt == True


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
    assert cx._idearoot._all_party_credit is None
    assert cx._idearoot._all_party_debt is None
    assert cx._idearoot._kids["work"]._descendant_promise_count is None
    assert cx._idearoot._kids["work"]._all_party_credit is None
    assert cx._idearoot._kids["work"]._all_party_debt is None
    assert (
        cx._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count is None
    )
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_party_credit is None
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_party_debt is None

    cx.set_contract_metrics()
    assert cx._idearoot._descendant_promise_count == 3
    assert cx._idearoot._kids["work"]._descendant_promise_count == 1
    assert cx._idearoot._kids["work"]._kids["email"]._descendant_promise_count == 0
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count == 0
    assert cx._idearoot._all_party_credit == True
    assert cx._idearoot._all_party_debt == True
    assert cx._idearoot._kids["work"]._all_party_credit == True
    assert cx._idearoot._kids["work"]._all_party_debt == True
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_party_credit == True
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_party_debt == True


def test_set_contract_metrics_NLevelCorrectlySetsDescendantAttributes_2():
    cx = example_contracts_get_contract_with_4_levels()
    x1_idea = IdeaKid(_label="email", promise=True)
    cx.add_idea(idea_kid=x1_idea, walk=f"{cx._economy_title},work")
    x2_idea = IdeaKid(_label="sweep", promise=True)
    cx.add_idea(idea_kid=x2_idea, walk=f"{cx._economy_title},work")

    cx.add_partyunit(name="sandy")
    x_balancelink = Balancelink(brand="sandy")
    cx._idearoot._kids["work"]._kids["email"].set_balancelink(balancelink=x_balancelink)
    # print(cx._kids["work"]._kids["email"])
    # print(cx._kids["work"]._kids["email"]._balancelink)
    cx.set_contract_metrics()
    # print(cx._kids["work"]._kids["email"])
    # print(cx._kids["work"]._kids["email"]._balancelink)

    assert cx._idearoot._all_party_credit == False
    assert cx._idearoot._all_party_debt == False
    assert cx._idearoot._kids["work"]._all_party_credit == False
    assert cx._idearoot._kids["work"]._all_party_debt == False
    assert cx._idearoot._kids["work"]._kids["email"]._all_party_credit == False
    assert cx._idearoot._kids["work"]._kids["email"]._all_party_debt == False
    assert cx._idearoot._kids["work"]._kids["sweep"]._all_party_credit == True
    assert cx._idearoot._kids["work"]._kids["sweep"]._all_party_debt == True
    assert cx._idearoot._kids["weekdays"]._all_party_credit == True
    assert cx._idearoot._kids["weekdays"]._all_party_debt == True
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_party_credit == True
    assert cx._idearoot._kids["weekdays"]._kids["Monday"]._all_party_debt == True
    assert cx._idearoot._kids["weekdays"]._kids["Tuesday"]._all_party_credit == True
    assert cx._idearoot._kids["weekdays"]._kids["Tuesday"]._all_party_debt == True


def test_TreeTraverseSetsClearsBalancelineestorsCorrectly():
    # sourcery skip: simplify-empty-collection-comparison
    cx = example_contracts_get_contract_with_4_levels()
    cx.set_contract_metrics()
    # idea tree has no balancelinks
    assert cx._idearoot._balancelines == {}
    cx._idearoot._balancelines = {1: "testtest"}
    assert cx._idearoot._balancelines != {}
    cx.set_contract_metrics()
    assert cx._idearoot._balancelines == {}

    # test for level 1 and level n
    cx._idearoot._kids["work"]._balancelines = {1: "testtest"}
    assert cx._idearoot._kids["work"]._balancelines != {}
    cx.set_contract_metrics()
    assert cx._idearoot._kids["work"]._balancelines == {}


def test_TreeTraverseSetsBalancelineestorFromRootCorrectly():
    # GIVEN
    cx = example_contracts_get_contract_with_4_levels()
    cx.set_contract_metrics()
    # idea tree has no balancelinks
    assert cx._idearoot._balancelines == {}
    sandy_text = "sandy"
    sandy_balancelink = Balancelink(brand=sandy_text)
    cx.add_partyunit(name=sandy_text)
    cx._idearoot.set_balancelink(balancelink=sandy_balancelink)
    # idea tree has balancelines
    assert cx._idearoot._balanceheirs.get(sandy_text) is None

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assert cx._idearoot._balanceheirs.get(sandy_text) != None
    assert cx._idearoot._balanceheirs.get(sandy_text).brand == sandy_text
    assert cx._idearoot._balancelines != {}
    root_idea = cx.get_idea_kid(road=f"{cx._idearoot._label}")
    sandy_balanceline = cx._idearoot._balancelines.get(sandy_text)
    print(f"{sandy_balanceline._contract_credit=} {root_idea._contract_importance=} ")
    print(f"  {sandy_balanceline._contract_debt=} {root_idea._contract_importance=} ")
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
    assert round(sandy_balanceline._contract_credit, 15) == 1
    assert round(sandy_balanceline._contract_debt, 15) == 1
    x_balanceline = Balanceline(
        brand=sandy_text,
        _contract_credit=0.9999999999999998,
        _contract_debt=0.9999999999999998,
    )
    assert cx._idearoot._balancelines == {x_balanceline.brand: x_balanceline}


def test_TreeTraverseSetsBalancelineestorFromNonRootCorrectly():
    cx = example_contracts_get_contract_with_4_levels()
    cx.set_contract_metrics()
    # idea tree has no balancelinks
    assert cx._idearoot._balancelines == {}
    cx.add_partyunit(name="sandy")
    x_balancelink = Balancelink(brand="sandy")
    cx._idearoot._kids["work"].set_balancelink(balancelink=x_balancelink)

    # idea tree has balancelinks
    cx.set_contract_metrics()
    assert cx._idearoot._balancelines != {}
    x_balanceline = Balanceline(
        brand="sandy",
        _contract_credit=0.23076923076923078,
        _contract_debt=0.23076923076923078,
    )
    assert cx._idearoot._balancelines == {x_balanceline.brand: x_balanceline}
    assert cx._idearoot._kids["work"]._balancelines != {}
    assert cx._idearoot._kids["work"]._balancelines == {
        x_balanceline.brand: x_balanceline
    }


def test_contract4party_Exists():
    cx = example_contracts_get_contract_with_4_levels()
    x1_idea = IdeaKid(_label="email", promise=True)
    cx.add_idea(idea_kid=x1_idea, walk=f"{cx._economy_title},work")
    x2_idea = IdeaKid(_label="sweep", promise=True)
    cx.add_idea(idea_kid=x2_idea, walk=f"{cx._economy_title},work")

    sandy_name = PartyName("sandy")
    cx.add_partyunit(name=sandy_name)
    x_balancelink = Balancelink(brand=sandy_name)
    yrx = cx._idearoot
    yrx._kids["work"]._kids["email"].set_balancelink(balancelink=x_balancelink)
    sandy_contract4party = cx.get_contract4party(acptfacts=None, party_name=sandy_name)
    assert sandy_contract4party
    assert str(type(sandy_contract4party)).find(".contract.ContractUnit'>")
    assert sandy_contract4party._owner == sandy_name


def test_contract4party_hasCorrectLevel1StructureNoGrouplessBranches():
    cx = example_contracts_get_contract_with_4_levels()
    x1_idea = IdeaKid(_label="email", promise=True)
    cx.add_idea(idea_kid=x1_idea, walk=f"{cx._economy_title},work")
    x2_idea = IdeaKid(_label="sweep", promise=True)
    cx.add_idea(idea_kid=x2_idea, walk=f"{cx._economy_title},work")

    billy_name = PartyName("billy")
    cx.add_partyunit(name=billy_name)
    billy_bl = Balancelink(brand=billy_name)
    yrx = cx._idearoot
    yrx._kids["weekdays"].set_balancelink(balancelink=billy_bl)
    yrx._kids["feed cat"].set_balancelink(balancelink=billy_bl)
    yrx._kids["nation-state"].set_balancelink(balancelink=billy_bl)

    sandy_name = PartyName("sandy")
    cx.add_partyunit(name=sandy_name)
    sandy_bl = Balancelink(brand=sandy_name)
    yrx._kids["work"]._kids["email"].set_balancelink(balancelink=sandy_bl)

    sandy_contract4party = cx.get_contract4party(acptfacts=None, party_name=sandy_name)
    assert len(sandy_contract4party._idearoot._kids) > 0
    print(f"{len(sandy_contract4party._idearoot._kids)=}")
    assert (
        str(type(sandy_contract4party._idearoot._kids.get("work"))).find(
            ".idea.IdeaKid'>"
        )
        > 0
    )
    assert sandy_contract4party._idearoot._kids.get("feed cat") is None
    assert sandy_contract4party._idearoot._contract_importance == 1
    y4a_work = sandy_contract4party._idearoot._kids.get("work")
    assert y4a_work._contract_importance == yrx._kids["work"]._contract_importance
    assert sandy_contract4party._idearoot._kids.get("__other__") != None
    y4a_others = sandy_contract4party._idearoot._kids.get("__other__")
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


# def test_contract4party_hasCorrectLevel1StructureWithGrouplessBranches_2():
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

#     billy_name = PartyName("billy")
#     cx.add_partyunit(name=billy_name)
#     billy_bl = Balancelink(brand=billy_name)
#     cx.edit_idea_attr(road=f"{cx._economy_title},G", balancelink=billy_bl)
#     cx.edit_idea_attr(road=f"{cx._economy_title},G,H,M", balancelink=billy_bl)

#     sandy_name = PartyName("sandy")
#     cx.add_partyunit(name=sandy_name)
#     sandy_bl = Balancelink(brand=sandy_name)
#     cx.edit_idea_attr(road=f"{cx._economy_title},A", balancelink=sandy_bl)
#     cx.edit_idea_attr(road=f"{cx._economy_title},B", balancelink=sandy_bl)
#     cx.edit_idea_attr(road=f"{cx._economy_title},A,C,E", balancelink=sandy_bl)

#     # expected sandy
#     exp_sandy = ContractUnit(_owner=owner_text)
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="A", _contract_importance=0.07), walk="blahblah")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="C", _contract_importance=0.07), walk=f"{cx._economy_title},A")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="E", _contract_importance=0.5), walk=f"{cx._economy_title},A,C")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="B", _contract_importance=0.13), walk="blahblah")

#     # generated sandy
#     gen_sandy = cx.get_contract4party(acptfacts=None, party_name=sandy_name)

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
