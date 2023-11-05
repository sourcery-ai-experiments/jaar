from src.agenda.examples.example_agendas import get_agenda_with_4_levels
from src.agenda.idea import ideacore_shop
from src.agenda.required_idea import RequiredUnit, acptfactunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.group import balancelink_shop
from pytest import raises as pytest_raises
from src.agenda.road import Road


def test_root_has_kids():
    # GIVEN
    x_agenda = agendaunit_shop(_healer="prom")
    idearoot_x = x_agenda._idearoot
    idea1 = ideacore_shop(_weight=30, _label="work")
    idea2 = ideacore_shop(_weight=40, _label="ulty")

    # WHEN
    x_agenda.add_idea(idea_kid=idea1, pad=x_agenda._healer)
    x_agenda.add_idea(idea_kid=idea2, pad=x_agenda._healer)

    # THEN
    assert idearoot_x._weight == 1
    assert idearoot_x._kids
    assert len(idearoot_x._kids) == 2


def test_kid_can_have_kids():
    # GIVEN / WHEN
    x_agenda = get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

    # THEN
    assert x_agenda._weight == 10
    assert x_agenda._idearoot._kids
    print(f"{len(x_agenda._idearoot._kids)=} {x_agenda._idearoot._pad=}")
    assert x_agenda.get_level_count(level=0) == 1
    weekdays_kids = x_agenda._idearoot._kids["weekdays"]._kids
    weekdays_len = len(weekdays_kids)
    print(f"{weekdays_len=} {x_agenda._idearoot._pad=}")
    # for idea in weekdays_kids.values():
    #     print(f"{idea._label=}")
    assert x_agenda.get_node_count() == 17
    assert x_agenda.get_level_count(level=1) == 4
    assert x_agenda.get_level_count(level=2) == 10
    assert x_agenda.get_level_count(level=3) == 2


def test_agenda_add_idea_CanAddKidToRootIdea():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

    assert x_agenda.get_node_count() == 17
    assert x_agenda.get_level_count(level=1) == 4

    new_idea_parent_road = x_agenda._healer
    new_idea = ideacore_shop(_weight=40, _label="new_idea")

    # WHEN
    x_agenda.add_idea(idea_kid=new_idea, pad=new_idea_parent_road)
    x_agenda.set_agenda_metrics()

    # THEN
    print(f"{(x_agenda._healer == new_idea_parent_road[0])=}")
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert x_agenda.get_node_count() == 18
    assert x_agenda.get_level_count(level=1) == 5


def test_agenda_add_idea_CanAddKidToKidIdea():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

    assert x_agenda.get_node_count() == 17
    assert x_agenda.get_level_count(level=2) == 10

    new_idea_parent_road = f"{x_agenda._culture_title},work"
    new_idea = ideacore_shop(_weight=40, _label="new_york")

    # WHEN
    x_agenda.add_idea(idea_kid=new_idea, pad=new_idea_parent_road)
    x_agenda.set_agenda_metrics()

    # THEN
    # print(f"{(x_agenda._healer == new_idea_parent_road[0])=}")
    # print(x_agenda._idearoot._kids["work"])
    # print(f"{(len(new_idea_parent_road) == 1)=}")
    assert x_agenda.get_node_count() == 18
    assert x_agenda.get_level_count(level=2) == 11
    assert (
        x_agenda._idearoot._kids["work"]._kids["new_york"]._pad
        == f"{x_agenda._culture_title},work"
    )
    x_agenda._idearoot._kids["work"]._kids["new_york"].set_pad(parent_road="testing")
    assert x_agenda._idearoot._kids["work"]._kids["new_york"]._pad == "testing"
    assert x_agenda.get_intent_items


def test_agenda_add_idea_CanAddKidToGrandkidIdea():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

    assert x_agenda.get_node_count() == 17
    assert x_agenda.get_level_count(level=3) == 2
    new_idea_parent_road = f"{x_agenda._culture_title},weekdays,Wednesday"
    new_idea = ideacore_shop(_weight=40, _label="new_idea")

    # WHEN
    x_agenda.add_idea(idea_kid=new_idea, pad=new_idea_parent_road)
    x_agenda.set_agenda_metrics()

    # THEN
    print(f"{(x_agenda._healer == new_idea_parent_road[0])=}")
    print(x_agenda._idearoot._kids["work"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert x_agenda.get_node_count() == 18
    assert x_agenda.get_level_count(level=3) == 3


def test_agenda_add_idea_CanCreateRoadToGrandkidIdea():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

    assert x_agenda.get_node_count() == 17
    assert x_agenda.get_level_count(level=3) == 2
    new_idea_parent_road = f"{x_agenda._culture_title},ww2,battles,coralsea"
    new_idea = ideacore_shop(_weight=40, _label="USS Saratoga")

    # WHEN
    x_agenda.add_idea(idea_kid=new_idea, pad=new_idea_parent_road)
    x_agenda.set_agenda_metrics()

    # THEN
    print(x_agenda._idearoot._kids["ww2"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert x_agenda._idearoot._kids["ww2"]._label == "ww2"
    assert x_agenda._idearoot._kids["ww2"]._kids["battles"]._label == "battles"
    assert x_agenda.get_node_count() == 21
    assert x_agenda.get_level_count(level=3) == 3


def test_agenda_add_idea_creates_requireds_ideas():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

    assert x_agenda.get_node_count() == 17
    assert x_agenda.get_level_count(level=3) == 2
    new_idea_parent_road = f"{x_agenda._culture_title},work,cleaning"
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideacore_shop(
        _weight=40, _label=clean_cookery_text, promise=True
    )

    buildings_text = "buildings"
    buildings_road = Road(f"{x_agenda._culture_title},{buildings_text}")
    cookery_room_text = "cookery"
    cookery_room_road = Road(
        f"{x_agenda._culture_title},{buildings_text},{cookery_room_text}"
    )
    cookery_dirty_text = "dirty"
    cookery_dirty_road = Road(f"{cookery_room_road},{cookery_dirty_text}")
    required_x = RequiredUnit(base=cookery_room_road, sufffacts={})
    required_x.set_sufffact(sufffact=cookery_dirty_road)
    clean_cookery_idea.set_required_unit(required=required_x)

    assert x_agenda._idearoot._kids.get(buildings_text) is None

    # WHEN
    x_agenda.add_idea(
        idea_kid=clean_cookery_idea,
        pad=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )
    x_agenda.set_agenda_metrics()

    # THEN
    print(f"{(len(new_idea_parent_road) == 1)=}")
    # for idea_kid in x_agenda._idearoot._kids.values():
    #     print(f"{idea_kid._label=}")
    assert x_agenda._idearoot._kids.get(buildings_text) != None
    assert x_agenda.get_idea_kid(road=buildings_road) != None
    assert x_agenda.get_idea_kid(road=cookery_dirty_road) != None
    assert x_agenda.get_node_count() == 22
    assert x_agenda.get_level_count(level=3) == 4


def test_agenda_idearoot_is_heir_CorrectlyChecksLineage():
    x_agenda = get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()

    week_text = "weekdays"
    week_road = f"{x_agenda._culture_title},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"
    assert x_agenda._idearoot.is_heir(src=week_road, heir=week_road)
    assert x_agenda._idearoot.is_heir(src=week_road, heir=sun_road)
    assert x_agenda._idearoot.is_heir(src=sun_road, heir=week_road) == False


def test_agenda_del_idea_kid_Level0CannotBeDeleted():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    root_road = f"{x_agenda._culture_title}"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.del_idea_kid(road=root_road)
    assert str(excinfo.value) == "Object cannot delete itself"


def test_agenda_del_idea_kid_Level1CanBeDeleted_ChildrenDeleted():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    week_text = "weekdays"
    week_road = f"{x_agenda._culture_title},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"
    assert x_agenda.get_idea_kid(road=week_road)
    assert x_agenda.get_idea_kid(road=sun_road)

    # WHEN
    x_agenda.del_idea_kid(road=week_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.get_idea_kid(road=week_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='weekdays' failed no item at '{week_road}'"
    )
    new_sunday_road = f"{x_agenda._culture_title},Sunday"
    with pytest_raises(Exception) as excinfo:
        x_agenda.get_idea_kid(road=new_sunday_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='Sunday' failed no item at '{new_sunday_road}'"
    )


def test_agenda_del_idea_kid_Level1CanBeDeleted_ChildrenInherited():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    x_agenda.set_agenda_metrics()
    week_text = "weekdays"
    week_road = f"{x_agenda._culture_title},{week_text}"
    sun_text = "Sunday"
    old_sunday_road = f"{week_road},{sun_text}"
    assert x_agenda.get_idea_kid(road=old_sunday_road)

    # WHEN
    x_agenda.del_idea_kid(road=week_road, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.get_idea_kid(road=old_sunday_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='{sun_text}' failed no item at '{old_sunday_road}'"
    )
    new_sunday_road = f"{x_agenda._culture_title},{sun_text}"
    assert x_agenda.get_idea_kid(road=new_sunday_road)
    new_sunday_idea = x_agenda.get_idea_kid(road=new_sunday_road)
    assert new_sunday_idea._pad == x_agenda._culture_title


def test_agenda_del_idea_kid_LevelNCanBeDeleted_ChildrenInherited():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    states_text = "nation-state"
    states_road = f"{x_agenda._culture_title},{states_text}"
    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    texas_text = "Texas"
    oregon_text = "Oregon"
    usa_texas_road = f"{usa_road},{texas_text}"
    usa_oregon_road = f"{usa_road},{oregon_text}"
    states_texas_road = f"{states_road},{texas_text}"
    states_oregon_road = f"{states_road},{oregon_text}"
    x_agenda.set_agenda_metrics()
    assert x_agenda._idea_dict.get(usa_road) != None
    assert x_agenda._idea_dict.get(usa_texas_road) != None
    assert x_agenda._idea_dict.get(usa_oregon_road) != None
    assert x_agenda._idea_dict.get(states_texas_road) is None
    assert x_agenda._idea_dict.get(states_oregon_road) is None

    # WHEN
    x_agenda.del_idea_kid(road=usa_road, del_children=False)

    # THEN
    x_agenda.set_agenda_metrics()
    assert x_agenda._idea_dict.get(states_texas_road) != None
    assert x_agenda._idea_dict.get(states_oregon_road) != None
    assert x_agenda._idea_dict.get(usa_texas_road) is None
    assert x_agenda._idea_dict.get(usa_oregon_road) is None
    assert x_agenda._idea_dict.get(usa_road) is None


def test_agenda_del_idea_kid_Level2CanBeDeleted_ChildrenDeleted():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    monday_road = f"{x_agenda._culture_title},weekdays,Monday"
    assert x_agenda.get_idea_kid(road=monday_road)

    # WHEN
    x_agenda.del_idea_kid(road=monday_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.get_idea_kid(road=monday_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='Monday' failed no item at '{monday_road}'"
    )


def test_agenda_del_idea_kid_LevelNCanBeDeleted_ChildrenDeleted():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()
    states_text = "nation-state"
    states_road = f"{x_agenda._culture_title},{states_text}"
    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    texas_text = "Texas"
    usa_texas_road = f"{usa_road},{texas_text}"
    assert x_agenda.get_idea_kid(road=usa_texas_road)

    # WHEN
    x_agenda.del_idea_kid(road=usa_texas_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.get_idea_kid(road=usa_texas_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='Texas' failed no item at '{usa_texas_road}'"
    )


def test_agenda_edit_idea_attr_IsAbleToEditAnyAncestor_Idea():
    x_agenda = get_agenda_with_4_levels()
    work_text = "work"
    work_road = f"{x_agenda._culture_title},{work_text}"
    print(f"{work_road=}")
    current_weight = x_agenda._idearoot._kids[work_text]._weight
    assert current_weight == 30
    x_agenda.edit_idea_attr(road=work_road, weight=23)
    new_weight = x_agenda._idearoot._kids[work_text]._weight
    assert new_weight == 23

    # uid: int = None,
    x_agenda._idearoot._kids[work_text]._uid = 34
    uid_curr = x_agenda._idearoot._kids[work_text]._uid
    assert uid_curr == 34
    x_agenda.edit_idea_attr(road=work_road, uid=23)
    uid_new = x_agenda._idearoot._kids[work_text]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    x_agenda._idearoot._kids[work_text]._begin = 39
    begin_curr = x_agenda._idearoot._kids[work_text]._begin
    assert begin_curr == 39
    x_agenda._idearoot._kids[work_text]._close = 43
    close_curr = x_agenda._idearoot._kids[work_text]._close
    assert close_curr == 43
    x_agenda.edit_idea_attr(road=work_road, begin=25, close=29)
    assert x_agenda._idearoot._kids[work_text]._begin == 25
    assert x_agenda._idearoot._kids[work_text]._close == 29

    # acptfactunit: acptfactunit_shop = None,
    # x_agenda._idearoot._kids[work_text]._acptfactunits = None
    assert x_agenda._idearoot._kids[work_text]._acptfactunits is None
    acptfact_road = f"{x_agenda._culture_title},weekdays,Sunday"
    acptfactunit_x = acptfactunit_shop(base=acptfact_road, pick=acptfact_road)

    work_acptfactunits = x_agenda._idearoot._kids[work_text]._acptfactunits
    print(f"{work_acptfactunits=}")
    x_agenda.edit_idea_attr(road=work_road, acptfactunit=acptfactunit_x)
    work_acptfactunits = x_agenda._idearoot._kids[work_text]._acptfactunits
    print(f"{work_acptfactunits=}")
    assert x_agenda._idearoot._kids[work_text]._acptfactunits == {
        acptfactunit_x.base: acptfactunit_x
    }

    # _descendant_promise_count: int = None,
    x_agenda._idearoot._kids[work_text]._descendant_promise_count = 81
    _descendant_promise_count_curr = x_agenda._idearoot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_curr == 81
    x_agenda.edit_idea_attr(road=work_road, descendant_promise_count=67)
    _descendant_promise_count_new = x_agenda._idearoot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_new == 67

    # _all_party_credit: bool = None,
    x_agenda._idearoot._kids[work_text]._all_party_credit = 74
    _all_party_credit_curr = x_agenda._idearoot._kids[work_text]._all_party_credit
    assert _all_party_credit_curr == 74
    x_agenda.edit_idea_attr(road=work_road, all_party_credit=59)
    _all_party_credit_new = x_agenda._idearoot._kids[work_text]._all_party_credit
    assert _all_party_credit_new == 59

    # _all_party_debt: bool = None,
    x_agenda._idearoot._kids[work_text]._all_party_debt = 74
    _all_party_debt_curr = x_agenda._idearoot._kids[work_text]._all_party_debt
    assert _all_party_debt_curr == 74
    x_agenda.edit_idea_attr(road=work_road, all_party_debt=59)
    _all_party_debt_new = x_agenda._idearoot._kids[work_text]._all_party_debt
    assert _all_party_debt_new == 59

    # _balancelink: dict = None,
    x_agenda._idearoot._kids[work_text]._balancelinks = {
        "fun": balancelink_shop(brand="fun", creditor_weight=1, debtor_weight=7)
    }
    _balancelinks = x_agenda._idearoot._kids[work_text]._balancelinks
    assert _balancelinks == {
        "fun": balancelink_shop(brand="fun", creditor_weight=1, debtor_weight=7)
    }
    x_agenda.edit_idea_attr(
        road=work_road,
        balancelink=balancelink_shop(brand="fun", creditor_weight=4, debtor_weight=8),
    )
    assert x_agenda._idearoot._kids[work_text]._balancelinks == {
        "fun": balancelink_shop(brand="fun", creditor_weight=4, debtor_weight=8)
    }

    # _is_expanded: dict = None,
    x_agenda._idearoot._kids[work_text]._is_expanded = "what"
    _is_expanded = x_agenda._idearoot._kids[work_text]._is_expanded
    assert _is_expanded == "what"
    x_agenda.edit_idea_attr(road=work_road, is_expanded=True)
    assert x_agenda._idearoot._kids[work_text]._is_expanded == True

    # promise: dict = None,
    x_agenda._idearoot._kids[work_text].promise = "funfun3"
    action = x_agenda._idearoot._kids[work_text].promise
    assert action == "funfun3"
    x_agenda.edit_idea_attr(road=work_road, promise=True)
    assert x_agenda._idearoot._kids[work_text].promise == True

    # _problem_bool
    x_agenda._idearoot._kids[work_text]._problem_bool = "heat2"
    _problem_bool = x_agenda._idearoot._kids[work_text]._problem_bool
    assert _problem_bool == "heat2"
    x_agenda.edit_idea_attr(road=work_road, problem_bool=True)
    assert x_agenda._idearoot._kids[work_text]._problem_bool == True

    # _range_source_road: dict = None,
    x_agenda._idearoot._kids[work_text]._range_source_road = "fun3rol"
    range_source_road = x_agenda._idearoot._kids[work_text]._range_source_road
    assert range_source_road == "fun3rol"
    x_agenda.edit_idea_attr(road=work_road, range_source_road="my,work,end")
    assert x_agenda._idearoot._kids[work_text]._range_source_road == "my,work,end"


def test_agenda_edit_idea_attr_agendaIsAbleToEdit_on_meld_weight_action_AnyIdeaIfInvaildThrowsError():
    x_agenda = get_agenda_with_4_levels()
    work_road = f"{x_agenda._culture_title},work"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_attr(road=work_road, on_meld_weight_action="yahoo9")
    assert (
        str(excinfo.value)
        == "IdeaCore unit 'work' cannot have on_meld_weight_action 'yahoo9'."
    )


def test_agenda_edit_idea_attr_agendaIsAbleToEditDenomAnyIdeaIfInvaildDenomThrowsError():
    healer_text = "Yao"
    x_agenda = agendaunit_shop(_healer=healer_text)
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_attr(road="", denom=46)
    assert str(excinfo.value) == "Root Idea cannot have numor denom reest."

    work = "work"
    w_road = f"{x_agenda._culture_title},{work}"
    work_idea = ideacore_shop(_label=work)
    x_agenda.add_idea(work_idea, pad=x_agenda._culture_title)
    clean = "clean"
    clean_idea = ideacore_shop(_label=clean)
    c_road = f"{w_road},{clean}"
    x_agenda.add_idea(clean_idea, pad=w_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_attr(road=c_road, denom=46)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{x_agenda._culture_title},work,clean' if parent '{x_agenda._culture_title},work' or ideacore._numeric_road does not have begin/close range"
    )

    # GIVEN
    x_agenda.edit_idea_attr(road=w_road, begin=44, close=110)
    x_agenda.edit_idea_attr(road=c_road, denom=11)
    clean_idea = x_agenda.get_idea_kid(road=c_road)
    assert clean_idea._begin == 4
    assert clean_idea._close == 10


def test_agenda_edit_idea_attr_agendaIsAbleToEditDenomAnyIdeaInvaildDenomThrowsError():
    # GIVEN
    healer_text = "Yao"
    x_agenda = agendaunit_shop(_healer=healer_text)
    work = "work"
    w_road = f"{x_agenda._culture_title},{work}"
    work_idea = ideacore_shop(_label=work, _begin=8, _close=14)
    x_agenda.add_idea(work_idea, pad=x_agenda._culture_title)

    clean = "clean"
    clean_idea = ideacore_shop(_label=clean, _denom=1)
    c_road = f"{w_road},{clean}"
    x_agenda.add_idea(clean_idea, pad=w_road)

    clean_idea = x_agenda.get_idea_kid(road=c_road)

    day = "day_range"
    day_idea = ideacore_shop(_label=day, _begin=44, _close=110)
    day_road = f"{x_agenda._culture_title},{day}"
    x_agenda.add_idea(day_idea, pad=x_agenda._culture_title)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_attr(road=c_road, numeric_road=day_road)
    assert (
        str(excinfo.value)
        == "Idea has begin-close range parent, cannot have numeric_road"
    )

    x_agenda.edit_idea_attr(road=w_road, numeric_road=day_road)


def test_agenda_edit_idea_attr_agendaWhenParentAndNumeric_roadBothHaveRangeThrowError():
    # GIVEN
    healer_text = "Yao"
    x_agenda = agendaunit_shop(_healer=healer_text)
    work_text = "work"
    work_road = f"{x_agenda._culture_title},{work_text}"
    x_agenda.add_idea(ideacore_shop(_label=work_text), pad=x_agenda._culture_title)
    day_text = "day_range"
    day_idea = ideacore_shop(_label=day_text, _begin=44, _close=110)
    day_road = f"{x_agenda._culture_title},{day_text}"
    x_agenda.add_idea(day_idea, pad=x_agenda._culture_title)

    work_idea = x_agenda.get_idea_kid(road=work_road)
    assert work_idea._begin is None
    assert work_idea._close is None

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.edit_idea_attr(road=work_road, denom=11)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{x_agenda._culture_title},work' if parent '{x_agenda._culture_title}' or ideacore._numeric_road does not have begin/close range"
    )

    # WHEN
    x_agenda.edit_idea_attr(road=work_road, numeric_road=day_road)

    # THEN
    work_idea3 = x_agenda.get_idea_kid(road=work_road)
    assert work_idea3._addin is None
    assert work_idea3._numor is None
    assert work_idea3._denom is None
    assert work_idea3._reest is None
    assert work_idea3._begin == 44
    assert work_idea3._close == 110
    x_agenda.edit_idea_attr(road=work_road, denom=11, numeric_road=day_road)
    assert work_idea3._begin == 4
    assert work_idea3._close == 10
    assert work_idea3._numor == 1
    assert work_idea3._denom == 11
    assert work_idea3._reest == False
    assert work_idea3._addin == 0


def test_agenda_add_idea_MustReorderKidsDictToBeAlphabetical():
    # GIVEN
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    work_text = "work"
    x_agenda.add_idea(ideacore_shop(_label=work_text), pad=x_agenda._culture_title)
    swim_text = "swim"
    x_agenda.add_idea(ideacore_shop(_label=swim_text), pad=x_agenda._culture_title)

    # WHEN
    idea_list = list(x_agenda._idearoot._kids.values())

    # THEN
    assert idea_list[0]._label == swim_text


def test_agenda_add_idea_adoptee_RaisesErrorIfAdopteeIdeaDoesNotHaveCorrectParent():
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    sports_text = "sports"
    sports_road = f"{x_agenda._culture_title},{sports_text}"
    x_agenda.add_idea(ideacore_shop(_label=sports_text), pad=x_agenda._culture_title)
    swim_text = "swim"
    x_agenda.add_idea(ideacore_shop(_label=swim_text), pad=sports_road)

    # WHEN / THEN
    summer_text = "summer"
    hike_text = "hike"
    hike_road = f"{sports_road},{hike_text}"
    with pytest_raises(Exception) as excinfo:
        x_agenda.add_idea(
            idea_kid=ideacore_shop(_label=summer_text),
            pad=sports_road,
            adoptees=[swim_text, hike_text],
        )
    assert (
        str(excinfo.value)
        == f"Getting idea_label='{hike_text}' failed no item at '{hike_road}'"
    )


def test_agenda_add_idea_adoptee_CorrectlyAddsAdoptee():
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    sports_text = "sports"
    sports_road = f"{x_agenda._culture_title},{sports_text}"
    x_agenda.add_idea(ideacore_shop(_label=sports_text), pad=x_agenda._culture_title)
    swim_text = "swim"
    x_agenda.add_idea(ideacore_shop(_label=swim_text), pad=sports_road)
    hike_text = "hike"
    x_agenda.add_idea(ideacore_shop(_label=hike_text), pad=sports_road)

    x_agenda.set_agenda_metrics()
    sports_swim_road = f"{sports_road},{swim_text}"
    sports_hike_road = f"{sports_road},{hike_text}"
    assert x_agenda._idea_dict.get(sports_swim_road) != None
    assert x_agenda._idea_dict.get(sports_hike_road) != None
    summer_text = "summer"
    summer_road = f"{sports_road},{summer_text}"
    summer_swim_road = f"{summer_road},{swim_text}"
    summer_hike_road = f"{summer_road},{hike_text}"
    assert x_agenda._idea_dict.get(summer_swim_road) is None
    assert x_agenda._idea_dict.get(summer_hike_road) is None

    # WHEN / THEN
    x_agenda.add_idea(
        idea_kid=ideacore_shop(_label=summer_text),
        pad=sports_road,
        adoptees=[swim_text, hike_text],
    )

    # THEN
    summer_idea = x_agenda.get_idea_kid(summer_road)
    print(f"{summer_idea._kids.keys()=}")
    x_agenda.set_agenda_metrics()
    assert x_agenda._idea_dict.get(summer_swim_road) != None
    assert x_agenda._idea_dict.get(summer_hike_road) != None
    assert x_agenda._idea_dict.get(sports_swim_road) is None
    assert x_agenda._idea_dict.get(sports_hike_road) is None


def test_agenda_add_idea_bundling_SetsNewParentWithWeightEqualToSumOfAdoptedIdeas():
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    sports_text = "sports"
    sports_road = f"{x_agenda._culture_title},{sports_text}"
    x_agenda.add_idea(
        ideacore_shop(_label=sports_text, _weight=2), pad=x_agenda._culture_title
    )
    swim_text = "swim"
    swim_weight = 3
    x_agenda.add_idea(
        ideacore_shop(_label=swim_text, _weight=swim_weight), pad=sports_road
    )
    hike_text = "hike"
    hike_weight = 5
    x_agenda.add_idea(
        ideacore_shop(_label=hike_text, _weight=hike_weight), pad=sports_road
    )
    bball_text = "bball"
    bball_weight = 7
    x_agenda.add_idea(
        ideacore_shop(_label=bball_text, _weight=bball_weight), pad=sports_road
    )

    x_agenda.set_agenda_metrics()
    sports_swim_road = f"{sports_road},{swim_text}"
    sports_hike_road = f"{sports_road},{hike_text}"
    sports_bball_road = f"{sports_road},{bball_text}"
    assert x_agenda._idea_dict.get(sports_swim_road)._weight == swim_weight
    assert x_agenda._idea_dict.get(sports_hike_road)._weight == hike_weight
    assert x_agenda._idea_dict.get(sports_bball_road)._weight == bball_weight
    summer_text = "summer"
    summer_road = f"{sports_road},{summer_text}"
    summer_swim_road = f"{summer_road},{swim_text}"
    summer_hike_road = f"{summer_road},{hike_text}"
    summer_bball_road = f"{summer_road},{bball_text}"
    assert x_agenda._idea_dict.get(summer_swim_road) is None
    assert x_agenda._idea_dict.get(summer_hike_road) is None
    assert x_agenda._idea_dict.get(summer_bball_road) is None

    # WHEN / THEN
    x_agenda.add_idea(
        idea_kid=ideacore_shop(_label=summer_text),
        pad=sports_road,
        adoptees=[swim_text, hike_text],
        bundling=True,
    )

    # THEN
    x_agenda.set_agenda_metrics()
    assert x_agenda._idea_dict.get(summer_road)._weight == swim_weight + hike_weight
    assert x_agenda._idea_dict.get(summer_swim_road)._weight == swim_weight
    assert x_agenda._idea_dict.get(summer_hike_road)._weight == hike_weight
    assert x_agenda._idea_dict.get(summer_bball_road) is None
    assert x_agenda._idea_dict.get(sports_swim_road) is None
    assert x_agenda._idea_dict.get(sports_hike_road) is None
    assert x_agenda._idea_dict.get(sports_bball_road) != None


def test_agenda_del_idea_kid_DeletingBundledIdeaReturnsIdeasToOriginalState():
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text)
    sports_text = "sports"
    sports_road = f"{x_agenda._culture_title},{sports_text}"
    x_agenda.add_idea(
        ideacore_shop(_label=sports_text, _weight=2), pad=x_agenda._culture_title
    )
    swim_text = "swim"
    swim_weight = 3
    x_agenda.add_idea(
        ideacore_shop(_label=swim_text, _weight=swim_weight), pad=sports_road
    )
    hike_text = "hike"
    hike_weight = 5
    x_agenda.add_idea(
        ideacore_shop(_label=hike_text, _weight=hike_weight), pad=sports_road
    )
    bball_text = "bball"
    bball_weight = 7
    x_agenda.add_idea(
        ideacore_shop(_label=bball_text, _weight=bball_weight), pad=sports_road
    )

    x_agenda.set_agenda_metrics()
    sports_swim_road = f"{sports_road},{swim_text}"
    sports_hike_road = f"{sports_road},{hike_text}"
    sports_bball_road = f"{sports_road},{bball_text}"
    assert x_agenda._idea_dict.get(sports_swim_road)._weight == swim_weight
    assert x_agenda._idea_dict.get(sports_hike_road)._weight == hike_weight
    assert x_agenda._idea_dict.get(sports_bball_road)._weight == bball_weight
    summer_text = "summer"
    summer_road = f"{sports_road},{summer_text}"
    summer_swim_road = f"{summer_road},{swim_text}"
    summer_hike_road = f"{summer_road},{hike_text}"
    summer_bball_road = f"{summer_road},{bball_text}"
    assert x_agenda._idea_dict.get(summer_swim_road) is None
    assert x_agenda._idea_dict.get(summer_hike_road) is None
    assert x_agenda._idea_dict.get(summer_bball_road) is None
    x_agenda.add_idea(
        idea_kid=ideacore_shop(_label=summer_text),
        pad=sports_road,
        adoptees=[swim_text, hike_text],
        bundling=True,
    )
    x_agenda.set_agenda_metrics()
    assert x_agenda._idea_dict.get(summer_road)._weight == swim_weight + hike_weight
    assert x_agenda._idea_dict.get(summer_swim_road)._weight == swim_weight
    assert x_agenda._idea_dict.get(summer_hike_road)._weight == hike_weight
    assert x_agenda._idea_dict.get(summer_bball_road) is None
    assert x_agenda._idea_dict.get(sports_swim_road) is None
    assert x_agenda._idea_dict.get(sports_hike_road) is None
    assert x_agenda._idea_dict.get(sports_bball_road) != None
    print(f"{x_agenda._idea_dict.keys()=}")

    # WHEN
    x_agenda.del_idea_kid(road=summer_road, del_children=False)

    # THEN
    x_agenda.set_agenda_metrics()
    print(f"{x_agenda._idea_dict.keys()=}")
    assert x_agenda._idea_dict.get(sports_swim_road)._weight == swim_weight
    assert x_agenda._idea_dict.get(sports_hike_road)._weight == hike_weight
    assert x_agenda._idea_dict.get(sports_bball_road)._weight == bball_weight
