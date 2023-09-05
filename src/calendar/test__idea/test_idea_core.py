from src.calendar.idea import IdeaCore
from src.calendar.group import GroupName, grouplink_shop, groupheir_shop
from src.calendar.required_idea import (
    RequiredUnit,
    RequiredHeir,
    acptfactunit_shop,
    sufffactunit_shop,
    Road,
)
from src.calendar.required_assign import assigned_unit_shop, assigned_heir_shop
from src.calendar.road import get_global_root_label as root_label
from pytest import raises as pytest_raise


def test_idea_core_exists():
    new_obj = IdeaCore()
    assert new_obj
    assert new_obj._kids is None
    assert new_obj._weight >= 1
    assert new_obj._label is None
    assert new_obj._uid is None
    assert new_obj._all_member_credit is None
    assert new_obj._all_member_debt is None
    assert new_obj._begin is None
    assert new_obj._close is None
    assert new_obj._addin is None
    assert new_obj._numor is None
    assert new_obj._denom is None
    assert new_obj._reest is None
    assert new_obj._numeric_road is None
    assert new_obj._special_road is None
    assert new_obj.promise is False
    assert new_obj._problem_bool is False
    assert new_obj._descendant_promise_count is None
    assert new_obj._grouplines is None
    assert new_obj._groupheirs is None
    assert new_obj._is_expanded == True
    assert new_obj._acptfactheirs is None
    assert new_obj._acptfactunits is None
    assert new_obj._on_meld_weight_action == "default"
    assert new_obj._active_status_hx is None
    assert new_obj._calendar_importance is None
    assert new_obj._calendar_coin_onset is None
    assert new_obj._calendar_coin_cease is None
    assert new_obj._requiredunits is None
    assert new_obj._requiredheirs is None
    assert new_obj._assignedunit is None
    assert new_obj._assignedheir is None
    assert new_obj._originunit is None


def test_idea_core_get_key_road_works():
    round_text = "round_things"
    round_walk = f"{root_label()},{round_text}"
    x_label = "ball"
    idea = IdeaCore(_label=x_label, _walk=round_walk)
    assert idea.get_key_road() == f"{x_label}"


def test_idea_core_is_heir_CorrectlyIdentifiesHeirs():
    idea_core = IdeaCore()
    texas_road = "prom,Nation-States,USA,Texas"
    usa_road = "prom,Nation-States,USA"
    assert idea_core.is_heir(src=usa_road, heir=usa_road)
    assert idea_core.is_heir(src=usa_road, heir=texas_road)
    assert idea_core.is_heir(src="earth,sea", heir="earth,seaside,beach") == False
    assert idea_core.is_heir(src="earth,sea", heir="earth,seaside") == False


def test_idea_core_grouplinks_exist():
    # GIVEN
    biker_creditor_weight = 12
    biker_debtor_weight = 15
    biker_link = grouplink_shop(
        name=GroupName("bikers2"),
        creditor_weight=biker_creditor_weight,
        debtor_weight=biker_debtor_weight,
    )

    swimmer_name = GroupName("swimmers")
    swimmer_creditor_weight = 29
    swimmer_debtor_weight = 32
    swimmer_link = grouplink_shop(
        name=swimmer_name,
        creditor_weight=swimmer_creditor_weight,
        debtor_weight=swimmer_debtor_weight,
    )

    group_links = {swimmer_link.name: swimmer_link, biker_link.name: biker_link}

    # WHEN
    idea_core = IdeaCore(_label="exercising", _grouplinks=group_links)

    # THEN
    assert idea_core._grouplinks == group_links
    # assert group_link_x.weight == 1.0
    # group_link_x = grouplink_shop(name=bikers_name, weight=bikers_weight)
    # assert group_link_x.weight == 3.0


def test_idea_core_get_inherited_groupheirs_weight_sum_WorksCorrectlyWithValues():
    # GIVEN
    biker_creditor_weight = 12
    biker_debtor_weight = 15
    biker_text = "bikers2"
    biker_link = groupheir_shop(
        name=GroupName(biker_text),
        creditor_weight=biker_creditor_weight,
        debtor_weight=biker_debtor_weight,
    )

    swimmer_text = "swimmers"
    swimmer_name = GroupName(swimmer_text)
    swimmer_creditor_weight = 29
    swimmer_debtor_weight = 32
    swimmer_link = groupheir_shop(
        name=swimmer_name,
        creditor_weight=swimmer_creditor_weight,
        debtor_weight=swimmer_debtor_weight,
    )

    group_links = {swimmer_link.name: swimmer_link, biker_link.name: biker_link}

    # WHEN
    idea_core = IdeaCore(_label="exercising", _groupheirs=group_links)

    # THEN
    assert idea_core.get_groupheirs_creditor_weight_sum() != None
    assert idea_core.get_groupheirs_creditor_weight_sum() == 41
    assert idea_core.get_groupheirs_debtor_weight_sum() != None
    assert idea_core.get_groupheirs_debtor_weight_sum() == 47

    assert len(idea_core._groupheirs) == 2

    swimmer_groupheir = idea_core._groupheirs.get(swimmer_text)
    assert swimmer_groupheir._calendar_credit is None
    assert swimmer_groupheir._calendar_debt is None
    biker_groupheir = idea_core._groupheirs.get(biker_text)
    assert biker_groupheir._calendar_credit is None
    assert biker_groupheir._calendar_debt is None

    # WHEN
    idea_core._calendar_importance = 0.25
    idea_core.set_groupheirs_calendar_credit_debit()

    # THEN
    print(f"{len(idea_core._groupheirs)=}")
    swimmer_groupheir = idea_core._groupheirs.get(swimmer_text)
    assert swimmer_groupheir._calendar_credit != None
    assert swimmer_groupheir._calendar_debt != None
    biker_groupheir = idea_core._groupheirs.get(biker_text)
    assert biker_groupheir._calendar_credit != None
    assert biker_groupheir._calendar_debt != None


def test_idea_core_get_grouplinks_weight_sum_WorksCorrectlyNoValues():
    # GIVEN /WHEN
    idea_core = IdeaCore(_label="exercising")

    # THEN
    assert idea_core.get_groupheirs_creditor_weight_sum() != None
    assert idea_core.get_groupheirs_debtor_weight_sum() != None
    # does not crash with empty set
    idea_core.set_groupheirs_calendar_credit_debit()


def test_idea_core_set_requiredheirsCorrectlyTakesFromOutside():
    # GIVEN
    idea = IdeaCore(_label="ball")
    sufffact_x = sufffactunit_shop(need="ball,run", open=0, nigh=7)
    sufffacts = {sufffact_x.need: sufffact_x}
    requiredunit = RequiredUnit(base="ball,run", sufffacts=sufffacts)
    requiredunits = {requiredunit.base: requiredunit}
    requiredheir = RequiredHeir(base="ball,run", sufffacts=sufffacts)
    requiredheirs = {requiredheir.base: requiredheir}
    assert idea._requiredunits is None
    assert idea._requiredheirs is None
    idea.set_requiredheirs(requiredheirs=requiredheirs, calendar_idea_dict=None)
    assert idea._requiredunits == {}
    assert idea._requiredheirs == requiredheirs
    assert id(idea._requiredheirs) != id(requiredheirs)


def test_idea_core_set_requiredheirsCorrectlyTakesFromSelf():
    sufffact_x = sufffactunit_shop(need="ball,run", open=0, nigh=7)
    sufffacts = {sufffact_x.need: sufffact_x}
    requiredunit = RequiredUnit(base="ball,run", sufffacts=sufffacts)
    requiredunits = {requiredunit.base: requiredunit}
    idea = IdeaCore(_label="ball", _requiredunits=requiredunits)

    requiredheir = RequiredHeir(base="ball,run", sufffacts=sufffacts)
    requiredheirs = {requiredheir.base: requiredheir}

    assert idea._requiredunits != None
    assert idea._requiredheirs is None
    idea.set_requiredheirs(requiredheirs=None, calendar_idea_dict=None)
    assert idea._requiredheirs == requiredheirs


def test_idea_core_clear_descendant_promise_count_ClearsCorrectly():
    idea = IdeaCore(_label="ball", _descendant_promise_count=55)
    assert idea._descendant_promise_count == 55
    idea.clear_descendant_promise_count()
    assert idea._descendant_promise_count is None


def test_idea_core_clear_all_member_credit_debt_ClearsCorrectly():
    idea = IdeaCore(_label="ball", _all_member_credit=55, _all_member_debt=33)
    assert idea._all_member_credit == 55
    assert idea._all_member_debt == 33
    idea.clear_all_member_credit_debt()
    assert idea._all_member_credit is None
    assert idea._all_member_debt is None


def test_get_kids_in_range_GetsCorrectIdeas():
    # Given
    idea_x = IdeaCore(_label="366months", _begin=0, _close=366)
    idea_x.add_kid(idea_kid=IdeaCore(_label="Jan", _begin=0, _close=31))
    idea_x.add_kid(idea_kid=IdeaCore(_label="Feb29", _begin=31, _close=60))
    idea_x.add_kid(idea_kid=IdeaCore(_label="Mar", _begin=31, _close=91))

    # When/Then
    assert len(idea_x.get_kids_in_range(begin=100, close=120)) == 0
    assert len(idea_x.get_kids_in_range(begin=0, close=31)) == 1
    assert len(idea_x.get_kids_in_range(begin=5, close=5)) == 1
    assert len(idea_x.get_kids_in_range(begin=0, close=61)) == 3
    assert idea_x.get_kids_in_range(begin=31, close=31)[0]._label == "Feb29"


def test_idea_get_dict_ReturnsDict():
    # GIVEN
    week_text = "weekdays"
    week_road = f"{root_label()},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    states_text = "nation-state"
    states_road = f"{root_label()},{states_text}"
    france_text = "France"
    france_road = f"{states_road},{france_text}"
    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    oregon_text = "Oregon"
    oregon_road = f"{usa_road},{oregon_text}"

    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffact._status = True
    usa_sufffact = sufffactunit_shop(need=usa_road)
    usa_sufffact._status = False

    x1_requiredunits = {
        week_road: RequiredUnit(
            base=week_road, sufffacts={wed_sufffact.need: wed_sufffact}
        ),
        states_road: RequiredUnit(
            base=states_road, sufffacts={usa_sufffact.need: usa_sufffact}
        ),
    }
    x1_requiredheirs = {
        week_road: RequiredHeir(
            base=week_road, sufffacts={wed_sufffact.need: wed_sufffact}, _status=True
        ),
        states_road: RequiredHeir(
            base=states_road, sufffacts={usa_sufffact.need: usa_sufffact}, _status=False
        ),
    }
    biker_name = GroupName("bikers")
    biker_creditor_weight = 3.0
    biker_debtor_weight = 7.0
    biker_link = grouplink_shop(
        name=biker_name,
        creditor_weight=biker_creditor_weight,
        debtor_weight=biker_debtor_weight,
    )
    flyer_name = GroupName("flyers")
    flyer_creditor_weight = 6.0
    flyer_debtor_weight = 9.0
    flyer_link = grouplink_shop(
        name=flyer_name,
        creditor_weight=flyer_creditor_weight,
        debtor_weight=flyer_debtor_weight,
    )
    biker_and_flyer_grouplinks = {
        biker_link.name: biker_link,
        flyer_link.name: flyer_link,
    }
    biker_get_dict = {
        "name": biker_link.name,
        "creditor_weight": biker_link.creditor_weight,
        "debtor_weight": biker_link.debtor_weight,
    }
    flyer_get_dict = {
        "name": flyer_link.name,
        "creditor_weight": flyer_link.creditor_weight,
        "debtor_weight": flyer_link.debtor_weight,
    }
    x1_grouplinks = {biker_name: biker_get_dict, flyer_name: flyer_get_dict}

    temp_idea = IdeaCore(
        _walk=f"{root_label()},work",
        _kids=None,
        _grouplinks=biker_and_flyer_grouplinks,
        _weight=30,
        _label="work",
        _level=1,
        _requiredunits=x1_requiredunits,
        _requiredheirs=x1_requiredheirs,
        _active_status=True,
        _special_road="test123",
        promise=True,
        _problem_bool=True,
    )
    acptfactunit_x = acptfactunit_shop(base=week_road, pick=week_road, open=5, nigh=59)
    temp_idea._set_ideakid_attr(acptfactunit=acptfactunit_x)

    # WHEN
    ideakid_dict = temp_idea.get_dict()

    # THEN
    assert ideakid_dict != None
    assert ideakid_dict["_kids"] == temp_idea.get_kids_dict()
    assert ideakid_dict["_requiredunits"] == temp_idea.get_requiredunits_dict()
    assert ideakid_dict["_grouplinks"] == temp_idea.get_grouplinks_dict()
    assert ideakid_dict["_grouplinks"] == x1_grouplinks
    assert ideakid_dict["_weight"] == temp_idea._weight
    assert ideakid_dict["_label"] == temp_idea._label
    assert ideakid_dict["_uid"] == temp_idea._uid
    assert ideakid_dict["_begin"] == temp_idea._begin
    assert ideakid_dict["_close"] == temp_idea._close
    assert ideakid_dict["_numor"] == temp_idea._numor
    assert ideakid_dict["_denom"] == temp_idea._denom
    assert ideakid_dict["_reest"] == temp_idea._reest
    assert ideakid_dict["_special_road"] == temp_idea._special_road
    assert ideakid_dict["promise"] == temp_idea.promise
    assert ideakid_dict["_problem_bool"] == temp_idea._problem_bool
    assert ideakid_dict["_is_expanded"] == temp_idea._is_expanded
    assert len(ideakid_dict["_acptfactunits"]) == len(
        temp_idea.get_acptfactunits_dict()
    )
    assert ideakid_dict["_on_meld_weight_action"] == temp_idea._on_meld_weight_action


def test_idea_vaild_DenomCorrectInheritsBeginAndClose():
    parent_idea = IdeaCore(_label="work", _begin=22.0, _close=66.0)
    kid_idea_given = IdeaCore(_label="clean", _numor=1, _denom=11.0, _reest=False)
    kid_idea_expected = IdeaCore(
        _label="clean", _numor=1, _denom=11.0, _reest=False, _begin=2, _close=6
    )
    parent_idea.add_kid(idea_kid=kid_idea_given)
    assert parent_idea._kids["clean"]._begin == 2
    assert parent_idea._kids["clean"]._close == 6
    assert parent_idea._kids["clean"] == kid_idea_expected


def test_idea_invaild_DenomThrowsError():
    parent_idea = IdeaCore(_label="work")
    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    clean_text = "clean"
    clean_road = f"{casa_road},{clean_text}"
    kid_idea = IdeaCore(
        _label=clean_text, _walk=casa_road, _numor=1, _denom=11.0, _reest=False
    )
    # When/Then
    with pytest_raise(Exception) as excinfo:
        parent_idea.add_kid(idea_kid=kid_idea)
    assert (
        str(excinfo.value)
        == f"Idea {clean_road} cannot have numor,denom,reest if parent does not have begin/close range"
    )


def test_idea_get_requiredheir_correctlyReturnsRequiredHeir():
    # GIVEN
    idea_x = IdeaCore(_label="test4")
    test5_text = "test5"
    required_heir_x = RequiredHeir(base=test5_text, sufffacts={})
    required_heirs_x = {required_heir_x.base: required_heir_x}
    idea_x.set_requiredheirs(requiredheirs=required_heirs_x, calendar_idea_dict=None)

    # WHEN
    required_heir_z = idea_x.get_requiredheir(base=test5_text)

    # THEN
    assert required_heir_z != None
    assert required_heir_z.base == test5_text


def test_idea_get_requiredheir_correctlyReturnsNone():
    # GIVEN
    idea_x = IdeaCore(_label="test4")
    test5_text = "test5"
    required_heir_x = RequiredHeir(base=test5_text, sufffacts={})
    required_heirs_x = {required_heir_x.base: required_heir_x}
    idea_x.set_requiredheirs(requiredheirs=required_heirs_x, calendar_idea_dict=None)

    # WHEN
    test6_text = "test6"
    required_heir_test6 = idea_x.get_requiredheir(base=test6_text)

    # THEN
    assert required_heir_test6 is None


def test_idea_set_active_status_SetsNullactive_status_hxToNonEmpty():
    # GIVEN
    idea_x = IdeaCore(_label="test4")
    assert idea_x._active_status_hx is None

    # WHEN
    idea_x.set_active_status(tree_traverse_count=3)
    # THEN
    assert idea_x._active_status_hx == {3: True}


def test_idea_set_active_status_IfFullactive_status_hxResetToTrue():
    # GIVEN
    idea_x = IdeaCore(_label="test4")
    idea_x._active_status_hx = {0: True, 4: False}
    assert idea_x._active_status_hx != {0: True}
    # WHEN
    idea_x.set_active_status(tree_traverse_count=0)
    # THEN
    assert idea_x._active_status_hx == {0: True}


# def test_idea_set_active_status_IfFullactive_status_hxResetToFalse():
#     # GIVEN
#     idea_x = IdeaCore(_label="test4")
#     idea_x.set_required_sufffact(
#         base="testing1,second",
#         sufffact="testing1,second,next",
#         open=None,
#         nigh=None,
#         divisor=None,
#     )
#     idea_x._active_status_hx = {0: True, 4: False}
#     assert idea_x._active_status_hx != {0: False}
#     # WHEN
#     idea_x.set_active_status(tree_traverse_count=0)
#     # THEN
#     assert idea_x._active_status_hx == {0: False}


def test_idea_record_active_status_hx_CorrectlyRecordsHistorry():
    # GIVEN
    idea_x = IdeaCore(_label="test4")
    assert idea_x._active_status_hx is None

    # WHEN
    idea_x.record_active_status_hx(
        tree_traverse_count=0,
        prev_active_status=None,
        curr_active_status=True,
    )
    # THEN
    assert idea_x._active_status_hx == {0: True}

    # WHEN
    idea_x.record_active_status_hx(
        tree_traverse_count=1,
        prev_active_status=True,
        curr_active_status=True,
    )
    # THEN
    assert idea_x._active_status_hx == {0: True}

    # WHEN
    idea_x.record_active_status_hx(
        tree_traverse_count=2,
        prev_active_status=True,
        curr_active_status=False,
    )
    # THEN
    assert idea_x._active_status_hx == {0: True, 2: False}

    # WHEN
    idea_x.record_active_status_hx(
        tree_traverse_count=3,
        prev_active_status=False,
        curr_active_status=False,
    )
    # THEN
    assert idea_x._active_status_hx == {0: True, 2: False}

    # WHEN
    idea_x.record_active_status_hx(
        tree_traverse_count=4,
        prev_active_status=False,
        curr_active_status=True,
    )
    # THEN
    assert idea_x._active_status_hx == {0: True, 2: False, 4: True}

    # WHEN
    idea_x.record_active_status_hx(
        tree_traverse_count=0,
        prev_active_status=False,
        curr_active_status=False,
    )
    # THEN
    assert idea_x._active_status_hx == {0: False}


def test_idea_set_assignedunit_empty_if_null():
    # GIVEN
    idea_x = IdeaCore(_label="run")
    assert idea_x._assignedunit is None

    # WHEN
    idea_x.set_assignedunit_empty_if_null()

    # THEN
    assert idea_x._assignedunit != None
    assert idea_x._assignedunit == assigned_unit_shop()


def test_idea_set_assignedunit_empty_if_null():
    # GIVEN
    swim_text = "swimmers"
    idea_x = IdeaCore(_label="run")
    idea_x.set_assignedunit_empty_if_null()
    idea_x._assignedunit.set_suffgroup(name=swim_text)
    assert idea_x._assignedheir is None

    # WHEN
    idea_x.set_assignedheir(parent_assignheir=None, calendar_groups=None)

    # THEN
    assert idea_x._assignedheir != None
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(name=swim_text)
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        assignunit=assigned_unit_x, parent_assignheir=None, calendar_groups=None
    )
    assert idea_x._assignedheir == assigned_heir_x
