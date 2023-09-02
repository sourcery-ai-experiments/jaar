from src.calendar.examples.example_calendars import (
    get_calendar_with_4_levels as example_calendars_get_calendar_with_4_levels,
)
from src.calendar.member import MemberName
from src.calendar.idea import IdeaKid
from src.calendar.calendar import CalendarUnit
from src.calendar.group import Groupline, GroupLink
from pytest import raises as pytest_raises


def test_set_calendar_metrics_CorrectlyClearsDescendantAttributes():
    calendar_x = example_calendars_get_calendar_with_4_levels()

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
    yrx = calendar_x._idearoot
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

    calendar_x.set_calendar_metrics()

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
    lw_x = example_calendars_get_calendar_with_4_levels()

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


def test_set_calendar_metrics_RootOnlyCorrectlySetsDescendantAttributes():
    lw_x = CalendarUnit(_owner="src")
    assert lw_x._idearoot._descendant_promise_count is None
    assert lw_x._idearoot._all_member_credit is None
    assert lw_x._idearoot._all_member_debt is None

    lw_x.set_calendar_metrics()
    assert lw_x._idearoot._descendant_promise_count == 0
    assert lw_x._idearoot._all_member_credit == True
    assert lw_x._idearoot._all_member_debt == True


def test_set_calendar_metrics_NLevelCorrectlySetsDescendantAttributes_1():
    lw_x = example_calendars_get_calendar_with_4_levels()
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
    assert lw_x._idearoot._all_member_credit is None
    assert lw_x._idearoot._all_member_debt is None
    assert lw_x._idearoot._kids["work"]._descendant_promise_count is None
    assert lw_x._idearoot._kids["work"]._all_member_credit is None
    assert lw_x._idearoot._kids["work"]._all_member_debt is None
    assert (
        lw_x._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count
        is None
    )
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_member_credit is None
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_member_debt is None

    lw_x.set_calendar_metrics()
    assert lw_x._idearoot._descendant_promise_count == 3
    assert lw_x._idearoot._kids["work"]._descendant_promise_count == 1
    assert lw_x._idearoot._kids["work"]._kids["email"]._descendant_promise_count == 0
    assert (
        lw_x._idearoot._kids["weekdays"]._kids["Monday"]._descendant_promise_count == 0
    )
    assert lw_x._idearoot._all_member_credit == True
    assert lw_x._idearoot._all_member_debt == True
    assert lw_x._idearoot._kids["work"]._all_member_credit == True
    assert lw_x._idearoot._kids["work"]._all_member_debt == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_member_credit == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_member_debt == True


def test_set_calendar_metrics_NLevelCorrectlySetsDescendantAttributes_2():
    lw_x = example_calendars_get_calendar_with_4_levels()
    x1_idea = IdeaKid(_desc="email", promise=True)
    lw_x.add_idea(idea_kid=x1_idea, walk="src,work")
    x2_idea = IdeaKid(_desc="sweep", promise=True)
    lw_x.add_idea(idea_kid=x2_idea, walk="src,work")

    lw_x.add_memberunit(name="sandy")
    x_grouplink = GroupLink(name="sandy")
    lw_x._idearoot._kids["work"]._kids["email"].set_grouplink(grouplink=x_grouplink)
    # print(lw_x._kids["work"]._kids["email"])
    # print(lw_x._kids["work"]._kids["email"]._grouplink)
    lw_x.set_calendar_metrics()
    # print(lw_x._kids["work"]._kids["email"])
    # print(lw_x._kids["work"]._kids["email"]._grouplink)

    assert lw_x._idearoot._all_member_credit == False
    assert lw_x._idearoot._all_member_debt == False
    assert lw_x._idearoot._kids["work"]._all_member_credit == False
    assert lw_x._idearoot._kids["work"]._all_member_debt == False
    assert lw_x._idearoot._kids["work"]._kids["email"]._all_member_credit == False
    assert lw_x._idearoot._kids["work"]._kids["email"]._all_member_debt == False
    assert lw_x._idearoot._kids["work"]._kids["sweep"]._all_member_credit == True
    assert lw_x._idearoot._kids["work"]._kids["sweep"]._all_member_debt == True
    assert lw_x._idearoot._kids["weekdays"]._all_member_credit == True
    assert lw_x._idearoot._kids["weekdays"]._all_member_debt == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_member_credit == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Monday"]._all_member_debt == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Tuesday"]._all_member_credit == True
    assert lw_x._idearoot._kids["weekdays"]._kids["Tuesday"]._all_member_debt == True


def test_TreeTraverseSetsClearsGrouplineestorsCorrectly():
    # sourcery skip: simplify-empty-collection-comparison
    calendar_x = example_calendars_get_calendar_with_4_levels()
    calendar_x.set_calendar_metrics()
    # idea tree has no grouplinks
    assert calendar_x._idearoot._grouplines == {}
    calendar_x._idearoot._grouplines = {1: "testtest"}
    assert calendar_x._idearoot._grouplines != {}
    calendar_x.set_calendar_metrics()
    assert calendar_x._idearoot._grouplines == {}

    # test for level 1 and level n
    calendar_x._idearoot._kids["work"]._grouplines = {1: "testtest"}
    assert calendar_x._idearoot._kids["work"]._grouplines != {}
    calendar_x.set_calendar_metrics()
    assert calendar_x._idearoot._kids["work"]._grouplines == {}


def test_TreeTraverseSetsGrouplineestorFromRootCorrectly():
    # GIVEN
    a_x = example_calendars_get_calendar_with_4_levels()
    a_x.set_calendar_metrics()
    # idea tree has no grouplinks
    assert a_x._idearoot._grouplines == {}
    sandy_text = "sandy"
    sandy_grouplink = GroupLink(name=sandy_text)
    a_x.add_memberunit(name=sandy_text)
    a_x._idearoot.set_grouplink(grouplink=sandy_grouplink)
    # idea tree has grouplines
    assert a_x._idearoot._groupheirs.get(sandy_text) is None

    # WHEN
    a_x.set_calendar_metrics()

    # THEN
    assert a_x._idearoot._groupheirs.get(sandy_text) != None
    assert a_x._idearoot._groupheirs.get(sandy_text).name == sandy_text
    assert a_x._idearoot._grouplines != {}
    root_idea = a_x.get_idea_kid(road=f"{a_x._idearoot._desc}")
    sandy_groupline = a_x._idearoot._grouplines.get(sandy_text)
    print(f"{sandy_groupline._calendar_credit=} {root_idea._calendar_importance=} ")
    print(f"  {sandy_groupline._calendar_debt=} {root_idea._calendar_importance=} ")
    sum_x = 0
    cat_road = "src,feed cat"
    cat_idea = a_x.get_idea_kid(cat_road)
    week_road = "src,weekdays"
    week_idea = a_x.get_idea_kid(week_road)
    work_road = "src,work"
    work_idea = a_x.get_idea_kid(work_road)
    nation_road = "src,nation-state"
    nation_idea = a_x.get_idea_kid(nation_road)
    sum_x = cat_idea._calendar_importance
    print(f"{cat_idea._calendar_importance=} {sum_x} ")
    sum_x += week_idea._calendar_importance
    print(f"{week_idea._calendar_importance=} {sum_x} ")
    sum_x += work_idea._calendar_importance
    print(f"{work_idea._calendar_importance=} {sum_x} ")
    sum_x += nation_idea._calendar_importance
    print(f"{nation_idea._calendar_importance=} {sum_x} ")
    assert sum_x >= 1.0
    assert sum_x < 1.00000000001

    # for kid_idea in root_idea._kids.values():
    #     sum_x += kid_idea._calendar_importance
    #     print(f"  {kid_idea._calendar_importance=} {sum_x=} {kid_idea.get_road()=}")
    assert round(sandy_groupline._calendar_credit, 15) == 1
    assert round(sandy_groupline._calendar_debt, 15) == 1
    x_groupline = Groupline(
        name=sandy_text,
        _calendar_credit=0.9999999999999998,
        _calendar_debt=0.9999999999999998,
    )
    assert a_x._idearoot._grouplines == {x_groupline.name: x_groupline}


def test_TreeTraverseSetsGrouplineestorFromNonRootCorrectly():
    lw_x = example_calendars_get_calendar_with_4_levels()
    lw_x.set_calendar_metrics()
    # idea tree has no grouplinks
    assert lw_x._idearoot._grouplines == {}
    lw_x.add_memberunit(name="sandy")
    x_grouplink = GroupLink(name="sandy")
    lw_x._idearoot._kids["work"].set_grouplink(grouplink=x_grouplink)

    # idea tree has grouplinks
    lw_x.set_calendar_metrics()
    assert lw_x._idearoot._grouplines != {}
    x_groupline = Groupline(
        name="sandy",
        _calendar_credit=0.23076923076923078,
        _calendar_debt=0.23076923076923078,
    )
    assert lw_x._idearoot._grouplines == {x_groupline.name: x_groupline}
    assert lw_x._idearoot._kids["work"]._grouplines != {}
    assert lw_x._idearoot._kids["work"]._grouplines == {x_groupline.name: x_groupline}


def test_calendar4member_Exists():
    calendar_x = example_calendars_get_calendar_with_4_levels()
    x1_idea = IdeaKid(_desc="email", promise=True)
    calendar_x.add_idea(idea_kid=x1_idea, walk="src,work")
    x2_idea = IdeaKid(_desc="sweep", promise=True)
    calendar_x.add_idea(idea_kid=x2_idea, walk="src,work")

    sandy_name = MemberName("sandy")
    calendar_x.add_memberunit(name=sandy_name)
    x_grouplink = GroupLink(name=sandy_name)
    yrx = calendar_x._idearoot
    yrx._kids["work"]._kids["email"].set_grouplink(grouplink=x_grouplink)
    sandy_calendar4member = calendar_x.get_calendar4member(
        acptfacts=None, member_name=sandy_name
    )
    assert sandy_calendar4member
    assert str(type(sandy_calendar4member)).find(".calendar.CalendarUnit'>")
    assert sandy_calendar4member._owner == sandy_name


def test_calendar4member_hasCorrectLevel1StructureNoGrouplessBranches():
    calendar_x = example_calendars_get_calendar_with_4_levels()
    x1_idea = IdeaKid(_desc="email", promise=True)
    calendar_x.add_idea(idea_kid=x1_idea, walk="src,work")
    x2_idea = IdeaKid(_desc="sweep", promise=True)
    calendar_x.add_idea(idea_kid=x2_idea, walk="src,work")

    billy_name = MemberName("billy")
    calendar_x.add_memberunit(name=billy_name)
    billy_bl = GroupLink(name=billy_name)
    yrx = calendar_x._idearoot
    yrx._kids["weekdays"].set_grouplink(grouplink=billy_bl)
    yrx._kids["feed cat"].set_grouplink(grouplink=billy_bl)
    yrx._kids["nation-state"].set_grouplink(grouplink=billy_bl)

    sandy_name = MemberName("sandy")
    calendar_x.add_memberunit(name=sandy_name)
    sandy_bl = GroupLink(name=sandy_name)
    yrx._kids["work"]._kids["email"].set_grouplink(grouplink=sandy_bl)

    sandy_calendar4member = calendar_x.get_calendar4member(
        acptfacts=None, member_name=sandy_name
    )
    assert len(sandy_calendar4member._idearoot._kids) > 0
    print(f"{len(sandy_calendar4member._idearoot._kids)=}")
    assert (
        str(type(sandy_calendar4member._idearoot._kids.get("work"))).find(
            ".idea.IdeaKid'>"
        )
        > 0
    )
    assert sandy_calendar4member._idearoot._kids.get("feed cat") is None
    assert sandy_calendar4member._idearoot._calendar_importance == 1
    y4a_work = sandy_calendar4member._idearoot._kids.get("work")
    assert y4a_work._calendar_importance == yrx._kids["work"]._calendar_importance
    assert sandy_calendar4member._idearoot._kids.get("__other__") != None
    y4a_others = sandy_calendar4member._idearoot._kids.get("__other__")
    others_calendar_importance = yrx._kids["weekdays"]._calendar_importance
    others_calendar_importance += yrx._kids["feed cat"]._calendar_importance
    others_calendar_importance += yrx._kids["nation-state"]._calendar_importance
    print(f"{others_calendar_importance=}")
    assert round(y4a_others._calendar_importance, 15) == round(
        others_calendar_importance, 15
    )


def test_calendar_get_orderd_node_list_WorksCorrectly():
    lw_x = example_calendars_get_calendar_with_4_levels()
    assert lw_x.get_idea_tree_ordered_road_list()
    ordered_node_list = lw_x.get_idea_tree_ordered_road_list()
    # for node in ordered_node_list:
    #     print(f"{node}")
    assert len(ordered_node_list) == 17
    assert lw_x.get_idea_tree_ordered_road_list()[0] == "src"
    assert lw_x.get_idea_tree_ordered_road_list()[8] == "src,weekdays"

    lw_y = CalendarUnit(_owner="MyCalendar")
    assert lw_y.get_idea_tree_ordered_road_list()[0] == "MyCalendar"


def test_calendar_get_orderd_node_list_CorrectlyFiltersRangedIdeaRoads():
    src = "src"
    calendar_x = CalendarUnit(_owner=src)
    time = "timeline"
    calendar_x.add_idea(IdeaKid(_desc=time, _begin=0, _close=700), walk=src)
    t_road = f"{src},{time}"
    week = "weeks"
    calendar_x.add_idea(IdeaKid(_desc=week, _denom=7), walk=t_road)

    assert len(calendar_x.get_idea_tree_ordered_road_list()) == 3
    assert (
        len(calendar_x.get_idea_tree_ordered_road_list(no_range_descendents=True)) == 2
    )


def test_calendar_get_heir_road_list_returnsCorrectList():
    lw_x = example_calendars_get_calendar_with_4_levels()
    weekdays = "src,weekdays"
    assert lw_x.get_heir_road_list(src_road=weekdays)
    heir_node_road_list = lw_x.get_heir_road_list(src_road=weekdays)
    # for node in heir_node_road_list:
    #     print(f"{node}")
    assert len(heir_node_road_list) == 8
    assert heir_node_road_list[0] == weekdays
    assert heir_node_road_list[3] == f"{weekdays},Saturday"
    assert heir_node_road_list[4] == f"{weekdays},Sunday"


# def test_calendar4member_hasCorrectLevel1StructureWithGrouplessBranches_2():
#     lw_desc = "src"
#     lw_x = CalendarUnit(_owner=lw_desc)
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

#     billy_name = MemberName("billy")
#     lw_x.add_memberunit(name=billy_name)
#     billy_bl = GroupLink(name=billy_name)
#     lw_x.edit_idea_attr(road="src,G", grouplink=billy_bl)
#     lw_x.edit_idea_attr(road="src,G,H,M", grouplink=billy_bl)

#     sandy_name = MemberName("sandy")
#     lw_x.add_memberunit(name=sandy_name)
#     sandy_bl = GroupLink(name=sandy_name)
#     lw_x.edit_idea_attr(road="src,A", grouplink=sandy_bl)
#     lw_x.edit_idea_attr(road="src,B", grouplink=sandy_bl)
#     lw_x.edit_idea_attr(road="src,A,C,E", grouplink=sandy_bl)

#     # expected sandy
#     exp_sandy = CalendarUnit(_owner=lw_desc)
#     exp_sandy.add_idea(idea_kid=IdeaKid(_desc="A", _calendar_importance=0.07), walk="src")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_desc="C", _calendar_importance=0.07), walk="src,A")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_desc="E", _calendar_importance=0.5), walk="src,A,C")
#     exp_sandy.add_idea(idea_kid=IdeaKid(_desc="B", _calendar_importance=0.13), walk="src")

#     # generated sandy
#     gen_sandy = lw_x.get_calendar4member(acptfacts=None, member_name=sandy_name)

#     # confirm generated sandy is correct
#     assert gen_sandy.get_idea_kid(road="src,A")._calendar_importance == 0.07
#     assert gen_sandy.get_idea_kid(road="src,A,C")._calendar_importance == 0.07
#     assert gen_sandy.get_idea_kid(road="src,A,C,E")._calendar_importance == 0.5
#     assert gen_sandy.get_idea_kid(road="src,B")._calendar_importance == 0.13
#     assert (
#         gen_sandy.get_idea_kid(road="src,A")._calendar_importance
#         == exp_sandy.get_idea_kid(road="src,A")._calendar_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road="src,A,C")._calendar_importance
#         == exp_sandy.get_idea_kid(road="src,A,C")._calendar_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road="src,A,C,E")._calendar_importance
#         == exp_sandy.get_idea_kid(road="src,A,C,E")._calendar_importance
#     )
#     assert (
#         gen_sandy.get_idea_kid(road="src,B")._calendar_importance
#         == exp_sandy.get_idea_kid(road="src,B")._calendar_importance
#     )
#     gen_sandy_list = gen_sandy.get_idea_list()
#     assert len(gen_sandy_list) == 5
