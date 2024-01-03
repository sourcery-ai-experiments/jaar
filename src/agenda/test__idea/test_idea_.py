from src.agenda.idea import IdeaUnit, ideaunit_shop, get_obj_from_idea_dict
from src.agenda.group import GroupBrand, balancelink_shop, balanceheir_shop
from src.agenda.required_idea import (
    requiredunit_shop,
    requiredheir_shop,
    acptfactunit_shop,
    sufffactunit_shop,
)
from src.agenda.required_assign import assigned_unit_shop, assigned_heir_shop
from src.agenda.origin import originunit_shop
from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
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
    assert x_ideaunit._acptfactheirs is None
    assert x_ideaunit._acptfactunits is None
    assert x_ideaunit._on_meld_weight_action is None
    assert x_ideaunit._level is None
    assert x_ideaunit._kids_total_weight is None
    assert x_ideaunit._active_status_hx is None
    assert x_ideaunit._agenda_importance is None
    assert x_ideaunit._agenda_coin_onset is None
    assert x_ideaunit._agenda_coin_cease is None
    assert x_ideaunit._requiredunits is None
    assert x_ideaunit._requiredheirs is None
    assert x_ideaunit._assignedunit is None
    assert x_ideaunit._assignedheir is None
    assert x_ideaunit._originunit is None
    assert x_ideaunit._road_delimiter is None
    assert x_ideaunit._root is None
    assert x_ideaunit._agenda_economy_id is None


def test_ideaunit_shop_ReturnsCorrectObj():
    x_ideaunit = ideaunit_shop()
    print(f"{x_ideaunit._active_status=}")
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
    assert x_ideaunit._acptfactheirs == {}
    assert x_ideaunit._acptfactunits == {}
    assert x_ideaunit._on_meld_weight_action == "default"
    assert x_ideaunit._level is None
    assert x_ideaunit._kids_total_weight == 0
    assert x_ideaunit._active_status_hx == {}
    assert x_ideaunit._agenda_importance is None
    assert x_ideaunit._agenda_coin_onset is None
    assert x_ideaunit._agenda_coin_cease is None
    assert x_ideaunit._requiredunits == {}
    assert x_ideaunit._requiredheirs == {}
    assert x_ideaunit._assignedunit == assigned_unit_shop()
    assert x_ideaunit._assignedheir is None
    assert x_ideaunit._originunit == originunit_shop()
    assert x_ideaunit._road_delimiter == default_road_delimiter_if_none()
    assert x_ideaunit._root == False
    assert x_ideaunit._agenda_economy_id == root_label()


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
        brand=GroupBrand("bikers2"),
        creditor_weight=biker_creditor_weight,
        debtor_weight=biker_debtor_weight,
    )

    swimmer_pid = GroupBrand("swimmers")
    swimmer_creditor_weight = 29
    swimmer_debtor_weight = 32
    swimmer_link = balancelink_shop(
        brand=swimmer_pid,
        creditor_weight=swimmer_creditor_weight,
        debtor_weight=swimmer_debtor_weight,
    )

    group_links = {swimmer_link.brand: swimmer_link, biker_link.brand: biker_link}

    # WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text, _balancelinks=group_links)

    # THEN
    assert sport_idea._balancelinks == group_links
    # assert group_link_x.weight == 1.0
    # group_link_x = balancelink_shop(brand=bikers_pid, weight=bikers_weight)
    # assert group_link_x.weight == 3.0


def test_IdeaUnit_get_inherited_balanceheirs_weight_sum_WorksCorrectlyWithValues():
    # GIVEN
    biker_creditor_weight = 12
    biker_debtor_weight = 15
    biker_text = "bikers2"
    biker_link = balanceheir_shop(
        brand=GroupBrand(biker_text),
        creditor_weight=biker_creditor_weight,
        debtor_weight=biker_debtor_weight,
    )

    swimmer_text = "swimmers"
    swimmer_pid = GroupBrand(swimmer_text)
    swimmer_creditor_weight = 29
    swimmer_debtor_weight = 32
    swimmer_link = balanceheir_shop(
        brand=swimmer_pid,
        creditor_weight=swimmer_creditor_weight,
        debtor_weight=swimmer_debtor_weight,
    )

    group_links = {swimmer_link.brand: swimmer_link, biker_link.brand: biker_link}

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


def test_IdeaUnit_get_balancelinks_weight_sum_WorksCorrectlyNoValues():
    # GIVEN /WHEN
    sport_text = "sport"
    sport_idea = ideaunit_shop(_label=sport_text)
    assert sport_idea.get_balanceheirs_creditor_weight_sum() != None
    assert sport_idea.get_balanceheirs_debtor_weight_sum() != None

    # WHEN / THEN
    # does not crash with empty set
    sport_idea.set_balanceheirs_agenda_credit_debt()


def test_IdeaUnit_set_requiredheirsCorrectlyTakesFromOutside():
    # GIVEN
    ball_text = "ball"
    ball_road = create_road(ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    ball_idea = ideaunit_shop(_label=ball_text)
    run_sufffact = sufffactunit_shop(need=run_road, open=0, nigh=7)
    run_sufffacts = {run_sufffact.need: run_sufffact}
    requiredheir = requiredheir_shop(run_road, sufffacts=run_sufffacts)
    requiredheirs = {requiredheir.base: requiredheir}
    assert ball_idea._requiredheirs == {}

    # WHEN
    ball_idea.set_requiredheirs(requiredheirs=requiredheirs, agenda_idea_dict={})

    # THEN
    assert ball_idea._requiredheirs == requiredheirs
    assert id(ball_idea._requiredheirs) != id(requiredheirs)


def test_IdeaUnit_set_requiredheirsCorrectlyTakesFromSelf():
    # GIVEN
    ball_text = "ball"
    ball_road = create_road(ball_text)
    run_text = "run"
    run_road = create_road(ball_road, run_text)
    run_sufffact = sufffactunit_shop(need=run_road, open=0, nigh=7)
    run_sufffacts = {run_sufffact.need: run_sufffact}
    run_requiredunit = requiredunit_shop(base=run_road, sufffacts=run_sufffacts)
    run_requiredunits = {run_requiredunit.base: run_requiredunit}
    ball_idea = ideaunit_shop(_label=ball_text, _requiredunits=run_requiredunits)
    assert ball_idea._requiredunits != {}

    # WHEN
    ball_idea.set_requiredheirs(requiredheirs=None, agenda_idea_dict={})

    # THEN
    requiredheir = requiredheir_shop(run_road, sufffacts=run_sufffacts)
    requiredheirs = {requiredheir.base: requiredheir}
    assert ball_idea._requiredheirs == requiredheirs


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
    field_text = "_kids"
    # WHEN / THEN
    assert get_obj_from_idea_dict({field_text: {}}, field_text) == {}
    assert get_obj_from_idea_dict({}, field_text) == {}


def test_idea_get_dict_ReturnsCorrectCompleteDict():
    # GIVEN
    week_text = "weekdays"
    week_road = create_road(root_label(), week_text)
    wed_text = "Wednesday"
    wed_road = create_road(week_road, wed_text)
    states_text = "nation-state"
    states_road = create_road(root_label(), states_text)
    usa_text = "USA"
    usa_road = create_road(states_road, usa_text)

    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffact._status = True
    usa_sufffact = sufffactunit_shop(need=usa_road)
    usa_sufffact._status = False

    x1_requiredunits = {
        week_road: requiredunit_shop(
            base=week_road, sufffacts={wed_sufffact.need: wed_sufffact}
        ),
        states_road: requiredunit_shop(
            base=states_road, sufffacts={usa_sufffact.need: usa_sufffact}
        ),
    }
    x1_requiredheirs = {
        week_road: requiredheir_shop(
            base=week_road, sufffacts={wed_sufffact.need: wed_sufffact}, _status=True
        ),
        states_road: requiredheir_shop(
            base=states_road, sufffacts={usa_sufffact.need: usa_sufffact}, _status=False
        ),
    }
    biker_pid = GroupBrand("bikers")
    biker_creditor_weight = 3.0
    biker_debtor_weight = 7.0
    biker_link = balancelink_shop(biker_pid, biker_creditor_weight, biker_debtor_weight)
    flyer_pid = GroupBrand("flyers")
    flyer_creditor_weight = 6.0
    flyer_debtor_weight = 9.0
    flyer_link = balancelink_shop(
        brand=flyer_pid,
        creditor_weight=flyer_creditor_weight,
        debtor_weight=flyer_debtor_weight,
    )
    biker_and_flyer_balancelinks = {
        biker_link.brand: biker_link,
        flyer_link.brand: flyer_link,
    }
    biker_get_dict = {
        "brand": biker_link.brand,
        "creditor_weight": biker_link.creditor_weight,
        "debtor_weight": biker_link.debtor_weight,
    }
    flyer_get_dict = {
        "brand": flyer_link.brand,
        "creditor_weight": flyer_link.creditor_weight,
        "debtor_weight": flyer_link.debtor_weight,
    }
    x1_balancelinks = {biker_pid: biker_get_dict, flyer_pid: flyer_get_dict}

    work_text = "work"
    work_road = create_road(root_label(), work_text)
    work_idea = ideaunit_shop(
        _parent_road=work_road,
        _kids=None,
        _balancelinks=biker_and_flyer_balancelinks,
        _weight=30,
        _label=work_text,
        _level=1,
        _requiredunits=x1_requiredunits,
        _requiredheirs=x1_requiredheirs,
        _active_status=True,
        _range_source_road="test123",
        promise=True,
        _problem_bool=True,
    )
    acptfactunit_x = acptfactunit_shop(base=week_road, pick=week_road, open=5, nigh=59)
    work_idea.set_acptfactunit(acptfactunit=acptfactunit_x)
    work_idea._originunit.set_originlink(pid="Ray", weight=None)
    work_idea._originunit.set_originlink(pid="Lei", weight=4)
    x_begin = 11
    x_close = 12
    x_addin = 13
    x_denom = 14
    x_numor = 15
    x_reest = 16
    work_idea._begin = x_begin
    work_idea._close = x_close
    work_idea._addin = x_addin
    work_idea._denom = x_denom
    work_idea._numor = x_numor
    work_idea._reest = x_reest
    work_idea._uid = 17
    work_idea.add_kid(ideaunit_shop("paper"))

    # WHEN
    work_dict = work_idea.get_dict()

    # THEN
    assert work_dict != None
    assert len(work_dict["_kids"]) == 1
    assert work_dict["_kids"] == work_idea.get_kids_dict()
    assert work_dict["_requiredunits"] == work_idea.get_requiredunits_dict()
    assert work_dict["_balancelinks"] == work_idea.get_balancelinks_dict()
    assert work_dict["_balancelinks"] == x1_balancelinks
    assert work_dict["_originunit"] == work_idea.get_originunit_dict()
    assert work_dict["_weight"] == work_idea._weight
    assert work_dict["_label"] == work_idea._label
    assert work_dict["_uid"] == work_idea._uid
    assert work_dict["_begin"] == work_idea._begin
    assert work_dict["_close"] == work_idea._close
    assert work_dict["_numor"] == work_idea._numor
    assert work_dict["_denom"] == work_idea._denom
    assert work_dict["_reest"] == work_idea._reest
    assert work_dict["_range_source_road"] == work_idea._range_source_road
    assert work_dict["promise"] == work_idea.promise
    assert work_dict["_problem_bool"] == work_idea._problem_bool
    assert work_idea._is_expanded
    assert work_dict.get("_is_expanded") is None
    assert len(work_dict["_acptfactunits"]) == len(work_idea.get_acptfactunits_dict())
    assert work_idea._on_meld_weight_action == "default"
    assert work_dict.get("_on_meld_weight_action") is None


def test_idea_get_dict_ReturnsCorrectIncompleteDict():
    # GIVEN
    work_idea = ideaunit_shop()

    # WHEN
    work_dict = work_idea.get_dict()

    # THEN
    assert work_dict != None
    assert work_dict == {"_weight": 1}


def test_idea_get_dict_ReturnsDictWith_attrs_CorrectlySetTrue():
    # GIVEN
    work_idea = ideaunit_shop()
    work_idea._is_expanded = False
    work_idea.promise = True
    work_idea._problem_bool = True
    ignore_text = "ignore"
    work_idea._on_meld_weight_action = ignore_text

    a_text = "a"
    a_road = create_road(root_label(), a_text)
    work_idea.set_acptfactunit(acptfactunit_shop(a_road, a_road))

    yao_text = "Yao"
    work_idea.set_balancelink(balancelink_shop(yao_text))

    x_assignedunit = work_idea._assignedunit
    x_assignedunit.set_suffgroup(brand=yao_text)

    x_originunit = work_idea._originunit
    x_originunit.set_originlink(yao_text, 1)

    rock_text = "Rock"
    work_idea.add_kid(ideaunit_shop(rock_text))

    assert not work_idea._is_expanded
    assert work_idea.promise
    assert work_idea._problem_bool
    assert work_idea._on_meld_weight_action != "default"
    assert work_idea._acptfactunits != None
    assert work_idea._balancelinks != None
    assert work_idea._assignedunit != None
    assert work_idea._originunit != None
    assert work_idea._kids != {}

    # WHEN
    work_dict = work_idea.get_dict()

    # THEN
    assert work_dict.get("_is_expanded") == False
    assert work_dict.get("promise")
    assert work_dict.get("_problem_bool")
    assert work_dict.get("_on_meld_weight_action") == ignore_text
    assert work_dict.get("_acptfactunits") != None
    assert work_dict.get("_balancelinks") != None
    assert work_dict.get("_assignedunit") != None
    assert work_dict.get("_originunit") != None
    assert work_dict.get("_kids") != None


def test_idea_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # GIVEN
    work_idea = ideaunit_shop()
    assert work_idea._is_expanded
    assert work_idea.promise == False
    assert work_idea._problem_bool == False
    assert work_idea._on_meld_weight_action == "default"
    assert work_idea._acptfactunits == {}
    assert work_idea._balancelinks == {}
    assert work_idea._assignedunit == assigned_unit_shop()
    assert work_idea._originunit == originunit_shop()
    assert work_idea._kids == {}

    # WHEN
    work_dict = work_idea.get_dict()

    # THEN
    assert work_dict.get("_is_expanded") is None
    assert work_dict.get("promise") is None
    assert work_dict.get("_problem_bool") is None
    assert work_dict.get("_on_meld_weight_action") is None
    assert work_dict.get("_acptfactunits") is None
    assert work_dict.get("_balancelinks") is None
    assert work_dict.get("_assignedunit") is None
    assert work_dict.get("_originunit") is None
    assert work_dict.get("_kids") is None


def test_idea_vaild_DenomCorrectInheritsBeginAndClose():
    # GIVEN
    work_text = "work"
    clean_text = "clean"
    # parent idea
    work_idea = ideaunit_shop(_label=work_text, _begin=22.0, _close=66.0)
    # kid idea
    clean_idea = ideaunit_shop(_label=clean_text, _numor=1, _denom=11.0, _reest=False)

    # WHEN
    work_idea.add_kid(idea_kid=clean_idea)

    # THEN
    assert work_idea._kids[clean_text]._begin == 2
    assert work_idea._kids[clean_text]._close == 6
    kid_idea_expected = ideaunit_shop(
        clean_text, _numor=1, _denom=11.0, _reest=False, _begin=2, _close=6
    )
    assert work_idea._kids[clean_text] == kid_idea_expected


def test_idea_invaild_DenomThrowsError():
    # GIVEN
    work_text = "work"
    parent_idea = ideaunit_shop(_label=work_text)
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


def test_idea_get_requiredheir_correctlyReturnsrequiredheir_shop():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    tool_text = "tool"
    required_heir_x = requiredheir_shop(base=tool_text)
    required_heirs_x = {required_heir_x.base: required_heir_x}
    clean_idea.set_requiredheirs(requiredheirs=required_heirs_x, agenda_idea_dict={})

    # WHEN
    required_heir_z = clean_idea.get_requiredheir(base=tool_text)

    # THEN
    assert required_heir_z != None
    assert required_heir_z.base == tool_text


def test_idea_get_requiredheir_correctlyReturnsNone():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    tool_text = "tool"
    required_heir_x = requiredheir_shop(tool_text)
    required_heirs_x = {required_heir_x.base: required_heir_x}
    clean_idea.set_requiredheirs(requiredheirs=required_heirs_x, agenda_idea_dict={})

    # WHEN
    test6_text = "test6"
    required_heir_test6 = clean_idea.get_requiredheir(base=test6_text)

    # THEN
    assert required_heir_test6 is None


def test_idea_set_active_status_SetsNullactive_status_hxToNonEmpty():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    assert clean_idea._active_status_hx == {}

    # WHEN
    clean_idea.set_active_status(tree_traverse_count=3)
    # THEN
    assert clean_idea._active_status_hx == {3: True}


def test_idea_set_active_status_IfFullactive_status_hxResetToTrue():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    clean_idea._active_status_hx = {0: True, 4: False}
    assert clean_idea._active_status_hx != {0: True}
    # WHEN
    clean_idea.set_active_status(tree_traverse_count=0)
    # THEN
    assert clean_idea._active_status_hx == {0: True}


# def test_idea_set_active_status_IfFullactive_status_hxResetToFalse():
#     # GIVEN
# clean_text = "clean"
# clean_idea = ideaunit_shop(_label=clean_text)
#     clean_idea.set_required_sufffact(
#         base="testing1,second",
#         sufffact="testing1,second,next",
#         open=None,
#         nigh=None,
#         divisor=None,
#     )
#     clean_idea._active_status_hx = {0: True, 4: False}
#     assert clean_idea._active_status_hx != {0: False}
#     # WHEN
#     clean_idea.set_active_status(tree_traverse_count=0)
#     # THEN
#     assert clean_idea._active_status_hx == {0: False}


def test_idea_record_active_status_hx_CorrectlyRecordsHistorry():
    # GIVEN
    clean_text = "clean"
    clean_idea = ideaunit_shop(_label=clean_text)
    assert clean_idea._active_status_hx == {}

    # WHEN
    clean_idea.record_active_status_hx(
        tree_traverse_count=0,
        prev_active_status=None,
        curr_active_status=True,
    )
    # THEN
    assert clean_idea._active_status_hx == {0: True}

    # WHEN
    clean_idea.record_active_status_hx(
        tree_traverse_count=1,
        prev_active_status=True,
        curr_active_status=True,
    )
    # THEN
    assert clean_idea._active_status_hx == {0: True}

    # WHEN
    clean_idea.record_active_status_hx(
        tree_traverse_count=2,
        prev_active_status=True,
        curr_active_status=False,
    )
    # THEN
    assert clean_idea._active_status_hx == {0: True, 2: False}

    # WHEN
    clean_idea.record_active_status_hx(
        tree_traverse_count=3,
        prev_active_status=False,
        curr_active_status=False,
    )
    # THEN
    assert clean_idea._active_status_hx == {0: True, 2: False}

    # WHEN
    clean_idea.record_active_status_hx(
        tree_traverse_count=4,
        prev_active_status=False,
        curr_active_status=True,
    )
    # THEN
    assert clean_idea._active_status_hx == {0: True, 2: False, 4: True}

    # WHEN
    clean_idea.record_active_status_hx(
        tree_traverse_count=0,
        prev_active_status=False,
        curr_active_status=False,
    )
    # THEN
    assert clean_idea._active_status_hx == {0: False}


def test_idea_set_assignedunit_empty_if_null():
    # GIVEN
    run_text = "run"
    run_idea = ideaunit_shop(_label=run_text)
    run_idea._assignedunit = None
    assert run_idea._assignedunit is None

    # WHEN
    run_idea.set_assignedunit_empty_if_null()

    # THEN
    assert run_idea._assignedunit != None
    assert run_idea._assignedunit == assigned_unit_shop()


def test_idea_set_assignedheir_CorrectlySetsAttr():
    # GIVEN
    swim_text = "swimmers"
    sport_text = "sports"
    sport_idea = ideaunit_shop(_label=sport_text)
    sport_idea._assignedunit.set_suffgroup(brand=swim_text)
    assert sport_idea._assignedheir is None

    # WHEN
    sport_idea.set_assignedheir(parent_assignheir=None, agenda_groups=None)

    # THEN
    assert sport_idea._assignedheir != None
    swim_assigned_unit = assigned_unit_shop()
    swim_assigned_unit.set_suffgroup(brand=swim_text)
    swim_assigned_heir = assigned_heir_shop()
    swim_assigned_heir.set_suffgroups(
        assignunit=swim_assigned_unit, parent_assignheir=None, agenda_groups=None
    )
    assert sport_idea._assignedheir == swim_assigned_heir


def test_idea_get_descendants_ReturnsNoRoadUnits():
    # GIVEN
    nation_text = "nation-state"
    nation_idea = ideaunit_shop(_label=nation_text, _parent_road=root_label())

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads_from_kids()

    # THEN
    assert nation_descendants == {}


def test_idea_get_descendants_Returns3DescendantsRoadUnits():
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


def test_idea_get_descendants_ErrorRaisedIfInfiniteLoop():
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


def test_idea_clear_kids_CorrectlySetsAttr():
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


def test_idea_get_kid_ReturnsCorrectObj():
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


def test_idea_del_kid_CorrectChangesAttr():
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
