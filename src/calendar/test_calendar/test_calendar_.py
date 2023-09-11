from src.calendar.examples.example_calendars import (
    get_calendar_1Task_1CE0MinutesRequired_1AcptFact,
    get_calendar_with_4_levels,
)
from src.calendar.calendar import CalendarUnit
from src.calendar.road import get_global_root_label as root_label
from src.calendar.origin import originunit_shop
from pytest import raises as pytest_raises


def test_calendar_exists():
    # GIVEN

    # WHEN
    owner_text = "Noa"
    new_obj = CalendarUnit(_owner=owner_text)

    assert new_obj
    assert new_obj._owner == owner_text
    assert new_obj._weight == 1
    assert new_obj._max_tree_traverse == 3
    assert new_obj._tree_traverse_count is None
    assert new_obj._rational == False
    assert new_obj._originunit == originunit_shop()
    assert new_obj._auto_output_to_public == False
    assert str(type(new_obj._idearoot)).find(".idea.IdeaRoot'>")


def test_calendar_IsAbleToSetTaskAsComplete():
    calendar_x = get_calendar_1Task_1CE0MinutesRequired_1AcptFact()

    assert calendar_x != None
    assert len(calendar_x._idearoot._kids["obtain mail"]._requiredunits) == 1
    idea_list = calendar_x.get_idea_list()
    # for idea in idea_list:
    #     print(idea._label)
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True

    ced_min_label = "CE0_minutes"
    ced_road = f"{root_label()},{ced_min_label}"
    calendar_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = calendar_x.get_idea_list()
    assert mail_idea.promise == True
    assert mail_idea._task == False


def test_calendar_IsAbleToEditAcptFactUnitAnyAncestor_Idea_1():
    calendar_x = get_calendar_1Task_1CE0MinutesRequired_1AcptFact()
    ced_min_label = "CE0_minutes"
    ced_road = f"{root_label()},{ced_min_label}"
    calendar_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = calendar_x.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == False

    calendar_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_list = calendar_x.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True


def test_calendar_ideaoot_uid_isAlwaysEqualTo1():
    # GIVEN
    owner_text = "Zia"

    # WHEN
    sx = CalendarUnit(_owner=owner_text)

    # THEN
    assert sx._idearoot._uid == 1


def test_calendar_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    owner_text = "Zia"
    sx = CalendarUnit(_owner=owner_text)
    assert sx._max_tree_traverse == 3

    # WHEN
    sx.set_max_tree_traverse(int_x=11)

    # THEN
    assert sx._max_tree_traverse == 11


def test_calendar_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    owner_text = "Zia"
    sx = CalendarUnit(_owner=owner_text)
    assert sx._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sx.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_calendar_set_auto_output_to_public_SetsBoolCorrectlyGivenNoneOrBool():
    # GIVEN
    calendar_x = get_calendar_with_4_levels()

    # WHEN / THEN
    assert calendar_x._auto_output_to_public == False
    calendar_x._set_auto_output_to_public(None)
    assert calendar_x._auto_output_to_public == False

    # WHEN / THEN
    assert calendar_x._auto_output_to_public == False
    calendar_x._set_auto_output_to_public(True)
    assert calendar_x._auto_output_to_public

    # WHEN / THEN
    assert calendar_x._auto_output_to_public
    calendar_x._set_auto_output_to_public(True)
    assert calendar_x._auto_output_to_public

    # WHEN / THEN
    assert calendar_x._auto_output_to_public
    calendar_x._set_auto_output_to_public(None)
    assert calendar_x._auto_output_to_public

    # WHEN / THEN
    assert calendar_x._auto_output_to_public
    calendar_x._set_auto_output_to_public(False)
    assert calendar_x._auto_output_to_public == False

    # WHEN / THEN
    calendar_x._auto_output_to_public = None
    assert calendar_x._auto_output_to_public is None
    calendar_x._set_auto_output_to_public(None)
    assert calendar_x._auto_output_to_public == False


def test_calendar_init_CorrectlySetsGiven_auto_output_to_public():
    # GIVEN

    # WHEN
    owner_text = "Noa"
    new_obj = CalendarUnit(_owner=owner_text, _auto_output_to_public=True)

    # THEN
    assert new_obj._auto_output_to_public == True
