from src.agenda.examples.example_agendas import (
    agenda_v001_with_large_intent,
    get_agenda_with_4_levels,
    get_agenda_assignment_laundry_example1,
    get_agenda_with_4_levels_and_2reasons,
    get_agenda_x1_3levels_1reason_1beliefs,
)
from src.agenda.agenda import agendaunit_shop
from src.agenda.report import (
    get_agenda_partyunits_dataframe,
    get_agenda_intent_dataframe,
)


def test_get_agenda_partyunits_dataframe_ReturnsCorrectDataFrame():
    # GIVEN
    luca_agenda = agendaunit_shop()
    luca_agenda.set_party_creditor_pool(500)
    luca_agenda.set_party_debtor_pool(400)
    todd_text = "Todd"
    todd_creditor_weight = 66
    todd_debtor_weight = 77
    luca_agenda.add_partyunit(todd_text, todd_creditor_weight, todd_debtor_weight)
    sue_text = "Sue"
    sue_creditor_weight = 434
    sue_debtor_weight = 323
    luca_agenda.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)

    # WHEN
    x_df = get_agenda_partyunits_dataframe(luca_agenda)

    # THEN
    partyunit_colums = {
        "party_id",
        "creditor_weight",
        "debtor_weight",
        "_agenda_credit",
        "_agenda_debt",
        "_agenda_intent_credit",
        "_agenda_intent_debt",
        "_agenda_intent_ratio_credit",
        "_agenda_intent_ratio_debt",
        "_creditor_live",
        "_debtor_live",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_agenda_meld_order",
        "_treasury_credit_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
        "depotlink_type",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == partyunit_colums
    assert x_df.shape[0] == 2


def test_get_agenda_partyunits_dataframe_ReturnsCorrectEmptyDataFrame():
    # GIVEN
    luca_agenda = agendaunit_shop()

    # WHEN
    x_df = get_agenda_partyunits_dataframe(luca_agenda)

    # THEN
    partyunit_colums = {
        "party_id",
        "creditor_weight",
        "debtor_weight",
        "_agenda_credit",
        "_agenda_debt",
        "_agenda_intent_credit",
        "_agenda_intent_debt",
        "_agenda_intent_ratio_credit",
        "_agenda_intent_ratio_debt",
        "_creditor_live",
        "_debtor_live",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_agenda_meld_order",
        "_treasury_credit_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
        "depotlink_type",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == partyunit_colums
    assert x_df.shape[0] == 0


def test_get_agenda_intent_dataframe_ReturnsCorrectDataFrame():
    # GIVEN
    yao_agenda = agenda_v001_with_large_intent()
    week_text = "weekdays"
    week_road = yao_agenda.make_l1_road(week_text)
    assert len(yao_agenda.get_intent_dict()) == 63

    # WHEN
    x_df = get_agenda_intent_dataframe(yao_agenda)
    print(x_df)

    # THEN
    partyunit_colums = {
        "owner_id",
        "agenda_importance",
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

    assert set(x_df.columns) == partyunit_colums
    assert x_df.shape[0] == 63


def test_get_agenda_intent_dataframe_ReturnsCorrectEmptyDataFrame():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao")
    assert len(yao_agenda.get_intent_dict()) == 0

    # WHEN
    x_df = get_agenda_intent_dataframe(yao_agenda)
    print(x_df)

    # THEN
    partyunit_colums = {
        "owner_id",
        "agenda_importance",
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

    assert set(x_df.columns) == partyunit_colums
