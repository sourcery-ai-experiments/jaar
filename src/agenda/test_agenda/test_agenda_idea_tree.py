from src._road.road import get_default_real_id_roadnode as root_label
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
)
from src.agenda.healer import healerhold_shop
from src.agenda.party import PartyID
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.group import balanceline_shop, balancelink_shop
from src.agenda.graphic import display_ideatree
from pytest import raises as pytest_raises


def test_AgendaUnit_set_tree_traverse_starting_point_CorrectlySetsAttrs():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    x_rational = True
    x_tree_traverse_count = 555
    x_idea_dict = {1: 2, 2: 4}
    sue_agenda._rational = x_rational
    sue_agenda._tree_traverse_count = x_tree_traverse_count
    sue_agenda._idea_dict = x_idea_dict
    assert sue_agenda._rational == x_rational
    assert sue_agenda._tree_traverse_count == x_tree_traverse_count
    assert sue_agenda._idea_dict == x_idea_dict

    # WHEN
    sue_agenda._set_tree_traverse_starting_point()

    # THEN
    assert sue_agenda._rational != x_rational
    assert not sue_agenda._rational
    assert sue_agenda._tree_traverse_count != x_tree_traverse_count
    assert sue_agenda._tree_traverse_count == 0
    assert sue_agenda._idea_dict != x_idea_dict
    assert sue_agenda._idea_dict == {
        sue_agenda._idearoot.get_road(): sue_agenda._idearoot
    }


def test_AgendaUnit_clear_agenda_base_metrics_CorrectlySetsAttrs():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    x_econ_justifed = False
    x_sum_healerhold_importance = 140
    sue_agenda._econs_justified = x_econ_justifed
    sue_agenda._econs_buildable = "swimmers"
    sue_agenda._sum_healerhold_importance = x_sum_healerhold_importance
    sue_agenda._econ_dict = {"run": "run"}
    sue_agenda._healers_dict = {"run": "run"}
    assert sue_agenda._econs_justified == x_econ_justifed
    assert sue_agenda._econs_buildable != False
    assert sue_agenda._sum_healerhold_importance == x_sum_healerhold_importance
    assert sue_agenda._econ_dict != {}
    assert sue_agenda._healers_dict != {}

    # WHEN
    sue_agenda._clear_agenda_base_metrics()

    # THEN
    assert sue_agenda._econs_justified != x_econ_justifed
    assert sue_agenda._econs_justified
    assert sue_agenda._econs_buildable == False
    assert sue_agenda._sum_healerhold_importance == 0
    assert not sue_agenda._econ_dict
    assert not sue_agenda._healers_dict


def test_AgendaUnit_calc_agenda_metrics_ClearsDescendantAttributes():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    # test root status:
    casa_text = "casa"
    week_text = "weekdays"
    mon_text = "Monday"
    yrx = x_agenda._idearoot
    assert yrx._descendant_pledge_count is None
    assert yrx._all_party_credit is None
    assert yrx._all_party_debt is None
    assert yrx._kids[casa_text]._descendant_pledge_count is None
    assert yrx._kids[casa_text]._all_party_credit is None
    assert yrx._kids[casa_text]._all_party_debt is None
    assert yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count is None
    assert yrx._kids[week_text]._kids[mon_text]._all_party_credit is None
    assert yrx._kids[week_text]._kids[mon_text]._all_party_debt is None

    yrx._descendant_pledge_count = -2
    yrx._all_party_credit = -2
    yrx._all_party_debt = -2
    yrx._kids[casa_text]._descendant_pledge_count = -2
    yrx._kids[casa_text]._all_party_credit = -2
    yrx._kids[casa_text]._all_party_debt = -2
    yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count = -2
    yrx._kids[week_text]._kids[mon_text]._all_party_credit = -2
    yrx._kids[week_text]._kids[mon_text]._all_party_debt = -2

    assert yrx._descendant_pledge_count == -2
    assert yrx._all_party_credit == -2
    assert yrx._all_party_debt == -2
    assert yrx._kids[casa_text]._descendant_pledge_count == -2
    assert yrx._kids[casa_text]._all_party_credit == -2
    assert yrx._kids[casa_text]._all_party_debt == -2
    assert yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count == -2
    assert yrx._kids[week_text]._kids[mon_text]._all_party_credit == -2
    assert yrx._kids[week_text]._kids[mon_text]._all_party_debt == -2

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN
    assert yrx._descendant_pledge_count == 2
    assert yrx._kids[casa_text]._descendant_pledge_count == 0
    assert yrx._kids[week_text]._kids[mon_text]._descendant_pledge_count == 0

    assert yrx._kids[week_text]._kids[mon_text]._all_party_credit == True
    assert yrx._kids[week_text]._kids[mon_text]._all_party_debt == True
    assert yrx._kids[casa_text]._all_party_credit == True
    assert yrx._kids[casa_text]._all_party_debt == True
    assert yrx._all_party_credit == True
    assert yrx._all_party_debt == True


def test_AgendaUnit_get_idea_obj_ReturnsIdea():
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
    root_idea = x_agenda.get_idea_obj(road=x_agenda._real_id)

    # THEN
    assert root_idea != None
    assert root_idea._label == x_agenda._real_id

    # WHEN / THEN
    bobdylan_text = "bobdylan"
    wrong_road = x_agenda.make_l1_road(bobdylan_text)
    with pytest_raises(Exception) as excinfo:
        x_agenda.get_idea_obj(road=wrong_road)
    assert str(excinfo.value) == f"get_idea_obj failed. no item at '{wrong_road}'"


def test_AgendaUnit_calc_agenda_metrics_RootOnlyCorrectlySetsDescendantAttributes():
    # GIVEN
    tim_agenda = agendaunit_shop(_owner_id="Tim")
    assert tim_agenda._idearoot._descendant_pledge_count is None
    assert tim_agenda._idearoot._all_party_credit is None
    assert tim_agenda._idearoot._all_party_debt is None

    # WHEN
    tim_agenda.calc_agenda_metrics()

    # THEN
    assert tim_agenda._idearoot._descendant_pledge_count == 0
    assert tim_agenda._idearoot._all_party_credit == True
    assert tim_agenda._idearoot._all_party_debt == True


def test_AgendaUnit_calc_agenda_metrics_NLevelCorrectlySetsDescendantAttributes_1():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    week_text = "weekdays"
    mon_text = "Monday"

    email_text = "email"
    email_idea = ideaunit_shop(_label=email_text, pledge=True)
    x_agenda.add_idea(email_idea, parent_road=casa_road)

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
    # idea "casa"  # , pledge=True)
    # idea feed_text  # , pledge=True)
    # idea "

    # test root status:
    x_idearoot = x_agenda.get_idea_obj(x_agenda._real_id)
    assert x_idearoot._descendant_pledge_count is None
    assert x_idearoot._all_party_credit is None
    assert x_idearoot._all_party_debt is None
    assert x_idearoot._kids[casa_text]._descendant_pledge_count is None
    assert x_idearoot._kids[casa_text]._all_party_credit is None
    assert x_idearoot._kids[casa_text]._all_party_debt is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._descendant_pledge_count is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_party_credit is None
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_party_debt is None

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN
    assert x_idearoot._descendant_pledge_count == 3
    assert x_idearoot._kids[casa_text]._descendant_pledge_count == 1
    assert x_idearoot._kids[casa_text]._kids[email_text]._descendant_pledge_count == 0
    assert x_idearoot._kids[week_text]._kids[mon_text]._descendant_pledge_count == 0
    assert x_idearoot._all_party_credit == True
    assert x_idearoot._all_party_debt == True
    assert x_idearoot._kids[casa_text]._all_party_credit == True
    assert x_idearoot._kids[casa_text]._all_party_debt == True
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_party_credit == True
    assert x_idearoot._kids[week_text]._kids[mon_text]._all_party_debt == True


def test_AgendaUnit_calc_agenda_metrics_NLevelCorrectlySetsDescendantAttributes_2():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    email_text = "email"
    casa_text = "casa"
    week_text = "weekdays"
    mon_text = "Monday"
    tue_text = "Tuesday"
    vacuum_text = "vacuum"
    sue_text = "sue"

    casa_road = x_agenda.make_l1_road(casa_text)
    email_idea = ideaunit_shop(_label=email_text, pledge=True)
    x_agenda.add_idea(email_idea, parent_road=casa_road)
    vacuum_idea = ideaunit_shop(_label=vacuum_text, pledge=True)
    x_agenda.add_idea(vacuum_idea, parent_road=casa_road)

    x_agenda.add_partyunit(party_id=sue_text)
    x_balancelink = balancelink_shop(group_id=sue_text)

    x_agenda._idearoot._kids[casa_text]._kids[email_text].set_balancelink(
        balancelink=x_balancelink
    )
    # print(x_agenda._kids[casa_text]._kids[email_text])
    # print(x_agenda._kids[casa_text]._kids[email_text]._balancelink)

    # WHEN
    x_agenda.calc_agenda_metrics()
    # print(x_agenda._kids[casa_text]._kids[email_text])
    # print(x_agenda._kids[casa_text]._kids[email_text]._balancelink)

    # THEN
    assert x_agenda._idearoot._all_party_credit == False
    assert x_agenda._idearoot._all_party_debt == False
    casa_idea = x_agenda._idearoot._kids[casa_text]
    assert casa_idea._all_party_credit == False
    assert casa_idea._all_party_debt == False
    assert casa_idea._kids[email_text]._all_party_credit == False
    assert casa_idea._kids[email_text]._all_party_debt == False
    assert casa_idea._kids[vacuum_text]._all_party_credit == True
    assert casa_idea._kids[vacuum_text]._all_party_debt == True
    week_idea = x_agenda._idearoot._kids[week_text]
    assert week_idea._all_party_credit == True
    assert week_idea._all_party_debt == True
    assert week_idea._kids[mon_text]._all_party_credit == True
    assert week_idea._kids[mon_text]._all_party_debt == True
    assert week_idea._kids[tue_text]._all_party_credit == True
    assert week_idea._kids[tue_text]._all_party_debt == True


def test_AgendaUnit_TreeTraverseSetsClearsBalanceLineestorsCorrectly():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.calc_agenda_metrics()
    # idea tree has no balancelinks
    assert x_agenda._idearoot._balancelines == {}
    x_agenda._idearoot._balancelines = {1: "testtest"}
    assert x_agenda._idearoot._balancelines != {}

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN
    assert not x_agenda._idearoot._balancelines

    # WHEN
    # test for level 1 and level n
    casa_text = "casa"
    casa_idea = x_agenda._idearoot._kids[casa_text]
    casa_idea._balancelines = {1: "testtest"}
    assert casa_idea._balancelines != {}
    x_agenda.calc_agenda_metrics()

    # THEN
    assert not x_agenda._idearoot._kids[casa_text]._balancelines


def test_AgendaUnit_calc_agenda_metrics_TreeTraverseSetsBalanceLineestorFromRootCorrectly():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.calc_agenda_metrics()
    # idea tree has no balancelinks
    assert x_agenda._idearoot._balancelines == {}
    sue_text = "sue"
    week_text = "weekdays"
    nation_text = "nation-state"
    sue_balancelink = balancelink_shop(group_id=sue_text)
    x_agenda.add_partyunit(party_id=sue_text)
    x_agenda._idearoot.set_balancelink(balancelink=sue_balancelink)
    # idea tree has balancelines
    assert x_agenda._idearoot._balanceheirs.get(sue_text) is None

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN
    assert x_agenda._idearoot._balanceheirs.get(sue_text) != None
    assert x_agenda._idearoot._balanceheirs.get(sue_text).group_id == sue_text
    assert x_agenda._idearoot._balancelines != {}
    root_idea = x_agenda.get_idea_obj(road=x_agenda._idearoot._label)
    sue_balanceline = x_agenda._idearoot._balancelines.get(sue_text)
    print(f"{sue_balanceline._agenda_credit=} {root_idea._agenda_importance=} ")
    print(f"  {sue_balanceline._agenda_debt=} {root_idea._agenda_importance=} ")
    sum_x = 0
    cat_road = x_agenda.make_l1_road("feed cat")
    cat_idea = x_agenda.get_idea_obj(cat_road)
    week_road = x_agenda.make_l1_road(week_text)
    week_idea = x_agenda.get_idea_obj(week_road)
    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    casa_idea = x_agenda.get_idea_obj(casa_road)
    nation_road = x_agenda.make_l1_road(nation_text)
    nation_idea = x_agenda.get_idea_obj(nation_road)
    sum_x = cat_idea._agenda_importance
    print(f"{cat_idea._agenda_importance=} {sum_x} ")
    sum_x += week_idea._agenda_importance
    print(f"{week_idea._agenda_importance=} {sum_x} ")
    sum_x += casa_idea._agenda_importance
    print(f"{casa_idea._agenda_importance=} {sum_x} ")
    sum_x += nation_idea._agenda_importance
    print(f"{nation_idea._agenda_importance=} {sum_x} ")
    assert sum_x >= 1.0
    assert sum_x < 1.00000000001

    # for kid_idea in root_idea._kids.values():
    #     sum_x += kid_idea._agenda_importance
    #     print(f"  {kid_idea._agenda_importance=} {sum_x=} {kid_idea.get_road()=}")
    assert round(sue_balanceline._agenda_credit, 15) == 1
    assert round(sue_balanceline._agenda_debt, 15) == 1
    x_balanceline = balanceline_shop(
        group_id=sue_text,
        _agenda_credit=0.9999999999999998,
        _agenda_debt=0.9999999999999998,
    )
    assert x_agenda._idearoot._balancelines == {x_balanceline.group_id: x_balanceline}


def test_AgendaUnit_calc_agenda_metrics_TreeTraverseSetsBalanceLineestorFromNonRootCorrectly():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.calc_agenda_metrics()
    # idea tree has no balancelinks
    sue_text = "sue"
    assert x_agenda._idearoot._balancelines == {}
    x_agenda.add_partyunit(party_id=sue_text)
    x_balancelink = balancelink_shop(group_id=sue_text)
    casa_text = "casa"
    email_text = "email"
    x_agenda._idearoot._kids[casa_text].set_balancelink(balancelink=x_balancelink)

    # WHEN
    # idea tree has balancelinks
    x_agenda.calc_agenda_metrics()

    # THEN
    assert x_agenda._idearoot._balancelines != {}
    x_balanceline = balanceline_shop(
        group_id=sue_text,
        _agenda_credit=0.23076923076923078,
        _agenda_debt=0.23076923076923078,
    )
    assert x_agenda._idearoot._balancelines == {x_balanceline.group_id: x_balanceline}
    assert x_agenda._idearoot._kids[casa_text]._balancelines != {}
    assert x_agenda._idearoot._kids[casa_text]._balancelines == {
        x_balanceline.group_id: x_balanceline
    }


def test_agenda4party_Exists():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    email_text = "email"
    casa_text = "casa"
    vacuum_text = "vacuum"
    sue_text = "sue"
    casa_road = x_agenda.make_l1_road(casa_text)
    email_idea = ideaunit_shop(_label=email_text, pledge=True)
    x_agenda.add_idea(email_idea, parent_road=casa_road)
    vacuum_idea = ideaunit_shop(_label=vacuum_text, pledge=True)
    x_agenda.add_idea(vacuum_idea, parent_road=casa_road)

    sue_party_id = PartyID(sue_text)
    x_agenda.add_partyunit(party_id=sue_party_id)
    x_balancelink = balancelink_shop(group_id=sue_party_id)
    yrx = x_agenda._idearoot
    yrx._kids[casa_text]._kids[email_text].set_balancelink(balancelink=x_balancelink)

    # WHEN
    sue_agenda4party = x_agenda.get_agenda4party(beliefs=None, party_id=sue_party_id)

    # THEN
    assert sue_agenda4party
    assert str(type(sue_agenda4party)).find(".agenda.AgendaUnit'>")
    assert sue_agenda4party._owner_id == sue_party_id


def test_agenda4party_hasCorrectLevel1StructureNoGrouplessAncestors():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    email_text = "email"
    casa_text = "casa"
    vacuum_text = "vacuum"
    sue_text = "sue"
    week_text = "weekdays"
    feed_text = "feed cat"
    casa_road = x_agenda.make_l1_road(casa_text)
    email_idea = ideaunit_shop(_label=email_text, pledge=True)
    x_agenda.add_idea(email_idea, parent_road=casa_road)
    vacuum_idea = ideaunit_shop(_label=vacuum_text, pledge=True)
    x_agenda.add_idea(vacuum_idea, parent_road=casa_road)

    billy_party_id = PartyID("billy")
    x_agenda.add_partyunit(party_id=billy_party_id)
    billy_bl = balancelink_shop(group_id=billy_party_id)
    yrx = x_agenda._idearoot
    yrx._kids[week_text].set_balancelink(balancelink=billy_bl)
    yrx._kids[feed_text].set_balancelink(balancelink=billy_bl)
    nation_text = "nation-state"
    yrx._kids[nation_text].set_balancelink(balancelink=billy_bl)

    sue_party_id = PartyID(sue_text)
    x_agenda.add_partyunit(party_id=sue_party_id)
    sue_bl = balancelink_shop(group_id=sue_party_id)
    yrx._kids[casa_text]._kids[email_text].set_balancelink(balancelink=sue_bl)

    # WHEN
    sue_agenda4party = x_agenda.get_agenda4party(sue_party_id, beliefs=None)

    # THEN
    assert len(sue_agenda4party._idearoot._kids) > 0
    print(f"{len(sue_agenda4party._idearoot._kids)=}")

    casa_idea = sue_agenda4party.get_idea_obj(casa_road)
    type_check_IdeaUnit = str(type(casa_idea)).find(".idea.IdeaUnit'>")
    print(f"{type_check_IdeaUnit=}")
    type_check_IdeaUnit = str(type(casa_idea)).find(".idea.IdeaUnit'>")
    print(f"{type_check_IdeaUnit=}")
    assert str(type(casa_idea)).find(".idea.IdeaUnit'>") > 0

    assert sue_agenda4party._idearoot._kids.get(feed_text) is None
    assert sue_agenda4party._idearoot._agenda_importance == 1
    assert casa_idea._agenda_importance == yrx._kids[casa_text]._agenda_importance
    __other__road = sue_agenda4party.make_l1_road("__other__")
    assert sue_agenda4party.get_idea_obj(__other__road) != None

    y4a_others = sue_agenda4party.get_idea_obj(__other__road)
    others_agenda_importance = yrx._kids[week_text]._agenda_importance
    others_agenda_importance += yrx._kids[feed_text]._agenda_importance
    others_agenda_importance += yrx._kids[nation_text]._agenda_importance
    print(f"{others_agenda_importance=}")
    assert round(y4a_others._agenda_importance, 15) == round(
        others_agenda_importance, 15
    )


def test_AgendaUnit_get_orderd_node_list_ReturnsCorrectObj():
    # GIVEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    week_text = "weekdays"
    assert x_agenda.get_idea_tree_ordered_road_list()

    # WHEN
    ordered_node_list = x_agenda.get_idea_tree_ordered_road_list()
    # for node in ordered_node_list:
    #     print(f"{node=}")
    # assert 1 == 2

    # THEN
    assert len(ordered_node_list) == 17
    x_1st_road_in_ordered_list = x_agenda.get_idea_tree_ordered_road_list()[0]
    assert x_1st_road_in_ordered_list == x_agenda._real_id
    x_8th_road_in_ordered_list = x_agenda.get_idea_tree_ordered_road_list()[9]
    assert x_8th_road_in_ordered_list == x_agenda.make_l1_road(week_text)

    # WHEN
    y_agenda = agendaunit_shop()

    # THEN
    y_1st_road_in_ordered_list = y_agenda.get_idea_tree_ordered_road_list()[0]
    assert y_1st_road_in_ordered_list == x_agenda._real_id


def test_AgendaUnit_get_orderd_node_list_CorrectlyFiltersRangedIdeaRoadUnits():
    # GIVEN
    tim_agenda = agendaunit_shop("Tim")

    # WHEN
    time = "timeline"
    tim_agenda.add_l1_idea(ideaunit_shop(_label=time, _begin=0, _close=700))
    t_road = tim_agenda.make_l1_road(time)
    week = "weeks"
    tim_agenda.add_idea(ideaunit_shop(_label=week, _denom=7), parent_road=t_road)

    # THEN
    assert len(tim_agenda.get_idea_tree_ordered_road_list()) == 3
    assert (
        len(tim_agenda.get_idea_tree_ordered_road_list(no_range_descendants=True)) == 2
    )


def test_AgendaUnit_get_heir_road_list_returnsCorrectList():
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


def test_AgendaUnit_idea_exists_ReturnsCorrectBool():
    # GIVEN
    sue_agenda = example_agendas_get_agenda_with_4_levels()
    sue_agenda.calc_agenda_metrics()
    cat_road = sue_agenda.make_l1_road("feed cat")
    week_road = sue_agenda.make_l1_road("weekdays")
    casa_road = sue_agenda.make_l1_road("casa")
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
    assert sue_agenda.idea_exists(root_label())
    assert sue_agenda.idea_exists(cat_road)
    assert sue_agenda.idea_exists(week_road)
    assert sue_agenda.idea_exists(casa_road)
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


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econs_justified_WhenAgendaUnitEmpty():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    assert sue_agenda._econs_justified == False

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._econs_justified


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econs_justified_WhenThereAreNotAny():
    # GIVEN
    sue_agenda = example_agendas_get_agenda_with_4_levels()
    assert sue_agenda._econs_justified == False

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._econs_justified


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econs_justified_WhenSingleIdeaUnit_healerhold_any_group_id_exists_IsTrue():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    sue_agenda.add_l1_idea(ideaunit_shop("Texas", _healerhold=healerhold_shop({"Yao"})))
    assert sue_agenda._econs_justified == False

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._econs_justified == False


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econs_justified_WhenSingleProblemAndEcon():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    yao_text = "Yao"
    sue_agenda.add_partyunit(yao_text)
    yao_healerhold = healerhold_shop({yao_text})
    sue_agenda.add_l1_idea(
        ideaunit_shop("Texas", _healerhold=yao_healerhold, _problem_bool=True)
    )
    assert sue_agenda._econs_justified == False

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._econs_justified


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econs_justified_WhenEconIsLevelAboveProblem():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    yao_text = "Yao"
    sue_agenda.add_partyunit(yao_text)
    yao_healerhold = healerhold_shop({yao_text})

    texas_text = "Texas"
    texas_road = sue_agenda.make_l1_road(texas_text)
    sue_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    ep_text = "El Paso"
    sue_agenda.add_idea(ideaunit_shop(ep_text, _healerhold=yao_healerhold), texas_road)
    assert sue_agenda._econs_justified == False

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._econs_justified


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econs_justified_WhenEconIsLevelBelowProblem():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    texas_text = "Texas"
    texas_road = sue_agenda.make_l1_road(texas_text)
    yao_healerhold = healerhold_shop({"Yao"})
    sue_agenda.add_l1_idea(ideaunit_shop(texas_text, _healerhold=yao_healerhold))
    sue_agenda.add_idea(ideaunit_shop("El Paso", _problem_bool=True), texas_road)
    assert sue_agenda._econs_justified == False

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._econs_justified == False


def test_AgendaUnit_calc_agenda_metrics_CorrectlyRaisesErrorWhenEconIsLevelBelowProblem():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    texas_text = "Texas"
    texas_road = sue_agenda.make_l1_road(texas_text)
    yao_healerhold = healerhold_shop({"Yao"})
    texas_idea = ideaunit_shop(texas_text, _healerhold=yao_healerhold)
    sue_agenda.add_l1_idea(texas_idea)
    elpaso_idea = ideaunit_shop("El Paso", _problem_bool=True)
    sue_agenda.add_idea(elpaso_idea, texas_road)
    assert sue_agenda._econs_justified == False

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.calc_agenda_metrics(econ_exceptions=True)
    assert (
        str(excinfo.value)
        == f"IdeaUnit '{elpaso_idea.get_road()}' cannot sponsor ancestor econs."
    )


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econs_justified_WhenTwoEconsAreOneTheSameLine():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    yao_healerhold = healerhold_shop({"Yao"})
    texas_text = "Texas"
    texas_road = sue_agenda.make_l1_road(texas_text)
    texas_idea = ideaunit_shop(
        texas_text, _healerhold=yao_healerhold, _problem_bool=True
    )
    sue_agenda.add_l1_idea(texas_idea)
    elpaso_idea = ideaunit_shop(
        "El Paso", _healerhold=yao_healerhold, _problem_bool=True
    )
    sue_agenda.add_idea(elpaso_idea, texas_road)
    assert sue_agenda._econs_justified == False

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._econs_justified == False


def test_AgendaUnit_get_idea_dict_RaisesErrorWhen_econs_justified_IsFalse():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    yao_healerhold = healerhold_shop({"Yao"})
    texas_text = "Texas"
    texas_road = sue_agenda.make_l1_road(texas_text)
    texas_idea = ideaunit_shop(
        texas_text, _healerhold=yao_healerhold, _problem_bool=True
    )
    sue_agenda.add_l1_idea(texas_idea)
    elpaso_idea = ideaunit_shop(
        "El Paso", _healerhold=yao_healerhold, _problem_bool=True
    )
    sue_agenda.add_idea(elpaso_idea, texas_road)
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._econs_justified == False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_agenda.get_idea_dict(problem=True)
    assert (
        str(excinfo.value)
        == f"Cannot return problem set because _econs_justified={sue_agenda._econs_justified}."
    )


def test_AgendaUnit_get_idea_dict_ReturnsCorrectObjWhenSingle():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    texas_text = "Texas"
    sue_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    casa_text = "casa"
    sue_agenda.add_l1_idea(ideaunit_shop(casa_text))

    # WHEN
    problems_dict = sue_agenda.get_idea_dict(problem=True)

    # THEN
    assert sue_agenda._econs_justified
    texas_road = sue_agenda.make_l1_road(texas_text)
    texas_idea = sue_agenda.get_idea_obj(texas_road)
    assert len(problems_dict) == 1
    assert problems_dict == {texas_road: texas_idea}
