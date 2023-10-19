from src.deal.examples.example_deals import (
    get_deal_1Task_1CE0MinutesRequired_1AcptFact,
    get_deal_with_4_levels,
)
from src.deal.deal import dealunit_shop, DealUnit
from src.deal.road import get_default_project_root_label as root_label
from src.deal.origin import originunit_shop
from pytest import raises as pytest_raises


def test_DealUnit_exists():
    # GIVEN

    # WHEN
    x_deal = DealUnit()

    assert x_deal
    assert x_deal._healer is None
    assert x_deal._project_handle is None
    assert x_deal._weight is None
    assert x_deal._max_tree_traverse is None
    assert x_deal._tree_traverse_count is None
    assert x_deal._rational is None
    assert x_deal._originunit is None
    assert x_deal._auto_output_to_public is None
    assert x_deal._idearoot is None
    assert str(type(x_deal._idearoot)).find("None") == 8


def test_dealunit_shop_ReturnsCorrectObjectWithFilledFields():
    # GIVEN
    healer_text = "Noa"

    # WHEN
    x_deal = dealunit_shop(_healer=healer_text)

    assert x_deal
    assert x_deal._healer == healer_text
    assert x_deal._project_handle == root_label()
    assert x_deal._weight == 1
    assert x_deal._max_tree_traverse == 3
    assert x_deal._tree_traverse_count is None
    assert x_deal._rational == False
    assert x_deal._originunit == originunit_shop()
    assert x_deal._auto_output_to_public == False
    assert x_deal._idearoot != None
    print(f"{type(x_deal._idearoot)=}") == 0
    assert str(type(x_deal._idearoot)).find(".idea.IdeaRoot'>") > 0


def test_dealunit_shop_ReturnsCorrectObjectWithCorrectEmptyField():
    # GIVE/ WHEN
    x_deal = dealunit_shop()

    assert x_deal._healer == ""


def test_deal_IsAbleToSetTaskAsComplete():
    x_deal = get_deal_1Task_1CE0MinutesRequired_1AcptFact()

    assert x_deal != None
    assert len(x_deal._idearoot._kids["obtain mail"]._requiredunits) == 1
    idea_list = x_deal.get_idea_list()
    # for idea in idea_list:
    #     print(idea._label)
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True

    ced_min_label = "CE0_minutes"
    ced_road = f"{x_deal._project_handle},{ced_min_label}"
    x_deal.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = x_deal.get_idea_list()
    assert mail_idea.promise == True
    assert mail_idea._task == False


def test_deal_IsAbleToEditAcptFactUnitAnyAncestor_Idea_1():
    x_deal = get_deal_1Task_1CE0MinutesRequired_1AcptFact()
    ced_min_label = "CE0_minutes"
    ced_road = f"{x_deal._project_handle},{ced_min_label}"
    x_deal.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = x_deal.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == False

    x_deal.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_list = x_deal.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True


def test_deal_ideaoot_uid_isAlwaysEqualTo1():
    # GIVEN
    healer_text = "Zia"

    # WHEN
    x_deal = dealunit_shop(_healer=healer_text)

    # THEN
    assert x_deal._idearoot._uid == 1


def test_deal_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    healer_text = "Zia"
    x_deal = dealunit_shop(_healer=healer_text)
    assert x_deal._max_tree_traverse == 3

    # WHEN
    x_deal.set_max_tree_traverse(int_x=11)

    # THEN
    assert x_deal._max_tree_traverse == 11


def test_deal_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    healer_text = "Zia"
    x_deal = dealunit_shop(_healer=healer_text)
    assert x_deal._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_deal.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_deal_set_auto_output_to_public_SetsBoolCorrectlyGivenNoneOrBool():
    # GIVEN
    x_deal = get_deal_with_4_levels()

    # WHEN / THEN
    assert x_deal._auto_output_to_public == False
    x_deal._set_auto_output_to_public(None)
    assert x_deal._auto_output_to_public == False

    # WHEN / THEN
    assert x_deal._auto_output_to_public == False
    x_deal._set_auto_output_to_public(True)
    assert x_deal._auto_output_to_public

    # WHEN / THEN
    assert x_deal._auto_output_to_public
    x_deal._set_auto_output_to_public(True)
    assert x_deal._auto_output_to_public

    # WHEN / THEN
    assert x_deal._auto_output_to_public
    x_deal._set_auto_output_to_public(None)
    assert x_deal._auto_output_to_public

    # WHEN / THEN
    assert x_deal._auto_output_to_public
    x_deal._set_auto_output_to_public(False)
    assert x_deal._auto_output_to_public == False

    # WHEN / THEN
    x_deal._auto_output_to_public = None
    assert x_deal._auto_output_to_public is None
    x_deal._set_auto_output_to_public(None)
    assert x_deal._auto_output_to_public == False


def test_deal_init_CorrectlySetsGiven_auto_output_to_public():
    # GIVEN

    # WHEN
    healer_text = "Noa"
    x_deal = dealunit_shop(_healer=healer_text, _auto_output_to_public=True)

    # THEN
    assert x_deal._auto_output_to_public == True


def test_deal_set_project_handle_CorrectlySetsAttr():
    # GIVEN
    project_handle_text = "Sun"
    healer_text = "Noa"
    x_deal = dealunit_shop(_healer=healer_text, _auto_output_to_public=True)
    assert x_deal._project_handle == root_label()

    # WHEN
    x_deal.set_project_handle(project_handle=project_handle_text)

    # THEN
    assert x_deal._project_handle == project_handle_text
