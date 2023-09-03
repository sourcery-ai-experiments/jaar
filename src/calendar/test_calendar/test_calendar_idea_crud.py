from src.calendar.examples.example_calendars import get_calendar_with_4_levels
from src.calendar.idea import IdeaKid
from src.calendar.required_idea import RequiredUnit, acptfactunit_shop
from src.calendar.calendar import CalendarUnit
from src.calendar.group import grouplink_shop
from pytest import raises as pytest_raises
from src.calendar.road import Road


def test_root_has_kids():
    # GIVEN
    calendar_x = CalendarUnit(_owner="prom")
    idearoot_x = calendar_x._idearoot
    idea1 = IdeaKid(_weight=30, _desc="work")
    idea2 = IdeaKid(_weight=40, _desc="ulty")

    # WHEN
    calendar_x.add_idea(idea_kid=idea1, walk=calendar_x._owner)
    calendar_x.add_idea(idea_kid=idea2, walk=calendar_x._owner)

    # THEN
    assert idearoot_x._weight == 1
    assert idearoot_x._kids
    assert len(idearoot_x._kids) == 2


def test_kid_can_have_kids():
    # GIVEN/WHEN
    calendar_x = get_calendar_with_4_levels()

    # THEN
    assert calendar_x._weight == 10
    assert calendar_x._idearoot._kids
    print(f"{len(calendar_x._idearoot._kids)=} {calendar_x._idearoot._walk=}")
    assert calendar_x.get_level_count(level=0) == 1
    weekdays_kids = calendar_x._idearoot._kids["weekdays"]._kids
    weekdays_len = len(weekdays_kids)
    print(f"{weekdays_len=} {calendar_x._idearoot._walk=}")
    # for idea in weekdays_kids.values():
    #     print(f"{idea._desc=}")
    assert calendar_x.get_node_count() == 17
    assert calendar_x.get_level_count(level=1) == 4
    assert calendar_x.get_level_count(level=2) == 10
    assert calendar_x.get_level_count(level=3) == 2


def test_calendar_add_idea_CanAddKidToRootIdea():
    # GIVEN
    calendar_x = get_calendar_with_4_levels()
    assert calendar_x.get_node_count() == 17
    assert calendar_x.get_level_count(level=1) == 4

    new_idea_parent_road = calendar_x._owner
    new_idea = IdeaKid(_weight=40, _desc="new_idea")

    # WHEN
    calendar_x.add_idea(idea_kid=new_idea, walk=new_idea_parent_road)

    # THEN
    print(f"{(calendar_x._owner == new_idea_parent_road[0])=}")
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert calendar_x.get_node_count() == 18
    assert calendar_x.get_level_count(level=1) == 5


def test_calendar_add_idea_CanAddKidToKidIdea():
    # GIVEN
    calendar_x = get_calendar_with_4_levels()
    assert calendar_x.get_node_count() == 17
    assert calendar_x.get_level_count(level=2) == 10

    new_idea_parent_road = f"{calendar_x._owner},work"
    new_idea = IdeaKid(_weight=40, _desc="new_york")

    # WHEN
    calendar_x.add_idea(idea_kid=new_idea, walk=new_idea_parent_road)

    # THEN
    # print(f"{(calendar_x._owner == new_idea_parent_road[0])=}")
    # print(calendar_x._idearoot._kids["work"])
    # print(f"{(len(new_idea_parent_road) == 1)=}")
    assert calendar_x.get_node_count() == 18
    assert calendar_x.get_level_count(level=2) == 11
    assert (
        calendar_x._idearoot._kids["work"]._kids["new_york"]._walk
        == f"{calendar_x._owner},work"
    )
    calendar_x._idearoot._kids["work"]._kids["new_york"].set_road(parent_road="testing")
    assert calendar_x._idearoot._kids["work"]._kids["new_york"]._walk == "testing"
    assert calendar_x.get_agenda_items


def test_calendar_add_idea_CanAddKidToGrandkidIdea():
    # GIVEN
    calendar_x = get_calendar_with_4_levels()
    assert calendar_x.get_node_count() == 17
    assert calendar_x.get_level_count(level=3) == 2
    new_idea_parent_road = f"{calendar_x._owner},weekdays,Wednesday"
    new_idea = IdeaKid(_weight=40, _desc="new_idea")

    # WHEN
    calendar_x.add_idea(idea_kid=new_idea, walk=new_idea_parent_road)

    # THEN
    print(f"{(calendar_x._owner == new_idea_parent_road[0])=}")
    print(calendar_x._idearoot._kids["work"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert calendar_x.get_node_count() == 18
    assert calendar_x.get_level_count(level=3) == 3


def test_calendar_add_idea_CanCreateRoadToGrandkidIdea():
    # GIVEN
    calendar_x = get_calendar_with_4_levels()
    assert calendar_x.get_node_count() == 17
    assert calendar_x.get_level_count(level=3) == 2
    new_idea_parent_road = f"{calendar_x._owner},ww2,battles,coralsea"
    new_idea = IdeaKid(_weight=40, _desc="USS Saratoga")

    # WHEN
    calendar_x.add_idea(idea_kid=new_idea, walk=new_idea_parent_road)

    # THEN
    print(calendar_x._idearoot._kids["ww2"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert calendar_x._idearoot._kids["ww2"]._desc == "ww2"
    assert calendar_x._idearoot._kids["ww2"]._kids["battles"]._desc == "battles"
    assert calendar_x.get_node_count() == 21
    assert calendar_x.get_level_count(level=3) == 3


def test_calendar_add_idea_creates_requireds_ideas():
    # GIVEN
    calendar_x = get_calendar_with_4_levels()
    assert calendar_x.get_node_count() == 17
    assert calendar_x.get_level_count(level=3) == 2
    src_text = calendar_x._idearoot._desc
    new_idea_parent_road = f"{src_text},work,cleaning"
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = IdeaKid(_weight=40, _desc=clean_cookery_text, promise=True)

    buildings_text = "buildings"
    buildings_road = Road(f"{src_text},{buildings_text}")
    cookery_room_text = "cookery"
    cookery_room_road = Road(f"{src_text},{buildings_text},{cookery_room_text}")
    cookery_dirty_text = "dirty"
    cookery_dirty_road = Road(f"{cookery_room_road},{cookery_dirty_text}")
    required_x = RequiredUnit(base=cookery_room_road, sufffacts={})
    required_x.set_sufffact(sufffact=cookery_dirty_road)
    clean_cookery_idea.set_required_unit(required=required_x)

    assert calendar_x._idearoot._kids.get(buildings_text) is None

    # WHEN
    calendar_x.add_idea(
        idea_kid=clean_cookery_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )

    # THEN
    print(f"{(len(new_idea_parent_road) == 1)=}")
    # for idea_kid in calendar_x._idearoot._kids.values():
    #     print(f"{idea_kid._desc=}")
    assert calendar_x._idearoot._kids.get(buildings_text) != None
    assert calendar_x.get_idea_kid(road=buildings_road) != None
    assert calendar_x.get_idea_kid(road=cookery_dirty_road) != None
    assert calendar_x.get_node_count() == 22
    assert calendar_x.get_level_count(level=3) == 4


def test_calendar_idearoot_is_heir_CorrectlyChecksLineage():
    calendar_x = get_calendar_with_4_levels()
    sunday_road = f"{calendar_x._owner},weekdays,Sunday"
    weekday_road = f"{calendar_x._owner},weekdays"
    assert calendar_x._idearoot.is_heir(src=weekday_road, heir=weekday_road)
    assert calendar_x._idearoot.is_heir(src=weekday_road, heir=sunday_road)
    assert calendar_x._idearoot.is_heir(src=sunday_road, heir=weekday_road) == False


def test_calendar_del_idea_kid_IdeaLevel0CannotBeDeleted():
    # Given
    calendar_x = get_calendar_with_4_levels()
    root_road = f"{calendar_x._owner}"

    # When/Then
    with pytest_raises(Exception) as excinfo:
        calendar_x.del_idea_kid(road=root_road)
    assert str(excinfo.value) == "Object cannot delete itself"


def test_calendar_del_idea_kid_IdeaLevel1CanBeDeleted_ChildrenDeleted():
    # Given
    calendar_x = get_calendar_with_4_levels()
    weekdays_road = f"{calendar_x._owner},weekdays"
    sunday_road = f"{calendar_x._owner},weekdays,Sunday"
    assert calendar_x.get_idea_kid(road=weekdays_road)
    assert calendar_x.get_idea_kid(road=sunday_road)

    # When
    calendar_x.del_idea_kid(road=weekdays_road)

    # Then
    with pytest_raises(Exception) as excinfo:
        calendar_x.get_idea_kid(road=weekdays_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_desc='weekdays' failed no item at '{weekdays_road}'"
    )
    new_sunday_road = f"{calendar_x._owner},Sunday"
    with pytest_raises(Exception) as excinfo:
        calendar_x.get_idea_kid(road=new_sunday_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_desc='Sunday' failed no item at '{new_sunday_road}'"
    )


def test_calendar_del_idea_kid_IdeaLevel1CanBeDeleted_ChildrenInherited():
    # Given
    calendar_x = get_calendar_with_4_levels()
    weekdays_road = f"{calendar_x._owner},weekdays"
    old_sunday_road = f"{calendar_x._owner},weekdays,Sunday"
    assert calendar_x.get_idea_kid(road=old_sunday_road)

    # When
    calendar_x.del_idea_kid(road=weekdays_road, del_children=False)

    # Then
    with pytest_raises(Exception) as excinfo:
        calendar_x.get_idea_kid(road=old_sunday_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_desc='Sunday' failed no item at '{old_sunday_road}'"
    )
    new_sunday_road = f"{calendar_x._owner},Sunday"
    assert calendar_x.get_idea_kid(road=new_sunday_road)
    new_sunday_idea = calendar_x.get_idea_kid(road=new_sunday_road)
    assert new_sunday_idea._walk == f"{calendar_x._owner}"


def test_calendar_del_idea_kid_IdeaLevel2CanBeDeleted_ChildrenDeleted():
    # Given
    calendar_x = get_calendar_with_4_levels()
    monday_road = f"{calendar_x._owner},weekdays,Monday"
    assert calendar_x.get_idea_kid(road=monday_road)

    # When
    calendar_x.del_idea_kid(road=monday_road)

    # Then
    with pytest_raises(Exception) as excinfo:
        calendar_x.get_idea_kid(road=monday_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_desc='Monday' failed no item at '{monday_road}'"
    )


def test_calendar_del_idea_kid_IdeaLevelNCanBeDeleted_ChildrenDeleted():
    # Given
    calendar_x = get_calendar_with_4_levels()
    states = "nation-state"
    USA = "USA"
    Texas = "Texas"
    texas_road = f"{calendar_x._owner},{states},{USA},{Texas}"
    assert calendar_x.get_idea_kid(road=texas_road)

    # When
    calendar_x.del_idea_kid(road=texas_road)

    # Then
    with pytest_raises(Exception) as excinfo:
        calendar_x.get_idea_kid(road=texas_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_desc='Texas' failed no item at '{texas_road}'"
    )


def test_calendar_edit_idea_attr_IsAbleToEditAnyAncestor_Idea():
    calendar_x = get_calendar_with_4_levels()
    work_text = "work"
    work_road = f"{calendar_x._owner},{work_text}"
    print(f"{work_road=}")
    current_weight = calendar_x._idearoot._kids[work_text]._weight
    assert current_weight == 30
    calendar_x.edit_idea_attr(road=work_road, weight=23)
    new_weight = calendar_x._idearoot._kids[work_text]._weight
    assert new_weight == 23

    # uid: int = None,
    calendar_x._idearoot._kids[work_text]._uid = 34
    uid_curr = calendar_x._idearoot._kids[work_text]._uid
    assert uid_curr == 34
    calendar_x.edit_idea_attr(road=work_road, uid=23)
    uid_new = calendar_x._idearoot._kids[work_text]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    calendar_x._idearoot._kids[work_text]._begin = 39
    begin_curr = calendar_x._idearoot._kids[work_text]._begin
    assert begin_curr == 39
    calendar_x._idearoot._kids[work_text]._close = 43
    close_curr = calendar_x._idearoot._kids[work_text]._close
    assert close_curr == 43
    calendar_x.edit_idea_attr(road=work_road, begin=25, close=29)
    assert calendar_x._idearoot._kids[work_text]._begin == 25
    assert calendar_x._idearoot._kids[work_text]._close == 29

    # acptfactunit: acptfactunit_shop = None,
    # calendar_x._idearoot._kids[work_text]._acptfactunits = None
    assert calendar_x._idearoot._kids[work_text]._acptfactunits is None
    acptfact_road = "src,weekdays,Sunday"
    acptfactunit_x = acptfactunit_shop(base=acptfact_road, pick=acptfact_road)

    work_acptfactunits = calendar_x._idearoot._kids[work_text]._acptfactunits
    print(f"{work_acptfactunits=}")
    calendar_x.edit_idea_attr(road=work_road, acptfactunit=acptfactunit_x)
    work_acptfactunits = calendar_x._idearoot._kids[work_text]._acptfactunits
    print(f"{work_acptfactunits=}")
    assert calendar_x._idearoot._kids[work_text]._acptfactunits == {
        acptfactunit_x.base: acptfactunit_x
    }

    # _descendant_promise_count: int = None,
    calendar_x._idearoot._kids[work_text]._descendant_promise_count = 81
    _descendant_promise_count_curr = calendar_x._idearoot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_curr == 81
    calendar_x.edit_idea_attr(road=work_road, descendant_promise_count=67)
    _descendant_promise_count_new = calendar_x._idearoot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_new == 67

    # _all_member_credit: bool = None,
    calendar_x._idearoot._kids[work_text]._all_member_credit = 74
    _all_member_credit_curr = calendar_x._idearoot._kids[work_text]._all_member_credit
    assert _all_member_credit_curr == 74
    calendar_x.edit_idea_attr(road=work_road, all_member_credit=59)
    _all_member_credit_new = calendar_x._idearoot._kids[work_text]._all_member_credit
    assert _all_member_credit_new == 59

    # _all_member_debt: bool = None,
    calendar_x._idearoot._kids[work_text]._all_member_debt = 74
    _all_member_debt_curr = calendar_x._idearoot._kids[work_text]._all_member_debt
    assert _all_member_debt_curr == 74
    calendar_x.edit_idea_attr(road=work_road, all_member_debt=59)
    _all_member_debt_new = calendar_x._idearoot._kids[work_text]._all_member_debt
    assert _all_member_debt_new == 59

    # _grouplink: dict = None,
    calendar_x._idearoot._kids[work_text]._grouplinks = {
        "fun": grouplink_shop(name="fun", creditor_weight=1, debtor_weight=7)
    }
    _grouplinks = calendar_x._idearoot._kids[work_text]._grouplinks
    assert _grouplinks == {
        "fun": grouplink_shop(name="fun", creditor_weight=1, debtor_weight=7)
    }
    calendar_x.edit_idea_attr(
        road=work_road,
        grouplink=grouplink_shop(name="fun", creditor_weight=4, debtor_weight=8),
    )
    assert calendar_x._idearoot._kids[work_text]._grouplinks == {
        "fun": grouplink_shop(name="fun", creditor_weight=4, debtor_weight=8)
    }

    # _is_expanded: dict = None,
    calendar_x._idearoot._kids[work_text]._is_expanded = "what"
    _is_expanded = calendar_x._idearoot._kids[work_text]._is_expanded
    assert _is_expanded == "what"
    calendar_x.edit_idea_attr(road=work_road, is_expanded=True)
    assert calendar_x._idearoot._kids[work_text]._is_expanded == True

    # promise: dict = None,
    calendar_x._idearoot._kids[work_text].promise = "funfun3"
    action = calendar_x._idearoot._kids[work_text].promise
    assert action == "funfun3"
    calendar_x.edit_idea_attr(road=work_road, promise=True)
    assert calendar_x._idearoot._kids[work_text].promise == True

    # _problem_bool
    calendar_x._idearoot._kids[work_text]._problem_bool = "heat2"
    _problem_bool = calendar_x._idearoot._kids[work_text]._problem_bool
    assert _problem_bool == "heat2"
    calendar_x.edit_idea_attr(road=work_road, problem_bool=True)
    assert calendar_x._idearoot._kids[work_text]._problem_bool == True

    # _special_road: dict = None,
    calendar_x._idearoot._kids[work_text]._special_road = "fun3rol"
    special_road = calendar_x._idearoot._kids[work_text]._special_road
    assert special_road == "fun3rol"
    calendar_x.edit_idea_attr(road=work_road, special_road="my,work,end")
    assert calendar_x._idearoot._kids[work_text]._special_road == "my,work,end"


def test_calendar_edit_idea_attr_calendarIsAbleToEdit_on_meld_weight_action_AnyIdeaIfInvaildThrowsError():
    calendar_x = get_calendar_with_4_levels()
    work_road = f"{calendar_x._owner},work"

    # When/Then
    with pytest_raises(Exception) as excinfo:
        calendar_x.edit_idea_attr(road=work_road, on_meld_weight_action="yahoo9")
    assert (
        str(excinfo.value)
        == "IdeaCore unit 'work' cannot have on_meld_weight_action 'yahoo9'."
    )


def test_calendar_edit_idea_attr_calendarIsAbleToEditDenomAnyIdeaIfInvaildDenomThrowsError():
    flount_text = "flount"
    calendar_x = CalendarUnit(_owner=flount_text)
    # When/Then
    with pytest_raises(Exception) as excinfo:
        calendar_x.edit_idea_attr(road="", denom=46)
    assert str(excinfo.value) == "Root Idea cannot have numor denom reest."

    work = "work"
    w_road = f"{flount_text},{work}"
    work_idea = IdeaKid(_desc=work)
    calendar_x.add_idea(work_idea, walk=flount_text)
    clean = "clean"
    clean_idea = IdeaKid(_desc=clean)
    c_road = f"{w_road},{clean}"
    calendar_x.add_idea(clean_idea, walk=w_road)

    # When/Then
    with pytest_raises(Exception) as excinfo:
        calendar_x.edit_idea_attr(road=c_road, denom=46)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{flount_text},work,clean' if parent '{flount_text},work' or ideacore._numeric_road does not have begin/close range"
    )

    # Given
    calendar_x.edit_idea_attr(road=w_road, begin=44, close=110)
    calendar_x.edit_idea_attr(road=c_road, denom=11)
    clean_idea = calendar_x.get_idea_kid(road=c_road)
    assert clean_idea._begin == 4
    assert clean_idea._close == 10


def test_calendar_edit_idea_attr_calendarIsAbleToEditDenomAnyIdeaInvaildDenomThrowsError():
    flount_text = "flount"
    # Given
    calendar_x = CalendarUnit(_owner=flount_text)
    work = "work"
    w_road = f"{flount_text},{work}"
    work_idea = IdeaKid(_desc=work, _begin=8, _close=14)
    calendar_x.add_idea(work_idea, walk=flount_text)

    clean = "clean"
    clean_idea = IdeaKid(_desc=clean, _denom=1)
    c_road = f"{w_road},{clean}"
    calendar_x.add_idea(clean_idea, walk=w_road)

    clean_idea = calendar_x.get_idea_kid(road=c_road)

    day = "day_range"
    day_idea = IdeaKid(_desc=day, _begin=44, _close=110)
    day_road = f"{flount_text},{day}"
    calendar_x.add_idea(day_idea, walk=flount_text)

    # When/Then
    with pytest_raises(Exception) as excinfo:
        calendar_x.edit_idea_attr(road=c_road, numeric_road=day_road)
    assert (
        str(excinfo.value)
        == "Idea has begin-close range parent, cannot have numeric_road"
    )

    calendar_x.edit_idea_attr(road=w_road, numeric_road=day_road)


def test_calendar_edit_idea_attr_calendarWhenParentAndNumeric_roadBothHaveRangeThrowError():
    flount_text = "flount"
    # Given
    calendar_x = CalendarUnit(_owner=flount_text)
    work = "work"
    w_road = f"{flount_text},{work}"
    work_idea = IdeaKid(_desc=work)
    calendar_x.add_idea(work_idea, walk=flount_text)
    day = "day_range"
    day_idea = IdeaKid(_desc=day, _begin=44, _close=110)
    day_road = f"{flount_text},{day}"
    calendar_x.add_idea(day_idea, walk=flount_text)

    work_idea2 = calendar_x.get_idea_kid(road=w_road)
    assert work_idea2._begin is None
    assert work_idea2._close is None

    with pytest_raises(Exception) as excinfo:
        calendar_x.edit_idea_attr(road=w_road, denom=11)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{flount_text},work' if parent '{flount_text}' or ideacore._numeric_road does not have begin/close range"
    )

    # When
    calendar_x.edit_idea_attr(road=w_road, numeric_road=day_road)

    # Then
    work_idea3 = calendar_x.get_idea_kid(road=w_road)
    assert work_idea3._addin is None
    assert work_idea3._numor is None
    assert work_idea3._denom is None
    assert work_idea3._reest is None
    assert work_idea3._begin == 44
    assert work_idea3._close == 110
    calendar_x.edit_idea_attr(road=w_road, denom=11, numeric_road=day_road)
    assert work_idea3._begin == 4
    assert work_idea3._close == 10
    assert work_idea3._numor == 1
    assert work_idea3._denom == 11
    assert work_idea3._reest == False
    assert work_idea3._addin == 0


def test_calendar_add_idea_MustReorderKidsDictToBeAlphabetical():
    # Given
    src_text = "src"
    ax = CalendarUnit(_owner=src_text)
    work_text = "work"
    ax.add_idea(IdeaKid(_desc=work_text), walk=src_text)
    swim_text = "swim"
    ax.add_idea(IdeaKid(_desc=swim_text), walk=src_text)

    # WHEN
    idea_list = list(ax._idearoot._kids.values())

    # THEN
    assert idea_list[0]._desc == swim_text
