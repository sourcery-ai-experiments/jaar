from src.agenda.idea import IdeaAttrFilter
from pytest import raises as pytest_raise


def test_idea_attr_holder_exists():
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
    assert new_obj.reason_suff_idea_active_status is None
    assert new_obj.assignedunit is None
    assert new_obj.begin is None
    assert new_obj.close is None
    assert new_obj.addin is None
    assert new_obj.numor is None
    assert new_obj.denom is None
    assert new_obj.reest is None
    assert new_obj.numeric_road is None
    assert new_obj.range_source_road is None
    assert new_obj.promise is None
    assert new_obj.problem_bool is None
    assert new_obj.factunit is None
    assert new_obj.descendant_promise_count is None
    assert new_obj.all_party_credit is None
    assert new_obj.all_party_debt is None
    assert new_obj.balancelink is None
    assert new_obj.balancelink_del is None
    assert new_obj.is_expanded is None
    assert new_obj.on_meld_weight_action is None


def test_idea_attr_holder_CorrectlyCalculatesPremiseRanges():
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
