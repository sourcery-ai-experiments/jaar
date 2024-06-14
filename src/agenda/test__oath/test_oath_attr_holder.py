from src.agenda.healer import healerhold_shop
from src.agenda.fact import FactAttrFilter, factattrfilter_shop
from pytest import raises as pytest_raise


def test_FactAttrFilter_Exists():
    new_obj = FactAttrFilter()
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
    assert new_obj.reason_suff_fact_active is None
    assert new_obj.assignedunit is None
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
    assert new_obj.beliefunit is None
    assert new_obj.descendant_pledge_count is None
    assert new_obj.all_party_cred is None
    assert new_obj.all_party_debt is None
    assert new_obj.balancelink is None
    assert new_obj.balancelink_del is None
    assert new_obj.is_expanded is None
    assert new_obj.meld_strategy is None


def test_FactAttrFilter_CorrectlyCalculatesPremiseRanges():
    # GIVEN
    fact_attr = FactAttrFilter(reason_premise="some_road")
    assert fact_attr.reason_premise_open is None
    assert fact_attr.reason_premise_nigh is None
    # assert fact_attr.reason_premise_numor is None
    assert fact_attr.reason_premise_divisor is None
    # assert fact_attr.reason_premise_reest is None

    # WHEN
    fact_attr.set_premise_range_attributes_influenced_by_premise_fact(
        premise_open=5.0,
        premise_nigh=20.0,
        # premise_numor,
        premise_denom=4.0,
        # premise_reest,
    )
    assert fact_attr.reason_premise_open == 5.0
    assert fact_attr.reason_premise_nigh == 20.0
    # assert fact_attr.reason_premise_numor is None
    assert fact_attr.reason_premise_divisor == 4.0
    # assert fact_attr.reason_premise_reest is None


def test_factattrfilter_shop_ReturnsCorrectObj():
    # GIVEN
    sue_healerhold = healerhold_shop({"Sue", "Yim"})

    # WHEN
    x_factattrfilter = factattrfilter_shop(healerhold=sue_healerhold)

    # THEN
    assert x_factattrfilter.healerhold == sue_healerhold
