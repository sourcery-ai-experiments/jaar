from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
)
from src.agenda.party import PartyPID
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.group import balanceline_shop, balancelink_shop
from pytest import raises as pytest_raises


def test_set_agenda_metrics_CorrectlyClearsDescendantAttributes():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()

    # idea ",{week_text},Sunday"
    # idea ",{week_text},Monday"
    # idea ",{week_text},Tuesday"
    # idea ",{week_text},Wednesday"
    # idea ",{week_text},Thursday"
    # idea ",{week_text},Friday"
    # idea ",{week_text},Saturday"
    # idea ",{week_text}"
    # idea ",{nation_text},USA,Texas"
    # idea ",{nation_text},USA,Oregon"
    # idea ",{nation_text},USA"
    # idea ",{nation_text},France"
    # idea ",{nation_text},Brazil"
    # idea ",{nation_text}"
    # idea work_text  # , promise=True)
    # idea feed_text  # , promise=True)

    # test root init status:
    work_text = "work"
    week_text = "weekdays"
    mon_text = "Monday"
    yrx = x_agenda._idearoot
    assert yrx._descendant_promise_count is None
    assert yrx._all_party_credit is None
    assert yrx._all_party_debt is None
    assert yrx._kids[work_text]._descendant_promise_count is None
    assert yrx._kids[work_text]._all_party_credit is None
    assert yrx._kids[work_text]._all_party_debt is None
    assert yrx._kids[week_text]._kids[mon_text]._descendant_promise_count is None
    assert yrx._kids[week_text]._kids[mon_text]._all_party_credit is None
    assert yrx._kids[week_text]._kids[mon_text]._all_party_debt is None

    yrx._descendant_promise_count = -2
    yrx._all_party_credit = -2
    yrx._all_party_debt = -2
    yrx._kids[work_text]._descendant_promise_count = -2
    yrx._kids[work_text]._all_party_credit = -2
    yrx._kids[work_text]._all_party_debt = -2
    yrx._kids[week_text]._kids[mon_text]._descendant_promise_count = -2
    yrx._kids[week_text]._kids[mon_text]._all_party_credit = -2
    yrx._kids[week_text]._kids[mon_text]._all_party_debt = -2

    assert yrx._descendant_promise_count == -2
    assert yrx._all_party_credit == -2
    assert yrx._all_party_debt == -2
    assert yrx._kids[work_text]._descendant_promise_count == -2
    assert yrx._kids[work_text]._all_party_credit == -2
    assert yrx._kids[work_text]._all_party_debt == -2
    assert yrx._kids[week_text]._kids[mon_text]._descendant_promise_count == -2
    assert yrx._kids[week_text]._kids[mon_text]._all_party_credit == -2
    assert yrx._kids[week_text]._kids[mon_text]._all_party_debt == -2

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert yrx._descendant_promise_count == 2
    assert yrx._kids[work_text]._descendant_promise_count == 0
    assert yrx._kids[week_text]._kids[mon_text]._descendant_promise_count == 0

    assert yrx._kids[week_text]._kids[mon_text]._all_party_credit == True
    assert yrx._kids[week_text]._kids[mon_text]._all_party_debt == True
    assert yrx._kids[work_text]._all_party_credit == True
    assert yrx._kids[work_text]._all_party_debt == True
    assert yrx._all_party_credit == True
    assert yrx._all_party_debt == True


def test_get_idea_obj_CorrectlyReturnsIdea():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    nation_text = "nation-state"
    nation_road = x_agenda.make_l1_road(nation_text)
    brazil_text = "Brazil"
    brazil_road = x_agenda.make_road(nation_road, brazil_text)

    # WHEN
    brazil_idea = x_agenda.get_idea_obj(road=brazil_road)

    # THEN
    assert brazil_idea != None
    assert brazil_idea._label == brazil_text

    # WHEN
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    week_idea = x_agenda.get_idea_obj(road=week_road)

    # THEN
    assert week_idea != None
    assert week_idea._label == week_text

    # WHEN
    root_idea = x_agenda.get_idea_obj(road=x_agenda._economy_id)

    # THEN
    assert root_idea != None
    assert root_idea._label == x_agenda._economy_id

    # WHEN / THEN
    bobdylan_text = "bobdylan"
    wrong_road = x_agenda.make_l1_road(bobdylan_text)
    with pytest_raises(Exception) as excinfo:
        x_agenda.get_idea_obj(road=wrong_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{wrong_road}'"


def test_set_agenda_metrics_RootOnlyCorrectlySetsDescendantAttributes():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)
    assert x_agenda._idearoot._descendant_promise_count is None
    assert x_agenda._idearoot._all_party_credit is None
    assert x_agenda._idearoot._all_party_debt is None

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert x_agenda._idearoot._descendant_promise_count == 0
    assert x_agenda._idearoot._all_party_credit == True
    assert x_agenda._idearoot._all_party_debt == True


def test_set_agenda_metrics_NLevelCorrectlySetsDescendantAttributes_1():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    week_text = "weekdays"
    mon_text = "Monday"

    email_text = "email"
    email_idea = ideaunit_shop(_label=email_text, promise=True)
    x_agenda.add_idea(email_idea, parent_road=work_road)

    # idea ",{week_text},Sunday"
    # idea ",{week_text},Monday"
    # idea ",{week_text},Tuesday"
    # idea ",{week_text},Wednesday"
    # idea ",{week_text},Thursday"
    # idea ",{week_text},Friday"
    # idea ",{week_text},Saturday"
    # idea ",{week_text}"
    # idea ",{nation_text},USA,Texas"
    # idea ",{nation_text},USA,Oregon"
    # idea ",{nation_text},USA"
    # idea ",{nation_text},France"
    # idea ",{nation_text},Brazil"
    # idea ",{nation_text}"
    # idea "work"  # , promise=True)
    # idea feed_text  # , promise=True)
    # idea "

    # test root init status:
    x_idearoot = x_agenda.get_idea_obj(x_agenda._economy_id)
    assert x_idearoot._descendant_promise_count is None
    assert x_idearoot._all_party_credit is None
    assert x_idearoot._all_party_debt is None
    assert x_idearoot._kids[work_text]._descendant_promise_count is None
    assert x_idearoot._kids[work_text]._all_party_credit is None
    assert x_idearoot._kids[work_text]._all_party_debt is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._descendant_promise_count is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_party_credit is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_party_debt is None

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert x_idearoot._descendant_promise_count == 3
    assert x_idearoot._kids[work_text]._descendant_promise_count == 1
    assert x_idearoot._kids[work_text]._kids[email_text]._descendant_promise_count == 0
    assert x_idearoot._kids[week_text]._kids[mon_text]._descendant_promise_count == 0
    assert x_idearoot._all_party_credit == True
    assert x_idearoot._all_party_debt == True
    assert x_idearoot._kids[work_text]._all_party_credit == True
    assert x_idearoot._kids[work_text]._all_party_debt == True
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_party_credit == True
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_party_debt == True


def test_set_agenda_metrics_NLevelCorrectlySetsDescendantAttributes_2():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    email_text = "email"
    work_text = "work"
    week_text = "weekdays"
    mon_text = "Monday"
    tue_text = "Tuesday"
    vaccum_text = "vaccum"
    sandy_text = "sandy"

    work_road = x_agenda.make_l1_road(work_text)
    email_idea = ideaunit_shop(_label=email_text, promise=True)
    x_agenda.add_idea(email_idea, parent_road=work_road)
    vaccum_idea = ideaunit_shop(_label=vaccum_text, promise=True)
    x_agenda.add_idea(vaccum_idea, parent_road=work_road)

    x_agenda.add_partyunit(pid=sandy_text)
    x_balancelink = balancelink_shop(brand=sandy_text)

    x_agenda._idearoot._kids[work_text]._kids[email_text].set_balancelink(
        balancelink=x_balancelink
    )
    # print(x_agenda._kids[work_text]._kids[email_text])
    # print(x_agenda._kids[work_text]._kids[email_text]._balancelink)

    # WHEN
    x_agenda.set_agenda_metrics()
    # print(x_agenda._kids[work_text]._kids[email_text])
    # print(x_agenda._kids[work_text]._kids[email_text]._balancelink)

    # THEN
    assert x_agenda._idearoot._all_party_credit == False
    assert x_agenda._idearoot._all_party_debt == False
    work_idea = x_agenda._idearoot._kids[work_text]
    assert work_idea._all_party_credit == False
    assert work_idea._all_party_debt == False
    assert work_idea._kids[email_text]._all_party_credit == False
    assert work_idea._kids[email_text]._all_party_debt == False
    assert work_idea._kids[vaccum_text]._all_party_credit == True
    assert work_idea._kids[vaccum_text]._all_party_debt == True
    week_idea = x_agenda._idearoot._kids[week_text]
    assert week_idea._all_party_credit == True
    assert week_idea._all_party_debt == True
    assert week_idea._kids[mon_text]._all_party_credit == True
    assert week_idea._kids[mon_text]._all_party_debt == True
    assert week_idea._kids[tue_text]._all_party_credit == True
    assert week_idea._kids[tue_text]._all_party_debt == True


def test_TreeTraverseSetsClearsBalanceLineestorsCorrectly():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()
    # idea tree has no balancelinks
    assert x_agenda._idearoot._balancelines == {}
    x_agenda._idearoot._balancelines = {1: "testtest"}
    assert x_agenda._idearoot._balancelines != {}

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert not x_agenda._idearoot._balancelines

    # WHEN
    # test for level 1 and level n
    work_text = "work"
    work_idea = x_agenda._idearoot._kids[work_text]
    work_idea._balancelines = {1: "testtest"}
    assert work_idea._balancelines != {}
    x_agenda.set_agenda_metrics()

    # THEN
    assert not x_agenda._idearoot._kids[work_text]._balancelines


def test_TreeTraverseSetsBalanceLineestorFromRootCorrectly():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()
    # idea tree has no balancelinks
    assert x_agenda._idearoot._balancelines == {}
    sandy_text = "sandy"
    week_text = "weekdays"
    nation_text = "nation-state"
    sandy_balancelink = balancelink_shop(brand=sandy_text)
    x_agenda.add_partyunit(pid=sandy_text)
    x_agenda._idearoot.set_balancelink(balancelink=sandy_balancelink)
    # idea tree has balancelines
    assert x_agenda._idearoot._balanceheirs.get(sandy_text) is None

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert x_agenda._idearoot._balanceheirs.get(sandy_text) != None
    assert x_agenda._idearoot._balanceheirs.get(sandy_text).brand == sandy_text
    assert x_agenda._idearoot._balancelines != {}
    root_idea = x_agenda.get_idea_obj(road=x_agenda._idearoot._label)
    sandy_balanceline = x_agenda._idearoot._balancelines.get(sandy_text)
    print(f"{sandy_balanceline._agenda_credit=} {root_idea._agenda_importance=} ")
    print(f"  {sandy_balanceline._agenda_debt=} {root_idea._agenda_importance=} ")
    sum_x = 0
    cat_road = x_agenda.make_l1_road("feed cat")
    cat_idea = x_agenda.get_idea_obj(cat_road)
    week_road = x_agenda.make_l1_road(week_text)
    week_idea = x_agenda.get_idea_obj(week_road)
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    work_idea = x_agenda.get_idea_obj(work_road)
    nation_road = x_agenda.make_l1_road(nation_text)
    nation_idea = x_agenda.get_idea_obj(nation_road)
    sum_x = cat_idea._agenda_importance
    print(f"{cat_idea._agenda_importance=} {sum_x} ")
    sum_x += week_idea._agenda_importance
    print(f"{week_idea._agenda_importance=} {sum_x} ")
    sum_x += work_idea._agenda_importance
    print(f"{work_idea._agenda_importance=} {sum_x} ")
    sum_x += nation_idea._agenda_importance
    print(f"{nation_idea._agenda_importance=} {sum_x} ")
    assert sum_x >= 1.0
    assert sum_x < 1.00000000001

    # for kid_idea in root_idea._kids.values():
    #     sum_x += kid_idea._agenda_importance
    #     print(f"  {kid_idea._agenda_importance=} {sum_x=} {kid_idea.get_road()=}")
    assert round(sandy_balanceline._agenda_credit, 15) == 1
    assert round(sandy_balanceline._agenda_debt, 15) == 1
    x_balanceline = balanceline_shop(
        brand=sandy_text,
        _agenda_credit=0.9999999999999998,
        _agenda_debt=0.9999999999999998,
    )
    assert x_agenda._idearoot._balancelines == {x_balanceline.brand: x_balanceline}


def test_TreeTraverseSetsBalanceLineestorFromNonRootCorrectly():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()
    # idea tree has no balancelinks
    sandy_text = "sandy"
    assert x_agenda._idearoot._balancelines == {}
    x_agenda.add_partyunit(pid=sandy_text)
    x_balancelink = balancelink_shop(brand=sandy_text)
    work_text = "work"
    email_text = "email"
    x_agenda._idearoot._kids[work_text].set_balancelink(balancelink=x_balancelink)

    # WHEN
    # idea tree has balancelinks
    x_agenda.set_agenda_metrics()

    # THEN
    assert x_agenda._idearoot._balancelines != {}
    x_balanceline = balanceline_shop(
        brand=sandy_text,
        _agenda_credit=0.23076923076923078,
        _agenda_debt=0.23076923076923078,
    )
    assert x_agenda._idearoot._balancelines == {x_balanceline.brand: x_balanceline}
    assert x_agenda._idearoot._kids[work_text]._balancelines != {}
    assert x_agenda._idearoot._kids[work_text]._balancelines == {
        x_balanceline.brand: x_balanceline
    }


def test_agenda4party_Exists():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    email_text = "email"
    work_text = "work"
    vaccum_text = "vaccum"
    sandy_text = "sandy"
    work_road = x_agenda.make_l1_road(work_text)
    email_idea = ideaunit_shop(_label=email_text, promise=True)
    x_agenda.add_idea(email_idea, parent_road=work_road)
    vaccum_idea = ideaunit_shop(_label=vaccum_text, promise=True)
    x_agenda.add_idea(vaccum_idea, parent_road=work_road)

    sandy_pid = PartyPID(sandy_text)
    x_agenda.add_partyunit(pid=sandy_pid)
    x_balancelink = balancelink_shop(brand=sandy_pid)
    yrx = x_agenda._idearoot
    yrx._kids[work_text]._kids[email_text].set_balancelink(balancelink=x_balancelink)

    # WHEN
    sandy_agenda4party = x_agenda.get_agenda4party(acptfacts=None, party_pid=sandy_pid)

    # THEN
    assert sandy_agenda4party
    assert str(type(sandy_agenda4party)).find(".agenda.AgendaUnit'>")
    assert sandy_agenda4party._healer == sandy_pid


def test_agenda4party_hasCorrectLevel1StructureNoGrouplessAncestors():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    email_text = "email"
    work_text = "work"
    vaccum_text = "vaccum"
    sandy_text = "sandy"
    week_text = "weekdays"
    feed_text = "feed cat"
    work_road = x_agenda.make_l1_road(work_text)
    email_idea = ideaunit_shop(_label=email_text, promise=True)
    x_agenda.add_idea(email_idea, parent_road=work_road)
    vaccum_idea = ideaunit_shop(_label=vaccum_text, promise=True)
    x_agenda.add_idea(vaccum_idea, parent_road=work_road)

    billy_pid = PartyPID("billy")
    x_agenda.add_partyunit(pid=billy_pid)
    billy_bl = balancelink_shop(brand=billy_pid)
    yrx = x_agenda._idearoot
    yrx._kids[week_text].set_balancelink(balancelink=billy_bl)
    yrx._kids[feed_text].set_balancelink(balancelink=billy_bl)
    nation_text = "nation-state"
    yrx._kids[nation_text].set_balancelink(balancelink=billy_bl)

    sandy_pid = PartyPID(sandy_text)
    x_agenda.add_partyunit(pid=sandy_pid)
    sandy_bl = balancelink_shop(brand=sandy_pid)
    yrx._kids[work_text]._kids[email_text].set_balancelink(balancelink=sandy_bl)

    # WHEN
    sandy_agenda4party = x_agenda.get_agenda4party(sandy_pid, acptfacts=None)

    # THEN
    assert len(sandy_agenda4party._idearoot._kids) > 0
    print(f"{len(sandy_agenda4party._idearoot._kids)=}")

    work_idea = sandy_agenda4party.get_idea_obj(work_road)
    type_check_IdeaUnit = str(type(work_idea)).find(".idea.IdeaUnit'>")
    print(f"{type_check_IdeaUnit=}")
    type_check_IdeaUnit = str(type(work_idea)).find(".idea.IdeaUnit'>")
    print(f"{type_check_IdeaUnit=}")
    assert str(type(work_idea)).find(".idea.IdeaUnit'>") > 0

    assert sandy_agenda4party._idearoot._kids.get(feed_text) is None
    assert sandy_agenda4party._idearoot._agenda_importance == 1
    assert work_idea._agenda_importance == yrx._kids[work_text]._agenda_importance
    __other__road = sandy_agenda4party.make_l1_road("__other__")
    assert sandy_agenda4party.get_idea_obj(__other__road) != None

    y4a_others = sandy_agenda4party.get_idea_obj(__other__road)
    others_agenda_importance = yrx._kids[week_text]._agenda_importance
    others_agenda_importance += yrx._kids[feed_text]._agenda_importance
    others_agenda_importance += yrx._kids[nation_text]._agenda_importance
    print(f"{others_agenda_importance=}")
    assert round(y4a_others._agenda_importance, 15) == round(
        others_agenda_importance, 15
    )


def test_agenda_get_orderd_node_list_WorksCorrectly():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    week_text = "weekdays"
    assert x_agenda.get_idea_tree_ordered_road_list()

    # WHEN
    ordered_node_list = x_agenda.get_idea_tree_ordered_road_list()
    # for node in ordered_node_list:
    #     print(f"{node}")

    # THEN
    assert len(ordered_node_list) == 17
    x_1st_road_in_ordered_list = x_agenda.get_idea_tree_ordered_road_list()[0]
    assert x_1st_road_in_ordered_list == x_agenda._economy_id
    x_8th_road_in_ordered_list = x_agenda.get_idea_tree_ordered_road_list()[8]
    assert x_8th_road_in_ordered_list == x_agenda.make_road(
        x_agenda._economy_id, week_text
    )

    # WHEN
    y_agenda = agendaunit_shop()

    # THEN
    y_1st_road_in_ordered_list = y_agenda.get_idea_tree_ordered_road_list()[0]
    assert y_1st_road_in_ordered_list == x_agenda._economy_id


def test_agenda_get_orderd_node_list_CorrectlyFiltersRangedIdeaRoadUnits():
    # GIVEN
    healer_text = "Tim"
    x_agenda = agendaunit_shop(_healer=healer_text)

    # WHEN
    time = "timeline"
    x_agenda.add_idea(
        ideaunit_shop(_label=time, _begin=0, _close=700),
        parent_road=x_agenda._economy_id,
    )
    t_road = x_agenda.make_l1_road(time)
    week = "weeks"
    x_agenda.add_idea(ideaunit_shop(_label=week, _denom=7), parent_road=t_road)

    # THEN
    assert len(x_agenda.get_idea_tree_ordered_road_list()) == 3
    assert len(x_agenda.get_idea_tree_ordered_road_list(no_range_descendants=True)) == 2


def test_agenda_get_heir_road_list_returnsCorrectList():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    week_text = "weekdays"
    weekdays = x_agenda.make_l1_road(week_text)
    assert x_agenda.get_heir_road_list(x_road=weekdays)

    # WHEN
    heir_nodes_road_list = x_agenda.get_heir_road_list(x_road=weekdays)

    # THEN
    # for node in heir_nodes_road_list:
    #     print(f"{node}")
    assert len(heir_nodes_road_list) == 8
    assert heir_nodes_road_list[0] == weekdays
    sat_text = "Saturday"
    sun_text = "Sunday"
    assert heir_nodes_road_list[3] == x_agenda.make_road(weekdays, sat_text)
    assert heir_nodes_road_list[4] == x_agenda.make_road(weekdays, sun_text)


# def test_agenda4party_hasCorrectLevel1StructureWithGrouplessAncestors_2():
#     x_agenda = agendaunit_shop(_healer=healer_text)
#     x_agenda.add_idea(ideaunit_shop("A", _weight=7), parent_road="blahblah")
#     x_agenda.add_idea(ideaunit_shop("C", _weight=3), parent_road=f"{x_agenda._economy_id},A")
#     x_agenda.add_idea(ideaunit_shop("E", _weight=7), parent_road=f"{x_agenda._economy_id},A,C")
#     x_agenda.add_idea(ideaunit_shop("D", _weight=7), parent_road=f"{x_agenda._economy_id},A,C")
#     x_agenda.add_idea(ideaunit_shop("B", _weight=13), parent_road="blahblah")
#     x_agenda.add_idea(ideaunit_shop("F", _weight=23), parent_road="blahblah")
#     x_agenda.add_idea(ideaunit_shop("G", _weight=57), parent_road="blahblah")
#     x_agenda.add_idea(ideaunit_shop("I"), parent_road=f"{x_agenda._economy_id},G")
#     x_agenda.add_idea(ideaunit_shop("H"), parent_road=f"{x_agenda._economy_id},G")
#     x_agenda.add_idea(ideaunit_shop("J"), parent_road=f"{x_agenda._economy_id},G,I")
#     x_agenda.add_idea(ideaunit_shop("K"), parent_road=f"{x_agenda._economy_id},G,I")
#     x_agenda.add_idea(ideaunit_shop("M"), parent_road=f"{x_agenda._economy_id},G,H")

#     billy_pid = PartyPID("billy")
#     x_agenda.add_partyunit(pid=billy_pid)
#     billy_bl = balancelink_shop(brand=billy_pid)
#     x_agenda.edit_idea_attr(road=f"{x_agenda._economy_id},G", balancelink=billy_bl)
#     x_agenda.edit_idea_attr(road=f"{x_agenda._economy_id},G,H,M", balancelink=billy_bl)

#     sandy_pid = PartyPID(sandy_text)
#     x_agenda.add_partyunit(pid=sandy_pid)
#     sandy_bl = balancelink_shop(brand=sandy_pid)
#     x_agenda.edit_idea_attr(road=f"{x_agenda._economy_id},A", balancelink=sandy_bl)
#     x_agenda.edit_idea_attr(road=f"{x_agenda._economy_id},B", balancelink=sandy_bl)
#     x_agenda.edit_idea_attr(road=f"{x_agenda._economy_id},A,C,E", balancelink=sandy_bl)

#     # expected sandy
#     exp_sandy = agendaunit_shop(_healer=healer_text)
#     exp_sandy.add_idea(ideaunit_shop("A", _agenda_importance=0.07), parent_road="blahblah")
#     exp_sandy.add_idea(ideaunit_shop("C", _agenda_importance=0.07), parent_road=f"{x_agenda._economy_id},A")
#     exp_sandy.add_idea(ideaunit_shop("E", _agenda_importance=0.5), parent_road=f"{x_agenda._economy_id},A,C")
#     exp_sandy.add_idea(ideaunit_shop("B", _agenda_importance=0.13), parent_road="blahblah")

#     # generated sandy
#     gen_sandy = x_agenda.get_agenda4party(acptfacts=None, party_pid=sandy_pid)

#     # check generated sandy is correct
#     assert gen_sandy.get_idea_obj(road=f"{x_agenda._economy_id},A")._agenda_importance == 0.07
#     assert gen_sandy.get_idea_obj(road=f"{x_agenda._economy_id},A,C")._agenda_importance == 0.07
#     assert gen_sandy.get_idea_obj(road=f"{x_agenda._economy_id},A,C,E")._agenda_importance == 0.5
#     assert gen_sandy.get_idea_obj(road=f"{x_agenda._economy_id},B")._agenda_importance == 0.13
#     assert (
#         gen_sandy.get_idea_obj(f"{x_agenda._economy_id},A")._agenda_importance
#         == exp_sandy.get_idea_obj(road=f"{x_agenda._economy_id},A")._agenda_importance
#     )
#     assert (
#         gen_sandy.get_idea_obj(road=f"{x_agenda._economy_id},A,C")._agenda_importance
#         == exp_sandy.get_idea_obj(road=f"{x_agenda._economy_id},A,C")._agenda_importance
#     )
#     assert (
#         gen_sandy.get_idea_obj(road=f"{x_agenda._economy_id},A,C,E")._agenda_importance
#         == exp_sandy.get_idea_obj(road=f"{x_agenda._economy_id},A,C,E")._agenda_importance
#     )
#     assert (
#         gen_sandy.get_idea_obj(road=f"{x_agenda._economy_id},B")._agenda_importance
#         == exp_sandy.get_idea_obj(road=f"{x_agenda._economy_id},B")._agenda_importance
#     )
#     gen_sandy_list = gen_sandy.get_idea_list()
#     assert len(gen_sandy_list) == 5


def test_agenda_idea_exists_ReturnsCorrectBool():
    # GIVEN
    sue_agenda = example_agendas_get_agenda_with_4_levels()
    sue_agenda.set_agenda_metrics()
    cat_road = sue_agenda.make_l1_road("feed cat")
    week_road = sue_agenda.make_l1_road("weekdays")
    work_road = sue_agenda.make_l1_road("work")
    nation_road = sue_agenda.make_l1_road("nation-state")
    sun_road = sue_agenda.make_road(week_road, "Sunday")
    mon_road = sue_agenda.make_road(week_road, "Monday")
    tue_road = sue_agenda.make_road(week_road, "Tuesday")
    wed_road = sue_agenda.make_road(week_road, "Wednesday")
    thu_road = sue_agenda.make_road(week_road, "Thursday")
    fri_road = sue_agenda.make_road(week_road, "Friday")
    sat_road = sue_agenda.make_road(week_road, "Saturday")
    france_road = sue_agenda.make_road(nation_road, "France")
    brazil_road = sue_agenda.make_road(nation_road, "Brazil")
    usa_road = sue_agenda.make_road(nation_road, "USA")
    texas_road = sue_agenda.make_road(usa_road, "Texas")
    oregon_road = sue_agenda.make_road(usa_road, "Oregon")
    # do not exist in agenda
    sports_road = sue_agenda.make_l1_road("sports")
    swim_road = sue_agenda.make_road(sports_road, "swimming")
    idaho_road = sue_agenda.make_road(usa_road, "Idaho")
    japan_road = sue_agenda.make_road(nation_road, "Japan")

    # WHEN/THEN
    assert sue_agenda.idea_exists("") == False
    assert sue_agenda.idea_exists(None) == False
    assert sue_agenda.idea_exists("A")
    assert sue_agenda.idea_exists(cat_road)
    assert sue_agenda.idea_exists(week_road)
    assert sue_agenda.idea_exists(work_road)
    assert sue_agenda.idea_exists(nation_road)
    assert sue_agenda.idea_exists(sun_road)
    assert sue_agenda.idea_exists(mon_road)
    assert sue_agenda.idea_exists(tue_road)
    assert sue_agenda.idea_exists(wed_road)
    assert sue_agenda.idea_exists(thu_road)
    assert sue_agenda.idea_exists(fri_road)
    assert sue_agenda.idea_exists(sat_road)
    assert sue_agenda.idea_exists(usa_road)
    assert sue_agenda.idea_exists(france_road)
    assert sue_agenda.idea_exists(brazil_road)
    assert sue_agenda.idea_exists(texas_road)
    assert sue_agenda.idea_exists(oregon_road)
    assert sue_agenda.idea_exists("B") == False
    assert sue_agenda.idea_exists(sports_road) == False
    assert sue_agenda.idea_exists(swim_road) == False
    assert sue_agenda.idea_exists(idaho_road) == False
    assert sue_agenda.idea_exists(japan_road) == False
