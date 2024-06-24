from src._truth.examples.example_truths import truth_v001_with_large_agenda
from src._truth.truth import truthunit_shop
from src._truth.report import (
    get_truth_otherunits_dataframe,
    get_truth_agenda_dataframe,
)


def test_get_truth_otherunits_dataframe_ReturnsCorrectDataFrame():
    # GIVEN
    luca_truth = truthunit_shop()
    luca_truth.set_other_credor_pool(500)
    luca_truth.set_other_debtor_pool(400)
    todd_text = "Todd"
    todd_credor_weight = 66
    todd_debtor_weight = 77
    luca_truth.add_otherunit(todd_text, todd_credor_weight, todd_debtor_weight)
    sue_text = "Sue"
    sue_credor_weight = 434
    sue_debtor_weight = 323
    luca_truth.add_otherunit(sue_text, sue_credor_weight, sue_debtor_weight)

    # WHEN
    x_df = get_truth_otherunits_dataframe(luca_truth)

    # THEN
    otherunit_colums = {
        "other_id",
        "credor_weight",
        "debtor_weight",
        "_truth_cred",
        "_truth_debt",
        "_truth_agenda_cred",
        "_truth_agenda_debt",
        "_truth_agenda_ratio_cred",
        "_truth_agenda_ratio_debt",
        "_credor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_truth_meld_order",
        "_treasury_cred_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == otherunit_colums
    assert x_df.shape[0] == 2


def test_get_truth_otherunits_dataframe_ReturnsCorrectEmptyDataFrame():
    # GIVEN
    luca_truth = truthunit_shop()

    # WHEN
    x_df = get_truth_otherunits_dataframe(luca_truth)

    # THEN
    otherunit_colums = {
        "other_id",
        "credor_weight",
        "debtor_weight",
        "_truth_cred",
        "_truth_debt",
        "_truth_agenda_cred",
        "_truth_agenda_debt",
        "_truth_agenda_ratio_cred",
        "_truth_agenda_ratio_debt",
        "_credor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_truth_meld_order",
        "_treasury_cred_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == otherunit_colums
    assert x_df.shape[0] == 0


def test_get_truth_agenda_dataframe_ReturnsCorrectDataFrame():
    # GIVEN
    yao_truth = truth_v001_with_large_agenda()
    week_text = "weekdays"
    week_road = yao_truth.make_l1_road(week_text)
    assert len(yao_truth.get_agenda_dict()) == 63

    # WHEN
    x_df = get_truth_agenda_dataframe(yao_truth)
    print(x_df)

    # THEN
    otherunit_colums = {
        "owner_id",
        "truth_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == otherunit_colums
    assert x_df.shape[0] == 63


def test_get_truth_agenda_dataframe_ReturnsCorrectEmptyDataFrame():
    # GIVEN
    yao_truth = truthunit_shop("Yao")
    assert len(yao_truth.get_agenda_dict()) == 0

    # WHEN
    x_df = get_truth_agenda_dataframe(yao_truth)
    print(x_df)

    # THEN
    otherunit_colums = {
        "owner_id",
        "truth_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == otherunit_colums
