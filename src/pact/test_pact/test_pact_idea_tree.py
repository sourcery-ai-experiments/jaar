from src.pact.examples.example_pacts import (
    get_pact_with_4_levels as example_pacts_get_pact_with_4_levels,
)
from src.pact.party import PartyTitle
from src.pact.idea import IdeaKid
from src.pact.pact import PactUnit
from src.pact.group import Balanceline, Balancelink
from pytest import raises as pytest_raises


def test_set_pact_metrics_CorrectlyClearsDescendantAttributes():
    x_pact = example_pacts_get_pact_with_4_levels()

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
    yrx = x_pact._idearoot
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

    x_pact.set_pact_metrics()

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
    x_pact = example_pacts_get_pact_with_4_levels()

    brazil = f"{x_pact._cure_handle},nation-state,Brazil"
    idea_kid = x_pact.get_idea_kid(road=brazil)
    assert idea_kid != None
    assert idea_kid._label == "Brazil"

    weekdays = f"{x_pact._cure_handle},weekdays"
    idea_kid = x_pact.get_idea_kid(road=weekdays)
    assert idea_kid != None
    assert idea_kid._label == "weekdays"

    # with pytest.raises(Exception) as excinfo:
    #     x_pact.get_idea_kid(road=x_pact._cure_handle)
    # assert str(excinfo.value) == f"Cannot return root '{x_pact._cure_handle}'"
    idea_root = x_pact.get_idea_kid(road=x_pact._cure_handle)
    assert idea_root != None
    assert idea_root._label == x_pact._cure_handle

    wrong_road = f"{x_pact._cure_handle},bobdylan"
    with pytest_raises(Exception) as excinfo:
        x_pact.get_idea_kid(road=wrong_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='bobdylan' failed no item at '{wrong_road}'"
    )


def test_set_pact_metrics_RootOnlyCorrectlySetsDescendantAttributes():
    healer_text = "Tim"
    x_pact = PactUnit(_healer=healer_text)
    assert x_pact._idearoot._descendant_promise_count is None
    assert x_pact._idearoot._all_party_credit is None
    assert x_pact._idearoot._all_party_debt is None

    x_pact.set_pact_metrics()
    assert x_pact._idearoot._descendant_promise_count == 0
    assert x_pact._idearoot._all_party_credit == True
    assert x_pact._idearoot._all_party_debt == True


def test_set_pact_metrics_NLevelCorrectlySetsDescendantAttributes_1():
    x_pact = example_pacts_get_pact_with_4_levels()
    x_idea = IdeaKid(_label="email", promise=True)
    x_pact.add_idea(idea_kid=x_idea, pad=f"{x_pact._cure_handle},work")

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
    assert x_pact._idearoot._descendant_promise_count is None
    assert x_pact._idearoot._all_party_credit is None
    assert x_pact._idearoot._all_party_debt is None
    assert x_pact._idearoot._kids["work"]._descendant_promise_count is None
    assert x_pact._idearoot._kids["work"]._all_party_credit is None
    assert x_pact._idearoot._kids["work"]._all_party_debt is None
    assert (
        x_pact._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count
        is None
    )
    assert x_pact._idearoot._kids["weekdays"]._kids["Monday"]._all_party_credit is None
    assert x_pact._idearoot._kids["weekdays"]._kids["Monday"]._all_party_debt is None

    x_pact.set_pact_metrics()
    assert x_pact._idearoot._descendant_promise_count == 3
    assert x_pact._idearoot._kids["work"]._descendant_promise_count == 1
    assert x_pact._idearoot._kids["work"]._kids["email"]._descendant_promise_count == 0
    assert (
        x_pact._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count
        == 0
    )
    assert x_pact._idearoot._all_party_credit == True
    assert x_pact._idearoot._all_party_debt == True
    assert x_pact._idearoot._kids["work"]._all_party_credit == True
    assert x_pact._idearoot._kids["work"]._all_party_debt == True
    assert x_pact._idearoot._kids["weekdays"]._kids["Monday"]._all_party_credit == True
    assert x_pact._idearoot._kids["weekdays"]._kids["Monday"]._all_party_debt == True


def test_set_pact_metrics_NLevelCorrectlySetsDescendantAttributes_2():
    x_pact = example_pacts_get_pact_with_4_levels()
    x1_idea = IdeaKid(_label="email", promise=True)
    x_pact.add_idea(idea_kid=x1_idea, pad=f"{x_pact._cure_handle},work")
    x2_idea = IdeaKid(_label="sweep", promise=True)
    x_pact.add_idea(idea_kid=x2_idea, pad=f"{x_pact._cure_handle},work")

    x_pact.add_partyunit(title="sandy")
    x_balancelink = Balancelink(brand="sandy")
    x_pact._idearoot._kids["work"]._kids["email"].set_balancelink(
        balancelink=x_balancelink
    )
    # print(x_pact._kids["work"]._kids["email"])
    # print(x_pact._kids["work"]._kids["email"]._balancelink)
    x_pact.set_pact_metrics()
    # print(x_pact._kids["work"]._kids["email"])
    # print(x_pact._kids["work"]._kids["email"]._balancelink)

    assert x_pact._idearoot._all_party_credit == False
    assert x_pact._idearoot._all_party_debt == False
    assert x_pact._idearoot._kids["work"]._all_party_credit == False
    assert x_pact._idearoot._kids["work"]._all_party_debt == False
    assert x_pact._idearoot._kids["work"]._kids["email"]._all_party_credit == False
    assert x_pact._idearoot._kids["work"]._kids["email"]._all_party_debt == False
    assert x_pact._idearoot._kids["work"]._kids["sweep"]._all_party_credit == True
    assert x_pact._idearoot._kids["work"]._kids["sweep"]._all_party_debt == True
    assert x_pact._idearoot._kids["weekdays"]._all_party_credit == True
    assert x_pact._idearoot._kids["weekdays"]._all_party_debt == True
    assert x_pact._idearoot._kids["weekdays"]._kids["Monday"]._all_party_credit == True
    assert x_pact._idearoot._kids["weekdays"]._kids["Monday"]._all_party_debt == True
    assert x_pact._idearoot._kids["weekdays"]._kids["Tuesday"]._all_party_credit == True
    assert x_pact._idearoot._kids["weekdays"]._kids["Tuesday"]._all_party_debt == True


def test_TreeTraverseSetsClearsBalancelineestorsCorrectly():
    # sourcery skip: simplify-empty-collection-comparison
    x_pact = example_pacts_get_pact_with_4_levels()
    x_pact.set_pact_metrics()
    # idea tree has no balancelinks
    assert x_pact._idearoot._balancelines == {}
    x_pact._idearoot._balancelines = {1: "testtest"}
    assert x_pact._idearoot._balancelines != {}
    x_pact.set_pact_metrics()
    assert x_pact._idearoot._balancelines == {}

    # test for level 1 and level n
    x_pact._idearoot._kids["work"]._balancelines = {1: "testtest"}
    assert x_pact._idearoot._kids["work"]._balancelines != {}
    x_pact.set_pact_metrics()
    assert x_pact._idearoot._kids["work"]._balancelines == {}


def test_TreeTraverseSetsBalancelineestorFromRootCorrectly():
    # GIVEN
    x_pact = example_pacts_get_pact_with_4_levels()
    x_pact.set_pact_metrics()
    # idea tree has no balancelinks
    assert x_pact._idearoot._balancelines == {}
    sandy_text = "sandy"
    sandy_balancelink = Balancelink(brand=sandy_text)
    x_pact.add_partyunit(title=sandy_text)
    x_pact._idearoot.set_balancelink(balancelink=sandy_balancelink)
    # idea tree has balancelines
    assert x_pact._idearoot._balanceheirs.get(sandy_text) is None

    # WHEN
    x_pact.set_pact_metrics()

    # THEN
    assert x_pact._idearoot._balanceheirs.get(sandy_text) != None
    assert x_pact._idearoot._balanceheirs.get(sandy_text).brand == sandy_text
    assert x_pact._idearoot._balancelines != {}
    root_idea = x_pact.get_idea_kid(road=f"{x_pact._idearoot._label}")
    sandy_balanceline = x_pact._idearoot._balancelines.get(sandy_text)
    print(f"{sandy_balanceline._pact_credit=} {root_idea._pact_importance=} ")
    print(f"  {sandy_balanceline._pact_debt=} {root_idea._pact_importance=} ")
    sum_x = 0
    cat_road = f"{x_pact._cure_handle},feed cat"
    cat_idea = x_pact.get_idea_kid(cat_road)
    week_road = f"{x_pact._cure_handle},weekdays"
    week_idea = x_pact.get_idea_kid(week_road)
    work_road = f"{x_pact._cure_handle},work"
    work_idea = x_pact.get_idea_kid(work_road)
    nation_road = f"{x_pact._cure_handle},nation-state"
    nation_idea = x_pact.get_idea_kid(nation_road)
    sum_x = cat_idea._pact_importance
    print(f"{cat_idea._pact_importance=} {sum_x} ")
    sum_x += week_idea._pact_importance
    print(f"{week_idea._pact_importance=} {sum_x} ")
    sum_x += work_idea._pact_importance
    print(f"{work_idea._pact_importance=} {sum_x} ")
    sum_x += nation_idea._pact_importance
    print(f"{nation_idea._pact_importance=} {sum_x} ")
    assert sum_x >= 1.0
    assert sum_x < 1.00000000001

    # for kid_idea in root_idea._kids.values():
    #     sum_x += kid_idea._pact_importance
    #     print(f"  {kid_idea._pact_importance=} {sum_x=} {kid_idea.get_road()=}")
    assert round(sandy_balanceline._pact_credit, 15) == 1
    assert round(sandy_balanceline._pact_debt, 15) == 1
    x_balanceline = Balanceline(
        brand=sandy_text,
        _pact_credit=0.9999999999999998,
        _pact_debt=0.9999999999999998,
    )
    assert x_pact._idearoot._balancelines == {x_balanceline.brand: x_balanceline}


def test_TreeTraverseSetsBalancelineestorFromNonRootCorrectly():
    x_pact = example_pacts_get_pact_with_4_levels()
    x_pact.set_pact_metrics()
    # idea tree has no balancelinks
    assert x_pact._idearoot._balancelines == {}
    x_pact.add_partyunit(title="sandy")
    x_balancelink = Balancelink(brand="sandy")
    x_pact._idearoot._kids["work"].set_balancelink(balancelink=x_balancelink)

    # idea tree has balancelinks
    x_pact.set_pact_metrics()
    assert x_pact._idearoot._balancelines != {}
    x_balanceline = Balanceline(
        brand="sandy",
        _pact_credit=0.23076923076923078,
        _pact_debt=0.23076923076923078,
    )
    assert x_pact._idearoot._balancelines == {x_balanceline.brand: x_balanceline}
    assert x_pact._idearoot._kids["work"]._balancelines != {}
    assert x_pact._idearoot._kids["work"]._balancelines == {
        x_balanceline.brand: x_balanceline
    }


def test_pact4party_Exists():
    x_pact = example_pacts_get_pact_with_4_levels()
    x1_idea = IdeaKid(_label="email", promise=True)
    x_pact.add_idea(idea_kid=x1_idea, pad=f"{x_pact._cure_handle},work")
    x2_idea = IdeaKid(_label="sweep", promise=True)
    x_pact.add_idea(idea_kid=x2_idea, pad=f"{x_pact._cure_handle},work")

    sandy_title = PartyTitle("sandy")
    x_pact.add_partyunit(title=sandy_title)
    x_balancelink = Balancelink(brand=sandy_title)
    yrx = x_pact._idearoot
    yrx._kids["work"]._kids["email"].set_balancelink(balancelink=x_balancelink)
    sandy_pact4party = x_pact.get_pact4party(acptfacts=None, party_title=sandy_title)
    assert sandy_pact4party
    assert str(type(sandy_pact4party)).find(".pact.PactUnit'>")
    assert sandy_pact4party._healer == sandy_title


def test_pact4party_hasCorrectLevel1StructureNoGrouplessBranches():
    x_pact = example_pacts_get_pact_with_4_levels()
    x1_idea = IdeaKid(_label="email", promise=True)
    x_pact.add_idea(idea_kid=x1_idea, pad=f"{x_pact._cure_handle},work")
    x2_idea = IdeaKid(_label="sweep", promise=True)
    x_pact.add_idea(idea_kid=x2_idea, pad=f"{x_pact._cure_handle},work")

    billy_title = PartyTitle("billy")
    x_pact.add_partyunit(title=billy_title)
    billy_bl = Balancelink(brand=billy_title)
    yrx = x_pact._idearoot
    yrx._kids["weekdays"].set_balancelink(balancelink=billy_bl)
    yrx._kids["feed cat"].set_balancelink(balancelink=billy_bl)
    yrx._kids["nation-state"].set_balancelink(balancelink=billy_bl)

    sandy_title = PartyTitle("sandy")
    x_pact.add_partyunit(title=sandy_title)
    sandy_bl = Balancelink(brand=sandy_title)
    yrx._kids["work"]._kids["email"].set_balancelink(balancelink=sandy_bl)

    sandy_pact4party = x_pact.get_pact4party(acptfacts=None, party_title=sandy_title)
    assert len(sandy_pact4party._idearoot._kids) > 0
    print(f"{len(sandy_pact4party._idearoot._kids)=}")
    assert (
        str(type(sandy_pact4party._idearoot._kids.get("work"))).find(".idea.IdeaKid'>")
        > 0
    )
    assert sandy_pact4party._idearoot._kids.get("feed cat") is None
    assert sandy_pact4party._idearoot._pact_importance == 1
    y4a_work = sandy_pact4party._idearoot._kids.get("work")
    assert y4a_work._pact_importance == yrx._kids["work"]._pact_importance
    assert sandy_pact4party._idearoot._kids.get("__other__") != None
    y4a_others = sandy_pact4party._idearoot._kids.get("__other__")
    others_pact_importance = yrx._kids["weekdays"]._pact_importance
    others_pact_importance += yrx._kids["feed cat"]._pact_importance
    others_pact_importance += yrx._kids["nation-state"]._pact_importance
    print(f"{others_pact_importance=}")
    assert round(y4a_others._pact_importance, 15) == round(others_pact_importance, 15)


def test_pact_get_orderd_node_list_WorksCorrectly():
    x_pact = example_pacts_get_pact_with_4_levels()
    assert x_pact.get_idea_tree_ordered_road_list()
    ordered_node_list = x_pact.get_idea_tree_ordered_road_list()
    # for node in ordered_node_list:
    #     print(f"{node}")
    assert len(ordered_node_list) == 17
    assert x_pact.get_idea_tree_ordered_road_list()[0] == f"{x_pact._cure_handle}"
    assert (
        x_pact.get_idea_tree_ordered_road_list()[8] == f"{x_pact._cure_handle},weekdays"
    )

    lw_y = PactUnit(_healer="MyPact")
    assert lw_y.get_idea_tree_ordered_road_list()[0] == x_pact._cure_handle


def test_pact_get_orderd_node_list_CorrectlyFiltersRangedIdeaRoads():
    healer_text = "Tim"
    x_pact = PactUnit(_healer=healer_text)
    time = "timeline"
    x_pact.add_idea(IdeaKid(_label=time, _begin=0, _close=700), pad=x_pact._cure_handle)
    t_road = f"{x_pact._cure_handle},{time}"
    week = "weeks"
    x_pact.add_idea(IdeaKid(_label=week, _denom=7), pad=t_road)

    assert len(x_pact.get_idea_tree_ordered_road_list()) == 3
    assert len(x_pact.get_idea_tree_ordered_road_list(no_range_descendants=True)) == 2


def test_pact_get_heir_road_list_returnsCorrectList():
    x_pact = example_pacts_get_pact_with_4_levels()
    weekdays = f"{x_pact._cure_handle},weekdays"
    assert x_pact.get_heir_road_list(road_x=weekdays)
    heir_node_road_list = x_pact.get_heir_road_list(road_x=weekdays)
    # for node in heir_node_road_list:
    #     print(f"{node}")
    assert len(heir_node_road_list) == 8
    assert heir_node_road_list[0] == weekdays
    assert heir_node_road_list[3] == f"{weekdays},Saturday"
    assert heir_node_road_list[4] == f"{weekdays},Sunday"


# def test_pact4party_hasCorrectLevel1StructureWithGrouplessBranches_2():
#     x_pact = PactUnit(_healer=healer_text)
#     x_pact.add_idea(idea_kid=IdeaKid(_label="A", _weight=7), pad="blahblah")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="C", _weight=3), pad=f"{x_pact._cure_handle},A")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="E", _weight=7), pad=f"{x_pact._cure_handle},A,C")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="D", _weight=7), pad=f"{x_pact._cure_handle},A,C")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="B", _weight=13), pad="blahblah")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="F", _weight=23), pad="blahblah")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="G", _weight=57), pad="blahblah")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="I"), pad=f"{x_pact._cure_handle},G")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="H"), pad=f"{x_pact._cure_handle},G")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="J"), pad=f"{x_pact._cure_handle},G,I")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="K"), pad=f"{x_pact._cure_handle},G,I")
#     x_pact.add_idea(idea_kid=IdeaKid(_label="M"), pad=f"{x_pact._cure_handle},G,H")

#     billy_title = PartyTitle("billy")
#     x_pact.add_partyunit(title=billy_title)
#     billy_bl = Balancelink(brand=billy_title)
#     x_pact.edit_idea_attr(road=f"{x_pact._cure_handle},G", balancelink=billy_bl)
#     x_pact.edit_idea_attr(road=f"{x_pact._cure_handle},G,H,M", balancelink=billy_bl)

#     sandy_title = PartyTitle("sandy")
#     x_pact.add_partyunit(title=sandy_title)
#     sandy_bl = Balancelink(brand=sandy_title)
#     x_pact.edit_idea_attr(road=f"{x_pact._cure_handle},A", balancelink=sandy_bl)
#     x_pact.edit_idea_attr(road=f"{x_pact._cure_handle},B", balancelink=sandy_bl)
#     x_pact.edit_idea_attr(road=f"{x_pact._cure_handle},A,C,E", balancelink=sandy_bl)

#     # expected sandy
#     exp_sandy = PactUnit(_healer=healer_text)
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="A", _pact_importance=0.07), pad="blahblah")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="C", _pact_importance=0.07), pad=f"{x_pact._cure_handle},A")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="E", _pact_importance=0.5), pad=f"{x_pact._cure_handle},A,C")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_label="B", _pact_importance=0.13), pad="blahblah")

#     # generated sandy
#     gen_sandy = x_pact.get_pact4party(acptfacts=None, party_title=sandy_title)

#     # check generated sandy is correct
#     assert gen_sandy.get_idea_kid(road=f"{x_pact._cure_handle},A")._pact_importance == 0.07
#     assert gen_sandy.get_idea_kid(road=f"{x_pact._cure_handle},A,C")._pact_importance == 0.07
#     assert gen_sandy.get_idea_kid(road=f"{x_pact._cure_handle},A,C,E")._pact_importance == 0.5
#     assert gen_sandy.get_idea_kid(road=f"{x_pact._cure_handle},B")._pact_importance == 0.13
#     assert (
#         gen_sandy.get_idea_kid(road=f"{x_pact._cure_handle},A")._pact_importance
#         == exp_sandy.get_idea_kid(road=f"{x_pact._cure_handle},A")._pact_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road=f"{x_pact._cure_handle},A,C")._pact_importance
#         == exp_sandy.get_idea_kid(road=f"{x_pact._cure_handle},A,C")._pact_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road=f"{x_pact._cure_handle},A,C,E")._pact_importance
#         == exp_sandy.get_idea_kid(road=f"{x_pact._cure_handle},A,C,E")._pact_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road=f"{x_pact._cure_handle},B")._pact_importance
#         == exp_sandy.get_idea_kid(road=f"{x_pact._cure_handle},B")._pact_importance
#     )
#     gen_sandy_list = gen_sandy.get_idea_list()
#     assert len(gen_sandy_list) == 5
