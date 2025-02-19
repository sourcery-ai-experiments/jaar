from src._road.road import (
    get_default_world_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src.agenda.healer import healerhold_shop
from src.agenda.group import GroupID, balancelink_shop, balanceheir_shop
from src.agenda.reason_idea import (
    reasonunit_shop,
    reasonheir_shop,
    beliefunit_shop,
    premiseunit_shop,
)
from src.agenda.reason_assign import assignedunit_shop, assigned_heir_shop
from src.agenda.origin import originunit_shop
from src.agenda.idea import IdeaUnit, ideaunit_shop, get_obj_from_idea_dict
from pytest import raises as pytest_raises


def test_IdeaUnit_exists():
    x_ideaunit = IdeaUnit()
    assert x_ideaunit
    assert x_ideaunit._kids is None
    assert x_ideaunit._weight is None
    assert x_ideaunit._label is None
    assert x_ideaunit._uid is None
    assert x_ideaunit._all_party_credit is None
    assert x_ideaunit._all_party_debt is None
    assert x_ideaunit._begin is None
    assert x_ideaunit._close is None
    assert x_ideaunit._addin is None
    assert x_ideaunit._numor is None
    assert x_ideaunit._denom is None
    assert x_ideaunit._reest is None
    assert x_ideaunit._numeric_road is None
    assert x_ideaunit._range_source_road is None
    assert x_ideaunit.promise is None
    assert x_ideaunit._problem_bool is None
    assert x_ideaunit._descendant_promise_count is None
    assert x_ideaunit._balancelines is None
    assert x_ideaunit._balanceheirs is None
    assert x_ideaunit._is_expanded is None
    assert x_ideaunit._beliefheirs is None
    assert x_ideaunit._beliefunits is None
    assert x_ideaunit._meld_strategy is None
    assert x_ideaunit._healerhold is None
    assert x_ideaunit._level is None
    assert x_ideaunit._kids_total_weight is None
    assert x_ideaunit._active_hx is None
    assert x_ideaunit._agenda_importance is None
    assert x_ideaunit._agenda_fund_onset is None
    assert x_ideaunit._agenda_fund_cease is None
    assert x_ideaunit._reasonunits is None
    assert x_ideaunit._reasonheirs is None
    assert x_ideaunit._assignedunit is None
    assert x_ideaunit._assignedheir is None
    assert x_ideaunit._originunit is None
    assert x_ideaunit._road_delimiter is None
    assert x_ideaunit._root is None
    assert x_ideaunit._agenda_world_id is None
    assert x_ideaunit._healerhold_importance is None


def test_ideaunit_shop_NoParametersReturnsCorrectObj():
    # GIVEN / WHEN
    x_ideaunit = ideaunit_shop()

    # THEN
    assert x_ideaunit
    assert x_ideaunit._kids == {}
    assert x_ideaunit._weight >= 1
    assert x_ideaunit._label is None
    assert x_ideaunit._uid is None
    assert x_ideaunit._all_party_credit is None
    assert x_ideaunit._all_party_debt is None
    assert x_ideaunit._begin is None
    assert x_ideaunit._close is None
    assert x_ideaunit._addin is None
    assert x_ideaunit._numor is None
    assert x_ideaunit._denom is None
    assert x_ideaunit._reest is None
    assert x_ideaunit._numeric_road is None
    assert x_ideaunit._range_source_road is None
    assert x_ideaunit.promise is False
    assert x_ideaunit._problem_bool is False
    assert x_ideaunit._descendant_promise_count is None
    assert x_ideaunit._balancelines == {}
    assert x_ideaunit._balancelinks == {}
    assert x_ideaunit._balanceheirs == {}
    assert x_ideaunit._is_expanded == True
    assert x_ideaunit._beliefheirs == {}
    assert x_ideaunit._beliefunits == {}
    assert x_ideaunit._meld_strategy == "default"
    assert x_ideaunit._healerhold == healerhold_shop()
    assert x_ideaunit._level is None
    assert x_ideaunit._kids_total_weight == 0
    assert x_ideaunit._active_hx == {}
    assert x_ideaunit._agenda_importance is None
    assert x_ideaunit._agenda_fund_onset is None
    assert x_ideaunit._agenda_fund_cease is None
    assert x_ideaunit._reasonunits == {}
    assert x_ideaunit._reasonheirs == {}
    assert x_ideaunit._assignedunit == assignedunit_shop()
    assert x_ideaunit._assignedheir is None
    assert x_ideaunit._originunit == originunit_shop()
    assert x_ideaunit._road_delimiter == default_road_delimiter_if_none()
    assert x_ideaunit._root == False
    assert x_ideaunit._agenda_world_id == root_label()
    assert x_ideaunit._healerhold_importance == 0


def test_ideaunit_shop_NonNoneParametersReturnsCorrectObj():
    # GIVEN
    x_healerhold = healerhold_shop({"Sue", "Yao"})
    x_problem_bool = True

    # WHEN
    x_ideaunit = ideaunit_shop(_healerhold=x_healerhold, _problem_bool=x_problem_bool)

    # THEN
    assert x_ideaunit._healerhold == x_healerhold
    assert x_ideaunit._problem_bool == x_problem_bool


def test_IdeaUnit_get_obj_key_ReturnsCorrectObj():
    # GIVEN
    round_text = "round_things"
    round_road = create_road(root_label(), round_text)
    ball_text = "ball"

    # WHEN
    ball_idea = ideaunit_shop(_label=ball_text, _parent_road=round_road)

    # THEN
    assert ball_idea.get_obj_key() == ball_text


def test_IdeaUnit_get_road_ReturnsCorrectObj():
    # GIVEN
    round_text = "round_things"
    slash_text = "/"
    round_road = create_road(root_label(), round_text, delimiter=slash_text)
    ball_text = "ball"

    # WHEN
    ball_idea = ideaunit_shop(
        ball_text, _parent_road=round_road, _road_delimiter=slash_text
    )

    # THEN
    ball_road = create_road(round_road, ball_text, delimiter=slash_text)
    assert ball_idea.get_road() == ball_road


def test_IdeaUnit_set_parent_road_ReturnsCorrectObj():
    # GIVEN
    round_text = "round_things"
    slash_text = "/"
    round_road = create_road(root_label(), round_text, delimiter=slash_text)
    ball_text = "ball"
    ball_idea = ideaunit_shop(
        ball_text, _parent_road=round_road, _road_delimiter=slash_text
    )
    assert ball_idea._parent_road == round_road

    # WHEN
    sports_road = create_road(root_label(), "sports", delimiter=slash_text)
    ball_idea.set_parent_road(parent_road=sports_road)

    # THEN
    assert ball_idea._parent_road == sports_road


def test_IdeaUnit_balancelinks_exist():
    # GIVEN
    biker_creditor_weight = 12
    biker_debtor_weight = 15
    biker_link = balancelink_shop(
        group_id=GroupID("bikers2"),
        creditor_weight=biker_creditor_weight,
        debtor_weight=biker_debtor_weight,
    )

    swimmer_group_id = GroupID("swimmers")
    swimmer_creditor_weight = 29
    swimmer_debtor_weight = 32
    swimmer_link = balancelink_shop(
        group_id=swimmer_group_id,
        creditor_weight=swimmer_creditor_weight,
        debtor_weight=swimmer_debtor_weight,
    )

    group_links = {swimmer_link.group_id: swimmer_link, biker_link.group_id: biker_link}

    # WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text, _balancelinks=group_links)

    # THEN
    assert sport_idea._balancelinks == group_links


def test_IdeaUnit_get_inherited_balanceheirs_weight_sum_SetsAttrCorrectly_WithValues():
    # GIVEN
    biker_creditor_weight = 12
    biker_debtor_weight = 15
    biker_text = "bikers2"
    biker_link = balanceheir_shop(
        group_id=GroupID(biker_text),
        creditor_weight=biker_creditor_weight,
        debtor_weight=biker_debtor_weight,
    )

    swimmer_text = "swimmers"
    swimmer_group_id = GroupID(swimmer_text)
    swimmer_creditor_weight = 29
    swimmer_debtor_weight = 32
    swimmer_link = balanceheir_shop(
        group_id=swimmer_group_id,
        creditor_weight=swimmer_creditor_weight,
        debtor_weight=swimmer_debtor_weight,
    )

    group_links = {swimmer_link.group_id: swimmer_link, biker_link.group_id: biker_link}

    # WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text, _balanceheirs=group_links)

    # THEN
    assert sport_idea.get_balanceheirs_creditor_weight_sum() != None
    assert sport_idea.get_balanceheirs_creditor_weight_sum() == 41
    assert sport_idea.get_balanceheirs_debtor_weight_sum() != None
    assert sport_idea.get_balanceheirs_debtor_weight_sum() == 47

    assert len(sport_idea._balanceheirs) == 2

    swimmer_balanceheir = sport_idea._balanceheirs.get(swimmer_text)
    assert swimmer_balanceheir._agenda_credit is None
    assert swimmer_balanceheir._agenda_debt is None
    biker_balanceheir = sport_idea._balanceheirs.get(biker_text)
    assert biker_balanceheir._agenda_credit is None
    assert biker_balanceheir._agenda_debt is None

    # WHEN
    sport_idea._agenda_importance = 0.25
    sport_idea.set_balanceheirs_agenda_credit_debt()

    # THEN
    print(f"{len(sport_idea._balanceheirs)=}")
    swimmer_balanceheir = sport_idea._balanceheirs.get(swimmer_text)
    assert swimmer_balanceheir._agenda_credit != None
    assert swimmer_balanceheir._agenda_debt != None
    biker_balanceheir = sport_idea._balanceheirs.get(biker_text)
    assert biker_balanceheir._agenda_credit != None
    assert biker_balanceheir._agenda_debt != None


def test_IdeaUnit_get_balancelinks_weight_sum_ReturnsCorrectObj_NoValues():
    # GIVEN /WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text)
    assert sport_idea.get_balanceheirs_creditor_weight_sum() != None
    assert sport_idea.get_balanceheirs_debtor_weight_sum() != None

    # WHEN / THEN
    # does not crash with empty set
    sport_idea.set_balanceheirs_agenda_credit_debt()


def test_IdeaUnit_set_reasonheirsCorrectlySourcesFromOutside():
    # GIVEN
    ball_text = "ball"
    ball_road = create_road(ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    ball_idea = ideaunit_shop(_label=ball_text)
    run_premise = premiseunit_shop(need=run_road, open=0, nigh=7)
    run_premises = {run_premise.need: run_premise}
    reasonheir = reasonheir_shop(run_road, premises=run_premises)
    reasonheirs = {reasonheir.base: reasonheir}
    assert ball_idea._reasonheirs == {}

    # WHEN
    ball_idea.set_reasonheirs(reasonheirs=reasonheirs, agenda_idea_dict={})

    # THEN
    assert ball_idea._reasonheirs == reasonheirs
    assert id(ball_idea._reasonheirs) != id(reasonheirs)


def test_IdeaUnit_set_reasonheirsCorrectlySourcesFromSelf():
    # GIVEN
    ball_text = "ball"
    ball_road = create_road(ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    run_premise = premiseunit_shop(need=run_road, open=0, nigh=7)
    run_premises = {run_premise.need: run_premise}
    run_reasonunit = reasonunit_shop(base=run_road, premises=run_premises)
    run_reasonunits = {run_reasonunit.base: run_reasonunit}
    ball_idea = ideaunit_shop(_label=ball_text, _reasonunits=run_reasonunits)
    assert ball_idea._reasonunits != {}

    # WHEN
    ball_idea.set_reasonheirs(reasonheirs=None, agenda_idea_dict={})

    # THEN
    reasonheir = reasonheir_shop(run_road, premises=run_premises)
    reasonheirs = {reasonheir.base: reasonheir}
    assert ball_idea._reasonheirs == reasonheirs


def test_IdeaUnit_clear_descendant_promise_count_ClearsCorrectly():
    # GIVEN
    ball_text = "ball"
    ball_idea = ideaunit_shop(_label=ball_text, _descendant_promise_count=55)
    assert ball_idea._descendant_promise_count == 55

    # WHEN
    ball_idea.clear_descendant_promise_count()

    # THEN
    assert ball_idea._descendant_promise_count is None


def test_IdeaUnit_add_to_descendant_promise_count_CorrectlyAdds():
    # GIVEN
    ball_text = "ball"
    ball_idea = ideaunit_shop(_label=ball_text, _descendant_promise_count=55)
    ball_idea.clear_descendant_promise_count()
    assert ball_idea._descendant_promise_count is None

    # WHEN
    ball_idea.add_to_descendant_promise_count(44)

    # THEN
    assert ball_idea._descendant_promise_count == 44

    # WHEN
    ball_idea.add_to_descendant_promise_count(33)

    # THEN
    assert ball_idea._descendant_promise_count == 77


def test_IdeaUnit_clear_all_party_credit_debt_ClearsCorrectly():
    # GIVEN
    ball_text = "ball"
    ball_idea = ideaunit_shop(
        _label=ball_text, _all_party_credit=55, _all_party_debt=33
    )
    assert ball_idea._all_party_credit == 55
    assert ball_idea._all_party_debt == 33

    # WHEN
    ball_idea.clear_all_party_credit_debt()

    # THEN
    assert ball_idea._all_party_credit is None
    assert ball_idea._all_party_debt is None


def test_get_kids_in_range_GetsCorrectIdeas():
    # GIVEN
    mon366_text = "366months"
    mon366_idea = ideaunit_shop(_label=mon366_text, _begin=0, _close=366)
    jan_text = "Jan"
    feb29_text = "Feb29"
    mar_text = "Mar"
    mon366_idea.add_kid(idea_kid=ideaunit_shop(_label=jan_text, _begin=0, _close=31))
    mon366_idea.add_kid(idea_kid=ideaunit_shop(_label=feb29_text, _begin=31, _close=60))
    mon366_idea.add_kid(idea_kid=ideaunit_shop(_label=mar_text, _begin=31, _close=91))

    # WHEN / THEN
    assert len(mon366_idea.get_kids_in_range(begin=100, close=120)) == 0
    assert len(mon366_idea.get_kids_in_range(begin=0, close=31)) == 1
    assert len(mon366_idea.get_kids_in_range(begin=5, close=5)) == 1
    assert len(mon366_idea.get_kids_in_range(begin=0, close=61)) == 3
    assert mon366_idea.get_kids_in_range(begin=31, close=31)[0]._label == feb29_text


def test_get_obj_from_idea_dict_ReturnsCorrectObj():
    # GIVEN
    field_text = "_is_expanded"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_text: True}, field_text)
    assert get_obj_from_idea_dict({}, field_text)
    assert get_obj_from_idea_dict({field_text: False}, field_text) == False

    # GIVEN
    field_text = "promise"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_text: True}, field_text)
    assert get_obj_from_idea_dict({}, field_text) == False
    assert get_obj_from_idea_dict({field_text: False}, field_text) == False

    # GIVEN
    field_text = "_problem_bool"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_text: True}, field_text)
    assert get_obj_from_idea_dict({}, field_text) == False
    assert get_obj_from_idea_dict({field_text: False}, field_text) == False

    # GIVEN
    field_text = "_kids"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_text: {}}, field_text) == {}
    assert get_obj_from_idea_dict({}, field_text) == {}


def test_get_obj_from_idea_dict_ReturnsCorrect_HealerHold():
    # GIVEN
    # WHEN / THEN
    healerhold_key = "_healerhold"
    assert get_obj_from_idea_dict({}, healerhold_key) == healerhold_shop()

    # WHEN
    sue_text = "Sue"
    jim_text = "Jim"
    healerhold_dict = {"healerhold_group_ids": [sue_text, jim_text]}
    ideaunit_dict = {healerhold_key: healerhold_dict}

    # THEN
    static_healerhold = healerhold_shop()
    static_healerhold.set_group_id(x_group_id=sue_text)
    static_healerhold.set_group_id(x_group_id=jim_text)
    assert get_obj_from_idea_dict(ideaunit_dict, healerhold_key) != None
    assert get_obj_from_idea_dict(ideaunit_dict, healerhold_key) == static_healerhold


def test_IdeaUnit_get_dict_ReturnsCorrectCompleteDict():
    # GIVEN
    week_text = "weekdays"
    week_road = create_road(root_label(), week_text)
    wed_text = "Wednesday"
    wed_road = create_road(week_road, wed_text)
    states_text = "nation-state"
    states_road = create_road(root_label(), states_text)
    usa_text = "USA"
    usa_road = create_road(states_road, usa_text)

    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = True
    usa_premise = premiseunit_shop(need=usa_road)
    usa_premise._status = False

    x1_reasonunits = {
        week_road: reasonunit_shop(
            base=week_road, premises={wed_premise.need: wed_premise}
        ),
        states_road: reasonunit_shop(
            base=states_road, premises={usa_premise.need: usa_premise}
        ),
    }
    x1_reasonheirs = {
        week_road: reasonheir_shop(
            base=week_road, premises={wed_premise.need: wed_premise}, _status=True
        ),
        states_road: reasonheir_shop(
            base=states_road, premises={usa_premise.need: usa_premise}, _status=False
        ),
    }
    biker_group_id = GroupID("bikers")
    biker_creditor_weight = 3.0
    biker_debtor_weight = 7.0
    biker_link = balancelink_shop(
        biker_group_id, biker_creditor_weight, biker_debtor_weight
    )
    flyer_group_id = GroupID("flyers")
    flyer_creditor_weight = 6.0
    flyer_debtor_weight = 9.0
    flyer_link = balancelink_shop(
        group_id=flyer_group_id,
        creditor_weight=flyer_creditor_weight,
        debtor_weight=flyer_debtor_weight,
    )
    biker_and_flyer_balancelinks = {
        biker_link.group_id: biker_link,
        flyer_link.group_id: flyer_link,
    }
    biker_get_dict = {
        "group_id": biker_link.group_id,
        "creditor_weight": biker_link.creditor_weight,
        "debtor_weight": biker_link.debtor_weight,
    }
    flyer_get_dict = {
        "group_id": flyer_link.group_id,
        "creditor_weight": flyer_link.creditor_weight,
        "debtor_weight": flyer_link.debtor_weight,
    }
    x1_balancelinks = {biker_group_id: biker_get_dict, flyer_group_id: flyer_get_dict}
    sue_text = "Sue"
    yao_text = "Yao"
    sue_assignedunit = assignedunit_shop({sue_text: -1, yao_text: -1})
    yao_healerhold = healerhold_shop({yao_text})
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text)
    x_problem_bool = True
    gig_idea = ideaunit_shop(
        _parent_road=gig_road,
        _kids=None,
        _balancelinks=biker_and_flyer_balancelinks,
        _weight=30,
        _label=gig_text,
        _level=1,
        _reasonunits=x1_reasonunits,
        _reasonheirs=x1_reasonheirs,
        _assignedunit=sue_assignedunit,
        _healerhold=yao_healerhold,
        _active=True,
        _range_source_road="test123",
        promise=True,
        _problem_bool=x_problem_bool,
    )
    beliefunit_x = beliefunit_shop(base=week_road, pick=week_road, open=5, nigh=59)
    gig_idea.set_beliefunit(beliefunit=beliefunit_x)
    gig_idea._originunit.set_originlink(party_id="Ray", weight=None)
    gig_idea._originunit.set_originlink(party_id="Lei", weight=4)
    x_begin = 11
    x_close = 12
    x_addin = 13
    x_denom = 14
    x_numor = 15
    x_reest = 16
    gig_idea._begin = x_begin
    gig_idea._close = x_close
    gig_idea._addin = x_addin
    gig_idea._denom = x_denom
    gig_idea._numor = x_numor
    gig_idea._reest = x_reest
    gig_idea._uid = 17
    gig_idea.add_kid(ideaunit_shop("paper"))

    # WHEN
    gig_dict = gig_idea.get_dict()

    # THEN
    assert gig_dict != None
    assert len(gig_dict["_kids"]) == 1
    assert gig_dict["_kids"] == gig_idea.get_kids_dict()
    assert gig_dict["_reasonunits"] == gig_idea.get_reasonunits_dict()
    assert gig_dict["_balancelinks"] == gig_idea.get_balancelinks_dict()
    assert gig_dict["_balancelinks"] == x1_balancelinks
    assert gig_dict["_assignedunit"] == sue_assignedunit.get_dict()
    assert gig_dict["_healerhold"] == yao_healerhold.get_dict()
    assert gig_dict["_originunit"] == gig_idea.get_originunit_dict()
    assert gig_dict["_weight"] == gig_idea._weight
    assert gig_dict["_label"] == gig_idea._label
    assert gig_dict["_uid"] == gig_idea._uid
    assert gig_dict["_begin"] == gig_idea._begin
    assert gig_dict["_close"] == gig_idea._close
    assert gig_dict["_numor"] == gig_idea._numor
    assert gig_dict["_denom"] == gig_idea._denom
    assert gig_dict["_reest"] == gig_idea._reest
    assert gig_dict["_range_source_road"] == gig_idea._range_source_road
    assert gig_dict["promise"] == gig_idea.promise
    assert gig_dict["_problem_bool"] == gig_idea._problem_bool
    assert gig_dict["_problem_bool"] == x_problem_bool
    assert gig_idea._is_expanded
    assert gig_dict.get("_is_expanded") is None
    assert len(gig_dict["_beliefunits"]) == len(gig_idea.get_beliefunits_dict())
    assert gig_idea._meld_strategy == "default"
    assert gig_dict.get("_meld_strategy") is None


def test_IdeaUnit_get_dict_ReturnsCorrectDictWithoutEmptyAttributes():
    # GIVEN
    gig_idea = ideaunit_shop()

    # WHEN
    gig_dict = gig_idea.get_dict()

    # THEN
    assert gig_dict != None
    assert gig_dict == {"_weight": 1}


def test_IdeaUnit_get_dict_ReturnsDictWith_attrs_CorrectlySetTrue():
    # GIVEN
    gig_idea = ideaunit_shop()
    gig_idea._is_expanded = False
    gig_idea.promise = True
    ignore_text = "ignore"
    gig_idea._meld_strategy = ignore_text

    a_text = "a"
    a_road = create_road(root_label(), a_text)
    gig_idea.set_beliefunit(beliefunit_shop(a_road, a_road))

    yao_text = "Yao"
    gig_idea.set_balancelink(balancelink_shop(yao_text))

    x_assignedunit = gig_idea._assignedunit
    x_assignedunit.set_suffgroup(group_id=yao_text)

    x_originunit = gig_idea._originunit
    x_originunit.set_originlink(yao_text, 1)

    rock_text = "Rock"
    gig_idea.add_kid(ideaunit_shop(rock_text))

    assert not gig_idea._is_expanded
    assert gig_idea.promise
    assert gig_idea._meld_strategy != "default"
    assert gig_idea._beliefunits != None
    assert gig_idea._balancelinks != None
    assert gig_idea._assignedunit != None
    assert gig_idea._originunit != None
    assert gig_idea._kids != {}

    # WHEN
    gig_dict = gig_idea.get_dict()

    # THEN
    assert gig_dict.get("_is_expanded") == False
    assert gig_dict.get("promise")
    assert gig_dict.get("_meld_strategy") == ignore_text
    assert gig_dict.get("_beliefunits") != None
    assert gig_dict.get("_balancelinks") != None
    assert gig_dict.get("_assignedunit") != None
    assert gig_dict.get("_originunit") != None
    assert gig_dict.get("_kids") != None


def test_IdeaUnit_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # GIVEN
    gig_idea = ideaunit_shop()
    assert gig_idea._is_expanded
    assert gig_idea.promise == False
    assert gig_idea._meld_strategy == "default"
    assert gig_idea._beliefunits == {}
    assert gig_idea._balancelinks == {}
    assert gig_idea._assignedunit == assignedunit_shop()
    assert gig_idea._healerhold == healerhold_shop()
    assert gig_idea._originunit == originunit_shop()
    assert gig_idea._kids == {}

    # WHEN
    gig_dict = gig_idea.get_dict()

    # THEN
    assert gig_dict.get("_is_expanded") is None
    assert gig_dict.get("promise") is None
    assert gig_dict.get("_meld_strategy") is None
    assert gig_dict.get("_beliefunits") is None
    assert gig_dict.get("_balancelinks") is None
    assert gig_dict.get("_assignedunit") is None
    assert gig_dict.get("_healerhold") is None
    assert gig_dict.get("_originunit") is None
    assert gig_dict.get("_kids") is None


def test_IdeaUnit_vaild_DenomCorrectInheritsBeginAndClose():
    # GIVEN
    gig_text = "gig"
    clean_text = "clean"
    # parent idea
    gig_idea = ideaunit_shop(_label=gig_text, _begin=22.0, _close=66.0)
    # kid idea
    clean_idea = ideaunit_shop(_label=clean_text, _numor=1, _denom=11.0, _reest=False)

    # WHEN
    gig_idea.add_kid(idea_kid=clean_idea)

    # THEN
    assert gig_idea._kids[clean_text]._begin == 2
    assert gig_idea._kids[clean_text]._close == 6
    kid_idea_expected = ideaunit_shop(
        clean_text, _numor=1, _denom=11.0, _reest=False, _begin=2, _close=6
    )
    assert gig_idea._kids[clean_text] == kid_idea_expected


def test_IdeaUnit_invaild_DenomThrowsError():
    # GIVEN
    gig_text = "gig"
    parent_idea = ideaunit_shop(_label=gig_text)
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
    clean_text = "clean"
    clean_road = create_road(casa_road, clean_text)
    print(f"{clean_road=}")
    kid_idea = ideaunit_shop(
        clean_text, _parent_road=casa_road, _numor=1, _denom=11.0, _reest=False
    )
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        parent_idea.add_kid(idea_kid=kid_idea)
    print(f"{str(excinfo.value)=}")
    assert (
        str(excinfo.value)
        == f"Idea {clean_road} cannot have numor,denom,reest if parent does not have begin/close range"
    )


def test_IdeaUnit_get_reasonunit_ReturnsCorrectObj():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    instrument_text = "instrument"
    clean_idea.set_reasonunit(reasonunit_shop(base=instrument_text))

    # WHEN
    x_reasonunit = clean_idea.get_reasonunit(base=instrument_text)

    # THEN
    assert x_reasonunit != None
    assert x_reasonunit.base == instrument_text


def test_IdeaUnit_get_reasonheir_ReturnsCorrectObj():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    instrument_text = "instrument"
    reason_heir_x = reasonheir_shop(base=instrument_text)
    reason_heirs_x = {reason_heir_x.base: reason_heir_x}
    clean_idea.set_reasonheirs(reasonheirs=reason_heirs_x, agenda_idea_dict={})

    # WHEN
    reason_heir_z = clean_idea.get_reasonheir(base=instrument_text)

    # THEN
    assert reason_heir_z != None
    assert reason_heir_z.base == instrument_text


def test_IdeaUnit_get_reasonheir_ReturnsNone():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    instrument_text = "instrument"
    reason_heir_x = reasonheir_shop(instrument_text)
    reason_heirs_x = {reason_heir_x.base: reason_heir_x}
    clean_idea.set_reasonheirs(reasonheirs=reason_heirs_x, agenda_idea_dict={})

    # WHEN
    test6_text = "test6"
    reason_heir_test6 = clean_idea.get_reasonheir(base=test6_text)

    # THEN
    assert reason_heir_test6 is None


def test_IdeaUnit_set_active_SetsNullactive_hxToNonEmpty():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    assert clean_idea._active_hx == {}

    # WHEN
    clean_idea.set_active(tree_traverse_count=3)
    # THEN
    assert clean_idea._active_hx == {3: True}


def test_IdeaUnit_set_active_IfFullactive_hxResetToTrue():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    clean_idea._active_hx = {0: True, 4: False}
    assert clean_idea._active_hx != {0: True}
    # WHEN
    clean_idea.set_active(tree_traverse_count=0)
    # THEN
    assert clean_idea._active_hx == {0: True}


# def test_IdeaUnit_set_active_IfFullactive_hxResetToFalse():
#     # GIVEN
# clean_text = "clean"
# clean_idea = ideaunit_shop(_label=clean_text)
#     clean_idea.set_reason_premise(
#         base="testing1,sec",
#         premise="testing1,sec,next",
#         open=None,
#         nigh=None,
#         divisor=None,
#     )
#     clean_idea._active_hx = {0: True, 4: False}
#     assert clean_idea._active_hx != {0: False}
#     # WHEN
#     clean_idea.set_active(tree_traverse_count=0)
#     # THEN
#     assert clean_idea._active_hx == {0: False}


def test_IdeaUnit_record_active_hx_CorrectlyRecordsHistorry():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    assert clean_idea._active_hx == {}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=0,
        prev_active=None,
        curr_active=True,
    )
    # THEN
    assert clean_idea._active_hx == {0: True}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=1,
        prev_active=True,
        curr_active=True,
    )
    # THEN
    assert clean_idea._active_hx == {0: True}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=2,
        prev_active=True,
        curr_active=False,
    )
    # THEN
    assert clean_idea._active_hx == {0: True, 2: False}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=3,
        prev_active=False,
        curr_active=False,
    )
    # THEN
    assert clean_idea._active_hx == {0: True, 2: False}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=4,
        prev_active=False,
        curr_active=True,
    )
    # THEN
    assert clean_idea._active_hx == {0: True, 2: False, 4: True}

    # WHEN
    clean_idea.record_active_hx(
        tree_traverse_count=0,
        prev_active=False,
        curr_active=False,
    )
    # THEN
    assert clean_idea._active_hx == {0: False}


def test_IdeaUnit_set_assignedunit_empty_if_null():
    # GIVEN
    run_text = "run"
    run_idea = ideaunit_shop(_label=run_text)
    run_idea._assignedunit = None
    assert run_idea._assignedunit is None

    # WHEN
    run_idea.set_assignedunit_empty_if_null()

    # THEN
    assert run_idea._assignedunit != None
    assert run_idea._assignedunit == assignedunit_shop()


def test_IdeaUnit_set_assignedheir_CorrectlySetsAttr():
    # GIVEN
    swim_text = "swimmers"
    sport_text = "sports"
    sport_idea = ideaunit_shop(_label=sport_text)
    sport_idea._assignedunit.set_suffgroup(group_id=swim_text)
    assert sport_idea._assignedheir is None

    # WHEN
    sport_idea.set_assignedheir(parent_assignheir=None, agenda_groups=None)

    # THEN
    assert sport_idea._assignedheir != None
    swim_assignedunit = assignedunit_shop()
    swim_assignedunit.set_suffgroup(group_id=swim_text)
    swim_assigned_heir = assigned_heir_shop()
    swim_assigned_heir.set_suffgroups(
        assignunit=swim_assignedunit, parent_assignheir=None, agenda_groups=None
    )
    assert sport_idea._assignedheir == swim_assigned_heir


def test_IdeaUnit_get_descendants_ReturnsNoRoadUnits():
    # GIVEN
    nation_text = "nation-state"
    nation_idea = ideaunit_shop(_label=nation_text, _parent_road=root_label())

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads_from_kids()

    # THEN
    assert nation_descendants == {}


def test_IdeaUnit_get_descendants_Returns3DescendantsRoadUnits():
    # GIVEN
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    usa_idea = ideaunit_shop(usa_text, _parent_road=nation_road)
    nation_idea.add_kid(idea_kid=usa_idea)

    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    texas_idea = ideaunit_shop(texas_text, _parent_road=usa_road)
    usa_idea.add_kid(idea_kid=texas_idea)

    iowa_text = "Iowa"
    iowa_road = create_road(usa_road, iowa_text)
    iowa_idea = ideaunit_shop(iowa_text, _parent_road=usa_road)
    usa_idea.add_kid(idea_kid=iowa_idea)

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads_from_kids()

    # THEN
    assert len(nation_descendants) == 3
    assert nation_descendants.get(usa_road) != None
    assert nation_descendants.get(texas_road) != None
    assert nation_descendants.get(iowa_road) != None


def test_IdeaUnit_get_descendants_ErrorRaisedIfInfiniteLoop():
    # GIVEN
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())
    nation_idea.add_kid(idea_kid=nation_idea)
    max_count = 1000

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        nation_idea.get_descendant_roads_from_kids()
    assert (
        str(excinfo.value)
        == f"Idea '{nation_idea.get_road()}' either has an infinite loop or more than {max_count} descendants."
    )


def test_IdeaUnit_clear_kids_CorrectlySetsAttr():
    # GIVEN
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())
    nation_idea.add_kid(ideaunit_shop("USA", _parent_road=nation_road))
    nation_idea.add_kid(ideaunit_shop("France", _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    nation_idea.clear_kids()

    # THEN
    assert len(nation_idea._kids) == 0


def test_IdeaUnit_get_kid_ReturnsCorrectObj():
    # GIVEN
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    nation_idea.add_kid(ideaunit_shop(usa_text, _parent_road=nation_road))

    france_text = "France"
    france_road = create_road(nation_road, france_text)
    nation_idea.add_kid(ideaunit_shop(france_text, _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    france_idea = nation_idea.get_kid(france_text)

    # THEN
    assert france_idea._label == france_text


def test_IdeaUnit_del_kid_CorrectChangesAttr():
    # GIVEN
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    nation_idea = ideaunit_shop(nation_text, _parent_road=root_label())

    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    nation_idea.add_kid(ideaunit_shop(usa_text, _parent_road=nation_road))

    france_text = "France"
    france_road = create_road(nation_road, france_text)
    nation_idea.add_kid(ideaunit_shop(france_text, _parent_road=nation_road))
    assert len(nation_idea._kids) == 2

    # WHEN
    nation_idea.del_kid(france_text)

    # THEN
    assert len(nation_idea._kids) == 1
