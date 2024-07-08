from src._world.healer import healerhold_shop
from src._world.idea import IdeaAttrFilter, ideaattrfilter_shop
from pytest import raises as pytest_raise


def test_IdeaAttrFilter_Exists():
    new_obj = IdeaAttrFilter()
    assert new_obj.weight is None
    assert new_obj.uid is None
    assert new_obj.reason is None
    assert new_obj.reason_base is None
    assert new_obj.reason_premise is None
    assert new_obj.reason_premise_open is None
    assert new_obj.reason_premise_nigh is None
    assert new_obj.reason_premise_divisor is None
    assert new_obj.reason_del_premise_base is None
    assert new_obj.reason_del_premise_need is None
    assert new_obj.reason_base_idea_active_requisite is None
    assert new_obj.cultureunit is None
    assert new_obj.healerhold is None
    assert new_obj.begin is None
    assert new_obj.close is None
    assert new_obj.addin is None
    assert new_obj.numor is None
    assert new_obj.denom is None
    assert new_obj.reest is None
    assert new_obj.numeric_road is None
    assert new_obj.range_source_road is None
    assert new_obj.pledge is None
    assert new_obj.factunit is None
    assert new_obj.descendant_pledge_count is None
    assert new_obj.all_char_cred is None
    assert new_obj.all_char_debt is None
    assert new_obj.fiscallink is None
    assert new_obj.fiscallink_del is None
    assert new_obj.is_expanded is None
    assert new_obj.meld_strategy is None


def test_IdeaAttrFilter_CorrectlyCalculatesPremiseRanges():
    # GIVEN
    idea_attr = IdeaAttrFilter(reason_premise="some_road")
    assert idea_attr.reason_premise_open is None
    assert idea_attr.reason_premise_nigh is None
    # assert idea_attr.reason_premise_numor is None
    assert idea_attr.reason_premise_divisor is None
    # assert idea_attr.reason_premise_reest is None

    # WHEN
    idea_attr.set_premise_range_attributes_influenced_by_premise_idea(
        premise_open=5.0,
        premise_nigh=20.0,
        # premise_numor,
        premise_denom=4.0,
        # premise_reest,
    )
    assert idea_attr.reason_premise_open == 5.0
    assert idea_attr.reason_premise_nigh == 20.0
    # assert idea_attr.reason_premise_numor is None
    assert idea_attr.reason_premise_divisor == 4.0
    # assert idea_attr.reason_premise_reest is None


def test_ideaattrfilter_shop_ReturnsCorrectObj():
    # GIVEN
    sue_healerhold = healerhold_shop({"Sue", "Yim"})

    # WHEN
    x_ideaattrfilter = ideaattrfilter_shop(healerhold=sue_healerhold)

    # THEN
    assert x_ideaattrfilter.healerhold == sue_healerhold
