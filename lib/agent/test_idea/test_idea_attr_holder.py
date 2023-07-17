from lib.agent.idea import IdeaAttrHolder
from pytest import raises as pytest_raise


def test_idea_attr_holder_exists():
    new_obj = IdeaAttrHolder()
    assert new_obj.weight is None
    assert new_obj.uid is None
    assert new_obj.required is None
    assert new_obj.required_base is None
    assert new_obj.required_sufffact is None
    assert new_obj.required_sufffact_open is None
    assert new_obj.required_sufffact_nigh is None
    assert new_obj.required_sufffact_divisor is None
    assert new_obj.required_del_sufffact_base is None
    assert new_obj.required_del_sufffact_need is None
    assert new_obj.required_suff_idea_active_status is None
    assert new_obj.begin is None
    assert new_obj.close is None
    assert new_obj.addin is None
    assert new_obj.numor is None
    assert new_obj.denom is None
    assert new_obj.reest is None
    assert new_obj.numeric_road is None
    assert new_obj.special_road is None
    assert new_obj.promise is None
    assert new_obj.problem_bool is None
    assert new_obj.acptfactunit is None
    assert new_obj.descendant_promise_count is None
    assert new_obj.all_ally_credit is None
    assert new_obj.all_ally_debt is None
    assert new_obj.brandlink is None
    assert new_obj.brandlink_del is None
    assert new_obj.is_expanded is None
    assert new_obj.on_meld_weight_action is None


def test_idea_attr_holder_CorrectlyCalculatesSuffFactRanges():
    # Given
    idea_attr = IdeaAttrHolder(required_sufffact="some_road")
    assert idea_attr.required_sufffact_open is None
    assert idea_attr.required_sufffact_nigh is None
    # assert idea_attr.required_sufffact_numor is None
    assert idea_attr.required_sufffact_divisor is None
    # assert idea_attr.required_sufffact_reest is None

    # WHEN
    idea_attr.set_sufffact_range_attributes_influenced_by_sufffact_idea(
        sufffact_open=5.0,
        sufffact_nigh=20.0,
        # sufffact_numor,
        sufffact_denom=4.0,
        # sufffact_reest,
    )
    assert idea_attr.required_sufffact_open == 5.0
    assert idea_attr.required_sufffact_nigh == 20.0
    # assert idea_attr.required_sufffact_numor is None
    assert idea_attr.required_sufffact_divisor == 4.0
    # assert idea_attr.required_sufffact_reest is None
