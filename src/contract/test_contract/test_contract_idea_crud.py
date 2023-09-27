from src.contract.examples.example_contracts import get_contract_with_4_levels
from src.contract.idea import IdeaKid
from src.contract.required_idea import RequiredUnit, acptfactunit_shop
from src.contract.contract import ContractUnit
from src.contract.group import grouplink_shop
from pytest import raises as pytest_raises
from src.contract.road import Road, get_default_economy_root_label as root_label


def test_root_has_kids():
    # GIVEN
    contract_x = ContractUnit(_owner="prom")
    idearoot_x = contract_x._idearoot
    idea1 = IdeaKid(_weight=30, _label="work")
    idea2 = IdeaKid(_weight=40, _label="ulty")

    # WHEN
    contract_x.add_idea(idea_kid=idea1, walk=contract_x._owner)
    contract_x.add_idea(idea_kid=idea2, walk=contract_x._owner)

    # THEN
    assert idearoot_x._weight == 1
    assert idearoot_x._kids
    assert len(idearoot_x._kids) == 2


def test_kid_can_have_kids():
    # GIVEN / WHEN
    contract_x = get_contract_with_4_levels()
    contract_x.set_contract_metrics()

    # THEN
    assert contract_x._weight == 10
    assert contract_x._idearoot._kids
    print(f"{len(contract_x._idearoot._kids)=} {contract_x._idearoot._walk=}")
    assert contract_x.get_level_count(level=0) == 1
    weekdays_kids = contract_x._idearoot._kids["weekdays"]._kids
    weekdays_len = len(weekdays_kids)
    print(f"{weekdays_len=} {contract_x._idearoot._walk=}")
    # for idea in weekdays_kids.values():
    #     print(f"{idea._label=}")
    assert contract_x.get_node_count() == 17
    assert contract_x.get_level_count(level=1) == 4
    assert contract_x.get_level_count(level=2) == 10
    assert contract_x.get_level_count(level=3) == 2


def test_contract_add_idea_CanAddKidToRootIdea():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    contract_x.set_contract_metrics()

    assert contract_x.get_node_count() == 17
    assert contract_x.get_level_count(level=1) == 4

    new_idea_parent_road = contract_x._owner
    new_idea = IdeaKid(_weight=40, _label="new_idea")

    # WHEN
    contract_x.add_idea(idea_kid=new_idea, walk=new_idea_parent_road)
    contract_x.set_contract_metrics()

    # THEN
    print(f"{(contract_x._owner == new_idea_parent_road[0])=}")
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert contract_x.get_node_count() == 18
    assert contract_x.get_level_count(level=1) == 5


def test_contract_add_idea_CanAddKidToKidIdea():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    contract_x.set_contract_metrics()

    assert contract_x.get_node_count() == 17
    assert contract_x.get_level_count(level=2) == 10

    new_idea_parent_road = f"{root_label()},work"
    new_idea = IdeaKid(_weight=40, _label="new_york")

    # WHEN
    contract_x.add_idea(idea_kid=new_idea, walk=new_idea_parent_road)
    contract_x.set_contract_metrics()

    # THEN
    # print(f"{(contract_x._owner == new_idea_parent_road[0])=}")
    # print(contract_x._idearoot._kids["work"])
    # print(f"{(len(new_idea_parent_road) == 1)=}")
    assert contract_x.get_node_count() == 18
    assert contract_x.get_level_count(level=2) == 11
    assert (
        contract_x._idearoot._kids["work"]._kids["new_york"]._walk
        == f"{root_label()},work"
    )
    contract_x._idearoot._kids["work"]._kids["new_york"].set_walk(parent_road="testing")
    assert contract_x._idearoot._kids["work"]._kids["new_york"]._walk == "testing"
    assert contract_x.get_agenda_items


def test_contract_add_idea_CanAddKidToGrandkidIdea():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    contract_x.set_contract_metrics()

    assert contract_x.get_node_count() == 17
    assert contract_x.get_level_count(level=3) == 2
    new_idea_parent_road = f"{root_label()},weekdays,Wednesday"
    new_idea = IdeaKid(_weight=40, _label="new_idea")

    # WHEN
    contract_x.add_idea(idea_kid=new_idea, walk=new_idea_parent_road)
    contract_x.set_contract_metrics()

    # THEN
    print(f"{(contract_x._owner == new_idea_parent_road[0])=}")
    print(contract_x._idearoot._kids["work"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert contract_x.get_node_count() == 18
    assert contract_x.get_level_count(level=3) == 3


def test_contract_add_idea_CanCreateRoadToGrandkidIdea():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    contract_x.set_contract_metrics()

    assert contract_x.get_node_count() == 17
    assert contract_x.get_level_count(level=3) == 2
    new_idea_parent_road = f"{root_label()},ww2,battles,coralsea"
    new_idea = IdeaKid(_weight=40, _label="USS Saratoga")

    # WHEN
    contract_x.add_idea(idea_kid=new_idea, walk=new_idea_parent_road)
    contract_x.set_contract_metrics()

    # THEN
    print(contract_x._idearoot._kids["ww2"])
    print(f"{(len(new_idea_parent_road) == 1)=}")
    assert contract_x._idearoot._kids["ww2"]._label == "ww2"
    assert contract_x._idearoot._kids["ww2"]._kids["battles"]._label == "battles"
    assert contract_x.get_node_count() == 21
    assert contract_x.get_level_count(level=3) == 3


def test_contract_add_idea_creates_requireds_ideas():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    contract_x.set_contract_metrics()

    assert contract_x.get_node_count() == 17
    assert contract_x.get_level_count(level=3) == 2
    new_idea_parent_road = f"{root_label()},work,cleaning"
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = IdeaKid(_weight=40, _label=clean_cookery_text, promise=True)

    buildings_text = "buildings"
    buildings_road = Road(f"{root_label()},{buildings_text}")
    cookery_room_text = "cookery"
    cookery_room_road = Road(f"{root_label()},{buildings_text},{cookery_room_text}")
    cookery_dirty_text = "dirty"
    cookery_dirty_road = Road(f"{cookery_room_road},{cookery_dirty_text}")
    required_x = RequiredUnit(base=cookery_room_road, sufffacts={})
    required_x.set_sufffact(sufffact=cookery_dirty_road)
    clean_cookery_idea.set_required_unit(required=required_x)

    assert contract_x._idearoot._kids.get(buildings_text) is None

    # WHEN
    contract_x.add_idea(
        idea_kid=clean_cookery_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )
    contract_x.set_contract_metrics()

    # THEN
    print(f"{(len(new_idea_parent_road) == 1)=}")
    # for idea_kid in contract_x._idearoot._kids.values():
    #     print(f"{idea_kid._label=}")
    assert contract_x._idearoot._kids.get(buildings_text) != None
    assert contract_x.get_idea_kid(road=buildings_road) != None
    assert contract_x.get_idea_kid(road=cookery_dirty_road) != None
    assert contract_x.get_node_count() == 22
    assert contract_x.get_level_count(level=3) == 4


def test_contract_idearoot_is_heir_CorrectlyChecksLineage():
    contract_x = get_contract_with_4_levels()
    contract_x.set_contract_metrics()

    week_text = "weekdays"
    week_road = f"{root_label()},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"
    assert contract_x._idearoot.is_heir(src=week_road, heir=week_road)
    assert contract_x._idearoot.is_heir(src=week_road, heir=sun_road)
    assert contract_x._idearoot.is_heir(src=sun_road, heir=week_road) == False


def test_contract_del_idea_kid_IdeaLevel0CannotBeDeleted():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    root_road = f"{root_label()}"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.del_idea_kid(road=root_road)
    assert str(excinfo.value) == "Object cannot delete itself"


def test_contract_del_idea_kid_IdeaLevel1CanBeDeleted_ChildrenDeleted():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    week_text = "weekdays"
    week_road = f"{root_label()},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"
    assert contract_x.get_idea_kid(road=week_road)
    assert contract_x.get_idea_kid(road=sun_road)

    # WHEN
    contract_x.del_idea_kid(road=week_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.get_idea_kid(road=week_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='weekdays' failed no item at '{week_road}'"
    )
    new_sunday_road = f"{root_label()},Sunday"
    with pytest_raises(Exception) as excinfo:
        contract_x.get_idea_kid(road=new_sunday_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='Sunday' failed no item at '{new_sunday_road}'"
    )


def test_contract_del_idea_kid_IdeaLevel1CanBeDeleted_ChildrenInherited():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    contract_x.set_contract_metrics()
    week_text = "weekdays"
    week_road = f"{root_label()},{week_text}"
    sun_text = "Sunday"
    old_sunday_road = f"{week_road},{sun_text}"
    assert contract_x.get_idea_kid(road=old_sunday_road)

    # WHEN
    contract_x.del_idea_kid(road=week_road, del_children=False)

    # THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.get_idea_kid(road=old_sunday_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='{sun_text}' failed no item at '{old_sunday_road}'"
    )
    new_sunday_road = f"{root_label()},{sun_text}"
    assert contract_x.get_idea_kid(road=new_sunday_road)
    new_sunday_idea = contract_x.get_idea_kid(road=new_sunday_road)
    assert new_sunday_idea._walk == root_label()


def test_contract_del_idea_kid_IdeaLevel2CanBeDeleted_ChildrenDeleted():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    monday_road = f"{root_label()},weekdays,Monday"
    assert contract_x.get_idea_kid(road=monday_road)

    # WHEN
    contract_x.del_idea_kid(road=monday_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.get_idea_kid(road=monday_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='Monday' failed no item at '{monday_road}'"
    )


def test_contract_del_idea_kid_IdeaLevelNCanBeDeleted_ChildrenDeleted():
    # GIVEN
    contract_x = get_contract_with_4_levels()
    states = "nation-state"
    USA = "USA"
    Texas = "Texas"
    texas_road = f"{root_label()},{states},{USA},{Texas}"
    assert contract_x.get_idea_kid(road=texas_road)

    # WHEN
    contract_x.del_idea_kid(road=texas_road)

    # THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.get_idea_kid(road=texas_road)
    assert (
        str(excinfo.value)
        == f"Getting idea_label='Texas' failed no item at '{texas_road}'"
    )


def test_contract_edit_idea_attr_IsAbleToEditAnyAncestor_Idea():
    contract_x = get_contract_with_4_levels()
    work_text = "work"
    work_road = f"{root_label()},{work_text}"
    print(f"{work_road=}")
    current_weight = contract_x._idearoot._kids[work_text]._weight
    assert current_weight == 30
    contract_x.edit_idea_attr(road=work_road, weight=23)
    new_weight = contract_x._idearoot._kids[work_text]._weight
    assert new_weight == 23

    # uid: int = None,
    contract_x._idearoot._kids[work_text]._uid = 34
    uid_curr = contract_x._idearoot._kids[work_text]._uid
    assert uid_curr == 34
    contract_x.edit_idea_attr(road=work_road, uid=23)
    uid_new = contract_x._idearoot._kids[work_text]._uid
    assert uid_new == 23

    # begin: float = None,
    # close: float = None,
    contract_x._idearoot._kids[work_text]._begin = 39
    begin_curr = contract_x._idearoot._kids[work_text]._begin
    assert begin_curr == 39
    contract_x._idearoot._kids[work_text]._close = 43
    close_curr = contract_x._idearoot._kids[work_text]._close
    assert close_curr == 43
    contract_x.edit_idea_attr(road=work_road, begin=25, close=29)
    assert contract_x._idearoot._kids[work_text]._begin == 25
    assert contract_x._idearoot._kids[work_text]._close == 29

    # acptfactunit: acptfactunit_shop = None,
    # contract_x._idearoot._kids[work_text]._acptfactunits = None
    assert contract_x._idearoot._kids[work_text]._acptfactunits is None
    acptfact_road = f"{root_label()},weekdays,Sunday"
    acptfactunit_x = acptfactunit_shop(base=acptfact_road, pick=acptfact_road)

    work_acptfactunits = contract_x._idearoot._kids[work_text]._acptfactunits
    print(f"{work_acptfactunits=}")
    contract_x.edit_idea_attr(road=work_road, acptfactunit=acptfactunit_x)
    work_acptfactunits = contract_x._idearoot._kids[work_text]._acptfactunits
    print(f"{work_acptfactunits=}")
    assert contract_x._idearoot._kids[work_text]._acptfactunits == {
        acptfactunit_x.base: acptfactunit_x
    }

    # _descendant_promise_count: int = None,
    contract_x._idearoot._kids[work_text]._descendant_promise_count = 81
    _descendant_promise_count_curr = contract_x._idearoot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_curr == 81
    contract_x.edit_idea_attr(road=work_road, descendant_promise_count=67)
    _descendant_promise_count_new = contract_x._idearoot._kids[
        work_text
    ]._descendant_promise_count
    assert _descendant_promise_count_new == 67

    # _all_member_credit: bool = None,
    contract_x._idearoot._kids[work_text]._all_member_credit = 74
    _all_member_credit_curr = contract_x._idearoot._kids[work_text]._all_member_credit
    assert _all_member_credit_curr == 74
    contract_x.edit_idea_attr(road=work_road, all_member_credit=59)
    _all_member_credit_new = contract_x._idearoot._kids[work_text]._all_member_credit
    assert _all_member_credit_new == 59

    # _all_member_debt: bool = None,
    contract_x._idearoot._kids[work_text]._all_member_debt = 74
    _all_member_debt_curr = contract_x._idearoot._kids[work_text]._all_member_debt
    assert _all_member_debt_curr == 74
    contract_x.edit_idea_attr(road=work_road, all_member_debt=59)
    _all_member_debt_new = contract_x._idearoot._kids[work_text]._all_member_debt
    assert _all_member_debt_new == 59

    # _grouplink: dict = None,
    contract_x._idearoot._kids[work_text]._grouplinks = {
        "fun": grouplink_shop(name="fun", creditor_weight=1, debtor_weight=7)
    }
    _grouplinks = contract_x._idearoot._kids[work_text]._grouplinks
    assert _grouplinks == {
        "fun": grouplink_shop(name="fun", creditor_weight=1, debtor_weight=7)
    }
    contract_x.edit_idea_attr(
        road=work_road,
        grouplink=grouplink_shop(name="fun", creditor_weight=4, debtor_weight=8),
    )
    assert contract_x._idearoot._kids[work_text]._grouplinks == {
        "fun": grouplink_shop(name="fun", creditor_weight=4, debtor_weight=8)
    }

    # _is_expanded: dict = None,
    contract_x._idearoot._kids[work_text]._is_expanded = "what"
    _is_expanded = contract_x._idearoot._kids[work_text]._is_expanded
    assert _is_expanded == "what"
    contract_x.edit_idea_attr(road=work_road, is_expanded=True)
    assert contract_x._idearoot._kids[work_text]._is_expanded == True

    # promise: dict = None,
    contract_x._idearoot._kids[work_text].promise = "funfun3"
    action = contract_x._idearoot._kids[work_text].promise
    assert action == "funfun3"
    contract_x.edit_idea_attr(road=work_road, promise=True)
    assert contract_x._idearoot._kids[work_text].promise == True

    # _problem_bool
    contract_x._idearoot._kids[work_text]._problem_bool = "heat2"
    _problem_bool = contract_x._idearoot._kids[work_text]._problem_bool
    assert _problem_bool == "heat2"
    contract_x.edit_idea_attr(road=work_road, problem_bool=True)
    assert contract_x._idearoot._kids[work_text]._problem_bool == True

    # _range_source_road: dict = None,
    contract_x._idearoot._kids[work_text]._range_source_road = "fun3rol"
    range_source_road = contract_x._idearoot._kids[work_text]._range_source_road
    assert range_source_road == "fun3rol"
    contract_x.edit_idea_attr(road=work_road, range_source_road="my,work,end")
    assert contract_x._idearoot._kids[work_text]._range_source_road == "my,work,end"


def test_contract_edit_idea_attr_contractIsAbleToEdit_on_meld_weight_action_AnyIdeaIfInvaildThrowsError():
    contract_x = get_contract_with_4_levels()
    work_road = f"{root_label()},work"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.edit_idea_attr(road=work_road, on_meld_weight_action="yahoo9")
    assert (
        str(excinfo.value)
        == "IdeaCore unit 'work' cannot have on_meld_weight_action 'yahoo9'."
    )


def test_contract_edit_idea_attr_contractIsAbleToEditDenomAnyIdeaIfInvaildDenomThrowsError():
    owner_text = "Yao"
    contract_x = ContractUnit(_owner=owner_text)
    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.edit_idea_attr(road="", denom=46)
    assert str(excinfo.value) == "Root Idea cannot have numor denom reest."

    work = "work"
    w_road = f"{root_label()},{work}"
    work_idea = IdeaKid(_label=work)
    contract_x.add_idea(work_idea, walk=root_label())
    clean = "clean"
    clean_idea = IdeaKid(_label=clean)
    c_road = f"{w_road},{clean}"
    contract_x.add_idea(clean_idea, walk=w_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.edit_idea_attr(road=c_road, denom=46)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{root_label()},work,clean' if parent '{root_label()},work' or ideacore._numeric_road does not have begin/close range"
    )

    # GIVEN
    contract_x.edit_idea_attr(road=w_road, begin=44, close=110)
    contract_x.edit_idea_attr(road=c_road, denom=11)
    clean_idea = contract_x.get_idea_kid(road=c_road)
    assert clean_idea._begin == 4
    assert clean_idea._close == 10


def test_contract_edit_idea_attr_contractIsAbleToEditDenomAnyIdeaInvaildDenomThrowsError():
    # GIVEN
    owner_text = "Yao"
    contract_x = ContractUnit(_owner=owner_text)
    work = "work"
    w_road = f"{root_label()},{work}"
    work_idea = IdeaKid(_label=work, _begin=8, _close=14)
    contract_x.add_idea(work_idea, walk=root_label())

    clean = "clean"
    clean_idea = IdeaKid(_label=clean, _denom=1)
    c_road = f"{w_road},{clean}"
    contract_x.add_idea(clean_idea, walk=w_road)

    clean_idea = contract_x.get_idea_kid(road=c_road)

    day = "day_range"
    day_idea = IdeaKid(_label=day, _begin=44, _close=110)
    day_road = f"{root_label()},{day}"
    contract_x.add_idea(day_idea, walk=root_label())

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.edit_idea_attr(road=c_road, numeric_road=day_road)
    assert (
        str(excinfo.value)
        == "Idea has begin-close range parent, cannot have numeric_road"
    )

    contract_x.edit_idea_attr(road=w_road, numeric_road=day_road)


def test_contract_edit_idea_attr_contractWhenParentAndNumeric_roadBothHaveRangeThrowError():
    # GIVEN
    owner_text = "Yao"
    contract_x = ContractUnit(_owner=owner_text)
    work_text = "work"
    work_road = f"{root_label()},{work_text}"
    contract_x.add_idea(IdeaKid(_label=work_text), walk=root_label())
    day_text = "day_range"
    day_idea = IdeaKid(_label=day_text, _begin=44, _close=110)
    day_road = f"{root_label()},{day_text}"
    contract_x.add_idea(day_idea, walk=root_label())

    work_idea = contract_x.get_idea_kid(road=work_road)
    assert work_idea._begin is None
    assert work_idea._close is None

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        contract_x.edit_idea_attr(road=work_road, denom=11)
    assert (
        str(excinfo.value)
        == f"Idea cannot edit numor=1/denom/reest of '{root_label()},work' if parent '{root_label()}' or ideacore._numeric_road does not have begin/close range"
    )

    # WHEN
    contract_x.edit_idea_attr(road=work_road, numeric_road=day_road)

    # THEN
    work_idea3 = contract_x.get_idea_kid(road=work_road)
    assert work_idea3._addin is None
    assert work_idea3._numor is None
    assert work_idea3._denom is None
    assert work_idea3._reest is None
    assert work_idea3._begin == 44
    assert work_idea3._close == 110
    contract_x.edit_idea_attr(road=work_road, denom=11, numeric_road=day_road)
    assert work_idea3._begin == 4
    assert work_idea3._close == 10
    assert work_idea3._numor == 1
    assert work_idea3._denom == 11
    assert work_idea3._reest == False
    assert work_idea3._addin == 0


def test_contract_add_idea_MustReorderKidsDictToBeAlphabetical():
    # GIVEN
    owner_text = "Noa"
    cx = ContractUnit(_owner=owner_text)
    work_text = "work"
    cx.add_idea(IdeaKid(_label=work_text), walk=root_label())
    swim_text = "swim"
    cx.add_idea(IdeaKid(_label=swim_text), walk=root_label())

    # WHEN
    idea_list = list(cx._idearoot._kids.values())

    # THEN
    assert idea_list[0]._label == swim_text
