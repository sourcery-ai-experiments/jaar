from src.pact.idea import IdeaCore
from src.pact.group import GroupBrand, balancelink_shop, balanceheir_shop
from src.pact.required_idea import (
    RequiredUnit,
    RequiredHeir,
    acptfactunit_shop,
    sufffactunit_shop,
    Road,
)
from src.pact.required_assign import assigned_unit_shop, assigned_heir_shop
from src.pact.road import get_default_cure_root_label as root_label
from pytest import raises as pytest_raises


def test_idea_core_exists():
    new_obj = IdeaCore()
    assert new_obj
    assert new_obj._kids is None
    assert new_obj._weight >= 1
    assert new_obj._label is None
    assert new_obj._uid is None
    assert new_obj._all_party_credit is None
    assert new_obj._all_party_debt is None
    assert new_obj._begin is None
    assert new_obj._close is None
    assert new_obj._addin is None
    assert new_obj._numor is None
    assert new_obj._denom is None
    assert new_obj._reest is None
    assert new_obj._numeric_road is None
    assert new_obj._range_source_road is None
    assert new_obj.promise is False
    assert new_obj._problem_bool is False
    assert new_obj._descendant_promise_count is None
    assert new_obj._balancelines is None
    assert new_obj._balanceheirs is None
    assert new_obj._is_expanded == True
    assert new_obj._acptfactheirs is None
    assert new_obj._acptfactunits is None
    assert new_obj._on_meld_weight_action == "default"
    assert new_obj._active_status_hx is None
    assert new_obj._pact_importance is None
    assert new_obj._pact_coin_onset is None
    assert new_obj._pact_coin_cease is None
    assert new_obj._requiredunits is None
    assert new_obj._requiredheirs is None
    assert new_obj._assignedunit is None
    assert new_obj._assignedheir is None
    assert new_obj._originunit is None


def test_idea_core_get_key_road_works():
    round_text = "round_things"
    round_pad = f"{root_label()},{round_text}"
    x_label = "ball"
    idea = IdeaCore(_label=x_label, _pad=round_pad)
    assert idea.get_key_road() == f"{x_label}"


def test_idea_core_is_heir_CorrectlyIdentifiesHeirs():
    idea_core = IdeaCore()
    texas_road = f"{root_label()},Nation-States,USA,Texas"
    usa_road = f"{root_label()},Nation-States,USA"
    assert idea_core.is_heir(src=usa_road, heir=usa_road)
    assert idea_core.is_heir(src=usa_road, heir=texas_road)
    assert idea_core.is_heir(src="earth,sea", heir="earth,seaside,beach") == False
    assert idea_core.is_heir(src="earth,sea", heir="earth,seaside") == False


def test_idea_core_balancelinks_exist():
    # GIVEN
    biker_creditor_weight = 12
    biker_debtor_weight = 15
    biker_link = balancelink_shop(
        brand=GroupBrand("bikers2"),
        creditor_weight=biker_creditor_weight,
        debtor_weight=biker_debtor_weight,
    )

    swimmer_title = GroupBrand("swimmers")
    swimmer_creditor_weight = 29
    swimmer_debtor_weight = 32
    swimmer_link = balancelink_shop(
        brand=swimmer_title,
        creditor_weight=swimmer_creditor_weight,
        debtor_weight=swimmer_debtor_weight,
    )

    group_links = {swimmer_link.brand: swimmer_link, biker_link.brand: biker_link}

    # WHEN
    idea_core = IdeaCore(_label="exercising", _balancelinks=group_links)

    # THEN
    assert idea_core._balancelinks == group_links
    # assert group_link_x.weight == 1.0
    # group_link_x = balancelink_shop(brand=bikers_title, weight=bikers_weight)
    # assert group_link_x.weight == 3.0


def test_idea_core_get_inherited_balanceheirs_weight_sum_WorksCorrectlyWithValues():
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
    swimmer_title = GroupBrand(swimmer_text)
    swimmer_creditor_weight = 29
    swimmer_debtor_weight = 32
    swimmer_link = balanceheir_shop(
        brand=swimmer_title,
        creditor_weight=swimmer_creditor_weight,
        debtor_weight=swimmer_debtor_weight,
    )

    group_links = {swimmer_link.brand: swimmer_link, biker_link.brand: biker_link}

    # WHEN
    idea_core = IdeaCore(_label="exercising", _balanceheirs=group_links)

    # THEN
    assert idea_core.get_balanceheirs_creditor_weight_sum() != None
    assert idea_core.get_balanceheirs_creditor_weight_sum() == 41
    assert idea_core.get_balanceheirs_debtor_weight_sum() != None
    assert idea_core.get_balanceheirs_debtor_weight_sum() == 47

    assert len(idea_core._balanceheirs) == 2

    swimmer_balanceheir = idea_core._balanceheirs.get(swimmer_text)
    assert swimmer_balanceheir._pact_credit is None
    assert swimmer_balanceheir._pact_debt is None
    biker_balanceheir = idea_core._balanceheirs.get(biker_text)
    assert biker_balanceheir._pact_credit is None
    assert biker_balanceheir._pact_debt is None

    # WHEN
    idea_core._pact_importance = 0.25
    idea_core.set_balanceheirs_pact_credit_debit()

    # THEN
    print(f"{len(idea_core._balanceheirs)=}")
    swimmer_balanceheir = idea_core._balanceheirs.get(swimmer_text)
    assert swimmer_balanceheir._pact_credit != None
    assert swimmer_balanceheir._pact_debt != None
    biker_balanceheir = idea_core._balanceheirs.get(biker_text)
    assert biker_balanceheir._pact_credit != None
    assert biker_balanceheir._pact_debt != None


def test_idea_core_get_balancelinks_weight_sum_WorksCorrectlyNoValues():
    # GIVEN /WHEN
    idea_core = IdeaCore(_label="exercising")

    # THEN
    assert idea_core.get_balanceheirs_creditor_weight_sum() != None
    assert idea_core.get_balanceheirs_debtor_weight_sum() != None
    # does not crash with empty set
    idea_core.set_balanceheirs_pact_credit_debit()


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
    idea.set_requiredheirs(requiredheirs=requiredheirs, pact_idea_dict=None)
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
    idea.set_requiredheirs(requiredheirs=None, pact_idea_dict=None)
    assert idea._requiredheirs == requiredheirs


def test_idea_core_clear_descendant_promise_count_ClearsCorrectly():
    idea = IdeaCore(_label="ball", _descendant_promise_count=55)
    assert idea._descendant_promise_count == 55
    idea.clear_descendant_promise_count()
    assert idea._descendant_promise_count is None


def test_idea_core_clear_all_party_credit_debt_ClearsCorrectly():
    idea = IdeaCore(_label="ball", _all_party_credit=55, _all_party_debt=33)
    assert idea._all_party_credit == 55
    assert idea._all_party_debt == 33
    idea.clear_all_party_credit_debt()
    assert idea._all_party_credit is None
    assert idea._all_party_debt is None


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
    biker_title = GroupBrand("bikers")
    biker_creditor_weight = 3.0
    biker_debtor_weight = 7.0
    biker_link = balancelink_shop(
        brand=biker_title,
        creditor_weight=biker_creditor_weight,
        debtor_weight=biker_debtor_weight,
    )
    flyer_title = GroupBrand("flyers")
    flyer_creditor_weight = 6.0
    flyer_debtor_weight = 9.0
    flyer_link = balancelink_shop(
        brand=flyer_title,
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
    x1_balancelinks = {biker_title: biker_get_dict, flyer_title: flyer_get_dict}

    temp_idea = IdeaCore(
        _pad=f"{root_label()},work",
        _kids=None,
        _balancelinks=biker_and_flyer_balancelinks,
        _weight=30,
        _label="work",
        _level=1,
        _requiredunits=x1_requiredunits,
        _requiredheirs=x1_requiredheirs,
        _active_status=True,
        _range_source_road="test123",
        promise=True,
        _problem_bool=True,
    )
    acptfactunit_x = acptfactunit_shop(base=week_road, pick=week_road, open=5, nigh=59)
    temp_idea._set_ideakid_attr(acptfactunit=acptfactunit_x)
    temp_idea.set_originunit_empty_if_null()
    temp_idea._originunit.set_originlink(title="Ray", weight=None)
    temp_idea._originunit.set_originlink(title="Lei", weight=4)

    # WHEN
    ideakid_dict = temp_idea.get_dict()

    # THEN
    assert ideakid_dict != None
    assert ideakid_dict["_kids"] == temp_idea.get_kids_dict()
    assert ideakid_dict["_requiredunits"] == temp_idea.get_requiredunits_dict()
    assert ideakid_dict["_balancelinks"] == temp_idea.get_balancelinks_dict()
    assert ideakid_dict["_balancelinks"] == x1_balancelinks
    assert ideakid_dict["_originunit"] == temp_idea.get_originunit_dict()
    assert ideakid_dict["_weight"] == temp_idea._weight
    assert ideakid_dict["_label"] == temp_idea._label
    assert ideakid_dict["_uid"] == temp_idea._uid
    assert ideakid_dict["_begin"] == temp_idea._begin
    assert ideakid_dict["_close"] == temp_idea._close
    assert ideakid_dict["_numor"] == temp_idea._numor
    assert ideakid_dict["_denom"] == temp_idea._denom
    assert ideakid_dict["_reest"] == temp_idea._reest
    assert ideakid_dict["_range_source_road"] == temp_idea._range_source_road
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
        _label=clean_text, _pad=casa_road, _numor=1, _denom=11.0, _reest=False
    )
    # When/Then
    with pytest_raises(Exception) as excinfo:
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
    idea_x.set_requiredheirs(requiredheirs=required_heirs_x, pact_idea_dict=None)

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
    idea_x.set_requiredheirs(requiredheirs=required_heirs_x, pact_idea_dict=None)

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
    idea_x._assignedunit.set_suffgroup(title=swim_text)
    assert idea_x._assignedheir is None

    # WHEN
    idea_x.set_assignedheir(parent_assignheir=None, pact_groups=None)

    # THEN
    assert idea_x._assignedheir != None
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(title=swim_text)
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffgroups(
        assignunit=assigned_unit_x, parent_assignheir=None, pact_groups=None
    )
    assert idea_x._assignedheir == assigned_heir_x


def test_idea_get_descendants_ReturnsNoRoads():
    # GIVEN
    nation_text = "nation-state"
    nation_road = f"{root_label()},{nation_text}"
    nation_idea = IdeaCore(_label=nation_text, _pad=root_label())

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads()

    # THEN
    assert nation_descendants == {}


def test_idea_get_descendants_Returns3DescendantsRoads():
    # GIVEN
    nation_text = "nation-state"
    nation_road = f"{root_label()},{nation_text}"
    nation_idea = IdeaCore(_label=nation_text, _pad=root_label())

    usa_text = "USA"
    usa_road = f"{nation_road},{usa_text}"
    usa_idea = IdeaCore(_label=usa_text, _pad=nation_road)
    nation_idea.add_kid(idea_kid=usa_idea)

    texas_text = "Texas"
    texas_road = f"{usa_road},{texas_text}"
    texas_idea = IdeaCore(_label=texas_text, _pad=usa_road)
    usa_idea.add_kid(idea_kid=texas_idea)

    iowa_text = "iowa"
    iowa_road = f"{usa_road},{iowa_text}"
    iowa_idea = IdeaCore(_label=iowa_text, _pad=usa_road)
    usa_idea.add_kid(idea_kid=iowa_idea)

    # WHEN
    nation_descendants = nation_idea.get_descendant_roads()

    # THEN
    assert len(nation_descendants) == 3
    assert nation_descendants.get(usa_road) != None
    assert nation_descendants.get(texas_road) != None
    assert nation_descendants.get(iowa_road) != None


def test_idea_get_descendants_ErrorRaisedIfInfiniteLoop():
    # Given
    nation_text = "nation-state"
    nation_road = f"{root_label()},{nation_text}"
    nation_idea = IdeaCore(_label=nation_text, _pad=root_label())
    nation_idea.add_kid(idea_kid=nation_idea)
    max_count = 1000

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        nation_idea.get_descendant_roads()
    assert (
        str(excinfo.value)
        == f"Idea '{nation_idea.get_road()}' either has an infinite loop or more than {max_count} descendants."
    )
