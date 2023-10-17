from src.pact.examples.example_pacts import (
    get_pact_1Task_1CE0MinutesRequired_1AcptFact,
    get_pact_with_4_levels,
)
from src.pact.pact import PactUnit
from src.pact.road import get_default_cure_root_label as root_label
from src.pact.origin import originunit_shop
from pytest import raises as pytest_raises


def test_pact_exists():
    # GIVEN

    # WHEN
    healer_text = "Noa"
    new_obj = PactUnit(_healer=healer_text)

    assert new_obj
    assert new_obj._healer == healer_text
    assert new_obj._cure_handle == root_label()
    assert new_obj._weight == 1
    assert new_obj._max_tree_traverse == 3
    assert new_obj._tree_traverse_count is None
    assert new_obj._rational == False
    assert new_obj._originunit == originunit_shop()
    assert new_obj._auto_output_to_public == False
    assert str(type(new_obj._idearoot)).find(".idea.IdeaRoot'>")


def test_pact_IsAbleToSetTaskAsComplete():
    pact_x = get_pact_1Task_1CE0MinutesRequired_1AcptFact()

    assert pact_x != None
    assert len(pact_x._idearoot._kids["obtain mail"]._requiredunits) == 1
    idea_list = pact_x.get_idea_list()
    # for idea in idea_list:
    #     print(idea._label)
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True

    ced_min_label = "CE0_minutes"
    ced_road = f"{pact_x._cure_handle},{ced_min_label}"
    pact_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = pact_x.get_idea_list()
    assert mail_idea.promise == True
    assert mail_idea._task == False


def test_pact_IsAbleToEditAcptFactUnitAnyAncestor_Idea_1():
    pact_x = get_pact_1Task_1CE0MinutesRequired_1AcptFact()
    ced_min_label = "CE0_minutes"
    ced_road = f"{pact_x._cure_handle},{ced_min_label}"
    pact_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = pact_x.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == False

    pact_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_list = pact_x.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True


def test_pact_ideaoot_uid_isAlwaysEqualTo1():
    # GIVEN
    healer_text = "Zia"

    # WHEN
    sx = PactUnit(_healer=healer_text)

    # THEN
    assert sx._idearoot._uid == 1


def test_pact_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    healer_text = "Zia"
    sx = PactUnit(_healer=healer_text)
    assert sx._max_tree_traverse == 3

    # WHEN
    sx.set_max_tree_traverse(int_x=11)

    # THEN
    assert sx._max_tree_traverse == 11


def test_pact_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    healer_text = "Zia"
    sx = PactUnit(_healer=healer_text)
    assert sx._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sx.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_pact_set_auto_output_to_public_SetsBoolCorrectlyGivenNoneOrBool():
    # GIVEN
    pact_x = get_pact_with_4_levels()

    # WHEN / THEN
    assert pact_x._auto_output_to_public == False
    pact_x._set_auto_output_to_public(None)
    assert pact_x._auto_output_to_public == False

    # WHEN / THEN
    assert pact_x._auto_output_to_public == False
    pact_x._set_auto_output_to_public(True)
    assert pact_x._auto_output_to_public

    # WHEN / THEN
    assert pact_x._auto_output_to_public
    pact_x._set_auto_output_to_public(True)
    assert pact_x._auto_output_to_public

    # WHEN / THEN
    assert pact_x._auto_output_to_public
    pact_x._set_auto_output_to_public(None)
    assert pact_x._auto_output_to_public

    # WHEN / THEN
    assert pact_x._auto_output_to_public
    pact_x._set_auto_output_to_public(False)
    assert pact_x._auto_output_to_public == False

    # WHEN / THEN
    pact_x._auto_output_to_public = None
    assert pact_x._auto_output_to_public is None
    pact_x._set_auto_output_to_public(None)
    assert pact_x._auto_output_to_public == False


def test_pact_init_CorrectlySetsGiven_auto_output_to_public():
    # GIVEN

    # WHEN
    healer_text = "Noa"
    new_obj = PactUnit(_healer=healer_text, _auto_output_to_public=True)

    # THEN
    assert new_obj._auto_output_to_public == True


def test_pact_set_cure_handle_CorrectlySetsAttr():
    # GIVEN
    cure_handle_text = "Sun"
    healer_text = "Noa"
    new_obj = PactUnit(_healer=healer_text, _auto_output_to_public=True)
    assert new_obj._cure_handle == root_label()

    # WHEN
    new_obj.set_cure_handle(cure_handle=cure_handle_text)

    # THEN
    assert new_obj._cure_handle == cure_handle_text
