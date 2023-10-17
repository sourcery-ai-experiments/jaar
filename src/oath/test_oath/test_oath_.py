from src.oath.examples.example_oaths import (
    get_oath_1Task_1CE0MinutesRequired_1AcptFact,
    get_oath_with_4_levels,
)
from src.oath.oath import OathUnit
from src.oath.road import get_default_cure_root_label as root_label
from src.oath.origin import originunit_shop
from pytest import raises as pytest_raises


def test_oath_exists():
    # GIVEN

    # WHEN
    healer_text = "Noa"
    x_oath = OathUnit(_healer=healer_text)

    assert x_oath
    assert x_oath._healer == healer_text
    assert x_oath._cure_handle == root_label()
    assert x_oath._weight == 1
    assert x_oath._max_tree_traverse == 3
    assert x_oath._tree_traverse_count is None
    assert x_oath._rational == False
    assert x_oath._originunit == originunit_shop()
    assert x_oath._auto_output_to_public == False
    assert str(type(x_oath._idearoot)).find(".idea.IdeaRoot'>")


def test_oath_IsAbleToSetTaskAsComplete():
    x_oath = get_oath_1Task_1CE0MinutesRequired_1AcptFact()

    assert x_oath != None
    assert len(x_oath._idearoot._kids["obtain mail"]._requiredunits) == 1
    idea_list = x_oath.get_idea_list()
    # for idea in idea_list:
    #     print(idea._label)
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True

    ced_min_label = "CE0_minutes"
    ced_road = f"{x_oath._cure_handle},{ced_min_label}"
    x_oath.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = x_oath.get_idea_list()
    assert mail_idea.promise == True
    assert mail_idea._task == False


def test_oath_IsAbleToEditAcptFactUnitAnyAncestor_Idea_1():
    x_oath = get_oath_1Task_1CE0MinutesRequired_1AcptFact()
    ced_min_label = "CE0_minutes"
    ced_road = f"{x_oath._cure_handle},{ced_min_label}"
    x_oath.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = x_oath.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == False

    x_oath.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_list = x_oath.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True


def test_oath_ideaoot_uid_isAlwaysEqualTo1():
    # GIVEN
    healer_text = "Zia"

    # WHEN
    x_oath = OathUnit(_healer=healer_text)

    # THEN
    assert x_oath._idearoot._uid == 1


def test_oath_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    healer_text = "Zia"
    x_oath = OathUnit(_healer=healer_text)
    assert x_oath._max_tree_traverse == 3

    # WHEN
    x_oath.set_max_tree_traverse(int_x=11)

    # THEN
    assert x_oath._max_tree_traverse == 11


def test_oath_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    healer_text = "Zia"
    x_oath = OathUnit(_healer=healer_text)
    assert x_oath._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_oath.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_oath_set_auto_output_to_public_SetsBoolCorrectlyGivenNoneOrBool():
    # GIVEN
    x_oath = get_oath_with_4_levels()

    # WHEN / THEN
    assert x_oath._auto_output_to_public == False
    x_oath._set_auto_output_to_public(None)
    assert x_oath._auto_output_to_public == False

    # WHEN / THEN
    assert x_oath._auto_output_to_public == False
    x_oath._set_auto_output_to_public(True)
    assert x_oath._auto_output_to_public

    # WHEN / THEN
    assert x_oath._auto_output_to_public
    x_oath._set_auto_output_to_public(True)
    assert x_oath._auto_output_to_public

    # WHEN / THEN
    assert x_oath._auto_output_to_public
    x_oath._set_auto_output_to_public(None)
    assert x_oath._auto_output_to_public

    # WHEN / THEN
    assert x_oath._auto_output_to_public
    x_oath._set_auto_output_to_public(False)
    assert x_oath._auto_output_to_public == False

    # WHEN / THEN
    x_oath._auto_output_to_public = None
    assert x_oath._auto_output_to_public is None
    x_oath._set_auto_output_to_public(None)
    assert x_oath._auto_output_to_public == False


def test_oath_init_CorrectlySetsGiven_auto_output_to_public():
    # GIVEN

    # WHEN
    healer_text = "Noa"
    x_oath = OathUnit(_healer=healer_text, _auto_output_to_public=True)

    # THEN
    assert x_oath._auto_output_to_public == True


def test_oath_set_cure_handle_CorrectlySetsAttr():
    # GIVEN
    cure_handle_text = "Sun"
    healer_text = "Noa"
    x_oath = OathUnit(_healer=healer_text, _auto_output_to_public=True)
    assert x_oath._cure_handle == root_label()

    # WHEN
    x_oath.set_cure_handle(cure_handle=cure_handle_text)

    # THEN
    assert x_oath._cure_handle == cure_handle_text
