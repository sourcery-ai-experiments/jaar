from src.agent.tool import ToolCore
from src.agent.group import GroupName, grouplink_shop, groupheir_shop
from src.agent.required import (
    RequiredUnit,
    RequiredHeir,
    acptfactunit_shop,
    sufffactunit_shop,
    Road,
)
from pytest import raises as pytest_raise


def test_tool_core_exists():
    new_obj = ToolCore()
    assert new_obj
    assert new_obj._kids is None
    assert new_obj._weight >= 1
    assert new_obj._desc is None
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
    assert new_obj._agent_importance is None
    assert new_obj._agent_coin_onset is None
    assert new_obj._agent_coin_cease is None


def test_tool_core_get_key_road_works():
    x_walk = "src,round_things"
    x_desc = "ball"
    tool = ToolCore(_desc=x_desc, _walk=x_walk)
    assert tool.get_key_road() == f"{x_desc}"


def test_tool_core_is_heir_CorrectlyIdentifiesHeirs():
    tool_core = ToolCore()
    texas_road = "prom,Nation-States,USA,Texas"
    usa_road = "prom,Nation-States,USA"
    assert tool_core.is_heir(src=usa_road, heir=usa_road)
    assert tool_core.is_heir(src=usa_road, heir=texas_road)
    assert tool_core.is_heir(src="earth,sea", heir="earth,seaside,beach") == False
    assert tool_core.is_heir(src="earth,sea", heir="earth,seaside") == False


def test_tool_core_grouplinks_exist():
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
    tool_core = ToolCore(_desc="exercising", _grouplinks=group_links)

    # THEN
    assert tool_core._grouplinks == group_links
    # assert group_link_x.weight == 1.0
    # group_link_x = grouplink_shop(name=bikers_name, weight=bikers_weight)
    # assert group_link_x.weight == 3.0


def test_tool_core_get_inherited_groupheirs_weight_sum_WorksCorrectlyWithValues():
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
    tool_core = ToolCore(_desc="exercising", _groupheirs=group_links)

    # THEN
    assert tool_core.get_groupheirs_creditor_weight_sum() != None
    assert tool_core.get_groupheirs_creditor_weight_sum() == 41
    assert tool_core.get_groupheirs_debtor_weight_sum() != None
    assert tool_core.get_groupheirs_debtor_weight_sum() == 47

    assert len(tool_core._groupheirs) == 2

    swimmer_groupheir = tool_core._groupheirs.get(swimmer_text)
    assert swimmer_groupheir._agent_credit is None
    assert swimmer_groupheir._agent_debt is None
    biker_groupheir = tool_core._groupheirs.get(biker_text)
    assert biker_groupheir._agent_credit is None
    assert biker_groupheir._agent_debt is None

    # WHEN
    tool_core._agent_importance = 0.25
    tool_core.set_groupheirs_agent_credit_debit()

    # THEN
    print(f"{len(tool_core._groupheirs)=}")
    swimmer_groupheir = tool_core._groupheirs.get(swimmer_text)
    assert swimmer_groupheir._agent_credit != None
    assert swimmer_groupheir._agent_debt != None
    biker_groupheir = tool_core._groupheirs.get(biker_text)
    assert biker_groupheir._agent_credit != None
    assert biker_groupheir._agent_debt != None


def test_tool_core_get_grouplinks_weight_sum_WorksCorrectlyNoValues():
    # GIVEN /WHEN
    tool_core = ToolCore(_desc="exercising")

    # THEN
    assert tool_core.get_groupheirs_creditor_weight_sum() != None
    assert tool_core.get_groupheirs_debtor_weight_sum() != None
    # does not crash with empty set
    tool_core.set_groupheirs_agent_credit_debit()


def test_tool_core_set_requiredheirsCorrectlyTakesFromOutside():
    # GIVEN
    tool = ToolCore(_desc="ball")
    sufffact_x = sufffactunit_shop(need="ball,run", open=0, nigh=7)
    sufffacts = {sufffact_x.need: sufffact_x}
    requiredunit = RequiredUnit(base="ball,run", sufffacts=sufffacts)
    requiredunits = {requiredunit.base: requiredunit}
    requiredheir = RequiredHeir(base="ball,run", sufffacts=sufffacts)
    requiredheirs = {requiredheir.base: requiredheir}
    assert tool._requiredunits is None
    assert tool._requiredheirs is None
    tool.set_requiredheirs(requiredheirs=requiredheirs)
    assert tool._requiredunits == {}
    assert tool._requiredheirs == requiredheirs
    assert id(tool._requiredheirs) != id(requiredheirs)


def test_tool_core_set_requiredheirsCorrectlyTakesFromSelf():
    sufffact_x = sufffactunit_shop(need="ball,run", open=0, nigh=7)
    sufffacts = {sufffact_x.need: sufffact_x}
    requiredunit = RequiredUnit(base="ball,run", sufffacts=sufffacts)
    requiredunits = {requiredunit.base: requiredunit}
    tool = ToolCore(_desc="ball", _requiredunits=requiredunits)

    requiredheir = RequiredHeir(base="ball,run", sufffacts=sufffacts)
    requiredheirs = {requiredheir.base: requiredheir}

    assert tool._requiredunits != None
    assert tool._requiredheirs is None
    tool.set_requiredheirs(requiredheirs=None)
    assert tool._requiredheirs == requiredheirs


def test_tool_core_clear_descendant_promise_count_ClearsCorrectly():
    tool = ToolCore(_desc="ball", _descendant_promise_count=55)
    assert tool._descendant_promise_count == 55
    tool.clear_descendant_promise_count()
    assert tool._descendant_promise_count is None


def test_tool_core_clear_all_member_credit_debt_ClearsCorrectly():
    tool = ToolCore(_desc="ball", _all_member_credit=55, _all_member_debt=33)
    assert tool._all_member_credit == 55
    assert tool._all_member_debt == 33
    tool.clear_all_member_credit_debt()
    assert tool._all_member_credit is None
    assert tool._all_member_debt is None


def test_get_kids_in_range_GetsCorrectTools():
    # Given
    tool_x = ToolCore(_desc="366months", _begin=0, _close=366)
    tool_x.add_kid(tool_kid=ToolCore(_desc="Jan", _begin=0, _close=31))
    tool_x.add_kid(tool_kid=ToolCore(_desc="Feb29", _begin=31, _close=60))
    tool_x.add_kid(tool_kid=ToolCore(_desc="Mar", _begin=31, _close=91))

    # When/Then
    assert len(tool_x.get_kids_in_range(begin=100, close=120)) == 0
    assert len(tool_x.get_kids_in_range(begin=0, close=31)) == 1
    assert len(tool_x.get_kids_in_range(begin=5, close=5)) == 1
    assert len(tool_x.get_kids_in_range(begin=0, close=61)) == 3
    assert tool_x.get_kids_in_range(begin=31, close=31)[0]._desc == "Feb29"


def test_tool_get_dict_ReturnsDict():
    # GIVEN
    src_text = "src"
    week_text = "weekdays"
    week_road = f"{src_text},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    states_text = "nation-state"
    states_road = f"{src_text},{states_text}"
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

    temp_tool = ToolCore(
        _walk="src,work",
        _kids=None,
        _grouplinks=biker_and_flyer_grouplinks,
        _weight=30,
        _desc="work",
        _level=1,
        _requiredunits=x1_requiredunits,
        _requiredheirs=x1_requiredheirs,
        _active_status=True,
        _special_road="test123",
        promise=True,
        _problem_bool=True,
    )
    acptfactunit_x = acptfactunit_shop(base=week_road, pick=week_road, open=5, nigh=59)
    temp_tool._set_toolkid_attr(acptfactunit=acptfactunit_x)

    # WHEN
    toolkid_dict = temp_tool.get_dict()

    # THEN
    assert toolkid_dict != None
    assert toolkid_dict["_kids"] == temp_tool.get_kids_dict()
    assert toolkid_dict["_requiredunits"] == temp_tool.get_requiredunits_dict()
    assert toolkid_dict["_grouplinks"] == temp_tool.get_grouplinks_dict()
    assert toolkid_dict["_grouplinks"] == x1_grouplinks
    assert toolkid_dict["_weight"] == temp_tool._weight
    assert toolkid_dict["_desc"] == temp_tool._desc
    assert toolkid_dict["_uid"] == temp_tool._uid
    assert toolkid_dict["_begin"] == temp_tool._begin
    assert toolkid_dict["_close"] == temp_tool._close
    assert toolkid_dict["_numor"] == temp_tool._numor
    assert toolkid_dict["_denom"] == temp_tool._denom
    assert toolkid_dict["_reest"] == temp_tool._reest
    assert toolkid_dict["_special_road"] == temp_tool._special_road
    assert toolkid_dict["promise"] == temp_tool.promise
    assert toolkid_dict["_problem_bool"] == temp_tool._problem_bool
    assert toolkid_dict["_is_expanded"] == temp_tool._is_expanded
    assert len(toolkid_dict["_acptfactunits"]) == len(
        temp_tool.get_acptfactunits_dict()
    )
    assert toolkid_dict["_on_meld_weight_action"] == temp_tool._on_meld_weight_action


def test_tool_vaild_DenomCorrectInheritsBeginAndClose():
    parent_tool = ToolCore(_desc="work", _begin=22.0, _close=66.0)
    kid_tool_given = ToolCore(_desc="clean", _numor=1, _denom=11.0, _reest=False)
    kid_tool_expected = ToolCore(
        _desc="clean", _numor=1, _denom=11.0, _reest=False, _begin=2, _close=6
    )
    parent_tool.add_kid(tool_kid=kid_tool_given)
    assert parent_tool._kids["clean"]._begin == 2
    assert parent_tool._kids["clean"]._close == 6
    assert parent_tool._kids["clean"] == kid_tool_expected


def test_tool_invaild_DenomThrowsError():
    parent_tool = ToolCore(_desc="work")
    kid_tool = ToolCore(_desc="clean", _walk="src", _numor=1, _denom=11.0, _reest=False)
    # When/Then
    with pytest_raise(Exception) as excinfo:
        parent_tool.add_kid(tool_kid=kid_tool)
    assert (
        str(excinfo.value)
        == "Tool src,clean cannot have numor,denom,reest if parent does not have begin/close range"
    )


def test_tool_get_requiredheir_correctlyReturnsRequiredHeir():
    # GIVEN
    tool_x = ToolCore(_desc="test4")
    test5_text = "test5"
    required_heir_x = RequiredHeir(base=test5_text, sufffacts={})
    required_heirs_x = {required_heir_x.base: required_heir_x}
    tool_x.set_requiredheirs(requiredheirs=required_heirs_x)

    # WHEN
    required_heir_z = tool_x.get_requiredheir(base=test5_text)

    # THEN
    assert required_heir_z != None
    assert required_heir_z.base == test5_text


def test_tool_get_requiredheir_correctlyReturnsNone():
    # GIVEN
    tool_x = ToolCore(_desc="test4")
    test5_text = "test5"
    required_heir_x = RequiredHeir(base=test5_text, sufffacts={})
    required_heirs_x = {required_heir_x.base: required_heir_x}
    tool_x.set_requiredheirs(requiredheirs=required_heirs_x)

    # WHEN
    test6_text = "test6"
    required_heir_test6 = tool_x.get_requiredheir(base=test6_text)

    # THEN
    assert required_heir_test6 is None


def test_tool_set_active_status_SetsNullactive_status_hxToNonEmpty():
    # GIVEN
    tool_x = ToolCore(_desc="test4")
    assert tool_x._active_status_hx is None

    # WHEN
    tool_x.set_active_status(tree_traverse_count=3)
    # THEN
    assert tool_x._active_status_hx == {3: True}


def test_tool_set_active_status_IfFullactive_status_hxResetToTrue():
    # GIVEN
    tool_x = ToolCore(_desc="test4")
    tool_x._active_status_hx = {0: True, 4: False}
    assert tool_x._active_status_hx != {0: True}
    # WHEN
    tool_x.set_active_status(tree_traverse_count=0)
    # THEN
    assert tool_x._active_status_hx == {0: True}


# def test_tool_set_active_status_IfFullactive_status_hxResetToFalse():
#     # GIVEN
#     tool_x = ToolCore(_desc="test4")
#     tool_x.set_required_sufffact(
#         base="testing1,second",
#         sufffact="testing1,second,next",
#         open=None,
#         nigh=None,
#         divisor=None,
#     )
#     tool_x._active_status_hx = {0: True, 4: False}
#     assert tool_x._active_status_hx != {0: False}
#     # WHEN
#     tool_x.set_active_status(tree_traverse_count=0)
#     # THEN
#     assert tool_x._active_status_hx == {0: False}


def test_tool_record_active_status_hx_CorrectlyRecordsHistory():
    # GIVEN
    tool_x = ToolCore(_desc="test4")
    assert tool_x._active_status_hx is None

    # WHEN
    tool_x.record_active_status_hx(
        tree_traverse_count=0,
        prev_active_status=None,
        curr_active_status=True,
    )
    # THEN
    assert tool_x._active_status_hx == {0: True}

    # WHEN
    tool_x.record_active_status_hx(
        tree_traverse_count=1,
        prev_active_status=True,
        curr_active_status=True,
    )
    # THEN
    assert tool_x._active_status_hx == {0: True}

    # WHEN
    tool_x.record_active_status_hx(
        tree_traverse_count=2,
        prev_active_status=True,
        curr_active_status=False,
    )
    # THEN
    assert tool_x._active_status_hx == {0: True, 2: False}

    # WHEN
    tool_x.record_active_status_hx(
        tree_traverse_count=3,
        prev_active_status=False,
        curr_active_status=False,
    )
    # THEN
    assert tool_x._active_status_hx == {0: True, 2: False}

    # WHEN
    tool_x.record_active_status_hx(
        tree_traverse_count=4,
        prev_active_status=False,
        curr_active_status=True,
    )
    # THEN
    assert tool_x._active_status_hx == {0: True, 2: False, 4: True}

    # WHEN
    tool_x.record_active_status_hx(
        tree_traverse_count=0,
        prev_active_status=False,
        curr_active_status=False,
    )
    # THEN
    assert tool_x._active_status_hx == {0: False}
