# from src.agenda.examples.example_agendas import agenda_v001_with_large_intent
# from src.agenda.agenda import agendaunit_shop
from src.agenda.report import get_agenda_guyunits_dataframe, get_agenda_intent_dataframe
from src.money.money import GuyMoneyReport


def test_GuyMoneyReport_exists():
    # GIVEN / WHEN
    x_guymoneyreport = GuyMoneyReport()

    # THEN
    assert x_guymoneyreport.tax_total is None
    assert x_guymoneyreport.debtor_rank_num is None
    assert x_guymoneyreport.credor_rank_num is None
    assert x_guymoneyreport.debtor_rank_percent is None
    assert x_guymoneyreport.credor_rank_percent is None
    assert x_guymoneyreport.grant_total is None
    assert x_guymoneyreport.tax_paid_amount is None
    assert x_guymoneyreport.tax_paid_bool is None
    assert x_guymoneyreport.transactions_count is None
    assert x_guymoneyreport.transactions_magnitude is None


def test_GuyMoneyReport_DoesNotChangeInputs():
    # GIVEN
    tax_total = 500
    debtor_rank_num = 45
    credor_rank_num = 33
    debtor_rank_percent = 45
    credor_rank_percent = 33
    grant_total = 366
    tax_paid_amount = 499
    tax_paid_bool = True
    transactions_count = 788
    transactions_magnitude = 788000

    # WHEN
    x_guymoneyreport = GuyMoneyReport(
        tax_total,
        debtor_rank_num,
        credor_rank_num,
        debtor_rank_percent,
        credor_rank_percent,
        grant_total,
        tax_paid_amount,
        tax_paid_bool,
        transactions_count,
        transactions_magnitude,
    )

    # THEN
    assert x_guymoneyreport.tax_total == tax_total
    assert x_guymoneyreport.debtor_rank_num == debtor_rank_num
    assert x_guymoneyreport.credor_rank_num == credor_rank_num
    assert x_guymoneyreport.debtor_rank_percent == debtor_rank_percent
    assert x_guymoneyreport.credor_rank_percent == credor_rank_percent
    assert x_guymoneyreport.grant_total == grant_total
    assert x_guymoneyreport.tax_paid_amount == tax_paid_amount
    assert x_guymoneyreport.tax_paid_bool == tax_paid_bool
    assert x_guymoneyreport.transactions_count == transactions_count
    assert x_guymoneyreport.transactions_magnitude == transactions_magnitude


# during the currency river process
# init RiverCycle with init RiverBlock grants money to credors
# Every RiverCycle after that creates all the riverblocks, dstributes the money
# to the next RiverCycle.
# Money leaves the system by paying taxes
# Stop RiverCycling #1 If all money leaves the system by paying taxes
# Stop RiverCycling #2 if two rivercycles in a row don't pay more taxes AND have the same guys (no new guys added between Cycles)
# Stop RiverCycling #3 if cycles_run = rivercyclinglimit


# def test_get_agenda_guyunits_dataframe_ReturnsCorrectDataFrame():
#     # GIVEN
#     luca_agenda = agendaunit_shop()
#     luca_agenda.set_guy_credor_pool(500)
#     luca_agenda.set_guy_debtor_pool(400)
#     todd_text = "Todd"
#     todd_credor_weight = 66
#     todd_debtor_weight = 77
#     luca_agenda.add_guyunit(todd_text, todd_credor_weight, todd_debtor_weight)
#     sue_text = "Sue"
#     sue_credor_weight = 434
#     sue_debtor_weight = 323
#     luca_agenda.add_guyunit(sue_text, sue_credor_weight, sue_debtor_weight)

#     # WHEN
#     x_df = get_agenda_guyunits_dataframe(luca_agenda)

#     # THEN
#     guyunit_colums = {
#         "guy_id",
#         "credor_weight",
#         "debtor_weight",
#         "_agenda_cred",
#         "_agenda_debt",
#         "_agenda_intent_cred",
#         "_agenda_intent_debt",
#         "_agenda_intent_ratio_cred",
#         "_agenda_intent_ratio_debt",
#         "_credor_operational",
#         "_debtor_operational",
#         "_treasury_due_paid",
#         "_treasury_due_diff",
#         "_output_agenda_meld_order",
#         "_treasury_cred_score",
#         "_treasury_voice_rank",
#         "_treasury_voice_hx_lowest_rank",
#     }
#     print(f"{set(x_df.columns)=}")

#     assert set(x_df.columns) == guyunit_colums
#     assert x_df.shape[0] == 2


# def test_get_agenda_guyunits_dataframe_ReturnsCorrectEmptyDataFrame():
#     # GIVEN
#     luca_agenda = agendaunit_shop()

#     # WHEN
#     x_df = get_agenda_guyunits_dataframe(luca_agenda)

#     # THEN
#     guyunit_colums = {
#         "guy_id",
#         "credor_weight",
#         "debtor_weight",
#         "_agenda_cred",
#         "_agenda_debt",
#         "_agenda_intent_cred",
#         "_agenda_intent_debt",
#         "_agenda_intent_ratio_cred",
#         "_agenda_intent_ratio_debt",
#         "_credor_operational",
#         "_debtor_operational",
#         "_treasury_due_paid",
#         "_treasury_due_diff",
#         "_output_agenda_meld_order",
#         "_treasury_cred_score",
#         "_treasury_voice_rank",
#         "_treasury_voice_hx_lowest_rank",
#     }
#     print(f"{set(x_df.columns)=}")

#     assert set(x_df.columns) == guyunit_colums
#     assert x_df.shape[0] == 0


# def test_get_agenda_intent_dataframe_ReturnsCorrectDataFrame():
#     # GIVEN
#     yao_agenda = agenda_v001_with_large_intent()
#     week_text = "weekdays"
#     week_road = yao_agenda.make_l1_road(week_text)
#     assert len(yao_agenda.get_intent_dict()) == 63

#     # WHEN
#     x_df = get_agenda_intent_dataframe(yao_agenda)
#     print(x_df)

#     # THEN
#     guyunit_colums = {
#         "owner_id",
#         "agenda_importance",
#         "_label",
#         "_parent_road",
#         "_begin",
#         "_close",
#         "_addin",
#         "_denom",
#         "_numor",
#         "_reest",
#     }
#     print(f"{set(x_df.columns)=}")

#     assert set(x_df.columns) == guyunit_colums
#     assert x_df.shape[0] == 63


# def test_get_agenda_intent_dataframe_ReturnsCorrectEmptyDataFrame():
#     # GIVEN
#     yao_agenda = agendaunit_shop("Yao")
#     assert len(yao_agenda.get_intent_dict()) == 0

#     # WHEN
#     x_df = get_agenda_intent_dataframe(yao_agenda)
#     print(x_df)

#     # THEN
#     guyunit_colums = {
#         "owner_id",
#         "agenda_importance",
#         "_label",
#         "_parent_road",
#         "_begin",
#         "_close",
#         "_addin",
#         "_denom",
#         "_numor",
#         "_reest",
#     }
#     print(f"{set(x_df.columns)=}")

#     assert set(x_df.columns) == guyunit_colums
